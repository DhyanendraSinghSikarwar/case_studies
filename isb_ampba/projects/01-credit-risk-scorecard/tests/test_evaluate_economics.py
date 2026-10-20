from __future__ import annotations

import numpy as np

from credit import economics as eco
from credit import evaluate as ev
from credit import fairness, monitor
from credit.data import clean
from credit.features import add_features


def test_ks_perfect_and_random():
    rng = np.random.default_rng(0)
    y = np.array([0] * 50 + [1] * 50)
    assert ev.ks(y, np.r_[np.zeros(50), np.ones(50)]) == 1.0
    assert ev.ks(rng.integers(0, 2, 5000), rng.uniform(size=5000)) < 0.06


def test_calibration_slope_near_one_for_calibrated_scores():
    rng = np.random.default_rng(1)
    p = rng.uniform(0.02, 0.9, 40000)
    y = (rng.uniform(size=p.size) < p).astype(int)
    assert 0.9 < ev.calibration_slope(y, p) < 1.1


def test_psi_zero_for_identical_and_positive_for_shift():
    x = np.random.default_rng(2).normal(size=5000)
    assert ev.psi(x, x) == 0
    assert ev.psi(x, x + 1) > 0.2


def _sim(n=100000):
    rng = np.random.default_rng(3)
    p = rng.beta(2, 6, n)
    y = (rng.uniform(size=n) < p).astype(int)
    return p, np.full(n, 1000.0), y


def test_profit_is_maximised_near_breakeven_pd(cfg):
    p, ead, y = _sim()
    cur = eco.profit_curve(p, ead, y, 0.18, 0.65, eco.cutoff_grid(cfg))
    best = eco.find_optimal_cutoff(cur)["cutoff"]
    assert abs(best - 0.18 / (0.18 + 0.65)) < 0.05


def test_approve_all_equals_sum_of_unit_profit():
    p, ead, y = _sim(5000)
    cur = eco.profit_curve(p, ead, y, 0.18, 0.65, [1.0])
    assert np.isclose(cur["exp_profit"].iloc[0], eco.unit_profit(p, ead, 0.18, 0.65).sum())


def test_make_ead_floor_and_scaling():
    e = eco.make_ead([100000, 100000], [0.0, 0.5], fx=2.0)
    assert np.allclose(e, [100000 * 0.05 * 2, 100000 * 0.5 * 2])


def test_limit_action_follows_config(cfg):
    assert eco.limit_action("A", cfg["limits"])["action"] == "increase"
    assert eco.limit_action("E", cfg["limits"])["action"] == "decline"
    v = eco.limit_engine_value(np.array(["E", "E"]), [0.5, 0.6], [1.0, 1.0], 0.18, 0.65, cfg["limits"])
    assert v["profit_after"].iloc[0] == 0.0


def test_disparate_impact_ratio():
    y = np.array([0, 1] * 50)
    p = np.full(100, 0.2)
    appr = np.r_[np.ones(40, bool), np.zeros(10, bool), np.ones(20, bool), np.zeros(30, bool)]
    g = np.array(["a"] * 50 + ["b"] * 50)
    rep = fairness.disparate_impact(fairness.group_report(y, p, appr, g)).set_index("group")
    assert np.isclose(rep.loc["b", "di_ratio"], 0.5)
    assert not rep.loc["b", "passes_80pct"]


def test_drift_simulation_triggers_psi_alert(raw, cfg):
    base = add_features(clean(raw))
    shifted = monitor.simulate_limit_shift(clean(raw), -0.20)
    t = monitor.csi_table(base, shifted, ["LIMIT_BAL"], cfg["monitoring"]["psi_alert"])
    assert t["psi"].iloc[0] > 0.2 and t["status"].iloc[0] == "ALERT"
