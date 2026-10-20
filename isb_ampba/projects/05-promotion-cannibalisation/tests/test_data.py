import numpy as np
import pandas as pd

from promo.data import clean_sales, make_fixture, price_variation_report, sku_descriptions, weekly_panel


def test_clean_sales_rules(raw, cfg):
    sales, returns = clean_sales(raw, cfg)
    assert not sales["invoice"].str.startswith("C").any()
    assert not sales["stock_code"].isin(cfg["data"]["non_product_codes"]).any()
    assert (sales["quantity"] > 0).all() and (sales["unit_price"] > 0).all()
    assert len(returns) >= 1 and returns["invoice"].str.startswith("C").all()
    assert np.allclose(sales["revenue"], sales["quantity"] * sales["unit_price"])


def test_missing_customer_id_is_kept(raw, cfg):
    sales, _ = clean_sales(raw, cfg)
    assert sales["customer_id"].isna().any()


def test_modal_price_picks_most_sold_price(cfg):
    wk = pd.Timestamp("2010-03-01")
    rows = [("1", "10001", "X", 1, wk, 5.0, 1.0, "UK"), ("2", "10001", "X", 9, wk + pd.Timedelta(days=1), 4.0, 1.0, "UK"),
            ("3", "10001", "X", 2, wk + pd.Timedelta(days=2), 5.0, 1.0, "UK")]
    raw = pd.DataFrame(rows, columns=["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"])
    sales, _ = clean_sales(raw, cfg)
    panel = weekly_panel(sales)
    assert len(panel) == 1 and panel.iloc[0]["price"] == 4.0 and panel.iloc[0]["units"] == 12


def test_cancelled_bulk_order_is_dropped(cfg):
    wk = pd.Timestamp("2010-03-01")
    rows = [("1", "10001", "X", 20000, wk, 1.0, 1.0, "UK"), ("C2", "10001", "X", -20000, wk, 1.0, 1.0, "UK"),
            ("3", "10001", "X", 5, wk, 1.0, 1.0, "UK")]
    raw = pd.DataFrame(rows, columns=["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"])
    sales, _ = clean_sales(raw, cfg)
    assert sales["quantity"].tolist() == [5]


def test_panel_units_sum_to_sales(sales_panel):
    sales, _, panel = sales_panel
    assert panel["units"].sum() == sales["quantity"].sum()
    assert np.isclose(panel["revenue"].sum(), sales["revenue"].sum())
    assert not panel.duplicated(["stock_code", "week"]).any()


def test_price_variation_report_and_descriptions(sales_panel, cfg):
    sales, _, panel = sales_panel
    rep = price_variation_report(panel, cfg)
    assert 0 < rep["share_drop_gt5pct"] < 0.5 and rep["skus_identifiable"] > 0
    d = sku_descriptions(sales)
    assert d["stock_code"].is_unique and (d["description"].str.len() > 0).all()


def test_fixture_is_deterministic():
    a, b = make_fixture(n_weeks=8, seed=7), make_fixture(n_weeks=8, seed=7)
    assert a.equals(b)
