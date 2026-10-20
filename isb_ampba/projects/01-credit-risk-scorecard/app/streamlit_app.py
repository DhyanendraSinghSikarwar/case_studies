"""Streamlit app: Score a customer | Portfolio | Cut-off simulator | Model health.

Reads precomputed artefacts (models/*.joblib, outputs/*.csv|json); nothing is trained here.
Run:  python tasks.py app   (or: streamlit run app/streamlit_app.py)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import joblib  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from credit import economics as eco  # noqa: E402
from credit import explain  # noqa: E402
from credit import scorecard as sc  # noqa: E402
from credit.config import load_config  # noqa: E402
from credit.data import RAW_FEATURES, TARGET  # noqa: E402
from credit.features import add_features  # noqa: E402
from credit.models import predict_pd  # noqa: E402

CFG = load_config()
OUT, MODELS = ROOT / CFG["paths"]["outputs"], ROOT / CFG["paths"]["models"]
LIMITATIONS = ("Limitations: Taiwan 2005 data, random split (no out-of-time test), margin / LGD / limit-action effects "
               "are assumptions, SEX is never a model input.")

st.set_page_config(page_title="Credit Risk Scorecard", layout="wide")


@st.cache_resource
def load_bundle(name: str) -> dict:
    """Load a joblib model bundle once per session."""
    return joblib.load(MODELS / f"{name}.joblib")


@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    """Load an outputs/ CSV once."""
    return pd.read_csv(OUT / name)


@st.cache_data
def load_json(name: str) -> dict:
    """Load an outputs/ JSON once."""
    with open(OUT / name, encoding="utf-8") as fh:
        return json.load(fh)


@st.cache_data
def sample_rows() -> pd.DataFrame:
    """Real-data sample used to prefill the form."""
    return pd.read_csv(ROOT / "tests" / "fixtures" / "uci350_sample.csv")


st.title("Credit Risk Scorecard and Credit-Limit Engine")
if not (OUT / "summary.json").exists() or not (MODELS / "xgb.joblib").exists():
    st.error("Artefacts missing. Run `python tasks.py train` then `python tasks.py evaluate` first.")
    st.stop()

summary, metrics = load_json("summary.json"), load_json("metrics.json")
champion = metrics["champion"]
scfg = CFG["scorecard"]
tab1, tab2, tab3, tab4 = st.tabs(["Score a customer", "Portfolio", "Cut-off simulator", "Model health"])

with tab1:
    st.subheader("Score a customer")
    rows = sample_rows()
    idx = st.number_input("Prefill from sample row", 0, len(rows) - 1, 0, key="row_idx")
    base = rows.iloc[int(idx)]
    inputs: dict[str, float] = {}
    with st.form("customer"):
        cols = st.columns(4)
        feats = [c for c in RAW_FEATURES if c != "SEX"]                  # SEX is never a model input
        for i, c in enumerate(feats):
            inputs[c] = cols[i % 4].number_input(c, value=int(base[c]), step=1, key=f"in_{c}_{int(idx)}")
        submitted = st.form_submit_button("Score")
    row = pd.DataFrame([{**inputs, "SEX": int(base["SEX"]), TARGET: 0}])
    feat_row = add_features(row)
    bundle = load_bundle(champion)
    fcols = bundle["features"]
    pd_hat = float(predict_pd(bundle["model"], feat_row[fcols], bundle["calibrator"])[0])
    score = float(sc.pd_to_score(pd_hat, scfg["base_score"], scfg["base_odds"], scfg["pdo"], tuple(scfg["clip"])))
    band = str(sc.assign_band([pd_hat], scfg["band_pd_edges"])[0])
    act = eco.limit_action(band, CFG["limits"])
    approve = pd_hat <= summary["opt_cutoff"]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("PD (next month)", f"{pd_hat:.1%}")
    m2.metric("Score (300-900)", f"{score:.0f}")
    m3.metric("Risk band", band)
    m4.metric("Decision", "Approve" if approve else "Decline", help=f"Optimal cut-off PD <= {summary['opt_cutoff']:.2f}")
    st.write(f"**Limit action:** {act['action']} ({act['limit_change']:+.0%} of current limit)")
    sv = explain.shap_values(bundle["model"], feat_row[fcols])[0]
    reasons = explain.reason_codes(feat_row.iloc[0], sv, fcols)
    st.write("**Top reasons raising risk:**")
    for r in reasons or ["No factor materially increases risk for this customer."]:
        st.write(f"- {r}")
    st.caption(LIMITATIONS)

with tab2:
    st.subheader("Portfolio (test set)")
    pred = load_csv("test_predictions.csv")
    st.bar_chart(pd.cut(pred["score"], 30).value_counts().sort_index().rename(lambda i: f"{i.left:.0f}"))
    st.write("Band table")
    st.dataframe(load_csv("band_table.csv"), hide_index=True)
    curve = load_csv("profit_curve.csv")
    st.write("Approval rate vs bad rate among approved, by cut-off")
    st.line_chart(curve.set_index("approval_rate")[["bad_rate_approved"]])
    st.caption(LIMITATIONS)

with tab3:
    st.subheader("Cut-off simulator")
    pred = load_csv("test_predictions.csv")
    c1, c2 = st.columns(2)
    lgd = c1.slider("LGD", 0.30, 0.95, float(CFG["economics"]["lgd"]), 0.01)
    margin = c2.slider("Margin", 0.05, 0.35, float(CFG["economics"]["margin"]), 0.01)
    ead = eco.make_ead(pred["LIMIT_BAL"], pred["avg_util"], CFG["economics"]["fx_ntd_inr"])
    cur = eco.profit_curve(pred["pd"], ead, pred["y"], margin, lgd, eco.cutoff_grid(CFG))
    best = eco.find_optimal_cutoff(cur)
    all_in = float(eco.unit_profit(pred["pd"], ead, margin, lgd).sum())
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Optimal cut-off (PD)", f"{best['cutoff']:.2f}")
    k2.metric("Approval rate", f"{best['approval_rate']:.1%}")
    k3.metric("Expected profit (INR mn)", f"{best['exp_profit'] / 1e6:,.1f}")
    k4.metric("Uplift vs approve-all (INR mn)", f"{(best['exp_profit'] - all_in) / 1e6:,.1f}")
    st.line_chart(cur.set_index("cutoff")[["exp_profit", "real_profit"]])
    st.caption(f"Break-even PD = margin / (margin + LGD) = {margin / (margin + lgd):.3f}. " + LIMITATIONS)

with tab4:
    st.subheader("Model health")
    st.write("Feature drift: -20% LIMIT_BAL simulation (alert at PSI > 0.2)")
    st.dataframe(load_csv("csi_drift_sim.csv").head(12), hide_index=True)
    st.write("Test vs train (no drift)")
    st.dataframe(load_csv("csi_test_vs_train.csv").head(8), hide_index=True)
    cal = load_csv("calibration_table.csv")
    st.write("Calibration (test deciles): predicted vs observed")
    st.line_chart(cal.set_index("mean_pred")[["obs_rate"]])
    st.write("Lift deciles")
    st.dataframe(load_csv("decile_table.csv"), hide_index=True)
    st.caption(LIMITATIONS)
