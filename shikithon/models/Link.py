from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Link(BaseModel):
    id: int
    kind: str
    url: str
    source: str
    entry_id: int
    entry_type: str
    created_at: datetime
    updated_at: datetime
    imported_at: Optional[datetime]
