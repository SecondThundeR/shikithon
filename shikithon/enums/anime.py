"""Enums for /api/animes."""
from .enhanced_enum import EnhancedEnum


class AnimeOrder(EnhancedEnum):
    """Contains constants related for list ordering query."""
    ID = 'id'
    ID_DESC = 'id_desc'
    RANKED = 'ranked'
    KIND = 'kind'
    POPULARITY = 'popularity'
    NAME = 'name'
    AIRED_ON = 'aired_on'
    EPISODES = 'episodes'
    STATUS = 'status'
    CREATED_AT = 'created_at'
    CREATED_AT_DESC = 'created_at_desc'
    RANDOM = 'random'


class AnimeKind(EnhancedEnum):
    """Contains constants related for getting certain kind of anime."""
    TV = 'tv'
    NOT_TV = '!tv'
    TV_13 = 'tv_13'
    NOT_TV_13 = '!tv_13'
    TV_24 = 'tv_24'
    NOT_TV_24 = '!tv_24'
    TV_48 = 'tv_48'
    NOT_TV_48 = '!tv_48'
    MOVIE = 'movie'
    NOT_MOVIE = '!movie'
    OVA = 'ova'
    NOT_OVA = '!ova'
    ONA = 'ona'
    NOT_ONA = '!ona'
    SPECIAL = 'special'
    NOT_SPECIAL = '!special'
    MUSIC = 'music'
    NOT_MUSIC = '!music'


class AnimeStatus(EnhancedEnum):
    """Contains constants related for getting certain status of anime."""
    ANONS = 'anons'
    NOT_ANONS = '!anons'
    ONGOING = 'ongoing'
    NOT_ONGOING = '!ongoing'
    RELEASED = 'released'
    NOT_RELEASED = '!released'


class AnimeTopicKind(EnhancedEnum):
    """Contains constants related for getting certain kind of anime topic."""
    ANONS = 'anons'
    ONGOING = 'ongoing'
    RELEASED = 'released'


class AnimeDuration(EnhancedEnum):
    """Contains constants related for getting certain duration of anime."""
    SHORT = 'S'
    NOT_SHORT = '!S'
    MEDIUM = 'D'
    NOT_MEDIUM = '!D'
    LONG = 'F'
    NOT_LONG = '!F'


class AnimeRating(EnhancedEnum):
    """Contains constants related for getting certain rating of anime."""
    NO_RATING = 'none'
    NOT_NO_RATING = '!none'
    ALL_AGES = 'g'
    NOT_ALL_AGES = '!g'
    CHILDREN = 'pg'
    NOT_CHILDREN = '!pg'
    TEENS = 'pg_13'
    NOT_TEENS = '!pg_13'
    VIOLENCE = 'r'
    NOT_VIOLENCE = '!r'
    MILD_NUDITY = 'r_plus'
    NOT_MILD_NUDITY = '!r_plus'
    HENTAI = 'rx'
    NOT_HENTAI = '!rx'


class AnimeCensorship(EnhancedEnum):
    """Contains constants related for getting
    certain censorship status of anime.
    """
    CENSORED = 'true'
    UNCENSORED = 'false'


class AnimeList(EnhancedEnum):
    """Contains constants related for getting
    certain user list status of anime.
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
