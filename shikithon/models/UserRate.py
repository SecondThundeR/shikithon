from datetime import datetime
from typing import Union
from typing import Optional

from pydantic import BaseModel


class UserRate(BaseModel):
    id: int
    user_id: Optional[int]
    target_id: Optional[int]
    target_type: Optional[str]
    score: int
    status: str
    text: str
    episodes: Optional[int]
    chapters: Optional[int]
    volumes: Optional[int]
    text_html: str
    rewatches: int
    created_at: datetime
    updated_at: datetime


class RateScore(BaseModel):
    name: int
    value: Union[int, float]


class RateStatus(BaseModel):
    name: str
    value: int
