# leet-info-graph-gpt-5.1-mini

> This project is being developed by an autonomous coding agent.

## Overview

Product Requirements Document: Research Infograph Assistant

1. Purpose

Build a full-stack web app with Gmail OAuth login that lets users ask for web research, 
generates an infographic, and provides...

## Features

- Search: Added caching (TTL) and per-client rate limiting to the mock search endpoint (/api/search). Cache TTL is 10 minutes and rate limit default is 10 requests per 60s window. Utility endpoint to clear cache for testing is available at POST /api/search/cache/clear.
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
