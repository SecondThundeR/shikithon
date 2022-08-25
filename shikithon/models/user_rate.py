"""Model for /api/user_rates and /api/v2/user_rates"""
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
    text: Optional[str]
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    text_html: str
    rewatches: int
    created_at: datetime
    updated_at: datetime
