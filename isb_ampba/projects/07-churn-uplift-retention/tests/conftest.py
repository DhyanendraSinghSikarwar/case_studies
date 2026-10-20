"""Shared offline fixtures (synthetic data only; no network)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from churnx.config import load_config  # noqa: E402
from churnx.data import make_fixture  # noqa: E402
from churnx.snapshot import build_all_snapshots, clean_sales  # noqa: E402


@pytest.fixture(scope="session")
def cfg():
    """Project config with cheap bootstrap settings for tests."""
    c = load_config()
    c["uplift"]["n_boot"] = 20
    c["hillstrom"]["n_boot"] = 20
    return c


@pytest.fixture(scope="session")
def tx():
    """Synthetic Online-Retail-II-like transactions."""
    return make_fixture(n_customers=900, seed=42)


@pytest.fixture(scope="session")
def sales_returns(tx):
    """(sales, returns) after cleaning the fixture."""
    return clean_sales(tx)


@pytest.fixture(scope="session")
def snaps(sales_returns, cfg):
    """All snapshots built from the fixture."""
    sales, returns = sales_returns
    return build_all_snapshots(sales, returns, cfg)


def make_tx(rows):
    """Hand-built raw transactions: (customer, invoice, date, qty, price[, code[, country]])."""
    recs = []
    for r in rows:
        cid, inv, date, qty, price, *rest = r
        code = rest[0] if rest else "A1"
        country = rest[1] if len(rest) > 1 else "United Kingdom"
        recs.append({"invoice": inv, "stock_code": code, "description": "x", "quantity": qty,
                     "invoice_date": pd.Timestamp(date), "unit_price": price, "customer_id": cid, "country": country})
    df = pd.DataFrame(recs)
    df["customer_id"] = df["customer_id"].astype("Int64")
    return df
