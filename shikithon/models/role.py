"""Model for api/animes/:id/roles"""
from typing import List, Optional

from pydantic import BaseModel

from .character import Character
from .person import Person


class Role(BaseModel):
    """Represents anime role info."""
    roles: List[str]
    roles_russian: List[str]
    character: Optional[Character]
    person: Optional[Person]
