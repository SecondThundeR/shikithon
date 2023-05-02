"""Model for `/api/users/:id/favorites`."""
from typing import List

from pydantic import BaseModel

from .favourite import Favourite


class Favourites(BaseModel):
    """Represents collection of favourites by category."""
    animes: List[Favourite]
    mangas: List[Favourite]
    ranobe: List[Favourite]
    characters: List[Favourite]
    people: List[Favourite]
    mangakas: List[Favourite]
    seyu: List[Favourite]
    producers: List[Favourite]
