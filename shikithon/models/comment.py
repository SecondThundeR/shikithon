"""Submodel for ban.py"""
from datetime import datetime
from typing import Optional

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
    # Seems like is_summary was deleted for sure from Shikimori API
    # This field will be removed from here within a month
    is_summary: Optional[bool]
    is_offtopic: bool
