"""Baseline logit, XGBoost / LightGBM with Optuna tuning (train only), isotonic calibration (valid only)."""
from __future__ import annotations

import numpy as np
import optuna
from lightgbm import LGBMClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

optuna.logging.set_verbosity(optuna.logging.WARNING)


def fit_baseline_logit(X, y, seed: int = 42):
    """Naive-but-honest baseline: standardised logistic regression on the raw features."""
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=seed)).fit(X, y)


def fit_logit_scorecard(Xw, y, iv, corr_max: float = 0.7, seed: int = 42):
    """Convenience re-export so models.py exposes every model fitter (see scorecard.fit_logit_scorecard)."""
    from .scorecard import fit_logit_scorecard as _fit

    return _fit(Xw, y, iv, corr_max, seed)


def _xgb(params: dict, seed: int, n_jobs: int = 4) -> XGBClassifier:
    return XGBClassifier(tree_method="hist", eval_metric="auc", n_jobs=n_jobs, random_state=seed, **params)


def _lgbm(params: dict, seed: int, n_jobs: int = 4) -> LGBMClassifier:
    return LGBMClassifier(subsample_freq=1, n_jobs=n_jobs, random_state=seed, verbose=-1, **params)


def _space(trial: optuna.Trial, kind: str) -> dict:
    p = {"n_estimators": trial.suggest_int("n_estimators", 100, 500),
         "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1, log=True),
         "subsample": trial.suggest_float("subsample", 0.6, 1.0),
         "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0),
         "reg_lambda": trial.suggest_float("reg_lambda", 0.1, 20.0, log=True)}
    if kind == "xgb":
        p["max_depth"] = trial.suggest_int("max_depth", 2, 6)
        p["min_child_weight"] = trial.suggest_float("min_child_weight", 1, 50, log=True)
    else:
        p["num_leaves"] = trial.suggest_int("num_leaves", 8, 64)
        p["min_child_samples"] = trial.suggest_int("min_child_samples", 20, 200)
    return p


def tune_and_fit(kind: str, X, y, n_trials: int = 30, cv_folds: int = 3, seed: int = 42, n_jobs: int = 4):
    """Optuna TPE maximising CV AUC on TRAIN only. Returns (model, best_params, best_cv_auc)."""
    make = _xgb if kind == "xgb" else _lgbm
    cv = StratifiedKFold(cv_folds, shuffle=True, random_state=seed)

    def obj(t: optuna.Trial) -> float:
        return float(cross_val_score(make(_space(t, kind), seed, n_jobs), X, y, cv=cv, scoring="roc_auc").mean())

    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=seed))
    study.optimize(obj, n_trials=n_trials)
    return make(study.best_params, seed, n_jobs).fit(X, y), study.best_params, float(study.best_value)


def fit_isotonic(p_valid, y_valid) -> IsotonicRegression:
    """Monotone map raw probability -> calibrated PD, fitted on VALID only."""
    return IsotonicRegression(out_of_bounds="clip", y_min=1e-4, y_max=1 - 1e-4).fit(
        np.asarray(p_valid), np.asarray(y_valid))


def predict_pd(model, X, calibrator=None) -> np.ndarray:
    """Probability of default, optionally passed through the isotonic calibrator."""
    p = model.predict_proba(X)[:, 1]
    return calibrator.predict(p) if calibrator is not None else p
