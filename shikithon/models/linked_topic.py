"""Submodel for message.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Optional

from pydantic import BaseModel

from image import Image

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
