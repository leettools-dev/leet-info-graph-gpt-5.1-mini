# leet-info-graph-gpt-5.1-mini

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Research Infograph Assistant

1. Purpose

Build a full-stack web app with Gmail OAuth login that lets users ask for web research, 
generates an infographic, and provides...

## Features

- UI: Minimal SPA demo page (src/leet_apps/ui/index.html) with a simple chat interface wired to /api/messages endpoints. Accessible at / (serves static index.html).

- Backend: REST API endpoints for auth, users, sessions, search, messages (mock implementations) that support OAuth demo flow, session CRUD, mock search pipeline, and infographic placeholders.
- In-memory stores for rapid prototyping (replace with DB in production).
- UI: Minimal SPA demo page (src/leet_apps/ui/index.html) with a chat interface wired to /api/messages endpoints.
- Tests: pytest test suite under src/leet_apps/tests covering endpoints and mock pipelines.

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
