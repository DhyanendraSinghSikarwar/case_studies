import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from churnx.models import fit_all, fit_calibrated, group_splits, lift_table, make_models, metrics
from churnx.snapshot import FEATURES
from churnx.threshold import best_threshold, expected_profit, sweep_thresholds, threshold_report


def _train_test(snaps):
    tr, te = snaps[snaps["split"] == "train"], snaps[snaps["split"] == "test"]
    return tr, te


def test_group_calibration_never_splits_customers(snaps):
    tr, _ = _train_test(snaps)
    groups = tr["customer_id"].to_numpy()
    assert len(set(groups)) < len(groups)                     # customers repeat across snapshots
    for a, b in group_splits(tr[FEATURES], tr["churn"].to_numpy(), groups, 3):
        assert not set(groups[a]) & set(groups[b])


def test_models_beat_naive_baseline_on_temporal_split(snaps, cfg):
    tr, te = _train_test(snaps)
    res = fit_all(tr[FEATURES], tr["churn"].to_numpy(), tr["customer_id"].to_numpy(), te[FEATURES],
                  te["churn"].to_numpy(), cfg)
    assert res["metrics"]["baseline_train_rate"]["auc"] == 0.5
    for name in ["logit", "rf", "xgb", "lgbm"]:
        assert res["metrics"][name]["auc"] > 0.6, name
    assert res["champion"] in res["cv_auc"]
    assert res["p_test_cal"].min() >= 0 and res["p_test_cal"].max() <= 1


def test_calibrated_model_probabilities_valid(snaps, cfg):
    tr, te = _train_test(snaps)
    cal = fit_calibrated(make_models(42)["logit"], tr[FEATURES], tr["churn"].to_numpy(), tr["customer_id"].to_numpy())
    p = cal.predict_proba(te[FEATURES])[:, 1]
    assert 0 <= p.min() <= p.max() <= 1
    assert roc_auc_score(te["churn"], p) > 0.6


def test_lift_table_invariants():
    rng = np.random.default_rng(0)
    p = rng.random(1000)
    y = (rng.random(1000) < p).astype(int)
    t = lift_table(y, p)
    assert t["n"].sum() == 1000 and abs(t["cum_capture"].iloc[-1] - 1.0) < 1e-9
    assert t["churn_rate"].iloc[0] > t["churn_rate"].iloc[-1]
    assert set(metrics(y, p)) >= {"auc", "pr_auc", "ks", "brier"}


def test_expected_profit_sign():
    assert expected_profit(np.array([0.5]), np.array([100.0]), 250.0, 0.2)[0] < 0      # 10 < 250
    assert expected_profit(np.array([0.9]), np.array([10000.0]), 250.0, 0.2)[0] > 0


def test_threshold_profit_is_maximal_on_grid():
    rng = np.random.default_rng(1)
    p, v = rng.random(500), np.exp(rng.normal(9, 1, 500))
    sw = sweep_thresholds(p, v, 250.0, 0.2)
    best = best_threshold(sw)
    assert best["profit_inr"] == sw["profit_inr"].max()
    assert sw.iloc[-1]["n_contacted"] == 0 and sw.iloc[-1]["profit_inr"] == 0.0     # contact nobody = 0
    # brute-force the best threshold independently
    brute = max(expected_profit(p[p >= t], v[p >= t], 250.0, 0.2).sum() for t in np.linspace(0, 0.95, 96))
    assert best["profit_inr"] >= max(brute, 0.0) - 1e-6


def test_threshold_report_never_worse_than_nobody_or_everybody():
    rng = np.random.default_rng(2)
    p, m = rng.random(300), np.exp(rng.normal(6, 1, 300))
    biz = {"gbp_to_inr": 105.0, "gross_margin": 0.3, "clv_months": 12, "offer_cost_inr": 250.0, "save_rate": 0.2}
    rep = threshold_report(p, m, biz)
    assert rep["best"]["profit_inr"] >= 0
    assert rep["best"]["profit_inr"] >= rep["profit_contact_all_inr"] - 1e-6


def test_temporal_window_check_is_train_only(snaps):
    from churnx.models import temporal_window_check

    w = temporal_window_check(snaps, FEATURES)
    test_asof = snaps[snaps["split"] == "test"]["asof"].min()
    assert pd.Timestamp(w["validation_snapshot"]) < test_asof
    keys = [k for k in w if "__C=" in k]
    assert len(keys) == 4 and all(0.5 < w[k] <= 1 for k in keys)
