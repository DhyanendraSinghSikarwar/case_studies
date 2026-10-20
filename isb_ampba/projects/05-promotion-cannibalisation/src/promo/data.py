"""Data loading, cleaning, weekly SKU panel, identifiability report and a synthetic fixture."""
from __future__ import annotations

import io
import json
import os
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from .config import ROOT, get_logger, load_config, path_for

log = get_logger("promo.data")

COLS = ["invoice", "stock_code", "description", "quantity", "invoice_date", "unit_price", "customer_id", "country"]
_CODE_RE = re.compile(r"^\d{5}[A-Z]*$")


# --------------------------------------------------------------------------- loading
def _standardise(df: pd.DataFrame) -> pd.DataFrame:
    """Rename the 8 UCI columns positionally and cast to parquet-safe dtypes."""
    df = df.iloc[:, :8].copy()
    df.columns = COLS
    df["invoice"] = df["invoice"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)
    df["description"] = df["description"].astype("string")
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    return df.reset_index(drop=True)


def _download_zip(cfg: dict, raw_dir: Path) -> pd.DataFrame:
    """Download the UCI zip and read both xlsx sheets (slow); cache as parquet."""
    import requests

    log.info("downloading %s (slow)", cfg["data"]["uci_zip"])
    r = requests.get(cfg["data"]["uci_zip"], headers={"User-Agent": "Mozilla/5.0"}, timeout=300)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(".xlsx"))
        with z.open(name) as fh:
            sheets = pd.read_excel(fh, sheet_name=None)
    return _standardise(pd.concat(sheets.values(), ignore_index=True))


def load_raw(cfg: dict | None = None) -> pd.DataFrame:
    """Raw transactions. Order: data/raw cache -> $AMPBA_DATA_DIR parquet -> ucimlrepo -> zip download."""
    cfg = cfg or load_config()
    raw_dir = path_for(cfg, "raw")
    cache = raw_dir / cfg["data"]["parquet_name"]
    if cache.exists():
        log.info("reading cache %s", cache)
        return _standardise(pd.read_parquet(cache))
    ext = Path(os.environ.get(cfg["data"]["data_dir_env"], cfg["data"]["default_data_dir"])) / cfg["data"]["parquet_name"]
    if ext.exists():
        log.info("reading %s", ext)
        return _standardise(pd.read_parquet(ext))
    try:
        from ucimlrepo import fetch_ucirepo

        d = fetch_ucirepo(id=cfg["data"]["uci_id"])
        df = pd.concat([d.data.features, d.data.targets], axis=1) if d.data.targets is not None else d.data.features
        log.info("loaded via ucimlrepo")
        out = df.rename(columns=str)
        # ucimlrepo column order differs; map by name when possible
        names = {c.lower().replace(" ", "").replace("_", ""): c for c in out.columns}
        want = ["invoice", "stockcode", "description", "quantity", "invoicedate", "price", "customerid", "country"]
        out = out[[names[w] for w in want]]
        out = _standardise(out)
    except Exception as exc:  # noqa: BLE001
        log.warning("ucimlrepo failed (%s); falling back to zip download", exc)
        out = _download_zip(cfg, raw_dir)
    out.to_parquet(cache, index=False)
    return out


# --------------------------------------------------------------------------- cleaning
def clean_sales(raw: pd.DataFrame, cfg: dict | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply cleaning rules; return (sales, returns).

    Drops cancellations (invoice 'C...', kept separately), Quantity<=0, Price<=0 and non-product codes.
    Rows without Customer ID are kept (invoice-level project). Adds revenue and week.
    """
    cfg = cfg or load_config()
    df = _standardise(raw) if list(raw.columns[:8]) != COLS else raw.copy()
    df["stock_code"] = df["stock_code"].str.strip().str.upper()
    cancel = df["invoice"].str.upper().str.startswith("C")
    returns = df[cancel].copy()
    bad_codes = set(cfg["data"]["non_product_codes"])
    code_bad = df["stock_code"].isin(bad_codes)
    if cfg["data"].get("strict_code_regex", True):
        code_bad |= ~df["stock_code"].str.match(_CODE_RE)
    keep = ~cancel & ~code_bad & (df["quantity"] > 0) & (df["unit_price"] > 0)
    sales = df[keep].copy()
    # a bulk order that was fully cancelled later (same SKU, same quantity) is not demand: drop the sale line
    big = cfg["data"].get("cancelled_bulk_min_qty")
    if big and len(returns):
        key = set(zip(returns["stock_code"], (-returns["quantity"]).astype(int)))
        hit = (sales["quantity"] >= big) & pd.Series([(a, int(b)) in key for a, b in zip(sales["stock_code"], sales["quantity"])], index=sales.index)
        if hit.any():
            log.info("dropping %d fully-cancelled bulk order lines (qty >= %d)", int(hit.sum()), big)
        sales = sales[~hit]
    sales["unit_price"] = sales["unit_price"].astype(float).round(4)
    sales["description"] = sales["description"].astype("string").str.strip().str.upper()
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    sales["week"] = sales["invoice_date"].dt.to_period("W").dt.start_time
    log.info("clean sales %d of %d raw lines (%d cancellation lines)", len(sales), len(df), len(returns))
    return sales.reset_index(drop=True), returns.reset_index(drop=True)


def sku_descriptions(sales: pd.DataFrame) -> pd.DataFrame:
    """Most frequent description per SKU plus total revenue and invoice count."""
    d = sales.dropna(subset=["description"])
    desc = (
        d.groupby(["stock_code", "description"]).size().reset_index(name="n")
        .sort_values(["stock_code", "n", "description"], ascending=[True, False, True])
        .drop_duplicates("stock_code")[["stock_code", "description"]]
    )
    agg = sales.groupby("stock_code").agg(revenue=("revenue", "sum"), n_invoices=("invoice", "nunique")).reset_index()
    out = agg.merge(desc, on="stock_code", how="left")
    out["description"] = out["description"].fillna("").astype(str)
    return out.sort_values("revenue", ascending=False).reset_index(drop=True)


def load_clean(cfg: dict | None = None, raw: pd.DataFrame | None = None) -> pd.DataFrame:
    """Load (or take) raw data and return clean sales lines."""
    cfg = cfg or load_config()
    raw = load_raw(cfg) if raw is None else raw
    sales, _ = clean_sales(raw, cfg)
    return sales


# --------------------------------------------------------------------------- panel
def weekly_panel(sales: pd.DataFrame) -> pd.DataFrame:
    """SKU-week panel: modal price (price at which most units sold), units, revenue, n_baskets."""
    g = sales.groupby(["stock_code", "week", "unit_price"], sort=False).quantity.sum().reset_index()
    g = g.sort_values(["stock_code", "week", "quantity", "unit_price"], ascending=[True, True, False, True])
    modal = g.drop_duplicates(["stock_code", "week"])[["stock_code", "week", "unit_price"]].rename(columns={"unit_price": "price"})
    agg = (
        sales.groupby(["stock_code", "week"])
        .agg(units=("quantity", "sum"), revenue=("revenue", "sum"), n_baskets=("invoice", "nunique"))
        .reset_index()
    )
    panel = modal.merge(agg, on=["stock_code", "week"]).sort_values(["stock_code", "week"]).reset_index(drop=True)
    panel["month"] = panel["week"].dt.month
    log.info("panel: %d SKU-weeks, %d SKUs", len(panel), panel["stock_code"].nunique())
    return panel


def consecutive_changes(panel: pd.DataFrame) -> pd.DataFrame:
    """Price ratio between consecutive-week observations of the same SKU (gap exactly 7 days)."""
    p = panel.sort_values(["stock_code", "week"])
    prev_p = p.groupby("stock_code")["price"].shift()
    prev_w = p.groupby("stock_code")["week"].shift()
    ok = (p["week"] - prev_w) == pd.Timedelta(days=7)
    out = p.loc[ok, ["stock_code", "week"]].copy()
    out["ratio"] = (p.loc[ok, "price"] / prev_p[ok]).to_numpy()
    return out


def price_variation_report(panel: pd.DataFrame, cfg: dict | None = None) -> dict:
    """Identifiability diagnostics: how much does the modal price move?"""
    cfg = cfg or load_config()
    dm = cfg["demand"]
    ch = consecutive_changes(panel)
    r = ch["ratio"].to_numpy()
    thr = dm["drop_threshold"]
    drops = ch.assign(drop=r < 1 - thr).groupby("stock_code")["drop"].sum()
    nweeks = panel.groupby("stock_code").size()
    nprice = panel.groupby("stock_code")["price"].nunique()
    n_pairs = int(len(ch))
    return {
        "n_sku_weeks": int(len(panel)),
        "n_skus": int(panel["stock_code"].nunique()),
        "n_consecutive_pairs": n_pairs,
        "share_changed_gt1pct": float((np.abs(r - 1) > 0.01).mean()) if n_pairs else 0.0,
        "share_changed_gt5pct": float((np.abs(r - 1) > 0.05).mean()) if n_pairs else 0.0,
        "share_drop_gt5pct": float((r < 0.95).mean()) if n_pairs else 0.0,
        "share_drop_gt10pct": float((r < 0.90).mean()) if n_pairs else 0.0,
        "skus_with_min_drops": int((drops >= dm["min_price_drops"]).sum()),
        "skus_identifiable": int(((nweeks >= dm["min_weeks"]).reindex(drops.index, fill_value=False) & (drops >= dm["min_price_drops"])).sum()),
        "skus_single_price": int((nprice == 1).sum()),
    }


# --------------------------------------------------------------------------- fixture
FIXTURE_FAMILIES = ["LUNCH BAG", "MUG", "CANDLE HOLDER", "CAKE STAND", "PHOTO FRAME"]
FIXTURE_VARIANTS = ["RED", "BLUE", "GREEN", "PINK"]
FIXTURE_TRUE_ELASTICITY = -2.5


def make_fixture(n_weeks: int = 70, n_invoices_per_week: int = 400, seed: int = 42) -> pd.DataFrame:
    """Synthetic raw transactions in the UCI schema (offline tests).

    5 families x 4 variants + 6 standalone SKUs. Inclusion probability of a SKU in an invoice follows
    q * (price/base)^TRUE_ELASTICITY, so the true own-price elasticity of units is -2.5 for every SKU.
    SKU 0 pulls a standalone SKU (halo). Also contains junk rows (cancellations, POST, qty<=0, price 0).
    """
    rng = np.random.default_rng(seed)
    skus, descs, base_p, base_q = [], [], [], []
    code = 20000
    for fam in FIXTURE_FAMILIES:
        for v in FIXTURE_VARIANTS:
            skus.append(f"{code}"); descs.append(f"{v} {fam}"); base_p.append(2.0 + 0.5 * (code % 7)); base_q.append(0.10 + 0.02 * (code % 3))
            code += 1
    for k in range(6):
        skus.append(f"{30000 + k}"); descs.append(["TEAPOT COSY", "BRASS LANTERN", "WALL CLOCK", "DOORSTOP ELEPHANT", "WICKER BASKET", "SERVING TRAY"][k]); base_p.append(1.5 + k); base_q.append(0.12)
    S = len(skus)
    base_p = np.array(base_p); base_q = np.array(base_q)
    weeks = pd.date_range("2010-01-04", periods=n_weeks, freq="W-MON")
    rows = []
    inv_no = 500000
    for w_i, wk in enumerate(weeks):
        season = 1.0 + 0.5 * (wk.month >= 10)
        disc = np.where(rng.random(S) < 0.15, rng.choice([0.10, 0.15, 0.20, 0.25], S), 0.0)
        price = np.round(base_p * (1 - disc), 2)
        q = np.clip(base_q * season * (price / base_p) ** FIXTURE_TRUE_ELASTICITY, 0, 0.9)
        inc = rng.random((n_invoices_per_week, S)) < q[None, :]
        # halo: first SKU pulls first standalone SKU
        pull = inc[:, 0] & (rng.random(n_invoices_per_week) < 0.5)
        inc[pull, 20] = True
        ii, jj = np.nonzero(inc)
        qty = 1 + rng.poisson(2, len(ii))
        day = rng.integers(0, 5, n_invoices_per_week)
        for a, b, qq in zip(ii, jj, qty):
            rows.append((str(inv_no + a), skus[b], descs[b], int(qq),
                         wk + pd.Timedelta(days=int(day[a]), hours=10), float(price[b]), float(1000 + a % 50) if a % 5 else np.nan, "United Kingdom"))
        inv_no += n_invoices_per_week
    df = pd.DataFrame(rows, columns=["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"])
    junk = pd.DataFrame(
        [
            ("C900001", skus[0], descs[0], -1, weeks[3], base_p[0], 1001.0, "United Kingdom"),
            ("900002", "POST", "POSTAGE", 1, weeks[3], 18.0, 1001.0, "United Kingdom"),
            ("900003", skus[1], descs[1], -2, weeks[4], base_p[1], 1001.0, "United Kingdom"),
            ("900004", skus[2], descs[2], 3, weeks[4], 0.0, 1001.0, "United Kingdom"),
            ("900005", "M", "Manual", 1, weeks[5], 10.0, 1001.0, "United Kingdom"),
        ],
        columns=df.columns,
    )
    return pd.concat([df, junk], ignore_index=True)


def fixture_cfg() -> dict:
    """Config tuned for the small synthetic fixture."""
    from .config import clone

    cfg = clone(load_config())
    cfg["families"].update({"top_skus": 50, "distance_threshold": 0.9})
    cfg["baskets"].update({"top_skus": 30, "min_support": 0.02})
    cfg["optimiser"].update({"top_families": 20})
    cfg["sweep"]["n_draws"] = 1000
    return cfg


def main() -> None:
    """CLI: load, clean, build the weekly panel and store interim parquet files."""
    cfg = load_config()
    raw = load_raw(cfg)
    sales, returns = clean_sales(raw, cfg)
    panel = weekly_panel(sales)
    interim = path_for(cfg, "interim")
    sales.to_parquet(interim / "sales.parquet", index=False)
    panel.to_parquet(interim / "panel.parquet", index=False)
    (interim / "meta.json").write_text(json.dumps({"raw_rows": int(len(raw)), "cancellation_lines": int(len(returns))}), encoding="utf-8")
    log.info("wrote interim parquet to %s (root %s)", interim, ROOT)


if __name__ == "__main__":
    main()
