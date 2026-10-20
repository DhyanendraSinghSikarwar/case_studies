"""Basket association rules (FP-Growth) and halo pull per promoted SKU."""
from __future__ import annotations

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth

from .config import get_logger

log = get_logger("promo.baskets")

RULE_COLS = ["antecedent", "consequent", "support", "confidence", "lift"]


def basket_matrix(sales: pd.DataFrame, top_skus: int) -> pd.DataFrame:
    """Boolean invoice x SKU matrix restricted to the top_skus SKUs by invoice count."""
    inv = sales[["invoice", "stock_code"]].drop_duplicates()
    top = inv["stock_code"].value_counts().head(top_skus).index
    inv = inv[inv["stock_code"].isin(top)]
    ri, rows = pd.factorize(inv["invoice"])
    ci, cols = pd.factorize(inv["stock_code"])
    m = np.zeros((len(rows), len(cols)), dtype=bool)
    m[ri, ci] = True
    return pd.DataFrame(m, columns=cols)


def mine_rules(basket: pd.DataFrame, fam_of: dict[str, str], cfg: dict) -> pd.DataFrame:
    """FP-Growth -> single-item rules with lift/confidence filters; same-family consequents are excluded."""
    bc = cfg["baskets"]
    empty = pd.DataFrame(columns=RULE_COLS)
    if basket.empty:
        return empty
    fi = fpgrowth(basket, min_support=bc["min_support"], use_colnames=True, max_len=2)
    if fi.empty or not (fi["itemsets"].map(len) >= 2).any():
        return empty
    try:
        rules = association_rules(fi, num_itemsets=len(basket), metric="lift", min_threshold=bc["min_lift"])
    except TypeError:  # older mlxtend without num_itemsets
        rules = association_rules(fi, metric="lift", min_threshold=bc["min_lift"])
    rules = rules[
        (rules["antecedents"].map(len) == 1) & (rules["consequents"].map(len) == 1) & (rules["confidence"] >= bc["min_confidence"])
    ]
    out = pd.DataFrame({
        "antecedent": rules["antecedents"].map(lambda s: next(iter(s))),
        "consequent": rules["consequents"].map(lambda s: next(iter(s))),
        "support": rules["support"], "confidence": rules["confidence"], "lift": rules["lift"],
    })
    same = out["antecedent"].map(fam_of) == out["consequent"].map(fam_of)
    log.info("rules: %d kept, %d dropped as same-family", int((~same).sum()), int(same.sum()))
    return out[~same].reset_index(drop=True)


def halo_table(rules: pd.DataFrame, price_of: dict[str, float]) -> pd.DataFrame:
    """Per promoted SKU: halo_units = sum conf(i->k); halo_rev_per_unit = sum conf(i->k) * list price of k.

    Confidence is an association, not a causal pull; the engine multiplies by halo_factor.
    """
    if rules.empty:
        return pd.DataFrame(columns=["stock_code", "halo_units", "halo_rev_per_unit", "n_rules"])
    r = rules.assign(rev=rules["confidence"] * rules["consequent"].map(price_of).fillna(0.0))
    g = r.groupby("antecedent").agg(halo_units=("confidence", "sum"), halo_rev_per_unit=("rev", "sum"), n_rules=("consequent", "size"))
    return g.rename_axis("stock_code").reset_index()
