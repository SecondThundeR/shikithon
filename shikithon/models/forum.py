"""Model for api/forums"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from pydantic import BaseModel


class Forum(BaseModel):
    """Represents forum entity."""
    id: int
    position: int
    name: str
    permalink: str
    url: str
