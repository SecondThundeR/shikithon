"""Model for `/api/reviews`."""
from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel


class Review(BaseModel):
    """Represents review entity."""
    id: int
    user_id: int
    anime_id: Optional[int] = None
    manga_id: Optional[int] = None
    body: str
    opinion: Union[Literal['positive'], Literal['neutral'], Literal['negative']]
    is_written_before_release: bool
    created_at: datetime
    updated_at: datetime
    comments_count: int
    cached_votes_up: int
    cached_votes_down: int
    changed_at: Optional[datetime] = None
