"""Submodel for stats.py"""
from typing import List, Optional

from pydantic import BaseModel

from .type import Type


class TypeList(BaseModel):
    """Represents types collection of anime/manga."""
    anime: Optional[List[Type]]
    manga: Optional[List[Type]]
