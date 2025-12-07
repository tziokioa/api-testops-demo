import pytest

def pytest_addoption(parser):
    # We switch to JSONPlaceholder because it requires NO API KEY
    parser.addoption("--baseline", action="store", default="https://jsonplaceholder.typicode.com")
    parser.addoption("--candidate", action="store", default="https://jsonplaceholder.typicode.com")
    # A simple endpoint that returns a small JSON object
    parser.addoption("--endpoint", action="store", default="/todos/1")

@pytest.fixture
def config(request):
    return {
        "baseline": request.config.getoption("--baseline"),
        "candidate": request.config.getoption("--candidate"),
        "endpoint": request.config.getoption("--endpoint")
    }