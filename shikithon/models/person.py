"""Model for `/api/people` and submodel for `creator.py`."""
from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import BaseModel

from .date import Date
from .image import Image
from .roles import Roles
from .works import Works


class PersonInfo(BaseModel):
    """Represents person info entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str


class Person(PersonInfo):
    """Represents person entity."""
    japanese: str
    job_title: str
    birth_on: Date
    deceased_on: Date
    website: str
    groupped_roles: List[Tuple[str, int]]
    roles: List[Roles]
    works: List[Works]
    topic_id: Optional[int] = None
    person_favoured: bool
    producer: bool
    producer_favoured: bool
    mangaka: bool
    mangaka_favoured: bool
    seyu: bool
    seyu_favoured: bool
    updated_at: datetime
    thread_id: Optional[int] = None
    # ? Seems like it's gonna be removed soon
    # because of birth_on and deceased_on fields
    birthday: Date
