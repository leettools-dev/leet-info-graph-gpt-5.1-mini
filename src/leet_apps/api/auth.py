from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/auth")

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/login")
async def login():
    # Placeholder for Gmail OAuth login endpoint
    raise HTTPException(status_code=501, detail="Not implemented")
