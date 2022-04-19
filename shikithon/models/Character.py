"""Submodel for creator.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from datetime import datetime
from typing import Optional
from typing import List

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
