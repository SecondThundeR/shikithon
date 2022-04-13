from typing import List

from pydantic import BaseModel


class AnimeConstants(BaseModel):
    kind: List[str]
    status: List[str]


class MangaConstants(BaseModel):
    kind: List[str]
    status: List[str]


class UserRateConstants(BaseModel):
    status: List[str]


class ClubsConstants(BaseModel):
    join_policy: List[str]
    comment_policy: List[str]
    image_upload_policy: List[str]


class SmileyConstants(BaseModel):
    bbcode: str
    path: str
