"""Model for /api/animes/:anime_id/videos"""
from typing import Optional

from pydantic import BaseModel


class Video(BaseModel):
    """Represents a video entity."""
    id: int
    url: str
    image_url: str
    player_url: str
    name: Optional[str]
    kind: str
    hosting: str
