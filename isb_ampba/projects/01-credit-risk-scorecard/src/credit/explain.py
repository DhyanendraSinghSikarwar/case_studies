"""SHAP global importance and per-customer reason codes (explain the RAW tree model, not the calibrated PD)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import shap

TEMPLATES = {
    "avg_util": "High average utilisation ({v:.0%})",
    "util_1": "High utilisation last month ({v:.0%})",
    "max_delay": "Worst payment delay of {v:.0f} month(s)",
    "n_months_delayed": "{v:.0f} of last 6 months delayed",
    "delay_trend": "Delinquency getting worse (trend {v:+.2f})",
    "PAY_0": "Latest repayment status code {v:.0f} (1+ = late)",
    "PAY_2": "Repayment status 2 months ago: code {v:.0f}",
    "avg_pay_ratio": "Pays only {v:.0%} of the amount billed",
    "pay_ratio_1": "Last payment covered only {v:.0%} of the previous bill",
    "LIMIT_BAL": "Low credit limit (NT$ {v:,.0f})",
    "bill_growth": "Outstanding bill rising ({v:+.0%} of limit)",
    "util_volatility": "Unstable utilisation (sd {v:.0%})",
    "AGE": "Age {v:.0f}",
}


def shap_values(model, X: pd.DataFrame) -> np.ndarray:
    """SHAP log-odds contributions (positive = pushes PD up) for a tree model."""
    sv = shap.TreeExplainer(model).shap_values(X)
    return np.asarray(sv[1] if isinstance(sv, list) else sv)


def reason_codes(row, sv_row, cols, k: int = 4) -> list[str]:
    """Top-k plain-English factors that INCREASE this customer's risk."""
    out: list[str] = []
    for j in np.argsort(-np.asarray(sv_row)):
        if sv_row[j] <= 0 or len(out) == k:
            break
        out.append(TEMPLATES.get(cols[j], "{n} = {v:.2f}").format(n=cols[j], v=float(row[cols[j]])))
    return out


def global_importance(sv: np.ndarray, cols) -> pd.DataFrame:
    """Mean |SHAP| per feature, sorted."""
    imp = pd.DataFrame({"feature": list(cols), "mean_abs_shap": np.abs(sv).mean(axis=0)})
    return imp.sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)
