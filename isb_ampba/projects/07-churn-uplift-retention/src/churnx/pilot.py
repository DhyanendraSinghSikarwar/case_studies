"""Simulated randomised retention pilot with a known heterogeneous treatment effect (SYNTHETIC).

Baseline outcomes are the *real* churn labels; only the offer's effect is invented. The ground truth
(``save_rate_true``, ``saved``, ``tau_true``, ``p0``) is stored in the pilot table but must never be used as
a feature - see :data:`TRUTH_COLS` and ``docs/SIMULATOR.md``.
"""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier

from churnx.models import group_splits
from churnx.snapshot import FEATURES

TRUTH_COLS = ["p0", "save_rate_true", "tau_true", "saved"]
OUTCOME_COLS = ["w", "y", "retained", "churn"]


def true_save_rate(df: pd.DataFrame, rng: np.random.Generator, pattern: str = "mid_freq") -> np.ndarray:
    """True P(offer saves a would-be churner) as a function of pre-treatment features.

    ``mid_freq``: price-sensitive (low AOV) mid-frequency customers respond; Champions (top 15% frequency)
    do not; Hibernating (recency>100d) rarely. ``high_freq`` is an alternative world for sensitivity analysis:
    the response bump sits on *high* frequency, so high-risk (low-frequency) customers are not special.
    """
    grp = df["asof"] if "asof" in df.columns else pd.Series(0, index=df.index)
    f = df["frequency_6m"].groupby(grp).rank(pct=True).to_numpy()
    a = df["aov_6m"].groupby(grp).rank(pct=True).to_numpy()
    if pattern == "mid_freq":
        bump = np.exp(-(((f - 0.5) / 0.25) ** 2))
        base = 0.05 + 0.55 * bump * (1.0 - a)
        base = np.where(f > 0.85, 0.0, base)
    elif pattern == "high_freq":
        bump = np.exp(-(((f - 0.9) / 0.2) ** 2))
        base = 0.05 + 0.55 * bump * (1.0 - a)
    else:
        raise ValueError(f"unknown pattern {pattern}")
    base = np.where(df["recency_days"].to_numpy() > 100, base * 0.2, base)
    return np.clip(base + rng.normal(0, 0.03, len(df)), 0.0, 0.8)


def simulate_pilot(df: pd.DataFrame, p0: np.ndarray, seed: int, treat_share: float = 0.5,
                   pattern: str = "mid_freq") -> pd.DataFrame:
    """Randomise 50/50 and simulate outcomes. ``retained = 1 - y`` (higher is better)."""
    rng = np.random.default_rng(seed)
    out = df.copy()
    out["p0"] = np.clip(np.asarray(p0, float), 0.01, 0.99)
    out["w"] = (rng.random(len(out)) < treat_share).astype(int)
    out["save_rate_true"] = true_save_rate(out, rng, pattern)
    out["tau_true"] = out["p0"] * out["save_rate_true"]
    saved = (rng.random(len(out)) < out["save_rate_true"]) & (out["churn"] == 1)
    out["saved"] = saved.astype(int)
    out["y"] = np.where(out["w"] == 1, out["churn"] * (1 - out["saved"]), out["churn"])
    out["retained"] = 1 - out["y"]
    return out


def oof_churn_prob(df: pd.DataFrame, seed: int = 42, n_splits: int = 3) -> np.ndarray:
    """Out-of-fold churn probability (group-aware LightGBM) for stacked cohorts, clipped to [0.01, 0.99]."""
    X, y, g = df[FEATURES], df["churn"].to_numpy(), df["customer_id"].to_numpy()
    p = np.zeros(len(df))
    for tr, va in group_splits(X, y, g, n_splits):
        m = LGBMClassifier(n_estimators=200, num_leaves=8, learning_rate=0.05, min_child_samples=40,
                           subsample=0.8, subsample_freq=1, colsample_bytree=0.8, random_state=seed,
                           verbose=-1, n_jobs=1).fit(X.iloc[tr], y[tr])
        p[va] = m.predict_proba(X.iloc[va])[:, 1]
    return np.clip(p, 0.01, 0.99)


def shift_to_rate(p: np.ndarray, target_rate: float) -> np.ndarray:
    """Logit-intercept shift so that mean(p) == target_rate (used only to build simulator ground truth)."""
    from scipy.optimize import brentq

    p = np.clip(np.asarray(p, float), 1e-4, 1 - 1e-4)
    lg = np.log(p / (1 - p))
    f = lambda b: (1 / (1 + np.exp(-(lg + b)))).mean() - target_rate  # noqa: E731
    b = brentq(f, -10, 10)
    return np.clip(1 / (1 + np.exp(-(lg + b))), 0.01, 0.99)


def build_pilot(snaps: pd.DataFrame, p_test: np.ndarray, cfg: dict[str, Any],
                pattern: str | None = None) -> dict[str, pd.DataFrame]:
    """Build the pilot training cohort (history + train snapshots) and the pilot test cohort.

    Training cohorts use out-of-fold ``p0``; the test cohort uses the calibrated churn model probability,
    logit-shifted to the cohort's realised churn rate so that the simulator's ground-truth effect is consistent
    with the world it generates (documented in docs/SIMULATOR.md; the churn *model* is not recalibrated here).
    """
    pattern = pattern or cfg["pilot"].get("pattern", "mid_freq")
    seed, share = cfg["seed"], cfg["pilot"]["treat_share"]
    tr = snaps[snaps["split"].isin(["pilot_hist", "train"])].sort_values(["asof", "customer_id"]).reset_index(drop=True)
    te = snaps[snaps["split"] == "test"].sort_values("customer_id").reset_index(drop=True)
    p_tr = oof_churn_prob(tr, seed)
    p_te = shift_to_rate(np.asarray(p_test), float(te["churn"].mean()))
    return {"train": simulate_pilot(tr, p_tr, seed, share, pattern),
            "test": simulate_pilot(te, p_te, seed + 1, share, pattern)}


def ate_check(pilot: pd.DataFrame) -> dict[str, float]:
    """Observed difference in retention vs mean true tau, with the standard error of the difference."""
    t, c = pilot[pilot["w"] == 1]["retained"], pilot[pilot["w"] == 0]["retained"]
    se = float(np.sqrt(t.var(ddof=1) / len(t) + c.var(ddof=1) / len(c)))
    return {"observed_ate": float(t.mean() - c.mean()), "se": se, "mean_tau_true": float(pilot["tau_true"].mean()),
            "n_treated": int(len(t)), "n_control": int(len(c))}


def uplift_feature_matrix(pilot: pd.DataFrame) -> pd.DataFrame:
    """Pre-treatment features only (asserts that no ground-truth or outcome column leaks in)."""
    X = pilot[FEATURES]
    bad = set(X.columns) & (set(TRUTH_COLS) | set(OUTCOME_COLS))
    assert not bad, f"leaky columns in uplift features: {bad}"
    return X
