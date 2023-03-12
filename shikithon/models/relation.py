"""Model for /api/animes|mangas|ranobe/:id/related"""
from typing import Optional, Union

from pydantic import BaseModel

from .anime import Anime
from .manga import Manga
from .ranobe import Ranobe


class Relation(BaseModel):
    """Represents relation entity."""
    relation: str
    relation_russian: str
    anime: Optional[Anime]
    manga: Optional[Union[Manga, Ranobe]]
