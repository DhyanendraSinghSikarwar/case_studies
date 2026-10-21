# Final review (after M5) - CS07 churn + uplift retention

**Verdict: Needs work.** All modules, tests, app, memo and model card are present and numbers are consistent, but the churn AUC KPI (>= 0.75) is missed (0.747) and the headline uplift result is simulator-by-construction.
Deviation: `python tasks.py all` was not run (CPU shared with three other reviews). Ran (after fixes): ruff All checks passed; pytest 41 passed, 1 skipped; `train` stage (re-run, deterministic), docgen from outputs JSON. The `evaluate` stage was not re-run because nothing it consumes changed (churn champion/test scores identical).

## Acceptance checklist
| Criterion | Status | Evidence |
|---|---|---|
| Churn AUC >= 0.75 | FAIL | 0.747 (summary.json targets.churn_auc_ge_0.75.pass=false) |
| Qini > 0 | PARTIAL | 6,307 (S), CI [-7,887, 21,115] includes 0 |
| Uplift policy >= 70% oracle | PASS (weak) | profit_optimal 92.3%; but contact-all 98.2% and M2 risk-threshold 98.9% are higher at base cost |
| Uplift > risk-only > random | PASS | 1,351,339 / 1,275,673 / 802,532 for top-k at 30% budget; profit_optimal 2,584,617 |
| Temporal split, `test_features_before_asof` | PASS | tests/test_snapshot.py |
| Policy table with oracle ceiling | PASS | README Results, outputs/policy_table.csv |
| Memo: why highest-risk can lose money | PASS | docs/DECISION_MEMO.md (risk-top-30% negative at high offer costs; 21 of 63 grid cells) |

## Methodology scores (1-5)
| Area | Score | Note |
|---|---|---|
| Framing & KPI clarity | 5 | explicit targets table with FAIL shown |
| Data quality & validation | 4 | validate.py checks; duplicates not dropped (documented) |
| Leakage & split | 5 | temporal split, group-aware CV/calibration, truth-not-used test |
| Baseline vs model | 4 | naive baseline + 4 models; logit champion by CV |
| Business translation & sensitivity | 5 | INR tables, 63-cell grid, cost sweep, alt response pattern |
| Explainability / fairness | 3 | SHAP present; no fairness analysis (low relevance) |
| Reproducibility | 4 | seed, tasks.py, pinned requirements; run-time heavy on shared CPU |
| Code quality | 4 | ruff clean, 42 tests (41 pass, 1 skipped sklift cross-check; 2 new), typed/docstringed |
| App / deployment | 4 | Streamlit AppTest-verified, Dockerfile |

## Number audit
Programmatic: every numeric token in README, DECISION_MEMO, MODEL_CARD, SIMULATOR, PROBLEM_STATEMENT was matched to a value in outputs/*.json or outputs/*.csv (rounding tolerance <0.6%): 0 unmatched. Docs regenerated via `churnx.docgen.render_from_outputs`; pre-fix regeneration was byte-identical to committed docs.

## Fixes applied
1. `models.temporal_window_check` + train.py hook + docgen note: train-only evidence for not widening the window (tests added).
2. Memo now states the 70% criterion is weak (contact-all / risk-threshold beat uplift at base cost) - generated from JSON, test added.
3. test_e2e Streamlit timeout 120 -> 300 s.
4. Not changed: AUC kept at 0.747 (no test-snapshot tuning).

## Remaining issues
- AUC 0.747 < 0.75 (honest miss). - Qini CI includes 0; policy-vs-oracle is simulator-by-construction. - Real value of uplift is shown only at high offer cost; Hillstrom real-RCT IPW intervals overlap.

## Sponsor Q&A
1. Why miss 0.75? Seasonality/temporal shift; train-only checks did not support a better model; 0.756 with 6 snapshots was test-observed, so not claimed.
2. Is the 92% real? No: simulated effect; holds inside the simulator only.
3. Why contact-all ~ oracle? Offer cost INR 250 is tiny vs value; targeting pays at INR 1,000+.
4. Does real data support uplift? Hillstrom Qini for visit CI excludes 0; profit IPW CIs overlap.
5. What next? Real 50/50 pilot, refit quarterly, monitor calibration drift.
