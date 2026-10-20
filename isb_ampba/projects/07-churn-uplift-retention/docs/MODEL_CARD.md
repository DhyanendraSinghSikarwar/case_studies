# Model card - churn model and uplift learner (case study 07)

## Intended use
Rank eligible online-retail customers (>= 2 orders in the previous 180 days) by 90-day churn risk and by predicted
incremental response to a retention offer, to prioritise a retention budget. Portfolio / teaching project, not a production system.

## Out-of-scope use
Individual-level decisions with legal or financial consequences; other businesses or time periods without refit; reading the
simulated uplift results as evidence about real offers.

## Training data
UCI Online Retail II (real transactions, 2009-12-01 to 2011-12-09). Snapshots 2011-03-01, 2011-04-01, 2011-05-01 stacked
(5,131 customer-snapshot rows; customers repeat, so folds are grouped by customer). Test: 2011-08-01 (1,471 customers;
1,126 also appear in training). Pilot treatment is SIMULATED (docs/SIMULATOR.md). 7 snapshots built in total.

## Models
Logit, RandomForest, XGBoost, LightGBM; champion chosen by grouped-CV AUC on training snapshots only: `logit`;
isotonic calibration with group-aware folds. Uplift: S/T/X/transformed-outcome/class-transformation learners
(LightGBM base), selected by grouped-CV Qini on the training pilot: `S`. Seed 42.

## Metrics (test snapshot 2011-08-01)
| Metric | Champion (raw) | Champion (calibrated) | Naive baseline |
|---|---|---|---|
| ROC-AUC | 0.747 | 0.746 | 0.500 |
| PR-AUC | 0.523 | 0.518 | - |
| KS | 0.382 | 0.385 | - |
| Brier | 0.176 | 0.177 | 0.217 |
| Mean prediction (observed 0.285) | 0.322 | 0.319 | 0.401 |

Grouped-CV AUC on the training snapshots: 0.783; the gap to the test AUC reflects seasonal
non-stationarity. Uplift (simulated pilot): selected learner Qini 6,307
(95% CI -7,887 to
21,115).

## Fairness / segment checks
No protected attributes exist in the data; the only demographic-like feature is `is_uk` (country). Customers are wholesalers
and consumers mixed. Segment view of the simulated response (by construction of the simulator):

| Segment (test) | Customers | Mean true tau (simulated) |
|---|---|---|
| Champions | 194 | 0.000 |
| Hibernating | 107 | 0.023 |
| Mid-frequency | 482 | 0.080 |
| Other | 688 | 0.041 |

Check calibration and Qini by segment (UK vs non-UK, value tercile) before any real use; this has not been done here.

## Known failure modes
Calibration drifts across seasons (test mean prediction vs observed above); AUC below target on this split; wholesaler
outliers in `monetary_6m`; uplift estimates are noisy on ~1.5k customers; IPW evaluation on Hillstrom has wide intervals.

## Monitoring plan
Monthly: AUC and calibration by snapshot; population stability of features; holdout Qini once a real pilot exists; refit quarterly.

## Version
churnx 0.1.0, seed 42, config/config.yaml as committed.
