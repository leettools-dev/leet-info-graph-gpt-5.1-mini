from datetime import datetime
import uuid
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Response, Body
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/infographics")

# Simple in-memory stores for demo purposes
_infographics: Dict[str, Dict[str, Any]] = {}
_images: Dict[str, bytes] = {}


class Stat(BaseModel):
    label: str
    value: float


class InfographicCreate(BaseModel):
    session_id: Optional[str] = None
    title: Optional[str] = None
    prompt: Optional[str] = None
    stats: List[Stat] = Field(default_factory=list)
    bullets: List[str] = Field(default_factory=list)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    template: Optional[str] = "simple_v1"


class InfographicMeta(BaseModel):
    id: str
    session_id: Optional[str]
    image_url: str
    layout_meta: Dict[str, Any]
    created_at: datetime


SVG_TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600'>
  <style>
    .title {{ font: bold 24px sans-serif; }}
    .body {{ font: 14px sans-serif; }}
    .stat {{ font: 20px sans-serif; fill: #222; }}
    .bullet {{ font: 14px sans-serif; }}
    .source {{ font: 12px sans-serif; fill: #555; }}
  </style>
  <rect width='100%' height='100%' fill='#ffffff' />
  <text x='40' y='60' class='title'>Infographic: {title}</text>
  <text x='40' y='100' class='body'>Prompt: {prompt}</text>
  <g transform='translate(40,140)'>
    <!-- Stats block -->
    {stats_block}
  </g>
  <g transform='translate(320,140)'>
    <!-- Bullets block -->
    {bullets_block}
  </g>
  <g transform='translate(40,420)'>
    <text class='source'>Sources:</text>
    {sources}
  </g>
</svg>
"""

# Minimal valid PNG bytes for placeholder
MIN_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\x0cIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _render_stats(stats: List[Dict[str, Any]]) -> str:
    lines = []
    y = 0
    for s in stats[:4]:
        label = s.get('label', '')
        value = s.get('value', '')
        lines.append(f"<text x='0' y='{y}' class='stat'>{label}: {value}</text>")
        y += 30
    return "\n    ".join(lines)


def _render_bullets(bullets: List[str]) -> str:
    lines = []
    y = 0
    for b in bullets[:8]:
        lines.append(f"<text x='0' y='{y}' class='bullet'>- {b}</text>")
        y += 20
    return "\n    ".join(lines)


def _render_sources(sources: List[Dict[str, Any]]) -> str:
    lines = []
    y = 20
    for s in sources[:4]:
        lines.append(f"<text x='0' y='{y}' class='source'>{s.get('url')}</text>")
        y += 16
    return "\n    ".join(lines)


def generate_svg(title: str, prompt: str, stats: List[Dict[str, Any]], bullets: List[str], sources: List[Dict[str, Any]]) -> str:
    stats_block = _render_stats(stats)
    bullets_block = _render_bullets(bullets)
    sources_block = _render_sources(sources)
    return SVG_TEMPLATE.format(title=title, prompt=prompt, stats_block=stats_block, bullets_block=bullets_block, sources=sources_block)


@router.post("/generate", response_model=InfographicMeta)
async def generate(info: InfographicCreate = Body(...)):
    if info.title:
        title = info.title
    elif info.prompt:
        title = (info.prompt[:40] + "...") if len(info.prompt) > 40 else info.prompt
    else:
        title = "Untitled"

    prompt = info.prompt or (info.title or "")

    svg = generate_svg(title=title, prompt=prompt, stats=[s.dict() for s in info.stats], bullets=info.bullets, sources=info.sources)

    infographic_id = str(uuid.uuid4())
    created_at = datetime.utcnow()
    image_url = f"/api/infographics/{infographic_id}/image?format=svg"
    layout_meta = {"template": info.template, "source_count": len(info.sources), "stats_count": len(info.stats), "bullets_count": len(info.bullets)}

    _infographics[infographic_id] = {
        "id": infographic_id,
        "session_id": info.session_id,
        "svg": svg,
        "layout_meta": layout_meta,
        "created_at": created_at,
    }

    _images[infographic_id] = svg.encode("utf-8")

    return InfographicMeta(id=infographic_id, session_id=info.session_id, image_url=image_url, layout_meta=layout_meta, created_at=created_at)


@router.get("/{infographic_id}/image")
async def get_image(infographic_id: str, format: str = Query("svg", regex="^(svg|png)$")):
    obj = _infographics.get(infographic_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Infographic not found")

    if format == "svg":
        return Response(content=obj["svg"], media_type="image/svg+xml")
    else:
        return Response(content=MIN_PNG_BYTES, media_type="image/png")


# Helpers for other modules
async def create_infographic_for_session(session_id: str, prompt: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    payload = InfographicCreate(session_id=session_id, prompt=prompt, sources=sources)
    res = await generate(payload)
    return res.dict()


# Backwards compatible helper expected by sessions.run
async def create_from_prompt(session_id: str, prompt: str, sources: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Backwards-compatible helper used by sessions.run which expects create_from_prompt.
    Generates an infographic for the given session using provided sources or an empty list.
    """
    if sources is None:
        sources = []
    return await create_infographic_for_session(session_id=session_id, prompt=prompt, sources=sources)
