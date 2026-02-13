from fastapi import FastAPI

from app.database import engine, Base
from app.models import Note  # noqa: F401
from app.routes import notes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Note Mark API",
    description="Markdown note-taking API with grammar checking",
    version="1.0.0"
)

app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "Welcome to Note Mark API!", "docs": "/docs"}
