"""Submodel for stats.py"""
from typing import List, Optional

from pydantic import BaseModel

from .status import Status


class StatusList(BaseModel):
    """Represents status collection of anime/manga."""
    anime: Optional[List[Status]]
    manga: Optional[List[Status]]
