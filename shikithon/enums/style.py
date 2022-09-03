"""Enums for /api/styles."""
from shikithon.enums.enhanced_enum import EnhancedEnum


class OwnerType(EnhancedEnum):
    """Contains constants related for style owner type."""
    USER = 'User'
    CLUB = 'Club'
