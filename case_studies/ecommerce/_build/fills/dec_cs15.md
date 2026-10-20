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
