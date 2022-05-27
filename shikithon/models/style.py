"""Model for /api/styles"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Style(BaseModel):
    """Represents style entity."""
    id: int
    owner_id: int
    owner_type: str
    name: str
    css: str
    compiled_css: Optional[str]
    created_at: datetime
    updated_at: datetime
