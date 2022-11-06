"""Enums for /api/comments."""
from .enhanced_enum import EnhancedEnum


class CommentableType(EnhancedEnum):
    """Contains constants related for commentable type."""
    TOPIC = 'Topic'
    USER = 'User'
    REVIEW = 'Review'
    ANIME = 'Anime'
    MANGA = 'Manga'
    CHARACTER = 'Character'
    PERSON = 'Person'
