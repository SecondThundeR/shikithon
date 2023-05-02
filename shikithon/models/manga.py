"""Model for `/api/mangas`."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, validator

from .genre import Genre
from .image import Image
from .publisher import Publisher
from .user_rate import UserRate
from .user_rate_score import UserRateScore
from .user_rate_status import UserRateStatus

MANGAS_KIND = (
    'manga',
    'manhwa',
    'manhua',
    'one_shot',
    'doujin',
)


class MangaInfo(BaseModel):
    """Represents manga info entity."""
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
    aired_on: Optional[date]
    released_on: Optional[date]

    # pylint: disable=E0213
    @validator('kind')
    def kind_validator(cls, v):
        if v not in MANGAS_KIND:
            raise ValueError(f'Invalid manga kind. Got "{v}"'
                             f' but expected one of {MANGAS_KIND}')
        return v


class Manga(MangaInfo):
    """Represents manga entity."""
    english: List[Optional[str]]
    japanese: List[Optional[str]]
    synonyms: List[str]
    license_name_ru: Optional[str]
    description: Optional[str]
    description_html: str
    description_source: Optional[str]
    franchise: Optional[str]
    favoured: bool
    anons: bool
    ongoing: bool
    thread_id: Optional[int]
    topic_id: Optional[int]
    myanimelist_id: int
    rates_scores_stats: List[UserRateScore]
    rates_statuses_stats: List[UserRateStatus]
    licensors: List[str]
    genres: List[Genre]
    publishers: List[Publisher]
    user_rate: Optional[UserRate]


class CharacterManga(MangaInfo):
    """Represents a character manga info entity."""
    roles: List[str]
    role: str
