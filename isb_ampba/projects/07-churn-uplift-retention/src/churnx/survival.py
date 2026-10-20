"""Optional survival view: Kaplan-Meier and Cox PH for time-to-next-purchase (requires ``lifelines``)."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from churnx.snapshot import FEATURES

COX_FEATURES = ["recency_days", "frequency_6m", "aov_6m", "spend_trend", "ipt_mean", "n_returns", "is_uk"]


def time_to_next_purchase(sales: pd.DataFrame, cohort: pd.DataFrame, asof: str | pd.Timestamp,
                          horizon_days: int = 90) -> pd.DataFrame:
    """Duration (days) to the first purchase in [asof, asof+horizon), censored at ``horizon_days``.

    event=1 means the customer *returned*; event=0 means no purchase observed in the window (= churned).
    """
    asof = pd.Timestamp(asof)
    end = asof + pd.Timedelta(days=horizon_days)
    w = sales[(sales["invoice_date"] >= asof) & (sales["invoice_date"] < end)]
    first = w.groupby("customer_id")["invoice_date"].min()
    dur = ((first - asof).dt.total_seconds() / 86400).reindex(cohort["customer_id"]).to_numpy()
    event = ~np.isnan(dur)
    out = cohort[["customer_id", *FEATURES]].copy()
    out["duration"] = np.where(event, np.maximum(dur, 0.01), float(horizon_days))
    out["event"] = event.astype(int)
    return out


def run_survival(frame: pd.DataFrame) -> tuple[dict[str, Any], pd.DataFrame] | None:
    """KM median / survival at 30,60,90d overall and by recency tercile; Cox PH hazard ratios + concordance.

    Returns (summary dict, KM curve table) or None if lifelines is not installed.
    """
    try:
        from lifelines import CoxPHFitter, KaplanMeierFitter
    except ImportError:
        return None
    km = KaplanMeierFitter().fit(frame["duration"], frame["event"], label="all")
    curves = [km.survival_function_.reset_index().rename(columns={"timeline": "t", "all": "survival"}).assign(group="all")]
    terc = pd.qcut(frame["recency_days"], 3, labels=["recent", "mid", "stale"])
    by = {}
    for g in ["recent", "mid", "stale"]:
        sub = frame[terc == g]
        k = KaplanMeierFitter().fit(sub["duration"], sub["event"], label=g)
        by[g] = float(k.predict(60.0))
        curves.append(k.survival_function_.reset_index().rename(columns={"timeline": "t", g: "survival"}).assign(group=g))
    X = frame[COX_FEATURES + ["duration", "event"]].copy()
    X[COX_FEATURES] = (X[COX_FEATURES] - X[COX_FEATURES].mean()) / X[COX_FEATURES].std().replace(0, 1)
    cph = CoxPHFitter(penalizer=0.1).fit(X, duration_col="duration", event_col="event")
    hr = {k: float(v) for k, v in np.exp(cph.params_).items()}
    summ = {"n": int(len(frame)), "share_returned_within_horizon": float(frame["event"].mean()),
            "km_survival_30d": float(km.predict(30.0)), "km_survival_60d": float(km.predict(60.0)),
            "km_survival_90d": float(km.predict(90.0)), "km_survival_60d_by_recency_tercile": by,
            "cox_concordance": float(cph.concordance_index_), "cox_hazard_ratios_per_sd": hr}
    return summ, pd.concat(curves, ignore_index=True)
