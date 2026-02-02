from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.leet_apps.api.users import router as users_router

app = FastAPI()
app.include_router(users_router)

client = TestClient(app)


def test_create_and_get_user():
    payload = {"email": "u@example.com", "name": "User"}
    res = client.post("/api/users/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "u@example.com"
    user_id = data["id"]

    res2 = client.get(f"/api/users/{user_id}")
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["id"] == user_id


def test_list_users():
    client.post("/api/users/", json={"email": "a@example.com"})
    client.post("/api/users/", json={"email": "b@example.com"})
    res = client.get("/api/users/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 2
