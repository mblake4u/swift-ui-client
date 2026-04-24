import os
import httpx

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

PROXY_BASE_URL = os.getenv("PROXY_BASE_URL", "http://localhost:82/proxy")
TOKEN_SERVER_URL = os.getenv("TOKEN_SERVER_URL", "http://localhost:82")
SWAGGER_UI_URL = os.getenv("SWAGGER_UI_URL", "http://localhost:83")

app = FastAPI(title="SwiftOps Dashboard", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.svg", media_type="image/svg+xml")


# === JSON API ENDPOINTS ===

@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/status")
async def stack_status():
    results = {}
    async with httpx.AsyncClient(timeout=5) as client:
        for name, url in [
            ("token_server", f"{TOKEN_SERVER_URL}/health"),
            ("swagger_ui", f"{SWAGGER_UI_URL}"),
        ]:
            try:
                r = await client.get(url)
                results[name] = "ok" if r.status_code < 400 else "error"
            except Exception:
                results[name] = "error"
    return results


@app.get("/api/distributions")
async def get_distributions(limit: int = 50, offset: int = 0):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{PROXY_BASE_URL}/distributions",
            params={"limit": limit, "offset": offset},
        )
        r.raise_for_status()
        return r.json()


# === HTML PARTIAL ENDPOINTS (used by HTMX) ===

@app.get("/partials/status", response_class=HTMLResponse)
async def status_partial(request: Request):
    results = await stack_status()
    return templates.TemplateResponse(
        request=request, name="partials/status.html", context={"status": results}
    )


@app.get("/partials/distributions", response_class=HTMLResponse)
async def distributions_partial(request: Request, limit: int = 50, offset: int = 0):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{PROXY_BASE_URL}/distributions",
            params={"limit": limit, "offset": offset},
        )
        r.raise_for_status()
        data = r.json()
    return templates.TemplateResponse(
        request=request,
        name="partials/distributions.html",
        context={
            "distributions": data.get("distributions", []),
            "links": data.get("links", []),
        },
    )


# === FULL PAGE ENDPOINTS ===

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/distributions/{dist_id}", response_class=HTMLResponse)
async def distribution_detail(request: Request, dist_id: int):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{PROXY_BASE_URL}/distributions/{dist_id}")
        r.raise_for_status()
        distribution = r.json()
    return templates.TemplateResponse(
        request=request, name="distribution.html", context={"distribution": distribution}
    )
