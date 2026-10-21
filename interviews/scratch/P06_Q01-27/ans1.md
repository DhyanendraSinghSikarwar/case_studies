@@Q1
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

@@Q2
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
from statsmodels.tsa.seasonal import seasonal_decompose
d = seasonal_decompose(series, model="multiplicative", period=12)   # series: monthly pd.Series
d.trend, d.seasonal, d.resid
# On my synthetic multiplicative series the multiplicative fit gave seasonal factors 0.8-1.2 and residual sd 0.01;
# the additive series gave seasonal range about -10.6 to +9.9.
```

**Follow-ups:**
- *Why STL over classical decomposition?* STL is robust to outliers, allows seasonality to evolve, and handles any period.
- *Multiplicative with zeros?* Cannot be used (zeros/negatives); use additive or log1p.

**Common mistakes:** Calling a cycle "seasonality"; using multiplicative on data with zeros; treating decomposition as a forecast (it is a description).

@@Q3
**Say this first (1 line):** Random splits let the model train on the future and test on the past, which leaks information and overstates accuracy; I split by time so train always comes before test.

**Then explain:**
- **Leakage:** neighbouring days are correlated, so a random test point has its yesterday and tomorrow in training. The model effectively interpolates.
- **Wrong target:** in production you always predict forward, so evaluation must mimic that.
- **Correct split:** train on the past, validate on the next block, test on the latest block (e.g. train to Dec, validate Jan-Mar, test Apr-Jun).
- **Better:** walk-forward / rolling-origin validation with several folds (Q9), so one lucky or unlucky period does not decide.
- **Gap:** if features use lags or rolling windows, or the label is a future window, add a gap so train labels do not overlap with test inputs.
- Preprocessing (scaling, imputation, target encoding) must be fit on the train part only.

**Example:** Sales has a growing trend. A random 80/20 split shows MAPE 5%; the honest "train to Sep, test Oct-Dec" shows 14% because the trend and the holiday peak were never seen.

**Follow-ups:**
- *Multiple series (panel)?* Split by time cut-off across all series. Splitting by series answers a different question (cold start, Q29).
- *Is shuffling ever fine?* Only for models on lag features built per row if you still respect the cut-off, but a time cut-off is simpler and safer.

**Common mistakes:** `train_test_split` with defaults; scaling on the full data; tuning on the test block repeatedly; ignoring gap when the target is a 7-day sum.

@@Q4
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

@@Q5
**Say this first (1 line):** I always start with naive, seasonal naive and a moving average, because they are cheap, hard to beat, and any fancy model must prove it is better than them.

**Then explain:**
- **Naive:** tomorrow = today. Hard to beat for random-walk-like series (stocks).
- **Seasonal naive:** value = same period last cycle (same weekday last week, same month last year). The strongest simple baseline for seasonal data.
- **Moving average / mean:** average of the last k points. Good for stable, noisy series.
- **Why they matter:** (1) a sanity floor, (2) the denominator of MASE (Q11), (3) tell me how much is predictable at all, (4) often serve as a production fallback.
- If a complex model only gives 1-2% over seasonal naive, it is probably not worth deploying.

**Example (monthly synthetic data, 12-month test):** naive MAE 14.1, 12-month average 8.7, seasonal naive 6.6, Holt-Winters 1.9. The model clearly earns its place here.

**Code:**
```python
import numpy as np
naive   = np.repeat(train.iloc[-1], 12)
snaive  = train.iloc[-12:].values                 # same month last year
ma      = np.repeat(train.iloc[-12:].mean(), 12)
mae = lambda a, b: np.mean(np.abs(np.asarray(a) - np.asarray(b)))
print(mae(test, naive), mae(test, snaive), mae(test, ma))
```

**Follow-ups:**
- *Which is best for weekly retail data?* Seasonal naive with m = 7 (or 52 for yearly weekly data).
- *Drift method?* Naive plus average historical change; good for trending series.

**Common mistakes:** Comparing a model against nothing; using plain naive on strongly seasonal data; computing the baseline on a different window than the model.

@@Q6
**Say this first (1 line):** Differencing replaces each value with its change from the previous one (y_t - y_{t-1}) to remove trend; I pick the smallest d that makes the series stationary, and over-differencing adds noise and negative autocorrelation.

**Then explain:**
- **d = 1** removes a linear / stochastic trend; **d = 2** removes a trend in the trend (rare). **Seasonal difference** y_t - y_{t-m} removes seasonality.
- **How to choose:** plot; ADF/KPSS after each difference (`ndiffs` in pmdarima does this); look for a slowly decaying ACF (needs more differencing).
- **Rule of thumb:** the correct d gives the lowest variance of the differenced series.
- **Over-differencing signs:** variance goes up, lag-1 ACF is strongly negative (about -0.5), and the model needs MA terms that sit near -1 (non-invertible).
- Forecasts on differenced data must be integrated back (cumsum plus last observed value) to get the original scale.

**Example:** Random walk of 500 points: variance of the level is 79; after one difference it is 1.05 (right); after two it is 2.04 and lag-1 ACF is -0.49 (over-differenced; noise variance has doubled).

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

@@Q7
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

**Example (simulated, n = 2000):** AR(1) with phi = 0.7: ACF 0.68, 0.48, 0.33, 0.22 (decaying), PACF 0.68, 0.02, -0.01 (cut-off at 1). MA(1) with theta = 0.7: ACF 0.48 then about 0, PACF 0.48, -0.30, 0.14 (decaying).

**Code:**
```python
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.stattools import acf, pacf
import numpy as np
rng = np.random.default_rng(0)
ar = ArmaProcess([1, -0.7], [1]).generate_sample(2000, distrvs=rng.normal)
print(acf(ar, nlags=4)[1:].round(2), pacf(ar, nlags=4)[1:].round(2))
```

**Follow-ups:**
- *Seasonal spikes at 12, 24?* Seasonal AR/MA terms (P, Q) in SARIMA (Q20).
- *ACF decays very slowly?* Non-stationary; difference first.

**Common mistakes:** Reading ACF/PACF on a non-stationary series; swapping which one cuts off for AR vs MA; over-trusting borderline spikes; ignoring that `statsmodels` PACF defaults can differ (use `method="ywm"`/`"ols"` consciously).

@@Q8
**Say this first (1 line):** ARIMA(p,d,q) forecasts a series from its own past values (p AR terms), past forecast errors (q MA terms), after differencing d times to make it stationary; I choose orders by lowest AIC/BIC over a small grid, then check residuals.

**Then explain:**
- **AR(p):** y_t depends on the last p values. **MA(q):** y_t depends on the last q shocks. **I(d):** difference d times.
- **Selection:** d from unit-root tests, p/q from ACF/PACF as a start, then a grid search by AIC (better for forecasting) or BIC (penalises complexity more, prefers parsimonious). `auto_arima` automates this (stepwise search).
- **Do not** compare AIC across different d (different data).
- **Assumptions:** linear structure, stationarity after differencing, constant variance, residuals are white noise.
- **Limits:** univariate by default, one series at a time (slow for thousands), weak on long/multiple seasonality, no easy handling of promotions (ARIMAX helps), poor at non-linear effects, intervals assume normal errors.

**Example (monthly synthetic, trend + seasonality):** plain ARIMA(1,1,0) AIC 662.9, ARIMA(2,1,2) AIC 600.9 (it fakes the seasonal wave with complex roots), SARIMA(0,1,1)(0,1,1,12) AIC 491.1 and MAE 1.87 on the 12-month test: seasonal structure beats extra p/q.

**Code:**
```python
from statsmodels.tsa.arima.model import ARIMA
for order in [(1,1,0), (0,1,1), (1,1,1), (2,1,2)]:
    m = ARIMA(train, order=order).fit()
    print(order, round(m.aic, 1), round(m.bic, 1))
fc = ARIMA(train, order=(1,1,1)).fit().get_forecast(12)
print(fc.summary_frame(alpha=0.2).head())    # forecast + 80% interval
```

**Follow-ups:**
- *AIC vs time-series CV?* AIC is in-sample; for forecasting I prefer out-of-sample backtests when time allows.
- *ARIMA vs GBM?* ARIMA for a few clean series with little data; GBM/global model when many series and rich features (Q12).

**Common mistakes:** Letting auto_arima run blindly on seasonal data without `seasonal=True, m=`; skipping residual checks; comparing AIC across different d; assuming ARIMA handles holidays.
