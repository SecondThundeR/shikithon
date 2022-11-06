"""Enums for /api/styles."""
from .enhanced_enum import EnhancedEnum


class OwnerType(EnhancedEnum):
    """Contains constants related for style owner type."""
    USER = 'User'
    CLUB = 'Club'
