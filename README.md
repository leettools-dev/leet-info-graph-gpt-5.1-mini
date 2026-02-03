# leet-info-graph-gpt-5.1-mini

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Research Infograph Assistant

1. Purpose

Build a full-stack web app with Gmail OAuth login that lets users ask for web research, 
generates an infographic, and provides a library to browse past infographics and related sources.

## Features

- Basic backend API with in-memory stores for Users, ResearchSessions, Sources, and Infographics. Endpoints:
  - POST /api/users - create user
  - GET /api/users/{user_id} - get user
  - POST /api/sessions - create research session
  - GET /api/sessions/{session_id} - get session
  - POST /api/sessions/{session_id}/sources - add source
  - GET /api/sessions/{session_id}/sources - list sources
  - POST /api/sessions/{session_id}/infographic - generate simple SVG infographic (data URL)
  - GET /api/sessions/{session_id}/infographic - get infographic

Usage examples:

- Create a user and a session, add sources, and generate an infographic using the API endpoints. See src/leet_apps/tests/test_api_main.py for an end-to-end test example.
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
