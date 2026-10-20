"""Charts: waterfall, tornado, heat-maps, distributions (matplotlib, headless) and a plotly waterfall for the app."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

GREEN, RED, BLUE, GREY = "#2a9d8f", "#e76f51", "#264653", "#8d99ae"


def _save(fig: plt.Figure, path: str | Path | None) -> None:
    fig.tight_layout()
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=130)
    plt.close(fig)


def waterfall_steps(r: dict) -> list[tuple[str, float]]:
    """(label, signed value) steps of the contribution waterfall: +direct, -subsidy, -cannibalised, +halo."""
    return [("Direct uplift", r["direct_uplift"]), ("Subsidy on baseline", -r["subsidy_cost"]),
            ("Cannibalised siblings", -r["cannibalised_margin"]), ("Halo (basket pull)", r["halo_margin"])]


def waterfall(r: dict, title: str, path: str | Path | None = None) -> plt.Figure | None:
    """Waterfall chart of direct, subsidy, cannibalisation, halo and family net (GBP)."""
    steps = waterfall_steps(r)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    cum = 0.0
    for k, (lab, v) in enumerate(steps):
        ax.bar(k, v, bottom=cum, color=GREEN if v >= 0 else RED)
        ax.text(k, max(cum, cum + v), f"{v:+,.0f}", ha="center", va="bottom", fontsize=9)
        cum += v
    ax.bar(len(steps), cum, color=BLUE)
    ax.text(len(steps), max(cum, 0), f"{cum:+,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.axhline(0, color="black", lw=0.8)
    ax.axhline(r["promoted_only"], color=GREY, ls="--", lw=1)
    ax.text(len(steps) + 0.45, r["promoted_only"], "promoted-only view", fontsize=8, color=GREY, va="bottom", ha="right")
    ax.set_xticks(range(len(steps) + 1), [s[0] for s in steps] + ["Family net"], rotation=15, fontsize=8)
    ax.margins(y=0.15)
    ax.set_ylabel("GBP over promo window"); ax.set_title(title, fontsize=10)
    _save(fig, path)
    return None


def tornado_chart(t: pd.DataFrame, base_net: float, title: str, path: str | Path | None = None) -> None:
    """Tornado of family net swing per assumption (others at mid-point)."""
    t = t.sort_values("swing")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for k, r in enumerate(t.itertuples()):
        lo, hi = sorted([r.net_at_low, r.net_at_high])
        ax.barh(k, hi - lo, left=lo, color=BLUE, alpha=0.85)
        ax.text(hi, k, f"  {r.low_value:g} to {r.high_value:g}", va="center", fontsize=8)
    ax.axvline(base_net, color=GREY, ls="--"); ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(range(len(t)), t["param"]); ax.set_xlabel("family net per unit of baseline sales (normalised)")
    ax.set_title(title, fontsize=10)
    _save(fig, path)


def heatmap(xs: np.ndarray, ys: np.ndarray, z: np.ndarray, xlabel: str, ylabel: str, title: str, path: str | Path | None = None) -> None:
    """Heat-map of family net on a grid (rows = ys, cols = xs); zero contour drawn."""
    fig, ax = plt.subplots(figsize=(6.5, 5))
    lim = float(np.nanmax(np.abs(z))) or 1.0
    im = ax.imshow(z, origin="lower", aspect="auto", cmap="RdYlGn", vmin=-lim, vmax=lim,
                   extent=[xs.min(), xs.max(), ys.min(), ys.max()])
    X, Y = np.meshgrid(xs, ys)
    ax.contour(X, Y, z, levels=[0], colors="black", linewidths=1.2)
    fig.colorbar(im, ax=ax, label="family net (normalised)")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title, fontsize=10)
    _save(fig, path)


def hist(values: np.ndarray, xlabel: str, title: str, path: str | Path | None = None, vline: float | None = None, bins: int = 30) -> None:
    """Histogram helper."""
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.hist(np.asarray(values)[np.isfinite(values)], bins=bins, color=BLUE, alpha=0.85)
    if vline is not None:
        ax.axvline(vline, color=RED, ls="--")
    ax.set_xlabel(xlabel); ax.set_ylabel("count"); ax.set_title(title, fontsize=10)
    _save(fig, path)


def reference_bars(ref: pd.DataFrame, title: str, path: str | Path | None = None) -> None:
    """Promoted-only vs family net per reference SKU."""
    r = ref.sort_values("family_net")
    fig, ax = plt.subplots(figsize=(8, 7))
    y = np.arange(len(r))
    ax.barh(y - 0.2, r["promoted_only"], height=0.4, color=GREY, label="promoted-only view")
    ax.barh(y + 0.2, r["family_net"], height=0.4, color=BLUE, label="family net")
    ax.set_yticks(y, [str(d)[:28] for d in r["description"]], fontsize=7)
    ax.axvline(0, color="black", lw=0.8); ax.legend(fontsize=8); ax.set_xlabel("GBP over promo window"); ax.set_title(title, fontsize=10)
    _save(fig, path)


def family_units_chart(r: dict, names: list[str], title: str, path: str | Path | None = None) -> None:
    """Baseline vs promoted weekly units for every family member (promoted SKU first)."""
    fig, ax = plt.subplots(figsize=(7, 3.8))
    x = np.arange(len(names))
    ax.bar(x - 0.2, r["baseline_units"], 0.4, color=GREY, label="baseline")
    ax.bar(x + 0.2, r["units_after"], 0.4, color=GREEN, label="promoted")
    ax.set_xticks(x, [n[:18] for n in names], rotation=30, ha="right", fontsize=7); ax.legend(); ax.set_ylabel("weekly units"); ax.set_title(title, fontsize=10)
    _save(fig, path)


def plan_compare_chart(opt_net: float, dash_net: float, rev_net: float, title: str, path: str | Path | None = None) -> None:
    """Bar chart: optimiser plan vs the two dashboard-style policies (true family net)."""
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.bar(["Optimiser", "Dashboard\n(promoted-only rank)", "Top revenue"], [opt_net, dash_net, rev_net], color=[GREEN, RED, GREY])
    ax.axhline(0, color="black", lw=0.8); ax.set_ylabel("family net, GBP"); ax.set_title(title, fontsize=10)
    _save(fig, path)


def waterfall_plotly(r: dict, title: str = "") -> object:
    """Plotly waterfall (direct, -subsidy, -cannibalised, +halo, net) for the Streamlit app."""
    import plotly.graph_objects as go

    steps = waterfall_steps(r)
    fig = go.Figure(go.Waterfall(
        x=[s[0] for s in steps] + ["Family net"], measure=["relative"] * len(steps) + ["total"],
        y=[s[1] for s in steps] + [0], text=[f"{s[1]:+,.0f}" for s in steps] + [f"{r['family_net']:+,.0f}"], textposition="outside",
        increasing={"marker": {"color": GREEN}}, decreasing={"marker": {"color": RED}}, totals={"marker": {"color": BLUE}},
    ))
    fig.update_layout(title=title, yaxis_title="GBP over promo window", showlegend=False, height=420, margin=dict(t=50, b=30))
    return fig
