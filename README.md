# leet-info-graph-gpt-5.1-mini

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Research Infograph Assistant

1. Purpose

Build a full-stack web app with Gmail OAuth login that lets users ask for web research, 
generates an infographic, and provides...

## Features

- Infographic generation (MVP): POST /api/infographics/generate accepts a prompt, optional stats and bullets, and returns SVG/PNG image URLs. The generator produces a simple template with title, stats, bullets and source list. Usage example:

  POST /api/infographics/generate
  {
    "session_id": "s1",
    "prompt": "Summarize current EV market trends",
    "stats": [{"label":"EV Sales", "value": 42}],
    "bullets": ["Battery costs falling", "Charging infrastructure expanding"],
    "sources": [{"title":"A","url":"https://a","snippet":"..."}]
  }

- Export: /api/sessions/{session_id}/export and /api/sessions/{session_id}/export/infographic provide JSON exports and image streaming (PNG/SVG placeholders for demo).
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
