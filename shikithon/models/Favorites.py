from typing import Optional

from pydantic import BaseModel


class FavoriteData(BaseModel):
    id: int
    name: str
    russian: str
    image: str
    url: Optional[str]


class Favorites(BaseModel):
    animes: list[Optional[FavoriteData]]
    mangas: list[Optional[FavoriteData]]
    characters: list[Optional[FavoriteData]]
    people: list[Optional[FavoriteData]]
    mangakas: list[Optional[FavoriteData]]
    seyu: list[Optional[FavoriteData]]
    producers: list[Optional[FavoriteData]]
