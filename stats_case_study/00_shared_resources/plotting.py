"""Consistent, presentation-ready figure style for the whole book.

Every figure is saved at high resolution so the same PNG can be used in the
notebook and in the stakeholder deck.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Categorical colours in a FIXED order (colour-blind-checked palette).
# Use them in this order and never cycle past the number of groups you need.
COLORS = {
    "blue": "#2a78d6",
    "orange": "#eb6834",
    "aqua": "#1baf7a",
    "yellow": "#eda100",
    "magenta": "#e87ba4",
    "green": "#008300",
    "violet": "#4a3aa7",
    "red": "#e34948",
}
CATEGORICAL = list(COLORS.values())

# Neutral inks for text, reference lines and de-emphasised data.
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#8a8985"
GRID = "#e4e3df"
HIGHLIGHT = COLORS["orange"]   # the one thing we want the eye to land on
PRIMARY = COLORS["blue"]       # default single-series colour


def set_style() -> None:
    """Apply the book's plotting style. Call once at the top of each notebook."""
    sns.set_theme(style="whitegrid", palette=CATEGORICAL)
    mpl.rcParams.update(
        {
            "figure.figsize": (9, 5),
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.labelsize": 11,
            "axes.labelcolor": INK_SECONDARY,
            "axes.edgecolor": GRID,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "xtick.color": INK_SECONDARY,
            "ytick.color": INK_SECONDARY,
            "text.color": INK,
            "legend.frameon": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save_fig(fig: plt.Figure, name: str, figures_dir: Path) -> Path:
    """Save a figure as a high-resolution PNG and return its path."""
    path = Path(figures_dir) / f"{name}.png"
    fig.savefig(path, facecolor="white")
    return path


def add_note(ax: plt.Axes, text: str, loc="lower right") -> None:
    """Small grey annotation (e.g. 'Synthetic data, n = 4,800') inside an axes corner.

    ``loc`` is a corner name or an explicit (x, y, ha, va) tuple in axes coordinates.
    """
    positions = {
        "lower right": (0.99, 0.02, "right", "bottom"),
        "upper right": (0.99, 0.97, "right", "top"),
        "upper left": (0.01, 0.97, "left", "top"),
        "lower left": (0.01, 0.02, "left", "bottom"),
    }
    x, y, ha, va = positions[loc] if isinstance(loc, str) else loc
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=9, color=INK_MUTED)


def thousands_formatter(prefix: str = "", suffix: str = "", scale: float = 1.0, decimals: int = 0):
    """Tick formatter such as ₹250k: thousands_formatter('₹', 'k', 1e3)."""
    def fmt(v, _):
        sign = "−" if v < 0 else ""
        return f"{sign}{prefix}{abs(v) / scale:,.{decimals}f}{suffix}"
    return mpl.ticker.FuncFormatter(fmt)
