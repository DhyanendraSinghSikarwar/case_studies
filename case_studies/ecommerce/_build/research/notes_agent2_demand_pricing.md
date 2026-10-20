

### R1 Instamart grocery forecasting
(a) Calibrate to: delivery in about 10-15 minutes; SKUs on the order of 10^4 (talk); availability = share of day SKU orderable; warehouse accuracy improvements "21-38%" relative and OPD "7.5% WMAPE improvement" and "50% reduction in runtime" (summary). Simulate censored sales (sales = min(demand, stock)).
(b) Expected techniques: censored-demand / de-biasing, hierarchical reconciliation, quantile forecasts and newsvendor stocking, wMAPE and bias, perishables wastage vs availability trade-off, rolling-origin backtesting.
(c) Very common (every grocery/q-commerce player).

### R2 Marketplace pricing
(a) Only one figure: SVM accuracy "91.11%" on Flipkart Summer Sale phones (arXiv 2005.04612); all else must be assumed and labelled synthetic.
(b) Log-log elasticity regression, causal inference for price effects (A/B or diff-in-diff), gradient boosting for demand, bandits / Thompson sampling, constrained optimisation, competitor price scraping with product matching.
(c) Very common.

### R3 Surge / delivery fee / incentives
(a) Fee formula components from arXiv 2503.22753: base price x GST + platform fee + base delivery fee + per-km rate x distance + small-order fee (simulated study, not real outcomes). Everything else synthetic.
(b) Supply-demand ratio models, price elasticity of conversion, causal uplift for incentives, bandits, queueing / marketplace balancing, guardrail metrics.
(c) Common.

### R4 Sale-event capacity planning
(a) BBD 2025 (Flipkart claims): 7.3 million+ shipments in a day, 5,000+ shipments per minute at peak, 24% unit growth, 21,000+ pincodes, over 60% of orders from Tier 2/3.
(b) Time series with event regressors (Prophet / GBM), quantile or scenario forecasts, queueing and capacity buffers, load-test calibration, backtests on previous events.
(c) Common (every large marketplace; method detail rarely public).

### R5 Fashion assortment / new-item demand
(a) Test wMAPE naive about 1.0 vs XGBoost 0.51-0.60; training series 12,541-42,206 per article type; about 1 million styles listed; sell-through gains 10% and 7% (authors' claim); features as in section 3.
(b) Gradient boosting with Poisson/Huber/MSE, attribute embeddings, cold-start validation by launch cohort, wMAPE, Kendall Tau, sell-through curves for markdown.
(c) Very common in fashion/beauty commerce.

### R6 Hierarchical probabilistic forecasting
(a) CLOVER 15% average sCRPS gain (authors' claim); Favorita 93 series per item, 34-step horizon; Flipkart CPP: 10 days to 1 day planning, 4 million daily shipments (company claim via summary).
(b) Quantile regression / pinball loss, DeepAR-type models, CRPS, MinT / bottom-up / top-down reconciliation, conformal intervals, service-level quantile ordering.
(c) Common in large supply-chain teams; niche as an interview topic outside them.
