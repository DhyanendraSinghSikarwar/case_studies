# Case Study 8 — Two-sided Marketplace Dynamic Pricing (Quick-commerce / Gig platforms)

**Reference repo:** [R8 akash-sood97/two-sided-pricing-engine](https://github.com/akash-sood97/two-sided-pricing-engine) — "ISB AMPBA"; two-sided demand (customer elasticity + partner drop-off), per-segment optimiser with ₹220 partner pay floor and 90% fulfilment target; +7.1% contribution vs +3.2% for demand-only pricing; holdout, placebo and 400-draw robustness.

### 8.1 Business problem
A home-services / quick-commerce platform sets customer price **and** partner payout per (city × service × time-slot). Raising price lowers demand; lowering payout lowers partner acceptance → unfulfilled orders. Maximise contribution subject to fulfilment ≥ 90% and payout floor.

- **KPIs:** contribution uplift vs current pricing; fulfilment rate; partner earnings per hour.

### 8.2 Data — simulator (`src/mkt/sim.py`)
- 6 cities × 5 services × 4 time-slots × 52 weeks; segment-level base demand with seasonality.
- Customer demand: `D = D0 * (p/p0)^ε_c`, ε_c segment-specific drawn from priors whose mean is **calibrated** from Online Retail II price-quantity regressions (reuse Case 5 `demand.py`; note this calibration is an analogy).
- Partner supply: acceptance prob `A = sigmoid(α + β*(payout - reservation_wage))`; partner churn weekly if earnings < threshold.
- Historical log: random price experiments (±10%) on 20% of segment-weeks to allow estimation.

### 8.3 Modules (`PKG=mkt`)
```
src/mkt/
  sim.py         generate history + ground-truth parameters
  estimate.py    customer elasticity via log-log with segment FE on experiment rows; partner acceptance via logistic regression
  optimise.py    per segment grid/convex search over (price, payout) maximising
                 contribution = D(p)*min(1, A(w)*capacity/D)*(p - w - var_cost) s.t. fulfil>=0.9, w>=220
  policies.py    current (static), demand-only (ignores supply), two-sided (ours)
  validate.py    temporal holdout (last 12 weeks), placebo test (shuffled prices -> no gain), 400 posterior draws of params
  explorer/      optional stlite static page
app/streamlit_app.py  segment selector, price & payout sliders, live demand/fulfilment/contribution surface (plotly 3D/heatmap)
```

### 8.4 Acceptance criteria
- [ ] Estimated elasticities within ±20% of simulator truth (recovery test).
- [ ] Two-sided policy > demand-only > static on holdout contribution with fulfilment ≥ 90%.
- [ ] Robustness: % of 400 draws where two-sided wins ≥ 80%.

### 8.5 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 8 "Two-sided Marketplace Dynamic Pricing" per spec. PKG=mkt.
Follow github.com/akash-sood97/two-sided-pricing-engine; simulator with known truth so parameter recovery is testable.
Milestones: M1 simulator, M2 estimation+recovery tests, M3 optimiser+policies, M4 validation (holdout/placebo/draws), M5 app/memo/CI.
[PASTE SECTION 8.1–8.4 HERE]
```
