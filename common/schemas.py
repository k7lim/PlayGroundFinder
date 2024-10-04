from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AgeRange(BaseModel):
    min_age: int
    max_age: int

class PlaygroundFeature(BaseModel):
    primary_name: str
    aliases: Optional[str] = None

class PlaygroundImage(BaseModel):
    url: str
    taken_at: datetime
    children_detected: bool
    needs_face_blurring: bool
    estimated_age_range: AgeRange
    features_detected: Optional[List[PlaygroundFeature]] = None

class Playground(BaseModel):
    name: str
    host_location: dict
    features: list
    images: list
    recommended_age_range: dict
    last_updated: datetime
