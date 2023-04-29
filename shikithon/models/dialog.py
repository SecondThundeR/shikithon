"""Model for api/dialogs"""
from pydantic import BaseModel

from .message import Message
from .user import UserInfo


class Dialog(BaseModel):
    """Represents dialog entity."""
    target_user: UserInfo
    message: Message
