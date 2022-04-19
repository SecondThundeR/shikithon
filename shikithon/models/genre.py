"""Submodel for anime.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class Genre(BaseModel):
    """Represents genre of anime entity."""
    id: int
    name: str
    russian: str
    kind: str
