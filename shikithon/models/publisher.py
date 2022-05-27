"""Model for /api/publishers"""
from pydantic import BaseModel


class Publisher(BaseModel):
    """Represents publisher entity."""
    id: int
    name: str
