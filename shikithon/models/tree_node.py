"""Submodel for franchise_tree.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
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
