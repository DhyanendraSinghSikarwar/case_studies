---

# Case Study 3 — Dark-store demand planning, newsvendor and picking batching (Swiggy Instamart) · `cs03_dark_store_inventory.ipynb`

## D-03-01: Data source — synthetic pod logs with a replayable inventory twin

- Date: 2026-10-20
- Case: 3
- Context / question: We need pod inventory, wastage by shelf life and hourly sales, plus a known truth so any ordering policy can be replayed.
- Options considered: public retail sets (M5, Instacart, Favorita; no hourly stock state, no wastage, not Indian quick commerce); synthetic logs.
- Decision: 48 pods x 120 SKUs x 84 days with hidden hourly demand, FIFO ageing, vendor short-shipments, plus a synthetic picking order log.
- Why: EA/EW validity and ordering rules can only be scored against a known truth.
- Assumption checks / evidence: 483,600 clean pod-SKU-days; availability 86.4%, wastage 7.8% of units; true demand 1.93x sales when availability was below 75%.
- Impact if wrong / mitigation: Gains depend on assumed noise and costs; re-estimate on real pod logs.

## D-03-02: Judge forecast models by simulated availability and wastage, not wMAPE alone

- Date: 2026-10-20
- Case: 3
- Context / question: Does wMAPE on sales pick the model that is best for the business?
- Options considered: wMAPE on all rows; wMAPE on high-availability rows; EA/EW.
- Decision: Use EA/EW as the screen and a pod experiment as the decision.
- Why: wMAPE on all rows favours M1 (0.2385 vs 0.2406) but on availability >= 90% rows favours M2 (0.2694 vs 0.2725); both under-forecast true demand by 24% to 25%.
- Assumption checks / evidence: Hourly EA lift -0.37 pp (CI -0.42 to -0.32) vs true -0.39 pp; simple EA -0.49 pp.
- Impact if wrong / mitigation: EA is a one-day estimate with no carry-over; use the full replay where a simulator exists.

## D-03-03: Newsvendor order rule by category

- Date: 2026-10-20
- Case: 3
- Context / question: Fixed buffer or service-level (quantile) ordering?
- Options considered: fixed buffer m; negative-binomial newsvendor at quantile q; tuned on even pods, tested on odd pods.
- Decision: Newsvendor for dairy and non-perishables; keep the fixed buffer for fresh produce and bakery.
- Why: Gains on held-out pods: dairy +₹204, packaged +₹616, snacks +₹197, home care +₹1,334 per category-pod-day (Holm p < 0.001); produce -₹68 (p = 0.001); bakery -₹15 (p = 0.12).
- Assumption checks / evidence: Non-perishables chose grid edges (q 0.995, m 1.8); fitted dispersion was too high (17 to 50 vs true 5 to 12).
- Impact if wrong / mitigation: Widen the grid and fit dispersion censoring-aware.

## D-03-04: Do not use the textbook critical ratio for 2 to 3 day items

- Date: 2026-10-20
- Case: 3
- Context / question: Is q = CR the right service level?
- Options considered: q = CR; empirical profit-maximising q on the replay.
- Decision: Choose the quantile for multi-day items by replay or experiment.
- Why: CR is 0.45 for dairy and 0.49 for produce but best q was 0.995 and 0.98, because leftovers carry over.
- Assumption checks / evidence: Goodwill cost of a lost sale (50% of price) is our assumption.
- Impact if wrong / mitigation: The optimum moves with the assumed lost-sale cost; test it.

## D-03-05: Quantile GBM at the critical ratio as the planning model

- Date: 2026-10-20
- Case: 3
- Context / question: Which rule to roll out?
- Options considered: legacy buffer x M2; negative-binomial newsvendor; quantile GBM at CR.
- Decision: Quantile GBM per category, with produce and dairy levels set by replay rather than the clipped CR.
- Why: Profit ₹5,252 vs ₹1,715 per pod-day (+₹3,537, CI ₹3,369 to ₹3,685); availability 89.7% vs 83.7%; wastage 3.3% vs 4.7%; beat the newsvendor by ₹1,289.
- Assumption checks / evidence: Produce and dairy quantile was clipped at 0.5.
- Impact if wrong / mitigation: Part of the gap is a weak legacy rule; confirm in a live test.

## D-03-06: Pod experiment design and size

- Date: 2026-10-20
- Case: 3
- Context / question: How many pods does a store experiment need?
- Options considered: 24 v 24 raw; ANCOVA on pre-period availability; cluster randomisation.
- Decision: Randomise pods, adjust for pre-period availability; at least 8 pods per arm for 1 pp (21 raw, 19 if by cluster).
- Why: Pod SD 1.13 pp falls to 0.69 pp after adjustment; ICC 0.29, design effect 2.47; 24 v 24 detects only 0.56 pp.
- Assumption checks / evidence: In the 24 v 24 run, leak-free hourly EA -0.12 pp (CI -0.87 to +0.66) vs actual -0.50 pp (CI -0.90 to -0.10); leaky -0.52 pp was closer, so leakage was not shown.
- Impact if wrong / mitigation: Real pod variance may differ; measure it from pre-period data.

## D-03-07: Batching up to 2 orders only as a surge valve

- Date: 2026-10-20
- Case: 3
- Context / question: When does batching help?
- Options considered: no batching; similarity thresholds 0.2, 0.4, 0.6; 4 to 7 pickers.
- Decision: Batch only when pickers are scarce (similarity 0.2 to 0.4); do not count on it to remove a picker.
- Why: At 4 pickers order-to-ready fell 17.6 s (CI 9.6 to 25.5) from 243.7 s with +0.47 errors per pod-day; at 5 about zero; at 6 to 7 worse by 0.4 to 1.2 s.
- Assumption checks / evidence: Time-to-pack model R² 0.737 recovers 10.2 s per item and 24.2 s per zone; the gain-vs-staffing slope was not significant (p = 0.23).
- Impact if wrong / mitigation: Picking parameters are assumed; Swiggy gives only qualitative results.

## D-03-08: ₹ business case with a realisation haircut

- Date: 2026-10-20
- Case: 3
- Context / question: What is the annual value?
- Options considered: apply the simulated gain directly; apply a haircut.
- Decision: Base ₹98 crore a year (worst ₹21, best ₹215); picking ₹0.
- Why: Simulated gain is 4.49% of sales, too large to bank; 400 pods, ₹6 lakh sales per pod-day and a 25% survival share (15% to 35%) are assumptions.
- Assumption checks / evidence: No picker saving because batching at 4 pickers (226 s) does not reach the unbatched time at 5 (193 s).
- Impact if wrong / mitigation: Value scales with the assumed haircut, pod count and pod sales.
