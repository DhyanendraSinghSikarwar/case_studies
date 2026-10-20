"""CLV: BG/NBD + Gamma-Gamma fitted on the calibration period, validated on the holdout."""
from __future__ import annotations

import numpy as np
import pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
from scipy.stats import spearmanr

from .config import get_logger, load_config
from .data import invoices

log = get_logger(__name__)


def calibration_summary(cal_sales: pd.DataFrame, cutoff: pd.Timestamp) -> pd.DataFrame:
    """lifetimes RFM summary (frequency = repeat purchase DAYS, recency, T, monetary_value).

    `cal_sales` must contain only rows up to `cutoff` (asserted: no look-ahead).
    """
    assert cal_sales["invoice_date"].max() < cutoff + pd.Timedelta(days=1), "calibration leaks"
    inv = invoices(cal_sales)
    return summary_data_from_transaction_data(
        inv, "customer_id", "invoice_date", monetary_value_col="revenue",
        observation_period_end=cutoff, freq="D")


def fit_models(summary: pd.DataFrame, cfg: dict | None = None
               ) -> tuple[BetaGeoFitter, GammaGammaFitter]:
    """Fit BG/NBD on all customers and Gamma-Gamma on repeat customers (frequency>0)."""
    cfg = cfg or load_config()
    c = cfg["clv"]
    bgf = BetaGeoFitter(penalizer_coef=c["penalizer_bgnbd"])
    bgf.fit(summary["frequency"], summary["recency"], summary["T"])
    rep = summary[(summary["frequency"] > 0) & (summary["monetary_value"] > 0)]
    ggf = GammaGammaFitter(penalizer_coef=c["penalizer_gg"])
    ggf.fit(rep["frequency"], rep["monetary_value"])
    return bgf, ggf


def predict_clv(bgf: BetaGeoFitter, ggf: GammaGammaFitter, summary: pd.DataFrame,
                horizon_days: float) -> pd.DataFrame:
    """Expected purchases, avg order value (GG; population mean for one-time buyers), CLV.

    Returns frame indexed like `summary` with pred_purchases, pred_avg_value, pred_clv,
    p_alive.
    """
    out = pd.DataFrame(index=summary.index)
    f, r, t = summary["frequency"], summary["recency"], summary["T"]
    out["pred_purchases"] = bgf.conditional_expected_number_of_purchases_up_to_time(horizon_days, f, r, t)
    n_nan = int(out["pred_purchases"].isna().sum())
    if n_nan:
        log.warning("BG/NBD returned NaN for %d customers (numerical); filled with 0", n_nan)
        out["pred_purchases"] = out["pred_purchases"].fillna(0.0)
    out["p_alive"] = bgf.conditional_probability_alive(f, r, t)
    rep = (f > 0) & (summary["monetary_value"] > 0)
    avg = pd.Series(np.nan, index=summary.index)
    avg[rep] = ggf.conditional_expected_average_profit(f[rep], summary.loc[rep, "monetary_value"])
    avg = avg.fillna(avg[rep].mean())
    out["pred_avg_value"] = avg
    out["pred_clv"] = out["pred_purchases"] * out["pred_avg_value"]
    return out


def holdout_actuals(hold_sales: pd.DataFrame, index: pd.Index) -> pd.DataFrame:
    """Actual holdout purchase days and spend per customer (0 when absent), aligned to index."""
    h = hold_sales.copy()
    h["day"] = h["invoice_date"].dt.normalize()
    purchases = h.groupby("customer_id")["day"].nunique()
    spend = h.groupby("customer_id")["revenue"].sum()
    return pd.DataFrame({"actual_purchases": purchases.reindex(index).fillna(0.0),
                         "actual_spend": spend.reindex(index).fillna(0.0)})


def historical_baseline(cal_sales: pd.DataFrame, index: pd.Index, window_days: float,
                        horizon_days: float) -> pd.DataFrame:
    """Naive baseline: each customer's calibration purchase-day / spend rate, extrapolated."""
    c = cal_sales.copy()
    c["day"] = c["invoice_date"].dt.normalize()
    pur = c.groupby("customer_id")["day"].nunique().reindex(index).fillna(0.0)
    spend = c.groupby("customer_id")["revenue"].sum().reindex(index).fillna(0.0)
    return pd.DataFrame({"base_purchases": pur / window_days * horizon_days,
                         "base_spend": spend / window_days * horizon_days})


def _spearman(a: pd.Series, b: pd.Series) -> float:
    """Spearman rho, NaN-safe."""
    v = spearmanr(a, b).statistic
    return float(v) if np.isfinite(v) else 0.0


def evaluate(pred: pd.DataFrame, act: pd.DataFrame, base: pd.DataFrame, n_deciles: int = 10) -> dict:
    """MAE / Spearman vs actual holdout for model and baseline, plus top-decile concentration."""
    m = {}
    for name, p_pur, p_sp in (("model", pred["pred_purchases"], pred["pred_clv"]),
                              ("baseline_hist", base["base_purchases"], base["base_spend"])):
        m[name] = {
            "mae_spend": float((p_sp - act["actual_spend"]).abs().mean()),
            "mae_purchases": float((p_pur - act["actual_purchases"]).abs().mean()),
            "spearman_spend": _spearman(p_sp, act["actual_spend"]),
            "spearman_purchases": _spearman(p_pur, act["actual_purchases"]),
            "total_pred_spend": float(p_sp.sum()),
        }
    m["naive_mean"] = {"mae_spend": float((act["actual_spend"].mean() - act["actual_spend"]).abs().mean()),
                       "note": "predict the population mean spend for everyone"}
    m["actual_total_spend"] = float(act["actual_spend"].sum())
    n_top = max(1, len(pred) // n_deciles)
    top = pred["pred_clv"].sort_values(ascending=False).index[:n_top]
    m["top_decile"] = {
        "share_of_predicted_clv": float(pred.loc[top, "pred_clv"].sum() / pred["pred_clv"].sum()),
        "share_of_actual_holdout_spend": float(act.loc[top, "actual_spend"].sum()
                                               / act["actual_spend"].sum()),
        "share_of_actual_spend_oracle_top_decile": float(
            act["actual_spend"].sort_values(ascending=False).iloc[:n_top].sum()
            / act["actual_spend"].sum()),
    }
    top_b = base["base_spend"].sort_values(ascending=False).index[:n_top]
    m["top_decile"]["baseline_share_of_actual_holdout_spend"] = float(
        act.loc[top_b, "actual_spend"].sum() / act["actual_spend"].sum())
    return m


def calibration_table(summary: pd.DataFrame, pred: pd.DataFrame, act: pd.DataFrame,
                      max_freq: int = 7) -> pd.DataFrame:
    """Mean predicted vs actual holdout purchases by calibration-period frequency bucket."""
    d = pd.DataFrame({"freq": summary["frequency"].clip(upper=max_freq),
                      "pred": pred["pred_purchases"], "actual": act["actual_purchases"]})
    g = d.groupby("freq").agg(n=("pred", "size"), predicted=("pred", "mean"), actual=("actual", "mean"))
    return g.reset_index()


def run_clv(cal: pd.DataFrame, hold: pd.DataFrame, cfg: dict | None = None) -> dict:
    """End-to-end CLV: fit on calibration, validate on holdout, score 12-month CLV."""
    cfg = cfg or load_config()
    cutoff = pd.Timestamp(cfg["data"]["calibration_end"])
    hold_end = pd.Timestamp(cfg["data"]["holdout_end"])
    horizon = float((hold_end - cutoff).days)
    summ = calibration_summary(cal, cutoff)
    bgf, ggf = fit_models(summ, cfg)
    pred_h = predict_clv(bgf, ggf, summ, horizon)
    act = holdout_actuals(hold, summ.index)
    window = float((cutoff - cal["invoice_date"].min().normalize()).days + 1)
    base = historical_baseline(cal, summ.index, window, horizon)
    metrics = evaluate(pred_h, act, base, cfg["clv"]["decile_count"])
    metrics["horizon_days"] = horizon
    metrics["n_customers"] = len(summ)
    metrics["bgnbd_params"] = {k: float(v) for k, v in bgf.params_.items()}
    metrics["gg_params"] = {k: float(v) for k, v in ggf.params_.items()}
    metrics["freq_monetary_corr"] = float(
        summ.loc[summ["frequency"] > 0, ["frequency", "monetary_value"]].corr().iloc[0, 1])
    pred_12m = predict_clv(bgf, ggf, summ, float(cfg["clv"]["horizon_days_clv"]))
    n_top = max(1, len(pred_12m) // cfg["clv"]["decile_count"])
    metrics["clv_12m_top_decile_share"] = float(
        pred_12m["pred_clv"].nlargest(n_top).sum() / pred_12m["pred_clv"].sum())
    metrics["clv_12m_total"] = float(pred_12m["pred_clv"].sum())
    table = summ.join(pred_12m.add_prefix("m12_")).join(pred_h.add_prefix("h_")).join(act).join(base)
    table["clv_decile"] = pd.qcut(table["m12_pred_clv"].rank(method="first"), cfg["clv"]["decile_count"],
                                  labels=False) + 1
    return {"summary": summ, "bgf": bgf, "ggf": ggf, "pred_holdout": pred_h, "pred_12m": pred_12m,
            "actuals": act, "baseline": base, "metrics": metrics, "table": table.reset_index(),
            "calibration": calibration_table(summ, pred_h, act)}
