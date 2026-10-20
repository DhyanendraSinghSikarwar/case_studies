"""Training orchestration: baseline, WOE scorecard, tuned XGB/LGBM, isotonic calibration, champion selection."""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from . import evaluate as ev
from . import scorecard as sc
from . import woe
from .config import ROOT, get_logger, load_config
from .data import RAW_FEATURES, TARGET, build_splits
from .features import add_features, feature_cols
from .models import fit_baseline_logit, fit_isotonic, predict_pd, tune_and_fit

log = get_logger(__name__)
MODEL_KEYS = ["logit_raw", "scorecard", "xgb", "lgbm"]


def run(trials: int | None = None, raw: pd.DataFrame | None = None, out_dir: Path | str | None = None,
        model_dir: Path | str | None = None, cfg: dict | None = None) -> dict:
    """Train everything, write outputs/metrics.json etc. and return the metrics dict.

    Splits first; binning/scaling/tuning use TRAIN only, calibration uses VALID only, the champion is chosen on
    VALID (raw-probability AUC) and TEST metrics are computed exactly once.
    """
    t0 = time.time()
    cfg = cfg or load_config()
    seed = cfg["seed"]
    np.random.seed(seed)
    random.seed(seed)
    out = Path(out_dir) if out_dir else ROOT / cfg["paths"]["outputs"]
    mdir = Path(model_dir) if model_dir else ROOT / cfg["paths"]["models"]
    out.mkdir(parents=True, exist_ok=True)
    mdir.mkdir(parents=True, exist_ok=True)

    tr, va, te = [add_features(d) for d in build_splits(cfg, raw=raw, save=raw is None)]
    cols = feature_cols(tr, cfg)
    raw_cols = [c for c in cols if c in RAW_FEATURES]
    ytr, yva, yte = (d[TARGET].to_numpy() for d in (tr, va, te))
    n_trials = trials or cfg["models"]["optuna_trials"]

    pds: dict[str, dict[str, np.ndarray]] = {}
    base = fit_baseline_logit(tr[raw_cols], ytr, seed)
    pds["logit_raw"] = {"valid": base.predict_proba(va[raw_cols])[:, 1], "test": base.predict_proba(te[raw_cols])[:, 1]}

    scfg = cfg["scorecard"]
    bp = woe.fit_binning(tr[cols], ytr, scfg["iv_min"], seed)
    ivt = woe.iv_table(bp)
    iv = ivt.set_index("name")["iv"]
    lr, sc_cols = sc.fit_logit_scorecard(woe.woe_transform(bp, tr[cols]), ytr, iv, scfg["corr_max"], seed)
    pds["scorecard"] = {s: lr.predict_proba(woe.woe_transform(bp, d[cols])[sc_cols])[:, 1]
                        for s, d in [("valid", va), ("test", te)]}
    table = sc.build_points_table(bp, lr, sc_cols, scfg)
    table.to_csv(out / "scorecard_points.csv", index=False)
    ivt.to_csv(out / "iv_table.csv", index=False)
    joblib.dump({"bp": bp, "lr": lr, "cols": sc_cols, "table": table, "features": cols}, mdir / "scorecard.joblib")
    pts_test = sc.score_with_table(bp, te[cols], table, sc_cols)
    pts_diff = np.abs(pts_test - sc.pd_to_score(pds["scorecard"]["test"], scfg["base_score"], scfg["base_odds"],
                                                scfg["pdo"], clip=None))

    raw_valid_auc: dict[str, float] = {"scorecard": ev.auc(yva, pds["scorecard"]["valid"])}
    best_params: dict[str, dict] = {}
    cv_auc: dict[str, float] = {}
    for kind in ["xgb", "lgbm"]:
        model, params, cv = tune_and_fit(kind, tr[cols], ytr, n_trials, cfg["models"]["cv_folds"], seed,
                                         cfg["models"].get("n_jobs", 4))
        p_val_raw = model.predict_proba(va[cols])[:, 1]
        iso = fit_isotonic(p_val_raw, yva)
        pds[kind] = {"valid": predict_pd(model, va[cols], iso), "test": predict_pd(model, te[cols], iso)}
        raw_valid_auc[kind] = ev.auc(yva, p_val_raw)
        best_params[kind], cv_auc[kind] = params, cv
        joblib.dump({"model": model, "calibrator": iso, "features": cols}, mdir / f"{kind}.joblib")
        log.info("%s: cv auc %.4f valid auc (raw) %.4f", kind, cv, raw_valid_auc[kind])

    champion = max(["xgb", "lgbm"], key=lambda k: raw_valid_auc[k])     # chosen on VALID, never on test
    pds["champion"] = pds[champion]
    base_rate = float(ytr.mean())
    metrics: dict = {k: {"valid": ev.metrics(yva, pds[k]["valid"]), "test": ev.metrics(yte, pds[k]["test"])}
                     for k in MODEL_KEYS}
    metrics["naive_base_rate"] = {"valid": {"auc": 0.5, "gini": 0.0, "ks": 0.0, "brier": ev.brier(yva, np.full(len(yva), base_rate))},
                                  "test": {"auc": 0.5, "gini": 0.0, "ks": 0.0, "brier": ev.brier(yte, np.full(len(yte), base_rate))},
                                  "base_rate_train": base_rate}
    metrics["champion"] = champion
    metrics["champion_selection"] = {"criterion": "valid ROC-AUC of the uncalibrated model", "valid_auc_raw": raw_valid_auc}
    metrics["scorecard_check"] = {"max_abs_diff_points": float(pts_diff.max()),
                                  "mean_abs_diff_points": float(pts_diff.mean()), "n_variables": len(sc_cols),
                                  "variables": sc_cols}
    metrics["tuning"] = {"trials": n_trials, "cv_auc": cv_auc, "best_params": best_params}
    metrics["sizes"] = {"train": len(tr), "valid": len(va), "test": len(te)}
    metrics["seconds"] = round(time.time() - t0, 1)
    with open(out / "metrics.json", "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2, default=float)

    pred = te[["LIMIT_BAL", "AGE", "SEX", "avg_util", TARGET]].copy().rename(columns={TARGET: "y"})
    for k in MODEL_KEYS:
        pred[f"pd_{k}"] = pds[k]["test"]
    pred["pd"] = pds["champion"]["test"]
    pred["score"] = sc.pd_to_score(pred["pd"], scfg["base_score"], scfg["base_odds"], scfg["pdo"], tuple(scfg["clip"]))
    pred["score_points"] = pts_test
    pred["band"] = sc.assign_band(pred["pd"], scfg["band_pd_edges"])
    pred.to_csv(out / "test_predictions.csv", index_label="row_id")
    log.info("done in %.1fs; champion=%s test AUC %.4f", metrics["seconds"], champion,
             metrics[champion]["test"]["auc"])
    return metrics


def main() -> None:
    """CLI: python -m credit.train [--trials N]."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=None)
    run(ap.parse_args().trials)


if __name__ == "__main__":
    main()
