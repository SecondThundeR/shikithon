"""Model for api/animes/roles"""
from typing import List, Optional

from pydantic import BaseModel

from shikithon.models.character import Character
from shikithon.models.person import Person


class Creator(BaseModel):
    """Represents creator of an anime."""
    roles: List[str]
    roles_russian: List[str]
    character: Optional[Character]
    person: Optional[Person]
