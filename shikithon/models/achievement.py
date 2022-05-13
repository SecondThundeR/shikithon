"""Model for /api/achievements"""
from datetime import datetime

from pydantic import BaseModel


class Achievement(BaseModel):
    """Represents user achievement entity."""
    id: int
    neko_id: str
    level: int
    progress: int
    user_id: int
    created_at: datetime
    updated_at: datetime
