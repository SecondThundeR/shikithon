"""Enums for response status codes."""
from enum import Enum


class ResponseCode(Enum):
    """Contains response status codes."""
    RETRY_LATER = 429
