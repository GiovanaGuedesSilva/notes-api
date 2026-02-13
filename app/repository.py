from sqlalchemy.orm import Session

from app.models import Note
from app.schemas import NoteCreate, NoteUpdate


def create_note(db: Session, note_data: NoteCreate) -> Note:
    note = Note(title=note_data.title, content=note_data.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes(db: Session, skip: int = 0, limit: int = 100) -> list[Note]:
    return db.query(Note).offset(skip).limit(limit).all()


def get_note_by_id(db: Session, note_id: int) -> Note | None:
    return db.query(Note).filter(Note.id == note_id).first()


def update_note(db: Session, note_id: int, note_data: NoteUpdate) -> Note | None:
    note = get_note_by_id(db, note_id)
    if not note:
        return None

    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content

    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int) -> bool:
    note = get_note_by_id(db, note_id)
    if not note:
        return False

    db.delete(note)
    db.commit()
    return True
