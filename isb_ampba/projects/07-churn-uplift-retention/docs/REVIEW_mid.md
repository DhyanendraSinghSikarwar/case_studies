# Mid-review (after M3) - CS07 churn + uplift retention

**Verdict: Needs work (one KPI missed, honestly reported).** Scope at mid: M1 snapshots/labels, M2 churn models + threshold, M3 pilot + uplift.
Deviation: three other projects were reviewed concurrently, so `python tasks.py all` was NOT run; ruff, pytest and the `train` stage were run, the `evaluate` stage was not re-run (outputs/summary.json from the earlier full run was used).

## Checks
- ruff: All checks passed. pytest (full suite, before fixes): 38 passed, 1 skipped (sklift cross-check), 1 failed (`test_streamlit_app_runs`, AppTest 120 s timeout under CPU contention; timeout raised to 300 s).
- train stage re-run: champion `logit`, test AUC 0.747 (identical to stored outputs -> deterministic).

## Spec conformance (M1-M3)
snapshot.py, models.py (logit/RF/XGB/LGBM, isotonic calibration, SHAP), threshold.py, pilot.py (ground-truth tau stored), uplift.py (S/T/X/TO + class-transformation, Qini/AUUC) all exist, are implemented and tested. survival.py (optional) present.

## Acceptance (mid-relevant)
| Criterion | Status | Evidence |
|---|---|---|
| Temporal split + `test_features_before_asof` | PASS | tests/test_snapshot.py; train 2011-03/04/05, test 2011-08-01 |
| Churn AUC >= 0.75 | FAIL | test AUC 0.747 (outputs/summary.json churn.test_auc) |
| Qini > 0 | PARTIAL | S-learner 6,307 but 95% CI [-7,887, 21,115] includes 0 |

## AUC attempt
Added `models.temporal_window_check` (train-only; validates on the last training snapshot 2011-05-01). Adding pilot-history snapshots lowered AUC (0.783 -> 0.768) and stronger regularisation did not help (0.780), so no model change was adopted. The 6-snapshot logit reaches 0.756 on test but was NOT adopted because that would be selecting on the test snapshot. Honest miss kept.

## Scores (1-5)
Framing 5 | Data quality 4 | Leakage/split 5 | Baseline vs model 4 | Business translation 4 | Explainability 4 | Reproducibility 4 | Code quality 4 | App 4

## Top fixes (applied unless noted)
1. Document train-only evidence for the AUC miss (done: metrics.json key + README/docgen).
2. Streamlit e2e test timeout under load (done: 300 s).
3. Qini CI includes 0 - cannot be fixed without more data; stated in README/memo (not fixable).
