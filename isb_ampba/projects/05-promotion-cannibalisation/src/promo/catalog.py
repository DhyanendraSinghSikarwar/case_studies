"""Product families: TF-IDF + agglomerative clustering, co-purchase substitution check, manual overrides."""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer

from .config import ROOT, get_logger

log = get_logger("promo.catalog")


def clean_description(desc: str, drop_words: list[str]) -> str:
    """Lower-case, strip digits/punctuation and colour/size words so families follow product type."""
    toks = re.findall(r"[a-z]{2,}", str(desc).lower())
    drop = set(drop_words)
    return " ".join(t for t in toks if t not in drop)


def _name_families(df: pd.DataFrame) -> pd.DataFrame:
    """Family name = description of the top-revenue member; recompute n_members."""
    df = df.copy()
    top = df.sort_values("revenue", ascending=False).drop_duplicates("family").set_index("family")["description"]
    df["family_name"] = df["family"].map(top)
    df["n_members"] = df.groupby("family")["stock_code"].transform("size")
    return df


def build_families(sku_table: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Cluster SKUs into families.

    sku_table: stock_code, description, revenue. The top ``families.top_skus`` SKUs by revenue are clustered
    (cosine distance, average linkage, distance threshold); all others and SKUs with no usable tokens are singletons.
    Returns stock_code, description, revenue, family, family_name, n_members (every SKU exactly once).
    """
    fc = cfg["families"]
    df = sku_table.sort_values(["revenue", "stock_code"], ascending=[False, True]).reset_index(drop=True).copy()
    df["text"] = [clean_description(d, fc["drop_words"]) for d in df["description"]]
    df["cluster"] = -1
    top = df.head(fc["top_skus"])
    ok = top["text"].str.len() > 0
    if ok.sum() >= 2:
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english", token_pattern=r"[A-Za-z]{2,}")
        X = vec.fit_transform(top.loc[ok, "text"])
        lab = AgglomerativeClustering(
            n_clusters=None, distance_threshold=fc["distance_threshold"], metric="cosine", linkage="average"
        ).fit_predict(X.toarray())
        df.loc[top.index[ok.to_numpy()], "cluster"] = lab
    # family id: ordered by first appearance (= highest-revenue member); singletons get their own id
    fam_ids: dict = {}
    out = []
    for idx, c in zip(df.index, df["cluster"]):
        key = ("c", int(c)) if c >= 0 else ("s", int(idx))
        if key not in fam_ids:
            fam_ids[key] = f"F{len(fam_ids) + 1:04d}"
        out.append(fam_ids[key])
    df["family"] = out
    df = _name_families(df)
    n_multi = int((df.drop_duplicates("family")["n_members"] >= fc["min_family_size"]).sum())
    log.info("families: %d total, %d multi-SKU", df["family"].nunique(), n_multi)
    return df.drop(columns=["text", "cluster"])


def apply_overrides(fam: pd.DataFrame, path: str | Path | None) -> pd.DataFrame:
    """Apply a manual override CSV (stock_code,family) last; an unknown family id creates a new family."""
    if path is None:
        return fam
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    if not p.exists():
        return fam
    ov = pd.read_csv(p, dtype=str).dropna()
    if ov.empty:
        return fam
    fam = fam.copy()
    mapping = dict(zip(ov["stock_code"].str.strip().str.upper(), ov["family"].str.strip()))
    mask = fam["stock_code"].isin(mapping)
    fam.loc[mask, "family"] = fam.loc[mask, "stock_code"].map(mapping)
    log.info("applied %d family overrides", int(mask.sum()))
    return _name_families(fam)


def copurchase_share(sales: pd.DataFrame, fam: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Co-purchase substitution check.

    For each multi-SKU family: of the invoices containing at least one member, the share containing at least two
    distinct members. True substitutes are rarely bought together; a high share flags a weak-substitute family
    whose cannibalisation is capped in the engine.
    """
    fc = cfg["families"]
    multi = fam[fam["n_members"] >= fc["min_family_size"]]
    m = multi.set_index("stock_code")["family"]
    s = sales[sales["stock_code"].isin(m.index)][["invoice", "stock_code"]].drop_duplicates()
    s["family"] = s["stock_code"].map(m)
    per = s.groupby(["family", "invoice"]).size()
    n_inv = per.groupby("family").size()
    n_multi = (per >= 2).groupby("family").sum()
    out = pd.DataFrame({"n_invoices_with_member": n_inv, "n_invoices_multi": n_multi}).reset_index()
    out["copurchase_share"] = out["n_invoices_multi"] / out["n_invoices_with_member"]
    out["weak_substitute"] = out["copurchase_share"] > fc["copurchase_weak_threshold"]
    sizes = multi.drop_duplicates("family").set_index("family")["n_members"]
    out["n_members"] = out["family"].map(sizes)
    return out.sort_values("copurchase_share", ascending=False).reset_index(drop=True)


def substitution_weights(fam: pd.DataFrame, cop: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Add weak_sub flag and sub_weight (1.0 strong, weak_sub_weight for weak-substitute families)."""
    fam = fam.copy()
    weak = set(cop.loc[cop["weak_substitute"], "family"])
    fam["weak_sub"] = fam["family"].isin(weak)
    fam["sub_weight"] = np.where(fam["weak_sub"], cfg["families"]["weak_sub_weight"], 1.0)
    return fam
