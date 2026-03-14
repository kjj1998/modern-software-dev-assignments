from __future__ import annotations

from typing import List

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from .. import db


router = APIRouter(prefix="/notes", tags=["notes"])


class CreateNoteRequest(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


@router.post("", response_model=NoteResponse)
def create_note(payload: CreateNoteRequest) -> NoteResponse:
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=500, detail="failed to create note")
    return NoteResponse(id=note["id"], content=note["content"], created_at=note["created_at"])


@router.get("", response_model=List[NoteResponse])
def list_all_notes() -> List[NoteResponse]:
    rows = db.list_notes()
    return [
        NoteResponse(id=r["id"], content=r["content"], created_at=r["created_at"])
        for r in rows
    ]


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(id=row["id"], content=row["content"], created_at=row["created_at"])
