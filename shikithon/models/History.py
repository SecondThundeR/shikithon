"""Model for /api/users/:id/history"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from datetime import datetime
from typing import Union

from pydantic import BaseModel

from anime import Anime
from manga import Manga


class History(BaseModel):
    """Represents user history timeline entity."""
    id: int
    created_at: datetime
    description: str
    target: Union[Anime, Manga]
