from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .Comment import Comment
from .User import User


class Ban(BaseModel):
    id: int
    user_id: int
    comment: Optional[Comment]
    moderator_id: int
    reason: str
    created_at: datetime
    duration_minutes: int
    user: User
    moderator: User
