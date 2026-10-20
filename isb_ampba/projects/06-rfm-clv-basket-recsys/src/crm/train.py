"""Orchestrates M1-M5 modelling: writes CSV artifacts, models and outputs/metrics.json."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import joblib
import pandas as pd

from . import basket, campaign, cluster, clv, recsys, rfm
from .config import get_logger, load_config, resolve, seed_everything
from .data import load_sales, split_calibration_holdout

log = get_logger(__name__)


def _jsonable(o):
    """Make numpy / pandas scalars JSON serialisable."""
    import numpy as np

    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, list | tuple):
        return [_jsonable(v) for v in o]
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return None if np.isnan(o) else float(o)
    if isinstance(o, float) and np.isnan(o):
        return None
    return o


def run_pipeline(sales: pd.DataFrame, cfg: dict, out_dir: Path, models_dir: Path | None = None,
                 embed: bool = True) -> dict:
    """Run RFM -> clustering -> CLV -> basket -> recsys -> campaign. Returns the metrics dict."""
    seed_everything(cfg["seed"])
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    cal, hold = split_calibration_holdout(sales, cfg)
    asof = pd.Timestamp(cfg["data"]["calibration_end"]) + pd.Timedelta(days=1)
    metrics: dict = {"seed": cfg["seed"]}
    metrics["data"] = {
        "clean_lines": len(sales), "customers_total": int(sales["customer_id"].nunique()),
        "calibration_lines": len(cal), "calibration_customers": int(cal["customer_id"].nunique()),
        "holdout_lines": len(hold), "holdout_customers": int(hold["customer_id"].nunique()),
        "customers_in_both": len(set(cal["customer_id"]) & set(hold["customer_id"])),
        "holdout_spend": float(hold["revenue"].sum()),
        "date_min": str(sales["invoice_date"].min()), "date_max": str(sales["invoice_date"].max()),
        "calibration_max_date": str(cal["invoice_date"].max()),
        "holdout_min_date": str(hold["invoice_date"].min()),
    }

    # ---- M1 RFM
    r = rfm.build_rfm(cal, asof, cfg)
    seg = rfm.segment_summary(r)
    seg.to_csv(out_dir / "segment_summary.csv", index=False)
    metrics["rfm"] = {"asof": str(asof), "n_customers": len(r),
                      "segments": json.loads(seg.to_json(orient="records"))}
    log.info("M1 rfm done (%.0fs)", time.time() - t0)

    # ---- M2 clustering
    cl = cluster.run_clustering(r, cfg, embed=embed)
    r["cluster"] = cl["labels"]
    r["cluster_name"] = cl["cluster_names"]
    if embed:
        r["emb_x"], r["emb_y"] = cl["embedding"][:, 0], cl["embedding"][:, 1]
    cl["profile"].to_csv(out_dir / "cluster_profile.csv", index=False)
    cl["kmeans_sweep"].to_csv(out_dir / "kmeans_sweep.csv", index=False)
    cl["gmm_sweep"].to_csv(out_dir / "gmm_sweep.csv", index=False)
    metrics["cluster"] = dict(cl["metrics"])
    metrics["cluster"]["embedding_method"] = cl.get("embedding_method")
    metrics["cluster"]["features"] = cfg["cluster"]["features"]
    metrics["cluster"]["profile"] = json.loads(cl["profile"].to_json(orient="records"))
    log.info("M2 clustering done (%.0fs)", time.time() - t0)

    # ---- M3 CLV
    cv = clv.run_clv(cal, hold, cfg)
    metrics["clv"] = cv["metrics"]
    cv["calibration"].to_csv(out_dir / "clv_calibration.csv", index=False)
    tab = cv["table"].rename(columns={"index": "customer_id"})
    cust = r.merge(tab[["customer_id", "m12_pred_purchases", "m12_pred_avg_value", "m12_pred_clv",
                        "m12_p_alive", "h_pred_purchases", "h_pred_clv", "actual_purchases",
                        "actual_spend", "base_spend", "clv_decile"]], on="customer_id", how="left")
    log.info("M3 clv done (%.0fs)", time.time() - t0)

    # ---- M4 basket + recsys
    bk = basket.run_basket(sales, cfg)
    bk["bundles"].to_csv(out_dir / "bundles.csv", index=False)
    metrics["basket"] = bk["metrics"]
    names = bk["names"]
    names.rename_axis("stock_code").reset_index(name="description").to_csv(
        out_dir / "products.csv", index=False)
    rs = recsys.run_recsys(sales, cfg)
    rs["tuning"].to_csv(out_dir / "recsys_tuning.csv", index=False)
    metrics["recsys"] = rs["metrics"]
    metrics["recsys"]["best_params"] = rs["best_params"]
    metrics["recsys"]["best_hybrid_weight"] = rs["best_hybrid_weight"]
    uids = [int(u) for u in cust["customer_id"]]
    rec_rows = []
    for mode, excl in (("reorder_or_new", False), ("discovery", True)):
        recs = recsys.recommend_for_users(rs, uids, cfg["recsys"]["k"], exclude_seen=excl)
        for u, items in recs.items():
            for i, s in enumerate(items, 1):
                rec_rows.append((u, mode, i, s, names.get(s, s)))
    pd.DataFrame(rec_rows, columns=["customer_id", "mode", "rank", "stock_code", "description"]
                 ).to_csv(out_dir / "recommendations.csv", index=False)
    log.info("M4 basket+recsys done (%.0fs)", time.time() - t0)

    # ---- M5 campaign
    cp = campaign.run_campaign(cust, cfg)
    cp["economics"].to_csv(out_dir / "campaign_economics.csv", index=False)
    cp["plan"].to_csv(out_dir / "campaign_plan.csv", index=False)
    cp["sensitivity"].to_csv(out_dir / "campaign_sensitivity.csv", index=False)
    metrics["campaign"] = cp["metrics"]
    cust.to_csv(out_dir / "customers.csv", index=False)

    if models_dir is not None:
        models_dir = Path(models_dir)
        models_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump({"kmeans": cl["model"], "scaler": cl["scaler"]}, models_dir / "cluster.joblib")
        joblib.dump({"bgnbd_params": {k: float(v) for k, v in cv["bgf"].params_.items()},
                     "gg_params": {k: float(v) for k, v in cv["ggf"].params_.items()}},
                    models_dir / "clv.joblib")   # lifetimes fitters hold lambdas: store params only
        joblib.dump({"als_user": rs["model"].user_factors, "als_item": rs["model"].item_factors,
                     "users": list(rs["inter"].users), "items": list(rs["inter"].items),
                     "hybrid_weight": rs["best_hybrid_weight"]}, models_dir / "als.joblib")
    metrics["runtime_seconds"] = round(time.time() - t0, 1)
    with open(out_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(_jsonable(metrics), f, indent=2)
    log.info("pipeline done in %.0fs", time.time() - t0)
    return metrics


def main() -> None:
    """CLI entry: python -m crm.train [--no-embed]."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-embed", action="store_true", help="skip UMAP embedding")
    a = ap.parse_args()
    cfg = load_config()
    run_pipeline(load_sales(cfg), cfg, resolve(cfg, "outputs"), resolve(cfg, "models"),
                 embed=not a.no_embed)


if __name__ == "__main__":
    main()
