from pydantic import BaseModel

class TreeLink(BaseModel):
    id: int
    source_id: int
    target_id: int
    source: int
    target: int
    weight: int
    relation: str
