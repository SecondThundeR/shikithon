"""Submodel for other main models"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class Image(BaseModel):
    """Represents image links entity."""
    original: str
    preview: str
    x96: str
    x48: str
