# Decision memo - customer segmentation, CLV, bundles and recommendations

**Decision requested:** approve a segment-based CRM programme (six RFM segments, a 12-month CLV score, bundle cross-sell and ALS-based
top-10 recommendations in e-mail) with a first-wave budget of GBP 5,000.

**Recommendation:** run the funded campaign plan below as a controlled pilot (hold-out control group per segment). Champions are
23% of customers but 69% of revenue, so protect them first; use the ALS recommender
(2.73x popularity NDCG@10 under `repeat_allowed`) for e-mail content.

**Impact:** under the assumed response rates, margin (30% gross) and costs in `config/config.yaml`, the funded plan
costs GBP 5,000 for an expected net profit of GBP 7,623 (ROI 1.52; about
INR 800,435 at the configured display rate). These uplifts are **assumptions, not measured results**;
portfolio ROI stays between -0.27 and 2.97 across the sensitivity grid.

## Segment sizes and revenue share (rule-based RFM, as of 2011-06-30)
| Segment | Customers | % customers | % revenue (to 2011-06-30) | Mean recency (d) | Mean orders | Mean spend | Action |
|---|---|---|---|---|---|---|---|
| Champions | 1,166 | 23.2% | 68.7% | 32 | 14.00 | 7,426 | VIP loyalty perks + early access |
| Loyal | 1,471 | 29.3% | 9.2% | 107 | 3.00 | 784 | Loyalty points + cross-sell bundle |
| At-Risk | 642 | 12.8% | 5.3% | 294 | 3.50 | 1,050 | Win-back offer (10% off) |
| Hibernating | 1,278 | 25.5% | 3.1% | 357 | 1.20 | 308 | Low-cost reactivation e-mail |
| New | 208 | 4.1% | 0.7% | 28 | 1.20 | 432 | Welcome series + second-order incentive |
| Big-spenders | 251 | 5.0% | 13.0% | 193 | 8.70 | 6,505 | Upsell: personalised bundle + account manager call |

## Campaign ROI table
| Segment | Action | Contacts | Cost (GBP) | Incr. revenue (GBP) | Net profit (GBP) | ROI | Funded |
|---|---|---|---|---|---|---|---|
| Champions | VIP loyalty perks + early access | 1166 | 2,332 | 21,379 | 4,082 | 1.75 | 100.0% |
| New | Welcome series + second-order incentive | 208 | 366 | 3,158 | 581 | 1.59 | 100.0% |
| Loyal | Loyalty points + cross-sell bundle | 1471 | 1,471 | 11,487 | 1,975 | 1.34 | 100.0% |
| Big-spenders | Upsell: personalised bundle + account manager call | 251 | 1,506 | 10,970 | 1,785 | 1.19 | 55.2% |
| At-Risk | Win-back offer (10% off) | 642 | 1,419 | 4,558 | -51 | -0.04 | 0.0% |
| Hibernating | Low-cost reactivation e-mail | 1278 | 554 | 1,702 | -43 | -0.08 | 0.0% |

## Evidence
- **Segments:** KMeans on log-scaled RFM gives silhouette 0.377 at k=4
  (target 0.35: met); the 6-feature variant scores lower (see README).
- **CLV:** BG/NBD + Gamma-Gamma fitted to 2011-06-30 gives holdout spend MAE 549 vs 570 for the
  historical-average baseline, Spearman 0.608 vs 0.567. The **top CLV decile
  holds 58.9% of predicted 12-month CLV** and the same customers account for
  60.7% of actual holdout spend.
- **Recommender:** under `repeat_allowed` the best of ALS/hybrid ('als') reaches NDCG@10 0.242 vs popularity 0.089;
  plain ALS is 2.73x popularity (95% CI 2.54-2.99; target 1.30x:
  met) and 2.20x under `discovery`.
- **Bundles:** 20 bundles with lift > 3 and confidence > 0.3 (top lift 50.0), mostly colour/size variants of the same product family,
  suited to "complete the set" prompts.

## Risks and limitations
- Campaign response rates, costs and margin are planning assumptions; only a controlled pilot can validate them.
- About 5k customers and heavy-tailed spend: segment and decile boundaries are noisy; small segments should not be over-read.
- BG/NBD ignores seasonality (holdout contains the Q4 peak) and first-purchase dates are left-censored at 2009-12-01.
- Wholesale B2B behaviour (bulk re-orders) dominates; recommendations that include re-orders mostly resurface past purchases, discovery lift is lower.

## Next steps
1. Pilot with randomised control per segment for 4-8 weeks; replace config uplifts with measured ones.
2. Refit BG/NBD/GG and ALS monthly; monitor calibration drift and recommender HitRate@10 on a rolling 30-day test.
3. Owner: CRM analytics lead; review after the pilot readout.
