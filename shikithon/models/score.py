"""Submodel for score_list.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class Score(BaseModel):
    """Represents stats score data."""
    name: str
    value: int
