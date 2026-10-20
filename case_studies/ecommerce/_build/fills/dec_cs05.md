---

# Case Study 5 — Delivery promise date with breach control (Myntra) · `cs05_delivery_promise_date.ipynb`

## D-5-01: Data source — synthetic orders with hidden processing and shipping times

- Date: 2026-10-20
- Case: 5
- Context / question: We need orders with lanes, 3PL, backlogs and sale days, and a known process, to test breach control and coverage.
- Options considered: public logistics data (none Indian, none with sale days or lanes); synthetic orders.
- Decision: 60 days, 141,824 clean orders, 6 warehouses, 60 centres, three zones, two sale events.
- Why: The paper publishes only aggregate results; the structure (legs, pendency, 3PL, holidays, HRD) is documented, so we simulate it.
- Assumption checks / evidence: Median delivery 3 days (range 1 to 18); BAU mean 3.46 days, sale days 4.06; 22.1% of orders on sale days.
- Impact if wrong / mitigation: Sale-day effect and 3PL tails are assumed; recalibrate and re-run the segment tests on real data.

## D-5-02: Protocol — time split with an embargo, target 5% breach

- Date: 2026-10-20
- Case: 5
- Context / question: How do we evaluate a promise rule without leaking outcomes that are not yet known?
- Options considered: random split; train, calibrate, embargo (outcomes maturing), then test.
- Decision: Train days 0-34, calibrate 35-39, embargo 40-44, test 45-59 (includes a sale event).
- Why: Delivery takes days, so recent orders have no outcome yet.
- Assumption checks / evidence: 80,667 train, 9,816 calibration, 41,222 test orders.
- Impact if wrong / mitigation: A single static fit is harsher than daily retraining; retrain daily in production.

## D-5-03: Quantile regression over mean-plus-buffer or asymmetric loss as the base model

- Date: 2026-10-20
- Case: 5
- Context / question: Which model family should produce the safe date?
- Options considered: rule-based table; mean + 1 day; expectile (asymmetric) loss; quantile regression at 0.95.
- Decision: Gradient-boosted quantile regression at 0.95.
- Why: Lowest pinball loss (0.149 vs 0.158, 0.177 and 0.195); 0.75 points fewer breaches than the table (Holm p below 1e-4); expectile lands on an unplanned 2.3% breach.
- Assumption checks / evidence: At 5% breach a tuned mean + buffer reaches 84.0% accuracy vs 81.1% for quantile regression, so the frontier gain is not established. Quantile predictions cross for 11 to 12% of orders.
- Impact if wrong / mitigation: If the buffer rule is as good, prefer it for simplicity; compare in a live test.

## D-5-04: Conformal offset on normal days

- Date: 2026-10-20
- Case: 5
- Context / question: Plain quantile regression breaches only 1.3% against a 5% target; how do we use the slack?
- Options considered: plain quantile regression; split-conformal; Mondrian by zone; 3-day feedback; 10-day rolling conformal.
- Decision: Split-conformal offset on the rounded score scale.
- Why: BAU breach 4.9% (CI 3.8% to 5.9%), accuracy 73.7% vs 37.4%, mean promise 4.28 vs 5.29 days; the finite-sample coverage law was verified (mean 94.9% to 95.0%, KS p 0.34 to 0.69).
- Assumption checks / evidence: Mondrian zone is no better (4.9%, zone differences still significant, Holm p 0.002); orders after 16:00 breach 6.0%.
- Impact if wrong / mitigation: Valid only if calibration and future days are exchangeable; monitor by zone and cut-off.

## D-5-05: No conformal offset on sale and post-sale days

- Date: 2026-10-20
- Case: 5
- Context / question: Does the calibration transfer to sale days?
- Options considered: same offset; zone offsets; rolling offsets; plain quantile regression on sale days.
- Decision: Hybrid: offset on normal days, plain quantile regression on sale and post-sale days.
- Why: The offset breaches 9.6% on sale days and 11.8% after (coverage 90.4% and 88.2%; KS p below 1e-20); the hybrid gives 4.6% and 4.3%, against 6.8% and 6.4% for the table.
- Assumption checks / evidence: The hybrid was chosen after seeing this sale event, on the same test days.
- Impact if wrong / mitigation: Confirm on the next sale; consider a sale-specific calibration from a proxy event.

## D-5-06: Reject short-window feedback breach control

- Date: 2026-10-20
- Case: 5
- Context / question: Can recent errors correct the model, as the paper's third route does?
- Options considered: 3-day feedback; 10-day rolling conformal.
- Decision: Do not use windows shorter than the delivery time.
- Why: Only 6.6% of the last 3 days (62.8% of 10 days) is delivered, and those are fast orders; the 3-day rule breaches 34% on BAU days; the 10-day rule 6.9% (sale 10.7%).
- Assumption checks / evidence: Mean 3-day offset -1.91 days against -1.01 for the calibration offset.
- Impact if wrong / mitigation: A censoring-aware correction might work; not tested here.

## D-5-07: Certify breach by zone, not by lane

- Date: 2026-10-20
- Case: 5
- Context / question: At what level can we verify the 5% limit?
- Options considered: lane level; zone and courier level.
- Decision: Monitor and certify by zone, courier and cut-off timing.
- Why: ±1 point needs 1,825 orders (4,034 with daily clustering); no lane reaches that in a week (median 14 orders), and zones have 2,500 to 8,700.
- Assumption checks / evidence: Design effect 2.2 from about 2,000 orders a day.
- Impact if wrong / mitigation: Lanes can drift unseen; borrow strength through the model and use longer windows for large lanes.

## D-5-08: Business case and the 5% limit

- Date: 2026-10-20
- Case: 5
- Context / question: What is a tighter promise worth, and is 5% the right limit?
- Options considered: plain quantile regression; split-conformal; Mondrian; rolling; mean + 1 day.
- Decision: Treat ₹15.8 crore (split-conformal) and ₹19.3 crore (quantile regression) a year as base-case orders of magnitude; revisit the breach limit.
- Why: Split-conformal ranges from ₹-1.4 crore (worst) to ₹42.3 crore (best); quantile regression ₹7.4 to ₹35.7 crore; the newsvendor τ* is 0.97 in the base case.
- Assumption checks / evidence: 2 lakh orders a day, ₹1,300 order, 22% margin; 1% conversion per promised day; breach costs ₹94 (6% churn × ₹900 + ₹40).
- Impact if wrong / mitigation: Elasticities are assumptions; measure them in an A/B test of the promise rule.
