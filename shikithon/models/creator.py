"""Model for api/animes/roles"""
from typing import List, Optional

from pydantic import BaseModel

from .character import Character
from .person import Person


class Creator(BaseModel):
    """Represents creator of an anime."""
    roles: List[str]
    roles_russian: List[str]
    character: Optional[Character]
    person: Optional[Person]
