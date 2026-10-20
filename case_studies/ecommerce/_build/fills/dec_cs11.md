---

# Case Study 11 — Forecasting demand for new fashion styles (Myntra) · `cs11_new_item_demand_forecasting.ipynb`

## D-11-01: Data source — synthetic style-week sales with hidden demand and quality

- Date: 2026-10-20
- Case: 11
- Context / question: Myntra's style-level sales are confidential, and we need a known truth to check drivers and buying plans.
- Options considered: public fashion datasets (no style-week sales with plan data); synthetic data.
- Decision: 9,000 styles, five article types, 104 launch weeks, 4 to 26 weeks of life, hidden quality and expected-demand columns.
- Why: A hidden truth lets us test the driver analysis and give an oracle benchmark.
- Assumption checks / evidence: 103,017 clean style-weeks; zero-sales weeks 8.5%; top 10% of styles make 40% of units.
- Impact if wrong / mitigation: Effect sizes are our assumptions; re-measure on real data.

## D-11-02: Validation — split by launch date, never random

- Date: 2026-10-20
- Case: 11
- Context / question: How do we score a cold-start forecast honestly?
- Options considered: random split of style-weeks; random split of styles; launch-date split (documented in the paper).
- Decision: Train on launches in weeks 0 to 51, validate 52 to 77, test 78 to 103; choose the champion on validation only.
- Why: Random splits were 0.049 (style-weeks) and 0.027 (styles) too optimistic in wMAPE (CIs 0.036 to 0.062 and 0.012 to 0.041).
- Assumption checks / evidence: Colour shares drift by up to 6.9 points between half-years.
- Impact if wrong / mitigation: A real trend break is larger than our drift; monitor bias and coverage.

## D-11-03: Model and loss — gradient boosting on log units

- Date: 2026-10-20
- Case: 11
- Context / question: Which model and loss should forecast new styles?
- Options considered: naive and article-type averages, Poisson linear, random forest, boosting with raw MSE, Poisson and log MSE, small MLP.
- Decision: Boosting with MSE on log units for ranking and allocation.
- Why: Test wMAPE 0.597 (CI 0.586 to 0.607) vs 0.870 naive; beats every rival (Holm p = 0.007), the nearest by only 0.013 (Poisson boosting).
- Assumption checks / evidence: No tuning; paper's LSTM and embeddings not run.
- Impact if wrong / mitigation: Loss choice is a small effect; the Poisson model is the fallback.

## D-11-04: Use the forecast for shares, rescale the totals

- Date: 2026-10-20
- Case: 11
- Context / question: Is the champion calibrated for buying volumes?
- Options considered: use as is; rescale by a calibration factor; switch to Poisson loss.
- Decision: Allocate by forecast share and set the total separately.
- Why: Calibration slope 1.03 (CI 0.99 to 1.07) but the total is 32% low; 80% interval covered 71.5% (77.7% after conformal).
- Assumption checks / evidence: Actual / forecast is 1.41 to 1.61 in every decile.
- Impact if wrong / mitigation: If the bias changes by cohort, recalibrate monthly.

## D-11-05: Aggregate forecasts to attribute combinations for budgets

- Date: 2026-10-20
- Case: 11
- Context / question: Does the forecast rank combinations for buying budgets?
- Options considered: style-level only; article type x colour x price band combinations.
- Decision: Report Pearson, Kendall Tau and top-quintile capture over 180 combinations.
- Why: r = 0.88, Tau = 0.71, capture 42.0% (best possible 44.9%, naive 36.3%).
- Assumption checks / evidence: Poisson linear is nearly as good (Tau 0.70, capture 42.3%).
- Impact if wrong / mitigation: A simple model may be enough at combination level; the oracle capture interval looked biased, so read intervals loosely.

## D-11-06: Do not read merchandising coefficients as causal

- Date: 2026-10-20
- Case: 11
- Context / question: Can buyers use the driver model to set visibility or discount?
- Options considered: naive Poisson; Poisson with the hidden quality term; experiments.
- Decision: Use drivers for explanation only; run experiments before changing placement.
- Why: Naive visibility coefficient 1.65 vs true 0.50; adjusted 0.46. Discount is recovered (0.023 vs 0.022).
- Assumption checks / evidence: Merchandising is the largest feature group (wMAPE +0.206 when shuffled).
- Impact if wrong / mitigation: Real quality is unobserved; use randomised placement tests.

## D-11-07: Buying simulation and ₹ assumptions

- Date: 2026-10-20
- Case: 11
- Context / question: What is the value of a forecast-guided buy?
- Options considered: equal split vs forecast-proportional vs oracle; liquidation at 25%, 35%, 45% of list.
- Decision: Unit cost 55% of list, full-price realisation 85%, base liquidation 35%; scale to 50,000 styles a year at 30%, 60%, 90% adoption.
- Why: Sell-through +16.0 points (CI 14.8 to 17.2); base ₹233,237 per style, about ₹700 crore a year (worst ₹188 crore, best ₹1,629 crore).
- Assumption checks / evidence: Captures 58% of the oracle gain.
- Impact if wrong / mitigation: The equal split is a weak baseline; compare to the buyer's actual plan in a live test.

## D-11-08: Pilot design and decision rule

- Date: 2026-10-20
- Case: 11
- Context / question: How do we confirm the gain on real data?
- Options considered: full rollout; brand-level holdout test.
- Decision: Pilot with a styles-level holdout; go if sell-through beats the buyer plan by at least 5% relative with the interval above zero.
- Why: 1,095 styles per arm detect 7% (537 for 10%, 2,145 for 5%) with 80% power.
- Assumption checks / evidence: One early week of sales cuts wMAPE from 0.608 to 0.538, so refresh after week 1.
- Impact if wrong / mitigation: Stop and retrain if coverage falls below 70% or error approaches the naive baseline.
