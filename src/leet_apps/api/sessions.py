import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/sessions")

# In-memory store for demo purposes. In production this would be a DB.
_sessions = {}
_sources: Dict[str, List[dict]] = {}
_infographics: Dict[str, dict] = {}

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

class Source(BaseModel):
    title: str
    url: str
    snippet: str
    fetched_at: datetime
    confidence: float


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


@router.post("/{session_id}/run")
async def run_research_session(session_id: str):
    """
    Run a mock research pipeline for the session:
    - Fetch sources using the mock search endpoint implementation
    - Save sources associated with the session
    - Create a placeholder infographic entry
    """
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Use the mock search implementation in src.leet_apps.api.search
    try:
        from src.leet_apps.api import search as search_module
    except Exception:
        raise HTTPException(status_code=500, detail="Search module unavailable")

    # Call the search function with the session prompt
    results = await search_module.search(query=session.prompt)

    # Store sources for the session
    _sources[session_id] = [dict(r) for r in results]

    # Create a placeholder infographic record
    infographic = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "image_url": f"/static/infographics/{session_id}.png",
        "layout_meta": {"template": "basic_v1"},
        "created_at": datetime.utcnow(),
    }
    _infographics[session_id] = infographic

    # Update session status
    session.status = "completed"
    _sessions[session_id] = session

    return {"session": session, "sources": _sources[session_id], "infographic": infographic}


@router.get("/{session_id}/sources", response_model=List[Source])
async def list_sources_for_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return _sources.get(session_id, [])


@router.get("/{session_id}/infographic")
async def get_infographic_for_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    infographic = _infographics.get(session_id)
    if not infographic:
        raise HTTPException(status_code=404, detail="Infographic not found")
    return infographic


@router.get("/{session_id}/export")
async def export_session(session_id: str):
    """
    Export the full session data as JSON, including session record, messages, sources and infographic metadata.
    """
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Gather messages from messages module if available
    messages = []
    try:
        from src.leet_apps.api import messages as messages_module
        msgs = [m for m in messages_module._messages.values() if m.session_id == session_id]
        # sort by created_at
        msgs.sort(key=lambda m: m.created_at)
        messages = [m.dict() for m in msgs]
    except Exception:
        messages = []

    sources = _sources.get(session_id, [])
    infographic = _infographics.get(session_id)

    return {
        "session": session.dict() if hasattr(session, "dict") else session,
        "messages": messages,
        "sources": sources,
        "infographic": infographic,
    }


@router.get("/{session_id}/export/infographic")
async def export_infographic(session_id: str, format: str = Query("png", regex="^(png|svg)$")):
    """
    Export the infographic image. For demo purposes this returns the image URL and requested format.
    In a real implementation this would stream the image bytes with appropriate content-type.
    """
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    infographic = _infographics.get(session_id)
    if not infographic:
        raise HTTPException(status_code=404, detail="Infographic not found")

    return {"image_url": infographic["image_url"], "format": format}
