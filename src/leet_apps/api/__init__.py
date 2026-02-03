from .auth import router as auth_router
from .sessions import router as sessions_router
from .search import router as search_router

# messages router may be provided by other feature branches; include if present
try:
    from .messages import router as messages_router  # type: ignore
except Exception:
    messages_router = None

from .infographics import router as infographics_router

__all__ = ["auth_router", "sessions_router", "search_router", "infographics_router"]
if messages_router is not None:
    __all__.insert(3, "messages_router")
