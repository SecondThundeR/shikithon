"""Model for /api/animes/:id/topics"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from datetime import datetime
from typing import Union
from typing import Optional

from pydantic import BaseModel

from .anime import Anime
from .forum import Forum
from .manga import Manga
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
    linked: Union[Anime, Manga]
    viewed: bool
    last_comment_viewed: Optional[bool]
    event: Optional[str]
    episode: Optional[int]
