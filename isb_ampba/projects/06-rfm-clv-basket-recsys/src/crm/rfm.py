"""RFM features, quintile codes and rule-based named segments."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import get_logger, load_config
from .data import invoices

log = get_logger(__name__)

SEGMENTS = ["Champions", "Loyal", "At-Risk", "Hibernating", "New", "Big-spenders"]


def compute_rfm(sales: pd.DataFrame, asof: pd.Timestamp) -> pd.DataFrame:
    """Customer table from sales strictly before `asof` (snapshot date, exclusive).

    Columns: customer_id, recency (days since last order), frequency (distinct invoices),
    monetary (total revenue), tenure (days since first order), avg_basket (revenue per invoice),
    n_products (distinct StockCodes: the data has no category taxonomy, see README Deviations).
    Rows at/after `asof` are ignored so holdout data can never leak in.
    """
    s = sales[sales["invoice_date"] < asof]
    inv = invoices(s)
    g = inv.groupby("customer_id").agg(
        first_purchase=("invoice_date", "min"), last_purchase=("invoice_date", "max"),
        frequency=("invoice", "nunique"), monetary=("revenue", "sum"))
    g["n_products"] = s.groupby("customer_id")["stock_code"].nunique()
    g["recency"] = (asof - g["last_purchase"]).dt.total_seconds() / 86400.0
    g["tenure"] = (asof - g["first_purchase"]).dt.total_seconds() / 86400.0
    g["avg_basket"] = g["monetary"] / g["frequency"]
    return g.reset_index()


def _quintile(x: pd.Series, ascending: bool = True, tiebreak: pd.Series | None = None) -> pd.Series:
    """Score 1..5 by rank-based quintiles; ties broken by `tiebreak` (then index) so bins stay equal."""
    tb = tiebreak if tiebreak is not None else pd.Series(0.0, index=x.index)
    order = pd.DataFrame({"x": x if ascending else -x, "tb": tb}).sort_values(["x", "tb"])
    r = pd.Series(np.arange(len(order)), index=order.index).reindex(x.index)
    return pd.qcut(r, 5, labels=False).astype(int) + 1


def add_rfm_scores(rfm: pd.DataFrame) -> pd.DataFrame:
    """Add R/F/M quintile scores (5 = best) and the 3-digit `rfm_code` string."""
    out = rfm.copy()
    out["r_score"] = _quintile(out["recency"], ascending=False, tiebreak=out["monetary"])   # small recency = good = 5
    out["f_score"] = _quintile(out["frequency"], tiebreak=out["monetary"])
    out["m_score"] = _quintile(out["monetary"])
    out["rfm_code"] = (out["r_score"].astype(str) + out["f_score"].astype(str)
                       + out["m_score"].astype(str))
    out["rfm_total"] = out[["r_score", "f_score", "m_score"]].sum(axis=1)
    return out


def assign_segments(df: pd.DataFrame, cfg: dict | None = None) -> pd.DataFrame:
    """Rule-based named segments, evaluated in priority order (first match wins):

    New (young, <=2 orders) > Champions (R,F,M>=4) > Big-spenders (M=5, not champion)
    > At-Risk (R<=2, F>=3) > Loyal (F>=3, R>=3) > Loyal if R>=3 else Hibernating.
    """
    cfg = cfg or load_config()
    c = cfg["rfm"]
    r, f, m = df["r_score"], df["f_score"], df["m_score"]
    conds = [
        (df["tenure"] <= c["new_max_tenure_days"]) & (df["frequency"] <= 2),
        (r >= c["champions_min_score"]) & (f >= c["champions_min_score"])
        & (m >= c["champions_min_score"]),
        m == 5,
        (r <= c["at_risk_max_r"]) & (f >= c["at_risk_min_f"]),
        (f >= c["loyal_min_f"]) & (r >= c["loyal_min_r"]),
        r >= c["loyal_min_r"],
    ]
    names = ["New", "Champions", "Big-spenders", "At-Risk", "Loyal", "Loyal"]
    out = df.copy()
    out["segment"] = np.select(conds, names, default="Hibernating")
    return out


def build_rfm(sales: pd.DataFrame, asof: pd.Timestamp, cfg: dict | None = None) -> pd.DataFrame:
    """Full pipeline: features -> quintile codes -> named segments."""
    return assign_segments(add_rfm_scores(compute_rfm(sales, asof)), cfg)


def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Segment sizes, revenue share and mean RFM per segment."""
    g = df.groupby("segment").agg(
        customers=("customer_id", "size"), revenue=("monetary", "sum"),
        recency=("recency", "mean"), frequency=("frequency", "mean"),
        monetary=("monetary", "mean"), avg_basket=("avg_basket", "mean"))
    g["customer_share"] = g["customers"] / g["customers"].sum()
    g["revenue_share"] = g["revenue"] / g["revenue"].sum()
    return g.reindex([s for s in SEGMENTS if s in g.index]).reset_index()
