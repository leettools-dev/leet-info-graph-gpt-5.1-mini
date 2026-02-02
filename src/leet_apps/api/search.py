from datetime import datetime
from typing import List, Dict
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/search")

# Simple in-memory cache for fetched sources keyed by query.
_cache: Dict[str, List[dict]] = {}

class Source(BaseModel):
    title: str
    url: str
    snippet: str
    fetched_at: datetime
    confidence: float


@router.get("/", response_model=List[Source])
async def search(query: str = Query(..., min_length=1)):
    """
    Mock web search endpoint that returns a list of sources for a given query.
    - Uses an in-memory cache to avoid repeated work for the same query.
    - In production this would call a search engine, fetch pages, parse and summarize them.
    """
    q = query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="query parameter is required")

    # Return cached result if available
    if q in _cache:
        return _cache[q]

    now = datetime.utcnow()
    # Mock results - deterministic based on query so tests can rely on them
    results = [
        {
            "title": f"Overview of {q}",
            "url": f"https://example.com/{q.replace(' ', '-')}",
            "snippet": f"This is a short snippet summarizing {q}.",
            "fetched_at": now,
            "confidence": 0.9,
        },
        {
            "title": f"Recent news about {q}",
            "url": f"https://news.example.com/{q.replace(' ', '-')}",
            "snippet": f"Latest news and analysis on {q}.",
            "fetched_at": now,
            "confidence": 0.75,
        },
    ]

    _cache[q] = results
    return results
