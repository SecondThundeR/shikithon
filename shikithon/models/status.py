"""Submodel for status_list.py"""
from pydantic import BaseModel


class Status(BaseModel):
    """Represents stats status data."""
    id: int
    grouped_id: str
    name: str
    size: int
    type: str
