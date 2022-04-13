from datetime import datetime
from typing import Optional
from typing import List

from pydantic import BaseModel

from .Genre import Genre
from .Image import Image
from .Screenshot import Screenshot
from .Studio import Studio
from .UserRate import UserRate
from .UserRate import RateScore
from .UserRate import RateStatus
from .Video import Video


"""
    Many fields are optional, due to API behaviour
    Returning short info and/or full info
"""


class Anime(BaseModel):
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
    english: Optional[List[str | None]]
    japanese: Optional[List[str | None]]
    synonyms: Optional[List[str | None]]
    license_name_ru: Optional[str]
    duration: Optional[int]
    description: Optional[str]
    description_html: Optional[str]
    description_source: Optional[str]  # TODO: Change type to correct one
    franchise: Optional[str]  # TODO: Change type to correct one
    favoured: Optional[bool]
    anons: Optional[bool]
    ongoing: Optional[bool]
    thread_id: Optional[int]
    topic_id: Optional[int]
    myanimelist_id: Optional[int]
    rates_scores_stats: Optional[List[RateScore]]
    rates_statuses_stats: Optional[List[RateStatus]]
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
