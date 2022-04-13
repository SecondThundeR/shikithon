from typing import Optional
from typing import List

from pydantic import BaseModel

from .Character import Character
from .Person import Person


class Creator(BaseModel):
    roles: List[str]
    roles_russian: List[str]
    character: Optional[Character]
    person: Optional[Person]
