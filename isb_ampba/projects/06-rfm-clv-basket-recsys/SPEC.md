# Case Study 6 — Customer Segmentation (RFM + CLV), Market Basket & Recommender (E-commerce Marketing)

**Reference repos:** [R17 RishabhBansal2409/Recommendation_Engine](https://github.com/RishabhBansal2409/Recommendation_Engine) (user/item CF) · ISB capstone title "Customer Profiling & Market Basket Analysis" (AMPBA Applied Learning page) · [R7](https://github.com/akash-sood97/promotion-cannibalisation-engine) for basket rules on the same data.

### 6.1 Business problem
CRM team needs (a) actionable segments, (b) 12-month CLV per customer, (c) cross-sell bundles, (d) personalised top-10 product recommendations for email campaigns.

- **KPIs:** silhouette ≥ 0.35 for segments; CLV MAE vs holdout spend; Recommender HitRate@10 and NDCG@10 beating popularity baseline by ≥ 30%.

### 6.2 Data
UCI Online Retail II (id=502), rows with Customer ID only. Calibration period up to 2011-06-30, holdout 2011-07-01 → 2011-12-09.

### 6.3 Modules (`PKG=crm`)
```
src/crm/
  data.py        clean (as Case 5) + customer-level table
  rfm.py         recency, frequency, monetary, tenure, avg basket, n_categories; quintile RFM codes;
                 named segments (Champions, Loyal, At-Risk, Hibernating, New, Big-spenders)
  cluster.py     log+scale; KMeans k=2..10 (elbow, silhouette), GMM, HDBSCAN comparison; profile table
  clv.py         lifetimes BG/NBD + Gamma-Gamma on calibration; predict holdout purchases & spend;
                 baseline = historical avg; metrics MAE, Spearman
  basket.py      FP-Growth (mlxtend) min_support tuned; rules filtered lift>3, conf>0.3; bundle candidates
  recsys.py      baselines: popularity, item-item cosine CF; models: implicit ALS (implicit lib), LightFM optional;
                 time-based split (last 30 days per user as test); HitRate@10, NDCG@10, coverage
  campaign.py    segment × action matrix (win-back, upsell, loyalty) with expected ₹ uplift assumptions
app/streamlit_app.py
```

### 6.4 Method
1. RFM + rule segments → cluster segments; compare & name.
2. CLV with BG/NBD/GG; calibration plot; top-decile CLV share.
3. Market basket rules → top 20 bundles with lift.
4. Recommender: baselines vs ALS; tune factors/regularisation; evaluate.
5. Campaign plan per segment with budget and expected ROI.

### 6.5 App
Segment explorer (2D UMAP plot, profile cards) · Customer 360 (RFM, CLV, recommendations) · Bundle finder · Campaign planner.

### 6.6 Acceptance criteria
- [ ] Time-based splits; no holdout leakage into CLV/recsys.
- [ ] Recsys beats popularity on NDCG@10 by ≥ 30%.
- [ ] Memo: segment sizes, revenue share, CLV top-decile share, campaign ROI table.

### 6.7 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 6 "RFM Segmentation, CLV, Market Basket & Recommender" per spec. PKG=crm.
Data UCI id=502. Extend github.com/RishabhBansal2409/Recommendation_Engine with implicit ALS and proper time split.
Milestones: M1 data+RFM, M2 clustering, M3 CLV, M4 basket+recsys, M5 campaign/app/memo/CI.
[PASTE SECTION 6.1–6.6 HERE]
```
