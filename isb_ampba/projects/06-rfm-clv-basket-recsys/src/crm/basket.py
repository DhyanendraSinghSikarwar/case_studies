"""Market-basket analysis: FP-Growth (mlxtend), rule filtering and top bundles."""
from __future__ import annotations

import time

import pandas as pd
import scipy.sparse as sp
from mlxtend.frequent_patterns import association_rules, fpgrowth

from .config import get_logger, load_config

log = get_logger(__name__)


def product_names(sales: pd.DataFrame) -> pd.Series:
    """stock_code -> most frequent (cleaned) description."""
    d = sales.dropna(subset=["description"])
    d = d[d["description"].str.len() > 0]
    mode = d.groupby("stock_code")["description"].agg(lambda s: s.value_counts().index[0])
    return mode.astype(str)


def build_basket_matrix(sales: pd.DataFrame, top_items: int) -> pd.DataFrame:
    """Boolean invoice x item sparse DataFrame restricted to the `top_items` most frequent items."""
    keep = sales.groupby("stock_code")["invoice"].nunique().nlargest(top_items).index
    s = sales[sales["stock_code"].isin(keep)][["invoice", "stock_code"]].drop_duplicates()
    inv_codes, inv_idx = pd.factorize(s["invoice"])
    it_codes, it_idx = pd.factorize(s["stock_code"])
    m = sp.csr_matrix(([True] * len(s), (inv_codes, it_codes)),
                      shape=(len(inv_idx), len(it_idx)), dtype=bool)
    return pd.DataFrame.sparse.from_spmatrix(m, index=inv_idx, columns=it_idx)


def mine_rules(basket: pd.DataFrame, cfg: dict | None = None) -> dict:
    """Tune min_support over a descending grid; stop at the first support giving enough rules.

    Rules are filtered to lift > min_lift and confidence > min_confidence. If the grid is
    exhausted the lowest-support result is used. Itemset explosion is guarded by max_itemsets.
    """
    cfg = cfg or load_config()
    b = cfg["basket"]
    tried = []
    best = None
    for sup in b["support_grid"]:
        t = time.time()
        fi = fpgrowth(basket, min_support=sup, use_colnames=True, max_len=b["max_len"])
        n_sets = len(fi)
        if n_sets > b["max_itemsets"]:
            tried.append({"min_support": sup, "itemsets": n_sets, "rules": None, "note": "too many"})
            break
        if n_sets == 0 or not (fi["itemsets"].map(len) >= 2).any():
            tried.append({"min_support": sup, "itemsets": n_sets, "rules": 0})
            continue
        rules = association_rules(fi, metric="lift", min_threshold=b["min_lift"])
        rules = rules[rules["confidence"] > b["min_confidence"]]
        rules = rules[rules["lift"] > b["min_lift"]].reset_index(drop=True)
        tried.append({"min_support": sup, "itemsets": n_sets, "rules": len(rules),
                      "seconds": round(time.time() - t, 1)})
        best = {"min_support": sup, "itemsets": fi, "rules": rules}
        if len(rules) >= b["target_rules"]:
            break
    if best is None:
        best = {"min_support": b["support_grid"][-1], "itemsets": pd.DataFrame(),
                "rules": pd.DataFrame()}
    best["tuning"] = tried
    log.info("basket tuning: %s", tried)
    return best


def top_bundles(rules: pd.DataFrame, names: pd.Series, n: int = 20) -> pd.DataFrame:
    """Top-n distinct bundles (unique item sets) ranked by lift, then confidence."""
    if rules.empty:
        return pd.DataFrame(columns=["bundle", "items", "support", "confidence", "lift"])
    r = rules.copy()
    r["items_set"] = [frozenset(a) | frozenset(c) for a, c in zip(r["antecedents"], r["consequents"],
                                                                  strict=True)]
    r = r.sort_values(["lift", "confidence"], ascending=False).drop_duplicates("items_set")
    r = r.head(n).reset_index(drop=True)

    def label(codes: frozenset) -> str:
        return " + ".join(str(names.get(c, c)) for c in sorted(codes))

    out = pd.DataFrame({
        "rank": range(1, len(r) + 1),
        "bundle": [label(s) for s in r["items_set"]],
        "items": [",".join(sorted(s)) for s in r["items_set"]],
        "antecedent": [",".join(sorted(a)) for a in r["antecedents"]],
        "consequent": [",".join(sorted(c)) for c in r["consequents"]],
        "support": r["support"].round(5), "confidence": r["confidence"].round(4),
        "lift": r["lift"].round(3),
    })
    return out


def run_basket(sales: pd.DataFrame, cfg: dict | None = None) -> dict:
    """Mine rules on invoice baskets and return bundles + summary metrics."""
    cfg = cfg or load_config()
    names = product_names(sales)
    basket = build_basket_matrix(sales, cfg["basket"]["top_items"])
    res = mine_rules(basket, cfg)
    bundles = top_bundles(res["rules"], names, cfg["basket"]["top_bundles"])
    metrics = {
        "n_baskets": int(basket.shape[0]), "n_items_considered": int(basket.shape[1]),
        "min_support_chosen": res["min_support"], "n_itemsets": len(res["itemsets"]),
        "n_rules_filtered": len(res["rules"]), "n_bundles": len(bundles),
        "top_lift": float(bundles["lift"].max()) if len(bundles) else None,
        "median_lift_top20": float(bundles["lift"].median()) if len(bundles) else None,
        "tuning": res["tuning"],
    }
    return {"rules": res["rules"], "bundles": bundles, "metrics": metrics, "names": names}
