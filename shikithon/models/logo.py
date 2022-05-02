"""Submodel for club.py"""
from pydantic import BaseModel


class Logo(BaseModel):
    """Represents club logo links entity."""
    original: str
    main: str
    x96: str
    x73: str
    x48: str
