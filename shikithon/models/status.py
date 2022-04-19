"""Submodel for status_list.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class Status(BaseModel):
    """Represents stats status data."""
    id: int
    grouped_id: str
    name: str
    size: int
    type: str
