"""Submodel for stats.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import List
from typing import Optional

from pydantic import BaseModel

from .type import Type


class TypeList(BaseModel):
    """Represents types collection of anime/manga."""
    anime: Optional[List[Type]]
    manga: Optional[List[Type]]
