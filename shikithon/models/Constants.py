"""Model for /api/constants"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
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


class ClubsConstants(BaseModel):
    """Represents clubs constants."""
    join_policy: List[str]
    comment_policy: List[str]
    image_upload_policy: List[str]


class SmileyConstants(BaseModel):
    """Represents smiley constants."""
    bbcode: str
    path: str
