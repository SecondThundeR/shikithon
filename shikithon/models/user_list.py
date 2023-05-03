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
    text: Optional[str]
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    text_html: str
    rewatches: int
    created_at: datetime
    updated_at: datetime
    user: UserInfo
    anime: Optional[AnimeInfo]
    manga: Optional[Union[MangaInfo, RanobeInfo]]
