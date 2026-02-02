from datetime import datetime
import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

router = APIRouter(prefix="/api/users")

# Simple in-memory store for demo purposes
_users = {}

class UserCreate(BaseModel):
    email: str
    name: Optional[str]

class User(BaseModel):
    id: str
    email: str
    name: Optional[str]
    created_at: datetime


@router.post("/", response_model=User)
async def create_user(payload: UserCreate = Body(...)):
    if not payload.email or not payload.email.strip():
        raise HTTPException(status_code=400, detail="email is required")
    user_id = str(uuid.uuid4())
    now = datetime.utcnow()
    user = User(id=user_id, email=payload.email, name=payload.name, created_at=now)
    _users[user_id] = user
    return user


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = _users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[User])
async def list_users():
    return list(_users.values())
