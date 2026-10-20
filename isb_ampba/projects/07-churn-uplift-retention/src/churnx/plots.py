"""Matplotlib figures (saved to figures/). Headless backend; one function per figure."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

plt.rcParams.update({"figure.dpi": 110, "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False,
                     "axes.spines.right": False})


def _save(fig, path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path.name


def churn_rate_by_snapshot(snaps: pd.DataFrame, path: Path) -> str:
    """Bar chart of eligible customers and churn rate per snapshot (shows seasonal drift)."""
    t = snaps.groupby(["asof", "split"]).agg(n=("churn", "size"), rate=("churn", "mean")).reset_index()
    fig, ax = plt.subplots(figsize=(7, 3.6))
    colors = {"pilot_hist": "#9aa5b1", "train": "#2f6fb0", "test": "#d9534f"}
    ax.bar(t["asof"].dt.strftime("%Y-%m"), t["rate"], color=[colors[s] for s in t["split"]])
    for i, (r, n) in enumerate(zip(t["rate"], t["n"])):
        ax.text(i, r + 0.01, f"{r:.0%}\nn={n}", ha="center", fontsize=7)
    ax.set_ylabel("90-day churn rate")
    ax.set_title("Churn rate by snapshot (grey=pilot history, blue=train, red=test)")
    ax.set_ylim(0, max(t["rate"]) * 1.25)
    return _save(fig, path)


def model_comparison(y: np.ndarray, probs: dict[str, np.ndarray], path: Path) -> str:
    """ROC curves of all models on the test snapshot."""
    from sklearn.metrics import roc_auc_score, roc_curve

    fig, ax = plt.subplots(figsize=(5, 4.2))
    for k, p in probs.items():
        fpr, tpr, _ = roc_curve(y, p)
        ax.plot(fpr, tpr, label=f"{k} (AUC {roc_auc_score(y, p):.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=0.8, label="baseline (0.5)")
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    ax.set_title("Test snapshot (2011-08-01) ROC")
    ax.legend(fontsize=7)
    return _save(fig, path)


def calibration_plot(cal_raw: pd.DataFrame, cal_cal: pd.DataFrame, path: Path) -> str:
    """Reliability diagram for the raw and calibrated champion on the test snapshot."""
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.plot([0, 1], [0, 1], "k--", lw=0.8)
    ax.plot(cal_raw["mean_pred"], cal_raw["frac_pos"], "o-", label="raw")
    ax.plot(cal_cal["mean_pred"], cal_cal["frac_pos"], "s-", label="isotonic (group-CV)")
    ax.set_xlabel("mean predicted churn")
    ax.set_ylabel("observed churn rate")
    ax.set_title("Calibration on test snapshot")
    ax.legend()
    return _save(fig, path)


def lift_chart(lift: pd.DataFrame, path: Path) -> str:
    """Decile lift and cumulative capture."""
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.bar(lift["decile"], lift["lift"], color="#2f6fb0")
    ax.axhline(1, color="k", lw=0.8)
    ax2 = ax.twinx()
    ax2.plot(lift["decile"], lift["cum_capture"], "o-", color="#d9534f")
    ax2.set_ylabel("cumulative churners captured")
    ax2.grid(False)
    ax.set_xlabel("risk decile (1 = highest predicted risk)")
    ax.set_ylabel("lift")
    ax.set_title("Lift by decile (test)")
    return _save(fig, path)


def shap_summary(sv: np.ndarray, X: pd.DataFrame, path: Path) -> str:
    """Beeswarm SHAP summary."""
    import shap

    fig = plt.figure(figsize=(7, 4.5))
    shap.summary_plot(sv, X, show=False, max_display=12)
    return _save(plt.gcf() if plt.get_fignums() else fig, path)


def threshold_profit(sweep: pd.DataFrame, best: dict, path: Path) -> str:
    """Expected profit vs contact threshold."""
    s = sweep[sweep["n_contacted"] > 0]
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(s["threshold"], s["profit_inr"] / 1e6, color="#2f6fb0")
    ax.axvline(best["threshold"], color="#d9534f", ls="--", label=f"best t={best['threshold']:.2f}")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("contact threshold on churn probability")
    ax.set_ylabel("expected profit (INR million)")
    ax.set_title("Cost-optimal threshold (constant save-rate assumption)")
    ax.legend()
    return _save(fig, path)


def qini_plot(curves: dict[str, tuple[np.ndarray, np.ndarray]], path: Path, title: str, annotate: dict | None = None) -> str:
    """Qini curves (cumulative incremental outcome vs customers targeted) with the random line."""
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    last = None
    for k, (n, q) in curves.items():
        ax.plot(n, q, label=k, lw=1.6 if k in {"oracle", "risk"} else 1.2, ls="--" if k in {"oracle", "risk"} else "-")
        last = (n, q)
    if last is not None and "random" not in curves:
        pass
    n_end = max(c[0][-1] for c in curves.values())
    q_end = float(np.mean([c[1][-1] for c in curves.values()]))
    ax.plot([0, n_end], [0, q_end], "k:", label="random targeting")
    ax.set_xlabel("customers targeted (top-k by score)")
    ax.set_ylabel("cumulative incremental outcome")
    ax.set_title(title)
    ax.legend(fontsize=7)
    return _save(fig, path)


def tau_scatter(tau_hat: np.ndarray, tau_true: np.ndarray, path: Path, label: str) -> str:
    """Estimated vs true tau on the pilot test cohort."""
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.scatter(tau_true, tau_hat, s=6, alpha=0.4)
    lim = [min(tau_true.min(), tau_hat.min()), max(tau_true.max(), tau_hat.max())]
    ax.plot(lim, lim, "k--", lw=0.8)
    ax.set_xlabel("true tau (simulator)")
    ax.set_ylabel(f"estimated tau ({label})")
    ax.set_title("Treatment-effect recovery")
    return _save(fig, path)


def policy_bars(table: pd.DataFrame, path: Path, title: str) -> str:
    """Profit by policy (INR million), red when negative."""
    fig, ax = plt.subplots(figsize=(7, 3.8))
    v = table["profit_inr"] / 1e6
    ax.bar(table["policy"], v, color=["#d9534f" if x < 0 else "#2f6fb0" for x in v])
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("incremental profit (INR million)")
    ax.set_title(title)
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    return _save(fig, path)


def sensitivity_heatmap(sens: pd.DataFrame, policy: str, path: Path, margin: float, months: int) -> str:
    """Policy profit (or %-of-oracle) across offer_cost for each policy at fixed margin/CLV horizon."""
    d = sens[(sens["gross_margin"] == margin) & (sens["clv_months"] == months)]
    piv = d.pivot(index="policy", columns="offer_cost_inr", values="profit_inr") / 1e6
    names = ["random", "all", "risk_top_k", "clv_top_k", "uplift_top_k", "profit_optimal", "oracle"]
    order = [p for p in names if p in piv.index]
    piv = piv.loc[order]
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    im = ax.imshow(piv.values, cmap="RdBu", vmin=-abs(piv.values).max(), vmax=abs(piv.values).max(), aspect="auto")
    ax.set_xticks(range(len(piv.columns)), [f"{c:,.0f}" for c in piv.columns])
    ax.set_yticks(range(len(piv.index)), piv.index)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            ax.text(j, i, f"{piv.values[i, j]:.2f}", ha="center", va="center", fontsize=7)
    ax.grid(False)
    ax.set_xlabel("offer cost (INR)")
    ax.set_title(f"Profit (INR m) by policy vs offer cost (margin {margin:.0%}, {months}m CLV)")
    fig.colorbar(im, ax=ax, fraction=0.03)
    return _save(fig, path)


def km_plot(curves: pd.DataFrame, path: Path) -> str:
    """Kaplan-Meier curves of time-to-next-purchase by recency tercile."""
    fig, ax = plt.subplots(figsize=(6, 3.8))
    for g, d in curves.groupby("group"):
        ax.step(d["t"], d["survival"], where="post", label=g, lw=2 if g == "all" else 1.2)
    ax.set_xlabel("days since snapshot")
    ax.set_ylabel("P(no purchase yet)")
    ax.set_title("Kaplan-Meier: time to next purchase (test snapshot)")
    ax.legend()
    return _save(fig, path)


def hillstrom_qini(curves: dict[str, tuple[np.ndarray, np.ndarray]], path: Path, outcome: str) -> str:
    """Qini curves on the real Hillstrom RCT."""
    return qini_plot(curves, path, f"Hillstrom (real RCT): Qini for '{outcome}'")


def segment_bar(seg: pd.DataFrame, path: Path) -> str:
    """Profit contribution of risk-only targeting by segment."""
    fig, ax = plt.subplots(figsize=(6, 3.6))
    v = seg["profit_inr"] / 1e6
    ax.bar(seg["segment"], v, color=["#d9534f" if x < 0 else "#2f6fb0" for x in v])
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("profit contribution (INR m)")
    ax.set_title("Risk-top-30% policy: who earns / loses money")
    return _save(fig, path)
