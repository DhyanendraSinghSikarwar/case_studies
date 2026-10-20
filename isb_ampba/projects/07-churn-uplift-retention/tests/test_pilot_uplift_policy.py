import inspect

import numpy as np
import pandas as pd
import pytest

from churnx import uplift as uplift_mod
from churnx.pilot import (
    OUTCOME_COLS,
    TRUTH_COLS,
    ate_check,
    build_pilot,
    shift_to_rate,
    simulate_pilot,
    uplift_feature_matrix,
)
from churnx.policy import exact_value, ipw_value, oracle_mask, policy_table, select_policies
from churnx.snapshot import FEATURES
from churnx.uplift import MetaLearner, qini_auc, qini_curve, tau_recovery, uplift_at_k


@pytest.fixture(scope="module")
def pilot_df(snaps):
    d = snaps[snaps["split"] != "test"].reset_index(drop=True)
    p0 = np.clip(0.2 + 0.5 * d["churn"].to_numpy() * 0 + 0.3 * d["recency_days"].to_numpy() / 180, 0.05, 0.95)
    return simulate_pilot(d, p0, seed=42)


def test_simulator_is_reproducible(snaps):
    d = snaps[snaps["split"] != "test"].reset_index(drop=True)
    p0 = np.full(len(d), 0.4)
    a, b = simulate_pilot(d, p0, 7), simulate_pilot(d, p0, 7)
    c = simulate_pilot(d, p0, 8)
    pd.testing.assert_frame_equal(a[["w", "saved", "y"]], b[["w", "saved", "y"]])
    assert not a["w"].equals(c["w"])


def test_pilot_ate_close_to_true_mean_tau(pilot_df):
    chk = ate_check(pilot_df)
    assert abs(chk["observed_ate"] - chk["mean_tau_true"]) < 3 * chk["se"]
    assert abs(pilot_df["w"].mean() - 0.5) < 0.03          # randomised 50/50


def test_uplift_features_exclude_truth(pilot_df):
    X = uplift_feature_matrix(pilot_df)
    assert not set(X.columns) & (set(TRUTH_COLS) | set(OUTCOME_COLS))
    assert list(X.columns) == FEATURES
    with pytest.raises(AssertionError):
        bad = pilot_df.copy()
        import churnx.pilot as pm
        old = pm.FEATURES
        pm.FEATURES = [*FEATURES, "tau_true"]
        try:
            uplift_feature_matrix(bad)
        finally:
            pm.FEATURES = old


def test_ground_truth_never_used_by_modelling_code():
    """tau/truth columns may only be referenced by evaluation code, never inside learners/feature builders."""
    src = inspect.getsource(uplift_mod.MetaLearner) + inspect.getsource(uplift_mod.fit_learners)
    assert "tau_true" not in src and "save_rate_true" not in src and "saved" not in src
    import churnx.models as m
    import churnx.snapshot as s
    for mod in (m, s):
        src = inspect.getsource(mod)
        assert "tau_true" not in src and "save_rate_true" not in src


def test_shift_to_rate_hits_target():
    p = np.random.default_rng(0).random(500) * 0.8 + 0.1
    assert abs(shift_to_rate(p, 0.3).mean() - 0.3) < 1e-6


def test_qini_oracle_beats_random(pilot_df):
    y, w = pilot_df["retained"].to_numpy(), pilot_df["w"].to_numpy()
    q_or = qini_auc(y, w, pilot_df["tau_true"].to_numpy())
    rng = np.random.default_rng(0)
    q_rnd = np.mean([qini_auc(y, w, rng.random(len(y))) for _ in range(20)])
    assert q_or > 0
    assert abs(q_rnd) < 0.35 * q_or


def test_qini_matches_bruteforce():
    rng = np.random.default_rng(3)
    n = 400
    s, w = rng.random(n), rng.integers(0, 2, n)
    y = (rng.random(n) < 0.3 + 0.2 * w * s).astype(float)
    order = np.argsort(-s, kind="mergesort")
    ks, qs = qini_curve(y, w, s)
    for k in (50, 200, 400):                                   # independent recomputation of Q(k)
        idx = order[:k]
        yt, yc = y[idx][w[idx] == 1].sum(), y[idx][w[idx] == 0].sum()
        nt, nc = (w[idx] == 1).sum(), (w[idx] == 0).sum()
        assert qs[k - 1] == pytest.approx(yt - yc * nt / nc)
    assert uplift_at_k(y, w, s, 0.5) == pytest.approx(
        y[order[:200]][w[order[:200]] == 1].mean() - y[order[:200]][w[order[:200]] == 0].mean())


def test_qini_matches_sklift():
    sklift = pytest.importorskip("sklift.metrics")
    rng = np.random.default_rng(3)
    s, w = rng.random(500), rng.integers(0, 2, 500)
    y = (rng.random(500) < 0.3 + 0.2 * w * s).astype(int)
    ref = sklift.qini_auc_score(y, s, w)
    mine = qini_auc(y, w, s) / (len(y) ** 2)
    assert np.sign(ref) == np.sign(mine)


def test_meta_learners_recover_tau_better_than_chance():
    rng = np.random.default_rng(0)
    n = 6000
    X = rng.normal(size=(n, 4))
    tau = 0.3 * (X[:, 0] > 0)
    w = rng.integers(0, 2, n)
    y = (rng.random(n) < 0.3 + tau * w).astype(float)
    for L in ["S", "T", "X", "TO", "CT"]:
        m = MetaLearner(L, "binary", {"n_estimators": 60, "num_leaves": 6, "min_child_samples": 40,
                                      "learning_rate": 0.05}, 42).fit(X, w, y)
        th = m.predict(X)
        assert tau_recovery(th, tau)["pearson"] > 0.25, L
        assert qini_auc(y, w, th) > 0, L


def test_policy_masks_respect_budget_and_oracle_is_ceiling(pilot_df):
    n = len(pilot_df)
    value = np.exp(np.random.default_rng(0).normal(10, 1, n))
    cost = 250.0
    masks = select_policies(pilot_df["tau_true"] * 0.9, pilot_df["p0"], value, 0.3, cost, 42)
    k = int(round(0.3 * n))
    for name in ["random", "risk_top_k", "clv_top_k", "uplift_top_k"]:
        assert masks[name].sum() == k, name
    assert masks["all"].all()
    tab = policy_table(masks, pilot_df["tau_true"].to_numpy(), value, cost).set_index("policy")
    assert (tab["profit_inr"].drop("oracle") <= tab.loc["oracle", "profit_inr"] + 1e-6).all()
    assert tab.loc["oracle", "pct_of_oracle"] == pytest.approx(100.0)
    orc = oracle_mask(pilot_df["tau_true"], value, cost)
    assert exact_value(orc, pilot_df["tau_true"], value, cost) == pytest.approx(tab.loc["oracle", "profit_inr"])


def test_ipw_value_unbiased_on_simulated_rct():
    rng = np.random.default_rng(0)
    n, e, cost = 4000, 0.5, 0.2
    x = rng.random(n)
    tau = 1.0 * x                                              # true incremental money
    mask = x > 0.4
    exact = ((tau - cost) * mask).sum()
    ests = []
    for _ in range(300):
        w = (rng.random(n) < e).astype(float)
        y = 1.0 + tau * w + rng.normal(0, 1, n)
        ests.append(ipw_value(mask, w, y, e, cost))
    assert abs(np.mean(ests) - exact) < 0.05 * abs(exact) + 5 * np.std(ests) / np.sqrt(300)


def test_build_pilot_on_fixture(snaps, cfg):
    te = snaps[snaps["split"] == "test"].sort_values("customer_id")
    pil = build_pilot(snaps, np.full(len(te), 0.4), cfg)
    assert set(pil) == {"train", "test"} and len(pil["test"]) == len(te)
    assert {"w", "tau_true", "retained"} <= set(pil["train"].columns)
