"""Drift monitoring: PSI / CSI per feature and the LIMIT_BAL shift simulation."""
from __future__ import annotations

import pandas as pd

from .evaluate import psi
from .features import add_features


def csi_table(train: pd.DataFrame, new: pd.DataFrame, cols, alert: float = 0.2) -> pd.DataFrame:
    """Characteristic stability index (same maths as PSI) per feature with stable/watch/ALERT status."""
    out = pd.DataFrame([{"feature": c, "psi": psi(train[c], new[c])} for c in cols])
    out = out.sort_values("psi", ascending=False).reset_index(drop=True)
    out["status"] = pd.cut(out["psi"], [-1, 0.1, alert, 1e9], labels=["stable", "watch", "ALERT"]).astype(str)
    return out


def simulate_limit_shift(df_raw: pd.DataFrame, shift: float = -0.20) -> pd.DataFrame:
    """Scale RAW LIMIT_BAL then recompute features (utilisation depends on the limit)."""
    d = df_raw.copy()
    d["LIMIT_BAL"] = (d["LIMIT_BAL"] * (1 + shift)).round()
    return add_features(d)


def score_drift_alert(psi_value: float, alert: float = 0.2) -> bool:
    """True when the score PSI breaches the alert level."""
    return bool(psi_value > alert)
