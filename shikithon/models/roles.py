"""Submodel for people.py"""
from typing import List

from pydantic import BaseModel

from .anime import Anime
from .character import Character


class Roles(BaseModel):
    """Represents roles entity of person."""
    characters: List[Character]
    animes: List[Anime]
