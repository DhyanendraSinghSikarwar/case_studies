# Case Study 4 — NSE Factor Screener & Regime-aware Backtester (Capital Markets)

**Reference repo:** [R5 anmolisb/Stock2026 (Stock-Algo)](https://github.com/anmolisb/Stock2026) — 9-factor scoring of Nifty-500, regime filter (Nifty > 200-DMA, India VIX < 22), post-earnings drift entry, 5-layer exits, paper trading. ISB capstone theme reference: "Prediction of Future Security Prices".

### 4.1 Business problem
A retail-focused wealth/PMS desk wants a transparent, rules + ML swing-trading model on NSE stocks, with honest backtests (no look-ahead, survivorship noted, costs included).

- **KPIs (out-of-sample 2023-01 → latest):** CAGR > Nifty 50 TRI, Sharpe ≥ 1.0, max drawdown ≤ 20%, turnover-adjusted after 0.25% round-trip cost + 0.1% slippage.

### 4.2 Data
- Prices: `yfinance` daily OHLCV, tickers with `.NS` suffix; benchmark `^NSEI`; volatility `^INDIAVIX`. Period 2015-01-01 → today. Cache parquet per ticker.
- Universe: Nifty 500 list CSV `https://archives.nseindia.com/content/indices/ind_nifty500list.csv`. **Fallback** (if blocked): hard-coded Nifty 100 symbols list in `config/universe_fallback.txt`.
- Fundamentals (optional): `yf.Ticker(t).quarterly_financials` for earnings dates/surprise; skip gracefully if missing.

### 4.3 Modules (`PKG=quant`)
```
src/quant/
  data.py        download_prices(universe, start, end) with retry + cache; adjust for splits (auto_adjust=True)
  universe.py    load_universe(); liquidity filter (median 60d traded value > ₹10 Cr)
  factors.py     9 factors, each cross-sectionally z-scored daily:
                 mom_12_1, mom_3m, rel_strength_vs_nifty, dist_from_52w_high, low_vol_60d,
                 volume_surge_20d, rsi_14, trend (close>50DMA>200DMA), earnings_drift (if data)
  regime.py      risk_on = Nifty>200DMA and VIX<22 (thresholds in config); regime-switching via 2-state HMM (hmmlearn) as alternative
  signals.py     composite = weighted z-score (weights: equal | IC-weighted rolling 252d);
                 entry rules: top-N composite, trend ok, risk_on; ML variant: LightGBM ranking 20d fwd return
  portfolio.py   N=15 positions, equal or inverse-vol weights, max 20% per sector, weekly rebalance
  exits.py       5 layers: initial stop 2×ATR, trailing stop, time stop 30d, rank decay (falls out of top 50), regime off
  backtest.py    event-driven daily loop (vectorbt optional); costs & slippage; no look-ahead (signals at t close, trade t+1 open)
  metrics.py     CAGR, vol, Sharpe, Sortino, Calmar, max DD, hit rate, avg win/loss, turnover, IC/IR per factor
  walkforward.py rolling train 3y / test 1y for ML variant; purged + embargoed CV
  paper.py       daily run -> today's watchlist & orders CSV (no broker integration; Kite stub only)
app/streamlit_app.py
```

### 4.4 Method
1. Download & cache; data quality report (missing days, zero volume).
2. Factor research: IC, quintile spread returns, decay; correlation of factors.
3. Rules strategy backtest vs Nifty buy-and-hold.
4. ML ranking variant with walk-forward; compare.
5. Robustness: parameter sweep (N, stop multiple, rebalance freq) heatmap; bootstrap of monthly returns → Sharpe CI; Monte-Carlo trade shuffles.
6. Explicit limitations: survivorship bias (current constituents), no corporate actions beyond yfinance adjustment.

### 4.5 App
Tabs: **Today's screen** (ranked table + factor bars) · **Backtest** (equity curve vs Nifty, drawdown, monthly heatmap) · **Factor lab** (IC charts) · **Regime** (Nifty, VIX, risk-on shading) · **Stock drill-down** (chart with entries/exits).

### 4.6 Acceptance criteria
- [ ] `test_no_lookahead`: shifting future prices does not change past signals.
- [ ] Costs applied on every trade; turnover reported.
- [ ] Out-of-sample metrics table for rules & ML vs benchmark in README.
- [ ] Disclaimer: research only, not investment advice.

### 4.7 Claude Code kickoff prompt
```text
Read CLAUDE.md. Build Case Study 4 "NSE Factor Screener & Regime-aware Backtester" per spec. PKG=quant.
Reference design: github.com/anmolisb/Stock2026. yfinance data with caching and fallback universe.
Milestones: M1 data+universe, M2 factors+IC research, M3 rules backtest+exits+regime, M4 ML walk-forward+robustness,
M5 app, memo, CI. Enforce no look-ahead with a unit test.
[PASTE SECTION 4.1–4.6 HERE]
```
