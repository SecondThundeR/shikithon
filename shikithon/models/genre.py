"""Submodel for anime.py"""
from pydantic import BaseModel


class Genre(BaseModel):
    """Represents genre of anime entity."""
    id: int
    name: str
    russian: str
    kind: str
