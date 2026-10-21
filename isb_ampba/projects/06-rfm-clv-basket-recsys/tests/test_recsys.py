"""Tests for recommenders, time split and metrics."""
from __future__ import annotations

import numpy as np
import pandas as pd

from crm.recsys import (
    Interactions,
    als_model,
    als_scores,
    ndcg_hit_per_user,
    own_history_eval,
    own_history_scores,
    popularity_scores,
    run_recsys,
    time_split,
    topk,
)

SPLIT = ("2011-11-09", "2011-11-10", "2011-12-09")


def test_ndcg_hand_computed():
    rec = np.array([[2, 0, 1], [5, 6, 7]])
    nd, hit, _ = ndcg_hit_per_user(rec, [{2}, {0}], 3)
    assert nd[0] == 1.0 and hit[0] == 1.0
    assert nd[1] == 0.0 and hit[1] == 0.0
    nd2, _, rc2 = ndcg_hit_per_user(np.array([[9, 0, 1]]), [{0, 1}], 3)
    ideal = 1 / np.log2(2) + 1 / np.log2(3)
    assert np.isclose(nd2[0], (1 / np.log2(3) + 1 / np.log2(4)) / ideal) and rc2[0] == 1.0


def test_topk_excludes_seen_and_sorts():
    import scipy.sparse as sp

    s = np.array([[0.1, 0.9, 0.5, 0.7]])
    assert list(topk(s, 2)[0]) == [1, 3]
    seen = sp.csr_matrix(np.array([[0, 1, 0, 0]]))
    assert list(topk(s, 2, seen)[0]) == [3, 2]


def test_time_split_no_leakage(sales):
    tr, te = time_split(sales, *SPLIT)
    assert tr["invoice_date"].max() < te["invoice_date"].min()
    assert te["invoice_date"].min() >= pd.Timestamp("2011-11-10")
    assert te["invoice_date"].max() < pd.Timestamp("2011-12-10")


def test_no_test_data_in_recsys_training(sales):
    """Tampering with test-window purchases must not change the train matrix or ALS scores."""
    tr, te = time_split(sales, *SPLIT)
    te2 = te.copy()
    te2["stock_code"] = te2["stock_code"].iloc[::-1].to_numpy()
    sales2 = pd.concat([sales[~sales.index.isin(te.index)], te2])
    tr2, _ = time_split(sales2, *SPLIT)
    i1, i2 = Interactions(tr), Interactions(tr2)
    assert (i1.matrix != i2.matrix).nnz == 0 and list(i1.items) == list(i2.items)
    s1 = als_scores(als_model(i1.matrix, 8, 0.1, 5, 5, 42), np.arange(10))
    s2 = als_scores(als_model(i2.matrix, 8, 0.1, 5, 5, 42), np.arange(10))
    assert np.allclose(s1, s2)


def test_popularity_is_global_and_user_independent(sales):
    tr, _ = time_split(sales, *SPLIT)
    m = Interactions(tr).matrix
    p = popularity_scores(m, 4)
    assert (p == p[0]).all() and p[0].max() <= m.shape[0]


def test_run_recsys_beats_random_and_reports_protocols(sales, fast_cfg):
    o = run_recsys(sales, fast_cfg)
    for prot in ("repeat_allowed", "discovery"):
        r = o["metrics"][prot]
        assert r["als"]["ndcg"] > r["random"]["ndcg"]
        assert 0 <= r["als"]["hitrate"] <= 1 and 0 < r["als"]["coverage"] <= 1
    assert o["metrics"]["train_max_date"] < o["metrics"]["test_min_date"]


def test_own_history_baseline_ranks_own_items_and_is_personal(sales):
    tr, _ = time_split(sales, *SPLIT)
    m = Interactions(tr).matrix
    rows = np.arange(5)
    sc = own_history_scores(m, rows)
    top = topk(sc, 1)
    dense = m[rows].toarray()
    for r in range(5):
        if dense[r].max() > 0:                       # most-bought own item ranks first
            assert dense[r, top[r, 0]] == dense[r].max()
    assert not (sc == sc[0]).all()                   # unlike popularity, differs per user


def test_own_history_eval_reports_both_protocols(sales, fast_cfg):
    ev = own_history_eval(sales, fast_cfg)
    assert set(ev) == {"repeat_allowed", "discovery"}
    # discovery masks seen items, so the baseline cannot beat itself being popularity-like: just bounded
    assert 0 <= ev["discovery"]["ndcg"] <= 1 and 0 <= ev["repeat_allowed"]["hitrate"] <= 1
