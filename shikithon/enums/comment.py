"""Enums for `/api/comments`."""
from .enhanced_enum import EnhancedEnum


class CommentableType(EnhancedEnum):
    """Contains constants related for commentable type
    of fetched comment."""
    TOPIC = 'Topic'
    USER = 'User'


class CommentableCreateType(EnhancedEnum):
    """Contains constants related for commentable type
    of created comment."""
    TOPIC = 'Topic'
    USER = 'User'
    ANIME = 'Anime'
    MANGA = 'Manga'
    CHARACTER = 'Character'
    PERSON = 'Person'
    ARTICLE = 'Article'
    CLUB = 'Club'
    CLUB_PAGE = 'ClubPage'
    COLLECTION = 'Collection'
    CRITIQUE = 'Critique'
    REVIEW = 'Review'
