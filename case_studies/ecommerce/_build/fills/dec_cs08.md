---

# Case Study 8 — Price elasticity and discount efficacy (Flipkart, outside academic analysis; weak evidence) · `cs08_price_elasticity_discounts.ipynb`

## D-08-01: Data source — synthetic SKU-week panel with hidden elasticity

- Date: 2026-10-19
- Case: 8
- Context / question: No public Indian marketplace data has prices and units; the only public source (arXiv 2005.04612) is an outside study of public Flipkart prices without sales. We need a hidden truth to check estimators.
- Options considered: public price scrapes (no units); synthetic panel with hidden elasticity, endogenous pricing, post-promotion dips, MRP inflation and a randomised price test.
- Decision: 600 SKUs in 8 categories over 52 weeks (31,800 rows before cleaning), true category elasticity means −1.4 to −2.6, 120 SKUs in a 8-week ±10% price experiment.
- Why: Every estimator can be scored against the truth. Evidence is weak: this is an interview-standard solution on simulated data, not a reproduction of any company system.
- Assumption checks / evidence: 600 duplicates, 481 missing prices, 94 paise errors and 968 stock-outs found and handled; modelling frame 28,623 rows.
- Impact if wrong / mitigation: All elasticities, dips and rupee figures are assumptions; the method ranking (naive biased, IV and experiment sound) is the transferable result.

## D-08-02: Estimating elasticity — instrument plus experiment, not naive or control-only regressions

- Date: 2026-10-19
- Case: 8
- Context / question: Which estimator can be trusted when sellers set prices in response to demand?
- Options considered: pooled OLS; SKU fixed effects; fixed effects with sale flag, competitor price and week effects; IV with the supplier-cost index; randomised test.
- Decision: Use IV (supplier cost shocks) for breadth and a randomised price test for validation.
- Why: Pooled OLS gave −0.24 and controls-only fixed effects −1.51, against a true −1.97; IV gave −1.94 (CI −2.05 to −1.83, first-stage F = 5,658) and the experiment −2.00 (CI −2.30 to −1.70). IV differs from fixed effects (Hausman-type z = −9.2).
- Assumption checks / evidence: Cost index uncorrelated with last week's residual (+0.003); exclusion cannot be tested with one instrument; SKU fixed effects alone (−1.99) are close, apparently by cancelling biases.
- Impact if wrong / mitigation: If the cost shock also moves quality or stock in real data, IV is biased; confirm with price experiments.

## D-08-03: Category elasticities drive the promotion policy

- Date: 2026-10-19
- Case: 8
- Context / question: Do all categories respond enough to price to justify discounts?
- Options considered: one pooled elasticity; category IV estimates with Holm-corrected tests against −1.
- Decision: Set policy by category using IV estimates and CIs.
- Why: All eight are elastic (−1.41 for mobiles to −2.74 for mobile accessories); H0 ε = −1 rejected in all after Holm (mobiles p = 0.024); all CIs cover the truth.
- Assumption checks / evidence: First-stage F 567 to 847 by category; CIs 0.5 to 0.7 wide, so neighbouring categories are not distinguishable.
- Impact if wrong / mitigation: Mobiles' CI upper end (−1.06) is near −1; treat mobiles as marginal and test directly.

## D-08-04: Judge promotions on three-week net units, not sale-week lift

- Date: 2026-10-19
- Case: 8
- Context / question: Does the sale-week lift survive the weeks after?
- Options considered: sale-week lift only; event study with two lags and a cluster bootstrap.
- Decision: Report net units over the promotion week and the next two weeks.
- Why: Estimated lift +64% then −16% and −8%; net +13.6% (CI +12.3% to +14.9%). Truth in the simulation is +24.2% net, so the event study overstates the dip.
- Assumption checks / evidence: Promotion flag (15% below trailing median) has precision 92.6% and recall 87.0% against the hidden truth.
- Impact if wrong / mitigation: The estimated dip is conservative; a real test with randomised promotions would measure it directly.

## D-08-05: Define a real sale against the SKU's own price history, not MRP

- Date: 2026-10-19
- Case: 8
- Context / question: Is a "% off MRP" badge an honest test of a significant discount?
- Options considered: badge (30% or more off MRP); 15% or more below the trailing 8-week median price.
- Decision: Use the trailing-median definition for audits and analysis; do not use the badge.
- Why: 32.6% of SKU-weeks carry the badge but 10.7% are real sales; badge precision 23.8%, recall 73.3%, kappa 0.236 (CI 0.209 to 0.268); every false badge is on an inflated-MRP SKU.
- Assumption checks / evidence: McNemar: 7,103 badge-only weeks vs 806 true-only weeks.
- Impact if wrong / mitigation: The paper's definition of significance is not documented, so this is our own definition; the 15% threshold is a choice.

## D-08-06: Classifier of significant discounts — report the majority baseline

- Date: 2026-10-19
- Case: 8
- Context / question: Can SVM-style classifiers call a discount significant, as the paper claims (accuracy 91.11%, authors' claim, not tested)?
- Options considered: logistic regression, SVM (RBF), gradient boosting; with and without the sale-week flag; 70/30 split by SKU.
- Decision: Treat accuracy near 90% as uninformative; use PR-AUC and balanced accuracy and always show the baseline.
- Why: Majority baseline is 89.4% accuracy. With the sale flag: 92.0% accuracy, PR-AUC 0.449 (prevalence 0.106), McNemar p = 2.6e-16. With product features and price only: 89.4%, F1 = 0.
- Assumption checks / evidence: Default settings, no tuning; SVM trained on 6,000 rows.
- Impact if wrong / mitigation: Real data may carry more signal in product features; re-run on scraped prices.

## D-08-07: Stop platform-funded promotions below break-even; move them to seller funding

- Date: 2026-10-19
- Case: 8
- Context / question: Do platform-funded discounts pay back?
- Options considered: keep all promotions; stop where the base three-week profit multiplier is below 1; seller funding.
- Decision: Fund a promotion only if its multiplier at the less elastic end of the CI is at least 1; otherwise seller-funded or none.
- Why: At 17% take rate and 10% platform funding every category is below 1 (0.91 to 0.99); break-even elasticity for a 20% promotion is −1.79 (0% funding), −2.88 (10%) and −4.76 (25%). Stopping is worth about ₹136 crore a year (₹106 to ₹160 crore) on an assumed ₹30,000 crore of GMV.
- Assumption checks / evidence: Take rate, funding share and GMV are assumptions; the dip estimate overstates the true dip; acquisition and ad value are excluded.
- Impact if wrong / mitigation: Rupee figure may be too high; the category ranking is the more reliable result. Validate with seller-funded versus platform-funded tests.

## D-08-08: Size price experiments for a 0.3 half-width

- Date: 2026-10-19
- Case: 8
- Context / question: How large must a category price test be?
- Options considered: current design (120 SKUs, 8 weeks); larger tests for half-widths 0.5, 0.3, 0.2, 0.1.
- Decision: Plan about 90 SKUs for 8 weeks per category for a half-width of 0.3.
- Why: Current half-width is 0.30 and the minimum detectable elasticity is 0.43; half-width 0.2 needs about 203 SKUs and 0.1 about 809 SKUs.
- Assumption checks / evidence: Arms balanced on prior sales (ANOVA p = 0.48); cut and rise slopes (−2.17 vs −1.80) not different (p = 0.46).
- Impact if wrong / mitigation: Real demand noise is likely higher than the simulated residual sd of 0.31; re-size with real variance.
