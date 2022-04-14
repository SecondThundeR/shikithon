from pydantic import BaseModel

class TreeNode(BaseModel):
    id: int
    date: int
    name: str
    image_url: str
    url: str
    year: int
    kind: str
    weight: int
