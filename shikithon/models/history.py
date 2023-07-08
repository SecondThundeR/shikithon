"""Model for `/api/users/:id/history`."""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .manga import MangaInfo
from .ranobe import RanobeInfo


class History(BaseModel):
    """Represents user history timeline entity."""
    id: int
    created_at: datetime
    description: str
    target: Optional[Union[AnimeInfo, MangaInfo, RanobeInfo]] = None
