"""Submodel for favourites.py"""
from typing import Optional

from pydantic import BaseModel


class Favourite(BaseModel):
    """Represents favourite entity."""
    id: int
    name: str
    russian: str
    image: str
    url: Optional[str]
