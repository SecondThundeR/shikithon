"""Model for /api/users/:id/history"""
from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel

from .anime import Anime
from .manga import Manga
from .ranobe import Ranobe


class History(BaseModel):
    """Represents user history timeline entity."""
    id: int
    created_at: datetime
    description: str
    target: Optional[Union[Anime, Manga, Ranobe]]
