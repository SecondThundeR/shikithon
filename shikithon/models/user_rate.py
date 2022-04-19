"""Model for /api/v2/user_rates"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserRate(BaseModel):
    """Represents user rate entity."""
    id: int
    user_id: Optional[int]
    target_id: Optional[int]
    target_type: Optional[str]
    score: int
    status: str
    text: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    text_html: str
    rewatches: int
    created_at: datetime
    updated_at: datetime
