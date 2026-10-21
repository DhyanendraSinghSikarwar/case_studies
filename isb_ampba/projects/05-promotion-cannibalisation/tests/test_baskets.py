"""Unit tests for basket rules and halo (hand-made baskets, offline)."""
import numpy as np
import pandas as pd

from promo.baskets import basket_matrix, halo_table, mine_rules

CFG = {"baskets": {"top_skus": 10, "min_support": 0.05, "min_lift": 1.2, "min_confidence": 0.3}}


def _sales() -> pd.DataFrame:
    rows = []
    for i in range(60):          # A and B always together, C always alone, D with A in half of the baskets
        inv = f"I{i}"
        if i % 2 == 0:
            rows += [(inv, "A"), (inv, "B")]
            if i % 4 == 0:
                rows.append((inv, "D"))
        else:
            rows.append((inv, "C"))
    return pd.DataFrame(rows, columns=["invoice", "stock_code"])


def test_basket_matrix_shape_and_top_skus():
    m = basket_matrix(_sales(), top_skus=10)
    assert m.shape == (60, 4) and m.dtypes.eq(bool).all()
    assert basket_matrix(_sales(), top_skus=3).shape[1] == 3       # restricted to the top SKUs by invoice count
    assert m["D"].sum() == 15 and m["A"].sum() == 30


def test_rules_filtered_and_same_family_excluded():
    basket = basket_matrix(_sales(), 10)
    fam = {"A": "f1", "B": "f2", "C": "f3", "D": "f4"}
    r = mine_rules(basket, fam, CFG)
    assert len(r) > 0 and (r["lift"] >= 1.2).all() and (r["confidence"] >= 0.3).all()
    assert not ((r["antecedent"] == "C") | (r["consequent"] == "C")).any()      # C never co-occurs
    same = mine_rules(basket, {"A": "x", "B": "x", "C": "y", "D": "z"}, CFG)
    assert not ((same["antecedent"] == "A") & (same["consequent"] == "B")).any()  # same-family pair dropped


def test_halo_table_sums_confidence_and_revenue():
    rules = pd.DataFrame({"antecedent": ["A", "A"], "consequent": ["B", "D"], "support": [0.1, 0.1],
                          "confidence": [0.5, 0.2], "lift": [2.0, 2.0]})
    h = halo_table(rules, {"B": 4.0, "D": 10.0}).set_index("stock_code")
    assert np.isclose(h.at["A", "halo_units"], 0.7) and np.isclose(h.at["A", "halo_rev_per_unit"], 0.5 * 4 + 0.2 * 10)
    assert halo_table(rules.iloc[0:0], {}).empty
