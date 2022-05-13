"""Model for /api/ranobe"""
from typing import List, Optional

from pydantic import BaseModel

from shikithon.models.genre import Genre
from shikithon.models.image import Image
from shikithon.models.user_rate import UserRate
from shikithon.models.user_rate_score import UserRateScore
from shikithon.models.user_rate_status import UserRateStatus


class Ranobe(BaseModel):
    """Represents ranobe entity."""
    id: int
    name: str
    russian: str
    image: Image
    url: str
    kind: str
    score: float
    status: str
    volumes: int
    chapters: int
    aired_on: Optional[str]
    released_on: Optional[str]
    english: Optional[List[str]]
    japanese: Optional[List[str]]
    synonyms: Optional[List[str]]
    license_name_ru: Optional[str]
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
    licensors: Optional[List[str]]
    genres: Optional[List[Genre]]
    publishers: Optional[List[str]]
    user_rate: Optional[UserRate]
