from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import NoteCreate, NoteUpdate, NoteResponse, NoteHTMLResponse
from app import repository
from app.services.markdown_service import render_markdown_to_html

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note_data: NoteCreate, db: Session = Depends(get_db)):
    return repository.create_note(db, note_data)


@router.get("/", response_model=list[NoteResponse])
def list_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository.get_notes(db, skip=skip, limit=limit)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = repository.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/{note_id}/html", response_model=NoteHTMLResponse)
def get_note_html(note_id: int, db: Session = Depends(get_db)):
    note = repository.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return NoteHTMLResponse(
        id=note.id,
        title=note.title,
        html_content=render_markdown_to_html(note.content)
    )


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_data: NoteUpdate, db: Session = Depends(get_db)):
    note = repository.update_note(db, note_id, note_data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    if not repository.delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Note not found")
