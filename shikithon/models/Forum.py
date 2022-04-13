from pydantic import BaseModel


class Forum(BaseModel):
    id: int
    position: int
    name: str
    permalink: str
    url: str
