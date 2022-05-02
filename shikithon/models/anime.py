"""Model for /api/animes"""
from datetime import datetime
from typing import Optional
from typing import Union
from typing import List

from pydantic import BaseModel

from shikithon.models.genre import Genre
from shikithon.models.image import Image
from shikithon.models.screenshot import Screenshot
from shikithon.models.studio import Studio
from shikithon.models.user_rate import UserRate
from shikithon.models.user_rate_score import UserRateScore
from shikithon.models.user_rate_status import UserRateStatus
from shikithon.models.video import Video


class Anime(BaseModel):
    """Represents an anime entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
    kind: str
    score: float
    status: str
    episodes: int
    episodes_aired: int
    aired_on: str
    released_on: Optional[str]
    rating: Optional[str]
    english: Optional[List[Union[str, None]]]
    japanese: Optional[List[Union[str, None]]]
    synonyms: Optional[List[Union[str, None]]]
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
