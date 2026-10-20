"""Campaign planner: segment x action matrix, expected uplift/ROI under config assumptions."""
from __future__ import annotations

import pandas as pd

from .config import load_config


def segment_economics(df: pd.DataFrame, cfg: dict | None = None, response_mult: float = 1.0,
                      margin: float | None = None) -> pd.DataFrame:
    """Per-segment campaign economics.

    `df` needs: segment, avg_basket, and optionally m12_pred_clv / actual_purchases.
    Formulae (all assumptions from config.campaign.actions):
      contacts = n * reach;  contact_cost = contacts * cost_per_contact
      responders = contacts * response_rate * response_mult   (incremental, i.e. caused by campaign)
      incr_revenue = responders * avg_basket * order_value_factor
      discount_cost = incr_revenue * discount_cost_rate
      gross_profit = incr_revenue * margin;  total_cost = contact_cost + discount_cost
      net_profit = gross_profit - total_cost;  ROI = net_profit / total_cost
    """
    cfg = cfg or load_config()
    cc = cfg["campaign"]
    margin = cc["gross_margin"] if margin is None else margin
    rows = []
    for seg, a in cc["actions"].items():
        d = df[df["segment"] == seg]
        if d.empty:
            continue
        n = len(d)
        contacts = n * a["reach"]
        contact_cost = contacts * a["cost_per_contact"]
        responders = contacts * a["response_rate"] * response_mult
        aov = float(d["avg_basket"].mean())
        incr_rev = responders * aov * a["order_value_factor"]
        disc = incr_rev * a.get("discount_cost_rate", 0.0)
        gross = incr_rev * margin
        total_cost = contact_cost + disc
        row = {
            "segment": seg, "action": a["action"], "customers": n, "contacts": contacts,
            "avg_basket": aov, "cost_per_contact": a["cost_per_contact"],
            "response_rate": a["response_rate"] * response_mult,
            "expected_responders": responders, "incremental_revenue": incr_rev,
            "gross_profit": gross, "total_cost": total_cost, "net_profit": gross - total_cost,
            "roi": (gross - total_cost) / total_cost if total_cost > 0 else float("nan"),
        }
        if "m12_pred_clv" in d:
            row["avg_clv_12m"] = float(d["m12_pred_clv"].mean())
        if "actual_purchases" in d:
            row["holdout_purchase_rate"] = float((d["actual_purchases"] > 0).mean())
        rows.append(row)
    return pd.DataFrame(rows)


def allocate_budget(econ: pd.DataFrame, budget: float) -> pd.DataFrame:
    """Fund actions in descending ROI until the budget is spent (last one partially funded)."""
    e = econ.sort_values("roi", ascending=False).copy()
    left = budget
    frac = []
    for c in e["total_cost"]:
        f = 0.0 if left <= 0 else min(1.0, left / c)
        frac.append(f)
        left -= c * f
    e["funded_fraction"] = frac
    for col in ("contacts", "total_cost", "incremental_revenue", "net_profit", "expected_responders"):
        e[f"funded_{col}"] = e[col] * e["funded_fraction"]
    return e


def sensitivity(df: pd.DataFrame, cfg: dict | None = None) -> pd.DataFrame:
    """Portfolio net profit and ROI over response-rate multipliers x gross margins (unconstrained)."""
    cfg = cfg or load_config()
    s = cfg["campaign"]["sensitivity"]
    rows = []
    for m in s["margins"]:
        for r in s["response_multipliers"]:
            e = segment_economics(df, cfg, response_mult=r, margin=m)
            tc, npf = float(e["total_cost"].sum()), float(e["net_profit"].sum())
            rows.append({"gross_margin": m, "response_multiplier": r, "total_cost": tc,
                         "net_profit": npf, "roi": npf / tc})
    return pd.DataFrame(rows)


def run_campaign(df: pd.DataFrame, cfg: dict | None = None) -> dict:
    """Economics table, budget-constrained plan, sensitivity grid and headline metrics."""
    cfg = cfg or load_config()
    econ = segment_economics(df, cfg)
    plan = allocate_budget(econ, cfg["campaign"]["total_budget_gbp"])
    sens = sensitivity(df, cfg)
    fx = cfg["campaign"]["inr_per_gbp"]
    funded_cost = float(plan["funded_total_cost"].sum())
    funded_net = float(plan["funded_net_profit"].sum())
    metrics = {
        "unconstrained_total_cost": float(econ["total_cost"].sum()),
        "unconstrained_net_profit": float(econ["net_profit"].sum()),
        "unconstrained_roi": float(econ["net_profit"].sum() / econ["total_cost"].sum()),
        "budget": float(cfg["campaign"]["total_budget_gbp"]),
        "funded_cost": funded_cost, "funded_net_profit": funded_net,
        "funded_roi": funded_net / funded_cost if funded_cost else None,
        "funded_net_profit_inr": funded_net * fx,
        "break_even_response_multiplier_at_margin": _break_even(df, cfg),
        "sensitivity_min_roi": float(sens["roi"].min()), "sensitivity_max_roi": float(sens["roi"].max()),
    }
    return {"economics": econ, "plan": plan, "sensitivity": sens, "metrics": metrics}


def _break_even(df: pd.DataFrame, cfg: dict) -> float | None:
    """Smallest response multiplier (grid of 0.05) at which portfolio net profit >= 0."""
    for i in range(1, 400):
        m = i * 0.05
        if segment_economics(df, cfg, response_mult=m)["net_profit"].sum() >= 0:
            return round(m, 2)
    return None
