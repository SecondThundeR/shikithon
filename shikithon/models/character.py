"""Submodel for creator.py"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .anime import Anime
from .image import Image
from .manga import Manga
from .seyu import Seyu


class Character(BaseModel):
    """Represents character of anime."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
    altname: Optional[str]
    japanese: Optional[str]
    description: Optional[str]
    description_html: Optional[str]
    description_source: Optional[str]
    favoured: Optional[bool]
    thread_id: Optional[int]
    topic_id: Optional[int]
    updated_at: Optional[datetime]
    seyu: Optional[List[Seyu]]
    animes: Optional[List[Anime]]
    mangas: Optional[List[Manga]]
