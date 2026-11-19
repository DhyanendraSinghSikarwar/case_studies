# Book 9 — Basic ML + AI Tools for Analysts | Part 7: Forecasting Basics (Moving Average, Trend, Seasonality) 🟡

**Target:** 38 questions | **Actual:** 45 questions
**Scope:** forecasting basics for analysts: time series features, moving averages, trend lines, seasonal indices, exponential smoothing, naive baselines, error metrics, time-based validation, and short statsmodels/pandas tasks.

### Q1 ⭐⭐⭐ 🟢 What is a time series, and how does forecasting a time series differ from predicting a value for ordinary independent rows?
**Asked at:** commonly asked (no company-specific report found); this is the opening question in the time series prep-site banks reviewed (unverified).
**What the interviewer is checking:** That you understand order and time matter, so you do not treat the rows like a shuffled deck of cards.
**Say this in the interview:** "A time series is the same measure recorded at regular times, like monthly sales or daily attendance. Unlike ordinary rows, the order carries information: this month depends on recent months. So we forecast forward in time and test on later periods, never on shuffled rows."
**Explain simply:**
- **Time series:** one measure, equally spaced times (daily, weekly, monthly), kept in date order.
- Ordinary rows (say, 1,000 employees and whether each left) are treated as independent: shuffling them changes nothing. In a time series, shuffling destroys the story, because March sales are close to February sales.
- The patterns we exploit are **trend** (slow rise or fall), **seasonality** (repeating calendar pattern) and **noise** (random leftovers). Ordinary prediction uses other columns (tenure, salary); basic forecasting mostly uses the past of the series itself.
- Forecasting also means predicting the future, where we have no rows yet, so validation must mimic that: train on the past, test on the later period.
**Worked example (concept question):** Predicting whether an employee leaves: you can split 1,000 rows randomly into train and test. Predicting next month's headcount: the training data must end before the test months, otherwise the model "sees the future".
**Alternative / pitfalls:** A time series can be turned into ordinary rows by adding lag columns (last month's value, last week's value), but the date order must still be respected in the split.
**Likely follow-ups:** 1) *What is the frequency?* How often values are recorded (daily, monthly). 2) *What if dates are missing?* Fill or flag the gaps first, since many methods assume equal spacing.
**Common mistakes:** Shuffling rows before splitting; ignoring missing dates; forecasting without first plotting the series.

### Q2 ⭐⭐⭐ 🟢 Explain trend, seasonality and random noise in a monthly sales series to a non-technical manager.
**Asked at:** commonly asked (no company-specific report found); a standard opener in time series question banks (unverified).
**What the interviewer is checking:** Can you describe the three building blocks in plain words with an example.
**Say this in the interview:** "Trend is the long-run direction, say sales creeping up each year. Seasonality is the pattern that repeats every year, like a festive-season peak. Noise is the random wobble left over that no pattern explains. A forecast tries to continue the first two and accept the third."
**Explain simply:**
- **Trend:** the slow, underlying direction. Think of it as the average level climbing or falling over years.
- **Seasonality:** a regular, calendar-linked rise and fall with a fixed length (12 months for monthly data). Think of Diwali demand, or April attrition after appraisals.
- **Noise (random variation):** one-off ups and downs from chance, such as a big order that landed a week early. You cannot forecast it, only estimate how large it usually is.
**Worked example (concept question):** In an invented 3-year monthly series (units), the yearly average was 1,056, 1,120 and 1,182: that is the trend, about +5 units per month. Within each year, December ran about 23% above that year's average and February about 12% below: that is seasonality. Month to month wobble of roughly 15 units around the pattern is noise.
**Alternative / pitfalls:** Some series also have cycles (multi-year booms and slowdowns with no fixed length); these are harder than seasonality because the length is not fixed.
**Likely follow-ups:** 1) *Can seasonality change?* Yes, if customer behaviour or the calendar (festival dates) shifts. 2) *How do you see them?* Plot the series and a yearly overlay (Q13).
**Common mistakes:** Calling any bump "seasonality" after one year of data; mixing up a trend with a one-time jump.

### Q3 ⭐⭐⭐ 🟢 What is a moving average, and why do analysts use it on sales or attendance data?
**Asked at:** commonly asked (no company-specific report found); fresher-level banks ask "define moving average" (unverified).
**What the interviewer is checking:** Do you know it is an average of the latest few periods that smooths noise, and its main limitation.
**Say this in the interview:** "A moving average takes the average of the latest N periods and slides forward one period at a time. It smooths out random ups and downs so the underlying direction is easier to see, and it can be used as a simple forecast."
**Explain simply:**
- **Window:** how many recent periods go into the average (3 months here).
- It reduces noise: one bad day matters less when averaged with its neighbours.
- It is simple and explainable, so it makes a fair first forecast.
- It lags behind real change (Q10, Q17) and the first N-1 periods have no value.
**Sample data:** Monthly attendance % (made-up).

| Month | Jan | Feb | Mar | Apr | May | Jun |
|---|---|---|---|---|---|---|
| Attendance % | 92 | 95 | 90 | 94 | 96 | 91 |

**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.Series(
    [92, 95, 90, 94, 96, 91],
    index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
)

# Average of the latest 3 months, moving forward one month at a time
smoothed = attendance.rolling(3).mean().round(1)
print(smoothed)
```
**Output:**
```text
Jan     NaN
Feb     NaN
Mar    92.3
Apr    93.0
May    93.3
Jun    93.7
dtype: float64
```
**What it means:** The raw series jumps between 90 and 96, but the smoothed line sits calmly around 93. Jan and Feb are blank because three months of history do not yet exist.
**Likely follow-ups:** 1) *Simple vs weighted?* Weighted gives recent months more say (Q20). 2) *Is it a forecast?* Only if you shift it forward one period (Q11).
**Common mistakes:** Reporting the smoothed value for today as if it were tomorrow's forecast; choosing a window without thinking about lag.

### Q4 ⭐⭐⭐ 🟢 What is a naive forecast, and why should every forecasting model be compared with one?
**Asked at:** commonly asked (no company-specific report found); baseline questions appear in time series banks (unverified).
**What the interviewer is checking:** That you benchmark before claiming a model is good.
**Say this in the interview:** "A naive forecast says next period will equal the last one (or, for seasonal data, the same period last year). It costs nothing, so any fancier model has to beat it on a fair test, otherwise the extra effort is not worth it."
**Explain simply:**
- **Naive forecast:** tomorrow = today. **Seasonal naive:** this December = last December.
- It is the **baseline**: the score to beat. A model with 8% error sounds fine until you learn the naive forecast gets 6%.
- Surprisingly hard to beat on short horizons and noisy data.
**Sample data:** 12 months of sales (units, made-up): 120, 130, 125, 140, 150, 145, 160, 170, 165, 180, 190, 185.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.Series([120, 130, 125, 140, 150, 145, 160, 170, 165, 180, 190, 185])

# Naive: this month's forecast = last month's actual
naive_forecast = sales.shift(1)

# 3-month moving average: average of the 3 months before
average_forecast = sales.rolling(3).mean().shift(1)

# Compare only months where both forecasts exist (month 4 onwards)
naive_error = (sales - naive_forecast).iloc[3:].abs().mean()
average_error = (sales - average_forecast).iloc[3:].abs().mean()
print("Naive MAE:", round(naive_error, 1))
print("3-month average MAE:", round(average_error, 1))
```
**Output:**
```text
Naive MAE: 10.0
3-month average MAE: 13.3
```
**What it means:** On this rising series the simple "same as last month" guess is off by 10 units on average, better than the 3-month average (13.3), which lags the rise. Report any model's error next to the naive error.
**Alternative / pitfalls:** For seasonal data the plain naive baseline is weak; use the seasonal naive one too.
**Likely follow-ups:** 1) *What if the model only ties naive?* Prefer the simpler one. 2) *Which metric?* The same one for both, on the same test months.
**Common mistakes:** Comparing models on different test periods; skipping the baseline.

### Q5 ⭐⭐⭐ 🟢 How would you explain to a manager that a forecast is an estimate with a range and not a promise?
**Asked at:** commonly asked (no company-specific report found); communication of uncertainty is a gap-fill question (judgement, unverified).
**What the interviewer is checking:** Can you communicate uncertainty without sounding evasive.
**Say this in the interview:** "I will give a best guess and a likely range, like a weather forecast: 'about 1,200 units, most likely between 1,170 and 1,230'. The range comes from how far off my forecasts were in the past. Plan stock and staffing for the range, not just the single number."
**Explain simply:**
- A **point forecast** is the single best-guess number. A **range** (prediction interval) says where the actual will probably land.
- A rough range uses the spread of past errors: forecast plus or minus about 1.3 times the typical error spread covers roughly 80% of outcomes (assuming errors are roughly bell-shaped and unbiased; this is a rule of thumb).
- Wider range means less certainty: longer horizons, volatile data, or promotions all widen it.
- Offer decisions by scenario: plan to the middle, protect against the low end.
**Worked example (concept question):** 12 past monthly errors (units): 30, -25, 40, -10, 15, -35, 20, -5, 25, -30, 10, -20. Their standard deviation is 25.4, so a forecast of 1,200 gets a rough 80% range of 1,200 plus or minus 33, that is 1,167 to 1,233.
**Alternative / pitfalls:** Statistical models (statsmodels, Prophet) can output intervals directly; still check them against past misses.
**Likely follow-ups:** 1) *Does 80% mean the actual will always be inside?* No, about 1 month in 5 lands outside. 2) *Is a range a way to avoid being wrong?* No, it is an honest statement of risk.
**Common mistakes:** Quoting one number to the decimal ("1,203.7 units"); presenting the range as a guarantee.

### Q6 ⭐⭐⭐ 🟢 What are MAE, RMSE and MAPE for a forecast, and which one would you show to a sales head?
**Asked at:** commonly asked (no company-specific report found); error-metric questions appear in forecasting banks and fresher PDFs (unverified).
**What the interviewer is checking:** That you know each metric's meaning, units and weakness, and can pick one for a business audience.
**Say this in the interview:** "MAE is the average miss in units. RMSE is similar but punishes big misses more. MAPE is the average miss as a percentage of actual. For a sales head I would show MAPE for a quick feel and MAE in units so they can plan stock; I would watch RMSE if big misses are costly."
**Explain simply:**
- **Error** = actual minus forecast. **MAE (mean absolute error):** average of the errors ignoring sign. In the same units as sales.
- **RMSE (root mean squared error):** square the errors, average, take the square root. Squaring makes one big miss count more than several small ones.
- **MAPE (mean absolute percentage error):** average of error divided by actual, as a %. Easy to read, but breaks when actuals are near zero (Q24).
- MAE and RMSE depend on units, so they cannot compare a 100-unit product with a 10,000-unit one; MAPE can.
**Worked example (concept question):** Actual 100, 110, 120; forecast 105, 100, 130 (see Q9). MAE = 8.33 units, RMSE = 8.66 units, MAPE = 7.47%.
**What it means:** "We are typically about 8 units, or 7.5%, off."
**Alternative / pitfalls:** Always show the naive forecast's score alongside.
**Likely follow-ups:** 1) *Why RMSE at least MAE?* Squaring weights big errors more; RMSE is never below MAE. 2) *Which is best?* Depends on the cost of misses.
**Common mistakes:** Mixing percentages and units; dividing by the forecast instead of actual in MAPE.

### Q7 ⭐⭐⭐ 🟢 Monthly sales for six months are given. What is the 3-month simple moving average forecast for July?
Month: Jan 120, Feb 130, Mar 125, Apr 140, May 150, Jun 145 (units).
**Asked at:** commonly asked (no company-specific report found); a standard fresher calculation (unverified).
**What the interviewer is checking:** Can you pick the right three months and average them.
**Say this in the interview:** "Use the latest three months, April, May and June: (140 + 150 + 145) / 3 = 145 units for July."
**Explain simply:**
- "3-month" means the three most recent actuals before the month you forecast.
- Do not include Jan to Mar; they are older. Simple means equal weights.
**Sample data:**

| Month | Jan | Feb | Mar | Apr | May | Jun |
|---|---|---|---|---|---|---|
| Units | 120 | 130 | 125 | 140 | 150 | 145 |

**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.Series([120, 130, 125, 140, 150, 145], index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"])

# Average of the latest 3 months (Apr, May, Jun)
july_forecast = sales.tail(3).mean()
print(july_forecast)
```
**Output:**
```text
145.0
```
**What it means:** Forecast for July is 145 units, equal to June because the series went up then dipped. Say it is an estimate, and that it will lag if sales keep climbing.
**Likely follow-ups:** 1) *And August?* Use May, Jun and the July forecast, or wait for July's actual. 2) *Why not 6 months?* Smoother but slower to react (Q10).
**Common mistakes:** Averaging all six months (140.0); using Mar, Apr, May.

### Q8 ⭐⭐⭐ 🟡 Why can you not use a random train/test split for a forecasting problem, and how do you split instead?
**Asked at:** commonly asked (no company-specific report found); an unverified anonymous Tiger Analytics report mentions a related time-series cross-validation question.
**What the interviewer is checking:** That you understand leakage from the future.
**Say this in the interview:** "A random split lets the model train on months after the ones it is tested on, so it effectively sees the future and the score looks better than it will be live. I split by date: train on the earlier months, test on the most recent ones."
**Explain simply:**
- Neighbouring months are similar, so a test month sandwiched between two training months is almost a copy of them. This is **leakage**: information from the test period reaching the model.
- In real use you only ever know the past, so the test must mimic that.
- Keep the test window as long as the horizon you will forecast (6 months ahead means test on 6 months).
- Refit on all data before the final live forecast.
**Sample data:** 24 monthly rows, Jan 2023 to Dec 2024, sorted oldest first.
**Code (what you write in the interview):**
```python
import pandas as pd

# 24 months of sales, already sorted by month (oldest first)
sales = pd.DataFrame({
    "month": pd.date_range("2023-01-01", periods=24, freq="MS"),
    "units": range(100, 124),
})

# Train on the first 18 months, test on the last 6
train = sales.iloc[:-6]
test = sales.iloc[-6:]

print("Train:", train["month"].min().date(), "to", train["month"].max().date())
print("Test: ", test["month"].min().date(), "to", test["month"].max().date())
```
**Output:**
```text
Train: 2023-01-01 to 2024-06-01
Test:  2024-07-01 to 2024-12-01
```
**What it means:** Every test month is later than every training month, like real forecasting. Report error on the test months only.
**Alternative / pitfalls:** For more reliable scores use walk-forward validation with several cut-off dates (Q26). `sklearn.model_selection.train_test_split(shuffle=False)` also keeps order (from memory, unverified).
**Likely follow-ups:** 1) *How long a test period?* Match the forecast horizon. 2) *What if the data is not sorted?* Sort by date first.
**Common mistakes:** Shuffling by default; including the test period when computing scaling or averages (Q29).

### Q9 ⭐⭐⭐ 🟡 Actual and forecast values for three months are given. Calculate MAE, RMSE and MAPE.
Actual: 100, 110, 120. Forecast: 105, 100, 130.
**Asked at:** commonly asked (no company-specific report found); a standard calculation question (unverified).
**What the interviewer is checking:** Correct formulas and the ability to read the answers.
**Say this in the interview:** "Errors are -5, 10, -10. MAE is 8.33 units. RMSE is about 8.66 units. MAPE is about 7.47%."
**Explain simply:**
- Error = actual minus forecast: 100-105 = -5; 110-100 = 10; 120-130 = -10.
- MAE: (5 + 10 + 10) / 3 = 8.33. RMSE: square root of (25 + 100 + 100) / 3 = square root of 75 = 8.66.
- MAPE: average of 5/100, 10/110, 10/120 = 5%, 9.09%, 8.33%, giving 7.47%.
**Sample data:**

| Month | Actual | Forecast | Error |
|---|---|---|---|
| 1 | 100 | 105 | -5 |
| 2 | 110 | 100 | 10 |
| 3 | 120 | 130 | -10 |

**Code (what you write in the interview):**
```python
import numpy as np

actual = np.array([100, 110, 120])
forecast = np.array([105, 100, 130])
error = actual - forecast

mae = np.abs(error).mean()
rmse = np.sqrt((error ** 2).mean())
mape = (np.abs(error) / actual).mean() * 100

print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("MAPE %:", round(mape, 2))
```
**Output:**
```text
MAE: 8.33
RMSE: 8.66
MAPE %: 7.47
```
**What it means:** We miss by about 8 units, or roughly 7.5%, per month. RMSE is slightly higher than MAE because two misses were bigger. Tell a manager: "about 7 to 8% off on average over three months", with the caution that three months is a tiny test.
**Likely follow-ups:** 1) *Why is RMSE bigger?* Squaring weights large errors. 2) *Over- or under-forecast?* Mean error is -1.67 (slightly over-forecast), mostly cancelling; see bias (Q23).
**Common mistakes:** Forgetting the absolute value; dividing by forecast in MAPE; stating MAPE as 0.0747.

### Q10 ⭐⭐⭐ 🟡 You are asked for a 3-month versus a 12-month moving average on monthly sales. What is the trade-off in choosing the window size?
**Asked at:** commonly asked (no company-specific report found); window-size trade-off is a common smoothing question (unverified).
**What the interviewer is checking:** That you understand smoothness versus responsiveness.
**Say this in the interview:** "A short window reacts fast but stays noisy. A long window is smooth but slow, and it lags behind real changes. A 12-month window also averages out one full seasonal cycle, so it hides seasonality. I choose by testing which window forecasts held-out months best."
**Explain simply:**
- Short window (3): follows recent change, picks up noise too.
- Long window (12): very smooth; slow to notice a rise or fall; needs 12 months of history.
- A 12-month average on monthly data removes seasonality (each month appears once), useful for seeing the trend but not for forecasting a peak.
- Pick with a time-based test, not by eye.
**Worked example (concept question):** Sales rising 5 units a month (with small seasonal wiggles) reached 215 in the last month. The 3-month average was 210 (5 below) but the 12-month average was 187.5 (27.5 below).
**Alternative / pitfalls:** If there is a trend, a plain moving average always trails it; consider trend-aware methods (Holt-Winters, Q37).
**Likely follow-ups:** 1) *Best window?* Whichever has lowest test error. 2) *What about 6?* A compromise.
**Common mistakes:** Picking a long window for "accuracy" when it just lags; using a window that is not a multiple of the seasonal length when smoothing seasonal data.

### Q11 ⭐⭐⭐ 🟡 A pandas column `sales` holds daily sales. What does `df['sales'].rolling(3).mean()` return for the first two rows, and what extra step turns it into a forecast for the next day rather than a smoothed value for today?
**Asked at:** commonly asked (no company-specific report found); rolling-window code is typical in time series banks (unverified).
**What the interviewer is checking:** NaN handling and the shift step that avoids using today's data to "forecast" today.
**Say this in the interview:** "The first two rows are NaN because there are not yet three days. To get a forecast you shift it by one row: `.shift(1)`, so row t holds the average of days t-3 to t-1."
**Explain simply:**
- `rolling(3)` makes a window of three rows; `.mean()` averages them. Rows 0 and 1 have fewer than 3 values, so pandas returns NaN (not a number: missing).
- The value at row t includes row t itself. A forecast made for day t may only use days before t, hence `.shift(1)`.
- The very last rolling value, unshifted, is the forecast for the next day not yet in the data.
**Sample data:** Daily sales: 100, 110, 130, 120, 140.
**Code (what you write in the interview):**
```python
import pandas as pd

df = pd.DataFrame({"sales": [100, 110, 130, 120, 140]})

# Smoothed value for each day (uses today and the 2 days before)
df["rolling_3"] = df["sales"].rolling(3).mean()

# Shift down one row so each row holds the forecast made from earlier days
df["forecast"] = df["rolling_3"].shift(1)
print(df.round(1))
```
**Output:**
```text
   sales  rolling_3  forecast
0    100        NaN       NaN
1    110        NaN       NaN
2    130      113.3       NaN
3    120      120.0     113.3
4    140      130.0     120.0
```
**What it means:** Day 3's forecast (113.3) was built from days 0 to 2 only. The next day's (day 5) forecast is 130.0, the last rolling value.
**Alternative / pitfalls:** `rolling(3, min_periods=1)` fills the first rows with partial averages; say so if you use it. Do not use `center=True` for forecasting (Q29).
**Likely follow-ups:** 1) *Why NaN, not zero?* Zero would be a false value. 2) *Evaluate how?* Compare the forecast column with actual on test rows.
**Common mistakes:** Treating the rolling mean as the forecast without shifting; filling NaN with 0.

### Q12 ⭐⭐ 🟢 What is the difference between a forecast, a target and a budget?
**Asked at:** commonly asked (no company-specific report found); a business-vocabulary gap-fill question (judgement, unverified).
**What the interviewer is checking:** Whether you separate prediction from ambition and from money.
**Say this in the interview:** "A forecast is my best estimate of what will happen. A target is what the business wants to happen. A budget is the money and resources approved to get there. They can differ, and the gap is the useful conversation."
**Explain simply:**
- **Forecast:** based on data and assumptions; neutral; can say "we will fall short".
- **Target:** a goal that may stretch beyond the forecast to motivate people.
- **Budget:** a spending or revenue plan agreed with finance, often fixed for the year.
- Never adjust a forecast to match a target; adjust the plan or the target.
**Worked example (concept question):** Forecast sales 1,000 units, target 1,200, budget set at 1,100. The 200-unit gap between forecast and target needs actions (promotion, new channel), not a bigger forecast number.
**Alternative / pitfalls:** In HR, headcount forecast (expected leavers), headcount target (hiring goal) and hiring budget are likewise different.
**Likely follow-ups:** 1) *Can they be equal?* Yes, but only by coincidence or by plan. 2) *Who owns each?* Analysts the forecast; leadership the target; finance the budget.
**Common mistakes:** Bending the forecast to please; using the words as synonyms.

### Q13 ⭐⭐ 🟢 How would you check whether monthly sales data has seasonality before building any model?
**Asked at:** commonly asked (no company-specific report found); seasonality checks appear in trend/seasonality banks (unverified).
**What the interviewer is checking:** Visual-first, simple checks before modelling.
**Say this in the interview:** "I plot the series, then overlay the years or group by calendar month. If the same months are high or low every year, it is seasonal. I confirm with each month's share of its year's average, and ideally have at least two full years."
**Explain simply:**
- Line plot: do the same peaks and dips repeat at the same time each year?
- Month-by-year table or "seasonal plot": one line per year; lines that move together mean seasonality.
- Ratio to yearly average: a value consistently away from 1.0 for a given month is its seasonal effect.
- With under two cycles you cannot separate seasonality from a one-off event.
**Sample data:** `sales_series`: 36 monthly values (units, made-up, Jan 2022 to Dec 2024) with a rising level and a festive peak in November and December. Its December values are 1,317, 1,363 and 1,442.
**Code (what you write in the interview):**
```python
import pandas as pd

# sales_series: monthly units with a date index (36 months, Jan 2022 to Dec 2024)
sales = sales_series.to_frame(name="units")
sales["year"] = sales.index.year
sales["month"] = sales.index.month

# Each month's sales as a share of that year's average month
sales["vs_year_average"] = sales["units"] / sales.groupby("year")["units"].transform("mean")

# If some months are always above or below 1.0, there is seasonality
print(sales.groupby("month")["vs_year_average"].mean().round(2))
```
**Output:**
```text
month
1     0.89
2     0.88
3     0.93
4     0.95
5     0.96
6     0.97
7     1.01
8     1.00
9     1.02
10    1.03
11    1.14
12    1.23
Name: vs_year_average, dtype: float64
```
**What it means:** January and February sit about 11 to 12% below the yearly average; November and December run 14% and 23% above. That repeated shape across three years is seasonality. The table was computed on this invented series.
**Alternative / pitfalls:** `seasonal_decompose` (Q27) or an ACF plot (Q45). A trend inflates later months within a year, so ratios are slightly confounded by it.
**Likely follow-ups:** 1) *How many years?* At least two, preferably three or more. 2) *Seasonality or promotion?* Check whether it repeats on the same calendar month.
**Common mistakes:** Judging from one year; forgetting the data trend.

### Q14 ⭐⭐ 🟢 What is the difference between additive and multiplicative seasonality, and how do you tell which one your data shows?
**Asked at:** commonly asked (no company-specific report found); a standard decomposition question (unverified).
**What the interviewer is checking:** Do you understand constant versus proportional swings.
**Say this in the interview:** "Additive means the seasonal swing is a fixed number of units, say plus 20 in December. Multiplicative means it is a percentage, say 20% above normal, so it grows as sales grow. I plot the series: if the swings get bigger as the level rises, it is multiplicative."
**Explain simply:**
- **Additive:** value = trend + seasonal effect + noise. Swing stays about the same size.
- **Multiplicative:** value = trend x seasonal index x noise. Swing scales with the level.
- Most sales series grow with the business, so they are often multiplicative; a series with a flat level is often additive (judgement, not a rule).
- A log transform turns multiplicative patterns into additive ones.
**Worked example (concept question):** A December peak of +20 units is additive: it is +20 whether baseline is 100 or 200. A December peak of +20% is multiplicative: +20 at baseline 100 but +40 at baseline 200.
**Alternative / pitfalls:** If unsure, fit both and compare errors on a test period. Multiplicative cannot handle zero or negative values.
**Likely follow-ups:** 1) *Which does Q15 use?* Ratios, so multiplicative style. 2) *Does it matter?* Yes, wrong choice leaves a pattern in the leftovers.
**Common mistakes:** Defaulting to additive without looking; using multiplicative with zeros.

### Q15 ⭐⭐ 🟢 Quarterly sales over two years are given. Compute the seasonal index for Q3, using the average of all four quarter means as the base.
Q1: Year 1 = 80, Year 2 = 90. Q2: 100, 110. Q3: 130, 140. Q4: 90, 100.
**Asked at:** commonly asked (no company-specific report found); seasonal index calculations are standard (unverified).
**What the interviewer is checking:** Correct average-of-averages method and the meaning of an index above 1.
**Say this in the interview:** "Q3 averages 135; the average of the four quarter means is 105; 135 / 105 = 1.286, so Q3 runs about 29% above an average quarter."
**Explain simply:**
- Quarter means: Q1 85, Q2 105, Q3 135, Q4 95.
- Base = (85 + 105 + 135 + 95) / 4 = 105.
- Index = quarter mean / base. Above 1 is a strong quarter; below 1 is weak. The four indices average to 1.
**Sample data:**

| Quarter | Year 1 | Year 2 | Mean |
|---|---|---|---|
| Q1 | 80 | 90 | 85 |
| Q2 | 100 | 110 | 105 |
| Q3 | 130 | 140 | 135 |
| Q4 | 90 | 100 | 95 |

**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({"Q1": [80, 90], "Q2": [100, 110], "Q3": [130, 140], "Q4": [90, 100]})

quarter_means = sales.mean()
base = quarter_means.mean()
seasonal_index = quarter_means / base

print(quarter_means.tolist(), base)
print(seasonal_index.round(3))
```
**Output:**
```text
[85.0, 105.0, 135.0, 95.0] 105.0
Q1    0.810
Q2    1.000
Q3    1.286
Q4    0.905
dtype: float64
```
**What it means:** Q3 index is 1.286: Q3 is about 29% above the average quarter; Q1 is about 19% below. Q19 uses the same indices (rounded).
**Alternative / pitfalls:** With a strong trend, the plain average mixes trend into the index; first remove the trend (centered moving average) for a cleaner index.
**Likely follow-ups:** 1) *Why two years?* One year cannot show repeat. 2) *Index of 1.0?* An average quarter.
**Common mistakes:** Dividing by one year's total; dividing by the Q3 mean itself.

### Q16 ⭐⭐ 🟢 Last December sales were 500 units. January to November this year ran 10% above the same months last year. Using a seasonal naive forecast with a growth adjustment, what is the December forecast?
**Asked at:** commonly asked (no company-specific report found); seasonal naive is a standard baseline (unverified).
**What the interviewer is checking:** Can you combine the seasonal pattern with recent growth.
**Say this in the interview:** "Seasonal naive says December repeats last December, 500. Adjusting for the 10% growth gives 500 x 1.10 = 550 units."
**Explain simply:**
- **Seasonal naive:** forecast = same period last year. Keeps the seasonal shape.
- **Growth adjustment:** scale it by how this year has run versus last year so far.
- The 10% is only an estimate; December may behave differently if promotions or calendar dates moved.
**Code (what you write in the interview):**
```python
last_december = 500
growth = 0.10

# Same month last year, scaled by this year's growth so far
december_forecast = last_december * (1 + growth)
print(december_forecast)
```
**Output:**
```text
550.0
```
**What it means:** Forecast December at about 550 units. Add a range, for example if past months missed by about 5%, say "roughly 520 to 580" (illustrative).
**Alternative / pitfalls:** Use growth from several months rather than the last one; check festival dates did not shift between years.
**Likely follow-ups:** 1) *If growth is slowing?* Use the recent months' growth. 2) *Why not just 500?* It ignores growth.
**Common mistakes:** Adding 10 units instead of 10%; using the overall average instead of December.

### Q17 ⭐⭐ 🟡 Sales rise by exactly 10 units every month. Why does a 3-month moving average lag the trend, and what does it forecast for the next month?
Series: 100, 110, 120, 130.
**Asked at:** commonly asked (no company-specific report found); lag of moving averages is a standard follow-up (unverified).
**What the interviewer is checking:** That you know averaging past values on a rising series always underestimates.
**Say this in the interview:** "The 3-month average of 110, 120 and 130 is 120. But the trend says the next value is 140, so it is 20 short. The average sits in the middle of the window, which is one month back, so it trails by roughly a month of growth plus the extra month of forecasting."
**Explain simply:**
- Each value in the window is older and lower than the latest, so their average is below it.
- The 3-month average equals the value from the middle month (120), so it lags the latest actual (130) by 10, one month of growth.
- Forecasting the next month adds another month of growth missed: 140 versus 120, a miss of 20.
- On a falling series it would over-forecast.
**Sample data:** 100, 110, 120, 130 (units).
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.Series([100, 110, 120, 130])

# Forecast for the next month = average of the last 3 months
forecast = sales.tail(3).mean()
print(forecast)
```
**Output:**
```text
120.0
```
**What it means:** The forecast is 120, but the straight-line pattern implies 140. Do not use a plain moving average when there is a clear trend.
**Alternative / pitfalls:** Use a trend line (Q18), Holt's method (trend-aware exponential smoothing, Q37) or a smaller window.
**Likely follow-ups:** 1) *Does a shorter window help?* Yes, a 2-month average gives 125. 2) *Is it good for flat data?* Yes.
**Common mistakes:** Forecasting 130 or 120 and calling it fine; blaming noise when this series has none.

### Q18 ⭐⭐ 🟡 Fit a straight-line trend to five periods of data and forecast period 6.
t = 1, 2, 3, 4, 5; sales = 10, 12, 15, 16, 19.
**Asked at:** commonly asked (no company-specific report found); a simple regression-on-time question (unverified).
**What the interviewer is checking:** Can you fit a line, read slope and intercept, and extrapolate carefully.
**Say this in the interview:** "The fitted line is sales = 7.8 + 2.2 x t. Sales grow about 2.2 units per period, and period 6 forecasts to 7.8 + 2.2 x 6 = 21 units."
**Explain simply:**
- **Slope (2.2):** average rise per period. **Intercept (7.8):** the line's value at period 0.
- The line is the one that minimises the squared gaps to the five points (least squares).
- Only five points: treat the forecast as rough.
**Sample data:**

| t | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Sales | 10 | 12 | 15 | 16 | 19 |

**Code (what you write in the interview):**
```python
import numpy as np

period = np.array([1, 2, 3, 4, 5])
sales = np.array([10, 12, 15, 16, 19])

# Straight line: sales = intercept + slope * period
slope, intercept = np.polyfit(period, sales, 1)
forecast_period_6 = intercept + slope * 6

print("slope:", round(slope, 2), "intercept:", round(intercept, 2))
print("Period 6 forecast:", round(forecast_period_6, 1))
```
**Output:**
```text
slope: 2.2 intercept: 7.8
Period 6 forecast: 21.0
```
**What it means:** Sales are rising about 2.2 units per period; the next one is expected near 21, give or take. In Excel, `=FORECAST.LINEAR(6, sales_range, t_range)` gives the same (from memory, unverified).
**Alternative / pitfalls:** A line assumes growth stays constant; forecasts far beyond the data are risky (Q33). Five points support only a short extrapolation.
**Likely follow-ups:** 1) *How good is the fit?* Look at residuals and R-squared, but do not over-trust R-squared. 2) *Period 20?* Too far for this data.
**Common mistakes:** Using month names rather than numbers as the x-axis; extrapolating far ahead.

### Q19 ⭐⭐ 🟡 Given quarterly seasonal indices, how do you deseasonalise a figure and use the index to forecast next quarter?
Indices: Q1 0.81, Q2 1.00, Q3 1.29, Q4 0.90. Deseasonalised level expected for next quarter = 110, which is Q1.
**Asked at:** commonly asked (no company-specific report found); classical seasonal-index method (unverified).
**What the interviewer is checking:** Divide to remove, multiply to put back.
**Say this in the interview:** "To deseasonalise I divide the actual by its index; to forecast I multiply the underlying level by the index of the target quarter. Next quarter is Q1: 110 x 0.81 = 89.1 units."
**Explain simply:**
- Deseasonalised = actual / index. If Q3 sold 129, the underlying level is 129 / 1.29 = 100, because Q3 is naturally strong.
- Forecast = deseasonalised level x index. Q1 is a naturally weak quarter, so the forecast (89.1) is lower than the level (110).
- Deseasonalising lets you see whether growth is real or just the calendar.
**Code (what you write in the interview):**
```python
seasonal_index = {"Q1": 0.81, "Q2": 1.00, "Q3": 1.29, "Q4": 0.90}

# Deseasonalise: divide by the index (example: Q3 actual 129)
print(round(129 / seasonal_index["Q3"], 1))

# Forecast: deseasonalised level times next quarter's index
print(round(110 * seasonal_index["Q1"], 1))
```
**Output:**
```text
100.0
89.1
```
**What it means:** Q3's 129 units is just a level of 100 in disguise. For next quarter (Q1) expect about 89 units, not 110.
**Alternative / pitfalls:** Indices assume the pattern stays stable; they do not capture a changing trend. Round the answer when presenting (about 89).
**Likely follow-ups:** 1) *Where do indices come from?* Q15. 2) *Additive version?* Subtract and add the seasonal amount instead.
**Common mistakes:** Multiplying to deseasonalise; forgetting to re-apply the index.

### Q20 ⭐⭐ 🟡 A weighted moving average gives weights 0.5, 0.3 and 0.2 to the latest, previous and earlier months. What is the forecast, and why use weights?
Last three months in order: 100, 110, 130 (130 is the latest).
**Asked at:** commonly asked (no company-specific report found); a typical weighted-average calculation (unverified).
**What the interviewer is checking:** Weights go to the right months, and you know the reason.
**Say this in the interview:** "0.5 x 130 + 0.3 x 110 + 0.2 x 100 = 65 + 33 + 20 = 118 units. Weights let recent months count more, so it reacts faster than a simple average, which gives 113.3."
**Explain simply:**
- The weights add to 1 (0.5 + 0.3 + 0.2), so the result is still on the sales scale.
- The latest month (130) gets 0.5, not the oldest. A common slip is reversing the order.
- Simple average of the same data is 113.3; weighting moves the forecast toward the recent rise.
**Code (what you write in the interview):**
```python
weights = [0.5, 0.3, 0.2]
latest_first = [130, 110, 100]

# Multiply each month by its weight and add up
forecast = sum(w * x for w, x in zip(weights, latest_first))
print(forecast)
```
**Output:**
```text
118.0
```
**What it means:** Forecast is 118 units. The weights are a judgement call; choose them by testing on past data.
**Alternative / pitfalls:** Exponential smoothing (Q21) is a weighted average with automatically shrinking weights.
**Likely follow-ups:** 1) *What if weights do not add to 1?* The forecast is scaled wrongly. 2) *How to choose them?* Test on held-out months.
**Common mistakes:** Giving 0.5 to the oldest value; weights that do not sum to 1.

### Q21 ⭐⭐ 🟡 What is simple exponential smoothing, and how does it differ from a moving average? Calculate the new forecast.
Alpha = 0.5, previous forecast = 100, actual = 120.
**Asked at:** commonly asked (no company-specific report found); exponential smoothing is a standard forecasting topic (unverified).
**What the interviewer is checking:** The update rule and the weighting idea.
**Say this in the interview:** "New forecast = old forecast + alpha x (actual - old forecast) = 100 + 0.5 x 20 = 110. Unlike a moving average, it uses all history with weights that shrink for older months, and needs only the last forecast and last actual."
**Explain simply:**
- **Alpha** (between 0 and 1) is how fast it learns: high alpha follows recent data; low alpha is smooth.
- The forecast moves a fraction alpha of the way toward the latest miss (20 x 0.5 = 10).
- A moving average gives equal weight to the last N periods and none to older ones; exponential smoothing never fully forgets, it just fades.
- Simple version assumes no clear trend or seasonality.
**Code (what you write in the interview):**
```python
alpha = 0.5
previous_forecast = 100
actual = 120

# New forecast = old forecast + alpha * (actual - old forecast)
new_forecast = previous_forecast + alpha * (actual - previous_forecast)
print(new_forecast)
```
**Output:**
```text
110.0
```
**What it means:** Forecast moves from 100 to 110: halfway to the actual of 120. With alpha 0.2 it would be only 104.
**Alternative / pitfalls:** Choose alpha by minimising error on past data (statsmodels does it automatically; from memory, check the API on your version).
**Likely follow-ups:** 1) *Alpha of 1?* Equals naive forecast. 2) *Trend?* Use Holt's method (Q37).
**Common mistakes:** Mixing up alpha (weight on the actual); thinking it forgets old data completely.

### Q22 ⭐⭐ 🟡 Two methods are tested on four months. Which has the better MAE, which has the better RMSE, and what does the difference tell you?
Method A errors: +2, -2, +2, -2. Method B errors: 0, 0, 0, +6.
**Asked at:** commonly asked (no company-specific report found); MAE versus RMSE is a standard follow-up (unverified).
**What the interviewer is checking:** That you know RMSE punishes a single big miss.
**Say this in the interview:** "B has the better MAE (1.5 versus 2.0), but A has the better RMSE (2.0 versus 3.0). B is usually perfect but missed one month badly. RMSE penalises that, so which is better depends on whether big misses are costly."
**Explain simply:**
- MAE for A: (2+2+2+2)/4 = 2. For B: (0+0+0+6)/4 = 1.5.
- RMSE for A: square root of (4+4+4+4)/4 = 2. For B: square root of 36/4 = 3.
- Same total error idea, different shape: A is steady small misses, B is mostly right with one big miss.
- If one big miss means a stockout or an overspend, prefer A; if small misses are cheap and the big one is rare, B may be fine.
**Code (what you write in the interview):**
```python
import numpy as np

method_a = np.array([2, -2, 2, -2])
method_b = np.array([0, 0, 0, 6])

for name, errors in [("A", method_a), ("B", method_b)]:
    mae = np.abs(errors).mean()
    rmse = np.sqrt((errors ** 2).mean())
    print(name, "MAE:", mae, "RMSE:", round(rmse, 2))
```
**Output:**
```text
A MAE: 2.0 RMSE: 2.0
B MAE: 1.5 RMSE: 3.0
```
**What it means:** The metric you pick changes the winner. Say which cost matters to the business, then choose. A also has zero bias (errors cancel) while B is biased low.
**Alternative / pitfalls:** With four months the comparison is fragile; test over more periods.
**Likely follow-ups:** 1) *When are MAE and RMSE equal?* When all errors have the same size. 2) *Which to report?* Both.
**Common mistakes:** Declaring a winner without saying which metric; thinking RMSE can be below MAE (it cannot).

### Q23 ⭐⭐ 🟡 Forecast errors (actual minus forecast) are given. Is the forecast biased, and how do you measure it?
Actual: 100, 100, 100. Forecast: 110, 105, 115.
**Asked at:** commonly asked (no company-specific report found); bias is a gap-fill question (judgement, unverified).
**What the interviewer is checking:** That you separate bias (direction) from accuracy (size).
**Say this in the interview:** "Errors (actual minus forecast) are -10, -5 and -15, all negative. The mean error, the bias, is -10 units or -10%. The forecast is consistently too high, which is bias, not random miss."
**Explain simply:**
- The question gives actual and forecast, not errors, so I first compute them (actual minus forecast).
- **Bias** = mean error with its sign kept. Zero means over and under misses cancel; negative here means over-forecasting.
- MAE ignores sign, so it hides direction: MAE is also 10 here, but a bias of -10 shows every miss was in the same direction.
- Biased forecasts are good news in a sense: a systematic shift can be corrected.
**Code (what you write in the interview):**
```python
import numpy as np

actual = np.array([100, 100, 100])
forecast = np.array([110, 105, 115])

error = actual - forecast
bias = error.mean()
bias_percent = (error / actual).mean() * 100
mae = np.abs(error).mean()

print("Errors:", error.tolist())
print("Bias (mean error):", bias)
print("Bias %:", round(bias_percent, 1))
print("MAE:", mae)
```
**Output:**
```text
Errors: [-10, -5, -15]
Bias (mean error): -10.0
Bias %: -10.0
MAE: 10.0
```
**What it means:** The forecast runs about 10 units (10%) too high every time. Tell the manager: "the model over-forecasts; lowering it by about 10% would remove the bias, but I would check it on more months first."
**Alternative / pitfalls:** Three points are few; confirm over a longer test window. The sign convention (actual minus forecast, here) flips if you define error the other way; state it.
**Likely follow-ups:** 1) *Is the forecast good if bias is zero?* Not necessarily; the errors may still be large. 2) *Cause?* Over-optimistic assumptions, missed decline.
**Common mistakes:** Mixing sign conventions; reading MAE as "no bias".

### Q24 ⭐⭐ 🟡 Why can MAPE mislead when some actual values are zero or very small, and what would you use instead?
**Asked at:** commonly asked (no company-specific report found); MAPE and the follow-up on zeros appear in prep-site forecasting banks (HelloIntern, Dataford; unverified).
**What the interviewer is checking:** Whether you know MAPE divides by the actual value, so zeros break it and tiny values blow it up.
**Say this in the interview:** "MAPE is the error divided by the actual, so a zero actual gives a division by zero and a tiny actual gives a huge percentage. I would use MAE for units, or a weighted MAPE, which divides the total error by the total actual."
**Explain simply:**
- MAPE (mean absolute percentage error) = average of |actual minus forecast| / actual, shown as a percent.
- If a day has 0 sales, the percentage is infinite and the average cannot be computed. If a day has 2 sales and you forecast 5, that one day shows 150% and drags the whole average up.
- Weighted MAPE (WMAPE) = total absolute error / total actual. Big days count more, small days cannot explode it.
- MAE is simple and stays in units (orders, people), so it is easy to explain.
**Sample data:** 4 days of orders for a slow item: actual 0, 2, 100, 3; forecast 4, 5, 95, 2.
**Code (what you write in the interview):**
```python
import numpy as np

actual = np.array([0, 2, 100, 3])
forecast = np.array([4, 5, 95, 2])
errors = actual - forecast

# MAE: average size of the miss, in units
mae = np.abs(errors).mean()

# Weighted MAPE: total miss divided by total actual sales
wmape = np.abs(errors).sum() / actual.sum() * 100

# Ordinary MAPE only works on the rows where actual is not zero
nonzero = actual != 0
mape = (np.abs(errors[nonzero]) / actual[nonzero]).mean() * 100

print("MAE", mae, "| MAPE (zero row dropped)", round(mape, 1), "| WMAPE", round(wmape, 1))
```
**Output:**
```text
MAE 3.25 | MAPE (zero row dropped) 62.8 | WMAPE 12.4
```
**What it means:** The forecast is off by about 3 orders a day (MAE 3.25) and by 12% of total volume (WMAPE). MAPE says 63% only because two tiny days look terrible in percent. Show the sales head MAE or WMAPE here.
**Alternative / pitfalls:** sMAPE (divides by the average of actual and forecast) avoids the zero division in most cases but has its own quirks, so do not present it as a perfect fix. Dropping zero rows hides the days you may care about most.
**Likely follow-ups:** 1) *Is MAPE ever fine?* Yes, when values are large and never near zero. 2) *Which is better for large misses?* RMSE punishes them more.
**Common mistakes:** Quoting MAPE on intermittent or low-volume items; silently dropping zero days; mixing MAPE (percent) with MAE (units).

### Q25 ⭐⭐ 🟡 What is stationarity, why does it matter for ARIMA-type models, and how would you check it in a few lines of Python?
**Asked at:** commonly asked (no company-specific report found); stationarity appears in prep-site time series banks (Analytics Vidhya, Hyring, techprep; unverified).
**What the interviewer is checking:** Whether you can define it in plain words and know one test for it.
**Say this in the interview:** "A stationary series has a steady average and a steady spread over time, with no trend and no changing pattern. ARIMA assumes that, so if sales trend upward I difference it (subtract the previous value) first. I check with a plot and the ADF test."
**Explain simply:**
- Stationary means the series behaves the same way whenever you look: stable average, stable ups and downs, no long climb or fall.
- Monthly sales with a steady climb is not stationary. The month-on-month change often is.
- Differencing = this month minus last month. It removes a trend. The "I" in ARIMA (Q34) is that step.
- ADF test (Augmented Dickey-Fuller): a p-value below 0.05 suggests the series is stationary; a large p-value says it is not. It is a guide, always look at the plot too.
**Sample data:** 36 months of sales climbing about 3 a month plus noise (seeded, invented).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

# Sample data: 36 months of sales that climb steadily (seeded)
rng = np.random.default_rng(42)
months = pd.date_range('2022-01-01', periods=36, freq='MS')
sales = pd.Series(100 + 3 * np.arange(36) + rng.normal(0, 4, 36), index=months)

# Augmented Dickey-Fuller test: a small p-value (below 0.05) suggests stationary
p_raw = adfuller(sales)[1]
p_differenced = adfuller(sales.diff().dropna())[1]

print("raw p-value:", round(p_raw, 3))
print("after differencing p-value:", round(p_differenced, 6))
```
**Output:**
```text
raw p-value: 0.916
after differencing p-value: 0.0
```
**What it means:** The raw series is clearly not stationary (0.916 is far above 0.05). After differencing the p-value is essentially zero, so the changes are stationary and suitable for ARIMA.
**Alternative / pitfalls:** The ADF test has low power on short series (like 24 points), so a plot and judgement matter. Seasonal patterns also break stationarity; seasonal differencing (subtract the value 12 months ago) handles that.
**Likely follow-ups:** 1) *Can I over-difference?* Yes, it adds noise; difference only as much as needed. 2) *Do I need this for moving averages?* No, it matters for ARIMA-type models.
**Common mistakes:** Reading a high p-value as "stationary"; running ARIMA on trending data without differencing; trusting one test on 20 data points.

### Q26 ⭐⭐ 🟡 Explain walk-forward (rolling-origin) validation, and why ordinary k-fold cross-validation is wrong for a time series.
**Asked at:** One candidate report (Tiger Analytics, Senior Analyst review, via aggregator snippet; anonymous, unverified) lists how to do cross-validation for a time series and how it differs from k-fold.
**What the interviewer is checking:** Whether you understand that time order must be respected, so you never train on the future.
**Say this in the interview:** "Ordinary k-fold shuffles rows, so the model trains on months that come after the ones it is tested on, which is cheating. Walk-forward trains on the past, tests on the next block, then moves the cut-off forward and repeats."
**Explain simply:**
- Cross-validation means testing a model several times on different held-out pieces to see how stable it is.
- In k-fold, pieces are random, so the training data includes the future. A model that has seen December cannot honestly be tested on November.
- Walk-forward (also called rolling-origin): train on months 1-6, test on 7-8; train on 1-8, test on 9-10; and so on. The training window grows (an expanding window) or slides.
- Average the error across rounds. This also shows whether accuracy is stable or got worse recently.
**Sample data:** 12 months numbered 0 (oldest) to 11.
**Code (what you write in the interview):**
```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

months = np.arange(12)   # 12 months in time order, 0 = oldest

# Each round trains on the past and tests on the next 2 months
walk_forward = TimeSeriesSplit(n_splits=3, test_size=2)
for train_months, test_months in walk_forward.split(months):
    print("train on months", train_months.min(), "to", train_months.max(),
          "| test on months", test_months.tolist())
```
**Output:**
```text
train on months 0 to 5 | test on months [6, 7]
train on months 0 to 7 | test on months [8, 9]
train on months 0 to 9 | test on months [10, 11]
```
**What it means:** Every test block is strictly later than its training data. Report the average error across the three rounds. (A shuffled `KFold` on the same months would put months 8 to 11 in training while testing on earlier ones.)
**Alternative / pitfalls:** Keep a final untouched test period for the last check. With seasonal data, make sure the training window covers at least one full year.
**Likely follow-ups:** 1) *Expanding or sliding window?* Expanding uses all history; sliding adapts faster if the business changed. 2) *Why does the first fold have less data?* It starts early in history; that is normal.
**Common mistakes:** Using `shuffle=True` or plain k-fold; tuning on the test blocks; ignoring that early folds are weaker.

### Q27 ⭐⭐ 🟡 What does `seasonal_decompose(df['sales'], model='additive', period=12)` from statsmodels give you, and how do you read each part?
**Asked at:** commonly asked (no company-specific report found); decomposition appears in prep-site banks (DevInterview, techprep; unverified).
**What the interviewer is checking:** Whether you can name the pieces (trend, seasonal, residual) and read them in plain words.
**Say this in the interview:** "It splits monthly sales into three parts that add up to the original: a slow-moving trend, a repeating 12-month seasonal pattern, and a leftover residual. I read the trend for direction, the seasonal part for which months are high or low, and the residual for noise or oddities."
**Explain simply:**
- Additive means sales = trend + seasonal + residual. `period=12` says the pattern repeats every 12 rows (monthly data, yearly cycle).
- `result.trend`: smoothed level. It is empty (NaN) for the first 6 and last 6 months because it uses a centered average (Q44).
- `result.seasonal`: the same 12 numbers repeated each year, summing to about 0 (for example, December is +10 units above normal).
- `result.resid`: what is left. Big residuals flag one-off events (a promotion, a strike). Needs at least two full years of data.
**Sample data:** 36 months of invented sales with a rising trend and a yearly pattern (seeded).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# Sample data: 36 months, rising trend plus a repeating yearly pattern (seeded)
rng = np.random.default_rng(42)
months = pd.date_range('2022-01-01', periods=36, freq='MS')
yearly_pattern = np.array([-10, -8, -3, 0, 3, 6, 8, 6, 2, 0, 5, 12])
yearly_pattern = yearly_pattern - yearly_pattern.mean()
df = pd.DataFrame({'sales': 200 + 2 * np.arange(36) + np.tile(yearly_pattern, 3)
                   + rng.normal(0, 2, 36)}, index=months)

result = seasonal_decompose(df['sales'], model='additive', period=12)

print("Trend, months 1, 7 and 13:", result.trend.iloc[[0, 6, 12]].round(1).tolist())
print("Seasonal effect, Jan to Dec:", result.seasonal.iloc[:12].round(1).tolist())
print("Biggest leftover (residual):", round(result.resid.abs().max(), 1))
```
**Output:**
```text
Trend, months 1, 7 and 13: [nan, 211.7, 224.2]
Seasonal effect, Jan to Dec: [-12.5, -9.4, -4.2, -2.7, 1.6, 3.3, 7.3, 3.9, 0.0, -3.3, 5.3, 10.6]
Biggest leftover (residual): 1.7
```
**What it means:** Trend rises about 2 units a month; January is about 12 below the trend and December about 11 above; residuals are small (max 1.7), so trend plus season explains the data well.
**Alternative / pitfalls:** Use `model='multiplicative'` if the seasonal swings grow with the level (Q14). It is a description of the past, not a forecast. Classical decomposition assumes the pattern is identical every year.
**Likely follow-ups:** 1) *Why NaN at the ends?* The centered average needs 6 months on each side. 2) *Can it forecast?* Not directly; extend trend and add the seasonal part.
**Common mistakes:** Wrong `period` (12 for monthly, 7 for daily-with-weekly pattern); using it with under two years of data; reading residuals as "error" when they may be real events.

### Q28 ⭐⭐ 🟡 How would you handle a festival or promotion spike, such as Diwali sales, when forecasting monthly or daily sales?
**Asked at:** commonly asked (no company-specific report found); a gap-fill topic for India-based retail and e-commerce analyst roles.
**What the interviewer is checking:** Whether you treat the spike as a known, explainable event instead of noise or a trend change.
**Say this in the interview:** "I would not let it distort the baseline. I flag the festival period, estimate the normal level without it, measure the usual uplift from past festivals, and add it back in the right month. Diwali moves between October and November, so a plain seasonal pattern by calendar month will mislabel it."
**Explain simply:**
- Diwali follows a lunar calendar, so it falls in a different month or week each year. A "same month last year" forecast puts the spike in the wrong place.
- Create a flag column (1 during the festival window, 0 otherwise) or a "days to festival" feature, and keep promotion dates in the same way.
- Estimate the baseline from non-festival periods, then the uplift as festival sales / baseline.
- Check with the business for the confirmed festival and promotion calendar, and also look at the weeks just before (build-up) and after (hangover dip).
**Worked example (concept question):** Invented monthly units over three years. Festival lands in Oct, Nov, Oct:

| Year | Oct | Nov |
|---|---|---|
| 1 | 520 (festival) | 400 |
| 2 | 380 | 540 (festival) |
| 3 | 560 (festival) | 410 |

Baseline (non-festival months) = (400 + 380 + 410) / 3 = 396.7. Festival months average 540, an uplift of 540 / 396.7 = 1.36 times. A calendar-month average for October (487) would be wrong in any year where Diwali falls in November. Better: forecast the festival month as baseline x 1.36.
**Alternative / pitfalls:** Do not delete the spike as an outlier; it is real and repeats. With only 2-3 past festivals the uplift is uncertain, so give a range. Promotions that you run yourself (discounts) are a decision, not a forecast; model them separately.
**Likely follow-ups:** 1) *What about daily data?* Flag festival days and the days around them. 2) *Which tools handle holidays?* Models with holiday inputs (for example Prophet, Q43) can, but you still check dates.
**Common mistakes:** Removing festival months as outliers; assuming the same calendar month every year; forgetting the post-festival dip.

### Q29 ⭐⭐ 🟡 Give an example of data leakage in forecasting, such as using a centered moving average or full-sample statistics, and how you avoid it.
**Asked at:** commonly asked (no company-specific report found); mistakes such as random splits and leakage appear in teaching blogs (MetricGate; unverified).
**What the interviewer is checking:** Whether you understand that any feature must be computable using only information available at the time of the forecast.
**Say this in the interview:** "Leakage is when the model sees information from the future that it would not have in real life. A centered moving average uses tomorrow's value to smooth today. Scaling or averaging using the whole series, including the test period, is the same problem. I use trailing windows and compute statistics only on the training data."
**Explain simply:**
- Leakage makes a model look excellent in testing and then fail in real use, because the test was unfair.
- Centered average: day t uses t-1, t and t+1. Fine for describing history, not for a feature in a forecasting model.
- Full-sample statistics: if you standardise or fill gaps using the mean of all 12 months and then split, the test months have influenced the training.
- Fix: split by time first, then compute anything (averages, scalers, seasonal indices) on training rows only.
**Sample data:** Daily orders 50, 52, 51, 90, 53, 52.
**Code (what you write in the interview):**
```python
import pandas as pd

daily_orders = pd.Series([50, 52, 51, 90, 53, 52])

# Centered average: day t uses yesterday, today AND tomorrow (looks into the future)
centered = daily_orders.rolling(3, center=True).mean().round(1)

# Trailing average: day t uses only today and the two days before
trailing = daily_orders.rolling(3).mean().round(1)

print("centered:", centered.tolist())
print("trailing:", trailing.tolist())
```
**Output:**
```text
centered: [nan, 51.0, 64.3, 64.7, 65.0, nan]
trailing: [nan, nan, 51.0, 64.3, 64.7, 65.0]
```
**What it means:** The centered value on day 3 (64.3) already contains the day-4 spike of 90 that nobody knew yet on day 3. The trailing value on day 3 (51.0) is honest. If the target is today's value, even the trailing average that includes today leaks (Q36); use yesterday's.
**Alternative / pitfalls:** Other leakage: using a column that is only known after the event (for example, final monthly headcount to forecast attrition that month), or tuning on the test period.
**Likely follow-ups:** 1) *Is a centered average ever fine?* Yes, for plotting or decomposition of history. 2) *How do you catch leakage?* Suspiciously perfect test accuracy.
**Common mistakes:** Splitting after scaling; centered windows in features; shuffling before splitting.

### Q30 ⭐⭐ 🟡 The HR head asks you to forecast monthly attrition for the next six months from three years of history. How would you approach it, and how will you present the result?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured forecasting scenario added as a gap-fill.
**What the interviewer is checking:** Whether you follow a sensible process: clean the data, set a baseline, validate over time, and communicate a range.
**Say this in the interview:** "I would first define attrition clearly (monthly leavers / average headcount) and plot it. I would try simple methods first, like a seasonal naive and a moving average, test them on the last six known months, and keep the one with the lowest error. I would present a forecast range with a plain-language note on what could change it."
**Explain simply:**
- Steps: confirm the definition and that it was constant over three years (voluntary vs total, contractors); plot and check for seasonality (for example after appraisals or bonus payouts); hold out the last 6 months; compare simple methods; refit on all data; forecast 6 months.
- Three years is only 36 points, so avoid complicated models. Simple methods are hard to beat on small data.
- Present: a line chart (history, forecast, range), the expected number of leavers, and the main assumptions (no restructuring, no big hiring wave, no pay change).
- Add business drivers separately: a planned layoff or a policy change is not in the history.
**Worked example (concept question):** Invented monthly attrition rate (%), 36 months with a mild April and May bump (seeded). Hold out the last 6 months and test three methods (computed by script):

| Method | MAE (percentage points) |
|---|---|
| Naive (repeat last month) | 0.096 |
| 3-month average | 0.222 |
| Seasonal naive (same month last year) | 0.079 |

Seasonal naive wins. Its biggest miss was 0.15 points, so quote a range of about the forecast plus or minus 0.15 points. For example, "expect about 1.5% to 1.7% a month, roughly 30 to 34 leavers on a headcount of 2,000" is easier to act on than one decimal-precise number. This is synthetic data, so the ranking will differ on real data.
**Alternative / pitfalls:** If monthly counts are very small (say under 5 leavers), the series is mostly noise; consider quarterly. Report both rate and count.
**Likely follow-ups:** 1) *What if I only have 3 years?* Stick to simple, seasonal methods. 2) *Can I predict who will leave?* That is a separate classification problem.
**Common mistakes:** One number with no range; ignoring a changed definition; fancy model on 36 points; no holdout check.

### Q31 ⭐⭐ 🟡 When would you move from a moving average or exponential smoothing to a machine learning model with lag features for forecasting, and when would you not?
**Asked at:** commonly asked (no company-specific report found); a gap-fill comparison question.
**What the interviewer is checking:** Whether you choose complexity only when it is justified and know the risks.
**Say this in the interview:** "I start simple and move to machine learning when I have many related series or outside drivers, like price, promotions, weather and holidays, plus enough data to test properly. I would not for a single short series, where a seasonal naive or smoothing is hard to beat and easier to explain."
**Explain simply:**
- A lag feature is an earlier value used as an input column (sales 7 days ago, Q36). A machine learning model (for example a random forest) then learns from those columns and any extra drivers.
- Move up when: many products or stores, useful extra features, several hundred or more rows, and the simple methods leave clear patterns in their errors.
- Stay simple when: one short series, little data, the business wants a clear explanation, or no extra drivers exist.
- Always compare against the naive baseline (Q4) with walk-forward validation (Q26). If the ML model does not clearly beat it, do not use it.
**Alternative / pitfalls:** Tree models cannot extrapolate a trend beyond the range seen in training; remove the trend first (use changes or ratios). Rolling features need care to avoid leakage (Q36). Maintenance cost is higher too.
**Likely follow-ups:** 1) *Biggest risk of ML here?* Leakage and overfitting. 2) *Does ML always win?* No, simple methods often tie on small data.
**Common mistakes:** Jumping to ML for 24 monthly points; random train/test split; not comparing against a baseline.

### Q32 ⭐⭐ 🟡 A forecast missed last quarter's sales by a wide margin and the manager asks why. How do you investigate and explain it?
**Asked at:** commonly asked (no company-specific report found); an explaining-a-miss scenario added as a gap-fill.
**What the interviewer is checking:** Whether you investigate calmly and in a structured way, rather than defend or blame.
**Say this in the interview:** "I would first size the miss, then split it into causes: did the inputs behave as assumed, did something one-off happen, or is the model weak? I would break the gap down by product, region and month, and check what changed against the plan, such as a cancelled promotion or a stockout."
**Explain simply:**
- Size it: forecast minus actual, in units and percent, compared with the model's usual error. A 20% miss when the usual error is 8% is a real signal.
- Check the data: was the actual data complete and was the history correct?
- Check assumptions: promotion dates, pricing, stock availability, competitor action, a festival date shift.
- Split the gap by segment to find where it came from, then attribute it to drivers.
- Explain without jargon and propose a fix: add the missed driver, widen the range, or retire the method.
**Worked example (concept question):** Invented figures. Forecast 1,000 units, actual 800: a miss of 200 units, minus 20%. The usual error is about 8%. Breakdown from the review:

| Cause | Units |
|---|---|
| Planned promotion cancelled | 90 |
| Stockout in two regions | 60 |
| Competitor price cut | 30 |
| Unexplained | 20 |
| Total gap | 200 |

So 180 of the 200 units are explained by events outside the model, and only 20 are unexplained. The fix is to get promotion and stock information into the forecast process, not to rebuild the model.
**Alternative / pitfalls:** One miss does not prove the method is bad; look at errors over many periods (bias, Q23). Do not retrofit the story to fit the data; show evidence for each cause.
**Likely follow-ups:** 1) *How do you prevent a repeat?* Track error monthly and add known drivers. 2) *Was the forecast wrong or the plan?* Separate the two.
**Common mistakes:** Blaming "the model" with no breakdown; defending the number; explaining with jargon.

### Q33 ⭐⭐ 🟡 Common misconception check: a trend line fits the last 12 months with a high R-squared, so the team says it will continue to hold for two more years. What is wrong with that reasoning?
**Asked at:** commonly asked (no company-specific report found); a gap-fill misconception check.
**What the interviewer is checking:** Whether you know that a good fit to the past does not mean the pattern continues, and that R-squared says nothing about extrapolation.
**Say this in the interview:** "R-squared only says how well the line fits the 12 months we already have. It says nothing about month 24 or 36. Growth often slows, markets saturate, and extrapolating far beyond the data is unreliable. I would forecast a short horizon with a range and update it often."
**Explain simply:**
- R-squared (0 to 1) is the share of the up-and-down in the data explained by the line. It measures fit, not forecasting power.
- Twelve points is a short window; a straight line forced through a curve can still score high.
- The further out you project, the wider the real uncertainty, and the line has no range at all.
- Business reasons also change: capacity limits, competitors, market size.
**Worked example (concept question):** Invented monthly sales that grow quickly and then flatten: 100, 108, 115, 121, 126, 130, 133, 135, 136, 137, 137.5, 138. A straight line fits with slope 3.30 a month and R-squared of 0.87 (computed by script). Extending the line 24 months ahead (month 36) gives about 224, but the real series is clearly flattening near 138 (the last month added only 0.5). The line would overstate by over 60%.
**Alternative / pitfalls:** Use a method that allows growth to slow (damped trend), compare against a naive forecast, and test on a later holdout. Judge a model on out-of-sample error, not R-squared.
**Likely follow-ups:** 1) *What horizon is reasonable?* Short, and updated regularly. 2) *What would you show instead?* A range plus scenarios (slow, base, fast).
**Common mistakes:** Using R-squared as proof of future accuracy; long extrapolation; one-line forecasts without a range.

### Q34 ⭐ 🟢 What does ARIMA stand for, and how would you describe it in plain words to a colleague who has only used moving averages?
**Asked at:** commonly asked (no company-specific report found); ARIMA appears in prep-site banks (DevInterview, Analytics Vidhya; unverified).
**What the interviewer is checking:** Whether you can explain the name and its three ideas without jargon.
**Say this in the interview:** "ARIMA is AutoRegressive Integrated Moving Average. It predicts the next value from the recent past values, from recent forecast errors, and after differencing the series to remove a trend."
**Explain simply:**
- AR (autoregressive, order p): the next value depends on the last p values (this month looks like the last two months).
- I (integrated, order d): how many times we difference (this month minus last month) to remove a trend and make the data steady (Q25).
- MA (moving average, order q): the forecast is corrected by the last q forecast errors. This is not the same as the moving average used for smoothing; it averages past mistakes, not past values.
- Written ARIMA(p, d, q). SARIMA adds a yearly seasonal part.
**Alternative / pitfalls:** Choosing p, d, q takes care (ACF plots, Q45, or automatic search). On short series it often does no better than seasonal naive or Holt-Winters (Q37).
**Likely follow-ups:** 1) *What is the d for trending data?* Usually 1. 2) *Does it handle seasonality?* Plain ARIMA does not; use SARIMA.
**Common mistakes:** Treating the "MA" in ARIMA as the smoothing moving average; not differencing trending data; not comparing to a baseline.

### Q35 ⭐ 🟡 Read this code and say what it does and where it could go wrong:
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
m = ExponentialSmoothing(train['sales'], trend='add', seasonal='mul', seasonal_periods=12).fit()
fc = m.forecast(6)
```
Assume `train` is monthly data with one row per month and a date index.
**Asked at:** commonly asked (no company-specific report found); a code-reading question in the style of Holt-Winters prep-bank items (unverified).
**What the interviewer is checking:** Whether you can read the model setup and name realistic failure points.
**Say this in the interview:** "It fits Holt-Winters with an additive trend and multiplicative seasonality on a 12-month cycle and forecasts the next six months. It can fail with under two full years of data, with zeros or negatives in sales, or if the seasonal pattern is not really multiplicative, and I would compare it with a seasonal naive on a holdout."
**Explain simply:**
- `trend='add'`: the trend adds a fixed amount per month. `seasonal='mul'`: seasonal effects multiply the level (December is, say, 12% above normal). `seasonal_periods=12`: pattern repeats every 12 months.
- `.fit()` picks the smoothing weights automatically; `.forecast(6)` returns the next 6 months, labelled with the dates that follow the index.
- Going wrong, verified on statsmodels 0.15.0: with 12 rows it raises "Cannot compute initial seasonals using heuristic method with less than two full seasonal cycles"; 24 rows works. Multiplicative seasonality raises "endog must be strictly positive" if any sales value is 0 or negative.
- Other risks: missing months (gaps) or a date index without a clear monthly frequency; a straight-line trend running on indefinitely; a festival that moves between months (Q28); no forecast range or holdout test shown.
**Sample data:** 36 invented months with a trend and yearly pattern (seeded).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Sample data: 36 months of sales with trend and yearly pattern (seeded)
rng = np.random.default_rng(42)
months = pd.date_range('2022-01-01', periods=36, freq='MS')
pattern = np.array([-10, -8, -3, 0, 3, 6, 8, 6, 2, 0, 5, 12])
pattern = pattern - pattern.mean()
train = pd.DataFrame({'sales': 250 + 2 * np.arange(36) + np.tile(pattern, 3) * 3
                      + rng.normal(0, 3, 36)}, index=months)

m = ExponentialSmoothing(train['sales'], trend='add', seasonal='mul', seasonal_periods=12).fit()
fc = m.forecast(6)
print(fc.round(1))
```
**Output:**
```text
2025-01-01    281.7
2025-02-01    290.6
2025-03-01    312.5
2025-04-01    323.5
2025-05-01    334.4
2025-06-01    346.0
Freq: MS, dtype: float64
```
**What it means:** It forecasts January to June 2025 and keeps rising because of the trend. Judge it by comparing with a seasonal naive on a holdout, not by how smooth the line looks.
**Alternative / pitfalls:** Use `seasonal='add'` if swings stay the same size as sales grow. `trend='add', damped_trend=True` stops the trend running forever (from memory, unverified as an argument name in this run).
**Likely follow-ups:** 1) *How do you test it?* Hold out the last months, compare MAE to seasonal naive. 2) *How do you get a range?* Look at holdout errors or simulate; the basic `.forecast` gives only point values.
**Common mistakes:** Fitting on under two years; ignoring zeros; trusting the output without a baseline.

### Q36 ⭐ 🟡 You create `df['lag_7'] = df['sales'].shift(7)` and `df['roll_7'] = df['sales'].rolling(7).mean()` as features. What leakage risk do you check, and what do you do with the missing rows?
**Asked at:** commonly asked (no company-specific report found); rolling-window and lag features appear in prep-site time series banks (unverified).
**What the interviewer is checking:** Whether you know the rolling window includes today's own value, and that missing rows need care.
**Say this in the interview:** "`shift(7)` is safe, it is last week's value. `rolling(7).mean()` includes today's sales, which is the thing I am predicting, so that leaks the answer. I would use `shift(1)` first so the window ends yesterday, and drop the early rows that have no history rather than fill them with zero."
**Explain simply:**
- A feature must be known at forecast time. If the target is today's sales, today's sales cannot be an ingredient.
- `shift(7)` moves values down 7 rows: the first 7 rows have no value (NaN, meaning missing).
- `rolling(7).mean()` averages the current row and 6 before it: it includes today.
- Fix: `df['sales'].shift(1).rolling(7).mean()` averages the 7 days up to yesterday. Missing rows at the start: drop them with `dropna()`; filling with 0 would teach the model false values.
**Sample data:** 12 days of invented sales.
**Code (what you write in the interview):**
```python
import pandas as pd

df = pd.DataFrame({'sales': [112, 82, 114, 91, 116, 91, 97, 106, 85, 102, 100, 111]})

# Safe: sales exactly 7 days ago
df['lag_7'] = df['sales'].shift(7)

# Leaky if the target is today's sales: this average includes today
df['roll_7_leaky'] = df['sales'].rolling(7).mean()

# Safe: average of the 7 days up to yesterday
df['roll_7_safe'] = df['sales'].shift(1).rolling(7).mean()

print(df.round(1))

# Drop the early rows that have no history (do not fill them with 0)
model_data = df.dropna()
print("rows kept:", len(model_data), "of", len(df))
```
**Output:**
```text
    sales  lag_7  roll_7_leaky  roll_7_safe
0     112    NaN           NaN          NaN
1      82    NaN           NaN          NaN
2     114    NaN           NaN          NaN
3      91    NaN           NaN          NaN
4     116    NaN           NaN          NaN
5      91    NaN           NaN          NaN
6      97    NaN         100.4          NaN
7     106  112.0          99.6        100.4
8      85   82.0         100.0         99.6
9     102  114.0          98.3        100.0
10    100   91.0          99.6         98.3
11    111  116.0          98.9         99.6
rows kept: 5 of 12
```
**What it means:** Row 7 uses 100.4 in the safe version, which is the leaky average one row earlier, so it uses only past days. Dropping missing rows keeps 5 of 12 here; with real data the loss of the first week is small.
**Alternative / pitfalls:** Also split by time, not randomly, and compute any scaling on training rows only (Q29).
**Likely follow-ups:** 1) *Why not fill NaN with the mean?* The mean uses future values; for a few rows, drop. 2) *What if I forecast 7 days ahead?* Shift features by at least 7.
**Common mistakes:** Rolling without shift; filling early NaNs with 0; random split afterwards.

### Q37 ⭐ 🟡 What is Holt-Winters (triple exponential smoothing), and which of trend and seasonality does each of its three smoothing parts handle?
**Asked at:** commonly asked (no company-specific report found); Holt-Winters appears in prep-site time series banks (DevInterview, techprep; unverified).
**What the interviewer is checking:** Whether you know that the three parts are level, trend and seasonality, each with its own weight.
**Say this in the interview:** "Holt-Winters is exponential smoothing with three parts: one for the level, one for the trend and one for the seasonal pattern. Each has its own smoothing weight between 0 and 1: higher means react faster to new data."
**Explain simply:**
- Simple exponential smoothing (Q21) tracks only the level. Holt's method adds a trend. Holt-Winters adds seasonality, so it is "triple".
- Alpha: level (the current baseline). Beta: trend (how quickly the slope updates). Gamma: seasonality (how quickly the seasonal pattern updates).
- Seasonality can be additive (fixed amount) or multiplicative (a percentage).
- In statsmodels the fitted weights are `smoothing_level`, `smoothing_trend`, `smoothing_seasonal` (checked on 0.15.0; Q35 uses it).
**Alternative / pitfalls:** Needs at least two full cycles of data. Weights close to 0 mean a very slow-changing part. If the weights land on 0 or 1 (the edges), the fit may be unreliable.
**Likely follow-ups:** 1) *Without a trend?* Set `trend=None`. 2) *Which one for flat data with seasonality?* Level plus seasonality only.
**Common mistakes:** Calling beta the seasonal part; applying it to data with fewer than two cycles; no baseline comparison.

### Q38 ⭐ 🟡 How would you forecast demand for a new product with no sales history, and what do you tell the business about confidence?
**Asked at:** commonly asked; cold-start forecasting appears in Dataford and other prep-page snippets (unverified); no company-specific report found.
**What the interviewer is checking:** Whether you can use analogies and judgement and be honest about uncertainty.
**Say this in the interview:** "With no history I borrow from similar products: same category, price band and launch season. I take their first-weeks sales, adjust for differences, and give a low, base and high scenario. I tell the business the range is wide at first and will narrow as real sales come in."
**Explain simply:**
- Analogue method: pick 3-5 comparable past launches and use their early sales curve.
- Adjust for price, marketing spend, number of stores and season.
- Add other signals: pre-orders, search interest, test-market results, expert input.
- Present scenarios, not one number, and update weekly after launch (the first two to four weeks of real data are very informative).
**Worked example (concept question):** Invented first-quarter units of three similar launches: 300, 450 and 600. Average 450; present low 300, base 450, high 600. After four weeks, if actual sales run at a pace consistent with the high case, move the base toward 600.
**Alternative / pitfalls:** Analogues from a different customer segment mislead. Do not hide the uncertainty behind a point forecast. Plan stock flexibly (small first order, fast reorder).
**Likely follow-ups:** 1) *How wide is the range?* Wide, so say so; it narrows with data. 2) *When do you switch to a normal model?* After enough weeks of actual sales.
**Common mistakes:** Giving one confident number; using one analogue only; not updating after launch.

### Q39 ⭐ 🟡 Stockouts hid true demand for a fast-selling item for two weeks. How does that distort the history you forecast from, and what would you do?
**Asked at:** commonly asked; censored demand from stockouts appears in prep-page snippets (futurevocation, Dataford; unverified); no company-specific report found.
**What the interviewer is checking:** Whether you separate sales (what was sold) from demand (what customers wanted).
**Say this in the interview:** "Sales are capped by stock, so the history understates demand and a forecast built from it would be too low and make the next stockout more likely. I mark the stockout days, estimate the missing demand, and forecast from the corrected history."
**Explain simply:**
- Sales data is censored: it shows what you sold, not what people tried to buy. Zero or low sales on a stockout day does not mean low demand.
- Options: exclude stockout days and treat them as missing; replace them with demand from similar in-stock days (same weekday); or scale up a partial day (for example, sales before the item ran out).
- Record stock levels so this is detectable in future.
- Tell the business the correction is an estimate.
**Worked example (concept question):** Invented figures. On normal days the item sells 100 a day. During 14 stockout days, stock ran out around 11am, with 55 units sold per day. Forecasting from the raw history uses 55 (45% too low). If 55% of daily sales usually happen before 11am, estimated demand = 55 / 0.55 = 100 a day. Total for the 14 days: 770 recorded vs about 1,400 estimated, so 630 units of demand were hidden.
**Alternative / pitfalls:** Over-correcting also misleads (some customers would switch to another product, so demand is not all lost). Check with supply-chain data.
**Likely follow-ups:** 1) *Why not just average?* The stockout days drag it down. 2) *How else can you detect it?* Stock-on-hand data, or hourly sales stopping.
**Common mistakes:** Treating sales as demand; keeping zeros as "real" demand; no stock data.

### Q40 ⭐ 🟡 Compute 3-day moving averages and say what an outlier does to them.
Daily orders: 50, 52, 51, 90, 53, 52. Compute the average for days 3 to 6.
**Asked at:** commonly asked (no company-specific report found); moving-average calculations appear in fresher forecasting prep (HelloIntern; unverified).
**What the interviewer is checking:** Whether you can do the arithmetic and notice the spike's effect.
**Say this in the interview:** "Each value is the average of today and the two days before. The 90 pushes up three averages in a row, days 4, 5 and 6, from about 51 to about 65, then drops out."
**Explain simply:**
- Day 3 = (50 + 52 + 51) / 3 = 51.0. Day 4 = (52 + 51 + 90) / 3 = 64.33. Day 5 = (51 + 90 + 53) / 3 = 64.67. Day 6 = (90 + 53 + 52) / 3 = 65.0.
- An outlier (a one-off extreme value) affects every window that contains it, so the average stays high for 3 days after one odd day.
- Median-based smoothing, or capping a known one-off, reduces the effect.
**Sample data:** Daily orders: 50, 52, 51, 90, 53, 52.
**Code (what you write in the interview):**
```python
import pandas as pd

daily_orders = pd.Series([50, 52, 51, 90, 53, 52], index=range(1, 7))

# Average of today and the two days before, so the first value is on day 3
moving_average = daily_orders.rolling(3).mean().round(2)
print(moving_average.dropna())
```
**Output:**
```text
3    51.00
4    64.33
5    64.67
6    65.00
dtype: float64
```
**What it means:** One spike lifted the smoothed level from 51 to about 65 for three days, although normal orders stayed near 52. If used as a forecast, that would over-forecast.
**Alternative / pitfalls:** Check whether the 90 is real (a promotion) or an error before deciding to remove it.
**Likely follow-ups:** 1) *What if the window were 7 days?* Smaller bump per day, but it lasts 7 days. 2) *Median instead?* Resists the spike.
**Common mistakes:** Starting the average at day 1; deleting outliers without checking; forgetting the spike remains in later windows.

### Q41 ⭐ 🟡 Daily orders show weekly seasonality. Given two weeks of data, compute the Monday index and use it to forecast next Monday, assuming the weekly average level stays at 100.
Week 1 Mon 80, Tue 100, Wed 110, Thu 105, Fri 120, Sat 95, Sun 90. Week 2 Mon 84, Tue 104, Wed 106, Thu 111, Fri 118, Sat 99, Sun 96. Use the average over both weeks of all 14 days as the base.
**Asked at:** commonly asked (no company-specific report found); a gap-fill weekday-index question.
**What the interviewer is checking:** Whether you can build a seasonal index and apply it.
**Say this in the interview:** "The Monday index is the average Monday divided by the average of all days: 82 / 101.29 = 0.81. Next Monday is the expected level of 100 times 0.81, so about 81 orders."
**Explain simply:**
- A seasonal index (here by weekday) says how a day compares with the average day. 0.81 means Mondays run about 19% below an average day.
- Base = all 14 days averaged = 101.29. Monday average = (80 + 84) / 2 = 82.
- Forecast = level x index = 100 x 0.81 = 80.96, about 81.
- Note: the question's level of 100 is slightly below the two-week average of 101.29; that is the stated assumption.
**Sample data:** The 14 values from the question.
**Code (what you write in the interview):**
```python
import pandas as pd

orders = pd.Series([80, 100, 110, 105, 120, 95, 90,
                    84, 104, 106, 111, 118, 99, 96])

# Base = average of all 14 days
base = orders.mean()

# Average of the two Mondays (positions 0 and 7)
monday_average = orders.iloc[[0, 7]].mean()

monday_index = monday_average / base
next_monday = 100 * monday_index

print("base", round(base, 2), "| Monday average", monday_average)
print("Monday index", round(monday_index, 3), "| forecast", round(next_monday, 1))
```
**Output:**
```text
base 101.29 | Monday average 82.0
Monday index 0.81 | forecast 81.0
```
**What it means:** Plan for about 81 orders next Monday, not 100. Tell a manager "about 80 to 85" since two weeks of data is a thin base.
**Alternative / pitfalls:** Two weeks gives one pair of Mondays per index; more weeks make it stable. A holiday in either week would distort it.
**Likely follow-ups:** 1) *Do all indices sum to 7?* Yes, they average 1. 2) *How many weeks would you want?* Eight or more.
**Common mistakes:** Dividing by 100 instead of the data average; using one Monday only; not checking for holidays.

### Q42 ⭐ 🟡 You want to paste last quarter's sales data into a public AI chatbot to get a forecast. What privacy and accuracy checks do you make first, and how do you verify the output?
**Asked at:** commonly asked (no company-specific report found); an AI-tool gap-fill question. Policy and product points below are general principles, from memory, unverified; confirm with your company's IT, security and legal teams and the tool's official documentation.
**What the interviewer is checking:** Whether you protect company data and do not trust AI numbers blindly.
**Say this in the interview:** "First I check whether company policy allows it at all. Sales data may be confidential, so I would remove customer names and anything personal and prefer an approved company tool. Then I treat the chatbot's forecast as a draft: I rebuild it with a simple baseline and check it."
**Explain simply:**
- Privacy: do not paste employee or customer personal data (names, IDs, salaries) into public tools. Commercially sensitive figures can also be confidential. Use approved, enterprise tools and aggregated or anonymised data where policy allows. Rules like India's DPDP Act or GDPR may apply (confirm with legal; unverified here).
- Accuracy: a chatbot is a language tool, not a forecasting engine. It can produce a plausible-looking number with no honest method, may mis-add, and may not state assumptions.
- Example prompt (text only): "Here are monthly sales (anonymised). Suggest a simple forecasting method, explain the assumptions, and write Python for it." Asking for the method and code (which you can run and check) is safer than asking for the number.
- Verify: re-compute totals and row counts; compare with a seasonal naive and a moving average; run a holdout test; check the forecast against known events; ask for the range and assumptions.
**Alternative / pitfalls:** A forecast you cannot reproduce should not go to a manager. Keep a record of the data and method used.
**Likely follow-ups:** 1) *What if the tool is approved?* Still verify the output. 2) *Can you share dummy data?* Yes, anonymised or invented data with the same shape.
**Common mistakes:** Pasting raw data with names; trusting the number; not reproducing the result independently.

### Q43 ⭐ 🟡 When is Prophet a sensible choice for an analyst, and what would you still check about its output?
**Asked at:** commonly asked (no company-specific report found); a gap-fill tool question. Prophet is not installed in this environment, so the points below are from memory, unverified; confirm with Prophet's official documentation.
**What the interviewer is checking:** Whether you know when a ready-made tool helps and that you still validate it.
**Say this in the interview:** "Prophet suits business series with strong yearly or weekly seasonality, holidays and a few years of daily or weekly data, when you want a quick, explainable baseline. I would still check it against a naive forecast on a holdout, look at the components, and not trust the range blindly."
**Explain simply:**
- Prophet (an open-source forecasting library from Meta, from memory) fits trend, seasonality and holiday effects, and handles missing days and outliers reasonably (from memory).
- Good fit: daily sales with weekly and yearly patterns, holiday or festival effects, an analyst who wants low effort.
- Less suited: very short series, series with irregular events, or when you need the best accuracy on many series without checking.
- Still check: a time-ordered holdout and comparison with seasonal naive, whether the trend changepoints look sensible, whether holiday dates are correct, whether the forecast range is realistic, and the data for gaps.
**Alternative / pitfalls:** Easy-to-run does not mean accurate. Simple methods (Q4, Q37) are often as good. Version and install issues are common in practice (from memory).
**Likely follow-ups:** 1) *Does it need stationarity?* No (from memory), unlike ARIMA. 2) *Where do you put festival dates?* In the holiday table (Q28).
**Common mistakes:** Running it on 20 points; trusting the default; no baseline comparison.

### Q44 ⭐ 🔴 Why is a trend estimated with a 2x12 centered moving average for monthly data, rather than a plain 12-month average?
**Asked at:** commonly asked (no company-specific report found); the centered 2xm moving average appears in prep-site time series banks (unverified).
**What the interviewer is checking:** Whether you understand the alignment problem of an even-length window.
**Say this in the interview:** "A 12-month average has no middle month: it sits half a month between month 6 and 7. To centre it on a real month I average two neighbouring 12-month averages. That also gives the ends half weight, and it removes the yearly seasonality cleanly."
**Explain simply:**
- Averaging 12 months covers a full year, so each month appears once and the seasonal ups and downs cancel out, leaving the trend.
- With an even window like 12, the centre falls between two months (6.5). Plotting it against month 7 or 6 is half a month off.
- 2x12: take the 12-month average ending at month 12 and the one ending at month 13, then average them. The result is centred on month 7.
- Weights: first and last of 13 months get 1/24, the 11 in between get 1/12; they sum to 1.
**Sample data:** Months 1 to 24 with values 1 to 24 (rising by 1 a month).
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.Series(range(1, 25), index=range(1, 25))   # months 1 to 24, rising by 1

# Plain 12-month average: result sits at month 12 but is centred on month 6.5
plain = sales.rolling(12).mean()

# 2x12: average two neighbouring 12-month averages, then shift back 6 months
centered_trend = plain.rolling(2).mean().shift(-6)

print("plain 12-month average at month 12:", plain[12], "(centre is 6.5)")
print("2x12 trend at month 7:", centered_trend[7])
```
**Output:**
```text
plain 12-month average at month 12: 6.5 (centre is 6.5)
2x12 trend at month 7: 7.0
```
**What it means:** For a perfectly straight rise the true level at month 7 is 7. The 2x12 gives exactly 7.0, whereas the plain average gives 6.5 and is labelled at the wrong month.
**Alternative / pitfalls:** The first 6 and last 6 months have no value (the trend ends early). This is a description of history, not a forecast. Quarterly data would use 2x4. For odd windows (3, 7) a simple centered average is already centred.
**Likely follow-ups:** 1) *Why lose the ends?* Needs 6 months on each side. 2) *Where is it used?* Classical decomposition (Q27).
**Common mistakes:** Using a plain 12-month average and calling it centered; forgetting the ends; using it as a forecasting feature (leakage, Q29).

### Q45 ⭐ 🔴 What do the autocorrelation function (ACF) plot and a lag spike at 12 tell you about monthly data?
**Asked at:** commonly asked (no company-specific report found); ACF appears in prep-site time series banks (Analytics Vidhya, DevInterview; unverified).
**What the interviewer is checking:** Whether you can read an ACF plot and connect lag 12 to yearly seasonality.
**Say this in the interview:** "Autocorrelation is how strongly the series is related to itself some months earlier. A tall spike at lag 12 means this month looks like the same month a year ago, which signals yearly seasonality."
**Explain simply:**
- Lag k means "k months ago". The ACF plot shows the correlation (a score from -1 to 1) between the series and itself shifted by each lag.
- Bars outside the shaded band (roughly plus or minus 2 / square root of the number of points) are unlikely to be chance.
- A spike at 12 (and 24) means a yearly cycle. Slowly falling bars at lags 1, 2, 3 usually mean a trend.
- Use it to decide on seasonal differencing or seasonal ARIMA terms (Q34), and to check that residuals are clean after a model.
**Sample data:** 5 years of invented monthly sales with a yearly pattern (seeded).
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

# Sample data: 5 years of monthly sales with a yearly pattern (seeded)
rng = np.random.default_rng(42)
pattern = np.array([-10, -8, -3, 0, 3, 6, 8, 6, 2, 0, 5, 12])
pattern = pattern - pattern.mean()
sales = pd.Series(100 + np.tile(pattern, 5) * 2 + rng.normal(0, 3, 60))

correlations = acf(sales, nlags=12)
rough_limit = 2 / np.sqrt(len(sales))

print("lag 1:", round(correlations[1], 2), "| lag 6:", round(correlations[6], 2),
      "| lag 12:", round(correlations[12], 2))
print("rough noise limit:", round(rough_limit, 2))
```
**Output:**
```text
lag 1: 0.31 | lag 6: -0.26 | lag 12: 0.79
rough noise limit: 0.26
```
**What it means:** Lag 12 is 0.79, far above the 0.26 noise limit, so this month is strongly tied to the same month a year earlier: clear yearly seasonality. Lag 6 is negative because half a year apart is the opposite season.
**Alternative / pitfalls:** A trend also inflates ACF at many lags, so remove the trend first. The `plot_acf` function draws the chart (needs matplotlib; not run here). With few years of data the bars are noisy.
**Likely follow-ups:** 1) *What is PACF?* The correlation at a lag after removing the effect of shorter lags. 2) *What would a flat ACF mean?* Mostly random noise.
**Common mistakes:** Reading every small bar as a pattern; ignoring a trend; confusing lag 12 with 12 days on daily data.

