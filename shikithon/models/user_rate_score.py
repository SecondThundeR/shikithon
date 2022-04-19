"""Submodel for anime.py"""
# pylint: disable=E0611, R0903, E0402 (no-name-in-module, too-few-public-methods, relative-beyond-top-level)
from typing import Union

from pydantic import BaseModel


class UserRateScore(BaseModel):
    """Represents user rate score entity.

    Because of the unusual behavior of the Shikimori API,
    it can return either int or float as a result.
    """
    name: int
    value: Union[int, float]
