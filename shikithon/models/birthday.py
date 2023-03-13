"""Submodel for people.py"""
from typing import Optional

from pydantic import BaseModel


class Birthday(BaseModel):
    """Birthday model class.

    Used to represent birthday of person.
    """
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]
