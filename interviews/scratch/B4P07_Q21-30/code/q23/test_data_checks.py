import pandas as pd
import pytest

from data_checks import check_frame


@pytest.fixture
def good():
    return pd.DataFrame({
        "customer_id": [1, 2, 3, 4, 5, 6],
        "age": [25, 40, 33, 58, 29, 61],
        "plan": ["basic", "plus", "pro", "basic", "plus", "pro"],
        "monthly_spend": [10.0, 25.5, 40.0, 12.0, 30.0, 55.0],
        "churned": [0, 1, 0, 0, 1, 0],
    })


def test_good_frame_passes(good):
    assert check_frame(good) == []


def test_corrupted_frame_reports_every_problem(good):
    bad = good.copy()
    bad.loc[1, "age"] = 250
    bad.loc[2, "plan"] = "platinum"
    bad.loc[3, "monthly_spend"] = -5.0
    bad.loc[4, "customer_id"] = 1
    bad.loc[[0, 5], "monthly_spend"] = None
    out = check_frame(bad)
    assert "customer_id not unique" in out
    assert "age out of range 18-100" in out
    assert "monthly_spend negative" in out
    assert any("unknown values" in m for m in out)
    assert any("null rate" in m for m in out)


def test_wrong_dtype_and_missing_column(good):
    bad = good.astype({"age": "float64"}).drop(columns=["plan"])
    out = check_frame(bad)
    assert "missing column: plan" in out
    assert any(m.startswith("dtype age") for m in out)


def test_too_few_rows(good):
    assert any("row count" in m for m in check_frame(good.head(2)))
