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
    name: Optional[str]
    russian: Optional[str]
    image: Optional[Image]
    url: Optional[str]
    kind: Optional[str]
    score: Optional[float]
    status: Optional[str]
    episodes: Optional[int]
    episodes_aired: Optional[int]
    aired_on: Optional[date]
    released_on: Optional[date]
