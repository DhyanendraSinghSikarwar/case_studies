"""Tests for clustering utilities."""
from __future__ import annotations

import numpy as np
import pandas as pd

from crm.cluster import prepare_features, run_clustering, sweep_kmeans
from crm.rfm import build_rfm


def test_prepare_features_standardised(cal_hold, cfg):
    r = build_rfm(cal_hold[0], pd.Timestamp("2011-07-01"), cfg)
    x, _ = prepare_features(r, cfg["cluster"]["features"])
    assert np.allclose(x.mean(axis=0), 0, atol=1e-8) and np.allclose(x.std(axis=0), 1, atol=1e-8)


def test_sweep_and_run_clustering(cal_hold, fast_cfg):
    r = build_rfm(cal_hold[0], pd.Timestamp("2011-07-01"), fast_cfg)
    x, _ = prepare_features(r, fast_cfg["cluster"]["features"])
    sw = sweep_kmeans(x, fast_cfg)
    assert list(sw["k"]) == [2, 3, 4, 5] and sw["silhouette"].between(-1, 1).all()
    assert (sw["inertia"].diff().dropna() < 0).all()           # inertia falls as k grows
    a = run_clustering(r, fast_cfg, embed=False)
    b = run_clustering(r, fast_cfg, embed=False)
    assert np.array_equal(a["labels"], b["labels"])            # seeded -> reproducible
    assert a["k_final"] >= fast_cfg["cluster"]["k_final_min"]
    assert a["profile"]["customers"].sum() == len(r)
    assert abs(a["profile"]["revenue_share"].sum() - 1) < 1e-9
