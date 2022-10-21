"""Enums for /api/ranobe."""
from .enhanced_enum import EnhancedEnum


class RanobeOrder(EnhancedEnum):
    """Contains constants related for list ordering query."""
    ID = 'id'
    ID_DESC = 'id_desc'
    RANKED = 'ranked'
    KIND = 'kind'
    POPULARITY = 'popularity'
    NAME = 'name'
    AIRED_ON = 'aired_on'
    VOLUMES = 'volumes'
    CHAPTERS = 'chapters'
    STATUS = 'status'
    CREATED_AT = 'created_at'
    CREATED_AT_DESC = 'created_at_desc'
    RANDOM = 'random'


class RanobeStatus(EnhancedEnum):
    """Contains constants related for getting certain status of ranobe."""
    ANONS = 'anons'
    NOT_ANONS = '!anons'
    ONGOING = 'ongoing'
    NOT_ONGOING = '!ongoing'
    RELEASED = 'released'
    NOT_RELEASED = '!released'
    PAUSED = 'paused'
    NOT_PAUSED = '!paused'
    DISCONTINUED = 'discontinued'
    NOT_DISCONTINUED = '!discontinued'


class RanobeCensorship(EnhancedEnum):
    """Contains constants related for getting
    certain censorship status of ranobe.
    """
    CENSORED = 'true'
    UNCENSORED = 'false'


class RanobeList(EnhancedEnum):
    """Contains constants related for getting
    certain user list status of ranobe.
    """
    PLANNED = 'planned'
    NOT_PLANNED = '!planned'
    WATCHING = 'watching'
    NOT_WATCHING = '!watching'
    REWATCHING = 'rewatching'
    NOT_REWATCHING = '!rewatching'
    COMPLETED = 'completed'
    NOT_COMPLETED = '!completed'
    ON_HOLD = 'on_hold'
    NOT_ON_HOLD = '!on_hold'
    DROPPED = 'dropped'
    NOT_DROPPED = '!dropped'
