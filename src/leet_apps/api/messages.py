import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

router = APIRouter(prefix="/api/messages")

# In-memory store for messages keyed by message id
_messages = {}


class MessageCreate(BaseModel):
    session_id: str
    role: str  # 'user' or 'assistant'
    content: str


class Message(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime


@router.post("/", response_model=Message)
async def create_message(payload: MessageCreate = Body(...)):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="content cannot be empty")
    msg_id = str(uuid.uuid4())
    now = datetime.utcnow()
    message = Message(
        id=msg_id,
        session_id=payload.session_id,
        role=payload.role,
        content=payload.content,
        created_at=now,
    )
    _messages[msg_id] = message
    return message


@router.get("/session/{session_id}", response_model=List[Message])
async def list_messages_for_session(session_id: str):
    msgs = [m for m in _messages.values() if m.session_id == session_id]
    # sort by created_at ascending
    msgs.sort(key=lambda m: m.created_at)
    return msgs


@router.get("/{message_id}", response_model=Message)
async def get_message(message_id: str):
    msg = _messages.get(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg
