import pytest


def pytest_addoption(parser):
    parser.addoption("--base-url", default="http://localhost:84", help="UI client base URL")
    parser.addoption("--run-live", action="store_true", default=False,
                     help="Run tests that require a live proxy (swift-token-server on port 82)")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")


@pytest.fixture(scope="session")
def run_live(request):
    return request.config.getoption("--run-live")
