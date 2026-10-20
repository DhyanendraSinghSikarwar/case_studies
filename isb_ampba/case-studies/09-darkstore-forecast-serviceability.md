# Case Study 9 — Dark-store Demand Forecasting & Serviceability Optimiser (Quick-commerce Supply Chain)

**Reference repos:** [R10 akash-sood97/supply-serviceability-capstone](https://github.com/akash-sood97/supply-serviceability-capstone) (count forecast + MIP lever mix; hub-weeks at 95% service 74% → 100%, contribution ₹2.74M → ₹3.88M) · [R11 akash-sood97/distribution-network-design](https://github.com/akash-sood97/distribution-network-design) (PuLP/HiGHS vs heuristic) · [R13 Siddharth0711/Foundation-Project-2](https://github.com/Siddharth0711/Foundation-Project-2) (Holt-Winters/SARIMAX/Prophet/LSTM + P5/P50/P95) · [R12 Siddharth0711/AMPBA-Capstone-PharmaTrace](https://github.com/Siddharth0711/AMPBA-Capstone-PharmaTrace) (ABC-FSN + LP). ISB capstone theme: "Freight Optimization through Analytical Model".

### 9.1 Business problem
A 10-minute-delivery company runs 12 dark stores × 4 categories. Forecast weekly orders with uncertainty, then choose the cheapest mix of levers — add riders, rebalance riders across stores, surge price, cap intake, extend radius — to hold 95% on-time serviceability.

- **KPIs:** forecast WAPE beats seasonal-naive by ≥ 15%; P90 coverage 85–95%; % store-weeks meeting 95% SLA; ₹ contribution.

### 9.2 Data — generator (`src/qc/sim.py`)
Store × category × day for 2 years: trend, weekly + annual seasonality, Indian festival spikes (Diwali, Holi, IPL weekends via calendar CSV), weather shocks, promotions; rider capacity, rider cost/hour, order margin. Seeded. Provide real-data hook: `load_external(path)` expecting same schema.

### 9.3 Modules (`PKG=qc`)
```
src/qc/
  sim.py         generator + festival calendar
  features.py    lags, rolling means, calendar & festival flags, promo flag
  forecast.py    seasonal-naive, ETS/Holt-Winters, SARIMAX, Prophet, LightGBM global model (quantile 0.1/0.5/0.9),
                 optional N-BEATS/TFT via darts; rolling-origin backtest 8 folds
  reconcile.py   hierarchical reconciliation store->city (MinT via statsforecast/hierarchicalforecast) optional
  abc_fsn.py     ABC (value) × FSN (velocity) classification of SKUs for stocking policy
  inventory.py   safety stock = z*σ_LT*√LT; reorder point; service-level vs holding-cost curve
  optimise.py    MIP (pulp+HiGHS): decision vars riders_added[s,w], transfers[s,s',w], surge[s,w]∈levels, cap[s,w];
                 constraint served >= 0.95*demand_P90; minimise cost - margin; heuristic baseline (greedy + local search)
  evaluate.py    run plan against 200 simulated demand paths -> SLA attainment distribution
app/streamlit_app.py  forecast fan charts, lever plan table, map of stores (pydeck), what-if sliders (SLA target, rider cost)
```

### 9.4 Acceptance criteria
- [ ] Rolling-origin backtest table (WAPE, MASE, pinball loss) per model; best beats seasonal-naive ≥ 15%.
- [ ] MIP solution vs heuristic gap reported; MIP solves < 60 s.
- [ ] SLA attainment across 200 paths reported (mean & P10).
- [ ] Memo: lever mix, ₹ cost, SLA before/after.

### 9.5 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 9 "Dark-store Demand Forecasting & Serviceability Optimiser" per spec. PKG=qc.
Combine ideas from github.com/akash-sood97/supply-serviceability-capstone, github.com/akash-sood97/distribution-network-design
and github.com/Siddharth0711/Foundation-Project-2. Milestones: M1 generator, M2 forecasting backtest, M3 inventory/ABC-FSN,
M4 MIP + heuristic + simulation eval, M5 app/memo/CI.
[PASTE SECTION 9.1–9.4 HERE]
```
