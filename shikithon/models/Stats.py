from typing import Optional
from typing import List

from pydantic import BaseModel
from pydantic import Field


class Status(BaseModel):
    id: int
    grouped_id: str
    name: str
    size: int
    type: str


class Statuses(BaseModel):
    anime: Optional[List[Status]]
    manga: Optional[List[Status]]


class FullStatuses(BaseModel):
    anime: Optional[List[Status]]
    manga: Optional[List[Status]]


class Score(BaseModel):
    name: str
    value: int


class Scores(BaseModel):
    anime: Optional[List[Score]]
    manga: Optional[List[Score]]


class Type(BaseModel):
    name: str
    value: int


class Types(BaseModel):
    anime: Optional[List[Type]]
    manga: Optional[List[Type]]


class Rating(BaseModel):
    name: str
    value: int


class Ratings(BaseModel):
    anime: Optional[List[Rating]]
    manga: Optional[List[Rating]]


class Activity(BaseModel):
    name: List[int]
    value: int


"""
Only this model isn't using dataclass decorator
due to unexpected fields name
"""


class Stats(BaseModel):
    statuses: Optional[Statuses]
    full_statuses: Optional[FullStatuses]
    scores: Optional[Scores]
    types: Optional[Types]
    ratings: Optional[Ratings]
    has_anime: Optional[bool] = Field(alias='has_anime?')
    has_manga: Optional[bool] = Field(alias='has_manga?')
    genres: Optional[List[str]]
    studios: Optional[List[str]]
    publishers: Optional[List[str]]
    activity: Optional[List[Activity]]
