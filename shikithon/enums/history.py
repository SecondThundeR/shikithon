"""Enums for /api/users/:id/history"""
from enum import Enum


class TargetType(Enum):
    """Contains constants related for history target type."""
    ANIME = 'Anime'
    MANGA = 'Manga'
