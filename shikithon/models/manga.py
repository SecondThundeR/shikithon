"""Model for `/api/mangas`."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, field_validator

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
    aired_on: Optional[date] = None
    released_on: Optional[date] = None

    @field_validator('kind')
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
    license_name_ru: Optional[str] = None
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
    licensors: List[str]
    genres: List[Genre]
    publishers: List[Publisher]
    user_rate: Optional[UserRate] = None


class CharacterManga(MangaInfo):
    """Represents a character manga info entity."""
    roles: List[str]
    role: str
