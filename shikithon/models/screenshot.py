"""Submodel for anime.py"""
from pydantic import BaseModel


class Screenshot(BaseModel):
    """Represents screenshot links entity."""
    original: str
    preview: str
