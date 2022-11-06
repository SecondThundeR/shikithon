"""Model for /api/users/:id/anime_rates | manga_rates"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .anime import Anime
from .manga import Manga
from .user import User


class UserList(BaseModel):
    """Represents user list entity.

    Contains data of watched/read titles.
    """
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
