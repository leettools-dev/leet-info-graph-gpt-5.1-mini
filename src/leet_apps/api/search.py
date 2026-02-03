from datetime import datetime, timedelta
from typing import List, Dict
from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/search")

# Simple in-memory cache for fetched sources keyed by query.
# Each cache entry stores the results and an expires_at timestamp.
_cache: Dict[str, Dict] = {}

# Simple in-memory rate limiter per client IP. Stores list of request timestamps.
_rate_limits: Dict[str, List[float]] = {}

# Configuration
CACHE_TTL_SECONDS = 600  # 10 minutes
RATE_LIMIT_MAX = 10  # max requests
RATE_LIMIT_WINDOW_SECONDS = 60  # per 60s window


class Source(BaseModel):
    title: str
    url: str
    snippet: str
    fetched_at: datetime
    confidence: float


@router.get("/", response_model=List[Source])
async def search(request: Request, query: str = Query(..., min_length=1)):
    """
    Mock web search endpoint that returns a list of sources for a given query.
    - Uses an in-memory cache with TTL to avoid repeated work for the same query.
    - Enforces a basic per-client rate limit to prevent abuse in the demo.
    - In production this would call a search engine, fetch pages, parse and summarize them.
    """
    q = query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="query parameter is required")

    # Determine client id for rate limiting
    client = getattr(request, "client", None)
    client_ip = getattr(client, "host", None) or "testclient"

    # Rate limiting: keep timestamps and enforce sliding window
    now_ts = datetime.utcnow().timestamp()
    timestamps = _rate_limits.setdefault(client_ip, [])
    # Prune old timestamps
    window_start = now_ts - RATE_LIMIT_WINDOW_SECONDS
    timestamps = [t for t in timestamps if t >= window_start]
    if len(timestamps) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    timestamps.append(now_ts)
    _rate_limits[client_ip] = timestamps

    # Return cached result if available and not expired
    entry = _cache.get(q)
    if entry and entry.get("expires_at") > datetime.utcnow():
        return entry["results"]

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

    _cache[q] = {"results": results, "expires_at": now + timedelta(seconds=CACHE_TTL_SECONDS)}
    return results


@router.post("/cache/clear")
async def clear_cache(query: str | None = None):
    """Utility endpoint (demo/testing) to clear the cache for a specific query or all cache."""
    if query:
        _cache.pop(query, None)
    else:
        _cache.clear()
    return {"status": "ok"}
