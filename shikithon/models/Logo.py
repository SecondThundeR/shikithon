from pydantic import BaseModel


class Logo(BaseModel):
    original: str
    main: str
    x96: str
    x73: str
    x48: str
