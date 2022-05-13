"""Enums for /api/comments."""
from enum import Enum


class CommentableType(Enum):
    """Contains constants related for commentable type."""
    TOPIC = 'Topic'
    USER = 'User'
    REVIEW = 'Review'
    ANIME = 'Anime'
    MANGA = 'Manga'
    CHARACTER = 'Character'
    PERSON = 'Person'
