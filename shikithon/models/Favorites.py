from typing import Optional
from typing import List

from pydantic import BaseModel


class FavoriteData(BaseModel):
    id: int
    name: str
    russian: str
    image: str
    url: Optional[str]


class Favorites(BaseModel):
    animes: List[Optional[FavoriteData]]
    mangas: List[Optional[FavoriteData]]
    characters: List[Optional[FavoriteData]]
    people: List[Optional[FavoriteData]]
    mangakas: List[Optional[FavoriteData]]
    seyu: List[Optional[FavoriteData]]
    producers: List[Optional[FavoriteData]]
