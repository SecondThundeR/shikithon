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
    id: Optional[int]
    owner_id: Optional[int]
    owner_type: Optional[str]
    name: str
    css: str
    compiled_css: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
