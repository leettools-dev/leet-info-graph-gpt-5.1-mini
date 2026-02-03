# leet-info-graph-gpt-5.1-mini

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Research Infograph Assistant

1. Purpose

Build a full-stack web app with Gmail OAuth login that lets users ask for web research, 
generates an infographic, and provides...

## Features

- Auth: Gmail OAuth demo endpoints (POST /api/auth/login, GET /api/auth/callback, GET /api/auth/me, POST /api/auth/logout). Simulated token exchange for local development when GOOGLE_OAUTH_CLIENT_SECRET is set; safe placeholder mode when not set.
- Backend: FastAPI REST endpoints for users, sessions, search, messages with in-memory stores for rapid prototyping (src/leet_apps/api).
- UI: Minimal SPA demo page (src/leet_apps/ui/index.html) with a simple chat UI wired to /api/messages endpoints.
- Sessions: Create, list, update, run (mock research pipeline), export session JSON and infographic metadata (src/leet_apps/api/sessions.py).
- Search: Mock search endpoint with simple in-memory cache to avoid repeated fetches (src/leet_apps/api/search.py).
- Tests: pytest test suite under src/leet_apps/tests covering endpoints and mock pipelines.

Usage examples:
- Start OAuth flow (demo): POST /api/auth/login -> returns Google authorization URL (requires GOOGLE_OAUTH_CLIENT_ID env var).
- Create a session: POST /api/sessions/ { user_id, prompt }
- Run a session (mock pipeline): POST /api/sessions/{session_id}/run
- View messages: GET /api/messages/session/{session_id}

Configuration notes:
- Set GOOGLE_OAUTH_CLIENT_ID and optionally GOOGLE_OAUTH_CLIENT_SECRET and GOOGLE_OAUTH_REDIRECT_URI for OAuth demo flows.
- Do not commit secrets to the repository; use environment variables or a secrets manager.

## Getting Started

### Prerequisites

Environment variables required for OAuth and local development:

- GOOGLE_OAUTH_CLIENT_ID: OAuth client ID from Google Cloud Console.
- GOOGLE_OAUTH_CLIENT_SECRET: OAuth client secret (optional for local development; if set, auth callback will simulate a token exchange).
- GOOGLE_OAUTH_REDIRECT_URI: Redirect URI configured for the OAuth client (defaults to http://localhost:8000/api/auth/callback).

Note: Do NOT commit secrets to the repository. Use a secrets manager or environment variables in CI/CD.

### Installation

```bash
# Installation instructions will be added
```

### Usage

```bash
# Usage examples will be added
```

## Development

See .leet/.todos.json for the current development status.

## Testing

```bash
# Test instructions will be added
```

## License

MIT
