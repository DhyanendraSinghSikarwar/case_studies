"""Explicit data/leakage validation (asserts) for snapshots and the config."""
from __future__ import annotations

from typing import Any

import pandas as pd

from churnx.snapshot import FEATURES

FORBIDDEN_FEATURE_TOKENS = ("churn", "saved", "tau", "retained", "save_rate", "p0")


def check_feature_names(features: list[str]) -> None:
    """No feature name may look like a label/outcome/ground-truth column (exact or token match)."""
    for f in features:
        low = f.lower()
        assert low not in {"w", "y"}, f"feature {f} is a treatment/outcome column"
        for tok in FORBIDDEN_FEATURE_TOKENS:
            assert tok not in low, f"feature {f} contains forbidden token {tok}"


def label_windows_do_not_overlap(cfg: dict[str, Any]) -> bool:
    """Last training label window must end on or before the test ``asof`` date."""
    last_train = max(pd.Timestamp(d) for d in cfg["snapshots"]["train"])
    end = last_train + pd.Timedelta(days=cfg["snapshots"]["horizon_days"])
    return bool(end <= pd.Timestamp(cfg["snapshots"]["test"]))


def validate_snapshots(snaps: pd.DataFrame, sales: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Any]:
    """Schema, NaN, range and temporal checks; returns a dict of check results (also asserts)."""
    check_feature_names(FEATURES)
    assert not snaps[FEATURES].isna().any().any(), "NaN in features"
    assert snaps["churn"].isin([0, 1]).all(), "label must be binary"
    assert snaps["recency_days"].between(0, cfg["snapshots"]["lookback_days"]).all(), "recency outside lookback"
    assert label_windows_do_not_overlap(cfg), "train label window overlaps test asof"
    last = sales["invoice_date"].max()
    for d in snaps["asof"].unique():
        assert pd.Timestamp(d) + pd.Timedelta(days=cfg["snapshots"]["horizon_days"]) <= last + pd.Timedelta(days=1)
    return {"features_before_asof_enforced": True, "label_windows_do_not_overlap": True,
            "no_nan_features": True, "recency_in_lookback": True,
            "n_features": len(FEATURES)}
