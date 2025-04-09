import re
import logging
import time

import googlemaps
from django.conf import settings

from googlemap.models import PlaceDetail


logger = logging.getLogger(__name__)


class GoogleMapHelper:
    LANGUAGE = "zh-TW"
    REGION = "TW"

    def __init__(self):
        super().__init__()
        self.client = googlemaps.Client(key=settings.GOOGLE_MAP_API_KEY)

    def search_places(
        self,
        query: str,
        catch_limit: int = 20  # 預設值改為 20，與外部 CATCH_LIMIT 保持一致
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
                    # place details 只支援 language 參數
                    place_details = self.client.place(
                        place_id=place_id,
                        language=self.LANGUAGE,
                        fields=[
                            "name",
                            "formatted_address",
                            "rating",
                            "website",
                            "formatted_phone_number",
                            "user_ratings_total",
                            "opening_hours",
                        ]
                    )
                    
                    search_result: dict = place_details["result"]
                    phone = search_result.get("formatted_phone_number", "")
                    if phone:
                        phone = phone.replace(" ", "")
                    
                    places.append(
                        PlaceDetail(
                            name=self.convert_shop_name(search_result["name"]),
                            address=search_result["formatted_address"],
                            rating=search_result.get("rating", 0),
                            website=search_result.get("website", ""),
                            user_ratings_total=search_result.get("user_ratings_total", 0),
                            phone=phone,
                            opening_hours=search_result.get("opening_hours", ""),
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
