"""Submodel for stats.py"""
from typing import List
from typing import Optional

from pydantic import BaseModel

from shikithon.models.rating import Rating


class RatingList(BaseModel):
    """Represents ratings collection of anime/manga."""
    anime: Optional[List[Rating]]
    manga: Optional[List[Rating]]
