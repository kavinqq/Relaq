import re
import logging

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
        query: str
    ) -> list[PlaceDetail]:
        logger.info(f"Google Map API 搜尋地點: {query} 開始")

        places_result = self.client.places(
            query=query,
            language=self.LANGUAGE,
            region=self.REGION
        )

        places = []

        # 處理搜尋結果
        for place in places_result["results"]:
            place_id = place["place_id"]

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

        logger.info(f"Google Map API 搜尋地點: {query} 結束")

        return places

    def convert_shop_name(self, shop_name: str) -> str:
        safe_name = re.sub(r'[/\\:*?"<>|]', '', shop_name)
        safe_name = safe_name.replace(' ', '_')

        return safe_name
