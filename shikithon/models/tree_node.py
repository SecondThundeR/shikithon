"""Submodel for franchise_tree.py"""
from pydantic import BaseModel


class TreeNode(BaseModel):
    """Represents tree node entity."""
    id: int
    date: int
    name: str
    image_url: str
    url: str
    year: int
    kind: str
    weight: int
