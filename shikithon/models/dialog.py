"""Model for api/dialogs"""
from pydantic import BaseModel

from .message import Message
from .user import User


class Dialog(BaseModel):
    """Represents dialog entity."""
    target_user: User
    message: Message
