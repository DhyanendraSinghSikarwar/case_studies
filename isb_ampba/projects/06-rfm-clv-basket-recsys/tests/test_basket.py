"""Tests for market-basket mining."""
from __future__ import annotations

from crm.basket import build_basket_matrix, run_basket


def test_basket_matrix_is_boolean_per_invoice(sales):
    m = build_basket_matrix(sales, top_items=30)
    assert m.shape[0] <= sales["invoice"].nunique()
    assert m.shape[1] <= 30
    assert (m.sparse.to_dense().sum(axis=1) >= 1).all()


def test_rules_respect_thresholds_and_bundles_unique(sales, fast_cfg):
    out = run_basket(sales, fast_cfg)
    b = fast_cfg["basket"]
    r = out["rules"]
    assert len(r) > 0
    assert (r["lift"] > b["min_lift"]).all() and (r["confidence"] > b["min_confidence"]).all()
    bun = out["bundles"]
    assert 0 < len(bun) <= b["top_bundles"]
    assert bun["items"].is_unique
    assert bun["lift"].is_monotonic_decreasing
