from pydantic import BaseModel

from .Image import Image


class Seyu(BaseModel):
    id: int
    name: str
    russian: str
    image: Image
    url: str
