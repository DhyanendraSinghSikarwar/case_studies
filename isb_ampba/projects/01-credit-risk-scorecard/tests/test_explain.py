"""Unit tests for credit.explain (SHAP importance and reason codes); small synthetic model, offline."""
from __future__ import annotations

import numpy as np
import pandas as pd
from xgboost import XGBClassifier

from credit import explain


def _toy():
    rng = np.random.default_rng(0)
    X = pd.DataFrame({"max_delay": rng.integers(0, 6, 600).astype(float), "avg_util": rng.random(600),
                      "AGE": rng.integers(21, 70, 600).astype(float)})
    y = (X["max_delay"] + rng.normal(0, 1, 600) > 2.5).astype(int)
    m = XGBClassifier(n_estimators=30, max_depth=2, random_state=0, n_jobs=1).fit(X, y)
    return m, X


def test_global_importance_sorted_and_driver_first():
    m, X = _toy()
    sv = explain.shap_values(m, X)
    imp = explain.global_importance(sv, X.columns)
    assert sv.shape == X.shape
    assert imp["mean_abs_shap"].is_monotonic_decreasing
    assert imp.loc[0, "feature"] == "max_delay"


def test_reason_codes_only_risk_increasing_and_at_most_k():
    cols = ["max_delay", "avg_util", "AGE"]
    row = pd.Series({"max_delay": 3.0, "avg_util": 0.82, "AGE": 30.0})
    codes = explain.reason_codes(row, np.array([0.9, 0.5, -0.4]), cols, k=4)
    assert len(codes) == 2  # the negative contribution (AGE) is excluded
    assert "82%" in codes[1] and "3 month" in codes[0]
    assert len(explain.reason_codes(row, np.array([0.9, 0.5, 0.4]), cols, k=2)) == 2
    assert explain.reason_codes(row, np.array([-1.0, -0.5, -0.4]), cols) == []
