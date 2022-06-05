"""Model for /api/animes/:id/topics"""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from shikithon.models.anime import Anime
from shikithon.models.forum import Forum
from shikithon.models.manga import Manga
from shikithon.models.user import User


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
    linked: Union[Anime, Manga]
    viewed: Optional[bool]
    last_comment_viewed: Optional[bool]
    event: Optional[str]
    episode: Optional[int]
