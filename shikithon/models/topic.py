"""Model for /api/animes/:id/topics"""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .ranobe import RanobeInfo
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
    viewed: bool
    last_comment_viewed: Optional[bool]
    event: Optional[str]
    episode: Optional[int]


class CollectionTopic(Topic):
    """Represents club collection topic entity.

    Used in /api/clubs/:id/collections
    """
    linked: None


class AnimeTopic(Topic):
    """Represents anime topic entity.

    Used in /api/animes/:id/topics
    """
    linked: Optional[AnimeInfo]


class MangaTopic(Topic):
    """Represents manga topic entity.

    Used in /api/mangas/:id/topics
    """
    linked: Optional[MangaInfo]


class RanobeTopic(Topic):
    """Represents ranobe topic entity.

    Used in /api/ranobe/:id/topics
    """
    linked: Optional[RanobeInfo]


class TopicUpdate(BaseModel):
    """Represents topic update entity."""
    id: int
    linked: Union[AnimeInfo, MangaInfo]
    event: Optional[str]
    episode: Optional[int]
    created_at: datetime
    url: str
