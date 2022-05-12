"""Model for /api/clubs/:id/images"""
from typing import Optional

from pydantic import BaseModel


class ClubImage(BaseModel):
    """Represents club image entity."""
    id: int
    original_url: str
    main_url: str
    preview_url: str
    can_destroy: Optional[bool]
    user_id: int
