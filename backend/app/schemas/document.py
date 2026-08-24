from pydantic import BaseModel


class DocumentCreate(BaseModel):

    title: str
    content: str
    type: str


class DocumentUpdate(BaseModel):

    title: str | None = None
    content: str | None = None
    type: str | None = None