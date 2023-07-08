"""Model for `/api/users/:id/anime_rates|manga_rates`."""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .manga import MangaInfo
from .ranobe import RanobeInfo
from .user import UserInfo


class UserList(BaseModel):
    """Represents user list entity.

    Contains data of watched/read titles.
    """
    id: int
    score: int
    status: str
    text: Optional[str] = None
    episodes: Optional[int] = None
    chapters: Optional[int] = None
    volumes: Optional[int] = None
    text_html: str
    rewatches: int
    created_at: datetime
    updated_at: datetime
    user: UserInfo
    anime: Optional[AnimeInfo] = None
    manga: Optional[Union[MangaInfo, RanobeInfo]] = None
