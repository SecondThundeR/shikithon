from typing import Optional

from pydantic import BaseModel

class Favorite(BaseModel):
    id: int
    name: str
    russian: str
    image: str
    url: Optional[str]
