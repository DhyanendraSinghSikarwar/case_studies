"""Fairness audit by SEX and age bucket: approval rate, bad rate, AUC, disparate-impact ratio."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluate import auc


def age_bucket(age, cfg: dict) -> pd.Series:
    """Age buckets from config (<30, 30-39, 40-49, 50+)."""
    f = cfg["fairness"]
    return pd.cut(pd.Series(np.asarray(age)), f["age_bins"], labels=f["age_labels"], right=False)


def group_report(y, p, approved, groups) -> pd.DataFrame:
    """Per-group n, approval rate, bad rate among approved, default rate and AUC."""
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p), "approved": np.asarray(approved).astype(bool),
                       "g": np.asarray(groups)})
    rows = []
    for g, d in df.groupby("g", observed=True):
        rows.append({"group": g, "n": len(d), "approval_rate": d["approved"].mean(),
                     "bad_rate_approved": d.loc[d["approved"], "y"].mean() if d["approved"].any() else np.nan,
                     "default_rate": d["y"].mean(), "auc": auc(d["y"], d["p"]) if d["y"].nunique() == 2 else np.nan})
    return pd.DataFrame(rows)


def disparate_impact(report: pd.DataFrame, threshold: float = 0.8) -> pd.DataFrame:
    """di_ratio = group approval rate / highest group approval rate (four-fifths screening heuristic)."""
    ref = report.loc[report["approval_rate"].idxmax(), "group"]
    out = report.copy()
    out["di_ratio"] = out["approval_rate"] / report.loc[report["group"] == ref, "approval_rate"].iloc[0]
    out["passes_80pct"] = out["di_ratio"] >= threshold
    return out
