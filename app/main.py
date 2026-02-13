from fastapi import FastAPI

app = FastAPI(
    title="Note Mark API",
    description="API for note-taking and grammar checking",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to Note Mark API!", "docs": "/docs"}
