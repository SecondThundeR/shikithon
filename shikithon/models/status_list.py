"""Submodel for stats.py"""
from typing import List
from typing import Optional

from pydantic import BaseModel

from shikithon.models.status import Status


class StatusList(BaseModel):
    """Represents status collection of anime/manga."""
    anime: Optional[List[Status]]
    manga: Optional[List[Status]]
