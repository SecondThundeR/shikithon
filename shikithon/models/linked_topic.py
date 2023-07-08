"""Submodel for `message.py`."""
from datetime import date
from typing import Optional

from pydantic import BaseModel

from .image import Image


class LinkedTopic(BaseModel):
    """Represents linked topic of message entity."""
    id: int
    topic_url: str
    thread_id: int
    topic_id: int
    type: str
    name: Optional[str] = None
    russian: Optional[str] = None
    image: Optional[Image] = None
    url: Optional[str] = None
    kind: Optional[str] = None
    score: Optional[float] = None
    status: Optional[str] = None
    episodes: Optional[int] = None
    episodes_aired: Optional[int] = None
    aired_on: Optional[date] = None
    released_on: Optional[date] = None
