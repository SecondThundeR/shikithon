"""Submodel for stats.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import List
from typing import Optional

from pydantic import BaseModel

from .score import Score


class ScoreList(BaseModel):
    """Represents scores collection of anime/manga."""
    anime: Optional[List[Score]]
    manga: Optional[List[Score]]
