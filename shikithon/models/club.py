"""Model for /api/clubs"""
from pydantic import BaseModel

from .logo import Logo


class Club(BaseModel):
    """Represents a club entity."""
    id: int
    name: str
    logo: Logo
    is_censored: bool
    join_policy: str
    comment_policy: str
