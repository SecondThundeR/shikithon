"""Model for /api/calendar"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .anime import Anime


class CalendarEvent(BaseModel):
    """Represents event entity in events calendar."""
    next_episode: int
    next_episode_at: datetime
    duration: Optional[int]
    anime: Anime
