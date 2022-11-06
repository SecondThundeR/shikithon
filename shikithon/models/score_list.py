"""Submodel for stats.py"""
from typing import List, Optional

from pydantic import BaseModel

from .score import Score


class ScoreList(BaseModel):
    """Represents scores collection of anime/manga."""
    anime: Optional[List[Score]]
    manga: Optional[List[Score]]
