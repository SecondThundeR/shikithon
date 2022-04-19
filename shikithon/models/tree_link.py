"""Submodel for franchise_tree.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class TreeLink(BaseModel):
    """Represents tree link entity."""
    id: int
    source_id: int
    target_id: int
    source: int
    target: int
    weight: int
    relation: str
