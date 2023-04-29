"""Model for /api/clubs"""
from typing import List, Optional

from pydantic import BaseModel

from .anime import AnimeInfo
from .character import CharacterInfo
from .club_image import ClubImage
from .logo import Logo
from .manga import Manga
from .user import User


class Club(BaseModel):
    """Represents a club entity."""
    id: int
    name: str
    logo: Logo
    is_censored: bool
    join_policy: str
    comment_policy: str
    description: Optional[str]
    description_html: Optional[str]
    mangas: Optional[List[Manga]]
    characters: Optional[List[CharacterInfo]]
    thread_id: Optional[int]
    topic_id: Optional[int]
    user_role: Optional[str]
    style_id: Optional[int]
    members: Optional[List[User]]
    animes: Optional[List[AnimeInfo]]
    images: Optional[List[ClubImage]]
