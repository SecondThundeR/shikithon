"""Submodel for anime.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class UserRateStatus(BaseModel):
    """Represents user rate status entity."""
    name: str
    value: int
