from datetime import datetime
from typing import Union
from typing import Optional

from pydantic import BaseModel

from .Anime import Anime
from .Forum import Forum
from .Image import Image
from .Manga import Manga
from .User import User


class Topic(BaseModel):
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


class LinkedTopic(BaseModel):
    id: int
    topic_url: str
    thread_id: int
    topic_id: int
    type: str
    name: str
    russian: str
    image: Image
    url: str
    kind: str
    score: float
    status: str
    episodes: int
    episodes_aired: int
    aired_on: str
    released_on: Optional[str]
