import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.leet_apps.api.sessions import router as sessions_router

app = FastAPI()
app.include_router(sessions_router)

client = TestClient(app)


def test_create_and_get_session():
    payload = {"user_id": "u1", "prompt": "Summarize EV trends"}
    res = client.post("/api/sessions/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == "u1"
    session_id = data["id"]

    res2 = client.get(f"/api/sessions/{session_id}")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["id"] == session_id


def test_list_sessions_filter():
    # create two sessions
    client.post("/api/sessions/", json={"user_id": "userA", "prompt": "p1"})
    client.post("/api/sessions/", json={"user_id": "userB", "prompt": "p2"})
    res = client.get("/api/sessions/?user_id=userA")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert all(s["user_id"] == "userA" for s in data)
