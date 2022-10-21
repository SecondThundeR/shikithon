"""Enums for /api/users/:id/messages"""
from .enhanced_enum import EnhancedEnum


class MessageType(EnhancedEnum):
    """Contains constants related for message type."""
    INBOX = 'inbox'
    PRIVATE = 'private'
    SENT = 'sent'
    NEWS = 'news'
    NOTIFICATIONS = 'notifications'
