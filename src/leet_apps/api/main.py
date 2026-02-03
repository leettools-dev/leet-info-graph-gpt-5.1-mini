from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

app = FastAPI(title="Infograph Research API (MVP)")

# In-memory stores (MVP)
USERS = {}
SESSIONS = {}
SOURCES = {}
INFOGRAPHICS = {}

# Data models
class UserCreate(BaseModel):
    email: str
    name: Optional[str]

class User(BaseModel):
    id: str
    email: str
    name: Optional[str]
    created_at: datetime

class ResearchSessionCreate(BaseModel):
    user_id: str
    prompt: str

class ResearchSession(BaseModel):
    id: str
    user_id: str
    prompt: str
    status: str
    created_at: datetime

class SourceCreate(BaseModel):
    title: str
    url: HttpUrl
    snippet: Optional[str]
    confidence: Optional[float] = 0.0

class Source(BaseModel):
    id: str
    session_id: str
    title: str
    url: HttpUrl
    snippet: Optional[str]
    fetched_at: datetime
    confidence: float

class InfographicCreate(BaseModel):
    title: str
    layout_meta: Optional[dict] = {}

class Infographic(BaseModel):
    id: str
    session_id: str
    image_url: str
    layout_meta: dict
    created_at: datetime

# User endpoints
@app.post("/api/users", response_model=User)
def create_user(u: UserCreate):
    user_id = str(uuid4())
    now = datetime.utcnow()
    user = User(id=user_id, email=u.email, name=u.name, created_at=now)
    USERS[user_id] = user.dict()
    return user

@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Session endpoints
@app.post("/api/sessions", response_model=ResearchSession)
def create_session(s: ResearchSessionCreate):
    if s.user_id not in USERS:
        raise HTTPException(status_code=400, detail="Unknown user_id")
    sid = str(uuid4())
    now = datetime.utcnow()
    session = ResearchSession(id=sid, user_id=s.user_id, prompt=s.prompt, status="created", created_at=now)
    SESSIONS[sid] = session.dict()
    SOURCES[sid] = []
    INFOGRAPHICS[sid] = None
    return session

@app.get("/api/sessions/{session_id}", response_model=ResearchSession)
def get_session(session_id: str):
    sess = SESSIONS.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess

# Source endpoints
@app.post("/api/sessions/{session_id}/sources", response_model=Source)
def add_source(session_id: str, src: SourceCreate):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    sid = str(uuid4())
    now = datetime.utcnow()
    source = Source(id=sid, session_id=session_id, title=src.title, url=src.url, snippet=src.snippet, fetched_at=now, confidence=src.confidence or 0.0)
    SOURCES[session_id].append(source.dict())
    return source

@app.get("/api/sessions/{session_id}/sources", response_model=List[Source])
def list_sources(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    return SOURCES.get(session_id, [])

# Infographic generation (MVP static SVG)
@app.post("/api/sessions/{session_id}/infographic", response_model=Infographic)
def generate_infographic(session_id: str, info: InfographicCreate):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    # Create a simple SVG as placeholder
    svg = f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"800\" height=\"600\">"
    svg += f"<rect width=\"100%\" height=\"100%\" fill=\"#ffffff\"/>"
    svg += f"<text x=\"40\" y=\"80\" font-size=\"28\" fill=\"#111827\">{info.title}</text>"
    svg += f"<text x=\"40\" y=\"120\" font-size=\"16\" fill=\"#374151\">Prompt: {SESSIONS[session_id]['prompt']}</text>"
    svg += "</svg>"
    # For MVP, store the SVG as a data URL
    data_url = "data:image/svg+xml;utf8," + svg.replace("\n", "")
    iid = str(uuid4())
    now = datetime.utcnow()
    infographic = Infographic(id=iid, session_id=session_id, image_url=data_url, layout_meta=info.layout_meta or {}, created_at=now)
    INFOGRAPHICS[session_id] = infographic.dict()
    # mark session status
    sess = SESSIONS[session_id]
    sess["status"] = "infographic_ready"
    SESSIONS[session_id] = sess
    return infographic

@app.get("/api/sessions/{session_id}/infographic", response_model=Optional[Infographic])
def get_infographic(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    return INFOGRAPHICS.get(session_id)
