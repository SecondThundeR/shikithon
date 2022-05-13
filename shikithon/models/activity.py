"""Submodel for stats.py"""
from typing import List

from pydantic import BaseModel


class Activity(BaseModel):
    """Represents stats activity data."""
    name: List[int]
    value: int
