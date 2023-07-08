"""Submodel for `stats.py`."""
from typing import List, Optional

from pydantic import BaseModel

from .rating import Rating


class RatingList(BaseModel):
    """Represents ratings collection of anime/manga."""
    anime: Optional[List[Rating]] = None
    manga: Optional[List[Rating]] = None
