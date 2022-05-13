"""Submodel for type_list.py"""
from pydantic import BaseModel


class Type(BaseModel):
    """Represents stats type data."""
    name: str
    value: int
