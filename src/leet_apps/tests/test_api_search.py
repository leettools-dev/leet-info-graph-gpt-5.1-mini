from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.leet_apps.api.search import router as search_router

app = FastAPI()
app.include_router(search_router)

client = TestClient(app)


def test_search_requires_query():
    res = client.get("/api/search/")
    assert res.status_code == 422  # missing query parameter


def test_search_returns_results_and_caches():
    res = client.get("/api/search/?query=ev trends")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Call again and ensure deterministic results
    res2 = client.get("/api/search/?query=ev trends")
    assert res2.status_code == 200
    assert res2.json() == data
