from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.leet_apps.api.infographics import router as infographics_router

app = FastAPI()
app.include_router(infographics_router)

client = TestClient(app)


def test_generate_and_fetch_svg():
    payload = {"session_id": "s1", "prompt": "EV market trends", "sources": [{"title":"a","url":"https://a","snippet":"s"}]}
    res = client.post("/api/infographics/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    inf_id = data["id"]

    res2 = client.get(f"/api/infographics/{inf_id}/image?format=svg")
    assert res2.status_code == 200
    assert "<svg" in res2.text


def test_fetch_png_placeholder():
    payload = {"session_id": "s2", "prompt": "Short prompt", "sources": []}
    res = client.post("/api/infographics/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    inf_id = data["id"]

    res2 = client.get(f"/api/infographics/{inf_id}/image?format=png")
    assert res2.status_code == 200
    assert res2.headers["content-type"] == "image/png"
