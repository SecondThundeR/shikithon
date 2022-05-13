"""Model for /api/users/:id/unread_messages"""
from pydantic import BaseModel


class UnreadMessages(BaseModel):
    """Represents counter entity for unread messages/news/notifications"""
    messages: int
    news: int
    notifications: int
