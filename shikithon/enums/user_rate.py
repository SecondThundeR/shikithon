"""Enums for /api/user_rates."""
from enum import Enum


class UserRateType(Enum):
    """Contains constants related for getting certain type of user rate."""
    ANIME = 'anime'
    MANGA = 'manga'
