import os
from fastapi import APIRouter, HTTPException
from urllib.parse import urlencode
from typing import Optional

router = APIRouter(prefix="/api/auth")

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

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
async def callback(code: Optional[str] = None, error: Optional[str] = None):
    """
    Handle the OAuth callback. In a real implementation this would exchange the code for tokens
    and create/lookup the user in the database.

    For local development and tests this endpoint has two modes:
    - If GOOGLE_OAUTH_CLIENT_SECRET is not set, return a placeholder response acknowledging the code.
    - If GOOGLE_OAUTH_CLIENT_SECRET is set, return a simulated token response (no external network calls).
    """
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in callback")

    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    redirect_uri = os.environ.get("GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8000/api/auth/callback")

    # If client_secret is not configured, avoid performing network calls and return a placeholder.
    if not client_secret:
        return {"status": "ok", "message": "Received code (placeholder)", "code": code}

    # NOTE: In a production implementation, exchange the code for tokens by POSTing to
    # GOOGLE_TOKEN_ENDPOINT and validate the ID token, then look up or create the user in DB.
    # Here we simulate a successful token exchange and user info for testing purposes.
    tokens = {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
        "expires_in": 3600,
        "scope": "openid email profile",
        "token_type": "Bearer",
    }
    user = {"id": "123", "email": "user@example.com", "name": "Test User"}
    return {"status": "ok", "tokens": tokens, "user": user}
