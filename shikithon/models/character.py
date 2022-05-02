"""Submodel for creator.py"""
from datetime import datetime
from typing import Optional
from typing import List

from pydantic import BaseModel

from shikithon.models.anime import Anime
from shikithon.models.image import Image
from shikithon.models.manga import Manga
from shikithon.models.seyu import Seyu


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
