# Agent 2 research: demand forecasting and pricing cases (R1-R6)

Compiled 2026-10-17. Method note: the primary pages for two key sources (Swiggy Bytes Instamart post, Flipkart Tech blog CPP post) returned HTTP 403 or failed to fetch from this environment. For those two, only third-party summaries (daily.dev) that I did fetch are used and are labelled as such. Anything not seen on a fetched page is "ND". Search-result snippets that I did not open are NOT treated as documented fact.

## Case R1 — Instamart quick-commerce demand forecasting: availability de-biasing, SKU grouping and TimesFM
**Company:** Swiggy Instamart (India)
**Industry:** Quick commerce / grocery
**Business Area:** Supply chain, dark-store replenishment, rider fleet planning
**Problem Type:** Demand forecasting under censored (stock-out) data; hierarchical forecasting
**Evidence Level:** Medium (A/C: company blog post and a company-employee conference talk exist, but I could read only a third-party summary of the blog and the abstract of the talk, not the full texts)
**Primary Sources:** Swiggy Bytes post "Instamart's Generative AI Forecasting: Scaling from Flat Forecasts to Deep Hierarchies" (URL known from daily.dev; direct fetch failed); Fifth Elephant 2023 Monsoon talk "Adaptive Metric Alignment for Demand Forecasting in Swiggy Instamart" (Priyanka Banik)

### 1. Business Problem
Instamart delivers groceries in about 10-15 minutes from dark stores (talk abstract). Demand forecasting is hard because of high variation across locations, items and days, and SKU counts "on the order of 10^4" (talk abstract). Recorded sales are censored: when an item is out of stock, sales understate true demand. Wrong forecasts cause either lost availability (under-prediction) or wastage (over-prediction). Two forecasting tasks are named in the blog summary: warehouse-level SKU demand, and Orders per Day (OPD) used for rider fleet planning.

### 2. Business Question
How can the team forecast true (uncensored) demand per SKU and per day accurately enough to keep availability high and wastage low, and how should forecast models be judged so that offline accuracy reflects those two business outcomes?

### 3. Data Available
| Data | Description |
|---|---|
| Historical SKU sales per dark store / warehouse | Censored by stock-outs (talk abstract; blog summary) |
| Availability signal | Share of the day a SKU was orderable; used for de-biasing and as a business metric |
| Product substitution patterns | Cause variance; handled via Group SKUs (GSKU) (blog summary) |
| Orders per day | Target of the OPD model for rider planning (blog summary) |
| Covariates | Blog summary says covariate support was added via ridge regression; which covariates: ND |

### 4. Data Science Approach
Documented (blog summary, not the original): (a) availability de-biasing to correct censored sales; (b) GSKU aggregation to reduce variance from substitution; (c) a "dual-hierarchy framework" separating the business-objective level from the level where modelling works best; (d) Google's TimesFM foundation model used zero-shot, with covariates added via ridge regression. Talk abstract: critiques wMAPE-on-backtest evaluation and proposes "Adaptive Metric Alignment" using estimated availability and estimated wastage as evaluation targets. Perishables-specific modelling (shelf life): ND; the talk only mentions wastage from overstock.

### 5. Statistical Analysis
Censored-demand correction (availability de-biasing) is documented by name only; the statistical form (e.g. likelihood or imputation) is ND. Ridge regression for covariates. wMAPE as an accuracy metric.

### 6. Machine Learning
- Model(s): TimesFM (zero-shot foundation model) plus ridge regression for covariates; prior OPD system was TFT (Temporal Fusion Transformer) per the summary.
- Target variable: de-biased SKU demand (warehouse model); orders per day (OPD model).
- Features: ND beyond "covariates".
- Validation approach: ND (talk argues for evaluating against estimated availability and wastage rather than only backtest wMAPE).
- Metrics: WMAPE (OPD); "relative accuracy" for warehouse (exact definition ND); estimated availability and estimated wastage (talk).

### 7. Tools & Technology
| Tool | Use |
|---|---|
| TimesFM (Google) | Zero-shot time-series foundation model |
| Ridge regression | Covariate adjustment |
| TFT | Previous OPD baseline |

### 8. Business Decision
Forecasts drive dark-store SKU replenishment (availability vs wastage) and rider fleet sizing (OPD). Specific operating rules (safety stock, order cadence): ND.

### 9. Business Impact
From the daily.dev summary of the blog (company's own claim, second-hand): "21-38% relative accuracy improvements across product categories" for warehouse forecasting; "7.5% WMAPE improvement and a 50% reduction in runtime" for OPD versus the TFT-based system. Revenue or wastage impact: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
Observed sales are not demand; fix censoring before choosing a model. Aggregate to a level where signal is stable (substitutes grouped), then reconcile to the decision level. Evaluate models on business metrics (availability, wastage), not only wMAPE. Zero-shot foundation models can beat a tuned deep model on runtime and accuracy when the data is noisy and hierarchical.

### 11. Source Links
- https://daily.dev/posts/instamart-s-generative-ai-forecasting-scaling-from-flat-forecasts-to-deep-hierarchies-sm44pwri5 (summary, dated 2026-05-15 on daily.dev; original Swiggy Bytes URL given there: https://bytes.swiggy.com/instamarts-generative-ai-forecasting-scaling-from-flat-forecasts-to-deep-hierarchies-89357682fbb5, could not be fetched)
- https://hasgeek.com/fifthelephant/2023-08/sub/adaptive-metric-alignment-for-demand-forecasting-i-XqLQxwWhh5j2KoqqefSeqs (Fifth Elephant 2023 Monsoon, Aug 2023)

## Case R2 — Marketplace price monitoring / discount efficacy on Flipkart (substitution: only an external analysis is public)
**Company:** Flipkart (external analysis by academic authors)
**Industry:** E-commerce marketplace
**Business Area:** Pricing and promotions
**Problem Type:** Price / discount assessment (classification), proxy for competitive price monitoring
**Evidence Level:** Weak (D/B: no Flipkart or Amazon India engineering source on pricing models was found; the one fetched paper is an outside academic study of public Flipkart data, not the company's own system)
**Primary Sources:** arXiv 2005.04612 (Singhania et al., 2020)

### 1. Business Problem
Only the problem framing is public. The paper asks whether a "sale" discount is genuinely significant, using Flipkart Summer Sale data. It is a buyer-side view, not Flipkart's pricing engine. Flipkart's own price-optimisation methods: ND (not found in any fetched source).

### 2. Business Question
Can product features and original price be used to predict whether a sale discount is significant?

### 3. Data Available
| Data | Description |
|---|---|
| Flipkart Summer Sale dataset | Mobile phones; size and fields ND on the page I read |

### 4. Data Science Approach
Only that a machine learning heuristic quantifies discount significance from product features and original price. Details ND.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- Model(s): Support Vector Machine.
- Target variable: efficacy / significance of the sale discount (definition ND).
- Features: product features and original price (list ND).
- Validation approach: ND.
- Metrics: accuracy.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| SVM | Classifier (library ND) |

### 8. Business Decision
Buyer decision aid; no Flipkart business decision documented.

### 9. Business Impact
Paper reports "accuracy of 91.11%" and that very few mobile phones have a significant discount during the sale. This is the authors' own claim; no business impact.

### 10. What a Data Scientist Can Learn *(interpretation)*
Public India-specific evidence on marketplace pricing models is thin; interviews will test general knowledge (price elasticity, log-log regression, competitive price scraping, constrained optimisation, bandits). Define "discount significance" relative to a reference price (MRP inflation is a known concern) before modelling.

### 11. Source Links
- https://arxiv.org/abs/2005.04612 (A machine learning based heuristic to predict the efficacy of online sale, submitted 10 May 2020)

## Case R3 — Delivery-fee / surge design in food delivery (Weak; only problem framing and a simulated academic study)
**Company:** Swiggy / Zomato (no company technical source found)
**Industry:** Food delivery marketplace
**Business Area:** Pricing, delivery supply management
**Problem Type:** Dynamic fee / surge and demand-supply balancing
**Evidence Level:** Weak (D: no Swiggy Bytes or Zomato engineering post on fee or incentive design was found; the only fetched paper uses simulated data)
**Primary Sources:** arXiv 2503.22753 (Ghosh, 2025), simulated data

### 1. Business Problem
Problem framing only. Not publicly disclosed (ND) by the companies in sources I read. (Search snippets, not opened by me: Swiggy tested surge fees in 2016; Zomato Care said surge fees apply when few riders are available. Treat as unverified.)

### 2. Business Question
The paper asks how demand forecasting can reduce the bullwhip effect (order-variability amplification) in the Swiggy/Zomato rivalry, using the platforms' pricing formula as an input.

### 3. Data Available
| Data | Description |
|---|---|
| Simulated demand | Paper says it "relies on simulated data rather than real-world transactional data"; SimPy simulation based on two Kaggle datasets; five daily time slots; 3,675 observations, 19 variables; Jan 2023-Jan 2025; baselines 12,000 (Swiggy) and 10,000 (Zomato); demand correlation 0.93 |

### 4. Data Science Approach
Two-phase LSTM (intraday to next-day; six-day window to seventh day) plus newsvendor-based inventory (z = 1.96). Platform-derived pricing formula given: P = (Pb x G) + F + B + (R x D) + S (base price x GST, platform fee, base delivery fee, per-km rate x distance, small-order fee). It is a static formula; the dynamic surge logic is ND.

### 5. Statistical Analysis
Bullwhip ratio (variance amplification): Phase 1 2.61 (train), 2.01 (test), 0.96 (predicted); Phase 2 2.19, 1.86, 0.80. Computed on simulated data.

### 6. Machine Learning
- Model(s): multilayer LSTM, Adam, MSE loss.
- Target variable: demand per time slot / day.
- Features: ND beyond time-slot and lagged demand.
- Validation approach: chronological 70/15/15 split (train Jan 2023-Apr 2024; validate May-Sep 2024; test Oct 2024-Jan 2025); grid search on validation.
- Metrics: RMSE, MAE, R2. Phase 2 test: Zomato RMSE 536.25, R2 0.88; Swiggy RMSE 579.40, R2 0.90.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Python, SimPy | Simulation |
| scikit-learn StandardScaler | Scaling |
| LSTM (framework ND) | Forecasting |

### 8. Business Decision
Not a company decision; academic inventory-planning illustration.

### 9. Business Impact
ND for the companies. Simulated bullwhip reductions only; not real-world impact.

### 10. What a Data Scientist Can Learn *(interpretation)*
Real surge/incentive design is not publicly documented for Indian platforms, so the notebook should be framed as a generic marketplace problem (supply-demand ratio, elasticity of order conversion to fee, rider-supply response to incentives, guardrails like cancellation and customer-fairness). Do not present the simulated paper as evidence of real Swiggy/Zomato outcomes.

### 11. Source Links
- https://arxiv.org/html/2503.22753v1 (Combating the Bullwhip Effect in Rival Online Food Delivery Platforms Using Deep Learning, 27 Mar 2025)

## Case R4 — Sale-event (Big Billion Days) planning at Flipkart (Weak: outcomes published, methods not)
**Company:** Flipkart
**Industry:** E-commerce marketplace
**Business Area:** Supply chain / capacity planning for festive sale
**Problem Type:** Peak-event demand and capacity forecasting
**Evidence Level:** Weak (D/A: company press story with outcomes but no method detail; traffic-forecasting engineering posts were not found)
**Primary Sources:** Flipkart Stories, BBD 2025 supply-chain announcement

### 1. Business Problem
Handling surge volumes during the Big Billion Days festive sale across a national network. Traffic/infrastructure forecasting method: ND.

### 2. Business Question
How to keep inventory in stock, capacity adequate and deliveries fast during a demand surge? (framing derived from the press story)

### 3. Data Available
| Data | Description |
|---|---|
| ND | Not disclosed |

### 4. Data Science Approach
Page states the supply chain used "AI-powered forecasting, ML-driven planning and real-time capacity orchestration"; automated inventory placement and AI-led Inter-Warehouse Inventory Transfer (IWIT) improved in-stock availability. No model detail.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- Model(s): ND
- Target variable: ND
- Features: ND
- Validation approach: ND
- Metrics: ND

### 7. Tools & Technology
| Tool | Use |
|---|---|
| AGVs, robotic arms, cross-belt sorters, sensor-led tracking | Fulfilment centres (page) |
| Forecasting stack | ND |

### 8. Business Decision
Inventory placement, inter-warehouse transfers, regional infrastructure in Tier 2/3 cities, seasonal hiring.

### 9. Business Impact
Company's own claims for BBD 2025: "24% year-over-year growth in units" (as summarised by the fetch tool); over 60% of orders from Tier 2 and 3; 5,000+ shipments per minute on peak days; 7.3 million+ shipments in a single day, over 3 lakh per hour; 44% increase in same-day and next-day deliveries; network 21,000+ pincodes; 4 lakh+ seasonal jobs. Attribution of any figure to forecasting: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
Only scale parameters are public; the notebook can simulate a multiplicative event spike with trend, weekly seasonality, event flags and quantile (not point) capacity targets. Search results also mentioned third-party claims of 6-10x volume surges; I did not verify them from a primary page and do not rely on them.

### 11. Source Links
- https://stories.flipkart.com/announcement/millions-served-lakhs-empowered-flipkart-s-festive-supply-chain-at-the-heart-of-bharat (dateline 18 Dec 2025, published 25 Dec 2025)

## Case R5 — Myntra: forecasting demand for new fashion items to guide assortment and buying
**Company:** Myntra (India, fashion e-commerce)
**Industry:** Fashion e-commerce
**Business Area:** Merchandising, assortment planning, buying budgets
**Problem Type:** New-item (cold-start) demand forecasting for assortment planning
**Evidence Level:** Strong (C: paper by Myntra Designs authors with data, models, metrics and deployment note)
**Primary Sources:** arXiv 1907.01960, "Fashion Retail: Forecasting Demand for New Items" (Singh, Gupta, Jha, Rajan; Myntra Designs, submitted 27 Jun 2019)

### 1. Business Problem
Fashion trends change fast, bulk production is needed for economies of scale and retailers lose money on unsold stock and liquidation. Item-level history models rarely generalise to new styles. About 1 million styles are listed at any time (paper).

### 2. Business Question
Can attributes and merchandising factors of a not-yet-sold style predict its weekly demand, so buyers can allocate budgets across attributes?

### 3. Data Available
| Data | Description |
|---|---|
| Weekly style sales | Five article types: Shirts, Casual Shoes, Kurtas, Tops, Tshirts; training series 12,541 to 42,206 per type; test series: Shirts 16,409, Casual Shoes 6,732, Kurtas 9,161, Tops 10,618, Tshirts 18,364; series length 4 to 104 weeks |
| Fashion attributes | Colour, material etc., embedded or one-hot |
| Merchandising | Discount deviation from brand/platform averages; list-page visibility ratios; days to/from promotions |
| Time | Style age, trend, three Fourier seasonality terms, lags up to 4 weeks |
| Cannibalisation | Styles listed per week, per brand, by other brands in similar price ranges |

### 4. Data Science Approach
Generalised models forecasting weekly sales from attributes rather than own history. Split by launch date: train = first-year launches, validation = next 6 months, test = following 6 months. 13 models compared against a naive average style-week baseline. Forecasts aggregated by attribute combinations to guide buying.

### 5. Statistical Analysis
Large-scale analysis of which attributes and merchandising factors drive demand (feature design above); Fourier seasonality; Pearson correlation and Kendall Tau for ranking quality. Formal hypothesis tests: ND.

### 6. Machine Learning
- Model(s): Random Forest (MSE); GBRT (MSE, Huber); LightGBM, CatBoost, XGBoost (MSE, Poisson); attribute-embedding + MLP and + LSTM (seq2seq, MSE, Poisson).
- Target variable: weekly sales per style (the best XGBoost used MSE in log scale).
- Features: as in section 3.
- Validation approach: out-of-time split by launch cohort; Bayesian optimisation for trees; validation set for tuning.
- Metrics: weighted MAPE (wMAPE), Pearson correlation, Kendall Tau. Test wMAPE, naive vs XGBoost-MSE: Shirts 0.97 vs 0.52; Casual Shoes 1.00 vs 0.51; Kurtas 1.08 vs 0.60; Tops 1.00 vs 0.51; Tshirts 1.01 vs 0.55. LSTM was best deep model; MLP not in top five.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| PyTorch | Deep models, Azure instance with 6 CPUs and 1 GPU |
| scikit-learn, LightGBM, CatBoost, XGBoost | Tree models |
| Bayesian optimisation | Tree tuning |

### 8. Business Decision
Seasonal assortment planning (deployed): forecasts for attribute combinations guided buying budgets for two footwear brands in Autumn Winter 2018. Roadshow product selection (in progress) and phased "drop" planning (being tested).

### 9. Business Impact
Paper reports year-on-year one-month sell-through improvements of 10% and 7% for the two footwear brands (authors' own claim). Markdown or inventory-cost impact: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
Cold-start forecasting by attributes, out-of-time validation by launch cohort, ranking metrics matter for procurement, and gradient boosting beat deep models on tabular style data. Markdown optimisation itself was not documented by Myntra in sources found (substitution note: the closest markdown paper found, ASOS arXiv 2207.01137, is UK, appeared only in search results and was not opened).

### 11. Source Links
- https://arxiv.org/abs/1907.01960 (submitted 27 Jun 2019)
- https://ar5iv.arxiv.org/html/1907.01960 (full text)

## Case R6 — Hierarchical probabilistic forecasting for supply chain: Amazon Forecasting Science (CLOVER), with Flipkart CPP context
**Company:** Amazon (Forecasting Science / Supply Chain Optimization Team); Flipkart CPP as Indian context
**Industry:** E-commerce / supply chain
**Business Area:** Supply chain planning
**Problem Type:** Coherent probabilistic hierarchical forecasting
**Evidence Level:** Medium (C: paper by Amazon team, but experiments use six public datasets, not Amazon production data; Flipkart CPP seen only through a third-party summary)
**Primary Sources:** arXiv 2307.09797 CLOVER (Olivares et al.; v4 revised 21 Dec 2024); Flipkart Tech blog CPP post (summary only)

### 1. Business Problem
Forecasts at different hierarchy levels must be coherent (add up) and probabilistic. Paper cites supply-chain planning, resource allocation and retail demand as uses. Flipkart (daily.dev summary): Central Planning Platform for 500 million users, 150 million products, 4 million daily shipments; challenges named: systemic interdependence, forecast precision vs lead times, dynamic scalability.

### 2. Business Question
How to train one model that outputs full predictive distributions across a hierarchy whose samples always respect aggregation constraints?

### 3. Data Available
| Data | Description |
|---|---|
| Public datasets (CLOVER) | Labour, Traffic, Tourism-S, Tourism-L, Wiki, Favorita; Favorita has 93 series per item over 4,036 items (over 340,000 series), horizon 34; no proprietary Amazon data described |
| Flipkart CPP | Data ND |

### 4. Data Science Approach
CLOVER: MQCNN-style encoder (dilated temporal convolutions) with MLP decoders; Gaussian multivariate factor model on bottom-level series; coherence via bottom-up aggregation; residual cross-series MLP; reparameterisation trick; trained on CRPS or Energy Score. Flipkart CPP (summary): forecasting layer (ML/deep learning, multiple granularities, hierarchical reconciliation) feeding an operations-research optimisation layer.

### 5. Statistical Analysis
Probabilistic scoring (scaled CRPS, Energy Score), multivariate Gaussian factor structure, 95% confidence intervals over 5 runs.

### 6. Machine Learning
- Model(s): CLOVER (MQCNN-based).
- Target variable: bottom-level series with aggregates by construction.
- Features: history and (per dataset) covariates; detail ND.
- Validation approach: last horizon window = test, preceding window = validation, earlier = train.
- Metrics: mean scaled CRPS; relative squared error in appendix.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| PyTorch, NeuralForecast, StatsForecast, HierarchicalForecast | Implementation and baselines |
| NVIDIA V100 | Single GPU |

### 8. Business Decision
CLOVER: not tied to a documented Amazon decision beyond acknowledgement of the Supply Chain Optimization Team. Flipkart CPP (summary): inventory placement and customer delivery planning.

### 9. Business Impact
CLOVER (authors' claim): "average gains of 15%" in sCRPS over state-of-the-art coherent methods; per-dataset overall improvements Favorita 27.67%, Traffic 54.40%, Tourism-S 10.24%, Tourism-L 4.16%, Wiki 4.5%; the paper is internally inconsistent on Labour (about 8% degradation in one place, 4% in another). Flipkart CPP (company claim via summary): planning cycle time cut by 90% (10 days to 1 day), 50% increase in 1-day deliveries, 50% reduction in unhealthy inventory, 10% manpower reduction, finalist for 2025 Franz Edelman Award.

### 10. What a Data Scientist Can Learn *(interpretation)*
Evaluate quantile/distribution forecasts with CRPS or pinball loss, not MAPE; enforce coherence by construction or reconciliation (bottom-up, MinT); the order decision should use a service-level quantile.

### 11. Source Links
- https://arxiv.org/html/2307.09797v4 (CLOVER, revised 21 Dec 2024)
- https://daily.dev/posts/the-pulse-of-india-s-supply-chain-how-flipkart-plans-for-500-million-customers-part-1-hxe7hr5gd (summary; original https://blog.flipkart.tech/the-pulse-of-indias-supply-chain-how-flipkart-plans-for-500-million-customers-part-1-50d241ca494f returned 403)

## Notes for the notebook author

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
