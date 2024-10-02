from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Set
from datetime import datetime
from enum import Enum

class HostLocationType(str, Enum):
    PUBLIC_PARK = "public_park"
    SCHOOL = "school"
    SHOPPING_AREA = "shopping_area"
    OTHER = "other"

class PlaygroundFeature(BaseModel):
    primary_name: str
    aliases: Set[str]

class AgeRange(BaseModel):
    min_age: int = Field(..., ge=0, le=18)
    max_age: int = Field(..., ge=0, le=18)

class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class HostLocation(BaseModel):
    name: str
    type: HostLocationType
    address: Address
    location: Location

class PlaygroundImage(BaseModel):
    url: HttpUrl
    taken_at: datetime
    features_detected: List[PlaygroundFeature]
    children_detected: bool
    estimated_age_range: Optional[AgeRange]
    needs_face_blurring: bool

class Playground(BaseModel):
    id: str
    name: str
    host_location: HostLocation
    features: List[PlaygroundFeature]
    images: List[PlaygroundImage]
    recommended_age_range: AgeRange
    last_updated: datetime

class PlaygroundSearchCriteria(BaseModel):
    features: Optional[List[str]]  # Can search by primary name or alias
    location: Optional[Location]
    max_distance_km: Optional[float] = Field(None, ge=0)
    age_range: Optional[AgeRange]

class PlaygroundSearchResult(BaseModel):
    playgrounds: List[Playground]
    total_count: int

# Pre-defined playground features with aliases
COMMON_PLAYGROUND_FEATURES = [
    PlaygroundFeature(primary_name="swing", aliases={"swings", "swingset"}),
    PlaygroundFeature(primary_name="slide", aliases={"slides", "slippery slide"}),
    PlaygroundFeature(primary_name="monkey_bars", aliases={"jungle gym", "climbing bars"}),
    PlaygroundFeature(primary_name="seesaw", aliases={"teeter-totter", "teeterboard"}),
    PlaygroundFeature(primary_name="climbing_frame", aliases={"climbing structure", "play structure"}),
    PlaygroundFeature(primary_name="sandbox", aliases={"sand pit", "sand box"}),
    PlaygroundFeature(primary_name="merry_go_round", aliases={"roundabout", "carousel"}),
    PlaygroundFeature(primary_name="spring_rider", aliases={"rocking horse", "spring rocker"}),
    PlaygroundFeature(primary_name="playhouse", aliases={"play house", "wendy house"}),
    PlaygroundFeature(primary_name="balance_beam", aliases={"balance bar"}),
    PlaygroundFeature(primary_name="tire_swing", aliases={"tyre swing"}),
    PlaygroundFeature(primary_name="zipline", aliases={"flying fox", "zip wire"}),
]