import numpy as np
import pandas as pd
import pytest


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="run tests marked slow")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip = pytest.mark.skip(reason="slow: use --runslow to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip)


BUILDS = []                                          # counts how often the fixture body really ran


@pytest.fixture(scope="session")
def small_df():
    BUILDS.append(1)                                 # built once per session, shared by every test
    rng = np.random.default_rng(0)
    x = rng.normal(size=(50, 2))
    return pd.DataFrame({"a": x[:, 0], "b": x[:, 1], "y": (x[:, 0] > 0).astype(int)})


@pytest.fixture(scope="session", autouse=True)
def report_builds():
    yield
    print(f"\n[session fixture small_df built {len(BUILDS)} time(s)]")
