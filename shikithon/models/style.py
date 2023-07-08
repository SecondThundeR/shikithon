"""Model for `/api/styles`."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Style(BaseModel):
    """Represents style entity.

    Many fields are optional due to
    `/api/styles/preview` returning non-null
    for 3 fields only
    """
    id: Optional[int] = None
    owner_id: Optional[int] = None
    owner_type: Optional[str] = None
    name: str
    css: str
    compiled_css: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
