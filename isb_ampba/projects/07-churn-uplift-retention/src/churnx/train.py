"""Stage 1+2: snapshots + churn models (temporal split) -> data/processed, models/, outputs/metrics.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from churnx import plots
from churnx.config import ROOT, get_logger, load_config, resolve, set_seed
from churnx.data import load_transactions
from churnx.models import calibration_table, fit_all, lift_table, make_models, shap_importance, temporal_window_check
from churnx.snapshot import FEATURES, build_all_snapshots, clean_sales
from churnx.validate import validate_snapshots

log = get_logger(__name__)


def to_jsonable(o: Any) -> Any:
    """json.dump default hook for numpy / pandas scalars."""
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.ndarray,)):
        return o.tolist()
    if isinstance(o, (pd.Timestamp,)):
        return str(o)
    raise TypeError(f"not serialisable: {type(o)}")


def write_json(obj: Any, path: Path) -> None:
    """Write JSON with numpy support."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=to_jsonable)


def run(cfg: dict[str, Any], tx: pd.DataFrame, root: Path | None = None, make_figures: bool = True) -> dict[str, Any]:
    """Build snapshots, fit/calibrate churn models, save artefacts. Returns the churn metrics dict."""
    root = root or ROOT
    set_seed(cfg["seed"])
    proc, outs, figs, mdl = (resolve(cfg, k, root) for k in ("processed", "outputs", "figures", "models"))
    sales, returns = clean_sales(tx)
    snaps = build_all_snapshots(sales, returns, cfg)
    checks = validate_snapshots(snaps, sales, cfg)
    snaps.to_parquet(proc / "snapshots.parquet", index=False)
    tr, te = snaps[snaps["split"] == "train"], snaps[snaps["split"] == "test"]
    res = fit_all(tr[FEATURES], tr["churn"].to_numpy(), tr["customer_id"].to_numpy(),
                  te[FEATURES], te["churn"].to_numpy(), cfg)
    yte = te["churn"].to_numpy()
    scores = te[["customer_id"]].copy()
    for k, p in res["probs"].items():
        scores[f"p_{k}"] = p
    scores["p_champion_raw"], scores["p_champion_cal"] = res["p_test_raw"], res["p_test_cal"]
    scores.to_parquet(proc / "test_scores.parquet", index=False)
    joblib.dump({"calibrated": res["calibrated"], "champion": res["champion"], "features": FEATURES,
                 "model": res["fitted"][res["champion"]]}, mdl / "churn_champion.joblib")
    lift = lift_table(yte, res["p_test_cal"])
    cal_raw = calibration_table(yte, res["p_test_raw"])
    cal_cal = calibration_table(yte, res["p_test_cal"])
    lift.to_csv(outs / "lift_table.csv", index=False)
    cal_cal.to_csv(outs / "calibration_table.csv", index=False)
    sv, Xs = shap_importance(res["fitted"][res["tree_champion"]], te[FEATURES], seed=cfg["seed"])
    imp = pd.Series(np.abs(sv).mean(0), index=FEATURES).sort_values(ascending=False)
    imp.rename("mean_abs_shap").to_csv(outs / "shap_importance.csv")
    if make_figures:
        plots.churn_rate_by_snapshot(snaps, figs / "01_churn_rate_by_snapshot.png")
        plots.model_comparison(yte, {**res["probs"], "champion_calibrated": res["p_test_cal"]}, figs / "02_model_roc.png")
        plots.calibration_plot(cal_raw, cal_cal, figs / "03_calibration.png")
        plots.lift_chart(lift, figs / "04_lift.png")
        plots.shap_summary(sv, Xs, figs / "05_shap_summary.png")
    snap_tbl = (snaps.groupby(["asof", "split"]).agg(n_eligible=("churn", "size"), churn_rate=("churn", "mean"))
                .reset_index().assign(asof=lambda d: d["asof"].dt.strftime("%Y-%m-%d")))
    hist = snaps[snaps["split"].isin(["pilot_hist", "train"])]
    sup = make_models(cfg["seed"])["logit"].fit(hist[FEATURES], hist["churn"])
    sup_auc = float(roc_auc_score(yte, sup.predict_proba(te[FEATURES])[:, 1]))
    metrics = {"supplementary_logit_6_snapshots_test_auc": sup_auc,
               "temporal_window_check_train_only": temporal_window_check(snaps, FEATURES, cfg["seed"]),
               "models": res["metrics"], "cv_auc_train": res["cv_auc"], "champion": res["champion"],
               "tree_champion_for_shap": res["tree_champion"], "snapshots": snap_tbl.to_dict("records"),
               "checks": checks, "shap_top5": imp.head(5).round(4).to_dict(),
               "calibration_gap_test": {"mean_pred_calibrated": float(res["p_test_cal"].mean()),
                                        "observed_rate": float(yte.mean())},
               "n_train_rows": int(len(tr)), "n_test_rows": int(len(te)),
               "n_customers_in_train_and_test": int(len(set(tr["customer_id"]) & set(te["customer_id"])))}
    write_json({"churn": metrics}, outs / "metrics.json")
    log.info("champion=%s test AUC=%.3f (calibrated %.3f)", res["champion"],
             res["metrics"][res["champion"]]["auc"], res["metrics"]["champion_calibrated"]["auc"])
    return metrics


def main() -> None:
    """CLI entry point (``python -m churnx.train``)."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    a = ap.parse_args()
    cfg = load_config(a.config)
    run(cfg, load_transactions(cfg))


if __name__ == "__main__":
    main()
