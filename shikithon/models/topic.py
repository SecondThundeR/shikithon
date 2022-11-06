"""Model for /api/animes/:id/topics"""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import Anime
from .club import Club
from .forum import Forum
from .manga import Manga
from .user import User


class Topic(BaseModel):
    """Represents topic entity."""
    id: int
    topic_title: Optional[str]
    body: Optional[str]
    html_body: Optional[str]
    html_footer: Optional[str]
    created_at: datetime
    comments_count: Optional[int]
    forum: Optional[Forum]
    user: Optional[User]
    type: Optional[str]
    linked_id: Optional[int]
    linked_type: Optional[str]
    linked: Optional[Union[Club, Anime, Manga]]
    viewed: Optional[bool]
    last_comment_viewed: Optional[bool]
    event: Optional[str]
    episode: Optional[int]
