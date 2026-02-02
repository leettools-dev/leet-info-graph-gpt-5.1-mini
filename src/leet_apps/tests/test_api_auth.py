import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.leet_apps.api.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

client = TestClient(app)

def test_health_ok():
    res = client.get("/api/auth/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_login_not_implemented():
    res = client.post("/api/auth/login")
    assert res.status_code == 501
    assert res.json()["detail"] == "Not implemented"
