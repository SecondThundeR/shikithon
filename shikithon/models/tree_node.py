"""Submodel for `franchise_tree.py`."""
from typing import Optional

from pydantic import BaseModel


class TreeNode(BaseModel):
    """Represents tree node entity."""
    id: int
    date: int
    name: str
    image_url: str
    url: str
    year: Optional[int] = None
    kind: Optional[str] = None
    weight: int
