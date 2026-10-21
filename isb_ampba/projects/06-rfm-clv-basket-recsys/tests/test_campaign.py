"""Tests for the campaign planner economics."""
from __future__ import annotations

import pandas as pd
import pytest

from crm.campaign import allocate_budget, segment_economics, sensitivity


@pytest.fixture
def seg_df():
    return pd.DataFrame({"segment": ["Champions"] * 10 + ["At-Risk"] * 20,
                         "avg_basket": [400.0] * 10 + [300.0] * 20})


def test_roi_formula_hand_computed(seg_df, cfg):
    e = segment_economics(seg_df, cfg).set_index("segment")
    a = cfg["campaign"]["actions"]["Champions"]
    contact = 10 * a["cost_per_contact"]
    incr = 10 * a["response_rate"] * 400 * a["order_value_factor"]
    gross = incr * cfg["campaign"]["gross_margin"]
    assert e.loc["Champions", "total_cost"] == pytest.approx(contact)
    assert e.loc["Champions", "roi"] == pytest.approx((gross - contact) / contact)


def test_budget_never_exceeded_and_roi_ordered(seg_df, cfg):
    e = segment_economics(seg_df, cfg)
    for budget in (0.0, 5.0, 12.0, 1e9):
        p = allocate_budget(e, budget)
        assert p["funded_total_cost"].sum() <= budget + 1e-9
        assert p["roi"].is_monotonic_decreasing
        assert p["funded_fraction"].between(0, 1).all()


def test_sensitivity_monotone_in_response_rate(seg_df, cfg):
    s = sensitivity(seg_df, cfg)
    for _, g in s.groupby("gross_margin"):
        g = g.sort_values("response_multiplier")
        assert g["net_profit"].is_monotonic_increasing
    for _, g in s.groupby("response_multiplier"):
        assert g.sort_values("gross_margin")["net_profit"].is_monotonic_increasing


def test_break_even_multiplier_is_consistent(seg_df, cfg):
    from crm.campaign import _break_even

    m = _break_even(seg_df, cfg)
    assert m is not None
    assert segment_economics(seg_df, cfg, response_mult=m)["net_profit"].sum() >= 0
    if m > 0.05:
        assert segment_economics(seg_df, cfg, response_mult=m - 0.05)["net_profit"].sum() < 0
