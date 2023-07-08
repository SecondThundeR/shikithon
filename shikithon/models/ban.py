"""Model for `/api/bans`."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .comment import CommentInfo
from .user import UserInfo


class Ban(BaseModel):
    """Represents ban entity."""
    id: int
    user_id: int
    comment: Optional[CommentInfo] = None
    moderator_id: int
    reason: str
    created_at: datetime
    duration_minutes: int
    user: UserInfo
    moderator: UserInfo
