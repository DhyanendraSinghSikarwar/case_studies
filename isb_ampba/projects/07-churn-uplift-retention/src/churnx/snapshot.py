"""Point-in-time snapshots: cleaning, features (strictly before ``asof``) and 90-day churn labels."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from churnx.config import get_logger

log = get_logger(__name__)

NON_PRODUCT = {"POST", "D", "DOT", "M", "BANK CHARGES", "S", "AMAZONFEE", "ADJUST", "ADJUST2", "CRUK",
               "C2", "PADS", "TEST001", "TEST002"}
FEATURES = ["recency_days", "frequency_6m", "monetary_6m", "aov_6m", "ipt_mean", "ipt_std", "spend_trend",
            "n_returns", "n_skus_6m", "items_per_order", "is_uk", "tenure_days", "recency_over_ipt"]
VALUE_COL = "monetary_6m"


def clean_sales(tx: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split raw transactions into ``sales`` (positive product lines) and ``returns`` (cancellations).

    Drops rows with no customer ID, non-product stock codes and gift codes; sales need quantity>0, price>0.
    """
    df = tx.dropna(subset=["customer_id"]).copy()
    df["customer_id"] = df["customer_id"].astype("int64")
    code = df["stock_code"].str.upper()
    product = ~code.isin(NON_PRODUCT) & ~code.str.startswith("GIFT")
    df = df[product]
    is_cancel = df["invoice"].str.upper().str.startswith("C")
    returns = df[is_cancel].copy()
    sales = df[~is_cancel & (df["quantity"] > 0) & (df["unit_price"] > 0)].copy()
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    return sales.reset_index(drop=True), returns.reset_index(drop=True)


def _orders(sales: pd.DataFrame) -> pd.DataFrame:
    """Invoice-level table: one row per (customer, invoice)."""
    g = sales.groupby(["customer_id", "invoice"], sort=False)
    o = g.agg(date=("invoice_date", "min"), revenue=("revenue", "sum"), items=("quantity", "sum")).reset_index()
    return o.sort_values(["customer_id", "date"]).reset_index(drop=True)


def build_features(sales: pd.DataFrame, returns: pd.DataFrame, asof: str | pd.Timestamp,
                   lookback_days: int = 180, min_orders: int = 2) -> pd.DataFrame:
    """Point-in-time features for eligible customers at ``asof`` using only rows with date < asof."""
    asof = pd.Timestamp(asof)
    s = sales[sales["invoice_date"] < asof]
    r = returns[returns["invoice_date"] < asof]
    orders = _orders(s)
    win = orders["date"] >= asof - pd.Timedelta(days=lookback_days)
    o6 = orders[win]
    g6 = o6.groupby("customer_id")
    freq = g6["invoice"].nunique().rename("frequency_6m")
    eligible = freq[freq >= min_orders].index
    feats = pd.DataFrame(index=pd.Index(eligible, name="customer_id"))
    feats["recency_days"] = (asof - orders.groupby("customer_id")["date"].max()).dt.total_seconds() / 86400
    feats["frequency_6m"] = freq
    feats["monetary_6m"] = g6["revenue"].sum()
    feats["aov_6m"] = feats["monetary_6m"] / feats["frequency_6m"]
    feats["items_per_order"] = g6["items"].sum() / feats["frequency_6m"]
    s6 = s[s["invoice_date"] >= asof - pd.Timedelta(days=lookback_days)]
    feats["n_skus_6m"] = s6.groupby("customer_id")["stock_code"].nunique()
    # inter-purchase time over all history, ignoring identical timestamps
    d = orders.groupby("customer_id")["date"].diff().dt.total_seconds() / 86400
    gaps = pd.DataFrame({"customer_id": orders["customer_id"], "gap": d}).query("gap > 0")
    gg = gaps.groupby("customer_id")["gap"]
    feats["ipt_mean"] = gg.mean()
    feats["ipt_std"] = gg.std()
    half = asof - pd.Timedelta(days=lookback_days // 2)
    recent = orders[orders["date"] >= half].groupby("customer_id")["revenue"].sum().reindex(feats.index).fillna(0)
    prev = orders[(orders["date"] < half) & win].groupby("customer_id")["revenue"].sum().reindex(feats.index).fillna(0)
    feats["spend_trend"] = (recent - prev) / (recent + prev + 1)
    rw = r[r["invoice_date"] >= asof - pd.Timedelta(days=lookback_days)]
    feats["n_returns"] = rw.groupby("customer_id")["invoice"].nunique()
    feats["n_returns"] = feats["n_returns"].fillna(0)
    last_country = s.sort_values("invoice_date").groupby("customer_id")["country"].last()
    feats["is_uk"] = (last_country.reindex(feats.index) == "United Kingdom").astype(float)
    feats["tenure_days"] = (asof - orders.groupby("customer_id")["date"].min()).dt.total_seconds() / 86400
    feats["ipt_mean"] = feats["ipt_mean"].fillna(feats["ipt_mean"].median())
    feats["ipt_std"] = feats["ipt_std"].fillna(0.0)
    feats["recency_over_ipt"] = feats["recency_days"] / (feats["ipt_mean"] + 1.0)
    feats = feats.loc[:, FEATURES].astype(float)
    assert not feats.isna().any().any(), "NaNs remain in features"
    return feats.reset_index()


def make_label(sales: pd.DataFrame, customers: pd.Series | np.ndarray, asof: str | pd.Timestamp,
               horizon_days: int = 90) -> pd.Series:
    """Churn = 1 if the customer has no sales invoice in [asof, asof + horizon). Asserts window is observed."""
    asof = pd.Timestamp(asof)
    end = asof + pd.Timedelta(days=horizon_days)
    assert end <= sales["invoice_date"].max() + pd.Timedelta(days=1), "label window runs past end of data"
    customers = pd.Series(np.asarray(customers))
    w = sales[(sales["invoice_date"] >= asof) & (sales["invoice_date"] < end)]
    bought = set(w["customer_id"].unique())
    return pd.Series((~customers.isin(bought)).astype(int).to_numpy(), index=customers.to_numpy(), name="churn")


def build_snapshot(sales: pd.DataFrame, returns: pd.DataFrame, asof: str | pd.Timestamp,
                   snap_cfg: dict[str, Any]) -> pd.DataFrame:
    """Features + label for one snapshot date."""
    f = build_features(sales, returns, asof, snap_cfg["lookback_days"], snap_cfg["min_orders"])
    y = make_label(sales, f["customer_id"], asof, snap_cfg["horizon_days"])
    f["churn"] = y.to_numpy()
    f["asof"] = pd.Timestamp(asof)
    return f


def build_all_snapshots(sales: pd.DataFrame, returns: pd.DataFrame, cfg: dict[str, Any]) -> pd.DataFrame:
    """Build pilot-history, train and test snapshots, tagged with a ``split`` column."""
    sc = cfg["snapshots"]
    plan = ([(d, "pilot_hist") for d in cfg["pilot"]["extra_snapshots"]] + [(d, "train") for d in sc["train"]]
            + [(sc["test"], "test")])
    parts = []
    for d, split in plan:
        snap = build_snapshot(sales, returns, d, sc)
        snap["split"] = split
        log.info("snapshot %s [%s]: %d eligible, churn rate %.3f", d, split, len(snap), snap["churn"].mean())
        parts.append(snap)
    return pd.concat(parts, ignore_index=True)


def customer_value_inr(monetary_6m: np.ndarray | pd.Series, biz: dict[str, Any]) -> np.ndarray:
    """Value (INR) of saving a customer: monthly pre-snapshot spend x clv_months x margin x FX."""
    return np.asarray(monetary_6m, float) / 6.0 * biz["clv_months"] * biz["gross_margin"] * biz["gbp_to_inr"]
