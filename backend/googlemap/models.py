from dataclasses import dataclass


@dataclass
class PlaceDetail:
    name: str
    address: str
    rating: float
    website: str
    phone: str
    user_ratings_total: int

@dataclass
class Place:
    result: PlaceDetail
