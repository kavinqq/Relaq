from dataclasses import dataclass, field


@dataclass
class PlaceDetail:
    name: str
    address: str
    rating: float
    website: str
    phone: str
    user_ratings_total: int
    opening_hours: dict
    photos: list[str] = field(default_factory=list)

@dataclass
class Place:
    result: PlaceDetail
