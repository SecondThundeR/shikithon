from pydantic import BaseModel

from .Logo import Logo


class Club(BaseModel):
    id: int
    name: str
    logo: Logo
    is_censored: bool
    join_policy: str
    comment_policy: str
