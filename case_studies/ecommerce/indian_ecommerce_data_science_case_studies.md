# How Real Indian Ecommerce and Quick-Commerce Data Scientists Solved Real Business Problems

**30 case studies from food delivery, quick commerce, marketplaces and fashion/beauty ecommerce: delivery, demand, search, ads, growth, trust and support**

*Research compiled: 17 October 2026. All facts come from the cited public sources that the research agents actually opened. "Not publicly disclosed" (ND) means the sources do not state the detail. "What a Data Scientist Can Learn" sections are interpretation and are labelled as such.*

---

## Executive Summary

### What was researched
- Company engineering blogs (Swiggy Bytes, Zomato, Flipkart Tech, Myntra, Meesho), arXiv and conference papers by company authors (Flipkart, Myntra, Amazon, Swiggy), cloud-vendor case studies, IPO coverage and business press.
- Five parallel research streams (delivery and quick-commerce operations, demand and pricing, search and recommendations, growth and customer value, trust and returns), each told to record only what it could read and to mark the rest as ND.
- **Several primary pages were unreachable** (Medium, parts of Swiggy Bytes, some press sites). Where a post was read through an archive or a summary, the entry says so. Anything seen only in a search snippet was left out.

### How well documented is each case?

| Evidence | Cases | Count |
|---|---|---|
| Strong | 1, 2, 3, 4, 5, 6, 11, 14, 15, 16, 17, 22, 25, 26, 27 | 15 |
| Medium | 7, 12, 13, 18, 19, 20, 28, 29, 30 | 9 |
| Weak | 8, 9, 10, 21, 23, 24 | 6 |

### What the research found about public disclosure
1. **Method detail is public for forecasting, search, recommendations, ETA, and returns/fraud classification**, mostly through company-authored papers. Pricing, surge/fee design, sale-event planning, push notifications and marketing-mix modelling have almost no public method detail from Indian companies; those entries say so, and the notebooks treat them as **interview-standard problems solved with simulated data**, not as reproductions of any company's system.
2. **Impact numbers are rare and are almost always the company's own claims.** The strongest quantified results are Flipkart's unified ads ranking (organic orders +1.36%, ad revenue +3.4%) and Myntra's visual-similarity A/B (CTR +25%, add-to-cart +4%).
3. **Several cases substitute a better-documented company for the one first named** (e.g., Myntra for Flipkart on delivery promise; Meituan for Indian coupon allocation; Cabify for switchback experiments). Each entry states the substitution.
4. **Cash-on-delivery and returns are India-specific problems:** Meesho's IPO documents (as reported by MediaNama) put COD at the large majority of its orders, and Flipkart's published COD study found 32% RTO in its sample.

### Evidence legend

| Level | Meaning | Shown as |
|---|---|---|
| A | Company or named employee described the project | **Strong** |
| C | Paper / conference talk by company team | **Strong** |
| B | Credible external source on the actual implementation | **Medium** |
| D | Generic or vendor marketing with little method detail | **Weak / partially documented** |

---

<!-- PRIORITY-INDEX-START -->
### Priority guide (added by the notebook series)

How to read the stars: **★★★ Must-visit** = core techniques that Indian ecommerce and quick-commerce teams use every day and that interviews ask about most; study these first. **★★ Good to have** = valuable technique, narrower use or thinner public evidence. **★ Optional** = niche, or mostly deep-learning engineering. Ratings are my interpretation (frequency in industry and in interviews), not part of the sources.

| Case | Priority | Why | Notebook | Status |
|---|---|---|---|---|
| 1 | ★★★ Must-visit | ETA / delivery-time regression with SLA-aware loss: the most-asked ML case in food and quick-commerce interviews | `cs01_delivery_eta_prediction.ipynb` | ✅ |
| 2 | ★★ Good to have | Prep-time estimation and its effect on dispatch: noisy-label regression and cost of lateness | `cs02_prep_time_dispatch.ipynb` | ⏳ |
| 3 | ★★ Good to have | Demand planning for availability vs wastage plus picking batching: the newsvendor core | `cs03_dark_store_inventory.ipynb` | ⏳ |
| 4 | ★★ Good to have | Assignment and batching as an optimisation problem; rolling-horizon dispatch | `cs04_rider_assignment_batching.ipynb` | ⏳ |
| 5 | ★★ Good to have | Delivery promise with breach control: quantile regression and coverage guarantees | `cs05_delivery_promise_date.ipynb` | ⏳ |
| 6 | ★ Optional | Address and geocoding quality: classification with clustering; narrower use | `cs06_address_quality_geocoding.ipynb` | ⏳ |
| 7 | ★★★ Must-visit | Demand forecasting under stock-outs (censored sales): asked in every supply-chain interview | `cs07_quickcommerce_demand_forecasting.ipynb` | ✅ |
| 8 | ★★ Good to have | Price elasticity and discount efficacy; interview staple but little public company method | `cs08_price_elasticity_discounts.ipynb` | ⏳ |
| 9 | ★★ Good to have | Surge and fee design; marketplace economics, little public company method | `cs09_delivery_fee_surge_pricing.ipynb` | ⏳ |
| 10 | ★ Optional | Sale-event capacity planning; methods undisclosed, seasonal and peak forecasting | `cs10_sale_event_capacity_planning.ipynb` | ⏳ |
| 11 | ★★★ Must-visit | Cold-start demand forecasting for new items (fashion); strongly documented | `cs11_new_item_demand_forecasting.ipynb` | ⏳ |
| 12 | ★★ Good to have | Hierarchical, probabilistic forecasting; advanced but increasingly standard | `cs12_hierarchical_probabilistic_forecasting.ipynb` | ⏳ |
| 13 | ★★ Good to have | Query understanding for Hinglish; NLP evaluation in search | `cs13_hinglish_search_queries.ipynb` | ⏳ |
| 14 | ★★ Good to have | Visual similar-item retrieval with A/B-validated lift | `cs14_visual_similarity_recommendations.ipynb` | ⏳ |
| 15 | ★★★ Must-visit | Item-to-item CF: the foundational recommender, asked in almost every ecommerce interview | `cs15_item_to_item_collaborative_filtering.ipynb` | ✅ |
| 16 | ★★ Good to have | Search relevance and ranking metrics (NDCG, MRR) in food delivery | `cs16_dish_search_ranking.ipynb` | ⏳ |
| 17 | ★★★ Must-visit | Sponsored/organic ranking with CTR/CVR prediction and calibration: the revenue engine of marketplaces | `cs17_ads_ranking_ctr_cvr.ipynb` | ⏳ |
| 18 | ★★ Good to have | Cold start and bandit exploration for feeds | `cs18_cold_start_exploration_bandits.ipynb` | ⏳ |
| 19 | ★★★ Must-visit | A/B testing, variance reduction, interference and switchbacks: THE interview staple | `cs19_experimentation_ab_testing.ipynb` | ⏳ |
| 20 | ★★★ Must-visit | Predicted customer LTV for acquisition bidding: asked everywhere, drives marketing spend | `cs20_customer_lifetime_value.ipynb` | ⏳ |
| 21 | ★★ Good to have | Membership design and retention: causal measurement without randomisation | `cs21_membership_programme_retention.ipynb` | ⏳ |
| 22 | ★★★ Must-visit | Uplift targeting and budget-constrained coupon allocation: the core promo-optimisation problem | `cs22_coupon_allocation_uplift_budget.ipynb` | ⏳ |
| 23 | ★ Optional | Notification volume and timing experiments; methods undisclosed | `cs23_push_notification_optimisation.ipynb` | ⏳ |
| 24 | ★★ Good to have | Marketing-mix modelling with geo-lift calibration; common in D2C and marketplaces | `cs24_marketing_mix_modelling.ipynb` | ⏳ |
| 25 | ★★★ Must-visit | COD return-to-origin prediction: imbalanced classification with a business cost; India-specific and very common | `cs25_cod_rto_prediction.ipynb` | ⏳ |
| 26 | ★★ Good to have | Size/fit prediction to cut returns in fashion | `cs26_size_fit_returns.ipynb` | ⏳ |
| 27 | ★★ Good to have | Rating-fraud detection with anomaly scoring | `cs27_fake_review_rating_fraud.ipynb` | ⏳ |
| 28 | ★ Optional | Catalogue attribute extraction with multimodal models; heavy deep-learning engineering | `cs28_catalogue_attribute_extraction.ipynb` | ⏳ |
| 29 | ★★ Good to have | Support automation, containment vs CSAT | `cs29_support_automation_resolution.ipynb` | ⏳ |
| 30 | ★★ Good to have | Buy Box and seller quality: auditing a ranking algorithm from outside | `cs30_buy_box_seller_quality.ipynb` | ⏳ |
<!-- PRIORITY-INDEX-END -->

---

# PART A — DELIVERY & QUICK-COMMERCE OPERATIONS

## Case Study 1 — Swiggy's multi-stage ETA and delivery-time promise models (cart pSLA and tracking-screen ETA)

**Priority:** ★★★ Must-visit — ETA / delivery-time regression with SLA-aware loss: the most-asked ML case in food and quick-commerce interviews. **Notebook:** `cs01_delivery_eta_prediction.ipynb` (✅ notebook built)

**Company:** Swiggy (India, food delivery)
**Industry:** Food delivery / hyperlocal logistics
**Business Area:** Customer promise (cart delivery-time) and post-order tracking ETA; downstream dispatch and customer care
**Problem Type:** Supervised regression (multi-target time prediction), plus metric design for customer trust
**Evidence Level:** Strong (A: three posts on Swiggy's own engineering blog by named Swiggy data scientists; no absolute error values disclosed, only relative improvements)
**Primary Sources:** Swiggy Bytes "Predicting Food Delivery Time at Cart" (Aug 11, 2023); "Where is my order? Part I" (May 22, 2023); "How ML Powers — When is my order coming? Part II" (May 26, 2023); "The Swiggy Delivery Challenge Part One" (Sep 27, 2018)

### 1. Business Problem
Swiggy shows a promised delivery time (pSLA) on the cart page and a live ETA on the tracking screen. The cart post says the promise "can be a make or break factor for placing an order" and is "a double edged sword": a delayed order upsets customers, but a conservative promise "reduces the propensity of the customer to place an order", so Swiggy has to operate "within the Goldilocks zone". The Part I tracking post adds that customers anchor on the ETA to judge whether an order is late, so it drives chat/call contacts and cancellations. Downstream systems also consume the promise: the assignment system, customer-care ticket handling, and exception management.

### 2. Business Question
How accurately can Swiggy predict, at cart time and then as the order progresses, the time legs of an order (assignment, first mile, wait, last mile) so the promise is neither too long (lost orders) nor too short (breaches, contacts, cancellations), and so the displayed ETA does not jump erratically?

### 3. Data Available
| Data | Description (as stated in sources) |
|---|---|
| Historical order legs | Past O2A, FM, WT, LM, O2R times by restaurant, zone, hour and week; used as historical and near-real-time moving averages "with different time windows and pivots" |
| Restaurant and order attributes | Restaurant type (cloud kitchen vs dine-in), number of unique and total items, kind of dishes, restaurant stress from recent orders placed vs prepared, past prep behaviour per item |
| Network/assignment state | Active delivery executives (DEs) vs active orders ("stress in the system"), number of DEs near the restaurant and their average distance, historical assignment and first-mile behaviour by restaurant and ops zone |
| Delivery-executive GPS pings | Real-time pings turned into current speed, "global speed", remaining haversine distance, cumulative distance; DE familiarity with restaurant/customer location; mode of transport |
| Geography | Customer geohashes, city; historic and real-time speed patterns around customer and restaurant locations |
| Other real-time signals | Rain, DE rejection possibility, RX (restaurant) confirm flag, time elapsed in stage, live restaurant order count |

### 4. Data Science Approach
Documented structure:
- Definition (2018 post): Delivery Time = Max(Assignment Delay + First Mile Time, Prep Time) + Last Mile Time, because assignment and first mile run in parallel with food preparation. The 2018 post says Google Maps was not used because it is too slow and costly at Swiggy's scale and does not predict two-wheeler times or the "last last mile" (gate to door).
- Cart model (2023): one multi-input multi-output (MIMO) deep network with entity embeddings predicts five targets: O2A (order to assignment), FM (first mile), WT (wait), LM (last mile) and O2R (order to reached). Embeddings encode restaurants, customer geohashes and cities. The shared network is used because O2A and FM are "intricately linked": the assignment engine tries to send a DE to arrive just before the food is ready, so assignment delay depends on first-mile distance and prep time. The cart model also consumes the output of the separate food-preparation-time model.
- Tracking ETA (2023): four separate models, one per stage (Ordered, Assigned, Arrived/Wait, Picked up), refreshed at fixed intervals, built on top of the cart pSLA and adding stage-specific real-time features. The stated reason for four models is that the feature space differs by stage.
- Model evolution (Part II): first gradient boosting trees (GBT) with absolute loss, then replaced by neural networks to make predictions "more dynamic".
- Planned: RNN/LSTM sequence models, Graph Neural Networks for the last-mile stage, POI features and DE rejection probability.

### 5. Statistical Analysis
Documented: seasonality and recency are explicitly used ("hourly and weekly seasonality", Saturday 9 pm compared with the previous week), implemented as historical plus near-real-time moving averages over several windows. Outlier pings are screened before speed and distance features are computed. Metric design is documented (section 6). No hypothesis tests, confidence intervals or A/B test design are described. ND otherwise.

### 6. Machine Learning
- **Models:** Cart: MIMO deep network with entity embeddings. Tracking ETA: four stage models; GBT with absolute loss (v1), then feed-forward neural networks (v2) with four hidden layers, Leaky ReLU, Adam, 50 epochs; hidden sizes OR (32,32,16,16), FM (24,24,12,12), WT (16,16,16,16), LM (8,8,8,8).
- **Target variable:** Cart: O2A, FM, WT, LM, O2R times. Tracking: remaining time to delivery at each stage (stage-specific leg predictions).
- **Features:** see section 3, plus in-model embeddings for restaurant, geohash and city.
- **Validation approach:** ND (no train/test split, backtest or experiment design described; Part II shows before/after charts vs the legacy system).
- **Metrics:** MAE; BDC (bi-directional compliance: % of targets within +/-X of prediction); ED (egregious delay: % of targets beyond +Y of prediction); for tracking, MAE against a threshold and "Percentage of Orders with Inaccurate Bumps" (sudden ETA jumps). Values of X, Y and the MAE threshold are ND. The post notes necessary jumps (batching, stationary DE, high restaurant stress) should not be penalised.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Deep learning (entity embeddings, MIMO, feed-forward NN) | Cart and tracking models |
| Gradient boosting trees | First tracking-ETA version |
| Real-time DE pings and feature pipelines | Speed/distance features (platform details ND in these posts) |
| Haversine distance | Ping-derived distance features |
| Separate prep-time model | Input to the cart model |

### 8. Business Decision
Documented: replace the legacy ETA framework with the ML-based four-stage ETA and move it from GBT to neural networks; use a MIMO architecture for the cart promise; use the promise as an input to assignment and exception management. The tracking screen was revamped to show the ML ETA ("The revamped Swiggy Track Screen powered by ML based predictions").

### 9. Business Impact
Swiggy's own claims (Part II, May 2023; "Accuracy" is a Swiggy-defined measure whose absolute level is ND):
- GBT vs legacy: "Accuracy improving by ~62% and the number of inaccurate bumps decreasing by ~27%".
- Neural network vs GBT: "an increase of approximately 15%" in accuracy and "a reduction of approximately 12%" in orders with inaccurate bumps.
- "a notable decline in customer-care agent interactions and order cancellations" (no figure: ND).

Cart model (Aug 2023, company claims): MIMO reduced training memory footprint "by around 50%" and training times "to nearly a fifth"; "nearly 30% improvement in the MAE for O2A predictions"; in-model embeddings reduced overall MAE (O2R time) "by 5%".

### 10. What a Data Scientist Can Learn *(interpretation)*
- A customer-facing time estimate is a trade-off, not a pure accuracy problem; the Goldilocks framing and the BDC/ED metrics show why MAE alone is not enough.
- Splitting by stage because features differ (no assigned DE yet vs live pings) is a general pattern for "time remaining" models; the stage models re-use the earlier prediction as an input.
- Joint multi-output training helps when outputs are causally linked (assignment delay and first mile via the dispatch policy): the model is partly predicting the behaviour of another algorithm.
- Smoothness of the displayed estimate (bump metric) is a product metric worth designing for.

### 11. Source Links
- https://bytes.swiggy.com/predicting-food-delivery-time-at-cart-cda23a84ba63 — "Predicting Food Delivery Time at Cart", Swiggy Bytes, Aug 11, 2023 (read via web.archive.org snapshot)
- https://bytes.swiggy.com/how-ml-powers-when-is-my-order-coming-part-i-4ef24eae70da — "Where is my order? Part I", May 22, 2023 (archive snapshot)
- https://bytes.swiggy.com/how-ml-powers-when-is-my-order-coming-part-ii-eae83575e3a9 — "How ML Powers — When is my order coming? Part II", May 26, 2023 (archive snapshot)
- https://bytes.swiggy.com/the-swiggy-delivery-challenge-part-one-6a2abb4f82f6 — "The Swiggy Delivery Challenge (Part One)", Sep 27, 2018 (archive snapshot)
- Supplementary, academic not company: https://arxiv.org/abs/2503.15177 — "Food Delivery Time Prediction in Indian Cities Using Machine Learning Models", IIIT Delhi authors, Mar 2025 (PDF read). It uses a public Kaggle dataset of 45,000 records (41,368 after cleaning); best model LightGBM, R2 0.76, MSE 20.59 (the paper's own numbers; not Swiggy or Zomato data)

---

## Case Study 2 — Zomato's food preparation time (FPT) prediction and how prep time drives rider dispatch (with Swiggy JIT dispatch)

**Priority:** ★★ Good to have — Prep-time estimation and its effect on dispatch: noisy-label regression and cost of lateness. **Notebook:** `cs02_prep_time_dispatch.ipynb` (⏳ notebook pending)

**Company:** Zomato (prep-time model); Swiggy (documents how prep time feeds just-in-time dispatch)
**Industry:** Food delivery
**Business Area:** Kitchen prep-time estimation, delivery-partner assignment timing
**Problem Type:** Supervised regression (sequence model plus entity embeddings), feeding a dispatch-timing rule
**Evidence Level:** Strong for the prep-time model (A: named Zomato engineer's blog post, 2020); Medium for the dispatch effect (Swiggy describes the logic and trade-offs but gives no quantified result)
**Primary Sources:** Zomato blog "The Deep Tech Behind Estimating Food Preparation Time" (Deepankar Pal, Feb 4, 2020); Swiggy Bytes "The Swiggy Delivery Challenge Part Two" (May 8, 2019); Swiggy Bytes cart post (Aug 2023)

### 1. Business Problem
Zomato says accurate time estimation matters because a higher-than-actual estimate "can deter customers from ordering" and a lower one "can then increase inflow to our customer support". FPT (the time a restaurant takes to prepare food) is one component, along with delivery-partner (DP) pick-up time and drop time. Zomato says better FPT prediction helps "better delivery time, better allocation of DPs in order assignment and efficient delivery of orders" and helps monitor restaurant FPT breaches and compliance. Swiggy (2019) states the dispatch side: if food takes 15 minutes and a DE can arrive in 5, the executive waits 10 minutes, which reduces "the number of orders we can do per day per Delivery Executive"; arriving too late makes food go cold.

### 2. Business Question
How accurately can the kitchen preparation time of an order be predicted at order placement (thousands of restaurants, ~3.5 million distinct dishes, varying kitchen load), and how should that estimate be used to time the rider's dispatch so the rider arrives just as the food is ready?

### 3. Data Available
| Data | Description (as stated) |
|---|---|
| Order items | Item text, quantity, cost; ~3.5m distinct dishes on the platform |
| Restaurant identity | Food ordered from ~150k+ restaurants in a month; restaurant-level traits (delivery-only vs fine dining, kitchen capacity) |
| Kitchen state | Queued/running orders (max 5 running orders used), last 5 completed orders, opening hours (how long the kitchen has been open for delivery) |
| Labels | FPT originally = restaurant-accepted timestamp to DP pick-up timestamp; later improved using a restaurant-marked "Food Order Ready" (FOR) button |
| Swiggy side (2019 and 2023 posts) | Item type, number of items, restaurant load, restaurant's and customer's order history, how long existing orders are taking |

### 4. Data Science Approach
Zomato (documented): item-level information encoded with Word2Vec embeddings (Bag-of-Words and Tf-Idf rejected: millions of columns, growth with new dishes, sparsity, latency). Multi-item orders get a quantity- and cost-weighted average of item vectors. Restaurants are encoded by entity embeddings learned by a neural network (X = current order information, order vector, restaurant vector; Y = FPT), visualised with t-SNE. Model 1: learned restaurant embeddings plus the same feature vector fed to an XGBoost regressor. Model 2: a deep sequential architecture where the last 5 completed and up to 5 running orders go through a stacked LSTM, concatenated with current-order features and restaurant embedding, then a 2-layer dense network regressed on FPT. Next step stated: reinforcement learning that updates with real-time restaurant-level errors.

Label fix: because the old label included rider pick-up behaviour, Zomato added the FOR button so restaurants mark when food is ready.

Dispatch (Swiggy, documented logic): the naive just-in-time rule delays assignment by "Estimated Prep Time - Avg. First Mile Time"; a refinement earmarks a DE but dispatches just in time so assignments can be swapped when a new order arrives; Next Order Assignment considers DEs about to finish an order. Risks listed: DE rejection after a delay, prep over-estimate (food sits), first-mile under-estimate. The 2023 Swiggy post confirms the prep-time model's output is consumed by the assignment engine "to make sure the DE arrives before food is ready".

### 5. Statistical Analysis
Documented: framing of FPT as a time series per restaurant ("FPT of a restaurant could also be understood as a time series"); label-noise reasoning about the FPT definition; t-SNE and clustering of embeddings as a sanity check. No hypothesis tests or interval estimates. ND otherwise.

### 6. Machine Learning
- **Models:** Word2Vec item embeddings; entity embeddings for restaurants; XGBoost regressor; stacked LSTM plus dense network.
- **Target variable:** Food preparation time (minutes).
- **Features:** order vector (item embeddings weighted by quantity and cost), restaurant embedding, current order-level information, previous 5 completed and up to 5 running orders at the restaurant, opening-hours signal, queued orders, other items in the order.
- **Validation approach:** ND (no split described).
- **Metrics:** MAE, MSE; "within 5 minutes" accuracy for the FOR-label experiment.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Word2Vec | Menu item embeddings |
| Neural network entity embeddings, t-SNE | Restaurant representation and visualisation |
| XGBoost | First FPT regressor |
| Stacked LSTM + dense layers | Sequential kitchen-state model |
| Restaurant Partner app "Food Order Ready" button | Cleaner FPT label |
| Swiggy assignment engine | Consumes prep prediction (details ND) |

### 8. Business Decision
Documented: adopt a sequential deep model; change label capture by adding the FOR button to the Restaurant Partner app; move toward reinforcement-learning style online updating. For dispatch (Swiggy): defer dispatch so the DE reaches the restaurant just in time rather than as early as possible, while keeping the ability to swap assignments.

### 9. Business Impact
Zomato (company claims, 2020): the deep learning architecture let them "reduce our mean absolute error from 4.64 mins to 4.13 mins and mean squared error from 32 to 28" (the page presents this as improvement over the previous architecture; the XGBoost model's own MAE is not separately stated). FOR button: "we saw a 9 percent improvement within 5 minutes accuracy for our prediction" in "initial results". Dispatch efficiency gains from JIT/prep-time (rider wait saved, orders per rider): ND. Swiggy gives only an illustrative example (15 min prep, 5 min first mile, 10 min wait).

### 10. What a Data Scientist Can Learn *(interpretation)*
- Label definition can dominate model quality: an FPT label contaminated by rider behaviour limits any model; fixing measurement (the FOR button) produced a gain that model changes alone would not.
- High-cardinality categoricals (restaurants, dishes) are the central modelling issue; embeddings are the documented solution at both Zomato and Swiggy.
- A prediction used by a dispatch policy has asymmetric costs (over-estimate holds food; under-estimate leaves the rider waiting or food late), so interviewers may expect discussion of quantile or asymmetric loss even though these posts only report MAE/MSE.
- Restaurant compliance in pressing FOR is itself a data-quality and incentive problem.

### 11. Source Links
- https://www.zomato.com/blog/food-preparation-time — "The Deep Tech Behind Estimating Food Preparation Time", Deepankar Pal, Feb 4, 2020 (fetched directly)
- https://bytes.swiggy.com/the-swiggy-delivery-challenge-part-two-f095930816e3 — "The Swiggy Delivery Challenge (Part Two)", May 8, 2019 (archive snapshot)
- https://bytes.swiggy.com/the-swiggy-delivery-challenge-part-one-6a2abb4f82f6 — Part One, Sep 27, 2018 (archive snapshot)
- https://bytes.swiggy.com/predicting-food-delivery-time-at-cart-cda23a84ba63 — Aug 11, 2023 (archive snapshot)

---

## Case Study 3 — Swiggy Instamart dark-store demand planning: forecasting for availability versus wastage (plus dark-store picking batching)

**Priority:** ★★ Good to have — Demand planning for availability vs wastage plus picking batching: the newsvendor core. **Notebook:** `cs03_dark_store_inventory.ipynb` (⏳ notebook pending)

**Company:** Swiggy Instamart (substituted for Zepto/Blinkit: I found no primary technical post for either that I could fetch)
**Industry:** Quick commerce (grocery)
**Business Area:** Dark-store (pod) inventory planning and operations
**Problem Type:** Demand forecasting with censored (stock-out truncated) demand; offline evaluation design; plus optimisation for in-store picking
**Evidence Level:** Strong for inventory/forecast evaluation (A: named Swiggy data scientists, 2023); Medium for picking (A, but results are qualitative only). Assortment selection and dark-store placement: Weak, not publicly documented in what I read
**Primary Sources:** Swiggy Bytes "Adaptive Metric Alignment for Demand Forecasting in Swiggy Instamart" (May 24, 2023); "Optimising the picking process to enable faster deliveries for Instamart" (Jul 10, 2024)

### 1. Business Problem
Instamart runs dark stores ("pods") serving a few kilometres' radius, with an assortment of "hundreds of thousands of products". Demand planning must "maximize 'availability' while reducing the 'wastage'". Stock-outs hurt customer experience and are opportunity loss; over-procurement of perishables causes wastage through expiry. The business team defines different availability and wastage targets by category. Sales data equals true demand only when the item was available; during an out-of-stock, sales are truncated demand, so standard forecast metrics mislead.

### 2. Business Question
How should demand be forecast, and forecast models be evaluated offline, so that deploying a model actually improves pod-level availability and reduces wastage, given censored sales data?

### 3. Data Available
| Data | Description (as stated) |
|---|---|
| Daily SKU-by-pod sales | Units sold per SKU per pod per day, S_i(t) |
| Observed availability | A_i(t): share of store-open hours the SKU was in stock |
| Hourly sales | Available for many SKUs; used to estimate when predicted stock would have sold out |
| Item attributes | Shelf life, vendor turnaround time (set the forecast horizon k = 1 to 7 days), fill rate |
| Hierarchy | City/zone of pod, trend and seasonality; "6–7 pods form a cluster" served by a warehouse |
| Wastage | Measured as GMV of units marked for wastage on expiry |

### 4. Data Science Approach
Documented demand-planning chain: forecast demand k days ahead per SKU per pod; purchase-order generation (a second ML model adds buffer for forecast error and fill rate); delivery to warehouse; distribution to pods; inventory-system update. Core contribution: replace wMAPE-against-sales with simulated business metrics. Estimated Availability (EA) asks "what would availability and wastage have been if this prediction had been used?" A simple version assumes availability rises proportionally with sales; a refined version uses hourly sales: estimated available hours are computed from the hour the predicted units would have sold out, otherwise extrapolated using the day's median hourly sales. Estimated Wastage (EW) is defined analogously. The post lists three wMAPE flaws: under-prediction bias when availability is low; wMAPE on only high-availability days ignores cold-start/long-tail SKUs; and wMAPE is non-directional for the business metrics.

Related dark-store operations (picking, Jul 2024): free pickers are assigned round-robin; the proposal batches up to k = 2 orders for one picker using an optimisation model with Time To Pack (accounting for item similarity), Time To Free, and a delay cost, validated with a discrete-time SimPy simulation on real order, picker and shelving data.

### 5. Statistical Analysis
Documented: truncated/censored demand reasoning; definition of the offline estimators EA and EW; validation of EA/EW against production using randomised store experiments: (a) two models running in two randomly chosen pod sets, with each model's EA/EW computed on the pods where it was not used, to avoid leakage; (b) a 50-50 random bucketing of stores comparing predicted lift (EA/EW from backtesting) with actual lift. Significance tests: ND.

### 6. Machine Learning
- **Models:** "ML based forecasting models" (specific algorithms ND in this part of the series; later parts not read); PO-buffer model (ND).
- **Target variable:** Units demanded per SKU per pod per day (forecast k days ahead), with the truncated-sales caveat.
- **Features:** historic SKU sales in the pod, city/zone, trend and seasonality of item demand (others ND).
- **Validation approach:** offline backtesting with EA/EW, then live randomised store experiments as above.
- **Metrics:** wMAPE (criticised), Estimated Availability, Estimated Wastage, observed availability and wastage.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| ML forecasting pipeline | SKU-pod daily demand (stack ND) |
| Inventory Management System (IMS) | Live stock per pod |
| SimPy (picking post) | Discrete-time simulation of batch picking |
| Optimisation model (picking post) | Batch-to-picker assignment |

### 8. Business Decision
Select forecasting models by backtested EA/EW rather than wMAPE; deploy the winner into demand planning (purchase orders per pod). For picking: batch up to two similar orders per picker when free pickers are fewer than unassigned orders, subject to item-count, weight and similarity thresholds (cap of 2 chosen to limit packing errors).

### 9. Business Impact
- In an example the post reports model M2 vs M1 with "a relative 2.4% better estimated availability with relative 2% reduced estimated wastage"; the post says the live 50-50 store experiment showed the availability lift "is very well estimated" and the wastage direction matched. The table of actual values was an image I could not read, so the actual numbers: ND here. Company claim.
- The 65% availability and 146-unit examples in the post are explicitly illustrative, not results.
- Picking: results are qualitative (picker assignment time down, picker-assigned-to-ready time down, mean time-to-pack up for batched orders); no numeric figures: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Censored demand is the central trap in retail forecasting: training on sales conflates demand with availability.
- When the business metric cannot be measured offline, build a defensible simulated metric and validate it against randomised store experiments (the leakage-free cross-evaluation is a clean trick).
- Perishability makes the loss asymmetric and category-specific; the policy output (purchase order) matters more than point forecast error.

### 11. Source Links
- https://bytes.swiggy.com/adaptive-metric-alignment-for-demand-forecasting-in-instamart-9aa5d2fca308 — Swiggy Bytes, published 2023-05-24 per page metadata (archive snapshot of 2023-05-29)
- https://bytes.swiggy.com/optimizing-the-picking-process-to-enable-faster-deliveries-for-instamart-93de0fe9d819 — Swiggy Bytes, 2024-07-10 per page metadata (archive snapshot)

---

## Case Study 4 — Swiggy Instamart (and food delivery) delivery-executive assignment, batching and just-in-time dispatch

**Priority:** ★★ Good to have — Assignment and batching as an optimisation problem; rolling-horizon dispatch. **Notebook:** `cs04_rider_assignment_batching.ipynb` (⏳ notebook pending)

**Company:** Swiggy (Instamart for the detailed method; food delivery for JIT/NOA/batching background)
**Industry:** Quick commerce / food delivery
**Business Area:** Last-mile fleet assignment and routing
**Problem Type:** Combinatorial optimisation (rolling-horizon dynamic pickup-and-delivery with time windows, plus assignment), with ML time predictions as inputs
**Evidence Level:** Strong for method (A: named Swiggy data scientists); outcome figures largely ND
**Primary Sources:** Swiggy Bytes "Assignment & Routing Optimization for Swiggy Instamart Delivery" Parts I (Sep 15, 2022) and II (Sep 20, 2022); "The Swiggy Delivery Challenge Part Two" (May 8, 2019); "Paper on ML-based batching prediction" (Feb 23, 2022 summary of Moghe, Rathee, Nayak, Adusumilli, ACM IKDD CODS-COMAD 2021)

### 1. Business Problem
Part I frames it: "The overall objective is to deliver groceries within promised time but at minimal delivery cost" while finding routes in near real time. It describes the scale as "more than 200K+ Orders with 150K+ DEs and 100+ IM stores every day". The 2019 food-delivery post says assigning the closest DE "is usually bad on a global scale", and that unlike other e-commerce companies, Swiggy has "at best a few minutes" to optimise.

### 2. Business Question
Which delivery executive should get which order or batch, in what sequence, and when should assignment/dispatch happen, so cost per delivery (CPD) falls while promised delivery times are met?

### 3. Data Available
| Data | Description (as stated) |
|---|---|
| Orders | Customer locations, store (depot), promised slot/pSLA, weight and volume, perishable flags |
| DEs | Current location/state, capacity limits (max weight W, volume, max k orders) |
| Time predictions | ML-predicted FM, LM, wait, customer-to-customer and store-to-store travel times, and O2A; "we heavily rely on the time prediction models" |
| Constraints | Time windows (earliest/latest pickup and drop), service time per stop, LIFO for perishables |

### 4. Data Science Approach
Instamart: the full problem is a Multi-Depot Pickup Delivery Problem with Time Windows (MDPDPTW), judged infeasible to solve directly in near real time; clustering the DEs is hard because DEs are not mutually exclusive across clusters. So it is split into two sequential stages solved every decision cycle (cron) on a rolling horizon, with a sub-minute target.
- Stage I (last mile): batching and sequencing as a Dynamic PDPTW solved by a construction heuristic plus a meta-heuristic; also a greedy heuristic to maximise batching percentage. Orders can be added to existing batches until pickup by freezing the route up to the store. Documented trade-off: a longer cron collects more orders (better solutions) but raises O2A time.
- Stage II (first mile): just-in-time (JIT) assignment. External JIT heuristic holds a batch until slot end/pSLA minus predicted FM and O2A (example: defer pickup 15 min; FM 3, O2A 2, so hold 10 min). Internal JIT: a multi-objective assignment model (each DE to one batch and vice versa) whose objective trades off the cost of assigning now vs later, combining CPD and a customer-experience term that is a function of estimated delay.

Food delivery (2019): JIT, Next Order Assignment, and batching; batching is said to be NP-hard; batchability depends on concurrent orders and proximity of customers and restaurants; promises are raised only for orders likely to be batched. A 2021 paper by Swiggy authors built ML to predict delivery times for batched orders.

### 5. Statistical Analysis
Documented: none specific beyond cost trade-off reasoning (per-order first-mile distance halves when two orders share a trip: 1 km becomes 0.5 km per order, the post's illustration). ND otherwise.

### 6. Machine Learning
- **Models:** Optimisation (not learned) core; learned time-prediction models feed it. The batching-prediction paper abstract says it uses "multiple machine learning algorithms that work together" (specifics ND; I read only Swiggy's summary of the abstract, not the paper).
- **Target variable:** For the batching paper: delivery time estimates for batched orders (from the abstract). For the optimisation: minimise CPD plus a delay-based CX cost.
- **Features:** ND.
- **Validation approach:** ND.
- **Metrics:** CPD, delay vs promise, DE wait time at store, batching percentage (named, values ND).

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Construction heuristic plus metaheuristic (DPDPTW) | Batching and sequencing |
| Multi-objective assignment optimisation | DE-to-batch matching each cron |
| Prediction serving at scale (Akka customer story, vendor marketing) | The Akka page says Swiggy's order-assignment flow scores candidate order-DE pairs and returns a decision "within one minute"; P99 prediction latency fell from 144ms to 71ms; 5,000+ predictions per second on a single model. Treat as vendor claim |

### 8. Business Decision
Adopt two-stage rolling-horizon batching plus JIT assignment with external and internal JIT; apply batching where promise slack exists; defer pickups to improve batch formation.

### 9. Business Impact
Instamart posts: ND (no figures). The 2022 ML batching paper summary: "an increase in the number of times the food is delivered within the estimated delivery times by about 6%" (Swiggy's post quoting its authors' abstract; company claim). 2019 post: "batching all orders will double the capacity of the entire delivery fleet" (a theoretical upper-bound statement, not a measured result).

### 10. What a Data Scientist Can Learn *(interpretation)*
- Dispatch is "predict then optimise": prediction errors (prep time, first mile, rider-free time) flow into constraint violations, so prediction quality matters as much as the solver.
- Decomposing an intractable joint problem into sequential stages is a standard, defensible choice under a hard latency budget.
- Local greedy (nearest rider) versus global optimisation is the key conceptual contrast to articulate.

### 11. Source Links
- https://bytes.swiggy.com/assignment-routing-optimization-for-swiggy-instamart-delivery-part-i-2e8fb3115463 — Part I, Sep 15, 2022 (archive snapshot)
- https://bytes.swiggy.com/assignment-routing-optimization-for-swiggy-instamart-delivery-part-ii-844341bd6f00 — Part II, Sep 20, 2022 (archive snapshot)
- https://bytes.swiggy.com/the-swiggy-delivery-challenge-part-two-f095930816e3 — May 8, 2019 (archive snapshot)
- https://bytes.swiggy.com/paper-on-ml-based-batching-prediction-published-ba3f16d060c1 — Feb 23, 2022 (archive snapshot); the paper link given there (https://dl.acm.org/doi/pdf/10.1145/3430984.3430999) was not fetched
- https://akka.io/customer-stories/swiggy — Akka customer story (vendor marketing; fetched, undated)

---

## Case Study 5 — Myntra (Flipkart group) customer promise date: predicting delivery dates with breach control

**Priority:** ★★ Good to have — Delivery promise with breach control: quantile regression and coverage guarantees. **Notebook:** `cs05_delivery_promise_date.ipynb` (⏳ notebook pending)

**Company:** Myntra, an Indian fashion e-commerce company (substituted for Flipkart and Amazon India: I found no Flipkart or Amazon India primary technical source on delivery promise; the paper's own text says "Myntra" and lists "Myntra Designs, India". That Myntra belongs to the Flipkart group is my background knowledge, not stated on the pages I read)
**Industry:** E-commerce (fashion)
**Business Area:** Delivery promise / estimated delivery date at order placement; supply-chain operations monitoring
**Problem Type:** Supervised regression with asymmetric cost (quantile regression), time-series comparison
**Evidence Level:** Strong (C: workshop paper by Myntra authors, SDM Data Science for Retail and E-Commerce Workshop 2021; it states the solution "is deployed and operational for Myntra"); business impact beyond model accuracy is ND
**Primary Sources:** Preethi V, Nachiappan Sundaram, Ravindra Babu Tallamraju, "Online Fashion Commerce: Modelling Customer Promise Date", arXiv:2105.00315 (May 1, 2021)

### 1. Business Problem
The paper states that predicting a date later than the actual delivery date "might sometimes result in the customer not placing the order (lost sales)" while promising earlier than actual delivery "would lead to a bad customer experience and consequent customer churn". It cites Indian constraints (limited infrastructure in remote areas, traffic, weather, variable holidays), low SKU depth in fashion so a small number of warehouses serve demand, hard-to-decipher addresses, and high revenue days (HRD) when variability is higher and cutoffs are not adhered to. A pre-existing rule-based model used configured static processing times per leg.

### 2. Business Question
At order placement, how can the delivery date be promised so that on-time or early delivery is as high as possible while breaches (delivery after the promised date) stay below a business-set limit?

### 3. Data Available
| Data | Description (as stated) |
|---|---|
| Training set | Deliveries from the last few weeks before the prediction date, "more than a million training examples"; tested on orders placed the subsequent day |
| Supply-chain legs | Vendor procurement (items not in warehouse), warehouse processing (pick, consolidate, pack), linehaul hops through hubs, last-mile centre |
| Operational features | Pendency (recent inflow/outflow) at linehaul and last-mile, per-lane and per-last-mile-centre performance, manpower, holiday and weekday types, regional holiday calendars (including 3PL partners), geography of the customer address, planned volume and capacity on HRD |
| 3PL | Courier-partner shipments (limited visibility of their network) |

### 4. Data Science Approach
Promise date = order time + (warehouse model, or vendor-procurement model for items not in the warehouse) + shipping-time model. Warehouse leg: fbprophet time series (separate for single-item and multi-item orders) and a LightGBM variant. Shipping leg (Myntra logistics and 3PL): LightGBM with categorical lane and centre features, decay-weighted training examples, tuned parameters (final: 1000 boosting iterations, 15 leaves, 0.6 data and feature fraction), and holiday and weekend handling per last-mile centre. HRD: LightGBM trained on proxy days from a prior sale event with planned volume/capacity inputs. Breach control compared three ways: (1) asymmetric loss functions, (2) quantile regression, (3) a feedback-based breach control model that corrects LightGBM using recent prediction errors. fbprophet and LSTM (7 LSTM blocks, 300 epochs, batch size 100) were also compared, including a short lane (Delhi-Gurugram) vs a long lane (Delhi-Kolkata). Operational use: deviation of on-ground processing time from the predicted time is used to flag pendencies early.

### 5. Statistical Analysis
Documented: asymmetric loss and quantile regression (quantile loss as asymmetrically weighted absolute residuals) to hit a target breach percentile rather than the mean; time-series decomposition (trend, seasonality, holiday: fbprophet equation y(t) = g(t) + s(t) + h(t) + error); a validation set chosen to resemble the test set by order day; decayed example weights for recency.

### 6. Machine Learning
- **Models:** LightGBM (asymmetric loss; quantile regression; with breach-control model), XGBoost, random forest, fbprophet, LSTM; rule-based baseline.
- **Target variable:** Processing/shipping time per leg (order placement to shipping for warehouse/vendor legs, shipping time for the shipping leg); final output is the delivery date.
- **Features:** see section 3 (pendency, lane, holiday, weekday, geography, planned volume).
- **Validation approach:** train on prior weeks, test on the next order day; results averaged over one week in September for business-as-usual (BAU) days and over HRD/post-HRD days in December.
- **Metrics:** Accuracy(0 to -1) = % of packets delivered on the promised date or one day earlier (Accuracy(0 to -2) for HRD); Breach = % delivered after the promised date; measured at order-day level.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| LightGBM (GOSS, exclusive feature bundling) | Main shipping, vendor and HRD models |
| fbprophet | Warehouse processing and shipping time series |
| LSTM, XGBoost, random forest | Comparison models |
| Quantile regression | Breach control |

### 8. Business Decision
Replace the rule-based model with the LightGBM quantile-regression promise model for shipping time (fbprophet for the warehouse leg), use dedicated HRD models during sale events, and use predicted-versus-actual to flag pendencies.

### 9. Business Impact
From the paper's tables (authors' own results; absolute levels depend on their metric). BAU days, all lanes: LightGBM quantile regression Accuracy 68.10%, Breach 4.68%; rule-based baseline 36.56% / 5.63%; LightGBM asymmetric loss 61.54% / 5.50%; LightGBM with breach control 58.30% / 3.90%; fbprophet 40.30% / 2.74%. HRD: LightGBM 65.15% / 7.86% vs rule-based 44.23% / 5.44%; post-HRD: 74.58% / 4.82% vs 54.48% / 3.06%. The authors say quantile regression "almost doubl[ed] the accuracy achieved using the baseline model, while also reducing the breaches", and that the best LightGBM gave "more than 20 percentage points" over baseline for HRD and post-HRD days (note: in the paper's table the HRD and post-HRD breach rates are higher than the baseline's). Lane example: Delhi-Gurugram, all models 83.55% accuracy; Delhi-Kolkata, time series 50.34%, LSTM 70.65%, LightGBM 75.26%. LightGBM training was "8x times faster" than XGBoost. Revenue, conversion or return impact: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- A promise date is a quantile, not a mean: the business objective (keep breaches under X%) points to quantile regression rather than tuning a penalty on MSE; the paper itself found the asymmetric-loss route could not deterministically control breaches.
- Report both a hit rate and a breach rate; accuracy gains can come with different breach behaviour (visible on HRD).
- Event days (sales) are rare, so models must borrow from proxy days.
- Different legs deserve different model families; time series did well on short lanes but not on long ones.

### 11. Source Links
- https://arxiv.org/abs/2105.00315 — "Online Fashion Commerce: Modelling Customer Promise Date", May 1, 2021 (PDF read at https://arxiv.org/pdf/2105.00315; arXiv metadata lists SDM Data Science for Retail and E-Commerce Workshop 2021)

---

## Case Study 6 — Swiggy q-commerce address correction: location inaccuracy classifier and geocoder

**Priority:** ★ Optional — Address and geocoding quality: classification with clustering; narrower use. **Notebook:** `cs06_address_quality_geocoding.ipynb` (⏳ notebook pending)

**Company:** Swiggy (Instamart / food delivery)
**Industry:** Quick commerce / hyperlocal delivery
**Business Area:** Address and location quality, geocoding, rider routing accuracy
**Problem Type:** Self-supervised text-plus-numeric classification; geocoding/retrieval; certification against a clustering baseline
**Evidence Level:** Strong (A: two-part post by named Swiggy data scientists, which cites a 2022 AI-ML Systems conference paper by Swiggy authors)
**Primary Sources:** Swiggy Bytes "Address Correction for Q-Commerce Part 1: Location Inaccuracy Classifier" and "Part 2: Geocoder" (both dated May 27, 2024 on the archived pages I read)

### 1. Business Problem
Customer locations are captured by phone GPS, which can be inaccurate. Part 1 says inaccurate locations affect customers and delivery partners (DPs): promised delivery times "may be compromised due to the inability of the DP to locate the customer", DPs call support or the customer, and raise payout-correction tickets when they travel farther than the automated distance prediction implied. Part 2 stresses that q-commerce differs from e-commerce geocoding because the customer's location is already available, so it should be corrected only when inaccurate, and with accuracy "within tens of meters".

### 2. Business Question
Which addresses have a captured location that disagrees with the address text, and for those, what is the correct geocode, accurate enough to route delivery partners, without manually labelled data?

### 3. Data Available
| Data | Description (as stated) |
|---|---|
| Captured location + address text | Customer-entered address line plus reverse geocode of the captured location |
| Historical delivery locations | Locations marked by DPs at delivery; the median is used to generate negative (accurate) examples |
| DP and care signals per address | Fraction of orders with Incorrect Address (ICA) flagged; fraction with DP-to-customer call (DP2Cr); average DP2Cr call duration; fraction with tickets for travelling longer distance (TLD); fraction of cancellations citing incorrectly selected address (ISA); counts of delivered and cancelled orders |
| Geo indexes | Geohash level 8 for the classifier; H3 cells at resolutions 8 and 11 for the geocoder |

### 4. Data Science Approach
Architecture: pre-filter (skip addresses where the median delivery location is within a set distance of the captured location), then location inaccuracy classifier, then geocoder, then post-processor. Classifier: binary, self-supervised. Earlier work trained RoBERTa on perturbation data (Gaussian noise added to accurate locations) and address-swapped data (swapping distant addresses); the union (Boolean OR) model had the best F1. New work: a multimodal model combining RoBERTa address embedding, L8 geohash and numeric DP/care signals; two variants (concatenated vs weighted), trained in three phases (MLM, fine-tune on perturbation data, then FC layers only or end-to-end); the best is the Concat model fine-tuned end-to-end, flagging inaccuracy when softmax confidence exceeds 0.5.

Geocoder: three architectures compared. (1) Seq2Seq (RoBERTa encoder, LSTM decoder predicting the last five characters of an L8 geohash; first three copied from the captured location). (2) Unsupervised Address Matching (UAM): coarse retrieval in the H8 cell, fine retrieval of the best H11 cell by median fuzzy-match score (Jaro-Winkler plus token set plus token sort ratios). (3) Self-Supervised Address Matching (SAM): RoBERTa-Triplet embedding nearest neighbour within the H8 cell. Raw geocodes were not production-grade; a post-processor tags a geocode "usable" if it is within a certain distance of all historical delivery locations of that address. Benchmark: DBSCAN over historical delivery locations (parameters garbled in my copy: min points 4 and an epsilon of 20, unit not legible, presumably metres). The final system is a union of usable predictions prioritised Seq2Seq, then SAM, then UAM.

### 5. Statistical Analysis
Documented: evaluation on an imbalanced held-out set, with the imbalance factor "of the order of a few tens" estimated from manual validation of "a few thousand orders"; ROC-AUC, precision, recall, F1; delivery deviation (Haversine distance from predicted location to delivery location) with mean, median and 95th percentile; the post argues absolute percentile thresholds are misleading and compares with DBSCAN instead; relative delivery deviation (RDD) and relative delivery precision (RDP, fraction of addresses where the prediction is closer to the delivery point than the captured location). Significance tests: ND.

### 6. Machine Learning
- **Models:** RoBERTa-based multimodal classifier; Seq2Seq (RoBERTa + LSTM); UAM (fuzzy matching); SAM (RoBERTa triplet embeddings); DBSCAN baseline.
- **Target variable:** Classifier: location inaccurate (1) or accurate (0), with labels synthesised self-supervised. Geocoder: L8 geohash suffix, or the geocode of the matched address.
- **Features:** L8 geohash of the captured location, address text (plus reverse geocode), numeric DP/care signals.
- **Validation approach:** held-out imbalanced set; geocoder experiments on 3 large South Indian cities; production pan-India with four Seq2Seq models (South, Central, North, East).
- **Metrics:** AUC-ROC, precision, recall, F1; DD, RDD, RDP, order coverage, median successful deliveries needed per prediction.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| RoBERTa (MLM pre-training, fine-tuning) | Address text encoding |
| LSTM decoder | Seq2Seq geohash prediction |
| Geohash (L8) and Uber H3 (res. 8 and 11) | Spatial indexing |
| fuzzywuzzy | Fuzzy string similarity in UAM |
| DBSCAN | Baseline and certification benchmark |

### 8. Business Decision
Deploy the Seq2Seq geocoder pan-India (four regional models) to route DPs to the predicted location when the classifier flags the captured location as inaccurate; use the inaccuracy flag standalone to nudge customers to correct addresses; use a union of geocoder models rather than one.

### 9. Business Impact
Company claims from the posts: the multimodal classifier "achieves an AUC-ROC of 0.89" and "improved precision and recall by 23 pp and 32 pp respectively over the baseline model"; the Union geocoder "achieves a 139 pp improvement in order coverage over the DBSCAN model"; DBSCAN needed a median number of successful deliveries 1.25, 2.5 and 2.5 times larger than Seq2Seq, UAM and SAM respectively; maximum correction distances 8.8 km (Seq2Seq), 942 m (UAM), 956 m (SAM); H8 cell edge 531 m; in production "The DD decreased by an average distance of 143" (unit symbol garbled in my copy; metres by context) "on the corrected addresses". Effects on delivery time, cost or ticket volume: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Labels can be manufactured from operational byproducts (delivery pins, support calls) when manual labelling is impossible, but their noise should be acknowledged.
- When no ground truth exists for the target, benchmark against a trusted simple baseline (DBSCAN on delivery points) instead of inventing an absolute accuracy threshold.
- Spatial indexes (geohash, H3) turn geocoding into retrieval and classification problems.
- "Only correct if confident" interventions favour precision; the post-processor encodes that.

### 11. Source Links
- https://bytes.swiggy.com/address-correction-for-q-commerce-part-1-location-inaccuracy-classifier-e72b88a33d2f — Part 1, May 27, 2024 (archive snapshot)
- https://bytes.swiggy.com/address-correction-for-q-commerce-part-2-geocoder-3bbd6ee828c0 — Part 2, dated May 27, 2024 on the archived page (archive snapshot)

---

---

# PART B — DEMAND, PRICING & SUPPLY CHAIN

## Case Study 7 — Instamart quick-commerce demand forecasting: availability de-biasing, SKU grouping and TimesFM

**Priority:** ★★★ Must-visit — Demand forecasting under stock-outs (censored sales): asked in every supply-chain interview. **Notebook:** `cs07_quickcommerce_demand_forecasting.ipynb` (✅ notebook built)

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

## Case Study 8 — Marketplace price monitoring / discount efficacy on Flipkart (substitution: only an external analysis is public)

**Priority:** ★★ Good to have — Price elasticity and discount efficacy; interview staple but little public company method. **Notebook:** `cs08_price_elasticity_discounts.ipynb` (⏳ notebook pending)

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

## Case Study 9 — Delivery-fee / surge design in food delivery (Weak; only problem framing and a simulated academic study)

**Priority:** ★★ Good to have — Surge and fee design; marketplace economics, little public company method. **Notebook:** `cs09_delivery_fee_surge_pricing.ipynb` (⏳ notebook pending)

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

## Case Study 10 — Sale-event (Big Billion Days) planning at Flipkart (Weak: outcomes published, methods not)

**Priority:** ★ Optional — Sale-event capacity planning; methods undisclosed, seasonal and peak forecasting. **Notebook:** `cs10_sale_event_capacity_planning.ipynb` (⏳ notebook pending)

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

## Case Study 11 — Myntra: forecasting demand for new fashion items to guide assortment and buying

**Priority:** ★★★ Must-visit — Cold-start demand forecasting for new items (fashion); strongly documented. **Notebook:** `cs11_new_item_demand_forecasting.ipynb` (⏳ notebook pending)

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

## Case Study 12 — Hierarchical probabilistic forecasting for supply chain: Amazon Forecasting Science (CLOVER), with Flipkart CPP context

**Priority:** ★★ Good to have — Hierarchical, probabilistic forecasting; advanced but increasingly standard. **Notebook:** `cs12_hierarchical_probabilistic_forecasting.ipynb` (⏳ notebook pending)

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

---

# PART C — SEARCH, RECOMMENDATIONS & ADS

## Case Study 13 — Hinglish Search Query Translation at Flipkart

**Priority:** ★★ Good to have — Query understanding for Hinglish; NLP evaluation in search. **Notebook:** `cs13_hinglish_search_queries.ipynb` (⏳ notebook pending)

**Company:** Flipkart
**Industry:** Ecommerce (marketplace)
**Business Area:** Search / query understanding
**Problem Type:** Code-mixed (Hinglish) query translation, language identification, relevance
**Evidence Level:** Medium. Category C (arXiv paper by Flipkart team: Kulkarni, Chennabasavaraj, Garera) with real method detail, but business impact is not quantified.
**Primary Sources:** arXiv 2208.03713 "Study of Encoder-Decoder Architectures for Code-Mix Search Query Translation" (7 Aug 2022).

### 1. Business Problem
The paper states that about 21% of Flipkart's queries are Hinglish (Hindi words typed in Latin script). Translating them to English lets the existing English search stack handle them. Stated difficulties: no parallel training data, spelling errors, brand misspellings, ambiguous language identification, non-standard query format, and "articulation gap" queries (example given: "juta bina dori wala" for "shoe without lace").

### 2. Business Question
How can a Hinglish query be reliably translated to English, at production latency, so that existing English-language retrieval and ranking serve it well?

### 3. Data Available
| Data | Description |
|---|---|
| Pseudo-labelled corpus | About 5M unlabeled Hindi/Hinglish queries, labelled using third-party translation and transliteration APIs (an earlier pilot used 200k queries) |
| In-house tagged Hinglish set | About 70k queries (under 1.5% of labelled set); stage-2 fine-tuning used 55k (10% validation), 15k test |
| Initial test set | 15k manually tagged Hinglish queries, balanced across Head, Torso, Tail |
| Language-detection set | 80k queries tagged per word, 20k held out for test |
| In-house alternative data (Sec 8.2) | Generic English-Hindi translation model on about 1.4M pairs translated about 18M English queries; transliteration model trained on 96.4k word pairs |

### 4. Data Science Approach
Documented: (a) a per-word language-identification step to detect Hinglish; (b) a sequence-to-sequence translation model trained in two stages (stage 1 on the 5M pseudo-labelled corpus for 5 epochs; stage 2 on in-house human labels until validation loss stopped improving); (c) data augmentation (Masking, AutoEncoder, DropChar dropping a character from 30-50% of words, WordOrderPermute); (d) knowledge distillation to a single-layer quantized student to meet latency. Loss was a weighted mix of supervised and augmentation cross-entropy (lambda = 0.5).

### 5. Statistical Analysis
No hypothesis testing documented. The paper compares models on BLEU and per-class precision/recall; A/B testing is mentioned without numbers. Test sets were stratified Head/Torso/Tail.

### 6. Machine Learning
- **Models:** T5-base (about 222M params), BART-base (about 139M, chosen), Bert2Bert, mT5-small and mBART-large-50 as multilingual comparisons; distilled 1-layer BART student. Language ID: CRF, FastText, CNN, LSTM.
- **Target variable:** English translation of the Hinglish query (seq2seq); language label per word for detection.
- **Features:** Raw query text (subword tokens). ND beyond that.
- **Validation approach:** Held-out tagged test sets (15k Head/Torso/Tail balanced); 10% validation split in stage 2; online A/B test (no figures).
- **Metrics:** SacreBLEU. Hinglish test set: Azure Translate 25.5, Google Translate 35.8, BART random init 49.9, BART no augmentation 50.3, BART with augmentation 51.3, mT5 48.3, mBART 46.6. Augmentation: AutoEncoder +1.37 (BART), WordOrderPermute -3.1 (BART). Language ID precision/recall/F1: CRF 0.84/0.72/0.76 (best), FastText 0.90/0.61/0.73, CNN 0.80/0.65/0.72, LSTM 0.82/0.63/0.71; the paper notes CRF recall rose from 28% (keyword baseline) to 72%. Distillation: teacher BLEU 51.3, p95 about 200 ms; quantized student with Jensen-Shannon KD loss BLEU 50.8, about 47 ms; with cross-entropy KD loss BLEU 49.7.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| T5 / BART / BERT checkpoints | Seq2seq models |
| AdamW, label smoothing 0.1, beam size 3 | Training and decoding |
| A100 GPU | Training |
| SacreBLEU | Evaluation |
| FastText, CRF | Language identification |
| Weight quantization on CPU, C libraries | Latency reduction in production |
| Azure / Google translation APIs | Pseudo-labelling only |

### 8. Business Decision
Documented: the model is live on the Flipkart app and website for millions of queries, and A/B testing was used to validate it. The choice of the distilled student over the teacher for latency is documented.

### 9. Business Impact
"Live on Flipkart" and "A/B testing was used" are the company authors' own claims. No quantified business metric (conversion, revenue, search success) is given: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
Without labels, bootstrap with noisy third-party labels at scale, then correct with a small high-quality human set (two-stage training). Evaluate by Head/Torso/Tail strata. Latency is a first-class constraint: a 0.5 BLEU drop for roughly 4x speed was accepted. Google/Azure scored far below the in-domain model, which illustrates how domain-specific the noise is.

### 11. Source Links
- arXiv 2208.03713, "Study of Encoder-Decoder Architectures for Code-Mix Search Query Translation", 2022-08-07: https://arxiv.org/abs/2208.03713 (content read via https://ar5iv.labs.arxiv.org/html/2208.03713; listing via arXiv API)

---

## Case Study 14 — ShopLook: Recommending Similar Products for Every Garment in a Model Image at Myntra

**Priority:** ★★ Good to have — Visual similar-item retrieval with A/B-validated lift. **Notebook:** `cs14_visual_similarity_recommendations.ipynb` (⏳ notebook pending)

**Company:** Myntra (Flipkart group)
**Industry:** Fashion ecommerce
**Business Area:** Recommendations / visual similarity ("shop the look")
**Problem Type:** Computer-vision retrieval, cross-sell
**Evidence Level:** Strong. Category C (Myntra Designs authors; accepted at IEEE MIPR 2021), with a stated A/B result.
**Primary Sources:** Ravi, Repakula, Dutta, Parmar, "Buy Me That Look: An Approach for Recommending Similar Fashion Products", arXiv 2008.11638 (26 Aug 2020, revised 6 Apr 2021).

Note: Pinterest's "Complete the Look" (CVPR 2019) surfaced in search but was not fetched and is not used as a source. ShopLook is similar-item retrieval for each worn garment, not complementary-item recommendation.

### 1. Business Problem
Product pages show a model wearing a full outfit; shoppers who search for one item may want similar items for every garment worn. The authors state this supports cross-selling and customer engagement.

### 2. Business Question
Given a full-shot catalog image, can we automatically detect each garment worn and recommend visually similar catalog products for each?

### 3. Data Available
| Data | Description |
|---|---|
| Myntra catalog images | Roughly 7-9k training and about 800 test images per article type; about 150k training images total |
| Street2Shop (Kiapour et al.) | Street photos paired with catalog images, used for hard anchor-positive pairs |
| In-house tagger labels | Active-learning loop: taggers flag misclassifications for retraining |

### 4. Data Science Approach
Four-stage pipeline: (1) full-shot detection via human keypoints (head and ankle present) plus a pose classifier (front/back/left/right/detailed); (2) article localisation with Mask R-CNN for about 20 apparel types, with active learning; (3) a triplet-network embedding per detected article; (4) cosine-similarity retrieval against the catalog.

### 5. Statistical Analysis
Online A/B test reported; the paper gives no duration, sample size or significance for it. Expert review: 477 of 500 sampled recommendations judged visually relevant (about 95%).

### 6. Machine Learning
- **Models:** keypoint model (Xiao et al., ResNet-based); ResNet18 pose classifier; Mask R-CNN (ResNet-101-FPN); triplet network with shared-weight ResNet50 branches (best backbone), weighted triplet loss.
- **Target variable:** Pose class; article class and mask; embedding trained so same-article images are closer than different ones (triplet).
- **Features:** Raw images.
- **Validation approach:** Per-article held-out test images; retrieval baselines EUC, CE, SIFT; expert relevance review of 500 samples; online A/B.
- **Metrics:** Mask R-CNN average mAP 78% (up to 92% for some top-wear classes). Active learning AP (before to after): topwear 82.65 to 87.60, bottomwear 87.11 to 90.25, skirts 51.42 to 69.09, footwear 87.32 to 88.47, bags 69.71 to 78.37. Retrieval: P@3 28.4, R@3 15.5, P@5 24.6, R@5 26.1, P@10 15.8, R@10 37.6, beating the baselines at every K. Triplet: margin 0.2, embedding size 2048, ADAM lr 5e-5, batch 32, semi-hard mining. Inference per image (V100): pose about 200 ms, detection about 400 ms, embedding about 100 ms, retrieval about 5 ms.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Mask R-CNN, ResNet18/50/101 | Detection, classification, embeddings |
| ADAM optimizer | Triplet training |
| Tesla V100 GPUs | Training and timing |
| Serving stack | ND (not named in the paper) |

### 8. Business Decision
Documented: evaluated at Myntra and tested online; also noted to work on user-uploaded fashion images. Rollout scale: ND.

### 9. Business Impact
Authors' own claim from an online A/B test: click-through rate up 25%, add-to-cart ratio up 4%, and longer sessions (paraphrased by the fetch tool; exact paper wording not verified). No duration or significance given.

### 10. What a Data Scientist Can Learn *(interpretation)*
Decompose a complex visual task into stages, each with its own metric. Use active learning to improve weak classes (skirts, bags). Triplet loss with semi-hard mining is the standard metric-learning answer. Precision@K looks low (28.4 at K=3) yet expert-judged relevance was about 95%, a reminder that offline label-matching metrics understate perceived relevance.

### 11. Source Links
- arXiv 2008.11638 abstract page: https://arxiv.org/abs/2008.11638 (fetched)
- Full text via ar5iv: https://ar5iv.labs.arxiv.org/html/2008.11638 (fetched)
- Related, from arXiv listing only (not read in full): arXiv 1806.11371 "Personalizing Similar Product Recommendations in Fashion E-commerce" (Myntra, 2018-06-29).

---

## Case Study 15 — Item-to-Item Collaborative Filtering at Amazon.com

**Priority:** ★★★ Must-visit — Item-to-item CF: the foundational recommender, asked in almost every ecommerce interview. **Notebook:** `cs15_item_to_item_collaborative_filtering.ipynb` (✅ notebook built)

**Company:** Amazon.com (global; the template used across Indian ecommerce)
**Industry:** Ecommerce
**Business Area:** Recommendations
**Problem Type:** Collaborative filtering at scale
**Evidence Level:** Strong. Category A/C: published by Amazon employees (Linden, Smith, York), IEEE Internet Computing, Jan/Feb 2003.
**Primary Sources:** Linden, Smith, York, "Amazon.com Recommendations: Item-to-Item Collaborative Filtering" (hosted copy at cs.umd.edu).

### 1. Business Problem
Amazon needed real-time personalised recommendations over a very large catalog and customer base. The paper states Amazon had more than 29 million customers and several million catalog items, and notes prior algorithms were typically tested on much smaller datasets such as MovieLens (35,000 customers, 3,000 items).

### 2. Business Question
How can recommendations be generated in real time, with good quality even when a customer has little history, at a scale where classic user-based CF breaks?

### 3. Data Available
| Data | Description |
|---|---|
| Purchase/rating histories | Customer-item vectors, very sparse (most customers buy few items) |
| Catalog | Several million items |

### 4. Data Science Approach
Documented steps: (1) offline, build a similar-items table by finding items that customers tend to buy together (loop over items, then customers who bought each, then other items they bought); (2) similarity per item pair, typically cosine similarity over the customers who bought each; (3) online, for each item the user bought or rated, look up similar items, aggregate, and recommend the most popular or correlated. The paper contrasts three alternatives: traditional CF (compares a user to many customers; sampling or dimensionality reduction hurts quality), cluster models (cheap online but lower quality), and search/content-based methods (too general or too narrow).

### 5. Statistical Analysis
Cosine similarity between item vectors. Complexity analysis: offline table worst case O(N^2 M) but closer to O(NM) in practice; sampling buyers of best-sellers reduces cost further; online lookup depends only on the number of items the user has purchased or rated. Traditional CF: worst case O(MN), about O(M+N) with sparse data, with "severe performance and scaling issues" at 10M+ customers and 1M+ items (per the fetched summary).

### 6. Machine Learning
- **Models:** Item-to-item neighbourhood CF (memory-based, no trained parameters).
- **Target variable:** None (unsupervised similarity).
- **Features:** Co-purchase / co-rating vectors.
- **Validation approach:** ND (no offline metric tables appeared in the fetched summary; the paper is qualitative on quality).
- **Metrics:** ND.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Offline batch computation | Similar-items table build |
| Online lookup | Real-time recommendation |
| Specific software | ND |

### 8. Business Decision
Adopt item-to-item CF in production: expensive computation offline, cheap real-time lookup online, which the authors identify as the key to scalability. They state it works "based on as few as two or three items" (per the fetched summary).

### 9. Business Impact
No revenue or conversion figures in the fetched content: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
Move cost from the online path to the offline path. Item similarity is more stable than user similarity, so the table can be precomputed. Know the tradeoffs versus matrix factorisation and the known weaknesses (popularity bias, cold-start for new items, limited personalisation beyond history).

### 11. Source Links
- Linden, Smith, York, "Amazon.com Recommendations: Item-to-Item Collaborative Filtering", IEEE Internet Computing, 2003: https://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf (read through a text-extraction proxy)

---

## Case Study 16 — Dish Search and Query Understanding at Swiggy

**Priority:** ★★ Good to have — Search relevance and ranking metrics (NDCG, MRR) in food delivery. **Notebook:** `cs16_dish_search_ranking.ipynb` (⏳ notebook pending)

**Company:** Swiggy (substituted from "Swiggy/Zomato": Swiggy is far better documented)
**Industry:** Food delivery
**Business Area:** Search, dish ranking, discovery
**Problem Type:** Query understanding (misspellings, transliteration), semantic retrieval, learning-to-rank
**Evidence Level:** Strong. Category A/C: Swiggy Bytes posts by named engineers; the 2024 post is a CODS-COMAD 2024 conference paper.
**Primary Sources:** Swiggy Bytes: "Find My Food" (2021-03-27), "Using Deep Learning for Ranking in Dish Search" (2021-07-20), "Improving search relevance in hyperlocal food delivery using (small) language models" (2024-03-13); Swiggy blog on neural search (2023-07-20).

### 1. Business Problem
Search is the main entry point for high-intent customers. The posts state that Indian dish names have no standard English spelling (biryani typed as 'biriyani', 'biriani', 'beriani', 'briyani' and others), text matching can return no results, and some searched dishes are unavailable locally so nothing similar is shown. Later posts add complex multi-intent queries (dish, diet, mood, time slot).

### 2. Business Question
How do we retrieve and rank dishes that match customer intent despite misspellings, regional names, vague queries and hyperlocal availability?

### 3. Data Available
| Data | Description |
|---|---|
| Search logs | About 2M <query, ordered_dish> tuples over 2 months for embedding training; 35,000 <query, clicked_dish> pairs for validation V1 (26,000 pairs for misspelled V2) |
| Click-through logs | Ranking: one month of training data, validation on a week from a much later period |
| Food Taxonomy | In-house; 300+ dish families and 6 dish categories |
| Historical orders | 996,000 documents (query + bought item + taxonomy metadata) for stage-1 fine-tuning in the 2024 post |
| Curated pairs | More than 300,000 query-item pairs, manually verified, LLM-augmented |
| Test set (2024) | 5000+ samples across 5 international cuisines, 15 Indian regional cuisines, 10+ dietary preferences |

### 4. Data Science Approach
Documented evolution: (1) 2021 embedding model: Siamese network with custom trigram tokenizer, embeddings of queries and dishes, used as a feature in an LTR model for re-ranking; a word-piece transformer variant was rejected because misspellings break tokenization and it was slow; (2) 2021 ranking: retrieval cuts "millions of dishes to hundreds", then a modular deep model scores semantic, restaurant, popularity and distance-time inputs, combined by a bias-free linear layer; (3) 2024: two-stage fine-tuned small language model for embedding-based retrieval of complex queries; (4) 2023 blog: LLM-based neural search planned (pilot "by September" 2023).

### 5. Statistical Analysis
Davies-Bouldin index to test whether embeddings cluster dishes by dish family (10 head families, 250 dishes each); proportion of top-10 results sharing the searched dish's category (2,000 historical queries that returned empty results). Synthetic misspelling set (V2) built from a curated spelling-variation dictionary.

### 6. Machine Learning
- **Models:** Siamese FCN with trigram tokenization (triplet loss, margin 0.4); Siamese Transformer (4 layers x 8 heads, rejected); baselines Word2Vec and FastText (64-d, skip-gram); ranking model inspired by Google's "Neural Ranking Model with Multiple Document Fields"; all-mpnet-base-v2 and all-MiniLM-L6-v2 fine-tuned and compared to BM25.
- **Target variable:** Ranking: clicked dish > shown-but-not-clicked dish > random dish (margin ranking loss, margins chosen experimentally). Embeddings: ordered dish is positive for the query; negatives sampled to be semantically related.
- **Features:** Query, dish name and dish family (trigram embeddings); restaurant embedding, cuisine embeddings, rating, preparation time, cost for two, SLA; normalized daily and monthly orders of dish and restaurant and query-restaurant interactions; last-mile distance, max delivery time (with squared and root transforms).
- **Validation approach:** Time split for ranking (1 month train, 1 later week validate); V1/V2 validation sets; manually relevance-tagged test set for the 2024 retrieval work.
- **Metrics:** MRR, Recall@100 (embeddings); MRR (ranking; result table was an image, values ND); MAP, Precision@1, Precision@5 (2024; values in images, ND). Documented figures: Siamese FCN-T (triplet) improves over the FastText baseline by 3% (MRR) and 4.49% (Recall@100) on V1, and by 93% and 25% on misspelled V2; 3X faster training and over 6X faster inference than the transformer; Word2Vec could not embed about 32% of available dishes in the test city.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| ElasticSearch | Existing fuzzy text retrieval backend |
| TensorFlow (Tensorflow estimator) | Embedding model training and serving |
| Learning-to-rank model | Consumes the cosine-similarity feature (described as one of its top features) |
| HuggingFace sentence-transformer models | 2024 retrieval; CPU instances with a 100 ms query-embedding latency budget |

### 8. Business Decision
Documented: Siamese FCN-T embeddings deployed online to re-rank dish search (query embedding latency about 2 ms at p99); small-LM retrieval "currently in the experimental phase and is being tested with a small cohort" (2024).

### 9. Business Impact
Offline metrics only, as listed above. No online conversion/revenue lift published in the posts read: ND. Catalog size claim: "more than 50 million items" (Swiggy's own 2023 blog).

### 10. What a Data Scientist Can Learn *(interpretation)*
Three-level negatives (clicked > shown > random) are a practical way to use implicit feedback. Character n-gram tokenization is the principled fix for transliteration noise. Build synthetic hard test sets (V2) for the failure you care about. Choosing the model with 3X/6X cheaper train/infer over the best-semantic model is a typical production tradeoff. No online impact is published, so do not claim one.

### 11. Source Links
- "Using Deep Learning for Ranking in Dish Search", Swiggy Bytes, 2021-07-20: https://medium.com/swiggy-bytes/using-deep-learning-for-ranking-in-dish-search-4df2772dddce (fetched via proxy)
- "Find My Food: Semantic Embeddings for Food Search Using Siamese Networks", 2021-03-27: https://medium.com/swiggy-bytes/find-my-food-semantic-embeddings-for-food-search-using-siamese-networks-abb55be0b639 (fetched via proxy)
- "Improving search relevance in hyperlocal food delivery using (small) language models", 2024-03-13 (CODS-COMAD 2024, doi 10.1145/3632410.3632428): https://medium.com/swiggy-bytes/improving-search-relevance-in-hyperlocal-food-delivery-using-small-language-models-ecda2acc24e6 (fetched via proxy)
- Swiggy generative AI / neural search blog, 2023-07-20: https://blog.swiggy.com/?p=14845 (fetched)
- "Personalizing Swiggy POP Recommendations", 2020-03-03: https://medium.com/swiggy-bytes/personalizing-swiggy-pop-recommendations-d434b6f555f9 (retrieved but not analysed here)
- Fifth Elephant 2018 talk abstract (Nitin Hardeniya): https://hasgeek.com/fifthelephant/2018/sub/our-experiments-with-food-recommendations-swiggy-Va5Tmf45onrjBbVMAor7vB (abstract only; no results)

---

## Case Study 17 — Unified Ranking of Sponsored and Organic Products on Flipkart "Similar Products"

**Priority:** ★★★ Must-visit — Sponsored/organic ranking with CTR/CVR prediction and calibration: the revenue engine of marketplaces. **Notebook:** `cs17_ads_ranking_ctr_cvr.ipynb` (⏳ notebook pending)

**Company:** Flipkart
**Industry:** Ecommerce / retail media
**Business Area:** Ads ranking, recommendations
**Problem Type:** pCTR/pCVR modelling, ad/organic blending, calibration
**Evidence Level:** Strong. Category A: Flipkart Tech blog by a named data-science team (Amar Kumar et al.), 4 Nov 2025.
**Primary Sources:** "The Science of Unified Ranking: Integrating Ads and Organic Recommendations", Flipkart Tech.

### 1. Business Problem
Product-page widgets pinned sponsored items at fixed slots 2 and 5. The authors call this "safe, predictable, but ultimately sub-optimal" (for a new smartphone all five most relevant items might be sponsored; for pocket scissors, any ad hurts). Goal: let sponsored and organic items compete for slots under one objective.

### 2. Business Question
Can one model and one ranking function compare ads and organic products fairly and beat pinned slots on both organic orders and ad revenue?

### 3. Data Available
| Data | Description |
|---|---|
| Impression logs | Historical impressions from both organic and ads pipelines, combined; organic feedback is "multi-fold" larger than ads |
| Feature sets | Co-browse, co-impression "pair stats" (directional, e.g., impressions of P2 when P1 is viewed), popularity etc.; 27 key features identified for crossing |
| Candidate sources | Co-purchase, co-browse, attribute similarity |
| Ad bids/costs | Used in the sponsored score (exact formula ND) |

### 4. Data Science Approach
Funnel: candidate sourcing, a relevance-filtering stage (SGD classifier predicting probability of conversion given impression, pCVI, daily batch, cached), then a personalised online ranker (FTRL) with separate CTR and CVR models. Unification: single training set with an isAds flag plus 2-way and 3-way crosses of 27 features with isAds; separate organic and sponsored objective functions (organic is a weighted combination with tunable alpha and beta; sponsored adds bid cost components); weights chosen by offline simulation framed as multi-objective optimisation; circuit breaker reverting to pinned slots 2 and 5 if the organic ranker fails; parity pipelines for pair stats on ads plus TOTAL aggregate features.

### 5. Statistical Analysis
Online "high-mod AB test with cumulative exposures crossing 100M"; results reported as statistically significant (test type and confidence intervals: ND). Request AUC (within-request pairwise ordering) used offline.

### 6. Machine Learning
- **Models:** SGD classifier (log loss) for retrieval-stage pCVI; FTRL online logistic models for pCTR and pCVR.
- **Target variable:** Click given impression; conversion given click; conversion given impression.
- **Features:** isAds flag, isAds crosses, popularity, co-browse, co-impression pair stats, TOTAL aggregates; full list ND.
- **Validation approach:** Offline grid: baseline organic-only features vs isAds flag only vs full crosses, evaluated separately on organic-only and ads-only test sets; offline simulations over weights; online A/B.
- **Metrics:** AUC, Request AUC, NDCG, MAP, MRR; business: share of sponsored products, ad spend efficiency, organic orders, ad revenue. The offline lift chart is an image (values ND); the text says the lift was larger for ads with organic about unchanged.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| scikit-learn SGDClassifier | Batch relevance stage |
| FTRL (online learning) | Personalised CTR/CVR rankers |
| Daily batch jobs + cache | Retrieval stage scoring |
| Circuit breaker | Fallback to pinned ads |

### 8. Business Decision
Scaled to 100% of Flipkart traffic after the A/B test; launched for the "Similar Products" recommender.

### 9. Business Impact
Company's own claim: "a statistically significant (1.36%) increase in orders for organic products and a 3.4% increase in bottomline Ads revenue."

### 10. What a Data Scientist Can Learn *(interpretation)*
Calibration across populations with different base rates is the core difficulty in blending ads and organic. A flag plus crosses gives one model with separate effective weights. Design failure modes up front (the 0.5 default-score fallback could flood the page with ads). Report counter metrics (organic orders as well as ad revenue). The exact auction/pricing mechanism is not described, so do not attribute one.

### 11. Source Links
- "The Science of Unified Ranking: Integrating Ads and Organic Recommendations", Flipkart Tech, 2025-11-04: https://blog.flipkart.tech/the-science-of-unified-ranking-integrating-ads-and-organic-recommendations-8cc24113ef21 (fetched via proxy)
- Secondary summary used to locate it: https://daily.dev/posts/the-science-of-unified-ranking-integrating-ads-and-organic-recommendations-fecxacm1v

Gap: no public Flipkart/Meesho/Myntra source on auction mechanics (GSP/VCG, reserve prices) was found. Auction design for this case remains ND.

---

## Case Study 18 — Cold-Start Feeds for New Users at Meesho (with exploration evidence from Myntra)

**Priority:** ★★ Good to have — Cold start and bandit exploration for feeds. **Notebook:** `cs18_cold_start_exploration_bandits.ipynb` (⏳ notebook pending)

**Company:** Meesho (cold-start); Myntra (bandit exploration, substituted in because the Meesho post contains no exploration detail)
**Industry:** Value commerce / fashion ecommerce
**Business Area:** Feed ranking, new-user personalisation
**Problem Type:** Cold-start recommendation, contextual bandits
**Evidence Level:** Medium. Meesho: Category A (named senior data scientist, blog) but no numbers and no date; Myntra: Category C (arXiv paper by company team).
**Primary Sources:** Meesho blog "Personalization from Day One: Solving the Cold Start Problem at Meesho" (Vaishnav Chandak; publication date not stated); arXiv 2309.14046 "Diversify and Conquer: Bandits and Diversity for an Enhanced E-commerce Homepage Experience" (Jaiswal, Malayil, Jawaid, Vempati; 25 Sep 2023).

### 1. Business Problem
Meesho: "New users rarely give second chances." Irrelevant first-session feeds drove high bounce rates. Challenges: few early behavioural signals, and incorporating new in-app interactions in real time. Myntra: ranking heterogeneous homepage widgets per user, where widgets are added and removed over time (item cold-start), framed as a contextual bandit with delayed batch feedback.

### 2. Business Question
How can a useful feed be shown from the first session, and how can a ranker explore new items while exploiting what it knows?

### 3. Data Available
| Data | Description |
|---|---|
| Meesho demographics | Gender, location (X_demo) |
| Meesho early behaviour | Clicks, time on listings, scroll patterns; interaction sequences (X_seq) |
| Meesho user state | Login state, activity level, lifecycle stage (X_state) |
| Meesho item labels | sub_category, price_decile (auxiliary targets); dataset size: ND |
| Myntra | User-widget impressions and clicks; user vectors from browsing/cart/purchase (short and long ranges), SVD user and widget representations, widget metadata, time-of-day/week/year context, revenue features |

### 4. Data Science Approach
Meesho progression: (1) DemoRec: cohort popularity by demographics; (2) ESPM, Early Signal Personalization Model: demographics plus early behaviour predict purchase probability by category, feed built from top categories; (3) CWN, Cold-Warm Net: cold expert tower (demographics) and warm expert tower (sequences) blended by a gating network driven by user-state features, with dynamic knowledge distillation. Myntra: LinUCB and Linear Thompson Sampling produce relevance scores, then a Determinantal Point Process re-ranks for diversity.

### 5. Statistical Analysis
Meesho: backtests shown as charts only; no numbers or design details. Myntra: online A/B vs XGBoost, "high statistical significance" for the click lift (test details ND). Exploration: LinUCB exploration parameter alpha; LinTS posterior sampling; forgetting factor gamma in [0,1] for batch updates; DPP trade-off theta (range 0.6-0.8 reported as promising).

### 6. Machine Learning
- **Models:** Meesho: two-tower cold/warm experts with gating (CWN); prediction is sigmoid of cosine similarity of user and item embeddings; loss binary cross-entropy; a distillation loss is added only when the cold expert's loss exceeds the warm expert's; auxiliary sub_category and price_decile losses. Myntra: LinUCB, LinTS, XGBoost baseline, DPP re-ranker.
- **Target variable:** Meesho: user-item interaction (BCE; the exact label, e.g. click vs order, is not stated: ND). Myntra: widget click.
- **Features:** As in section 3. Item embeddings in Meesho come from a randomly initialised lookup table.
- **Validation approach:** Meesho: backtesting (details ND). Myntra: offline nDCG plus diversity metrics ILAD and ILMD; online A/B; the online model was warm-started on the last 7 days of data.
- **Metrics:** Meesho: CTR, CVR, "O/Vi" (undefined in the post), "FY" order contribution (abbreviation as written; not defined in the post), bounce rate, new-user activation. Myntra: nDCG; ILAD 0.480-0.502 and ILMD 0.039-0.042 across alpha settings (top-10 lists).

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Meesho | No frameworks named (ND) |
| Myntra | No libraries named; architecture has an online inference service, batch retraining per interval, model versioning |

### 8. Business Decision
Meesho: deploy a cold/warm gated model so the feed adapts from the first interactions; the post says the "FY" improvements also helped Search and other surfaces. Myntra: replace the XGBoost widget ranker with bandit plus DPP.

### 9. Business Impact
Meesho (company's own claim, no figures): "notable uplift" in CTR, CVR and O/Vi, "significant" increase in FY order contribution, "sharp drop in bounce rate". Myntra (authors' claim): +0.24% homepage clicks per user over XGBoost, which they call "a decent gain given our scale"; revenue per user and conversion guardrails positive but unquantified.

### 10. What a Data Scientist Can Learn *(interpretation)*
Treat cold-start as a gating problem: blend a demographic expert and a behavioural expert by how much history exists. Distilling warm knowledge into the cold expert only when the cold expert is worse is a neat conditional regulariser. For exploration, bandits give principled explore/exploit and handle item cold-start; add diversity re-ranking so exploitation does not collapse the page. Weak point: Meesho publishes no numbers, so use the Myntra figure (0.24%) only as an order of magnitude in any simulation.

### 11. Source Links
- Meesho, "Personalization from Day One: Solving the Cold Start Problem at Meesho": https://www.meesho.io/blog/personalization-from-day-one-solving-the-cold-start-problem-at-meesho (fetched via proxy; direct fetch returned 403; date not shown)
- arXiv 2309.14046, "Diversify and Conquer: Bandits and Diversity for an Enhanced E-commerce Homepage Experience", 2023-09-25: https://arxiv.org/abs/2309.14046 (content read via https://ar5iv.labs.arxiv.org/html/2309.14046)

---

---

# PART D — GROWTH, EXPERIMENTATION & CUSTOMER VALUE

## Case Study 19 — Switchback vs A/B experimentation in two-sided marketplaces (Cabify documented; Flipkart's early A/B framework as the Indian reference)

**Priority:** ★★★ Must-visit — A/B testing, variance reduction, interference and switchbacks: THE interview staple. **Notebook:** `cs19_experimentation_ab_testing.ipynb` (⏳ notebook pending)

**Company:** Cabify (substitute; Spain/LatAm ride-hailing marketplace). Indian reference: Flipkart (2012 A/B framework). Swiggy's in-house Experimentation Platform (XP) exists per search-result snippets, but its posts could not be fetched.
**Industry:** Ride-hailing marketplace (substitute); Indian ecommerce (reference)
**Business Area:** Product experimentation / growth analytics
**Problem Type:** Experiment design under interference (A/B vs switchback), experimentation platform
**Evidence Level:** Medium (A for Cabify, a named engineer's post; the Indian leg is only a 2012 press account with no statistics; no Indian method-level source was readable)
**Primary Sources:** Cabify engineering blog (Albert Rego, 4 Mar 2026); CIO India (Varsha Chidambaram, 21 May 2012) on Flipkart's framework.

### 1. Business Problem
Documented (Cabify): A/B tests split users into fixed groups, but some metrics are marketplace-wide. If treatment users create more journeys, they consume the shared driver pool and lower the success rate for control users. The post calls this cross-group interference "cannibalization", which makes A/B results misleading for such metrics.
Documented (Flipkart, 2012): Flipkart wanted to ship site changes without lengthy process. Amod Malviya (VP Engineering) designed a framework with a real-time metrics dashboard plus an A/B component.
Note: Swiggy/Zomato face the same shared-supply (delivery partner) structure, but the source for that is my inference, not a fetched page.

### 2. Business Question
Can a change to a marketplace-level algorithm or message be evaluated when treatment and control share supply? (Cabify example: standard ETA message vs a "more than 6 minutes" message.) For Flipkart: does a new homepage design hurt sales if shown to a slice of traffic?

### 3. Data Available
| Data | Description |
|---|---|
| Interval-level marketplace metrics (Cabify) | Performance (e.g. journey success) measured in each time interval, each interval is one sample |
| Journey / request logs (Cabify) | Journeys can start in one interval and finish in another (carryover) |
| Real-time site metrics (Flipkart, 2012) | Transaction rate etc. on a dashboard with threshold alerts |
| Dataset sizes, dates, schema | Not publicly disclosed (ND) |

### 4. Data Science Approach
Cabify: switchback design. All users see the same version at a given time; the group is determined by the time slot, so a user may experience both versions. Interval length is chosen to include all hour/day combinations (peak and off-peak), spread samples across hours and days, and fit the planned experiment duration. Example uses 53-minute intervals (a prime number, chosen to avoid cycling effects); alternatives mentioned: 58, 112, 29 minutes. Carryover is handled by switching less often when effects are persistent and by washout periods that drop early-treatment data. Duration depends on MDE and sample size, plus cost of running, uncertainty in sample rate, and blocking with other experiments (e.g. by region).
Flipkart 2012: 10% of traffic routed to the new version; metrics tool measures impact; if sales dip the change is rolled back.

### 5. Statistical Analysis
Cabify: performance compared across alternating intervals; sample-size/MDE logic "the same statistics as A/B tests"; washout. Specific test statistic, variance estimator, or CUPED-type adjustment: ND in the fetched post. Flipkart 2012: no statistics described (ND).
(DoorDash material on cluster-robust standard errors and CUPAC ">25% shorter switchback tests" appeared only in a search snippet; the DoorDash pages returned 403, so it is not treated as documented.)

### 6. Machine Learning
- Model(s): None (design/statistics case); ND
- Target variable: Marketplace-level success metric per interval (Cabify); ND beyond that
- Features: ND
- Validation approach: ND
- Metrics: ND

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Flipkart in-house A/B framework + metrics dashboard (2012) | Traffic split, real-time metrics on screens |
| Cabify internal switchback tooling | ND (tooling not named) |

### 8. Business Decision
Cabify: use switchback rather than user-level A/B for marketplace-wide metrics. Flipkart: roll out or roll back UI changes based on live metrics, accepting some risk to keep a "fearless culture of innovation" (Malviya).

### 9. Business Impact
No numeric lift stated for Cabify's example (ND). Flipkart 2012 article: tool introduced mid-2010; article context figures (company-reported/press): sales of Rs 75 crore a month, revenue doubling every quarter for eight quarters. These are not attributed causally to the framework.

### 10. What a Data Scientist Can Learn *(interpretation)*
Be able to say when user-level randomisation breaks (shared supply), what the unit of analysis becomes (the interval), why a prime interval length helps, and how washout trades bias for sample size. An interviewer will also expect power calculation, SRM checks and guardrail metrics, none of which these sources document.

### 11. Source Links
- Cabify Engineering, "Why do you need switchback experimentation", Albert Rego, 4 Mar 2026 - https://tech.cabify.com/blog/engineering/why-do-you-need-switchback-experimentation
- CIO India, "Flipkart Drives Innovation Through Intelligent use of IT", 21 May 2012 - https://www.cio.com/article/215584/flipkart-drives-innovation-through-intelligent-use-of-it.html

## Case Study 20 — Predicted lifetime value (pLTV) of new customers for bid optimisation at Swiggy

**Priority:** ★★★ Must-visit — Predicted customer LTV for acquisition bidding: asked everywhere, drives marketing spend. **Notebook:** `cs20_customer_lifetime_value.ipynb` (⏳ notebook pending)

**Company:** Swiggy (Food delivery and Instamart)
**Industry:** Food delivery / quick commerce
**Business Area:** Customer acquisition and lifetime value
**Problem Type:** Customer lifetime value prediction (cold start), multi-task learning
**Evidence Level:** Medium (B: InfoQ report of Swiggy's own Bytes post, quoting named Swiggy staff; the original Medium post returned 403 so details come second-hand). Classic RFM-based segmentation at Nykaa/Myntra/FirstCry/Flipkart: no company source found.
**Primary Sources:** InfoQ, "Swiggy Uses 350+ Features and Multi-Task MLP to Predict Customer Lifetime Value", Leela Kumili, 2 Sep 2026; original Swiggy Bytes post (not read).

### 1. Business Problem
Documented (via InfoQ): Predict the long-term value of new customers across Food and Instamart before their first order, so advertising bids optimise for long-term value instead of short-term conversion. Sparse early signals and a skewed target: many new users place no orders in 30 days while a small group generates much higher lifetime value.

### 2. Business Question
Can pre-first-order information rank new users by future value well enough to differentiate ad bids?

### 3. Data Available
| Data | Description |
|---|---|
| Pre-first-order features (350+) | Acquisition channel, device and fraud signals, geographic behaviour, complaint history, Instamart category affinity, order behaviour, payment patterns, socioeconomic indicators |
| Dataset size / time range | Not publicly disclosed (ND) |

### 4. Data Science Approach
Features built only from information available before first order (cold-start). A relatively simple MLP with three shared hidden layers and task-specific heads for Food and Instamart. Output used with Google tROAS bidding. Next step stated: probabilistic pLTV to represent uncertainty.

### 5. Statistical Analysis
MAE and MAPE judged insufficient because of many zeros and a long tail. Evaluation by ranking: predicted and actual values split into ten quantiles; Spearman correlation and decile "diagonal coverage". Hypothesis tests on the A/B: ND.

### 6. Machine Learning
- Model(s): Multi-task MLP, 3 shared hidden layers, heads for Food and Instamart; parameters reduced from 363,000 to 135,000 ("63% reduction"); the four-head version performed marginally better. Layer sizes/activations: ND
- Target variable: Lifetime value (primary); order count (auxiliary task)
- Features: 350+ pre-first-order features (categories above)
- Validation approach: Decile-ranking comparison of predicted vs actual; split scheme ND
- Metrics: Spearman above 0.75 for both Food and Instamart; diagonal coverage across deciles 70% to 80%

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Google Ads tROAS bidding | Consumes pLTV signal |
| ML framework | Not named (ND) |

### 8. Business Decision
Use the in-house pLTV signal for acquisition bidding instead of a third-party pLTV platform.

### 9. Business Impact
In production A/B, versus a third-party pLTV platform, the in-house model gave "higher retention and gross order value per acquired user, with no additional platform costs"; the external platform acquired more users per dollar. Exact figures: ND (InfoQ states none).

### 10. What a Data Scientist Can Learn *(interpretation)*
Zero-inflated, heavy-tailed LTV targets are better evaluated by ranking than by MAE; a model is judged by the downstream decision (bid), and a comparison against a vendor shows the CAC-versus-quality trade-off. Standard interview material: RFM, BG/NBD + Gamma-Gamma, hurdle models, calibration.

### 11. Source Links
- InfoQ, "Swiggy Uses 350+ Features and Multi-Task MLP to Predict Customer Lifetime Value", 2 Sep 2026 - https://www.infoq.com/news/2026/09/swiggy-pltv-multitask-mlp/

## Case Study 21 — Zomato Gold relaunch (2023) and Flipkart Plus tiering as membership design

**Priority:** ★★ Good to have — Membership design and retention: causal measurement without randomisation. **Notebook:** `cs21_membership_programme_retention.ipynb` (⏳ notebook pending)

**Company:** Zomato (primary); Flipkart (design contrast)
**Industry:** Food delivery; ecommerce
**Business Area:** Loyalty / subscription and retention
**Problem Type:** Membership programme design, retention, frequency uplift
**Evidence Level:** Weak-to-Medium (A for programme design and CEO statements via press coverage of the shareholder letter; no model or experiment method is public; the shareholder-letter PDFs themselves returned 403)
**Primary Sources:** Business Today (9 Feb 2023, 22 Mar 2023) reporting Zomato's Q3 FY23 letter; Flipkart Stories (15 Aug 2023).

### 1. Business Problem
Documented: Zomato relaunched Gold in January 2023 with a redesign that CEO Deepinder Goyal said was built on lessons from past years and is "more sustainable for customers, restaurant partners, and Zomato's P&L". It was expected to "drive loyalty and higher frequency of ordering going forward".

### 2. Business Question
Can a redesigned paid membership raise order frequency and loyalty without destroying unit economics? (Stated framing, not a documented analytical question.)

### 3. Data Available
| Data | Description |
|---|---|
| Order history | Not publicly disclosed (ND) as an input to design |
| Flipkart Plus eligibility data | Successful transactions in last 365 days (rule-based) |

### 4. Data Science Approach
Only programme design is public. Zomato Gold: Rs 149 for three months introductory price; unlimited free delivery within 10 km or on orders above Rs 199; "On Time Guarantee" Rs 100 coupons for delayed orders; up to 30% off delivery and up to 40% flat off dining at 25,000+ restaurants. Flipkart Plus: earned tiers, Silver at 15 and Gold at 25 successful transactions in 365 days, auto-activation, SuperCoins 1 or 2 per Rs 100, caps of 50 per month and 15 per order. Any modelling behind these thresholds: ND.

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
| Not disclosed | ND |

### 8. Business Decision
Zomato: relaunch Gold at a low entry price with delivery, on-time-guarantee and dining benefits. Flipkart: auto-enrol based on trailing-12-month transaction counts rather than a coin threshold (earlier 200-SuperCoin criterion per a search snippet, unverified).

### 9. Business Impact
Company-reported: "over nine lakh" Gold members within a month of relaunch (Business Today, 9 Feb 2023). HSBC (external broker, not company) says Gold helped Zomato take share from Swiggy in Q4FY23. Shareholder-letter figures that appeared only in a search snippet and are unverified here: Gold about 30% of food-delivery GOV (Mar-23) with order frequency up about 60% post joining; about 40% of food GOV in Q2 FY24; Gold orders worse on contribution margin. Swiggy One figures (7.40 vs 4.50 orders per member, 5.71 million members in Q1 FY25) also came only from a snippet of a third-party newsletter and are unverified. Flipkart: no membership size or share of transactions published on the fetched page.

### 10. What a Data Scientist Can Learn *(interpretation)*
Members self-select, so "frequency up 60% after joining" is not a causal effect; interviewers expect propensity matching, difference-in-differences or holdout design, and contribution-margin (not GOV) as the success metric. Threshold-based tiers are a design lever to analyse with elasticity or breakpoint analysis.

### 11. Source Links
- Business Today, "Zomato Gold adds 9 lakh members in a month...", Binu Paul, 9 Feb 2023 - https://www.businesstoday.in/amp/latest/corporate/story/zomato-gold-adds-9-lakh-members-in-a-month-10-minute-delivery-service-to-be-replaced-with-home-style-meal-service-369712-2023-02-09
- Business Today, "Zomato Gold or Swiggy One: Who's winning the loyalty programme race?", Sohini Mitter, 22 Mar 2023 - https://www.businesstoday.in/amp/entrepreneurship/story/zomato-gold-or-swiggy-one-whos-winning-the-loyalty-programme-race-374408-2023-03-22
- Flipkart Stories, Flipkart Plus programme page, 15 Aug 2023 - https://stories.flipkart.com/flipkart-plus-premium-loyalty-memberships
- Inc42, Swiggy FY26 metrics (platform frequency 4.07, MTUs 23.5 Mn; no Swiggy One data), 24 Jul 2026 - https://inc42.com/buzz/over-35-of-swiggy-users-try-multiple-services-but-order-frequency-slips/

## Case Study 22 — Real-time personalised coupon allocation under a budget (Meituan Bike; substitute for Indian companies)

**Priority:** ★★★ Must-visit — Uplift targeting and budget-constrained coupon allocation: the core promo-optimisation problem. **Notebook:** `cs22_coupon_allocation_uplift_budget.ipynb` (⏳ notebook pending)

**Company:** Meituan (substitute; no Indian company source with method detail found)
**Industry:** Bike-sharing subscription / local-services platform (China)
**Business Area:** Promotions and discount targeting
**Problem Type:** Personalised discount allocation under budget constraint (predict-then-optimise)
**Evidence Level:** Strong (C: paper by company team with online A/B test; but not Indian)
**Primary Sources:** Dai, Li, Zhu, Lin, Huang, "Data-Driven Real-time Coupon Allocation in the Online Platform", arXiv:2406.05987v3 (17 Jun 2024). Dai, Lin and Huang are at Meituan.

### 1. Business Problem
Meituan Bike sells monthly subscriptions and wants a personalised coupon for each arriving customer. The old offline integer-program system set coupons a day ahead, could not use same-day information, had to group customers and stored a value per user. The new system must decide within 50 ms and stay within a marketing budget under uncertain traffic.

### 2. Business Question
Which coupon level should each arriving user get to maximise revenue (price x conversion) subject to an average-price budget?

### 3. Data Available
| Data | Description |
|---|---|
| Random-traffic group | About 3 million user-level entries (20% of traffic across roughly 100 Chinese cities), split 80/20 train/test |
| Features | Over 200 customer, riding-behaviour and transaction features |
| Online test population | 3,867,738 random users in two cities, February 2024, about a month |

### 4. Data Science Approach
Predict conversion rate (CVR) for each coupon level; calibrate so CVR is non-increasing in price; relax the integer program via a Lagrangian dual; choose the coupon by argmax over the coupon ladder for a given multiplier lambda; initialise lambda offline by trisection search; a PID controller adjusts lambda during the day to keep average offered price near budget.

### 5. Statistical Analysis
Isotonic regression for calibration; PCOC (predicted-to-observed conversion) check; online randomised comparison across groups (Random, Manual, Offline-IP, LDM, LDM-IR). Significance testing: ND in the summary I read (the last 26k characters of the page were not read).

### 6. Machine Learning
- Model(s): XGBoost CVR model with isotonic-regression calibration
- Target variable: Conversion (CVR) at each coupon level
- Features: 200+ customer, riding-behaviour, transaction features
- Validation approach: 80/20 split on random-traffic data; offline runtime comparison; PID simulation; online A/B
- Metrics: AUC 0.891 (plain and calibrated); PCOC 0.971 to 0.982 after calibration; CVR, average price, price x CVR

### 7. Tools & Technology
| Tool | Use |
|---|---|
| XGBoost | CVR model |
| Lagrangian dual + trisection + PID controller | Allocation and budget control, 50 ms decisions |

### 8. Business Decision
Replace the offline integer-program allocation with the real-time LDM-IR system, rolled out beyond the test.

### 9. Business Impact
Company/author-reported. City B online test: LDM-IR price x CVR 2.15 vs Offline-IP 2.09; authors report "a 2.8% revenue gain per exposed user for LDM-IR over Offline-IP, about CNY 6 million per month per 100 million exposed users". City A: LDM-IR CVR 14.49% vs Random 12.93%. Abstract: 0.7% revenue uptick, about CNY 8 million annual profit; deployed to over 100 million users in 110+ cities as of May 2024. Group-level solve 0.28 s vs 83.42 s for the offline IP in City C. PID kept average price within about 1% of target versus about 3% overshoot without control.

### 10. What a Data Scientist Can Learn *(interpretation)*
Predict-then-optimise with a budget constraint is the standard template; calibration matters because the optimiser consumes probabilities, not ranks. Indian practice likely uses uplift models rather than pure CVR, but I found no public Indian method source (Meesho, Flipkart, Swiggy, Zomato searches returned nothing usable).

### 11. Source Links
- arXiv:2406.05987v3, "Data-Driven Real-time Coupon Allocation in the Online Platform", 17 Jun 2024 - https://arxiv.org/html/2406.05987v3

## Case Study 23 — Meesho notification volume, relevance and send-time experiments

**Priority:** ★ Optional — Notification volume and timing experiments; methods undisclosed. **Notebook:** `cs23_push_notification_optimisation.ipynb` (⏳ notebook pending)

**Company:** Meesho
**Industry:** Social / value ecommerce marketplace
**Business Area:** CRM / push notifications
**Problem Type:** Notification frequency, content relevance and send-time personalisation
**Evidence Level:** Weak (A: named executive on a panel, but only outcomes and framing; no method, data or numbers beyond volume)
**Primary Sources:** CleverTap blog, "How Meesho Created an App Experience to Serve an Untapped Market (Part 2 of 2)", 14 Feb 2023; panel with Kirti Varun Avasarala (Meesho CPO) and Abhishek Gupta (CleverTap CCO).

### 1. Business Problem
Conventional wisdom, as Avasarala put it: "Send too many notifications, and customers will uninstall your app because you're annoying them." Meesho tested this assumption.

### 2. Business Question
Does a much higher notification volume hurt uninstalls and retention, and what content, volume and timing should each customer receive?

### 3. Data Available
| Data | Description |
|---|---|
| Analysis, customer conversations, usage patterns | Mentioned qualitatively; specifics ND |

### 4. Data Science Approach
Only the framing is public. Meesho experimented with which content to send to each customer, and both notification volume and time of day of sending were personalised. Model, design, holdouts: ND.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- Model(s): ND (a separate talk summary says Meesho's Chief Data Scientist mentions ML for personalised push, from a search snippet only)
- Target variable: ND
- Features: ND
- Validation approach: ND
- Metrics: Engagement, uninstalls, retention named qualitatively

### 7. Tools & Technology
| Tool | Use |
|---|---|
| CleverTap | Engagement platform (the panel was hosted by CleverTap; Meesho named as a customer by Gupta) |

### 8. Business Decision
Send roughly 20 to 30 notifications per day, personalising content, volume and timing.

### 9. Business Impact
Company executive statement: engagement increased, uninstalls unaffected, retention "stayed strong"; Avasarala called it "very, very counterintuitive" and reported "very, very high engagement". No percentages (ND).

### 10. What a Data Scientist Can Learn *(interpretation)*
Frequency is context-dependent (Meesho is "a sort of hybrid of a social app and an ecommerce app"); test with long-run holdouts that track uninstall and opt-out, not only click-through. Expect questions on bandits for send-time, uplift per user and fatigue modelling.

### 11. Source Links
- CleverTap blog, "How Meesho Created an App Experience to Serve an Untapped Market (Part 2 of 2)", 14 Feb 2023 - https://clevertap.com/?p=56922

## Case Study 24 — Marketing mix modelling plus geo-lift experiments at Honasa Consumer

**Priority:** ★★ Good to have — Marketing-mix modelling with geo-lift calibration; common in D2C and marketplaces. **Notebook:** `cs24_marketing_mix_modelling.ipynb` (⏳ notebook pending)

**Company:** Honasa Consumer (Mamaearth parent). Nykaa, FirstCry, Flipkart and Swiggy: no usable source found.
**Industry:** D2C personal care (omnichannel, including ecommerce)
**Business Area:** Marketing measurement
**Problem Type:** MMM, incrementality (geo lift)
**Evidence Level:** Weak (A: named SVP quoted by Google; vendor-hosted write-up with no numbers or method detail)
**Primary Sources:** Think with Google India, MMM mindset shifts, Isha Puri and Naveen Yadav, December 2024; quotes from Vipul Maheshwari, SVP Product and Analytics, Honasa.

### 1. Business Problem
Honasa broadened its MMM to cover a wide range of factors rather than a narrow set, to make better-considered marketing decisions to reach millennial customers across India (as summarised from the page).

### 2. Business Question
Which marketing inputs drive sales, and how do strategies perform locally by geography?

### 3. Data Available
| Data | Description |
|---|---|
| Sales and marketing data, external factors | Maheshwari: "We analysed everything from sales and marketing data to external factors." Granularity, history, channels: ND |
| Geo lift experiment data | Maheshwari: "We also layered in our geo lift experiments" |

### 4. Data Science Approach
MMM combined with geo-lift experiments to see how strategies affect performance regionally. Model form, priors, calibration procedure: ND. The same page notes that in India MMM is often seen as "once-and-done" and argues for re-running (from a search summary of the Google page; not independently quoted).

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- Model(s): ND
- Target variable: ND (sales implied)
- Features: ND
- Validation approach: ND
- Metrics: ND

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Not named | ND |

### 8. Business Decision
Use MMM outputs to guide marketing decisions for millennial audiences; specifics ND.

### 9. Business Impact
ND. The page gives no Honasa-specific results.

### 10. What a Data Scientist Can Learn *(interpretation)*
Interviewers expect: MMM as regression with adstock and saturation (Bayesian, e.g. Robyn/Meridian-style), calibrated by geo-lift or holdout tests, and why last-click attribution over-credits bottom-funnel channels. This page confirms only that Indian firms pair the two.

### 11. Source Links
- Think with Google India, "Marketing mix modelling mindset shifts", Dec 2024 - https://business.google.com/in/think/measurement/marketing-mix-modelling-mindset-shifts/

---

# PART E — TRUST, RETURNS, RISK & SUPPORT

## Case Study 25 — Predicting Return-to-Origin (RTO) on cash-on-delivery orders at checkout using order history plus public social-profile signals

**Priority:** ★★★ Must-visit — COD return-to-origin prediction: imbalanced classification with a business cost; India-specific and very common. **Notebook:** `cs25_cod_rto_prediction.ipynb` (⏳ notebook pending)

**Company:** Flipkart (research with IIIT Delhi / IIIT Hyderabad academics)
**Industry:** Ecommerce marketplace (India)
**Business Area:** Checkout risk / logistics cost / fraud and abuse
**Problem Type:** Binary classification (order-level risk scoring), imbalanced, with feature enrichment from an external data source
**Evidence Level:** Strong (C) — peer-reviewed workshop paper (WWW '23 Companion) with four Flipkart-affiliated authors, real order data, full result table; no deployment or revenue figure is given.
**Primary Sources:** Hitkul, Abinaya K, Soham Saha, Satyajit Banerjee, Muthusamy Chelliah, Ponnurangam Kumaraguru, "Social Re-Identification Assisted RTO Detection for E-Commerce", WWW '23 Companion (April 30-May 4, 2023), DOI 10.1145/3543873.3587620. Supporting framing only: Meesho RHP coverage (MediaNama), practitioner article (HackerNoon).

### 1. Business Problem
The paper defines RTO as the case where "the user cancels an order while it is in transit for delivery" (authors' definition; its Figure 1 shows an order becoming RTO when cancelled after it has shipped from the source location). It names two losses:
- Logistical cost: shipping to the point of cancellation, returning, and restocking.
- Opportunity cost: the unit is unavailable to another customer who would have accepted delivery.

The authors say an increased RTO rate "by uninformed customers or bad actors can cause unanticipated revenue losses totaling double-digit million dollars annually" (company-team claim, no breakdown). They observed that "orders with cash on delivery are more prone to RTO", and so restricted the study to COD orders.

Context from a different primary document: Meesho's RHP states "72% of orders on Meesho were paid for using cash on delivery (CoD)" for the six months to September 2025, down from 77% in FY25 and 85% in FY24 (as reported by MediaNama; the article gives no RTO rate). The RHP also says CoD "requires physical cash handling by our last mile delivery partners" and raises the risk of unsuccessful deliveries when customers refuse products. This shows why COD risk matters in India but is not a Meesho RTO model.

### 2. Business Question
Can the platform predict, at the time of checkout, the likelihood that an order will become RTO, so that precautionary measures can be triggered? The paper's specific hypothesis: does adding socio-economic signals from a re-identified public professional-network profile improve RTO prediction over historical-trend features alone?

### 3. Data Available
| Data | Description |
|---|---|
| Historical orders and outcomes | "All past orders and their subsequent outcomes"; label = RTO vs delivered |
| Randomised control set | 5% of all orders randomly set aside with no intervention, to avoid bias from other checkout models; only COD orders from this set were used |
| Past-trend features (internal) | RTO ratio vs total orders over last 3 months and 1 year, for user, product, seller, product category; same trends for pin code, street and city in the delivery address; hour of day and weekday of order |
| Social profile, quantitative | Whether user is a student, number of jobs, number of degrees, friends and followers, total years working and in education |
| Social profile, abstractive | Embeddings (S-BERT, 387-dim vector) of job and education text |
| Re-identification inputs | User name and city, plus the set of cities the user has ordered from |
| Study window | November 2021 to April 2022; first 5 months train, last 1 month test |
| Final dataset | 6,881 orders by 2,121 unique users; 2,201 (32%) orders were RTO |

Only users who explicitly made name and city public were used; the paper states compliance with platform privacy policies.

### 4. Data Science Approach
Documented pipeline:
1. Ground truth from past orders; the 5% randomised, un-intervened control set is used so labels are not contaminated by earlier models' interventions. COD orders only.
2. Candidate extraction: query "<user name> <city name>" on a professional-network search and a web search engine; top 10 results are candidate profiles. Candidates were found for 1,091 of 2,121 users.
3. Re-identification: reject candidates whose name does not match; then compute a match score = share of locations in the candidate's profile that are also in the user's order-city set, with fuzzy matching (e.g., Delhi vs New Delhi, Bangalore vs Bengaluru). A profile is a match if the score exceeds a threshold (results reported at 0.6). Users fall into No match / Exact match / Multiple matches; no-match users are dropped from modelling; for multiple matches the feature values are averaged.
4. Feature construction (three groups above) and model training.
5. Classification threshold chosen to maximise "Goodness" subject to a cap on false-positive rate (cap set by product requirement; value ND), because a high FPR means false interventions that hurt customer experience.

Re-identification outcomes (Table 1): at threshold 0.6, Exact match 68.92%, Multiple 17.68%, No match 13.40%; at threshold 1.0 No match rises to 40.02%.

### 5. Statistical Analysis
- Randomised holdout (5% of orders with no intervention) to obtain unbiased outcome labels. This is the main statistical-design point documented.
- Time-based split (5 months train / 1 month test) rather than random split.
- Fuzzy string matching and a threshold-based match score for entity resolution; sensitivity to the threshold was checked ("results for varying values ... were consistent", not shown).
- No hypothesis tests, confidence intervals or significance values are reported (ND).

### 6. Machine Learning
- **Model(s):** Random Forest, XGBoost, TabNet (tabular deep net; tabular features encoded by TabNet, concatenated with S-BERT embeddings, then feed-forward layers). Random Forest performed best; the paper notes deep models did worse, consistent with the literature on tabular data.
- **Target variable:** Order becomes RTO (binary), COD orders in the control set.
- **Features:** See section 3. For tree models, the 387-dim S-BERT vectors for job and education were reduced with UMAP (output dimension treated as a hyperparameter) to limit overfitting.
- **Validation approach:** 5-month train / 1-month test; hyperparameters tuned by random search with 4-fold cross-validation on the training data.
- **Metrics:** Precision, recall, and a custom "Goodness" in basis points, described as reflecting "the reduction in the ratio of RTO orders after being evaluated by the model" (formula in the paper's equation 2). Test results, Random Forest (Table 2):

| Features | Precision % | Recall % | Goodness (bps) |
|---|---|---|---|
| Past trends | 85.7 | 40.3 | 1,005.7 |
| + Social quantitative | 85.7 | 50.4 | 1,305.6 |
| + Social quantitative + abstractive | 88.8 | 60.2 | 1,633.7 |

XGBoost with all features: precision 86.8, recall 44.5, Goodness 1,129.4. TabNet with all features: precision 64.2, recall 15.1, Goodness 320.0 (TabNet with past trends only: 82.4 / 39.4 / 977.0).

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Models | Random Forest, XGBoost, TabNet |
| Text embeddings | S-BERT (387-dim), UMAP for dimensionality reduction |
| Data sources | Internal order data; public professional-network profiles; search engines |
| Serving / infra | ND (paper only says a real-time checkout system is needed) |

### 8. Business Decision
The paper says the prediction, "combined with other attributes like customer history, and available stock of the product", can be used to "initiate precautionary measures that can mitigate RTO risk". The specific measure (block COD, require prepayment, extra verification, etc.) is ND. The decision threshold is set to maximise Goodness under a fixed false-positive-rate cap.

### 9. Business Impact
- "3.1% increase in precision and 19.9% increase in recall" (authors' wording; the table shows these are percentage-point gains: 85.7 to 88.8 precision and 40.3 to 60.2 recall for Random Forest).
- Goodness rises by 628 bps (1,005.7 to 1,633.7): +300 bps from quantitative social features, +328 bps from abstractive embeddings.
- Authors' claim: "every 1% increase in the recall can add six figures to the bottom-line revenue for a large-scale organization" (no currency or basis given, not independently verified).
- Production deployment, A/B test result and rupee savings: ND.
- Caveats stated by the authors: India-only data; social re-identification covered only a subset of users (1,091 of 2,121 had candidate profiles); privacy considerations.

### 10. What a Data Scientist Can Learn *(interpretation)*
- The 5% no-intervention holdout is the key design idea: when earlier models already block or alter orders, outcomes are censored, and a random holdout is the clean way to get labels. Interviewers like this.
- Report business-aligned metrics (the paper's Goodness at a fixed FPR cap) next to precision and recall.
- The final sample is small (6,881 orders, 32% positive) because of the privacy filter and the control-set restriction, so the lift is a proof of concept, not a production estimate. A candid answer would say so.
- Tree ensembles beat TabNet on this tabular problem; do not default to deep learning.
- Using social-profile data raises fairness and privacy questions (proxy for socio-economic status); be ready to discuss.

### 11. Source Links
- https://precog.iiit.ac.in/pubs/Flipkart_RTO_WWW_workshop_Cameraready.pdf — "Social Re-Identification Assisted RTO Detection for E-Commerce" (WWW '23 Companion, 2023; fetched PDF)
- https://medianama.com/2025/12/223-meesho-ipo-rhp-filing-5421-crore/ — MediaNama on Meesho RHP, COD share (December 2025; fetched)
- https://hackernoon.com/using-data-science-to-deal-with-rtos — Shaurya Uppal, "Using data science to deal with RTOs" (August 22, 2022; fetched; generic practitioner article, employer not named, no measured results; background only, not used for any figure in sections 1-9)

---

## Case Study 26 — Reducing size-related returns with a size and fit predictor that reads customer reviews

**Priority:** ★★ Good to have — Size/fit prediction to cut returns in fashion. **Notebook:** `cs26_size_fit_returns.ipynb` (⏳ notebook pending)

**Company:** Flipkart (substituted for Myntra; see below)
**Industry:** Fashion ecommerce (India)
**Business Area:** Returns reduction, product-page size and fit recommendation
**Problem Type:** Three-class classification (small / fit / large) with cold-start handling and text embeddings
**Evidence Level:** Strong (C) for the method (SIGIR eCom '22 workshop paper, three Flipkart authors, four category datasets); no business-impact figure is published, so impact is ND.
**Primary Sources:** Oishik Chatterjee, Jaidam Ram Tej, Narendra Varma Dasaraju (Flipkart Internet Pvt Ltd), "Incorporating Customer Reviews in Size and Fit Recommendation systems for Fashion E-Commerce", SIGIR eCom'22, July 2022, arXiv:2208.06261.

**Substitution note:** I could not find a Myntra, Ajio or Nykaa Fashion paper or engineering post with method detail on size recommendation. Search results only surfaced 2016 press about Myntra's uniform size chart and a job listing; I did not read those pages in full, so nothing from them is used as fact here. Flipkart's paper is a better-documented case of the same problem type.

### 1. Business Problem
The paper states "there are a lot of size related returns and refunds in e-fashion domain which causes inconvenience to the customers as well as costs the company", and cites "Up to 40% of online fashion products are returned" (from a third-party reference in the paper, not Flipkart's own number). It notes that symbolic sizes (S/M/L) vary between brands and sometimes within a brand, and that size guides are brand-level and cumbersome.

### 2. Business Question
Given a customer, a product and the reviews on that product's page, will the product be small, true-to-size, or large for this customer, so the platform can show "buy one size larger / smaller" tips? Can review text improve on a model that uses only customer and product features, especially for new customers (cold start)?

### 3. Data Available
| Data | Description |
|---|---|
| Product details | Numeric (e.g., size) and categorical (brand, fabric etc.) product features |
| Purchase and returns data | Each purchase labelled "small" or "large" if returned with that reason code ("Size smaller" / "Size larger"), otherwise "fit" |
| Customer features | Continuous and categorical (specific fields ND) |
| Customer reviews | Text reviews on the product page; zero, one or many per product |
| Public dataset | ModCloth fit reviews, used to train BERT where labelled reviews are not available |

Dataset scale (Table 1; "one of the largest e-commerce platforms"; Flipkart named in author affiliations):

| Category | Customers | Products | % Small | % Large |
|---|---|---|---|---|
| Women Jacket | 14,94,713 (1.49M) | 47,040 | 4.52% | 1.68% |
| Women Kurta and Kurti | 61,53,598 (6.15M) | 1,20,425 | 2.40% | 1.30% |
| Men's Jean | 31,72,637 (3.17M) | 47,140 | 2.92% | 2.35% |
| Men's Polo T-shirt | 21,18,089 (2.12M) | 47,040 | 3.14% | 2.76% |

(Indian digit grouping as printed in the paper.) Time window of the data: ND.

### 4. Data Science Approach
Documented:
1. Framed as classification P(F | C, P, R) over {small, fit, large}.
2. Three input pathways (product, customer, reviews), each a stack of residual blocks, then a combined pathway ending in softmax. Categorical features go through embedding layers; numeric features are normalised.
3. Each review is embedded with a pre-trained language model; embeddings for a product are averaged; a zero vector is used when no reviews exist.
4. Four language-model variants compared: BERT trained on ModCloth fit classification (BM), BERT fine-tuned on the platform's own review fit classification (BFC), FKBERT (a RoBERTa model pre-trained with masked-language-modelling on platform text: descriptions, reviews, Q&A) (FB), and FKBERT fine-tuned on fit classification (FFC). "Only Reviews" (majority vote of review-level predictions) is also reported.
5. Baseline: SFNet, a deep model using only customer and product features.
6. Because "the dataset is highly skewed towards the fit class", fit instances in training were re-sampled to equal the number of small plus large instances.

### 5. Statistical Analysis
- 80:10:10 train / validation / test split per category.
- Class-imbalance handling by re-sampling the majority class in training.
- Model selection by best validation F1 over up to 100 epochs.
- No significance tests, confidence intervals or variance across seeds are reported (ND). Improvements are single-run relative differences.

### 6. Machine Learning
- **Model(s):** Residual-block neural network with three pathways plus BERT/RoBERTa-style review encoder (768-dim review embedding); baseline SFNet.
- **Target variable:** Three classes: small / fit / large, derived from return reason codes (not returned = fit).
- **Features:** Product features, customer features, averaged review embeddings (details in section 3).
- **Validation approach:** 80:10:10 split; best-validation-F1 epoch; Adam, learning rate 0.01, batch size 2,048; BERT trained with AdamW at 2e-5.
- **Metrics:** Macro F1. Baseline SFNet macro F1: Women Jacket 38.26, Women Kurta/Kurti 35.6, Men's Jean 37.19, Men's Polo 37.2. Best model (FKBERT-FC) improvement over baseline: +4.31%, +3.09%, +1.37%, +2.42% respectively (relative improvements as presented in the table). "Only Reviews" was worse than baseline by 8.13% to 15.68%.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Language models | BERT, RoBERTa-based "FKBERT" |
| Baseline | SFNet |
| Optimisers | Adam, AdamW |
| Public data | ModCloth |
| Serving, A/B testing, infra | ND |

### 8. Business Decision
Output is intended as a product-page tip: "buy one size large", "buy one size small", or no recommendation when the product is true to size. Whether and how this was launched, and the thresholds used, are ND.

### 9. Business Impact
- Paper's claim: "an improvement of 1.37% - 4.31% in F1 (macro) score over the baseline across the 4 different datasets"; transfer from the public ModCloth data alone gives "0.43% - 1.94% improvement".
- Reduction in return rate, return cost or conversion uplift: ND (not measured in the paper).

### 10. What a Data Scientist Can Learn *(interpretation)*
- Return reason codes act as free labels; the labelling rule (not returned = fit) is noisy because non-returners may still have been unhappy. Interviewers often probe this label noise.
- Macro F1 around 35 to 38 shows the task is hard and highly imbalanced (small and large are 1.3% to 4.5% of instances each). Accuracy would be meaningless here.
- Gains are modest (1% to 4% relative); a good answer discusses whether that is worth the engineering and how it would be tested (A/B test on return rate per category).
- Cold start is the real motivation for text features; discuss alternatives (brand-level embeddings, measurement questionnaires).

### 11. Source Links
- https://arxiv.org/abs/2208.06261 and https://arxiv.org/pdf/2208.06261 — Chatterjee, Tej, Dasaraju, "Incorporating Customer Reviews in Size and Fit Recommendation systems for Fashion E-Commerce" (arXiv August 11, 2022; SIGIR eCom'22, July 15, 2022; fetched PDF)

---

## Case Study 27 — Detecting rating fraud (fake and defaming reviews) on a marketplace with a Bayesian anomaly model (BIRDNEST)

**Priority:** ★★ Good to have — Rating-fraud detection with anomaly scoring. **Notebook:** `cs27_fake_review_rating_fraud.ipynb` (⏳ notebook pending)

**Company:** Flipkart (with Carnegie Mellon and other academic collaborators)
**Industry:** Ecommerce marketplace (India)
**Business Area:** Trust and safety, review integrity, seller fraud
**Problem Type:** Unsupervised anomaly detection / fraud ranking, validated by manual labelling
**Evidence Level:** Strong (C) — arXiv paper with two Flipkart-linked co-authors (Mohit Kumar, Disha Makhija; the paper's affiliation markers were not cleanly readable, but the paper reports Flipkart's own labelling), real Flipkart data, expert-labelled precision; dated (2015-16) and no production-impact figure.
**Primary Sources:** Bryan Hooi, Neil Shah, Alex Beutel, Stephan Gunnemann, Leman Akoglu, Mohit Kumar, Disha Makhija, Christos Faloutsos, "BIRDNEST: Bayesian Inference for Ratings-Fraud Detection", arXiv:1511.06030 (v1 November 19, 2015; v2 March 7, 2016).

Note: this paper does not cover refund/return abuse or promo abuse. For those, only an unofficial write-up of Swiggy's support flow (see R5) mentions refund-abuse scoring; no Flipkart/Amazon India return-abuse method with detail was found.

### 1. Business Problem
"Review fraud is a pervasive problem in online commerce, in which fraudulent sellers write or purchase fake reviews to manipulate perception of their products and services." Prior detectors rely either on bursts in time or on skewed rating distributions; either signal may be absent in a given dataset.

### 2. Business Question
Can a single principled model combine temporal-burst and rating-distribution signals to rank users by how suspicious they are, at scale, with no labelled training data, so that investigators review the most suspicious accounts first?

### 3. Data Available
| Data | Description |
|---|---|
| Flipkart ratings | 1.1M users, 550K products, 3.3M ratings (1 to 5 stars) with timestamps (Table 2 of paper) |
| Software-app reviews (SWM) | 0.97M users, 15K products, 1.1M ratings; crawled app reviews used as a second dataset |
| Expert labels (Flipkart) | Top 250 flagged users were investigated and hand-labelled by Flipkart |

Features per user: the count of each star rating, and the count of inter-rating time gaps in log-scale buckets (time since the user's previous rating, bucketed by integer part of the log, with base chosen to give close to 20 buckets).

### 4. Data Science Approach
1. Represent each user by two count vectors: ratings by star level and time-gap bucket counts.
2. BIRD model: users belong to one of K clusters (a mixture); each cluster has Dirichlet parameters; each user's rating distribution and temporal distribution are drawn from the cluster's Dirichlet prior; observed counts are multinomial. Parameters are fit by maximum likelihood (fixed-point iterations for the Dirichlet-multinomial).
3. Posterior for each user's true rating and temporal distributions is Dirichlet (conjugate update).
4. NEST suspiciousness metric: the expected "surprise" of a user's posterior under the global fitted distribution, computed separately for ratings and for time gaps, each normalised by its standard deviation across users, then combined so neither dominates.
5. Rank users by NEST; submit the top 250 Flipkart users to Flipkart for manual investigation.
6. Interpretability check on three anonymised real Flipkart users (alice, bob, carol), simulating 10,000 draws from each posterior to show the posterior of the long-run average rating.

Fraud patterns found by Flipkart's domain experts (as reported in the paper): users "spamming 4/5 star ratings to multiple products from a single seller (boosting seller's ratings), or spamming 1/2 star ratings to multiple products from another seller (defaming the competition)."

### 5. Statistical Analysis
- Dirichlet-multinomial mixture model, conjugate Bayesian updating, posterior simulation for interpretability.
- Likelihood-based "expected surprise" score (a Bayesian anomaly score) with standard-deviation normalisation.
- Precision-at-k reported against expert labels (precision 1.0 for the first 50 users).
- Scalability: linear-time algorithm; "running on our 1.1M user, 3.3M ratings dataset in around 2 minutes" on a 2.4 GHz Intel Core i5 MacBook Pro, 16 GB RAM (authors' statement).
- Baseline comparisons beyond the Flipkart evaluation: ND (not extracted).

### 6. Machine Learning
- **Model(s):** BIRD (Bayesian mixture of Dirichlet-multinomials) with NEST score; unsupervised.
- **Target variable:** None at training time (unsupervised). Evaluation target: whether a flagged user was "involved in fraud" per Flipkart labelling.
- **Features:** Star-rating histogram and log-bucketed inter-rating time histogram per user.
- **Validation approach:** Expert manual labelling of the top-250 output; precision@k. No train/test split (unsupervised). Recall and false-negative rate: ND (cannot be computed from top-k labelling alone).
- **Metrics:** Precision at k.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Implementation | Python; code released by the authors (CMU-hosted archive) |
| Hardware | Single laptop for experiments (see section 5) |
| Production deployment at Flipkart | ND |

### 8. Business Decision
Flipkart investigated and hand-labelled the flagged accounts; what action followed (removal of reviews, account bans, seller penalties) is ND in the paper. The paper only says these are "substantial findings for Flipkart".

### 9. Business Impact
- "the 50 most suspicious users of the Flipkart platform flagged by our algorithm were investigated and all identified as fraudulent by domain experts at Flipkart" (abstract).
- "211 users of the top 250 flagged by BIRDNEST involved in fraud", and the paper's text states "precision of over 84% on the top 250" (211/250 = 84.4%). Authors' claim, validated by Flipkart reviewers; no independent audit.
- Revenue, trust-score or review-removal volume: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Fraud problems rarely have clean labels; an unsupervised score plus a human-in-the-loop review of the top-k, with precision@k as the headline metric, is a realistic design.
- Small-sample users (few ratings) are where Bayesian shrinkage matters: a Dirichlet prior stops one-or-two-rating users from looking extreme. This is a good interview talking point on smoothing versus raw proportions.
- Combining two weak signals (burstiness and skew) by normalising their scales is a general pattern; mention the risk of one signal dominating.
- The result is from 2015-16 data; it says nothing about modern LLM-generated or incentivised reviews.

### 11. Source Links
- https://arxiv.org/abs/1511.06030 — BIRDNEST abstract page (v1 November 19, 2015; v2 March 7, 2016; fetched)
- https://arxiv.org/pdf/1511.06030 — full paper (fetched and text-extracted)

---

## Case Study 28 — Filling missing product attributes automatically to improve catalogue quality (multimodal generative extraction), with a Flipkart image-similarity service as a supplementary data point

**Priority:** ★ Optional — Catalogue attribute extraction with multimodal models; heavy deep-learning engineering. **Notebook:** `cs28_catalogue_attribute_extraction.ipynb` (⏳ notebook pending)

**Company:** Amazon (the paper does not state the India marketplace; see substitution note). Supplementary: Flipkart Trust & Safety (vendor case study).
**Industry:** Ecommerce marketplace (global; India-operating company)
**Business Area:** Catalogue quality, attribute enrichment (search and filters)
**Problem Type:** Information extraction / generative question answering over text and image
**Evidence Level:** Medium (C) — ACL 2023 Industry Track paper by Amazon authors with datasets, metrics and deployment scale; but India-specific deployment is not stated in the paper. The Flipkart supplementary item is D (vendor-authored).
**Primary Sources:** Anant Khandelwal, Happy Mittal, Shreyas Sunil Kulkarni, Deepak Gupta (Amazon), "Large Scale Generative Multimodal Attribute Extraction for E-commerce Attributes", arXiv:2306.00379 (June 1, 2023; ACL 2023 Industry Track). Supplementary: Daniel Azoulai, Qdrant blog, "Building real-time multimodal similarity search in Flipkart Trust & Safety with Qdrant" (January 9, 2026).

**Substitution note:** I found no Flipkart, Myntra or Amazon India engineering post or paper with attribute-extraction or counterfeit-detection method detail that I could fetch and confirm. Meesho's counterfeit-removal claim (about 42 lakh listings) appeared only in a search-result snippet; the Business Standard page returned HTTP 403, so it is not used as fact. The Amazon paper is the best-documented catalogue-quality case found; the paper does not name its marketplace ("a popular e-commerce store") nor say it serves India. Treat India relevance as the problem type, not the site.

### 1. Business Problem
"Sellers rarely specify all attribute values or mistakenly fill incorrect values." Missing or wrong attributes (colour, size, material, sleeve type) hurt catalogue quality and customer experience. Attributes may or may not appear in the text, and may only be inferable from images.

### 2. Business Question
Can one model extract (or infer) attribute values for thousands of product-type and attribute combinations from product text plus image, including values never seen in training and values not written in the text?

### 3. Data Available
| Data | Description |
|---|---|
| Product text | Product-type plus textual description |
| Product images | One image per product, embedded with ResNet-152 |
| Labels | Distant supervision: the abstract says it needs no human labelling (label source detail not extracted) |
| 30PT dataset | 30 product types, 38 unique attributes; 569k train and 84k validation products; test data from two product types, 73k products |
| E-commerce5PT dataset | A second dataset used for F1 comparison (size ND) |

### 4. Data Science Approach
The problem is posed as question answering: question = attribute name; context = product type + text + image; answer = attribute value. Architecture (MXT): T5 encoder-decoder; image embeddings from ResNet-152 fused into T5 text embeddings through a Multimodal Adaptation Gate (MAG); an Xception network gives attribute-aware regional visual embeddings fused via dot-product attention; T5 decoder generates the value. A single model is trained across many product-type/attribute pairs by putting the product type in the input. Compared against NER-MQMRC (extractive) and CMA-CLIP (multimodal classifier). Ablations: single-PT vs multi-PT training, without Xception, without MAG. Zero-shot (unseen value) and value-absent (not in text) inference are demonstrated.

### 5. Statistical Analysis
No hypothesis tests or confidence intervals are documented (ND). Evaluation uses recall at a fixed 90% precision (Recall@90P), on the top-5, top-10 and top-15 attributes by product count, plus ablation comparisons.

### 6. Machine Learning
- **Model(s):** MXT = T5 (t5-base) + MAG + ResNet-152 + Xception.
- **Target variable:** Attribute value (generated text) for a given attribute name.
- **Features:** Product type, text description, image embeddings.
- **Validation approach:** Train/validation/test by product type (test on two held-out product types for the 30PT dataset); trained 20 epochs, batch size 4, 8 V100 GPUs (16 GB).
- **Metrics:** Recall@90P (relative improvement over NER-MQMRC), F1.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Models | T5-base, ResNet-152, Xception, MAG |
| Training hardware | 8 x NVIDIA V100 (16 GB) |
| Optimiser | Adam |
| Supplementary (Flipkart T&S) | Qdrant vector DB (HNSW), Java gRPC SDK, Prometheus, HBase+LSH (previous system), 2048-dim embeddings from Flipkart models (not named) |

### 8. Business Decision
Extracted values are used to fill catalogue attributes. The paper says models "are being used to extract attributes for over 12000 PT-attributes in a popular e-commerce store, and have extracted more than 150MM attribute values" (introduction); the deployment section says "6 English speaking markets covering >10K PT-attributes" and ">150MM attribute values" (the paper itself gives 12000 and >10K in different places). Confidence thresholds and human review: ND.

Supplementary Flipkart item (vendor-authored, D): Flipkart's Trust & Safety team moved from an HBase plus locality-sensitive-hashing batch system to a Qdrant-based real-time image-similarity service to catch fraud and abuse such as repeat returns and duplicate seller claims. It also supports address clustering for last-mile routing and retrieval for RAG. This is fraud and duplicate-claim matching, not catalogue attribute work.

### 9. Business Impact
- Paper: Recall@90P improvements of "10.16% and 6.9%" over existing state-of-the-art models (abstract). The in-paper table 1 gives gains over NER-MQMRC by attribute group, e.g., CMA-CLIP +1.81% to +6.70% and MXT variants up to +22.33% on the 30PT table. Treat the abstract figures as the headline claim and the table as detail; I did not reconcile the two.
- Scale: >150MM attribute values extracted.
- Effect on conversion, search quality or catalogue completeness rate: ND.
- Flipkart supplementary (Qdrant's narrative, quoting Flipkart engineer Sourabh Sarkar, SDE-III): lookups that "took up to nine hours" now take "under one minute"; no dataset size or methodology; vendor claim.

### 10. What a Data Scientist Can Learn *(interpretation)*
- "Recall at fixed precision" is the natural metric when auto-filling a catalogue: wrong values are costlier than missing ones.
- Distant supervision means label noise from sellers' own entries; interviewers may ask how you would audit it.
- Single multi-task model versus one model per category is a maintenance and monitoring trade-off, explicitly argued in the paper.
- Duplicate and counterfeit detection is usually embedding plus approximate nearest-neighbour search; the speed-up claim in the Flipkart case is about infrastructure, not model accuracy.

### 11. Source Links
- https://arxiv.org/abs/2306.00379 and https://arxiv.org/pdf/2306.00379 — Khandelwal et al., MXT (June 1, 2023; fetched)
- https://qdrant.tech/blog/case-study-flipkart/ — Qdrant, Flipkart Trust & Safety case study (January 9, 2026; fetched; vendor-authored)

---

## Case Study 29 — Automating food-delivery customer support with LLM agents and measuring containment, latency and CSAT (Zomato Zia and Nugget)

**Priority:** ★★ Good to have — Support automation, containment vs CSAT. **Notebook:** `cs29_support_automation_resolution.ipynb` (⏳ notebook pending)

**Company:** Zomato (Eternal group), with Together AI and MongoDB as vendor narrators
**Industry:** Food delivery / quick commerce (India)
**Business Area:** Customer support automation
**Problem Type:** Conversational AI (intent detection, function calling, escalation policy) with operational KPIs
**Evidence Level:** Medium (A/D) — one source is adapted from a named Zomato AI engineer's Fifth Elephant 2024 talk (published by Together AI), the other is a MongoDB vendor case study quoting Zomato; all headline numbers are company-sourced via vendors and unaudited.
**Primary Sources:** Together AI customer story on Zomato's bot "Zia" (adapted from a talk by Yuvraj Gagneja, AI Engineer, Zomato AI, Fifth Elephant 2024; publication date ND); MongoDB blog by Vinay Agarwal, "Zomato Cuts $11M in Support Costs With MongoDB-Powered AI Platform" (March 24, 2026). Context: Swiggy chatbot architecture write-up by Arpit Bhayani (external, not a Swiggy source).

### 1. Business Problem
From the MongoDB case study (vendor-authored): support costs had grown to "US$20M annually"; operations were spread across "10 disparate platforms"; about 60% of tickets were already auto-resolved but Zomato wanted higher customer satisfaction. From the Together AI story: Zomato handles over one million orders a day across India, with meal-time spikes of 10 to 50 times baseline traffic and messages above 1,000 per minute at peak.

### 2. Business Question
Can LLM-based agents resolve a high share of order-related support queries within seconds, with safe escalation to humans, while improving CSAT and cutting cost per ticket?

### 3. Data Available
| Data | Description |
|---|---|
| Real-time order data | Fetched through targeted API calls via function classification and function calling; JSON converted to natural language for the LLM |
| Chat history | Conversation context in the prompt |
| Business guidelines | Policy text included in the final prompt |
| Escalation tags | Escalations carry predefined reasons, checked against order data |
| Ticket metadata and user history | Stored in MongoDB Atlas for Nugget (flexible schema, compound indexes) |

Training/fine-tuning data: ND (the story does not say Zomato fine-tuned any model).

### 4. Data Science Approach
Documented (Together AI story, talk-derived):
- First version used closed-source models including GPT-4; Llama 3 made open-source models competitive enough to switch.
- Larger 70B models for intent detection; smaller 8B models for chat completion.
- Function classification then function calling to pull order data; response composed from data + history + guidelines.
- "With LLM-only escalation decisions, containment swung between 80% and 50% day to day. A policy layer was added to stabilize it." (This is the fetched tool's paraphrase of the page, not a verbatim quote.)
- Evaluation: every system change gets human review, a sample of responses is graded by humans, LLM-as-judge is also used; four metrics tracked: factual consistency, information relevance, guideline compliance, customer pain-point resolution.
- Infrastructure: serverless endpoints for baseline traffic and dedicated endpoints for peaks.

Documented (MongoDB story): Nugget is an in-house "AI-native CX platform" with autonomous multi-channel agents (voice, chat, social, in-app), an agent co-pilot for humans, triage automation and outcome tracking; launched as a multi-tenant enterprise offering in 2025.

Context (not Zomato): an external write-up says Swiggy's bot is a deterministic decision tree built from top contact drivers, with fraud/refund-abuse scoring (refund-to-order ratio, past abuse scores) deciding auto-refund vs proof vs human. That article is by a Razorpay engineer, not Swiggy, and gives no efficacy percentage.

### 5. Statistical Analysis
No statistical tests, A/B design or confidence intervals are documented (ND). The only quality-measurement design point is human sampling plus LLM-as-judge on four rubric metrics.

### 6. Machine Learning
- **Model(s):** Llama family on Together AI (70B for intent detection, 8B for chat completion; earlier GPT-4). Model versions beyond "Llama 3" and fine-tuning: ND.
- **Target variable:** Intent / next action (resolve, call function, escalate) per turn; no explicit supervised label reported.
- **Features:** Prompt context (order data, chat history, guidelines).
- **Validation approach:** Human review of changes; sampled human grading; LLM-as-judge. Offline accuracy numbers: ND.
- **Metrics:** Containment/resolution rate, response latency, CSAT, factual consistency, relevance, guideline compliance, pain-point resolution.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| LLM serving | Together AI (serverless and dedicated endpoints), Llama models; GPT-4 in v1 |
| Data store | MongoDB Atlas (chosen after testing DynamoDB and DocumentDB, per Zomato via MongoDB) |
| Platform | Nugget (in-house); function calling to order APIs |
| Evaluation | Human review, LLM-as-judge |

### 8. Business Decision
Replace most first-line support with LLM agents; keep humans via escalation and an agent co-pilot; add a policy layer to stabilise escalation decisions; offer the platform to other enterprises as Nugget.

### 9. Business Impact (all company-sourced via vendors, unaudited)
- Together AI story: CSAT "roughly doubled (2x)", no before/after scores; average response time fell 75% to under 10 seconds; target sub-10-second; on Mother's Day Zia "served over 80,000 customers" with peaks above 1,000 messages per minute; no final containment percentage; no cost figure.
- MongoDB story (as of January 2026): "more than 15 million" conversations per month; "85%" average query resolution rate; human-agent productivity up 40%; support cost down from US$20M to "$9 million annually" ("reduce support costs by 55%", headline $11M).
- Conflict note: a search result indicated Nugget's own case study reports a 25% CSAT improvement; I did not fetch it, so no figure is taken from it. Treat 2x CSAT as unreconciled.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Define resolution/containment precisely (resolved vs deflected vs abandoned); a bot can show high "resolution" while users give up, as press complaints about Swiggy and Zomato bots suggest (search-result summary only, not read in full).
- LLM-only escalation decisions were unstable (80% vs 50% daily containment); a deterministic policy layer on top of the model is a transferable design lesson.
- Report latency and cost alongside quality; model-size routing (70B for intent, 8B for generation) is a standard cost lever.
- Without a randomised holdout, a before/after CSAT comparison is confounded; ask what the control was.

### 11. Source Links
- https://www.together.ai/customers/zomato — Together AI, Zomato support bot Zia (adapted from Fifth Elephant 2024 talk; date ND; fetched; vendor-published)
- https://www.mongodb.com/company/blog/innovation/zomato-ai-solution-nugget-reduces-support-costs — MongoDB, Zomato Nugget (March 24, 2026; fetched; vendor-authored)
- https://arpitbhayani.me/videos/swiggy-chatbot-system-design/ — Arpit Bhayani, Swiggy chatbot design (date ND; fetched; external analysis, not Swiggy)
- https://arxiv.org/html/2507.05788v1 — Rajasekar et al. (Flipkart US R&D Center), "Flippi: End To End GenAI Assistant for E-Commerce" (July 8, 2025; fetched). Pre-purchase shopping assistant: 8-intent DistilBERT router with test accuracy 94.89% (final coarse intent accuracy "approximately 97%"); post-purchase issues are only routed to existing support channels. Not a support-automation case; listed as a Flipkart alternative considered.

---

## Case Study 30 — Marketplace winner selection (Buy Box) and seller-quality signals: an external audit of Amazon.in and other Amazon sites

**Priority:** ★★ Good to have — Buy Box and seller quality: auditing a ranking algorithm from outside. **Notebook:** `cs30_buy_box_seller_quality.ipynb` (⏳ notebook pending)

**Company:** Amazon (India marketplace, plus US, Germany, France), studied by Indian and German academics
**Industry:** Ecommerce marketplace
**Business Area:** Seller ranking, default-offer (Buy Box) selection, seller performance metrics
**Problem Type:** Algorithm audit (choice architecture), with survey experiments and a surrogate feature-importance model
**Evidence Level:** Medium (B) — peer-reviewed academic audit (CSCW 2024) of the actual Amazon.in Buy Box outcomes; it does not disclose Amazon's algorithm (the authors say they have only partial knowledge of its features). No Flipkart or Meesho seller-scoring method with detail was found.
**Primary Sources:** Abhisek Dash, Abhijnan Chakraborty, Saptarshi Ghosh, Animesh Mukherjee, Krishna P. Gummadi, "Investigating Nudges toward Related Sellers on E-commerce Marketplaces: A Case Study on Amazon", arXiv:2407.01732 (July 1, 2024), ACM CSCW 2024.

**Substitution note:** Flipkart seller tiers (Bronze/Silver/Gold) and Meesho supplier ranking appeared only in seller-service blogs and unofficial guides in search results; none was fetched, and no Flipkart/Meesho paper or engineering post was found. The Meesho RHP coverage (MediaNama) only says Meesho delisted over 2 lakh products in September-November 2023 for poor quality and lists seller quality as a risk. CCI Director General findings on preferred sellers (reported by Reuters via secondary outlets) were seen only in search summaries, not fetched, and are not used as fact. Everything below is about Amazon's observable behaviour, not Amazon's internal model.

### 1. Business Problem
"When multiple sellers offer to sell the same product, the marketplace helps a customer in selecting an offer ... through a default offer selection algorithm" (the Buy Box) and by showing seller performance metrics. The paper asks whether this choice architecture nudges customers toward "Related Sellers": Amazon itself (US/DE/FR), special merchants (Cloudtail India and Appario Retail in India), and sellers using Amazon's fulfilment (FBA). Note: Cloudtail stopped selling on Amazon in 2022; data were collected while it was active.

### 2. Business Question
RQ1: how often do Amazon/related sellers win the Buy Box, and do the algorithm's choices match what customers would pick when shown all offers? RQ2: which seller features drive customer choice? RQ3: how do Amazon's review strike-through policies affect reported seller metrics, and how do customers react to corrected metrics?

### 3. Data Available
| Data | Description |
|---|---|
| Buy Box competitions | Scraped from Amazon.in, .com, .de, .fr: 100 most-searched keywords, product pages followed from search results, data collected over two weeks; each competition is a (product, timestamp) pair |
| India dataset size | 20,553 competitions, 2,766 distinct sellers (Table 3) |
| Seller feedback | Feedback for 1,000 active sellers across the four marketplaces, to recompute metrics including struck-through reviews |
| Survey 1 | 200 Prolific participants (50 per country, approval rate 98% or higher); 60 products (15 per marketplace) where special merchants won the Buy Box without the lowest price; top-4 offers shown; India: 750 evaluations |
| Survey 2 | 100 Prolific participants on understanding and fairness of strike-through |
| Survey 3 | 50 Indian participants per treatment setting (control and three treatments) |

### 4. Data Science Approach
1. Scrape Buy Box outcomes over time and compute how often Amazon or its special merchants win ("% Buy Box won"), and how often they win "out of position" (when not the lowest-price offer).
2. Survey 1: show people the top-4 offers with all features and record first-preference votes; compare with the algorithm's winner.
3. Fit a random forest regression on first-preference votes to rank feature importance (price, delivery option, average rating, percentage positive feedback, number of ratings).
4. Recompute seller metrics from raw feedback including reviews that Amazon struck through; compare with Amazon's reported metrics.
5. Survey 3 treatments (India): (T1) hide number of ratings, (T2) show rectified metrics without number of ratings, (T3) show rectified metrics with number of ratings; compare first-preference shares with control.

### 5. Statistical Analysis
Documented: comparison of proportions across control and treatment survey arms (first-preference vote shares); descriptive distributions of seller metrics (box plots) with and without struck-through reviews; counterfactual survey design (treatment arms). Formal hypothesis tests and p-values: not extracted (ND).

### 6. Machine Learning
- **Model(s):** Random forest regression as a descriptive surrogate of respondent choices (not Amazon's algorithm).
- **Target variable:** Respondent first-preference vote.
- **Features:** Relative price, delivery option, average rating, percentage positive feedback, number of ratings.
- **Validation approach:** ND (used for feature-importance ranking, not prediction).
- **Metrics:** Feature-importance ranking. Amazon's actual Buy Box model, features and metrics: ND (proprietary; the authors state partial knowledge only).

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Data collection | Custom web scraper |
| Surveys | Prolific crowdsourcing platform |
| Modelling | Random forest regression (library ND) |

### 8. Business Decision
Not a company decision; this is an external audit. The documented platform design is: default offer chosen by a proprietary algorithm; offer listing page sorted by price plus delivery charge; seller metrics shown (average rating, percentage positive feedback over 12 months, lifetime number of ratings); a policy allowing Amazon to strike through some negative feedback for related (Amazon-fulfilled) sellers. The authors raise fairness concerns; Amazon "has consistently denied the presence of any systemic preferential treatments" (as the paper reports).

### 9. Business Impact
These are audit findings, not company impact:
- Buy Box win rate of Amazon and special merchants (Table 4): India 87.74% (29.15% out of position), USA 86.12% (26.39%), Germany 85.35% (13.91%), France 79.98% (12.45%).
- India survey: of 750 evaluations, 407 (about 54%) gave first preference to the special merchants, whereas they won the Buy Box in nearly 90% of competitions.
- India, strike-through: 74.13% of low-rated reviews for Amazon-fulfilled sellers were struck through (97,603 of 131,664). Example: Appario Retail's reported positive feedback of 87% falls to 61% when struck-through reviews are included.
- India treatments: special-merchant first-preference share fell from about 54% (control) to 14.5% when number of ratings was hidden (T1), 6.93% with rectified metrics and no number of ratings (T2), and 28.53% with rectified metrics plus number of ratings (T3). Abstract: preference for related sellers is "almost halved" with rectified metrics.
- Number of ratings was the most influential feature in India (random-forest ranking), possibly reflecting scale rather than service quality (authors' interpretation).
- Seller conversion, GMV or return-rate effects of the Buy Box: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Black-box audits can still be rigorous: scrape outcomes, build counterfactual surveys, and fit a surrogate model to learn which features matter.
- Un-normalised features (lifetime number of ratings) favour incumbents; a well-designed seller score should normalise for scale and use recent, outcome-based metrics (late shipment, cancellation, return and defect rates). This is a design inference, not something this paper tests.
- Metric integrity matters: if bad outcomes are filtered from the metric, the score stops measuring quality.
- Winner-selection is a ranking problem with fairness constraints and exploration (rotation among eligible sellers); the paper raises skewed winner distribution as a concern.

### 11. Source Links
- https://arxiv.org/abs/2407.01732 and https://arxiv.org/pdf/2407.01732 — Dash et al., "Investigating Nudges toward Related Sellers on E-commerce Marketplaces: A Case Study on Amazon" (July 1, 2024; CSCW 2024; fetched PDF)
- https://medianama.com/2025/12/223-meesho-ipo-rhp-filing-5421-crore/ — Meesho RHP coverage, 2 lakh products delisted for quality (December 2025; fetched)

---

---

# MASTER COMPARISON TABLE

| # | Priority | Case | Evidence |
|---|---|---|---|
| 1 | ★★★ | Swiggy's multi-stage ETA and delivery-time promise models (cart pSLA and tracking-screen ETA) | Strong |
| 2 | ★★ | Zomato's food preparation time (FPT) prediction and how prep time drives rider dispatch (with Swiggy JIT dispa | Strong |
| 3 | ★★ | Swiggy Instamart dark-store demand planning: forecasting for availability versus wastage (plus dark-store pick | Strong |
| 4 | ★★ | Swiggy Instamart (and food delivery) delivery-executive assignment, batching and just-in-time dispatch | Strong |
| 5 | ★★ | Myntra (Flipkart group) customer promise date: predicting delivery dates with breach control | Strong |
| 6 | ★ | Swiggy q-commerce address correction: location inaccuracy classifier and geocoder | Strong |
| 7 | ★★★ | Instamart quick-commerce demand forecasting: availability de-biasing, SKU grouping and TimesFM | Medium |
| 8 | ★★ | Marketplace price monitoring / discount efficacy on Flipkart (substitution: only an external analysis is publi | Weak |
| 9 | ★★ | Delivery-fee / surge design in food delivery (Weak; only problem framing and a simulated academic study) | Weak |
| 10 | ★ | Sale-event (Big Billion Days) planning at Flipkart (Weak: outcomes published, methods not) | Weak |
| 11 | ★★★ | Myntra: forecasting demand for new fashion items to guide assortment and buying | Strong |
| 12 | ★★ | Hierarchical probabilistic forecasting for supply chain: Amazon Forecasting Science (CLOVER), with Flipkart CP | Medium |
| 13 | ★★ | Hinglish Search Query Translation at Flipkart | Medium |
| 14 | ★★ | ShopLook: Recommending Similar Products for Every Garment in a Model Image at Myntra | Strong |
| 15 | ★★★ | Item-to-Item Collaborative Filtering at Amazon.com | Strong |
| 16 | ★★ | Dish Search and Query Understanding at Swiggy | Strong |
| 17 | ★★★ | Unified Ranking of Sponsored and Organic Products on Flipkart "Similar Products" | Strong |
| 18 | ★★ | Cold-Start Feeds for New Users at Meesho (with exploration evidence from Myntra) | Medium |
| 19 | ★★★ | Switchback vs A/B experimentation in two-sided marketplaces (Cabify documented; Flipkart's early A/B framework | Medium |
| 20 | ★★★ | Predicted lifetime value (pLTV) of new customers for bid optimisation at Swiggy | Medium |
| 21 | ★★ | Zomato Gold relaunch (2023) and Flipkart Plus tiering as membership design | Weak |
| 22 | ★★★ | Real-time personalised coupon allocation under a budget (Meituan Bike; substitute for Indian companies) | Strong |
| 23 | ★ | Meesho notification volume, relevance and send-time experiments | Weak |
| 24 | ★★ | Marketing mix modelling plus geo-lift experiments at Honasa Consumer | Weak |
| 25 | ★★★ | Predicting Return-to-Origin (RTO) on cash-on-delivery orders at checkout using order history plus public socia | Strong |
| 26 | ★★ | Reducing size-related returns with a size and fit predictor that reads customer reviews | Strong |
| 27 | ★★ | Detecting rating fraud (fake and defaming reviews) on a marketplace with a Bayesian anomaly model (BIRDNEST) | Strong |
| 28 | ★ | Filling missing product attributes automatically to improve catalogue quality (multimodal generative extractio | Medium |
| 29 | ★★ | Automating food-delivery customer support with LLM agents and measuring containment, latency and CSAT (Zomato  | Medium |
| 30 | ★★ | Marketplace winner selection (Buy Box) and seller-quality signals: an external audit of Amazon.in and other Am | Medium |
