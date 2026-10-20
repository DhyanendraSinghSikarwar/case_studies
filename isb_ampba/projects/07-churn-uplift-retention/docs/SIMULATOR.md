# Simulator documentation (Track A pilot) - SYNTHETIC TREATMENT

**Everything about the offer's effect in Track A is invented.** Only the baseline outcome (who churned) comes from real
Online Retail II transactions. Policy-vs-oracle conclusions therefore hold *by construction of this simulator*; the
sensitivity analysis (alternative response pattern, cost/margin sweeps) and Track B (real Hillstrom RCT) exist to show
how far the conclusions travel. Code: `src/churnx/pilot.py`; seed 42 (`np.random.default_rng(seed)`).

## Cohorts
- Pilot **training** cohort: stacked snapshots 2010-12-01, 2011-01-01, 2011-02-01 (history) + 2011-03-01, 04-01, 05-01 (train).
- Pilot **test** cohort: snapshot 2011-08-01. Uplift models never see test rows during fitting or learner selection.

## Baseline churn probability `p0` (ground-truth construction only, never a feature)
- Training cohorts: **out-of-fold** group-aware (3-fold on `customer_id`) LightGBM churn probability, clipped to [0.01, 0.99].
- Test cohort: calibrated champion churn probability, logit-shifted so its mean equals the cohort's realised churn rate
  (keeps the simulator's true effect consistent with the world it generates; the churn *model* itself is not recalibrated).

## Treatment assignment
`w ~ Bernoulli(0.5)` independent of everything (randomised 50/50 RCT).

## True save rate (`save_rate_true`, P(offer saves a would-be churner))
With `f` = within-snapshot percentile rank of `frequency_6m` and `a` = percentile rank of `aov_6m` (low = price sensitive):

| Rule (pattern `mid_freq`, the base case) | Effect |
|---|---|
| `0.05 + 0.55 * exp(-((f-0.5)/0.25)^2) * (1-a)` | price-sensitive, mid-frequency customers respond most |
| `f > 0.85` -> 0 | "Champions" do not respond |
| `recency_days > 100` -> x 0.2 | "Hibernating" customers rarely respond |
| + `N(0, 0.03)` noise, clipped to [0, 0.8] | |

Alternative world `high_freq` (sensitivity only): the bump is centred at `f = 0.9`, no Champion cut-off.

## Outcomes
- `saved = Bernoulli(save_rate_true)` AND `churn == 1`.
- `y = churn * (1 - saved)` if treated else `churn`; modelled outcome `retained = 1 - y` (higher is better).
- Ground truth: `tau_true = p0 * save_rate_true` (effect of the offer on retention probability).

## Stored but forbidden as features
`p0`, `save_rate_true`, `tau_true`, `saved` live in the pilot table (`TRUTH_COLS` in `pilot.py`). `uplift_feature_matrix`
asserts none of them (nor `w`, `y`, `retained`, `churn`) is in the feature matrix, and tests
`test_uplift_features_exclude_truth` / `test_ground_truth_never_used_by_modelling_code` enforce it. Ground truth is used
only for evaluation: tau-recovery correlation and the exact policy value / oracle ceiling.

## Sanity checks (see `outputs/summary.json`, key `pilot`)
Observed treated-minus-control retention vs mean `tau_true` (training cohort and test cohort, with standard errors).

## Limits
Invented functional form; effect sizes (mean tau about 5-7 percentage points) are not estimates of any real offer;
the test cohort has ~1.5k customers, so uplift metrics on it are noisy (bootstrap CIs reported).
