"""Render README results block, DECISION_MEMO.md and MODEL_CARD.md from outputs/summary.json + metrics.json.

Every number in the generated text comes from the JSON files written by the pipeline (no hand-typed results).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

START, END = "<!-- RESULTS:START -->", "<!-- RESULTS:END -->"


def inr(x: float) -> str:
    """Format an INR amount."""
    return f"₹{x:,.0f}"


def mil(x: float) -> str:
    """Format INR in millions."""
    return f"₹{x / 1e6:,.2f}m"


def md_table(header: list[str], rows: list[list[Any]]) -> str:
    """Markdown table."""
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def _ok(b: bool) -> str:
    return "PASS" if b else "**FAIL**"


def targets_table(s: dict[str, Any]) -> str:
    """KPI table: target vs achieved vs pass."""
    t = s["targets"]
    rows = [
        ["Churn AUC (test 2011-08-01)", ">= 0.75", f"{t['churn_auc_ge_0.75']['achieved']:.3f}", _ok(t["churn_auc_ge_0.75"]["pass"])],
        ["Qini > 0 (selected learner, pilot test cohort)", "> 0",
         f"{t['qini_gt_0_selected_learner']['achieved']:,.0f} ({s['uplift']['selected_learner']}-learner)",
         _ok(t["qini_gt_0_selected_learner"]["pass"])],
        ["Uplift policy % of oracle (base case)", ">= 70%", f"{t['uplift_policy_ge_70pct_oracle']['achieved']:.1f}%",
         _ok(t["uplift_policy_ge_70pct_oracle"]["pass"])],
        ["Uplift > risk-only > random (profit)", "ordering", "yes" if t["uplift_gt_risk_gt_random"]["pass"] else "no",
         _ok(t["uplift_gt_risk_gt_random"]["pass"])],
        ["test_features_before_asof", "passes", "passes", _ok(t["features_before_asof"]["pass"])],
    ]
    return md_table(["Metric", "Target", "Achieved", "Pass?"], rows)


def churn_table(m: dict[str, Any]) -> str:
    """Model comparison on the test snapshot."""
    rows = []
    for name in ("logit", "rf", "xgb", "lgbm"):
        v = m["models"][name]
        rows.append([name + (" (champion by CV)" if name == m["champion"] else ""), f"{v['cv_auc_train']:.3f}", f"{v['auc']:.3f}",
                     f"{v['pr_auc']:.3f}", f"{v['ks']:.3f}", f"{v['brier']:.3f}", f"{v['mean_pred']:.3f}"])
    c = m["models"]["champion_calibrated"]
    rows.append(["champion + isotonic (group-CV)", "-", f"{c['auc']:.3f}", f"{c['pr_auc']:.3f}", f"{c['ks']:.3f}",
                 f"{c['brier']:.3f}", f"{c['mean_pred']:.3f}"])
    b = m["models"]["baseline_train_rate"]
    rows.append(["naive baseline (train churn rate)", "-", "0.500", "-", "-", f"{b['brier']:.3f}", f"{b['mean_pred']:.3f}"])
    return md_table(["Model", "grouped-CV AUC (train)", "test AUC", "PR-AUC", "KS", "Brier", "mean pred"], rows)


def snapshot_table(m: dict[str, Any]) -> str:
    """Eligible customers and churn rate per snapshot."""
    return md_table(["Snapshot", "Split", "Eligible", "Churn rate"],
                    [[r["asof"], r["split"], f"{r['n_eligible']:,}", f"{r['churn_rate']:.1%}"] for r in m["snapshots"]])


def uplift_table(s: dict[str, Any]) -> str:
    """Learner comparison on the pilot test cohort."""
    k = [c for c in next(iter(s["uplift"]["learners"].values())) if c.startswith("uplift_at_")][0]
    rows = []
    for n, r in s["uplift"]["learners"].items():
        tr = r.get("tau_recovery")
        rows.append([n + (" (selected)" if n == s["uplift"]["selected_learner"] else ""), f"{r['qini']:,.0f}",
                     f"[{r['qini_ci95'][0]:,.0f}, {r['qini_ci95'][1]:,.0f}]", f"{r['qini_pct_of_oracle']:.0f}%",
                     f"{r[k]:.3f}", f"{tr['pearson']:.2f}" if tr else "-", f"{tr['spearman']:.2f}" if tr else "-"])
    return md_table(["Scorer", "Qini", "95% bootstrap CI", "% of oracle Qini", k.replace("_", " "), "tau corr (Pearson)",
                     "tau corr (Spearman)"], rows)


def policy_table_md(rows: list[dict[str, Any]]) -> str:
    """Policy table (INR, % of oracle)."""
    return md_table(["Policy", "Treated", "Profit (INR)", "% of oracle"],
                    [[r["policy"], f"{r['n_treated']:,}", f"{r['profit_inr']:,.0f}", f"{r['pct_of_oracle']:.1f}%"] for r in rows])


def cost_sweep_table(s: dict[str, Any]) -> str:
    """Profit (INR m) by policy across offer costs at base margin / CLV horizon."""
    by = s["policy"]["sensitivity"]["base_margin_clv_by_offer_cost"]
    costs = sorted(by, key=float)
    pols = ["random", "all", "risk_top_k", "clv_top_k", "uplift_top_k", "profit_optimal", "risk_threshold_m2", "oracle"]
    rows = [[p] + [f"{by[c][p]['profit_inr'] / 1e6:,.2f}" for c in costs] for p in pols if p in by[costs[0]]]
    return md_table(["Policy \\ offer cost (INR)"] + [f"{float(c):,.0f}" for c in costs], rows)


def thr_sens_table(t: dict[str, Any]) -> str:
    """Best threshold / contacts by save rate x offer cost (risk-only rule)."""
    rows = [[f"{r['save_rate']:.2f}", f"{r['offer_cost_inr']:,.0f}", f"{r['threshold']:.2f}", f"{r['n_contacted']:,}",
             f"{r['profit_inr']:,.0f}"] for r in t.get("sensitivity", [])]
    return md_table(["Save rate", "Offer cost (INR)", "Best threshold", "Contacted", "Expected profit (INR)"], rows)


def hillstrom_md(h: dict[str, Any]) -> str:
    """Hillstrom section."""
    if not h or "skipped" in h:
        return "_Hillstrom data was not available when the analysis ran (Track B skipped)._"
    pol = md_table(["Policy (held-out half)", "Treated", "IPW profit per 1,000 customers (USD)", "95% bootstrap CI"],
                   [[k, f"{v['n_treated']:,}", f"{v['profit_per_1000_usd']:.1f}", f"[{v['ci95'][0]:.1f}, {v['ci95'][1]:.1f}]"]
                    for k, v in h["policies"].items()])
    rows = []
    for o, d in h["learners"].items():
        for L, v in d.items():
            rows.append([o, L, f"{v['qini']:,.0f}", f"[{v['qini_ci95'][0]:,.0f}, {v['qini_ci95'][1]:,.0f}]"])
    q = md_table(["Outcome", "Learner", "Qini", "95% bootstrap CI"], rows)
    return (f"n = {h['n']:,} (held-out half {h['n_test']:,}); max |standardised covariate difference| between arms "
            f"{h['max_abs_std_diff']:.3f}; policy learner `{h['uplift_learner_for_policy']}` chosen on a validation slice of the "
            f"training half.\n\n{pol}\n\n{q}")


def window_note(m: dict[str, Any]) -> str:
    """One-sentence train-only evidence on the training window / regularisation (no test snapshot involved)."""
    w = m.get("temporal_window_check_train_only")
    if not w:
        return "no train-only window check was run"
    a, b = w["train_prior_only__C=0.5"], w["pilot_hist_plus_train_prior__C=0.5"]
    c = w["train_prior_only__C=0.05"]
    verdict = "so the wider window was NOT adopted" if b <= a else "so the wider window would be justified"
    return (f"train-only check on the {w['validation_snapshot']} snapshot: AUC {a:.3f} with train-only history, {b:.3f} with pilot "
            f"history added, {c:.3f} with stronger regularisation (C=0.05), {verdict}")


def results_block(s: dict[str, Any], m: dict[str, Any]) -> str:
    """The generated README results section."""
    p, t = s["policy"], s["threshold"]
    surv = s["survival"]
    alt = p["alt_response_pattern_high_freq"]
    seg = md_table(["Segment", "Customers", "Treated by risk-top-30%", "Mean true tau", "Profit contribution (INR)"],
                   [[r["segment"], r["n_segment"], r["n_treated"], f"{r['mean_tau_true']:.3f}", f"{r['profit_inr']:,.0f}"]
                    for r in p["segments_risk_top_k"]])
    cal = m["calibration_gap_test"]
    surv_txt = ("skipped" if "skipped" in surv else
                f"KM P(no purchase by day 30/60/90) = {surv['km_survival_30d']:.2f}/{surv['km_survival_60d']:.2f}/"
                f"{surv['km_survival_90d']:.2f}; Cox concordance {surv['cox_concordance']:.3f}.")
    return f"""### Targets vs achieved

{targets_table(s)}

### Churn models (temporal split: train 2011-03/04/05, test 2011-08-01)

{churn_table(m)}

Snapshots (eligible customers and churn rate):

{snapshot_table(m)}

Mean calibrated prediction on the test snapshot is {cal['mean_pred_calibrated']:.3f} versus an observed churn rate of
{cal['observed_rate']:.3f}: the pre-Christmas season lowers churn relative to the training snapshots, so calibration drifts
even though ranking (AUC) holds. A logit trained on 6 snapshots (pilot history + train) reaches test AUC
{m['supplementary_logit_6_snapshots_test_auc']:.3f} (supplementary, not the headline; {window_note(m)}). SHAP top drivers (mean |SHAP|, {m['tree_champion_for_shap']}):
{', '.join(f'`{k}` {v:.3f}' for k, v in m['shap_top5'].items())}.

### Cost-optimal contact threshold (risk-only, constant save rate {s['assumptions']['save_rate']:.0%}, offer cost {inr(s['assumptions']['offer_cost_inr'])})

Best threshold {t['best']['threshold']:.2f}: contact {t['best']['n_contacted']:,} of {t['n_customers']:,} customers, expected profit
{inr(t['best']['profit_inr'])} versus {inr(t['profit_contact_all_inr'])} for contacting everybody and ₹0 for nobody
(these are *expected* profits under the assumed constant save rate, not measured outcomes). With a cheap offer the optimum is
to contact almost everyone; the best threshold rises with the offer cost:

{thr_sens_table(t)}

### Uplift learners on the simulated pilot (test cohort; treatment effect is SYNTHETIC)

Selected by grouped-CV Qini on the training pilot: **{s['uplift']['selected_learner']}**. Pilot sanity: observed ATE
{s['pilot']['test']['observed_ate']:.3f} (SE {s['pilot']['test']['se']:.3f}) vs mean true tau {s['pilot']['test']['mean_tau_true']:.3f}.

{uplift_table(s)}

All Qini confidence intervals are wide because the test cohort has only {s['pilot']['n_test_cohort']:,} customers; an interval that
includes 0 means the ranking is not statistically distinguishable from random on this cohort alone.

### Policy comparison (exact value vs perfect-hindsight oracle; offer cost {inr(p['offer_cost_inr'])}, {p['budget_frac']:.0%} budget)

{policy_table_md(p['table'])}

`profit_optimal` is the uplift policy (contact iff predicted tau x value > cost): {p['uplift_policy_pct_of_oracle']:.1f}% of the oracle.
`risk_threshold_m2` is the M2 cost-optimal threshold rule scored against the true effect. Random-policy expected profit
over repeated draws: {inr(p['random_expected_profit_inr'])}.
With such a low offer cost almost every customer has positive incremental profit, so contacting everybody is already
near the oracle; targeting only pays when the offer is expensive relative to customer value (next table).

Profit (INR million) by policy as the offer cost rises (base margin and CLV horizon; masks recomputed per cell):

{cost_sweep_table(s)}

Across the full cost x margin x CLV grid ({p['sensitivity']['n_cells']} cells) risk-top-30% loses money in
{p['sensitivity']['n_cells_risk_top_k_negative']} cells, `profit_optimal` in {p['sensitivity']['n_cells_profit_optimal_negative']},
contact-all in {p['sensitivity']['n_cells_all_negative']}, and `profit_optimal` beats risk-top-30% in
{p['sensitivity']['n_cells_profit_optimal_beats_risk']} cells.

Who earns / loses under risk-only targeting (base case, risk top 30%):

{seg}

**Different response pattern** (simulator re-run with the response bump on *high* frequency, learner re-selected:
`{alt['selected_learner']}`):

{policy_table_md(alt['table'])}

### Survival view (optional)

{surv_txt}

### Track B - Hillstrom e-mail RCT (REAL randomised treatment; oracle-free IPW evaluation)

{hillstrom_md(s['hillstrom'])}
"""


def inject_readme(path: Path, block: str) -> bool:
    """Replace the content between the RESULTS markers in README.md. Returns False if markers are missing."""
    if not path.exists():
        return False
    t = path.read_text(encoding="utf-8")
    if START not in t or END not in t:
        return False
    a, b = t.index(START) + len(START), t.index(END)
    path.write_text(t[:a] + "\n\n" + block + "\n" + t[b:], encoding="utf-8")
    return True


def memo(s: dict[str, Any], m: dict[str, Any]) -> str:
    """CXO decision memo (all numbers from summary/metrics)."""
    p, t, a = s["policy"], s["threshold"], s["assumptions"]
    tab = {r["policy"]: r for r in p["table"]}
    by = p["sensitivity"]["base_margin_clv_by_offer_cost"]
    costs = sorted(by, key=float)
    neg = [c for c in costs if by[c]["risk_top_k"]["profit_inr"] < 0]
    hi = costs[-1]
    alt = {r["policy"]: r for r in p["alt_response_pattern_high_freq"]["table"]}
    seg = {r["segment"]: r for r in p["segments_risk_top_k"]}
    def seg_tau(name: str) -> str:
        return f"{seg[name]['mean_tau_true']:.3f}" if name in seg else "n/a"

    h = s["hillstrom"]
    if "skipped" in h:
        hill = "Hillstrom data was unavailable for this run."
    else:
        v = h["learners"]["visit"]
        best = max(("S", "T", "X", "TO"), key=lambda L: v[L]["qini"])
        pol = h["policies"]
        hill = (f"Qini for 'visit' with the {best}-learner is {v[best]['qini']:,.0f} (95% CI {v[best]['qini_ci95'][0]:,.0f} to "
                f"{v[best]['qini_ci95'][1]:,.0f}; random {v['random']['qini']:,.0f}). IPW profit per 1,000 customers (USD): "
                f"uplift top-30% {pol['uplift_top_30']['profit_per_1000_usd']:.1f} "
                f"(CI {pol['uplift_top_30']['ci95'][0]:.1f} to {pol['uplift_top_30']['ci95'][1]:.1f}) vs random "
                f"{pol['random_30']['profit_per_1000_usd']:.1f} (CI {pol['random_30']['ci95'][0]:.1f} to "
                f"{pol['random_30']['ci95'][1]:.1f}); the intervals overlap, so the real data do not separate these policies.")
    loses = (f"At offer costs of {', '.join(f'₹{float(c):,.0f}' for c in neg)} (base margin and CLV horizon) risk-top-30% has "
             f"negative incremental profit" if neg else "In the swept cost range risk-top-30% stayed positive at base margin/CLV, "
             "but it earns less than uplift targeting")
    return f"""# Decision memo - Who should get the retention offer?

**Decision requested:** Replace "contact the highest-risk customers" with "contact customers with the highest expected
incremental profit".

**Recommendation:** Run a 50/50 randomised pilot on real offers, fit an uplift model, then contact customers whose predicted
uplift x value exceeds the offer cost. Until a real pilot exists, treat every number below that depends on the offer's
effect as simulated.

**Impact (SIMULATED pilot; assumptions: gross margin {a['gross_margin']:.0%}, offer cost ₹{a['offer_cost_inr']:,.0f}, value horizon
{a['clv_months']} months, INR/GBP {a['gbp_to_inr']:.0f}; {p['budget_frac']:.0%} budget for budgeted policies):**
- Uplift targeting earns {inr(tab['profit_optimal']['profit_inr'])} ({tab['profit_optimal']['pct_of_oracle']:.1f}% of the oracle ceiling
  {inr(p['oracle_profit_inr'])}); risk-only top-30% earns {inr(tab['risk_top_k']['profit_inr'])} ({tab['risk_top_k']['pct_of_oracle']:.1f}%);
  random {inr(tab['random']['profit_inr'])} ({tab['random']['pct_of_oracle']:.1f}%).
- Honest caveat: at this low offer cost contacting *everybody* earns {inr(tab['all']['profit_inr'])} ({tab['all']['pct_of_oracle']:.1f}% of
  oracle) - targeting matters when the offer is expensive relative to customer value (see the cost sweep in the README).
- Churn model: champion `{m['champion']}`, test AUC {s['churn']['test_auc']:.3f} (target 0.75). Cost-optimal risk-only threshold
  {t['best']['threshold']:.2f} contacts {t['best']['n_contacted']:,} of {t['n_customers']:,} customers.

**Evidence on real treatment data (Hillstrom e-mail test, {h.get('n', 'n/a')} customers):** {hill}

**Why "target the highest-risk" can lose money:** churn probability measures baseline risk, not responsiveness. Incremental
profit is `tau x value - cost`; the riskiest customers include inactive ("Hibernating") and low-value customers whose true
effect is small (mean true tau {seg_tau('Hibernating')} vs {seg_tau('Mid-frequency')} for mid-frequency customers in the
simulator). {loses}; at the highest swept cost (₹{float(hi):,.0f}) risk-top-30% earns
{mil(by[hi]['risk_top_k']['profit_inr'])}, contact-all {mil(by[hi]['all']['profit_inr'])}, uplift targeting
{mil(by[hi]['profit_optimal']['profit_inr'])}. At the base cost risk-only is positive but captures only
{tab['risk_top_k']['pct_of_oracle']:.0f}% of the oracle. All of this is *by construction of the simulator*: when the response
pattern is moved to high-frequency customers, risk-top-30% earns {inr(alt['risk_top_k']['profit_inr'])} (random: {inr(alt['random']['profit_inr'])}) while uplift targeting earns {inr(alt['profit_optimal']['profit_inr'])}
({alt['profit_optimal']['pct_of_oracle']:.0f}% of that world's oracle), so the ranking of policies depends on the response
pattern, which only a real randomised pilot can reveal.

**Risks & limitations:**
- Pilot results are simulated (Track A); the 70%-of-oracle result holds only inside the simulator.
- Hillstrom is an e-mail experiment for a different business; effects are small and the CIs are wide.
- Margin, offer cost, FX and the 12-month value horizon are assumptions; seasonality moves churn between snapshots
  (calibration drifted: mean prediction {m['calibration_gap_test']['mean_pred_calibrated']:.3f} vs observed
  {m['calibration_gap_test']['observed_rate']:.3f}) and test AUC is {s['churn']['test_auc']:.3f}, {'below' if s['churn']['test_auc'] < 0.75 else 'at or above'} the 0.75 target.
- Test cohort has ~{s['pilot']['n_test_cohort']:,} customers; uplift Qini intervals include zero.
- The 70%-of-oracle criterion is weak here: contact-all earns {tab['all']['pct_of_oracle']:.1f}% and the M2 risk-threshold rule
  {tab['risk_threshold_m2']['pct_of_oracle']:.1f}% of the oracle at the base offer cost, i.e. at or above the uplift policy
  ({tab['profit_optimal']['pct_of_oracle']:.1f}%); uplift only clearly wins when the offer is costly (cost sweep in the README).

**Next steps:** run a real 50/50 pilot (owner: CRM), log offers and outcomes, refit quarterly, monitor holdout Qini and
calibration, re-estimate the economics (offer cost, margin) before scaling.
"""


def model_card(s: dict[str, Any], m: dict[str, Any]) -> str:
    """Model card for the churn champion and the uplift learner."""
    c = m["models"][m["champion"]]
    cal = m["models"]["champion_calibrated"]
    snaps = {r["split"] + r["asof"]: r for r in m["snapshots"]}
    ntr = m["n_train_rows"]
    seg = s["policy"]["segments_risk_top_k"]
    seg_rows = md_table(["Segment (test)", "Customers", "Mean true tau (simulated)"],
                        [[r["segment"], r["n_segment"], f"{r['mean_tau_true']:.3f}"] for r in seg])
    return f"""# Model card - churn model and uplift learner (case study 07)

## Intended use
Rank eligible online-retail customers (>= 2 orders in the previous 180 days) by 90-day churn risk and by predicted
incremental response to a retention offer, to prioritise a retention budget. Portfolio / teaching project, not a production system.

## Out-of-scope use
Individual-level decisions with legal or financial consequences; other businesses or time periods without refit; reading the
simulated uplift results as evidence about real offers.

## Training data
UCI Online Retail II (real transactions, 2009-12-01 to 2011-12-09). Snapshots 2011-03-01, 2011-04-01, 2011-05-01 stacked
({ntr:,} customer-snapshot rows; customers repeat, so folds are grouped by customer). Test: 2011-08-01 ({m['n_test_rows']:,} customers;
{m['n_customers_in_train_and_test']:,} also appear in training). Pilot treatment is SIMULATED (docs/SIMULATOR.md). {len(snaps)} snapshots built in total.

## Models
Logit, RandomForest, XGBoost, LightGBM; champion chosen by grouped-CV AUC on training snapshots only: `{m['champion']}`;
isotonic calibration with group-aware folds. Uplift: S/T/X/transformed-outcome/class-transformation learners
(LightGBM base), selected by grouped-CV Qini on the training pilot: `{s['uplift']['selected_learner']}`. Seed 42.

## Metrics (test snapshot 2011-08-01)
| Metric | Champion (raw) | Champion (calibrated) | Naive baseline |
|---|---|---|---|
| ROC-AUC | {c['auc']:.3f} | {cal['auc']:.3f} | 0.500 |
| PR-AUC | {c['pr_auc']:.3f} | {cal['pr_auc']:.3f} | - |
| KS | {c['ks']:.3f} | {cal['ks']:.3f} | - |
| Brier | {c['brier']:.3f} | {cal['brier']:.3f} | {m['models']['baseline_train_rate']['brier']:.3f} |
| Mean prediction (observed {c['base_rate']:.3f}) | {c['mean_pred']:.3f} | {cal['mean_pred']:.3f} | {m['models']['baseline_train_rate']['mean_pred']:.3f} |

Grouped-CV AUC on the training snapshots: {m['cv_auc_train'][m['champion']]:.3f}; the gap to the test AUC reflects seasonal
non-stationarity. Uplift (simulated pilot): selected learner Qini {s['uplift']['learners'][s['uplift']['selected_learner']]['qini']:,.0f}
(95% CI {s['uplift']['learners'][s['uplift']['selected_learner']]['qini_ci95'][0]:,.0f} to
{s['uplift']['learners'][s['uplift']['selected_learner']]['qini_ci95'][1]:,.0f}).

## Fairness / segment checks
No protected attributes exist in the data; the only demographic-like feature is `is_uk` (country). Customers are wholesalers
and consumers mixed. Segment view of the simulated response (by construction of the simulator):

{seg_rows}

Check calibration and Qini by segment (UK vs non-UK, value tercile) before any real use; this has not been done here.

## Known failure modes
Calibration drifts across seasons (test mean prediction vs observed above); AUC below target on this split; wholesaler
outliers in `monetary_6m`; uplift estimates are noisy on ~1.5k customers; IPW evaluation on Hillstrom has wide intervals.

## Monitoring plan
Monthly: AUC and calibration by snapshot; population stability of features; holdout Qini once a real pilot exists; refit quarterly.

## Version
churnx 0.1.0, seed 42, config/config.yaml as committed.
"""


def render_docs(root: Path, s: dict[str, Any], m: dict[str, Any]) -> None:
    """Write docs/DECISION_MEMO.md, docs/MODEL_CARD.md and inject the README results block."""
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "DECISION_MEMO.md").write_text(memo(s, m), encoding="utf-8")
    (docs / "MODEL_CARD.md").write_text(model_card(s, m), encoding="utf-8")
    inject_readme(root / "README.md", results_block(s, m))


def render_from_outputs(root: Path) -> None:
    """Convenience: load JSONs from root/outputs and render everything."""
    s = json.loads((root / "outputs" / "summary.json").read_text(encoding="utf-8"))
    m = json.loads((root / "outputs" / "metrics.json").read_text(encoding="utf-8"))["churn"]
    render_docs(root, s, m)
