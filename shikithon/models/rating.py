"""Submodel for rating_list.py"""
from pydantic import BaseModel


class Rating(BaseModel):
    """Represents stats rating data."""
    name: str
    value: int
