"""Submodel for user.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
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
