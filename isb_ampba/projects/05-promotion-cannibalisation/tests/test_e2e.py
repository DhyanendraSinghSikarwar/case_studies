"""End-to-end smoke tests on the synthetic fixture (offline)."""
import json
import os
from pathlib import Path

import numpy as np
import pytest

from promo.data import fixture_cfg
from promo.pipeline import run_pipeline
from promo.report import memo, model_card, results_block


@pytest.fixture(scope="module")
def run(raw, tmp_path_factory):
    d = tmp_path_factory.mktemp("e2e")
    s = run_pipeline(raw, fixture_cfg(), d / "outputs", d / "figures", d / "models")
    return s, d


def test_pipeline_writes_artifacts(run):
    s, d = run
    for f in ("summary.json", "metrics.json", "engine_inputs.parquet", "promo_plan.csv", "reference_promo.csv", "sweep_draws.csv"):
        assert (d / "outputs" / f).exists(), f
    assert (d / "figures" / "tornado.png").exists() and (d / "figures" / "waterfall_top_revenue_sku.png").exists()
    on_disk = json.loads((d / "outputs" / "summary.json").read_text())
    assert on_disk["sweep"]["n_draws"] >= 1000 and on_disk["sweep"]["reproducible_with_seed"] is True


def test_pipeline_numbers_consistent(run):
    s, _ = run
    r = s["reference"]
    assert abs(r["family_net_total_gbp"] - (r["direct_total_gbp"] - r["subsidy_total_gbp"] - r["cannibalised_total_gbp"] + r["halo_total_gbp"])) < 1e-4
    assert s["mnl_checks"]["max_share_sum_error"] < 1e-9 and s["mnl_checks"]["max_rel_elasticity_error_d0.001"] < 0.01
    assert s["optimiser"]["plan_within_budget"] is True
    assert abs(s["demand"]["pooled_two_way_fe"]["eps"] + 2.5) < 0.3


def test_pipeline_is_reproducible(raw, run, tmp_path):
    s1, _ = run
    s2 = run_pipeline(raw, fixture_cfg(), tmp_path / "o", tmp_path / "f")
    for k in ("reference", "sweep", "kpi_classification"):
        assert s1[k] == s2[k]


def test_docs_are_generated_from_summary(run):
    s, _ = run
    m = memo(s)
    assert f"{s['sweep']['pct_family_profitable']:,.1f}%" in m and "break-even multiplier" in m
    assert "Intended use" in model_card(s) and "RESULTS:START" in results_block(s)


def test_streamlit_app_runs(run):
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    s, d = run
    os.environ["PROMO_OUT_DIR"] = str(d / "outputs")
    try:
        app = Path(__file__).resolve().parents[1] / "app" / "streamlit_app.py"
        at = AppTest.from_file(str(app), default_timeout=180).run()
        assert not at.exception, at.exception
        assert len(at.tabs) == 4 and len(at.metric) >= 5
        at.selectbox(key="sku").select_index(2).run()
        assert not at.exception
        at.select_slider(key="disc").set_value(0.25).run()
        assert not at.exception
        [w for w in at.slider if w.key.startswith("eps_")][0].set_value(-6.0).run()
        assert not at.exception
        net_hi = [m.value for m in at.metric if m.label == "Family net"][0]
        [w for w in at.slider if w.key.startswith("eps_")][0].set_value(-0.6).run()
        net_lo = [m.value for m in at.metric if m.label == "Family net"][0]
        assert net_hi != net_lo
    finally:
        os.environ.pop("PROMO_OUT_DIR", None)
    assert np.isfinite(s["reference"]["family_net_total_gbp"])
