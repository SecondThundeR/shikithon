"""Model for `/api/animes|mangas|ranobe/:id/related`."""
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .manga import MangaInfo
from .ranobe import RanobeInfo


class Relation(BaseModel):
    """Represents relation entity."""
    relation: str
    relation_russian: str
    anime: Optional[AnimeInfo] = None
    manga: Optional[Union[MangaInfo, RanobeInfo]] = None
