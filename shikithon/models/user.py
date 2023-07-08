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


class UserPersonal(UserInfo):
    """Represents user personal info entity."""
    name: Optional[str] = None
    sex: Optional[str] = None
    website: str
    full_years: Optional[int] = None


class UserBrief(UserPersonal):
    """Represents user brief info entity."""
    birth_on: Optional[datetime] = None
    locale: Optional[str] = None


class User(UserPersonal):
    """Represents user full info entity."""
    last_online: str
    location: Optional[str] = None
    banned: bool
    about: str
    about_html: str
    common_info: List[str]
    show_comments: bool
    in_friends: Optional[bool] = None
    is_ignored: bool
    stats: Stats
    style_id: int
