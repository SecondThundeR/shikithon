"""Model for api/forums"""
from pydantic import BaseModel


class Forum(BaseModel):
    """Represents forum entity."""
    id: int
    position: int
    name: str
    permalink: str
    url: str
