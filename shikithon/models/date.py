"""Submodel for `people.py`."""
from typing import Optional

from pydantic import BaseModel


class Date(BaseModel):
    """Date object model.

    Used to represent birthday or decease of person
    """
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]
