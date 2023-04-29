"""Model for /api/animes/:id/topics"""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .club import Club
from .forum import Forum
from .manga import MangaInfo
from .user import User


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
    user: User
    type: str
    linked_id: int
    linked_type: str
    linked: Union[AnimeInfo, MangaInfo, Club]
    viewed: bool
    last_comment_viewed: Optional[bool]
    event: Optional[str]
    episode: Optional[int]
