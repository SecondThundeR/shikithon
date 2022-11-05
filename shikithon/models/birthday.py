"""Submodel for people.py"""
from pydantic import BaseModel


class Birthday(BaseModel):
    """Birthday model class.

    Used to represent birthday of person.
    """

    day: int
    month: int
    year: int
