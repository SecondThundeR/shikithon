"""Submodel for `stats.py`."""
from typing import List

from pydantic import BaseModel

from .type import Type


class TypeList(BaseModel):
    """Represents types collection of anime/manga."""
    anime: List[Type]
    manga: List[Type]
