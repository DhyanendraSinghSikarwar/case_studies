"""Churn models: logit, RF, XGBoost, LightGBM; group-aware calibration; lift; SHAP."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, clone
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score, roc_curve
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from churnx.config import get_logger

log = get_logger(__name__)
TREE_MODELS = ("rf", "xgb", "lgbm")


def _signed_log1p(x: np.ndarray) -> np.ndarray:
    return np.sign(x) * np.log1p(np.abs(x))


def make_models(seed: int = 42) -> dict[str, BaseEstimator]:
    """The four candidate models with the hyper-parameters fixed in the plan."""
    from lightgbm import LGBMClassifier
    from xgboost import XGBClassifier

    return {
        "logit": make_pipeline(FunctionTransformer(_signed_log1p), StandardScaler(),
                               LogisticRegression(max_iter=2000, C=0.5)),
        "rf": RandomForestClassifier(n_estimators=400, min_samples_leaf=10, n_jobs=4, random_state=seed),
        "xgb": XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.05, subsample=0.8,
                             colsample_bytree=0.8, eval_metric="logloss", random_state=seed, n_jobs=2),
        "lgbm": LGBMClassifier(n_estimators=300, num_leaves=15, learning_rate=0.05, min_child_samples=30,
                               subsample=0.8, subsample_freq=1, colsample_bytree=0.8, random_state=seed,
                               verbose=-1, n_jobs=2),
    }


def ks_stat(y: np.ndarray, p: np.ndarray) -> float:
    """Kolmogorov-Smirnov statistic: max(tpr - fpr)."""
    fpr, tpr, _ = roc_curve(y, p)
    return float(np.max(tpr - fpr))


def metrics(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    """ROC-AUC, PR-AUC, KS, Brier, plus mean prediction vs observed rate."""
    y, p = np.asarray(y), np.asarray(p)
    return {"auc": float(roc_auc_score(y, p)), "pr_auc": float(average_precision_score(y, p)),
            "ks": ks_stat(y, p), "brier": float(brier_score_loss(y, p)),
            "mean_pred": float(p.mean()), "base_rate": float(y.mean())}


def group_splits(X: pd.DataFrame, y: np.ndarray, groups: np.ndarray, n_splits: int = 3) -> list[tuple]:
    """Group-aware folds on customer_id (a customer never sits in both train and validation)."""
    return list(GroupKFold(n_splits).split(X, y, groups))


def cv_auc(models: dict[str, BaseEstimator], X: pd.DataFrame, y: np.ndarray, groups: np.ndarray,
           n_splits: int = 3) -> dict[str, float]:
    """Grouped cross-validated AUC within the training snapshots (used for champion selection)."""
    splits = group_splits(X, y, groups, n_splits)
    out = {}
    for name, m in models.items():
        aucs = []
        for tr, va in splits:
            mm = clone(m).fit(X.iloc[tr], y[tr])
            aucs.append(roc_auc_score(y[va], mm.predict_proba(X.iloc[va])[:, 1]))
        out[name] = float(np.mean(aucs))
    return out


def fit_calibrated(model: BaseEstimator, X: pd.DataFrame, y: np.ndarray, groups: np.ndarray,
                   method: str = "isotonic", n_splits: int = 3) -> CalibratedClassifierCV:
    """Isotonic calibration with group-aware folds (calibrator never sees its own training customers)."""
    splits = group_splits(X, y, groups, n_splits)
    return CalibratedClassifierCV(clone(model), method=method, cv=splits).fit(X, y)


def calibration_table(y: np.ndarray, p: np.ndarray, n_bins: int = 10) -> pd.DataFrame:
    """Reliability-curve points (quantile bins)."""
    frac, mean_p = calibration_curve(y, p, n_bins=n_bins, strategy="quantile")
    return pd.DataFrame({"mean_pred": mean_p, "frac_pos": frac})


def lift_table(y: np.ndarray, p: np.ndarray, n_bins: int = 10) -> pd.DataFrame:
    """Decile lift table: churn rate, lift and cumulative capture of churners (decile 1 = riskiest)."""
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p)}).sort_values("p", ascending=False)
    df["decile"] = np.minimum((np.arange(len(df)) * n_bins // len(df)) + 1, n_bins)
    t = df.groupby("decile").agg(n=("y", "size"), churners=("y", "sum"), churn_rate=("y", "mean"),
                                 mean_pred=("p", "mean")).reset_index()
    base = df["y"].mean()
    t["lift"] = t["churn_rate"] / base if base > 0 else np.nan
    t["cum_capture"] = t["churners"].cumsum() / max(df["y"].sum(), 1)
    return t


def shap_importance(model: BaseEstimator, X: pd.DataFrame, max_rows: int = 1500, seed: int = 42):
    """SHAP values for a fitted tree model on a subsample; returns (values array, X sample)."""
    import shap

    Xs = X.sample(min(len(X), max_rows), random_state=seed)
    sv = shap.TreeExplainer(model).shap_values(Xs)
    if isinstance(sv, list):
        sv = sv[1]
    sv = np.asarray(sv)
    if sv.ndim == 3:
        sv = sv[:, :, 1]
    return sv, Xs


def fit_all(X: pd.DataFrame, y: np.ndarray, groups: np.ndarray, Xte: pd.DataFrame, yte: np.ndarray,
            cfg: dict[str, Any]) -> dict[str, Any]:
    """Fit all models on train, score test, select champion by grouped-CV AUC (never by test)."""
    seed = cfg["seed"]
    models = make_models(seed)
    cv = cv_auc(models, X, y, groups, cfg["models"]["cv_folds"])
    fitted, probs, mets = {}, {}, {}
    for name, m in models.items():
        fitted[name] = clone(m).fit(X, y)
        probs[name] = fitted[name].predict_proba(Xte)[:, 1]
        mets[name] = metrics(yte, probs[name])
        mets[name]["cv_auc_train"] = cv[name]
    base = np.full(len(yte), float(np.mean(y)))
    mets["baseline_train_rate"] = {"auc": 0.5, "brier": float(brier_score_loss(yte, base)),
                                   "mean_pred": float(base[0]), "base_rate": float(np.mean(yte))}
    champion = max(cv, key=cv.get)
    tree_champ = max(TREE_MODELS, key=lambda k: cv[k])
    cal = fit_calibrated(models[champion], X, y, groups, cfg["models"]["calibration_method"],
                         cfg["models"]["cv_folds"])
    p_cal = cal.predict_proba(Xte)[:, 1]
    mets["champion_calibrated"] = metrics(yte, p_cal)
    return {"fitted": fitted, "probs": probs, "metrics": mets, "cv_auc": cv, "champion": champion,
            "tree_champion": tree_champ, "calibrated": cal, "p_test_cal": p_cal, "p_test_raw": probs[champion]}


def temporal_window_check(snaps: pd.DataFrame, features: list[str], seed: int = 42) -> dict[str, Any]:
    """Train-only check of the training window and regularisation (never touches the test snapshot).

    Fits the logit on the earlier training snapshots (``train`` split, excluding the last) versus those plus the
    ``pilot_hist`` snapshots, and scores each on the last training snapshot. Used to justify (or reject) a wider
    window / different ``C`` without looking at the test AUC.
    """
    tr = snaps[snaps["split"] == "train"]
    last = tr["asof"].max()
    val = tr[tr["asof"] == last]
    windows = {"train_prior_only": tr[tr["asof"] < last],
               "pilot_hist_plus_train_prior": snaps[snaps["split"].isin(["pilot_hist", "train"]) & (snaps["asof"] < last)]}
    out: dict[str, Any] = {"validation_snapshot": str(pd.Timestamp(last).date())}
    for wname, w in windows.items():
        for c in (0.05, 0.5):
            m = make_pipeline(FunctionTransformer(_signed_log1p), StandardScaler(),
                              LogisticRegression(max_iter=2000, C=c)).fit(w[features], w["churn"])
            out[f"{wname}__C={c}"] = float(roc_auc_score(val["churn"], m.predict_proba(val[features])[:, 1]))
    out["n_validation_rows"] = int(len(val))
    return out
