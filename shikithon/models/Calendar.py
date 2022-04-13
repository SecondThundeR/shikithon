from datetime import datetime
from typing import Optional

from pydantic import BaseModel


from .Anime import Anime


class Calendar(BaseModel):
    next_episode: int
    next_episode_at: datetime
    duration: Optional[int]
    anime: Anime
