"""Submodel for anime.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class UserRateScore(BaseModel):
    """Represents user rate score entity."""
    name: int
    value: int
