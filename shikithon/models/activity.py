"""Submodel for stats.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import List

from pydantic import BaseModel


class Activity(BaseModel):
    """Represents stats activity data."""
    name: List[int]
    value: int
