"""Submodel for anime.py"""
from pydantic import BaseModel


class UserRateScore(BaseModel):
    """Represents user rate score entity."""
    name: int
    value: int
