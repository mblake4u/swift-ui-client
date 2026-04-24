import httpx
import pytest


def test_health(base_url):
    r = httpx.get(f"{base_url}/health", timeout=5)
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_root_returns_html(base_url):
    r = httpx.get(f"{base_url}/", timeout=5)
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_distributions_api_reaches_proxy(base_url, run_live):
    if not run_live:
        pytest.skip("requires swift-token-server proxy (pass --run-live)")
    r = httpx.get(f"{base_url}/api/distributions", timeout=15)
    assert r.status_code < 500, f"Unexpected server error: {r.status_code}"
