"""Submodel for `people.py`."""
from typing import List

from pydantic import BaseModel

from .anime import AnimeInfo
from .character import CharacterInfo


class Roles(BaseModel):
    """Represents roles entity of person."""
    characters: List[CharacterInfo]
    animes: List[AnimeInfo]
