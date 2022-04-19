"""Model for /api/users/:id/favorites"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Optional
from typing import List

from pydantic import BaseModel

from favorite import Favorite


class Favorites(BaseModel):
    """Represents collection of favorites by category."""
    animes: List[Optional[Favorite]]
    mangas: List[Optional[Favorite]]
    characters: List[Optional[Favorite]]
    people: List[Optional[Favorite]]
    mangakas: List[Optional[Favorite]]
    seyu: List[Optional[Favorite]]
    producers: List[Optional[Favorite]]
