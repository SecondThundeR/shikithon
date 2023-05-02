"""Submodel for `stats.py`."""
from typing import List

from pydantic import BaseModel

from .score import Score


class ScoreList(BaseModel):
    """Represents scores collection of anime/manga."""
    anime: List[Score]
    manga: List[Score]
