"""Submodel for user.py"""
from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from pydantic import Field

from .activity import Activity
from .genre import Genre
from .publisher import Publisher
from .rating_list import RatingList
from .score_list import ScoreList
from .status_list import StatusList
from .studio import Studio
from .type_list import TypeList


class Stats(BaseModel):
    """Represents user's stats entity."""
    statuses: Optional[StatusList]
    full_statuses: Optional[StatusList]
    scores: Optional[ScoreList]
    types: Optional[TypeList]
    ratings: Optional[RatingList]
    has_anime: Optional[bool] = Field(alias='has_anime?')
    has_manga: Optional[bool] = Field(alias='has_manga?')
    genres: Optional[List[Genre]]
    studios: Optional[List[Studio]]
    publishers: Optional[List[Publisher]]
    activity: Optional[Union[List[Activity], Dict]]
