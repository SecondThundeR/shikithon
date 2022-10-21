"""Enums for /api/users/:id/history"""
from .enhanced_enum import EnhancedEnum


class TargetType(EnhancedEnum):
    """Contains constants related for history target type."""
    ANIME = 'Anime'
    MANGA = 'Manga'
