"""Regenerate every figure, CSV and outputs/summary.json from trained models + test predictions.

Run after `python -m credit.train`:  python analysis/run_analysis.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import joblib  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import roc_curve  # noqa: E402

from credit import economics as eco  # noqa: E402
from credit import evaluate as ev  # noqa: E402
from credit import explain, fairness, monitor  # noqa: E402
from credit import scorecard as sc  # noqa: E402
from credit.config import get_logger, load_config  # noqa: E402
from credit.data import TARGET, build_splits, load_raw  # noqa: E402
from credit.features import add_features  # noqa: E402
from credit.models import predict_pd  # noqa: E402
from credit.validate import validate_raw  # noqa: E402

log = get_logger("analysis")
CFG = load_config()
OUT, FIG = ROOT / CFG["paths"]["outputs"], ROOT / CFG["paths"]["figures"]
COL = {"main": "#1f4e79", "alt": "#c0504d", "grey": "#7f7f7f", "ok": "#2e8b57"}
plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10})


def save(fig: plt.Figure, name: str) -> None:
    """Save a figure to figures/ and close it."""
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=130)
    plt.close(fig)


def eda_figures(train: pd.DataFrame) -> None:
    """Six EDA figures on the TRAIN split."""
    rate = train[TARGET].mean()

    def bar(series_x, name, title, xlabel, rot=0):
        g = train.groupby(series_x, observed=True)[TARGET].agg(["mean", "size"])
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(g.index.astype(str), g["mean"], color=COL["main"])
        ax.axhline(rate, color=COL["alt"], ls="--", label=f"overall {rate:.1%}")
        ax.set(title=title, xlabel=xlabel, ylabel="default rate")
        ax.tick_params(axis="x", rotation=rot)
        ax.legend()
        save(fig, name)

    bar("PAY_0", "eda_default_by_pay0.png", "Default rate by latest repayment status (PAY_0)", "PAY_0")
    bar(pd.qcut(train["LIMIT_BAL"], 10, duplicates="drop"), "eda_default_by_limit_decile.png",
        "Default rate by LIMIT_BAL decile", "LIMIT_BAL decile (NT$)", rot=60)
    bar("EDUCATION", "eda_default_by_education.png", "Default rate by EDUCATION (1 grad, 2 univ, 3 HS, 4 other)",
        "EDUCATION")
    f = add_features(train)
    cols = ["default", "LIMIT_BAL", "AGE", "PAY_0", "PAY_2", "max_delay", "n_months_delayed", "avg_util",
            "util_volatility", "avg_pay_ratio", "delay_trend", "bill_growth"]
    cm = f[cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6.5))
    im = ax.imshow(cm, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)), cols, rotation=70, ha="right")
    ax.set_yticks(range(len(cols)), cols)
    fig.colorbar(im)
    ax.set_title("Correlation heat-map (train)")
    save(fig, "eda_correlation_heatmap.png")
    fig, ax = plt.subplots(figsize=(7, 4))
    for v, lab, c in [(0, "no default", COL["main"]), (1, "default", COL["alt"])]:
        ax.hist(f.loc[f[TARGET] == v, "avg_util"].clip(-0.2, 1.5), bins=40, alpha=0.6, density=True, label=lab, color=c)
    ax.set(title="Average utilisation by outcome", xlabel="avg_util (bill / limit)", ylabel="density")
    ax.legend()
    save(fig, "eda_avg_util_by_outcome.png")
    g = f.groupby("n_months_delayed")[TARGET].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(g.index.astype(str), g.values, color=COL["main"])
    ax.axhline(rate, color=COL["alt"], ls="--")
    ax.set(title="Default rate by number of months delayed (of 6)", xlabel="months delayed", ylabel="default rate")
    save(fig, "eda_default_by_months_delayed.png")


def model_figures(pred: pd.DataFrame, metrics: dict, curve: pd.DataFrame, opt: pd.Series, sens: pd.DataFrame,
                  imp: pd.DataFrame, band_t: pd.DataFrame) -> None:
    """ROC, calibration, lift, score distribution, profit curve, sensitivity heat-map, SHAP bar, bands."""
    y = pred["y"].to_numpy()
    labels = {"logit_raw": "Baseline logit (raw)", "scorecard": "WOE scorecard", "xgb": "XGBoost", "lgbm": "LightGBM"}
    fig, ax = plt.subplots(figsize=(5.5, 5))
    for k, lab in labels.items():
        fpr, tpr, _ = roc_curve(y, pred[f"pd_{k}"])
        ax.plot(fpr, tpr, label=f"{lab} (AUC {metrics[k]['test']['auc']:.3f})")
    ax.plot([0, 1], [0, 1], "k:", label="naive (0.500)")
    ax.set(title="ROC - test set", xlabel="false positive rate", ylabel="true positive rate")
    ax.legend(fontsize=8)
    save(fig, "roc_test.png")

    fig, ax = plt.subplots(figsize=(5.5, 5))
    for k, c in [("scorecard", COL["grey"]), ("champion", COL["main"])]:
        p = pred["pd"] if k == "champion" else pred[f"pd_{k}"]
        t = ev.calibration_table(y, p)
        ax.plot(t["mean_pred"], t["obs_rate"], "o-", color=c, label=k)
    ax.plot([0, 0.8], [0, 0.8], "k:")
    ax.set(title="Calibration (test deciles)", xlabel="mean predicted PD", ylabel="observed default rate")
    ax.legend()
    save(fig, "calibration_test.png")

    d = ev.decile_table(y, pred["pd"])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(d["decile"].astype(str), d["bad_rate"], color=COL["main"])
    ax.axhline(y.mean(), color=COL["alt"], ls="--", label="portfolio bad rate")
    ax.set(title="Bad rate by risk decile (1 = riskiest)", xlabel="decile", ylabel="bad rate")
    ax.legend()
    save(fig, "lift_deciles.png")

    fig, ax = plt.subplots(figsize=(7, 4))
    for v, lab, c in [(0, "no default", COL["main"]), (1, "default", COL["alt"])]:
        ax.hist(pred.loc[pred["y"] == v, "score"], bins=40, alpha=0.6, density=True, label=lab, color=c)
    ax.set(title="Score distribution by outcome (test)", xlabel="score (300-900, higher = safer)", ylabel="density")
    ax.legend()
    save(fig, "score_distribution.png")

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(curve["cutoff"], curve["exp_profit"] / 1e6, color=COL["main"], label="expected profit (model PD)")
    ax.plot(curve["cutoff"], curve["real_profit"] / 1e6, color=COL["ok"], label="realised profit (actual y)")
    ax.axvline(opt["cutoff"], color=COL["alt"], ls="--", label=f"optimal cut-off {opt['cutoff']:.2f}")
    ax.set(title="Profit vs PD cut-off (test, INR mn)", xlabel="approve if PD <= cut-off", ylabel="profit (INR mn)")
    ax.legend(fontsize=8)
    save(fig, "profit_curve.png")

    pv = sens.pivot(index="lgd", columns="margin", values="uplift") / 1e6
    fig, ax = plt.subplots(figsize=(6, 4.5))
    im = ax.imshow(pv.values, cmap="YlGn", origin="lower", aspect="auto")
    ax.set_xticks(range(len(pv.columns)), [f"{c:.2f}" for c in pv.columns])
    ax.set_yticks(range(len(pv.index)), [f"{c:.2f}" for c in pv.index])
    for i in range(pv.shape[0]):
        for j in range(pv.shape[1]):
            ax.text(j, i, f"{pv.values[i, j]:.1f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, label="uplift vs approve-all (INR mn)")
    ax.set(title="Profit uplift: LGD x margin", xlabel="margin", ylabel="LGD")
    save(fig, "sensitivity_heatmap.png")

    top = imp.head(15).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(top["feature"], top["mean_abs_shap"], color=COL["main"])
    ax.set(title="SHAP global importance (champion, 1,000 test rows)", xlabel="mean |SHAP| (log-odds)")
    save(fig, "shap_global_bar.png")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(band_t["band"], band_t["bad_rate"], color=COL["main"])
    for i, r in band_t.iterrows():
        ax.text(i, r["bad_rate"], f"{r['share']:.0%} of book", ha="center", va="bottom", fontsize=8)
    ax.set(title="Bad rate by risk band (test)", xlabel="band (A safest)", ylabel="observed bad rate")
    save(fig, "band_bad_rate.png")


def main() -> None:
    """Build all analysis artefacts."""
    FIG.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    metrics = json.load(open(OUT / "metrics.json", encoding="utf-8"))
    pred = pd.read_csv(OUT / "test_predictions.csv", index_col="row_id")
    scfg, ecfg = CFG["scorecard"], CFG["economics"]
    champion = metrics["champion"]

    dq = validate_raw(load_raw(CFG), CFG["data"]["expected_rows"])
    json.dump(dq, open(OUT / "data_quality.json", "w", encoding="utf-8"), indent=2)
    train_raw, valid_raw, test_raw = build_splits(CFG, save=False)
    eda_figures(train_raw)

    fx, margin, lgd = ecfg["fx_ntd_inr"], ecfg["margin"], ecfg["lgd"]
    ead = eco.make_ead(pred["LIMIT_BAL"], pred["avg_util"], fx)
    y, p = pred["y"].to_numpy(), pred["pd"].to_numpy()
    grid = eco.cutoff_grid(CFG)
    curve = eco.profit_curve(p, ead, y, margin, lgd, grid)
    opt = eco.find_optimal_cutoff(curve)
    curve.to_csv(OUT / "profit_curve.csv", index=False)
    approve_all_exp = float(eco.unit_profit(p, ead, margin, lgd).sum())
    approve_all_real = float(eco.realised_profit(y, ead, margin, lgd).sum())
    sens = eco.sensitivity_grid(p, ead, y, ecfg["sensitivity"]["lgd"], ecfg["sensitivity"]["margin"], grid)
    sens.to_csv(OUT / "sensitivity_lgd_margin.csv", index=False)
    breakeven_pd = margin / (margin + lgd)

    band_t = sc.band_table(p, y, pred["score"], scfg["band_pd_edges"])
    band_t.to_csv(OUT / "band_table.csv", index=False)
    limit_v = eco.limit_engine_value(pred["band"], p, ead, margin, lgd, CFG["limits"])
    limit_v.to_csv(OUT / "limit_engine_value.csv", index=False)
    ev.decile_table(y, p).to_csv(OUT / "decile_table.csv", index=False)
    ev.calibration_table(y, p).to_csv(OUT / "calibration_table.csv", index=False)

    # fairness at the optimal cut-off
    approved = p <= opt["cutoff"]
    rep_sex = fairness.disparate_impact(fairness.group_report(y, p, approved, pred["SEX"].map({1: "male", 2: "female"})),
                                        CFG["fairness"]["di_threshold"])
    rep_age = fairness.disparate_impact(fairness.group_report(y, p, approved, fairness.age_bucket(pred["AGE"], CFG).to_numpy()),
                                        CFG["fairness"]["di_threshold"])
    rep_sex.to_csv(OUT / "fairness_sex.csv", index=False)
    rep_age.to_csv(OUT / "fairness_age.csv", index=False)

    # SHAP + reason codes (champion raw tree model)
    bundle = joblib.load(ROOT / CFG["paths"]["models"] / f"{champion}.joblib")
    model, calib, cols = bundle["model"], bundle["calibrator"], bundle["features"]
    te_f = add_features(test_raw)
    samp = te_f.sample(1000, random_state=CFG["seed"])
    sv = explain.shap_values(model, samp[cols])
    imp = explain.global_importance(sv, cols)
    imp.to_csv(OUT / "shap_importance.csv", index=False)
    risky = np.argsort(-model.predict_proba(samp[cols])[:, 1])[:8]
    rc = pd.DataFrame([{"row_id": samp.index[i], "pd": float(predict_pd(model, samp[cols].iloc[[i]], calib)[0]),
                        "reasons": " | ".join(explain.reason_codes(samp.iloc[i], sv[i], cols))} for i in risky])
    rc.to_csv(OUT / "reason_code_samples.csv", index=False)

    # monitoring
    tr_f = add_features(train_raw)
    csi_clean = monitor.csi_table(tr_f, te_f, cols, CFG["monitoring"]["psi_alert"])
    csi_clean.to_csv(OUT / "csi_test_vs_train.csv", index=False)
    shifted = monitor.simulate_limit_shift(test_raw, CFG["monitoring"]["drift_limit_shift"])
    csi_drift = monitor.csi_table(tr_f, shifted, cols, CFG["monitoring"]["psi_alert"])
    pd_tr = predict_pd(model, tr_f[cols], calib)
    pd_clean = predict_pd(model, te_f[cols], calib)
    pd_shift = predict_pd(model, shifted[cols], calib)
    score_psi_clean, score_psi_shift = ev.psi(pd_tr, pd_clean), ev.psi(pd_tr, pd_shift)
    csi_drift.to_csv(OUT / "csi_drift_sim.csv", index=False)

    model_figures(pred, metrics, curve, opt, sens, imp, band_t)

    n = len(pred)
    f = metrics[champion]["test"]
    di_sex = float(rep_sex["di_ratio"].min())
    di_age = float(rep_age["di_ratio"].min())
    summary = {
        "n_test": n, "champion": champion, "data": dq, "sizes": metrics["sizes"],
        "auc_test": f["auc"], "gini_test": f["gini"], "ks_test": f["ks"], "brier_test": f["brier"],
        "cal_slope_test": f["cal_slope"],
        "auc_logit_raw": metrics["logit_raw"]["test"]["auc"], "auc_scorecard": metrics["scorecard"]["test"]["auc"],
        "ks_scorecard": metrics["scorecard"]["test"]["ks"],
        "auc_naive": 0.5, "brier_naive": metrics["naive_base_rate"]["test"]["brier"],
        "benchmark_r1": {"auc": 0.783, "ks": 0.424},
        "scorecard_max_point_diff": metrics["scorecard_check"]["max_abs_diff_points"],
        "assumptions": {"margin": margin, "lgd": lgd, "fx_ntd_inr": fx, "breakeven_pd": breakeven_pd},
        "opt_cutoff": float(opt["cutoff"]), "opt_cutoff_score": float(sc.pd_to_score(opt["cutoff"], scfg["base_score"], scfg["base_odds"], scfg["pdo"],
                                                 tuple(scfg["clip"]))),
        "approval_rate": float(opt["approval_rate"]), "bad_rate_approved": float(opt["bad_rate_approved"]),
        "bad_rate_all": float(y.mean()),
        "profit_opt_inr": float(opt["exp_profit"]), "profit_approve_all_inr": approve_all_exp,
        "uplift_inr": float(opt["exp_profit"] - approve_all_exp),
        "uplift_per_1000_inr": float((opt["exp_profit"] - approve_all_exp) / n * 1000),
        "profit_opt_per_1000_inr": float(opt["exp_profit"] / n * 1000),
        "real_profit_opt_inr": float(opt["real_profit"]), "real_profit_approve_all_inr": approve_all_real,
        "real_uplift_inr": float(opt["real_profit"] - approve_all_real),
        "sens_cutoff_min": float(sens["opt_cutoff"].min()), "sens_cutoff_max": float(sens["opt_cutoff"].max()),
        "sens_uplift_min_inr": float(sens["uplift"].min()), "sens_uplift_max_inr": float(sens["uplift"].max()),
        "sens_uplift_all_positive": bool((sens["uplift"] > 0).all()),
        "limit_engine_total_delta_inr": float(limit_v["delta"].sum()),
        "fairness_di_min_sex": di_sex, "fairness_di_min_age": di_age,
        "fairness_di_pass_sex": bool(rep_sex["passes_80pct"].all()), "fairness_di_pass_age": bool(rep_age["passes_80pct"].all()),
        "psi_limit_drift": float(csi_drift.set_index("feature").loc["LIMIT_BAL", "psi"]),
        "psi_max_no_drift": float(csi_clean["psi"].max()),
        "score_psi_no_drift": score_psi_clean, "score_psi_limit_drift": score_psi_shift,
        "score_drift_alert": monitor.score_drift_alert(score_psi_shift, CFG["monitoring"]["psi_alert"]),
        "top_shap_features": imp["feature"].head(5).tolist(),
        "bands": band_t.to_dict(orient="records"),
        "targets": {"auc": [0.78, f["auc"] >= 0.78], "ks": [0.42, f["ks"] >= 0.42], "gini": [0.56, f["gini"] >= 0.56],
                    "brier": [0.14, f["brier"] <= 0.14], "cal_slope": [[0.9, 1.1], 0.9 <= f["cal_slope"] <= 1.1],
                    "points_table_within_1pt": metrics["scorecard_check"]["max_abs_diff_points"] <= 1.0},
    }
    with open(OUT / "summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=float)
    log.info("summary.json written; opt cutoff %.2f, uplift INR %.0f", opt["cutoff"], summary["uplift_inr"])


if __name__ == "__main__":
    main()
