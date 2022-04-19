"""Model for /api/animes/:id/related"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Optional

from pydantic import BaseModel

from .anime import Anime
from .manga import Manga


class Relation(BaseModel):
    """Represents relation entity for anime."""
    relation: str
    relation_russian: str
    anime: Optional[Anime]
    manga: Optional[Manga]
