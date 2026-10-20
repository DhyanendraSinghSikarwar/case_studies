# Model card - Credit risk PD model (champion: xgb)
_Generated 2026-10-20 from `outputs/`._

## Intended use
Rank card customers by probability of default (next month), convert to a 300-900 score with bands A-F, and support approve/decline and limit actions in a portfolio-economics analysis. Portfolio/educational use; not validated for live credit decisions.

## Data
UCI "Default of Credit Card Clients" (id 350; Yeh and Lien 2009; CC BY 4.0). 30,000 customers, default rate 22.12%, 590 rows with negative BILL_AMT1 (1930 with any negative bill), 35 duplicate rows (kept). Stratified split: 18,000 / 6,000 / 6,000 (train / valid / test). Amounts are NT$ (converted to INR only for business outputs).

## Models
Baseline logistic on raw features; WOE/logistic scorecard (18 variables, monotonic bins, points table); tuned XGBoost and LightGBM (30 Optuna trials, 3-fold CV on train only) with isotonic calibration fitted on the validation split. Champion chosen on validation AUC of the uncalibrated model; test set evaluated once. SEX is never a model input.

## Metrics (test set, n=6,000)
| Model | Test AUC | Test Gini | Test KS | Test Brier | Cal. slope | Valid AUC |
|---|---|---|---|---|---|---|
| Naive (predict base rate) | 0.500 | 0.000 | 0.000 | 0.1723 | n/a | 0.500 |
| Baseline logistic (raw features) | 0.7243 | 0.4486 | 0.3852 | 0.1437 | 0.983 | 0.7024 |
| WOE scorecard (logistic) | 0.7720 | 0.5439 | 0.4206 | 0.1356 | 0.988 | 0.7627 |
| XGBoost (isotonic-calibrated) **(champion)** | 0.7907 | 0.5815 | 0.4498 | 0.1312 | 1.012 | 0.7863 |
| LightGBM (isotonic-calibrated) | 0.7899 | 0.5798 | 0.4498 | 0.1318 | 1.006 | 0.7840 |
| Benchmark R1 (Abhinav19-isb) | 0.783 | - | 0.424 | - | - | - |

Targets: all met.

| Metric | Target | Achieved (test, champion) | Result |
|---|---|---|---|
| ROC-AUC | >= 0.78 | 0.7907 | PASS |
| KS | >= 0.42 | 0.4498 | PASS |
| Gini | >= 0.56 | 0.5815 | PASS |
| Brier | <= 0.14 | 0.1312 | PASS |
| Calibration slope | 0.9 - 1.1 | 1.012 | PASS |
| Points table reproduces score | within 1 point | max diff 0.043 | PASS |

## Fairness check (at the optimal cut-off 0.19)
**By SEX**

| group | n | approval_rate | bad_rate_approved | default_rate | auc | di_ratio | passes_80pct |
|---|---|---|---|---|---|---|---|
| female | 3628 | 66.8% | 9.4% | 20.8% | 0.795 | 1.000 | True |
| male | 2372 | 63.6% | 12.7% | 24.1% | 0.783 | 0.952 | True |

**By AGE**

| group | n | approval_rate | bad_rate_approved | default_rate | auc | di_ratio | passes_80pct |
|---|---|---|---|---|---|---|---|
| 30-39 | 2206 | 70.1% | 10.0% | 19.9% | 0.793 | 1.000 | True |
| 40-49 | 1296 | 63.5% | 11.5% | 24.5% | 0.794 | 0.906 | True |
| 50+ | 572 | 59.8% | 13.7% | 26.0% | 0.763 | 0.853 | True |
| <30 | 1926 | 63.4% | 10.2% | 21.9% | 0.792 | 0.904 | True |

Disparate-impact ratio = group approval rate / highest group approval rate; 0.8 is a screening heuristic.

## Limitations
- 2005 Taiwanese issuer data, random (not out-of-time) split; population and macro conditions differ from any current book.
- Outcomes observed only over one month; the 'default' definition is the dataset's.
- Profit figures depend on assumed margin, LGD and limit-action effects (swept in the sensitivity analysis, not estimated from data).
- Age and credit limit may act as proxies for protected attributes; disparate-impact ratios are screening metrics.
- Calibration is isotonic on a 6,000-row validation split; recalibrate regularly.
- Top SHAP drivers: max_delay, PAY_0, n_months_delayed, PAY_AMT1, LIMIT_BAL.
