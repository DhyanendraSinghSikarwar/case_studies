"""End-to-end smoke test on the synthetic fixture (offline) + Streamlit AppTest."""
import json
import os
from pathlib import Path

import pytest

from churnx import report, train
from churnx.data import make_hillstrom_fixture

APP = Path(__file__).resolve().parents[1] / "app" / "streamlit_app.py"


@pytest.fixture(scope="module")
def project(tmp_path_factory, tx, cfg):
    root = tmp_path_factory.mktemp("proj")
    cfg = {**cfg, "survival": {"enabled": True}}
    train.run(cfg, tx, root, make_figures=True)
    summary = report.run(cfg, tx, root, hillstrom=make_hillstrom_fixture(6000), make_figures=True)
    return root, summary


def test_e2e_outputs_written(project):
    root, summary = project
    for f in ("summary.json", "metrics.json", "policy_table.csv", "test_cohort.csv", "lift_table.csv"):
        assert (root / "outputs" / f).exists(), f
    s = json.loads((root / "outputs" / "summary.json").read_text())
    assert {"churn", "threshold", "pilot", "uplift", "policy", "hillstrom", "survival", "targets"} <= set(s)
    assert (root / "figures" / "09_policy_profit.png").exists()
    assert (root / "figures" / "05_shap_summary.png").exists()


def test_e2e_policy_table_consistent(project):
    _, summary = project
    tab = {r["policy"]: r for r in summary["policy"]["table"]}
    assert tab["oracle"]["profit_inr"] >= max(v["profit_inr"] for k, v in tab.items() if k != "oracle") - 1e-6
    assert tab["oracle"]["pct_of_oracle"] == pytest.approx(100.0)
    assert summary["seed"] == 42
    assert summary["churn"]["test_auc"] > 0.55
    assert summary["hillstrom"]["n"] == 6000


def test_e2e_deterministic_numbers(project, tx, cfg, tmp_path):
    """Re-running the pipeline with seed 42 reproduces the headline numbers exactly."""
    _, summary = project
    cfg2 = {**cfg, "survival": {"enabled": False}}
    train.run(cfg2, tx, tmp_path, make_figures=False)
    s2 = report.run(cfg2, tx, tmp_path, hillstrom=make_hillstrom_fixture(6000), make_figures=False)
    assert s2["churn"]["test_auc"] == pytest.approx(summary["churn"]["test_auc"])
    assert s2["policy"]["table"] == summary["policy"]["table"]


def test_streamlit_app_runs(project):
    from streamlit.testing.v1 import AppTest

    root, _ = project
    os.environ["CHURNX_ROOT"] = str(root)
    try:
        at = AppTest.from_file(str(APP), default_timeout=120).run()
        assert not at.exception, [e.value for e in at.exception]
        assert len(at.tabs) == 5
        at.slider(key="p_cost").set_value(5000).run()
        assert not at.exception
    finally:
        os.environ.pop("CHURNX_ROOT", None)
