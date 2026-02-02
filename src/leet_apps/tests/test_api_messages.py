from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.leet_apps.api.messages import router as messages_router

app = FastAPI()
app.include_router(messages_router)

client = TestClient(app)


def test_create_and_get_message():
    payload = {"session_id": "s1", "role": "user", "content": "Hello"}
    res = client.post("/api/messages/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["session_id"] == "s1"
    message_id = data["id"]

    res2 = client.get(f"/api/messages/{message_id}")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["id"] == message_id


def test_list_messages_for_session():
    client.post("/api/messages/", json={"session_id": "s2", "role": "user", "content": "First"})
    client.post("/api/messages/", json={"session_id": "s2", "role": "assistant", "content": "Reply"})
    res = client.get("/api/messages/session/s2")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 2
