"""Submodel for `topic.py`."""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .manga import MangaInfo
from .ranobe import RanobeInfo
from .user import UserInfo


class Critique(BaseModel):
    """Represents critique entity.

    Can be found in topics with type
    `Topics::EntryTopics::CritiqueTopic`
    """
    id: int
    target: Optional[Union[AnimeInfo, MangaInfo, RanobeInfo]] = None
    user: UserInfo
    votes_count: int
    votes_for: int
    body: str
    html_body: str
    overall: Optional[int] = None
    storyline: Optional[int] = None
    music: Optional[int] = None
    characters: Optional[int] = None
    animation: Optional[int] = None
    created_at: datetime
