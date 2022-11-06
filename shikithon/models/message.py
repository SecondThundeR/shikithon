"""Model for /api/messages and submodel for dialog.py"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from .linked_topic import LinkedTopic
from .user import User


class Message(BaseModel):
    """Represents message entity."""
    id: int
    kind: str
    read: bool
    body: str
    html_body: str
    created_at: datetime
    linked_id: int
    linked_type: Optional[str]
    linked: Optional[LinkedTopic]
    from_user: Optional[User] = Field(alias='from')
    to_user: Optional[User] = Field(alias='to')
