"""Model for /api/mangas"""
from typing import List, Optional

from pydantic import BaseModel, validator

from .genre import Genre
from .image import Image
from .publisher import Publisher
from .user_rate import UserRate
from .user_rate_score import UserRateScore
from .user_rate_status import UserRateStatus

MANGAS_KIND = ['manga', 'manhwa', 'manhua', 'one_shot', 'doujin']


class Manga(BaseModel):
    """Represents manga entity."""
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
    english: Optional[List[Optional[str]]]
    japanese: Optional[List[Optional[str]]]
    synonyms: Optional[List[Optional[str]]]
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
    publishers: Optional[List[Publisher]]
    user_rate: Optional[UserRate]

    # pylint: disable=E0213
    @validator('kind')
    def kind_validator(cls, v):
        if v not in MANGAS_KIND:
            raise ValueError(f'Invalid manga kind. Got "{v}"'
                             f' but expected one of {MANGAS_KIND}')
        return v
