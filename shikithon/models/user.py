"""Model for `/api/users`"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .stats import Stats
from .user_image import UserImage


class UserInfo(BaseModel):
    """Represents user basic info entity."""
    id: int
    nickname: str
    avatar: str
    image: UserImage
    last_online_at: datetime
    url: str


class UserBrief(UserInfo):
    """Represents user brief info entity."""
    name: Optional[str]
    sex: Optional[str]
    full_years: Optional[int]
    locale: Optional[str]


class User(UserBrief):
    """Represents user full info entity."""
    last_online: str
    website: str
    birth_on: Optional[datetime]
    location: Optional[str]
    banned: bool
    about: str
    about_html: str
    common_info: List[str]
    show_comments: bool
    in_friends: Optional[bool]
    is_ignored: bool
    stats: Stats
    style_id: int
