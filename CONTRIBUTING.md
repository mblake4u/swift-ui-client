# Contributing

## Branch model

| Branch | Purpose |
|---|---|
| `dev` | Active development — target PRs here |
| `main` | Stable baseline; tagged releases only |

## Getting started

```bash
git clone https://github.com/mblake4u/swift-ui-client.git
cd swift-ui-client
```

Requires [`swift-token-server`](https://github.com/mblake4u/swift-token-server)
running on port 82 for the proxy and token endpoints.

## Running locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## Running tests

```bash
pip install pytest httpx
# Requires the container or uvicorn running on localhost:84
pytest tests/ -v
```

## Pull requests

1. Branch from `dev`: `git checkout -b feat/my-thing`
2. Keep changes focused — one concern per PR
3. Run smoke tests before opening the PR
4. For architectural changes, add or update an ADR in `docs/`

## Template variables

HTMX partials live in `app/templates/partials/`. The `TemplateResponse` API
uses `request=request, name="...", context={...}` (Starlette 0.36+ style).
