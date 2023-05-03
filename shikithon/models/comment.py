"""Submodel for `ban.py` and model for `/api/comments`."""
from datetime import datetime

from pydantic import BaseModel

from .user import UserInfo


class CommentInfo(BaseModel):
    """Represents a comment info entity.

    Used for `ban.py` model
    """
    id: int
    user_id: int
    commentable_id: int
    commentable_type: str
    body: str
    created_at: datetime
    updated_at: datetime
    is_offtopic: bool


class Comment(CommentInfo):
    """Represents a comment entity.

    Used for `/api/comments`
    """
    html_body: str
    can_be_edited: bool
    user: UserInfo
