"""Small, transparent statistical helpers reused across cases.

Each function is short enough to read in a minute. The notebooks first compute
every quantity by hand, then call these helpers once the learner has seen the
mechanics. All helpers return plain dicts / DataFrames so results are easy to
tabulate and save.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.proportion import proportion_confint


# ---------------------------------------------------------------------------
# Descriptive statistics
# ---------------------------------------------------------------------------
def describe_numeric(x: pd.Series, percentiles=(0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)) -> pd.Series:
    """A richer replacement for ``Series.describe()``.

    Adds the statistics a business-facing analyst actually needs: IQR,
    coefficient of variation, skewness, (excess) kurtosis and missing count.
    """
    s = pd.Series(x)
    clean = s.dropna()
    q = clean.quantile(list(percentiles))
    out = {
        "n": clean.size,
        "missing": int(s.isna().sum()),
        "mean": clean.mean(),
        "median": clean.median(),
        "std": clean.std(ddof=1),
        "min": clean.min(),
    }
    for p, v in q.items():
        out[f"p{int(round(p * 100))}"] = v
    out.update(
        {
            "max": clean.max(),
            "range": clean.max() - clean.min(),
            "iqr": q.get(0.75, clean.quantile(0.75)) - q.get(0.25, clean.quantile(0.25)),
            "cv": clean.std(ddof=1) / clean.mean() if clean.mean() != 0 else np.nan,
            "skewness": stats.skew(clean, bias=False),
            "excess_kurtosis": stats.kurtosis(clean, fisher=True, bias=False),
        }
    )
    return pd.Series(out, name=s.name)


# ---------------------------------------------------------------------------
# Confidence intervals
# ---------------------------------------------------------------------------
def mean_ci(x, conf: float = 0.95) -> dict:
    """t-based confidence interval for a population mean."""
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    n = x.size
    mean = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    t_crit = stats.t.ppf(1 - (1 - conf) / 2, df=n - 1)
    return {"estimate": mean, "se": se, "lower": mean - t_crit * se, "upper": mean + t_crit * se,
            "n": n, "t_crit": t_crit, "conf": conf}


def proportion_ci(successes: int, n: int, conf: float = 0.95, method: str = "wilson") -> dict:
    """Confidence interval for a proportion (Wilson by default; better than the textbook Wald interval)."""
    p_hat = successes / n
    lower, upper = proportion_confint(successes, n, alpha=1 - conf, method=method)
    return {"estimate": p_hat, "se": np.sqrt(p_hat * (1 - p_hat) / n), "lower": lower, "upper": upper,
            "n": n, "successes": successes, "method": method, "conf": conf}


def bootstrap_ci(x, statistic=np.median, n_boot: int = 10_000, conf: float = 0.95, seed: int = 0) -> dict:
    """Percentile bootstrap CI for any one-sample statistic (median, trimmed mean, ...)."""
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, x.size, size=(n_boot, x.size))
    boot = np.apply_along_axis(statistic, 1, x[idx])
    alpha = 1 - conf
    return {"estimate": statistic(x), "se": boot.std(ddof=1),
            "lower": np.quantile(boot, alpha / 2), "upper": np.quantile(boot, 1 - alpha / 2),
            "n": x.size, "n_boot": n_boot, "conf": conf}


# ---------------------------------------------------------------------------
# Effect sizes
# ---------------------------------------------------------------------------
def cohens_d(x, y) -> float:
    """Standardised mean difference (x - y) using the pooled standard deviation."""
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    y = np.asarray(pd.Series(y).dropna(), dtype=float)
    nx, ny = x.size, y.size
    pooled = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2))
    return (x.mean() - y.mean()) / pooled


def cohens_h(p1: float, p2: float) -> float:
    """Effect size for the difference between two proportions (arcsine transformation)."""
    return 2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2))


def ci_table(rows: dict[str, dict], value_fmt=None) -> pd.DataFrame:
    """Turn {label: ci_dict} into a tidy table with estimate / se / lower / upper / n."""
    df = pd.DataFrame(rows).T
    cols = [c for c in ["estimate", "se", "lower", "upper", "n"] if c in df.columns]
    return df[cols].apply(pd.to_numeric)


# ---------------------------------------------------------------------------
# Comparing predictive models (Case 13 onwards)
# ---------------------------------------------------------------------------
def delong_test(y_true, score_a, score_b) -> dict:
    """DeLong test for the difference between two correlated ROC AUCs (same observations).

    Uses the structural-components formulation (DeLong, DeLong & Clarke-Pearson 1988;
    fast midrank version of Sun & Xu 2014). Returns both AUCs, their difference,
    its standard error, a 95% CI and the two-sided p-value.
    """
    y = np.asarray(y_true).astype(bool)
    preds = np.vstack([np.asarray(score_a, float), np.asarray(score_b, float)])
    m, n = y.sum(), (~y).sum()
    pos, neg = preds[:, y], preds[:, ~y]
    tx = np.vstack([stats.rankdata(p) for p in pos])          # ranks within positives
    ty = np.vstack([stats.rankdata(p) for p in neg])          # ranks within negatives
    tz = np.vstack([stats.rankdata(np.r_[a, b]) for a, b in zip(pos, neg)])  # ranks in pooled sample
    aucs = tz[:, :m].sum(axis=1) / (m * n) - (m + 1) / (2 * n)
    v01 = (tz[:, :m] - tx) / n                                 # structural components, positives
    v10 = 1 - (tz[:, m:] - ty) / m                             # structural components, negatives
    cov = np.cov(v01) / m + np.cov(v10) / n
    diff = aucs[0] - aucs[1]
    se = np.sqrt(cov[0, 0] + cov[1, 1] - 2 * cov[0, 1])
    z = diff / se
    return {"auc_a": aucs[0], "auc_b": aucs[1], "diff": diff, "se": se,
            "ci_low": diff - 1.96 * se, "ci_high": diff + 1.96 * se, "z": z, "p_value": 2 * stats.norm.sf(abs(z))}


def corrected_resampled_ttest(scores_a, scores_b, n_train: int, n_test: int) -> dict:
    """Nadeau & Bengio (2003) corrected resampled t-test for repeated cross-validation.

    A naive paired t-test on CV fold scores is badly over-confident because folds share
    training data (the fold scores are positively correlated). The correction inflates the
    variance by (1/k + n_test/n_train).
    """
    d = np.asarray(scores_a, float) - np.asarray(scores_b, float)
    k = d.size
    var = d.var(ddof=1)
    se_naive = np.sqrt(var / k)
    se_corr = np.sqrt((1 / k + n_test / n_train) * var)
    t_corr = d.mean() / se_corr
    t_crit = stats.t.ppf(0.975, k - 1)
    return {"mean_diff": d.mean(), "se_corrected": se_corr, "t_corrected": t_corr,
            "p_corrected": 2 * stats.t.sf(abs(t_corr), k - 1),
            "ci_low": d.mean() - t_crit * se_corr, "ci_high": d.mean() + t_crit * se_corr,
            "t_naive": d.mean() / se_naive, "p_naive": 2 * stats.t.sf(abs(d.mean() / se_naive), k - 1), "k": k}


def psi(expected, actual, bins: int = 10) -> float:
    """Population Stability Index between a reference sample and a new sample.

    Rule of thumb used in credit risk: < 0.10 stable, 0.10-0.25 moderate shift, > 0.25 major shift.
    """
    expected, actual = np.asarray(expected, float), np.asarray(actual, float)
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(expected, edges)[0] / expected.size
    a = np.histogram(actual, edges)[0] / actual.size
    e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)
    return float(np.sum((a - e) * np.log(a / e)))
