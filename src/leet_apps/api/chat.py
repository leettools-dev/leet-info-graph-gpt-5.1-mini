import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

router = APIRouter(prefix="/api/chat")


class ChatCreatePayload(BaseModel):
    user_id: str
    prompt: str
    topic: Optional[str] = None
    tags: Optional[list[str]] = None


@router.post("/send")
async def send_and_run(payload: ChatCreatePayload = Body(...)):
    """
    Convenience endpoint for the demo UI:
    - Creates a ResearchSession for the provided user_id and prompt
    - Stores an initial user message
    - Runs the mock research pipeline (sessions.run_research_session)
    - Returns the aggregated session, messages, sources and infographic

    This endpoint is intended for demo/dev usage to simplify the frontend integration.
    """
    if not payload.prompt or not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt is required")

    try:
        from src.leet_apps.api import sessions as sessions_module
        from src.leet_apps.api import messages as messages_module
    except Exception:
        raise HTTPException(status_code=500, detail="Internal modules unavailable")

    # Create a session record
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    session = sessions_module.ResearchSession(
        id=session_id,
        user_id=payload.user_id,
        prompt=payload.prompt,
        status="pending",
        created_at=now,
        topic=payload.topic,
        tags=payload.tags or [],
    )
    sessions_module._sessions[session_id] = session

    # Create initial user message
    msg_id = str(uuid.uuid4())
    message = messages_module.Message(
        id=msg_id,
        session_id=session_id,
        role="user",
        content=payload.prompt,
        created_at=now,
    )
    messages_module._messages[msg_id] = message

    # Run the research pipeline for the session (this will call the mock search implementation)
    try:
        result = await sessions_module.run_research_session(session_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run research pipeline: {e}")

    # Gather messages for the session
    msgs = [m for m in messages_module._messages.values() if m.session_id == session_id]
    msgs.sort(key=lambda m: m.created_at)
    messages_list = [m.dict() for m in msgs]

    return {
        "session": result["session"],
        "messages": messages_list,
        "sources": result.get("sources", []),
        "infographic": result.get("infographic"),
    }
