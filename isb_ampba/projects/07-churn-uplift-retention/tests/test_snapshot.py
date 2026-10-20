import pandas as pd
import pytest

from churnx.snapshot import FEATURES, build_features, build_snapshot, clean_sales, make_label
from churnx.validate import check_feature_names, label_windows_do_not_overlap
from tests.conftest import make_tx

BASE = [(1, "10", "2011-01-05", 2, 3.0), (1, "11", "2011-01-20", 1, 4.0), (1, "12", "2011-02-10", 3, 2.0),
        (2, "20", "2011-01-06", 2, 3.0), (2, "21", "2011-02-01", 1, 4.0)]


def test_features_before_asof():
    """A huge purchase on asof+1 day must not change any feature at asof (point-in-time features)."""
    asof = "2011-03-01"
    s0, r0 = clean_sales(make_tx(BASE))
    future = [(1, "99", "2011-03-02", 1000, 50.0), (3, "98", "2011-03-02", 5, 1.0),
              (3, "97", "2011-03-03", 5, 1.0), (1, "C96", "2011-03-02", -5, 1.0)]
    s1, r1 = clean_sales(make_tx(BASE + future))
    f0 = build_features(s0, r0, asof).set_index("customer_id").sort_index()
    f1 = build_features(s1, r1, asof).set_index("customer_id").sort_index()
    pd.testing.assert_frame_equal(f0, f1)


def test_features_before_asof_on_fixture(sales_returns):
    """Dropping every row on/after asof must leave the features identical (strict < asof)."""
    sales, returns = sales_returns
    asof = pd.Timestamp("2011-05-01")
    full = build_features(sales, returns, asof)
    cut = build_features(sales[sales["invoice_date"] < asof], returns[returns["invoice_date"] < asof], asof)
    pd.testing.assert_frame_equal(full, cut)


def test_features_exclude_asof_boundary():
    s, r = clean_sales(make_tx(BASE + [(1, "50", "2011-03-01 00:00:00", 1, 1.0)]))
    f = build_features(s, r, "2011-03-01").set_index("customer_id")
    assert f.loc[1, "frequency_6m"] == 3      # the order exactly at asof is excluded


def test_label_window_matches_horizon():
    """Day 89 purchase -> not churned; day 91 purchase -> churned."""
    rows = BASE + [(1, "30", "2011-05-29 23:00", 1, 1.0), (2, "32", "2011-05-31", 1, 1.0),
                   (9, "33", "2011-06-15", 1, 1.0)]
    s, _ = clean_sales(make_tx(rows))
    lab = make_label(s, [1, 2], "2011-03-01", 90)
    assert lab[1] == 0 and lab[2] == 1


def test_label_window_assertion():
    s, _ = clean_sales(make_tx(BASE))
    with pytest.raises(AssertionError):
        make_label(s, [1, 2], "2011-02-01", 90)


def test_eligibility_requires_min_orders():
    s, r = clean_sales(make_tx(BASE + [(5, "60", "2011-02-15", 1, 1.0)]))
    f = build_features(s, r, "2011-03-01", 180, 2)
    assert 5 not in set(f["customer_id"]) and {1, 2} <= set(f["customer_id"])


def test_snapshots_do_not_overlap_in_label_time(cfg):
    assert label_windows_do_not_overlap(cfg)
    bad = {**cfg, "snapshots": {**cfg["snapshots"], "test": "2011-06-15"}}
    assert not label_windows_do_not_overlap(bad)


def test_model_has_no_future_columns():
    check_feature_names(FEATURES)
    assert not set(FEATURES) & {"churn", "w", "y", "saved", "tau_true", "retained", "p0", "save_rate_true"}
    with pytest.raises(AssertionError):
        check_feature_names(["recency_days", "tau_hat"])


def test_build_snapshot_no_nans_and_binary_label(sales_returns, cfg):
    sales, returns = sales_returns
    s = build_snapshot(sales, returns, "2011-04-01", cfg["snapshots"])
    assert len(s) > 50 and not s[FEATURES].isna().any().any() and set(s["churn"]) <= {0, 1}
    assert s["recency_days"].between(0, 180).all()
