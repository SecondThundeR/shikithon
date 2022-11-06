"""Enums for /api/favorites."""
from .enhanced_enum import EnhancedEnum


class FavoriteLinkedType(EnhancedEnum):
    """Contains constants related for favorite linked type."""
    ANIME = 'Anime'
    MANGA = 'Manga'
    RANOBE = 'Ranobe'
    PERSON = 'Person'
    CHARACTER = 'Character'
