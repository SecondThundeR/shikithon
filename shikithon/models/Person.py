from pydantic import BaseModel

from .Image import Image


class Person(BaseModel):
    id: int
    name: str
    russian: str
    image: Image
    url: str
