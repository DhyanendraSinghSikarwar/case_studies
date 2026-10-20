from __future__ import annotations

import numpy as np
import pandas as pd

from credit import scorecard as sc
from credit import woe
from credit.data import TARGET, make_fixture


def test_woe_monotonic(fitted):
    sel = woe.selected_variables(fitted["bp"])
    assert sel
    assert all(woe.woe_is_monotonic(fitted["bp"], v) for v in sel)


def test_iv_filter_drops_noise(cfg):
    df = make_fixture(8000, seed=7)
    X = df[["PAY_0", "LIMIT_BAL"]].copy()
    X["noise"] = np.random.default_rng(0).normal(size=len(X))
    bp = woe.fit_binning(X, df[TARGET], cfg["scorecard"]["iv_min"])
    assert "noise" not in woe.selected_variables(bp)
    assert "PAY_0" in woe.selected_variables(bp)


def test_pd_to_score_monotonic():
    p = np.linspace(0.001, 0.999, 500)
    s = sc.pd_to_score(p)
    assert np.all(np.diff(s) <= 1e-12)


def test_pd_to_score_anchor_points():
    assert abs(float(sc.pd_to_score(1 / 51, clip=None)) - 600) < 1e-6
    assert abs(float(sc.pd_to_score(1 / 101, clip=None)) - 620) < 1e-6
    assert abs(float(sc.score_to_pd(600)) - 1 / 51) < 1e-9


def test_points_table_reproduces_score(fitted, splits):
    _, _, te = splits
    bp, lr, cols, table, feats = (fitted[k] for k in ("bp", "lr", "cols", "table", "features"))
    pdv = lr.predict_proba(woe.woe_transform(bp, te[feats])[cols])[:, 1]
    expected = sc.pd_to_score(pdv, clip=None)
    got = sc.score_with_table(bp, te[feats], table, cols)
    assert np.max(np.abs(got - expected)) <= 1.0


def test_scorecard_signs_are_negative(fitted):
    assert (fitted["lr"].coef_[0] <= 0).all()


def test_assign_band_is_ordered(cfg):
    p = np.linspace(0, 1, 1000)
    b = sc.assign_band(p, cfg["scorecard"]["band_pd_edges"])
    idx = pd.Series(b).map({c: i for i, c in enumerate(sc.BAND_LETTERS)})
    assert idx.is_monotonic_increasing and set(b) == set(sc.BAND_LETTERS)
