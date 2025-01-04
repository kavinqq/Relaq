from datetime import datetime

import pandas as pd

from chatgpt.api import ChatGPTHelper
from felo.scraper import FeloScraper
from googlemap.api import GoogleMapHelper
from outscraper.api import OutscraperHelper
from prompts import BASIC_PROMPT


class Relaq:
    def __init__(self):
        super().__init__()
        
        self.result: list = []
        self.catch_limit = 10
    
    def get_all_shop_data(
        self,
        search_query: str
    ):
        google_map_helper = GoogleMapHelper()
        places = google_map_helper.search_places(query=search_query)
        
        return places
    
    def get_shop_review(
        self,
        shop_name: str
    ):
        outscraper_helper = OutscraperHelper()
        _, data = outscraper_helper.get_map_review(shop_name)
        
        reviews = data.get("留言", [])
        
        result = [
            review.get("評論")
            for review in reviews
        ]
        
        return "\n".join(result)
    
    def get_shop_price_and_service(
        self,
        shop_name: str
    ) -> str:
        felo_scraper = FeloScraper()
        result = felo_scraper.get_shop_info(shop_name)
        
        return result
    
    def get_ai_result(
        self
    ) -> str:        
        all_shop_data = self.get_all_shop_data(search_query="大安區 美甲")
        
        for index, shop_data in enumerate(all_shop_data, start=1):
            if index > self.catch_limit:
                break
            
            shop_basic_info = f"""
                店家名稱: {shop_data.name}
                地址: {shop_data.address}
                評分: {shop_data.rating}
                網站: {shop_data.website}
                店家電話: {shop_data.phone}
                總評論數: {shop_data.user_ratings_total}
            """
                
            shop_review = self.get_shop_review(shop_data.name)        
            price_and_service = self.get_shop_price_and_service(shop_data.name)
        
            chatgpt_helper = ChatGPTHelper()
            ai_result = chatgpt_helper.chat(
                user_input=f"""
                店家基本資訊:{shop_basic_info},
                店家評論:{shop_review},
                店家價格與服務:{price_and_service},
                """,
                system_setting=BASIC_PROMPT,
            )

            self.result.append(
                {
                    "店家資訊": shop_basic_info,
                    "店家評論": shop_review,
                    "店家價格與服務": price_and_service,
                    "AI_summary": ai_result
                }
            )
        
        df = pd.DataFrame(self.result)
        df.to_excel(f"ai_summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx", index=False)
        
        return 
    
relaq = Relaq()
relaq.get_ai_result()
