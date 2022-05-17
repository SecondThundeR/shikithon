"""Submodel for people.py"""
from typing import List, Optional

from pydantic import BaseModel

from shikithon.models.anime import Anime
from shikithon.models.character import Character


class PeopleRoles(BaseModel):
    """Represents roles entity of person."""
    characters: Optional[List[Character]]
    anime: Optional[List[Anime]]
