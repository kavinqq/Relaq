import time

from cms.models import Shop, ShopTag
from chatgpt.services import ChatGPTHelper
from chatgpt.constants import SUMMARY_PROMPT, TAG_PROMPT
from felo.scraper import FeloScraper
from googlemap.services import GoogleMapHelper
from googlemap.models import PlaceDetail
from outscrapers.services import OutscraperHelper


class CoreService:
    def __init__(self, catch_limit: int = 10):
        super().__init__()

        self.result: list = []
        self.catch_limit = catch_limit
        self.search_keyword = "美甲"

    def _get_all_shop_data(
        self,
        search_query: str
    ):
        google_map_helper = GoogleMapHelper()
        places = google_map_helper.search_places(query=search_query)

        return places

    def _get_shop_review(
        self,
        shop_name: str
    ):
        outscraper_helper = OutscraperHelper()
        _, data = outscraper_helper.get_map_review(shop_name)

        reviews: list[dict] = data.get("留言", [])
        result: list[str] = [review.get("評論") for review in reviews]

        return "\n".join(result)

    def _get_shop_price_and_service(
        self,
        shop_name: str
    ) -> str:
        felo_scraper = FeloScraper()
        result = felo_scraper.get_shop_info(shop_name)

        return result
    
    def _gen_shop_basic_info(
        self,
        shop_data: PlaceDetail
    ) -> str:
        return f"""
            店家名稱: {shop_data.name}
            地址: {shop_data.address}
            評分: {shop_data.rating}
            網站: {shop_data.website}
            店家電話: {shop_data.phone}
            總評論數: {shop_data.user_ratings_total}
        """
    
    def main(
        self,
        search_region: str
    ) -> None:
        start_time = time.time()
        print(f"[Core] 開始抓取 {search_region} 的店家資訊")
        
        search_query = f"{search_region} {self.search_keyword}"
        all_shop_data = self._get_all_shop_data(search_query=search_query)
        total_progress = len(all_shop_data)
        print(f"[Core] 共找到 {total_progress} 家店家")
        if total_progress <= 0:
            print(f"[Core] 找不到任何店家資訊")
            return None

        chatgpt_helper = ChatGPTHelper()        
        for index, shop_data in enumerate(all_shop_data, start=1):
            if index > self.catch_limit:
                break
            
            shop_basic_info = self._gen_shop_basic_info(shop_data)
            shop_review = self._get_shop_review(shop_data.name)
            price_and_service = self._get_shop_price_and_service(shop_data.name)
            
            ai_summary = chatgpt_helper.chat(
                user_input=f"""
                店家基本資訊:{shop_basic_info},
                店家評論:{shop_review},
                店家價格與服務:{price_and_service},
                """,
                system_setting=SUMMARY_PROMPT,
            )
            
            ai_tag = chatgpt_helper.chat(
                user_input=f"""
                店家基本資訊:{shop_basic_info},
                店家評論:{shop_review},
                店家價格與服務:{price_and_service},
                """,
                system_setting=TAG_PROMPT,
            )
            
            # 解析並儲存標籤
            tags = chatgpt_helper.convert_tag_response(ai_tag)
            shop_tags = []
            for tag_data in tags:
                tag, _ = ShopTag.objects.get_or_create(
                    name=tag_data['name'],
                    type=tag_data['type'],
                    defaults={
                        'emoji': tag_data['emoji'],
                        'description': tag_data['description']
                    }
                )
                shop_tags.append(tag)
            
            # 創建店家資料
            shop = Shop.objects.create(
                name=shop_data.name,
                address=shop_data.address,
                phone=shop_data.phone,
                website=shop_data.website,
                rating=shop_data.rating,
                review_count=shop_data.user_ratings_total,
                reviews=shop_review,
                price_and_service=price_and_service,
                ai_summary=ai_summary,
            )
            shop.tags.set(shop_tags)  # 設置標籤關聯
            
            print(f"\033[92m 店家資訊: {shop.name} 抓取成功! 進度: {index}/{total_progress} \033[0m")

        end_time = time.time()
        print(f"[Core] 抓取 {search_query} 的店家資訊完成, 共花費 {end_time - start_time} 秒")

        return None
