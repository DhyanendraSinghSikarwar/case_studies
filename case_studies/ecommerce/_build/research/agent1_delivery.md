# Agent 1 research: delivery, dispatch, dark-store and logistics case studies

Compiled 2026-10-17. Conventions: "ND" = Not publicly disclosed (in the sources I read). "Company claim" = the number is the company's own statement and was not independently verified. Direct access to bytes.swiggy.com and Medium was blocked from my environment, so Swiggy Bytes posts were read through Internet Archive (web.archive.org) snapshots of the original pages; the canonical URL is given and the snapshot is noted. Where a fetched copy had garbled characters (e.g. a unit symbol) I say so rather than guess.

---

## Case R1 — Swiggy's multi-stage ETA and delivery-time promise models (cart pSLA and tracking-screen ETA)
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

## Case R2 — Zomato's food preparation time (FPT) prediction and how prep time drives rider dispatch (with Swiggy JIT dispatch)
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

## Case R3 — Swiggy Instamart dark-store demand planning: forecasting for availability versus wastage (plus dark-store picking batching)
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

## Case R4 — Swiggy Instamart (and food delivery) delivery-executive assignment, batching and just-in-time dispatch
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

## Case R5 — Myntra (Flipkart group) customer promise date: predicting delivery dates with breach control
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

## Case R6 — Swiggy q-commerce address correction: location inaccuracy classifier and geocoder
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

## Notes for the notebook author

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
