from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .Anime import Anime
from .Manga import Manga
from .User import User


class UserList(BaseModel):
    id: int
    score: int
    status: str
    text: Optional[str]
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    text_html: str
    rewatches: int
    created_at: datetime
    updated_at: datetime
    user: Optional[User]
    anime: Optional[Anime]
    manga: Optional[Manga]
