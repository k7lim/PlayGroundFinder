from pydantic import BaseModel
from datetime import datetime

class PlaygroundImage(BaseModel):
    url: str
    taken_at: datetime
    children_detected: bool
    needs_face_blurring: bool
    estimated_age_range: dict

class Playground(BaseModel):
    name: str
    host_location: dict
    features: list
    images: list
    recommended_age_range: dict
    last_updated: datetime
