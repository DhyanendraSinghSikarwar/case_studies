"""Cost-optimal contact threshold for a risk-only (constant save-rate) retention policy."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from churnx.snapshot import customer_value_inr


def expected_profit(p: np.ndarray, value: np.ndarray, cost: float, save_rate: float) -> np.ndarray:
    """Expected profit of contacting each customer: p * save_rate * value - cost."""
    return np.asarray(p, float) * save_rate * np.asarray(value, float) - cost


def sweep_thresholds(p: np.ndarray, value: np.ndarray, cost: float, save_rate: float,
                     grid: np.ndarray | None = None) -> pd.DataFrame:
    """Profit and #contacted for each threshold (contact iff p >= t); costs only counted for contacted.

    A final row with a threshold above every score represents "contact nobody" (profit 0).
    """
    p, value = np.asarray(p, float), np.asarray(value, float)
    grid = np.linspace(0.0, 0.95, 96) if grid is None else np.asarray(grid, float)
    rows = [{"threshold": float(t), "n_contacted": int((p >= t).sum()),
             "profit_inr": float(expected_profit(p[p >= t], value[p >= t], cost, save_rate).sum())} for t in grid]
    rows.append({"threshold": float(max(grid.max(), p.max())) + 1e-9, "n_contacted": 0, "profit_inr": 0.0})
    return pd.DataFrame(rows)


def best_threshold(sweep: pd.DataFrame) -> dict[str, float]:
    """Row of the sweep with maximal profit (ties -> higher threshold, i.e. fewer contacts)."""
    s = sweep.sort_values(["profit_inr", "threshold"], ascending=[False, False]).iloc[0]
    return {"threshold": float(s["threshold"]), "n_contacted": int(s["n_contacted"]),
            "profit_inr": float(s["profit_inr"])}


def threshold_report(p: np.ndarray, monetary_6m: np.ndarray, biz: dict[str, Any],
                     grid_max: float = 0.95) -> dict[str, Any]:
    """Best threshold plus comparison with contact-nobody and contact-everybody."""
    value = customer_value_inr(monetary_6m, biz)
    grid = np.linspace(0.0, grid_max, int(round(grid_max * 100)) + 1)
    sw = sweep_thresholds(p, value, biz["offer_cost_inr"], biz["save_rate"], grid)
    best = best_threshold(sw)
    everybody = float(expected_profit(p, value, biz["offer_cost_inr"], biz["save_rate"]).sum())
    return {"sweep": sw, "best": best, "profit_contact_all_inr": everybody, "profit_contact_nobody_inr": 0.0,
            "n_customers": int(len(p))}


def sensitivity_table(p: np.ndarray, monetary_6m: np.ndarray, biz: dict[str, Any], save_rates: list[float],
                      costs: list[float]) -> pd.DataFrame:
    """Best threshold / contacts / profit over save_rate x offer_cost."""
    rows = []
    for sr in save_rates:
        for c in costs:
            b = {**biz, "save_rate": sr, "offer_cost_inr": c}
            rep = threshold_report(p, monetary_6m, b)
            rows.append({"save_rate": sr, "offer_cost_inr": c, **rep["best"]})
    return pd.DataFrame(rows)
