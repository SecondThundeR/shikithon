from datetime import datetime
from typing import Union
from typing import Optional

from pydantic import BaseModel

from .Anime import Anime
from .Forum import Forum
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
