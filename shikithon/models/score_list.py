"""Submodel for stats.py"""
from typing import List
from typing import Optional

from pydantic import BaseModel

from shikithon.models.score import Score


class ScoreList(BaseModel):
    """Represents scores collection of anime/manga."""
    anime: Optional[List[Score]]
    manga: Optional[List[Score]]
