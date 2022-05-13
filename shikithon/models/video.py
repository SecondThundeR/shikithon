"""Model for /api/videos"""
from pydantic import BaseModel


class Video(BaseModel):
    """Represents a video entity."""
    id: int
    url: str
    image_url: str
    player_url: str
    name: str
    kind: str
    hosting: str
