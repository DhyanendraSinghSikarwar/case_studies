---

# Case Study 7 — Quick-commerce demand forecasting with censored sales (Swiggy Instamart) · `cs07_quickcommerce_demand_forecasting.ipynb`

## D-7-01: Data source — synthetic dark-store sales with hidden true demand

- Date: 2026-10-17
- Case: 7
- Context / question: We need sales that are cut by stock and the true demand behind them.
- Options considered: public retail sales sets (none censored, none quick-commerce); synthetic data.
- Decision: 40 stores × 200 SKUs × 105 days, negative-binomial demand, legacy replenishment, substitution spill, perishable waste.
- Why: Only a simulation lets us score a forecast against true demand.
- Assumption checks / evidence: 29.6% stock-out days, mean availability 91.6%.
- Impact if wrong / mitigation: Magnitudes are illustrative; the method transfers.

## D-7-02: Synthetic parameters — legacy rule ratchets stock down

- Date: 2026-10-17
- Case: 7
- Context / question: How should replenishment be modelled?
- Options considered: perfect stocking; stock = last 7 days of sales × 1.10 + 0.5.
- Decision: The second, plus 8% short shipments.
- Why: Sales-based replenishment is the classic censoring trap.
- Assumption checks / evidence: Stock falls 0.8 pp of demand a week (p = 0.04) and settles near 93%.
- Impact if wrong / mitigation: Real rules differ; the ratchet is mild here.

## D-7-03: De-biasing — availability scaling first, profile scaling when estimable

- Date: 2026-10-17
- Case: 7
- Context / question: How do we recover demand from censored sales?
- Options considered: raw sales, availability scaling, profile scaling.
- Decision: Availability scaling as the default; profile scaling when an intraday profile is available.
- Why: Error on stock-out days 40.5% (raw), 16.6% (availability), 1.5% (profile).
- Assumption checks / evidence: Profile scaling uses the simulator's own profile, so 1.5% is an upper bound.
- Impact if wrong / mitigation: A mis-estimated profile would reduce the gain; test on held-out stores.

## D-7-04: Evaluate against true demand, not sales

- Date: 2026-10-17
- Case: 7
- Context / question: Which metric picks the right model?
- Options considered: wMAPE vs observed sales; wMAPE vs true (estimated) demand.
- Decision: Report both; select on true demand.
- Why: Rankings disagree (Spearman −0.50); raw-sales models under-forecast by ~28%.
- Assumption checks / evidence: De-biased GBM wins in all three test weeks and all pairwise tests (Holm p < 1e-4).
- Impact if wrong / mitigation: In practice true demand is unobserved; use estimated demand and availability.

## D-7-05: Grouping SKUs is for substitution, not accuracy

- Date: 2026-10-17
- Case: 7
- Context / question: Does forecasting at the SKU-group level improve accuracy?
- Options considered: SKU-level GBM; group-level GBM allocated to SKUs.
- Decision: Keep SKU-level forecasts.
- Why: wMAPE 0.448 vs 0.454 (CI −0.0074 to −0.0046); slow movers 0.82 either way.
- Assumption checks / evidence: Substitution and availability effects not tested here.
- Impact if wrong / mitigation: If substitution is strong in practice, grouping may help availability estimates.

## D-7-06: Stock by class-specific critical ratio

- Date: 2026-10-17
- Case: 7
- Context / question: What service level should each SKU get?
- Options considered: legacy rule; mean forecast × 1.0/1.1; one quantile (τ = 0.9); class-specific critical ratio.
- Decision: Class-specific ratio (0.93 non-perishable, 0.42 perishable).
- Why: +₹28.2 per store-SKU-day (CI 26.5 to 29.9); fill 88.5% vs 71.3%; expiry 1.87% vs 4.07%. One τ = 0.9 loses ₹11.3.
- Assumption checks / evidence: Quantile coverage conservative because stock is an integer.
- Impact if wrong / mitigation: Margins and waste costs are assumed; re-fit the ratios with real costs.

## D-7-07: Business case — scale to 1,000 stores × 200 core SKUs

- Date: 2026-10-17
- Case: 7
- Context / question: What is the annual value?
- Options considered: point estimate; CI bounds; haircut for long-tail drag.
- Decision: About ₹206 crore base, ₹97 crore pessimistic (×0.5 on the CI low).
- Why: Linear scale-up of a 200-SKU assortment is optimistic.
- Assumption checks / evidence: Test window has no festival days; festival behaviour is untested.
- Impact if wrong / mitigation: Validate with a store-level holdout on fill rate, expiry and profit.
