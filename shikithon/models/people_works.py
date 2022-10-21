"""Submodel for people.py"""
from typing import Optional

from pydantic import BaseModel

from .anime import Anime
from .manga import Manga


class PeopleWorks(BaseModel):
    """Represents works entity of person."""
    anime: Optional[Anime]
    manga: Optional[Manga]
    role: str
