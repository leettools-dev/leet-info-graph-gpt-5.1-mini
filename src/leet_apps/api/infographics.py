from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel, Field
import uuid

router = APIRouter(prefix="/api/infographics")

# In-memory store for infographics and image bytes
_images: Dict[str, bytes] = {}
_infographics: Dict[str, Dict[str, Any]] = {}


class Stat(BaseModel):
    label: str
    value: float


class InfographicCreate(BaseModel):
    session_id: Optional[str]
    title: str
    stats: List[Stat] = Field(default_factory=list)
    bullets: List[str] = Field(default_factory=list)
    template: Optional[str] = "basic_v1"


class InfographicMeta(BaseModel):
    id: str
    session_id: Optional[str]
    image_url: str
    layout_meta: Dict[str, Any]
    created_at: datetime


def _create_svg(title: str, stats: List[Dict[str, Any]], bullets: List[str]) -> str:
    """
    Very small deterministic SVG generator for demo purposes.
    Lays out title, a simple bar chart for stats, and bullets.
    """
    width = 800
    height = 420 + max(0, len(bullets) * 20)
    bg = "#ffffff"
    title_y = 40
    svg_parts = [f'<?xml version="1.0" encoding="UTF-8"?>',
                 f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
                 f'<rect width="100%" height="100%" fill="{bg}"/>',
                 f'<text x="40" y="{title_y}" font-family="Arial" font-size="24" fill="#111">{title}</text>']

    # Draw simple bars for stats
    if stats:
        max_val = max(s.get('value', 0) for s in stats) or 1
        bar_x = 40
        bar_y = 80
        bar_height = 20
        gap = 10
        for i, s in enumerate(stats):
            label = s.get('label', '')
            val = float(s.get('value', 0))
            bar_width = int((width - 160) * (val / max_val))
            y = bar_y + i * (bar_height + gap)
            svg_parts.append(f'<text x="{bar_x}" y="{y+14}" font-family="Arial" font-size="12" fill="#333">{label}</text>')
            svg_parts.append(f'<rect x="{bar_x+200}" y="{y}" width="{bar_width}" height="{bar_height}" fill="#4f8ef7" rx="4"/>')
            svg_parts.append(f'<text x="{bar_x+210+bar_width}" y="{y+14}" font-family="Arial" font-size="12" fill="#111">{val:.1f}</text>')

    # Bullets
    bullets_x = 40
    bullets_y = 80 + max(0, len(stats)) * (bar_height + gap) + 40
    for idx, b in enumerate(bullets):
        y = bullets_y + idx * 20
        svg_parts.append(f'<text x="{bullets_x}" y="{y}" font-family="Arial" font-size="14" fill="#222">• {b}</text>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


@router.post("/generate", response_model=InfographicMeta)
async def generate_infographic(payload: InfographicCreate = Body(...)):
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=400, detail="title is required")

    info_id = str(uuid.uuid4())
    svg = _create_svg(payload.title, [s.dict() for s in payload.stats], payload.bullets)
    svg_bytes = svg.encode("utf-8")

    _images[info_id] = svg_bytes
    meta = {
        "id": info_id,
        "session_id": payload.session_id,
        "image_url": f"/api/infographics/{info_id}/image",
        "layout_meta": {"template": payload.template},
        "created_at": datetime.utcnow(),
    }
    _infographics[info_id] = meta
    return meta


@router.get("/{infographic_id}", response_model=InfographicMeta)
async def get_infographic(infographic_id: str):
    meta = _infographics.get(infographic_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Infographic not found")
    return meta


from fastapi.responses import StreamingResponse
import io


@router.get("/{infographic_id}/image")
async def get_infographic_image(infographic_id: str, format: str = Query("svg", regex="^(svg|png)$")):
    # For demo, we only have SVG bytes. If png requested, return 415
    svg_bytes = _images.get(infographic_id)
    if not svg_bytes:
        raise HTTPException(status_code=404, detail="Infographic image not found")
    if format == "svg":
        return StreamingResponse(io.BytesIO(svg_bytes), media_type="image/svg+xml")
    else:
        raise HTTPException(status_code=415, detail="PNG export not implemented in demo")


# Helper for other modules to create an infographic from a prompt/session
async def create_from_prompt(session_id: str, prompt: str):
    # Create a simple title and two mock stats derived deterministically from prompt
    title = f"{prompt.strip().capitalize()} - Summary"
    # create deterministic numeric values using hash of prompt
    h = abs(hash(prompt))
    stat1 = {"label": "Key stat A", "value": float((h % 100) + 10)}
    stat2 = {"label": "Key stat B", "value": float(((h // 2) % 100) + 5)}
    bullets = [f"Summary point about {prompt.split()[0] if prompt.split() else 'topic'}.", "Further context and references included."]
    payload = InfographicCreate(session_id=session_id, title=title, stats=[Stat(**stat1), Stat(**stat2)], bullets=bullets)
    meta = await generate_infographic(payload)
    return meta
