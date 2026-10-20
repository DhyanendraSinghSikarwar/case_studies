

### R1 — ETA / delivery-time prediction (Swiggy)
**(a) Calibrate to:**
1. Delivery time = Max(assignment delay + first mile, prep time) + last mile (Swiggy 2018).
2. Five targets with an additive identity: O2A + FM + WT + LM = O2R (Swiggy 2023).
3. Relative gains vs legacy: GBT "accuracy ~62%", inaccurate bumps "~27%" lower; neural network adds "~15%" and "~12%" (Swiggy 2023, company claim; absolute error not disclosed, so choose your own simulated scale).
4. MIMO sharing: "nearly 30%" lower O2A MAE; embeddings: 5% lower O2R MAE.
5. Public academic tabular analogue (not company data): LightGBM R2 0.76, MSE 20.59 on 41,368 cleaned rows (IIIT Delhi paper, Kaggle data).

**(b) Interviewer-expected techniques:** regression baselines (mean per restaurant-hour), gradient boosting (LightGBM/XGBoost), MAE/MAPE plus tail/percentile metrics, quantile or asymmetric loss, time-based train/test split, leakage avoidance (only features available at prediction time), coverage calibration, multi-output networks, categorical embeddings, seasonality handling (hour, weekday, weather).

**(c) Prevalence:** very common.

### R2 — Prep time and dispatch (Zomato / Swiggy)
**(a) Calibrate to:**
1. Zomato: MAE 4.64 to 4.13 minutes, MSE 32 to 28 after moving to the LSTM architecture.
2. ~3.5 million distinct dishes; ~150k+ restaurants ordered from in a month; 500+ cities, 400+ cuisines.
3. Sequence window: last 5 completed and up to 5 running orders per restaurant.
4. FOR (food-ready) button label fix: "9 percent improvement within 5 minutes accuracy".
5. Swiggy JIT illustration: prep 15 min, first mile 5 min, 10 minutes rider idle (illustrative only).

**(b) Expected techniques:** target definition and label noise, high-cardinality encoding (target encoding, embeddings), gradient boosting, quantile/asymmetric loss for dispatch decisions, rolling-window kitchen-load features, within-X-minutes hit rate, simulation of rider-wait versus food-wait trade-off.

**(c) Prevalence:** very common in food delivery; in grocery quick commerce the analogue is pick/pack time.

### R3 — Dark-store inventory / demand planning (Swiggy Instamart)
**(a) Calibrate to:**
1. Forecast horizon k of 1 to 7 days depending on shelf life and vendor turnaround.
2. Availability = % of store-open hours the SKU is in stock; wastage = GMV of units marked wasted.
3. 6–7 pods per warehouse cluster.
4. Estimated-metric example: new model "relative 2.4% better estimated availability with relative 2% reduced estimated wastage".
5. Assortment "hundreds of thousands of products"; picking batches capped at 2 orders.

**(b) Expected techniques:** SKU-store time-series and gradient-boosting forecasting, hierarchical and cold-start handling, censored-demand correction (stock-out imputation, Tobit-style thinking), wMAPE and bias, newsvendor/service-level inventory logic, safety stock, A/B or switchback store experiments, ABC/XYZ analysis.

**(c) Prevalence:** very common in quick commerce and grocery; assortment selection specifically is common but little documented publicly.

### R4 — Rider assignment, dispatch and batching (Swiggy)
**(a) Calibrate to:**
1. Scale statement: "200K+ Orders with 150K+ DEs and 100+ IM stores every day".
2. Decision cycle under one minute; cron-based rolling horizon.
3. JIT hold example: 15 min deferral less FM 3 less O2A 2 = 10 min hold.
4. Batching: first-mile distance per order halves when two orders share a trip (1 km to 0.5 km, illustration); batching paper: delivered-within-estimate up "about 6%".
5. Constraints: max weight, volume, k orders at once, LIFO for perishables, time windows.

**(b) Expected techniques:** vehicle routing with pickup/delivery and time windows, Hungarian/min-cost-flow assignment, greedy vs optimal, rolling-horizon simulation, cost-per-delivery metrics, ML for batchability and time prediction, city-level A/B tests (interference, switchback).

**(c) Prevalence:** very common in food and quick commerce; common in ecommerce last mile in a slower route-planning form.

### R5 — Delivery promise / EDD (Myntra)
**(a) Calibrate to:**
1. BAU accuracy/breach: rule-based 36.56% / 5.63%; LightGBM quantile 68.10% / 4.68%.
2. HRD: LightGBM 65.15% / 7.86% vs rule-based 44.23% / 5.44%; post-HRD 74.58% / 4.82% vs 54.48% / 3.06%.
3. Lane contrast: Delhi-Gurugram ~83.55% for all models; Delhi-Kolkata 50.34% (time series) to 75.26% (LightGBM).
4. Training set "more than a million" examples from the last few weeks; tested the next day.
5. Warehouse leg: fbprophet 88.19% / 6.54% vs rule-based 82.23% / 3.79%.

**(b) Expected techniques:** quantile regression, asymmetric/pinball loss, distributional or survival models for lead time, hit-rate versus breach-rate trade-off, holiday and weekday seasonality, event-day handling, leg-wise decomposition, time-based validation, monitoring and drift.

**(c) Prevalence:** very common in ecommerce (every marketplace shows a delivery date).

### R6 — Address quality / geocoding (Swiggy)
**(a) Calibrate to:**
1. Classifier AUC-ROC 0.89; +23 pp precision and +32 pp recall vs the earlier text+location model.
2. Imbalance factor "of the order of a few tens" negatives per positive (estimated on a few thousand manually checked orders).
3. DBSCAN baseline: min points 4, epsilon 20 (unit not legible in my copy); H8 cell edge 531 m.
4. Raw geocoder delivery deviation is "of the order of a few hundred metres" (unusable); target accuracy "tens of meters".
5. Union geocoder: +139 pp order coverage vs DBSCAN; production correction: delivery deviation down by 143 (unit garbled, presumably metres) on corrected addresses.

**(b) Expected techniques:** DBSCAN/density clustering of delivery pins, geohash/H3 indexing, Haversine distance, address-text NLP (TF-IDF fuzzy match, transformers), imbalanced classification (PR curve, threshold choice), weak/self-supervised labels, percentile error metrics, pincode/locality classification, route optimisation (VRP/TSP heuristics) as the downstream use.

**(c) Prevalence:** very common in India (unstructured addresses affect every ecommerce and logistics firm).

### Cases where evidence was thin or substituted
- R3: no Zepto or Blinkit primary engineering source found; used Swiggy Instamart. Assortment selection and dark-store placement are not documented in anything I read (only forecasting/inventory and picking). A web search surfaced Zepto write-ups, but they were secondary summaries which I did not fetch and have not used.
- R5: no Flipkart or Amazon India primary source found; used the Myntra paper. Nothing credible found for Amazon India.
- bytes.swiggy.com and Medium were unreachable from my environment; all Swiggy Bytes content was read via web.archive.org snapshots. Publication dates come from the page text or page metadata.
- R4: the Instamart posts and the batching paper summary give no outcome metrics; the ACM paper itself was not fetched.
- No Zomato post on rider dispatch/assignment was found; Swiggy is used for R4.
