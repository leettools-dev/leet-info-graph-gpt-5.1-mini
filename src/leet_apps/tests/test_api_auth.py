import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.leet_apps.api.auth import router as auth_router
from src.leet_apps.api.users import router as users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)

client = TestClient(app)


def test_health_ok():
    res = client.get("/api/auth/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_login_requires_client_id():
    res = client.post("/api/auth/login")
    assert res.status_code == 400
    assert "Missing configuration" in res.json()["detail"]
