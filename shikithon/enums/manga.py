"""Enums for /api/mangas."""
from .enhanced_enum import EnhancedEnum


class MangaOrder(EnhancedEnum):
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
    CREATED_AT = 'created_at'
    CREATED_AT_DESC = 'created_at_desc'
    RANDOM = 'random'


class MangaKind(EnhancedEnum):
    """Contains constants related for getting certain kind of manga."""
    MANGA = 'manga'
    NOT_MANGA = '!manga'
    MANHWA = 'manhwa'
    NOT_MANHWA = '!manhwa'
    MANHUA = 'manhua'
    NOT_MANHUA = '!manhua'
    LIGHT_NOVEL = 'light_novel'
    NOT_LIGHT_NOVEL = '!light_novel'
    NOVEL = 'novel'
    NOT_NOVEL = '!novel'
    ONE_SHOT = 'one_shot'
    NOT_ONE_SHOT = '!one_shot'
    DOUJIN = 'doujin'
    NOT_DOUJIN = '!doujin'


class MangaStatus(EnhancedEnum):
    """Contains constants related for getting certain status of manga."""
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


class MangaCensorship(EnhancedEnum):
    """Contains constants related for getting
    certain censorship status of manga.
    """
    CENSORED = 'true'
    UNCENSORED = 'false'


class MangaList(EnhancedEnum):
    """Contains constants related for getting
    certain user list status of manga.
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
