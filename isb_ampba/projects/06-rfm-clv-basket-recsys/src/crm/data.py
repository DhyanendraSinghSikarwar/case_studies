"""Load, clean and split UCI Online Retail II (id=502); synthetic fixture for offline tests."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

from .config import get_logger, load_config, resolve, seed_everything

log = get_logger(__name__)

RAW_COLS = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price",
            "Customer ID", "Country"]
RENAME = {"Invoice": "invoice", "StockCode": "stock_code", "Description": "description",
          "Quantity": "quantity", "InvoiceDate": "invoice_date", "Price": "unit_price",
          "Customer ID": "customer_id", "Country": "country"}


def _normalise_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtypes of a raw frame so that it can be cached as parquet."""
    df = df.copy()
    df["Invoice"] = df["Invoice"].astype(str)
    df["StockCode"] = df["StockCode"].astype(str)
    df["Description"] = df["Description"].astype("string")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df[RAW_COLS]


def load_raw(cfg: dict | None = None) -> pd.DataFrame:
    """Return raw Online Retail II lines. Order: data/raw cache, external dir, ucimlrepo, zip."""
    cfg = cfg or load_config()
    name = cfg["data"]["parquet_name"]
    cache = resolve(cfg, "raw") / name
    if cache.exists():
        log.info("raw cache hit: %s", cache)
        return pd.read_parquet(cache)
    ext = Path(os.environ.get(cfg["data"]["external_dir_env"], cfg["data"]["external_dir_default"]))
    if (ext / name).exists():
        log.info("reading external parquet %s", ext / name)
        return pd.read_parquet(ext / name)
    df = None
    try:  # pragma: no cover - network path
        from ucimlrepo import fetch_ucirepo

        d = fetch_ucirepo(id=cfg["data"]["ucimlrepo_id"])
        df = pd.concat([d.data.features, d.data.targets], axis=1)
        if len(df.columns) == len(RAW_COLS):
            df.columns = RAW_COLS
    except Exception as exc:  # noqa: BLE001  # pragma: no cover
        log.warning("ucimlrepo failed (%s); falling back to zip download", exc)
    if df is None or "Invoice" not in df.columns:  # pragma: no cover
        import io
        import zipfile

        import requests

        r = requests.get(cfg["data"]["zip_url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=300)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        x = next(n for n in z.namelist() if n.endswith(".xlsx"))
        sheets = pd.read_excel(z.open(x), sheet_name=None)
        df = pd.concat(sheets.values(), ignore_index=True)
        df.columns = RAW_COLS
    df = _normalise_raw(df)
    cache.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache, index=False)
    return df


def clean(raw: pd.DataFrame, cfg: dict | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean raw lines. Returns (sales, returns); sales only keep rows with a Customer ID.

    Rules: drop missing Customer ID; cancellations (Invoice starting 'C') go to returns;
    drop Quantity<=0, Price<=0, non-product StockCodes; strip descriptions;
    revenue = quantity * unit_price. Exact duplicate lines are KEPT (documented in README).
    """
    cfg = cfg or load_config()
    df = raw.rename(columns=RENAME).copy()
    df["invoice"] = df["invoice"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str).str.strip().str.upper()
    df["description"] = df["description"].astype("string").str.strip()
    df = df[df["customer_id"].notna()].copy()
    df["customer_id"] = df["customer_id"].astype("int64")
    is_cancel = df["invoice"].str.startswith("C")
    returns = df[is_cancel].copy()
    df = df[~is_cancel]
    bad = set(cfg["data"]["non_product_codes"])
    mask = (df["quantity"] > 0) & (df["unit_price"] > 0) & ~df["stock_code"].isin(bad)
    mask &= ~df["stock_code"].str.startswith("GIFT")
    sales = df[mask].copy()
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    sales["invoice_date"] = pd.to_datetime(sales["invoice_date"])
    sales = sales.sort_values(["invoice_date", "invoice"]).reset_index(drop=True)
    log.info("clean sales: %d lines, %d customers", len(sales), sales["customer_id"].nunique())
    return sales, returns


def split_calibration_holdout(sales: pd.DataFrame, cfg: dict | None = None
                              ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Time split: calibration <= calibration_end (inclusive day); holdout after, to holdout_end."""
    cfg = cfg or load_config()
    cal_end = pd.Timestamp(cfg["data"]["calibration_end"]) + pd.Timedelta(days=1)
    hold_end = pd.Timestamp(cfg["data"]["holdout_end"]) + pd.Timedelta(days=1)
    cal = sales[sales["invoice_date"] < cal_end].copy()
    hold = sales[(sales["invoice_date"] >= cal_end) & (sales["invoice_date"] < hold_end)].copy()
    return cal, hold


def invoices(sales: pd.DataFrame) -> pd.DataFrame:
    """Invoice-level table: customer, date, revenue, n_lines, n_products."""
    return sales.groupby(["customer_id", "invoice"], as_index=False).agg(
        invoice_date=("invoice_date", "min"), revenue=("revenue", "sum"),
        n_lines=("stock_code", "size"), n_products=("stock_code", "nunique"))


def make_fixture(n_customers: int = 300, n_items: int = 60, seed: int = 42) -> pd.DataFrame:
    """Synthetic RAW Online Retail II-like frame (same columns/dtypes), spanning the real dates.

    Customers have heterogeneous purchase rates and lifetimes (BG/NBD-like), prefer one of
    several product groups (so baskets/bundles/CF have structure) and the frame includes junk
    rows (cancellations, no Customer ID, postage, zero price) that `clean` must remove.
    """
    rng = np.random.default_rng(seed)
    start, end = pd.Timestamp("2009-12-01"), pd.Timestamp("2011-12-09")
    span = (end - start).days
    n_groups = 6
    items = [f"{10000 + i}" for i in range(n_items)]
    group_of = rng.integers(0, n_groups, n_items)
    price = np.round(rng.lognormal(1.0, 0.6, n_items), 2) + 0.5
    rows = []
    inv_no = 500000
    for c in range(n_customers):
        cid = 12000 + c
        rate = rng.gamma(2.0, 0.012)
        first = int(rng.integers(0, span - 30))
        life = rng.exponential(250) + 30
        pref = rng.integers(0, n_groups)
        t = first
        while t < min(span, first + life):
            inv_no += 1
            n_l = int(rng.integers(3, 9))
            pool = np.where(group_of == pref)[0] if rng.random() < 0.8 else np.arange(n_items)
            chosen = rng.choice(pool, size=min(n_l, len(pool)), replace=False)
            d = start + pd.Timedelta(days=int(t), hours=int(rng.integers(8, 17)))
            for it in chosen:
                rows.append((str(inv_no), items[it], f"ITEM {items[it]}", int(rng.integers(1, 12)),
                             d, float(price[it]), float(cid), "United Kingdom"))
            t += max(1, int(rng.exponential(1 / rate)))
    df = pd.DataFrame(rows, columns=RAW_COLS)
    d0 = start + pd.Timedelta(days=10)
    junk = [
        ("C900001", items[0], "ITEM X", -1, d0, 2.0, 12000.0, "United Kingdom"),
        ("900002", "POST", "POSTAGE", 1, d0, 15.0, 12001.0, "United Kingdom"),
        ("900003", items[1], "ITEM Y", 1, d0, 2.0, np.nan, "United Kingdom"),
        ("900004", items[2], "ITEM Z", 1, d0, 0.0, 12002.0, "United Kingdom"),
        ("900005", items[3], "ITEM W", -3, d0, 2.0, 12003.0, "United Kingdom"),
    ]
    df = pd.concat([df, pd.DataFrame(junk, columns=RAW_COLS)], ignore_index=True)
    return _normalise_raw(df)


def load_sales(cfg: dict | None = None) -> pd.DataFrame:
    """Load cleaned sales from the processed cache, building it if absent."""
    cfg = cfg or load_config()
    p = resolve(cfg, "processed") / "sales.parquet"
    if p.exists():
        return pd.read_parquet(p)
    sales, _ = clean(load_raw(cfg), cfg)
    p.parent.mkdir(parents=True, exist_ok=True)
    sales.to_parquet(p, index=False)
    return sales


def main() -> None:
    """CLI: load raw, clean, cache cleaned sales to data/processed/sales.parquet."""
    cfg = load_config()
    seed_everything(cfg["seed"])
    raw = load_raw(cfg)
    sales, returns = clean(raw, cfg)
    out = resolve(cfg, "processed")
    out.mkdir(parents=True, exist_ok=True)
    sales.to_parquet(out / "sales.parquet", index=False)
    log.info("raw rows=%d sales=%d returns=%d -> %s", len(raw), len(sales), len(returns), out)


if __name__ == "__main__":
    main()
