# Implementation Guide

This file explains the project layout and where to implement features for the Research Infograph Assistant.

Conventions
- UI code: src/leet_apps/ui (Single Page App, static assets, and build output)
- Backend API: src/leet_apps/api (FastAPI routers grouped by responsibility)
- Config: src/leet_apps/config.yaml (project-level configuration; do not store secrets here)
- Tests: src/leet_apps/tests (pytest test suite for backend and integration tests)

Quick start
1. Backend
   - FastAPI routers live under src/leet_apps/api. Add new endpoints by creating modules and an APIRouter with a prefix. Keep business logic small in routers and factor reusable logic into modules.
2. UI
   - Place the SPA source (React/Vue/Svelte) under src/leet_apps/ui/src and compiled output under src/leet_apps/ui/dist for distribution. For demos, a minimal static index.html can live under src/leet_apps/ui.
3. Config
   - Keep non-secret configuration in src/leet_apps/config.yaml. Load secrets (OAuth client secrets, DB passwords) from environment variables or a secrets manager at runtime.

Testing
- Add pytest tests to src/leet_apps/tests following the existing pattern.
- Tests should cover happy paths, edge cases and error handling.

Security and secrets
- Never commit client secrets or API keys to the repository. Use environment variables or a secrets manager in CI/CD.

Notes specific to this project
- OAuth: src/leet_apps/api/auth.py provides a simple Gmail OAuth flow helper. Configure GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_REDIRECT_URI in the environment. If GOOGLE_OAUTH_CLIENT_SECRET is set, the callback simulates a token exchange for local testing.
- Infographic generation: Implement template-based rendering in a worker or background job. For the prototype, a placeholder image URL is created by sessions.run.
- Search/ingest: src/leet_apps/api/search.py contains a mock search with in-memory cache; replace with a fetch-and-parse pipeline when integrating a real search provider.

Developer checklist
- [ ] Implement UI skeleton in src/leet_apps/ui
- [ ] Provide config.yaml with placeholders
- [ ] Write tests for new modules
- [ ] Keep secrets out of the repo
