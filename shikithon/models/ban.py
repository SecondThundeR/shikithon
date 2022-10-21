"""Model for /api/bans"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .comment import Comment
from .user import User


class Ban(BaseModel):
    """Represents ban entity."""
    id: int
    user_id: int
    comment: Optional[Comment]
    moderator_id: int
    reason: str
    created_at: datetime
    duration_minutes: int
    user: User
    moderator: User
