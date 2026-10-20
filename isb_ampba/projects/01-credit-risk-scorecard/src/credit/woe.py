"""Monotonic optimal binning, WOE transform and IV table (optbinning). Fit on TRAIN only."""
from __future__ import annotations

import numpy as np
import pandas as pd
from optbinning import BinningProcess


def fit_binning(X_train: pd.DataFrame, y_train, iv_min: float = 0.02, seed: int = 42) -> BinningProcess:
    """Fit monotonic bins per variable; variables with IV < iv_min are marked not selected."""
    cols = list(X_train.columns)
    bp = BinningProcess(
        variable_names=cols, max_n_prebins=20, min_prebin_size=0.05,
        selection_criteria={"iv": {"min": iv_min}},
        binning_fit_params={c: {"monotonic_trend": "auto_asc_desc"} for c in cols})
    return bp.fit(X_train, np.asarray(y_train))


def iv_table(bp: BinningProcess) -> pd.DataFrame:
    """Variable, n_bins, IV, gini, selected - sorted by IV."""
    s = bp.summary()[["name", "n_bins", "iv", "gini", "selected"]]
    return s.sort_values("iv", ascending=False).reset_index(drop=True)


def selected_variables(bp: BinningProcess) -> list[str]:
    """Names of variables passing the IV filter (order = optbinning transform order)."""
    s = bp.summary()
    return [str(n) for n in s.loc[s["selected"].astype(bool), "name"]]


def woe_transform(bp: BinningProcess, X: pd.DataFrame) -> pd.DataFrame:
    """WOE-encode X for the selected variables."""
    arr = bp.transform(X, metric="woe")
    return pd.DataFrame(np.asarray(arr), columns=selected_variables(bp), index=X.index)


def woe_is_monotonic(bp: BinningProcess, var: str) -> bool:
    """True if the WOE across regular bins of `var` is monotone (either direction)."""
    t = bp.get_binned_variable(var).binning_table.build()
    t = t.loc[[i for i in t.index if str(i) != "Totals"]]
    t = t[~t["Bin"].astype(str).isin(["Special", "Missing"])]
    d = np.diff(t["WoE"].to_numpy(dtype=float))
    return bool(np.all(d >= -1e-12) or np.all(d <= 1e-12))
