"""Submodel for favorites.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Optional

from pydantic import BaseModel

class Favorite(BaseModel):
    """Represents favorite entity."""
    id: int
    name: str
    russian: str
    image: str
    url: Optional[str]
