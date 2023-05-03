"""Model for `/api/constants`."""
from typing import Tuple, Literal

from pydantic import BaseModel


class AnimeConstants(BaseModel):
    """Represents anime constants."""
    kind: Tuple[Literal['tv'], Literal['movie'], Literal['ova'], Literal['ona'],
                Literal['special'], Literal['music']]
    status: Tuple[Literal['anons'], Literal['ongoing'], Literal['released']]


class MangaConstants(BaseModel):
    """Represents manga constants."""
    kind: Tuple[Literal['manga'], Literal['manhwa'], Literal['manhua'],
                Literal['light_novel'], Literal['novel'], Literal['one_shot'],
                Literal['doujin']]
    status: Tuple[Literal['anons'], Literal['ongoing'], Literal['released'],
                  Literal['paused'], Literal['discontinued']]


class UserRateConstants(BaseModel):
    """Represents user rate constants."""
    status: Tuple[Literal['planned'], Literal['watching'],
                  Literal['rewatching'], Literal['completed'],
                  Literal['on_hold'], Literal['dropped']]


class ClubConstants(BaseModel):
    """Represents clubs constants."""
    join_policy: Tuple[
        Literal['free'],
        Literal['member_invite'],
        Literal['admin_invite'],
        Literal['owner_invite'],
    ]
    comment_policy: Tuple[
        Literal['free'],
        Literal['members'],
        Literal['admins'],
    ]
    image_upload_policy: Tuple[
        Literal['members'],
        Literal['admins'],
    ]


class SmileyConstant(BaseModel):
    """Represents smiley constant."""
    bbcode: str
    path: str
