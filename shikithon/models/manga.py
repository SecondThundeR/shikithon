"""Model for /api/mangas"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Optional
from typing import List

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
    aired_on: str
    released_on: Optional[str]
    roles: Optional[List[str]]
    role: Optional[str]
