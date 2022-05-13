"""Submodel for score_list.py"""
from pydantic import BaseModel


class Score(BaseModel):
    """Represents stats score data."""
    name: str
    value: int
