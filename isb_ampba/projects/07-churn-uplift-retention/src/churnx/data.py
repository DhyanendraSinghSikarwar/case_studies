"""Data loading (Online Retail II, Hillstrom) with caching, plus offline fixtures.

Resolution order for Online Retail II (first hit wins):
1. ``data/interim/transactions.parquet`` (standardised cache written by this module)
2. ``data/raw/online_retail_ii.parquet``
3. ``$AMPBA_DATA_DIR/online_retail_ii.parquet`` (default ``C:/ampba_data``)
4. ``ucimlrepo.fetch_ucirepo(id=502)``
5. UCI zip download (slow; the Excel read is cached to ``data/raw`` as parquet)
"""
from __future__ import annotations

import io
import os
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from churnx.config import ROOT, get_logger, load_config, resolve

log = get_logger(__name__)

TX_COLS = {"Invoice": "invoice", "StockCode": "stock_code", "Description": "description",
           "Quantity": "quantity", "InvoiceDate": "invoice_date", "Price": "unit_price",
           "Customer ID": "customer_id", "Country": "country"}
HILLSTROM_COLS = ["recency", "history_segment", "history", "mens", "womens", "zip_code", "newbie",
                  "channel", "segment", "visit", "conversion", "spend"]


def standardise(df: pd.DataFrame) -> pd.DataFrame:
    """Rename to snake_case and fix dtypes (Invoice/StockCode strings, Customer ID nullable Int64)."""
    df = df.rename(columns=TX_COLS).copy()
    df["invoice"] = df["invoice"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)
    df["description"] = df["description"].astype("string").str.strip()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["customer_id"] = df["customer_id"].astype("Int64")
    df["country"] = df["country"].astype(str)
    return df[list(TX_COLS.values())]


def _from_ucimlrepo() -> pd.DataFrame:
    from ucimlrepo import fetch_ucirepo

    d = fetch_ucirepo(id=502)
    return pd.concat([d.data.features, d.data.targets], axis=1)


def _from_zip(url: str, cache: Path) -> pd.DataFrame:
    import requests

    log.info("Downloading %s (slow, ~45MB)", url)
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=300)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        sheets = pd.read_excel(io.BytesIO(z.read(name)), sheet_name=None)
    df = pd.concat(sheets.values(), ignore_index=True)
    df["Invoice"] = df["Invoice"].astype(str)
    df["StockCode"] = df["StockCode"].astype(str)
    df["Description"] = df["Description"].astype("string")
    cache.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache, index=False)
    return df


def load_transactions(cfg: dict[str, Any] | None = None, root: Path | None = None,
                      force: bool = False) -> pd.DataFrame:
    """Load standardised Online Retail II transactions using the documented resolution order."""
    cfg = cfg or load_config()
    root = root or ROOT
    interim = root / cfg["paths"]["interim"] / "transactions.parquet"
    if interim.exists() and not force:
        tx = pd.read_parquet(interim)
        log.info("Loaded cache %s (%d rows)", interim, len(tx))
        return tx
    raw_cache = root / cfg["paths"]["raw"] / cfg["data"]["parquet_name"]
    ext_dir = os.environ.get(cfg["data"]["env_var"], cfg["data"]["default_dir"])
    ext = Path(ext_dir) / cfg["data"]["parquet_name"]
    if raw_cache.exists():
        raw = pd.read_parquet(raw_cache)
    elif ext.exists():
        log.info("Reading external parquet %s", ext)
        raw = pd.read_parquet(ext)
    else:
        try:
            raw = _from_ucimlrepo()
            raw_cache.parent.mkdir(parents=True, exist_ok=True)
            raw.to_parquet(raw_cache, index=False)
        except Exception as exc:  # network / API failure -> fall back to the zip
            log.warning("ucimlrepo failed (%s); trying zip download", exc)
            raw = _from_zip(cfg["data"]["uci_zip_url"], raw_cache)
    tx = standardise(raw)
    interim.parent.mkdir(parents=True, exist_ok=True)
    tx.to_parquet(interim, index=False)
    log.info("Transactions: %d rows, %d customers, %s -> %s", len(tx), tx["customer_id"].nunique(),
             tx["invoice_date"].min(), tx["invoice_date"].max())
    return tx


def load_hillstrom(cfg: dict[str, Any] | None = None, root: Path | None = None) -> pd.DataFrame | None:
    """Load the Hillstrom e-mail RCT (cached to data/raw/hillstrom.csv). Returns None if unavailable."""
    cfg = cfg or load_config()
    root = root or ROOT
    path = root / cfg["paths"]["raw"] / "hillstrom.csv"
    try:
        if not path.exists():
            import requests

            r = requests.get(cfg["data"]["hillstrom_url"], headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
            r.raise_for_status()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(r.content)
        df = pd.read_csv(path)
        missing = set(HILLSTROM_COLS) - set(df.columns)
        assert not missing, f"Hillstrom columns missing: {missing}"
        return df
    except Exception as exc:
        log.warning("Hillstrom unavailable (%s) - Track B will be skipped", exc)
        return None


def make_fixture(n_customers: int = 700, seed: int = 42, start: str = "2009-12-01",
                 end: str = "2011-12-09") -> pd.DataFrame:
    """Synthetic Online-Retail-II-like transactions for offline tests.

    Customers have a purchase rate and a finite active lifetime (so recency is predictive of churn),
    plus cancellations, non-product codes and anonymous rows to exercise the cleaning rules.
    """
    rng = np.random.default_rng(seed)
    t0, t1 = pd.Timestamp(start), pd.Timestamp(end)
    span = (t1 - t0).days
    skus = [f"{rng.integers(10000, 99999)}{rng.choice(['', 'A', 'B'])}" for _ in range(200)]
    rows: list[tuple] = []
    inv = 500000
    for cid in range(12000, 12000 + n_customers):
        first = rng.integers(0, int(span * 0.6))
        rate = float(np.exp(rng.normal(-3.0, 0.5)))              # orders per day
        life = rng.exponential(220) + 40                          # active days after first order
        country = "United Kingdom" if rng.random() < 0.9 else str(rng.choice(["France", "Germany", "EIRE"]))
        t = float(first)
        while t < min(first + life, span):
            t += rng.exponential(1.0 / rate)
            if t >= min(first + life, span):
                break
            inv += 1
            date = t0 + pd.Timedelta(days=t, hours=int(rng.integers(8, 17)), minutes=int(rng.integers(0, 59)))
            for _ in range(int(rng.integers(1, 6))):
                price = float(np.round(np.exp(rng.normal(1.0, 0.7)), 2))
                qty = int(rng.integers(1, 13))
                rows.append((str(inv), str(rng.choice(skus)), "ITEM", qty, date, price, float(cid), country))
            if rng.random() < 0.05:                               # cancellation of this order
                inv += 1
                rows.append((f"C{inv}", str(rng.choice(skus)), "ITEM", -2, date + pd.Timedelta(days=1), 3.0,
                             float(cid), country))
            if rng.random() < 0.05:                               # non-product line
                rows.append((str(inv), "POST", "POSTAGE", 1, date, 18.0, float(cid), country))
    for _ in range(40):                                          # anonymous lines (no customer)
        inv += 1
        d = t0 + pd.Timedelta(days=float(rng.integers(0, span)))
        rows.append((str(inv), str(rng.choice(skus)), "ITEM", 1, d, 2.0, np.nan, "United Kingdom"))
    cols = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
    df = pd.DataFrame(rows, columns=cols)
    return standardise(df.sort_values("InvoiceDate").reset_index(drop=True))


def make_hillstrom_fixture(n: int = 6000, seed: int = 42) -> pd.DataFrame:
    """Synthetic Hillstrom-schema RCT with a small heterogeneous e-mail effect (offline tests)."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "recency": rng.integers(1, 13, n),
        "history": np.round(np.exp(rng.normal(5, 0.8, n)), 2),
        "mens": rng.integers(0, 2, n), "womens": rng.integers(0, 2, n),
        "zip_code": rng.choice(["Urban", "Surburban", "Rural"], n),
        "newbie": rng.integers(0, 2, n),
        "channel": rng.choice(["Web", "Phone", "Multichannel"], n),
        "segment": rng.choice(["No E-Mail", "Mens E-Mail", "Womens E-Mail"], n),
    })
    df["history_segment"] = pd.qcut(df["history"], 4, labels=False).astype(str)
    base = 0.08 + 0.01 * (12 - df["recency"]) / 12
    lift = np.where(df["segment"] != "No E-Mail", 0.05 * (df["mens"] + 0.5), 0.0)
    df["visit"] = (rng.random(n) < base + lift).astype(int)
    df["conversion"] = ((rng.random(n) < 0.3) & (df["visit"] == 1)).astype(int)
    df["spend"] = df["conversion"] * np.round(np.exp(rng.normal(4, 0.5, n)), 2)
    return df[HILLSTROM_COLS]


def main() -> None:
    """CLI: python -m churnx.data -> cache transactions parquet and (best-effort) Hillstrom."""
    from churnx.snapshot import clean_sales

    cfg = load_config()
    tx = load_transactions(cfg)
    sales, returns = clean_sales(tx)
    log.info("After cleaning: %d sales lines, %d customers, %d return lines", len(sales),
             sales["customer_id"].nunique(), len(returns))
    resolve(cfg, "raw")
    load_hillstrom(cfg)


if __name__ == "__main__":
    main()
