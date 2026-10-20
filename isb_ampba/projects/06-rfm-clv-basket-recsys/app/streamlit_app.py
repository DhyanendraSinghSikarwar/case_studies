"""Streamlit app: segment explorer, Customer 360, bundle finder, campaign planner.

Reads precomputed artifacts from outputs/ (override with env CRM_OUTPUTS). No retraining here.
"""
from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from crm.campaign import allocate_budget, segment_economics
from crm.config import load_config

CAPTION = ("Data: UCI Online Retail II (customer-identified sales, UK wholesale gift retailer), "
           "segments/CLV as of 2011-06-30, recommender trained to 2011-11-09. Limitations: ~5k "
           "customers, heavy-tailed spend, campaign uplifts are config assumptions, not measured.")


def out_dir() -> Path:
    """Artifact directory."""
    return Path(os.environ.get("CRM_OUTPUTS", ROOT / "outputs"))


@st.cache_data
def load_artifacts(path: str) -> dict:
    """Load all CSV/JSON artifacts once."""
    p = Path(path)
    d = {n: pd.read_csv(p / f"{n}.csv") for n in
         ("customers", "segment_summary", "cluster_profile", "bundles", "recommendations", "products")}
    d["metrics"] = json.loads((p / "metrics.json").read_text(encoding="utf-8"))
    return d


def main() -> None:
    """Render the app."""
    st.set_page_config(page_title="CRM analytics", layout="wide")
    st.title("Customer segmentation, CLV, bundles and recommendations")
    try:
        art = load_artifacts(str(out_dir()))
    except FileNotFoundError:
        st.error("Artifacts not found in outputs/. Run `python tasks.py train` first.")
        st.stop()
    cust, cfg = art["customers"], load_config()
    t1, t2, t3, t4 = st.tabs(["Segment explorer", "Customer 360", "Bundle finder", "Campaign planner"])

    with t1:
        by = st.radio("Colour by", ["segment", "cluster_name"], horizontal=True)
        if "emb_x" in cust:
            x, y, method = "emb_x", "emb_y", art["metrics"]["cluster"].get("embedding_method", "2D")
            d = cust
        else:
            d = cust.assign(x=np.log1p(cust["frequency"]), y=np.log1p(cust["monetary"]))
            x, y, method = "x", "y", "log frequency vs log monetary"
        st.caption(f"2D map: {method}")
        chart = alt.Chart(d).mark_circle(size=18, opacity=0.6).encode(
            x=alt.X(x, title=None), y=alt.Y(y, title=None), color=by,
            tooltip=["customer_id", "segment", "cluster_name", "recency", "frequency", "monetary"])
        st.altair_chart(chart.interactive(), use_container_width=True)
        st.subheader("Rule segment profile cards")
        seg = art["segment_summary"]
        cols = st.columns(len(seg))
        for c, (_, r) in zip(cols, seg.iterrows(), strict=True):
            c.metric(r["segment"], f"{int(r['customers']):,} customers",
                     f"{r['revenue_share']:.0%} of revenue", delta_color="off")
            c.caption(f"R {r['recency']:.0f}d - F {r['frequency']:.1f} - M {r['monetary']:,.0f}")
        st.subheader("Behavioural clusters (KMeans)")
        st.dataframe(art["cluster_profile"].round(2), use_container_width=True)
        st.caption(CAPTION)

    with t2:
        cid = st.selectbox("Customer ID", cust["customer_id"].tolist())
        c = cust[cust["customer_id"] == cid].iloc[0]
        a, b, cc, dd = st.columns(4)
        a.metric("Segment", c["segment"])
        b.metric("Cluster", c["cluster_name"])
        cc.metric("12-month CLV", f"{c['m12_pred_clv']:,.0f}")
        dd.metric("P(alive)", f"{c['m12_p_alive']:.0%}")
        st.write(f"RFM code **{c['rfm_code']}** - recency {c['recency']:.0f} days, frequency "
                 f"{int(c['frequency'])} orders, monetary {c['monetary']:,.0f}, avg basket "
                 f"{c['avg_basket']:,.0f}, CLV decile {int(c['clv_decile'])}/10")
        mode = st.radio("Recommendations", ["reorder_or_new", "discovery"], horizontal=True)
        rec = art["recommendations"]
        rec = rec[(rec["customer_id"] == cid) & (rec["mode"] == mode)].sort_values("rank")
        st.dataframe(rec[["rank", "stock_code", "description"]], hide_index=True)
        st.caption(CAPTION)

    with t3:
        bun = art["bundles"]
        st.dataframe(bun[["rank", "bundle", "support", "confidence", "lift"]], hide_index=True,
                     use_container_width=True)
        names = art["products"].set_index("stock_code")["description"].to_dict()
        codes = sorted({i for s in bun["items"] for i in s.split(",")}, key=lambda i: names.get(str(i), str(i)))
        pick = st.selectbox("Find bundles containing", codes,
                            format_func=lambda i: f"{names.get(str(i), i)} ({i})")
        hit = bun[bun["items"].apply(lambda s: str(pick) in s.split(","))]
        st.dataframe(hit[["rank", "bundle", "confidence", "lift"]], hide_index=True)
        st.caption(CAPTION)

    with t4:
        st.write("Edit assumptions; economics are recomputed from the segment table (no retraining).")
        c1, c2, c3 = st.columns(3)
        mult = c1.slider("Response-rate multiplier", 0.25, 2.0, 1.0, 0.05)
        margin = c2.slider("Gross margin", 0.10, 0.60, float(cfg["campaign"]["gross_margin"]), 0.01)
        budget = c3.number_input("Budget", 0.0, 1e7, float(cfg["campaign"]["total_budget_gbp"]), 500.0)
        econ = segment_economics(cust, copy.deepcopy(cfg), response_mult=mult, margin=margin)
        plan = allocate_budget(econ, budget)
        show = ["segment", "action", "customers", "funded_fraction", "total_cost", "incremental_revenue",
                "net_profit", "roi"]
        st.dataframe(plan[show].round(2), hide_index=True, use_container_width=True)
        f_cost, f_net = plan["funded_total_cost"].sum(), plan["funded_net_profit"].sum()
        m1, m2, m3 = st.columns(3)
        m1.metric("Funded cost", f"{f_cost:,.0f}")
        m2.metric("Funded net profit", f"{f_net:,.0f}")
        m3.metric("Funded ROI", f"{(f_net / f_cost) if f_cost else 0:.2f}")
        st.caption(CAPTION)


main()
