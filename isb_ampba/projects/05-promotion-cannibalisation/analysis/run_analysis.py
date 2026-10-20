"""Regenerate every figure, outputs/summary.json, metrics.json and the number-bearing docs.

Usage: python analysis/run_analysis.py [--fixture]
  default   reads outputs/engine_inputs.parquet + interim panel (run `python tasks.py data train` first)
  --fixture runs the whole pipeline end-to-end on the synthetic fixture into a temp dir (offline smoke run)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from promo.config import get_logger, seed_everything  # noqa: E402
from promo.pipeline import default_dirs, evaluate, load_stage_inputs, to_py  # noqa: E402
from promo.report import write_docs  # noqa: E402

log = get_logger("analysis")


def main() -> None:
    """Run the evaluation stage on the trained engine table and write all artifacts."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", action="store_true", help="synthetic offline run (does not touch outputs/)")
    args = ap.parse_args()
    t0 = time.time()
    cfg, out_dir, fig_dir, _ = default_dirs()
    seed_everything(cfg)
    if args.fixture:
        import tempfile

        from promo.data import fixture_cfg, make_fixture
        from promo.pipeline import run_pipeline

        tmp = Path(tempfile.mkdtemp())
        s = run_pipeline(make_fixture(), fixture_cfg(), tmp / "outputs", tmp / "figures")
        log.info("fixture run done: %s", json.dumps(s["reference"])[:300])
        return
    train = json.loads((out_dir / "train_summary.json").read_text(encoding="utf-8"))
    table = pd.read_parquet(out_dir / "engine_inputs.parquet")
    _, panel = load_stage_inputs(cfg)
    el = pd.read_csv(out_dir / "elasticities.csv")
    res = {"table": table, "elasticities": el}
    summary = {"seed": cfg["seed"], **train}
    summary.update(evaluate(res, panel, cfg, out_dir, fig_dir))
    summary["runtime_seconds_evaluate"] = round(time.time() - t0, 1)
    summary = to_py(summary)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    metrics = {"identity_tolerance": 1e-6, "sweep_n_draws": summary["sweep"]["n_draws"], **summary["kpi_classification"],
               "pct_promoted_only_profitable": summary["sweep"]["pct_promoted_only_profitable"],
               "pct_family_profitable": summary["sweep"]["pct_family_profitable"],
               "reference_family_net_total_gbp": summary["reference"]["family_net_total_gbp"]}
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    write_docs(summary, ROOT)
    log.info("analysis done in %.1fs", time.time() - t0)


if __name__ == "__main__":
    main()
