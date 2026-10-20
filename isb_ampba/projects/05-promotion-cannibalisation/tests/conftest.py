"""Shared offline fixtures (synthetic UCI-schema data, seed 42)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from promo.data import clean_sales, fixture_cfg, make_fixture, weekly_panel  # noqa: E402
from promo.engine import EngineContext  # noqa: E402
from promo.pipeline import build_engine_table  # noqa: E402


@pytest.fixture(scope="session")
def cfg() -> dict:
    return fixture_cfg()


@pytest.fixture(scope="session")
def raw():
    return make_fixture(seed=42)


@pytest.fixture(scope="session")
def sales_panel(raw, cfg):
    sales, returns = clean_sales(raw, cfg)
    return sales, returns, weekly_panel(sales)


@pytest.fixture(scope="session")
def engine_res(sales_panel, cfg):
    sales, _, panel = sales_panel
    return build_engine_table(sales, panel, cfg, overrides=None)


@pytest.fixture(scope="session")
def ctx(engine_res, cfg):
    return EngineContext(engine_res["table"].copy(), cfg)


@pytest.fixture()
def family():
    """A small hand-made family: baseline weekly units and prices."""
    return np.array([100.0, 80.0, 50.0]), np.array([3.0, 3.5, 2.5])
