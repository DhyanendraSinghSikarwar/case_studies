"""Behavioural clustering: log+scale, KMeans sweep, GMM, HDBSCAN comparison, profile table."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from .config import get_logger, load_config

log = get_logger(__name__)


def prepare_features(df: pd.DataFrame, features: list[str]) -> tuple[np.ndarray, StandardScaler]:
    """log1p-transform then z-score the behavioural features. Returns (X, fitted scaler)."""
    x = np.log1p(df[features].clip(lower=0).to_numpy(dtype=float))
    scaler = StandardScaler().fit(x)
    return scaler.transform(x), scaler


def _sil(x: np.ndarray, labels: np.ndarray, sample: int, seed: int) -> float:
    """Silhouette (sampled when n is large); NaN when <2 clusters."""
    if len(set(labels)) < 2:
        return float("nan")
    n = len(x)
    ss = sample if n > sample else None
    return float(silhouette_score(x, labels, sample_size=ss, random_state=seed))


def sweep_kmeans(x: np.ndarray, cfg: dict | None = None) -> pd.DataFrame:
    """KMeans for k in [k_min, k_max]: inertia (elbow) and silhouette."""
    cfg = cfg or load_config()
    c, seed = cfg["cluster"], cfg["seed"]
    rows = []
    for k in range(c["k_min"], c["k_max"] + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(x)
        rows.append({"k": k, "inertia": float(km.inertia_),
                     "silhouette": _sil(x, km.labels_, c["silhouette_sample"], seed)})
    return pd.DataFrame(rows)


def fit_gmm_sweep(x: np.ndarray, cfg: dict | None = None) -> pd.DataFrame:
    """GMM for k in range: BIC and silhouette of the hard assignment."""
    cfg = cfg or load_config()
    c, seed = cfg["cluster"], cfg["seed"]
    rows = []
    for k in range(c["k_min"], c["k_max"] + 1):
        g = GaussianMixture(k, covariance_type=c["gmm_covariance"], random_state=seed,
                            n_init=c.get("gmm_n_init", 1)).fit(x)
        lab = g.predict(x)
        rows.append({"k": k, "bic": float(g.bic(x)),
                     "silhouette": _sil(x, lab, c["silhouette_sample"], seed)})
    return pd.DataFrame(rows)


def fit_hdbscan(x: np.ndarray, cfg: dict | None = None) -> dict:
    """HDBSCAN: labels (-1 = noise), n_clusters, noise share, silhouette on non-noise points."""
    cfg = cfg or load_config()
    c = cfg["cluster"]
    lab = HDBSCAN(min_cluster_size=c["hdbscan_min_cluster_size"], copy=True).fit_predict(x)
    keep = lab >= 0
    n_cl = len(set(lab[keep]))
    sil = _sil(x[keep], lab[keep], c["silhouette_sample"], cfg["seed"]) if n_cl >= 2 else float("nan")
    return {"labels": lab, "n_clusters": int(n_cl), "noise_share": float(1 - keep.mean()),
            "silhouette_non_noise": sil}


def name_clusters(profile: pd.DataFrame) -> dict[int, str]:
    """Give each cluster a business name from its centroid (monetary rank, frequency, recency)."""
    names: dict[int, str] = {}
    p = profile.set_index("cluster")
    top = p["monetary"].idxmax()
    med_r = p["recency"].median()
    used: set[str] = set()
    for cl in p.index:
        recent = p.loc[cl, "recency"] <= med_r
        if cl == top:
            nm = "Top spenders"
        elif p.loc[cl, "frequency"] <= 2:
            nm = "New / early" if recent else "One-off lapsed"
        else:
            nm = "Active regulars" if recent else "Lapsing regulars"
        base, i = nm, 2
        while nm in used:
            nm, i = f"{base} {i}", i + 1
        used.add(nm)
        names[int(cl)] = nm
    return names


def profile_table(df: pd.DataFrame, labels: np.ndarray, features: list[str]) -> pd.DataFrame:
    """Per-cluster size, revenue share and mean raw features."""
    d = df.copy()
    d["cluster"] = labels
    g = d.groupby("cluster").agg(
        customers=("customer_id", "size"), revenue=("monetary", "sum"),
        **{f: (f, "mean") for f in features if f != "monetary"}, monetary=("monetary", "mean"))
    g["customer_share"] = g["customers"] / g["customers"].sum()
    g["revenue_share"] = g["revenue"] / g["revenue"].sum()
    g = g.reset_index()
    g["name"] = g["cluster"].map(name_clusters(g))
    return g


def embed_2d(x: np.ndarray, cfg: dict | None = None) -> tuple[np.ndarray, str]:
    """2D embedding for the explorer: UMAP if installed, else PCA. Returns (coords, method)."""
    cfg = cfg or load_config()
    try:
        import umap

        z = umap.UMAP(n_neighbors=cfg["cluster"]["umap_neighbors"], random_state=cfg["seed"]
                      ).fit_transform(x)
        return z, "UMAP"
    except Exception as exc:  # noqa: BLE001  # pragma: no cover
        log.warning("UMAP unavailable (%s); using PCA", exc)
        return PCA(2, random_state=cfg["seed"]).fit_transform(x), "PCA"


def run_clustering(rfm: pd.DataFrame, cfg: dict | None = None, embed: bool = True) -> dict:
    """Full comparison. Returns dict with sweeps, chosen model, labels, profile, metrics.

    Final k = argmax silhouette over k >= cluster.k_final_min (k=2 splits mostly active vs lapsed
    and is not actionable). The unconstrained best k is reported too.
    """
    cfg = cfg or load_config()
    c = cfg["cluster"]
    x, scaler = prepare_features(rfm, c["features"])
    km = sweep_kmeans(x, cfg)
    gm = fit_gmm_sweep(x, cfg)
    hd = fit_hdbscan(x, cfg)
    cand = km[km["k"] >= c["k_final_min"]]
    k_final = int(cand.loc[cand["silhouette"].idxmax(), "k"])
    model = KMeans(n_clusters=k_final, n_init=10, random_state=cfg["seed"]).fit(x)
    labels = model.labels_
    prof = profile_table(rfm, labels, c["profile_features"])
    name_map = dict(zip(prof["cluster"], prof["name"], strict=True))
    out = {
        "x": x, "scaler": scaler, "kmeans_sweep": km, "gmm_sweep": gm, "hdbscan": hd,
        "k_final": k_final, "model": model, "labels": labels, "profile": prof,
        "cluster_names": [name_map[int(i)] for i in labels],
        "metrics": {
            "kmeans_best_k_any": int(km.loc[km["silhouette"].idxmax(), "k"]),
            "kmeans_best_silhouette_any": float(km["silhouette"].max()),
            "kmeans_k_final": k_final,
            "kmeans_silhouette_final": float(km.set_index("k").loc[k_final, "silhouette"]),
            "gmm_best_k_bic": int(gm.loc[gm["bic"].idxmin(), "k"]),
            "gmm_silhouette_at_k_final": float(gm.set_index("k").loc[k_final, "silhouette"]),
            "gmm_best_silhouette": float(gm["silhouette"].max()),
            "hdbscan_n_clusters": hd["n_clusters"],
            "hdbscan_noise_share": hd["noise_share"],
            "hdbscan_silhouette_non_noise": hd["silhouette_non_noise"],
            "ari_kmeans_vs_rule_segments": float(adjusted_rand_score(rfm["segment"], labels))
            if "segment" in rfm else float("nan"),
        },
    }
    abl = {}
    for nm, feats in c.get("ablation_feature_sets", {}).items():
        xa, _ = prepare_features(rfm, feats)
        sw = sweep_kmeans(xa, cfg)
        abl[nm] = {"features": feats, "best_k": int(sw.loc[sw["silhouette"].idxmax(), "k"]),
                   "best_silhouette": float(sw["silhouette"].max()),
                   "silhouette_by_k": {int(k): float(v) for k, v in zip(sw["k"], sw["silhouette"],
                                                                         strict=True)}}
    out["metrics"]["feature_set_ablation"] = abl
    if embed:
        z, method = embed_2d(x, cfg)
        out["embedding"], out["embedding_method"] = z, method
    return out
