# Book 9 — Basic ML + AI Tools for Analysts | Part 7: Forecasting Basics (Moving Average, Trend, Seasonality) 🟡

**Target:** 38 questions | **Actual:** 45 questions
**Scope:** forecasting basics for analysts: time series features, moving averages, trend lines, seasonal indices, exponential smoothing, naive baselines, error metrics, time-based validation, and short statsmodels/pandas tasks.

### Q1 ⭐⭐⭐ 🟢 What is a time series, and how does forecasting a time series differ from predicting a value for ordinary independent rows?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Explain trend, seasonality and random noise in a monthly sales series to a non-technical manager.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is a moving average, and why do analysts use it on sales or attendance data?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is a naive forecast, and why should every forecasting model be compared with one?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How would you explain to a manager that a forecast is an estimate with a range and not a promise?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What are MAE, RMSE and MAPE for a forecast, and which one would you show to a sales head?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 Monthly sales for six months are given. What is the 3-month simple moving average forecast for July?
Month: Jan 120, Feb 130, Mar 125, Apr 140, May 150, Jun 145 (units).
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Why can you not use a random train/test split for a forecasting problem, and how do you split instead?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Actual and forecast values for three months are given. Calculate MAE, RMSE and MAPE.
Actual: 100, 110, 120. Forecast: 105, 100, 130.
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 You are asked for a 3-month versus a 12-month moving average on monthly sales. What is the trade-off in choosing the window size?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 A pandas column `sales` holds daily sales. What does `df['sales'].rolling(3).mean()` return for the first two rows, and what extra step turns it into a forecast for the next day rather than a smoothed value for today?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐ 🟢 What is the difference between a forecast, a target and a budget?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟢 How would you check whether monthly sales data has seasonality before building any model?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 What is the difference between additive and multiplicative seasonality, and how do you tell which one your data shows?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 Quarterly sales over two years are given. Compute the seasonal index for Q3, using the average of all four quarter means as the base.
Q1: Year 1 = 80, Year 2 = 90. Q2: 100, 110. Q3: 130, 140. Q4: 90, 100.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Last December sales were 500 units. January to November this year ran 10% above the same months last year. Using a seasonal naive forecast with a growth adjustment, what is the December forecast?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 Sales rise by exactly 10 units every month. Why does a 3-month moving average lag the trend, and what does it forecast for the next month?
Series: 100, 110, 120, 130.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Fit a straight-line trend to five periods of data and forecast period 6.
t = 1, 2, 3, 4, 5; sales = 10, 12, 15, 16, 19.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Using the quarterly seasonal indices from your own working, how do you deseasonalise a figure and use the index to forecast next quarter?
Indices: Q1 0.81, Q2 1.00, Q3 1.29, Q4 0.90. Deseasonalised level expected for next quarter = 110, which is Q1.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 A weighted moving average gives weights 0.5, 0.3 and 0.2 to the latest, previous and earlier months. What is the forecast, and why use weights?
Last three months in order: 100, 110, 130 (130 is the latest).
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 What is simple exponential smoothing, and how does it differ from a moving average? Calculate the new forecast.
Alpha = 0.5, previous forecast = 100, actual = 120.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Two methods are tested on four months. Which has the better MAE, which has the better RMSE, and what does the difference tell you?
Method A errors: +2, -2, +2, -2. Method B errors: 0, 0, 0, +6.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Forecast errors (actual minus forecast) are given. Is the forecast biased, and how do you measure it?
Actual: 100, 100, 100. Forecast: 110, 105, 115.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Why can MAPE mislead when some actual values are zero or very small, and what would you use instead?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 What is stationarity, why does it matter for ARIMA-type models, and how would you check it in a few lines of Python?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Explain walk-forward (rolling-origin) validation, and why ordinary k-fold cross-validation is wrong for a time series.
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 What does `seasonal_decompose(df['sales'], model='additive', period=12)` from statsmodels give you, and how do you read each part?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How would you handle a festival or promotion spike, such as Diwali sales, when forecasting monthly or daily sales?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Give an example of data leakage in forecasting, such as using a centered moving average or full-sample statistics, and how you avoid it.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 The HR head asks you to forecast monthly attrition for the next six months from three years of history. How would you approach it, and how will you present the result?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 When would you move from a moving average or exponential smoothing to a machine learning model with lag features for forecasting, and when would you not?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 A forecast missed last quarter's sales by a wide margin and the manager asks why. How do you investigate and explain it?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Common misconception check: a trend line fits the last 12 months with a high R-squared, so the team says it will continue to hold for two more years. What is wrong with that reasoning?
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🟢 What does ARIMA stand for, and how would you describe it in plain words to a colleague who has only used moving averages?
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🟡 Read this code and say what it does and where it could go wrong:
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
m = ExponentialSmoothing(train['sales'], trend='add', seasonal='mul', seasonal_periods=12).fit()
fc = m.forecast(6)
```
Assume `train` is monthly data with one row per month and a date index.
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟡 You create `df['lag_7'] = df['sales'].shift(7)` and `df['roll_7'] = df['sales'].rolling(7).mean()` as features. What leakage risk do you check, and what do you do with the missing rows?
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 What is Holt-Winters (triple exponential smoothing), and which of trend and seasonality does each of its three smoothing parts handle?
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 How would you forecast demand for a new product with no sales history, and what do you tell the business about confidence?
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 Stockouts hid true demand for a fast-selling item for two weeks. How does that distort the history you forecast from, and what would you do?
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 Compute 3-day moving averages and say what an outlier does to them.
Daily orders: 50, 52, 51, 90, 53, 52. Compute the average for days 3 to 6.
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 Daily orders show weekly seasonality. Given two weeks of data, compute the Monday index and use it to forecast next Monday, assuming the weekly average level stays at 100.
Week 1 Mon 80, Tue 100, Wed 110, Thu 105, Fri 120, Sat 95, Sun 90. Week 2 Mon 84, Tue 104, Wed 106, Thu 111, Fri 118, Sat 99, Sun 96. Use the average over both weeks of all 14 days as the base.
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🟡 You want to paste last quarter's sales data into a public AI chatbot to get a forecast. What privacy and accuracy checks do you make first, and how do you verify the output?
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟡 When is Prophet a sensible choice for an analyst, and what would you still check about its output?
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Why is a trend estimated with a 2x12 centered moving average for monthly data, rather than a plain 12-month average?
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 What do the autocorrelation function (ACF) plot and a lag spike at 12 tell you about monthly data?
<!-- ANSWER_PENDING -->
