# Review deck outline - case study 06

## Mid-review (after M3), ~10 slides
1. Problem and KPIs (CRM: segments, CLV, bundles, recommendations)
2. Data: Online Retail II, cleaning funnel, time splits (calibration / holdout)
3. RFM construction and rule segments (sizes, revenue share; Champions 69% of revenue)
4. Clustering: elbow / silhouette (final 0.377 vs target 0.35), GMM and HDBSCAN comparison, feature-set ablation
5. CLV: BG/NBD + GG, calibration plot, MAE / Spearman vs baseline
6. Top-decile CLV share (58.9%) and what it means
7. Risks found so far (seasonality, left-censoring, small samples)
8. Plan for M4/M5

## Final review (after M5), ~10 slides
1. Recap and results vs targets table
2. Bundles: top 20 by lift
3. Recommender: popularity vs item-KNN vs ALS vs hybrid (both protocols; ALS 2.73x popularity under repeat_allowed)
4. Campaign matrix and ROI table (funded ROI 1.52), sensitivity
5. App demo: segment explorer, Customer 360, bundle finder, campaign planner
6. Leakage controls and tests
7. Limitations, deviations, next steps (pilot with control group)
