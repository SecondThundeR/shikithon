from pydantic import BaseModel


class Genre(BaseModel):
    id: int
    name: str
    russian: str
    kind: str
