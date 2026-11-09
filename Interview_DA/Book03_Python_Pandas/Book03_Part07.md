# Book 3 — Python & pandas for Analysts | Part 7: Dates & Time Series in pandas 🟡

**Target:** 40 questions | **Actual:** 46 questions
**Scope:** parsing and extracting dates, date arithmetic, filtering by date, resampling, shift, rolling windows, month-over-month growth and time zones in pandas, with HR and sales examples.

### Q1 ⭐⭐⭐ 🟢 How do you convert a text column of dates to a proper datetime column in pandas?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Write code to read a CSV with a joining_date column and make pandas parse it as a date while loading.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 How do you extract the year, month, day and weekday name from a datetime column using the .dt accessor?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Write code to calculate the number of days between date_of_joining and date_of_exit for each employee.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 Write code to calculate each employee's tenure in years from the joining date to today.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Write code to find total monthly sales from a table with order_date and amount columns.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 What does errors="coerce" do in pd.to_datetime, and how do you find which rows failed to convert?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 What is the difference between resample and groupby in pandas for time-based aggregation?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Write code to resample daily attendance records to monthly totals.
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Write code to calculate month-over-month percentage growth in sales.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you calculate a 7-day rolling average of daily orders in pandas?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐ 🟢 How do you filter a DataFrame for rows between two dates?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐ 🟢 How do you set a date column as the index, and why does that help with time series?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 How do you create a range of dates in pandas using pd.date_range?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 How do you find the earliest and latest date in a column and the span between them?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 What is the difference between datetime64, Timestamp and Timedelta in pandas?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 How do you check whether a column is stored as text or as datetime?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 Write code to add a new column that flags weekend dates (Saturday or Sunday) in an attendance table.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 Write code to count hires per month from a joining_date column.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 How do you format a datetime column as a string such as 05-Nov-2026 using strftime?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 How do you handle dates like 03/04/2026 that could be day-first or month-first when parsing?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How do you parse a date column stored in a custom format such as 20260315 or 15-Mar-26?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 What is the shift function in pandas, and how do you use it to compare each day with the previous day?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you use pct_change on monthly data, and why is the first value NaN?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Write code to find the day of the week with the highest average sales.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Write code to compute a cumulative sum of sales within each year.
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Write code to group data by quarter and by financial year (April to March) in pandas.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you find missing dates in a daily series and fill them in with zero?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Write code to find employees who joined in the last 90 days.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Write code to compute monthly attrition rate from joining and exit date columns.
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Why do I get a "Can only use .dt accessor with datetimelike values" error, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q32 ⭐ 🟡 What is the difference between rolling, expanding and ewm windows?
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🟡 What is the difference between resample and asfreq?
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🟡 How do you fill gaps after resampling using ffill, bfill or interpolate?
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🟡 How do you subtract or add months and days to a date column using Timedelta and DateOffset?
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟡 How do you find the last working day or month-end date for each row using pandas offsets?
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 Write code to calculate working days between two dates, excluding weekends, using numpy busday_count.
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Write code to find the gap in days between consecutive events (for example logins) for each employee.
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 How do you compare this month with the same month last year in pandas?
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 How do you handle time zones in pandas using tz_localize and tz_convert?
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 How do you convert Unix timestamps (epoch seconds) to readable dates in pandas?
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 How do you use pd.Grouper to group by month while also grouping by another column?
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 How do you detect and handle outliers or spikes in a daily time series?
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 How do you split a time series into train and test sets without shuffling, and why does order matter?
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 What is a Period in pandas, and how does it differ from a Timestamp?
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 What is the difference between closed and label arguments in resample, and when do they matter?
<!-- ANSWER_PENDING -->
