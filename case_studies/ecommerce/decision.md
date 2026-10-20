# Decision Log: Indian Ecommerce and Quick-Commerce Case Studies

Every sourcing, modelling and interpretation decision, in the format used in the fintech project: **Date / Case / Context / Options / Decision / Why / Assumption checks / Impact**, followed by a summary table at the end.

---

# Project-wide decisions

## D-0-01: All outcome data is synthetic

- Date: 2026-10-17
- Case: 0 (all)
- Context / question: Ecommerce, quick-commerce and food-delivery logs are confidential. Can public data replace them?
- Options considered: public datasets (Instacart, Olist, Retailrocket, Criteo, Kaggle-hosted sets: several are Kaggle-only or lack the needed fields); scraping marketplaces (terms-of-service and robots restrictions); synthetic data calibrated to documented figures.
- Decision: Synthetic data with hidden ground-truth columns (prefixed `_`), calibrated to figures the cited sources state. No Kaggle data and no scraping.
- Why: Only simulation provides both realistic messiness and a known truth against which methods can be checked.
- Assumption checks / evidence: Each notebook separates documented from simulated parameters in section 2.
- Impact if wrong / mitigation: Magnitudes are illustrative. Methods transfer; re-run on real data.

## D-0-02: Evidence levels and substitutions in the case list

- Date: 2026-10-17
- Case: 0 (all)
- Context / question: Public method detail is uneven across companies.
- Options considered: fill gaps from memory; substitute a better-documented company; mark ND.
- Decision: Research agents recorded only facts they opened, substituted better-documented companies where needed (stated in each entry), and marked everything else ND. Six cases are Weak: the notebooks for those are interview-standard problems on simulated data.
- Why: Not inventing "documented" facts.
- Assumption checks / evidence: Evidence column in the README; entries in the reference file.
- Impact if wrong / mitigation: None.

## D-0-03: Same method standards as the fintech series

- Date: 2026-10-17
- Case: 0 (all)
- Context / question: Which standards apply to every notebook?
- Options considered: ad hoc; the fintech standards.
- Decision: Seed 42; pandas, numpy, scipy, statsmodels, scikit-learn, matplotlib, seaborn (xgboost or boosting via scikit-learn); every chart titled, labelled and followed by a takeaway; observations written after execution; no hyper-parameter tuning; honest reporting of null and negative results.
- Why: Comparability and honesty.
- Assumption checks / evidence: `_build/nbtool.py verify` on every notebook.
- Impact if wrong / mitigation: None.

---

# Case Study 1 — Delivery-time promise and live ETA (Swiggy) · `cs01_delivery_eta_prediction.ipynb`

## D-1-01: Data source — synthetic sessions, delivery legs, and a randomised promise offset

- Date: 2026-10-17
- Case: 1
- Context / question: We need cart sessions with both the shown promise and the outcome, plus a causal handle on what a promised minute costs.
- Options considered: public delivery datasets (none Indian, none with the shown promise or conversion); synthetic data.
- Decision: 220,000 sessions across 3 cities with four delivery legs, a legacy promise and a ±3 min randomised offset.
- Why: The conversion cost of a promised minute cannot be learned from observational logs alone.
- Assumption checks / evidence: Legs add up to the total within 0.02 min; covariates balanced across offsets.
- Impact if wrong / mitigation: Magnitudes are illustrative; the method transfers. Re-estimate with a real randomised test.

## D-1-02: Synthetic parameters — last mile dominates, legs negatively correlated

- Date: 2026-10-17
- Case: 1
- Context / question: How should delivery legs be modelled?
- Options considered: independent legs; legs linked through a rider-waiting mechanism.
- Decision: The second, so a rider who arrives early waits longer.
- Why: The documented stage-wise structure and the practical failure of summing independent leg models.
- Assumption checks / evidence: Last mile 54% of variance; wait vs first mile correlation −0.47.
- Impact if wrong / mitigation: Real correlations differ; test on real stage logs.

## D-1-03: Model choice — direct model for the total, joint network for stage-wise ETAs

- Date: 2026-10-17
- Case: 1
- Context / question: Predict the total directly, sum independent leg models, or use a joint model?
- Options considered: legacy promise, restaurant-hour mean, gradient boosting, four independent leg models, joint multi-output network.
- Decision: Gradient boosting for the cart promise; the joint network where stage consistency matters.
- Why: Boosting MAE 4.63 vs legacy 9.52 (paired ΔMAE −4.9, CI −4.96 to −4.82); summing independent legs 4.99 and biased by −2.8 min.
- Assumption checks / evidence: Time-based split (train to day 20, test the last week); Wilcoxon p < 1e-4.
- Impact if wrong / mitigation: Drift would erode the gain; monitor MAE and coverage weekly.

## D-1-04: Promise is a quantile — calibrate by binomial test

- Date: 2026-10-17
- Case: 1
- Context / question: What number should the customer see?
- Options considered: predicted mean; mean plus padding; quantile model at level τ.
- Decision: Quantile gradient boosting; coverage is checked against τ.
- Why: Coverage 50.3 / 60.4 / 70.3 / 79.9 / 89.8% for τ = 0.5…0.9, all binomial p > 0.14.
- Assumption checks / evidence: Calibration holds in almost every segment; fast-prep kitchens over-covered (81.5%, q = 0.0008).
- Impact if wrong / mitigation: Rain calibration is untested (dry test week); test before the monsoon.

## D-1-05: Estimate the cost of a promised minute from the randomised arm

- Date: 2026-10-17
- Case: 1
- Context / question: How much does a longer promise reduce orders?
- Options considered: observational slope; randomised ±3 min offset.
- Decision: Randomised logistic estimate, with the observational slope as a check.
- Why: OR 0.960 per minute (CI 0.954 to 0.967) vs observational 0.957; placement 69.3 / 66.8 / 63.9% at −3 / 0 / +3 min.
- Assumption checks / evidence: Covariates balanced across offsets.
- Impact if wrong / mitigation: Real observational slopes are usually more biased; keep the randomisation running.

## D-1-06: Pick the percentile by expected margin with a service guardrail

- Date: 2026-10-17
- Case: 1
- Context / question: Which τ should we ship?
- Options considered: τ = 0.5 to 0.9 on the test week.
- Decision: τ = 0.7 (+₹1.81 per session, 10.6% late by more than 5 min) over τ = 0.5 (+₹2.20, 20.0% late).
- Why: Legacy is already late 14.5% of the time; a rise to 20% is not acceptable when lateness costs are assumed small.
- Assumption checks / evidence: Margin ₹55, care contact ₹40, cancellation ₹180; 5 lakh orders a day.
- Impact if wrong / mitigation: Replace assumed costs with measured ones; the choice may move toward a higher τ.

## D-1-07: Live ETA — chain the stage models, accept real jumps

- Date: 2026-10-17
- Case: 1
- Context / question: Do chained stage models reduce ETA jumps?
- Options considered: independent stage models; chained models.
- Decision: Chained models; no extra smoothing at pickup.
- Why: Early-stage jumps fall ~10% (1.21 vs 1.35 min) but the pickup jump is 3.6 min either way, with 23% of customers seeing > 5 min.
- Assumption checks / evidence: Wilcoxon p < 1e-4.
- Impact if wrong / mitigation: A damper may hide real information; test the customer experience.

## D-1-08: Validation — switchback test, not a session-level A/B

- Date: 2026-10-17
- Case: 1
- Context / question: How should we test the new promise live?
- Options considered: session-level randomisation; city-hour switchback.
- Decision: Switchback with about 463 blocks per arm (about 9 days) for +1 pp conversion.
- Why: Sessions in a city-hour share rider supply and demand, so session-level randomisation understates variance; between-block SD of conversion is 0.054.
- Assumption checks / evidence: Session-level needs 34,550 per arm for +1 pp (138,746 for +0.5 pp).
- Impact if wrong / mitigation: Carry-over between blocks; add a washout period.

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

---

# Case Study 15 — Item-to-item collaborative filtering (Amazon) · `cs15_item_to_item_collaborative_filtering.ipynb`

## D-15-01: Data source — synthetic purchases with hidden taste and popularity

- Date: 2026-10-17
- Case: 15
- Context / question: We need purchases plus a known truth so that offline and online evaluation can both be run.
- Options considered: public logs (Instacart, Retailrocket, Amazon reviews; none Indian, none with known truth); synthetic data.
- Decision: 15,000 customers × 2,500 items over 180 days with a 12-dimension taste model, long-tailed popularity and 120 accessory pairs.
- Why: The digital-twin test needs a hidden click model.
- Assumption checks / evidence: Density 0.44%; 15.5% of customers with 3 or fewer purchases; top 1% of items = 21% of purchases.
- Impact if wrong / mitigation: Method rankings depend on the taste-vs-popularity mix; re-measure on real logs.

## D-15-02: Evaluation protocol — leave the last purchase out, in time order

- Date: 2026-10-17
- Case: 15
- Context / question: How do we score a recommender without leaking the future?
- Options considered: random hold-out; leave-last-out by time.
- Decision: Hold out each customer's last purchase; report HR@10, NDCG@10, MRR, with Wilson CIs.
- Why: Random hold-out lets the model see later behaviour.
- Assumption checks / evidence: 14,160 evaluation customers.
- Impact if wrong / mitigation: Logged purchases reflect past exposure; confirm with a live test.

## D-15-03: Item-to-item filtering as the default

- Date: 2026-10-17
- Case: 15
- Context / question: Which method should generate candidates?
- Options considered: best-sellers, user-based CF, item-to-item, damped item-to-item, SVD-32, sequence-aware co-purchase.
- Decision: Item-to-item with a top-50 neighbour table.
- Why: HR@10 19.7% (CI 19.1% to 20.4%) vs 11.2% for best-sellers; every gap significant (McNemar, Holm p < 1e-4).
- Assumption checks / evidence: Smallest gaps are to user-based (0.015 NDCG) and sequence-aware (0.017).
- Impact if wrong / mitigation: Matrix factorisation was untuned; revisit with tuning.

## D-15-04: Cold start — fall back to best-sellers for the first purchase

- Date: 2026-10-17
- Case: 15
- Context / question: Does item-to-item work for customers with little history?
- Options considered: item-to-item for all; best-sellers for the first purchases.
- Decision: Item-to-item from 2 items; best-sellers below that.
- Why: Lift over best-sellers is only 1.27× for 1 to 3 items, 1.76× for 4 to 9 and 2.03× for 10+ (interaction p = 1.3e-7).
- Assumption checks / evidence: Best-sellers HR 14.3% for 1 to 3 items vs 18.1% for item-to-item.
- Impact if wrong / mitigation: Real new customers may be less predictable; monitor by history bucket.

## D-15-05: Popularity damping on discovery surfaces only

- Date: 2026-10-17
- Case: 15
- Context / question: Do we accept popularity bias?
- Options considered: none; damping at scoring time with exponent 0.3.
- Decision: Damp on home and discovery surfaces, not on product-page lists.
- Why: Damping lowers HR@10 from 19.7% to 14.3% but raises tail hits from 3.8% to 5.9%, coverage from 72% to 90% and lowers Gini from 0.95 to 0.84.
- Assumption checks / evidence: A first damping at neighbour-table level collapsed accuracy (HR 2.8%) because rare items dominate; scoring-time damping with a +10 support floor avoids that.
- Impact if wrong / mitigation: Pick the exponent in a live test; the offline numbers cannot value diversity.

## D-15-06: Add a sequence-aware list for accessories

- Date: 2026-10-17
- Case: 15
- Context / question: How do we serve "goes with this" items?
- Options considered: item-to-item only; co-purchase within 7 days.
- Decision: Separate sequence-aware list for accessory placements.
- Why: Hit rate on accessory-pair purchases 70% vs 27% (item-to-item) and 1% (best-sellers).
- Assumption checks / evidence: Only 112 such test purchases; the percentages are uncertain.
- Impact if wrong / mitigation: Confirm on a larger real sample.

## D-15-07: Offline vs online — use the twin to check, A/B to confirm

- Date: 2026-10-17
- Case: 15
- Context / question: Can offline accuracy replace an A/B test?
- Options considered: offline only; twin expected CTR; live test.
- Decision: Treat offline ranks as screening only.
- Why: Spearman +0.89 between offline and twin online ranks; user-based and sequence-aware swap places.
- Assumption checks / evidence: Twin CTR (best-sellers 13.4%, item-to-item 25.3%) is assumed.
- Impact if wrong / mitigation: Run a live A/B with ≈ 1,500 customers per arm for a 10% relative lift.

## D-15-08: Business case and scaling claim

- Date: 2026-10-17
- Case: 15
- Context / question: What is it worth, and does it scale as documented?
- Options considered: point estimate with bootstrap CI; log-log timing fit.
- Decision: ≈ ₹73 crore a year over best-sellers (CI 72 to 75) under assumed click rates; scaling reported as measured.
- Why: Similarity step grows ~N^1.5 in items and ≤ linear in customers, so Amazon's O(NM) claim is not confirmed at this size.
- Assumption checks / evidence: 1 crore impressions a day, 2% conversion, ₹700 order, 12% margin.
- Impact if wrong / mitigation: Treat the rupee figure as an order of magnitude; rely on the method ranking.

---

# Summary table

| ID | Case | Decision | Why |
|---|---|---|---|
| D-0-01 | 0 | All outcome data synthetic, hidden truth columns | Logs confidential; known truth for validation |
| D-0-02 | 0 | Evidence levels; substitutions; Weak cases flagged | No invented "documented" facts |
| D-0-03 | 0 | Same method standards as fintech series | Comparability and honesty |
| D-1-01 | 1 | Synthetic sessions with legs and a randomised promise offset | Observational logs cannot give the cost of a promised minute |
| D-1-02 | 1 | Last mile dominates; legs negatively correlated | Wait vs first mile −0.47; last mile 54% of variance |
| D-1-03 | 1 | Direct boosting for the total; joint network for stages | MAE 4.63 vs legacy 9.52; independent legs 4.99 and biased |
| D-1-04 | 1 | Promise as a calibrated quantile | Coverage matches τ (all p > 0.14); rain untested |
| D-1-05 | 1 | Cost of a promised minute from the randomised arm | OR 0.960 per minute; placement 69.3 → 63.9% |
| D-1-06 | 1 | Ship τ = 0.7 with a service guardrail | +₹1.81 per session, 10.6% late vs 20.0% at τ = 0.5 |
| D-1-07 | 1 | Chain the stage ETA models | Early jumps −10%; pickup jump is real information |
| D-1-08 | 1 | Switchback validation | ~463 city-hour blocks per arm (≈ 9 days) for +1 pp |
| D-7-01 | 7 | Synthetic dark-store sales with hidden true demand | Only a simulation can score against true demand |
| D-7-02 | 7 | Legacy rule ratchets stock down | −0.8 pp of demand a week (p = 0.04), settles near 93% |
| D-7-03 | 7 | Availability scaling by default, profile scaling if estimable | Error 40.5% → 16.6% → 1.5% (upper bound) |
| D-7-04 | 7 | Evaluate against true demand, not sales | Rank correlation −0.50; raw-sales models under-forecast ~28% |
| D-7-05 | 7 | Group SKUs for substitution, not accuracy | wMAPE 0.448 SKU-level vs 0.454 group-level |
| D-7-06 | 7 | Class-specific newsvendor ratios | +₹28.2 per store-SKU-day; expiry 4.07% → 1.87% |
| D-7-07 | 7 | Scale to 1,000 stores × 200 SKUs with a haircut | ≈ ₹206 crore base, ₹97 crore pessimistic |
| D-15-01 | 15 | Synthetic purchases with hidden taste and popularity | Needed for a digital-twin online test |
| D-15-02 | 15 | Leave-last-out evaluation in time order | Avoids leaking the future |
| D-15-03 | 15 | Item-to-item filtering as the default | HR@10 19.7% vs 11.2% best-sellers |
| D-15-04 | 15 | Best-sellers fallback for first purchases | Lift 1.27× at 1 to 3 items vs 2.03× at 10+ |
| D-15-05 | 15 | Popularity damping on discovery surfaces only | HR 14.3%, tail hits 5.9%, coverage 90% |
| D-15-06 | 15 | Sequence-aware list for accessories | 70% vs 27% hit rate on accessory pairs (n = 112) |
| D-15-07 | 15 | Offline screens, A/B confirms | Spearman +0.89; middle ranks swap |
| D-15-08 | 15 | ≈ ₹73 crore a year; scaling ~N^1.5 in items | O(NM) not confirmed at this size |
