import os
from fastapi import APIRouter, HTTPException
from urllib.parse import urlencode

router = APIRouter(prefix="/api/auth")

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/login")
async def login():
    """
    Start Gmail OAuth login by returning the Google authorization URL.
    Requires environment variable GOOGLE_OAUTH_CLIENT_ID to be set.
    Redirect URI should be configured in GOOGLE_OAUTH_REDIRECT_URI (optional, defaults to http://localhost:8000/api/auth/callback)
    """
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    if not client_id:
        raise HTTPException(status_code=400, detail="Missing configuration: set GOOGLE_OAUTH_CLIENT_ID environment variable")

    redirect_uri = os.environ.get("GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8000/api/auth/callback")
    scope = "openid email profile"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": redirect_uri,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"
    return {"auth_url": auth_url}

@router.get("/callback")
async def callback(code: str | None = None, error: str | None = None):
    # Placeholder for handling the OAuth callback. In a real implementation this would
    # exchange the code for tokens and create/lookup the user in the database.
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in callback")
    return {"status": "ok", "message": "Received code (placeholder)"}
