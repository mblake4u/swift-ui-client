# swift-ui-client

FastAPI + HTMX dashboard for the Swift Alliance Cloud API. Provides a
business-focused interface to Swift distributions data, with live auto-refreshing
via HTMX and a JSON API layer ready for a future React frontend.

Part of the **[SwiftOps](https://github.com/mblake4u/swiftops)** stack — requires
[`swift-token-server`](https://github.com/mblake4u/swift-token-server) running
on port 82.

> **Status note (2026-05):** SwiftOps closed out as an open-source portfolio piece. This dashboard continues to work. See the [SwiftOps devlog](https://github.com/mblake4u/swiftops/blob/main/docs/DEVLOG.md) for the full project arc.

## Features

- Live distributions list — auto-refreshes every 30 seconds
- Distribution detail pages
- Stack status indicator (token server + Swagger UI health)
- JSON API endpoints at `/api/*` for programmatic access or future React migration
- Dark monospace UI, no npm build step

## Quick start

```bash
# Run the full stack (token-server + swagger-ui + ui-client + mcp-gateway)
cd ~/dev/github/mblake4u/swiftops && docker compose up -d

# Or run ui-client standalone (requires token-server accessible)
docker run -d \
  --name swift-ui-client \
  -e PROXY_BASE_URL=http://localhost:82/proxy \
  -e TOKEN_SERVER_URL=http://localhost:82 \
  -e SWAGGER_UI_URL=http://localhost:83 \
  -p 84:8080 \
  everyday-ai/swift-ui-client:v0.1.0-dev
```

Open `http://localhost:84` in your browser.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `PROXY_BASE_URL` | `http://localhost:82/proxy` | Swift API proxy base URL |
| `TOKEN_SERVER_URL` | `http://localhost:82` | Token server base URL (for health checks) |
| `SWAGGER_UI_URL` | `http://localhost:83` | Swagger UI URL (for health checks) |

Inside Docker Compose, these are set to use internal service names automatically.

## Build

```bash
docker build -t everyday-ai/swift-ui-client:v0.1.0-dev .
```

## Smoke tests

```bash
pip install pytest httpx
pytest tests/ -v
# or against a specific host:
pytest tests/ -v --base-url http://localhost:84
```

## API endpoints

| Endpoint | Type | Description |
|---|---|---|
| `GET /health` | JSON | Health check |
| `GET /api/status` | JSON | Stack component status |
| `GET /api/distributions` | JSON | Distributions list (proxied) |
| `GET /` | HTML | Dashboard |
| `GET /distributions/{id}` | HTML | Distribution detail |
| `GET /partials/status` | HTML fragment | HTMX status indicator |
| `GET /partials/distributions` | HTML fragment | HTMX distributions table |

FastAPI also auto-generates interactive docs at `/docs`.

## Versioning

| Tag | Environment |
|---|---|
| `vX.Y.Z-dev` | gentoo-x13 (development) |
| `vX.Y.Z-staging` | Windows home lab |
| `vX.Y.Z` (date) | Production / hosting provider |

## Related

- [`swiftops`](https://github.com/mblake4u/swiftops) — orchestration repo + project hub + devlog
- [`swift-token-server`](https://github.com/mblake4u/swift-token-server) — OAuth token service and proxy (required)
- [`swift-swagger-ui`](https://github.com/mblake4u/swift-swagger-ui) — Swagger UI for the API spec
- [`swift-mcp-gateway`](https://github.com/mblake4u/swift-mcp-gateway) — MCP server exposing Swift API as Claude tools
- [Swift Developer Portal](https://developer.swift.com)
- [ADR-001: Python UI Client Stack](docs/ADR-001-python-ui-client-stack.md)
