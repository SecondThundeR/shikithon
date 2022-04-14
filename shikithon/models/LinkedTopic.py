from typing import Optional

from pydantic import BaseModel

from .Image import Image

class LinkedTopic(BaseModel):
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
