"""Model for `/api/animes`."""
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from .genre import Genre
from .image import Image
from .screenshot import Screenshot
from .studio import Studio
from .user_rate import UserRate
from .user_rate_score import UserRateScore
from .user_rate_status import UserRateStatus
from .video import Video


class AnimeInfo(BaseModel):
    """Represents an anime info entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
    kind: Optional[str] = None
    score: float
    status: str
    episodes: int
    episodes_aired: int
    aired_on: Optional[date] = None
    released_on: Optional[date] = None


class Anime(AnimeInfo):
    """Represents an anime entity."""
    rating: str
    english: List[Optional[str]]
    japanese: List[Optional[str]]
    synonyms: List[str]
    license_name_ru: Optional[str] = None
    duration: int
    description: Optional[str] = None
    description_html: str
    description_source: Optional[str] = None
    franchise: Optional[str] = None
    favoured: bool
    anons: bool
    ongoing: bool
    thread_id: Optional[int] = None
    topic_id: Optional[int] = None
    myanimelist_id: int
    rates_scores_stats: List[UserRateScore]
    rates_statuses_stats: List[UserRateStatus]
    updated_at: datetime
    next_episode_at: Optional[datetime] = None
    fansubbers: List[str]
    fandubbers: List[str]
    licensors: List[str]
    genres: List[Genre]
    studios: List[Studio]
    videos: List[Video]
    screenshots: List[Screenshot]
    user_rate: Optional[UserRate] = None


class CharacterAnime(AnimeInfo):
    """Represents a character anime info entity."""
    roles: List[str]
    role: str
