from datetime import datetime
from typing import Union

from pydantic import BaseModel

from .Anime import Anime
from .Manga import Manga


class History(BaseModel):
    id: int
    created_at: datetime
    description: str
    target: Union[Anime, Manga]
