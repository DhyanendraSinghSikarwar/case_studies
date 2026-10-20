"""Streamlit app: churn risk, uplift, policy simulator, Hillstrom (real RCT), About.

Reads PRECOMPUTED artefacts from outputs/ (run ``python tasks.py all`` first); nothing is retrained here.
Set CHURNX_ROOT to point at another project root (used by the tests).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(os.environ.get("CHURNX_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from churnx.policy import policy_table, select_policies  # noqa: E402
from churnx.snapshot import customer_value_inr  # noqa: E402
from churnx.threshold import expected_profit, sweep_thresholds  # noqa: E402

OUT = ROOT / "outputs"
FIG = ROOT / "figures"
LIMITS = ("Data: UCI Online Retail II (real, UK gift retailer, 2009-2011). Treatment effects in the pilot are "
          "SIMULATED; Hillstrom is a real RCT for a different business. Margin / cost / FX are assumptions.")

st.set_page_config(page_title="Churn + Uplift Retention", layout="wide")


@st.cache_data
def load_json(name: str) -> dict:
    """Load outputs/<name> JSON ({} if missing)."""
    p = OUT / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


@st.cache_data
def load_csv(name: str) -> pd.DataFrame | None:
    """Load outputs/<name> CSV (None if missing)."""
    p = OUT / name
    return pd.read_csv(p) if p.exists() else None


summary = load_json("summary.json")
cohort = load_csv("test_cohort.csv")
if not summary or cohort is None:
    st.error("No precomputed outputs found. Run `python tasks.py all` first.")
    st.stop()

biz = summary["assumptions"]
st.title("Who should get the retention offer?")
st.caption(LIMITS)
tab_risk, tab_uplift, tab_policy, tab_hill, tab_about = st.tabs(
    ["Churn risk", "Uplift", "Policy simulator", "Hillstrom (real RCT)", "About"])

# ------------------------------------------------------------------ Churn risk
with tab_risk:
    ch = summary["churn"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Champion test AUC", f"{ch['test_auc']:.3f}", help=f"champion = {ch['champion']}; target 0.75")
    c2.metric("Mean predicted churn (test)", f"{ch['calibration_gap_test']['mean_pred_calibrated']:.1%}")
    c3.metric("Observed churn (test)", f"{ch['calibration_gap_test']['observed_rate']:.1%}")
    st.dataframe(pd.DataFrame(ch["models_test_auc"], index=["test AUC"]).T.style.format("{:.3f}"))
    lift = load_csv("lift_table.csv")
    if lift is not None:
        st.subheader("Lift by risk decile (test snapshot 2011-08-01)")
        st.bar_chart(lift.set_index("decile")["lift"])
    st.subheader("Cost-optimal threshold (risk-only rule, constant save-rate)")
    s1, s2, s3 = st.columns(3)
    cost = s1.slider("Offer cost (INR)", 50, 10000, int(biz["offer_cost_inr"]), 50, key="r_cost")
    save = s2.slider("Assumed save rate", 0.02, 0.5, float(biz["save_rate"]), 0.01, key="r_save")
    thr = s3.slider("Contact threshold", 0.0, 0.95, 0.30, 0.01, key="r_thr")
    value = customer_value_inr(cohort["monetary_6m"], {**biz, "offer_cost_inr": cost})
    sw = sweep_thresholds(cohort["p_churn"].to_numpy(), value, cost, save, np.linspace(0, 0.95, 96))
    best = sw.sort_values(["profit_inr", "threshold"], ascending=[False, False]).iloc[0]
    sel = cohort["p_churn"] >= thr
    st.write(f"At threshold {thr:.2f}: contact **{int(sel.sum())}** customers, expected profit "
             f"**INR {expected_profit(cohort.loc[sel, 'p_churn'], value[sel.to_numpy()], cost, save).sum():,.0f}**. "
             f"Best threshold: {best['threshold']:.2f} (INR {best['profit_inr']:,.0f}, {int(best['n_contacted'])} contacted).")
    st.line_chart(sw[sw["n_contacted"] > 0].set_index("threshold")["profit_inr"])
    st.subheader("Score table (top 50 by risk)")
    st.dataframe(cohort.sort_values("p_churn", ascending=False).head(50)[
        ["customer_id", "p_churn", "recency_days", "frequency_6m", "monetary_6m", "segment"]], hide_index=True)
    st.caption(LIMITS)

# ------------------------------------------------------------------ Uplift
with tab_uplift:
    up = summary["uplift"]
    st.write(f"Selected learner (grouped-CV Qini on the training pilot): **{up['selected_learner']}**")
    rows = []
    for name, r in up["learners"].items():
        tr = r.get("tau_recovery", {})
        rows.append({"scorer": name, "Qini": r["qini"], "CI low": r["qini_ci95"][0], "CI high": r["qini_ci95"][1],
                     "% of oracle": r["qini_pct_of_oracle"], "tau corr (Pearson)": tr.get("pearson", np.nan)})
    st.dataframe(pd.DataFrame(rows).style.format(precision=2), hide_index=True)
    q = load_csv("qini_curves.csv")
    if q is not None:
        st.subheader("Qini curves (simulated pilot, test cohort)")
        st.line_chart(q.rename(columns={q.columns[0]: "customers"}).set_index("customers"))
    st.caption("Treatment effect is simulated (known tau). With ~1.5k test customers the Qini CIs are wide. " + LIMITS)

# ------------------------------------------------------------------ Policy simulator
with tab_policy:
    p1, p2, p3, p4 = st.columns(4)
    budget = p1.slider("Contact budget (share of customers)", 0.05, 1.0, 0.30, 0.05)
    cost_p = p2.slider("Offer cost (INR)", 50, 10000, int(biz["offer_cost_inr"]), 50, key="p_cost")
    margin = p3.slider("Gross margin", 0.05, 0.6, float(biz["gross_margin"]), 0.05)
    months = p4.slider("CLV horizon (months)", 3, 24, int(biz["clv_months"]), 3)
    b2 = {**biz, "offer_cost_inr": cost_p, "gross_margin": margin, "clv_months": months}
    val = customer_value_inr(cohort["monetary_6m"], b2)
    masks = select_policies(cohort["tau_hat"], cohort["p_churn"], val, budget, cost_p, int(summary["seed"]))
    tab = policy_table(masks, cohort["tau_true"].to_numpy(), val, cost_p)
    st.dataframe(tab.style.format({"profit_inr": "{:,.0f}", "total_offer_cost_inr": "{:,.0f}", "pct_of_oracle": "{:.1f}"}),
                 hide_index=True)
    st.bar_chart(tab.set_index("policy")["profit_inr"])
    risk = float(tab.set_index("policy").loc["risk_top_k", "profit_inr"])
    if risk < 0:
        st.warning("Under these assumptions targeting the highest-risk customers LOSES money.")
    st.caption("Exact profits use the simulator's true tau (Track A, synthetic treatment). " + LIMITS)
    sens = load_csv("policy_sensitivity.csv")
    if sens is not None:
        st.subheader("Pre-computed sensitivity (profit, INR) at base margin / CLV horizon")
        d = sens[(sens["gross_margin"] == biz["gross_margin"]) & (sens["clv_months"] == biz["clv_months"])]
        st.dataframe(d.pivot(index="policy", columns="offer_cost_inr", values="profit_inr").style.format("{:,.0f}"))

# ------------------------------------------------------------------ Hillstrom
with tab_hill:
    h = summary.get("hillstrom", {})
    if "skipped" in h or not h:
        st.info("Hillstrom data was not available when the analysis ran.")
    else:
        st.write(f"Real randomised e-mail experiment, n = {h['n']:,}; evaluated on the held-out half (n = {h['n_test']:,}). "
                 f"Max |standardised covariate difference| between arms: {h['max_abs_std_diff']:.3f}.")
        pol = pd.DataFrame(h["policies"]).T
        pol["CI low"] = pol["ci95"].map(lambda c: c[0])
        pol["CI high"] = pol["ci95"].map(lambda c: c[1])
        st.subheader("IPW profit per 1,000 customers (USD, 95% bootstrap CI)")
        st.dataframe(pol[["n_treated", "profit_per_1000_usd", "CI low", "CI high"]].astype(float).style.format(precision=1))
        lr = [{"outcome": o, "learner": L, "Qini": v["qini"], "CI low": v["qini_ci95"][0], "CI high": v["qini_ci95"][1]}
              for o, d in h["learners"].items() for L, v in d.items()]
        st.subheader("Qini by outcome and learner")
        st.dataframe(pd.DataFrame(lr).style.format(precision=1), hide_index=True)
        st.caption("Intervals that include 0 / overlap mean the data cannot separate the policies.")

# ------------------------------------------------------------------ About
with tab_about:
    st.subheader("Assumptions (config/config.yaml)")
    st.json(biz)
    st.markdown(
        "- **Real:** transactions, features, 90-day churn labels (snapshots 2011-03/04/05 train, 2011-08 test).\n"
        "- **Simulated:** the 50/50 offer pilot (Track A). Baseline outcomes are the real churn labels; the offer's "
        "effect is invented (see docs/SIMULATOR.md). Policy-vs-oracle results hold by construction of the simulator.\n"
        "- **Real treatment data:** Hillstrom e-mail RCT (Track B) with oracle-free IPW evaluation.\n"
        "- Seasonality: churn rate drifts from ~49% to ~28% across snapshots; calibration on the test snapshot is imperfect.")
    for f in sorted(FIG.glob("*.png"))[:3]:
        st.image(str(f))
