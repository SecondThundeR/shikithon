"""Submodel for anime.py"""
from typing import Optional

from pydantic import BaseModel


class Studio(BaseModel):
    """Represents studio of anime entity."""
    id: int
    name: str
    filtered_name: str
    real: bool
    image: Optional[str]
