from pydantic import BaseModel


class TreeLink(BaseModel):
    id: int
    source_id: int
    target_id: int
    source: int
    target: int
    weight: int
    relation: str


class TreeNode(BaseModel):
    id: int
    date: int
    name: str
    image_url: str
    url: str
    year: int
    kind: str
    weight: int


class FranchiseTree(BaseModel):
    links: list[TreeLink]
    nodes: list[TreeNode]
    current_id: int
