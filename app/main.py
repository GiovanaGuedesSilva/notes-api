from fastapi import FastAPI

from app.database import engine, Base
from app.models import Note, User  # noqa: F401
from app.routes import notes, grammar, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Note Mark API",
    description="Markdown note-taking API with JWT authentication and grammar checking",
    version="2.0.0",
)

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(grammar.router)


@app.get("/")
def root():
    return {"message": "Welcome to Note Mark API!", "docs": "/docs"}
