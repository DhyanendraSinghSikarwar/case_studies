from __future__ import annotations

import json

import pandas as pd

from credit import train


def test_end_to_end_smoke(raw, tmp_path):
    m = train.run(trials=2, raw=raw, out_dir=tmp_path, model_dir=tmp_path)
    on_disk = json.loads((tmp_path / "metrics.json").read_text())
    for k in ["logit_raw", "scorecard", "xgb", "lgbm"]:
        assert set(on_disk[k]["test"]) >= {"auc", "gini", "ks", "brier"}
    assert on_disk["champion"] in ("xgb", "lgbm") and m["champion"] == on_disk["champion"]
    assert on_disk["scorecard_check"]["max_abs_diff_points"] <= 1.0
    pred = pd.read_csv(tmp_path / "test_predictions.csv")
    assert {"pd", "score", "band"} <= set(pred.columns) and len(pred) == int(len(raw) * 0.2)
    assert (tmp_path / "scorecard_points.csv").exists() and (tmp_path / "lgbm.joblib").exists()
