"""Submodel for stats.py"""
from typing import List
from typing import Optional

from pydantic import BaseModel

from shikithon.models.type import Type


class TypeList(BaseModel):
    """Represents types collection of anime/manga."""
    anime: Optional[List[Type]]
    manga: Optional[List[Type]]
