"""Model metrics: AUC, Gini, KS, Brier, calibration slope, calibration/decile tables, PSI."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import ks_2samp
from sklearn.metrics import brier_score_loss, roc_auc_score


def auc(y, p) -> float:
    """ROC-AUC."""
    return float(roc_auc_score(y, p))


def gini(y, p) -> float:
    """Gini = 2*AUC - 1."""
    return 2 * auc(y, p) - 1


def brier(y, p) -> float:
    """Brier score."""
    return float(brier_score_loss(y, p))


def ks(y, p) -> float:
    """Kolmogorov-Smirnov: max gap between score distributions of defaulters and non-defaulters."""
    y, p = np.asarray(y), np.asarray(p)
    return float(ks_2samp(p[y == 1], p[y == 0]).statistic)


def calibration_slope(y, p, eps: float = 1e-6) -> float:
    """Slope of Logit(y ~ logit(p)); 1.0 = perfectly calibrated spread."""
    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    z = np.log(p / (1 - p))
    return float(sm.Logit(np.asarray(y), sm.add_constant(z)).fit(disp=0).params[1])


def metrics(y, p) -> dict:
    """All headline metrics for one (y, PD) pair."""
    return {"auc": auc(y, p), "gini": gini(y, p), "ks": ks(y, p), "brier": brier(y, p),
            "cal_slope": calibration_slope(y, p)}


def calibration_table(y, p, n_bins: int = 10) -> pd.DataFrame:
    """Mean predicted vs observed default rate per PD decile."""
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p)})
    df["bin"] = pd.qcut(df["p"].rank(method="first"), n_bins, labels=False)
    return df.groupby("bin").agg(mean_pred=("p", "mean"), obs_rate=("y", "mean"), n=("y", "size")).reset_index()


def decile_table(y, p, n: int = 10) -> pd.DataFrame:
    """Lift table, decile 1 = riskiest."""
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p)})
    df["decile"] = pd.qcut(df["p"].rank(method="first", ascending=False), n, labels=range(1, n + 1))
    t = df.groupby("decile", observed=True).agg(n=("y", "size"), bads=("y", "sum"), bad_rate=("y", "mean"),
                                                avg_pd=("p", "mean"))
    t["cum_bad_capture"] = t["bads"].cumsum() / t["bads"].sum()
    t["lift"] = t["bad_rate"] / df["y"].mean()
    return t.reset_index()


def psi(expected, actual, bins: int = 10, eps: float = 1e-4) -> float:
    """Population stability index with quantile bins of the *expected* sample."""
    expected, actual = np.asarray(expected, dtype=float), np.asarray(actual, dtype=float)
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.clip(np.histogram(expected, edges)[0] / len(expected), eps, None)
    a = np.clip(np.histogram(actual, edges)[0] / len(actual), eps, None)
    return float(np.sum((a - e) * np.log(a / e)))
