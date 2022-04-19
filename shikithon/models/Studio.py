"""Submodel for anime.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Optional

from pydantic import BaseModel


class Studio(BaseModel):
    """Represents studio of anime entity."""
    id: int
    name: str
    filtered_name: str
    real: bool
    image: Optional[str]
