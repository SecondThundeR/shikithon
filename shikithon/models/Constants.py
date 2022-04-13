from pydantic import BaseModel


class AnimeConstants(BaseModel):
    kind: list[str]
    status: list[str]


class MangaConstants(BaseModel):
    kind: list[str]
    status: list[str]


class UserRateConstants(BaseModel):
    status: list[str]


class ClubsConstants(BaseModel):
    join_policy: list[str]
    comment_policy: list[str]
    image_upload_policy: list[str]


class SmileyConstants(BaseModel):
    bbcode: str
    path: str
