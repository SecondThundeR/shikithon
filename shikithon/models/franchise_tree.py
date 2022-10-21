"""Model for /api/animes | mangas/:id/franchise"""
from typing import List

from pydantic import BaseModel

from .tree_link import TreeLink
from .tree_node import TreeNode


class FranchiseTree(BaseModel):
    """Represents franchise tree entity."""
    links: List[TreeLink]
    nodes: List[TreeNode]
    current_id: int
