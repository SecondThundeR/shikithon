"""Model for /api/animes"""
from datetime import datetime
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


class Anime(BaseModel):
    """Represents an anime entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
    kind: Optional[str]
    score: float
    status: str
    episodes: int
    episodes_aired: int
    aired_on: Optional[str]
    released_on: Optional[str]
    rating: Optional[str]
    english: Optional[List[Optional[str]]]
    japanese: Optional[List[Optional[str]]]
    synonyms: Optional[List[Optional[str]]]
    license_name_ru: Optional[str]
    duration: Optional[int]
    description: Optional[str]
    description_html: Optional[str]
    description_source: Optional[str]
    franchise: Optional[str]
    favoured: Optional[bool]
    anons: Optional[bool]
    ongoing: Optional[bool]
    thread_id: Optional[int]
    topic_id: Optional[int]
    myanimelist_id: Optional[int]
    rates_scores_stats: Optional[List[UserRateScore]]
    rates_statuses_stats: Optional[List[UserRateStatus]]
    updated_at: Optional[datetime]
    next_episode_at: Optional[datetime]
    fansubbers: Optional[List[str]]
    fandubbers: Optional[List[str]]
    licensors: Optional[List[str]]
    genres: Optional[List[Genre]]
    studios: Optional[List[Studio]]
    videos: Optional[List[Video]]
    screenshots: Optional[List[Screenshot]]
    user_rate: Optional[UserRate]
    roles: Optional[List[str]]
    role: Optional[str]
