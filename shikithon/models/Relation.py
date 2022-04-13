from typing import Optional

from pydantic import BaseModel

from .Anime import Anime


class Relation(BaseModel):
    relation: str
    relation_russian: str
    anime: Optional[Anime]
    manga: Optional[str]
