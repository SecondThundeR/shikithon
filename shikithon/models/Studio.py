from typing import Optional

from pydantic import BaseModel


class Studio(BaseModel):
    id: int
    name: str
    filtered_name: str
    real: bool
    image: Optional[str]
