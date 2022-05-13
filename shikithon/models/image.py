"""Submodel for other main models"""
from pydantic import BaseModel


class Image(BaseModel):
    """Represents image links entity."""
    original: str
    preview: str
    x96: str
    x48: str
