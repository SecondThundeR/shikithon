"""Model for `/api/clubs`."""
from typing import List, Optional

from pydantic import BaseModel

from .anime import AnimeInfo
from .character import CharacterInfo
from .club_image import ClubImage
from .logo import Logo
from .manga import MangaInfo
from .user import UserInfo


class ClubInfo(BaseModel):
    """Represents a club info entity."""
    id: int
    name: str
    logo: Logo
    is_censored: bool
    join_policy: str
    comment_policy: str


class Club(ClubInfo):
    """Represents a club entity."""
    description: Optional[str] = None
    description_html: str
    mangas: List[MangaInfo]
    characters: List[CharacterInfo]
    thread_id: int
    topic_id: int
    user_role: Optional[str] = None
    style_id: int
    members: List[UserInfo]
    animes: List[AnimeInfo]
    images: List[ClubImage]
