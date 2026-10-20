# Problem statement - Case study 06

## Objective
The CRM team of an online gift wholesaler needs, from customer-identified transactions
(UCI Online Retail II, 2009-12-01 to 2011-12-09):
1. actionable customer **segments** (rule-based RFM segments and behavioural clusters),
2. a 12-month **customer lifetime value** (CLV) for every customer,
3. cross-sell **bundles** from market-basket rules,
4. personalised **top-10 product recommendations** for e-mail campaigns,
5. a **campaign plan** per segment with budget and expected ROI.

## KPIs and success criteria (from the spec)
| KPI | Target |
|---|---|
| Segment quality | silhouette >= 0.35 |
| CLV | MAE vs holdout spend and Spearman reported against a historical-average baseline; top-decile CLV share reported |
| Recommender | HitRate@10 and NDCG@10 beat the popularity baseline by >= 30% |
| Leakage | time-based splits; no holdout information in CLV or recommender training |
| Memo | segment sizes, revenue share, CLV top-decile share, campaign ROI table |

## Constraints
- Customer-identified rows only (~5.9k customers); heavy-tailed spend; left-censored first purchase.
- Calibration to 2011-06-30, holdout 2011-07-01 to 2011-12-09; recommender train to 2011-11-09, test last 30 days.
- Everything reproducible with seed 42; `python tasks.py all` under 15 minutes on a laptop; offline tests.
- Campaign uplift/cost/margin figures are **assumptions** in `config/config.yaml` and are swept in a sensitivity table.
- Currency: the data is in GBP; amounts are reported in GBP, with an INR display factor in config.

## Stakeholders
CRM / e-mail marketing (consumer of segments, bundles, recommendations), finance (campaign ROI), analytics lead (model governance).
