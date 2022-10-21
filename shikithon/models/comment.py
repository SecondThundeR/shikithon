"""Submodel for ban.py and model for /api/comments"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .user import User


class Comment(BaseModel):
    """Represents a comment entity."""
    id: int
    user_id: int
    commentable_id: int
    commentable_type: str
    body: str
    html_body: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_offtopic: bool
    is_summary: Optional[bool]
    can_be_edited: Optional[bool]
    user: Optional[User]
