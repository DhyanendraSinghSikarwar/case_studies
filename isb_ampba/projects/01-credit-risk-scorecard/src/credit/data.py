"""Load, clean and split the UCI 'Default of Credit Card Clients' data (id 350).

Load order: parquet cache -> local xls (env AMPBA_DATA_DIR, default C:/ampba_data) -> ucimlrepo -> direct zip.
"""
from __future__ import annotations

import io
import os
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from .config import ROOT, get_logger, load_config

log = get_logger(__name__)
TARGET = "default"
PAY_COLS = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]     # PAY_0 = most recent month (Sep)
BILL_COLS = [f"BILL_AMT{i}" for i in range(1, 7)]
PAYAMT_COLS = [f"PAY_AMT{i}" for i in range(1, 7)]
RAW_FEATURES = ["LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE"] + PAY_COLS + BILL_COLS + PAYAMT_COLS
RAW_COLUMNS = RAW_FEATURES + [TARGET]


def _tidy_excel(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=[c for c in df.columns if str(c).upper() == "ID"])
    return df.rename(columns={"default payment next month": TARGET})


def _from_local(cfg: dict) -> pd.DataFrame:
    """Read the xls from AMPBA_DATA_DIR (default C:/ampba_data), searching sub-folders."""
    base = Path(os.environ.get(cfg["data"]["local_dir_env"], cfg["data"]["local_dir_default"]))
    hits = sorted(base.rglob("default of credit card clients*.xls*")) if base.exists() else []
    if not hits:
        raise FileNotFoundError(f"no xls under {base}")
    log.info("reading local file %s", hits[0])
    return _tidy_excel(pd.read_excel(hits[0], header=1))     # row 0 holds X1..X23,Y; row 1 holds the names


def _from_ucimlrepo(uci_id: int) -> pd.DataFrame:
    from ucimlrepo import fetch_ucirepo

    d = fetch_ucirepo(id=uci_id)
    X, y = d.data.features.copy(), d.data.targets.copy()
    if list(X.columns) == [f"X{i}" for i in range(1, 24)]:
        X.columns = RAW_FEATURES
    df = X.copy()
    df[TARGET] = y.iloc[:, 0].to_numpy()
    return df


def _from_zip(url: str) -> pd.DataFrame:
    import requests

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = [n for n in z.namelist() if n.lower().endswith((".xls", ".xlsx"))][0]
        return _tidy_excel(pd.read_excel(z.open(name), header=1))


def load_raw(cfg: dict | None = None, refresh: bool = False) -> pd.DataFrame:
    """Return the raw 30,000 x 24 frame, using the parquet cache when present."""
    cfg = cfg or load_config()
    cache = ROOT / cfg["data"]["raw_cache"]
    if cache.exists() and not refresh:
        return pd.read_parquet(cache)
    df = None
    for name, fn in [("local xls", lambda: _from_local(cfg)),
                     ("ucimlrepo", lambda: _from_ucimlrepo(cfg["data"]["uci_id"])),
                     ("zip download", lambda: _from_zip(cfg["data"]["zip_url"]))]:
        try:
            df = fn()
            log.info("loaded raw data via %s", name)
            break
        except Exception as e:  # noqa: BLE001 - any failure -> try next source
            log.warning("%s failed (%s)", name, e)
    if df is None:
        raise RuntimeError("could not load UCI 350 from any source")
    df = df[RAW_COLUMNS].astype("int64")
    cache.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache, index=False)
    log.info("cached %s rows to %s", len(df), cache)
    return df


def make_fixture(n: int = 1500, seed: int = 42) -> pd.DataFrame:
    """Synthetic frame with the UCI 350 schema (offline tests). Default depends on repayment behaviour."""
    rng = np.random.default_rng(seed)
    lim = rng.choice(np.arange(1, 81) * 10000, size=n)
    pay = np.clip(np.round(rng.normal(0, 1.2, size=(n, 6)) + rng.normal(0, 1, size=(n, 1))), -2, 8).astype(int)
    bill = np.round(lim[:, None] * rng.uniform(0, 1.1, size=(n, 6)) * rng.uniform(0.3, 1, size=(n, 1)))
    payamt = np.round(bill[:, 1:].mean(axis=1, keepdims=True) * rng.uniform(0, 0.6, size=(n, 6)))
    z = -1.9 + 0.55 * np.clip(pay[:, 0], 0, None) + 0.15 * np.clip(pay, 0, None).sum(axis=1) - 0.000004 * lim
    y = (rng.uniform(size=n) < 1 / (1 + np.exp(-z))).astype(int)
    df = pd.DataFrame({"LIMIT_BAL": lim, "SEX": rng.integers(1, 3, n), "EDUCATION": rng.integers(0, 7, n),
                       "MARRIAGE": rng.integers(0, 4, n), "AGE": rng.integers(21, 70, n)})
    for j, c in enumerate(PAY_COLS):
        df[c] = pay[:, j]
    for j, c in enumerate(BILL_COLS):
        df[c] = bill[:, j].astype(int)
    for j, c in enumerate(PAYAMT_COLS):
        df[c] = payamt[:, j].astype(int)
    df[TARGET] = y
    return df[RAW_COLUMNS]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """EDUCATION {0,5,6} -> 4 (others); MARRIAGE 0 -> 3 (others). Keeps every row (incl. duplicates)."""
    out = df.copy()
    out["EDUCATION"] = out["EDUCATION"].replace({0: 4, 5: 4, 6: 4})
    out["MARRIAGE"] = out["MARRIAGE"].replace({0: 3})
    return out


def split(df: pd.DataFrame, cfg: dict | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Stratified 60/20/20 split; the original index is preserved."""
    cfg = cfg or load_config()
    s, seed = cfg["data"]["split"], cfg["seed"]
    train, rest = train_test_split(df, train_size=s["train"], stratify=df[TARGET], random_state=seed)
    valid, test = train_test_split(rest, test_size=s["test"] / (s["valid"] + s["test"]),
                                   stratify=rest[TARGET], random_state=seed)
    return train, valid, test


def build_splits(cfg: dict | None = None, raw: pd.DataFrame | None = None, save: bool = True):
    """Load (or take) raw data, clean, split; optionally persist to data/processed."""
    cfg = cfg or load_config()
    df = clean(load_raw(cfg) if raw is None else raw)
    train, valid, test = split(df, cfg)
    if save:
        out = ROOT / cfg["paths"]["processed"]
        out.mkdir(parents=True, exist_ok=True)
        for name, part in zip(["train", "valid", "test"], [train, valid, test], strict=True):
            part.to_parquet(out / f"{name}.parquet")
    return train, valid, test


if __name__ == "__main__":
    tr, va, te = build_splits()
    log.info("train/valid/test = %s/%s/%s", len(tr), len(va), len(te))
