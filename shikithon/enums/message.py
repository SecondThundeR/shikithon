"""Enums for /api/users/:id/messages"""
from enum import Enum


class MessageType(Enum):
    """Contains constants related for message type."""
    INBOX = 'inbox'
    PRIVATE = 'private'
    SENT = 'sent'
    NEWS = 'news'
    NOTIFICATIONS = 'notifications'
