# Book 1 — Part 06: Time Series & Forecasting

**Topic:** stationarity, ACF/PACF, ARIMA/SARIMA, exponential smoothing, Prophet, GBM with lag features, DL and foundation-model forecasting, backtesting, hierarchical/intermittent demand, forecast metrics
**Target:** 45 | **Actual:** 54 | **Date:** 2026-10-20
**Stars:** ⭐⭐⭐ 16, ⭐⭐ 26, ⭐ 12

---

### Q1 ⭐⭐⭐ 🟢 What is stationarity, why does it matter for time series models, and how do you test and fix non-stationarity (ADF, KPSS)?
**Asked at:** Product cos, GCCs, consulting, fintech (very common opener)
**Say this first (1 line):** A series is stationary when its mean, variance and autocorrelation do not change over time; most classical models (ARIMA, regression on lags) assume it, so I test it with ADF and KPSS and fix it by differencing or transforming.

**Then explain:**
- **Why it matters:** if the statistical behaviour keeps shifting, patterns learned in the past do not hold in the future, and relationships can be spurious (two trending series look "correlated").
- **ADF test:** null = unit root (non-stationary). Small p-value (< 0.05) means reject, so the series looks stationary.
- **KPSS test:** null = stationary. Small p-value means non-stationary. The two have opposite nulls, so I run both: both agree -> confident; they disagree -> trend-stationary or not enough data, so I look at the plot too.
- **Fixes:** first difference (removes stochastic trend), seasonal difference (removes seasonality), log (stabilises growing variance), detrend (for deterministic trend).
- Tree/GBM models do not strictly need stationarity, but they cannot extrapolate a trend, so I still difference or model the ratio to a baseline.

**Example:** Daily sales with a rising trend: ADF p = 0.84 (cannot reject unit root), KPSS p = 0.01 (reject stationarity) -> non-stationary. After one difference ADF p = 0.000, KPSS p = 0.10 -> stationary, so d = 1.

**Code:**
```python
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss
rng = np.random.default_rng(0)
rw = np.cumsum(rng.normal(size=300))            # random walk = non-stationary
for name, x in [("level", rw), ("diff", np.diff(rw))]:
    print(name, "ADF p=%.3f" % adfuller(x)[1], "KPSS p=%.3f" % kpss(x, regression="c", nlags="auto")[1])
# level: ADF p=0.841 KPSS p=0.010 | diff: ADF p=0.000 KPSS p=0.100
```

**Follow-ups:**
- *Trend-stationary vs difference-stationary?* Trend-stationary = stationary around a deterministic line (detrend). Difference-stationary = has a unit root (difference). ADF with `regression="ct"` helps tell them apart.
- *Is stationary the same as no seasonality?* No. Seasonality also breaks stationarity, since the mean depends on the calendar.

**Common mistakes:** Reading a high ADF p-value as "stationary"; running only one test; differencing a series that is already stationary (Q6); forgetting to invert differencing when reporting forecasts.

### Q2 ⭐⭐⭐ 🟢 What are the components of a time series (trend, seasonality, cyclic, noise) and how do additive vs multiplicative decomposition differ?
**Asked at:** Product cos, GCCs, retail analytics
**Say this first (1 line):** A series is trend + seasonality + cycle + noise; I use additive decomposition when the seasonal swing is constant in size and multiplicative when it grows with the level.

**Then explain:**
- **Trend:** long-run direction (growth, decline).
- **Seasonality:** fixed-period repeating pattern (weekly, yearly). Period is known from the calendar.
- **Cyclic:** rises and falls with no fixed period (business cycles, multi-year). Hard to forecast and often folded into the trend.
- **Noise (residual):** what is left; ideally unpredictable.
- **Additive:** y = T + S + R. Seasonal swing is, say, +/-10 units regardless of level.
- **Multiplicative:** y = T x S x R. Swing is, say, +/-20% of level, so it widens as the series grows. A log turns multiplicative into additive.
- How I decide: plot it. Funnel-shaped seasonal swings mean multiplicative. A quick check is whether the residuals look homoscedastic after decomposing.

**Example:** Retail sales that grow from 100k to 500k a month with a Diwali spike that is always +30% -> multiplicative. A thermostat reading with a +/-2 degree daily wave on a flat mean -> additive.

**Code:**
```python
import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
rng = np.random.default_rng(0); t = np.arange(120); idx = pd.date_range("2015-01", periods=120, freq="MS")
mult = pd.Series((50 + 0.5*t) * (1 + 0.2*np.sin(2*np.pi*t/12)) * np.exp(rng.normal(0, 0.01, 120)), index=idx)
add = pd.Series(50 + 0.5*t + 10*np.sin(2*np.pi*t/12) + rng.normal(0, 1.5, 120), index=idx)
d = seasonal_decompose(mult, model="multiplicative", period=12)     # d.trend, d.seasonal, d.resid
print(d.seasonal.min().round(2), d.seasonal.max().round(2), d.resid.std().round(3))   # 0.8 1.2 0.008
a = seasonal_decompose(add, model="additive", period=12)
print(a.seasonal.min().round(1), a.seasonal.max().round(1))                           # -9.8 10.1
```

**Follow-ups:**
- *Why STL over classical decomposition?* STL is robust to outliers, allows seasonality to evolve, and handles any period.
- *Multiplicative with zeros?* Cannot be used (zeros/negatives); use additive or log1p.

**Common mistakes:** Calling a cycle "seasonality"; using multiplicative on data with zeros; treating decomposition as a forecast (it is a description).

### Q3 ⭐⭐⭐ 🟢 Why is a random train/test split wrong for time series, and how should you split the data?
**Asked at:** Product cos, e-commerce, quick-commerce, GCCs
**Say this first (1 line):** Random splits let the model train on the future and test on the past, which leaks information and overstates accuracy; I split by time so train always comes before test.

**Then explain:**
- **Leakage:** neighbouring days are correlated, so a random test point has its yesterday and tomorrow in training. The model effectively interpolates.
- **Wrong target:** in production you always predict forward, so evaluation must mimic that.
- **Correct split:** train on the past, validate on the next block, test on the latest block (e.g. train to Dec, validate Jan-Mar, test Apr-Jun).
- **Better:** walk-forward / rolling-origin validation with several folds (Q9), so one lucky or unlucky period does not decide.
- **Gap:** if features use lags or rolling windows, or the label is a future window, add a gap so train labels do not overlap with test inputs.
- Preprocessing (scaling, imputation, target encoding) must be fit on the train part only.

**Example (illustrative numbers):** Sales has a growing trend. A random 80/20 split shows MAPE 5%; the honest "train to Sep, test Oct-Dec" shows 14% because the trend and the holiday peak were never seen.

**Follow-ups:**
- *Multiple series (panel)?* Split by time cut-off across all series. Splitting by series answers a different question (cold start, Q29).
- *Is shuffling ever fine?* Only for models on lag features built per row if you still respect the cut-off, but a time cut-off is simpler and safer.

**Common mistakes:** `train_test_split` with defaults; scaling on the full data; tuning on the test block repeatedly; ignoring gap when the target is a 7-day sum.

### Q4 ⭐⭐⭐ 🟢 How would you explain time series forecasting to a non-technical stakeholder?
**Asked at:** Product cos, Europe (reported at Rovio, Disney, Novartis, Marqeta per Prepfully)
**Say this first (1 line):** Forecasting is using what happened in the past, plus what we already know about the future (holidays, promotions), to give a best estimate and a likely range for the next few weeks, so the business can plan stock, staff or cash.

**Then explain:**
- Use a familiar analogy: a weather forecast. We say "70% chance of rain", not "it will rain". Our forecast is a number plus a range.
- **What it sees:** the level of sales, the trend, repeating patterns (weekends, festivals), and special events.
- **What it cannot see:** one-off shocks (a competitor's launch, a strike). So we track the error and refresh the forecast regularly.
- **How we judge it:** simple, business terms: "on average we are off by 8% per week", compared against a simple rule like "same as last week/year".
- **How it is used:** the number is an input to a decision (how many units to order), so under/over-forecast costs matter more than the model.

**Example:** "Next month we expect about 12,000 orders, likely between 10,500 and 13,500. Last quarter our forecast was within 8% on average, against 15% if we had just copied last year's numbers."

**Follow-ups:**
- *Why not just use last year's numbers?* That is our baseline; the model must beat it by a clear margin to be worth its cost.
- *What if the forecast is wrong?* We show the range, monitor the error, and review the biggest misses with the business.

**Common mistakes:** Talking about ARIMA/LSTM; giving a single number with no range; promising accuracy without a benchmark; not linking to the decision it supports.

### Q5 ⭐⭐⭐ 🟢 Which baselines would you build first (naive, seasonal naive, moving average) and why do they matter?
**Asked at:** Retail / supply-chain DS roles, Europe product cos
**Say this first (1 line):** I always start with naive, seasonal naive and a moving average, because they are cheap, hard to beat, and any fancy model must prove it is better than them.

**Then explain:**
- **Naive:** tomorrow = today. Hard to beat for random-walk-like series (stocks).
- **Seasonal naive:** value = same period last cycle (same weekday last week, same month last year). The strongest simple baseline for seasonal data.
- **Moving average / mean:** average of the last k points. Good for stable, noisy series.
- **Why they matter:** (1) a sanity floor, (2) the denominator of MASE (Q11), (3) tell me how much is predictable at all, (4) often serve as a production fallback.
- If a complex model only gives 1-2% over seasonal naive, it is probably not worth deploying.

**Example (the synthetic monthly series in the code below, 12-month test):** naive MAE 7.55, 12-month average 6.78, seasonal naive 6.66, Holt-Winters 1.36. The seasonal baselines are close to each other because the trend adds about 6 units a year, and the model clearly earns its place here.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0); t = np.arange(120)       # 10 years of monthly data: trend + seasonality + noise
y = pd.Series(50 + 0.5*t + 10*np.sin(2*np.pi*t/12) + rng.normal(0, 1.5, 120),
              index=pd.date_range("2015-01", periods=120, freq="MS"))
train, test = y[:-12], y[-12:]                            # reused as `train`, `test` in Q8, Q9, Q20, Q21, Q25
naive   = np.repeat(train.iloc[-1], 12)
snaive  = train.iloc[-12:].values                 # same month last year
ma      = np.repeat(train.iloc[-12:].mean(), 12)
mae = lambda a, b: np.mean(np.abs(np.asarray(a) - np.asarray(b)))
print(mae(test, naive), mae(test, snaive), mae(test, ma))   # 7.55 6.66 6.78
```

**Follow-ups:**
- *Which is best for weekly retail data?* Seasonal naive with m = 7 (or 52 for yearly weekly data).
- *Drift method?* Naive plus average historical change; good for trending series.

**Common mistakes:** Comparing a model against nothing; using plain naive on strongly seasonal data; computing the baseline on a different window than the model.

### Q6 ⭐⭐⭐ 🟡 What is differencing, how do you choose d, and what goes wrong with over-differencing?
**Asked at:** GCCs, consulting, product cos
**Say this first (1 line):** Differencing replaces each value with its change from the previous one (y_t - y_{t-1}) to remove trend; I pick the smallest d that makes the series stationary, and over-differencing adds noise and negative autocorrelation.

**Then explain:**
- **d = 1** removes a linear / stochastic trend; **d = 2** removes a trend in the trend (rare). **Seasonal difference** y_t - y_{t-m} removes seasonality.
- **How to choose:** plot; ADF/KPSS after each difference (`ndiffs` in pmdarima does this); look for a slowly decaying ACF (needs more differencing).
- **Rule of thumb:** the correct d gives the lowest variance of the differenced series.
- **Over-differencing signs:** variance goes up, lag-1 ACF is strongly negative (about -0.5), and the model needs MA terms that sit near -1 (non-invertible).
- Forecasts on differenced data must be integrated back (cumsum plus last observed value) to get the original scale.

**Example:** Random walk of 500 points: variance of the level is 73.6; after one difference it is 1.03 (right); after two it is 2.11 and lag-1 ACF is -0.51 (over-differenced; noise variance has doubled).

**Code:**
```python
import numpy as np
from statsmodels.tsa.stattools import acf
rw = np.cumsum(np.random.default_rng(0).normal(size=500))
for d in range(3):
    x = np.diff(rw, d) if d else rw
    print(d, round(x.var(), 2), round(acf(x, nlags=1)[1], 2))
```

**Follow-ups:**
- *Why does over-differencing give ACF -0.5?* Differencing white noise creates e_t - e_{t-1}, an MA(1) with theta = -1 and lag-1 autocorrelation -0.5.
- *Fractional differencing?* Keeps some memory while achieving stationarity; used in finance.

**Common mistakes:** Differencing "to be safe"; using d from one test only; differencing a series with a deterministic trend instead of detrending; not undoing differences before reporting.

### Q7 ⭐⭐⭐ 🟡 How do you read ACF and PACF plots to choose p and q for an ARIMA model?
**Asked at:** GCCs, banks/fintech, product cos
**Say this first (1 line):** On the stationary series, a PACF that cuts off after lag p suggests AR(p), an ACF that cuts off after lag q suggests MA(q), and if both tail off slowly it is a mix (ARMA).

**Then explain:**
- **ACF:** correlation of the series with its lag-k self, including indirect effects through the lags in between.
- **PACF:** correlation at lag k after removing the effect of lags 1..k-1 (direct effect only).
- **Patterns:**

| Series | ACF | PACF |
|---|---|---|
| AR(p) | decays gradually | cuts off after p |
| MA(q) | cuts off after q | decays gradually |
| ARMA | decays | decays |

- **Significance:** bars outside the ~ +/-1.96/sqrt(n) band; 1 in 20 can be outside by chance.
- Use it as a starting point, then compare AIC/BIC and check residuals (Q8, Q25). Real data is rarely clean.

**Example (simulated, n = 2000):** AR(1) with phi = 0.7: ACF 0.70, 0.49, 0.35, 0.24 (decaying), PACF 0.70, 0.01, 0.01, -0.02 (cut-off at 1). MA(1) with theta = 0.7 (second print in the code): ACF cuts off after lag 1, PACF decays.

**Code:**
```python
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.stattools import acf, pacf
import numpy as np
rng = np.random.default_rng(0)
ar = ArmaProcess([1, -0.7], [1]).generate_sample(2000, distrvs=rng.normal)
print(acf(ar, nlags=4)[1:].round(2), pacf(ar, nlags=4)[1:].round(2))   # [0.7 0.49 0.35 0.24] [0.7 0.01 0.01 -0.02]
ma = ArmaProcess([1], [1, 0.7]).generate_sample(2000, distrvs=rng.normal)       # MA(1), theta = 0.7
print(acf(ma, nlags=4)[1:].round(2), pacf(ma, nlags=4)[1:].round(2))   # ACF cuts off after lag 1; PACF decays
```

**Follow-ups:**
- *Seasonal spikes at 12, 24?* Seasonal AR/MA terms (P, Q) in SARIMA (Q20).
- *ACF decays very slowly?* Non-stationary; difference first.

**Common mistakes:** Reading ACF/PACF on a non-stationary series; swapping which one cuts off for AR vs MA; over-trusting borderline spikes; ignoring that `statsmodels` PACF defaults can differ (use `method="ywm"`/`"ols"` consciously).

### Q8 ⭐⭐⭐ 🟡 Explain ARIMA(p,d,q). How do you select orders (AIC/BIC, auto_arima) and what are its assumptions and limits?
**Asked at:** GCCs, banks, consulting, product cos
**Say this first (1 line):** ARIMA(p,d,q) forecasts a series from its own past values (p AR terms), past forecast errors (q MA terms), after differencing d times to make it stationary; I choose orders by lowest AIC/BIC over a small grid, then check residuals.

**Then explain:**
- **AR(p):** y_t depends on the last p values. **MA(q):** y_t depends on the last q shocks. **I(d):** difference d times.
- **Selection:** d from unit-root tests, p/q from ACF/PACF as a start, then a grid search by AIC (better for forecasting) or BIC (penalises complexity more, prefers parsimonious). `auto_arima` automates this (stepwise search).
- **Do not** compare AIC across different d (different data).
- **Assumptions:** linear structure, stationarity after differencing, constant variance, residuals are white noise.
- **Limits:** univariate by default, one series at a time (slow for thousands), weak on long/multiple seasonality, no easy handling of promotions (ARIMAX helps), poor at non-linear effects, intervals assume normal errors.

**Example (the monthly synthetic series from Q5, trend + seasonality):** plain ARIMA(1,1,0) AIC 572.0, ARIMA(2,1,2) AIC 475.5 (it fakes the seasonal wave with complex roots), SARIMA(0,1,1)(0,1,1,12) AIC 371.9 and MAE 1.46 on the 12-month test: seasonal structure beats extra p/q.

**Code:**
```python
# continuation of Q5: uses `train` (108 monthly points) built there
from statsmodels.tsa.arima.model import ARIMA
for order in [(1,1,0), (0,1,1), (1,1,1), (2,1,2)]:
    m = ARIMA(train, order=order).fit()
    print(order, round(m.aic, 1), round(m.bic, 1))
fc = ARIMA(train, order=(1,1,1)).fit().get_forecast(12)
print(fc.summary_frame(alpha=0.2).head())    # forecast + 80% interval
# AICs: 572.0, 588.0, 573.5, 475.5 (the (2,1,2) fit is the one that fakes seasonality)
```

**Follow-ups:**
- *AIC vs time-series CV?* AIC is in-sample; for forecasting I prefer out-of-sample backtests when time allows.
- *ARIMA vs GBM?* ARIMA for a few clean series with little data; GBM/global model when many series and rich features (Q12).

**Common mistakes:** Letting auto_arima run blindly on seasonal data without `seasonal=True, m=`; skipping residual checks; comparing AIC across different d; assuming ARIMA handles holidays.

### Q9 ⭐⭐⭐ 🟡 What is walk-forward validation / backtesting? Compare expanding vs rolling window and explain how you pick horizon and folds.
**Asked at:** Product cos, Amazon-style forecasting teams, Europe retail
**Say this first (1 line):** Walk-forward validation repeatedly trains on the past and tests on the next block, then rolls forward, so I get many realistic out-of-sample errors instead of one.

**Then explain:**
- **Expanding window:** train start is fixed, train grows each fold. Uses all history; best when old data is still relevant and the series is stable.
- **Rolling (sliding) window:** fixed-length train that moves. Better when the process drifts (old data hurts) and keeps training cost constant.
- **Horizon:** equal to the real business horizon (e.g. 14 days for replenishment). If several horizons matter, report error per horizon.
- **Folds:** enough to cover seasonality and a couple of regimes (at least one full year if yearly seasonality matters; typically 5-20 origins). Step size = how often you retrain in production.
- Keep a final untouched holdout after tuning, and apply a gap if features/labels overlap (Q19).
- Report mean plus spread across folds; a model that wins on average but is wild in one fold is risky.

**Example:** Monthly data, first train 60 months, horizon 3, step 3 gave 20 folds. Seasonal naive MAE 6.01; Holt-Winters 1.30 expanding vs 1.36 rolling-48. Stable series, so expanding is slightly better.

**Code:**
```python
# continuation of Q5: `y` is the 120-point monthly pd.Series built there
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
def walk_forward(y, fit_forecast, horizon=3, first_train=60, step=3, window=None):
    errs = []
    for end in range(first_train, len(y) - horizon + 1, step):
        start = 0 if window is None else end - window      # expanding vs rolling
        train, test = y.iloc[start:end], y.iloc[end:end+horizon]
        errs.append(np.mean(np.abs(test.values - fit_forecast(train, horizon))))
    return np.mean(errs), len(errs)
hw = lambda tr, h: ExponentialSmoothing(tr, trend="add", seasonal="add", seasonal_periods=12).fit().forecast(h).values
sn = lambda tr, h: tr.values[-12:][:h]
print(walk_forward(y, sn), walk_forward(y, hw), walk_forward(y, hw, window=48))   # 6.01, 1.30, 1.36 (20 folds each)
```

**Follow-ups:**
- *Cost?* k refits; parallelise or refit every few origins.
- *Backtest vs live?* Always some optimism: revised data, tuning on the same folds (Q43).

**Common mistakes:** One split only; horizon in backtest differing from production; fitting scalers/encoders on all data; using future-known features that are not really known at the origin.

### Q10 ⭐⭐⭐ 🟡 How do you build lag and rolling-window features for a GBM (XGBoost/LightGBM) forecaster without leaking future information?
**Asked at:** Flipkart/Swiggy-style demand teams, product cos, Europe retail
**Say this first (1 line):** Every feature for a row at time t must be computable using data up to t-1 (or up to the forecast origin), so I build lags with shift(), shift before rolling, and only use future-known covariates (calendar, planned promo).

**Then explain:**
- **Lags:** `y.shift(k)`; k must be >= the forecast horizon in a direct model, otherwise you need recursive prediction.
- **Rolling stats:** `y.shift(1).rolling(7).mean()`. Forgetting the shift lets the current target into its own feature.
- **Group-wise:** compute per series (`groupby(id)`), never across series boundaries.
- **Calendar and planned events:** safe because known ahead. Weather, ad spend actuals are not (Q34).
- **Split by time**, fit encoders only on train, and check feature importance: a lag-0-like feature dominating is a leakage red flag.
- Sanity test: recompute features at an old origin using only data before it and compare.

**Example (code below):** 20 synthetic daily series, global LightGBM with lag1/7/14 and shifted roll7: WAPE 0.072 on the last 45 days, against seasonal naive 0.088. Averaging several recent days (roll7) removes noise that seasonal naive copies from one day. Always show the baseline next to the model.

**Code:**
```python
import numpy as np, pandas as pd, lightgbm as lgb
rng = np.random.default_rng(0); dates = pd.date_range("2023-01-01", periods=400); rows = []
for s in range(20):                                   # 20 synthetic daily series: level x weekday pattern x trend x 8% noise
    wk = rng.uniform(.1, .4); dow = np.array([1, 1, 1, 1, 1.1, 1 + wk, 1 - wk])
    y = rng.uniform(20, 100) * dow[dates.dayofweek] * (1 + 0.0005*np.arange(400)) * np.exp(rng.normal(0, .08, 400))
    rows.append(pd.DataFrame({"series": s, "date": dates, "y": y}))
df = pd.concat(rows, ignore_index=True)
g = df.groupby("series")["y"]
for l in (1, 7, 14):
    df[f"lag{l}"] = g.shift(l)
df["roll7"] = g.transform(lambda x: x.shift(1).rolling(7).mean())   # shift BEFORE rolling
df["dow"] = df.date.dt.dayofweek
# LEAKY: x.rolling(7).mean() without shift includes today's y
df = df.dropna(); cut = df.date.max() - pd.Timedelta(days=45)       # time split: last 45 days are the test block
train, test = df[df.date <= cut].copy(), df[df.date > cut].copy()
feats = ["series", "lag1", "lag7", "lag14", "roll7", "dow"]
train["series"] = train["series"].astype("category")
test["series"] = pd.Categorical(test["series"], categories=train["series"].cat.categories)
m = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, verbose=-1, random_state=0).fit(train[feats], train.y)
print(abs(test.y - m.predict(test[feats])).sum() / test.y.sum(),     # LightGBM WAPE  0.072
      abs(test.y - test.lag7).sum() / test.y.sum())                  # seasonal naive 0.088
```

**Follow-ups:**
- *Rolling window ending at today when predicting 7 days out?* At origin t, only rows up to t exist; for horizon 7 the lag must be >= 7 in a direct model.
- *Expanding mean encodings?* Same rule: shift and compute only from the past.

**Common mistakes:** Rolling without shift; global scaling before split; random CV; using centered rolling windows; computing lags across series after a sort mistake.

### Q11 ⭐⭐⭐ 🟡 Which forecast metric would you choose (MAE, RMSE, MAPE, sMAPE, MASE, WAPE) and why? Why is MAPE huge for low-volume items?
**Asked at:** Product cos, retail, GCCs
**Say this first (1 line):** I pick the metric from the business cost: WAPE or MAE for aggregate accuracy, RMSE if big misses are very costly, MASE to compare across series, and I avoid MAPE for low-volume or zero data.

**Then explain:**

| Metric | Good for | Weakness |
|---|---|---|
| MAE | simple, same units | scale-dependent |
| RMSE | penalises large errors | outlier-sensitive; favours the mean |
| MAPE | % intuition | undefined at 0, explodes at small actuals, penalises over-forecast more |
| sMAPE | bounded-ish | still unstable near 0, odd asymmetry |
| WAPE = sum|e| / sum y | volume-weighted, robust for retail | hides small items |
| MASE = MAE / MAE of (seasonal) naive in-sample | cross-series, tells if you beat naive (<1 is good) | needs a sensible naive scale |

- **MAPE huge at low volume:** error divided by a tiny actual. Actual 1, forecast 3 gives 200% even though the miss is 2 units.
- Match the metric to the decision: a target that is a median needs MAE; mean needs RMSE; bias also tracked separately.

**Example:** Actuals [200,150,300,1], forecasts [210,140,310,3]: MAPE 53.8% (dominated by the 1-unit item), WAPE 4.9%. MASE needs the training history: if the in-sample naive MAE is 1.57 and the model's MAE is 1.0, MASE = 0.64 (better than naive).

**Code:**
```python
import numpy as np
wape = lambda y, f: np.abs(y - f).sum() / np.abs(y).sum()
mase = lambda y, f, tr, m=1: np.abs(y - f).mean() / np.abs(tr[m:] - tr[:-m]).mean()
y, f = np.array([200, 150, 300, 1.]), np.array([210, 140, 310, 3.])
print(np.mean(np.abs(y - f) / y), wape(y, f))      # MAPE 0.5375, WAPE 0.049
```

**Follow-ups:**
- *Which for intermittent demand?* MASE/RMSSE, or MAE with bias, not MAPE (Q30).
- *Aggregation across SKUs?* Weighted by volume (WAPE) or by revenue/margin.

**Common mistakes:** Averaging MAPE across SKUs; ignoring bias; optimising RMSE but reporting MAPE; MASE scale computed on test data.

### Q12 ⭐⭐⭐ 🟡 ARIMA vs Prophet vs GBM with lag features vs deep learning: how do you choose the model for a given problem?
**Asked at:** Product cos, GCCs, Europe
**Say this first (1 line):** I start with simple baselines, then choose by data shape: classical (ETS/ARIMA) for few clean series, Prophet for quick business-seasonality with holidays, global GBM for many series with rich features, deep learning only when there is lots of data and a clear gain.

**Then explain:**

| Model | Best when | Watch out |
|---|---|---|
| ETS/ARIMA | few series, short history, interpretability | one model per series, no rich features |
| Prophet | daily data, multiple seasonalities, holidays, analyst-friendly | often loses to tuned alternatives, weak at short-term dynamics |
| GBM + lag features | thousands of series, promos, price, hierarchy, cross-series learning | cannot extrapolate trend, needs careful features and a baseline |
| Deep (DeepAR, N-BEATS, TFT, PatchTST) | huge panels, long histories, many covariates, probabilistic output | needs tuning, compute, often ties GBM |

- Decision drivers: number of series, history length, covariates, horizon, need for intervals, latency, team skills, explainability.
- Evidence beats opinion: run the same walk-forward backtest for each candidate against seasonal naive, and consider an ensemble (Q41).
- Practical result (M5 competition): LightGBM-based global models dominated the top ranks.

**Example:** 50k SKU-store series with price and promo -> global LightGBM; 5 national KPIs with 10 years of monthly data -> ETS/ARIMA ensemble; need quick forecast with Indian holidays for a product team -> Prophet as a first version.

**Follow-ups:**
- *Why not LSTM by default?* Needs more data and tuning and usually does not beat GBM on tabular retail panels (Q31).
- *Foundation models?* Good zero-shot baseline (Q49).

**Common mistakes:** Picking by hype; no baseline; comparing on one fold; ignoring serving cost and maintenance.

### Q13 ⭐⭐⭐ 🟡 How do you model holidays, promotions and other external regressors (exogenous variables) in a forecast?
**Asked at:** Retail, e-commerce, quick commerce, Europe retail
**Say this first (1 line):** I encode holidays and promos as features known in advance (flags, days-to/since, intensity), and use a model that can take regressors: GBM features, ARIMAX/SARIMAX, or Prophet holiday regressors.

**Then explain:**
- **Holidays:** binary flag, plus a window (days before/after, since shopping ramps up before a festival). Moving holidays (Diwali, Eid) need a real calendar each year.
- **Promotions:** discount depth, type, duration, channel, days since promo start, and a cannibalisation or halo flag for related items.
- **Other regressors:** price, competitor price, weather forecast, stock-out flag.
- **Key rule:** future values must be available at forecast time (planned promos yes, realised weather no, use forecast weather, Q34).
- **Models:** tree models take these as columns; SARIMAX and Prophet take external regressors; for sparse events, a baseline x uplift split works (Q39).
- Validate: check error specifically on holiday/promo weeks, not only overall.

**Example:** Days-to-holiday feature for 13 dates (20 Oct to 1 Nov 2024): 11 on 20 Oct (far), 1 on 30 Oct (day before; flagged `pre_holiday_week`), 0 on the holiday itself.

**Code:**
```python
import numpy as np, pandas as pd
hol = pd.to_datetime(["2024-10-31", "2024-11-01"])
d = pd.DataFrame({"date": pd.date_range("2024-10-20", "2024-11-01")})
d["is_holiday"] = d.date.isin(hol).astype(int)
nxt = np.searchsorted(hol.values, d.date.values)                 # next holiday on/after date
nxt_d = np.where(nxt < len(hol), hol.values[np.minimum(nxt, len(hol)-1)], np.datetime64("NaT"))
d["days_to_holiday"] = (pd.to_datetime(nxt_d) - d.date).dt.days.clip(upper=14)
d["pre_holiday_week"] = d.days_to_holiday.between(1, 7).astype(int)
```

**Follow-ups:**
- *Few holiday examples?* Share effects across similar holidays or use a hierarchical/regularised prior (Prophet).
- *Regressor not known in future?* Forecast it first or use lagged values (Q34).

**Common mistakes:** Using realised promo data not planned at origin; only a binary flag with no lead/lag window; ignoring holiday date shifts; leaking promo effect through the target.

### Q14 ⭐⭐⭐ 🟡 How do you handle missing timestamps, missing values and outliers in a time series before modelling?
**Asked at:** Product cos, IoT/energy, GCCs
**Say this first (1 line):** I first reindex to a complete regular time grid to expose missing timestamps, then decide per cause: fill, interpolate, flag or leave as missing; and treat outliers by flagging and capping rather than deleting blindly.

**Then explain:**
- **Missing timestamps:** `asfreq` / reindex to the expected frequency; understand why (system outage, no sales = true zero, store closed).
- **Missing values:** true zeros -> fill with 0; sensor gaps -> interpolate (short) or seasonal fill; long gaps -> mask and let the model handle or drop that period. Always add a "was missing" flag if it is informative.
- **Do not** backfill with future data (leakage); use forward fill/interpolation only from the past in the training pipeline for features.
- **Outliers:** detect with rolling median + MAD or STL residuals; distinguish errors (cap/replace) from real events (promo, festival: keep and explain with a feature).
- Duplicates and time-zone/DST issues are common sources of bugs.

**Example:** Daily values 1, 2, (day missing), 4, 5, 100, 6: reindex exposes the gap, rolling-median/MAD flags the 100, and masking plus linear interpolation yields [1, 2, 3, 4, 5, 5.5, 6].

**Code:**
```python
import numpy as np, pandas as pd
s = pd.Series([1, 2, 4, 5, 100, 6.], index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-04",
                                                           "2024-01-05", "2024-01-06", "2024-01-07"]))
s = s.asfreq("D")                                           # exposes missing dates as NaN
med = s.rolling(5, center=True, min_periods=1).median()
mad = (s - med).abs().rolling(5, center=True, min_periods=1).median()
out = (s - med).abs() > 5 * mad.clip(lower=0.5)
clean = s.mask(out).interpolate()                           # centred window: fine for history cleaning, not for live features
print(clean.values)                                         # [1. 2. 3. 4. 5. 5.5 6.]
```

**Follow-ups:**
- *Interpolate in the test period?* Only using past data; otherwise leakage.
- *Intermittent demand zeros?* They are real; do not interpolate (Q30).

**Common mistakes:** Treating missing sales as missing instead of zero (or vice versa); removing real spikes; centred rolling windows in live features; imputing before the train/test split with future info.

### Q15 ⭐⭐⭐ 🟡 How do you forecast multiple steps ahead (recursive, direct, multi-output)? What are the trade-offs?
**Asked at:** Product cos, Amazon-style teams
**Say this first (1 line):** Recursive uses one one-step model fed with its own predictions; direct trains one model per horizon; multi-output trains one model with several outputs. Recursive is simple but accumulates error, direct avoids that but costs more models.

**Then explain:**

| Strategy | How | Pros | Cons |
|---|---|---|---|
| Recursive | predict t+1, feed back, repeat | one model, any horizon | errors compound, needs future covariates at every step |
| Direct | separate model per h | no error accumulation | H models, ignores dependence between horizons, inconsistent paths |
| Multi-output / seq2seq | one model outputs the whole vector | shares information, coherent | needs NN or special wrappers |
| DirRec / hybrid | direct with recursive inputs | balance | complexity |

- Recursive suits ARIMA/ETS (naturally) and short horizons; direct is common with GBM at weekly/daily retail horizons.
- With direct, features must be lagged relative to the origin and at least horizon-old for known inputs.

**Example (simulated daily series, weekly seasonality, noise sd 2):** horizon 7, LightGBM with lags 1,2,3,7, 34 rolling origins: recursive MAE 2.00, direct MAE 2.11. Essentially tied here; direct is not automatically better, so I backtest both.

**Code:**
```python
import numpy as np, lightgbm as lgb
rng = np.random.default_rng(0); t = np.arange(400)
y = 50 + 0.02*t + 8*np.sin(2*np.pi*t/7) + rng.normal(0, 2, 400)
L, H, split = (1, 2, 3, 7), 7, 360                      # train on y[:split], test on the rest
mk = lambda: lgb.LGBMRegressor(n_estimators=200, learning_rate=.05, verbose=-1, random_state=0)
# recursive: one one-step model, predictions fed back
one = mk().fit([[y[i-l] for l in L] for i in range(7, split)], y[7:split])
# direct: model h predicts y[o+h+1] from features at origin o (o = last observed index)
feat = lambda o: [y[o-l+1] for l in L]
direct = [mk().fit([feat(o) for o in range(7, split-h-1)], [y[o+h+1] for o in range(7, split-h-1)]) for h in range(H)]
er, ed = [], []
for o in range(split-1, 400-H):
    hist, pr = list(y[:o+1]), []
    for h in range(H):
        hist.append(one.predict([[hist[-l] for l in L]])[0]); pr.append(hist[-1])
    er.append(np.abs(y[o+1:o+1+H] - pr).mean())
    ed.append(np.abs(y[o+1:o+1+H] - [direct[h].predict([feat(o)])[0] for h in range(H)]).mean())
print(np.mean(er), np.mean(ed))                        # about 2.00 recursive, 2.11 direct
```

**Follow-ups:**
- *Bias vs variance?* Direct has lower bias; recursive has lower variance but compounding bias.
- *Quantile forecasts?* Direct is easier; recursive needs simulation.

**Common mistakes:** Using lag-1 features in a direct 7-day model at inference without them being available; not saying how covariates are filled in recursion; evaluating only horizon 1.

### Q16 ⭐⭐⭐ 🟡 Design an end-to-end demand/sales forecasting solution: data, features, model, validation, deployment, monitoring.
**Asked at:** Flipkart, Swiggy, Amazon India, Walmart, Zalando-style roles (design/case round)
**Say this first (1 line):** I would start from the decision the forecast drives (inventory/replenishment), build a strong baseline, then a global GBM with calendar, price and promo features, validate with walk-forward, deploy as a scheduled batch with monitoring and a fallback.

**Then explain (framework):**
- **Requirements:** what is forecast (SKU x store x day), horizon (lead time + review period), granularity, frequency, KPI (WAPE, bias, stockout/waste cost), latency (batch daily is typical), service-level target.
- **Data:** sales (not demand: handle stockouts, Q28), prices, promos, calendar/holidays, weather, inventory, catalogue attributes, new-item flags; fix missing dates and outliers.
- **Features:** lags (>= horizon), shifted rolling means, calendar/Fourier, price/promo lead and lag, hierarchy ids, product/store attributes, days since launch.
- **Model:** baselines (seasonal naive, ETS), global LightGBM with direct per-horizon or recursive approach, quantile objectives for safety stock, special models for intermittent items (Q30) and cold start (Q29), reconciliation to hierarchy (Q42).
- **Validation:** walk-forward by time, metrics by segment (fast/slow, promo/non-promo, new items), bias, interval coverage, comparison with the current process.
- **Serving:** daily/hourly batch job, feature store with point-in-time correctness, model registry, forecast table with version, backfills when data is revised.
- **Monitoring:** rolling WAPE/bias vs baseline, data quality and feature drift, interval coverage, tracking signal; retraining schedule plus alert-based retrain; human override and fallback to seasonal naive.
- **Trade-offs:** accuracy vs interpretability; one global model vs segments; compute vs freshness; forecast accuracy vs inventory cost (optimise decision, not just MAE).

**Example:** Quick-commerce dark stores: 200k series, 14-day horizon, daily batch at 3 a.m.; global LightGBM must beat the seasonal-naive baseline in walk-forward backtest before go-live; weekly retrain; fallback to baseline if feed is stale.

**Follow-ups:**
- *Biggest risk?* Training on censored sales and leakage in lags/promo features.
- *How to roll out?* Shadow mode, A/B or region pilot, then compare business KPIs, not only WAPE.

**Common mistakes:** Jumping to deep learning; ignoring stockouts and promos; one number without an interval; no baseline or fallback; evaluating only aggregate WAPE.

### Q17 ⭐⭐ 🟢 What is the difference between white noise and a random walk, and why does it matter for forecasting?
**Asked at:** GCCs, consulting
**Say this first (1 line):** White noise is random values with constant mean and variance and no autocorrelation, so it is unpredictable beyond its mean; a random walk is the running sum of white noise, which is non-stationary, and its best forecast is just the last value.

**Then explain:**
- **White noise:** y_t = e_t. Stationary. Best forecast = mean. ACF all about 0.
- **Random walk:** y_t = y_{t-1} + e_t. Variance grows with time, ACF decays very slowly, one difference gives white noise. Best forecast = last value (naive); intervals widen with sqrt(h).
- **Why it matters:** (1) residuals of a good model should be white noise (nothing left to learn); (2) if a series is a random walk, complex models cannot beat naive, as in many financial prices; (3) regression between two random walks gives spurious results (Q40).
- A random walk with drift adds a constant slope.

**Example:** Simulated 1000 points: for white noise the mean is the right forecast (naive just adds the last shock as extra noise); for a random walk, naive MAE is 0.80 but using the global mean gives MAE 14.1.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(3)
wn = rng.normal(size=1000); rw = np.cumsum(wn)
print(np.abs(rw[1:] - rw.mean()).mean(), np.abs(np.diff(rw)).mean())   # mean forecast vs naive on a random walk
```

**Follow-ups:**
- *How to test?* ADF for unit root, Ljung-Box for autocorrelation.
- *Is a stock price a random walk?* Roughly for prices; returns are close to white noise, but volatility is predictable (GARCH, Q53).

**Common mistakes:** Calling any noisy series white noise; modelling a random walk with trend regression; forgetting intervals grow with horizon.

### Q18 ⭐⭐ 🟢 Explain AR, MA and ARMA models. What does each term capture intuitively?
**Asked at:** GCCs, banks, consulting
**Say this first (1 line):** AR uses past values to predict the present, MA uses past forecast errors (shocks), and ARMA combines both for a stationary series.

**Then explain:**
- **AR(p):** y_t = c + phi_1 y_{t-1} + ... + phi_p y_{t-p} + e_t. Intuition: momentum or persistence (today is like yesterday). Stationary if |phi| < 1 (AR(1)).
- **MA(q):** y_t = mu + e_t + theta_1 e_{t-1} + ... Intuition: a shock keeps echoing for q periods, then dies out (a promotion shock affecting the next day).
- **ARMA(p,q):** both; a compact way to represent a long AR with few parameters. ARIMA adds differencing.
- **Shape:** AR(1) ACF decays geometrically (phi^k); MA(q) ACF is zero after lag q (Q7).
- Do not mix up MA with moving average smoothing; here it is a model of errors.

**Example:** AR(1) with phi = 0.7: if today is +10 above average, tomorrow expect +7, then +4.9. MA(1) with theta = 0.7: a shock of +10 today contributes +7 tomorrow, then nothing.

**Code:**
```python
import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima.model import ARIMA
rng = np.random.default_rng(0)
y_stationary = ArmaProcess([1, -0.6], [1, 0.4]).generate_sample(1000, distrvs=rng.normal)   # true phi=0.6, theta=0.4
fit = ARIMA(y_stationary, order=(1, 0, 1)).fit()
print(fit.params.round(2))      # const, ar.L1, ma.L1, sigma2: ar and ma close to 0.6 and 0.4
```

**Follow-ups:**
- *Invertibility?* MA roots must be outside the unit circle so shocks can be recovered from data.
- *Why both?* Parsimony: ARMA(1,1) can replace a high-order AR.

**Common mistakes:** Applying ARMA to non-stationary data; confusing MA with a rolling mean; assuming longer p, q always helps.

### Q19 ⭐⭐ 🟡 How do you do cross-validation with sklearn TimeSeriesSplit? What does the gap parameter do and when would you add it?
**Asked at:** Product cos, live-coding rounds
**Say this first (1 line):** `TimeSeriesSplit` makes expanding-window folds where each test block comes after its train block; `gap` skips some samples between train and test so overlapping lags or labels do not leak.

**Then explain:**
- Splits are ordered: train grows, test is the next `test_size` rows. No shuffling, and the earliest rows are never tested.
- **gap = number of samples dropped between train end and test start.**
- **Add a gap when:** the target is a multi-step window (e.g. sum of next 7 days), features use rolling windows ending near the boundary, or the forecast has a lead time (you must decide 7 days ahead, so the last 7 days of data are unavailable at the origin).
- For panel data (many series), TimeSeriesSplit on row order is wrong; split on unique dates and apply the cut-off to all series.
- Use `max_train_size` for a rolling window.

**Example:** 20 rows, 3 splits, test_size 3, gap 2: train 0-8 / test 11-13, train 0-11 / test 14-16, train 0-14 / test 17-19 (rows 9-10, 12-13, 15-16 are skipped).

**Code:**
```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
X = np.arange(20).reshape(-1, 1)
for tr, te in TimeSeriesSplit(n_splits=3, test_size=3, gap=2).split(X):
    print("train", tr[0], "-", tr[-1], "test", te[0], "-", te[-1])
```

**Follow-ups:**
- *Does it support groups?* No; write a custom date-based splitter.
- *How big should gap be?* At least the horizon or the largest window overlapping the label.

**Common mistakes:** Using it on stacked panel data sorted by series; no gap with a 7-day target; thinking it shuffles; tuning on the last fold only.

### Q20 ⭐⭐ 🟡 How does SARIMA handle seasonality, and how do you pick seasonal orders (P,D,Q,m)? What about multiple seasonalities?
**Asked at:** GCCs, consulting, retail
**Say this first (1 line):** SARIMA adds seasonal AR/MA terms and seasonal differencing at lag m, written ARIMA(p,d,q)(P,D,Q)m; I choose D from the seasonal strength, P and Q from ACF/PACF spikes at multiples of m, and use other tools when there are multiple seasonalities.

**Then explain:**
- **m:** seasonal period (12 monthly, 7 daily-weekly, 24 hourly-daily).
- **D:** usually 0 or 1; seasonal difference y_t - y_{t-m}. Do not over-difference.
- **P, Q:** look at ACF/PACF at lags m, 2m. Spike at m in ACF only -> seasonal MA(1); in PACF only -> seasonal AR(1). Common default: (0,1,1)(0,1,1)m, the "airline model".
- Confirm by AIC and residual checks.
- **Limits:** one seasonal period only; large m (e.g. 365 or 168) is slow and unstable.
- **Multiple seasonalities** (hourly with daily and weekly): Fourier terms as regressors (ARIMA errors + K harmonics), TBATS, MSTL decomposition + model, Prophet, or GBM with calendar features.

**Example (Q5 monthly series):** plain ARIMA(1,1,0) AIC 572.0; SARIMA(0,1,1)(0,1,1,12) AIC 371.9, test MAE 1.46 on 12 months.

**Code:**
```python
# continuation of Q5: uses `train` built there
from statsmodels.tsa.statespace.sarimax import SARIMAX
m = SARIMAX(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit(disp=False)
print(m.aic, m.forecast(12).head(3))
```

**Follow-ups:**
- *Why not SARIMA for hourly data?* m = 168 makes the state space huge; use Fourier regressors or a global ML model.
- *Seasonality changing over time?* Use STL/ETS or rolling windows.

**Common mistakes:** Wrong m; both D = 1 and d = 1 with no need; ignoring that seasonality may be multiplicative (log first, Q24); comparing AIC across different D.

### Q21 ⭐⭐ 🟡 Explain exponential smoothing (SES, Holt, Holt-Winters/ETS). When is it better than ARIMA?
**Asked at:** Retail, supply chain, GCCs
**Say this first (1 line):** Exponential smoothing forecasts as a weighted average of the past with weights that decay exponentially: SES for level only, Holt adds trend, Holt-Winters/ETS adds seasonality.

**Then explain:**
- **SES:** level_t = alpha * y_t + (1 - alpha) * level_{t-1}. Flat forecast. Large alpha = reacts fast, small = smooth.
- **Holt:** adds a trend (beta); damped trend (phi) flattens long-horizon forecasts, usually safer.
- **Holt-Winters:** adds seasonality (gamma), additive or multiplicative.
- **ETS** is the state-space framework: Error, Trend, Seasonal each as None/Additive/Multiplicative; chooses the model by AIC and gives intervals.
- **Better than ARIMA when:** the series has clear level/trend/seasonal components, little data, you need many fast automatic forecasts, or multiplicative seasonality; ETS and ARIMA overlap but neither contains the other entirely.
- ARIMA can model richer autocorrelation, and handles regressors more directly (ARIMAX).

**Example (Q5 monthly series):** Holt-Winters (additive trend and seasonality, undamped) test MAE 1.36 vs seasonal naive 6.66; the damped version scored 2.33 here, because this series has a real linear trend that damping flattens.

**Code:**
```python
# continuation of Q5: uses `train`, `test` built there
from statsmodels.tsa.holtwinters import ExponentialSmoothing
for damped in (False, True):
    hw = ExponentialSmoothing(train, trend="add", damped_trend=damped,
                              seasonal="add", seasonal_periods=12).fit()
    print(damped, abs(test.values - hw.forecast(12).values).mean())   # False 1.36, True 2.33
```

**Follow-ups:**
- *How to choose alpha?* Fit by minimising squared one-step error; do not hand-tune.
- *Why damped?* Linear trends rarely continue forever; damped usually wins in M-competitions.

**Common mistakes:** Using additive seasonality on growing amplitude; SES on trending data; forgetting that ETS cannot use external regressors.

### Q22 ⭐⭐ 🟡 How does Prophet work (trend, seasonality, holidays, changepoints), and what are its strengths and weaknesses?
**Asked at:** Product cos, startups, analytics roles
**Say this first (1 line):** Prophet is an additive regression: trend (piecewise linear or logistic with changepoints) + Fourier-term seasonalities + holiday effects + noise, fitted as a Bayesian model, built to be quick and analyst-friendly.

**Then explain:**
- **Trend:** piecewise with automatically placed changepoints; `changepoint_prior_scale` controls flexibility. Logistic growth supports a cap.
- **Seasonality:** weekly, yearly (and custom) using Fourier series; `seasonality_mode` additive or multiplicative.
- **Holidays:** a list of dates with lower/upper windows, each gets its own effect; extra regressors supported.
- **Strengths:** handles missing data and outliers decently, interpretable components, multiple seasonalities, holidays, little tuning, uncertainty intervals.
- **Weaknesses:** often beaten by tuned GBM/ETS on accuracy, weak at short-term autocorrelation, trend extrapolation can be risky, one model per series (slow for thousands), intervals only cover trend uncertainty by default.

**Example:** Daily orders for one product with weekly and festival peaks: Prophet gives a quick, explainable decomposition for stakeholders, then a global GBM is built if accuracy matters at scale.

**Code (not executed: prophet not installed here):**
```python
from prophet import Prophet
m = Prophet(changepoint_prior_scale=0.05, seasonality_mode="multiplicative")
m.add_country_holidays(country_name="IN")
m.fit(df.rename(columns={"date": "ds", "y": "y"}))
fc = m.predict(m.make_future_dataframe(periods=28))
```

**Follow-ups:**
- *Overfitting changepoints?* Lower `changepoint_prior_scale`, restrict `changepoint_range`.
- *Cross-validation?* `prophet.diagnostics.cross_validation` for rolling-origin evaluation.

**Common mistakes:** Using it as a default winner without a baseline; leaving yearly seasonality on short history; forgetting that the regressors need future values.

### Q23 ⭐⭐ 🟡 How do you encode calendar features for ML forecasters (day-of-week, month, Fourier terms, cyclical sin/cos) and which works best?
**Asked at:** Product cos, e-commerce
**Say this first (1 line):** I use plain categorical (or integer) calendar features for tree models, sin/cos or Fourier terms when I want smooth cyclic behaviour in linear/NN models, and I pick by backtest.

**Then explain:**
- **Day-of-week, month, hour:** integer or categorical; trees split on them fine and can model each weekday separately.
- **Cyclical sin/cos:** puts a cycle on a circle so Sunday is next to Monday. For linear/neural models, raw integers wrongly say 6 is far from 0.
- **Fourier terms:** K harmonics of the period (yearly with K = 3-10) give smooth seasonality with few features; K controls flexibility.
- **Others:** holiday flags, days to/since event, week of month, payday, is-weekend.
- **What works best:** GBM: raw categorical/integer features, sin/cos adds little because trees can split; linear models and NNs: Fourier/sin-cos. Always check.

**Example:** Raw distance between Sunday (6) and Monday (0) is 6; with sin/cos it is 0.868, the same as Monday to Tuesday.

**Code:**
```python
import numpy as np, pandas as pd
c = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=400)})
c["dow"] = c.date.dt.dayofweek
c["dow_sin"], c["dow_cos"] = np.sin(2*np.pi*c.dow/7), np.cos(2*np.pi*c.dow/7)
doy = c.date.dt.dayofyear
for k in (1, 2, 3):
    c[f"yr_sin{k}"] = np.sin(2*np.pi*k*doy/365.25)
    c[f"yr_cos{k}"] = np.cos(2*np.pi*k*doy/365.25)
```

**Follow-ups:**
- *One-hot vs integer for trees?* Integer works; one-hot is fine for few levels.
- *Leap years?* Use day-of-year / 365.25 or a continuous time-of-year fraction.

**Common mistakes:** Feeding raw month integers to a linear model; sin without cos (ambiguous); too many Fourier terms overfitting; calendar features computed in the wrong time zone.

### Q24 ⭐⭐ 🟡 When do you use a log or Box-Cox transform in forecasting, and how do you back-transform correctly?
**Asked at:** GCCs, retail, consulting
**Say this first (1 line):** I take the log (or Box-Cox) when variance grows with the level or seasonality is multiplicative; the key is back-transforming correctly, because exp of the mean forecast is the median, not the mean.

**Then explain:**
- **Use when:** growing seasonal amplitude, right-skewed positive data, percent-type effects.
- **Log:** simple, Box-Cox lambda = 0. **Box-Cox:** lambda between 0 and 1 for milder stabilisation; estimate with `scipy.stats.boxcox` (training data only). Needs positive data; use log1p or Yeo-Johnson with zeros.
- **Back-transform:** point forecast of the log is the median on the original scale. The mean is exp(mu + sigma^2/2) for a log-normal. Prediction interval limits can be transformed directly (quantiles are preserved).
- Decide which you need: median for MAE targets, mean for totals/inventory sums.

**Example:** Log-normal data (mu = 3, sigma = 0.5): true mean 22.76, exp(mean of log) = 20.09 (median is 20.08), exp(mu + sigma^2/2) = 22.76. Naive back-transform under-forecasts by about 12%.

**Code:**
```python
import numpy as np
from scipy.stats import boxcox
from scipy.special import inv_boxcox
x = np.random.default_rng(3).normal(3, 0.5, 100000); y = np.exp(x)
print(y.mean(), np.exp(x.mean()), np.exp(x.mean() + x.var()/2))     # 22.76, 20.09, 22.76
b, lam = boxcox(y[:1000]); print(np.allclose(inv_boxcox(b, lam), y[:1000]))
```

**Follow-ups:**
- *Does a log change the metric you optimise?* Yes: MSE in log space is not MSE in original units; evaluate in original units.
- *Tree models need a log?* Not for stationarity, but it can help with skewed targets, or use Tweedie/Poisson objectives.

**Common mistakes:** Forgetting to invert; summing exp(forecasts) and treating it as a mean total; fitting lambda on the full data (leakage); logging zeros.

### Q25 ⭐⭐ 🟡 How do you diagnose a fitted forecasting model using residuals (Ljung-Box, residual ACF, normality)?
**Asked at:** GCCs, banks, consulting
**Say this first (1 line):** If the model has captured the signal, residuals should look like white noise: no autocorrelation, zero mean, roughly constant variance, and approximately normal; I check with the residual plot, residual ACF, Ljung-Box and a QQ plot.

**Then explain:**
- **Residual ACF + Ljung-Box:** null = no autocorrelation up to lag h. Large p-value is good. Set `model_df` = number of fitted ARMA parameters.
- **Mean zero / bias:** residual mean test; a non-zero mean is bias.
- **Constant variance:** residuals vs time and vs fitted; look for changing variance (log, GARCH).
- **Normality:** QQ plot, Jarque-Bera. Needed for analytic intervals, not for point forecasts.
- **If it fails:** add AR/MA or seasonal terms, regressors, handle outliers, transform.
- **Remember:** passing the checks does not mean it forecasts well; out-of-sample error decides.

**Example (Q5 monthly series):** SARIMA(0,1,1)(0,1,1,12) residuals: Ljung-Box p = 0.50 (pass). A plain AR(1) on the same trending-seasonal series: p about 3e-57 (clear leftover pattern).

**Code:**
```python
# continuation of Q5: uses `train` built there
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
fit = SARIMAX(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit(disp=False)
print(acorr_ljungbox(fit.resid[13:], lags=[12], model_df=2))   # skip burn-in residuals; p = 0.50
fit.plot_diagnostics()                                          # residuals, hist, QQ, correlogram
```

**Follow-ups:**
- *Lags to test?* About min(10, n/5) non-seasonal; 2m for seasonal.
- *Heteroscedastic residuals?* Transform or model variance (Q53).

**Common mistakes:** Forgetting `model_df`; including the burn-in residuals; relying on Ljung-Box with many lags; treating non-normality as fatal for point forecasts.

### Q26 ⭐⭐ 🟡 How do you produce prediction intervals / uncertainty ranges (analytic, bootstrap, quantile regression), and what do you do when intervals miss too many actuals?
**Asked at:** Product cos, supply chain, Europe retail
**Say this first (1 line):** I get intervals three ways: analytic from the model's error assumptions, bootstrap of residuals, or quantile regression/conformal; then I check empirical coverage in a backtest and recalibrate if it is off.

**Then explain:**
- **Analytic:** ARIMA/ETS give forecast +/- z * sd(h), assuming normal, uncorrelated errors; widens with horizon.
- **Bootstrap:** resample residuals (block bootstrap if autocorrelated) and simulate future paths; no normal assumption.
- **Quantile regression:** train for the 10th and 90th percentiles (pinball loss; LightGBM `objective="quantile"`). Handy for global ML models.
- **Conformal:** use backtest residuals to calibrate interval width (Q47).
- **Coverage check:** the share of actuals inside an 80% interval should be about 80%.
- **Too many misses:** intervals too narrow. Fix by using residuals from multi-step out-of-sample backtests per horizon, inflating by scaling factors, conformal recalibration, modelling heteroscedasticity, or checking for drift.

**Example:** on the 20 synthetic series of Q10, LightGBM quantile models (0.1 and 0.9) gave 74% coverage on the last 45 days versus a nominal 80%, a typical under-coverage because the models are fitted on training noise levels that differ from the test block; I would recalibrate on backtest residuals.

**Code:**
```python
# continuation of Q10: uses `train`, `test`, `feats` built there
import lightgbm as lgb, numpy as np
Xtr, ytr, Xte, yte = train[feats], train.y, test[feats], test.y
q = {a: lgb.LGBMRegressor(objective="quantile", alpha=a, n_estimators=200,
                          learning_rate=0.05, verbose=-1, random_state=0).fit(Xtr, ytr) for a in (0.1, 0.9)}
lo, hi = q[0.1].predict(Xte), q[0.9].predict(Xte)
print("coverage", np.mean((yte >= lo) & (yte <= hi)))   # about 0.74 vs nominal 0.80
```

**Follow-ups:**
- *Quantile crossing?* Sort the quantiles or fit monotone models.
- *Which metric for intervals?* Coverage, width, pinball loss/CRPS (Q46).

**Common mistakes:** Trusting normal intervals blindly; evaluating coverage in-sample; ignoring that intervals must widen with horizon; reporting only a point forecast.

### Q27 ⭐⭐ 🟡 Global vs local models: how do you forecast thousands of related series, and when do you pick one global GBM/DL model over per-series models?
**Asked at:** Flipkart, Amazon, Walmart, Zalando, Delivery Hero-style roles
**Say this first (1 line):** For thousands of related series I usually train one global model (GBM or deep net) across all of them with series identifiers and features, because it shares patterns, handles short histories and is far cheaper to maintain than thousands of local models.

**Then explain:**
- **Local models:** one per series (ARIMA/ETS). Fit each series' own dynamics, but noisy for short or sparse series, and thousands of models to fit and monitor.
- **Global model:** one model on all series, features include lags, calendar, price, promo, series/category embedding or id. Learns shared seasonality and promo effects; works for new/short series.
- **When local wins:** few, long, very different series (national KPIs), strong series-specific dynamics, small data.
- **Practical:** normalise or scale series (divide by recent mean) so large and small series are comparable; use weights (e.g. by volume) in the loss; segment very different groups (fast vs slow movers) or use a hybrid; add hierarchy reconciliation (Q42).
- M5 competition winners used global LightGBM.

**Example:** the same 20 synthetic daily series as Q10: one global LightGBM with `series` as a categorical plus lag1/7/14 and shifted roll7 gave WAPE 0.072 on the last 45 days vs seasonal naive 0.088, with one model instead of 20.

**Code:**
```python
# continuation of Q10: uses `train`, `test`, `feats` built there (series already a category)
import lightgbm as lgb
m = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, verbose=-1, random_state=0)
m.fit(train[feats], train.y)
wape = abs(test.y - m.predict(test[feats])).sum() / test.y.sum()     # 0.072
```

**Follow-ups:**
- *Cold start?* Global model plus attributes handles new series (Q29).
- *Does one global model ignore series differences?* Series id, per-series scaling and interaction features restore them.

**Common mistakes:** Not scaling series; random CV across series and time; letting big series dominate the loss unintentionally; assuming global always beats local without a backtest.

### Q28 ⭐⭐ 🟡 Why does a demand forecast under-forecast after stockouts, and how do you handle censored (sales != demand) data?
**Asked at:** Retail, quick commerce, e-commerce
**Say this first (1 line):** Sales are not demand: when stock runs out, sales stop at the stock level, so a model trained on sales learns a number lower than real demand and under-forecasts again, which causes more stockouts.

**Then explain:**
- **Censored data:** on a stockout day we only know demand was at least the sales figure, not the exact value.
- **Feedback loop:** low forecast, less stock, more stockouts, lower sales, lower forecast.
- **Detect it:** join with inventory/availability data; flag days with zero or low stock, or hours out of stock for the item.
- **Fixes, simplest first:**
  - Flag in-stock vs out-of-stock and add availability as a feature, then forecast with availability set to 100%.
  - Impute demand on stockout days (similar days, sibling stores, hourly profile of the day before stock ran out).
  - Censored likelihood (Tobit-style): in-stock days use the normal likelihood, stockout days use the probability of "demand at least sales".
  - Use substitutes and lost-sale proxies (page views, add-to-cart, searches) as demand signals.
- **Do not just drop stockout days.** Stockouts happen on high-demand days, so dropping them biases the mean downward.
- **Business side:** forecast demand, then decide stock; keep a service-level target separate from the forecast.

**Example:** Simulated Poisson demand with mean 20 and stock caps of 12 to 40: 54% of days stocked out. Mean sales was 17.0 against true 20.7. Dropping stockout days gave 19.9, still low. The censored MLE gave 20.8.

**Code:**
```python
import numpy as np
from scipy.stats import poisson
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(0)
demand = rng.poisson(20, 200)
stock = rng.choice([12, 15, 18, 40], 200, p=[.2, .2, .2, .4])
sales = np.minimum(demand, stock); so = sales >= stock
nll = lambda l: -(poisson.logpmf(sales[~so], l).sum() + poisson.logsf(sales[so] - 1, l).sum())
print(sales.mean(), sales[~so].mean(), minimize_scalar(nll, bounds=(1, 60), method="bounded").x)
# 17.04 19.86 20.78  (true mean of demand: 20.7)
```

**Follow-ups:**
- *No inventory data?* Use zero-sales streaks and proxies such as page views, and be explicit about the bias.
- *Quick commerce?* Hourly availability matters; weight demand by hours in stock.

**Common mistakes:** Treating sales as demand; dropping stockout days; not versioning availability data; evaluating on sales so the biased model looks accurate.

### Q29 ⭐⭐ 🟡 How do you forecast a new product or new store with no history (cold start)?
**Asked at:** Retail, fashion e-commerce (Zalando-style), quick commerce
**Say this first (1 line):** With no history I borrow it: forecast from similar products or stores using attributes, then switch to the product's own data as it arrives.

**Then explain:**
- **Analogs:** find similar items (category, price, brand, season, size) and use their launch curves, scaled to an expected level.
- **Global model with attributes:** a GBM trained on all items with attribute and calendar features (no lags at launch) predicts launch-week volume; lag features appear only as data arrives.
- **Hierarchy prior:** start from the category or cluster forecast and split by a share estimate.
- **Blend over time:** weight = prior at week 0, moving to the item's own history by week 4-8 (Bayesian shrinkage idea, a partial pooling of item vs group).
- **Extras:** launch marketing, placement, price, initial stock (stock caps sales, see Q28), and a wide interval.
- **Evaluate:** backtest on past launches only: "forecast the first N weeks of items launched last season".

**Example:** 300 synthetic items with 4 attributes; for one new item the median of its 10 nearest neighbours gave 19.2 weekly units against a true 21.2, while the all-item mean was 16.6 (one item only, so a demonstration rather than a benchmark).

**Code:**
```python
import numpy as np
from sklearn.neighbors import NearestNeighbors
rng = np.random.default_rng(0)
attrs = rng.normal(size=(300, 4))                                             # n_items x n_features
level = np.exp(2.5 + attrs @ [.5, .3, -.2, .4] + rng.normal(0, .15, 300))     # past items' typical weekly volume
new_attr = rng.normal(size=(1, 4)); true = np.exp(2.5 + new_attr @ [.5, .3, -.2, .4])[0]
nn = NearestNeighbors(n_neighbors=10).fit(attrs)
_, idx = nn.kneighbors(new_attr)
est = np.median(level[idx[0]])                          # 19.2 (true 21.2, all-item mean 16.6)
```

**Follow-ups:**
- *New store?* Same idea: similar stores by catchment, size and format, plus local events.
- *How fast to update?* Let the item's own sales take over once the error vs the prior is consistently lower, often 2-4 weeks.

**Common mistakes:** Using the overall average; random split across items (leaks launch seasons); ignoring stock limits at launch; overconfident intervals; never switching to own data.

### Q30 ⭐⭐ 🟡 How do you forecast intermittent / lumpy demand? Explain Croston, SBA, TSB and which metrics to use.
**Asked at:** Supply chain, spare parts, retail
**Say this first (1 line):** Intermittent demand is mostly zeros with occasional spikes; I use Croston-type methods that smooth the demand size and the gap between demands separately, and judge them with bias and scaled or probabilistic metrics rather than MAPE.

**Then explain:**
- **Croston:** smooth non-zero size z and interval p with SES; forecast = z / p. Updates only when demand occurs.
- **SBA (Syntetos-Boylan):** Croston is biased upward; multiply by (1 - alpha/2).
- **TSB:** smooths the probability of demand every period (so it decays to zero) and size separately; better for items going obsolete. Croston never decays between demands.
- **Classify first:** ADI (average gap) and CV^2 of sizes give smooth / erratic / intermittent / lumpy.
- **Metrics:** MAPE is undefined with zeros; use MASE or RMSSE, bias (ME), and for stock decisions quantile/pinball loss or service level, since the mean forecast is not the order-up-to level.
- **Modern:** global GBM with count objective (Poisson/Tweedie), or probabilistic forecasts of the demand distribution.

**Example (simulated, code below):** 104 weeks, about 25% non-zero demand, true mean 1.47: Croston 1.41, SBA 1.34, TSB 1.27 (all in the right range). After 24 further zero weeks (item gone obsolete), Croston still says 1.41 because it never updates on zeros, while TSB falls to 0.10.

**Code:**
```python
import numpy as np
def croston(y, a=.1, sba=False):
    z = p = None; q = 1
    for v in y:
        if v > 0:
            if z is None: z, p = v, q
            else: z += a*(v - z); p += a*(q - p)
            q = 1
        else: q += 1
    f = z / p
    return f*(1 - a/2) if sba else f
def tsb(y, a=.1, b=.1):
    pr = (y[:5] > 0).mean(); z = y[y > 0][0]
    for v in y:
        pr += b*((v > 0) - pr)
        if v > 0: z += a*(v - z)
    return pr * z
rng = np.random.default_rng(0)
y = np.where(rng.random(104) < .25, rng.poisson(5, 104) + 1, 0).astype(float)
print(y.mean(), croston(y), croston(y, sba=True), tsb(y))      # 1.47 1.41 1.34 1.27
y2 = np.r_[y, np.zeros(24)]
print(croston(y2), tsb(y2))                                    # 1.41 0.10
```

**Follow-ups:**
- *Why not ARIMA?* Normal-error models handle zero-heavy data poorly and give negative values.
- *How to set stock?* Use the demand distribution over lead time (Poisson, negative binomial, bootstrap), not the mean.

**Common mistakes:** Using MAPE; evaluating only RMSE (rewards forecasting zeros); using Croston on obsolescent items; forgetting that the point forecast is not a safety-stock level.

### Q31 ⭐⭐ 🟡 When would you use LSTM/GRU/1D-CNN for forecasting instead of GBM, and why do deep models often fail to beat strong baselines?
**Asked at:** Product cos, research-leaning teams
**Say this first (1 line):** I reach for LSTM/GRU/CNN when I have lots of data, many related series, rich covariates or long complex patterns; otherwise a lag-feature GBM or a seasonal baseline usually matches or beats them with much less effort.

**Then explain:**
- **When deep helps:** many thousands of series, long histories, multi-horizon outputs, text/image or other non-tabular inputs, probabilistic outputs (DeepAR style, Q48).
- **1D-CNN:** fast, good for local patterns, easy to parallelise; GRU is a lighter LSTM.
- **Why they often fail to beat baselines:**
  - Most business series are short and noisy; a deep net overfits.
  - Need careful scaling, windowing, seeds, tuning; results vary across seeds.
  - Strong baselines (seasonal naive, ETS, GBM) already capture most signal; M4/M5 results show simple or hybrid methods competitive.
  - Tabular feature engineering (calendar, price, promo) is easier with GBMs.
- **Fair comparison:** same rolling-origin backtest, several seeds, tuned baselines, and cost (training time, serving, explainability).

**Example:** On a noisy daily series with weekly seasonality (see Q36), a 2x256 MLP scored 9.1% held-out WAPE against 9.0% for seasonal naive: the series is mostly pattern plus noise, no model can go below the noise floor, so extra capacity only adds variance.

**Follow-ups:**
- *Your first approach?* Seasonal naive, ETS, then global LightGBM; deep model only if gains are clear.
- *Scaling inputs?* Scale per series using the training window only.

**Common mistakes:** Starting with deep nets; comparing against an untuned baseline; one seed; random split; ignoring serving and maintenance cost.

### Q32 ⭐⭐ 🟡 How do you monitor a deployed forecast model and decide retraining frequency?
**Asked at:** Product cos, MLE roles
**Say this first (1 line):** I track forecast error and bias against a naive baseline as actuals arrive, alert on drift, and retrain on a schedule matched to how fast the data changes, plus a trigger when monitoring says the model is stale.

**Then explain:**
- **Accuracy:** rolling WAPE/MASE per horizon and segment (not just one global number), always against seasonal naive so you know if the model still adds value.
- **Bias:** mean error and tracking signal; persistent over- or under-forecasting hurts inventory more than noise.
- **Interval coverage:** is the 80% interval still covering about 80%?
- **Input drift:** feature distributions, missing data, price/promo mix, new items (PSI or simple summary stats); and data pipeline health (late or missing data).
- **Retraining:** fixed cadence (weekly/monthly) for stable series, plus trigger-based (error above threshold for N periods, drift, structural break). Retrain on rolling or expanding window; validate with a backtest, compare champion vs challenger, then promote.
- **Operations:** log forecasts with the model version and data vintage so error can be computed later (Q38); fallbacks if the model fails.

**Example:** Simulated weekly demand with a level shift of +12 (about 2.4 sd) at week 80. A trailing 8-week mean-error z-score alarm at |z| > 3 first fired at week 83 (3 weeks after the shift), with 2 false alarms in the 80 weeks before. WAPE over 14 weeks moved from 5.2% to 10.8%.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0); actual = 100 + rng.normal(0, 5, 94); actual[80:] += 12   # level shift at week 80
forecast = np.full(94, 100.)                       # a stale forecast that does not know about the shift
e = pd.Series(actual - forecast)
sd = e[:60].std()                                  # error spread from a stable period
z = e.rolling(8).mean() / (sd / np.sqrt(8))        # bias alarm
alarm = z.abs() > 3
wape14 = e.abs().rolling(14).sum() / pd.Series(actual).rolling(14).sum()
print(alarm[alarm].index.tolist(), wape14[79].round(3), wape14[93].round(3))   # [48, 49, 83, ...] 0.052 0.108
```

**Follow-ups:**
- *How often to retrain?* As often as the cost of a stale model exceeds retraining cost; fast-changing retail often weekly, stable KPIs quarterly.
- *Alert fatigue?* Use multi-period windows and tiered thresholds.

**Common mistakes:** Monitoring only an aggregate metric; no baseline comparison; retraining blindly without backtest; not storing forecasts for later scoring; confusing data drift with model error.

### Q33 ⭐⭐ 🟡 One-step-ahead forecasts look good but 12-step-ahead forecasts fail. What are the likely causes?
**Asked at:** Product cos, Amazon-style
**Say this first (1 line):** One-step forecasts can lean on yesterday's actual, which is mostly persistence; at 12 steps that anchor is gone, so errors compound and any missing structure shows up.

**Then explain:**
- **Easy one-step task:** the last value is a strong predictor, so even a weak model looks good; always compare to naive at each horizon.
- **Recursive error accumulation:** feeding your own predictions back in compounds errors (and shrinks toward the mean).
- **Missing future inputs:** lags are fine at h=1 but features such as price, promo, weather need future values (Q34).
- **Wrong training target:** model trained for h=1 only; use direct models per horizon or a multi-output model.
- **Leakage at h=1:** a leaky feature may only exist for the short horizon.
- **Evaluation:** one-step rolling backtests do not test long-horizon behaviour; evaluate per horizon with the real forecast origin.
- **Drift, trend and seasonality** not modelled: errors grow with horizon naturally.

**Example (simulated daily series with weekly seasonality and a drift, Ridge on 7 lags, 100 held-out days):** recursive MAE at horizons 1/6/12: 0.91 / 0.95 / 0.85. Direct models trained per horizon: 0.91 / 0.91 / 0.84. Identical at h=1 and only slightly better at longer horizons: on an easy periodic series the compounding is small. The gap is larger with weaker or non-linear models and noisier series, which is why I always measure per horizon. (Numbers from a throwaway simulation, not a benchmark.)

**Follow-ups:**
- *Recursive vs direct?* Recursive: one model, error compounds. Direct: one per horizon, no compounding, more models and no consistency across horizons. Hybrids and multi-output nets exist.
- *Expected error growth?* Roughly with the square root of horizon for random-walk-like series.

**Common mistakes:** Reporting only h=1 metrics; no naive baseline per horizon; using actual future covariates in the backtest; mixing training horizon and evaluation horizon.

### Q34 ⭐⭐ 🟡 A useful feature (e.g. weather, ad spend) is not known at forecast time. How do you handle it without leakage?
**Asked at:** Product cos, energy, retail
**Say this first (1 line):** I only use a feature in the form I will actually have at forecast time: lagged values, a planned/forecasted version of it, or a scenario input, and I backtest with the same version.

**Then explain:**
- **Known in future:** calendar, holidays, planned price or promo, planned ad budget: use freely.
- **Unknown in future:** weather, competitor price, actual traffic: use lags only (value up to the origin), or a forecast of it.
- **Forecast of the feature:** use the forecast that was available then (the weather forecast issued the day before, not the actual); a two-stage model adds the first model's error.
- **Scenario:** for controllable drivers (ad spend), forecast conditional on a plan: "if spend is X, demand is Y".
- **Backtest honesty:** build features by origin date: for each origin, only data up to that origin (and forecast vintages, Q38).
- **Leakage test:** if accuracy at h=1 is suspiciously great, check whether a feature uses the target period.

**Example:** Using actual temperature of the forecast day improves backtest WAPE; in production only the day-ahead weather forecast exists, so the accuracy drops. Training on actual weather but serving forecast weather is a train/serve mismatch; train on archived forecasts instead.

**Code:**
```python
# features valid at origin t for horizon h   # not executed (illustrative)
df["temp_lag_h"] = df.groupby("series")["temp"].shift(h)       # known at origin
df["temp_fc_h"] = df["temp_forecast_issued_t"]                  # archived forecast, not the actual
```

**Follow-ups:**
- *Is a lag of ad spend useful?* Yes if the effect is delayed (carry-over), and it is known at the origin.
- *What about the quality of the feature forecast?* Include its error in intervals.

**Common mistakes:** Using actuals of the future period in the backtest; training on actual weather but serving forecasted weather; shifting by the wrong amount; ignoring feature availability lag.

### Q35 ⭐⭐ 🟡 How do you handle structural breaks, regime shifts (COVID, pricing change) and concept drift in forecasting?
**Asked at:** Product cos, fintech, retail
**Say this first (1 line):** I detect the break, decide if it is a one-off shock or a new regime, then adapt: flag/remove the shock, add regime features, shorten the training window, or reweight recent data, and monitor so I catch the next one early.

**Then explain:**
- **Detect:** residual drift or tracking signal (Q32), changepoint tests (CUSUM, Chow, PELT), or just a plot with business context.
- **Temporary shock (lockdown week, outage):** mark with a dummy variable or treat as missing; do not let it teach the model a false seasonality.
- **Permanent shift (price change, new policy):** add a level-shift/step feature, or train only on the post-break data; weight recent data more.
- **Gradual drift:** rolling window, exponential weighting, frequent retraining; adaptive models (ETS adapts by design).
- **Use external knowledge:** the cause is often known to the business: include it as a feature; use scenarios and wider intervals.
- **Validate:** backtest across the break to see how fast the method recovers; compare with naive.

**Example:** A weekly series (level 100, noise sd 5) jumps by 12 at week 80. Ten weeks later, forecasting the next 2 weeks: the all-data mean (101.9) has expected MAE about 10.1, a 20-week window (107.0) about 5.7, an 8-week window (112.4) about 4.0 (simulated, averaged over 2,000 future weeks). Shorter windows adapt faster, at the cost of more noise when there is no break.

**Follow-ups:**
- *Remove COVID data?* Usually mark it and down-weight, not delete, so calendar alignment stays intact; for a new regime keep recent data only.
- *Break at the very end of the data?* Hard to tell shock from shift; widen intervals and watch.

**Common mistakes:** Averaging over a break; deleting rows (breaking lags); refitting too late; treating every outlier as a regime change.

### Q36 ⭐⭐ 🟡 A deep model beats the baseline in training but not in backtesting. What do you do?
**Asked at:** Product cos, senior rounds
**Say this first (1 line):** It is overfitting or the training setup leaks, so I trust the backtest, check the evaluation setup first, then reduce model capacity and compare against a tuned simple baseline.

**Then explain:**
- **Check for leakage/mismatch first:** does the training metric use data the backtest cannot see (scaling on the full series, future features, random split)?
- **Overfitting:** high-capacity net on few windows; use smaller model, dropout, weight decay, early stopping on a time-based validation set, fewer features.
- **Same protocol:** rolling-origin backtest with several origins, several seeds, and per-horizon metrics; one origin is noisy.
- **Baselines:** seasonal naive, ETS and tuned LightGBM must be evaluated the same way.
- **Data size:** more series (global model), augmentation, or pre-trained/foundation model (Q49) rather than a deeper net.
- **Decide:** if no consistent win after these checks, ship the simpler model.

**Example (code below):** a 2x256 MLP on 14 lags of a noisy weekly-seasonal series (214 points, 70/30 time split). Training WAPE 4.4%, held-out WAPE 9.1%, seasonal naive 9.0% on the same held-out block. The training number says nothing; the net does no better than the baseline, so the extra complexity buys nothing.

**Code:**
```python
import numpy as np
from sklearn.neural_network import MLPRegressor
rng = np.random.default_rng(2); t = np.arange(214)
y = 50 + 8*np.sin(2*np.pi*t/7) + rng.normal(0, 4, 214)      # weekly seasonality + noise
P = 14
X = np.array([y[i-P:i] for i in range(P, 214)]); Y = y[P:]; cut = int(len(Y)*.7)
mlp = MLPRegressor(hidden_layer_sizes=(256, 256), max_iter=3000, random_state=0).fit(X[:cut], Y[:cut])
w = lambda a, b: abs(a - b).sum() / abs(a).sum()
print(w(Y[:cut], mlp.predict(X[:cut])), w(Y[cut:], mlp.predict(X[cut:])), w(Y[cut:], X[cut:, -7]))   # 0.044 0.091 0.090
```

**Follow-ups:**
- *Is a train/backtest gap always overfitting?* No: also distribution shift, leaking features or evaluation bugs.
- *How to compare fairly?* Same folds, same horizon, paired differences across series.

**Common mistakes:** Believing training metrics; tuning on the backtest folds; evaluating one seed or one origin; adding complexity rather than checking the baseline.

### Q37 ⭐⭐ 🟡 How do you pick a forecast loss when over- and under-forecasting have different costs (bias, tracking signal, quantile/newsvendor)?
**Asked at:** Supply chain, retail, Amazon-style
**Say this first (1 line):** When under- and over-forecasting cost different amounts, the best forecast is not the mean but a quantile, the critical ratio cu / (cu + co), so I train with pinball (quantile) loss and track bias separately.

**Then explain:**
- **Symmetric loss (MAE/MSE):** treats both errors alike; gives median (MAE) or mean (MSE).
- **Newsvendor:** if a lost sale costs cu and a leftover unit costs co, the optimal stock is the quantile at tau = cu / (cu + co).
- **Pinball loss at tau:** tau * max(y - q, 0) + (1 - tau) * max(q - y, 0). Minimised by the true tau-quantile. LightGBM `objective="quantile"`.
- **Bias:** mean error (or sum of errors / sum of actuals); persistent bias is a model problem, not noise.
- **Tracking signal:** cumulative error / MAD; flags drift in bias (Q32).
- **Business metric last:** evaluate with the real cost function (inventory + lost sales) or service level, not only MAPE.

**Example:** Poisson demand mean 50; lost sale costs 9, leftover costs 1 (tau = 0.9). Ordering the mean (50) costs 28.3 per period; ordering the 90th percentile (59) costs 12.7.

**Code:**
```python
import numpy as np
d = np.random.default_rng(0).poisson(50, 20000).astype(float)
cu, co = 9, 1
cost = lambda q: (cu*np.maximum(d - q, 0) + co*np.maximum(q - d, 0)).mean()
print(cost(d.mean()), cost(np.quantile(d, cu/(cu+co))))   # 28.29  12.71
```

**Follow-ups:**
- *Why not MAPE?* It penalises over-forecasts more than under-forecasts, favouring low forecasts, and breaks on zeros.
- *Same tau for all items?* No: the ratio varies by margin, shelf life and substitutability.

**Common mistakes:** Optimising MSE then adding ad hoc safety stock; using MAPE; ignoring bias; one quantile for every SKU.

### Q38 ⭐⭐ 🟡 How does late-arriving or revised recent data affect forecasting, and how do you evaluate with data vintages?
**Asked at:** Product cos, fintech
**Say this first (1 line):** Recent data is often incomplete or later revised, so I train and backtest on the data as it looked at the time (vintages), and I design the model to cope with immature recent values.

**Then explain:**
- **Late arrivals:** the last few days show artificially low counts (orders still being logged); models see a false "drop".
- **Revisions:** metrics like GDP, returns, or corrected orders change after the first release.
- **Vintage-aware evaluation:** for each forecast origin, use only the data snapshot available at that time ("real-time data"), and score against a defined final value (e.g. after 14 days).
- **Handling:** drop or down-weight the incomplete tail; model the completion curve (share of final value known after k days) to nowcast the final number; add "data age" as a feature.
- **Store snapshots:** keep as-of tables (data with load timestamps) so backtests are reproducible.
- **Choose the target:** forecast the final value, not the first release.

**Example (illustrative numbers):** Orders for yesterday are 70% complete at 8am. If the model uses the raw count, it sees a drop of 30%. Dividing by the historical completion rate (0.70) gives a nowcast near the final figure.

**Follow-ups:**
- *Training on final data, serving on immature data?* Train/serve mismatch; build training features from the same lag.
- *Where to store?* Bitemporal tables: event time and ingestion time.

**Common mistakes:** Backtesting on fully revised data; treating the incomplete tail as real; overwriting history without timestamps; no definition of "actual".

### Q39 ⭐⭐ 🟡 A promotion changes the demand pattern. How do you separate baseline demand from promo uplift and forecast it?
**Asked at:** Retail, e-commerce, quick commerce
**Say this first (1 line):** I model promo as a driver with its own effect (an uplift multiplier on a baseline), estimated while controlling for seasonality and price, then forecast baseline times uplift using the planned promo calendar.

**Then explain:**
- **Baseline:** what would have sold without a promo, from seasonality, trend, price and calendar.
- **Uplift:** promo effect, usually multiplicative: use log-linear/Poisson regression, or a GBM with promo features (depth, type, duration, display).
- **Confounding:** promos run on busy days, so a naive promo vs non-promo comparison overstates uplift; control for day of week and season.
- **Other effects:** pre-promo dip (customers wait), post-promo dip (pull-forward), cannibalisation of substitutes, halo on complements; add lead/lag promo features.
- **Forecast:** the promo calendar is known in advance, so promo features are legitimate future inputs (Q34).
- **Validate:** hold out whole promo events; check uplift by promo type; use experiments if possible.

**Example (simulated, code below):** promos were more likely on high-demand days, true uplift 1.35x. The naive promo / non-promo sales ratio was 1.60x; a Poisson GLM controlling for the demand signal gave 1.35x.

**Code:**
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0); n = 600
dow_signal = rng.normal(0, .5, n)                                  # busy-day signal (day of week / season)
promo = (rng.random(n) < 1/(1 + np.exp(-(2*dow_signal - 1.5)))).astype(float)   # promos favour busy days
y = rng.poisson(np.exp(3 + 0.5*dow_signal + np.log(1.35)*promo))   # true uplift 1.35x
X = np.c_[np.ones(n), dow_signal, promo]
m = sm.GLM(y, X, family=sm.families.Poisson()).fit()
print(y[promo == 1].mean() / y[promo == 0].mean(), np.exp(m.params[2]))   # naive 1.60, GLM 1.35
```

**Follow-ups:**
- *How to get a clean baseline for the past?* Fit the model without promo days, or predict with the promo feature set to 0.
- *Cannibalisation?* Add own-category promo intensity features.

**Common mistakes:** Naive comparison of promo vs non-promo days; ignoring pull-forward; no promo features in future; random CV across promo events.

### Q40 ⭐⭐ 🟡 Why does autocorrelation in residuals break OLS regression assumptions, and what is spurious regression?
**Asked at:** GCCs, economics-flavoured DS roles
**Say this first (1 line):** OLS assumes independent errors; with autocorrelated residuals the coefficients stay unbiased (if regressors are exogenous) but the standard errors are wrong, so p-values and intervals are overconfident, and with trending series you can get spurious regression.

**Then explain:**
- **Effect:** positive autocorrelation makes each observation carry less new information than OLS thinks, so standard errors are too small and t-stats too large.
- **Detect:** Durbin-Watson (near 2 is fine; near 0 is strong positive autocorrelation), residual ACF, Ljung-Box (Q25).
- **Spurious regression:** two independent random walks regress on each other with high R-squared and significant slope, because both trend (Granger-Newbold).
- **Fixes:** difference the series, model the errors (ARIMA errors, GLS), use HAC (Newey-West) standard errors, add lags, or check cointegration (Q51).
- **Red flag:** high R-squared with very low Durbin-Watson.

**Example:** 500 pairs of independent random walks (length 200): slope "significant" at 5% in 82% of runs (expected 5%), mean R-squared 0.24, mean Durbin-Watson 0.09. Regressing the differences gave p = 0.61 in the one pair printed by the code.

**Code:**
```python
import numpy as np, statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
g = np.random.default_rng(1)
x, y = np.cumsum(g.normal(size=200)), np.cumsum(g.normal(size=200))
X = sm.add_constant(x)
ols = sm.OLS(y, X).fit()
hac = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 8})   # robust SEs
print(durbin_watson(ols.resid), ols.pvalues[1], hac.pvalues[1])   # 0.13, 7e-58, 4e-15
print(sm.OLS(np.diff(y), sm.add_constant(np.diff(x))).fit().pvalues[1])   # differenced: 0.61
# the 500-pair figures in the example: repeat this with a loop over seeds (82% significant)
```
Note: on this pair the HAC p-value is still tiny (about 4e-15, versus 7e-58 for plain OLS). HAC helps with stationary autocorrelated errors but does not cure a regression of one random walk on another; differencing does.

**Follow-ups:**
- *Does autocorrelation bias coefficients?* Not by itself, unless there is a lagged dependent variable with autocorrelated errors.
- *Cointegrated series?* Then the levels regression is meaningful (error-correction model).

**Common mistakes:** Trusting R-squared and p-values on trending data; using Durbin-Watson with lagged dependent variables; differencing without checking for cointegration.

### Q41 ⭐⭐ 🟡 What is forecast combination/ensembling and why does averaging models often beat the best single model?
**Asked at:** Product cos, supply chain
**Say this first (1 line):** Combining forecasts from different models is usually more accurate than a typical single model and often matches or beats the best one, because their errors partly cancel and it protects against picking the wrong model.

**Then explain:**
- **Why it works:** models have different biases and noise; the average has lower variance, as long as the errors are not perfectly correlated.
- **Simple average often wins:** weights estimated from short history are noisy (the "forecast combination puzzle").
- **Options:** simple mean or median, inverse-error weights, stacking on backtest forecasts (Q43), or ensembles of the same model on different windows or seeds.
- **Diversity matters:** combine unlike models (ETS, ARIMA, GBM, seasonal naive), not similar ones.
- **Cost:** more models to run, monitor and explain. The gain is usually a few percent, but reliably.

**Example (simulated trend + weekly season, 14-day test, code below):** MAE of seasonal naive 2.72, 3-week weekday average 2.30, seasonal naive plus drift 2.01. The equal-weight average of the three scored 2.07: better than two of the three members and within 3% of the best one. In hindsight the drift model won, but in advance I would not know that, so the average is the safe pick. It does not always beat the best member; it reliably avoids the worst.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); t = np.arange(200)
y = 50 + 0.2*t + 8*np.sin(2*np.pi*t/7) + rng.normal(0, 2, 200)     # trend + weekly season + noise
tr, te = y[:186], y[186:]; H = 14
drift = (tr[-1] - tr[-29]) / 28                                     # average daily change, last 4 weeks
f_snaive = np.tile(tr[-7:], 2)                                      # same weekday last week
f_3wk = np.tile(tr[-21:].reshape(3, 7).mean(0), 2) + 14*drift       # 3-week weekday average, shifted up for the trend
f_drift = f_snaive + drift*(7 + np.arange(H) // 7 * 7)              # seasonal naive plus drift
f_combo = (f_snaive + f_3wk + f_drift) / 3
mae = lambda f: np.abs(te - f).mean()
print([round(mae(f), 2) for f in (f_snaive, f_3wk, f_drift, f_combo)])   # [2.72, 2.3, 2.01, 2.07]
```

**Follow-ups:**
- *Weighted or simple average?* Start simple; use weights only if backtests show a consistent gain.
- *Does it need to beat each model?* Not on every series; it is the safer choice across thousands of series.

**Common mistakes:** Combining near-identical models; estimating weights in-sample; adding a bad model with high correlation and no benefit; ignoring cost.

### Q42 ⭐⭐ 🔴 What is hierarchical forecasting? Explain bottom-up, top-down and MinT reconciliation, and what to do when store forecasts do not sum to the region forecast.
**Asked at:** Walmart, Amazon, retail GCCs, Europe retail
**Say this first (1 line):** Hierarchical forecasting means forecasting at several levels (SKU, store, region, total) and making the numbers add up; I reconcile with bottom-up, top-down or MinT so that forecasts are coherent.

**Then explain:**
- **Coherence:** children must sum to the parent. Independent forecasts per level rarely do.
- **Bottom-up:** forecast the lowest level, sum up. Keeps detail, but bottom series are noisy.
- **Top-down:** forecast the total, split by historical or forecast proportions. Smooth totals, but loses local patterns.
- **Middle-out:** forecast a middle level, sum up and split down.
- **MinT (optimal reconciliation):** forecast every level, then adjust all forecasts with a projection that minimises total error variance, using the covariance of base forecast errors: tilde y = S (S' W^-1 S)^-1 S' W^-1 y_hat. Needs an estimate of W (shrinkage or diagonal).
- **Plus:** reconciliation usually improves accuracy at most levels, not just consistency.

**Example:** Total forecast 105; three stores forecast 38, 31, 22 (sum 91). Bottom-up gives total 91. OLS reconciliation: 101.5 with stores 41.5/34.5/25.5. MinT with the total's error variance higher (9 vs 4 each) gives 99.0 with stores 40.7/33.7/24.7, which sum exactly to 99.0.

**Code:**
```python
import numpy as np
S = np.array([[1,1,1],[1,0,0],[0,1,0],[0,0,1]], float)   # total + 3 stores
yhat = np.array([105, 38, 31, 22.])
W = np.diag([9., 4, 4, 4]); Wi = np.linalg.inv(W)
P = np.linalg.inv(S.T @ Wi @ S) @ S.T @ Wi
print(S @ P @ yhat)      # [99.   40.67 33.67 24.67]
```

**Follow-ups:**
- *Negative values after reconciliation?* Use non-negative reconciliation or constrain it.
- *Libraries?* `hierarchicalforecast` (Nixtla), `scikit-hts`, R `fable`.

**Common mistakes:** Publishing incoherent numbers; top-down by static shares; full covariance estimates on short history; ignoring that reconciliation can reduce but not remove model error.

### Q43 ⭐ 🟡 How do you tune hyperparameters of a forecasting model (e.g. LightGBM, Prophet) with time-aware CV without overfitting to the backtest?
**Asked at:** Product cos
**Say this first (1 line):** I tune with rolling-origin (expanding window) CV, keep a final untouched holdout period, search a small sensible space, and prefer simple, stable settings over the single best CV score.

**Then explain:**
- **Time-aware CV:** several forecast origins, each trains on the past and tests on the next block (`TimeSeriesSplit` with `test_size` = forecast horizon). Never shuffle.
- **Same as production:** test block length = real horizon; features built per origin with no future data.
- **Avoid overfitting the backtest:** limit trials, use a coarse grid or Bayesian search (Optuna) with early stopping, and check that the top few settings give similar scores (flat optimum).
- **Final holdout:** the latest period is touched only once, after tuning.
- **Prophet:** `prophet.diagnostics.cross_validation(m, initial, period, horizon)` then `performance_metrics`; tune changepoint prior, seasonality prior and seasonality mode. # not executed (Prophet not installed here)
- **Metric:** the business one (WAPE, pinball) averaged across origins and series, plus its spread across folds.

**Example (simulated daily series, code below):** LightGBM, 6 settings (num_leaves 4/15/63, learning rate 0.02/0.1) over 4 rolling folds of 60 days. CV WAPE ranged only 3.50% to 3.81% across all settings; the best (4 leaves, lr 0.02) scored 3.43% on the untouched 120-day holdout. The flat range says that fine tuning matters little here.

**Code:**
```python
import numpy as np, pandas as pd, lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit
rng = np.random.default_rng(0); n = 600; t = np.arange(n)
df = pd.DataFrame({"y": 50 + 0.01*t + 8*np.sin(2*np.pi*t/7) + rng.normal(0, 2, n), "dow": t % 7})   # one daily series
for l in (1, 7, 14): df[f"lag{l}"] = df.y.shift(l)
df["roll7"] = df.y.shift(1).rolling(7).mean()
df = df.dropna().reset_index(drop=True); F = ["lag1", "lag7", "lag14", "roll7", "dow"]
dev, hold = df.iloc[:-120], df.iloc[-120:]                          # last 120 days = untouched final holdout
tscv = TimeSeriesSplit(n_splits=4, test_size=60)
def cv_wape(params):
    s = []
    for a, b in tscv.split(dev):
        m = lgb.LGBMRegressor(**params, n_estimators=200, verbose=-1, random_state=0).fit(dev.iloc[a][F], dev.iloc[a].y)
        s.append(abs(dev.iloc[b].y - m.predict(dev.iloc[b][F])).sum() / dev.iloc[b].y.sum())
    return np.mean(s)
grid = [dict(num_leaves=nl, learning_rate=lr) for nl in (4, 15, 63) for lr in (0.02, 0.1)]
res = [(cv_wape(p), p) for p in grid]                               # CV WAPE 3.50% to 3.81%
best = min(res, key=lambda r: r[0])[1]
m = lgb.LGBMRegressor(**best, n_estimators=200, verbose=-1, random_state=0).fit(dev[F], dev.y)
print(best, abs(hold.y - m.predict(hold[F])).sum() / hold.y.sum())  # holdout touched once: 0.034
```

**Follow-ups:**
- *Expanding or sliding window?* Expanding for stable data, sliding when old data is irrelevant (drift).
- *Many series?* Tune on a sample of series/origins, evaluate on the rest.

**Common mistakes:** Random k-fold; reporting the best CV score as expected performance; giant search spaces; tuning on the final holdout; ignoring variance across folds.

### Q44 ⭐ 🟡 Implement from scratch in NumPy: moving average, simple exponential smoothing, ACF, and seasonal-naive forecast.
**Asked at:** Live-coding rounds, product cos
**Say this first (1 line):** All four are a few lines of NumPy: moving average via cumulative sum, exponential smoothing as a one-line recursion, ACF as lagged covariance divided by variance, and seasonal naive as repeating the last season.

**Then explain:**
- **Moving average:** mean of the last k points; cumulative sum makes it O(n).
- **SES:** level_t = alpha * y_t + (1 - alpha) * level_(t-1); forecast = last level (flat).
- **ACF:** r_k = sum((y_t - mean)(y_(t+k) - mean)) / sum((y_t - mean)^2).
- **Seasonal naive:** forecast for h = value one season (m periods) before.
- Point out edge cases: alpha in (0, 1], k <= n, lags < n.

**Example:** On a 14-point series with period 7: MA(3) starts 4, 5, 6; SES(0.3) final level 7.174; ACF lags 0-3: 1, 0.196, 0.179, -0.375 (matches statsmodels); seasonal naive 9 steps ahead repeats the last week then the first two days.

**Code:**
```python
import numpy as np
def sma(x, k):
    c = np.cumsum(np.insert(x, 0, 0.)); return (c[k:] - c[:-k]) / k
def ses(x, a):
    l = x[0]
    for v in x[1:]: l = a*v + (1 - a)*l
    return l
def acf(x, nl):
    x = x - x.mean(); d = (x*x).sum()
    return np.array([(x[:len(x)-k] * x[k:]).sum() / d for k in range(nl + 1)])
def snaive(x, h, m):
    return np.array([x[len(x) - m + (i % m)] for i in range(h)])
s = np.array([3,5,4,6,8,7,9,3,5,4,6,8,7,9.])
print(sma(s,3)[:3], ses(s,.3), np.round(acf(s,3),3), snaive(s,9,7))
```
Output: `[4. 5. 6.] 7.1741772874595995 [ 1. 0.196 0.179 -0.375] [3. 5. 4. 6. 8. 7. 9. 3. 5.]`; ACF and SES also match statsmodels.

**Follow-ups:**
- *Why divide by the lag-0 sum even at high lags?* The standard estimator; keeps the ACF a valid positive-definite sequence.
- *Complexity?* MA O(n) with cumsum, SES O(n), ACF O(n * nlags).

**Common mistakes:** Off-by-one in the window; using np.corrcoef per lag (different estimator); forgetting seasonal naive wraps around for h > m; initialising SES badly.

### Q45 ⭐ 🟡 AI-era: review this LLM-generated forecasting code. Spot leakage (shuffled split, scaler fit on all data, future-rolling features) and other bugs.
**Asked at:** Product cos, 2025-26 code-review rounds
**Say this first (1 line):** The code leaks the future three ways (centered rolling feature, scaler fit on all data, shuffled split), so its error looks great and will not hold in production; I would fix the order, the feature shift and the fit scope, and compare to a seasonal naive baseline.

**Buggy snippet (as an LLM might write it):**
```python
import numpy as np, pandas as pd
from lightgbm import LGBMRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0); n = 400; t = np.arange(n)           # synthetic trend + weekly season (setup so it runs)
df = pd.DataFrame({"date": pd.date_range("2023-01-01", periods=n)})
df["y"] = 50 + 0.2*t + 8*np.sin(2*np.pi*t/7) + rng.normal(0, 2, n); df["dow"] = df.date.dt.dayofweek
mape = lambda a, b: np.mean(np.abs(np.asarray(a) - np.asarray(b)) / np.asarray(a)) * 100
df["lag1"] = df.y.shift(1)
df["roll7"] = df.y.rolling(7, center=True).mean()                 # BUG 1
d = df.dropna()
X = StandardScaler().fit_transform(d[["lag1", "roll7", "dow"]])   # BUG 2
Xtr, Xte, ytr, yte = train_test_split(X, d.y, test_size=0.2, shuffle=True, random_state=0)   # BUG 3
m = LGBMRegressor(verbose=-1).fit(Xtr, ytr)
print(mape(yte, m.predict(Xte)))                                  # 2.9
```

**Bugs:**
- **Centered rolling mean** uses 3 future points; the target is almost inside the feature. Use `shift(1).rolling(7)`.
- **Scaler fit on all data** leaks test statistics; fit on train only (and trees do not need scaling at all).
- **Shuffled split:** test points sit between training points in time; use a time split or rolling-origin CV.
- **Other issues:** no baseline (seasonal naive), single split, MAPE on small values, no check of horizon (lag1 is not available when forecasting h > 1), trees cannot extrapolate trend (difference the target or add a trend model), no random seed.

**Fixed:**
```python
# continuation of the buggy snippet: same imports, `df`, `mape`
F = ["lag1", "roll7", "dow"]
df["lag1"] = df.y.shift(1)
df["roll7"] = df.y.shift(1).rolling(7).mean()
df["lag7"] = df.y.shift(7)
d = df.dropna(); cut = int(len(d) * .8)
tr, te = d.iloc[:cut], d.iloc[cut:]
m = LGBMRegressor(random_state=0, verbose=-1).fit(tr[F], tr.y)
print(mape(te.y, m.predict(te[F])), mape(te.y, te.lag7))          # fixed 7.7 | seasonal naive 2.0: still loses
# trees cannot extrapolate the trend: predict the change versus last week instead of the level
m2 = LGBMRegressor(random_state=0, verbose=-1).fit(tr[F + ["lag7"]], tr.y - tr.lag7)
print(mape(te.y, m2.predict(te[F + ["lag7"]]) + te.lag7))         # 1.7: now beats seasonal naive
```

**Example (run on a synthetic trend + weekly seasonal series):** buggy MAPE 2.9%; fixed 7.7%; seasonal naive 2.0%. The leak made the model look about 2.6x better than it is, and the honestly fixed model is far worse than the baseline because the trees cannot extrapolate the trend. Predicting the change versus last week (the differenced target) gives 1.7%, which finally beats seasonal naive.

**Follow-ups:**
- *How would you review LLM-written forecasting code in general?* Check feature timing, split logic, fit scope of transforms, baselines, horizon, metrics.
- *Quick leakage test?* Shift the target forward randomly or drop a suspicious feature and see if accuracy collapses.

**Common mistakes:** Trusting a high score; fixing only one leak; not comparing to naive; assuming a random split is fine for "stationary-looking" data.

### Q46 ⭐ 🔴 Which probabilistic forecast metrics do you use (pinball loss, CRPS, coverage, interval width) and how do you evaluate quantile forecasts?
**Asked at:** Amazon-style, Europe retail, senior roles
**Say this first (1 line):** I score quantile forecasts with pinball loss (CRPS across all quantiles) for overall quality, and check calibration with coverage and sharpness with interval width: good forecasts are calibrated and as narrow as possible.

**Then explain:**
- **Pinball loss (tau):** tau * max(y - q, 0) + (1 - tau) * max(q - y, 0); a proper scoring rule, minimised by the true quantile.
- **CRPS:** average pinball over all quantile levels (times 2); score for the whole predictive distribution; reduces to MAE for a point forecast. Lower is better.
- **Coverage:** share of actuals inside the interval; 80% interval should cover about 80%.
- **Width (sharpness):** narrower is better, but only if calibrated; a huge interval has perfect coverage and is useless.
- **Interval score:** width plus penalty for misses (Winkler score), combining both.
- **Per horizon and per segment,** and via rolling-origin backtests.

**Example:** Actuals from Normal(100, 10), forecasts with the right, too small (5) and too large (20) spread. Coverage of 80% interval: 0.81 / 0.47 / 0.99; width 25.6 / 12.8 / 51.3; mean pinball over the 0.1 to 0.9 quantiles 3.07 / 3.28 / 3.55; Gaussian CRPS 5.62 (sd 10) vs 6.08 (sd 5) vs 6.54 (sd 20) from 20,000 draws. The calibrated forecast wins on both.

**Code:**
```python
import numpy as np
from scipy.stats import norm
def pinball(y, q, t):
    d = y - q; return np.mean(np.maximum(t*d, (t-1)*d))
def crps_gauss(y, mu, s):
    z = (y - mu)/s
    return (s*(z*(2*norm.cdf(z) - 1) + 2*norm.pdf(z) - 1/np.sqrt(np.pi))).mean()
y = np.random.default_rng(0).normal(100, 10, 20000)           # actuals ~ N(100, 10)
for s in (10, 5, 20):                                          # right, too narrow, too wide
    lo, hi = 100 - norm.ppf(.9)*s, 100 + norm.ppf(.9)*s        # 80% interval
    pb = np.mean([pinball(y, 100 + norm.ppf(t)*s, t) for t in np.arange(.1, .95, .1)])
    print(s, np.mean((y >= lo) & (y <= hi)).round(2), round(hi - lo, 1), pb.round(2), crps_gauss(y, 100, s).round(2))
```

**Follow-ups:**
- *Why not just coverage?* It can be gamed by wide intervals; pair it with width or pinball.
- *Scaled version for many series?* Divide by a naive forecast's score or by the series scale (as in M5 WSPL).

**Common mistakes:** Reporting only coverage; evaluating in-sample; averaging unscaled losses so big series dominate; quantile crossing left uncorrected.

### Q47 ⭐ 🔴 What is conformal prediction for time series, and why do standard conformal guarantees break under autocorrelation?
**Asked at:** Senior / research-leaning roles
**Say this first (1 line):** Conformal prediction wraps any point forecaster and uses past errors on held-out data to size the interval, with a coverage guarantee that needs exchangeable errors; time series break that, so I use rolling or adaptive versions.

**Then explain:**
- **Split conformal:** compute absolute errors on a calibration set; the interval is forecast +/- the (1 - alpha) quantile (with a small finite-sample correction). Model-agnostic and distribution-free.
- **The guarantee:** coverage of at least 1 - alpha on average, if calibration and test errors are exchangeable (like draws from the same bag).
- **Why time series break it:** errors are autocorrelated and change over time (volatility clusters, drift, seasonality, horizon effects), so past errors are not a fair sample of future ones. Coverage is only right on average; it can be far off in specific periods.
- **Fixes:** rolling/recent calibration window, horizon-specific residuals, scale by local volatility (normalised conformal), **adaptive conformal inference (ACI)**, which nudges alpha up or down after each miss or hit, and block-based or EnbPI-style methods.
- Check coverage by period and horizon, not only overall.

**Example (simulated, code below):** forecast of 0; errors with noise sd 1 in calm periods and 3 in volatile ones (alternating 500-point blocks), 90% target, test on points 1000-1999. Static split conformal (calibrated once on the first 1000 points) covered 0.87 overall, but by 250-point block 1.00 / 1.00 / 0.75 / 0.74: far too wide when calm, too narrow when volatile. A 250-point rolling window gave 0.87 overall with blocks 0.99 / 0.88 / 0.72 / 0.89 (it lags each regime change). ACI gave 0.90 overall with blocks 0.94 / 0.90 / 0.85 / 0.89: it recovers the target on average and adapts faster, though a volatile block can still under-cover.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0); n = 2000
sd = np.where((np.arange(n) // 500) % 2 == 0, 1, 3); err = rng.normal(0, sd)   # forecast error of a model that predicts 0
alpha, g, a_t, hits = .1, .02, .1, []
for i in range(1000, n):
    q = np.quantile(np.abs(err[:i][-1000:]), min(max(1 - a_t, 0), 1))
    miss = abs(err[i]) > q
    hits.append(not miss); a_t += g * (alpha - miss)   # ACI update
h = np.array(hits); print(h.mean(), [h[i:i+250].mean().round(2) for i in range(0, 1000, 250)])   # 0.897 [0.94, 0.9, 0.85, 0.89]
# static baseline: q = np.quantile(np.abs(err[:1000]), .9) held fixed; rolling: use err[i-250:i] and no alpha update
```

**Follow-ups:**
- *Does it fix a bad model?* No: it gives valid coverage but wide intervals if the model is poor.
- *Multi-step horizons?* Calibrate separately for each h.

**Common mistakes:** Assuming the guarantee holds out of the box; random split of calibration data; only checking overall coverage; calibrating on in-sample residuals.

### Q48 ⭐ 🔴 Compare modern deep forecasters: DeepAR, N-BEATS, Temporal Fusion Transformer, PatchTST. When are they worth it?
**Asked at:** Senior DS/MLE, product cos
**Say this first (1 line):** DeepAR, N-BEATS, TFT and PatchTST are deep forecasters for many series with covariates; they are worth it with lots of related data, rich covariates and a need for probabilistic or multi-horizon outputs, and otherwise a tuned GBM or ETS is usually enough.

**Then explain:**

| Model | Idea | Strength | Caveat |
|---|---|---|---|
| DeepAR | Autoregressive RNN across many series, outputs a distribution (e.g. negative binomial) | Probabilistic, global, handles scale and count data | Recursive sampling, tuning |
| N-BEATS | Stacks of fully-connected blocks with backward/forward residual links on a lookback window | Strong univariate (reported to beat the M4 winning entry), interpretable variant | Weak on covariates (N-BEATSx adds them) |
| TFT | LSTM + attention, variable selection, static and known-future covariates, quantile outputs | Multi-horizon, interpretable attention, handles known/unknown inputs | Heavy, many hyperparameters |
| PatchTST | Transformer on patches of the series, channel-independent | Long-horizon, efficient | Benchmarks sensitive to settings; simple linear models can match it |

- **Worth it when:** thousands of related series, long histories, rich covariates, need probabilistic or long-horizon output, team can maintain it.
- **Not worth it when:** few series, short history, strong seasonality a baseline already captures; cost, latency and explainability matter.
- **Always compare** with seasonal naive, ETS and global LightGBM, same backtest, several seeds.

**Example:** Retail with 50,000 SKU-store series, promos, prices, holidays and weather: TFT or LightGBM global. Start with LightGBM; try TFT if gains over it persist across seeds and horizons.

**Follow-ups:**
- *Why do some transformer forecasters lose to linear models?* Reported in the "Are Transformers Effective for Time Series Forecasting?" line of work; noisy benchmarks and weak inductive bias for temporal order.
- *Libraries?* GluonTS, PyTorch Forecasting, Darts, NeuralForecast. # not executed

**Common mistakes:** Picking the architecture by hype; no tuned GBM baseline; one seed; ignoring training and serving cost; claiming interpretability from attention weights alone.

### Q49 ⭐ 🔴 AI-era: What are time-series foundation models (Chronos, TimesFM, Moirai)? When do you use zero-shot vs fine-tune vs a tuned LightGBM?
**Asked at:** 2025-26 product cos, senior MLE
**Say this first (1 line):** Time-series foundation models are big pre-trained forecasters that give a forecast out of the box with no per-series training; I benchmark them zero-shot against seasonal naive and a tuned LightGBM, and fine-tune only if the gap justifies the cost.

**Then explain:**
- **What they are:** Chronos (Amazon; tokenises values and uses a language-model architecture, probabilistic output), TimesFM (Google; decoder-only transformer on patches), Moirai (Salesforce; masked encoder, handles multivariate and varying frequencies). All pre-trained on large collections of series.
- **Zero-shot:** good when history is short, many series, no time to build a pipeline, or as a strong baseline; weak when covariates (price, promo, holidays) drive demand because most models use only the series.
- **Fine-tune:** when you have domain data and zero-shot is close but not good enough.
- **Tuned LightGBM wins when:** rich covariates, lots of history, business-specific effects, cheap and fast inference needed, interpretability.
- **Decision:** evaluate all three in the same rolling-origin backtest; consider cost, latency, privacy (self-hosted vs API), and benchmark-leakage risk (pre-training data may overlap test periods).
- **Practical:** use as a candidate in an ensemble; foundation model + GBM on residuals or covariates is a common hybrid.

**Example:** New markets with 8 weeks of history and no promo calendar: a zero-shot foundation model likely beats a GBM trained on 8 points. A mature category with years of history, promos and price: tuned global LightGBM with covariates.

**Code:**
```python
# not executed: the chronos package (and its model download) is not available here; API per the chronos-forecasting docs
from chronos import ChronosPipeline
pipe = ChronosPipeline.from_pretrained("amazon/chronos-t5-small")
samples = pipe.predict(context_tensor, prediction_length=12)   # (series, samples, horizon)
```

**Follow-ups:**
- *Risks?* Pre-training leakage in benchmarks, no covariates, inference cost, drift handling.
- *How to evaluate fairly?* Hold out recent periods after the model's data cut-off.

**Common mistakes:** Adopting without a baseline comparison; ignoring covariates; assuming zero-shot is magic; leakage through public benchmark datasets.

### Q50 ⭐ 🔴 AI-era: Can you prompt an LLM to forecast numbers? What works, what fails, and how would you evaluate it?
**Asked at:** 2025-26 GenAI-flavoured DS loops
**Say this first (1 line):** You can prompt an LLM to extrapolate a short, clean series, but it is unreliable for real forecasting; it is best used to explain, extract features or call a real forecasting tool, and I would evaluate it like any model against naive baselines.

**Then explain:**
- **What works:** short simple patterns, pattern descriptions, reading context (news, events) into features, writing code that calls a forecasting library, explaining results, and tool use (LLM orchestrates a model).
- **What fails:** arithmetic and exact numeric consistency, long series (token limits, number tokenisation), seasonality across many cycles, calibrated uncertainty, reproducibility (sampling), and cost at scale.
- **Evaluation:** same rolling-origin backtest, same metrics (MASE, WAPE, pinball), compared to seasonal naive, ETS and LightGBM; many series and origins, repeated runs for variability; check for memorisation of public datasets.
- **Prompt design:** give structured context, ask for quantiles, set temperature low, validate output format.
- **Better pattern:** LLM as agent that selects and runs a forecasting tool (or a foundation model, Q49), and a human reviews.

**Example (general behaviour, not measured by me here):** Given 24 monthly values, an LLM can often continue the trend plausibly. On hundreds of daily points with weekly and yearly patterns, outputs tend to be smoothed or repeated and intervals poorly calibrated, so I would expect seasonal naive to be a hard baseline to beat; the backtest decides.

**Follow-ups:**
- *Is there evidence?* Studies such as LLMTime ("Large Language Models Are Zero-Shot Time Series Forecasters") show decent zero-shot results on some benchmarks, but strong baselines remain competitive; results depend heavily on data and prompt.
- *Production safe?* Only with guardrails, fallbacks and monitoring.

**Common mistakes:** Judging by one eyeballed example; no baseline; trusting LLM arithmetic; evaluating on data the LLM may have seen in pre-training; ignoring cost and latency.

### Q51 ⭐ 🔴 Explain VAR, Granger causality and cointegration. When is each appropriate?
**Asked at:** Banks, quant-flavoured, consulting
**Say this first (1 line):** VAR models several series together, each as a function of the lags of all of them; Granger causality tests whether one series' past helps predict another; cointegration says non-stationary series share a long-run relationship, handled with an error-correction model.

**Then explain:**
- **VAR(p):** each variable regressed on p lags of every variable. Use for interrelated stationary series (e.g. sales, price, ad spend) and joint forecasts and impulse responses. Pick p by AIC/BIC.
- **Granger causality:** x Granger-causes y if past x improves the prediction of y beyond past y. It is predictive, not true causation, and depends on the variables and lags included.
- **Cointegration:** two I(1) series (random-walk-like) whose combination is stationary (e.g. spot and futures price). Differencing loses the long-run link; use a VECM (Engle-Granger or Johansen tests).
- **When:** stationary related series: VAR; levels non-stationary but cointegrated: VECM; non-stationary and not cointegrated: VAR on differences; checking "does x lead y": Granger.
- **Check:** unit-root tests (ADF) first, residual autocorrelation after fitting.

**Example (simulated, code below):** y depends on lagged x; Granger test x to y: p about 6e-48; y to x: p = 0.89 (no effect); VAR selected 1 lag. Cointegration test on two series built from a common random walk: p < 0.001; on two independent random walks: p = 0.06 (correctly not rejected at 5%, though borderline).

**Code:**
```python
import numpy as np, pandas as pd
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import grangercausalitytests, coint
rng = np.random.default_rng(0); n = 500; x = np.zeros(n); y = np.zeros(n)
for t in range(1, n):
    x[t] = 0.5*x[t-1] + rng.normal(); y[t] = 0.4*y[t-1] + 0.6*x[t-1] + rng.normal()   # x drives y
df = pd.DataFrame({"y": y, "x": x})
res = VAR(df[["y", "x"]]).fit(maxlags=4, ic="aic")          # picked 1 lag
gc = grangercausalitytests(df[["y", "x"]], maxlag=2, verbose=False)   # does x help predict y
print(gc[1][0]["ssr_ftest"][1])                              # about 6e-48 (reverse direction: 0.89)
w = np.cumsum(rng.normal(size=500)); a, b = w + rng.normal(size=500), 2*w + rng.normal(size=500)   # common random walk
print(coint(a, b)[1])                                        # Engle-Granger p-value, about 0
```

**Follow-ups:**
- *Does Granger mean causation?* No: a confounder or common driver can create it.
- *Why not VAR on levels of non-stationary data?* Spurious results (Q40) unless cointegrated.

**Common mistakes:** Granger tests on non-stationary data; reading Granger as causal; too many lags with short data; differencing cointegrated series without an error-correction term.

### Q52 ⭐ 🔴 What is a state-space model / Kalman filter and how does it relate to exponential smoothing and ARIMA?
**Asked at:** Senior, quant-flavoured, research roles
**Say this first (1 line):** A state-space model describes a hidden state (level, trend, seasonality) evolving over time plus noisy observations, and the Kalman filter updates the state estimate with each new data point; ETS and ARIMA are special cases of it.

**Then explain:**
- **Two equations:** state (x_t = F x_(t-1) + noise) and observation (y_t = H x_t + noise).
- **Kalman filter:** predict the state, then correct it by gain K times the forecast error, where K balances state noise against observation noise. Gives forecasts, intervals and handles missing data naturally.
- **Local level model:** state is a random-walk level; the steady-state Kalman filter is exactly simple exponential smoothing with alpha = K.
- **ETS:** exponential smoothing methods are the state-space forms (innovations form) with a single error source; ARIMA also has a state-space representation.
- **Why use it:** missing values, time-varying parameters, regression effects, structural time series (trend, seasonal, cycle), Bayesian structural models (Q54).
- **Fit:** maximum likelihood via the Kalman filter (statsmodels `UnobservedComponents`, `SARIMAX`, `ETSModel`).

**Example:** Local level with state variance 1 and observation variance 4: the steady-state gain is K = 0.39. Running a Kalman filter and SES with alpha = 0.39 over the same 300 simulated points gave the identical final level (-12.18 in the code below). Fitting by maximum likelihood (statsmodels `UnobservedComponents`) estimated variances 4.02 (observation) and 1.38 (level), near the true 4 and 1.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
y = np.cumsum(rng.normal(0, 1, 300)) + rng.normal(0, 2, 300)   # random-walk level (var 1) + observation noise (var 4)
q, r, P, m = 1.0, 4.0, 1e3, y[0]
for v in y:
    P += q; K = P / (P + r)       # predict, then gain
    m += K * (v - m); P *= (1 - K)   # update level and variance
l = y[0]
for v in y: l = K*v + (1 - K)*l   # SES with alpha = settled K
print(K, m, l)                    # K = 0.39; both levels -12.18
```

**Follow-ups:**
- *Why does K settle?* P converges to a fixed point for constant noise variances.
- *Nonlinear/non-Gaussian?* Extended/unscented Kalman or particle filters.

**Common mistakes:** Thinking the Kalman filter is only for tracking; not knowing SES is a special case; poorly initialised state variance; ignoring the noise-ratio meaning of alpha.

### Q53 ⭐ 🔴 What is GARCH / volatility modelling and when do you model variance instead of the mean?
**Asked at:** Banks, fintech, trading-adjacent
**Say this first (1 line):** GARCH models how volatility (the variance of returns) changes over time and clusters; I use it when the spread of outcomes matters, such as risk (VaR), option pricing or position sizing, and the average return is hard to predict.

**Then explain:**
- **Volatility clustering:** big moves follow big moves. Returns look uncorrelated, but squared returns are autocorrelated.
- **GARCH(1,1):** sigma_t^2 = omega + alpha * r_(t-1)^2 + beta * sigma_(t-1)^2. Alpha is the reaction to the latest shock, beta is persistence; alpha + beta < 1 for stationarity (near 1 means long memory).
- **When variance, not mean:** financial returns, risk limits, interval widths that change over time (heteroscedastic forecast errors), demand series with volatile periods.
- **Test:** Ljung-Box on squared residuals, or the ARCH-LM test.
- **Extensions:** EGARCH/GJR (leverage: bad news raises volatility more), t-distributed errors for fat tails, realised-volatility models.
- **Use:** forecast sigma, then compute intervals, VaR or scale conformal bands (Q47).

**Example:** Simulated GARCH(1,1) with omega 0.1, alpha 0.1, beta 0.85 (3,000 points). Ljung-Box (10 lags) on returns p = 0.41 (no mean pattern) but on squared returns p about 9e-49 (clear ARCH effect). The maximum-likelihood fit below recovered omega 0.071, alpha 0.087, beta 0.877 (persistence 0.96, close to the true 0.95; omega is the least well pinned down).

**Code:**
```python
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(0); N = 3000; h = np.empty(N); r = np.empty(N); h[0] = 1
r[0] = rng.normal() * np.sqrt(h[0])
for i in range(1, N):             # simulate GARCH(1,1): omega 0.1, alpha 0.1, beta 0.85
    h[i] = 0.1 + 0.1*r[i-1]**2 + 0.85*h[i-1]; r[i] = rng.normal() * np.sqrt(h[i])
def nll(p):                       # r: return series
    o, a, b = p
    if o <= 0 or a < 0 or b < 0 or a + b >= .999: return 1e10
    h = np.empty(len(r)); h[0] = r.var()
    for i in range(1, len(r)): h[i] = o + a*r[i-1]**2 + b*h[i-1]
    return .5*np.sum(np.log(h) + r**2/h)
fit = minimize(nll, [.05, .05, .8], method="Nelder-Mead")   # in practice use the arch package
print(fit.x)                                                # about [0.071, 0.087, 0.877]
```

**Follow-ups:**
- *GARCH vs stochastic volatility?* GARCH conditional variance is deterministic given the past; SV has its own noise.
- *Why not ARMA for the mean?* The mean model can still be ARMA; GARCH models the residual variance.

**Common mistakes:** Applying ARIMA intervals with constant variance to volatile data; ignoring fat tails; reading alpha + beta near 1 without thinking about persistence; skipping ARCH tests.

### Q54 ⭐ 🔴 How would you use Bayesian structural time series / counterfactual forecasting to estimate the impact of an intervention (CausalImpact)?
**Asked at:** Product cos, experimentation teams
**Say this first (1 line):** I model the treated series before the intervention using control series that were not affected (a Bayesian structural time-series model, as in CausalImpact), predict what would have happened without it, and call the gap the effect.

**Then explain:**
- **Idea:** pre-period: learn how the target relates to controls (and its own trend/seasonality). Post-period: forecast the counterfactual, subtract from the actual; cumulative effect with credible intervals.
- **Model:** structural time series (local level/trend, seasonality) with regression on control series and spike-and-slab priors; fit by Kalman filter / MCMC (CausalImpact in R/Python).
- **Assumptions:** controls are not affected by the intervention; the relationship between target and controls is stable after the intervention; no other change at the same time; enough pre-period data.
- **Validation:** placebo tests (fake intervention date in the pre-period, effect should be about 0), different control sets, pre-period fit quality.
- **Use when:** you cannot randomise (market-wide launch, regional campaign, pricing change); otherwise run an experiment (geo experiment is better).
- **Alternatives:** difference-in-differences, synthetic control.

**Example:** Target built from three random-walk controls, a true lift of +5 added after day 100. A regression on controls fitted on the 100 pre-days gave an average post effect of 4.74 (true 5.0); a placebo date at day 70 gave -0.24. A naive 95% interval from the post-period spread (4.54 to 4.95) ignored parameter uncertainty and autocorrelation and missed the truth, which is why the full Bayesian model with proper uncertainty is used.

**Code:**
```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(0); controls = np.cumsum(rng.normal(size=(200, 3)), axis=0)   # 3 random-walk controls
y = controls @ [1, .5, .3] + rng.normal(0, 1, 200); y[100:] += 5                         # true lift +5 from day 100
pre = 100
X = sm.add_constant(controls)
m = sm.OLS(y[:pre], X[:pre]).fit()
effect = y[pre:] - m.predict(X[pre:])        # pointwise effect; avg = effect.mean() = 4.74
placebo = sm.OLS(y[:70], X[:70]).fit(); print(effect.mean(), (y[70:100] - placebo.predict(X[70:100])).mean())   # 4.74, -0.24
# CausalImpact (pycausalimpact / tfcausalimpact) adds the BSTS model and intervals  # not executed
```

**Follow-ups:**
- *What if controls are also affected?* Spillover biases the effect; choose unaffected controls or geographies.
- *Why not before/after?* Trend, seasonality and external events confound it.

**Common mistakes:** Using controls that are affected by the intervention; short pre-period; no placebo test; reporting point estimates without intervals; confusing statistical with practical significance.
