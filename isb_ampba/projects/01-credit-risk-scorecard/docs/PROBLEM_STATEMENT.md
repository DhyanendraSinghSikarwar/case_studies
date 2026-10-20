# Problem statement - Credit risk scorecard and credit-limit engine

## Objective
A card issuer (NBFC/bank) wants to (a) predict whether a customer defaults next month (PD), (b) convert PD into a 300-900 bureau-style score with risk bands A-F (base 600 at 50:1 odds, 20 points to double the odds), and (c) set an approve/decline cut-off and credit-limit actions that maximise expected portfolio profit.

## KPIs
- Primary business KPI: expected portfolio profit (INR) at the chosen cut-off versus approve-all.
- Model KPIs: ROC-AUC >= 0.78, KS >= 0.42, Gini >= 0.56, Brier <= 0.14, calibration slope 0.9-1.1.
- Benchmark to beat: R1 Abhinav19-isb/credit-risk-scorecard (AUC 0.783, KS 0.424).

## Constraints
- `SEX` is never a model input; it is used only for the fairness audit.
- Binning, scaling, tuning and calibration never see the test set; the test set is evaluated once.
- Business assumptions (margin, LGD, FX, limit actions) live in `config/config.yaml` and are swept in a sensitivity analysis.
- Everything runs offline in tests and end-to-end in under 15 minutes on a laptop.

## Stakeholders
Head of Credit Risk (cut-off and limit policy), Model Risk / validation (scorecard transparency, calibration, drift), Compliance (fairness and reason codes), Finance (profit assumptions).

## Success criteria (acceptance checklist)
- [ ] `python tasks.py all` passes; `outputs/metrics.json` has auc/gini/ks/brier for logit, scorecard, xgb, lgbm.
- [ ] Champion test AUC >= 0.78 and KS >= 0.42 (otherwise report honest numbers and what was tried).
- [ ] Scorecard points-table sums reproduce the score within +/-1 point.
- [ ] `DECISION_MEMO.md` states optimal cut-off, approval %, bad rate %, INR profit vs approve-all, all from `summary.json`.
- [ ] >= 10 tests including `test_pd_to_score_monotonic`, `test_woe_monotonic`, `test_no_target_leakage`.
- [ ] README has baseline-vs-model table, limitations and the R1 benchmark comparison.
- [ ] Streamlit app runs with 4 tabs; CI configured (ruff + pytest).
