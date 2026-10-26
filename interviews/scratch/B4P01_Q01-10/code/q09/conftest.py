import pytest
from churn import make_data

def pytest_configure(config):
    for m in ("unit", "data", "model", "integration"):
        config.addinivalue_line("markers", f"{m}: {m} tests")

@pytest.fixture(scope="session")
def df():
    return make_data()
