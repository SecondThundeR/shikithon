from enum import Enum


class Order(Enum):
    NONE = ""
    ID = "id",
    RANKED = "ranked",
    KIND = "kind",
    POPULARITY = "popularity",
    NAME = "name",
    AIRED_ON = "aired_on",
    EPISODES = "episodes",
    STATUS = "status",
    RANDOM = "random"

class Kind(Enum):
    NONE = ""
    TV = "tv"
    TV_13 = "tv_13",
    TV_24 = "tv_24",
    TV_48 = "tv_48",
    MOVIE = "movie",
    OVA = "ova",
    ONA = "ona",
    SPECIAL = "special",
    MUSIC = "music"

class Status(Enum):
    NONE = ""
    ANONS = "anons",
    ONGOING = "ongoing"
    RELEASED = "released"

class Duration(Enum):
    NONE = ""
    SHORT = "S"
    MEDIUM = "D"
    LONG = "F"

class Rating(Enum):
    NONE = ""
    NO_RATING = "none"
    ALL_AGES = "g",
    CHILDREN = "pg"
    TEENS = "pg_13",
    VIOLENCE = "r"
    MILD_NUDITY = "r_plus"
    HENTAI = "rx"

class MyList(Enum):
    NONE = "",
    PLANNED = "planned",
    WATCHING = "watching",
    REWATCHING = "rewatching",
    COMPLETED = "completed",
    ON_HOLD = "on_hold",
    DROPPED = "dropped"
