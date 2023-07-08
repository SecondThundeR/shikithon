"""Submodel for `anime.py`."""
from typing import Literal

from pydantic import BaseModel


class Genre(BaseModel):
    """Represents genre of anime entity."""
    id: int
    name: str
    russian: str
    kind: Literal['genre', 'demographic', 'theme']
    entry_type: Literal['Anime', 'Manga']
