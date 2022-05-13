"""Model for /api/users/:id/history"""
from datetime import datetime
from typing import Union

from pydantic import BaseModel

from shikithon.models.anime import Anime
from shikithon.models.manga import Manga


class History(BaseModel):
    """Represents user history timeline entity."""
    id: int
    created_at: datetime
    description: str
    target: Union[Anime, Manga]