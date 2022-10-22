"""Submodel for user.py"""
from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from pydantic import Field

from .activity import Activity
from .rating_list import RatingList
from .score_list import ScoreList
from .status_list import StatusList
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
    genres: Optional[List[str]]
    studios: Optional[List[str]]
    publishers: Optional[List[str]]
    activity: Optional[Union[List[Activity], Dict]]
