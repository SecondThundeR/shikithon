"""Submodel for `creator.py`."""
from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from .anime import CharacterAnime
from .image import Image
from .manga import CharacterManga
from .ranobe import CharacterRanobe
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
    description: Optional[str] = None
    description_html: str
    description_source: Optional[str] = None
    favoured: bool
    thread_id: Optional[int] = None
    topic_id: Optional[int] = None
    updated_at: datetime
    seyu: List[Seyu]
    animes: List[CharacterAnime]
    mangas: List[Union[CharacterManga, CharacterRanobe]]
