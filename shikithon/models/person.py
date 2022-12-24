"""Model for /api/people and submodel for creator.py"""
from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import BaseModel

from .birthday import Birthday
from .image import Image
from .roles import Roles
from .works import Works


class Person(BaseModel):
    """Represents person entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
    japanese: Optional[str]
    job_title: Optional[str]
    birthday: Optional[Birthday]
    website: Optional[str]
    groupped_roles: Optional[List[Tuple[str, int]]]
    roles: Optional[List[Roles]]
    works: Optional[List[Works]]
    thread_id: Optional[int]
    topic_id: Optional[int]
    person_favoured: Optional[bool]
    producer: Optional[bool]
    producer_favoured: Optional[bool]
    mangaka: Optional[bool]
    mangaka_favoured: Optional[bool]
    seyu: Optional[bool]
    seyu_favoured: Optional[bool]
    updated_at: Optional[datetime]
