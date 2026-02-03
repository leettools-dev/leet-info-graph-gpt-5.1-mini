# leet-info-graph-gpt-5.1-mini

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Research Infograph Assistant

1. Purpose

Build a full-stack web app with Gmail OAuth login that lets users ask for web research, 
generates an infographic, and provides...

## Features

- History: sessions can be filtered by topic, date range, and tags via API parameters (topic, start_date, end_date, tags). Usage examples: GET /api/sessions?topic=ev&start_date=2026-01-01T00:00:00&end_date=2026-02-01T00:00:00&tags=market,analysis

- OAuth: Gmail OAuth helper endpoints in /api/auth to start login and handle callback (simulated in local dev)
- Sessions: create/list/update research sessions with filters (topic, date range, tags)
- Search: mock search endpoint with in-memory cache
- Infographic: placeholder infographic generation when running session pipeline
- Messages: chat messages stored per session
- UI: minimal static index.html under src/leet_apps/ui for demo
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
