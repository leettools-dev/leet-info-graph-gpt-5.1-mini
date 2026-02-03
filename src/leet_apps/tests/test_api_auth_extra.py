import os
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.leet_apps.api.auth import router as auth_router
from src.leet_apps.api import users as users_module

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_module.router)

client = TestClient(app)


def test_callback_placeholder_mode(monkeypatch):
    # Ensure client secret is NOT set to trigger placeholder mode
    monkeypatch.delenv("GOOGLE_OAUTH_CLIENT_SECRET", raising=False)
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_ID", "test-client-id")

    res = client.get("/api/auth/callback?code=testcode")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "Received code (placeholder)" in data["message"]
    assert data["code"] == "testcode"


def test_callback_with_client_secret_simulates_token_exchange(monkeypatch):
    # Set client secret to trigger simulated token exchange
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_SECRET", "test-secret")

    # Ensure users store is empty before
    users_module._users.clear()

    res = client.get("/api/auth/callback?code=abc123")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "tokens" in data
    assert data["tokens"]["access_token"] == "fake_access_token"
    assert "user" in data
    assert data["user"]["email"] == "user@example.com"

    # The callback attempts to register the user in users_module._users with id '123'
    assert "123" in users_module._users


def test_me_with_x_user_id_header_returns_user(monkeypatch):
    # Create a user in the in-memory store
    users_module._users.clear()
    u = users_module.User(id="u-test", email="u@test.com", name="Test", created_at=__import__("datetime").datetime.utcnow())
    users_module._users[u.id] = u

    res = client.get("/api/auth/me", headers={"X-User-Id": "u-test"})
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "u-test"
    assert data["email"] == "u@test.com"


def test_me_with_authorization_bearer_token_returns_simulated_user(monkeypatch):
    # Ensure the simulated token path returns the fallback user when user store missing
    users_module._users.clear()
    res = client.get("/api/auth/me", headers={"Authorization": "Bearer fake_access_token"})
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "user@example.com"
    assert data["id"] == "123"


def test_login_returns_auth_url(monkeypatch):
    # Set the client id so login can build an auth URL
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_ID", "test-client-id")
    # Ensure redirect uri not set so default path is used
    monkeypatch.delenv("GOOGLE_OAUTH_REDIRECT_URI", raising=False)

    res = client.post("/api/auth/login")
    assert res.status_code == 200
    data = res.json()
    assert "auth_url" in data
    auth_url = data["auth_url"]
    # Basic checks that required query params are present
    assert "client_id=test-client-id" in auth_url
    assert "scope=openid+email+profile" in auth_url or "scope=openid%20email%20profile" in auth_url
    assert "response_type=code" in auth_url
    # redirect_uri default should be present
    assert "redirect_uri=" in auth_url
