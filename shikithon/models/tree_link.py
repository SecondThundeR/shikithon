"""Submodel for franchise_tree.py"""
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
