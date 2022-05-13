"""Model for /api/constants"""
from typing import List

from pydantic import BaseModel


class AnimeConstants(BaseModel):
    """Represents anime constants."""
    kind: List[str]
    status: List[str]


class MangaConstants(BaseModel):
    """Represents manga constants."""
    kind: List[str]
    status: List[str]


class UserRateConstants(BaseModel):
    """Represents user rate constants."""
    status: List[str]


class ClubConstants(BaseModel):
    """Represents clubs constants."""
    join_policy: List[str]
    comment_policy: List[str]
    image_upload_policy: List[str]


class SmileyConstants(BaseModel):
    """Represents smiley constants."""
    bbcode: str
    path: str
