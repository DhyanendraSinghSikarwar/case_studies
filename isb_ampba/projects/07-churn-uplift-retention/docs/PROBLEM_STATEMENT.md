# Problem statement - Churn prediction + uplift-based retention

## Objective
Retention budget is wasted on customers who would stay anyway or who cannot be saved. Predict who will churn in the
next 90 days **and** who actually responds to an offer, then target by expected incremental profit
(`tau x value - cost`) rather than by churn risk.

## KPIs (from the case-study spec)
| KPI | Target |
|---|---|
| Churn ROC-AUC on the later (2011-08-01) snapshot | >= 0.75 |
| Qini coefficient of the uplift model on the pilot | > 0 |
| Incremental profit ordering | uplift policy > risk-only policy > random |
| Uplift policy as share of the perfect-hindsight oracle | >= 70% |
| `test_features_before_asof` | passes |

## Definitions
- **Eligible customer at snapshot `asof`:** >= 2 distinct invoices in the 180 days before `asof`.
- **Churn label:** no sales invoice in `[asof, asof + 90 days)`.
- **Snapshots:** train 2011-03-01 / 04-01 / 05-01, test 2011-08-01 (last train label window ends 2011-07-30 < test asof).
- **Value of saving a customer (INR):** `monetary_6m / 6 x clv_months x gross_margin x gbp_to_inr` (pre-snapshot spend only).

## Constraints
Features strictly before `asof`; temporal validation; group-aware folds on `customer_id`; seed 42; all business assumptions
in `config/config.yaml` and swept; every reported number written by code to `outputs/*.json`; runs offline from fixtures;
`python tasks.py all` < 15 minutes.

## Success criteria
All KPIs above reported honestly (pass or fail), a policy table with the oracle ceiling, a memo explaining why
"target the highest-risk" can lose money, and a clear split between simulated (Track A) and real (Track B) treatment evidence.

## Stakeholders
CRM / retention marketing (who to contact), Finance (offer budget, margin assumptions), Data science (model monitoring).
