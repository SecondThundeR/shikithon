"""Submodel for `people.py`."""
from typing import Optional, Union

from pydantic import BaseModel

from .anime import AnimeInfo
from .manga import MangaInfo
from .ranobe import RanobeInfo


class Works(BaseModel):
    """Represents works entity of person."""
    anime: Optional[AnimeInfo] = None
    manga: Optional[Union[MangaInfo, RanobeInfo]] = None
    role: str
