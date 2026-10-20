"""Tests for data loading, cleaning and time splits."""
from __future__ import annotations

import pandas as pd

from crm.data import clean, make_fixture, split_calibration_holdout


def test_clean_removes_junk(raw, cfg):
    sales, returns = clean(raw, cfg)
    assert (sales["quantity"] > 0).all() and (sales["unit_price"] > 0).all()
    assert not sales["invoice"].str.startswith("C").any()
    assert not sales["stock_code"].isin(cfg["data"]["non_product_codes"]).any()
    assert sales["customer_id"].notna().all()
    assert len(returns) >= 1 and returns["invoice"].str.startswith("C").all()
    assert (sales["revenue"] - sales["quantity"] * sales["unit_price"]).abs().max() < 1e-9


def test_split_is_strictly_time_ordered(sales, cfg):
    cal, hold = split_calibration_holdout(sales, cfg)
    assert cal["invoice_date"].max() < pd.Timestamp("2011-07-01")
    assert hold["invoice_date"].min() >= pd.Timestamp("2011-07-01")
    assert hold["invoice_date"].max() < pd.Timestamp("2011-12-10")
    assert len(cal) + len(hold) <= len(sales)


def test_fixture_is_deterministic():
    a, b = make_fixture(50, 20, seed=1), make_fixture(50, 20, seed=1)
    pd.testing.assert_frame_equal(a, b)
    assert not a.equals(make_fixture(50, 20, seed=2))
