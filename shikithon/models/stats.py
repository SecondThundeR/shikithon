"""Submodel for user.py"""
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

from shikithon.models.activity import Activity
from shikithon.models.rating_list import RatingList
from shikithon.models.score_list import ScoreList
from shikithon.models.status_list import StatusList
from shikithon.models.type_list import TypeList


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
