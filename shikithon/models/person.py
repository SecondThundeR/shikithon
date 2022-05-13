"""Submodel for creator.py"""
from pydantic import BaseModel

from shikithon.models.image import Image


class Person(BaseModel):
    """Represents person entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
