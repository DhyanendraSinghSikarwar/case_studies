"""Tests for RFM features, quintile scores and named segments."""
from __future__ import annotations

import pandas as pd

from crm.rfm import SEGMENTS, build_rfm, compute_rfm

ASOF = pd.Timestamp("2011-07-01")


def test_scores_in_range_and_balanced(cal_hold, cfg):
    r = build_rfm(cal_hold[0], ASOF, cfg)
    for c in ("r_score", "f_score", "m_score"):
        assert r[c].between(1, 5).all()
        counts = r[c].value_counts()
        assert counts.max() - counts.min() <= 1          # rank-based quintiles are equal-sized
    assert r["rfm_code"].str.fullmatch(r"[1-5]{3}").all()


def test_segments_valid_and_cover_everyone(cal_hold, cfg):
    r = build_rfm(cal_hold[0], ASOF, cfg)
    assert set(r["segment"]) <= set(SEGMENTS)
    assert r["segment"].notna().all()


def test_monetary_score_is_monotone(cal_hold, cfg):
    r = build_rfm(cal_hold[0], ASOF, cfg).sort_values("monetary")
    assert r["m_score"].is_monotonic_increasing
    r2 = r.sort_values("recency", ascending=False)
    assert r2["r_score"].is_monotonic_increasing        # larger recency (staler) -> lower score


def test_rfm_ignores_rows_after_snapshot(sales):
    """Adding post-snapshot rows must not change the RFM table (no look-ahead)."""
    base = compute_rfm(sales, ASOF)
    future = sales[sales["invoice_date"] >= ASOF].copy()
    future["revenue"] *= 100
    tampered = pd.concat([sales[sales["invoice_date"] < ASOF], future])
    pd.testing.assert_frame_equal(base, compute_rfm(tampered, ASOF))
