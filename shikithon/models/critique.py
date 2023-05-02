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
    target: Optional[Union[AnimeInfo, MangaInfo, RanobeInfo]]
    user: UserInfo
    votes_count: int
    votes_for: int
    body: str
    html_body: str
    overall: Optional[int]
    storyline: Optional[int]
    music: Optional[int]
    characters: Optional[int]
    animation: Optional[int]
    created_at: datetime
