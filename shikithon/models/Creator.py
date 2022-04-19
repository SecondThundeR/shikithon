"""Model for api/animes/roles"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Optional
from typing import List

from pydantic import BaseModel

from .character import Character
from .person import Person


class Creator(BaseModel):
    """Represents creator of an anime."""
    roles: List[str]
    roles_russian: List[str]
    character: Optional[Character]
    person: Optional[Person]
