"""Demand: price-response (log-log) estimates where price varies, baseline table, and the MNL / nested-logit choice models."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import get_logger

log = get_logger("promo.demand")


# --------------------------------------------------------------------------- baseline
def baseline_table(panel: pd.DataFrame, cfg: dict, as_of: pd.Timestamp | None = None) -> pd.DataFrame:
    """Per-SKU baseline weekly units / list price from the last ``baseline_weeks`` active weeks up to ``as_of``.

    Only weeks <= as_of are used (no look-ahead). ``active`` = sold within ``catalog.active_within_weeks`` of as_of.
    """
    p = panel if as_of is None else panel[panel["week"] <= as_of]
    end = p["week"].max() if as_of is None else pd.Timestamp(as_of)
    tail = p.sort_values(["stock_code", "week"]).groupby("stock_code").tail(cfg["demand"]["baseline_weeks"])
    g = tail.groupby("stock_code").agg(
        base_units=("units", "mean"), list_price=("price", "median"), last_week=("week", "max"), n_active_weeks=("week", "size")
    ).reset_index()
    g["weekly_revenue"] = g["base_units"] * g["list_price"]
    g["active"] = g["last_week"] >= end - pd.Timedelta(weeks=cfg["catalog"]["active_within_weeks"])
    return g


def seasonal_index(panel: pd.DataFrame, horizon_weeks: int, as_of: pd.Timestamp | None = None) -> np.ndarray:
    """Seasonal index for the next ``horizon_weeks`` weeks = revenue in the same week one year earlier / mean weekly revenue.

    Uses only weeks <= as_of (the target week minus 52 weeks is always <= as_of for horizon <= 52).
    """
    p = panel if as_of is None else panel[panel["week"] <= as_of]
    tot = p.groupby("week")["revenue"].sum()
    end = tot.index.max()
    full = tot.reindex(pd.date_range(tot.index.min(), end, freq="7D")).fillna(0.0)
    mean_w = full.iloc[-52:].fillna(0).mean()
    out = []
    for k in range(1, horizon_weeks + 1):
        w = end + pd.Timedelta(weeks=k - 52)
        v = full.get(w, np.nan)
        out.append(float(v / mean_w) if np.isfinite(v) and mean_w > 0 else 1.0)
    return np.array(out)


# --------------------------------------------------------------------------- price response
def ols_hc1(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """OLS coefficients and HC1 robust standard errors."""
    n, k = X.shape
    xtx_inv = np.linalg.pinv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    e = y - X @ beta
    meat = (X * e[:, None] ** 2).T @ X
    cov = xtx_inv @ meat @ xtx_inv * (n / max(n - k, 1))
    return beta, np.sqrt(np.clip(np.diag(cov), 0, None))


def sku_elasticity_ols(units: np.ndarray, price: np.ndarray, month: np.ndarray) -> tuple[float, float, int]:
    """ln(units) = a + eps*ln(price) + month dummies, OLS with HC1 errors. Returns (eps, se, n)."""
    y = np.log(np.asarray(units, float))
    lp = np.log(np.asarray(price, float))
    cols = [np.ones_like(lp), lp]
    for m in np.unique(month)[1:]:
        cols.append((month == m).astype(float))
    X = np.column_stack(cols)
    if len(y) <= X.shape[1] or np.std(lp) < 1e-9:
        return np.nan, np.nan, len(y)
    beta, se = ols_hc1(X, y)
    return float(beta[1]), float(se[1]), len(y)


def pooled_fe_elasticity(panel: pd.DataFrame, n_iter: int = 30) -> dict:
    """Pooled log-log elasticity with SKU and week fixed effects (two-way demeaning), SKU-clustered SE."""
    d = panel[["stock_code", "week", "units", "price"]].copy()
    d["y"] = np.log(d["units"]); d["x"] = np.log(d["price"])
    for _ in range(n_iter):
        for col in ("y", "x"):
            d[col] = d[col] - d.groupby("stock_code")[col].transform("mean")
            d[col] = d[col] - d.groupby("week")[col].transform("mean")
    sxx = float((d["x"] ** 2).sum())
    if sxx <= 0:
        return {"eps": float("nan"), "se": float("nan"), "n_obs": len(d)}
    b = float((d["x"] * d["y"]).sum() / sxx)
    e = d["y"] - b * d["x"]
    score = (d["x"] * e).groupby(d["stock_code"]).sum()
    se = float(np.sqrt((score**2).sum()) / sxx)
    return {"eps": b, "se": se, "n_obs": int(len(d)), "n_skus": int(d["stock_code"].nunique())}


def estimate_elasticities(panel: pd.DataFrame, fam_of: dict[str, str], cfg: dict) -> pd.DataFrame:
    """Per-SKU price-response estimates with an identifiability filter, shrinkage and prior fallback.

    - eligible: >= min_weeks weeks and >= min_price_drops consecutive-week price drops > drop_threshold
    - valid: eligible, finite and negative (positive estimates are dropped and counted)
    - shrunk toward the leave-one-out family median (else the prior) with weight tau2 / (tau2 + se^2)
    - ineligible / invalid SKUs get the family median of valid estimates, else the prior
    Returns one row per SKU: eps_hat, se, eps (final), eps_source. These are association estimates, not causal.
    """
    dm = cfg["demand"]
    lo, hi = dm["eps_bounds"]
    p = panel.sort_values(["stock_code", "week"]).copy()
    prev_p = p.groupby("stock_code")["price"].shift()
    prev_w = p.groupby("stock_code")["week"].shift()
    consec = (p["week"] - prev_w) == pd.Timedelta(days=7)
    p["drop"] = consec & (p["price"] / prev_p < 1 - dm["drop_threshold"])
    stats = p.groupby("stock_code").agg(n_weeks=("week", "size"), n_drops=("drop", "sum")).reset_index()
    stats["eligible"] = (stats["n_weeks"] >= dm["min_weeks"]) & (stats["n_drops"] >= dm["min_price_drops"])
    elig = set(stats.loc[stats["eligible"], "stock_code"])
    rows = []
    for sku, g in p[p["stock_code"].isin(elig)].groupby("stock_code"):
        eps, se, n = sku_elasticity_ols(g["units"].to_numpy(), g["price"].to_numpy(), g["month"].to_numpy())
        rows.append((sku, eps, se))
    est = pd.DataFrame(rows, columns=["stock_code", "eps_hat", "se"])
    out = stats.merge(est, on="stock_code", how="left")
    out["family"] = out["stock_code"].map(fam_of)
    out["positive"] = out["eligible"] & (out["eps_hat"] >= 0)
    out["valid"] = out["eligible"] & np.isfinite(out["eps_hat"]) & (out["eps_hat"] < 0) & np.isfinite(out["se"])
    v = out[out["valid"]]
    global_med = float(v["eps_hat"].median()) if len(v) else dm["prior_elasticity"]
    tau2 = max(float(v["eps_hat"].var(ddof=1) - (v["se"] ** 2).mean()) if len(v) > 2 else dm["tau2_floor"], dm["tau2_floor"])
    fam_vals = v.groupby("family")["eps_hat"].apply(list).to_dict()
    eps_final, src = [], []
    for r in out.itertuples():
        peers = fam_vals.get(r.family, [])
        if r.valid:
            others = list(peers)
            others.remove(r.eps_hat)
            if others:
                target = float(np.median(others))
            else:
                target = dm["prior_elasticity"]
            w = tau2 / (tau2 + r.se**2)
            eps_final.append(w * r.eps_hat + (1 - w) * target)
            src.append("estimated_shrunk")
        elif peers:
            eps_final.append(float(np.median(peers))); src.append("family_median")
        else:
            eps_final.append(dm["prior_elasticity"]); src.append("prior")
    out["eps"] = np.clip(eps_final, lo, hi)
    out["eps_source"] = src
    out.attrs.update({"tau2": tau2, "global_median": global_med})
    log.info("elasticities: %d eligible, %d valid, %d positive dropped", int(out["eligible"].sum()), int(out["valid"].sum()), int(out["positive"].sum()))
    return out


# --------------------------------------------------------------------------- MNL choice model
def mnl_shares_after_discount(u: np.ndarray, p: np.ndarray, i: int, d: float, eps_i: float, outside_share: float) -> tuple[np.ndarray, float, float]:
    """MNL with outside option calibrated so SKU i's own-price elasticity equals eps_i.

    Returns (shares s' of the family SKUs, outside share s0', market size M). Shares + outside sum to one.
    """
    u = np.asarray(u, float); p = np.asarray(p, float)
    s0 = outside_share
    M = u.sum() / (1 - s0)
    s = u / M
    beta = -eps_i / (p[i] * (1 - s[i]))
    a = np.log(s / s0) + beta * p
    p2 = p.copy(); p2[i] = p[i] * (1 - d)
    e = np.exp(a - beta * p2)
    denom = 1.0 + e.sum()
    return e / denom, 1.0 / denom, float(M)


def nested_shares_after_discount(u: np.ndarray, p: np.ndarray, i: int, d: float, eps_i: float, outside_share: float,
                                 lam: float) -> tuple[np.ndarray, float, float]:
    """Two-level nested logit: the family is one nest (dissimilarity ``lam`` in (0, 1]), "no purchase" is a singleton nest.

    lam = 1 is exactly the MNL; lam < 1 means siblings are closer substitutes than the outside option (more of the
    promoted SKU's gain is diverted from siblings, less from the outside). Calibrated to the baseline shares and to SKU
    i's own-price elasticity eps_i = -beta p_i [1/lam - (1/lam - 1) s_i|g - s_i]. Returns (shares, s0', market size M).
    """
    if not 0 < lam <= 1:
        raise ValueError("nest lambda must be in (0, 1]")
    u = np.asarray(u, float); p = np.asarray(p, float)
    s0 = outside_share
    M = u.sum() / (1 - s0)
    s = u / M
    S = s.sum()
    s_cond = s / S
    beta = -eps_i / (p[i] * (1 / lam - (1 / lam - 1) * s_cond[i] - s[i]))
    v = lam * np.log(s / s0) - (lam - 1) * np.log(S / s0)          # systematic utilities at baseline prices
    p2 = p.copy(); p2[i] = p[i] * (1 - d)
    ev = np.exp((v + beta * p - beta * p2) / lam)                   # exp(V'_j / lam), V'_j = a_j - beta p'_j
    inc = ev.sum()
    inside_prob = inc**lam / (1.0 + inc**lam)
    return ev / inc * inside_prob, 1.0 - inside_prob, float(M)


def mnl_after_discount(u: np.ndarray, p: np.ndarray, i: int, d: float, eps_i: float, outside_share: float,
                       sub_weight: float = 1.0, nest_lambda: float = 1.0) -> np.ndarray:
    """New weekly units of every family SKU after discount d on SKU i.

    sub_weight in [0, 1] scales how much of the sibling losses is realised (1 = pure MNL/IIA; <1 caps
    cannibalisation for weak-substitute families). The promoted SKU's units are unaffected by the cap.
    nest_lambda < 1 switches to the nested-logit variant (1 = MNL).
    """
    if nest_lambda == 1.0:
        s2, _, M = mnl_shares_after_discount(u, p, i, d, eps_i, outside_share)
    else:
        s2, _, M = nested_shares_after_discount(u, p, i, d, eps_i, outside_share, nest_lambda)
    u2 = M * s2
    if sub_weight != 1.0:
        sib = np.arange(len(u)) != i
        u2[sib] = u[sib] + sub_weight * (u2[sib] - u[sib])
    return u2
