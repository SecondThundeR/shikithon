"""Model for `/api/animes/:id/topics`."""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .club import ClubInfo
from .character import CharacterInfo
from .critique import Critique
from .ranobe import RanobeInfo
from .forum import Forum
from .manga import MangaInfo
from .user import UserInfo


class Topic(BaseModel):
    """Represents topic entity.

    `linked` field can represent multiple models,
    based on `linked_type`

    - Anime: Used in `/api/animes/:id/topics` and `/api/topics/`
    - Manga: Used in `/api/mangas/:id/topics` and `/api/topics/`
    - Ranobe: Used in `/api/ranobe/:id/topics` and `/api/topics/`
    - Club: Used in `/api/topics`
    - Character: Used in `/api/topics`
    - Critique: Used in `/api/topics`
    - None: Used `/api/clubs/:id/collections` and `/api/topics/`
    """
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
    linked_id: Optional[int] = None
    linked_type: Optional[str] = None
    linked: Optional[Union[AnimeInfo, MangaInfo, RanobeInfo, ClubInfo,
                           CharacterInfo, Critique]] = None
    viewed: bool
    last_comment_viewed: Optional[bool] = None
    event: Optional[str] = None
    episode: Optional[int] = None


class TopicUpdate(BaseModel):
    """Represents topic update entity."""
    id: int
    linked: Union[AnimeInfo, MangaInfo, RanobeInfo]
    event: Optional[str] = None
    episode: Optional[int] = None
    created_at: datetime
    url: str
