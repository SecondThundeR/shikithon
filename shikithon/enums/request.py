"""Enums for types of requests."""
from .enhanced_enum import EnhancedEnum


class RequestType(EnhancedEnum):
    """Contains types of requests."""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
