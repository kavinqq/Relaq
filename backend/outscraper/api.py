import sys
sys.path.append(".")

import time
import requests 

from config import OUTSCRAPER_API_KEY


class OutscraperHelper:
    API_PATH = {
        "MAPS_REVIEWS": "https://api.app.outscraper.com/maps/reviews-v3",
    }
    
    
    def __init__(self):
        super().__init__()
        self.api_key = OUTSCRAPER_API_KEY
        self.reviews_limit = 20
        
    def _get_results_location(
        self,
        shop_name: str
    ) -> tuple[str, str]:
        query_params = {
            "ignoreEmpty": "true",
            "language": "zh-TW",
            "region": "TW",
            "reviewsLimit": self.reviews_limit,
            "query": shop_name,
            "async": "true"
        }
        
        response = requests.get(
            self.API_PATH["MAPS_REVIEWS"],
            params=query_params,
            headers={"X-API-KEY": self.api_key}
        )
        
        if response.ok:
            response_json: dict = response.json()
            
            request_id = response_json.get("id")
            results_location = response_json.get("results_location")
            
            self.wait_for_results(30)
            
            return request_id, results_location
        
    def get_map_review(
        self,
        shop_name:str
    ) -> tuple[bool, dict]:
        _, results_location = self._get_results_location(shop_name)
        is_ok, result = self.get_result(results_location)
        
        return is_ok, result
    
    def wait_for_results(
        self,
        wait_seconds: int,
    ) -> None:
        for sec in range(wait_seconds):
            time.sleep(1)
            print(f"等待 {sec + 1} 秒")
            
        return None

    def get_result(
        self,
        results_location: str
    ) -> tuple[bool, dict]:
        response = requests.get(results_location)
        if response.ok:
            resp_data = response.json().get("data")
            
            shop_data = resp_data[0]
            shop_name = shop_data.get("name")
            full_address = shop_data.get("full_address")
            rating = shop_data.get("rating")
            reviews = shop_data.get("reviews")
            
            reviews_data: list[dict] = shop_data.get("reviews_data")                                       
            reviews_data = [
                {
                    "評論者": review.get("author_title"),
                    "評論日期": review.get("review_datetime_utc"),
                    "評分": review.get("review_rating"),
                    "評論": review.get("review_text")
                }
                for review in reviews_data
            ]
                     
            result = {
                "商家名稱": shop_name,
                "地址": full_address,
                "評分": rating,
                "評論數": reviews,
                "留言": reviews_data
            }
            
            return True, result
        else:
            return False, None
