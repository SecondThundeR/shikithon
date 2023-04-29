"""Submodel for creator.py"""
from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

from .anime import CharacterAnime
from .image import Image
from .manga import Manga
from .ranobe import Ranobe
from .seyu import Seyu


class CharacterInfo(BaseModel):
    """Represents character info entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str


class Character(CharacterInfo):
    """Represents character entity."""
    altname: str
    japanese: str
    description: str
    description_html: str
    description_source: str
    favoured: bool
    thread_id: int
    topic_id: int
    updated_at: datetime
    seyu: List[Seyu]
    animes: List[CharacterAnime]
    mangas: List[Union[Manga, Ranobe]]
