"""Model for `/api/ranobe`."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, validator

from .genre import Genre
from .image import Image
from .publisher import Publisher
from .user_rate import UserRate
from .user_rate_score import UserRateScore
from .user_rate_status import UserRateStatus


class RanobeInfo(BaseModel):
    """Represents ranobe info entity."""
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
        if 'novel' not in v:
            raise ValueError(f'Invalid kind. Got "{v}"'
                             f' but expected kind, containing "novel"')
        return v


class Ranobe(RanobeInfo):
    """Represents ranobe entity."""
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


class CharacterRanobe(RanobeInfo):
    """Represents a character ranobe info entity."""
    roles: List[str]
    role: str
