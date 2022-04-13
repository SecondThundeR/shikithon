from pydantic import BaseModel


class Image(BaseModel):
    original: str
    preview: str
    x96: str
    x48: str
