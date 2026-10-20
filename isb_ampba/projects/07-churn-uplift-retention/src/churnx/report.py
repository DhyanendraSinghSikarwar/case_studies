"""Stage 3: threshold, pilot, uplift, policy, survival, Hillstrom -> figures, outputs/summary.json."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from churnx import plots
from churnx.config import ROOT, get_logger, load_config, resolve, set_seed
from churnx.data import load_hillstrom, load_transactions
from churnx.docgen import render_docs
from churnx.hillstrom import balance_table, run_hillstrom
from churnx.pilot import ate_check, build_pilot, uplift_feature_matrix
from churnx.policy import policy_table, segment_breakdown, segment_labels, select_policies, sensitivity_sweep
from churnx.snapshot import clean_sales, customer_value_inr
from churnx.survival import run_survival, time_to_next_purchase
from churnx.threshold import expected_profit, sensitivity_table, threshold_report
from churnx.train import write_json
from churnx.uplift import (
    MetaLearner,
    auuc,
    bootstrap_ci,
    cv_qini,
    qini_auc,
    qini_curve,
    tau_recovery,
    uplift_at_k,
)

log = get_logger(__name__)


def evaluate_uplift(pilot: dict[str, pd.DataFrame], p_churn: np.ndarray, cfg: dict[str, Any]) -> dict[str, Any]:
    """Select a learner by grouped-CV Qini on the training pilot, fit all learners, evaluate on the test cohort."""
    ucfg, seed = cfg["uplift"], cfg["seed"]
    ptr, pte = pilot["train"], pilot["test"]
    Xtr, Xte = uplift_feature_matrix(ptr), uplift_feature_matrix(pte)
    cvq = {L: cv_qini(Xtr, ptr["w"], ptr["retained"], ptr["customer_id"], L, ucfg["base"], seed, ucfg["cv_folds"])
           for L in ucfg["learners"]}
    selected = max(cvq, key=cvq.get)
    y, w = pte["retained"].to_numpy(float), pte["w"].to_numpy()
    tau_hat, rows = {}, {}
    k = ucfg["uplift_at_k"]
    scorers = {}
    for L in ucfg["learners"]:
        m = MetaLearner(L, "binary", ucfg["base"], seed).fit(Xtr, ptr["w"], ptr["retained"])
        tau_hat[L] = m.predict(Xte)
        scorers[L] = tau_hat[L]
    rnd = np.random.default_rng(seed).random(len(pte))
    scorers.update({"oracle": pte["tau_true"].to_numpy(), "random": rnd, "risk_only": np.asarray(p_churn)})
    oracle_q = qini_auc(y, w, scorers["oracle"])
    for name, s in scorers.items():
        lo, hi = bootstrap_ci(lambda idx, s=s: qini_auc(y[idx], w[idx], s[idx]), len(y), ucfg["n_boot"], seed)
        rows[name] = {"qini": qini_auc(y, w, s), "qini_ci95": [lo, hi], "qini_pct_of_oracle": 100 * qini_auc(y, w, s) / oracle_q,
                      "auuc": auuc(y, w, s), f"uplift_at_{int(k * 100)}": uplift_at_k(y, w, s, k)}
        if name in tau_hat:
            rows[name]["tau_recovery"] = tau_recovery(tau_hat[name], pte["tau_true"])
            rows[name]["cv_qini_train"] = cvq[name]
    return {"cv_qini": cvq, "selected_learner": selected, "learners": rows, "tau_hat": tau_hat,
            "curves": {n: qini_curve(y, w, s) for n, s in scorers.items()}}


def run(cfg: dict[str, Any], tx: pd.DataFrame, root: Path | None = None, hillstrom: pd.DataFrame | None = None,
        make_figures: bool = True) -> dict[str, Any]:
    """Run the whole analysis stage and write outputs/summary.json (returns the summary dict)."""
    t0 = time.time()
    root = root or ROOT
    set_seed(cfg["seed"])
    proc, outs, figs = (resolve(cfg, k, root) for k in ("processed", "outputs", "figures"))
    seed, biz, budget = cfg["seed"], cfg["business"], cfg["policy"]["budget_frac"]
    snaps = pd.read_parquet(proc / "snapshots.parquet")
    scores = pd.read_parquet(proc / "test_scores.parquet")
    metrics = json.loads((outs / "metrics.json").read_text(encoding="utf-8"))["churn"]
    sales, returns = clean_sales(tx)
    te = snaps[snaps["split"] == "test"].sort_values("customer_id").reset_index(drop=True)
    scores = scores.set_index("customer_id").loc[te["customer_id"]].reset_index()
    p_cal = scores["p_champion_cal"].to_numpy()

    # ---- cost-optimal threshold (risk-only, constant save-rate) --------------------------------------------
    thr = threshold_report(p_cal, te["monetary_6m"].to_numpy(), biz, cfg["models"]["threshold_grid_max"])
    thr["sweep"].to_csv(outs / "threshold_sweep.csv", index=False)
    thr_sens = sensitivity_table(p_cal, te["monetary_6m"].to_numpy(), biz, cfg["sensitivity"]["save_rate"],
                                 cfg["sensitivity"]["offer_cost_inr"])
    thr_sens.to_csv(outs / "threshold_sensitivity.csv", index=False)
    summary: dict[str, Any] = {"seed": seed, "assumptions": cfg["business"],
                               "threshold": {"best": thr["best"], "profit_contact_all_inr": thr["profit_contact_all_inr"],
                                             "profit_contact_nobody_inr": 0.0, "n_customers": thr["n_customers"],
                                             "note": "expected profit under the constant save_rate assumption",
                                             "sensitivity": thr_sens.to_dict("records")}}

    # ---- pilot + uplift --------------------------------------------------------------------------------------
    pilot = build_pilot(snaps, p_cal, cfg)
    pte = pilot["test"]
    assert (pte["customer_id"].to_numpy() == te["customer_id"].to_numpy()).all()
    up = evaluate_uplift(pilot, p_cal, cfg)
    sel = up["selected_learner"]
    tau_hat = up["tau_hat"][sel]
    summary["pilot"] = {"train": ate_check(pilot["train"]), "test": ate_check(pte), "pattern": cfg["pilot"]["pattern"],
                        "n_train_cohort": int(len(pilot["train"])), "n_test_cohort": int(len(pte)),
                        "synthetic_note": "treatment effect is SIMULATED; baseline churn labels are real"}
    summary["uplift"] = {"selected_learner": sel, "selection_rule": "highest grouped-CV Qini on the training pilot",
                         "cv_qini_train": up["cv_qini"], "learners": up["learners"]}

    # ---- policies ----------------------------------------------------------------------------------------------
    value = customer_value_inr(te["monetary_6m"], biz)
    cost = biz["offer_cost_inr"]
    tau_true = pte["tau_true"].to_numpy()
    masks = select_policies(tau_hat, p_cal, value, budget, cost, seed)
    ptab = policy_table(masks, tau_true, value, cost)
    # M2 threshold rule evaluated against the TRUE effect (risk-only, constant save rate)
    thr_mask = expected_profit(p_cal, value, cost, biz["save_rate"]) > 0
    ptab = pd.concat([ptab, policy_table({"risk_threshold_m2": thr_mask}, tau_true, value, cost).iloc[[0]]], ignore_index=True)
    k = int(round(budget * len(te)))
    rand_exp = float(k * np.mean(tau_true * value - cost))
    ptab.to_csv(outs / "policy_table.csv", index=False)
    per_learner = {}
    for L, th in up["tau_hat"].items():
        mk = select_policies(th, p_cal, value, budget, cost, seed)
        t = policy_table(mk, tau_true, value, cost).set_index("policy")
        per_learner[L] = {"uplift_top_k_pct_oracle": float(t.loc["uplift_top_k", "pct_of_oracle"]),
                          "profit_optimal_pct_oracle": float(t.loc["profit_optimal", "pct_of_oracle"]),
                          "profit_optimal_inr": float(t.loc["profit_optimal", "profit_inr"])}
    pt = ptab.set_index("policy")
    seg = segment_breakdown(pte, masks["risk_top_k"], tau_true, value, cost)
    seg.to_csv(outs / "risk_policy_segments.csv", index=False)
    seg_uplift = segment_breakdown(pte, masks["profit_optimal"], tau_true, value, cost)
    summary["policy"] = {
        "budget_frac": budget, "offer_cost_inr": cost, "table": ptab.to_dict("records"),
        "oracle_profit_inr": float(pt.loc["oracle", "profit_inr"]),
        "uplift_policy": "profit_optimal", "uplift_policy_pct_of_oracle": float(pt.loc["profit_optimal", "pct_of_oracle"]),
        "uplift_top_k_pct_of_oracle": float(pt.loc["uplift_top_k", "pct_of_oracle"]),
        "risk_top_k_pct_of_oracle": float(pt.loc["risk_top_k", "pct_of_oracle"]),
        "random_expected_profit_inr": rand_exp, "per_learner": per_learner,
        "ordering_uplift_gt_risk_gt_random": bool(pt.loc["profit_optimal", "profit_inr"] > pt.loc["risk_top_k", "profit_inr"]
                                                  > pt.loc["random", "profit_inr"]),
        "segments_risk_top_k": seg.to_dict("records"), "segments_profit_optimal": seg_uplift.to_dict("records")}

    # sensitivity: economics (cost x margin x CLV horizon), constant masks recomputed per cell
    sens = sensitivity_sweep(pte, tau_hat, p_cal, te["monetary_6m"], biz, budget, seed, cfg["sensitivity"])
    sens.to_csv(outs / "policy_sensitivity.csv", index=False)
    cells = sens[sens["policy"] == "risk_top_k"]
    neg = cells[cells["profit_inr"] < 0]
    base_neg = neg[(neg["gross_margin"] == biz["gross_margin"]) & (neg["clv_months"] == biz["clv_months"])]
    po_all = sens[sens["policy"] == "profit_optimal"]
    thr_cells = sens[sens["policy"] == "risk_threshold_m2"]
    base_cells = sens[(sens["gross_margin"] == biz["gross_margin"]) & (sens["clv_months"] == biz["clv_months"])]
    by_cost = {}
    for c, d in base_cells.groupby("offer_cost_inr"):
        d = d.set_index("policy")
        by_cost[str(c)] = {p: {"profit_inr": float(d.loc[p, "profit_inr"]), "pct_of_oracle": float(d.loc[p, "pct_of_oracle"])}
                           for p in d.index}
    key = ["offer_cost_inr", "gross_margin", "clv_months"]
    po = sens[sens["policy"] == "profit_optimal"].set_index(key)["profit_inr"]
    summary["policy"]["sensitivity"] = {
        "n_cells": int(len(cells)), "n_cells_risk_top_k_negative": int(len(neg)),
        "min_cost_where_risk_top_k_negative": float(neg["offer_cost_inr"].min()) if len(neg) else None,
        "min_cost_where_risk_top_k_negative_at_base_margin_clv": (
            float(base_neg["offer_cost_inr"].min()) if len(base_neg) else None),
        "n_cells_profit_optimal_negative": int((po_all["profit_inr"] < 0).sum()),
        "n_cells_risk_threshold_m2_negative": int((thr_cells["profit_inr"] < 0).sum()),
        "n_cells_all_negative": int((sens[sens["policy"] == "all"]["profit_inr"] < 0).sum()),
        "base_margin_clv_by_offer_cost": by_cost,
        "n_cells_profit_optimal_beats_risk": int((po > cells.set_index(key)["profit_inr"].reindex(po.index)).sum())}

    # sensitivity: different true response pattern (response bump on HIGH frequency)
    alt_cfg = {**cfg, "pilot": {**cfg["pilot"], "pattern": "high_freq"}}
    pilot_alt = build_pilot(snaps, p_cal, alt_cfg)
    up_alt = evaluate_uplift(pilot_alt, p_cal, alt_cfg)
    pte_a = pilot_alt["test"]
    mk_alt = select_policies(up_alt["tau_hat"][up_alt["selected_learner"]], p_cal, value, budget, cost, seed)
    alt_tab = policy_table(mk_alt, pte_a["tau_true"].to_numpy(), value, cost)
    alt_tab.to_csv(outs / "policy_table_high_freq_pattern.csv", index=False)
    summary["policy"]["alt_response_pattern_high_freq"] = {
        "selected_learner": up_alt["selected_learner"], "table": alt_tab.to_dict("records"),
        "qini_selected": up_alt["learners"][up_alt["selected_learner"]]["qini"]}

    # ---- cohort csv for the app ---------------------------------------------------------------------------------
    cohort = te[["customer_id", "recency_days", "frequency_6m", "monetary_6m", "aov_6m", "churn"]].copy()
    cohort["p_churn"] = p_cal
    cohort["value_inr"] = value
    cohort["segment"] = segment_labels(pte).to_numpy()
    for L, th in up["tau_hat"].items():
        cohort[f"tau_hat_{L}"] = th
    cohort["tau_hat"] = tau_hat
    cohort["tau_true"] = tau_true
    cohort["w"], cohort["retained"] = pte["w"].to_numpy(), pte["retained"].to_numpy()
    cohort.to_csv(outs / "test_cohort.csv", index=False)
    pd.DataFrame({n: pd.Series(q, index=nn) for n, (nn, q) in up["curves"].items()}).iloc[::10].to_csv(outs / "qini_curves.csv")

    # ---- survival (optional) --------------------------------------------------------------------------------------
    surv = None
    if cfg["survival"]["enabled"]:
        out = run_survival(time_to_next_purchase(sales, te, cfg["snapshots"]["test"], cfg["snapshots"]["horizon_days"]))
        if out is not None:
            surv, km = out
            km.to_csv(outs / "km_curves.csv", index=False)
            if make_figures:
                plots.km_plot(km, figs / "13_km_time_to_next_purchase.png")
    summary["survival"] = surv if surv else {"skipped": "lifelines not installed or disabled"}

    # ---- Hillstrom (Track B, real RCT) ------------------------------------------------------------------------------
    if hillstrom is None:
        hillstrom = load_hillstrom(cfg, root)
    if hillstrom is not None:
        hres, hx = run_hillstrom(hillstrom, cfg)
        bal = balance_table(hillstrom)
        bal.to_csv(outs / "hillstrom_balance.csv", index=False)
        hres["max_abs_std_diff"] = float(bal["std_diff"].abs().max())
        summary["hillstrom"] = hres
        if make_figures:
            for o in ("visit", "conversion", "spend"):
                plots.hillstrom_qini(hx["qini_curves"][o], figs / f"12_hillstrom_qini_{o}.png", o)
        pd.DataFrame(hres["policies"]).T.to_csv(outs / "hillstrom_policy_ipw.csv")
    else:
        summary["hillstrom"] = {"skipped": "Hillstrom data unavailable (offline)"}

    # ---- figures ------------------------------------------------------------------------------------------------------
    if make_figures:
        plots.threshold_profit(thr["sweep"], thr["best"], figs / "06_threshold_profit.png")
        q_curves = {L: up["curves"][L] for L in cfg["uplift"]["learners"]}
        q_curves.update({"oracle": up["curves"]["oracle"], "risk": up["curves"]["risk_only"]})
        plots.qini_plot(q_curves, figs / "07_qini_pilot.png", "Qini curves, simulated pilot (test cohort)")
        plots.tau_scatter(tau_hat, tau_true, figs / "08_tau_recovery.png", sel)
        plots.policy_bars(ptab, figs / "09_policy_profit.png", f"Incremental profit by policy (offer cost INR {cost:,.0f})")
        plots.segment_bar(seg, figs / "10_risk_policy_by_segment.png")
        plots.sensitivity_heatmap(sens, "all", figs / "11_policy_sensitivity.png", biz["gross_margin"], biz["clv_months"])

    # ---- targets --------------------------------------------------------------------------------------------------------
    auc = metrics["models"][metrics["champion"]]["auc"]
    summary["churn"] = {"champion": metrics["champion"], "test_auc": auc,
                        "test_auc_calibrated": metrics["models"]["champion_calibrated"]["auc"],
                        "models_test_auc": {m: v["auc"] for m, v in metrics["models"].items() if "auc" in v},
                        "baseline_auc": 0.5, "calibration_gap_test": metrics["calibration_gap_test"]}
    sel_q = up["learners"][sel]["qini"]
    summary["targets"] = {
        "churn_auc_ge_0.75": {"target": 0.75, "achieved": auc, "pass": bool(auc >= 0.75)},
        "qini_gt_0_selected_learner": {"achieved": sel_q, "pass": bool(sel_q > 0)},
        "uplift_policy_ge_70pct_oracle": {"target": 70.0, "achieved": summary["policy"]["uplift_policy_pct_of_oracle"],
                                          "pass": bool(summary["policy"]["uplift_policy_pct_of_oracle"] >= 70.0)},
        "uplift_gt_risk_gt_random": {"pass": summary["policy"]["ordering_uplift_gt_risk_gt_random"]},
        "features_before_asof": {"pass": True, "note": "enforced by tests/test_snapshot.py::test_features_before_asof"}}
    summary["runtime_seconds_analysis"] = round(time.time() - t0, 1)
    write_json(summary, outs / "summary.json")
    # merge churn metrics + uplift/policy into metrics.json
    write_json({"churn": metrics, "uplift": summary["uplift"], "policy": {k: v for k, v in summary["policy"].items()
                                                                         if k in ("table", "uplift_policy_pct_of_oracle")}},
               outs / "metrics.json")
    render_docs(root, summary, metrics)
    log.info("analysis done in %.1fs", time.time() - t0)
    return summary


def main() -> None:
    """CLI entry point (``python analysis/run_analysis.py`` or ``python -m churnx.report``)."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    a = ap.parse_args()
    cfg = load_config(a.config)
    run(cfg, load_transactions(cfg))


if __name__ == "__main__":
    main()
