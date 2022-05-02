"""Submodel for message.py"""
from typing import Optional

from pydantic import BaseModel

from shikithon.models.image import Image


class LinkedTopic(BaseModel):
    """Represents linked topic of message entity."""
    id: int
    topic_url: str
    thread_id: int
    topic_id: int
    type: str
    name: str
    russian: str
    image: Image
    url: str
    kind: str
    score: float
    status: str
    episodes: int
    episodes_aired: int
    aired_on: str
    released_on: Optional[str]
