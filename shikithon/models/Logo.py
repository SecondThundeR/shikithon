"""Submodel for club.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class Logo(BaseModel):
    """Represents club logo links entity."""
    original: str
    main: str
    x96: str
    x73: str
    x48: str
