import re
import logging
import time
import os
import requests
from urllib.parse import urljoin
import uuid

import googlemaps
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from googlemap.models import PlaceDetail


logger = logging.getLogger(__name__)


class GoogleMapHelper:
    LANGUAGE = "zh-TW"
    REGION = "TW"
    MAX_PHOTO_HEIGHT = 800  # 照片最大高度
    MAX_PHOTO_WIDTH = 800   # 照片最大寬度
    PHOTOS_STORAGE_PATH = 'place_photos/'  # 照片儲存路徑

    def __init__(self):
        super().__init__()
        self.client = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

    def download_and_save_photo(self, photo_ref: str, place_name: str) -> str:
        """下載並保存照片，返回相對URL路徑"""
        try:
            # 構建臨時的 Google Places Photo URL
            temp_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={self.MAX_PHOTO_WIDTH}&maxheight={self.MAX_PHOTO_HEIGHT}&photo_reference={photo_ref}&key={settings.GOOGLE_MAP_API_KEY}"
            
            # 下載照片
            response = requests.get(temp_url)
            if response.status_code != 200:
                return None

            # 生成唯一的檔案名
            file_extension = 'jpg'  # Google Places Photos 通常是 JPEG 格式
            filename = f"{place_name}_{uuid.uuid4().hex[:8]}.{file_extension}"
            file_path = os.path.join(self.PHOTOS_STORAGE_PATH, filename)

            # 保存照片
            path = default_storage.save(file_path, ContentFile(response.content))
            
            # 返回相對 URL 路徑
            return default_storage.url(path)
        except Exception as e:
            logger.error(f"下載照片失敗: {str(e)}")
            return None

    def search_places(
        self,
        query: str,
        catch_limit: int = 20,  # 預設值改為 20，與外部 CATCH_LIMIT 保持一致
    ) -> list[PlaceDetail]:
        logger.info(f"Google Map API 搜尋地點: {query} 開始，限制數量: {catch_limit}")

        places = []
        next_page_token = None
        
        while len(places) < catch_limit:
            # 構建請求參數
            request_params = {
                "query": query,
                "language": self.LANGUAGE,
                "region": self.REGION
            }
            
            # 如果有 next_page_token，添加到參數中
            if next_page_token:
                request_params["page_token"] = next_page_token
            
            # 發送請求
            places_result = self.client.places(**request_params)
            
            # 處理搜尋結果
            for place in places_result["results"]:
                if len(places) >= catch_limit:
                    break
                    
                place_id = place["place_id"]
                
                try:
                    # 準備所需的欄位列表
                    fields = [
                        "name",
                        "formatted_address",
                        "rating",
                        "website",
                        "formatted_phone_number",
                        "user_ratings_total",
                        "opening_hours",
                        "photo"
                    ]
                    
                    # 一次性獲取所有需要的資訊
                    place_details = self.client.place(
                        place_id=place_id,
                        language=self.LANGUAGE,
                        fields=fields
                    )
                    
                    search_result: dict = place_details["result"]
                    phone = search_result.get("formatted_phone_number", "")
                    if phone:
                        phone = phone.replace(" ", "")
                    
                    # 處理照片 - 下載並保存到我們的伺服器
                    photos = []
                    photo_references = search_result.get("photos", [])
                    place_name = self.convert_shop_name(search_result["name"])
                    
                    for photo in photo_references:
                        try:
                            photo_ref = photo.get("photo_reference")
                            if photo_ref:
                                permanent_url = self.download_and_save_photo(photo_ref, place_name)
                                if permanent_url:
                                    photos.append(permanent_url)
                        except Exception as e:
                            logger.error(f"獲取照片失敗: {str(e)}")
                            continue
                    
                    places.append(
                        PlaceDetail(
                            name=place_name,
                            address=search_result["formatted_address"],
                            rating=search_result.get("rating", 0),
                            website=search_result.get("website", ""),
                            user_ratings_total=search_result.get("user_ratings_total", 0),
                            phone=phone,
                            opening_hours=search_result.get("opening_hours", ""),
                            photos=photos
                        )
                    )
                except Exception as e:
                    logger.error(f"處理地點 {place_id} 時發生錯誤: {str(e)}")
                    continue
            
            # 檢查是否有下一頁
            next_page_token = places_result.get("next_page_token")
            if not next_page_token:
                break
                
            # 等待一下再請求下一頁（避免 rate limit）
            time.sleep(2)
        
        logger.info(f"Google Map API 搜尋地點: {query} 結束，共找到 {len(places)} 個地點")
        return places

    def convert_shop_name(self, shop_name: str) -> str:
        safe_name = re.sub(r'[/\\:*?"<>|]', '', shop_name)
        safe_name = safe_name.replace(' ', '_')
        return safe_name
