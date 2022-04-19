"""Model for /api/bans"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
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
