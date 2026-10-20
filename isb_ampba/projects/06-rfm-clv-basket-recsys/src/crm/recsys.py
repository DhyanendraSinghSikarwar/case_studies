"""Recommenders: popularity, item-item cosine CF, implicit ALS (+ popularity hybrid).

Evaluation is strictly time-based: models see interactions up to `train_end`; the test set is
the last 30 days. Two protocols are reported (DATA.md pitfall 5):
  * repeat_allowed - already-bought items may be recommended and count as hits (re-orders);
  * discovery      - already-bought items are excluded from ranking and from the positives.
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.preprocessing import normalize
from threadpoolctl import threadpool_limits

from .config import get_logger, load_config

log = get_logger(__name__)


class Interactions:
    """User x item implicit-feedback matrix with id maps (count of distinct invoices)."""

    def __init__(self, df: pd.DataFrame, users: pd.Index | None = None,
                 items: pd.Index | None = None) -> None:
        g = df.groupby(["customer_id", "stock_code"])["invoice"].nunique().rename("n").reset_index()
        self.users = users if users is not None else pd.Index(sorted(g["customer_id"].unique()))
        self.items = items if items is not None else pd.Index(sorted(g["stock_code"].unique()))
        g = g[g["customer_id"].isin(self.users) & g["stock_code"].isin(self.items)]
        ui = self.users.get_indexer(g["customer_id"])
        ii = self.items.get_indexer(g["stock_code"])
        self.matrix = sp.csr_matrix((g["n"].to_numpy(float), (ui, ii)),
                                    shape=(len(self.users), len(self.items)))


def time_split(sales: pd.DataFrame, train_end: str, test_start: str, test_end: str
               ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """train = lines with date <= train_end (end of day); test = [test_start, test_end]."""
    d = sales["invoice_date"]
    tr = sales[d < pd.Timestamp(train_end) + pd.Timedelta(days=1)]
    te = sales[(d >= pd.Timestamp(test_start)) & (d < pd.Timestamp(test_end) + pd.Timedelta(days=1))]
    assert tr["invoice_date"].max() < te["invoice_date"].min() if len(te) and len(tr) else True
    return tr, te


# ----------------------------------------------------------------------------- scorers
def popularity_scores(train: sp.csr_matrix, n_users: int) -> np.ndarray:
    """Global popularity (number of distinct buyers per item) repeated for each user row."""
    pop = np.asarray((train > 0).sum(axis=0)).ravel().astype(float)
    return np.tile(pop, (n_users, 1))


def itemknn_scores(train: sp.csr_matrix, rows: np.ndarray) -> np.ndarray:
    """Item-item cosine CF on the binary matrix: score = user_vector @ item_similarity."""
    b = (train > 0).astype(np.float32)
    bn = normalize(b, axis=0)          # unit-norm item columns
    sim = (bn.T @ bn).toarray()        # items x items cosine
    return np.asarray(b[rows] @ sim)


def als_model(train: sp.csr_matrix, factors: int, regularization: float, alpha: float,
              iterations: int, seed: int):
    """Fit implicit ALS on confidence = alpha * log1p(count) (user x item)."""
    from implicit.als import AlternatingLeastSquares

    conf = train.copy()
    conf.data = alpha * np.log1p(conf.data)
    model = AlternatingLeastSquares(factors=factors, regularization=regularization,
                                    iterations=iterations, random_state=seed,
                                    calculate_training_loss=False, use_gpu=False)
    with threadpool_limits(1, "blas"):
        model.fit(conf.tocsr(), show_progress=False)
    return model


def als_scores(model, rows: np.ndarray) -> np.ndarray:
    """Dense scores for user rows from ALS factors."""
    return np.asarray(model.user_factors[rows] @ model.item_factors.T)


def _minmax_rows(s: np.ndarray) -> np.ndarray:
    lo, hi = s.min(axis=1, keepdims=True), s.max(axis=1, keepdims=True)
    return (s - lo) / np.where(hi - lo > 0, hi - lo, 1.0)


def hybrid_scores(als: np.ndarray, pop: np.ndarray, w: float) -> np.ndarray:
    """(1-w) * minmax(ALS) + w * minmax(log1p popularity), row-wise."""
    return (1 - w) * _minmax_rows(als) + w * _minmax_rows(np.log1p(pop))


# ----------------------------------------------------------------------------- evaluation
def topk(scores: np.ndarray, k: int, seen: sp.csr_matrix | None = None) -> np.ndarray:
    """Top-k item indices per row (descending); `seen` entries are excluded when given."""
    s = scores.astype(float).copy()
    if seen is not None:
        r, c = seen.nonzero()
        s[r, c] = -np.inf
    idx = np.argpartition(-s, kth=min(k, s.shape[1] - 1), axis=1)[:, :k]
    order = np.argsort(-np.take_along_axis(s, idx, axis=1), axis=1)
    return np.take_along_axis(idx, order, axis=1)


def ndcg_hit_per_user(rec: np.ndarray, positives: list[set[int]], k: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-user binary NDCG@k, hit@k and recall@k."""
    disc = 1.0 / np.log2(np.arange(2, k + 2))
    nd, hit, rc = [], [], []
    for r, pos in zip(rec, positives, strict=True):
        rel = np.array([1.0 if i in pos else 0.0 for i in r[:k]])
        dcg = float((rel * disc[: len(rel)]).sum())
        idcg = float(disc[: min(len(pos), k)].sum())
        nd.append(dcg / idcg if idcg > 0 else 0.0)
        hit.append(float(rel.sum() > 0))
        rc.append(float(rel.sum() / len(pos)))
    return np.array(nd), np.array(hit), np.array(rc)


def build_eval_sets(train_inter: Interactions, test_df: pd.DataFrame, protocol: str
                    ) -> tuple[np.ndarray, list[set[int]]]:
    """Eval rows (user indices in train matrix) and their positive item index sets."""
    t = test_df[["customer_id", "stock_code"]].drop_duplicates()
    t = t[t["customer_id"].isin(train_inter.users) & t["stock_code"].isin(train_inter.items)]
    ui = train_inter.users.get_indexer(t["customer_id"])
    ii = train_inter.items.get_indexer(t["stock_code"])
    pos: dict[int, set[int]] = {}
    for u, i in zip(ui, ii, strict=True):
        pos.setdefault(int(u), set()).add(int(i))
    if protocol == "discovery":
        tm = train_inter.matrix.tocsr()
        for u in list(pos):
            seen = set(tm.indices[tm.indptr[u]: tm.indptr[u + 1]])
            pos[u] = pos[u] - seen
            if not pos[u]:
                del pos[u]
    rows = np.array(sorted(pos))
    return rows, [pos[int(u)] for u in rows]


def evaluate_scores(scores: np.ndarray, rows: np.ndarray, positives: list[set[int]],
                    train: sp.csr_matrix, protocol: str, k: int) -> dict:
    """HitRate@k, NDCG@k, Recall@k, catalogue coverage; scores has one row per eval user."""
    seen = train[rows] if protocol == "discovery" else None
    rec = topk(scores, k, seen)
    nd, hit, rc = ndcg_hit_per_user(rec, positives, k)
    return {"hitrate": float(hit.mean()), "ndcg": float(nd.mean()), "recall": float(rc.mean()),
            "coverage": float(len(np.unique(rec)) / train.shape[1]), "n_users": len(rows),
            "_ndcg_users": nd, "_hit_users": hit, "_rec": rec}


def _score_all(name: str, train: sp.csr_matrix, rows: np.ndarray, **kw) -> np.ndarray:
    if name == "popularity":
        return popularity_scores(train, len(rows))
    if name == "itemknn":
        return itemknn_scores(train, rows)
    raise ValueError(name)


def tune_als(train_inter: Interactions, val_df: pd.DataFrame, cfg: dict) -> tuple[dict, pd.DataFrame, float]:
    """Grid-search ALS (and hybrid weight) on a validation window INSIDE the training period."""
    rc = cfg["recsys"]
    protocol, k = rc["primary_protocol"], rc["k"]
    rows, pos = build_eval_sets(train_inter, val_df, protocol)
    tr = train_inter.matrix
    pop = popularity_scores(tr, len(rows))
    g = rc["als_grid"]
    res = []
    for f, reg, a, it in itertools.product(g["factors"], g["regularization"], g["alpha"],
                                           g["iterations"]):
        m = als_model(tr, f, reg, a, it, cfg["seed"])
        sc = als_scores(m, rows)
        e = evaluate_scores(sc, rows, pos, tr, protocol, k)
        res.append({"factors": f, "regularization": reg, "alpha": a, "iterations": it,
                    "val_ndcg": e["ndcg"], "val_hitrate": e["hitrate"]})
    df = pd.DataFrame(res).sort_values("val_ndcg", ascending=False).reset_index(drop=True)
    best = df.iloc[0].to_dict()
    m = als_model(tr, int(best["factors"]), best["regularization"], best["alpha"],
                  int(best["iterations"]), cfg["seed"])
    sc = als_scores(m, rows)
    hres = []
    for w in rc["hybrid_weights"]:
        e = evaluate_scores(hybrid_scores(sc, pop, w), rows, pos, tr, protocol, k)
        hres.append((w, e["ndcg"]))
    best_w = max(hres, key=lambda x: x[1])[0]
    best = {k_: (int(v) if k_ in ("factors", "iterations") else float(v)) for k_, v in best.items()
            if k_ in ("factors", "regularization", "alpha", "iterations")}
    return best, df, float(best_w)


def run_recsys(sales: pd.DataFrame, cfg: dict | None = None) -> dict:
    """Tune on the validation split, refit on the full training period, evaluate on the last 30 days."""
    cfg = cfg or load_config()
    rc = cfg["recsys"]
    k = rc["k"]
    train_df, test_df = time_split(sales, rc["train_end"], rc["test_start"], rc["test_end"])
    # --- tuning (only uses data <= train_end)
    sub_tr, val_df = time_split(train_df, rc["val_train_end"],
                                str(pd.Timestamp(rc["val_train_end"]) + pd.Timedelta(days=1))[:10],
                                rc["train_end"])
    best, tuning_df, best_w = tune_als(Interactions(sub_tr), val_df, cfg)
    log.info("best ALS %s hybrid_w=%.2f", best, best_w)
    # --- final fit and test
    inter = Interactions(train_df)
    tr = inter.matrix
    model = als_model(tr, best["factors"], best["regularization"], best["alpha"],
                      best["iterations"], cfg["seed"])
    out: dict = {"metrics": {}, "best_params": best, "best_hybrid_weight": best_w,
                 "tuning": tuning_df, "inter": inter, "model": model}
    users_per_protocol = {}
    for protocol in ("repeat_allowed", "discovery"):
        rows, pos = build_eval_sets(inter, test_df, protocol)
        users_per_protocol[protocol] = len(rows)
        pop = popularity_scores(tr, len(rows))
        als = als_scores(model, rows)
        cands = {"popularity": pop, "itemknn_cosine": itemknn_scores(tr, rows), "als": als,
                 "hybrid_als_pop": hybrid_scores(als, pop, best_w)}
        # random baseline for sanity
        rng = np.random.default_rng(cfg["seed"])
        cands["random"] = rng.random(pop.shape)
        res = {n: evaluate_scores(s, rows, pos, tr, protocol, k) for n, s in cands.items()}
        pm = res["popularity"]["_ndcg_users"]
        boot = {}
        rng = np.random.default_rng(cfg["seed"])
        for n in ("itemknn_cosine", "als", "hybrid_als_pop"):
            v = res[n]["_ndcg_users"]
            ratios = []
            for _ in range(rc["bootstrap"]):
                ix = rng.integers(0, len(v), len(v))
                ratios.append(v[ix].mean() / max(pm[ix].mean(), 1e-12))
            boot[n] = [float(np.percentile(ratios, 2.5)), float(np.percentile(ratios, 97.5))]
        out["metrics"][protocol] = {
            n: {kk: vv for kk, vv in r.items() if not kk.startswith("_")} for n, r in res.items()}
        for n in ("itemknn_cosine", "als", "hybrid_als_pop"):
            out["metrics"][protocol][n]["ndcg_ratio_vs_popularity"] = (
                res[n]["ndcg"] / res["popularity"]["ndcg"])
            out["metrics"][protocol][n]["ndcg_ratio_ci95"] = boot[n]
            out["metrics"][protocol][n]["hitrate_ratio_vs_popularity"] = (
                res[n]["hitrate"] / res["popularity"]["hitrate"])
    out["metrics"]["n_eval_users"] = users_per_protocol
    out["metrics"]["train_rows"] = len(train_df)
    out["metrics"]["test_rows"] = len(test_df)
    out["metrics"]["n_users_train"] = len(inter.users)
    out["metrics"]["n_items_train"] = len(inter.items)
    out["metrics"]["train_max_date"] = str(train_df["invoice_date"].max())
    out["metrics"]["test_min_date"] = str(test_df["invoice_date"].min())
    return out


def recommend_for_users(result: dict, user_ids: list[int], k: int = 10,
                        exclude_seen: bool = False, use_hybrid: bool = True) -> dict[int, list[str]]:
    """Top-k stock codes per user from the final model (hybrid when use_hybrid)."""
    inter: Interactions = result["inter"]
    rows = inter.users.get_indexer(user_ids)
    ok = rows >= 0
    rows_ok = rows[ok]
    als = als_scores(result["model"], rows_ok)
    sc = hybrid_scores(als, popularity_scores(inter.matrix, len(rows_ok)),
                       result["best_hybrid_weight"]) if use_hybrid else als
    rec = topk(sc, k, inter.matrix[rows_ok] if exclude_seen else None)
    uid_ok = np.array(user_ids)[ok]
    return {int(u): [inter.items[i] for i in r] for u, r in zip(uid_ok, rec, strict=True)}
