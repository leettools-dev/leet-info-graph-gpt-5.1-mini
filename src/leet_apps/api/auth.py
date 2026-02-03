import os
from fastapi import APIRouter, HTTPException, Header
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
    # Default scopes: OpenID Connect for identity (id token), plus email and profile
    # For Gmail-specific features, set GOOGLE_OAUTH_SCOPES env var to a comma-separated list
    scope = os.environ.get("GOOGLE_OAUTH_SCOPES", "openid email profile")
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

    # Try to create or register the user in the in-memory user store for demos.
    try:
        from src.leet_apps.api import users as users_module
        # Create a user entry using the users.User model so other endpoints can find it in tests
        user_obj = users_module.User(id=user["id"], email=user["email"], name=user["name"], created_at=__import__("datetime").datetime.utcnow())
        users_module._users[user_obj.id] = user_obj
    except Exception:
        # If importing or creating the user fails for any reason, continue gracefully.
        pass

    return {"status": "ok", "tokens": tokens, "user": user}


@router.get("/me")
async def me(x_user_id: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
    """
    Return the current user information.
    Authentication for the demo supports either:
    - X-User-Id header with a user id present in the in-memory users store
    - Authorization: Bearer <token> where token == 'fake_access_token' created by the callback simulation

    This is intentionally simple for the prototype; in production, validate JWTs or session cookies.
    """
    # If X-User-Id header provided, try to fetch the user
    if x_user_id:
        try:
            from src.leet_apps.api import users as users_module
            user = users_module._users.get(x_user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=500, detail="Unable to access user store")

    # Fallback: check Authorization header for the demo token
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1] == "fake_access_token":
            # Return the simulated user created by callback
            try:
                from src.leet_apps.api import users as users_module
                user = users_module._users.get("123")
                if user:
                    return user
                # If not present, return a minimal simulated user
                return {"id": "123", "email": "user@example.com", "name": "Test User"}
            except Exception:
                return {"id": "123", "email": "user@example.com", "name": "Test User"}

    raise HTTPException(status_code=401, detail="Not authenticated")


@router.post("/logout")
async def logout(x_user_id: Optional[str] = Header(None)):
    """
    Logout a user in the demo by removing them from the in-memory user store if X-User-Id is provided.
    In production, revoke tokens and clear sessions instead.
    """
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-Id header required for demo logout")
    try:
        from src.leet_apps.api import users as users_module
        if x_user_id in users_module._users:
            del users_module._users[x_user_id]
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to modify user store")
