# Book 1 — Part 11: ML System Design (Question List)

**Topic:** ML system design (framework, fraud, feed, ETA, pricing, churn, recsys, search, CTR, credit, forecasting, notifications, trade-offs)
**Target:** 40 questions  |  **Actual:** 53  |  **Date:** 2026-10-20

_Cross-references: MLOps tooling depth -> Book 4; GenAI system design -> Book 2; recsys/ranking algorithms -> Part 7._

### Q1 ⭐⭐⭐ 🟢 Walk me through your end-to-end framework for any ML system design question (requirements to monitoring).
**Asked at:** All companies; product, fintech, GCC, Europe
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 A product manager says 'reduce fraud' (or 'reduce churn'). How do you turn that vague ask into a well-defined ML problem with a success metric?
**Asked at:** Product cos, fintech, consulting-style DS rounds
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Batch vs real-time (online) inference: how do you decide for a given use case?
**Asked at:** Product cos, Amazon, Flipkart, GCCs
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 Design a fraud detection system for UPI / card payments.
**Asked at:** PhonePe, Paytm, Amazon Pay, JPMC/GCCs, Klarna, DoorDash-type marketplaces
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Design a news-feed / social-media feed ranking system.
**Asked at:** Meta-type, ShareChat, Instagram, product cos
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Design a recommendation system for an e-commerce home page at scale.
**Asked at:** Flipkart, Amazon, Zalando, Spotify, Walmart
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Design an ETA prediction system for food or grocery delivery.
**Asked at:** Swiggy, Zomato, Uber, DoorDash
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Design a customer churn prediction and retention system.
**Asked at:** Telecom, SaaS, fintech, Booking, Spotify, GCCs
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Design a demand forecasting system for a retailer or quick-commerce platform.
**Asked at:** Walmart, Amazon, Zalando, Swiggy Instamart, Bain-type consulting DS
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Design a credit risk / loan default scoring system.
**Asked at:** JPMC and bank GCCs, Klarna, Indian NBFCs/fintech
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Design an ad click-through rate (CTR) prediction system.
**Asked at:** Amazon Ads, Flipkart Ads, Meta, Google, Microsoft
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Design a search ranking system for an e-commerce site.
**Asked at:** Flipkart, Amazon, Walmart, Booking, Zalando
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you choose offline metrics and online metrics for an ML system, and what do you do when they disagree?
**Asked at:** Product cos, Amazon, Spotify, Booking
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do you handle the cold-start problem (new users, new items) in a production system?
**Asked at:** Flipkart, Spotify, Zalando, Swiggy
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 What is training-serving skew and how do you prevent it?
**Asked at:** Amazon, Microsoft IDC, Flipkart, GCCs
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 How would you monitor an ML model in production and decide when to retrain?
**Asked at:** Almost all MLE/DS loops (deep tooling in Book 4)
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 What are feedback loops and selection bias in deployed ML systems, and how do you mitigate them?
**Asked at:** Product cos, Spotify, Meta-type, Flipkart
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 Walk through how you would prevent data leakage when building training data for a time-dependent system.
**Asked at:** Fintech, GCCs, product cos
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 When should you not use ML at all? How do you decide between rules, heuristics and a model?
**Asked at:** Fintech, consulting-style DS, startups
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 Do a back-of-envelope estimate of QPS, storage and latency budget for a ranking or fraud system.
**Asked at:** Amazon, Flipkart, Microsoft IDC, senior roles
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Why do large-scale recommender and search systems use a multi-stage (retrieval, ranking, re-ranking) architecture?
**Asked at:** Flipkart, Amazon, Spotify, Zalando
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Design a dynamic / surge pricing system.
**Asked at:** Uber, Swiggy, Booking, airlines, Flipkart
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Design a notification / push system that decides what to send, to whom and when.
**Asked at:** Swiggy, Zomato, Flipkart, Spotify, PhonePe
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Design a content moderation or spam / abuse detection system.
**Asked at:** Social/product cos, ShareChat, Microsoft
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Design an anomaly detection system for business or payment metrics.
**Asked at:** Fintech, GCCs, Walmart
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Design a model to predict cash-on-delivery order cancellations or return-to-origin (RTO) in Indian e-commerce.
**Asked at:** Flipkart, Meesho, Amazon India
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Design a product-return prediction system for a fashion marketplace.
**Asked at:** Zalando, Myntra, Amazon
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Design a customer lifetime value (LTV) prediction system.
**Asked at:** Booking, Spotify, fintech, e-commerce
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Design a lead scoring / propensity-to-buy model for sales or lending.
**Asked at:** Fintech, banks, SaaS, GCCs
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Design a Spotify-style personalised playlist / 'because you watched' recommender.
**Asked at:** Spotify, Netflix-type, Hotstar
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Design a restaurant / dish ranking system for a food-delivery app.
**Asked at:** Swiggy, Zomato, DoorDash
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Design a customer-support ticket routing and prioritisation system.
**Asked at:** Amazon, Microsoft, SaaS, GCCs
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you design real-time velocity and aggregate features for fraud, and where do they live (feature store)?
**Asked at:** PhonePe, Paytm, Klarna, JPMC
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you handle concept drift and adversaries adapting in a fraud system?
**Asked at:** Fintech, Klarna, PhonePe, GCCs
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How do you roll out a new model safely (shadow, canary, A/B) and decide to ramp up?
**Asked at:** Amazon, Flipkart, Spotify, Microsoft
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do you reduce inference cost and latency (cascade models, distillation, caching, quantisation) without losing quality?
**Asked at:** Amazon, Flipkart, Microsoft IDC, product cos
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do you incorporate exploration vs exploitation (bandits) into a recommender or notification system?
**Asked at:** Spotify, Flipkart, Booking, Meta-type
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you design a human-in-the-loop review queue for fraud or moderation and use analyst feedback as labels?
**Asked at:** Fintech, JPMC, Klarna, PhonePe
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 How do you ensure explainability and regulatory compliance (RBI, GDPR, EU AI Act) in a credit or fraud model?
**Asked at:** Banks/GCCs, Klarna, Europe fintech
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 AI-era: when would you use an LLM inside a classic ML system (classification, feature extraction, explanations) versus a trained classifier or embedding model?
**Asked at:** Product cos 2025-26, Amazon, Microsoft; GenAI depth in Book 2
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 AI-era: how do embeddings, two-tower models and vector search change retrieval in search and recommendation systems?
**Asked at:** Flipkart, Amazon, Spotify, Booking; algorithm depth in Part 7
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🔴 Design a delivery-partner / driver assignment (matching) system.
**Asked at:** Swiggy, Zomato, Uber, DoorDash
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🔴 Design a hierarchical demand-forecasting system for 100k+ SKU-store combinations with promotions and stock-outs.
**Asked at:** Walmart, Amazon, Zalando, Instamart
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 Design a 'people you may know' / friend recommendation system.
**Asked at:** Meta-type, LinkedIn, ShareChat
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 Design a search autocomplete / query suggestion system.
**Asked at:** Flipkart, Amazon, Google, Microsoft
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 How would you decide between one global model and per-country / per-segment models across markets?
**Asked at:** Booking, Zalando, Spotify, Amazon (Europe/global)
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 How do you design for privacy and data minimisation (DPDP Act, GDPR) in a personalisation system?
**Asked at:** Europe companies, banks, GCCs
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 AI-era: you are handed an AI-generated ML system design or architecture doc. What red flags do you look for in review?
**Asked at:** 2025-26 AI-assisted rounds, GCCs
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 Design a system that handles delayed conversion feedback (ads / lending) when labels arrive days or weeks late.
**Asked at:** Amazon Ads, Flipkart Ads, fintech
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 How do you correct position bias and evaluate a ranker offline using logged data (counterfactual evaluation)?
**Asked at:** Flipkart, Amazon, Spotify, Booking
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 Design a multi-objective ranking system balancing engagement, revenue, creator fairness and integrity.
**Asked at:** Meta-type, Spotify, ShareChat, senior roles
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 Design a fairness and bias audit process for a credit-scoring model.
**Asked at:** Banks/GCCs, Klarna, Europe fintech
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 Design an inventory replenishment system for dark stores combining forecasting and optimisation.
**Asked at:** Swiggy Instamart, Zepto, Walmart, Amazon
<!-- ANSWER_PENDING -->
