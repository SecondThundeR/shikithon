"""Enums for /api/styles."""
from enum import Enum


class OwnerType(Enum):
    """Contains constants related for style owner type."""
    USER = 'User'
    CLUB = 'Club'
