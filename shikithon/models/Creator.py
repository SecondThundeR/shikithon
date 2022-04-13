from typing import Optional

from pydantic import BaseModel

from .Character import Character
from .Person import Person


class Creator(BaseModel):
    roles: list[str]
    roles_russian: list[str]
    character: Optional[Character]
    person: Optional[Person]
