"""Model for /api/users/:id/favorites"""
from typing import List, Optional

from pydantic import BaseModel

from shikithon.models.favourite import Favourite


class Favourites(BaseModel):
    """Represents collection of favourites by category."""
    animes: List[Optional[Favourite]]
    mangas: List[Optional[Favourite]]
    characters: List[Optional[Favourite]]
    people: List[Optional[Favourite]]
    mangakas: List[Optional[Favourite]]
    seyu: List[Optional[Favourite]]
    producers: List[Optional[Favourite]]
