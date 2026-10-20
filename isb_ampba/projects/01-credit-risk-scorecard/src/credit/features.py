"""Engineered repayment-behaviour features. PAY_AMT_i settles BILL_AMT_{i+1}."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import BILL_COLS, PAY_COLS, PAYAMT_COLS, TARGET

ENGINEERED = ([f"util_{i}" for i in range(1, 7)] + [f"pay_ratio_{i}" for i in range(1, 6)]
              + ["avg_util", "util_volatility", "max_delay", "n_months_delayed", "delay_trend",
                 "bill_growth", "avg_pay_ratio"])


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with engineered features appended (no target information used)."""
    out = df.copy()
    lim = out["LIMIT_BAL"].astype(float)
    for i in range(1, 7):
        out[f"util_{i}"] = out[f"BILL_AMT{i}"] / lim
    for i in range(1, 6):                                  # payment in month i settles bill of month i+1
        owed = out[f"BILL_AMT{i + 1}"].astype(float)
        ratio = np.where(owed > 0, out[f"PAY_AMT{i}"] / owed.where(owed > 0, 1.0), 1.0)
        out[f"pay_ratio_{i}"] = np.clip(ratio, 0.0, 1.0)
    util = out[[f"util_{i}" for i in range(1, 7)]]
    out["avg_util"] = util.mean(axis=1)
    out["util_volatility"] = util.std(axis=1, ddof=0)
    delays = out[PAY_COLS].clip(lower=0)                   # -2 / -1 / 0 all mean "no delay"
    out["max_delay"] = delays.max(axis=1)
    out["n_months_delayed"] = (delays > 0).sum(axis=1)
    y = delays[PAY_COLS[::-1]].to_numpy(dtype=float)       # oldest -> newest
    xc = np.arange(y.shape[1], dtype=float) - (y.shape[1] - 1) / 2
    out["delay_trend"] = (xc * (y - y.mean(axis=1, keepdims=True))).sum(axis=1) / (xc ** 2).sum()  # OLS slope
    out["bill_growth"] = (out["BILL_AMT1"] - out["BILL_AMT6"]) / lim
    owed_all = out[BILL_COLS[1:]].clip(lower=0).sum(axis=1)
    paid_all = out[PAYAMT_COLS[:5]].sum(axis=1)
    out["avg_pay_ratio"] = np.clip(np.where(owed_all > 0, paid_all / owed_all.where(owed_all > 0, 1.0), 1.0), 0, 1)
    return out


def feature_cols(df: pd.DataFrame, cfg: dict) -> list[str]:
    """Every column except the target and the fairness-excluded ones (SEX)."""
    drop = set(cfg["data"]["exclude_features"]) | {TARGET}
    return [c for c in df.columns if c not in drop]
