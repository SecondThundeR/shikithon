"""Enums for response status codes."""
from enum import Enum


class ResponseCode(Enum):
    """Contains response status codes."""
    SUCCESS = 200
    NO_CONTENT = 204
    RETRY_LATER = 429
