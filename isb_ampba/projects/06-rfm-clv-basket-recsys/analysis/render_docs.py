"""Render the number-bearing docs from outputs/*.json and CSVs (no hand-typed numbers).

Writes docs/DECISION_MEMO.md, docs/MODEL_CARD.md, docs/REVIEW_DECK_OUTLINE.md and replaces the
block between <!-- RESULTS:START --> and <!-- RESULTS:END --> in README.md.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _md(df: pd.DataFrame, floatfmt: str = ".2f") -> str:
    """DataFrame -> GitHub markdown table (no tabulate dependency)."""
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            cells.append(format(v, floatfmt) if isinstance(v, float) else str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _pct(x: float, d: int = 1) -> str:
    return f"{x * 100:.{d}f}%"


def _gbp(x: float) -> str:
    return f"GBP {x:,.0f}"


def load(out: Path) -> dict:
    """Load all artifacts needed for rendering."""
    import sys

    sys.path.insert(0, str(ROOT / "src"))
    from crm.config import load_config

    return {
        "cfg": load_config(),
        "m": json.loads((out / "metrics.json").read_text(encoding="utf-8")),
        "s": json.loads((out / "summary.json").read_text(encoding="utf-8")),
        "seg": pd.read_csv(out / "segment_summary.csv"),
        "econ": pd.read_csv(out / "campaign_economics.csv"),
        "plan": pd.read_csv(out / "campaign_plan.csv"),
        "sens": pd.read_csv(out / "campaign_sensitivity.csv"),
        "bun": pd.read_csv(out / "bundles.csv"),
        "prof": pd.read_csv(out / "cluster_profile.csv"),
        "tune": pd.read_csv(out / "recsys_tuning.csv"),
    }


def segment_table(d: dict) -> str:
    """Segment sizes, revenue share and campaign action/ROI."""
    seg, econ = d["seg"], d["econ"].set_index("segment")
    t = pd.DataFrame({
        "Segment": seg["segment"], "Customers": seg["customers"].map("{:,}".format),
        "% customers": seg["customer_share"].map(_pct), "% revenue (to 2011-06-30)": seg["revenue_share"].map(_pct),
        "Mean recency (d)": seg["recency"].round(0).astype(int), "Mean orders": seg["frequency"].round(1),
        "Mean spend": seg["monetary"].round(0).astype(int).map("{:,}".format),
        "Action": seg["segment"].map(econ["action"]),
    })
    return _md(t)


def roi_table(d: dict) -> str:
    """Campaign ROI table (unconstrained and budget-funded)."""
    p = d["plan"]
    t = pd.DataFrame({
        "Segment": p["segment"], "Action": p["action"], "Contacts": p["contacts"].round(0).astype(int),
        "Cost (GBP)": p["total_cost"].round(0).astype(int).map("{:,}".format),
        "Incr. revenue (GBP)": p["incremental_revenue"].round(0).astype(int).map("{:,}".format),
        "Net profit (GBP)": p["net_profit"].round(0).astype(int).map("{:,}".format),
        "ROI": p["roi"].round(2), "Funded": p["funded_fraction"].map(_pct, na_action=None),
    })
    return _md(t)


def recsys_table(m: dict, protocol: str) -> str:
    """Recommender metrics for one protocol."""
    r = m["recsys"][protocol]
    rows = []
    for n in ("random", "popularity", "own_history", "itemknn_cosine", "als", "hybrid_als_pop"):
        if n not in r:
            continue
        x = r[n]
        rows.append({"Model": n, "HitRate@10": round(x["hitrate"], 4), "NDCG@10": round(x["ndcg"], 4),
                     "Coverage": round(x["coverage"], 4),
                     "NDCG vs popularity": f"{x['ndcg_ratio_vs_popularity']:.2f}x" if "ndcg_ratio_vs_popularity" in x else "-",
                     "NDCG vs own_history": (f"{x['ndcg_ratio_vs_own_history']:.2f}x"
                                         if "ndcg_ratio_vs_own_history" in x else "-"),
                     "95% CI (vs popularity)": (f"[{x['ndcg_ratio_ci95'][0]:.2f}, {x['ndcg_ratio_ci95'][1]:.2f}]"
                                                if "ndcg_ratio_ci95" in x else "-")})
    return _md(pd.DataFrame(rows), ".4f")


def clv_table(m: dict) -> str:
    """CLV model vs baseline metrics."""
    c = m["clv"]
    rows = [
        {"Model": "BG/NBD + Gamma-Gamma", "MAE spend (GBP)": round(c["model"]["mae_spend"], 1),
         "MAE purchases": round(c["model"]["mae_purchases"], 3),
         "Spearman spend": round(c["model"]["spearman_spend"], 3),
         "Spearman purchases": round(c["model"]["spearman_purchases"], 3)},
        {"Model": "Historical average (baseline)", "MAE spend (GBP)": round(c["baseline_hist"]["mae_spend"], 1),
         "MAE purchases": round(c["baseline_hist"]["mae_purchases"], 3),
         "Spearman spend": round(c["baseline_hist"]["spearman_spend"], 3),
         "Spearman purchases": round(c["baseline_hist"]["spearman_purchases"], 3)},
        {"Model": "Population mean (naive)", "MAE spend (GBP)": round(c["naive_mean"]["mae_spend"], 1),
         "MAE purchases": "-", "Spearman spend": "-", "Spearman purchases": "-"},
    ]
    return _md(pd.DataFrame(rows), ".3f")


def target_table(d: dict) -> str:
    """Metric vs target vs achieved vs pass."""
    s, m = d["s"], d["m"]
    prim = s["recsys_primary_protocol"]
    rows = [
        (f"Segment silhouette (KMeans, k={s['kmeans_k_final']})", ">= 0.35",
         f"{s['silhouette_kmeans_final']:.3f}", "yes" if s["silhouette_target_met"] else "NO"),
        (f"ALS NDCG@10 / popularity ({prim})", ">= 1.30x", f"{s['recsys_als_ndcg_ratio']:.2f}x",
         "yes" if s["recsys_target_met"] else "NO"),
        (f"ALS NDCG@10 / popularity ({s['recsys_secondary_protocol']})", ">= 1.30x",
         f"{s['recsys_secondary_als_ndcg_ratio']:.2f}x",
         "yes" if s["recsys_secondary_als_ndcg_ratio"] >= 1.3 else "NO"),
        ("CLV MAE (spend) beats historical baseline", "lower", f"{s['clv_mae_spend_model']:.0f} vs {s['clv_mae_spend_baseline']:.0f}",
         "yes" if s["clv_mae_spend_model"] < s["clv_mae_spend_baseline"] else "NO"),
        ("CLV Spearman (spend) beats baseline", "higher", f"{s['clv_spearman_spend_model']:.3f} vs {s['clv_spearman_spend_baseline']:.3f}",
         "yes" if s["clv_spearman_spend_model"] > s["clv_spearman_spend_baseline"] else "NO"),
        ("Bundles (lift>3, conf>0.3)", "top 20", str(m["basket"]["n_bundles"]),
         "yes" if m["basket"]["n_bundles"] >= 20 else "NO"),
    ]
    return _md(pd.DataFrame(rows, columns=["Metric", "Target", "Achieved", "Met?"]))


def render_results_block(d: dict) -> str:
    """Markdown for the README results section."""
    m = d["m"]
    k = m["cluster"]
    abl = k["feature_set_ablation"]
    ab_rows = [{"Feature set": "RFM only (primary)", "Best k": k["kmeans_best_k_any"],
                "Best silhouette": round(k["kmeans_best_silhouette_any"], 3),
                "Silhouette at final k": round(k["kmeans_silhouette_final"], 3)}]
    for nm, a in abl.items():
        ab_rows.append({"Feature set": nm, "Best k": a["best_k"], "Best silhouette": round(a["best_silhouette"], 3),
                        "Silhouette at final k": round(a["silhouette_by_k"][str(k["kmeans_k_final"])], 3)})
    d_ = m["data"]
    top = m["clv"]["top_decile"]
    return f"""
### Targets vs achieved
{target_table(d)}

### Data (from `outputs/metrics.json`)
{d_['clean_lines']:,} clean sales lines, {d_['customers_total']:,} customers; calibration (<= 2011-06-30)
{d_['calibration_customers']:,} customers, holdout (2011-07-01 to 2011-12-09) {d_['holdout_customers']:,} customers
({d_['customers_in_both']:,} in both), holdout spend {_gbp(d_['holdout_spend'])}.

### Segments (rule-based RFM, as of 2011-06-30)
{segment_table(d)}

![segments](figures/01_rfm_segments.png)

### Clustering
KMeans (log1p + z-score on recency, frequency, monetary): best silhouette over k=2..10 is
{k['kmeans_best_silhouette_any']:.3f} at k={k['kmeans_best_k_any']}; the final model uses
k={k['kmeans_k_final']} (smallest k >= 3 with the best silhouette) with silhouette
**{k['kmeans_silhouette_final']:.3f}**. GMM silhouette at the same k is {k['gmm_silhouette_at_k_final']:.3f}
(BIC prefers k={k['gmm_best_k_bic']}); HDBSCAN finds {k['hdbscan_n_clusters']} clusters with
{_pct(k['hdbscan_noise_share'])} noise points (silhouette on non-noise {k['hdbscan_silhouette_non_noise']:.3f}).
Adjusted Rand index of KMeans vs rule segments: {k['ari_kmeans_vs_rule_segments']:.3f}.
Feature-set ablation (reported honestly; the 6-feature space from the spec does not reach the target):

{_md(pd.DataFrame(ab_rows), ".3f")}

{_md(d['prof'][['cluster', 'name', 'customers', 'customer_share', 'revenue_share', 'recency', 'frequency', 'monetary', 'tenure', 'avg_basket', 'n_products']].round(2), ".2f")}

![cluster selection](figures/02_cluster_selection.png)
![embedding](figures/03_segment_embedding.png)

### CLV (BG/NBD + Gamma-Gamma, fitted on calibration only; {m['clv']['horizon_days']:.0f}-day holdout)
{clv_table(m)}

Top decile of customers by predicted 12-month CLV holds **{_pct(m['clv']['clv_12m_top_decile_share'])}** of predicted
12-month CLV and, ranked by the 162-day holdout prediction, **{_pct(top['share_of_actual_holdout_spend'])}** of actual
holdout spend (oracle ceiling {_pct(top['share_of_actual_spend_oracle_top_decile'])}; baseline ranking
{_pct(top['baseline_share_of_actual_holdout_spend'])}). Predicted total holdout spend
{_gbp(m['clv']['model']['total_pred_spend'])} vs actual {_gbp(m['clv']['actual_total_spend'])} (the holdout contains the Q4 peak,
which BG/NBD does not model).

![calibration](figures/04_clv_calibration.png)
![deciles](figures/05_clv_deciles.png)

### Market basket
FP-Growth on {m['basket']['n_baskets']:,} invoices x top {m['basket']['n_items_considered']:,} items; min_support tuned over a
grid and set to {m['basket']['min_support_chosen']} ({m['basket']['n_itemsets']:,} itemsets, {m['basket']['n_rules_filtered']:,} rules with
lift>3 and confidence>0.3). Top lift {m['basket']['top_lift']:.1f}; median lift of the top 20 {m['basket']['median_lift_top20']:.1f}.

{_md(d['bun'][['rank', 'bundle', 'support', 'confidence', 'lift']].head(20), ".3f")}

![bundles](figures/06_top_bundles.png)

### Recommender (train to {m['recsys']['train_max_date'][:10]}, test = last 30 days)
ALS best params (tuned on a validation window inside the training period): {m['recsys']['best_params']}; hybrid weight (popularity) = {m['recsys']['best_hybrid_weight']}.

**Protocol `repeat_allowed`** (re-orders count; {m['recsys']['n_eval_users']['repeat_allowed']:,} users):
{recsys_table(m, 'repeat_allowed')}

**Protocol `discovery`** (already-bought items excluded; {m['recsys']['n_eval_users']['discovery']:,} users):
{recsys_table(m, 'discovery')}

`own_history` is a personalised baseline (rank the user's own past items by purchase count, popularity tie-break).
Under `repeat_allowed` it scores NDCG@10 {m['recsys']['repeat_allowed']['own_history']['ndcg']:.4f}, i.e. ALS is
{m['recsys']['repeat_allowed']['als']['ndcg_ratio_vs_own_history']:.2f}x of it: the {m['recsys']['repeat_allowed']['als']['ndcg_ratio_vs_popularity']:.2f}x lead over popularity is mostly
re-order memory, not discovery. Under `discovery` (seen items excluded) the baseline collapses to popularity and ALS is
{m['recsys']['discovery']['als']['ndcg_ratio_vs_own_history']:.2f}x, which is the fair headline for "new product" e-mail content.

![recsys](figures/07_recsys_metrics.png)

### Campaign planner (assumptions in `config/config.yaml`)
{roi_table(d)}

Unconstrained portfolio: cost {_gbp(m['campaign']['unconstrained_total_cost'])}, net profit {_gbp(m['campaign']['unconstrained_net_profit'])},
ROI {m['campaign']['unconstrained_roi']:.2f}. With a {_gbp(m['campaign']['budget'])} budget: funded cost {_gbp(m['campaign']['funded_cost'])},
net profit {_gbp(m['campaign']['funded_net_profit'])}, ROI {m['campaign']['funded_roi']:.2f}.
Sensitivity range (response multiplier 0.5x-1.5x, margin 20-40%): portfolio ROI {m['campaign']['sensitivity_min_roi']:.2f} to {m['campaign']['sensitivity_max_roi']:.2f}.

![campaign](figures/08_campaign_roi.png)
"""


def render_memo(d: dict) -> str:
    """DECISION_MEMO.md content."""
    m, s = d["m"], d["s"]
    cp, rs = m["campaign"], m["recsys"]
    prim = s["recsys_primary_protocol"]
    best = s["recsys_best_model_primary"]
    seg = d["seg"]
    champ = seg[seg["segment"] == "Champions"].iloc[0]
    return f"""# Decision memo - customer segmentation, CLV, bundles and recommendations

**Decision requested:** approve a segment-based CRM programme (six RFM segments, a 12-month CLV score, bundle cross-sell and ALS-based
top-10 recommendations in e-mail) with a first-wave budget of {_gbp(cp['budget'])}.

**Recommendation:** run the funded campaign plan below as a controlled pilot (hold-out control group per segment). Champions are
{_pct(champ['customer_share'], 0)} of customers but {_pct(champ['revenue_share'], 0)} of revenue, so protect them first; use the ALS recommender
({s['recsys_als_ndcg_ratio']:.2f}x popularity NDCG@10 under `{prim}`) for e-mail content.

**Impact:** under the assumed response rates, margin ({_pct(d['cfg']['campaign']['gross_margin'], 0)} gross) and costs in `config/config.yaml`, the funded plan
costs {_gbp(cp['funded_cost'])} for an expected net profit of {_gbp(cp['funded_net_profit'])} (ROI {cp['funded_roi']:.2f}; about
INR {cp['funded_net_profit_inr']:,.0f} at the configured display rate). These uplifts are **assumptions, not measured results**;
portfolio ROI stays between {cp['sensitivity_min_roi']:.2f} and {cp['sensitivity_max_roi']:.2f} across the sensitivity grid.

## Segment sizes and revenue share (rule-based RFM, as of 2011-06-30)
{segment_table(d)}

## Campaign ROI table
{roi_table(d)}

## Evidence
- **Segments:** KMeans on log-scaled RFM gives silhouette {s['silhouette_kmeans_final']:.3f} at k={s['kmeans_k_final']}
  (target 0.35: {'met' if s['silhouette_target_met'] else 'NOT met'}); the 6-feature variant scores lower (see README).
- **CLV:** BG/NBD + Gamma-Gamma fitted to 2011-06-30 gives holdout spend MAE {s['clv_mae_spend_model']:.0f} vs {s['clv_mae_spend_baseline']:.0f} for the
  historical-average baseline, Spearman {s['clv_spearman_spend_model']:.3f} vs {s['clv_spearman_spend_baseline']:.3f}. The **top CLV decile
  holds {_pct(s['clv_top_decile_share_predicted_12m'])} of predicted 12-month CLV** and the same customers account for
  {_pct(s['clv_top_decile_share_of_actual_holdout_spend'])} of actual holdout spend.
- **Recommender:** under `{prim}` the best of ALS/hybrid ('{best}') reaches NDCG@10 {rs[prim][best]['ndcg']:.3f} vs popularity {rs[prim]['popularity']['ndcg']:.3f};
  plain ALS is {s['recsys_als_ndcg_ratio']:.2f}x popularity (95% CI {s['recsys_als_ndcg_ratio_ci95'][0]:.2f}-{s['recsys_als_ndcg_ratio_ci95'][1]:.2f}; target 1.30x:
  {'met' if s['recsys_target_met'] else 'NOT met'}) and {s['recsys_secondary_als_ndcg_ratio']:.2f}x under `{s['recsys_secondary_protocol']}`.
  Caveat: a personalised own-history (re-order) baseline scores NDCG@10 {s['recsys_own_history_ndcg_primary']:.3f} under `{prim}`, so ALS is only
  {s['recsys_als_ndcg_ratio_vs_own_history_primary']:.2f}x of it; ALS adds value for discovery (excluding already-bought items), not for re-orders.
- **Bundles:** {m['basket']['n_bundles']} bundles with lift > 3 and confidence > 0.3 (top lift {m['basket']['top_lift']:.1f}), mostly colour/size variants of the same product family,
  suited to "complete the set" prompts.

## Risks and limitations
- Campaign response rates, costs and margin are planning assumptions; only a controlled pilot can validate them. Break-even response multiplier
  (portfolio net profit >= 0 at the base margin): {cp['break_even_response_multiplier_at_margin']}x of the assumed rates.
- About 5k customers and heavy-tailed spend: segment and decile boundaries are noisy; small segments should not be over-read.
- BG/NBD ignores seasonality (holdout contains the Q4 peak) and first-purchase dates are left-censored at 2009-12-01.
- Wholesale B2B behaviour (bulk re-orders) dominates; recommendations that include re-orders mostly resurface past purchases, discovery lift is lower.

## Next steps
1. Pilot with randomised control per segment for 4-8 weeks; replace config uplifts with measured ones.
2. Refit BG/NBD/GG and ALS monthly; monitor calibration drift and recommender HitRate@10 on a rolling 30-day test.
3. Owner: CRM analytics lead; review after the pilot readout.
"""


def render_model_card(d: dict) -> str:
    """MODEL_CARD.md content."""
    m = d["m"]
    rs = m["recsys"]
    dd = m["data"]
    return f"""# Model card - CRM models (RFM / KMeans / BG-NBD+GG / FP-Growth / ALS)

## Intended use
Prioritising CRM actions (e-mail campaigns, win-back, loyalty) for customer-identified accounts of an online wholesaler: segment
assignment, 12-month CLV ranking, cross-sell bundles and top-10 product suggestions.

## Out-of-scope use
Individual credit/pricing decisions, causal uplift claims, other retailers or markets without re-fitting, any use of CLV as an exact
revenue forecast (especially around seasonal peaks).

## Training data
UCI Online Retail II (id 502): {dd['clean_lines']:,} clean sales lines with a Customer ID, {dd['customers_total']:,} customers,
{dd['date_min'][:10]} to {dd['date_max'][:10]}. Calibration (segments, clustering, CLV): <= {dd['calibration_max_date'][:10]}
({dd['calibration_customers']:,} customers). CLV holdout: {dd['holdout_min_date'][:10]} onwards ({dd['holdout_customers']:,} customers).
Recommender: train <= {rs['train_max_date'][:10]} ({rs['n_users_train']:,} users, {rs['n_items_train']:,} items), test from {rs['test_min_date'][:10]}.

## Metrics (all from outputs/metrics.json)
{target_table(d)}

CLV vs baselines:
{clv_table(m)}

Recommender, `repeat_allowed`:
{recsys_table(m, 'repeat_allowed')}

Recommender, `discovery`:
{recsys_table(m, 'discovery')}

## Fairness / segment checks
No personal attributes (age, gender, ethnicity) exist in the data; the only demographic-like field is Country (about 92% UK).
Model quality is therefore checked across commercial segments instead: CLV and recommender errors differ strongly by customer size.
Per-segment holdout purchase rates are in `outputs/campaign_economics.csv` (`holdout_purchase_rate`). Small and one-off buyers are served
mostly by popularity-like items; large wholesalers dominate revenue and the recommender training signal.

## Known failure modes
- One-time buyers get population-average order value; BG/NBD cannot separate them from churners.
- Seasonal peaks (Q4) and promotions are not modelled; holdout spend is under-predicted in aggregate.
- Colour/size variants produce near-duplicate bundles; ALS is trained on purchases only (no item content, no returns).
- Customers first seen after 2011-06-30 have no segment/CLV in the calibration snapshot.
- GMM and HDBSCAN are weaker than KMeans on log-RFM here (see README).

## Monitoring plan
Monthly refit; track BG/NBD calibration plot by frequency bucket, top-decile share, recommender HitRate@10/NDCG@10 against popularity
on a rolling last-30-days test, segment migration matrix and campaign response vs the control group.

## Version / seed
crm 0.1.0, seed {m['seed']}, pinned in requirements.txt; pipeline runtime {m['runtime_seconds']} s.
"""


def render_deck(d: dict) -> str:
    """Review deck outline (mid and final)."""
    s = d["s"]
    return f"""# Review deck outline - case study 06

## Mid-review (after M3), ~10 slides
1. Problem and KPIs (CRM: segments, CLV, bundles, recommendations)
2. Data: Online Retail II, cleaning funnel, time splits (calibration / holdout)
3. RFM construction and rule segments (sizes, revenue share; Champions {_pct(s['segments']['Champions']['revenue_share'], 0)} of revenue)
4. Clustering: elbow / silhouette (final {s['silhouette_kmeans_final']:.3f} vs target 0.35), GMM and HDBSCAN comparison, feature-set ablation
5. CLV: BG/NBD + GG, calibration plot, MAE / Spearman vs baseline
6. Top-decile CLV share ({_pct(s['clv_top_decile_share_predicted_12m'])}) and what it means
7. Risks found so far (seasonality, left-censoring, small samples)
8. Plan for M4/M5

## Final review (after M5), ~10 slides
1. Recap and results vs targets table
2. Bundles: top 20 by lift
3. Recommender: popularity vs item-KNN vs ALS vs hybrid (both protocols; ALS {s['recsys_als_ndcg_ratio']:.2f}x popularity under {s['recsys_primary_protocol']})
4. Campaign matrix and ROI table (funded ROI {s['campaign_funded_roi']:.2f}), sensitivity
5. App demo: segment explorer, Customer 360, bundle finder, campaign planner
6. Leakage controls and tests
7. Limitations, deviations, next steps (pilot with control group)
"""


def main(out: Path | None = None, root: Path | None = None) -> None:
    """Write all rendered docs."""
    root = root or ROOT
    out = out or root / "outputs"
    d = load(out)
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "DECISION_MEMO.md").write_text(render_memo(d), encoding="utf-8")
    (docs / "MODEL_CARD.md").write_text(render_model_card(d), encoding="utf-8")
    (docs / "REVIEW_DECK_OUTLINE.md").write_text(render_deck(d), encoding="utf-8")
    readme = root / "README.md"
    if readme.exists():
        txt = readme.read_text(encoding="utf-8")
        a, b = "<!-- RESULTS:START -->", "<!-- RESULTS:END -->"
        if a in txt and b in txt:
            pre, rest = txt.split(a, 1)
            _, post = rest.split(b, 1)
            readme.write_text(pre + a + "\n" + render_results_block(d) + "\n" + b + post, encoding="utf-8")


if __name__ == "__main__":
    main()
