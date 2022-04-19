"""Model for /api/users/:id/unread_messages"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class UnreadMessages(BaseModel):
    """Represents counter entity for unread messages/news/notifications"""
    messages: int
    news: int
    notifications: int
