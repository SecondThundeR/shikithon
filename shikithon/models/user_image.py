"""Submodel for user.py"""
from pydantic import BaseModel


class UserImage(BaseModel):
    """Represents user profile links entity."""
    x160: str
    x148: str
    x80: str
    x64: str
    x48: str
    x32: str
    x16: str
