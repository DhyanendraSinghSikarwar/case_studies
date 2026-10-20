import numpy as np
import pytest

from churnx.data import make_hillstrom_fixture
from churnx.hillstrom import balance_table, run_hillstrom
from churnx.survival import run_survival, time_to_next_purchase


def test_hillstrom_balance_on_randomised_fixture():
    bal = balance_table(make_hillstrom_fixture(8000))
    assert bal["std_diff"].abs().max() < 0.1


def test_run_hillstrom_fixture_structure_and_positive_visit_qini(cfg):
    res, extras = run_hillstrom(make_hillstrom_fixture(8000), cfg)
    assert max(res["learners"]["visit"][L]["qini"] for L in ("S", "T", "X", "TO")) > 0
    lo, hi = res["learners"]["visit"]["S"]["qini_ci95"]
    assert lo <= res["learners"]["visit"]["S"]["qini"] <= hi
    assert set(res["policies"]) >= {"random_30", "all", "uplift_top_30", "uplift_profit_optimal"}
    assert "visit" in extras["qini_curves"]


def test_survival_durations_and_cox(snaps, sales_returns, cfg):
    sales, _ = sales_returns
    te = snaps[snaps["split"] == "test"]
    fr = time_to_next_purchase(sales, te, cfg["snapshots"]["test"], 90)
    assert fr["duration"].between(0, 90).all()
    assert abs((1 - fr["event"].mean()) - te["churn"].mean()) < 1e-9      # censored == churned
    pytest.importorskip("lifelines")
    summ, km = run_survival(fr)
    assert 0 <= summ["km_survival_90d"] <= summ["km_survival_30d"] <= 1
    assert np.isfinite(summ["cox_concordance"]) and len(km) > 0
