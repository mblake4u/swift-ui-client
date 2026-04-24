import pytest

def pytest_addoption(parser):
    parser.addoption("--base-url", default="http://localhost:84", help="UI client base URL")

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")
