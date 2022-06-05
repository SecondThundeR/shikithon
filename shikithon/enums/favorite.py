"""Enums for /api/favorites."""
from enum import Enum


class FavoriteLinkedType(Enum):
    """Contains constants related for favorite linked type."""
    ANIME = 'Anime'
    MANGA = 'Manga'
    RANOBE = 'Ranobe'
    PERSON = 'Person'
    CHARACTER = 'Character'
