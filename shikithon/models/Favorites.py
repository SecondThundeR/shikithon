from typing import Optional
from typing import List

from pydantic import BaseModel

from .Favorite import Favorite


class Favorites(BaseModel):
    animes: List[Optional[Favorite]]
    mangas: List[Optional[Favorite]]
    characters: List[Optional[Favorite]]
    people: List[Optional[Favorite]]
    mangakas: List[Optional[Favorite]]
    seyu: List[Optional[Favorite]]
    producers: List[Optional[Favorite]]
