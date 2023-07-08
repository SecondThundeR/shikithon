"""Model for `/api/animes|mangas|ranobe/:id/roles`."""
from typing import List, Optional

from pydantic import BaseModel

from .character import CharacterInfo
from .person import PersonInfo


class Role(BaseModel):
    """Represents role info entity."""
    roles: List[str]
    roles_russian: List[str]
    character: Optional[CharacterInfo] = None
    person: Optional[PersonInfo] = None
