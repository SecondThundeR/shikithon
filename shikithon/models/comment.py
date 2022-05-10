"""Submodel for ban.py"""
from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    """Represents a comment entity."""
    id: int
    commentable_id: int
    commentable_type: str
    body: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_offtopic: bool
