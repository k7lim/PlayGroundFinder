from pydantic import Field, HttpUrl
from typing import List, Optional, Set
from datetime import datetime
from enum import Enum as PyEnum
from base_model import OrmBaseModel

class HostLocationType(str, PyEnum):
    PUBLIC_PARK = "public_park"
    SCHOOL = "school"
    SHOPPING_AREA = "shopping_area"
    OTHER = "other"

class PlaygroundFeature(OrmBaseModel):
    id: Optional[int] = None
    primary_name: str
    aliases: Set[str]

class AgeRange(OrmBaseModel):
    id: Optional[int] = None
    min_age: int = Field(..., ge=0, le=18)
    max_age: int = Field(..., ge=0, le=18)

class Location(OrmBaseModel):
    id: Optional[int] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class Address(OrmBaseModel):
    id: Optional[int] = None
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class HostLocation(OrmBaseModel):
    id: Optional[int] = None
    name: str
    type: HostLocationType
    address: Address
    location: Location

class PlaygroundImage(OrmBaseModel):
    id: Optional[int] = None
    url: HttpUrl
    taken_at: datetime
    features_detected: List[PlaygroundFeature]
    children_detected: bool
    estimated_age_range: Optional[AgeRange]
    needs_face_blurring: bool

class Playground(OrmBaseModel):
    id: Optional[int] = None
    name: str
    host_location: HostLocation
    features: List[PlaygroundFeature]
    images: List[PlaygroundImage]
    recommended_age_range: AgeRange
    last_updated: datetime
