"""Model for `/api/user_rates` and `/api/v2/user_rates`."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserRate(BaseModel):
    """Represents user rate entity."""
    id: int
    user_id: Optional[int] = None
    target_id: Optional[int] = None
    target_type: Optional[str] = None
    score: int
    status: str
    text: Optional[str] = None
    episodes: Optional[int] = None
    chapters: Optional[int] = None
    volumes: Optional[int] = None
    text_html: str
    rewatches: int
    created_at: datetime
    updated_at: datetime
