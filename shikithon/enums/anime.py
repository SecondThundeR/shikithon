"""Enums for /api/animes."""
from enum import Enum


class Order(Enum):
    """Contains constants related for list ordering query."""
    NONE = ""
    ID = "id"
    RANKED = "ranked"
    KIND = "kind"
    POPULARITY = "popularity"
    NAME = "name"
    AIRED_ON = "aired_on"
    EPISODES = "episodes"
    STATUS = "status"
    RANDOM = "random"


class Kind(Enum):
    """Contains constants related for getting certain kind of anime."""
    NONE = ""
    TV = "tv"
    TV_13 = "tv_13"
    TV_24 = "tv_24"
    TV_48 = "tv_48"
    MOVIE = "movie"
    OVA = "ova"
    ONA = "ona"
    SPECIAL = "special"
    MUSIC = "music"


class Status(Enum):
    """Contains constants related for getting certain status of anime."""
    NONE = ""
    ANONS = "anons"
    ONGOING = "ongoing"
    RELEASED = "released"
    EPISODE = "episode"


class Duration(Enum):
    """Contains constants related for getting certain duration of anime."""
    NONE = ""
    SHORT = "S"
    MEDIUM = "D"
    LONG = "F"


class Rating(Enum):
    """Contains constants related for getting certain rating of anime."""
    NONE = ""
    NO_RATING = "none"
    ALL_AGES = "g"
    CHILDREN = "pg"
    TEENS = "pg_13"
    VIOLENCE = "r"
    MILD_NUDITY = "r_plus"
    HENTAI = "rx"


class Censorship(Enum):
    """Contains constants related for getting
    certain censorship status of anime.
    """
    CENSORED = "true"
    UNCENSORED = "false"


class MyList(Enum):
    """Contains constants related for getting
    certain user list status of anime.
    """
    NONE = ""
    PLANNED = "planned"
    WATCHING = "watching"
    REWATCHING = "rewatching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
