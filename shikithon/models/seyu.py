"""Submodel for character.py"""
from pydantic import BaseModel

from .image import Image


class Seyu(BaseModel):
    """Represents seyu of character entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
