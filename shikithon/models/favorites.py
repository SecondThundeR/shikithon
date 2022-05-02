"""Model for /api/users/:id/favorites"""
from typing import Optional
from typing import List

from pydantic import BaseModel

from shikithon.models.favorite import Favorite


class Favorites(BaseModel):
    """Represents collection of favorites by category."""
    animes: List[Optional[Favorite]]
    mangas: List[Optional[Favorite]]
    characters: List[Optional[Favorite]]
    people: List[Optional[Favorite]]
    mangakas: List[Optional[Favorite]]
    seyu: List[Optional[Favorite]]
    producers: List[Optional[Favorite]]
