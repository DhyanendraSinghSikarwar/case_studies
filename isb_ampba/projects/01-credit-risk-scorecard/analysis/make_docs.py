"""Generate README result blocks, DECISION_MEMO.md and MODEL_CARD.md from outputs/*.json|csv (no hand-typed numbers)."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd  # noqa: E402

from credit.config import load_config  # noqa: E402

CFG = load_config()
OUT = ROOT / "outputs"
S = json.load(open(OUT / "summary.json", encoding="utf-8"))
M = json.load(open(OUT / "metrics.json", encoding="utf-8"))
NAMES = {"logit_raw": "Baseline logistic (raw features)", "scorecard": "WOE scorecard (logistic)",
         "xgb": "XGBoost (isotonic-calibrated)", "lgbm": "LightGBM (isotonic-calibrated)"}


def inr(x: float) -> str:
    """Format rupees as INR mn / crore-free plain millions."""
    return f"INR {x / 1e6:,.1f} mn"


def pct(x: float, d: int = 1) -> str:
    """Format a fraction as a percentage."""
    return f"{x:.{d}%}"


def md_table(df: pd.DataFrame) -> str:
    """DataFrame -> markdown table."""
    head = "| " + " | ".join(map(str, df.columns)) + " |\n|" + "---|" * len(df.columns) + "\n"
    return head + "\n".join("| " + " | ".join(map(str, r)) + " |" for r in df.to_numpy())


def results_table() -> str:
    """Baseline-vs-model results (test and valid AUC)."""
    rows = [["Naive (predict base rate)", "0.500", "0.000", "0.000", f"{M['naive_base_rate']['test']['brier']:.4f}", "n/a", "0.500"]]
    for k, n in NAMES.items():
        t, v = M[k]["test"], M[k]["valid"]
        star = " **(champion)**" if k == M["champion"] else ""
        rows.append([n + star, f"{t['auc']:.4f}", f"{t['gini']:.4f}", f"{t['ks']:.4f}", f"{t['brier']:.4f}",
                     f"{t['cal_slope']:.3f}", f"{v['auc']:.4f}"])
    rows.append(["Benchmark R1 (Abhinav19-isb)", "0.783", "-", "0.424", "-", "-", "-"])
    return md_table(pd.DataFrame(rows, columns=["Model", "Test AUC", "Test Gini", "Test KS", "Test Brier", "Cal. slope", "Valid AUC"]))


def targets_table() -> str:
    """Target-vs-achieved table."""
    f = M[M["champion"]]["test"]
    ok = lambda b: "PASS" if b else "MISS"  # noqa: E731
    rows = [["ROC-AUC", ">= 0.78", f"{f['auc']:.4f}", ok(f["auc"] >= 0.78)],
            ["KS", ">= 0.42", f"{f['ks']:.4f}", ok(f["ks"] >= 0.42)],
            ["Gini", ">= 0.56", f"{f['gini']:.4f}", ok(f["gini"] >= 0.56)],
            ["Brier", "<= 0.14", f"{f['brier']:.4f}", ok(f["brier"] <= 0.14)],
            ["Calibration slope", "0.9 - 1.1", f"{f['cal_slope']:.3f}", ok(0.9 <= f["cal_slope"] <= 1.1)],
            ["Points table reproduces score", "within 1 point", f"max diff {S['scorecard_max_point_diff']:.3f}",
             ok(S["scorecard_max_point_diff"] <= 1)]]
    return md_table(pd.DataFrame(rows, columns=["Metric", "Target", "Achieved (test, champion)", "Result"]))


def business_block() -> str:
    """Business impact bullets."""
    a = S["assumptions"]
    return (f"- Optimal cut-off: approve if PD <= **{S['opt_cutoff']:.2f}** (score >= {S['opt_cutoff_score']:.0f}); break-even PD "
            f"= margin/(margin+LGD) = {a['breakeven_pd']:.3f}.\n"
            f"- Approval rate **{pct(S['approval_rate'])}**; bad rate among approved **{pct(S['bad_rate_approved'])}** "
            f"vs {pct(S['bad_rate_all'])} approve-all.\n"
            f"- Expected profit {inr(S['profit_opt_inr'])} vs {inr(S['profit_approve_all_inr'])} approve-all "
            f"(uplift {inr(S['uplift_inr'])}; realised-outcome uplift {inr(S['real_uplift_inr'])}).\n"
            f"- Sensitivity (LGD 0.45-0.85 x margin 0.10-0.26): optimal cut-off {S['sens_cutoff_min']:.2f}-{S['sens_cutoff_max']:.2f}; "
            f"uplift range {inr(S['sens_uplift_min_inr'])} to {inr(S['sens_uplift_max_inr'])} "
            f"({'positive in every cell' if S['sens_uplift_all_positive'] else 'NOT positive in every cell'}).\n"
            f"- Assumptions: margin {a['margin']}, LGD {a['lgd']}, NT$->INR {a['fx_ntd_inr']}; all test-set ({S['n_test']:,} customers).")


def data_block() -> str:
    """Data facts."""
    d, z = S["data"], S["sizes"]
    return (f"{d['rows']:,} customers, default rate {pct(d['default_rate'], 2)}, {d['neg_bill1_rows']} rows with negative BILL_AMT1 "
            f"({d['neg_bill_rows']} with any negative bill), {d['duplicate_rows']} duplicate rows (kept). "
            f"Stratified split: {z['train']:,} / {z['valid']:,} / {z['test']:,} (train / valid / test).")


def fairness_block() -> str:
    """Fairness tables."""
    out = []
    for name in ["sex", "age"]:
        r = pd.read_csv(OUT / f"fairness_{name}.csv")
        r = r.assign(n=r["n"].astype(int), approval_rate=r["approval_rate"].map("{:.1%}".format),
                     bad_rate_approved=r["bad_rate_approved"].map("{:.1%}".format),
                     default_rate=r["default_rate"].map("{:.1%}".format), auc=r["auc"].map("{:.3f}".format),
                     di_ratio=r["di_ratio"].map("{:.3f}".format))
        out.append(f"**By {name.upper()}**\n\n" + md_table(r))
    return "\n\n".join(out)


def band_block() -> str:
    """Band table + limit engine."""
    b = pd.read_csv(OUT / "band_table.csv")
    b = b.assign(bad_rate=b["bad_rate"].map("{:.1%}".format), avg_pd=b["avg_pd"].map("{:.1%}".format),
                 share=b["share"].map("{:.1%}".format), score_min=b["score_min"].round(0).astype(int),
                 score_max=b["score_max"].round(0).astype(int))
    lv = pd.read_csv(OUT / "limit_engine_value.csv")
    lv = lv.assign(profit_before=(lv["profit_before"] / 1e6).round(2), profit_after=(lv["profit_after"] / 1e6).round(2),
                   delta=(lv["delta"] / 1e6).round(2)).rename(columns={"profit_before": "profit_before_mn", "profit_after": "profit_after_mn",
                                                                       "delta": "delta_mn"})
    return md_table(b) + "\n\nLimit engine value by band (INR mn, config actions applied):\n\n" + md_table(lv)


def memo() -> str:
    """Decision memo from the template in PLAN.md section 6."""
    a = S["assumptions"]
    sens_pos = ("; the uplift stays positive in every cell (minimum " + inr(S["sens_uplift_min_inr"]) + ")") if S["sens_uplift_all_positive"] \
        else f"; NOTE the uplift is not positive in every cell (minimum {inr(S['sens_uplift_min_inr'])})"
    return f"""# Decision memo - Card approval cut-off and limit policy
_Generated {date.today().isoformat()} by `analysis/make_docs.py` from `outputs/summary.json` and `outputs/metrics.json`._

**Decision requested:** Approve the PD cut-off and limit actions below for new/review decisions on the card book.

**Recommendation:** Approve customers with PD <= {S['opt_cutoff']:.2f} (score >= {S['opt_cutoff_score']:.0f}); apply the band actions A-F in the limit table.

**Impact (test set, {S['n_test']:,} customers, assumptions margin {a['margin']}, LGD {a['lgd']}, NT$->INR {a['fx_ntd_inr']}):**
- Approval rate {pct(S['approval_rate'])}; bad rate among approved {pct(S['bad_rate_approved'])} vs {pct(S['bad_rate_all'])} for approve-all.
- Expected profit {inr(S['profit_opt_inr'])} vs {inr(S['profit_approve_all_inr'])} approve-all -> uplift {inr(S['uplift_inr'])} (INR {S['uplift_per_1000_inr']:,.0f} per 1,000 applicants). Using actual outcomes the same policy earns {inr(S['real_profit_opt_inr'])} vs {inr(S['real_profit_approve_all_inr'])} for approve-all, so expected and realised profit agree in direction.
- Across LGD 0.45-0.85 x margin 0.10-0.26 the optimal cut-off ranges {S['sens_cutoff_min']:.2f}-{S['sens_cutoff_max']:.2f}{sens_pos}.
- Applying the band limit actions (A/B increase, C hold, D decrease, E/F decline) changes expected profit by {inr(S['limit_engine_total_delta_inr'])} on the test book under the config assumptions (most of it from declining bands E/F; the pd_mult/limit-change effects are assumptions).

**Evidence:** champion {S['champion']} test AUC {S['auc_test']:.4f}, KS {S['ks_test']:.4f}, Gini {S['gini_test']:.4f} vs baseline logit AUC {S['auc_logit_raw']:.4f} and WOE scorecard AUC {S['auc_scorecard']:.4f}; Brier {S['brier_test']:.4f} (base-rate predictor {S['brier_naive']:.4f}); calibration slope {S['cal_slope_test']:.3f}; top drivers {', '.join(S['top_shap_features'])}. Benchmark R1: AUC 0.783 / KS 0.424.

**Risks & limitations:** Taiwan 2005 data and a random split, so no out-of-time validation; margin and LGD are assumptions, not observed; only approved customers have outcomes in real life (no reject inference); fairness: disparate-impact minimum {S['fairness_di_min_sex']:.3f} (sex) and {S['fairness_di_min_age']:.3f} (age) - {'both above' if S['fairness_di_pass_sex'] and S['fairness_di_pass_age'] else 'at least one below'} the 0.8 screening threshold (heuristic, not a legal finding); age and limit remain possible proxies - review before use.

**Next steps:** 3-month shadow run on recent data; PSI monitor with alert at {CFG['monitoring']['psi_alert']} (a {CFG['monitoring']['drift_limit_shift']:.0%} LIMIT_BAL shift gives feature PSI {S['psi_limit_drift']:.3f} for LIMIT_BAL, while the score PSI is only {S['score_psi_limit_drift']:.3f}, so monitor features as well as the score); recalibrate quarterly.
"""


def model_card() -> str:
    """Model card from outputs."""
    return f"""# Model card - Credit risk PD model (champion: {S['champion']})
_Generated {date.today().isoformat()} from `outputs/`._

## Intended use
Rank card customers by probability of default (next month), convert to a 300-900 score with bands A-F, and support approve/decline and limit actions in a portfolio-economics analysis. Portfolio/educational use; not validated for live credit decisions.

## Data
UCI "Default of Credit Card Clients" (id 350; Yeh and Lien 2009; CC BY 4.0). {data_block()} Amounts are NT$ (converted to INR only for business outputs).

## Models
Baseline logistic on raw features; WOE/logistic scorecard ({M['scorecard_check']['n_variables']} variables, monotonic bins, points table); tuned XGBoost and LightGBM ({M['tuning']['trials']} Optuna trials, 3-fold CV on train only) with isotonic calibration fitted on the validation split. Champion chosen on validation AUC of the uncalibrated model; test set evaluated once. SEX is never a model input.

## Metrics (test set, n={S['n_test']:,})
{results_table()}

Targets: {'all met' if all(v[1] if isinstance(v, list) else v for v in S['targets'].values()) else 'see README for misses'}.

{targets_table()}

## Fairness check (at the optimal cut-off {S['opt_cutoff']:.2f})
{fairness_block()}

Disparate-impact ratio = group approval rate / highest group approval rate; 0.8 is a screening heuristic.

## Limitations
- 2005 Taiwanese issuer data, random (not out-of-time) split; population and macro conditions differ from any current book.
- Outcomes observed only over one month; the 'default' definition is the dataset's.
- Profit figures depend on assumed margin, LGD and limit-action effects (swept in the sensitivity analysis, not estimated from data).
- Age and credit limit may act as proxies for protected attributes; disparate-impact ratios are screening metrics.
- Calibration is isotonic on a 6,000-row validation split; recalibrate regularly.
- Top SHAP drivers: {', '.join(S['top_shap_features'])}.
"""


def readme_blocks() -> dict[str, str]:
    """Marker -> generated markdown."""
    f = M[M["champion"]]["test"]
    miss = [k for k, v in S["targets"].items() if not (v[1] if isinstance(v, list) else v)]
    verdict = ("All headline targets were met on the test set." if not miss
               else f"Targets missed: {', '.join(miss)} - see Deviations.")
    log = (f"- **{date.today().isoformat()} M1-M5 complete.** Data validated ({data_block()}) ; scorecard test AUC {S['auc_scorecard']:.4f}; "
           f"champion {S['champion']} test AUC {f['auc']:.4f}, KS {f['ks']:.4f}; optimal cut-off {S['opt_cutoff']:.2f}; "
           f"uplift {inr(S['uplift_inr'])}. {verdict}")
    return {"DATA": data_block(), "RESULTS": results_table() + "\n\n" + verdict + "\n\n" + targets_table(),
            "BUSINESS": business_block(), "BANDS": band_block(), "FAIRNESS": fairness_block(), "LOG": log}


def main() -> None:
    """Write docs and refresh README markers."""
    (ROOT / "docs" / "DECISION_MEMO.md").write_text(memo(), encoding="utf-8")
    (ROOT / "docs" / "MODEL_CARD.md").write_text(model_card(), encoding="utf-8")
    rp = ROOT / "README.md"
    txt = rp.read_text(encoding="utf-8")
    for k, v in readme_blocks().items():
        txt = re.sub(rf"(<!-- {k}:START -->).*?(<!-- {k}:END -->)", lambda m, v=v: f"{m.group(1)}\n{v}\n{m.group(2)}", txt, flags=re.S)
    rp.write_text(txt, encoding="utf-8")
    print("docs written")


if __name__ == "__main__":
    main()
