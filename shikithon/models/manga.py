"""Model for /api/mangas"""
from typing import List, Optional

from pydantic import BaseModel

from .image import Image


class Manga(BaseModel):
    """Represents manga entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
    kind: str
    score: float
    status: str
    volumes: int
    chapters: int
    aired_on: Optional[str]
    released_on: Optional[str]
    roles: Optional[List[str]]
    role: Optional[str]
