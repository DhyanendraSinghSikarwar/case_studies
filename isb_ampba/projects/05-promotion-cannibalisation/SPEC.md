# Case Study 5 — Promotion Cannibalisation Engine (E-commerce Pricing)

**Reference repo:** [R7 akash-sood97/promotion-cannibalisation-engine](https://github.com/akash-sood97/promotion-cannibalisation-engine) — "ISB AMPBA"; on UCI Online Retail II shows the dashboard-preferred promo looks profitable in 86% of conditions but is profitable for the whole family in only 11%.

### 5.1 Business problem
Category managers judge promotions by the promoted SKU's uplift. Build an engine that scores a discount on **family net contribution** = incremental margin − subsidy on baseline units − margin lost on cannibalised siblings + basket pull (halo).

- **KPIs:** % of proposed promos correctly classified profitable/unprofitable vs simulation truth; ₹/£ net contribution per promo; break-even elasticity.

### 5.2 Data
- UCI Online Retail II — https://archive.ics.uci.edu/dataset/502/online+retail+ii — ~1M lines, UK online retailer, 2009-12 → 2011-12. Load via `fetch_ucirepo(id=502)`; if unavailable, download the xlsx from the UCI page (two sheets) with `pd.read_excel(sheet_name=None)`.
- Clean: drop cancellations (Invoice starts with "C"), Quantity ≤ 0, Price ≤ 0, non-product StockCodes (POST, M, DOT, BANK CHARGES, etc.), missing Customer ID kept for basket analysis only.

### 5.3 Modules (`PKG=promo`)
```
src/promo/
  data.py        load_clean(); weekly SKU panel (units, avg price, revenue, n_baskets)
  catalog.py     product families: TF-IDF on Description + agglomerative clustering, plus
                 co-purchase substitution check (substitutes rarely co-occur in a basket); manual override CSV
  baskets.py     association rules (mlxtend FP-Growth) -> lift/confidence; halo pull per SKU
  demand.py      (a) log-log elasticity regression per SKU with week FE where price varies;
                 (b) MNL/nested-logit choice model per family calibrated to shares (outside option = no purchase)
  engine.py      score_promo(sku, discount, params) -> {direct_uplift, subsidy_cost, cannibalised_margin,
                 halo_margin, family_net}; break_even_elasticity(sku, discount)
  sweep.py       Latin-hypercube sweep over elasticity [-1,-6], substitution share [0,0.8], margin [25%,55%],
                 halo discount [0,1] -> % conditions profitable (promoted-only vs family)
  optimise.py    pick best discount ∈ {0,5,10,15,20,25%} per family under budget constraint (pulp)
  viz.py         waterfall chart of contribution, tornado sensitivity, heatmaps
analysis/run_analysis.py  -> outputs/summary.json, figures/*.png, docs/DECISION_MEMO.md numbers
app/streamlit_app.py
```

### 5.4 Method
1. EDA: top families, price variation availability, seasonality (Q4 peak).
2. Build families; validate with low co-purchase rate among members.
3. Estimate elasticities where identifiable; otherwise priors + sweep (state this honestly).
4. Choice model → cannibalisation share; basket rules → halo.
5. Score a reference promotion (10% off) for 24 top SKUs; waterfall.
6. Sweep; report % profitable promoted-only vs family-net; break-even elasticity distribution.
7. Optimiser recommends promo calendar for next 8 weeks under discount budget.

### 5.5 App
Pick SKU + discount → waterfall (direct, subsidy, cannibalisation, halo, net) · sensitivity sliders · family view · recommended promo plan.

### 5.6 Acceptance criteria
- [ ] Engine identity test: family_net = direct − subsidy − cannibalised + halo (±1e-6).
- [ ] Sweep ≥ 1,000 draws; results reproducible with seed.
- [ ] Memo reports: reference promo family net, % profitable both views, break-even multiplier.

### 5.7 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 5 "Promotion Cannibalisation Engine" per spec. PKG=promo.
Data: UCI Online Retail II (id=502). Reproduce and extend github.com/akash-sood97/promotion-cannibalisation-engine
(add elasticity estimation where price varies, promo optimiser, Streamlit app).
Milestones: M1 data+families, M2 baskets+demand, M3 engine+sweep, M4 optimiser, M5 app/memo/CI.
[PASTE SECTION 5.1–5.6 HERE]
```
