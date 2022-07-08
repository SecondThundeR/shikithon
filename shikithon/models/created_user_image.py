"""Model for /api/user_images"""
from pydantic import BaseModel


class CreatedUserImage(BaseModel):
    """Represents created user image entity."""
    id: int
    preview: str
    url: str
    bbcode: str
