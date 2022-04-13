from datetime import datetime
from typing import Optional
from typing import List

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
    description_source: Optional[str]
    favoured: Optional[bool]
    thread_id: Optional[int]
    topic_id: Optional[int]
    updated_at: Optional[datetime]
    seyu: Optional[List[Seyu]]
    animes: Optional[List[Anime]]
    mangas: Optional[List[Manga]]
