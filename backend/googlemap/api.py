import sys
sys.path.append(".")

import googlemaps

from config import GOOGLE_MAP_API_KEY
from .models import PlaceDetail


class GoogleMapHelper:
    def __init__(self):        
        super().__init__()
        self.client = googlemaps.Client(key=GOOGLE_MAP_API_KEY)
        
    def search_places(
        self,
        query: str
    ) -> list[PlaceDetail]:
        places_result = self.client.places(query=query)
        
        places = []
        
        # 處理搜尋結果
        for place in places_result["results"]:
            place_id = place["place_id"]
            
            # 取得商家詳細資訊，包括評論
            place_details = self.client.place(
                place_id=place_id,
                fields=[
                    "name",
                    "formatted_address",
                    "rating",
                    "website",
                    "formatted_phone_number",
                    "user_ratings_total",
                    # "opening_hours",
                    # "business_status",
                ]
            )
                        
            places.append(
                PlaceDetail(
                    name=place_details["result"]["name"],
                    address=place_details["result"]["formatted_address"],
                    rating=place_details["result"].get("rating", 0),
                    website=place_details["result"].get("website", ""),
                    user_ratings_total=place.get("user_ratings_total", 0),
                    phone=place_details["result"].get("formatted_phone_number", "")
                )
            )
            
        return places
