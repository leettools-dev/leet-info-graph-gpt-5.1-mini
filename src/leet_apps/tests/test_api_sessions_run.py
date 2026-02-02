from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.leet_apps.api.sessions import router as sessions_router
from src.leet_apps.api.search import router as search_router

app = FastAPI()
app.include_router(sessions_router)
app.include_router(search_router)

client = TestClient(app)


def test_run_session_creates_sources_and_infographic():
    # Create a session
    res = client.post("/api/sessions/", json={"user_id": "u-run", "prompt": "ev market trends"})
    assert res.status_code == 200
    session = res.json()
    session_id = session["id"]

    # Run the research pipeline
    res2 = client.post(f"/api/sessions/{session_id}/run")
    assert res2.status_code == 200
    data = res2.json()
    assert "session" in data and "sources" in data and "infographic" in data

    sess = data["session"]
    assert sess["status"] == "completed"

    sources = data["sources"]
    assert isinstance(sources, list)
    assert len(sources) >= 1
    assert all("url" in s for s in sources)

    infographic = data["infographic"]
    assert infographic["session_id"] == session_id
    assert "image_url" in infographic

    # Fetch sources via endpoint
    res3 = client.get(f"/api/sessions/{session_id}/sources")
    assert res3.status_code == 200
    srcs = res3.json()
    assert srcs == sources

    # Fetch infographic via endpoint
    res4 = client.get(f"/api/sessions/{session_id}/infographic")
    assert res4.status_code == 200
    info = res4.json()
    assert info["session_id"] == session_id


def test_run_on_nonexistent_session_returns_404():
    res = client.post("/api/sessions/nonexistent/run")
    assert res.status_code == 404


def test_sources_for_unknown_session_returns_404():
    res = client.get("/api/sessions/nonexistent/sources")
    assert res.status_code == 404


def test_infographic_for_unknown_session_returns_404():
    res = client.get("/api/sessions/nonexistent/infographic")
    assert res.status_code == 404
