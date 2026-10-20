"""End-to-end smoke test on the offline fixture: pipeline -> analysis summary -> Streamlit AppTest."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

from crm.train import run_pipeline

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def artifacts(sales, fast_cfg, tmp_path_factory):
    out = tmp_path_factory.mktemp("outputs")
    metrics = run_pipeline(sales, fast_cfg, out, tmp_path_factory.mktemp("models"), embed=False)
    return out, metrics


def test_pipeline_writes_all_artifacts(artifacts):
    out, metrics = artifacts
    for f in ("customers.csv", "segment_summary.csv", "cluster_profile.csv", "bundles.csv",
              "recommendations.csv", "campaign_economics.csv", "campaign_plan.csv",
              "campaign_sensitivity.csv", "metrics.json", "products.csv", "clv_calibration.csv"):
        assert (out / f).exists(), f
    assert {"rfm", "cluster", "clv", "basket", "recsys", "campaign"} <= set(metrics)
    m = json.loads((out / "metrics.json").read_text())
    assert m["data"]["calibration_max_date"] < m["data"]["holdout_min_date"]
    assert m["recsys"]["train_max_date"] < m["recsys"]["test_min_date"]
    cust = pd.read_csv(out / "customers.csv")
    assert cust["customer_id"].is_unique and cust["segment"].notna().all()


def test_analysis_summary_and_figures(artifacts, fast_cfg, tmp_path):
    sys.path.insert(0, str(ROOT / "analysis"))
    import run_analysis as ra

    out, metrics = artifacts
    cust = pd.read_csv(out / "customers.csv")
    s = ra.build_summary(metrics, fast_cfg, cust)
    assert s["recsys_als_ndcg_ratio"] == metrics["recsys"][fast_cfg["recsys"]["primary_protocol"]][
        "als"]["ndcg_ratio_vs_popularity"]
    ra.fig_recsys(metrics["recsys"], tmp_path)
    ra.fig_campaign(pd.read_csv(out / "campaign_economics.csv"),
                    pd.read_csv(out / "campaign_sensitivity.csv"), tmp_path)
    assert (tmp_path / "07_recsys_metrics.png").stat().st_size > 1000


def test_streamlit_app_renders(artifacts, monkeypatch):
    from streamlit.testing.v1 import AppTest

    out, _ = artifacts
    monkeypatch.setenv("CRM_OUTPUTS", str(out))
    at = AppTest.from_file(str(ROOT / "app" / "streamlit_app.py"), default_timeout=90).run()
    assert not at.exception, at.exception
    assert len(at.tabs) == 4
    at.selectbox[0].select_index(3).run()                    # pick another customer in Customer 360
    assert not at.exception
    at.slider[0].set_value(1.5).run()                       # campaign planner response multiplier
    assert not at.exception
