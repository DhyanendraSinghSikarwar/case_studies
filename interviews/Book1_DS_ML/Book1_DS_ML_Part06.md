# Book 1 — Part 06: Time Series & Forecasting

**Topic:** stationarity, ACF/PACF, ARIMA/SARIMA, exponential smoothing, Prophet, GBM with lag features, DL and foundation-model forecasting, backtesting, hierarchical/intermittent demand, forecast metrics
**Target:** 45 | **Actual:** 54 | **Date:** 2026-10-20
**Stars:** ⭐⭐⭐ 16, ⭐⭐ 26, ⭐ 12

---

### Q1 ⭐⭐⭐ 🟢 What is stationarity, why does it matter for time series models, and how do you test and fix non-stationarity (ADF, KPSS)?
**Asked at:** Product cos, GCCs, consulting, fintech (very common opener)
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What are the components of a time series (trend, seasonality, cyclic, noise) and how do additive vs multiplicative decomposition differ?
**Asked at:** Product cos, GCCs, retail analytics
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Why is a random train/test split wrong for time series, and how should you split the data?
**Asked at:** Product cos, e-commerce, quick-commerce, GCCs
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 How would you explain time series forecasting to a non-technical stakeholder?
**Asked at:** Product cos, Europe (reported at Rovio, Disney, Novartis, Marqeta per Prepfully)
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 Which baselines would you build first (naive, seasonal naive, moving average) and why do they matter?
**Asked at:** Retail / supply-chain DS roles, Europe product cos
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 What is differencing, how do you choose d, and what goes wrong with over-differencing?
**Asked at:** GCCs, consulting, product cos
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How do you read ACF and PACF plots to choose p and q for an ARIMA model?
**Asked at:** GCCs, banks/fintech, product cos
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Explain ARIMA(p,d,q). How do you select orders (AIC/BIC, auto_arima) and what are its assumptions and limits?
**Asked at:** GCCs, banks, consulting, product cos
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 What is walk-forward validation / backtesting? Compare expanding vs rolling window and explain how you pick horizon and folds.
**Asked at:** Product cos, Amazon-style forecasting teams, Europe retail
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 How do you build lag and rolling-window features for a GBM (XGBoost/LightGBM) forecaster without leaking future information?
**Asked at:** Flipkart/Swiggy-style demand teams, product cos, Europe retail
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Which forecast metric would you choose (MAE, RMSE, MAPE, sMAPE, MASE, WAPE) and why? Why is MAPE huge for low-volume items?
**Asked at:** Product cos, retail, GCCs
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 ARIMA vs Prophet vs GBM with lag features vs deep learning: how do you choose the model for a given problem?
**Asked at:** Product cos, GCCs, Europe
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you model holidays, promotions and other external regressors (exogenous variables) in a forecast?
**Asked at:** Retail, e-commerce, quick commerce, Europe retail
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do you handle missing timestamps, missing values and outliers in a time series before modelling?
**Asked at:** Product cos, IoT/energy, GCCs
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 How do you forecast multiple steps ahead (recursive, direct, multi-output)? What are the trade-offs?
**Asked at:** Product cos, Amazon-style teams
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Design an end-to-end demand/sales forecasting solution: data, features, model, validation, deployment, monitoring.
**Asked at:** Flipkart, Swiggy, Amazon India, Walmart, Zalando-style roles (design/case round)
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What is the difference between white noise and a random walk, and why does it matter for forecasting?
**Asked at:** GCCs, consulting
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Explain AR, MA and ARMA models. What does each term capture intuitively?
**Asked at:** GCCs, banks, consulting
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 How do you do cross-validation with sklearn TimeSeriesSplit? What does the gap parameter do and when would you add it?
**Asked at:** Product cos, live-coding rounds
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 How does SARIMA handle seasonality, and how do you pick seasonal orders (P,D,Q,m)? What about multiple seasonalities?
**Asked at:** GCCs, consulting, retail
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Explain exponential smoothing (SES, Holt, Holt-Winters/ETS). When is it better than ARIMA?
**Asked at:** Retail, supply chain, GCCs
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How does Prophet work (trend, seasonality, holidays, changepoints), and what are its strengths and weaknesses?
**Asked at:** Product cos, startups, analytics roles
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How do you encode calendar features for ML forecasters (day-of-week, month, Fourier terms, cyclical sin/cos) and which works best?
**Asked at:** Product cos, e-commerce
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 When do you use a log or Box-Cox transform in forecasting, and how do you back-transform correctly?
**Asked at:** GCCs, retail, consulting
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How do you diagnose a fitted forecasting model using residuals (Ljung-Box, residual ACF, normality)?
**Asked at:** GCCs, banks, consulting
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 How do you produce prediction intervals / uncertainty ranges (analytic, bootstrap, quantile regression), and what do you do when intervals miss too many actuals?
**Asked at:** Product cos, supply chain, Europe retail
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Global vs local models: how do you forecast thousands of related series, and when do you pick one global GBM/DL model over per-series models?
**Asked at:** Flipkart, Amazon, Walmart, Zalando, Delivery Hero-style roles
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Why does a demand forecast under-forecast after stockouts, and how do you handle censored (sales != demand) data?
**Asked at:** Retail, quick commerce, e-commerce
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you forecast a new product or new store with no history (cold start)?
**Asked at:** Retail, fashion e-commerce (Zalando-style), quick commerce
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you forecast intermittent / lumpy demand? Explain Croston, SBA, TSB and which metrics to use.
**Asked at:** Supply chain, spare parts, retail
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 When would you use LSTM/GRU/1D-CNN for forecasting instead of GBM, and why do deep models often fail to beat strong baselines?
**Asked at:** Product cos, research-leaning teams
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you monitor a deployed forecast model and decide retraining frequency?
**Asked at:** Product cos, MLE roles
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 One-step-ahead forecasts look good but 12-step-ahead forecasts fail. What are the likely causes?
**Asked at:** Product cos, Amazon-style
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 A useful feature (e.g. weather, ad spend) is not known at forecast time. How do you handle it without leakage?
**Asked at:** Product cos, energy, retail
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How do you handle structural breaks, regime shifts (COVID, pricing change) and concept drift in forecasting?
**Asked at:** Product cos, fintech, retail
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 A deep model beats the baseline in training but not in backtesting. What do you do?
**Asked at:** Product cos, senior rounds
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do you pick a forecast loss when over- and under-forecasting have different costs (bias, tracking signal, quantile/newsvendor)?
**Asked at:** Supply chain, retail, Amazon-style
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How does late-arriving or revised recent data affect forecasting, and how do you evaluate with data vintages?
**Asked at:** Product cos, fintech
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 A promotion changes the demand pattern. How do you separate baseline demand from promo uplift and forecast it?
**Asked at:** Retail, e-commerce, quick commerce
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Why does autocorrelation in residuals break OLS regression assumptions, and what is spurious regression?
**Asked at:** GCCs, economics-flavoured DS roles
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 What is forecast combination/ensembling and why does averaging models often beat the best single model?
**Asked at:** Product cos, supply chain
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🔴 What is hierarchical forecasting? Explain bottom-up, top-down and MinT reconciliation, and what to do when store forecasts do not sum to the region forecast.
**Asked at:** Walmart, Amazon, retail GCCs, Europe retail
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟡 How do you tune hyperparameters of a forecasting model (e.g. LightGBM, Prophet) with time-aware CV without overfitting to the backtest?
**Asked at:** Product cos
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 Implement from scratch in NumPy: moving average, simple exponential smoothing, ACF, and seasonal-naive forecast.
**Asked at:** Live-coding rounds, product cos
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 AI-era: review this LLM-generated forecasting code. Spot leakage (shuffled split, scaler fit on all data, future-rolling features) and other bugs.
**Asked at:** Product cos, 2025-26 code-review rounds
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Which probabilistic forecast metrics do you use (pinball loss, CRPS, coverage, interval width) and how do you evaluate quantile forecasts?
**Asked at:** Amazon-style, Europe retail, senior roles
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 What is conformal prediction for time series, and why do standard conformal guarantees break under autocorrelation?
**Asked at:** Senior / research-leaning roles
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 Compare modern deep forecasters: DeepAR, N-BEATS, Temporal Fusion Transformer, PatchTST. When are they worth it?
**Asked at:** Senior DS/MLE, product cos
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 AI-era: What are time-series foundation models (Chronos, TimesFM, Moirai)? When do you use zero-shot vs fine-tune vs a tuned LightGBM?
**Asked at:** 2025-26 product cos, senior MLE
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 AI-era: Can you prompt an LLM to forecast numbers? What works, what fails, and how would you evaluate it?
**Asked at:** 2025-26 GenAI-flavoured DS loops
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 Explain VAR, Granger causality and cointegration. When is each appropriate?
**Asked at:** Banks, quant-flavoured, consulting
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 What is a state-space model / Kalman filter and how does it relate to exponential smoothing and ARIMA?
**Asked at:** Senior, quant-flavoured, research roles
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 What is GARCH / volatility modelling and when do you model variance instead of the mean?
**Asked at:** Banks, fintech, trading-adjacent
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 How would you use Bayesian structural time series / counterfactual forecasting to estimate the impact of an intervention (CausalImpact)?
**Asked at:** Product cos, experimentation teams
<!-- ANSWER_PENDING -->
