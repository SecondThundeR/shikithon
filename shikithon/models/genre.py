"""Submodel for `anime.py`."""
from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    """Represents genre of anime entity."""
    id: int
    name: str
    russian: str
    kind: Optional[str]
