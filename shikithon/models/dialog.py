"""Model for `/api/dialogs`."""
from pydantic import BaseModel

from .message import MessageInfo
from .user import UserInfo


class Dialog(BaseModel):
    """Represents dialog entity."""
    target_user: UserInfo
    message: MessageInfo
