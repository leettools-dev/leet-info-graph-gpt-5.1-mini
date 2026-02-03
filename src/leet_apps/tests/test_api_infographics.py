from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.leet_apps.api.infographics import router as inf_router, _images

app = FastAPI()
app.include_router(inf_router)

client = TestClient(app)


def test_generate_and_fetch_infographic():
    payload = {
        "session_id": "s1",
        "title": "EV Market Trends",
        "stats": [{"label": "Sales", "value": 45.2}, {"label": "Growth", "value": 12.3}],
        "bullets": ["Point one", "Point two"],
        "template": "basic_v1",
    }
    res = client.post("/api/infographics/generate", json=payload)
    assert res.status_code == 200
    meta = res.json()
    assert meta["session_id"] == "s1"
    assert "id" in meta
    info_id = meta["id"]

    # fetch meta
    res2 = client.get(f"/api/infographics/{info_id}")
    assert res2.status_code == 200
    m2 = res2.json()
    assert m2["id"] == info_id

    # fetch image as svg
    res3 = client.get(f"/api/infographics/{info_id}/image?format=svg")
    assert res3.status_code == 200
    assert res3.headers["content-type"].startswith("image/svg")

    # request unsupported png -> 415
    res4 = client.get(f"/api/infographics/{info_id}/image?format=png")
    assert res4.status_code == 415


def test_generate_without_title_fails():
    payload = {"session_id": "s2", "title": "   "}
    res = client.post("/api/infographics/generate", json=payload)
    assert res.status_code == 400
