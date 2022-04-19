"""Model for /api/achievements"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
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
