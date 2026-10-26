def pytest_configure(config):
    config.addinivalue_line("markers", "quarantine: known-flaky test, excluded from the PR gate (run nightly)")
