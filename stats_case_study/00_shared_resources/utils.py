"""General helpers shared by every case study.

Kept deliberately small: path handling, reproducibility and number formatting.
Anything statistical lives in ``statistical_tests.py`` so the learner can find it.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# One seed for the whole book. Each generator derives its own stream from it
# (np.random.default_rng(SEED + case_number)) so cases stay independent.
SEED = 20260401


def find_repo_root(start: Path | None = None) -> Path:
    """Walk upwards from ``start`` until the folder containing ``00_shared_resources``."""
    here = Path(start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "00_shared_resources").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate the repository root (00_shared_resources not found).")


def case_paths(case_dir: Path) -> dict[str, Path]:
    """Return the standard sub-folders of a case study, creating output folders if needed."""
    case_dir = Path(case_dir).resolve()
    paths = {
        "case": case_dir,
        "data": case_dir / "data",
        "figures": case_dir / "outputs" / "figures",
        "tables": case_dir / "outputs" / "tables",
        "presentation": case_dir / "presentation",
    }
    for key in ("data", "figures", "tables", "presentation"):
        paths[key].mkdir(parents=True, exist_ok=True)
    return paths


def rng_for_case(case_number: int) -> np.random.Generator:
    """Seeded random generator for a given case, so every case is reproducible on its own."""
    return np.random.default_rng(SEED + case_number)


def save_table(df: pd.DataFrame, name: str, tables_dir: Path, index: bool = True) -> Path:
    """Save a result table as CSV (rounded for readability) and return its path."""
    path = Path(tables_dir) / f"{name}.csv"
    out = df.copy()
    num_cols = out.select_dtypes("number").columns
    out[num_cols] = out[num_cols].round(10)
    out.to_csv(path, index=index)
    return path


def fmt_money(x: float, currency: str = "₹", decimals: int = 0) -> str:
    """Format a number as money with thousands separators, e.g. ₹4,25,000 -> '₹425,000'."""
    if pd.isna(x):
        return "n/a"
    return f"{currency}{x:,.{decimals}f}"


def fmt_pct(x: float, decimals: int = 1) -> str:
    """Format a proportion (0.0523) as a percentage string ('5.2%')."""
    if pd.isna(x):
        return "n/a"
    return f"{100 * x:.{decimals}f}%"


def fmt_p(p: float) -> str:
    """Report p-values the way a careful analyst does: never '0.000'."""
    if pd.isna(p):
        return "n/a"
    if p < 0.001:
        return "< 0.001"
    return f"{p:.3f}"
