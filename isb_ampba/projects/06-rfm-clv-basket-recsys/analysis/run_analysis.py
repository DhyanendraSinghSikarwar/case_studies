"""Regenerate every figure and outputs/summary.json from the artifacts written by `crm.train`.

Usage: python analysis/run_analysis.py [--outputs DIR] [--figures DIR]
If outputs/metrics.json is missing the full pipeline is run first.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "analysis"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from crm.config import get_logger, load_config, resolve

log = get_logger("analysis")
PAL = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2", "#9D755D", "#BAB0AC"]
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 110,
                     "axes.grid": True, "grid.alpha": 0.25, "font.size": 9})


def _save(fig, figdir: Path, name: str) -> None:
    fig.tight_layout()
    fig.savefig(figdir / name, dpi=130)
    plt.close(fig)


def fig_segments(seg: pd.DataFrame, figdir: Path) -> None:
    """Customer share vs revenue share per rule segment."""
    fig, ax = plt.subplots(figsize=(7, 3.6))
    x = np.arange(len(seg))
    ax.bar(x - 0.2, seg["customer_share"] * 100, 0.4, label="% customers", color=PAL[0])
    ax.bar(x + 0.2, seg["revenue_share"] * 100, 0.4, label="% revenue", color=PAL[1])
    ax.set_xticks(x, seg["segment"], rotation=20)
    ax.set_ylabel("%")
    ax.set_title("RFM rule segments: customers vs revenue (calibration to 2011-06-30)")
    ax.legend()
    _save(fig, figdir, "01_rfm_segments.png")


def fig_cluster_selection(km: pd.DataFrame, gm: pd.DataFrame, k_final: int, figdir: Path) -> None:
    """Elbow, silhouette and GMM BIC."""
    fig, ax = plt.subplots(1, 3, figsize=(10, 3.2))
    ax[0].plot(km["k"], km["inertia"], "o-", color=PAL[0])
    ax[0].set_title("KMeans elbow (inertia)")
    ax[1].plot(km["k"], km["silhouette"], "o-", color=PAL[0], label="KMeans")
    ax[1].plot(gm["k"], gm["silhouette"], "s--", color=PAL[1], label="GMM")
    ax[1].axhline(0.35, color="grey", ls=":", label="target 0.35")
    ax[1].axvline(k_final, color=PAL[2], ls=":", label=f"chosen k={k_final}")
    ax[1].set_title("Silhouette")
    ax[1].legend(fontsize=7)
    ax[2].plot(gm["k"], gm["bic"], "s-", color=PAL[1])
    ax[2].set_title("GMM BIC")
    for a in ax:
        a.set_xlabel("k")
    _save(fig, figdir, "02_cluster_selection.png")


def fig_embedding(cust: pd.DataFrame, method: str, figdir: Path) -> None:
    """2D embedding coloured by cluster and by rule segment."""
    if "emb_x" not in cust:
        return
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for a, col in zip(ax, ("cluster_name", "segment"), strict=True):
        for i, (nm, d) in enumerate(cust.groupby(col)):
            a.scatter(d["emb_x"], d["emb_y"], s=5, alpha=0.6, color=PAL[i % len(PAL)], label=nm)
        a.set_title(f"{method} of log-scaled RFM, coloured by {col}")
        a.legend(markerscale=3, fontsize=7)
        a.grid(False)
    _save(fig, figdir, "03_segment_embedding.png")


def fig_clv_calibration(cal: pd.DataFrame, figdir: Path) -> None:
    """Predicted vs actual holdout purchases by calibration frequency."""
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.plot(cal["freq"], cal["actual"], "o-", color=PAL[0], label="actual (holdout)")
    ax.plot(cal["freq"], cal["predicted"], "s--", color=PAL[1], label="BG/NBD predicted")
    ax.set_xlabel("repeat purchases in calibration (7 = 7+)")
    ax.set_ylabel("mean purchases in holdout (162 days)")
    ax.set_title("BG/NBD calibration plot")
    ax.legend()
    _save(fig, figdir, "04_clv_calibration.png")


def fig_clv_deciles(cust: pd.DataFrame, figdir: Path) -> None:
    """Actual holdout spend share by predicted-CLV decile."""
    d = cust.copy()
    g = d.groupby("clv_decile")["actual_spend"].sum()
    share = g / g.sum() * 100
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.bar(share.index, share.values, color=PAL[0])
    ax.set_xlabel("predicted 12-month CLV decile (10 = highest)")
    ax.set_ylabel("% of actual holdout spend")
    ax.set_title("Holdout spend concentration by predicted CLV decile")
    _save(fig, figdir, "05_clv_deciles.png")


def fig_bundles(b: pd.DataFrame, figdir: Path) -> None:
    """Top bundles by lift."""
    if b.empty:
        return
    fig, ax = plt.subplots(figsize=(9, 5.5))
    lab = [s if len(s) < 70 else s[:67] + "..." for s in b["bundle"]]
    ax.barh(lab[::-1], b["lift"].to_numpy()[::-1], color=PAL[0])
    ax.set_xlabel("lift")
    ax.set_title("Top 20 cross-sell bundles (FP-Growth, lift>3, confidence>0.3)")
    ax.tick_params(axis="y", labelsize=7)
    _save(fig, figdir, "06_top_bundles.png")


def fig_recsys(rs: dict, figdir: Path) -> None:
    """NDCG@10 and HitRate@10 by model and protocol."""
    models = ["popularity", "itemknn_cosine", "als", "hybrid_als_pop"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for a, met in zip(ax, ("ndcg", "hitrate"), strict=True):
        for j, prot in enumerate(("repeat_allowed", "discovery")):
            vals = [rs[prot][m][met] for m in models]
            a.bar(np.arange(len(models)) + (j - 0.5) * 0.38, vals, 0.38, color=PAL[j], label=prot)
        a.set_xticks(range(len(models)), models, rotation=15)
        a.set_title(f"{met.upper()}@10 (time-based test: last 30 days)")
    ax[0].legend()
    _save(fig, figdir, "07_recsys_metrics.png")


def fig_campaign(econ: pd.DataFrame, sens: pd.DataFrame, figdir: Path) -> None:
    """ROI by segment and sensitivity heat-map."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    e = econ.sort_values("roi")
    ax[0].barh(e["segment"], e["roi"], color=PAL[2])
    ax[0].set_xlabel("ROI (net profit / cost)")
    ax[0].set_title("Campaign ROI by segment (config assumptions)")
    pv = sens.pivot(index="gross_margin", columns="response_multiplier", values="roi")
    im = ax[1].imshow(pv.values, cmap="viridis", aspect="auto")
    ax[1].set_xticks(range(len(pv.columns)), [f"{c:g}x" for c in pv.columns])
    ax[1].set_yticks(range(len(pv.index)), [f"{i:.0%}" for i in pv.index])
    for (i, j), v in np.ndenumerate(pv.values):
        ax[1].text(j, i, f"{v:.1f}", ha="center", va="center", color="white", fontsize=8)
    ax[1].set_xlabel("response-rate multiplier")
    ax[1].set_ylabel("gross margin")
    ax[1].set_title("Portfolio ROI sensitivity")
    ax[1].grid(False)
    fig.colorbar(im, ax=ax[1])
    _save(fig, figdir, "08_campaign_roi.png")


def build_summary(m: dict, cfg: dict, cust: pd.DataFrame) -> dict:
    """Headline numbers + target checks, derived only from metrics.json / CSVs."""
    cl, cv, rs, cp = m["cluster"], m["clv"], m["recsys"], m["campaign"]
    prim = cfg["recsys"]["primary_protocol"]
    other = "discovery" if prim == "repeat_allowed" else "repeat_allowed"
    als_ratio = rs[prim]["als"]["ndcg_ratio_vs_popularity"]
    best_name = max(("als", "hybrid_als_pop"), key=lambda n: rs[prim][n]["ndcg"])
    seg = pd.DataFrame(m["rfm"]["segments"])
    s = {
        "segments": {r["segment"]: {"customers": r["customers"],
                                     "customer_share": r["customer_share"],
                                     "revenue_share": r["revenue_share"]} for _, r in seg.iterrows()},
        "silhouette_kmeans_final": cl["kmeans_silhouette_final"], "kmeans_k_final": cl["kmeans_k_final"],
        "silhouette_target": 0.35,
        "silhouette_target_met": bool(cl["kmeans_silhouette_final"] >= 0.35),
        "clv_mae_spend_model": cv["model"]["mae_spend"],
        "clv_mae_spend_baseline": cv["baseline_hist"]["mae_spend"],
        "clv_spearman_spend_model": cv["model"]["spearman_spend"],
        "clv_spearman_spend_baseline": cv["baseline_hist"]["spearman_spend"],
        "clv_top_decile_share_predicted_12m": cv["clv_12m_top_decile_share"],
        "clv_top_decile_share_of_actual_holdout_spend": cv["top_decile"]["share_of_actual_holdout_spend"],
        "n_bundles": m["basket"]["n_bundles"], "top_bundle_lift": m["basket"]["top_lift"],
        "recsys_primary_protocol": prim,
        "recsys_als_ndcg": rs[prim]["als"]["ndcg"], "recsys_popularity_ndcg": rs[prim]["popularity"]["ndcg"],
        "recsys_als_ndcg_ratio": als_ratio,
        "recsys_als_ndcg_ratio_ci95": rs[prim]["als"]["ndcg_ratio_ci95"],
        "recsys_target_ratio": 1.3, "recsys_target_met": bool(als_ratio >= 1.3),
        "recsys_secondary_protocol": other,
        "recsys_secondary_als_ndcg_ratio": rs[other]["als"]["ndcg_ratio_vs_popularity"],
        "recsys_best_model_primary": best_name,
        "campaign_funded_roi": cp["funded_roi"], "campaign_funded_net_profit_gbp": cp["funded_net_profit"],
        "campaign_unconstrained_roi": cp["unconstrained_roi"],
        "n_customers": len(cust), "runtime_seconds_pipeline": m.get("runtime_seconds"),
    }
    return s


def main() -> None:
    """Generate figures + summary.json."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--outputs")
    ap.add_argument("--figures")
    a = ap.parse_args()
    cfg = load_config()
    out = Path(a.outputs) if a.outputs else resolve(cfg, "outputs")
    figdir = Path(a.figures) if a.figures else resolve(cfg, "figures")
    figdir.mkdir(parents=True, exist_ok=True)
    if not (out / "metrics.json").exists():
        from crm.data import load_sales
        from crm.train import run_pipeline

        run_pipeline(load_sales(cfg), cfg, out, resolve(cfg, "models"))
    m = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    cust = pd.read_csv(out / "customers.csv")
    seg = pd.read_csv(out / "segment_summary.csv")
    fig_segments(seg, figdir)
    fig_cluster_selection(pd.read_csv(out / "kmeans_sweep.csv"), pd.read_csv(out / "gmm_sweep.csv"),
                          m["cluster"]["kmeans_k_final"], figdir)
    fig_embedding(cust, m["cluster"].get("embedding_method") or "2D", figdir)
    fig_clv_calibration(pd.read_csv(out / "clv_calibration.csv"), figdir)
    fig_clv_deciles(cust, figdir)
    fig_bundles(pd.read_csv(out / "bundles.csv"), figdir)
    fig_recsys(m["recsys"], figdir)
    fig_campaign(pd.read_csv(out / "campaign_economics.csv"), pd.read_csv(out / "campaign_sensitivity.csv"),
                 figdir)
    summary = build_summary(m, cfg, cust)
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    if not a.outputs:                       # default run: also refresh number-bearing docs
        import render_docs

        render_docs.main(out, ROOT)
    log.info("wrote %s and figures in %s", out / "summary.json", figdir)


if __name__ == "__main__":
    main()
