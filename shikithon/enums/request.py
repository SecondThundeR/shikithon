"""Enums for types of requests."""
from enum import Enum


class RequestType(Enum):
    """Contains types of requests."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
