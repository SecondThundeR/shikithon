"""Enums for response status codes."""
from .enhanced_enum import EnhancedEnum


class ResponseCode(EnhancedEnum):
    """Contains response status codes."""
    SUCCESS = 200
    NO_CONTENT = 204
    RETRY_LATER = 429
