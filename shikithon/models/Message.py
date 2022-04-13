from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from .Topic import LinkedTopic
from .User import User


class Message(BaseModel):
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
    to_user: Optional[User] = Field(alias="to")
