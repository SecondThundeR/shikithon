"""Submodel for `stats.py`."""
from typing import List

from pydantic import BaseModel

from .status import Status


class StatusList(BaseModel):
    """Represents status collection of anime/manga."""
    anime: List[Status]
    manga: List[Status]
