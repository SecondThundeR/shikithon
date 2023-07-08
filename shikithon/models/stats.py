"""Submodel for `user.py`."""
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

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
    statuses: Optional[StatusList] = None
    full_statuses: Optional[StatusList] = None
    scores: Optional[ScoreList] = None
    types: Optional[TypeList] = None
    ratings: Optional[RatingList] = None
    has_anime: Optional[bool] = Field(default=None, alias='has_anime?')
    has_manga: Optional[bool] = Field(default=None, alias='has_manga?')
    genres: List[Genre]
    studios: List[Studio]
    publishers: List[Publisher]
    activity: Optional[Union[List[Activity], Dict]] = None
