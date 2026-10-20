# Model card - Promotion Cannibalisation Engine

*Numbers from `outputs/summary.json`; seed 42.*

## Intended use
Ex-ante scoring of a proposed discount on one SKU of a product family: direct uplift, subsidy on baseline units, cannibalised sibling margin and basket halo, summarised as **family net contribution**; plus a discount-level optimiser and an assumption sweep. Decision support for category managers, not an automatic pricing system.

## Out-of-scope use
Causal claims about price elasticity; margin forecasts without finance cost data; promotions longer than a few weeks (no pull-forward / post-promo dip); competitor-driven pricing; markets other than a UK gift-ware wholesale/retail mix.

## Training / calibration data
UCI Online Retail II (id 502), 2009-12-01 to 2011-12-09: 1,036,875 clean sales lines, 39,514 invoices, 4,706 SKUs, £19,863,342 revenue. No costs and no promotion flags exist in the data. Fully cancelled bulk orders (qty >= 10,000) are removed.

## Components and diagnostics
| Component | Result |
|---|---|
| Families (TF-IDF + agglomerative) | 3,827 families, 331 multi-SKU (max size 27); co-purchase median 21.4%, 107 weak-substitute families (cannibalisation capped) |
| Basket halo (FP-Growth) | 640 cross-family rules, 162 SKUs with halo |
| Price response (log-log, month effects, HC1) | 1593 eligible SKUs, 1579 negative estimates, 14 positive dropped; median -2.39; pooled SKU+week FE -2.03 (se 0.030); sources: {'prior': 2913, 'estimated_shrunk': 1579, 'family_median': 214} |
| MNL calibration | max share-sum error 2.2e-16; max relative own-elasticity error at d=0.1% 0.40% |
| Engine identity | family_net = direct - subsidy - cannibalised + halo to 1e-6 (unit test) |

## Metrics (no trained predictor; business metrics)
Reference promo (10% off top-24): family net £779, promoted-only £133. Sweep (2,000 draws): 60.5% profitable promoted-only vs 38.7% family. **Naive baseline:** the promoted-only (dashboard) view is reported next to the family view everywhere.

## Segment / robustness checks
- By elasticity source: of the 24 reference SKUs, 23 use an estimated (shrunk) elasticity and 1 a family median or prior; across all 4,706 SKUs, 2913 rely on the prior.
- By substitute strength: weak-substitute families have cannibalisation scaled by the configured cap.
- No individual-level or protected attributes are used (invoice-level data), so no person-level fairness check applies; customer mix (wholesale vs retail) is not modelled.
- Sensitivity: margin and outside share grid in `outputs/reference_sensitivity.csv`; four-parameter sweep in `outputs/sweep_draws.csv`.

## Known failure modes
Confounded price changes (clearance, mix) bias elasticities; text-based families can mix product types (fix with `config/family_overrides.csv`); basket confidence is not causal pull; MNL/IIA spreads sibling losses by share; baseline units are means over active weeks and overstate sporadic SKUs.

## Monitoring plan
Compare predicted vs realised family net on each controlled promotion; track elasticity drift and share of SKUs on the prior; re-fit monthly.

## Version
promo 0.1.0, seed 42, config in `config/config.yaml`.
