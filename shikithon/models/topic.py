"""Model for /api/animes/:id/topics"""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .club import ClubInfo
from .forum import Forum
from .manga import MangaInfo
from .user import UserInfo


class Topic(BaseModel):
    """Represents topic entity."""
    id: int
    topic_title: str
    body: str
    html_body: str
    html_footer: str
    created_at: datetime
    comments_count: int
    forum: Forum
    user: UserInfo
    type: str
    linked_id: int
    linked_type: str
    linked: Optional[Union[AnimeInfo, MangaInfo, ClubInfo]]
    viewed: bool
    last_comment_viewed: Optional[bool]
    event: Optional[str]
    episode: Optional[int]


class TopicUpdate(BaseModel):
    """Represents topic update entity."""
    id: int
    linked: Union[AnimeInfo, MangaInfo]
    event: Optional[str]
    episode: Optional[int]
    created_at: datetime
    url: str
