from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NoteHTMLResponse(BaseModel):
    id: int
    title: str
    html_content: str


class GrammarCheckRequest(BaseModel):
    text: str


class GrammarError(BaseModel):
    message: str
    offset: int
    length: int
    replacements: list[str]


class GrammarCheckResponse(BaseModel):
    text: str
    errors: list[GrammarError]
    error_count: int
    warning: str | None = None
