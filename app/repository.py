from sqlalchemy.orm import Session

from app.models import Note, User
from app.schemas import NoteCreate, NoteUpdate, UserCreate


# ── User ──────────────────────────────────────────────────────────────────────


def create_user(db: Session, user_data: UserCreate, hashed_password: str) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


# ── Notes ─────────────────────────────────────────────────────────────────────


def create_note(db: Session, note_data: NoteCreate, owner_id: int) -> Note:
    note = Note(title=note_data.title, content=note_data.content, owner_id=owner_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> list[Note]:
    return (
        db.query(Note).filter(Note.owner_id == owner_id).offset(skip).limit(limit).all()
    )


def get_note_by_id(db: Session, note_id: int, owner_id: int) -> Note | None:
    return db.query(Note).filter(Note.id == note_id, Note.owner_id == owner_id).first()


def update_note(
    db: Session, note_id: int, note_data: NoteUpdate, owner_id: int
) -> Note | None:
    note = get_note_by_id(db, note_id, owner_id)
    if not note:
        return None

    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content

    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int, owner_id: int) -> bool:
    note = get_note_by_id(db, note_id, owner_id)
    if not note:
        return False

    db.delete(note)
    db.commit()
    return True
