"""Submodel for people.py"""
from typing import Optional

from pydantic import BaseModel

from shikithon.models.anime import Anime
from shikithon.models.manga import Manga


class PeopleWorks(BaseModel):
    """Represents works entity of person."""
    anime: Optional[Anime]
    manga: Optional[Manga]
    role: str
