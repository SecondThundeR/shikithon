from datetime import datetime
from typing import Optional
from typing import List

from pydantic import BaseModel

from .Stats import Stats
from .UserImage import UserImage


class User(BaseModel):
    id: int
    nickname: str
    avatar: str
    image: UserImage
    last_online_at: datetime
    url: str
    name: Optional[str]
    sex: Optional[str]
    full_years: Optional[int]
    locale: Optional[str]
    last_online: Optional[str]
    website: Optional[str]
    birth_on: Optional[datetime]
    location: Optional[str]
    banned: Optional[bool]
    about: Optional[str]
    about_html: Optional[str]
    common_info: Optional[List[str]]
    show_comments: Optional[bool]
    in_friends: Optional[bool]
    is_ignored: Optional[str]
    stats: Optional[Stats]
    style_id: Optional[int]
