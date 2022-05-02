"""Submodel for anime.py"""
from pydantic import BaseModel


class UserRateStatus(BaseModel):
    """Represents user rate status entity."""
    name: str
    value: int
