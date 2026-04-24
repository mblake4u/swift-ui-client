# ADR-001 — Python UI Client Stack

| Field | Value |
|---|---|
| **Date** | 2026-04-24 |
| **Status** | Accepted |
| **Deciders** | mblake4u |

---

## Context

Option C (proxy endpoint) is complete. The stack now has:
- `swift-token-server` (port 82) — auth + proxy
- `swift-swagger-ui` (port 83) — API spec browser

The next roadmap item is a Python UI client (3rd container) that provides a targeted,
business-focused interface to the Swift Alliance Cloud API — beyond what the Swagger spec
browser offers. It also serves as the FastAPI evaluation (roadmap item 5).

## Decision

Build a **FastAPI + HTMX** single-container dashboard on port 84.

## Options Considered

| Option | Pros | Cons | Decision |
|---|---|---|---|
| FastAPI + HTMX | Python-native, no build step, evaluates FastAPI, simple Docker story | Less frontend portfolio signal | **Selected** |
| FastAPI + React | Separation of concerns, shows React skills | Two build processes, JS ecosystem in a Python project | Deferred — add React frontend later if needed |
| Next.js | Good Vercel story | Node.js runtime, loses FastAPI evaluation, misaligns with Python positioning | Rejected |
| Flask + Jinja2 | Familiar | Doesn't evaluate FastAPI, no async | Rejected |

## Rationale

- **FastAPI** evaluates roadmap item 5 in a real workload. Auto-generates `/docs` (OpenAPI)
  for free — fitting for an API-focused portfolio project.
- **HTMX** provides live-updating UI (auto-refreshing distributions list) without npm,
  webpack, or a build step. Single container stays simple.
- **Port 84** continues the established port sequence (82, 83, 84).
- **Async HTTP via httpx** — consistent with FastAPI's async model; calls the proxy at
  `http://swift-token-server:8080` within the Docker network.

## Consequences

- FastAPI replaces Flask for new services going forward (evaluation complete on first use).
- `localhost:82` proxy URL becomes `http://swift-token-server:8080` inside Docker network;
  configurable via `PROXY_BASE_URL` env var.
- React frontend remains an option — FastAPI JSON endpoints are already in place when needed.
- Vercel deployment: the FastAPI backend needs a container host (not Vercel). A React or
  static frontend can be split out to Vercel for public demo later.
