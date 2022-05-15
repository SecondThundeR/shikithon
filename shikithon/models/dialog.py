"""Model for api/dialogs"""
from pydantic import BaseModel

from shikithon.models.message import Message
from shikithon.models.user import User


class Dialog(BaseModel):
    """Represents dialog entity."""
    target_user: User
    message: Message
