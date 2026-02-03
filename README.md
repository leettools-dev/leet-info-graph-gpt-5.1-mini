# leet-info-graph-gpt-5.1-mini

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Research Infograph Assistant

1. Purpose

Build a full-stack web app with Gmail OAuth login that lets users ask for web research, 
generates an infographic, and provides...

## Features

Phase 1 completed (demo):

- OAuth: Gmail OAuth endpoints implemented (start login, callback simulation, me/logout). Configure GOOGLE_OAUTH_CLIENT_ID and optionally GOOGLE_OAUTH_CLIENT_SECRET and GOOGLE_OAUTH_REDIRECT_URI as environment variables. For local development the callback can simulate a token exchange when GOOGLE_OAUTH_CLIENT_SECRET is set.
- Chat UI: Minimal demo chat UI at src/leet_apps/ui/index.html wired to messages API for sending and listing messages.
- Sessions: ResearchSession CRUD implemented with endpoints to create, list, get, update, run (runs mock pipeline), and export session data.
- Search: Mock web search endpoint at /api/search with in-memory cache (10 minute TTL) and per-client rate limiting (10 requests per 60s). Utility endpoint to clear cache for testing: POST /api/search/cache/clear.
- Infographics: Generate deterministic SVG infographics via /api/infographics/generate and fetch image bytes via /api/infographics/{id}/image (SVG streaming). Sessions.run invokes the generator and associates an infographic with the session.

Usage examples:

- Start OAuth flow (returns Google auth URL):
  GET /api/auth/login

- Simulate OAuth callback (development):
  GET /api/auth/callback?code=abc123

- Create a research session:
  POST /api/sessions/  {"user_id":"<user-id>", "prompt":"Summarize current EV market trends"}

- Run the session (mock pipeline):
  POST /api/sessions/{session_id}/run

- Fetch generated infographic metadata/image:
  GET /api/sessions/{session_id}/infographic
  GET /api/infographics/{infographic_id}/image?format=svg

Testing:

- Unit tests are provided under src/leet_apps/tests. They are written for pytest. If running locally, install test requirements (pytest, fastapi, httpx) and run:

  pip install -r requirements-dev.txt
  pytest -q src/leet_apps/tests/

Configuration:

- Keep secrets out of repo. Set the following environment variables for OAuth and local testing:
  - GOOGLE_OAUTH_CLIENT_ID
  - GOOGLE_OAUTH_CLIENT_SECRET (optional for development simulation)
  - GOOGLE_OAUTH_REDIRECT_URI (optional; default http://localhost:8000/api/auth/callback)

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
