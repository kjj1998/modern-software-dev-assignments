# Action Item Extractor

A FastAPI application that extracts action items from text notes using both heuristic-based parsing and LLM-powered extraction (Ollama + llama3.1). Includes a SQLite database for persistence and a minimal HTML frontend.

## Project Structure

```
week2/
├── app/
│   ├── main.py              # FastAPI app setup
│   ├── db.py                # SQLite database layer
│   ├── routers/
│   │   ├── notes.py         # Notes endpoints
│   │   └── action_items.py  # Action item endpoints
│   └── services/
│       └── extract.py       # Extraction logic (heuristic + LLM)
├── frontend/
│   └── index.html           # Single-page frontend
├── tests/
│   └── test_extract.py      # Unit tests
└── data/
    └── app.db               # SQLite database (auto-created)
```

## Setup

1. Activate the conda environment:
   ```bash
   conda activate cs146s
   ```

2. Install dependencies (from the project root):
   ```bash
   poetry install
   ```

3. Ensure Ollama is running with the llama3.1 model (required for LLM extraction):
   ```bash
   ollama pull llama3.1
   ```

## Running the App

From the project root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## API Endpoints

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/notes` | List all saved notes |
| `POST` | `/notes` | Create a new note (`{content: str}`) |
| `GET` | `/notes/{note_id}` | Get a specific note |

### Action Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/action-items/extract` | Extract action items using heuristic parsing |
| `POST` | `/action-items/extract-llm` | Extract action items using LLM |
| `GET` | `/action-items` | List all action items (optional `?note_id=` filter) |
| `POST` | `/action-items/{id}/done` | Mark an action item as done/undone |

**Extract request body:**
```json
{
  "text": "- [ ] Set up database\n- Implement API",
  "save_note": true
}
```

**Extract response:**
```json
{
  "note_id": 1,
  "items": [
    {"id": 1, "text": "Set up database"},
    {"id": 2, "text": "Implement API"}
  ]
}
```

## Running Tests

From the project root:

```bash
poetry run pytest week2/tests/test_extract.py -v
```
