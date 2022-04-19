"""Model for /api/animes/:id/external_links"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Link(BaseModel):
    """Represents external link entity."""
    id: Optional[int]
    kind: str
    url: str
    source: str
    entry_id: int
    entry_type: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    imported_at: Optional[datetime]
