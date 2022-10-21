"""Enums for /api/user_rates."""
from .enhanced_enum import EnhancedEnum


class UserRateType(EnhancedEnum):
    """Contains constants related for getting certain type of user rate."""
    ANIME = 'anime'
    MANGA = 'manga'


class UserRateTarget(EnhancedEnum):
    """Contains constants related for getting
    certain target type of user rate."""
    ANIME = 'Anime'
    MANGA = 'Manga'


class UserRateStatus(EnhancedEnum):
    """Contains constants related for getting
    certain status of item in user rates list.
    """
    PLANNED = 'planned'
    WATCHING = 'watching'
    REWATCHING = 'rewatching'
    COMPLETED = 'completed'
    ON_HOLD = 'on_hold'
    DROPPED = 'dropped'
