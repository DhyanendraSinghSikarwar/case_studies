"""Promotion Cannibalisation Engine - Streamlit app (reads precomputed artifacts from outputs/)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
import streamlit as st  # noqa: E402

from promo.config import load_config  # noqa: E402
from promo.engine import EngineContext  # noqa: E402
from promo.sweep import parametric_scores  # noqa: E402
from promo.viz import waterfall_plotly  # noqa: E402

OUT = Path(os.environ.get("PROMO_OUT_DIR", ROOT / "outputs"))
st.set_page_config(page_title="Promotion Cannibalisation Engine", layout="wide")


@st.cache_data(show_spinner=False)
def load_artifacts() -> tuple[pd.DataFrame, dict, pd.DataFrame, dict]:
    """Engine table, summary.json, promo plan, config (all precomputed; nothing is retrained here)."""
    table = pd.read_parquet(OUT / "engine_inputs.parquet")
    summary = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
    plan = pd.read_csv(OUT / "promo_plan.csv", dtype={"stock_code": str})
    return table, summary, plan, load_config()


def money(x: float) -> str:
    """Format GBP."""
    return f"-£{abs(x):,.0f}" if x < 0 else f"£{x:,.0f}"


st.title("Promotion Cannibalisation Engine")
st.caption("Data: UCI Online Retail II (UK gift-ware retailer, 2009-12 to 2011-12). Margin and promotions are "
           "ASSUMPTIONS / inferences (the data has no costs and no promo flags). Elasticities are associations, not causal.")

if not (OUT / "summary.json").exists() or not (OUT / "engine_inputs.parquet").exists():
    st.error("Artifacts missing. Run `python tasks.py all` first.")
    st.stop()

table, summary, plan, cfg = load_artifacts()
ctx = EngineContext(table.copy(), cfg)
act = ctx.table[ctx.table["active"]].sort_values("revenue", ascending=False).head(600)
labels = {f"{s} - {str(r['description'])[:45]}": s for s, r in act.iterrows()}

with st.sidebar:
    st.header("Promotion")
    sku = labels[st.selectbox("SKU", list(labels), key="sku")]
    levels = [d for d in cfg["optimiser"]["discounts"] if d > 0]
    disc = st.select_slider("Discount", options=levels, value=cfg["reference"]["discount"], format_func=lambda d: f"{d:.0%}", key="disc")
    st.header("Assumption overrides")
    row = ctx.table.loc[sku]
    eps = st.slider("Own-price elasticity", -12.0, -0.5, float(np.clip(row["eps"], -12, -0.5)), 0.1, key=f"eps_{sku}",
                    help=f"Default = engine estimate (source: {row['eps_source']})")
    margin = st.slider("Unit margin (assumed)", 0.10, 0.70, float(1 - cfg["engine"]["unit_cost_share"]), 0.01, key="margin")
    halo_f = st.slider("Halo factor (share of basket pull that is incremental)", 0.0, 1.0, float(cfg["engine"]["halo_factor"]), 0.05, key="halo")
    outside = st.slider("Outside share (no purchase from family)", 0.05, 0.90, float(cfg["demand"]["outside_share"]), 0.05, key="outside")

res = ctx.score(sku, disc, eps=eps, margin=margin, halo_factor=halo_f, outside_share=outside)
be = ctx.break_even(sku, disc, margin=margin, halo_factor=halo_f, outside_share=outside)

tab1, tab2, tab3, tab4 = st.tabs(["Waterfall", "Sensitivity", "Family view", "Promo plan"])

with tab1:
    st.subheader(f"{row['description']} - {disc:.0%} off for {cfg['engine']['promo_weeks']} weeks")
    c = st.columns(5)
    c[0].metric("Promoted-only", money(res["promoted_only"]))
    c[1].metric("Family net", money(res["family_net"]), delta=money(res["family_net"] - res["promoted_only"]) + " vs promoted-only")
    c[2].metric("Incremental units", f"{res['incremental_units']:,.0f}")
    c[3].metric("Elasticity used", f"{eps:.2f}")
    c[4].metric("Break-even elasticity", "n/a" if not np.isfinite(be) else f"{be:.2f}")
    st.plotly_chart(waterfall_plotly(res), width="stretch", key="waterfall")
    verdict = "profitable" if res["family_net"] > 0 else "NOT profitable"
    trap = res["promoted_only"] > 0 >= res["family_net"]
    st.write(f"Family view: **{verdict}**." + (" This is a **dashboard trap**: the promoted SKU looks profitable, the family is not." if trap else ""))
    st.caption(f"Elasticity source: {row['eps_source']}. Family has {len(res['members'])} active members; "
               f"substitution weight {row['sub_weight']:.2f} ({'weak-substitute family, cannibalisation capped' if row['weak_sub'] else 'normal'}).")

with tab2:
    st.subheader("Parametric engine with sliders (normalised per unit of baseline sales)")
    ratio = summary["sweep"]["halo_ref_ratio"]
    sw = cfg["sweep"]
    c = st.columns(4)
    s_eps = c[0].slider("Elasticity", float(sw["elasticity"][0]), float(sw["elasticity"][1]), -3.0, 0.1, key="s_eps")
    s_sub = c[1].slider("Substitution share", float(sw["substitution_share"][0]), float(sw["substitution_share"][1]), 0.4, 0.05, key="s_sub")
    s_mar = c[2].slider("Margin", float(sw["margin"][0]), float(sw["margin"][1]), 0.40, 0.01, key="s_mar")
    s_hal = c[3].slider("Halo", float(sw["halo"][0]), float(sw["halo"][1]), 0.5, 0.05, key="s_hal")
    p0 = parametric_scores(s_eps, s_sub, s_mar, s_hal, disc, ratio)
    m1, m2 = st.columns(2)
    m1.metric("Promoted-only (per unit baseline sales)", f"{float(p0['promoted_only']):+.3f}")
    m2.metric("Family net (per unit baseline sales)", f"{float(p0['family_net']):+.3f}")
    grid = np.linspace(min(sw["elasticity"]), max(sw["elasticity"]), 60)
    pg = parametric_scores(grid, s_sub, s_mar, s_hal, disc, ratio)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=grid, y=pg["promoted_only"], name="promoted-only"))
    fig.add_trace(go.Scatter(x=grid, y=pg["family_net"], name="family net"))
    fig.add_hline(y=0, line_color="black")
    fig.update_layout(xaxis_title="elasticity", yaxis_title="contribution per unit baseline sales", height=380, margin=dict(t=20))
    st.plotly_chart(fig, width="stretch", key="sens_line")
    w = summary["sweep"]
    st.write(f"Over {w['n_draws']:,} Latin-hypercube draws at {w['discount']:.0%} off: promoted-only profitable in "
             f"**{w['pct_promoted_only_profitable']:.1f}%**, family net in **{w['pct_family_profitable']:.1f}%**, "
             f"dashboard trap **{w['pct_dashboard_trap']:.1f}%**; median break-even elasticity {w['break_even_elasticity_median']:.2f}.")
    st.dataframe(pd.DataFrame(summary["tornado"])[["param", "low_value", "high_value", "net_at_low", "net_at_high", "pct_profitable_lower_half", "pct_profitable_upper_half"]],
                 width="stretch", hide_index=True)

with tab3:
    st.subheader(f"Family: {row['family_name']}")
    names = [str(ctx.table.at[m, "description"]) for m in res["members"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=names, y=res["baseline_units"], name="baseline"))
    fig.add_trace(go.Bar(x=names, y=res["units_after"], name="promoted"))
    fig.update_layout(barmode="group", yaxis_title="weekly units", height=380, margin=dict(t=20))
    st.plotly_chart(fig, width="stretch", key="family_units")
    df = pd.DataFrame({"SKU": res["members"], "Description": names, "Price": res["prices"], "Baseline units/wk": res["baseline_units"],
                       "Promoted units/wk": res["units_after"], "Change": res["units_after"] - res["baseline_units"]})
    st.dataframe(df.round(2), width="stretch", hide_index=True)
    st.caption("Substitution follows a multinomial logit with an outside option (IIA): siblings lose units in proportion to their share.")

with tab4:
    o = summary["optimiser"]
    st.subheader(f"Recommended {o['horizon_weeks']}-week promo plan (budget {money(o['budget_gbp'])})")
    if plan.empty:
        st.info("The optimiser recommends no discounts under the current assumptions.")
    else:
        st.dataframe(plan[["week", "family_name", "description", "discount", "family_net", "subsidy"]].round(2), width="stretch", hide_index=True)
    c = st.columns(3)
    c[0].metric("Optimiser family net", money(o["calendar"]["family_net"]))
    c[1].metric("Dashboard-ranked plan", money(o["dashboard_promoted_only_rank"]["family_net"]))
    c[2].metric("Top-revenue plan", money(o["top_revenue_rank"]["family_net"]))
    st.caption("Plan values are scaled by a seasonal index from the same weeks a year earlier; one promo per family; "
               f"at most {o['max_promos_per_week']} promos per week; one week of zero index = Christmas shutdown in the data.")
