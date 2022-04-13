from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .Stats import Stats


class UserImage(BaseModel):
    x160: str
    x148: str
    x80: str
    x64: str
    x48: str
    x32: str
    x16: str


class User(BaseModel):
    id: int
    nickname: str
    avatar: str
    image: UserImage
    last_online_at: datetime
    url: str
    name: Optional[str]  # TODO: Change type to correct one
    sex: Optional[str]
    full_years: Optional[int]
    locale: Optional[str]
    last_online: Optional[str]
    website: Optional[str]
    birth_on: Optional[str]  # TODO: Change type to correct one
    location: Optional[str]  # TODO: Change type to correct one
    banned: Optional[bool]
    about: Optional[str]
    about_html: Optional[str]
    common_info: Optional[list[str]]
    show_comments: Optional[bool]
    in_friends: Optional[bool]
    is_ignored: Optional[str]
    stats: Optional[Stats]
    style_id: Optional[int]
