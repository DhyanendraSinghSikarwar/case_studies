import numpy as np
import pandas as pd

from promo.optimise import candidate_table, dashboard_plan, optimise_calendar, optimise_single


def _cands(nets, subs):
    rows = []
    for f, (n, s) in enumerate(zip(nets, subs)):
        base = {"family": f"F{f}", "family_name": f"n{f}", "stock_code": f"{f}", "description": "d", "weekly_revenue": 100.0}
        rows.append({**base, "discount": 0.0, "family_net": 0.0, "subsidy": 0.0, "promoted_only": 0.0})
        for d, k in ((0.1, 1.0), (0.2, 1.8)):
            rows.append({**base, "discount": d, "family_net": n * k, "subsidy": s * (d / 0.1), "promoted_only": n * k})
    return pd.DataFrame(rows)


def test_optimiser_respects_budget():
    c = _cands([10, 8, 6, 4], [5, 5, 5, 5])
    plan = optimise_single(c, budget=12.0)
    assert plan["subsidy"].sum() <= 12.0 + 1e-9
    assert plan["family"].is_unique and len(plan) == 4


def test_optimiser_empty_plan_when_all_negative():
    c = _cands([-5, -2, -9], [5, 5, 5])
    plan = optimise_single(c, budget=1000.0)
    assert (plan["discount"] == 0).all()
    assert optimise_calendar(c, 1000.0, np.ones(4), 2).empty


def test_calendar_constraints():
    c = _cands([10, 9, 8, 7, 6, 5], [1, 1, 1, 1, 1, 1])
    season = np.array([1.0, 0.0, 2.0, 1.0])
    plan = optimise_calendar(c, 100.0, season, max_per_week=2)
    assert plan["family"].is_unique
    assert plan.groupby("week").size().max() <= 2
    assert (plan["week"] != 2).all()               # zero seasonal-index week is never used
    tight = optimise_calendar(c, 3.0, season, max_per_week=2)
    assert tight["subsidy"].sum() <= 3.0 + 1e-9


def test_optimiser_beats_or_matches_dashboard(ctx, cfg):
    cands = candidate_table(ctx, cfg)
    assert cands.groupby("family")["discount"].nunique().eq(len(cfg["optimiser"]["discounts"])).all()
    season = np.ones(4)
    budget = 0.3 * cands.drop_duplicates("family")["weekly_revenue"].sum()
    plan = optimise_calendar(cands, budget, season, 4)
    dash = dashboard_plan(cands, budget, season, 4, 0.10)
    assert plan["family_net"].sum() >= dash["family_net"] - 1e-9
    assert plan["subsidy"].sum() <= budget + 1e-9
