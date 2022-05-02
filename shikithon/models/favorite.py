"""Submodel for favorites.py"""
from typing import Optional

from pydantic import BaseModel


class Favorite(BaseModel):
    """Represents favorite entity."""
    id: int
    name: str
    russian: str
    image: str
    url: Optional[str]
