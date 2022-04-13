from pydantic import BaseModel


class UnreadMessages(BaseModel):
    messages: int
    news: int
    notifications: int
