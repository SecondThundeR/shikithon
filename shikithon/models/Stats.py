from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Status(BaseModel):
    id: int
    grouped_id: str
    name: str
    size: int
    type: str


class Statuses(BaseModel):
    anime: Optional[list[Status]]
    manga: Optional[list[Status]]


class FullStatuses(BaseModel):
    anime: Optional[list[Status]]
    manga: Optional[list[Status]]


class Score(BaseModel):
    name: str
    value: int


class Scores(BaseModel):
    anime: Optional[list[Score]]
    manga: Optional[list[Score]]


class Type(BaseModel):
    name: str
    value: int


class Types(BaseModel):
    anime: Optional[list[Type]]
    manga: Optional[list[Type]]


class Rating(BaseModel):
    name: str
    value: int


class Ratings(BaseModel):
    anime: Optional[list[Rating]]
    manga: Optional[list[Rating]]


class Activity(BaseModel):
    name: list[int]
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
    genres: Optional[list[str]]
    studios: Optional[list[str]]
    publishers: Optional[list[str]]
    activity: Optional[list[Activity]]
