"""Submodel for people.py"""
from typing import List, Optional

from pydantic import BaseModel

from .anime import Anime
from .character import Character


class PeopleRoles(BaseModel):
    """Represents roles entity of person."""
    characters: Optional[List[Character]]
    anime: Optional[List[Anime]]
