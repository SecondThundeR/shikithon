"""Model for /api/videos"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
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
