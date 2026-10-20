"""Promotion optimiser: best discount per family under a subsidy budget (pulp), single period and 8-week calendar."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pulp

from .config import get_logger
from .engine import EngineContext

log = get_logger("promo.optimise")


def _solver() -> pulp.LpSolver:
    """HiGHS if available, else CBC."""
    try:
        if "HiGHS" in pulp.listSolvers(onlyAvailable=True):
            return pulp.HiGHS(msg=False)
    except Exception:  # noqa: BLE001
        pass
    return pulp.PULP_CBC_CMD(msg=False)


def _binary(prob: pulp.LpProblem, name: str) -> pulp.LpVariable:
    """Binary variable; PuLP >= 4 creates variables through the problem, older versions directly."""
    if hasattr(prob, "add_variable"):
        return prob.add_variable(name, cat="Binary")
    return pulp.LpVariable(name, cat="Binary")


def candidate_table(ctx: EngineContext, cfg: dict, top_families: int | None = None) -> pd.DataFrame:
    """For each of the top families by weekly revenue: its top-revenue active SKU scored at every discount level.

    Columns: family, family_name, stock_code, description, weekly_revenue, discount, family_net, subsidy,
    promoted_only. discount 0 has all zeros.
    """
    oc = cfg["optimiser"]
    t = ctx.table[ctx.table["active"]]
    fam_rev = t.groupby("family")["weekly_revenue"].sum().sort_values(ascending=False)
    fams = fam_rev.head(top_families or oc["top_families"]).index
    rows = []
    for f in fams:
        g = t[t["family"] == f]
        sku = g["weekly_revenue"].idxmax()
        for d in oc["discounts"]:
            if d == 0:
                r = {"family_net": 0.0, "subsidy_cost": 0.0, "promoted_only": 0.0}
            else:
                r = ctx.score(sku, d)
            rows.append({
                "family": f, "family_name": g["family_name"].iloc[0], "stock_code": sku, "description": t.at[sku, "description"],
                "weekly_revenue": float(t.at[sku, "weekly_revenue"]), "family_weekly_revenue": float(g["weekly_revenue"].sum()), "discount": d, "family_net": r["family_net"],
                "subsidy": r["subsidy_cost"], "promoted_only": r["promoted_only"],
            })
    return pd.DataFrame(rows)


def budget_from(cands: pd.DataFrame, cfg: dict) -> float:
    """Budget = budget_frac x one week of promo-eligible revenue (weekly revenue of the promoted SKUs of the candidate families)."""
    elig = cands.drop_duplicates("family")["weekly_revenue"].sum()
    return float(cfg["optimiser"]["budget_frac"] * elig)


def optimise_single(cands: pd.DataFrame, budget: float) -> pd.DataFrame:
    """One discount level per family maximising total family net with total subsidy <= budget."""
    fams = cands["family"].unique().tolist()
    levels = sorted(cands["discount"].unique())
    idx = cands.set_index(["family", "discount"])
    prob = pulp.LpProblem("promo_plan", pulp.LpMaximize)
    x = {(f, d): _binary(prob, f"x_{i}_{j}") for i, f in enumerate(fams) for j, d in enumerate(levels)}
    prob += pulp.lpSum(float(idx.at[(f, d), "family_net"]) * x[f, d] for f, d in x)
    for f in fams:
        prob += pulp.lpSum(x[f, d] for d in levels) == 1
    prob += pulp.lpSum(float(idx.at[(f, d), "subsidy"]) * x[f, d] for f, d in x) <= budget
    prob.solve(_solver())
    chosen = {f: max(levels, key=lambda d: x[f, d].value() or 0.0) for f in fams}
    rows = []
    for f, d in chosen.items():
        r = idx.loc[(f, d)]
        base = cands[(cands["family"] == f)].iloc[0]
        rows.append({"family": f, "family_name": base["family_name"], "stock_code": base["stock_code"], "description": base["description"],
                     "discount": d, "family_net": float(r["family_net"]), "subsidy": float(r["subsidy"])})
    return pd.DataFrame(rows)


def optimise_calendar(cands: pd.DataFrame, budget: float, season: np.ndarray, max_per_week: int) -> pd.DataFrame:
    """Horizon plan x[f, w, d]: at most one promo per family, <= max_per_week promos per week, total subsidy <= budget.

    Net and subsidy of a promo in week w are scaled by the seasonal index of w. Only levels with positive net are
    modelled (zero is always available by not promoting), so an empty plan is a legitimate answer.
    """
    pos = cands[(cands["discount"] > 0) & (cands["family_net"] > 0)]
    H = len(season)
    prob = pulp.LpProblem("promo_calendar", pulp.LpMaximize)
    keys = [(r.family, w, r.discount) for r in pos.itertuples() for w in range(H)]
    x = {k: _binary(prob, f"y_{i}") for i, k in enumerate(keys)}
    if not keys:
        return pd.DataFrame(columns=["family", "family_name", "stock_code", "description", "week", "discount", "family_net", "subsidy"])
    info = pos.set_index(["family", "discount"])
    prob += pulp.lpSum(float(info.at[(f, d), "family_net"]) * season[w] * x[f, w, d] for f, w, d in keys)
    for f in pos["family"].unique():
        prob += pulp.lpSum(v for (ff, _, _), v in x.items() if ff == f) <= 1
    for w in range(H):
        prob += pulp.lpSum(v for (_, ww, _), v in x.items() if ww == w) <= max_per_week
    prob += pulp.lpSum(float(info.at[(f, d), "subsidy"]) * season[w] * x[f, w, d] for f, w, d in keys) <= budget
    prob.solve(_solver())
    rows = []
    for (f, w, d), v in x.items():
        if (v.value() or 0) > 0.5:
            r = info.loc[(f, d)]
            rows.append({"family": f, "family_name": r["family_name"], "stock_code": r["stock_code"], "description": r["description"],
                         "week": w + 1, "discount": d, "family_net": float(r["family_net"] * season[w]), "subsidy": float(r["subsidy"] * season[w])})
    return pd.DataFrame(rows).sort_values(["week", "family_net"], ascending=[True, False]).reset_index(drop=True) if rows else pd.DataFrame(
        columns=["family", "family_name", "stock_code", "description", "week", "discount", "family_net", "subsidy"])


def dashboard_plan(cands: pd.DataFrame, budget: float, season: np.ndarray, max_per_week: int, ref_discount: float, rank_by: str = "promoted_only") -> dict:
    """Naive policy: promote families ranked by the dashboard metric at one common discount, fill weeks in order.

    rank_by: 'promoted_only' (SKU uplift view) or 'weekly_revenue' (top revenue). Evaluated on TRUE family net.
    Stops at the budget; all chosen get the same discount.
    """
    c = cands[np.isclose(cands["discount"], ref_discount)].copy()
    if rank_by == "promoted_only":
        c = c[c["promoted_only"] > 0]
    c = c.sort_values(rank_by, ascending=False)
    H = len(season)
    spent, net, n = 0.0, 0.0, 0
    for r in c.itertuples():
        w = n // max_per_week
        if w >= H:
            break
        sub = r.subsidy * season[w]
        if spent + sub > budget:
            continue
        spent += sub; net += r.family_net * season[w]; n += 1
    return {"n_promos": n, "family_net": float(net), "subsidy": float(spent), "rank_by": rank_by}


def plan_summary(plan: pd.DataFrame, budget: float) -> dict:
    """Totals for a plan."""
    return {
        "n_promos": int(len(plan)), "family_net": float(plan["family_net"].sum()) if len(plan) else 0.0,
        "subsidy": float(plan["subsidy"].sum()) if len(plan) else 0.0, "budget": float(budget),
    }
