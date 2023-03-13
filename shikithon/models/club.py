"""Model for /api/clubs"""
from typing import List, Optional

from pydantic import BaseModel

from .anime import Anime
from .character import Character
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
    characters: Optional[List[Character]]
    thread_id: Optional[int]
    topic_id: Optional[int]
    user_role: Optional[str]
    style_id: Optional[int]
    members: Optional[List[User]]
    animes: Optional[List[Anime]]
    images: Optional[List[ClubImage]]
