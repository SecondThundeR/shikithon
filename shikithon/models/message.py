"""Model for `/api/messages` and submodel for `dialog.py`."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .linked_topic import LinkedTopic
from .user import UserInfo


class MessageInfo(BaseModel):
    """Represents message info entity."""
    id: int
    kind: str
    read: bool
    body: Optional[str] = None
    html_body: str
    created_at: datetime
    linked_id: int
    linked_type: Optional[str] = None
    linked: Optional[LinkedTopic] = None


class Message(MessageInfo):
    """Represents message entity."""
    from_user: UserInfo = Field(alias='from')
    to_user: UserInfo = Field(alias='to')
