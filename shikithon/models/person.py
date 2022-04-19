"""Submodel for creator.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel

from .image import Image


class Person(BaseModel):
    """Represents person entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
