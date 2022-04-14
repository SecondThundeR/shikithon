from typing import List

from pydantic import BaseModel

from .TreeLink import TreeLink
from .TreeNode import TreeNode


class FranchiseTree(BaseModel):
    links: List[TreeLink]
    nodes: List[TreeNode]
    current_id: int
