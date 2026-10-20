"""Tests for BG/NBD + Gamma-Gamma CLV, including the no-holdout-leakage check."""
from __future__ import annotations

import pandas as pd
import pytest

from crm.clv import calibration_summary, holdout_actuals, run_clv

CUT = pd.Timestamp("2011-06-30")


def test_no_holdout_leakage_into_clv(cal_hold, cfg):
    """Predictions must be identical whatever happens in the holdout window."""
    cal, hold = cal_hold
    a = run_clv(cal, hold, cfg)
    wild = hold.copy()
    wild["revenue"] *= 1000
    b = run_clv(cal, wild, cfg)
    pd.testing.assert_frame_equal(a["pred_holdout"], b["pred_holdout"])
    pd.testing.assert_frame_equal(a["pred_12m"], b["pred_12m"])
    assert a["actuals"]["actual_spend"].sum() * 1000 == pytest.approx(b["actuals"]["actual_spend"].sum())
    b2 = run_clv(cal, hold.iloc[0:0], cfg)                      # empty holdout
    pd.testing.assert_frame_equal(a["pred_holdout"], b2["pred_holdout"])


def test_calibration_summary_rejects_future_rows(sales):
    with pytest.raises(AssertionError):
        calibration_summary(sales, CUT)                         # full sales extend beyond cutoff


def test_predictions_are_sane(cal_hold, cfg):
    o = run_clv(*cal_hold, cfg)
    p = o["pred_holdout"]
    assert (p["pred_purchases"] >= 0).all() and (p["pred_clv"] >= 0).all()
    assert p["p_alive"].between(0, 1).all()
    assert o["pred_12m"]["pred_purchases"].mean() > p["pred_purchases"].mean()   # longer horizon
    m = o["metrics"]
    assert 0 < m["top_decile"]["share_of_predicted_clv"] <= 1
    assert m["top_decile"]["share_of_actual_spend_oracle_top_decile"] >= m["top_decile"][
        "share_of_actual_holdout_spend"]
    assert {"mae_spend", "spearman_spend"} <= set(m["model"])


def test_holdout_actuals_counts_days_not_lines(cal_hold):
    _, hold = cal_hold
    idx = pd.Index(sorted(hold["customer_id"].unique()))
    act = holdout_actuals(hold, idx)
    cid = idx[0]
    exp_days = hold[hold["customer_id"] == cid]["invoice_date"].dt.normalize().nunique()
    assert act.loc[cid, "actual_purchases"] == exp_days
    assert act["actual_spend"].sum() == pytest.approx(hold["revenue"].sum())
