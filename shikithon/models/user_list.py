"""Model for /api/users/:id/anime_rates | manga_rates"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from shikithon.models.anime import Anime
from shikithon.models.manga import Manga
from shikithon.models.user import User


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
