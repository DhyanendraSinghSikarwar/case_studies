# Model card - CRM models (RFM / KMeans / BG-NBD+GG / FP-Growth / ALS)

## Intended use
Prioritising CRM actions (e-mail campaigns, win-back, loyalty) for customer-identified accounts of an online wholesaler: segment
assignment, 12-month CLV ranking, cross-sell bundles and top-10 product suggestions.

## Out-of-scope use
Individual credit/pricing decisions, causal uplift claims, other retailers or markets without re-fitting, any use of CLV as an exact
revenue forecast (especially around seasonal peaks).

## Training data
UCI Online Retail II (id 502): 802,634 clean sales lines with a Customer ID, 5,852 customers,
2009-12-01 to 2011-12-09. Calibration (segments, clustering, CLV): <= 2011-06-30
(5,016 customers). CLV holdout: 2011-07-01 onwards (3,360 customers).
Recommender: train <= 2011-11-09 (5,700 users, 4,599 items), test from 2011-11-10.

## Metrics (all from outputs/metrics.json)
| Metric | Target | Achieved | Met? |
|---|---|---|---|
| Segment silhouette (KMeans, k=4) | >= 0.35 | 0.377 | yes |
| ALS NDCG@10 / popularity (repeat_allowed) | >= 1.30x | 2.73x | yes |
| ALS NDCG@10 / popularity (discovery) | >= 1.30x | 2.20x | yes |
| CLV MAE (spend) beats historical baseline | lower | 549 vs 570 | yes |
| CLV Spearman (spend) beats baseline | higher | 0.608 vs 0.567 | yes |
| Bundles (lift>3, conf>0.3) | top 20 | 20 | yes |

CLV vs baselines:
| Model | MAE spend (GBP) | MAE purchases | Spearman spend | Spearman purchases |
|---|---|---|---|---|
| BG/NBD + Gamma-Gamma | 549.000 | 0.959 | 0.608 | 0.619 |
| Historical average (baseline) | 570.500 | 1.029 | 0.567 | 0.543 |
| Population mean (naive) | 1106.900 | - | - | - |

Recommender, `repeat_allowed`:
| Model | HitRate@10 | NDCG@10 | Coverage | NDCG vs popularity | 95% CI |
|---|---|---|---|---|---|
| random | 0.0706 | 0.0081 | 0.9569 | - | - |
| popularity | 0.4878 | 0.0888 | 0.0022 | - | - |
| itemknn_cosine | 0.6839 | 0.2087 | 0.2344 | 2.35x | [2.20, 2.52] |
| als | 0.7273 | 0.2421 | 0.1333 | 2.73x | [2.54, 2.99] |
| hybrid_als_pop | 0.7273 | 0.2421 | 0.1333 | 2.73x | [2.54, 2.95] |

Recommender, `discovery`:
| Model | HitRate@10 | NDCG@10 | Coverage | NDCG vs popularity | 95% CI |
|---|---|---|---|---|---|
| random | 0.0449 | 0.0049 | 0.9428 | - | - |
| popularity | 0.2292 | 0.0342 | 0.0174 | - | - |
| itemknn_cosine | 0.2899 | 0.0570 | 0.1289 | 1.67x | [1.49, 1.89] |
| als | 0.3753 | 0.0753 | 0.1761 | 2.20x | [1.92, 2.58] |
| hybrid_als_pop | 0.3753 | 0.0753 | 0.1761 | 2.20x | [1.94, 2.57] |

## Fairness / segment checks
No personal attributes (age, gender, ethnicity) exist in the data; the only demographic-like field is Country (about 92% UK).
Model quality is therefore checked across commercial segments instead: CLV and recommender errors differ strongly by customer size.
Per-segment holdout purchase rates are in `outputs/campaign_economics.csv` (`holdout_purchase_rate`). Small and one-off buyers are served
mostly by popularity-like items; large wholesalers dominate revenue and the recommender training signal.

## Known failure modes
- One-time buyers get population-average order value; BG/NBD cannot separate them from churners.
- Seasonal peaks (Q4) and promotions are not modelled; holdout spend is under-predicted in aggregate.
- Colour/size variants produce near-duplicate bundles; ALS is trained on purchases only (no item content, no returns).
- Customers first seen after 2011-06-30 have no segment/CLV in the calibration snapshot.
- GMM and HDBSCAN are weaker than KMeans on log-RFM here (see README).

## Monitoring plan
Monthly refit; track BG/NBD calibration plot by frequency bucket, top-decile share, recommender HitRate@10/NDCG@10 against popularity
on a rolling last-30-days test, segment migration matrix and campaign response vs the control group.

## Version / seed
crm 0.1.0, seed 42, pinned in requirements.txt; pipeline runtime 1233.2 s.
