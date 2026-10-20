"""Shared offline fixtures: synthetic Online Retail II-like data and a fast config."""
from __future__ import annotations

import copy

import pytest

from crm.config import load_config
from crm.data import clean, make_fixture, split_calibration_holdout


@pytest.fixture(scope="session")
def cfg() -> dict:
    """Project config."""
    return load_config()


@pytest.fixture(scope="session")
def fast_cfg(cfg) -> dict:
    """Config with tiny grids so the full pipeline runs in seconds on the fixture."""
    c = copy.deepcopy(cfg)
    c["cluster"].update({"k_max": 5, "hdbscan_min_cluster_size": 10})
    c["basket"].update({"support_grid": [0.05, 0.03, 0.02, 0.01], "target_rules": 5, "top_items": 60})
    c["recsys"].update({"als_grid": {"factors": [8], "regularization": [0.1], "alpha": [5],
                                     "iterations": [5]},
                        "hybrid_weights": [0.0, 0.3], "bootstrap": 20})
    return c


@pytest.fixture(scope="session")
def raw():
    """Raw synthetic frame (with junk rows)."""
    return make_fixture(n_customers=300, n_items=60, seed=42)


@pytest.fixture(scope="session")
def sales(raw, cfg):
    """Cleaned synthetic sales."""
    s, _ = clean(raw, cfg)
    return s


@pytest.fixture(scope="session")
def cal_hold(sales, cfg):
    """(calibration, holdout) split of the fixture."""
    return split_calibration_holdout(sales, cfg)
