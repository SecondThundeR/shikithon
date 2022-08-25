"""Model for api/v2/abuse_requests"""
from typing import List

from pydantic import BaseModel


class AbuseResponse(BaseModel):
    """Represents abuse response entity."""
    kind: str
    value: bool
    affected_ids: List[int]
