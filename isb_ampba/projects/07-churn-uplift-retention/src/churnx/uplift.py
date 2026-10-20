"""Uplift modelling: S/T/X/transformed-outcome/class-transformation learners and Qini/uplift metrics.

Convention: ``w`` in {0,1} (1 = treated), ``y`` higher is better (retention), ``tau_hat`` = predicted
incremental outcome from treating (higher = treat first).
"""
from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import GroupKFold

_trapz = getattr(np, "trapezoid", None) or np.trapz  # numpy>=2 renamed trapz


def _base(kind: str, params: dict[str, Any], seed: int):
    p = {**params, "random_state": seed, "verbose": -1, "n_jobs": 1, "subsample_freq": 1}
    return LGBMClassifier(**p) if kind == "binary" else LGBMRegressor(**p)


def _pred(model, X: np.ndarray, kind: str) -> np.ndarray:
    return model.predict_proba(X)[:, 1] if kind == "binary" else model.predict(X)


class MetaLearner:
    """Meta-learner for heterogeneous treatment effects.

    learner: 'S' single model with w feature, 'T' two models, 'X' (Kunzel et al.), 'TO' transformed outcome
    (needs the randomisation probability) and 'CT' class-transformation (Jaskowski & Jaroszewicz; binary y,
    valid for e=0.5).
    """

    def __init__(self, learner: str = "T", kind: str = "binary", params: dict[str, Any] | None = None,
                 seed: int = 42, e: float | None = None) -> None:
        assert learner in {"S", "T", "X", "TO", "CT"}
        self.learner, self.kind, self.seed, self.e = learner, kind, seed, e
        self.params = params or {"n_estimators": 200, "num_leaves": 8, "min_child_samples": 40,
                                 "learning_rate": 0.03, "subsample": 0.8, "colsample_bytree": 0.8}

    def fit(self, X, w, y) -> MetaLearner:
        """Fit the chosen meta-learner."""
        X, w, y = np.asarray(X, float), np.asarray(w).astype(int), np.asarray(y, float)
        self.e_ = float(w.mean()) if self.e is None else self.e
        mk = lambda k=None: _base(k or self.kind, self.params, self.seed)  # noqa: E731
        t, c = w == 1, w == 0
        if self.learner == "S":
            self.m_ = mk().fit(np.column_stack([X, w]), y)
        elif self.learner == "T":
            self.m1_, self.m0_ = mk().fit(X[t], y[t]), mk().fit(X[c], y[c])
        elif self.learner == "X":
            self.m1_, self.m0_ = mk().fit(X[t], y[t]), mk().fit(X[c], y[c])
            d1 = y[t] - _pred(self.m0_, X[t], self.kind)
            d0 = _pred(self.m1_, X[c], self.kind) - y[c]
            self.t1_, self.t0_ = mk("cont").fit(X[t], d1), mk("cont").fit(X[c], d0)
        elif self.learner == "TO":
            ystar = y * (w - self.e_) / (self.e_ * (1 - self.e_))
            self.m_ = mk("cont").fit(X, ystar)
        else:  # CT
            z = w * y + (1 - w) * (1 - y)
            self.m_ = _base("binary", self.params, self.seed).fit(X, z.astype(int))
        return self

    def predict(self, X) -> np.ndarray:
        """Predicted incremental outcome of treating each row."""
        X = np.asarray(X, float)
        if self.learner == "S":
            one, zero = np.ones(len(X)), np.zeros(len(X))
            return _pred(self.m_, np.column_stack([X, one]), self.kind) - _pred(self.m_, np.column_stack([X, zero]), self.kind)
        if self.learner == "T":
            return _pred(self.m1_, X, self.kind) - _pred(self.m0_, X, self.kind)
        if self.learner == "X":
            return self.e_ * self.t0_.predict(X) + (1 - self.e_) * self.t1_.predict(X)
        if self.learner == "TO":
            return self.m_.predict(X)
        return 2.0 * self.m_.predict_proba(X)[:, 1] - 1.0


# ----------------------------------------------------------------------------- metrics
def qini_curve(y, w, score) -> tuple[np.ndarray, np.ndarray]:
    """Q(k) = Y_T(k) - Y_C(k) * N_T(k) / N_C(k) for the top-k scored customers (higher score = treat first)."""
    order = np.argsort(-np.asarray(score, float), kind="mergesort")
    y, w = np.asarray(y, float)[order], np.asarray(w)[order]
    cy_t, cy_c = np.cumsum(y * (w == 1)), np.cumsum(y * (w == 0))
    n_t, n_c = np.cumsum(w == 1), np.cumsum(w == 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        q = cy_t - np.where(n_c > 0, cy_c * n_t / np.maximum(n_c, 1), 0.0)
    return np.arange(1, len(y) + 1), q


def qini_auc(y, w, score) -> float:
    """Area between the Qini curve and the random-targeting line (the Qini coefficient, raw units)."""
    n, q = qini_curve(y, w, score)
    n, q = np.r_[0, n], np.r_[0.0, q]
    rand = q[-1] * n / n[-1]
    return float(_trapz(q, n) - _trapz(rand, n))


def uplift_at_k(y, w, score, k: float = 0.3) -> float:
    """Observed treated-minus-control mean outcome among the top-k fraction by score."""
    top = np.argsort(-np.asarray(score, float), kind="mergesort")[: max(int(len(y) * k), 2)]
    yy, ww = np.asarray(y, float)[top], np.asarray(w)[top]
    if (ww == 1).sum() == 0 or (ww == 0).sum() == 0:
        return float("nan")
    return float(yy[ww == 1].mean() - yy[ww == 0].mean())


def uplift_curve(y, w, score, n_points: int = 20) -> pd.DataFrame:
    """Cumulative uplift (treated-minus-control mean) among the top fraction, for plotting."""
    fr = np.linspace(1.0 / n_points, 1.0, n_points)
    return pd.DataFrame({"fraction": fr, "uplift": [uplift_at_k(y, w, score, k) for k in fr]})


def auuc(y, w, score) -> float:
    """Area under the uplift curve (mean cumulative gain Q(k)/N over fractions), a normalised AUUC."""
    n, q = qini_curve(y, w, score)
    return float(_trapz(np.r_[0.0, q], np.r_[0, n]) / (len(y) ** 2))


def tau_recovery(tau_hat, tau_true) -> dict[str, float]:
    """Pearson / Spearman correlation and RMSE of estimated vs ground-truth tau (Track A only)."""
    a, b = np.asarray(tau_hat, float), np.asarray(tau_true, float)
    return {"pearson": float(np.corrcoef(a, b)[0, 1]), "spearman": float(pd.Series(a).corr(pd.Series(b), method="spearman")),
            "rmse": float(np.sqrt(np.mean((a - b) ** 2)))}


def bootstrap_ci(fn: Callable[[np.ndarray], float], n: int, n_boot: int = 200, seed: int = 0,
                 alpha: float = 0.05) -> tuple[float, float]:
    """Percentile bootstrap CI of ``fn(index_array)``."""
    rng = np.random.default_rng(seed)
    vals = np.array([fn(rng.integers(0, n, n)) for _ in range(n_boot)])
    vals = vals[np.isfinite(vals)]
    return float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2))


def cv_qini(X: pd.DataFrame, w, y, groups, learner: str, params: dict[str, Any] | None, seed: int,
            n_splits: int = 3) -> float:
    """Grouped-CV Qini (pooled out-of-fold scores) used to *select* a learner without touching the test set."""
    X, w, y = np.asarray(X, float), np.asarray(w), np.asarray(y, float)
    oof = np.zeros(len(y))
    for tr, va in GroupKFold(n_splits).split(X, y, groups):
        oof[va] = MetaLearner(learner, "binary", params, seed).fit(X[tr], w[tr], y[tr]).predict(X[va])
    return qini_auc(y, w, oof)


def fit_learners(Xtr, wtr, ytr, Xte, learners: list[str], params: dict[str, Any] | None, seed: int) -> dict[str, np.ndarray]:
    """Fit every learner on the training pilot and return tau_hat on the test cohort."""
    return {name: MetaLearner(name, "binary", params, seed).fit(Xtr, wtr, ytr).predict(Xte) for name in learners}
