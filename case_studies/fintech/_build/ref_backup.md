# How Real Indian Fintech Data Scientists Solved Real Business Problems

**30 documented case studies across 19 organisations: payments, fraud, lending, collections, personalisation, insurance and wealthtech**

*Research compiled: 1 October 2026. All facts come from the cited public sources. "Not publicly disclosed" (ND) means the sources do not state the detail. "Learning notes" and the Data Scientist Thinking section are interpretation and are labelled as such.*

---

## Executive Summary

### What was researched
- I searched company engineering blogs (Razorpay, PhonePe, Juspay, Cashfree, Paytm Labs, Navi, Groww, Zerodha, Angel One), arXiv, SSRN, HasGeek/Fifth Elephant, cloud-vendor case studies (AWS, Google Cloud, Microsoft, Cloudera, web.dev), IPO filings (DRHP/RHP) and business press (Business Standard, Inc42, YourStory, CIO.com, AIM).
- Four parallel research streams covered payments, lending, wealth/insurance, and banks/consumer fintech. That was about 160 searches and over 120 page fetches. Key claims were then re-checked against the primary page.

### Organisations covered (19)
Juspay, Razorpay, Cashfree Payments, PhonePe, Paytm (Paytm Payments Bank / Paytm Labs), BharatPe, MobiKwik, Simpl, Navi, Lendingkart, Kissht (OnEMI), Credgenics, HDFC Bank, Axis Bank, YES Bank, Reserve Bank Innovation Hub (RBIH), ICICI Lombard, Policybazaar, Zerodha. One more case is an ISB/IIMB academic study on an unnamed Indian fintech lender.

### Problem types found

| Area | Cases |
|---|---|
| Payments (routing, success rate, anomaly detection, merchant risk) | 1–5 |
| Fraud & financial crime (P2P fraud, mule accounts, real-time screening) | 6–10 |
| Lending & credit (underwriting, alt-data scoring, limits, collections) | 11–19 |
| Customer & product analytics (recommendation, personalisation, nudges) | 20–23 |
| Insurance (claims CV, claims adjudication, sales conversion, lead qualification) | 24–28 |
| Wealthtech / broking (behavioural risk intervention) | 29 |
| Operations (support automation) | 30 |

### How data science was used
- **Supervised classification** is the most common pattern: fraud/not-fraud, mule/not-mule, default/not-default, convert/not-convert. Tree ensembles (Random Forest, XGBoost) are the only algorithms named in production write-ups.
- **Online decisioning / bandits** for payment routing (Juspay), with live A/B comparison against rule-based routing.
- **Ranking with business utility**: PhonePe ranks by *propensity × LTV*, not by propensity alone.
- **Bayesian methods** with simple, interpretable formulas (Paytm homepage).
- **Foundation models**: Razorpay's Vulcan pretrains one model on payment records and fine-tunes heads for 4 decisions.
- **Computer vision, OCR and LLMs** for documents and images in insurance claims.
- **Rules + ML hybrids** almost everywhere. ML scores feed a rule engine that applies the business action.

### Common patterns across teams
1. **The baseline is always a rule or a human process.** Impact is reported as improvement over it (Paytm mule: 20%/50% → 65.1%/74.1% precision/recall).
2. **Label quality is the hard part.** PhonePe had to separate *fraud* from *disputes* before modelling.
3. **Latency limits shape the model.** Decisions must fit in 5 ms (Juspay), 70–80 ms (Simpl) or 20 ms (NPCI), so feature stores and pre-computed aggregates matter as much as the algorithm.
4. **Evaluation uses business metrics.** Teams report success rate, GMV recovered, fraud rate, complaint volume, approval rate, TAT, loss rate and collection efficiency, not accuracy.
5. **Out-of-time validation** is explicit where documented (Razorpay Vulcan; Lendingkart's periodic statistical tests).
6. **Public disclosure of model metrics is rare.** No production source in this set publishes KS or Gini. Only the academic paper (Case 13) and Paytm (Case 8) give classification metrics.

### Evidence legend

| Level | Meaning | Shown as |
|---|---|---|
| A | Company or named employee described the project | **Strong** |
| C | Paper / conference talk by company team (or academic paper on company data) | **Strong** |
| B | Credible external source on the actual implementation (cloud-vendor case study, media interview with a named executive, IPO-filing summary) | **Medium** |
| D | Generic or vendor marketing with little method detail | **Weak / partially documented** |

<!-- PRIORITY-INDEX-START -->
### Priority guide (added by the notebook series)

How to read the stars: **★★★ Must-visit** = core statistics/ML that Indian fintech teams use every day; study these first. **★★ Good to have** = valuable technique, narrower use or weaker evidence. **★ Optional** = mostly deep-learning / LLM / speech engineering; the notebooks focus on how to *evaluate* such systems statistically. Ratings are my interpretation, not part of the sources.

| Case | Priority | Why | Notebook | Status |
|---|---|---|---|---|
| 1 | ★★★ Must-visit | Binomial SR testing, multiple testing, bandits and ₹ GMV: the core payments-DS toolkit | `01_payment_routing_success_rate.ipynb` | ✅ |
| 2 | ★★ Good to have | Funnel/stage decomposition: simple but used weekly by every payments team | `cs02_card_decline_funnel.ipynb` | ✅ |
| 3 | ★★ Good to have | Calibration vs ranking, fixed-alert-budget and out-of-time evaluation; the foundation model itself is hard to reproduce | `cs03_foundation_model_evaluation.ipynb` | ✅ |
| 4 | ★★★ Must-visit | Seasonality-aware anomaly detection and alert-fatigue economics: every ops/risk team needs it | `cs04_adaptive_anomaly_alerts.ipynb` | ✅ |
| 5 | ★ Optional | LLM-agent automation; the data-science part is measuring agreement with analysts | `cs05_merchant_review_automation.ipynb` | ⏳ |
| 6 | ★★★ Must-visit | Label engineering + real-time imbalanced fraud classification + reinstatement-rate KPI | `cs06_upi_p2p_fraud.ipynb` | ✅ |
| 7 | ★★ Good to have | Velocity and graph features, rules + anomaly scores per business line | `cs07_velocity_graph_fraud_screening.ipynb` | ⏳ |
| 8 | ★★★ Must-visit | Textbook imbalanced classification: class weights, PR curves, thresholds → action tiers | `cs08_mule_account_detection.ipynb` | ✅ |
| 9 | ★★ Good to have | Typology-first modelling and alert precision as the headline metric | `cs09_mule_typology_alert_precision.ipynb` | ⏳ |
| 10 | ★★ Good to have | Graph community detection for fraud rings and the cost to good users | `cs10_bnpl_fraud_rings_graph.ipynb` | ⏳ |
| 11 | ★★★ Must-visit | Full credit-scorecard lifecycle: WoE/IV, logistic, KS/Gini, calibration, PSI, cut-offs | `02_msme_credit_scoring.ipynb` | ✅ |
| 12 | ★★★ Must-visit | Collections as resource allocation: bucket-wise PD and channel policy | `cs12_collections_bucket_scorecards.ipynb` | ✅ |
| 13 | ★★★ Must-visit | Comparing data sources by AUC (DeLong) and reject inference for thin-file lending | `cs13_alternate_data_credit_scoring.ipynb` | ✅ |
| 14 | ★★ Good to have | Segmented models vs one global model; top/bottom bad-rate ratio | `cs14_segmented_underwriting.ipynb` | ⏳ |
| 15 | ★★ Good to have | Behavioural score → pre-approval and credit-limit assignment | `cs15_bnpl_limit_assignment.ipynb` | ⏳ |
| 16 | ★★ Good to have | Merchant cash-flow capacity modelling + fuzzy KYC name matching | `cs16_merchant_qr_lending.ipynb` | ⏳ |
| 17 | ★★ Good to have | Non-inferiority testing: 'same delinquency, 10 seconds instead of days' | `cs17_preapproved_pl_noninferiority.ipynb` | ⏳ |
| 18 | ★★ Good to have | Custom score vs bureau: 'better on what metric?' (Gini, KS, bad rate at fixed approval) | `cs18_custom_score_vs_bureau.ipynb` | ⏳ |
| 19 | ★★★ Must-visit | Propensity vs uplift for collections: call the customers a call actually changes | `cs19_collections_propensity_uplift.ipynb` | ✅ |
| 20 | ★★★ Must-visit | Expected-value ranking (propensity × LTV) validated by A/B tests vs random and rules | `cs20_propensity_ltv_ranking.ipynb` | ✅ |
| 21 | ★★ Good to have | Simple Bayesian personalisation; interpretable baseline for recommenders | `cs21_bayesian_trend_personalisation.ipynb` | ⏳ |
| 22 | ★★★ Must-visit | Causal campaign measurement: SRM, CUPED, power, heterogeneity, uplift, ROI | `03_nudge_campaign_ab_test.ipynb` | ✅ |
| 23 | ★ Optional | Transaction categorisation (text classification); a foundation for other models | `cs23_transaction_purpose_classification.ipynb` | ⏳ |
| 24 | ★ Optional | Computer vision; the DS part is validating 'fit for purpose' accuracy and triage | `cs24_motor_inspection_cv_validation.ipynb` | ⏳ |
| 25 | ★ Optional | OCR + LLM decision support; the DS part is measuring productivity and agreement | `cs25_claims_copilot_evaluation.ipynb` | ⏳ |
| 26 | ★★ Good to have | Observational vs causal channel comparison (self-selection, propensity matching) | `cs26_chat_conversion_causal.ipynb` | ⏳ |
| 27 | ★ Optional | Speech analytics; the DS part is intent-frequency analysis and dialler efficiency | `cs27_call_analytics_dialler.ipynb` | ⏳ |
| 28 | ★ Optional | Speed-to-lead: how contact delay erodes conversion; capacity-constrained routing | `cs28_speed_to_lead.ipynb` | ⏳ |
| 29 | ★★ Good to have | Pre/post vs difference-in-differences and interrupted time series | `cs29_penny_stock_nudge_causal.ipynb` | ⏳ |
| 30 | ★ Optional | Intent classification + resolution rate together with CSAT | `cs30_support_automation_resolution.ipynb` | ⏳ |
<!-- PRIORITY-INDEX-END -->

---

# PART A — PAYMENTS

## Case Study 1 — Maximising Payment Success Rate with Dynamic Gateway Routing

**Priority:** ★★★ Must-visit — Binomial SR testing, multiple testing, bandits and ₹ GMV: the core payments-DS toolkit. **Notebook:** `01_payment_routing_success_rate.ipynb` (✅ notebook built)

**Company:** Juspay
**Industry:** Payments orchestration
**Business Area:** Payments / transaction success
**Problem Type:** Online decision optimisation (multi-armed bandit + feedback control)
**Evidence Level:** Strong (C: arXiv paper by Juspay authors; A: Juspay blog; open-source code)
**Primary Sources:** arXiv 2510.16735 (Oct 2025); Juspay blog (Jan 2025); GitHub juspay/decision-engine

### 1. Business Problem
Merchants route each payment to one of several payment gateways (PGs). Static rule-based routing fails to adapt when a gateway degrades. Pushing all traffic to the "best" gateway starves the others of data, so the team cannot tell when they recover.

### 2. Business Question
Which gateway should *this* transaction go to, right now, to maximise the probability of success? And how fast can a gateway outage be detected and routed around?

### 3. Data Available

| Data | Description |
|---|---|
| Transaction outcomes | Success/failure per transaction, per gateway |
| Gateway health | Latency, downtime signals |
| Routing dimensions | Merchant ID, platform, payment instrument, card network, card BIN |

### 4. Data Science Approach
Business problem → sliding-window success rate (SR) per gateway × dimension → statistical comparison of gateways → explore/exploit allocation → feedback controller for downtime → live comparison vs rule-based routing → real-time deployment in the orchestrator.

### 5. Statistical Analysis
- SR is modelled as a **binomial proportion**, approximated as normal, and gateways are compared with **Z-scores**. The worked example uses about 1,104 transactions in a 2-hour window.
- **Exploration traffic** of 5–10% keeps estimates fresh for every gateway.
- The open-source engine supports **A/B testing with significance testing**.
- A toy example in the paper: two gateways at about 80% and 81% SR give 80.655% under optimised allocation vs 80.5% under random allocation.

### 6. Machine Learning
- **Model(s):** Non-stationary **multi-armed bandit** with delayed feedback, plus RL. A **control-theoretic (PID-inspired) feedback loop** with an exponentially decaying health score handles downtime.
- **Target variable:** Transaction success (binary).
- **Features:** Gateway × dimension SR windows, latency, health.
- **Training approach:** Online, continuously updated.
- **Validation approach:** 21-day production comparison against rule-based routing.
- **Metrics:** Success rate; time to detect downtime; GMV recovered.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Programming | Rust (open-source decision engine) |
| Database | Redis, ClickHouse, MySQL / Postgres / CockroachDB |
| Processing | Kafka |
| MLOps / Infra | Kubernetes |
| Cloud | ND |

### 8. Business Decision
Juspay offers dynamic (score-based) ordering inside its Payment Orchestrator alongside merchant-controlled rule-based routing. The blog notes that "95%+ merchants use rule-based ordering", so the ML route is an option merchants choose, not a forced default.

### 9. Business Impact
- "Improvement of up to **1.15%** in success rate over traditional rule-based routing." 21-day average: **83.19%** dynamic vs **82.60%** rule-based.
- About 2% gain in UPI and **up to 7%** in some card categories.
- In one 2.5-hour outage, about 8,000 transactions were rerouted, recovering about **$15,000 GMV** for a single merchant. Downtime was detected "within a minute".
- Decision latency of about 5 ms.

### 10. What a Data Scientist Can Learn *(interpretation)*
- At payment-scale volumes, a 1% SR gain is large money. Small effects need correct **binomial statistics**, not eyeballing.
- When your own decisions change the data you collect (starvation), you need **exploration**. That is the core idea behind bandits.
- Report impact as **GMV recovered**, which a business stakeholder understands immediately.

### 11. Source Links
- Agrawal & Patil, "A Control-Theoretic Approach to Dynamic Payment Routing for Success Rate Optimization", arXiv:2510.16735, Oct 2025 — https://arxiv.org/abs/2510.16735
- Juspay blog, "Juspay Orchestrator and Merchant-Controlled Routing Engine", Jan 2025 — https://juspay.io/blog/juspay-orchestrator-and-merchant-controlled-routing-engine
- Code — https://github.com/juspay/decision-engine

---

## Case Study 2 — Diagnosing Card Declines and Splitting Authentication from Authorisation

**Priority:** ★★ Good to have — Funnel/stage decomposition: simple but used weekly by every payments team. **Notebook:** `cs02_card_decline_funnel.ipynb` (✅ notebook built)

**Company:** Cashfree Payments
**Industry:** Payment gateway
**Business Area:** Payments / success rate
**Problem Type:** Diagnostic analytics (root-cause EDA) → routing policy
**Evidence Level:** Strong (A), but light on detail
**Primary Sources:** Cashfree blog, Rini Rafi, 1 Apr 2025; Cashfree FlowWise docs

### 1. Business Problem
A food-delivery client routed card traffic across two processors with similar volumes but different success rates. The cheaper processor had the lower SR.

### 2. Business Question
*Where* in the card flow does the weaker processor lose transactions, and can the flow be split to get the best of both?

### 3. Data Available

| Data | Description |
|---|---|
| Transaction logs per processor | Outcome by stage: authentication (3DS/OTP) vs authorisation (issuer approval) |
| Volume split | Comparable volumes on both processors |

### 4. Data Science Approach
Business problem → stage-wise funnel decomposition → comparison of failure rates by stage → hypothesis: the gap is authentication-driven → policy change. FlowWise docs describe the production mechanism: SR-based routing over the "last 15 or 30 minutes", threshold fallback (e.g., 70%) and weighted splits.

### 5. Statistical Analysis
Funnel / stage-wise comparison of failure proportions. EDA finding: Processor 2's gap was due to "higher authentication failures", while authorisation declines were about equal. No formal test is disclosed.

### 6. Machine Learning
- **Model(s):** None. This is an analytics-driven decision.
- **Target / Features / Validation:** ND.
- **Metrics:** Success rate.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Programming / DB / ML / Cloud | ND |
| Product | Cashfree FlowWise routing |

### 8. Business Decision
Use Processor 1 for **authentication** and the cheaper Processor 2 for **authorisation**.

### 9. Business Impact
"**2% increase in success rate**." Cost impact: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Not every problem needs a model. **Decomposing a funnel metric into stages** often finds the fix.
- Always ask "*which stage* fails?" before asking "*which provider* is better?"

### 11. Source Links
- Cashfree blog, "Reduce card declines via smart routing", 1 Apr 2025 — https://www.cashfree.com/blog/reduce-card-decline-via-smart-routing/
- FlowWise dynamic routing docs (undated) — https://www.cashfree.com/docs/payments/flowwise/routing/dynamic-routing

---

## Case Study 3 — One Foundation Model for Routing, Fraud, COD Risk and Checkout Ranking

**Priority:** ★★ Good to have — Calibration vs ranking, fixed-alert-budget and out-of-time evaluation; the foundation model itself is hard to reproduce. **Notebook:** `cs03_foundation_model_evaluation.ipynb` (✅ notebook built)

**Company:** Razorpay
**Industry:** Payment gateway
**Business Area:** Payments, fraud, e-commerce risk, checkout UX
**Problem Type:** Self-supervised representation learning + task-specific heads
**Evidence Level:** Strong (A: Razorpay blog by named authors); impact figures from launch press (Inc42)
**Primary Sources:** Razorpay blog, 10 Sep 2026; Inc42, 18 Aug 2026

### 1. Business Problem
Razorpay had separate decision problems, each needing its own model and data pipeline:
- Millisecond routing.
- Fraud patterns that move across merchants.
- Cash-on-delivery (COD) parcel rejection (return-to-origin, RTO).
- Ordering payment methods at checkout.

### 2. Business Question
Can one shared representation of a payment improve all four decisions?
- Which route succeeds?
- Is this payment fraudulent?
- Will this parcel be accepted?
- Which method will this shopper complete with?

### 3. Data Available

| Data | Description |
|---|---|
| Payment records | Payment method, merchant, issuer, credentials, geography, time |
| Scale (Inc42) | "3 trillion data points across 4 billion payments"; "3,000 signals per transaction" |
| Outcome labels | Route success; fraud loss/dispute (confirmed weeks later); parcel accepted/returned; checkout completion |

### 4. Data Science Approach
- **Data prep:** Direct identifiers (names, emails, phone numbers, account numbers) are removed. Categorical fields become **hashed tokens**, and each payment is treated as a **set of fields** (unordered).
- **Pretraining:** Self-supervised **Masked-Field Prediction**: hide fields and predict them from the rest.
- **Fine-tuning:** Task heads (routing: recent-context encoder + fusion + calibration).
- **Evaluation:** Out-of-time, per payment flow.

### 5. Statistical Analysis
- **Calibration** is evaluated separately from ranking.
- Fraud models are compared at **fixed alert volumes**, so a better model must catch more fraud without adding analyst workload.
- Formal hypothesis tests: ND.

### 6. Machine Learning
- **Model(s):** **Set Transformer** backbone; task-specific heads.
- **Target variable:** Per task (see table above).
- **Features:** Payment fields as tokens.
- **Training approach:** Self-supervised pretraining → supervised heads.
- **Validation approach:** "Train on the past… test on later traffic… inspect the slices."
- **Metrics:** Ranking quality, calibration, fraud caught at fixed alert volume, SR.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Cloud / Compute | AWS, NVIDIA (per launch coverage) |
| Other | ND |

### 8. Business Decision
Vulcan powers real-time routing, pre-authorisation fraud checks, COD risk scoring and checkout method ordering in Razorpay products.

### 9. Business Impact
As reported by Inc42 from Razorpay's launch:
- "**8–10%** improvement in payment success rates"
- "**8X** increase in international card frauds detected"
- "**5X** rise in fraudulent/disputed transactions identified"; the blog adds this was "without an increase in alerts"
- "**40%** more shoppers seeing preferred UPI app at checkout"

The blog notes early results applied to existing merchant traffic.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Fraud labels arrive weeks late. **Out-of-time validation** is mandatory, or leakage will flatter the model.
- Comparing fraud models at a **fixed alert budget** builds the operations team's capacity into the metric.

### 11. Source Links
- Razorpay blog, "Vulcan: how Razorpay built a foundation model for payment decisions", 10 Sep 2026 — https://razorpay.com/blog/vulcan-how-razorpay-built-a-foundation-model-for-payment-decisions
- Inc42, 18 Aug 2026 — https://inc42.com/buzz/razorpay-launches-ai-foundation-model-vulcan-to-expedite-digital-payments/

---

## Case Study 4 — Replacing Static Alert Thresholds with Adaptive Real-Time Anomaly Detection

**Priority:** ★★★ Must-visit — Seasonality-aware anomaly detection and alert-fatigue economics: every ops/risk team needs it. **Notebook:** `cs04_adaptive_anomaly_alerts.ipynb` (✅ notebook built)

**Company:** Razorpay
**Industry:** Payment gateway
**Business Area:** Operations / payment health / fraud signals
**Problem Type:** Time-series anomaly detection and alerting
**Evidence Level:** Strong / Medium (AWS Big Data Blog co-written with Razorpay)
**Primary Sources:** AWS Big Data Blog, 13 Jul 2026

### 1. Business Problem
Static thresholds could not scale to millions of merchants. They left blind spots, caused alert fatigue and cost about $500K a year.

### 2. Business Question
For every merchant × gateway combination, is the current success rate, latency or velocity *abnormal given its own normal pattern* (time of day, day of week, holidays)?

### 3. Data Available

| Data | Description |
|---|---|
| Event streams | ~5 billion events/day |
| Metrics monitored | Success rates, latency regressions, card testing, velocity abuse, gateway × merchant degradation |
| Settlement/disbursement events | Via change-data-capture |

### 4. Data Science Approach
- Build **calendar-aware adaptive baselines** for each series.
- Compare live streams against those baselines.
- Use **complex event processing** for sequence patterns. Example: five declines then a success suggests card testing.
- Rules are written in a declarative DSL (AdaDSL) that runs in both batch and streaming. ML models can supply thresholds.

### 5. Statistical Analysis
Seasonal / calendar baselining (day-of-week, time-of-day, holiday effects). The exact statistical method is ND.

### 6. Machine Learning
- **Model(s):** ML-supplied thresholds; algorithms ND.
- **Target / Validation:** ND.
- **Metrics:** Detection latency, false-positive volume, cost, uptime.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Processing | Amazon MSK (Kafka), Apache Flink |
| Database | ClickHouse (baselines), Aurora MySQL + Debezium CDC |
| Cloud | AWS |

### 8. Business Decision
Razorpay retired static threshold alerting in favour of the adaptive platform for merchant/gateway health and fraud-pattern alerts.

### 9. Business Impact
- Detection in under 30 seconds (previously 1–2 minutes)
- About **80%** cost reduction
- **>90%** reduction in false positives
- 99.99% uptime

### 10. What a Data Scientist Can Learn *(interpretation)*
- "Normal" depends on context. A 2 a.m. drop on Diwali is not the same as a 2 p.m. drop on a Tuesday. **Seasonality-aware baselines** cut false alerts.
- Alert fatigue is a business cost. Measure **false positives per analyst**.

### 11. Source Links
- AWS Big Data Blog, "How Razorpay built real-time anomaly detection with Amazon MSK", 13 Jul 2026 — https://aws.amazon.com/blogs/big-data/how-razorpay-built-real-time-anomaly-detection-with-amazon-msk/

---

## Case Study 5 — Automating Merchant Onboarding Risk Reviews with a Multi-Agent System

**Priority:** ★ Optional — LLM-agent automation; the data-science part is measuring agreement with analysts. **Notebook:** `cs05_merchant_review_automation.ipynb` (⏳ notebook pending)

**Company:** Razorpay
**Industry:** Payment gateway
**Business Area:** Merchant risk / onboarding operations
**Problem Type:** Decision support / automation of manual review (LLM agents + rules)
**Evidence Level:** Strong (A: Razorpay engineering blog)
**Primary Sources:** engineering.razorpay.com, Ankur Singh et al., 17 Dec 2025

### 1. Business Problem
About 12,000 merchant reviews a month at 20+ minutes each, which is about 8,500 analyst-hours a month, and different analysts reached different judgements.

### 2. Business Question
Can a system gather the evidence and make a consistent risk judgement on a new merchant in seconds?

### 3. Data Available

| Data | Description |
|---|---|
| Merchant website | Content, SSL certificate, page load time |
| Domain data | WHOIS |
| Internal | Fraud databases |
| External | Social profiles |

### 4. Data Science Approach
1. A **planner agent** decides what to check.
2. Parallel **fetcher agents** collect data and compress it into JSON summaries.
3. An **analyser agent** combines rules with LLM judgement.

An n8n prototype and a single monolithic agent were tried and dropped.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** LLM-based ReAct agents (Python), combined with rules.
- **Target variable / Validation design:** ND.
- **Metrics:** Accuracy (vs analyst decisions, presumably; the method is ND), latency, token cost.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Programming | Python |
| Other | ND |

### 8. Business Decision
Merchant risk evaluation moved to the agent system, with analysts handling escalations. The exact human-in-the-loop policy is ND.

### 9. Business Impact
- 8–12 seconds per evaluation, against 20+ minutes manually
- Accuracy "99%+", up from 88%
- 60% fewer tokens than the earlier design

### 10. What a Data Scientist Can Learn *(interpretation)*
- Manual-review automation is a capacity problem. Frame the impact in **analyst-hours saved** and **consistency**.
- Ask how "accuracy" was measured and against which ground truth. The source does not say.

### 11. Source Links
- "Meet Bumblebee: the multi-agent AI architecture that changed fraud detection at Razorpay", 17 Dec 2025 — https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51

---

# PART B — FRAUD & FINANCIAL CRIME

## Case Study 6 — Real-Time P2P Fraud Prevention on UPI

**Priority:** ★★★ Must-visit — Label engineering + real-time imbalanced fraud classification + reinstatement-rate KPI. **Notebook:** `cs06_upi_p2p_fraud.ipynb` (✅ notebook built)

**Company:** PhonePe
**Industry:** UPI payments
**Business Area:** Fraud & risk
**Problem Type:** Real-time binary classification
**Evidence Level:** Strong (A: PhonePe tech blog)
**Primary Sources:** tech.phonepe.com, Nipun VK, 28 Jul 2022

### 1. Business Problem
PhonePe handles over 2.5 billion transactions a month. In P2P fraud, money leaves the PhonePe ecosystem instantly, so it cannot be recovered after the fact. Many complaints are **disputes** (e.g., dissatisfaction with a product), not fraud. Blanket rules created too many false positives.

### 2. Business Question
At the moment of payment, before it completes, is this P2P transfer likely to be fraud?

### 3. Data Available

| Data | Description |
|---|---|
| Sender attributes | Demographics, behavioural variables, transaction history |
| Receiver attributes | Same families of variables |
| Transaction attributes | Current transaction details |
| Labels | Reported fraud, cleaned of disputes |

### 4. Data Science Approach
1. **Label engineering:** Reported transactions were segmented, and segments with high potential false positives were removed from the fraud labels.
2. **Modelling:** Several classifiers were tried and tuned on sender, receiver and transaction features.
3. **Operations validation:** An operations team checked flagged cases using risk signals and **calls to senders**.
4. **Batch vs real-time:** Weeks of simulation compared the two.
5. **Deployment:** Real-time, with **pre-filtering** by segment to meet the latency budget.

### 5. Statistical Analysis
Segmentation of complaint labels; precision/recall tracked across iterations. Formal tests: ND.

### 6. Machine Learning
- **Model(s):** "Various classification algorithms were tried." Final algorithm: ND.
- **Target variable:** Fraudulent P2P transaction (disputes excluded).
- **Features:** Sender / receiver / transaction aggregates (real-time and batch).
- **Training approach:** Retrained using feedback and escalations.
- **Validation approach:** Ops-team review plus simulation.
- **Metrics:** Precision, recall; business KPIs below.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Feature store | **Yoda** (real-time aggregates, integrated with ML flow server); **Profile Store** (batch variables) |
| Decision engine | **Kratos** (in-house evaluation engine) |
| Other | ND |

### 8. Business Decision
PhonePe moved from batch *detection* to real-time *prevention*, blocking risky transactions at payment time, and rejected blanket rules.

### 9. Business Impact
- **40%** reduction in fraud rate on consumer-to-consumer transactions
- **38%** reduction in daily fraud complaints (**50%** in the high-value segment)
- About **1%** reinstatement rate for blacklisted users. This is a proxy for false positives: few blocked users turned out to be genuine.

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Define the target carefully.** "Reported fraud" is not fraud. Cleaning labels was a core step.
- **Reinstatement rate** is a smart, cheap false-positive metric that operations already tracks.
- Latency is a design constraint. Pre-compute aggregates in a feature store.

### 11. Source Links
- "Building PhonePe's real-time transaction model to prevent frauds: a journey", 28 Jul 2022 — https://tech.phonepe.com/building-phonepes-real-time-transaction-model-to-prevent-frauds-a-journey/

---

## Case Study 7 — Real-Time Fraud Screening with Velocity, Graph and Anomaly Signals

**Priority:** ★★ Good to have — Velocity and graph features, rules + anomaly scores per business line. **Notebook:** `cs07_velocity_graph_fraud_screening.ipynb` (⏳ notebook pending)

**Company:** Cashfree Payments
**Industry:** Payment gateway
**Business Area:** Fraud & risk
**Problem Type:** Real-time risk scoring (rules + anomaly detection + graph)
**Evidence Level:** Strong (A), but no impact numbers
**Primary Sources:** Cashfree blog, Dipak Bansal, 9 May 2025

### 1. Business Problem
Merchants face UPI collect-request scams, chargeback fraud and promotion abuse, and need screening in real time.

### 2. Business Question
Should this transaction be allowed, challenged or blocked, given who is transacting, from which device and location, how fast, and who they are linked to?

### 3. Data Available (seven signal groups as stated)

| Data | Description |
|---|---|
| Negative lists | Known fraudster email, phone, IP, UPI handle, bank account (including from regulators) |
| Contact intelligence | Disposable / spam phone or email |
| Device intelligence | Device signals |
| Geo / IP | Geolocation, IP |
| Anomaly scores | ML scores on volume, frequency, user and device properties |
| Velocity aggregates | e.g., ">X distinct mobile numbers or devices within Y time" |
| Graph | Links to already-proven risky entities |

### 4. Data Science Approach
1. Feature families (velocity, graph, device).
2. Anomaly scoring.
3. A rule engine tuned by the merchant's line of business and transaction size.
4. Post-processing to cut false positives.
5. A feedback loop that auto-tunes features and thresholds.
6. Human-readable explanations.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** "Advanced anomaly detection algorithms" (not named).
- **Target / Validation / Metrics:** ND.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Processing | Apache Flink, Kafka |
| Database | Graph database (product ND) |
| Scale | Up to 12,000 screenings/second |

### 8. Business Decision
RiskShield is offered as a product that merchants use to allow, review or block transactions under rules for their business line.

### 9. Business Impact
Not publicly disclosed.

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Velocity features** ("how many distinct X in Y minutes") and **graph links** are the workhorse features of payment fraud.
- Rules tuned by business line show that one global threshold rarely fits all merchants.

### 11. Source Links
- "Cashfree RiskShield: fraud prevention tech, part 2", 9 May 2025 — https://www.cashfree.com/blog/cashfree-riskshield-fraud-prevention-tech-part-2/

---

## Case Study 8 — Detecting Mule Bank Accounts with a Class-Weighted Random Forest

**Priority:** ★★★ Must-visit — Textbook imbalanced classification: class weights, PR curves, thresholds → action tiers. **Notebook:** `cs08_mule_account_detection.ipynb` (✅ notebook built)

**Company:** Paytm (Paytm Payments Bank, with the Paytm Labs fraud prevention team)
**Industry:** Payments bank
**Business Area:** Financial crime / AML
**Problem Type:** Imbalanced binary classification
**Evidence Level:** Strong (A: Paytm Labs blog by a named analyst). Note: the post is undated, and the entity is described as "Paytm Bank" with an "India Fraud Prevention" team.
**Primary Sources:** paytmlabs.com/blog (post by "Hana, Cyber Analyst")

### 1. Business Problem
Mule accounts receive and pass on fraud proceeds. The existing detection had "roughly **20% precision and 50% recall**".

### 2. Business Question
Can ML raise recall without losing precision, so the bank can **tier its response**: investigate or limit uncertain accounts, and block high-confidence ones immediately?

### 3. Data Available

| Data | Description |
|---|---|
| Account data | Account-level attributes |
| Transaction data | Transaction behaviour |
| Size | 1.5M accounts train; 700K accounts validation |

Exact feature list: ND.

### 4. Data Science Approach
Problem introduced Jan 2020 → feature engineering with the India Fraud Prevention team → "significant feature pruning" down to **17 features** → algorithm comparison → class weighting → hold-out validation → real-time deployment with a rule engine.

### 5. Statistical Analysis
PR curves and ROC curves were used for threshold selection. Formal tests: ND.

### 6. Machine Learning
- **Model(s):** Random Forest Regressor, Gradient Boosting Classifier and neural networks were tested. **Random Forest Classifier** was chosen.
- **Target variable:** Mule vs non-mule account.
- **Features:** 17 (after pruning).
- **Training approach:** **Class weighting 1:5** (non-mule : mule) to handle imbalance.
- **Validation approach:** Hold-out set of 700K accounts.
- **Metrics:** Precision, recall, PR and ROC curves.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Risk platform | **Maquette** (Paytm Labs real-time risk platform) |
| Rule engine | Integrated with model output |
| Other | ND |

### 8. Business Decision
Model scores drive a tiered response: high scores lead to immediate blocking; medium scores lead to investigation or limits.

### 9. Business Impact
Production precision **65.1%** and recall **74.1%**, against a baseline of about 20% precision and 50% recall.

### 10. What a Data Scientist Can Learn *(interpretation)*
- This is a textbook **imbalanced classification** case: class weights, PR curves, and a baseline expressed in precision and recall.
- **Feature pruning to 17** shows that real-time systems favour small, robust feature sets.
- **Score bands mapped to actions** is how a model becomes an operating policy.

### 11. Source Links
- Paytm Labs blog (mule account detection post; undated) — https://paytmlabs.com/blog/

---
## Case Study 9 — A Central-Bank-Built Model to Flag Mule Accounts Across Banks

**Priority:** ★★ Good to have — Typology-first modelling and alert precision as the headline metric. **Notebook:** `cs09_mule_typology_alert_precision.ipynb` (⏳ notebook pending)

**Company:** Reserve Bank Innovation Hub (RBIH), a subsidiary of RBI. Product: **MuleHunter.AI**
**Industry:** Banking regulation / shared infrastructure
**Business Area:** Financial crime / AML
**Problem Type:** Pattern-based classification of mule accounts (supervised ML)
**Evidence Level:** Medium (B: Business Standard, MediaNama/RTI, official statements)
**Primary Sources:** Business Standard (9 Dec 2024; 1 Aug 2025); MediaNama (30 Dec 2025); ClearingPost (May 2026)

### 1. Business Problem
Money mules caused "53% of the total fraud threats to financial institutions" in 2023. Banks' rule-based systems produced many false positives.

### 2. Business Question
Which accounts at a bank are being used as mules?

### 3. Data Available

| Data | Description |
|---|---|
| Transaction & account datasets | From partner banks |
| Pattern library | "19 distinct patterns of mule account activity", studied with partner banks; a later report says "90 fraud patterns" |

### 4. Data Science Approach
1. Study mule typologies with partner banks.
2. Build AI/ML models on transaction and account data.
3. Pilot with two public sector banks.
4. Roll out across banks.

Architecture: ND.

### 5. Statistical Analysis
Descriptive finding stated by RBI: peak mule activity is **11 PM–1 AM**. Other statistics: ND.

### 6. Machine Learning
- **Model(s):** "AI and machine learning algorithms" (unspecified).
- **Target variable:** Mule account (implied).
- **Metrics:** Alert precision: "90 per cent positive alerts" vs "80 per cent false positives" on competing platforms (Suvendu Pati, CGM, RBI).

### 7. Tools & Technology
ND.

### 8. Business Decision
Announced by Governor Shaktikanta Das on 6 Dec 2024. Adoption:
- 6 banks by Aug 2025 (Canara, PNB, Bank of India, Bank of Baroda, AU SFB, Federal Bank)
- 23 banks by Dec 2025
- 26+ banks by May 2026, plus an MoU with I4C (Indian Cyber Crime Coordination Centre)

### 9. Business Impact
Alert precision as above. RBI declined an RTI request for the number of mule accounts detected.

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Typology-first modelling:** domain experts define the patterns, and the model generalises them.
- The headline business metric was **alert precision**, because it drives investigator workload.

### 11. Source Links
- https://www.business-standard.com/finance/personal-finance/explained-rbi-has-a-new-ai-tool-mulehunter-ai-to-reduce-digital-frauds-124120900250_1.html (9 Dec 2024)
- https://www.business-standard.com/amp/industry/banking/15-more-banks-to-adopt-rbi-s-mulehunter-fraud-detection-tool-by-october-125080101845_1.html (1 Aug 2025)
- https://www.medianama.com/2025/12/223-rti-23-banks-mulehunter-mule-accounts/ (30 Dec 2025)
- https://clearingpost.com/insights/i4c-rbih-mulehunter-ai-banking-fraud-detection-may-2026/ (May 2026)

---

## Case Study 10 — A BNPL ML Platform for Fraud Rings, Underwriting and Repayment Support

**Priority:** ★★ Good to have — Graph community detection for fraud rings and the cost to good users. **Notebook:** `cs10_bnpl_fraud_rings_graph.ipynb` (⏳ notebook pending)

**Company:** Simpl
**Industry:** Buy-now-pay-later / checkout credit
**Business Area:** Fraud, underwriting, collections support
**Problem Type:** Real-time neural scoring + graph community detection
**Evidence Level:** Strong (C: talk by Simpl's Director of Data Science)
**Primary Sources:** TrueFoundry "True ML Talks #5", Sheekha Verma, 6 Aug 2024

### 1. Business Problem
Simpl extends instant checkout credit across 26,000+ merchants. It needs to:
- Stop fraud, including account takeover and identity theft, in real time.
- Set eligibility and spend limits at onboarding.
- Help users who struggle to repay.

### 2. Business Question
- Is this transaction risky?
- What limit should this new user get?
- Which users need reminders or alternative payment plans?

### 3. Data Available

| Data | Description |
|---|---|
| Transaction payload | Current transaction |
| History | One year of user history |
| Identity | Email IDs, phone numbers (batch analysis) |
| Velocity | Real-time velocity and amount monitoring |

### 4. Data Science Approach
- Rules and filters, then ML models, then neural networks, for real-time fraud.
- **Graph ML** to find fraud communities.
- Batch models scheduled in Airflow.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** Neural network combining the current payload with history; **graph ML** for fraud communities.
- **Target / Validation:** ND.
- **Metrics:** Precision–recall trade-off and impact on "good users". No numbers.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Processing | Apache Flink (70–80 ms SLA), Airflow |
| Feature store | DynamoDB |
| ML platform | SageMaker (moving to an in-house platform) |
| Team | 28 data scientists + 16 data engineers |

### 8. Business Decision
Real-time approve/decline at checkout; limits set at onboarding; reminders and alternative payment plans for stressed users.

### 9. Business Impact
Not publicly disclosed.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Fraud rings are invisible at the single-account level. **Graph features** expose them.
- Measure the cost to **good users** (false declines), not just fraud caught.

### 11. Source Links
- https://www.truefoundry.com/blog/machine-learning-platform-simpl (6 Aug 2024)

---

# PART C — LENDING, CREDIT & COLLECTIONS

## Case Study 11 — Cash-Flow-Based MSME Underwriting with XGBoost

**Priority:** ★★★ Must-visit — Full credit-scorecard lifecycle: WoE/IV, logistic, KS/Gini, calibration, PSI, cut-offs. **Notebook:** `02_msme_credit_scoring.ipynb` (✅ notebook built)

**Company:** Lendingkart
**Industry:** MSME digital lending (NBFC)
**Business Area:** Credit risk / underwriting
**Problem Type:** Credit scoring (PD-style classification) + loan-amount assignment
**Evidence Level:** Strong (A: interview with Chief Analytics Officer; company annual report) + Medium (B: CIO.com)
**Primary Sources:** AIM interview with Abhishek Singh (republished on Lendingkart careers site, undated); CIO.com, 14 Sep 2020; Lendingkart Finance Annual Report FY2021

### 1. Business Problem
Most MSMEs lack formal credit ("only 16%" receive it, per AIM). Manual underwriting is slow and expensive. Bureau data is thin for new-to-credit businesses.

### 2. Business Question
From bank statements, GST and other data, how risky is this MSME? How much can it borrow over 1, 2 or 3 years?

### 3. Data Available

| Data | Description |
|---|---|
| Bank statements | Balances, credits/debits, cheque returns |
| GST data | Business turnover signals |
| Bureau & application | Credit history, applicant details |
| Other (CIO.com) | Social media, e-commerce purchases, utility data |

### 4. Data Science Approach
Raw data → **5,000+ derived variables** (CIO.com says "close to 10,000") in families:
- **Aggregates** (minimum closing balance, maximum credit months)
- **Trended** variables
- **Negative indicators** (cheque returns, credit declines)
- **Momentum** (QoQ / HoH / YoY growth)
- **Balance-transfer triggers**

These feed XGBoost, which outputs a score, a risk bucket and a loan amount. Early-warning trigger models are also mentioned.

### 5. Statistical Analysis
"Three types of statistical tests are run on the model to evaluate the model predictability and dependability on a sample from time to time" (CIO.com). The tests are not named. Model behaviour after COVID (when ITR and bureau data weakened) was discussed.

### 6. Machine Learning
- **Model(s):** **XGBoost**, with explainability.
- **Target variable:** ND. Outputs include "Expected bad amount rate".
- **Outputs (Annual Report):** Lendingkart Score (300–900), Risk Bucket (A–F), loan amount for 1/2/3-year tenure, expected bad amount rate, key ratios such as EMI/ADB (EMI to average daily balance).
- **Validation approach:** Periodic statistical tests (unnamed).
- **Metrics:** KS / Gini / AUC not disclosed.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Programming | Python |
| Processing | Apache Kafka (real-time scoring) |
| ML | XGBoost |
| Cloud | AWS (platform-as-a-service) |

### 8. Business Decision
Applications are scored automatically and assigned a risk bucket and loan amount. About 40% go through a "Zero Touch" process with no manual underwriting.

### 9. Business Impact
- About **50%** higher approval rates vs manual underwriting (AIM)
- About **40%** of customers on Zero Touch, with **75%** TAT reduction; more than 8 lakh applications evaluated (Annual Report)
- Average scoring time about 3.5 seconds
- Models "perform better for new-to-credit MSMEs that have CIBIL scores of 651–700" (CIO.com)

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Feature families** (aggregate, trend, negative event, momentum) are a reusable template for any bank-statement model.
- The model outputs a **decision package** (score, bucket, amount, ratios), not just a probability.
- The 5,000 vs 10,000 variable discrepancy shows why you should cross-check figures across sources.

### 11. Source Links
- https://www.lendingkartcareers.com/how-lendingkart-uses-machine-learning/ (undated)
- https://www.cio.com/article/193986/ (14 Sep 2020)
- https://www.lendingkartfinance.com/wp-content/uploads/2022/02/Annual-Report-2021.pdf (FY2021)

---

## Case Study 12 — Personal-Loan Underwriting and Bucket-Wise Collections Scorecards

**Priority:** ★★★ Must-visit — Collections as resource allocation: bucket-wise PD and channel policy. **Notebook:** `cs12_collections_bucket_scorecards.ipynb` (✅ notebook built)

**Company:** Navi (Navi Finserv / Navi Technologies)
**Industry:** Digital lending (NBFC)
**Business Area:** Underwriting, collections, fraud
**Problem Type:** Credit scoring, cohort segmentation, delinquency PD for collections allocation
**Evidence Level:** Strong (A: Navi Finserv Draft Prospectus filed with SEBI, and Navi's Medium blog)
**Primary Sources:** Navi Finserv DRHP, 18 Apr 2022, pp. 125–131; Navi Medium, 30 May 2021

### 1. Business Problem
Many Indians have "low or no credit history". Small-ticket loans are uneconomic to underwrite manually, and delinquent accounts must be routed to the right collection channel.

### 2. Business Question
- Should this applicant be approved, and at what price?
- For a delinquent borrower, how likely are they to default, and which channel should work the account?

### 3. Data Available

| Data | Description |
|---|---|
| Application | Name, DOB, KYC, pin code, employment |
| Device (with consent) | Geolocation, device details, contacts, transaction history |
| Third party | Credit bureaus, analytics providers, partners |
| Outcomes | "2.64 million repayment events as of December 31, 2021", growing by 0.28M a month |
| Total | "more than 400 variables" |

### 4. Data Science Approach
- Underwriting estimates repayment capacity from age, income stability and continuity, residence, geolocation, existing obligations and estimated living expenses.
- A **cohort-based approach** segments customers by yield, risk, ticket size and acquisition cost.
- **Collections** use payment-behaviour scorecards by delinquency bucket.
- **Fraud** uses outlier models, an in-house rule engine, face recognition and geotagging.

### 5. Statistical Analysis
Cohort segmentation is described. Hypothesis tests and validation statistics: ND.

### 6. Machine Learning
- **Model(s):** "AI-based underwriting models"; "customer-wise default probability prediction algorithms" for the PAR 30–89 bucket; outlier-based fraud models. Algorithm names: ND.
- **Target variable:** Default / repayment (implied); exact definition ND.
- **Validation / KS / Gini:** ND.

**Collections policy by bucket:**

| Bucket | Treatment |
|---|---|
| 0–29 DPD | Digital nudges |
| PAR 30–89 | 100+ tele-callers + default-probability algorithms |
| PAR >90 | Field agencies + skip tracing |

### 7. Tools & Technology
ND (models built by Navi Technologies).

### 8. Business Decision
Automated approve/price decisions; delinquent accounts sent to channels by bucket and predicted default risk.

### 9. Business Impact
- Collection efficiency "96.63% till December 31, 2021"
- "over 85% had CIBIL credit scores greater than 725" (portfolio mix)
- Processing time went from "about a month to just a few milliseconds" (blog)

### 10. What a Data Scientist Can Learn *(interpretation)*
- Collections is a **resource-allocation problem**. Expensive human effort goes where predicted risk × recoverable value is highest.
- **IPO filings (DRHP/RHP)** are an under-used public source on how Indian lenders' models are governed.

### 11. Source Links
- https://www.bseindia.com/corporates/download/12417/IPO/Navi%20Finserv%20Limited%20%20Draft%20Prospectus_April182022_20220418230940.pdf (18 Apr 2022)
- https://medium.com/navi-technologies/big-impact-with-big-data-navi-using-data-science-to-transform-lending-7cd29a1c22f2 (30 May 2021)

---

## Case Study 13 — Can a Mobile Phone Footprint Replace a Credit Bureau Score? (Research on Indian Fintech Data)

**Priority:** ★★★ Must-visit — Comparing data sources by AUC (DeLong) and reject inference for thin-file lending. **Notebook:** `cs13_alternate_data_credit_scoring.ipynb` (✅ notebook built)

**Company:** Unnamed large Indian fintech lender (academic study by ISB / IIM Bangalore researchers). **Not attributed to any named company.**
**Industry:** Digital consumer lending
**Business Area:** Credit risk / financial inclusion
**Problem Type:** Default prediction with alternate data + counterfactual approval analysis
**Evidence Level:** Strong (C: academic working paper using actual lender data)
**Primary Sources:** Agarwal, Alok, Ghosh & Gupta, "Financial Inclusion and Alternate Credit Scoring for the Millennials", SSRN 3507827 (posted 21 Dec 2019; revised 7 Dec 2023)

### 1. Business Problem
Young, thin-file applicants are rejected because bureau scores are weak or missing.

### 2. Business Question
Does a phone footprint (installed apps, call logs, social logins) predict default better than the bureau score? How many rejected applicants could safely be approved?

### 3. Data Available

| Data | Description |
|---|---|
| Applications | 417,578 (Feb 2016–Nov 2018); 272,931 approved, 144,647 denied |
| Loans | ₹10,000–₹200,000; 15–180 days; average ₹22,174 |
| Bureau | Average CIBIL 634 |
| Mobile footprint | Installed apps (Facebook, LinkedIn, financial, dating, e-commerce, travel, other loan apps); counts of calls, SMS, contacts; iOS vs Android |
| Social login | Facebook (27%), LinkedIn (2.1%) |
| Call logs | "Deep social footprint" (outgoing duration, missed calls) |
| Outcome | Default (~13.5%) |

### 4. Data Science Approach
1. Logit models (explanatory).
2. Out-of-sample ML.
3. Comparison of feature sets by AUC.
4. A prediction-based counterfactual (Kleinberg/Athey style) for denied applicants.

### 5. Statistical Analysis
Logistic regression with inference on the footprint variables, plus a counterfactual approval simulation.

### 6. Machine Learning
- **Model(s):** Logit, **Random Forest**, **XGBoost**.
- **Target variable:** Default dummy; approval as a second outcome.
- **Validation approach:** Out-of-sample.
- **Metrics (AUC):**
  - Bureau score alone: **59%**
  - Mobile/social footprint alone: **60.4%**
  - Footprint + call logs: **66%**
  - Out of sample: deep mobile footprint **74%** vs deep financial information **59%**

### 7. Tools & Technology
ND.

### 8. Business Decision
This is research, not a documented lender decision. The finding is that alternate data can support approving more thin-file applicants.

### 9. Business Impact (counterfactual, not realised)
At a 10% (1%) predicted-default threshold, "about 42% (22%) borrowers who were denied credit would have been granted loans".

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Compare feature sets by AUC** to show the business the value of a new data source.
- **Reject inference** matters: you never observe the outcomes of applicants you denied, and the counterfactual method addresses this.
- Use of consented alternate data must follow RBI's Digital Lending Directions and the DPDP Act. This regulatory note is mine, not the paper's.

### 11. Source Links
- SSRN 3507827 — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3507827

---

## Case Study 14 — Segment-Specific Underwriting with 39 Sub-Models

**Priority:** ★★ Good to have — Segmented models vs one global model; top/bottom bad-rate ratio. **Notebook:** `cs14_segmented_underwriting.ipynb` (⏳ notebook pending)

**Company:** Kissht (OnEMI Technology Solutions)
**Industry:** Digital consumer lending
**Business Area:** Underwriting, fraud, collections
**Problem Type:** Segmented credit scoring
**Evidence Level:** Medium (B: independent analyses of the RHP; figures differ between write-ups, so check the RHP)
**Primary Sources:** MoneyFlow India, 5 May 2026; Zen Nivesh / Ankit Kanodia, 17 Jul 2026

### 1. Business Problem
Underwrite very different customer types quickly and keep losses controlled.

### 2. Business Question
For each customer segment, what is the risk of default, and should an offer be made within minutes?

### 3. Data Available

| Data | Description |
|---|---|
| Key variables | "over 400" across bureau, KYC, banking/transactional, digital footprint |
| Feature library | "over 7,000 variables": 75% credit/financial, 25% consumption/online behaviour |
| Fraud | "200+ fraud triggers" (Zen Nivesh) |

### 4. Data Science Approach
A large feature library feeds **segment-specific models**: "39 specialized ML sub-models" (MoneyFlow) or "40+ underwriting models" (Zen Nivesh).

### 5. Statistical Analysis
Rank-ordering evidence:
- MoneyFlow: "approximately **5.17x** separation in default rates between highest and lowest risk segments" vs "**2.13x** for traditional credit bureau scores"
- Zen Nivesh: "2.5x better risk separation"

These figures are inconsistent between sources.

### 6. Machine Learning
- **Model(s):** Segmented ML sub-models; algorithms ND.
- **Target / Validation / KS / Gini:** ND.
- **Metric:** Default-rate ratio between top and bottom risk segments (a lift-style rank-ordering measure).

### 7. Tools & Technology
ND.

### 8. Business Decision
Automated offers: about 85% of new customers get offers within 10 minutes. "26.46% of repeat applicants were declined".

### 9. Business Impact (9M FY26, as reported)
GNPA 2.90%; NNPA 0.38%; 30-DPD collection efficiency 96.95%. Collections run on 1,074 tele-callers and 8,291 field agents.

### 10. What a Data Scientist Can Learn *(interpretation)*
- The **bad-rate ratio between top and bottom deciles/segments** is a stakeholder-friendly way to show rank ordering, often easier to grasp than KS.
- Segmenting models helps when populations differ structurally (e.g., new-to-credit vs repeat).

### 11. Source Links
- https://moneyflowindia.substack.com/p/moneyflow-india-deep-dive-2-kissht (5 May 2026)
- https://zennivesh.substack.com/p/onemi-tech-kissht-an-emi-factory (17 Jul 2026)

---

## Case Study 15 — Setting BNPL Credit Limits with a Wallet-Behaviour Score

**Priority:** ★★ Good to have — Behavioural score → pre-approval and credit-limit assignment. **Notebook:** `cs15_bnpl_limit_assignment.ipynb` (⏳ notebook pending)

**Company:** MobiKwik
**Industry:** Wallet / BNPL
**Business Area:** Credit underwriting / limit assignment
**Problem Type:** Behavioural credit score
**Evidence Level:** Medium (B: Inc42 summary of MobiKwik's DRHP)
**Primary Sources:** Inc42, 13 Jul 2021 (DRHP filed 12 Jul 2021)

### 1. Business Problem
Pre-approve wallet users for BNPL ("ZIP") and set credit limits without a traditional bureau history.

### 2. Business Question
Which users can be pre-approved, and what limit should each get?

### 3. Data Available

| Data | Description |
|---|---|
| Behavioural | Spending patterns, payment patterns, outstanding amounts, channel preferences |
| Device / location | Device information, location history, app usage |
| Engagement | Contactability, responsiveness |
| Total | "More than 500 raw and derived variables" |

### 4. Data Science Approach
Raw and derived behavioural variables feed the **MobiScore**, which drives pre-approval and limits. ML collection strategies are also mentioned.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s) / Target / Validation / Metrics:** ND.

### 7. Tools & Technology
ND.

### 8. Business Decision
BNPL pre-approval and limit assignment based on MobiScore. Collections used 89 in-house staff (as of 31 Mar 2021) plus agencies.

### 9. Business Impact
Not publicly disclosed.

### 10. What a Data Scientist Can Learn *(interpretation)*
- "Contactability" and "responsiveness" are features chosen for **collections feasibility**, not just willingness to pay. Good feature design anticipates the downstream process.

### 11. Source Links
- https://inc42.com/buzz/mobikwiks-mobiscore-collects-spending-patterns-device-information/ (13 Jul 2021)

---

## Case Study 16 — Merchant Lending from QR Transaction Data and Automated KYC

**Priority:** ★★ Good to have — Merchant cash-flow capacity modelling + fuzzy KYC name matching. **Notebook:** `cs16_merchant_qr_lending.ipynb` (⏳ notebook pending)

**Company:** BharatPe
**Industry:** Merchant payments (QR) + merchant lending
**Business Area:** Underwriting, KYC operations, data platform
**Problem Type:** Borrowing-capacity model + document AI
**Evidence Level:** Medium (B: Google Cloud customer story naming the Head of Data Sciences, Sunil Saini)
**Primary Sources:** Google Cloud customer story (undated; refers to 2022 awards)

### 1. Business Problem
The legacy warehouse could not scale, and loan decisions to small merchants were slow.

### 2. Business Question
How much can a merchant borrow, given their QR payment behaviour? Can KYC and store verification be automated?

### 3. Data Available

| Data | Description |
|---|---|
| Merchant transactions | Volume, frequency |
| Behaviour & demographics | "Over 200 attributes" |
| Documents & images | KYC documents, store photos |
| Scale | 80 TB processed a day |

### 4. Data Science Approach
- An ML model sets **borrowing capacity** from transaction volume and frequency.
- Document AI and Vision AI extract KYC and store-photo data.
- FuzzyWuzzy name matching runs in BigQuery.
- Payment-behaviour patterns are used for BNPL decisions.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** Borrowing-capacity ML model (algorithm ND); Document AI / Vision AI; fuzzy string matching.
- **Target / Validation / Metrics:** ND.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Data warehouse | BigQuery |
| ML | Vertex AI, Document AI, Vision AI, FuzzyWuzzy |
| Processing | Cloud Composer / Airflow (1,000+ DAGs), Dataflow, Pub/Sub |
| Database | Cloud SQL |
| Cloud | Google Cloud |

### 8. Business Decision
Automated loan eligibility and limits for merchants, plus automated KYC checks.

### 9. Business Impact
Loan "turnaround time has decreased from two days to just five seconds."

### 10. What a Data Scientist Can Learn *(interpretation)*
- A payments company's **own transaction data** is its underwriting advantage. Cash-flow features are the core of merchant lending.
- **Name matching** (fuzzy matching of KYC name vs bank account name) is a small but critical data-quality step.

### 11. Source Links
- https://cloud.google.com/customers/bharatpe (undated)

---

## Case Study 17 — 10-Second Pre-Approved Personal Loans for Existing Customers

**Priority:** ★★ Good to have — Non-inferiority testing: 'same delinquency, 10 seconds instead of days'. **Notebook:** `cs17_preapproved_pl_noninferiority.ipynb` (⏳ notebook pending)

**Company:** HDFC Bank
**Industry:** Banking
**Business Area:** Retail lending / pre-approved offers
**Problem Type:** Multi-layer behavioural underwriting + eligibility targeting
**Evidence Level:** Medium (B: Business Standard interview with Arvind Kapil, Country Head)
**Primary Sources:** Business Standard, 6 Jul 2019

### 1. Business Problem
Disburse personal loans instantly to existing customers, without paperwork, while keeping delinquency in check.

### 2. Business Question
Which existing customers can be pre-approved, and for how much?

### 3. Data Available

| Data | Description |
|---|---|
| Bank internal | Bank statements, transaction history, credit and debit card transactions, account inflows, payment records |
| Credit history | Internal and external (bureau) |
| "Social score" | Internet consumption patterns |

### 4. Data Science Approach
The **"P27" (Power of 27)** multi-layer framework combines:
- an ability-to-pay income score
- bureau scores
- a behavioural score (spending and past repayments)
- a "social score"

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s) / Target / Validation:** ND.
- **Metric used to judge success:** Delinquency compared with physically sourced loans.

### 7. Tools & Technology
ND.

### 8. Business Decision
About one-third of roughly 30M customers were deemed eligible, with loans capped at ₹15 lakh. Launched 30 Apr 2015.

### 9. Business Impact
- 10-second loans were about one-third of roughly ₹6,000 crore in monthly personal loan disbursals.
- About ₹350 crore was disbursed in the first month.
- Delinquency was "on a par with loans disbursed physically".

### 10. What a Data Scientist Can Learn *(interpretation)*
- The success criterion was **non-inferior risk** at far lower cost and TAT. "Same delinquency, faster" is a valid win.
- Layered scores (ability, willingness, behaviour) make the decision explainable to credit committees.

### 11. Source Links
- https://www.business-standard.com/article/finance/how-hdfc-recast-systems-to-offer-loan-approval-disbursement-in-10-seconds-119070600910_1.html (6 Jul 2019)

---

## Case Study 18 — In-House Credit Scores That Beat Generic Bureau Models

**Priority:** ★★ Good to have — Custom score vs bureau: 'better on what metric?' (Gini, KS, bad rate at fixed approval). **Notebook:** `cs18_custom_score_vs_bureau.ipynb` (⏳ notebook pending)

**Company:** Axis Bank
**Industry:** Banking
**Business Area:** Credit risk / data-driven sourcing
**Problem Type:** Custom credit scoring
**Evidence Level:** Medium (B: Cloudera customer story naming the Head of BIU and the Head of Data Science)
**Primary Sources:** Cloudera customer story (Axis Bank operational excellence; page undated)

### 1. Business Problem
Replace intuition-based credit strategy with data-driven decisions. The on-premises setup could not support ad-hoc ML.

### 2. Business Question
Can the bank's own data predict credit risk better than generic bureau scores, and support pre-approved, database-driven lending?

### 3. Data Available

| Data | Description |
|---|---|
| Sources | 750 TB from Oracle Exadata and other sources |
| Types | Application, transaction, collections data |
| Credit model attributes | 2,000 |

### 4. Data Science Approach
ML credit models built in the Cloudera data-mesh platform. Details: ND.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** "ML-based credit models"; algorithms ND.
- **Metrics:** "More than 40% improvement" over generic bureau models. The metric (Gini / KS / other) is ND.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Platform | Cloudera Machine Learning, Data Engineering, Data Warehouse (data mesh) |
| Source DB | Oracle Exadata |

### 8. Business Decision
A large share of lending is sourced through data-driven, pre-approved programmes.

### 9. Business Impact
- "66% of personal loans" via database-driven programmes
- "79% of new credit card sourcing via data-driven strategy"

### 10. What a Data Scientist Can Learn *(interpretation)*
- "40% better" means nothing without the metric. Always ask *"better on what: Gini, KS, bad rate at fixed approval rate?"*
- Banks' edge is **internal transaction and collections history**, data bureaus do not have.

### 11. Source Links
- https://www.cloudera.com/customers/axis-bank-operational-excellence.html (undated)
- Related, older and generic: https://www.sas.com/en_in/customers/axis-bank-india-capitalize-data.html

---

## Case Study 19 — Propensity-to-Pay Models for Debt Collections Allocation

**Priority:** ★★★ Must-visit — Propensity vs uplift for collections: call the customers a call actually changes. **Notebook:** `cs19_collections_propensity_uplift.ipynb` (✅ notebook built)

**Company:** Credgenics (collections SaaS; clients include banks and NBFCs such as IIFL Finance)
**Industry:** Collections technology
**Business Area:** Collections optimisation
**Problem Type:** Propensity-to-pay / resolution-likelihood scoring for agent allocation
**Evidence Level:** Weak / partially documented (vendor-reported, aggregated claims)
**Primary Sources:** Inc42, 13 May 2024; Credgenics blog, 11 May 2023; Credgenics case studies (undated)

### 1. Business Problem
Lenders have limited calling and field capacity across millions of delinquent accounts.

### 2. Business Question
Which delinquent borrowers are most likely to pay, through which channel, and which accounts are likely to become delinquent?

### 3. Data Available

| Data | Description |
|---|---|
| Loan accounts | About 11 million retail loan accounts on the platform |
| Specific features | ND |

### 4. Data Science Approach
Named methods:
- propensity-to-pay
- pre-delinquency prediction
- resolution likelihood
- segmentation
- ML intent-to-pay for agent allocation
- GenAI voice bots

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s) / Features / Metrics:** ND.

### 7. Tools & Technology
ND.

### 8. Business Decision
Lenders allocate agents and channels (digital, voice bot, tele-caller, field) by predicted propensity.

### 9. Business Impact (vendor claims)
- "20% increased resolution rates, 25% improved collections, 40% reduced collection costs, 30% reduced collection time"
- One unnamed fintech lender: "27% higher recoveries"

### 10. What a Data Scientist Can Learn *(interpretation)*
- The right collections target is *incremental* repayment due to contact (uplift), not raw propensity. Calling people who would pay anyway wastes capacity. This is my note; the source does not say uplift modelling was used.

### 11. Source Links
- https://inc42.com/startups/how-credgenics-is-using-ai-ml-to-help-banks-fis-improve-debt-collection-by-25/ (13 May 2024)
- https://blog.credgenics.com/technological-capabilities-in-debt-collections/ (11 May 2023)
- https://www.credgenics.com/case-studies (undated)

---
# PART D — CUSTOMER & PRODUCT ANALYTICS

## Case Study 20 — Ranking Home-Screen Categories by Propensity × Lifetime Value

**Priority:** ★★★ Must-visit — Expected-value ranking (propensity × LTV) validated by A/B tests vs random and rules. **Notebook:** `cs20_propensity_ltv_ranking.ipynb` (✅ notebook built)

**Company:** PhonePe
**Industry:** UPI payments super-app
**Business Area:** Growth / personalisation / cross-sell
**Problem Type:** Next-best-action recommendation with business-utility ranking
**Evidence Level:** Strong (A: PhonePe tech blog, five named authors)
**Primary Sources:** tech.phonepe.com, Walimbe, Patil, Bhadra, Doshi, Swadi, 16 Feb 2026

### 1. Business Problem
Home-screen masthead banners were curated manually. This caused operational bottlenecks and generic experiences, and the team was "missing revenue opportunities in niche or emerging categories".

### 2. Business Question
For each user, which category (recharge, bill pay, insurance, investments, etc.) should be shown to raise **lifetime value** and **categories per customer**?

### 3. Data Available

| Data | Description |
|---|---|
| User features | "Over 5,000 distinct user features": transactional, demographic, behavioural |
| Journey stage | User journey-stage indicators |
| Outcomes | Transaction completed after recommendation |

### 4. Data Science Approach
Two models:
- an **acquisition** model (first transaction in a new category)
- a **repeat** model (transact again)

Both produce per-category propensities. A **utility function (propensity × LTV)** ranks categories, inside a multi-stage pipeline of non-linear models. Batch scoring feeds a low-latency serving layer.

### 5. Statistical Analysis
**A/B testing** of treatment vs control, benchmarked against random recommendations and rule-based methods.

### 6. Machine Learning
- **Model(s):** Multi-stage non-linear models; specific algorithms ND.
- **Target variable:** Transaction completion in the recommended category (acquisition / repeat).
- **Features:** 5,000+ from a feature store.
- **Validation:** Online A/B tests.
- **Metrics:** Categories per customer (CPC), LTV, new acquisitions, conversions, incremental revenue.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Feature store | Central feature store |
| Compute / Serving | Distributed compute cluster; model serving layer |
| Specific products | ND |

### 8. Business Decision
Manual masthead curation was replaced by model-driven, per-user category ranking.

### 9. Business Impact
Not publicly disclosed (no numbers in the post).

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Rank by expected value, not probability.** A user may be very likely to recharge (low value) and less likely to buy insurance (high value). Propensity × LTV encodes that trade-off.
- Separate **acquisition** and **repeat** models, because the behaviours differ.
- Benchmark against **random** and **rule-based** baselines so stakeholders can see the lift.

### 11. Source Links
- https://tech.phonepe.com/optimizing-merchandising-machine-learning-for-real-time-app-experience-and-ltv-maximization (16 Feb 2026)

---

## Case Study 21 — Bayesian Trend Filtering for Homepage Personalisation

**Priority:** ★★ Good to have — Simple Bayesian personalisation; interpretable baseline for recommenders. **Notebook:** `cs21_bayesian_trend_personalisation.ipynb` (⏳ notebook pending)

**Company:** Paytm (Paytm Labs)
**Industry:** Payments super-app
**Business Area:** Personalisation
**Problem Type:** Bayesian recommendation (category affinity × trend)
**Evidence Level:** Strong (A: Paytm Labs blog by a named ML engineer), undated
**Primary Sources:** paytmlabs.com/blog ("Santoshi, Machine Learning Engineer")

### 1. Business Problem
The homepage has hundreds of service icons and banners for 400M+ users. The team had to decide what to show each user.

### 2. Business Question
Which categories should each user see, combining *their* interests with what is *trending* across the platform?

### 3. Data Available

| Data | Description |
|---|---|
| User clicks | Category-level click history |
| Global distribution | Platform-wide click distribution, time-windowed trends |
| Inventory | Banner/icon category proportions |

### 4. Data Science Approach
Category-level Bayesian update combining user affinity and global trend:

`p_next(c | click) = p(c | click) · p_next(c) / p(c)`

### 5. Statistical Analysis
Bayes' rule applied to category probabilities (affinity × trend ratio).

### 6. Machine Learning
- **Model(s):** Bayesian trend filtering (probabilistic, not a learned black box).
- **Target / Validation / A/B results:** ND.
- **Stated benefits:** "Simple to formulate and implement", interpretable, computable in real time.

### 7. Tools & Technology
ND.

### 8. Business Decision
Homepage icon and banner rankings are driven by this score.

### 9. Business Impact
Not publicly disclosed.

### 10. What a Data Scientist Can Learn *(interpretation)*
- A **one-line Bayesian formula** can beat a complex model on interpretability, speed and maintenance. Start simple.

### 11. Source Links
- https://paytmlabs.com/blog/ (undated)

---

## Case Study 22 — An Omnichannel Nudge Engine That Books Deposits and Loans

**Priority:** ★★★ Must-visit — Causal campaign measurement: SRM, CUPED, power, heterogeneity, uplift, ROI. **Notebook:** `03_nudge_campaign_ab_test.ipynb` (✅ notebook built)

**Company:** Axis Bank
**Industry:** Banking
**Business Area:** Marketing / cross-sell / campaign optimisation
**Problem Type:** Propensity + channel/product optimisation, measured by test vs control
**Evidence Level:** Medium (B: Cloudera customer story quoting Balaji Narayanamurthy, Head of Business Intelligence)
**Primary Sources:** Cloudera customer story, 4 Feb 2025

### 1. Business Problem
Move from product-push campaigns to customer-centric, personalised marketing across 50M+ customers.

### 2. Business Question
For each customer: which product, which channel, which message, and when?

### 3. Data Available

| Data | Description |
|---|---|
| Customer attributes | "2,000+ customer attributes updated daily": demographics, transactions, browsing, preferences |
| Scale | 50M+ customers |

### 4. Data Science Approach
1. ML models for **channel and product optimisation**.
2. Segmentation across 10 business lines.
3. 17,000+ nudge variants.
4. A "Control Tower" for campaign tracking.
5. **Test vs control** measurement.

### 5. Statistical Analysis
**Test vs control** comparison (e.g., BillPay "1.5x boost in test versus control"). Significance testing: ND.

### 6. Machine Learning
- **Model(s):** "Advanced ML models"; algorithms ND.
- **Target / Validation:** ND.
- **Metrics:** Campaign effectiveness, bookings via nudges.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Platform | Cloudera Open Data Lakehouse |
| Programming | Scala framework |
| Cloud | AWS (EKS, S3, RDS, EC2) + on-premises |
| Channels | 9, including SMS, email, push, WhatsApp, in-app banners |

### 8. Business Decision
Marketing moved to model-driven personalised nudges as a main sourcing channel.

### 9. Business Impact
- "**45%** of the term deposits and **70%** of instant loans on credit cards are booked via personalized nudges"
- Personal-loan campaign effectiveness **+10%**
- BillPay registration **1.5x** (test vs control)

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Hold-out control groups** turn "campaign performance" into causal lift. Without them, you only measure who would have bought anyway.
- "Share of bookings via nudges" shows adoption but is not causal on its own. Pair it with the test/control lift.

### 11. Source Links
- https://www.cloudera.com/customers/axis-bank.html (4 Feb 2025)

---

## Case Study 23 — Inferring the Purpose of Every Transaction with a Neural Network

**Priority:** ★ Optional — Transaction categorisation (text classification); a foundation for other models. **Notebook:** `cs23_transaction_purpose_classification.ipynb` (⏳ notebook pending)

**Company:** YES Bank
**Industry:** Banking
**Business Area:** Customer analytics / segmentation / personalisation
**Problem Type:** Multi-class classification of transaction purpose; demographic classification
**Evidence Level:** Medium (B: Cloudera customer story naming CIO Anup Purohit)
**Primary Sources:** Cloudera customer story (updated 2025); BigDataWire, 5 Jul 2017

### 1. Business Problem
Data was spread across federated marts, with no single customer view. The bank wanted to treat "every customer as a segment".

### 2. Business Question
What is each transaction *for* (rent, school fees, etc.), and what does that say about the customer?

### 3. Data Available

| Data | Description |
|---|---|
| Sources | 100+ applications |
| Types | Clickstreams, logs, emails, SMS, push notifications, transactions |

### 4. Data Science Approach
1. Unify data in a lake.
2. Engineer about **1,000 features**.
3. A neural network for transaction purpose.
4. A separate neural network for granular demographic classification.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** Neural networks.
- **Target:** Transaction purpose class; demographic class.
- **Accuracy / Validation:** ND.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Programming | Python, R |
| Platform | Cloudera |

### 8. Business Decision
The inferred purposes and demographics feed personalisation and the bank's in-house loyalty programme.

### 9. Business Impact
"100s of TB analyzed daily"; "$250,000 saved annually" from the in-house loyalty programme.

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Transaction categorisation** is an underrated foundation. Life-event signals (rent, school fees) are among the strongest inputs to cross-sell and risk models.

### 11. Source Links
- https://www.cloudera.com/customers/yes-bank.html
- https://www.hpcwire.com/bigdatawire/this-just-in/cloudera-empowers-yes-banks-digital-strategy/ (5 Jul 2017)

---

# PART E — INSURANCE / INSURTECH

## Case Study 24 — Replacing Physical Car Inspections with Smartphone Computer Vision

**Priority:** ★ Optional — Computer vision; the DS part is validating 'fit for purpose' accuracy and triage. **Notebook:** `cs24_motor_inspection_cv_validation.ipynb` (⏳ notebook pending)

**Company:** ICICI Lombard
**Industry:** General insurance
**Business Area:** Motor underwriting (renewals) and claims
**Problem Type:** Computer vision: part detection + damage classification
**Evidence Level:** Medium (B: Microsoft Stories India; Frontier Enterprise, quoting Girish Nayak, Chief – Customer Service, Ops & Technology)
**Primary Sources:** Microsoft Stories India, 16 Sep 2019; Frontier Enterprise, 7 Jun 2019

### 1. Business Problem
Policy renewals after a break and simple damage claims needed physical inspections, which took "days or longer".

### 2. Business Question
Can photos taken by the customer on a smartphone replace a surveyor's inspection?

### 3. Data Available

| Data | Description |
|---|---|
| Vehicle images | Uploaded by customers |
| Training set size | ND |

### 4. Data Science Approach
1. Split uploaded images into frames.
2. Identify car components.
3. Detect damage types (scratch, dent, crack).

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** Computer vision / ML; architecture ND.
- **Target:** Component and damage type.
- **Metrics:** Accuracy "fit for purpose" (no figure).

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Cloud | Microsoft Azure |
| ML | Computer vision services (specifics ND) |

### 8. Business Decision
Launched for renewals in Dec 2018; claims module in beta in 2019. Simple claims were to be settled on inspection by the app.

### 9. Business Impact
- 150–200 cars a day inspected through the app
- Inspection time cut from "days to mere minutes"
- Target of "over 80,000 simple claims every month" by end-2019, with same-day turnaround

### 10. What a Data Scientist Can Learn *(interpretation)*
- A "fit for purpose" accuracy bar is a real business framing. The model only needs to handle **simple** cases well, and complex ones go to humans.

### 11. Source Links
- https://news.microsoft.com/en-in/features/icici-lombard-ai-enabled-car-inspection-app-india/ (16 Sep 2019)
- https://www.frontier-enterprise.com/icici-lombard-microsoft-roll-out-ai-enabled-car-inspection-app/ (7 Jun 2019)

---

## Case Study 25 — Health-Claim Adjudication Copilot (OCR + LLM + Clinical Guidelines)

**Priority:** ★ Optional — OCR + LLM decision support; the DS part is measuring productivity and agreement. **Notebook:** `cs25_claims_copilot_evaluation.ipynb` (⏳ notebook pending)

**Company:** ICICI Lombard
**Industry:** General / health insurance
**Business Area:** Claims operations
**Problem Type:** Document understanding + guideline-based decision support
**Evidence Level:** Medium (B: Microsoft AI First Movers page quoting MD & CEO Sanjeev Mantri; Google Cloud customer story quoting Head of Technology Arif Syed). These may describe related programmes on two vendors; the sources don't say, so they are counted once here.
**Primary Sources:** Microsoft (undated); Google Cloud (undated)

### 1. Business Problem
Adjudicators read 20+ pages per claim (discharge summaries, lab reports, bills, handwritten notes). One adjudication took several hours.

### 2. Business Question
Can documents be structured automatically and checked against policy terms and treatment guidelines, so adjudicators decide faster and more consistently?

### 3. Data Available

| Data | Description |
|---|---|
| Claim documents | Discharge summaries, lab reports, medical bills (PDF / images), handwritten notes |
| Rules | Policy terms; National Health Authority (NHA) and disease treatment guidelines |

### 4. Data Science Approach
1. OCR and document extraction.
2. Structuring into diagnosis, clinical presentation, history, treatment and lab results.
3. Comparison of treatment against NHA and disease guidelines.
4. Summary for the adjudicator.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** Azure OCR / Document Intelligence + Azure OpenAI + an "indigenous model" (Microsoft page); Gemini models (Google page).
- **Target / Validation / Metrics:** ND.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| Cloud / AI | Azure OCR, Azure AI Document Intelligence, Azure OpenAI; Google Gemini |

### 8. Business Decision
Adjudicators work from AI-structured summaries and guideline checks. Humans remain the decision-makers.

### 9. Business Impact
- "**2x** productivity increase"; processing time cut "by over 50%" (Microsoft)
- Adjudication time cut "to just a few minutes"; extraction automated for "thousands of monthly medical claims" (Google)

### 10. What a Data Scientist Can Learn *(interpretation)*
- This is decision **support**, not automation. Measure productivity and TAT, and keep humans on the final decision for regulated outcomes.

### 11. Source Links
- https://www.microsoft.com/en-in/aifirstmovers/icici-lombard (undated)
- https://cloud.google.com/customers/icicilombard (undated)

---

## Case Study 26 — Using Chat to Double Motor-Insurance Conversion

**Priority:** ★★ Good to have — Observational vs causal channel comparison (self-selection, propensity matching). **Notebook:** `cs26_chat_conversion_causal.ipynb` (⏳ notebook pending)

**Company:** Policybazaar (PB Fintech)
**Industry:** Insurance marketplace
**Business Area:** Sales conversion / growth
**Problem Type:** Conversational AI driven by a conversion-rate finding
**Evidence Level:** Strong (A: interviews with named CTO Ashish Gupta)
**Primary Sources:** YourStory, Nov 2018; Digital Creed, 19 Jun 2018

### 1. Business Problem
Grow sales volume about 100% a year without hiring a proportionate number of sales agents.

### 2. Business Question
Is chat a better-converting channel, and can a bot handle most of the chat load?

### 3. Data Available

| Data | Description |
|---|---|
| Channel conversion | Conversion of chat vs non-chat users |
| Chat logs | Queries, bot errors |

### 4. Data Science Approach
**EDA finding:** chat users converted at about **2x** the rate of non-chat users, but were only 8–9% of customers. So the plan was to scale chat with an in-house bot (PBee), hand complex queries to humans, and retrain on recorded errors.

### 5. Statistical Analysis
Conversion-rate comparison by channel. Note that this comparison is observational, so self-selection may inflate the 2x (my note).

### 6. Machine Learning
- **Model(s):** In-house bot on Google Dialogflow (NLU).
- **Validation:** Human handover and error-based retraining.
- **Metrics:** Bot response share, response delay, chat sales share, agent productivity.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| NLP | Google Dialogflow |

### 8. Business Decision
Push motor-insurance customers to the chat channel and let the bot handle most responses.

### 9. Business Impact
- Bot share of responses: **20% → 75–80%** in 6–8 months
- Response delays: **35% → 7–8%**
- Motor sales via chat: **8–9% → almost 50%**
- Agent output: **1.5–2 → 7–8** sales a day
- About **$1M** premium a month through the bot

### 10. What a Data Scientist Can Learn *(interpretation)*
- A single **channel-level conversion insight** justified a whole product investment.
- Be careful with observational comparisons. Chat users may be more motivated buyers.

### 11. Source Links
- https://yourstory.com/2018/11/successful-ai-policybazaar-docprime (Nov 2018)
- https://www.digitalcreed.in/policybazaar/ (19 Jun 2018)

---

## Case Study 27 — Hindi Speech Analytics and Dialler Optimisation for an Insurance Call Centre

**Priority:** ★ Optional — Speech analytics; the DS part is intent-frequency analysis and dialler efficiency. **Notebook:** `cs27_call_analytics_dialler.ipynb` (⏳ notebook pending)

**Company:** Policybazaar (PB Fintech)
**Industry:** Insurance marketplace
**Business Area:** Call-centre operations / quality / product insight
**Problem Type:** Speech-to-text + NLP + dialler analytics
**Evidence Level:** Strong (A: CTO interviews; AWS ML blog by the CTO for the related Polly IVR work)
**Primary Sources:** YourStory, Nov 2018; Digital Creed, 19 Jun 2018; AWS ML Blog, 2 May 2018

### 1. Business Problem
Only 1–2% of about 10 million monthly call minutes could be quality-checked by humans. Call volumes were rising fast: "nearly 100 million customer queries over the phone in 2017".

### 2. Business Question
- What are customers asking for?
- Where are agents breaking compliance or mis-selling?
- How can dialler efficiency be improved?

### 3. Data Available

| Data | Description |
|---|---|
| Call audio | ~10M minutes/month (Hindi and English telephony) |
| Dialler logs | Dial-outs, connects, callbacks |

### 4. Data Science Approach
1. A proprietary Hindi voice-to-text engine (third-party tools were judged inadequate).
2. NLP on transcripts.
3. Real-time alerts for compliance breaches and pitch mismatches.
4. Frequency analysis of customer requests.
5. Dialler analytics.

Separately, Amazon Polly was used for personalised outbound voice and IVR.

### 5. Statistical Analysis
Frequency ranking of request types. Finding: **cashless hospital requests** were the 7th–8th most common request.

### 6. Machine Learning
- **Model(s):** In-house ASR + NLP; architecture ND.
- **WER / Validation:** ND.

### 7. Tools & Technology

| Category | Tools |
|---|---|
| ML | TensorFlow, Amazon SageMaker, GPUs |
| Speech | Amazon Polly (TTS for IVR) |
| Cloud | AWS |

### 8. Business Decision
- **Product:** a cashless-hospital integration, built because of the request-frequency insight.
- **Operations:** 100% call monitoring with alerts, and dialler changes.
- **IVR:** personalised voice messages.

### 9. Business Impact
- Dialler: "**50%** increase in dial-out rates"; call efficiency **40% → 85%**; callback time cut to 30–45 minutes
- Polly IVR, over 4 months: 150,000 calls; 80% answered; 53% responded positively; "41% of sales were closed without the interference of agents"; CSAT 60% → 85%

### 10. What a Data Scientist Can Learn *(interpretation)*
- Unstructured data (calls) can produce **product decisions**, not just efficiency gains. A simple frequency count of intents led to a new feature.

### 11. Source Links
- https://yourstory.com/2018/11/successful-ai-policybazaar-docprime (Nov 2018)
- https://www.digitalcreed.in/policybazaar/ (19 Jun 2018)
- https://aws.amazon.com/blogs/machine-learning/policybazaar-com-adopts-amazon-polly-to-enhance-efficiency-and-customer-experience/ (2 May 2018)

---

## Case Study 28 — Speed-to-Lead: AI Voice Qualification within 60 Seconds

**Priority:** ★ Optional — Speed-to-lead: how contact delay erodes conversion; capacity-constrained routing. **Notebook:** `cs28_speed_to_lead.ipynb` (⏳ notebook pending)

**Company:** Policybazaar (with vendor Ringg AI)
**Industry:** Insurance marketplace
**Business Area:** Lead management / marketing operations
**Problem Type:** Lead qualification and routing
**Evidence Level:** Medium (B: vendor case study naming Manoj Pandey, DVP – AI Initiatives & Health; possibly promotional)
**Primary Sources:** Ringg AI case study, 12 May 2026

### 1. Business Problem
Relationship managers (RMs) took 8–12 minutes to reach a new lead, and the lead's intent faded in that time. Each RM made about 80 calls a day.

### 2. Business Question
Can every lead be contacted within a minute, qualified on intent, profile, budget and coverage, and routed to the right next step?

### 3. Data Available

| Data | Description |
|---|---|
| Lead forms | Submitted details |
| Call conversations | Hindi / English / Hinglish |
| Volume | 57,000+ connected calls a day |

### 4. Data Science Approach
1. An AI voice call within 60 seconds of the form.
2. A 4-minute structured qualification.
3. Routing to AI handling, an RM, or a scheduled callback.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** Voice AI; scoring model ND.
- **Metrics:** Response time, qualified-lead rate, containment rate.

### 7. Tools & Technology
Ringg AI voice platform; others ND.

### 8. Business Decision
New leads are first-touched by AI. Only qualified leads go to RMs.

### 9. Business Impact
- Response time cut to under 60 seconds
- Qualified-lead rate 5–7%
- Level-0 containment 67%
- Routing: 67% AI-handled, 7% handed to RM, 26% scheduled callback

### 10. What a Data Scientist Can Learn *(interpretation)*
- **Speed-to-lead** is a measurable lever. Contact delay is a feature worth modelling in any conversion model.
- Routing splits express **RM capacity** as a constraint.

### 11. Source Links
- https://www.ringg.ai/case-studies/policybazaar (12 May 2026)

---

# PART F — WEALTHTECH / BROKING

## Case Study 29 — Nudging First-Time Investors Away from Penny Stocks

**Priority:** ★★ Good to have — Pre/post vs difference-in-differences and interrupted time series. **Notebook:** `cs29_penny_stock_nudge_causal.ipynb` (⏳ notebook pending)

**Company:** Zerodha
**Industry:** Stock broking
**Business Area:** Investor protection / behavioural product design
**Problem Type:** Rule-based behavioural intervention (**not ML**)
**Evidence Level:** Strong (A: posts by Nithin Kamath and Kailash Nadh)
**Primary Sources:** Zerodha Z-Connect, 15 Aug 2020; Kailash Nadh, "User disengagement", 6 May 2022

### 1. Business Problem
First-time investors were trading penny stocks and illiquid instruments, with a high risk of losses.

### 2. Business Question
Can contextual warnings at the point of trade reduce risky trading?

### 3. Data Available

| Data | Description |
|---|---|
| Trade attempts | Instrument type, liquidity, user profile (rules-based) |

Zerodha states it deliberately does not run behavioural tracking or engagement analytics.

### 4. Data Science Approach
Rules flag risky instruments, and a "Nudge" warning appears when a trade is attempted.

### 5. Statistical Analysis
Before/after comparison of penny-stock volumes. **No control group is stated.**

### 6. Machine Learning
None. This is rule-based.

### 7. Tools & Technology
ND.

### 8. Business Decision
Nudge warnings were built into the Kite trading platform.

### 9. Business Impact
"Penny stock trading volumes on Kite have dropped by more than 50%, probably saving tens of crores of rupees." This is before/after only; causality is not established.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Not every intervention needs ML. Sometimes the analysis *is* the decision.
- A pre/post drop without a control group can be confounded by market conditions. Push for a **staggered rollout or a hold-out**.

### 11. Source Links
- https://zerodha.com/z-connect/general/our-10th-anniversary-and-the-future (15 Aug 2020)

*Note on wealthtech coverage:* public technical write-ups from Groww, Angel One, Upstox, 5paisa, Smallcase and INDmoney were mostly about data engineering and infrastructure, not modelling. Angel One's ARQ Prime (Medium, Aug 2021) describes a rules-based factor engine tested on "terabytes of historical market data" but gives no backtest metrics. It was excluded as too thin.

---

# PART G — OPERATIONS

## Case Study 30 — Scaling Customer Support to One Agent per 20 Million Transactions

**Priority:** ★ Optional — Intent classification + resolution rate together with CSAT. **Notebook:** `cs30_support_automation_resolution.ipynb` (⏳ notebook pending)

**Company:** PhonePe
**Industry:** UPI payments
**Business Area:** Customer support operations
**Problem Type:** Intent classification + LLM summarisation + knowledge retrieval
**Evidence Level:** Strong (A: PhonePe tech blog)
**Primary Sources:** tech.phonepe.com, PhonePe Team, 13 Jul 2026

### 1. Business Problem
Support volume grows with billions of transactions a month. Hiring agents in proportion is not sustainable.

### 2. Business Question
What is the user's issue, and can it be resolved automatically using their transaction and ticket context?

### 3. Data Available

| Data | Description |
|---|---|
| Transaction history | Linked to the query |
| Ticket history | Prior tickets |
| Knowledge base | Resolution articles |

### 4. Data Science Approach
Intent classification → LLM summaries of transaction and ticket history → knowledge-base matching → multilingual chatbot or voicebot → human escalation.

### 5. Statistical Analysis
ND.

### 6. Machine Learning
- **Model(s):** Intent classifiers, LLMs; specifics ND.
- **Metrics:** AI resolution rate, CSAT, handling time.

### 7. Tools & Technology
ND.

### 8. Business Decision
AI is the first line of support, with agents for escalations.

### 9. Business Impact
- "Over **92%**" of queries resolved by AI
- "One support agent for every **20 million** transactions"
- CSAT **70%**
- 30–50 seconds saved per interaction

### 10. What a Data Scientist Can Learn *(interpretation)*
- Report **resolution rate together with CSAT**. Automation that resolves tickets but annoys users is not a win.

### 11. Source Links
- https://tech.phonepe.com/how-ai-driven-automation-is-scaling-phonepes-customer-support-framework/ (13 Jul 2026)

---
# MASTER COMPARISON TABLE

| # | Company | Business Problem | Data | Statistical Method | ML Method | Evaluation Metric | Decision | Impact | Tools | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Juspay | Gateway routing for SR | Txn outcomes × gateway × BIN/network | Binomial Z-scores, explore/exploit, A/B | Non-stationary MAB + RL + feedback control | SR, downtime detection time | Dynamic routing option in orchestrator | +1.15% SR (up to 7% cards); ~$15K GMV saved in one outage | Rust, Redis, Kafka, ClickHouse, K8s | Strong (C+A) |
| 2 | Cashfree | Card decline gap between processors | Stage-wise txn logs | Funnel decomposition | None | SR | Split auth vs authorisation | +2% SR | FlowWise | Strong (A) |
| 3 | Razorpay | Routing, fraud, COD RTO, checkout ranking | 4B payments, 3,000 signals | Calibration, fixed-alert comparison | Set Transformer foundation model (masked-field pretraining) | Ranking, calibration, fraud @ fixed alerts | Powers 4 real-time decisions | +8–10% SR; 5x fraud identified; 8x intl card fraud | AWS, NVIDIA | Strong (A) |
| 4 | Razorpay | Static alert thresholds | 5B events/day | Calendar-aware baselines | ML thresholds (ND) + CEP rules | Detection latency, FP | Replace static alerting | >90% fewer FPs; ~80% cost cut; <30s detection | MSK/Kafka, Flink, ClickHouse | Strong/Medium |
| 5 | Razorpay | Manual merchant reviews | Website, WHOIS, SSL, fraud DB | ND | LLM multi-agent + rules | Accuracy, latency | Automated onboarding review | 20+ min → 8–12 s; 88% → 99%+ accuracy | Python | Strong (A) |
| 6 | PhonePe | P2P UPI fraud | Sender/receiver/txn aggregates | Label segmentation | Classifier (ND) | Precision, recall, reinstatement | Real-time blocking | −40% fraud rate; −38% complaints | Yoda, Kratos | Strong (A) |
| 7 | Cashfree | Real-time fraud screening | Negative lists, device, geo, velocity, graph | ND | Anomaly detection + rules | ND | Allow/review/block | ND | Flink, Kafka, graph DB | Strong (A) |
| 8 | Paytm Payments Bank | Mule accounts | 1.5M/700K accounts, 17 features | PR/ROC analysis | Random Forest (1:5 class weight) | Precision, recall | Tiered block/investigate | P/R 20/50 → 65.1/74.1 | Maquette | Strong (A) |
| 9 | RBIH | Mule accounts across banks | Bank txn/account data | Typology study | AI/ML (ND) | Alert precision | Adopted by 26+ banks | 90% positive alerts | ND | Medium (B) |
| 10 | Simpl | BNPL fraud, limits, repayment | Txn payload + 1-yr history | ND | Neural net, graph ML | Precision–recall | Real-time approve/decline | ND | Flink, DynamoDB, Airflow, SageMaker | Strong (C) |
| 11 | Lendingkart | MSME underwriting | Bank statements, GST, bureau | 3 periodic stat tests (unnamed) | XGBoost | ND (score, bucket A–F) | Zero-touch approvals | +50% approvals; 75% TAT cut | Python, Kafka, AWS | Strong (A) |
| 12 | Navi | PL underwriting + collections | 400+ vars, 2.64M repayment events | Cohort segmentation | AI underwriting, PD for PAR 30–89 | Collection efficiency | Bucket-wise channel allocation | 96.63% collection efficiency | ND | Strong (A) |
| 13 | Unnamed lender (ISB study) | Thin-file scoring | 417K apps; apps, call logs | Logit, counterfactual | RF, XGBoost | AUC | Research finding | AUC 59% → 74% (OOS); 22–42% of rejects approvable | ND | Strong (C) |
| 14 | Kissht | Segmented underwriting | 7,000-var library | Rank-ordering bad-rate ratio | 39 segment sub-models | Top/bottom default ratio | Offers in 10 min | 5.17x vs 2.13x bureau separation | ND | Medium (B) |
| 15 | MobiKwik | BNPL limits | 500+ wallet/device vars | ND | MobiScore (ND) | ND | Pre-approval, limits | ND | ND | Medium (B) |
| 16 | BharatPe | Merchant loans + KYC | 200+ merchant attributes, docs | ND | Capacity model, Document/Vision AI | ND | Automated loans/KYC | TAT 2 days → 5 s | BigQuery, Vertex AI, Composer | Medium (B) |
| 17 | HDFC Bank | Pre-approved PL | Statements, cards, bureau | ND | P27 layered scores | Delinquency vs physical | 1/3 of base eligible | ~1/3 of PL disbursals; delinquency on par | ND | Medium (B) |
| 18 | Axis Bank | Custom credit scores | 750 TB; 2,000 attributes | ND | ML credit models | "40% better" (metric ND) | Data-driven sourcing | 66% PL, 79% new cards data-driven | Cloudera | Medium (B) |
| 19 | Credgenics | Collections allocation | 11M accounts | ND | Propensity-to-pay (ND) | ND | Agent/channel allocation | +25% collections (vendor) | ND | Weak (D) |
| 20 | PhonePe | Home-screen NBA | 5,000+ features | A/B vs random & rules | Acquisition + repeat models; propensity×LTV | CPC, LTV, incremental revenue | Replace manual curation | ND | Feature store | Strong (A) |
| 21 | Paytm | Homepage personalisation | Category clicks, trends | Bayes' rule | Bayesian trend filtering | ND | Rank icons/banners | ND | ND | Strong (A) |
| 22 | Axis Bank | Personalised nudges | 2,000+ attrs, 50M customers | Test vs control | ML channel/product optimisation | Campaign lift | Nudge-led sourcing | 45% TDs, 70% card loans via nudges; 1.5x BillPay | Cloudera, AWS, Scala | Medium (B) |
| 23 | YES Bank | Transaction purpose | 100+ apps; ~1,000 features | ND | Neural networks | ND | Personalisation, loyalty | $250K/yr saved | Python, R, Cloudera | Medium (B) |
| 24 | ICICI Lombard | Motor inspection | Vehicle images | ND | Computer vision | "Fit for purpose" | App-based inspection | Days → minutes | Azure | Medium (B) |
| 25 | ICICI Lombard | Health-claim adjudication | Claim documents + NHA guidelines | ND | OCR + LLM | Productivity, TAT | Copilot for adjudicators | 2x productivity; >50% faster | Azure OpenAI, Gemini | Medium (B) |
| 26 | Policybazaar | Sales scale via chat | Channel conversion, chat logs | Channel conversion comparison | Dialogflow bot | Bot share, sales share | Push chat channel | Chat sales 8–9% → ~50%; agent 2 → 8 sales/day | Dialogflow | Strong (A) |
| 27 | Policybazaar | Call QA + dialler | 10M call min/month | Request frequency ranking | In-house Hindi ASR + NLP | ND | 100% monitoring; cashless product | +50% dial-outs; efficiency 40% → 85% | TensorFlow, SageMaker, Polly | Strong (A) |
| 28 | Policybazaar | Lead response delay | Lead forms, calls | ND | Voice AI | Response time, containment | AI first-touch | <60 s; 67% containment | Ringg | Medium (B) |
| 29 | Zerodha | Risky penny-stock trading | Trade attempts | Pre/post (no control) | None (rules) | Volume change | Nudge warnings | >50% drop in penny volumes | ND | Strong (A) |
| 30 | PhonePe | Support scale | Txn + ticket history | ND | Intent classification + LLM | Resolution %, CSAT | AI-first support | 92% AI-resolved; CSAT 70% | ND | Strong (A) |

---

# DATA SCIENTIST THINKING — PATTERNS ACROSS THE CASES

*This section is interpretation, anchored to the cases above.*

### How do fintech data scientists convert business problems into ML problems?

| Business question (stakeholder) | ML / analytics formulation | Case |
|---|---|---|
| "Which gateway should we send this payment to?" | Maximise P(success \| gateway, BIN, network, time) online → **bandit** with exploration | 1 |
| "Why is Processor 2 worse?" | Decompose SR = P(auth) × P(authorisation \| auth) → compare stages | 2 |
| "Stop P2P fraud without blocking good users" | Target = confirmed fraud (disputes removed); classify in real time; KPI = fraud rate & reinstatement rate | 6 |
| "Find mule accounts" | Binary classifier on account behaviour; class-weighted; thresholds → action tiers | 8 |
| "How much can this MSME borrow?" | P(bad) from cash-flow features + amount/tenure grid → score, bucket, limit | 11 |
| "Which delinquent customers should our callers work?" | Target = P(default \| PAR 30–89) → allocate tele-callers by risk | 12 |
| "Should we use phone data for thin-file applicants?" | Compare AUC of feature sets + counterfactual approval simulation | 13 |
| "What should we show on the home screen?" | Rank categories by **P(transact) × LTV**; separate acquisition vs repeat targets | 20 |
| "Are our alerts too noisy?" | Seasonal baseline per series → anomaly = deviation from expected | 4 |

### How do they choose the target variable?
- **Clean the label before modelling.** PhonePe removed disputes from "reported fraud" (Case 6).
- **Match the target to the decision point.** Navi predicts default *within a delinquency bucket*, because the decision is which channel works the account (Case 12).
- **Separate behaviours that differ.** PhonePe built separate *acquisition* and *repeat* targets (Case 20).
- **Accept delayed labels and plan for them.** Razorpay fraud labels arrive weeks later, which forces out-of-time evaluation (Case 3).
- **Predict money, not just events.** Lendingkart outputs an "expected bad amount rate" and loan amount, not only a default flag (Case 11).

### How do they choose features?

| Feature type | Examples from cases |
|---|---|
| Behavioural | Spending patterns, contactability, responsiveness (MobiKwik, 15); app installs, call logs (Case 13) |
| Transaction | Sender/receiver/txn aggregates (PhonePe, 6); merchant txn volume and frequency (BharatPe, 16) |
| Aggregated / velocity | ">X distinct devices in Y minutes" (Cashfree, 7); min closing balance, max credit months (Lendingkart, 11) |
| Temporal / trend / momentum | QoQ/HoH/YoY growth (Lendingkart, 11); calendar baselines (Razorpay, 4); sliding-window SR (Juspay, 1) |
| Negative events | Cheque returns, credit declines (Lendingkart, 11) |
| Graph / network | Links to risky entities (Cashfree, 7); fraud communities (Simpl, 10); identity graph (PhonePe Guardrails) |
| Customer | KYC, pin code, employment, demographics (Navi, 12; HDFC, 17) |

Two practical lessons: real-time systems **prune features hard** (Paytm: 17 features), and features are served from **feature stores** (PhonePe Yoda, Simpl DynamoDB).

### How do they select models?

| Situation | Model family | Evidence |
|---|---|---|
| Need explainability, regulatory credit decisions, inference on drivers | **Logistic regression / scorecards** | Logit in Case 13; "scorecards" at Navi (12) |
| Tabular data, non-linear interactions, thousands of features | **Tree ensembles** (XGBoost, Random Forest) | Lendingkart XGBoost (11); Paytm RF (8); RF/XGB in 13 |
| Decisions that change future data; non-stationary environment | **Bandits / online control** | Juspay (1) |
| No reliable labels; novel patterns; ops monitoring | **Anomaly detection / baselines** | Cashfree (7); Razorpay ADA (4) |
| Rings of colluding accounts | **Graph ML** | Simpl (10); PhonePe Guardrails |
| Images, documents, speech, very high-cardinality payment data | **Deep learning** (CV, OCR/LLM, ASR, transformers) | ICICI Lombard (24, 25); Policybazaar (27); Razorpay Vulcan (3) |
| Need interpretability and real-time speed in ranking | **Simple Bayesian** scoring | Paytm (21) |
| Clustering / segmentation | Cohort segmentation | Navi (12); Axis (22) |
| The fix is a process change | **No model**: EDA / funnel analysis | Cashfree (2); Zerodha (29) |

### How do they evaluate models from a business perspective?
Accuracy alone fails, because fraud, mule and default rates are small. A model that predicts "never fraud" is about 99% accurate and worthless. The cases instead use:
- **Precision and recall against a baseline.** Paytm: 20/50 → 65.1/74.1 (Case 8).
- **Fixed alert-budget comparison**, which builds operations capacity into the metric. Razorpay: 5x fraud found with no extra alerts (Case 3).
- **False-positive proxies the business already tracks.** PhonePe's ~1% reinstatement rate (Case 6); RBIH's alert precision (Case 9).
- **AUC to compare data sources.** Bureau 59% vs footprint 74% (Case 13).
- **Rank ordering / lift.** Kissht's 5.17x top-to-bottom bad-rate ratio (Case 14).
- **Calibration**, because routing and pricing need true probabilities, not just ranks (Case 3).
- **Money.** GMV recovered (Case 1); loss rate; "expected bad amount rate" (Case 11).
- **Conversion and revenue.** Incremental revenue and CPC (Case 20); test-vs-control lift (Case 22).
- **Operations.** TAT (Cases 11, 16, 24), analyst-hours (Case 5), collection efficiency (Case 12), agent productivity (Case 26).
- **Non-inferiority.** HDFC's delinquency "on par" with physical loans, at 10 seconds (Case 17).

### How do they present results to business stakeholders?

| Format | Example |
|---|---|
| Before/after vs baseline | Paytm P/R baseline vs production (8); Razorpay manual 20 min → 8–12 s (5) |
| Controlled experiments | Juspay 21-day routing comparison (1); Axis test vs control (22); PhonePe A/B vs random & rules (20) |
| Decision packages / scorecards | Lendingkart score 300–900 + bucket A–F + loan amount (11) |
| Policy tables | Navi DPD bucket → channel (12); Paytm score tier → action (8) |
| ROI in rupees/dollars | ~$15K GMV saved (1); ~$500K alert cost base (4); $1M monthly premium via bot (26) |
| Business KPIs, not ML metrics | Fraud complaints −38% (6); approval rate +50% (11); collection efficiency 96.63% (12) |
| Insight → product change | Policybazaar cashless-hospital insight → integration (27) |

---

# LEARNING ROADMAP FOR A FINTECH DATA SCIENTIST

| # | Topic | Why it matters | Practise on these cases |
|---|---|---|---|
| 1 | **SQL & data extraction** | Every case starts with joining transaction, customer and outcome tables | Build Juspay-style SR by gateway × BIN (1); Cashfree stage funnel (2) |
| 2 | **Exploratory data analysis** | Many wins came from one EDA insight | Cashfree auth-vs-authorisation (2); Policybazaar chat conversion 2x (26) |
| 3 | **Probability & statistics** | SR, default rate and fraud rate are proportions | Binomial/normal approximation in Juspay (1); Bayes' rule in Paytm (21) |
| 4 | **Hypothesis testing** | Telling a real 1% SR gain from noise | Juspay Z-score comparison (1); Lendingkart periodic stat tests (11) |
| 5 | **Regression (incl. logistic)** | Interpretable drivers; regulatory scorecards | Logit models in Case 13; Navi scorecards (12) |
| 6 | **Classification** | Fraud, mule, default, conversion | PhonePe (6), Paytm (8), Lendingkart (11) |
| 7 | **Feature engineering** | Usually decides the result | Lendingkart aggregate/trend/momentum families (11); Cashfree velocity & graph (7) |
| 8 | **Imbalanced classification** | Fraud and default are rare | Paytm 1:5 class weights, PR curves (8) |
| 9 | **Model evaluation (business-aware)** | Accuracy misleads | Precision/recall vs baseline (8); fixed alert budget (3); AUC by data source (13); lift ratio (14) |
| 10 | **Credit-risk modelling** | Core of Indian lending fintech | Lendingkart (11), Navi (12), Case 13, Kissht (14), HDFC (17), Axis (18) |
| 11 | **Fraud detection & label design** | Labels are noisy and delayed | PhonePe dispute removal (6); Razorpay delayed labels (3); RBIH typologies (9) |
| 12 | **Graph analytics** | Fraud rings, mules, identity linking | Simpl (10); Cashfree (7) |
| 13 | **Customer segmentation** | Policies and models differ by segment | Navi cohorts (12); Kissht 39 sub-models (14); Axis segments (22) |
| 14 | **Experimentation / A/B testing & causal thinking** | Proves the lift is real | PhonePe A/B (20); Axis test vs control (22); critique Zerodha pre/post (29) |
| 15 | **Bandits & online decisioning** | When your decisions shape your data | Juspay routing (1) |
| 16 | **Time-series & anomaly detection** | Monitoring payment health | Razorpay ADA calendar baselines (4) |
| 17 | **Recommendation systems & expected-value ranking** | Cross-sell, LTV growth | PhonePe propensity × LTV (20); Paytm Bayesian (21) |
| 18 | **NLP, CV & document AI** | Claims, KYC, support, calls | ICICI Lombard (24, 25); BharatPe KYC (16); Policybazaar ASR (27); PhonePe support (30) |
| 19 | **Model explainability & governance** | RBI digital-lending rules, credit committees | Lendingkart XGBoost explainability (11); HDFC layered P27 (17) |
| 20 | **Deployment & real-time ML** | Latency budgets of 5–80 ms | Juspay 5 ms (1); Simpl 70–80 ms Flink (10); PhonePe Yoda/Kratos (6) |
| 21 | **Model monitoring & retraining** | Fraud and markets drift | PhonePe feedback retraining (6); Cashfree auto-tuning (7); Razorpay out-of-time slices (3) |
| 22 | **Business communication** | Turning metrics into decisions | GMV saved (1); policy tables (12); before/after (5) |
| 23 | **Decision-making with data** | Translating scores into actions under capacity limits | Paytm tiered actions (8); Navi bucket allocation (12); Policybazaar lead routing (28) |

---

# APPENDIX — ITEMS FOUND BUT NOT COUNTED AS CASES

| Item | Why excluded / evidence |
|---|---|
| Razorpay Optimizer ("tree-based ML", 150+ parameters, "up to 10%" SR) — blog, 10 Jan 2024 | Marketing post; likely overlaps with Case 3 |
| Razorpay AIOps incident prediction ("up to 8 minutes earlier") — 2 Jan 2025 | Models not named |
| Razorpay Thirdwatch acquisition (RTO fraud) — 5 Aug 2019 | Only a target of a 30–40% fraud reduction |
| PhonePe Guardrails (identity graph, device fingerprinting, on-device models) — 27 Mar 2025 | Descriptive; no metrics |
| Moneyview DRHP (100,000+ variables; annualised loss rate 7.07%) — Mar 2026 summary | Secondary summary; no method detail |
| PaySense SMS-mining ML pipeline (Fifth Elephant 2017 proposal) | Proposal only; no results |
| Spocto (Yubi) collections (80% self-pay increase, unnamed bank) | Vendor case study; no methods |
| Federal Bank "Feddy" (Dialogflow; 98% accuracy, +25% CSAT) | Customer-service chatbot; similar to Cases 26 and 30 |
| Bank of Baroda speech analytics (Verint; +5% sales conversion) | Vendor case study |
| InsuranceDekho RAG advisor assistant (80% faster responses) — AWS, 18 Nov 2024 | GenAI tooling; similar to Case 25 |
| Dhan support chatbot (60% resolution vs 33%) — AWS | Similar to Case 30 |
| NPCI UPI fraud platform (20 ms SLA, 24B txns/month) | Third-party summary of a talk; speaker unidentified |
| Paytm, SBI, HDFC "uses AI for fraud", Acko pricing engine, Star Health FWA, Bajaj Finance scorecards | Evidence level D: generic claims |
| arXiv 2308.01028 (bandit payment routing, +0.92% SR) | Dream11 paper, not a fintech company |

### Gaps found during research
- **No usable public DS case studies** for CRED, Groww (modelling), Pine Labs, PayU India, Fino Payments Bank, Jupiter, Fi, Navi (beyond the DRHP), KreditBee, CASHe, slice, Yubi, Perfios, ICICI Bank, Kotak and SBI (beyond high-level claims).
- **No production source publishes KS or Gini.** Indian lenders treat model performance as confidential. DRHPs and RHPs are the richest public source on model governance.
- **Wealthtech engineering blogs focus on infrastructure, not modelling.**
