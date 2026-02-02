import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/sessions")

# In-memory store for demo purposes. In production this would be a DB.
_sessions = {}

class ResearchSessionCreate(BaseModel):
    user_id: str
    prompt: str

class ResearchSessionUpdate(BaseModel):
    status: Optional[str]

class ResearchSession(BaseModel):
    id: str
    user_id: str
    prompt: str
    status: str
    created_at: datetime

@router.post("/", response_model=ResearchSession)
async def create_session(payload: ResearchSessionCreate = Body(...)):
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    session = ResearchSession(
        id=session_id,
        user_id=payload.user_id,
        prompt=payload.prompt,
        status="pending",
        created_at=now,
    )
    _sessions[session_id] = session
    return session

@router.get("/{session_id}", response_model=ResearchSession)
async def get_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/", response_model=List[ResearchSession])
async def list_sessions(user_id: Optional[str] = None):
    sessions = list(_sessions.values())
    if user_id:
        sessions = [s for s in sessions if s.user_id == user_id]
    return sessions

@router.put("/{session_id}", response_model=ResearchSession)
async def update_session(session_id: str, payload: ResearchSessionUpdate = Body(...)):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if payload.status:
        session.status = payload.status
        _sessions[session_id] = session
    return session
