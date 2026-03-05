from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# ── Auth ──────────────────────────────────────────────────────────────────────


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# ── Notes ─────────────────────────────────────────────────────────────────────


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


# ── Grammar ───────────────────────────────────────────────────────────────────


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
