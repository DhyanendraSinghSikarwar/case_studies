import numpy as np
import pandas as pd

from promo.demand import (
    baseline_table,
    estimate_elasticities,
    mnl_after_discount,
    mnl_shares_after_discount,
    pooled_fe_elasticity,
    seasonal_index,
    sku_elasticity_ols,
)
from promo.pipeline import build_engine_table


def test_mnl_shares_sum_to_one(family):
    u, p = family
    for d in (0.0, 0.05, 0.25, 0.6):
        s2, s0, _ = mnl_shares_after_discount(u, p, 1, d, -3.0, 0.4)
        assert abs(s2.sum() + s0 - 1) < 1e-12 and ((s2 > 0) & (s2 < 1)).all() and 0 < s0 < 1


def test_mnl_recovers_own_elasticity(family):
    u, p = family
    for eps in (-0.8, -2.0, -6.0):
        u2 = mnl_after_discount(u, p, 0, 0.001, eps, 0.4)
        num = np.log(u2[0] / u[0]) / np.log(1 - 0.001)
        assert abs(num / eps - 1) < 0.01


def test_mnl_zero_discount_is_baseline(family):
    u, p = family
    assert np.allclose(mnl_after_discount(u, p, 2, 0.0, -2.5, 0.4), u)


def test_mnl_siblings_lose_and_cap_scales(family):
    u, p = family
    u2 = mnl_after_discount(u, p, 0, 0.2, -3.0, 0.4)
    assert (u2[1:] < u[1:]).all() and u2[0] > u[0]
    u3 = mnl_after_discount(u, p, 0, 0.2, -3.0, 0.4, sub_weight=0.5)
    assert np.allclose(u[1:] - u3[1:], 0.5 * (u[1:] - u2[1:]))


def test_elasticity_regression_recovers_slope():
    rng = np.random.default_rng(42)
    n = 120
    lp = np.log(rng.choice([1.0, 0.9, 0.8, 0.7], n))
    month = rng.integers(1, 13, n)
    units = np.exp(4 + 0.3 * (month >= 10) - 2.5 * lp + rng.normal(0, 0.1, n))
    eps, se, _ = sku_elasticity_ols(units, np.exp(lp), month)
    assert abs(eps + 2.5) < 0.3 and se > 0


def test_fixture_elasticities_recovered(sales_panel, engine_res, cfg):
    _, _, panel = sales_panel
    el = estimate_elasticities(panel, dict(zip(engine_res["families"]["stock_code"], engine_res["families"]["family"])), cfg)
    v = el[el["valid"]]
    assert abs(v["eps_hat"].median() + 2.5) < 0.4
    pooled = pooled_fe_elasticity(panel[panel["stock_code"].isin(el.loc[el["eligible"], "stock_code"])])
    assert abs(pooled["eps"] + 2.5) < 0.3
    assert el["eps"].between(*cfg["demand"]["eps_bounds"]).all()


def test_no_leakage_baseline_and_elasticities(sales_panel, cfg):
    """Rows after as_of must not influence anything computed as of as_of."""
    sales, _, panel = sales_panel
    cut = panel["week"].sort_values().unique()[50]
    b1 = baseline_table(panel, cfg, as_of=cut)
    mod = panel.copy()
    mod.loc[mod["week"] > cut, "units"] *= 100
    b2 = baseline_table(mod, cfg, as_of=cut)
    pd.testing.assert_frame_equal(b1, b2)
    assert b1["last_week"].max() <= cut
    sales2 = sales.copy()
    sales2.loc[sales2["week"] > cut, "quantity"] *= 100
    t1 = build_engine_table(sales, panel, cfg, overrides=None, as_of=cut)["table"].set_index("stock_code")
    t2 = build_engine_table(sales2, mod, cfg, overrides=None, as_of=cut)["table"].set_index("stock_code")
    assert np.allclose(t1["eps"], t2["eps"]) and np.allclose(t1["base_units"], t2["base_units"])


def test_seasonal_index_uses_only_past(sales_panel):
    _, _, panel = sales_panel
    cut = panel["week"].sort_values().unique()[60]
    a = seasonal_index(panel, 4, as_of=cut)
    mod = panel.copy()
    mod.loc[mod["week"] > cut, "revenue"] *= 50
    assert np.allclose(a, seasonal_index(mod, 4, as_of=cut)) and (a >= 0).all()
