from pydantic import BaseModel


class Screenshot(BaseModel):
    original: str
    preview: str
