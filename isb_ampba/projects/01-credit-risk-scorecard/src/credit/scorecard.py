"""PD -> score scaling, WOE logistic scorecard, points table and risk bands."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

BAND_LETTERS = list("ABCDEF")


def factor_offset(base_score: float = 600, base_odds: float = 50, pdo: float = 20) -> tuple[float, float]:
    """Standard scorecard scaling: factor = pdo/ln2, offset = base - factor*ln(base_odds)."""
    factor = pdo / np.log(2)
    return float(factor), float(base_score - factor * np.log(base_odds))


def pd_to_score(p, base: float = 600, odds: float = 50, pdo: float = 20, clip: tuple | None = (300, 900)):
    """Convert PD to a bureau-style score (higher = safer). clip=None returns the unclipped score."""
    p = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
    factor, offset = factor_offset(base, odds, pdo)
    s = offset + factor * np.log((1 - p) / p)
    return s if clip is None else np.clip(s, clip[0], clip[1])


def score_to_pd(score, base: float = 600, odds: float = 50, pdo: float = 20):
    """Inverse of the unclipped pd_to_score."""
    factor, offset = factor_offset(base, odds, pdo)
    return 1.0 / (1.0 + np.exp((np.asarray(score, dtype=float) - offset) / factor))


def assign_band(p, edges) -> np.ndarray:
    """A = lowest PD. 5 ascending edges -> 6 bands A..F."""
    return np.array(BAND_LETTERS)[np.searchsorted(np.asarray(edges), np.asarray(p), side="right")]


def band_table(p, y, score, edges) -> pd.DataFrame:
    """Customers, bad rate, mean PD and score range per band."""
    df = pd.DataFrame({"band": assign_band(p, edges), "pd": np.asarray(p), "y": np.asarray(y),
                       "score": np.asarray(score)})
    t = df.groupby("band").agg(n=("y", "size"), bad_rate=("y", "mean"), avg_pd=("pd", "mean"),
                               score_min=("score", "min"), score_max=("score", "max")).reset_index()
    t["share"] = t["n"] / t["n"].sum()
    return t


def fit_logit_scorecard(Xw: pd.DataFrame, y, iv: pd.Series, corr_max: float = 0.7, seed: int = 42):
    """1) drop one of each pair with |corr| > corr_max (keep higher IV);
    2) refit, dropping any variable with a POSITIVE coefficient (WOE = ln(good/bad) so sign must be negative)."""
    cols = list(Xw.columns)
    corr = Xw.corr().abs()
    for a in sorted(cols, key=lambda c: -iv[c]):
        for b in sorted(cols, key=lambda c: -iv[c]):
            if a != b and a in cols and b in cols and corr.loc[a, b] > corr_max:
                cols.remove(a if iv[a] < iv[b] else b)
    while True:
        lr = LogisticRegression(C=1.0, max_iter=1000, random_state=seed).fit(Xw[cols], y)
        bad = [(c, b) for c, b in zip(cols, lr.coef_[0], strict=True) if b > 0]
        if not bad:
            return lr, cols
        cols.remove(max(bad, key=lambda t: t[1])[0])


def build_points_table(bp, lr, cols, sc_cfg: dict) -> pd.DataFrame:
    """points(var, bin) = -factor * coef * WOE + (offset - factor * intercept) / n_vars."""
    factor, offset = factor_offset(sc_cfg["base_score"], sc_cfg["base_odds"], sc_cfg["pdo"])
    b0, n = float(lr.intercept_[0]), len(cols)
    rows = []
    for c, coef in zip(cols, lr.coef_[0], strict=True):
        t = bp.get_binned_variable(c).binning_table.build()
        t = t.loc[[i for i in t.index if str(i) != "Totals"]]
        for idx, r in t.iterrows():
            woe = 0.0 if pd.isna(r["WoE"]) else float(r["WoE"])
            rows.append({"variable": c, "bin_index": idx, "bin": str(r["Bin"]), "woe": woe,
                         "points": round(-factor * float(coef) * woe + (offset - factor * b0) / n, 2)})
    return pd.DataFrame(rows)


def score_with_table(bp, X: pd.DataFrame, table: pd.DataFrame, cols) -> np.ndarray:
    """Score rows by LOOKING UP points (what a business user does by hand). Unseen bins get the variable mean."""
    s = bp.summary()
    names = [str(n) for n in s.loc[s["selected"].astype(bool), "name"]]
    idx = pd.DataFrame(np.asarray(bp.transform(X, metric="indices")), index=X.index, columns=names)
    total = np.zeros(len(X))
    for c in cols:
        lut = table[table["variable"] == c].set_index("bin_index")["points"]
        lut.index = lut.index.astype(str)
        total += idx[c].astype(int).astype(str).map(lut).fillna(float(lut.mean())).to_numpy(dtype=float)
    return total
