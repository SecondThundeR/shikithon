"""Submodel for stats.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import List
from typing import Optional

from pydantic import BaseModel

from .status import Status


class StatusList(BaseModel):
    """Represents status collection of anime/manga."""
    anime: Optional[List[Status]]
    manga: Optional[List[Status]]
