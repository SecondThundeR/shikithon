from pydantic import BaseModel


class Video(BaseModel):
    id: int
    url: str
    image_url: str
    player_url: str
    name: str
    kind: str
    hosting: str
