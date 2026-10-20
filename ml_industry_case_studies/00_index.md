# ML in Industry: 60 Case Studies for Junior Data Scientists

A mentor-style guide with 60 realistic case studies from Indian finance, quick commerce and EdTech. Every case follows the same ten-part structure, from business context to a focus checklist, so you can compare how the same ideas show up in different settings.

---

## 1. Folder Layout

| Folder | Cases | Count |
| --- | --- | --- |
| [finance/](finance/) | 1 to 4 and 11 to 30 | 24 |
| [qcommerce/](qcommerce/) | 5 to 8 and 31 to 50 | 24 |
| [edtech/](edtech/) | 9, 10 and 51 to 60 | 12 |
| [99_frameworks_and_lessons.md](99_frameworks_and_lessons.md) | Decision table, flowchart, domain comparison, 15 lessons, self-test | 1 |

- Cases 1 to 10 are the original "core ten". They are the most common industry and interview problems, and they teach the main ideas.
- Cases 11 to 60 extend each domain with more problems. Each one teaches a decision that the core ten did not.
- The core ten use one fictional company per domain, and the extension cases use their own fictional companies. All numbers are teaching figures, not real data.

---

## 2. How to Use This Guide

- **Start with the core ten.** Read cases 10, 9, 1, 2, 5 and 6 first, then branch out by interest.
- **Read one case a day.** Each takes 40 to 60 minutes. Take notes on the "What if" tables in section 4.
- **Try the "What if" tables first.** Cover the recommended action column, write your own answer, then compare.
- **Rebuild the rupee maths.** Section 6 of each case turns a model metric into business value. Recompute it yourself.
- **Use the cross-case file for real projects.** [99_frameworks_and_lessons.md](99_frameworks_and_lessons.md) maps situations (imbalance, latency, cold start and others) to approaches.
- **Test yourself.** The 10-question self-assessment is at the end of the frameworks file.

### The structure of every case

| Part | What it teaches |
| --- | --- |
| 1. Business Context | Who is hurt, by how much, and who wants what |
| 2. Translating Business to ML | The ML question, the target, the unit, the timing |
| 3. Data Understanding | Sources, volume, data issues, and where juniors go wrong |
| 4. Approach and Decision Points | Baseline, model choices, and "What if" scenarios |
| 5. Feature Engineering | Top 10 features and the leakage traps |
| 6. Evaluation Strategy | Metrics, misleading metrics, validation, rupee value |
| 7. Deployment and Monitoring | Batch or real time, drift, retraining, A/B tests |
| 8. Stakeholder Communication | A ready-to-use explanation and the questions leaders ask |
| 9. Common Pitfalls and Lessons | Mistakes, causes and cures |
| 10. Mentor's Focus Checklist | Where to spend 80% of your effort, and the key takeaway |

---

## 3. Finance Cases (24)

| # | Case study | Problem type | Difficulty |
| --- | --- | --- | --- |
| 1 | [Unsecured Personal Loan Default Scoring](finance/01_finance_credit_default_scoring.md) | Binary classification | Intermediate |
| 2 | [Real-Time UPI and Card Fraud Detection](finance/02_finance_fraud_detection.md) | Imbalanced classification and anomaly detection | Advanced |
| 3 | [Collections Prioritisation](finance/03_finance_collections_prioritization.md) | Ranking, uplift and capacity optimisation | Advanced |
| 4 | [Savings-Account Attrition in Retail Banking](finance/04_finance_banking_churn.md) | Classification with time-to-event thinking | Intermediate |
| 11 | [Credit Card Limit Assignment](finance/11_finance_credit_card_limit_assignment.md) | Regression and constrained optimisation | Advanced |
| 12 | [Application Fraud and Synthetic Identity](finance/12_finance_application_fraud_synthetic_identity.md) | Classification with graph features | Advanced |
| 13 | [Risk-Based Loan Pricing](finance/13_finance_risk_based_loan_pricing.md) | Regression and price-elasticity optimisation | Advanced |
| 14 | [MSME Cash-Flow Lending](finance/14_finance_msme_cashflow_lending.md) | Classification and limit sizing on small data | Intermediate |
| 15 | [Early-Warning Signals on the Loan Book](finance/15_finance_portfolio_early_warning.md) | Classification and hazard modelling | Intermediate |
| 16 | [Health Insurance Claim Fraud](finance/16_finance_health_claim_fraud.md) | Anomaly detection and investigation ranking | Advanced |
| 17 | [Motor Insurance Pricing](finance/17_finance_motor_insurance_pricing.md) | Frequency and severity regression | Advanced |
| 18 | [AML Alert Reduction](finance/18_finance_aml_alert_reduction.md) | Alert prioritisation on top of rules | Advanced |
| 19 | [Cross-Sell and Customer Lifetime Value](finance/19_finance_cross_sell_clv.md) | Multi-class propensity and regression | Intermediate |
| 20 | [ATM Cash Forecasting](finance/20_finance_atm_cash_forecasting.md) | Time series and replenishment optimisation | Intermediate |
| 21 | [Transaction Categorisation](finance/21_finance_transaction_categorisation.md) | NLP classification and entity matching | Intermediate |
| 22 | [Customer-Service Intent Routing](finance/22_finance_support_intent_routing.md) | NLP classification with automation thresholds | Intermediate |
| 23 | [SIP Stoppage and Investor Churn](finance/23_finance_sip_stoppage_churn.md) | Classification across market regimes | Intermediate |
| 24 | [Loan Prepayment and Foreclosure](finance/24_finance_loan_prepayment.md) | Survival with competing risks | Advanced |
| 25 | [Expected Credit Loss and Stress Testing](finance/25_finance_expected_credit_loss_stress_testing.md) | PD, LGD and EAD modelling with scenarios | Advanced |
| 26 | [Video-KYC Face Match](finance/26_finance_video_kyc_face_match.md) | Computer vision verification | Advanced |
| 27 | [Payment Routing Success Rate](finance/27_finance_payment_routing_success_rate.md) | Contextual bandit | Advanced |
| 28 | [Credit Model Fairness Audit](finance/28_finance_credit_model_fairness_audit.md) | Model audit and fairness analysis | Intermediate |
| 29 | [Insurance Renewal Persistency](finance/29_finance_insurance_renewal_persistency.md) | Classification and survival | Intermediate |
| 30 | [BNPL Micro-Limit Underwriting](finance/30_finance_bnpl_micro_limit_underwriting.md) | Classification with exploration policy | Advanced |

---

## 4. Quick Commerce Cases (24)

| # | Case study | Problem type | Difficulty |
| --- | --- | --- | --- |
| 5 | [SKU-Level Demand Forecasting per Dark Store](qcommerce/05_qcommerce_demand_forecasting.md) | Hierarchical, intermittent time series | Advanced |
| 6 | [Delivery ETA Prediction](qcommerce/06_qcommerce_eta_prediction.md) | Quantile regression | Intermediate |
| 7 | [Dynamic Discount Optimisation](qcommerce/07_qcommerce_dynamic_discount_optimization.md) | Causal estimation and optimisation | Advanced |
| 8 | [Stock-Out and Phantom Inventory Detection](qcommerce/08_qcommerce_stockout_phantom_inventory.md) | Anomaly detection with weak labels | Intermediate |
| 31 | [In-App Search Ranking](qcommerce/31_qcommerce_search_ranking.md) | Learning to rank | Advanced |
| 32 | [Cart Add-On Recommendations](qcommerce/32_qcommerce_cart_addon_recommendation.md) | Recommender system | Intermediate |
| 33 | [Rider Demand and Shift Planning](qcommerce/33_qcommerce_rider_demand_shift_planning.md) | Forecasting and staffing optimisation | Intermediate |
| 34 | [Order Batching and Rider Assignment](qcommerce/34_qcommerce_order_batching_rider_assignment.md) | Combinatorial optimisation with ML inputs | Advanced |
| 35 | [Dark-Store Location Selection](qcommerce/35_qcommerce_dark_store_location_selection.md) | Spatial regression and site ranking | Intermediate |
| 36 | [Replenishment and Reorder Optimisation](qcommerce/36_qcommerce_replenishment_reorder_optimisation.md) | Inventory optimisation | Advanced |
| 37 | [Fresh Produce Quality Grading](qcommerce/37_qcommerce_fresh_produce_quality_grading.md) | Image classification | Intermediate |
| 38 | [Customer Churn and Reactivation](qcommerce/38_qcommerce_customer_reactivation.md) | Classification and targeting | Intermediate |
| 39 | [New-User Conversion and Early LTV](qcommerce/39_qcommerce_new_user_conversion_early_ltv.md) | Regression and classification | Intermediate |
| 40 | [Promo Abuse and Refund Fraud](qcommerce/40_qcommerce_promo_abuse_refund_fraud.md) | Classification and graph anomaly detection | Advanced |
| 41 | [Item Substitution Recommendation](qcommerce/41_qcommerce_item_substitution.md) | Ranking with acceptance prediction | Intermediate |
| 42 | [Delivery and Small-Cart Fee Optimisation](qcommerce/42_qcommerce_delivery_fee_optimisation.md) | Pricing with causal estimation | Advanced |
| 43 | [Picker Productivity and Pick Path](qcommerce/43_qcommerce_picker_productivity_pick_path.md) | Regression and layout optimisation | Intermediate |
| 44 | [Catalogue Matching and Attribute Extraction](qcommerce/44_qcommerce_catalogue_matching_attribute_extraction.md) | NLP and vision entity matching | Intermediate |
| 45 | [Supplier Lead-Time and Fill-Rate](qcommerce/45_qcommerce_supplier_lead_time_fill_rate.md) | Regression and supplier risk | Intermediate |
| 46 | [Support Ticket Triage](qcommerce/46_qcommerce_support_ticket_triage.md) | NLP classification and refund policy | Intermediate |
| 47 | [Push-Notification Optimisation](qcommerce/47_qcommerce_push_notification_optimisation.md) | Contextual bandit and uplift | Intermediate |
| 48 | [Rider Attrition](qcommerce/48_qcommerce_rider_attrition.md) | Survival and classification | Intermediate |
| 49 | [Rider GPS Spoofing Detection](qcommerce/49_qcommerce_rider_gps_spoofing.md) | Trajectory anomaly detection | Advanced |
| 50 | [Intraday Nowcasting and Surge Staffing](qcommerce/50_qcommerce_intraday_nowcasting_surge_staffing.md) | Short-horizon forecasting | Advanced |

---

## 5. EdTech Cases (12)

| # | Case study | Problem type | Difficulty |
| --- | --- | --- | --- |
| 9 | [Course Dropout Early-Warning System](edtech/09_edtech_dropout_prediction.md) | Time-aware classification | Intermediate |
| 10 | [Lead Scoring for Paid-Course Conversion](edtech/10_edtech_lead_scoring.md) | Ranking and propensity | Beginner |
| 51 | [Next-Best-Content Recommendation](edtech/51_edtech_next_best_content_recommendation.md) | Recommender with a learning objective | Advanced |
| 52 | [Subjective Answer Grading](edtech/52_edtech_subjective_answer_grading.md) | NLP ordinal scoring | Advanced |
| 53 | [Knowledge Tracing and Adaptive Testing](edtech/53_edtech_knowledge_tracing_adaptive_testing.md) | Sequence modelling and item response theory | Advanced |
| 54 | [Course Cross-Sell Recommendation](edtech/54_edtech_course_cross_sell_recommendation.md) | Propensity and recommender | Intermediate |
| 55 | [Refund Prediction and Abuse](edtech/55_edtech_refund_prediction_abuse.md) | Time-to-event classification and abuse detection | Intermediate |
| 56 | [Doubt Routing and Answer Retrieval](edtech/56_edtech_doubt_routing_retrieval.md) | Retrieval, ranking and routing | Advanced |
| 57 | [Live-Class Engagement and Instructor Quality](edtech/57_edtech_live_class_engagement_instructor_quality.md) | Hierarchical scoring with fairness | Intermediate |
| 58 | [Placement Outcome Prediction](edtech/58_edtech_placement_outcome_prediction.md) | Classification with decision support | Intermediate |
| 59 | [Marketing Budget Allocation and CAC to LTV](edtech/59_edtech_marketing_budget_allocation_cac_ltv.md) | Marketing mix, incrementality, predicted LTV | Advanced |
| 60 | [Exam Proctoring and Cheating Detection](edtech/60_edtech_exam_proctoring_cheating_detection.md) | Multimodal anomaly detection | Advanced |

---

## 6. Problem Types Covered

| Problem type | Cases |
| --- | --- |
| Classification and propensity | 1, 4, 9, 10, 14, 15, 23, 29, 38, 39, 55, 58 |
| Fraud, abuse and anomaly detection | 2, 8, 12, 16, 18, 40, 49, 60 |
| Ranking, recommendation and retrieval | 3, 19, 31, 32, 41, 51, 54, 56 |
| Time-series forecasting and nowcasting | 5, 20, 33, 50 |
| Regression | 6, 17, 43, 45, 57 |
| Optimisation and causal decisions | 7, 11, 13, 34, 36, 42, 59 |
| Survival and time-to-event | 4, 15, 24, 29, 48 |
| Bandits and exploration | 27, 30, 47, 51 |
| NLP, vision and entity matching | 21, 22, 26, 37, 44, 46, 52 |
| Model risk, fairness and governance | 1, 25, 28 |
| Spatial, sequence and measurement | 35, 53 |

---

## 7. Suggested Learning Paths

| If you want to learn... | Read in this order |
| --- | --- |
| The basics of applied ML in a business | 10, 9, 1, 4, 38 |
| Rare events and real-time systems | 2, 6, 8, 12, 27, 40 |
| Forecasting and supply chain | 5, 8, 20, 33, 36, 50 |
| Causal thinking and decisions under constraints | 3, 7, 13, 42, 47, 59 |
| Recommendation and search | 31, 32, 41, 51, 54, 56 |
| Fraud and abuse across domains | 2, 12, 16, 18, 40, 49, 55, 60 |
| NLP and vision in industry | 21, 22, 26, 37, 44, 46, 52 |
| Regulated and high-stakes environments | 1, 25, 26, 28, 58, 60 |
| Interview preparation | 1, 2, 5, 7, 17, 31, 36, 59, then the self-test in the frameworks file |

---

## 8. Common Terms Used in the Guide

| Term | Meaning |
| --- | --- |
| DPD (Days Past Due) | Number of days a payment is overdue. 90 DPD is the NPA (non-performing asset) mark in RBI norms |
| KS and Gini | Standard measures of how well a score separates good and bad customers in credit risk |
| PR-AUC | Area under the precision-recall curve, a better measure than ROC-AUC for rare events |
| WAPE | Weighted Absolute Percentage Error, total absolute error divided by total actual volume |
| Pinball loss | The loss function used to train and judge quantile forecasts |
| Uplift | The extra effect caused by an action, compared with doing nothing |
| PSI (Population Stability Index) | A measure of how much a distribution has shifted between two periods |
| Leakage | Using information that would not be available at prediction time |
| Cold start | Predicting for something new that has no history |
| Champion-challenger | Running a new model against the current one on a share of traffic |
| Contextual bandit | A method that chooses actions and learns from their results while still exploring |
| Survival analysis | Modelling the time until an event, while handling cases where it has not happened yet |
