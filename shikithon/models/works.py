"""Submodel for people.py"""
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .manga import Manga
from .ranobe import Ranobe


class Works(BaseModel):
    """Represents works entity of person."""
    anime: Optional[AnimeInfo]
    manga: Optional[Union[Manga, Ranobe]]
    role: str
