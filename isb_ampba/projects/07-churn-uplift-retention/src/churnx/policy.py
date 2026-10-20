"""Targeting policies, exact (oracle-based) and IPW (oracle-free) policy evaluation."""
from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pandas as pd

POLICIES = ["random", "all", "risk_top_k", "clv_top_k", "uplift_top_k", "profit_optimal"]


def select_policies(tau_hat, p_churn, value_inr, budget_frac: float, cost: float, seed: int) -> dict[str, np.ndarray]:
    """Boolean treat-masks for the six policies (30% budget unless noted).

    ``all`` and ``profit_optimal`` (contact iff tau_hat * value - cost > 0) are unbudgeted.
    """
    tau_hat, p_churn, value_inr = (np.asarray(a, float) for a in (tau_hat, p_churn, value_inr))
    n = len(tau_hat)
    k = int(round(budget_frac * n))
    rng = np.random.default_rng(seed)

    def top_k(score: np.ndarray) -> np.ndarray:
        m = np.zeros(n, bool)
        m[np.argsort(-score, kind="mergesort")[:k]] = True
        return m

    rnd = np.zeros(n, bool)
    rnd[rng.permutation(n)[:k]] = True
    return {"random": rnd, "all": np.ones(n, bool), "risk_top_k": top_k(p_churn), "clv_top_k": top_k(value_inr),
            "uplift_top_k": top_k(tau_hat), "profit_optimal": (tau_hat * value_inr - cost) > 0}


def exact_value(mask, tau_true, value_inr, cost: float) -> float:
    """Track A: exact incremental profit using the TRUE effect."""
    return float(((np.asarray(tau_true) * np.asarray(value_inr) - cost) * np.asarray(mask)).sum())


def oracle_mask(tau_true, value_inr, cost: float) -> np.ndarray:
    """Perfect-hindsight policy: contact iff true tau * value > cost (the ceiling)."""
    return (np.asarray(tau_true) * np.asarray(value_inr) - cost) > 0


def policy_table(masks: dict[str, np.ndarray], tau_true, value_inr, cost: float) -> pd.DataFrame:
    """Policy, customers treated, cost, profit (INR) and % of the oracle ceiling."""
    orc = oracle_mask(tau_true, value_inr, cost)
    orc_val = exact_value(orc, tau_true, value_inr, cost)
    rows = []
    for name, m in {**masks, "oracle": orc}.items():
        v = exact_value(m, tau_true, value_inr, cost)
        rows.append({"policy": name, "n_treated": int(np.sum(m)), "total_offer_cost_inr": float(cost * np.sum(m)),
                     "profit_inr": v, "pct_of_oracle": float(100 * v / orc_val) if orc_val > 0 else float("nan")})
    return pd.DataFrame(rows)


def segment_labels(cohort: pd.DataFrame) -> pd.Series:
    """Behavioural segments mirroring the simulator's response rules (for explaining who loses money)."""
    f = cohort["frequency_6m"].groupby(cohort["asof"]).rank(pct=True) if "asof" in cohort.columns \
        else cohort["frequency_6m"].rank(pct=True)
    seg = np.where(f > 0.85, "Champions", np.where(cohort["recency_days"] > 100, "Hibernating",
                   np.where((f > 0.25) & (f <= 0.75), "Mid-frequency", "Other")))
    return pd.Series(seg, index=cohort.index, name="segment")


def segment_breakdown(cohort: pd.DataFrame, mask: np.ndarray, tau_true, value_inr, cost: float) -> pd.DataFrame:
    """For one policy's mask: per segment, #treated, mean true tau, and profit contribution (INR)."""
    seg = segment_labels(cohort).to_numpy()
    tau_true, value_inr, mask = np.asarray(tau_true), np.asarray(value_inr), np.asarray(mask, bool)
    rows = []
    for s in sorted(set(seg)):
        sel = seg == s
        rows.append({"segment": s, "n_segment": int(sel.sum()), "n_treated": int((sel & mask).sum()),
                     "mean_tau_true": float(tau_true[sel].mean()),
                     "profit_inr": float(((tau_true * value_inr - cost) * (sel & mask)).sum())})
    return pd.DataFrame(rows)


def sensitivity_sweep(cohort: pd.DataFrame, tau_hat, p_churn, monetary_6m, biz: dict[str, Any], budget_frac: float,
                      seed: int, grid: dict[str, list[float]]) -> pd.DataFrame:
    """Re-evaluate all policies over offer_cost x gross_margin x clv_months (masks recomputed per cell)."""
    from churnx.snapshot import customer_value_inr
    from churnx.threshold import expected_profit

    rows = []
    for cost in grid["offer_cost_inr"]:
        for margin in grid["gross_margin"]:
            for months in grid["clv_months"]:
                b = {**biz, "offer_cost_inr": cost, "gross_margin": margin, "clv_months": months}
                value = customer_value_inr(monetary_6m, b)
                masks = select_policies(tau_hat, p_churn, value, budget_frac, cost, seed)
                masks["risk_threshold_m2"] = expected_profit(p_churn, value, cost, biz["save_rate"]) > 0
                t = policy_table(masks, cohort["tau_true"].to_numpy(), value, cost)
                for _, r in t.iterrows():
                    rows.append({"offer_cost_inr": cost, "gross_margin": margin, "clv_months": months, **r.to_dict()})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------- Track B (oracle-free)
def ipw_value(mask, w, y_money, e: float, cost: float) -> float:
    """IPW incremental profit if ``mask`` were treated: sum pi*y*(w/e-(1-w)/(1-e)) - cost*sum(pi)."""
    pi, w = np.asarray(mask, float), np.asarray(w, float)
    return float((pi * np.asarray(y_money, float) * (w / e - (1 - w) / (1 - e))).sum() - cost * pi.sum())


def bootstrap_value_ci(fn: Callable[[np.ndarray], float], n: int, n_boot: int = 500, seed: int = 0,
                       alpha: float = 0.05) -> tuple[float, float]:
    """Percentile bootstrap CI for a statistic of resampled row indices."""
    rng = np.random.default_rng(seed)
    vals = np.array([fn(rng.integers(0, n, n)) for _ in range(n_boot)])
    return float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2))
