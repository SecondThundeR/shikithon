from datetime import datetime
from typing import Optional

from pydantic import BaseModel


from .Anime import Anime
from .Image import Image
from .Manga import Manga
from .Seyu import Seyu


class Character(BaseModel):
    id: int
    name: str
    russian: str
    image: Image
    url: str
    altname: Optional[str]
    japanese: Optional[str]
    description: Optional[str]
    description_html: Optional[str]
    description_source: Optional[None]  # TODO: Change type to correct one
    favoured: Optional[bool]
    thread_id: Optional[int]
    topic_id: Optional[int]
    updated_at: Optional[datetime]
    seyu: Optional[list[Seyu]]
    animes: Optional[list[Anime]]
    mangas: Optional[list[Manga]]
