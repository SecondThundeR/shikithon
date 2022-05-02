"""Model for /api/users"""
from datetime import datetime
from typing import Optional
from typing import List

from pydantic import BaseModel

from shikithon.models.stats import Stats
from shikithon.models.user_image import UserImage


class User(BaseModel):
    """Represents user entity."""
    id: int
    nickname: str
    avatar: str
    image: UserImage
    last_online_at: datetime
    url: Optional[str]
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
