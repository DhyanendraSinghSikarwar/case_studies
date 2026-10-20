import pandas as pd

from churnx.data import TX_COLS, load_transactions, make_fixture, make_hillstrom_fixture
from churnx.snapshot import NON_PRODUCT, clean_sales
from tests.conftest import make_tx


def test_fixture_schema_and_reproducible():
    a, b = make_fixture(50, seed=1), make_fixture(50, seed=1)
    assert list(a.columns) == list(TX_COLS.values())
    pd.testing.assert_frame_equal(a, b)
    assert a["invoice"].map(type).eq(str).all()


def test_clean_sales_removes_cancellations_and_non_products(tx):
    sales, returns = clean_sales(tx)
    assert not sales["invoice"].str.startswith("C").any()
    assert not sales["stock_code"].str.upper().isin(NON_PRODUCT).any()
    assert (sales["quantity"] > 0).all() and (sales["unit_price"] > 0).all()
    assert sales["customer_id"].notna().all()
    assert len(returns) > 0 and returns["invoice"].str.startswith("C").all()
    assert (sales["revenue"] == sales["quantity"] * sales["unit_price"]).all()


def test_clean_sales_drops_anonymous_and_bad_rows():
    raw = make_tx([(1, "10", "2011-01-01", 2, 3.0), (None, "11", "2011-01-01", 2, 3.0),
                   (1, "12", "2011-01-02", -1, 3.0), (1, "13", "2011-01-02", 1, 0.0),
                   (1, "14", "2011-01-03", 1, 5.0, "POST"), (1, "C15", "2011-01-03", -1, 5.0)])
    sales, returns = clean_sales(raw)
    assert list(sales["invoice"]) == ["10"]
    assert list(returns["invoice"]) == ["C15"]


def test_load_transactions_from_env_dir(tmp_path, monkeypatch, cfg):
    """Resolution order: external AMPBA_DATA_DIR parquet is used (and cached to interim) when no cache exists."""
    raw = make_fixture(30, seed=3).rename(columns={v: k for k, v in TX_COLS.items()})
    raw["Customer ID"] = raw["Customer ID"].astype(float)
    ext = tmp_path / "ext"
    ext.mkdir()
    raw.to_parquet(ext / cfg["data"]["parquet_name"])
    monkeypatch.setenv(cfg["data"]["env_var"], str(ext))
    root = tmp_path / "proj"
    out = load_transactions(cfg, root=root)
    assert len(out) == len(raw) and (root / cfg["paths"]["interim"] / "transactions.parquet").exists()
    assert len(load_transactions(cfg, root=root)) == len(raw)          # second call hits the cache


def test_hillstrom_fixture_schema():
    h = make_hillstrom_fixture(500)
    assert {"segment", "visit", "conversion", "spend"} <= set(h.columns)
