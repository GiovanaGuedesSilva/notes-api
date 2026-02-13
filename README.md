# Note Mark API

A RESTful API for markdown note-taking with grammar checking capabilities.

## Features

- Create, read, update, and delete markdown notes
- Render markdown content to HTML
- Grammar checking (coming soon)
- File upload support (coming soon)

## Tech Stack

- **Python 3.12**
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **Markdown** - Markdown to HTML conversion
- **LanguageTool** - Grammar checking

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd note-mark

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `POST` | `/notes/` | Create a new note |
| `GET` | `/notes/` | List all notes |
| `GET` | `/notes/{id}` | Get a note by ID |
| `GET` | `/notes/{id}/html` | Get note rendered as HTML |
| `PUT` | `/notes/{id}` | Update a note |
| `DELETE` | `/notes/{id}` | Delete a note |

## Usage Examples

### Create a note

```bash
curl -X POST http://localhost:8000/notes/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "# Hello\n\nThis is **bold**."}'
```

### List all notes

```bash
curl http://localhost:8000/notes/
```

### Get note as HTML

```bash
curl http://localhost:8000/notes/1/html
```

### Update a note

```bash
curl -X PUT http://localhost:8000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

### Delete a note

```bash
curl -X DELETE http://localhost:8000/notes/1
```

## Project Structure

```
note-mark/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── repository.py     # CRUD operations
│   ├── routes/
│   │   └── notes.py      # Note endpoints
│   └── services/
│       └── markdown_service.py
├── requirements.txt
└── README.md
```

## License

MIT
