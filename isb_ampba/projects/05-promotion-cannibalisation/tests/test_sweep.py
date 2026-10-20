import numpy as np

from promo.sweep import classification_accuracy, draw_conditions, param_ranges, parametric_scores, run_sweep, sweep_summary, tornado


def test_sweep_reproducible(cfg):
    a = run_sweep(cfg, 0.10, 0.4)
    b = run_sweep(cfg, 0.10, 0.4)
    assert a.equals(b)
    assert not draw_conditions(cfg, seed=1).equals(draw_conditions(cfg, seed=2))


def test_sweep_size_and_ranges(cfg):
    full = draw_conditions({**cfg, "sweep": {**cfg["sweep"], "n_draws": 2000}})
    assert len(full) >= 1000
    lo, hi = param_ranges(cfg)
    assert (full.to_numpy() >= lo - 1e-12).all() and (full.to_numpy() <= hi + 1e-12).all()


def test_parametric_identity_and_signs():
    eps = np.array([-1.0, -3.0, -6.0])
    s = np.array([0.0, 0.4, 0.8])
    m = np.array([0.3, 0.4, 0.5])
    h = np.array([0.0, 0.5, 1.0])
    r = parametric_scores(eps, s, m, h, 0.1, 0.5)
    assert np.allclose(r["family_net"], r["direct_uplift"] - r["subsidy_cost"] - r["cannibalised_margin"] + r["halo_margin"], atol=1e-12)
    assert (r["cannibalised_margin"] >= 0).all() and (r["subsidy_cost"] > 0).all()
    z = parametric_scores(-3.0, 0.4, 0.4, 0.5, 0.0, 0.5)
    assert abs(float(z["family_net"])) < 1e-12


def test_family_view_never_exceeds_promoted_only_without_halo(cfg):
    df = run_sweep({**cfg, "sweep": {**cfg["sweep"], "halo": [0.0, 1e-9]}}, 0.10, 0.5)
    assert (df["family_net"] <= df["promoted_only"] + 1e-8).all()
    assert df["dashboard_trap"].any()


def test_summary_tornado_kpi(cfg):
    df = run_sweep(cfg, 0.10, 0.4)
    s = sweep_summary(df)
    assert s["n_draws"] == len(df) and 0 <= s["pct_family_profitable"] <= 100
    t = tornado(cfg, 0.10, 0.4)
    assert set(t["param"]) == {"elasticity", "substitution_share", "margin", "halo"} and (t["swing"] >= 0).all()
    k = classification_accuracy(cfg, 0.10, 0.4)
    assert 0 <= k["dashboard_accuracy_pct"] <= 100 and k["engine_accuracy_pct_noise_10"] >= k["engine_accuracy_pct_noise_50"]
