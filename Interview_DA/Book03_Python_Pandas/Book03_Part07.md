# Book 3 — Python & pandas for Analysts | Part 7: Dates & Time Series in pandas 🟡

**Target:** 40 questions | **Actual:** 46 questions
**Scope:** parsing and extracting dates, date arithmetic, filtering by date, resampling, shift, rolling windows, month-over-month growth and time zones in pandas, with HR and sales examples.

### Q1 ⭐⭐⭐ 🟢 How do you convert a text column of dates to a proper datetime column in pandas?
**Asked at:** commonly asked (no company-specific report found); to_datetime appears in the Educative and AskPython pandas lists (snippet only).
**What the interviewer is checking:** Do you know dates read from files are often plain text, and that `pd.to_datetime` fixes that.
**Say this in the interview:** "I use `pd.to_datetime` on the column and assign it back. After that pandas treats it as a real date, so I can sort, subtract and pull out the month or year."
**Explain simply:**
- **Text (object/str) column:** pandas sees "2024-01-15" as letters, not a date, so date maths fails.
- **datetime column:** a real date type; you can add days, find gaps, group by month.
- **Assign it back:** `to_datetime` returns a new column; it does not change the old one by itself.
**Sample data:** three joining dates stored as text.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"joining_date": ["2024-01-15", "2024-03-01", "2025-07-20"]})

# Convert the text column to a real datetime column
employees["joining_date"] = pd.to_datetime(employees["joining_date"])

print(employees.dtypes)
```
**Output:**
```
joining_date    datetime64[us]
dtype: object
```
**What it means:** the column is now a datetime type (older pandas shows `datetime64[ns]`; same idea, different time precision).
**Likely follow-ups:**
- *What if some values are bad?* Use `errors="coerce"` (Q7).
- *What if the format is unusual?* Pass `format=` (Q22) or `dayfirst=True` (Q21).
**Common mistakes:** not assigning the result back, so the column stays text; assuming a CSV date column is already a date.

### Q2 ⭐⭐⭐ 🟢 Write code to read a CSV with a joining_date column and make pandas parse it as a date while loading.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know `parse_dates` in `read_csv`, so you skip a separate conversion step.
**Say this in the interview:** "I pass `parse_dates=['joining_date']` to `read_csv`. Pandas converts that column to datetime while loading."
**Explain simply:**
- **parse_dates:** a list of column names that pandas should turn into dates on load.
- Without it, the column loads as text and you must call `to_datetime` yourself.
- It saves a line and avoids forgetting the conversion.
**Sample data:** `emp.csv` has three rows: `101,Asha,2024-01-15`, `102,Ravi,2024-03-01`, `103,Meena,2025-07-20` (columns emp_id, name, joining_date).
**Code (what you write in the interview):**
```python
import pandas as pd

# parse_dates turns joining_date into a datetime while loading
employees = pd.read_csv("emp.csv", parse_dates=["joining_date"])

print(employees.dtypes)
```
**Output:**
```
emp_id                   int64
name                       str
joining_date    datetime64[us]
dtype: object
```
**What it means:** `joining_date` loaded as a date, not text (`name` shows `str` in pandas 3; older versions show `object`).
**Likely follow-ups:**
- *What if the format is day-first?* Add `dayfirst=True`, or load as text and use `to_datetime(..., format=...)`.
- *What about several date columns?* List them all: `parse_dates=["joining_date", "exit_date"]`.
**Common mistakes:** passing a string instead of a list; expecting `parse_dates` to cope with messy values (it leaves them as text, so check `dtypes`).

### Q3 ⭐⭐⭐ 🟢 How do you extract the year, month, day and weekday name from a datetime column using the .dt accessor?
**Asked at:** commonly asked (no company-specific report found); date parts are a standard item in datetime question lists (Educative, snippet only).
**What the interviewer is checking:** Do you know `.dt` and its common parts.
**Say this in the interview:** "Once the column is datetime, I use `.dt.year`, `.dt.month`, `.dt.day` and `.dt.day_name()`. The `.dt` accessor is the doorway to date parts."
**Explain simply:**
- **Accessor:** a prefix (`.dt`) that opens a group of date tools on a column, like `.str` for text.
- `year`, `month`, `day` are attributes (no brackets); `day_name()` is a method (brackets).
- It only works on a datetime column, not text (see Q31).
**Sample data:** three joining dates.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"joining_date": pd.to_datetime(["2024-01-15", "2024-03-01", "2025-07-20"])})

employees["year"] = employees["joining_date"].dt.year
employees["month"] = employees["joining_date"].dt.month
employees["day"] = employees["joining_date"].dt.day
employees["weekday"] = employees["joining_date"].dt.day_name()

print(employees)
```
**Output:**
```
  joining_date  year  month  day weekday
0   2024-01-15  2024      1   15  Monday
1   2024-03-01  2024      3    1  Friday
2   2025-07-20  2025      7   20  Sunday
```
**What it means:** each joining date is split into year, month, day and the name of the weekday.
**Likely follow-ups:**
- *How do I get the month name?* `.dt.month_name()`.
- *What does `.dt.weekday` give?* A number, Monday = 0 to Sunday = 6.
**Common mistakes:** writing `day_name` without brackets; using `.dt` on a text column; forgetting that weekday numbers start at 0 for Monday.

### Q4 ⭐⭐⭐ 🟢 Write code to calculate the number of days between date_of_joining and date_of_exit for each employee.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Date subtraction gives a Timedelta, and you know how to turn it into a plain number.
**Say this in the interview:** "I subtract the two date columns, which gives a Timedelta, then take `.dt.days` to get a whole number. Employees still working have no exit date, so they show NaN."
**Explain simply:**
- **Timedelta:** a length of time, such as "366 days".
- **.dt.days:** the whole-day part of that length, as a number.
- **NaT (Not a Time):** the empty value for dates. Date minus NaT gives NaN, which is right: the person has not left.
**Sample data:** Asha and Meena left; Ravi is still working (no exit date).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "date_of_joining": pd.to_datetime(["2024-01-15", "2024-03-01", "2025-07-20"]),
    "date_of_exit": pd.to_datetime(["2025-01-15", None, "2025-09-18"]),
})

# Subtracting two date columns gives a Timedelta; .dt.days keeps the whole days
employees["days_worked"] = (employees["date_of_exit"] - employees["date_of_joining"]).dt.days

print(employees)
```
**Output:**
```
    name date_of_joining date_of_exit  days_worked
0   Asha      2024-01-15   2025-01-15        366.0
1   Ravi      2024-03-01          NaT          NaN
2  Meena      2025-07-20   2025-09-18         60.0
```
**What it means:** Asha worked 366 days (2024 was a leap year); Ravi shows NaN because he has not exited.
**Likely follow-ups:**
- *How would you include current employees?* Fill the exit date with today: `date_of_exit.fillna(pd.Timestamp.today())`.
- *Why is the number a decimal?* NaN forces the column to float.
**Common mistakes:** doing this on text columns (error); forgetting `.dt.days` and printing "366 days 00:00:00"; filling missing exits with 0.

### Q5 ⭐⭐⭐ 🟢 Write code to calculate each employee's tenure in years from the joining date to today.
**Asked at:** commonly asked (no company-specific report found); a standard HR-analytics task.
**What the interviewer is checking:** Can you get "today", subtract, and convert days to years.
**Say this in the interview:** "I take today's date, subtract the joining date to get days, and divide by 365.25 so leap years are covered. I round to one decimal."
**Explain simply:**
- **Tenure:** how long someone has been with the company.
- **pd.Timestamp.today():** the current date and time; `.normalize()` sets the time to midnight so only the date counts.
- **365.25:** average days in a year, because every fourth year has 366.
- The answer is approximate (decimal years), which is normally fine for reports.
**Sample data:** three joining dates (the output below was run on 9 Nov 2026; your numbers change each day).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "joining_date": pd.to_datetime(["2020-01-15", "2022-03-01", "2025-07-20"]),
})

today = pd.Timestamp.today().normalize()

# Days since joining, divided by 365.25 to allow for leap years
employees["tenure_years"] = ((today - employees["joining_date"]).dt.days / 365.25).round(1)

print(employees)
```
**Output:**
```
    name joining_date  tenure_years
0   Asha   2020-01-15           6.8
1   Ravi   2022-03-01           4.7
2  Meena   2025-07-20           1.3
```
**What it means:** Asha has been here about 6.8 years, Meena about 1.3.
**Likely follow-ups:**
- *How do you get whole completed years?* Use `// 365.25`-style floor division, or `np.floor`.
- *For people who left?* Use the exit date instead of today where it exists.
**Common mistakes:** dividing by 365 and drifting over long periods; using `.dt.year` differences (2026 minus 2020 ignores the month); leaving the time part in "today".

### Q6 ⭐⭐⭐ 🟡 Write code to find total monthly sales from a table with order_date and amount columns.
**Asked at:** commonly asked (no company-specific report found); a month-wise sales scenario appears in an informal Telegram analytics channel post (snippet only).
**What the interviewer is checking:** Can you group rows by the month of a date and sum.
**Say this in the interview:** "I turn each order date into its month with `.dt.to_period('M')`, group by that, and sum the amount. Resample is another way."
**Explain simply:**
- **Period "M":** a whole month (2026-01) instead of an exact day, so all January orders share one label.
- **groupby then sum:** pile the rows by month, then add each pile.
- The date column must already be datetime (Q1).
**Sample data:** five orders across January to March.
**Code (what you write in the interview):**
```python
import pandas as pd

orders = pd.DataFrame({
    "order_date": pd.to_datetime(["2026-01-05", "2026-01-20", "2026-02-11", "2026-03-02", "2026-03-25"]),
    "amount": [1000, 500, 1200, 800, 700],
})

# Group by the month of each order and add up the amounts
monthly_sales = orders.groupby(orders["order_date"].dt.to_period("M"))["amount"].sum()

print(monthly_sales)
```
**Output:**
```
order_date
2026-01    1500
2026-02    1200
2026-03    1500
Freq: M, Name: amount, dtype: int64
```
**What it means:** total sales were 1500 in January, 1200 in February and 1500 in March.
**Alternative:** `orders.resample("ME", on="order_date")["amount"].sum()` gives the same totals labelled by month-end date (2026-01-31). It also shows months with no orders as 0.
**Likely follow-ups:**
- *Why not group by `.dt.month`?* It mixes January 2025 and January 2026 together.
- *Why "ME" and not "M"?* In pandas 3 "M" raises an error (verified); use "ME" for month-end.
**Common mistakes:** grouping by month number across several years; running it on a text date column.

### Q7 ⭐⭐⭐ 🟡 What does errors="coerce" do in pd.to_datetime, and how do you find which rows failed to convert?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to clean messy dates without the code crashing, and how to audit what failed.
**Say this in the interview:** "`errors='coerce'` turns any value it cannot read into NaT, the empty date, instead of raising an error. To find failures I look for rows where the new column is empty but the original was not."
**Explain simply:**
- **Default (`errors="raise"`):** one bad value stops everything with an error.
- **coerce:** bad values quietly become NaT (Not a Time).
- **Why the extra check:** NaT also appears for values that were already blank, so compare with the original.
- Always review the failed rows; do not just drop them.
**Sample data:** one valid date, an impossible date (31 Feb), a text note, another valid date.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"joining_date": ["2024-01-15", "31/02/2024", "not available", "2025-07-20"]})

# Bad values become NaT (Not a Time) instead of crashing
employees["joining_clean"] = pd.to_datetime(employees["joining_date"], errors="coerce")

# Rows that had text but now have NaT are the failures
failed_rows = employees[employees["joining_clean"].isna() & employees["joining_date"].notna()]

print(failed_rows)
```
**Output:**
```
    joining_date joining_clean
1     31/02/2024           NaT
2  not available           NaT
```
**What it means:** two rows could not be converted; I can now fix them or ask the data owner.
**Likely follow-ups:**
- *What does `errors="ignore"` do?* It was removed in pandas 3 (from memory, unverified); use coerce.
- *What if many rows fail?* Check the format; the data may be day-first (Q21).
**Common mistakes:** coercing and moving on without checking the NaT rows; counting NaT without comparing to the original blanks.

### Q8 ⭐⭐⭐ 🟡 What is the difference between resample and groupby in pandas for time-based aggregation?
**Asked at:** commonly asked (no company-specific report found); resampling and groupby both appear in pandas practice sets (Udemy, snippet only).
**What the interviewer is checking:** Do you know resample is a time-aware groupby that keeps empty periods.
**Say this in the interview:** "Resample is groupby built for dates. It needs a datetime, cuts the timeline into regular buckets like months, and includes empty buckets. A normal groupby only shows groups that exist in the data."
**Explain simply:**
- **groupby:** groups by any column value; skips combinations with no rows.
- **resample:** groups by regular time buckets (day, week, month); fills gaps with 0 or NaN.
- Resample needs a datetime index or `on="date_column"`.
- Use groupby when you also group by non-date things; use resample for a clean, continuous timeline.
**Sample data:** orders in January and March, none in February.
**Code (what you write in the interview):**
```python
import pandas as pd

orders = pd.DataFrame({
    "order_date": pd.to_datetime(["2026-01-05", "2026-01-20", "2026-03-02", "2026-03-25"]),
    "amount": [1000, 500, 800, 700],
})

# groupby: only months that exist in the data
by_groupby = orders.groupby(orders["order_date"].dt.to_period("M"))["amount"].sum()

# resample: every month in the range, empty ones shown as 0
by_resample = orders.resample("ME", on="order_date")["amount"].sum()

print(by_groupby)
print(by_resample)
```
**Output:**
```
order_date
2026-01    1500
2026-03    1500
Freq: M, Name: amount, dtype: int64
order_date
2026-01-31    1500
2026-02-28       0
2026-03-31    1500
Freq: ME, Name: amount, dtype: int64
```
**What it means:** groupby hides February; resample shows it as 0, which matters for charts and averages.
**Likely follow-ups:**
- *Can you do both together?* Yes, `pd.Grouper(freq="ME")` inside groupby (Q42).
- *Which is faster?* Not a deciding factor at interview scale.
**Common mistakes:** calling resample on a text column or without a datetime index; missing that empty months vanish in groupby.

### Q9 ⭐⭐⭐ 🟡 Write code to resample daily attendance records to monthly totals.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic `resample` usage with a frequency code and an aggregation.
**Say this in the interview:** "I call `resample('ME', on='date')` to put daily rows into month buckets, then `.sum()` the attendance column."
**Explain simply:**
- **resample:** regroups time data into a new frequency.
- **"ME":** month end (one bucket per month, labelled with its last day). "MS" labels by month start.
- **on="date":** tells pandas which column is the date, so no need to set an index.
**Sample data:** three January days and two February days of headcount present.
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.DataFrame({
    "date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03", "2026-02-01", "2026-02-02"]),
    "employees_present": [90, 88, 92, 85, 87],
})

# Group the daily rows into month-end buckets and add them up
monthly_attendance = attendance.resample("ME", on="date")["employees_present"].sum()

print(monthly_attendance)
```
**Output:**
```
date
2026-01-31    270
2026-02-28    172
Freq: ME, Name: employees_present, dtype: int64
```
**What it means:** 270 person-days present in January, 172 in February (in this tiny sample).
**Likely follow-ups:**
- *Average instead of total?* Swap `.sum()` for `.mean()`.
- *Weekly totals?* Use "W".
**Common mistakes:** using the old "M" code (an error in pandas 3, verified); summing a headcount when an average is the right measure.

### Q10 ⭐⭐⭐ 🟡 Write code to calculate month-over-month percentage growth in sales.
**Asked at:** commonly asked (no company-specific report found); an MoM growth scenario appears in an informal Telegram analytics channel post (snippet only).
**What the interviewer is checking:** Do you know `pct_change` and how growth is defined.
**Say this in the interview:** "I use `pct_change()` on the monthly sales column and multiply by 100. It does (this month minus last month) divided by last month. The first month has no previous month, so it is NaN."
**Explain simply:**
- **Month-over-month (MoM) growth:** how much sales moved compared with the month before, as a percentage.
- **pct_change:** the built-in way to compute it row by row.
- Data must already be one row per month and in date order.
**Sample data:** monthly sales for four months.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "sales": [100000, 120000, 108000, 135000],
})

# Percentage change from the previous month
sales["mom_growth_pct"] = (sales["sales"].pct_change() * 100).round(1)

print(sales)
```
**Output:**
```
  month   sales  mom_growth_pct
0   Jan  100000             NaN
1   Feb  120000            20.0
2   Mar  108000           -10.0
3   Apr  135000            25.0
```
**What it means:** sales grew 20% in February, fell 10% in March and grew 25% in April.
**Likely follow-ups:**
- *Why is January NaN?* No earlier month to compare with (Q24).
- *Raw orders, not monthly?* Resample to months first (Q9), then `pct_change`.
**Common mistakes:** forgetting to sort by date; dividing by the current month instead of the previous one; forgetting that a 0 in the previous month gives infinity.

### Q11 ⭐⭐⭐ 🟡 How do you calculate a 7-day rolling average of daily orders in pandas?
**Asked at:** commonly asked (no company-specific report found); rolling windows appear in pandas practice sets (Udemy, snippet only).
**What the interviewer is checking:** Do you know `rolling(window).mean()` and why early rows are empty.
**Say this in the interview:** "I use `.rolling(7).mean()` on the daily orders. Each value is the average of that day and the six days before it, so it smooths daily ups and downs. The first six rows are NaN because there are not seven days yet."
**Explain simply:**
- **Rolling window:** a sliding group of the last N rows.
- **Why use it:** weekends and spikes make daily numbers jumpy; a 7-day average shows the trend.
- **NaN at the start:** not enough history; `min_periods=1` would average whatever is available.
- Data should have one row per day, in order.
**Sample data:** ten days of orders.
**Code (what you write in the interview):**
```python
import pandas as pd

orders = pd.DataFrame({
    "date": pd.date_range("2026-01-01", periods=10),
    "orders": [20, 25, 22, 30, 28, 35, 40, 38, 33, 45],
})

# Average of the current day and the 6 days before it
orders["rolling_7_day_avg"] = orders["orders"].rolling(7).mean().round(1)

print(orders)
```
**Output:**
```
        date  orders  rolling_7_day_avg
0 2026-01-01      20                NaN
1 2026-01-02      25                NaN
2 2026-01-03      22                NaN
3 2026-01-04      30                NaN
4 2026-01-05      28                NaN
5 2026-01-06      35                NaN
6 2026-01-07      40               28.6
7 2026-01-08      38               31.1
8 2026-01-09      33               32.3
9 2026-01-10      45               35.6
```
**What it means:** on 7 January the average over the first seven days is 28.6; the line rises smoothly toward 35.6.
**Likely follow-ups:**
- *What if days are missing?* Rolling counts rows, not days; fill the missing dates first (Q28).
- *Centre the window?* Add `center=True`.
**Common mistakes:** unsorted data; counting rows when days are missing; reading the NaN rows as errors.

### Q12 ⭐⭐ 🟢 How do you filter a DataFrame for rows between two dates?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you filter on a datetime column cleanly.
**Say this in the interview:** "On a datetime column I use `.between(start, end)`; both ends are included. You can also use two comparisons joined with `&`."
**Explain simply:**
- **between:** True for dates from the start to the end, inclusive.
- Date strings like "2026-01-01" are understood when the column is datetime.
- **Boolean filter:** a True/False value per row; rows marked True are kept.
**Sample data:** four employees with joining dates.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Kiran"],
    "joining_date": pd.to_datetime(["2025-12-20", "2026-01-10", "2026-02-15", "2026-03-05"]),
})

# between includes both the start and the end date
q1_joiners = employees[employees["joining_date"].between("2026-01-01", "2026-03-31")]

print(q1_joiners)
```
**Output:**
```
    name joining_date
1   Ravi   2026-01-10
2  Meena   2026-02-15
3  Kiran   2026-03-05
```
**What it means:** three people joined in the first quarter of 2026; Asha (December) is excluded.
**Alternative:** `employees[(employees["joining_date"] >= "2026-01-01") & (employees["joining_date"] <= "2026-03-31")]`.
**Likely follow-ups:**
- *What if the column has times (like 14:30)?* An end of "2026-03-31" means midnight, so later times that day are cut off; use `< "2026-04-01"`.
- *Left side only?* A single `>=` comparison.
**Common mistakes:** filtering on a text column; forgetting brackets around each condition when using `&`; the end-date time-of-day trap above.

### Q13 ⭐⭐ 🟢 How do you set a date column as the index, and why does that help with time series?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know `set_index` and the benefits of a date index.
**Say this in the interview:** "`df.set_index('date')` makes the date the row label. Then I can slice by date text like `.loc['2026-02':'2026-03']`, and use resample and rolling easily."
**Explain simply:**
- **Index:** the row labels of a table; normally 0, 1, 2.
- **Date index (DatetimeIndex):** pandas knows the rows are on a timeline.
- **Benefits:** partial-date slicing ("2026-02" means all of February), resample without `on=`, and plots with dates on the x-axis.
- Sort the index first for reliable slicing.
**Sample data:** four sales rows, January to April.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "date": pd.to_datetime(["2026-01-05", "2026-02-11", "2026-03-02", "2026-04-20"]),
    "amount": [1000, 1200, 800, 900],
})

# Make the date column the index (the row labels)
sales = sales.set_index("date")

# Slice by dates directly; both ends are included
print(sales.loc["2026-02":"2026-03"])
```
**Output:**
```
            amount
date              
2026-02-11    1200
2026-03-02     800
```
**What it means:** February and March rows came back with one short slice, with no filter condition.
**Likely follow-ups:**
- *Undo it?* `reset_index()` brings the date back as a column.
- *Is the date still usable as a column?* No, it is the index until reset (use `drop=False` to keep both).
**Common mistakes:** setting a text column as the index (convert first); slicing an unsorted index; being surprised that the date is no longer a normal column.

### Q14 ⭐⭐ 🟢 How do you create a range of dates in pandas using pd.date_range?
**Asked at:** commonly asked (no company-specific report found); date_range is a named talking point in Coursera and Educative lists (snippet only).
**What the interviewer is checking:** Do you know the start, end, periods and freq arguments.
**Say this in the interview:** "`pd.date_range` makes a sequence of dates. I give a start, then either an end date or a number of periods, and a frequency like 'D' for daily or 'MS' for month start."
**Explain simply:**
- **start / end:** the first and last date (end is included).
- **periods:** how many dates you want, as an alternative to `end`.
- **freq:** the step: "D" day, "W" week, "MS" month start, "ME" month end, "B" business day.
- Handy for building a full calendar to find or fill missing dates (Q28).
**Code (what you write in the interview):**
```python
import pandas as pd

# Daily dates, 5 of them
print(pd.date_range(start="2026-01-01", periods=5, freq="D"))

# Month-start dates between two dates
print(pd.date_range(start="2026-01-01", end="2026-04-30", freq="MS"))
```
**Output:**
```
DatetimeIndex(['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04',
               '2026-01-05'],
              dtype='datetime64[us]', freq='D')
DatetimeIndex(['2026-01-01', '2026-02-01', '2026-03-01', '2026-04-01'], dtype='datetime64[us]', freq='MS')
```
**What it means:** the first call gives five consecutive days; the second gives the first day of each month from January to April.
**Likely follow-ups:**
- *Only working days?* `freq="B"` (Monday to Friday; it does not know public holidays).
- *Use it in a DataFrame?* `pd.DataFrame({"date": pd.date_range(...)})`.
**Common mistakes:** giving `end` and `periods` together with `start` (too many inputs); mixing up "MS" and "ME"; using the removed "M" code.

### Q15 ⭐⭐ 🟢 How do you find the earliest and latest date in a column and the span between them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** `min`, `max` work on dates, and subtraction gives a Timedelta.
**Say this in the interview:** "`.min()` gives the earliest date, `.max()` the latest, and latest minus earliest gives the span as a Timedelta. `.days` turns it into a number."
**Explain simply:**
- **min / max:** work on datetime columns just like numbers.
- **Span:** the length of time between two dates, a Timedelta.
- Useful to check the data's coverage before analysing it (for example "do we have a full year?").
**Sample data:** three joining dates.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "joining_date": pd.to_datetime(["2024-01-15", "2024-03-01", "2025-07-20"]),
})

earliest = employees["joining_date"].min()
latest = employees["joining_date"].max()
span = latest - earliest

print(earliest)
print(latest)
print(span)
print(span.days)
```
**Output:**
```
2024-01-15 00:00:00
2025-07-20 00:00:00
552 days 00:00:00
552
```
**What it means:** hiring data runs from 15 Jan 2024 to 20 Jul 2025, a span of 552 days.
**Likely follow-ups:**
- *How would you check coverage in months?* `span.days / 30.4` as an estimate.
- *NaT values?* `min` and `max` skip them.
**Common mistakes:** running min/max on a text column (it sorts as text, which can look right for ISO dates but fails for "15-Jan-24"); printing the Timedelta and forgetting `.days`.

### Q16 ⭐⭐ 🟢 What is the difference between datetime64, Timestamp and Timedelta in pandas?
**Asked at:** commonly asked (no company-specific report found); a Timedelta question appears on a Naukri Code360 pandas list (snippet only).
**What the interviewer is checking:** Do you know the column type versus a single value, and a point in time versus a length of time.
**Say this in the interview:** "`datetime64` is the type of a whole column of dates. A `Timestamp` is one single date-and-time value from it. A `Timedelta` is a length of time, like 552 days, which you get by subtracting two timestamps."
**Explain simply:**
- **datetime64:** the column's data type (dtype), for many dates.
- **Timestamp:** one point in time, such as 15 Jan 2024 00:00.
- **Timedelta:** a duration; date minus date gives a Timedelta; date plus Timedelta gives a date.
- Think: datetime64 is the bucket, Timestamp is one item, Timedelta is the distance between two items.
**Sample data:** two joining dates.
**Code (what you write in the interview):**
```python
import pandas as pd

joining_dates = pd.Series(pd.to_datetime(["2024-01-15", "2025-07-20"]))

one_date = joining_dates[0]
gap = joining_dates[1] - joining_dates[0]

print(joining_dates.dtype)
print(type(one_date))
print(type(gap))
print(gap)
```
**Output:**
```
datetime64[us]
<class 'pandas.Timestamp'>
<class 'pandas.Timedelta'>
552 days 00:00:00
```
**What it means:** the column is `datetime64`, one value is a `Timestamp`, and the gap between two is a `Timedelta` of 552 days.
**Likely follow-ups:**
- *What is the `[us]` or `[ns]`?* The time precision (microseconds or nanoseconds); pandas 3 often shows `us`, older versions `ns`.
- *What is a Period?* A whole span such as "March 2026" (Q45).
**Common mistakes:** mixing up Timestamp (a moment) and Timedelta (a duration); treating the `datetime64` dtype as a single value.

### Q17 ⭐⭐ 🟢 How do you check whether a column is stored as text or as datetime?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you look at the dtype before doing date work, instead of guessing from how the column prints?
**Say this in the interview:** "I check `df.dtypes`. If it says `datetime64`, it is a real date; if it says `str` or `object`, it is still text and I convert it with `pd.to_datetime`."
**Explain simply:**
- A **dtype** is the type pandas stores a column as (text, whole number, decimal, date).
- Dates that look right on screen can still be text. Only a datetime column lets you use `.dt` and do date maths.
- `datetime64` is the date type; text shows as `str` (pandas 3) or `object` (older versions).
- To test it in code, use `pd.api.types.is_datetime64_any_dtype(column)`, which returns True or False.
**Sample data:** an employee table with the joining date stored twice, once as text and once as a real date.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena"],
    "joining_text": ["2024-01-15", "2024-03-01", "2025-07-20"],
    "joining_date": pd.to_datetime(["2024-01-15", "2024-03-01", "2025-07-20"]),
})

# Look at the type of every column
print(employees.dtypes)

# Ask directly: is this column a real date?
print(pd.api.types.is_datetime64_any_dtype(employees["joining_text"]))
print(pd.api.types.is_datetime64_any_dtype(employees["joining_date"]))
```
**Output:**
```
name                       str
joining_text               str
joining_date    datetime64[us]
dtype: object
False
True
```
**What it means:** `joining_text` looks like a date but is text, so date tools will fail on it. `joining_date` is a real date. (Verified on pandas 3.0.5: text shows as `str`, the date unit shows as `us`; older versions show `object` and `ns`.)
**Likely follow-ups:**
- *How do you fix a text column?* `df["col"] = pd.to_datetime(df["col"])`.
- *What does `df.info()` show?* The same dtypes plus non-null counts, handy for a first look.
**Common mistakes:** Trusting the printed look of the column; comparing dtype to `"datetime64[ns]"` (fails on newer pandas where the unit can be `us`), so use `is_datetime64_any_dtype`.

### Q18 ⭐⭐ 🟢 Write code to add a new column that flags weekend dates (Saturday or Sunday) in an attendance table.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use `.dt.dayofweek` and a simple comparison to build a True/False flag?
**Say this in the interview:** "pandas numbers weekdays from Monday as 0 to Sunday as 6, so weekend means 5 or more. I compare `dt.dayofweek >= 5` and store it in a new column."
**Explain simply:**
- `.dt.dayofweek` gives a number for each date: Monday 0, Tuesday 1, ... Saturday 5, Sunday 6.
- `>= 5` gives True for Saturday and Sunday, False for the rest.
- The column must already be a datetime (see Q1).
**Sample data:** five days of attendance with the headcount present.
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.DataFrame({
    "date": pd.to_datetime(["2026-11-05", "2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09"]),
    "present": [52, 50, 8, 3, 54],
})

# Monday is 0 and Sunday is 6, so 5 and 6 are the weekend
attendance["is_weekend"] = attendance["date"].dt.dayofweek >= 5
print(attendance)
```
**Output:**
```
        date  present  is_weekend
0 2026-11-05       52       False
1 2026-11-06       50       False
2 2026-11-07        8        True
3 2026-11-08        3        True
4 2026-11-09       54       False
```
**What it means:** 7 and 8 November 2026 are a Saturday and Sunday, so they are flagged True. Attendance is low on those days, which is expected.
**Alternative:** `attendance["date"].dt.day_name().isin(["Saturday", "Sunday"])` is easier to read but slower and depends on English day names.
**Likely follow-ups:**
- *How do you drop the weekends?* `attendance[~attendance["is_weekend"]]`.
- *What if the weekend is Friday and Saturday (some countries)?* Use `isin([4, 5])`.
**Common mistakes:** Assuming Sunday is 0 (it is 6 in pandas); running `.dt` on a text column.

### Q19 ⭐⭐ 🟢 Write code to count hires per month from a joining_date column.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn dates into a month label and count rows per month?
**Say this in the interview:** "I convert each joining date to a month with `dt.to_period('M')`, group by it, and count the rows with `size()`."
**Explain simply:**
- A **Period** is a whole month (for example 2026-01), so all dates in January fall into one group.
- `groupby(...).size()` counts how many rows are in each group, which is how many people joined.
- Months with zero hires do not appear with this method; `resample` (below) shows them as 0.
**Sample data:** six employees with their joining dates.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["A", "B", "C", "D", "E", "F"],
    "joining_date": pd.to_datetime(["2026-01-05", "2026-01-20", "2026-02-10",
                                    "2026-04-01", "2026-04-15", "2026-04-28"]),
})

# Turn each date into its month, then count people per month
hires_per_month = employees.groupby(employees["joining_date"].dt.to_period("M")).size()
print(hires_per_month)
```
**Output:**
```
joining_date
2026-01    2
2026-02    1
2026-04    3
Freq: M, dtype: int64
```
**What it means:** 2 people joined in January, 1 in February, 3 in April. March is missing because nobody joined, so it is not listed.
**Alternative:** keep zero months visible with resample.
```python
hires_per_month = employees.set_index("joining_date").resample("MS").size()
```
This prints March 2026 with 0.
**Likely follow-ups:**
- *Why not group by `dt.month`?* It mixes January 2025 and January 2026 together.
- *How do you plot it?* `hires_per_month.plot(kind="bar")`.
**Common mistakes:** Grouping by month number only across several years; forgetting that empty months vanish with `groupby`.

### Q20 ⭐⭐ 🟢 How do you format a datetime column as a string such as 05-Nov-2026 using strftime?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `.dt.strftime` and the common format codes?
**Say this in the interview:** "I use `df['col'].dt.strftime('%d-%b-%Y')`. `%d` is day, `%b` is the short month name, `%Y` is the four digit year."
**Explain simply:**
- **strftime** means "string from time": it turns a date into text in the layout you choose.
- Common codes: `%d` day (05), `%m` month number (11), `%b` short month (Nov), `%B` full month (November), `%Y` four-digit year, `%y` two-digit year, `%A` weekday name.
- The result is text, so you cannot do date maths on it any more. Keep the original date column.
**Sample data:** two order dates.
**Code (what you write in the interview):**
```python
import pandas as pd

orders = pd.DataFrame({"order_date": pd.to_datetime(["2026-11-05", "2026-03-09"])})

# Make a text version for the report, keep the real date column untouched
orders["order_date_text"] = orders["order_date"].dt.strftime("%d-%b-%Y")
print(orders)
```
**Output:**
```
  order_date order_date_text
0 2026-11-05     05-Nov-2026
1 2026-03-09     09-Mar-2026
```
**What it means:** The new column shows dates in the 05-Nov-2026 style for display or export.
**Likely follow-ups:**
- *How do you go the other way?* `pd.to_datetime(text, format="%d-%b-%Y")` (see Q22).
- *Why not format first and then sort?* Text sorts alphabetically ("01-Apr" before "01-Jan" is wrong order by date); sort by the real date, then format.
**Common mistakes:** Formatting early and then trying to use `.dt` on the text; using `%m` when you want the month name (`%b`); using `.strftime` without `.dt` on a Series.

### Q21 ⭐⭐ 🟡 How do you handle dates like 03/04/2026 that could be day-first or month-first when parsing?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know pandas guesses month-first by default and that you must state the format when data is day-first (common in India and the UK)?
**Say this in the interview:** "I never let pandas guess. I give the exact `format='%d/%m/%Y'`, or at least `dayfirst=True`, so 03/04/2026 is read as 3 April."
**Explain simply:**
- An ambiguous date like 03/04/2026 can mean 3 April (day first) or 4 March (month first). Without guidance pandas leans month-first, so Indian or UK data can be silently read wrong.
- `dayfirst=True` tells pandas the first number is the day.
- `format="%d/%m/%Y"` is stricter and safest: it also fails loudly on rows that do not match.
- Check with a date you know, such as 25/12/2025, which can only be day-first.
**Sample data:** one ambiguous date and one clear day-first date.
**Code (what you write in the interview):**
```python
import pandas as pd

raw = pd.DataFrame({"date_text": ["03/04/2026", "25/12/2025"]})

# Day-first data (Indian style): say the format exactly
raw["date"] = pd.to_datetime(raw["date_text"], format="%d/%m/%Y")
print(raw)
```
**Output:**
```
    date_text       date
0  03/04/2026 2026-04-03
1  25/12/2025 2025-12-25
```
**What it means:** 03/04/2026 became 3 April 2026, as intended. If you read the same text month-first with `format="%m/%d/%Y"`, the 25/12/2025 row cannot be a valid month and turns into NaT (missing date) when `errors="coerce"`, which is a quick clue that the format is wrong.
**Alternative:** `pd.to_datetime(raw["date_text"], dayfirst=True)` gives the same result here, but it is only a hint and can misread mixed data.
**Likely follow-ups:**
- *What if the file mixes both layouts?* Ask the data owner; do not guess. Parse each source with its own format.
- *Best fix at the source?* Use ISO format `YYYY-MM-DD`, which is never ambiguous.
**Common mistakes:** Accepting the default and not noticing days and months swapped when the day is 12 or less; using `dayfirst=True` on ISO dates like 2026-04-03.

### Q22 ⭐⭐ 🟡 How do you parse a date column stored in a custom format such as 20260315 or 15-Mar-26?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pass the right `format` string to `pd.to_datetime`?
**Say this in the interview:** "I describe the layout with the `format` argument: `%Y%m%d` for 20260315 and `%d-%b-%y` for 15-Mar-26. If the column is numeric I first turn it into text with `astype(str)`."
**Explain simply:**
- The `format` string is a pattern: each code stands for one part of the date (`%Y` four-digit year, `%y` two-digit year, `%m` month number, `%b` short month name, `%d` day).
- Characters that are not codes (like the dashes) must match the text exactly.
- A number such as 20260315 stored as an integer must become text before parsing.
**Sample data:** the same two dates stored in two custom layouts.
**Code (what you write in the interview):**
```python
import pandas as pd

dates = pd.DataFrame({
    "compact": ["20260315", "20251201"],
    "short": ["15-Mar-26", "01-Dec-25"],
})

# Year-month-day with no separators
dates["compact_date"] = pd.to_datetime(dates["compact"], format="%Y%m%d")

# Day-ShortMonth-TwoDigitYear
dates["short_date"] = pd.to_datetime(dates["short"], format="%d-%b-%y")
print(dates)
```
**Output:**
```
    compact      short compact_date short_date
0  20260315  15-Mar-26   2026-03-15 2026-03-15
1  20251201  01-Dec-25   2025-12-01 2025-12-01
```
**What it means:** Both custom layouts were read into real dates. If the compact column were integers, use `dates["compact"].astype(str)` first (verified: this also gives 2026-03-15).
**Likely follow-ups:**
- *What if a few rows do not match?* Add `errors="coerce"` and look at the NaT rows (see Q7).
- *Why give a format at all?* It is faster and avoids wrong guesses.
**Common mistakes:** Using `%Y` for a two-digit year (use `%y`); using `%m` for a month name (use `%b`); passing integers without converting to text.

### Q23 ⭐⭐ 🟡 What is the shift function in pandas, and how do you use it to compare each day with the previous day?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that `shift` moves values down so each row can see the previous row (like SQL `LAG`)?
**Say this in the interview:** "`shift(1)` moves the column down one row, so each day sits next to the previous day's value. Then I subtract to get the daily change. The first row has no previous day, so it is NaN."
**Explain simply:**
- `shift(1)` = look one row back (like `LAG` in SQL). `shift(-1)` = look one row forward (like `LEAD`).
- The data must be sorted by date first, or "previous row" is not "previous day".
- The first row gets NaN (missing) because there is nothing before it.
**Sample data:** daily order counts for 5 days.
**Code (what you write in the interview):**
```python
import pandas as pd

daily = pd.DataFrame({
    "date": pd.date_range("2026-11-01", periods=5),
    "orders": [120, 135, 128, 150, 90],
})

# Put yesterday's orders next to today's orders
daily["previous_day"] = daily["orders"].shift(1)

# Today minus yesterday
daily["change"] = daily["orders"] - daily["previous_day"]
print(daily)
```
**Output:**
```
        date  orders  previous_day  change
0 2026-11-01     120           NaN     NaN
1 2026-11-02     135         120.0    15.0
2 2026-11-03     128         135.0    -7.0
3 2026-11-04     150         128.0    22.0
4 2026-11-05      90         150.0   -60.0
```
**What it means:** Orders rose by 15 on 2 November, fell by 7 on 3 November, and dropped sharply by 60 on 5 November, which is worth investigating.
**Alternative:** `daily["orders"].diff()` gives the change in one step.
**Likely follow-ups:**
- *Is the column a float now?* Yes, NaN forces decimals (120.0).
- *How do you shift within a group (per employee)?* `df.groupby("employee")["col"].shift(1)`.
**Common mistakes:** Not sorting by date first; missing days in the data, so "previous row" is not "yesterday" (reindex to all days first, see Q28); forgetting the first row is NaN.

### Q24 ⭐⭐ 🟡 How do you use pct_change on monthly data, and why is the first value NaN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `pct_change` gives the change versus the previous row as a fraction, and that the first row has nothing to compare to?
**Say this in the interview:** "`pct_change()` computes (this month minus last month) divided by last month. I multiply by 100 for percent. The first month has no previous month, so it is NaN."
**Explain simply:**
- Formula: (current - previous) / previous.
- The result is a fraction (0.10 means 10%), so multiply by 100 to show percent.
- First row: no previous value, so pandas returns NaN (not available) instead of inventing a number.
- Data must be sorted by month with no missing months.
**Sample data:** four months of sales.
**Code (what you write in the interview):**
```python
import pandas as pd

monthly = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "sales": [100000, 110000, 99000, 120000],
})

# Change versus the previous month, in percent
monthly["growth_pct"] = monthly["sales"].pct_change() * 100
print(monthly)
```
**Output:**
```
  month   sales  growth_pct
0   Jan  100000         NaN
1   Feb  110000   10.000000
2   Mar   99000  -10.000000
3   Apr  120000   21.212121
```
**What it means:** Sales grew 10% in February, fell 10% in March, and grew 21.2% in April. January shows NaN because it is the starting point.
**Alternative:** `(sales - sales.shift(1)) / sales.shift(1) * 100` does the same by hand. Use `pct_change(periods=12)` for monthly data versus the same month last year.
**Likely follow-ups:**
- *What if the previous value is 0?* The result is inf (division by zero); handle it separately.
- *Can you round it?* `.round(1)`.
**Common mistakes:** Forgetting `* 100`; running on unsorted data; expecting a number in the first row.

### Q25 ⭐⭐ 🟡 Write code to find the day of the week with the highest average sales.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you extract the weekday name, group by it, average, and pick the maximum?
**Say this in the interview:** "I add a weekday name column with `dt.day_name()`, group by it, take the mean of sales, and use `idxmax()` to get the name of the best day."
**Explain simply:**
- `dt.day_name()` turns each date into Monday, Tuesday and so on.
- `groupby("weekday")["amount"].mean()` gives the average sales for each weekday.
- `idxmax()` returns the label (the weekday name) of the largest value; `max()` returns the value itself.
- Use the average, not the total, so weekdays with more data do not look better just because they appear more often.
**Sample data:** two weeks of daily sales (14 rows, starting Monday 2 Nov 2026), shown in the code.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "date": pd.date_range("2026-11-02", periods=14),
    "amount": [200, 220, 210, 230, 300, 500, 450,
               190, 210, 205, 240, 310, 520, 430],
})

# Name of the weekday for each date
sales["weekday"] = sales["date"].dt.day_name()

# Average sales for each weekday
average_by_weekday = sales.groupby("weekday")["amount"].mean()
print(average_by_weekday.sort_values(ascending=False))

# The best day and its average
print(average_by_weekday.idxmax(), average_by_weekday.max())
```
**Output:**
```
weekday
Saturday     510.0
Sunday       440.0
Friday       305.0
Thursday     235.0
Tuesday      215.0
Wednesday    207.5
Monday       195.0
Name: amount, dtype: float64
Saturday 510.0
```
**What it means:** Saturday has the highest average sales (510), followed by Sunday. Weekends are the strongest days.
**Likely follow-ups:**
- *Why does the groupby output come out alphabetical?* groupby sorts the labels; use `sort_values` or a day-order list to show Monday to Sunday.
- *What about total instead of average?* Use `.sum()`; it can mislead if the data has uneven weeks.
**Common mistakes:** Using sum when asked for average; forgetting to convert the date column to datetime; using `idxmax` on the wrong object (the grouped series, not the raw table).

### Q26 ⭐⭐ 🟡 Write code to compute a cumulative sum of sales within each year.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine `groupby` with `cumsum` so the running total restarts every year?
**Say this in the interview:** "I sort by date, make a year column, then `groupby('year')['amount'].cumsum()`. The running total restarts when the year changes."
**Explain simply:**
- **Cumulative sum** (running total): each row shows the sum of all rows up to that point.
- `groupby("year")` makes the total restart for each year, like year-to-date (YTD) sales.
- Sorting by date first matters, because cumsum adds in row order.
**Sample data:** five orders over two years.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "order_date": pd.to_datetime(["2025-11-10", "2025-12-05", "2026-01-12",
                                  "2026-02-03", "2026-02-20"]),
    "amount": [100, 200, 150, 300, 50],
})

# Oldest to newest, so the running total adds in date order
sales = sales.sort_values("order_date")

sales["year"] = sales["order_date"].dt.year

# Running total that restarts every year
sales["running_total"] = sales.groupby("year")["amount"].cumsum()
print(sales)
```
**Output:**
```
  order_date  amount  year  running_total
0 2025-11-10     100  2025            100
1 2025-12-05     200  2025            300
2 2026-01-12     150  2026            150
3 2026-02-03     300  2026            450
4 2026-02-20      50  2026            500
```
**What it means:** 2025 reaches 300 by December. In 2026 the running total starts again at 150, so the last row shows 500 year to date.
**Likely follow-ups:**
- *How do you do it by financial year?* Group by the financial year label instead (Q27).
- *Running total per employee or region too?* `groupby(["region", "year"])`.
**Common mistakes:** Calling `cumsum()` without `groupby` (it never restarts); not sorting by date first.

### Q27 ⭐⭐ 🟡 Write code to group data by quarter and by financial year (April to March) in pandas.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know `to_period("Q")` and that `"Y-MAR"` shifts the year to end in March, as Indian companies use?
**Say this in the interview:** "For calendar quarters I use `dt.to_period('Q')`. For an April to March financial year I use `dt.to_period('Y-MAR')`, which labels each year by the year it ends in."
**Explain simply:**
- A **Period** is a block of time such as a quarter or a year. `"Q"` means quarter, `"Y-MAR"` means a year that ends in March.
- The label is the year in which the financial year **ends**: 1 Apr 2026 to 31 Mar 2027 is labelled 2027 (this is "FY2026-27", or "FY27" in common usage).
- `"Q-MAR"` gives fiscal quarters, where Apr-Jun is Q1 (so Jan-Mar 2026 is fiscal 2026Q4).
**Sample data:** six sales across two financial years.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "order_date": pd.to_datetime(["2026-01-15", "2026-03-31", "2026-04-01",
                                  "2026-08-10", "2027-02-14", "2027-04-02"]),
    "amount": [100, 200, 150, 300, 50, 400],
})

# Calendar quarters (Jan-Mar, Apr-Jun, ...)
sales["quarter"] = sales["order_date"].dt.to_period("Q")
print(sales.groupby("quarter")["amount"].sum())

# Financial year April to March (labelled by the year it ends)
sales["financial_year"] = sales["order_date"].dt.to_period("Y-MAR")
print(sales.groupby("financial_year")["amount"].sum())
```
**Output:**
```
quarter
2026Q1    300
2026Q2    150
2026Q3    300
2027Q1     50
2027Q2    400
Freq: Q-DEC, Name: amount, dtype: int64
financial_year
2026    300
2027    500
2028    400
Freq: Y-MAR, Name: amount, dtype: int64
```
**What it means:** 15 Jan and 31 Mar 2026 both belong to financial year 2026 (Apr 2025 to Mar 2026), total 300. 1 Apr 2026 starts financial year 2027, which holds 150 + 300 + 50 = 500. 2 Apr 2027 starts FY 2028.
**Alternative:** `sales["order_date"].dt.to_period("Q-MAR")` gives fiscal quarters (verified: 2026-01-15 becomes 2026Q4, 2026-04-01 becomes 2027Q1).
**Likely follow-ups:**
- *How do you show it as "FY2026-27"?* Build a text label from the year (a small helper column), or just explain that the period year is the end year.
- *What if the financial year starts in July?* Use `"Y-JUN"`.
**Common mistakes:** Using `dt.year` for a financial year (splits Jan to Mar from Apr to Dec wrongly); misreading the 2027 label as the start year.

### Q28 ⭐⭐ 🟡 How do you find missing dates in a daily series and fill them in with zero?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a full date range and use `reindex` to expose and fill gaps?
**Say this in the interview:** "I build a complete range with `pd.date_range` from the first to the last date. `difference` shows the missing days, and `reindex(..., fill_value=0)` adds them back with zero."
**Explain simply:**
- Daily data often skips days when nothing happened (no orders, no attendance record).
- `pd.date_range(start, end)` lists every day between two dates.
- `all_days.difference(existing_dates)` returns the dates that are missing.
- `reindex` makes the table follow the full list of days; new rows are filled with 0 here.
**Sample data:** orders for 1, 2, 5 and 6 November (3rd and 4th are missing).
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "date": pd.to_datetime(["2026-11-01", "2026-11-02", "2026-11-05", "2026-11-06"]),
    "orders": [10, 12, 9, 15],
})

# Every day from the first to the last date
all_days = pd.date_range(sales["date"].min(), sales["date"].max())

# Which days are missing?
missing_days = all_days.difference(sales["date"])
print(missing_days)

# Add the missing days with 0 orders
complete = sales.set_index("date").reindex(all_days, fill_value=0)
print(complete)
```
**Output:**
```
DatetimeIndex(['2026-11-03', '2026-11-04'], dtype='datetime64[us]', freq='D')
            orders
2026-11-01      10
2026-11-02      12
2026-11-03       0
2026-11-04       0
2026-11-05       9
2026-11-06      15
```
**What it means:** 3 and 4 November were missing; they are now rows with 0 orders, so rolling averages and charts treat them correctly.
**Alternative:** `sales.set_index("date").asfreq("D", fill_value=0)` does the same in one line.
**Likely follow-ups:**
- *Is zero always right?* No. For stock levels or prices, carry the last value forward (`ffill`) instead.
- *Duplicate dates?* Sum them first with `groupby`, because reindex fails on duplicate index values.
**Common mistakes:** Filling with zero when the true meaning is "unknown"; forgetting the date must be the index before reindexing.

### Q29 ⭐⭐ 🟡 Write code to find employees who joined in the last 90 days.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a cutoff date with `Timedelta` and filter with a comparison?
**Say this in the interview:** "I take today minus 90 days as the cutoff and keep rows where the joining date is on or after it."
**Explain simply:**
- `pd.Timestamp.today()` is the current date and time; `pd.Timedelta(days=90)` is a length of 90 days.
- Subtracting gives the cutoff date; comparing a date column to it gives True/False for each row, and that filters the table.
- In the example below I fix "today" as 9 Nov 2026 so the output is repeatable; in real work write `pd.Timestamp.today()`.
**Sample data:** four employees with joining dates.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["Asha", "Ravi", "Meena", "Kiran"],
    "joining_date": pd.to_datetime(["2026-10-20", "2026-06-01", "2026-09-15", "2026-08-12"]),
})

today = pd.Timestamp("2026-11-09")   # in real work: pd.Timestamp.today()
cutoff_date = today - pd.Timedelta(days=90)

# Keep people who joined on or after the cutoff
new_joiners = employees[employees["joining_date"] >= cutoff_date]
print(cutoff_date.date())
print(new_joiners)
```
**Output:**
```
2026-08-11
    name joining_date
0   Asha   2026-10-20
2  Meena   2026-09-15
3  Kiran   2026-08-12
```
**What it means:** Three employees joined in the last 90 days. Ravi (1 June) is older than the cutoff of 11 August, so he is left out.
**Likely follow-ups:**
- *Inclusive or exclusive?* `>=` includes someone who joined exactly on the cutoff date; say which one the business wants.
- *What about the time part of `today()`?* It includes the current time; use `pd.Timestamp.today().normalize()` to use midnight.
**Common mistakes:** Comparing a text column with a date (convert first); forgetting that the result depends on the day you run it; using `<=` by mistake.

### Q30 ⭐⭐ 🟡 Write code to compute monthly attrition rate from joining and exit date columns.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the HR definition (leavers in the month divided by headcount) and can you work out headcount at a date from joining and exit dates?
**Say this in the interview:** "For each month I count employees who were present on the first day (joined before it and had not left), count those whose exit date falls in the month, and divide leavers by the starting headcount."
**Explain simply:**
- **Attrition rate** = people who left in the month / headcount at the start of the month x 100. (Some firms use the average of opening and closing headcount; state which one you use.)
- Someone is present at the start of a month if they joined before that day and their exit date is empty or on/after that day.
- A blank exit date means the person is still employed.
**Sample data:** six employees, three of whom leave (exit date blank means still working).
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "name": ["A", "B", "C", "D", "E", "F"],
    "joining_date": pd.to_datetime(["2025-01-10", "2025-06-01", "2025-12-15",
                                    "2026-01-20", "2026-02-05", "2026-03-02"]),
    "exit_date": pd.to_datetime(["2026-01-25", None, "2026-02-14",
                                 "2026-03-10", None, None]),
})

results = []
for month_start in pd.date_range("2026-01-01", "2026-03-01", freq="MS"):
    month_end = month_start + pd.offsets.MonthEnd(0)

    # Present on the first day of the month
    present_at_start = (employees["joining_date"] < month_start) & (
        employees["exit_date"].isna() | (employees["exit_date"] >= month_start)
    )
    headcount_at_start = present_at_start.sum()

    # Left during the month
    leavers = employees["exit_date"].between(month_start, month_end).sum()

    results.append({
        "month": month_start.strftime("%Y-%m"),
        "headcount_at_start": headcount_at_start,
        "leavers": leavers,
        "attrition_pct": round(leavers / headcount_at_start * 100, 1),
    })

print(pd.DataFrame(results))
```
**Output:**
```
     month  headcount_at_start  leavers  attrition_pct
0  2026-01                   3        1           33.3
1  2026-02                   3        1           33.3
2  2026-03                   3        1           33.3
```
**What it means:** Each month, 1 of 3 starting employees left, so monthly attrition is 33.3%. (Small sample on purpose; real monthly rates are usually 1-3%.) Annual attrition is not 12 times the monthly rate; compute it from leavers in the year over average headcount.
**Likely follow-ups:**
- *What if starting headcount is 0?* The division fails or gives inf; guard with an `if`.
- *Why a loop?* It is easy to explain line by line; a vectorised version exists but is harder to defend live.
**Common mistakes:** Counting new joiners of the same month in the starting headcount; treating a blank exit date as a leaver; dividing by end-of-month headcount without saying so.

### Q31 ⭐⭐ 🟡 Why do I get a "Can only use .dt accessor with datetimelike values" error, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you recognise that the column is text, not a date, and know the fix?
**Say this in the interview:** "The column is still text, so `.dt` does not work. I convert it with `pd.to_datetime` first, then use `.dt`."
**Explain simply:**
- `.dt` is a set of date tools (year, month, weekday). It only works on real datetime columns.
- The error means the column is text (`str`/`object`) or numbers. Check with `df.dtypes` (Q17).
- Reading a CSV gives text for dates unless you use `parse_dates` (Q2).
**Sample data:** joining dates that were loaded as text.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({"joining_date": ["2024-01-15", "2024-03-01"]})

# This fails: the column is text
# employees["joining_date"].dt.year

# Fix: convert to a real date first
employees["joining_date"] = pd.to_datetime(employees["joining_date"])
print(employees["joining_date"].dt.year)
```
**Output:**
```
0    2024
1    2024
Name: joining_date, dtype: int32
```
(Before the fix, running `.dt.year` raised: `AttributeError: Can only use .dt accessor with datetimelike values`, verified.)
**What it means:** After conversion, `.dt.year` works and returns 2024 for both rows.
**Likely follow-ups:**
- *What if conversion fails on some rows?* Use `errors="coerce"` and inspect the NaT rows (Q7).
- *How do you avoid it when loading a CSV?* Use `pd.read_csv(..., parse_dates=["joining_date"])`.
**Common mistakes:** Using `.dt` on the whole DataFrame instead of one column; converting but not assigning the result back to the column.

### Q32 ⭐ 🟡 What is the difference between rolling, expanding and ewm windows?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the three kinds of moving calculation and when to use each?
**Say this in the interview:** "Rolling looks at a fixed number of recent rows, expanding uses everything from the start up to now, and ewm (exponentially weighted) uses everything but gives recent rows more weight."
**Explain simply:**
- **Rolling(3):** average of the latest 3 values; the window slides. The first 2 rows are NaN because there are not 3 values yet.
- **Expanding:** the window grows each row (all rows so far), so it is a running average.
- **ewm(span=3):** an exponentially weighted mean; newer values count more, older values fade. Good for reacting to recent change.
- Use rolling for a 7-day trend, expanding for an average since the start, ewm for a smoother, more responsive trend.
**Sample data:** five sales values 10 to 50.
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.Series([10, 20, 30, 40, 50], name="sales")

result = pd.DataFrame({
    "sales": sales,
    "rolling_3": sales.rolling(3).mean(),     # last 3 values only
    "expanding": sales.expanding().mean(),    # everything so far
    "ewm": sales.ewm(span=3).mean(),          # recent values weigh more
})
print(result)
```
**Output:**
```
   sales  rolling_3  expanding        ewm
0     10        NaN       10.0  10.000000
1     20        NaN       15.0  16.666667
2     30       20.0       20.0  24.285714
3     40       30.0       25.0  32.666667
4     50       40.0       30.0  41.612903
```
**What it means:** At the last row, rolling averages the latest 3 values (30, 40, 50 gives 40), expanding averages all 5 (30), and ewm sits near 41.6, close to the newest value because recent data weighs more.
**Likely follow-ups:**
- *How do you avoid the NaN at the start?* `rolling(3, min_periods=1)`.
- *Time-based window?* With a date index, `rolling("7D")`.
**Common mistakes:** Forgetting NaN in the first rows of a rolling window; using rolling on unsorted data.

### Q33 ⭐ 🟡 What is the difference between resample and asfreq?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know that resample summarises data into buckets while asfreq only changes the calendar and picks values.
**Say this in the interview:** "asfreq just re-stamps the series at a new frequency and picks the value that sits on each date, adding NaN for missing dates. resample groups rows into buckets, like weeks, and I must say how to combine them, such as sum or mean."
**Explain simply:**
- `asfreq("D")` means: give me one row per day. Existing values are kept as they are; new days get NaN (empty).
- `resample("W")` means: group the days into weeks, then calculate (sum, mean, count) on each group.
- asfreq throws away nothing but also adds up nothing. Going from daily to weekly with asfreq just keeps one day per week, which silently drops data.
- Use asfreq to fill the calendar; use resample to summarise.
**Sample data:** Hours worked on three days, with 3 Jan and 4 Jan missing. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

attendance = pd.Series(
    [8, 6, 9],
    index=pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-05"]),
    name="hours",
)

# asfreq: only adds the missing days, no calculation
print(attendance.asfreq("D"))

# resample: groups days into new buckets and needs a calculation
print(attendance.resample("W").sum())
```
**Output:**
```text
2026-01-01    8.0
2026-01-02    6.0
2026-01-03    NaN
2026-01-04    NaN
2026-01-05    9.0
Freq: D, Name: hours, dtype: float64
2026-01-04    14
2026-01-11     9
Freq: W-SUN, Name: hours, dtype: int64
```
**What it means:** asfreq exposed the two missing days as NaN. resample added up the hours per week (14 in the week ending 4 Jan, 9 in the next).
**Likely follow-ups:**
1. Can asfreq fill the gaps? Yes: `asfreq("D", method="ffill")` copies the last value forward (checked by running).
2. Which one needs an index of dates? Both: the date must be the index (or use `on=` in resample).
**Common mistakes:** Using asfreq to go from daily to monthly and thinking it totals the month. Forgetting the date index.

### Q34 ⭐ 🟡 How do you fill gaps after resampling using ffill, bfill or interpolate?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can pick a sensible fill method and know what each does.
**Say this in the interview:** "After resampling to a finer frequency I get NaN on the new dates. ffill carries the last value forward, bfill pulls the next value back, and interpolate draws a straight line between known points. I choose based on what the number means."
**Explain simply:**
- `ffill` (forward fill): copy the last known value down. Good for things that stay the same until changed, like headcount or salary.
- `bfill` (backward fill): copy the next known value up. Rarely right, because it uses the future.
- `interpolate()`: estimate in-between values on a straight line. Good for smooth measures, bad for counts of events.
- Never fill sales or attendance totals this way; a missing day there usually means zero, so use `fillna(0)`.
**Sample data:** Headcount recorded only on 1, 4 and 7 January. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

headcount = pd.Series(
    [100, 110, 120],
    index=pd.to_datetime(["2026-01-01", "2026-01-04", "2026-01-07"]),
)

daily = headcount.resample("D").mean()   # gaps appear as NaN

filled = pd.DataFrame({
    "gaps": daily,
    "ffill": daily.ffill(),
    "bfill": daily.bfill(),
    "interpolate": daily.interpolate(),
})
print(filled)
```
**Output:**
```text
             gaps  ffill  bfill  interpolate
2026-01-01  100.0  100.0  100.0   100.000000
2026-01-02    NaN  100.0  110.0   103.333333
2026-01-03    NaN  100.0  110.0   106.666667
2026-01-04  110.0  110.0  110.0   110.000000
2026-01-05    NaN  110.0  120.0   113.333333
2026-01-06    NaN  110.0  120.0   116.666667
2026-01-07  120.0  120.0  120.0   120.000000
```
**What it means:** Headcount is a step number (it changes only when someone joins or leaves), so ffill is the honest choice. Interpolate invents 103.3 people.
**Alternative:** `headcount.resample("D").ffill()` does the resample and fill in one step.
**Likely follow-ups:**
1. Why mean() before filling? resample needs some calculation; with one value per bucket mean just returns it.
2. Does interpolate fill leading NaN? No, not at the start by default.
**Common mistakes:** Interpolating counts or totals. Using bfill and leaking future information into the past.

### Q35 ⭐ 🟡 How do you subtract or add months and days to a date column using Timedelta and DateOffset?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know that days are fixed length but months are not.
**Say this in the interview:** "For a fixed number of days I add a Timedelta. For calendar units like months or years I use DateOffset, because months have different lengths and pandas handles that."
**Explain simply:**
- `pd.Timedelta(days=90)` is an exact length of time: 90 days always.
- `pd.DateOffset(months=6)` moves on the calendar: 6 months later, same day number.
- Timedelta cannot do months (a month is 28 to 31 days). Use DateOffset for months and years.
- If the day does not exist (31 Jan plus 1 month), DateOffset lands on the last valid day (28 Feb), checked by running.
**Sample data:** Three employees with joining dates. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

employees = pd.DataFrame({
    "employee": ["Asha", "Ravi", "Meena"],
    "joining_date": pd.to_datetime(["2026-01-31", "2026-03-15", "2026-08-20"]),
})

# Fixed number of days
employees["probation_end"] = employees["joining_date"] + pd.Timedelta(days=90)

# Calendar months (handles month lengths)
employees["review_date"] = employees["joining_date"] + pd.DateOffset(months=6)

# Go back one year
employees["last_year"] = employees["joining_date"] - pd.DateOffset(years=1)
print(employees)
```
**Output:**
```text
  employee joining_date probation_end review_date  last_year
0     Asha   2026-01-31    2026-05-01  2026-07-31 2025-01-31
1     Ravi   2026-03-15    2026-06-13  2026-09-15 2025-03-15
2    Meena   2026-08-20    2026-11-18  2027-02-20 2025-08-20
```
**What it means:** Probation end is exactly 90 days later; the review date is the same day number six months on.
**Likely follow-ups:**
1. Can I add 6 months with Timedelta(days=180)? Only roughly; it will drift from the calendar date.
2. Does it work on a whole column? Yes, both work on a datetime column in one step.
**Common mistakes:** Trying `Timedelta(months=1)` (not allowed). Adding to a text column that was never converted with `pd.to_datetime`.

### Q36 ⭐ 🟡 How do you find the last working day or month-end date for each row using pandas offsets?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know pandas offsets (ready-made calendar rules) and their roll-forward behaviour.
**Say this in the interview:** "MonthEnd(0) gives the month-end date, and BMonthEnd gives the last business day, meaning Monday to Friday. I start from the first of the month so the result always stays inside the same month."
**Explain simply:**
- An offset is a calendar rule, like "go to the end of the month".
- `MonthEnd(0)`: zero means "stay if already at month-end, else jump to this month's end".
- `BMonthEnd` is the business version (skips Saturday and Sunday). It does not know public holidays.
- Trap: `BMonthEnd(0)` on 31 May 2026 (a Sunday) rolls forward to 30 June. So I start from the 1st of the month.
**Sample data:** Three invoice dates. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

invoices = pd.DataFrame({
    "invoice_date": pd.to_datetime(["2026-02-10", "2026-05-31", "2026-08-30"]),
})

# Month-end date for each row (0 means: stay put if already month-end)
invoices["month_end"] = invoices["invoice_date"] + pd.offsets.MonthEnd(0)

# Last working day (Mon-Fri): start from the 1st of the month, then jump to month-end
month_start = invoices["invoice_date"].dt.to_period("M").dt.to_timestamp()
invoices["last_working_day"] = month_start + pd.offsets.BMonthEnd(0)
print(invoices)
```
**Output:**
```text
  invoice_date  month_end last_working_day
0   2026-02-10 2026-02-28       2026-02-27
1   2026-05-31 2026-05-31       2026-05-29
2   2026-08-30 2026-08-31       2026-08-31
```
**What it means:** 28 Feb 2026 is a Saturday, so the last working day is Friday 27 Feb. 31 May is a Sunday, so it is 29 May.
**Likely follow-ups:**
1. What about holidays? Use `pd.offsets.CustomBusinessDay(holidays=[...])`.
2. Add one month-end ahead? `MonthEnd(1)` always moves to the next month-end.
**Common mistakes:** Using BMonthEnd(0) straight on the date column and jumping into next month. Forgetting that Indian public holidays are not excluded.

### Q37 ⭐ 🟡 Write code to calculate working days between two dates, excluding weekends, using numpy busday_count.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can count business days and remember the end date is excluded.
**Say this in the interview:** "numpy's busday_count counts Monday to Friday days from start up to but not including the end. So to count the end date I add one day."
**Explain simply:**
- "Busday" means business day: Monday to Friday.
- `np.busday_count(start, end)` counts days in the range start to end, with end left out.
- Inputs must be numpy day-type dates, so I convert with `.astype("datetime64[D]")` (a plain datetime column raised an error when I ran it).
- It ignores holidays unless you pass `holidays=[...]`.
**Sample data:** Two leave requests. (created inside the code)
**Code (what you write in the interview):**
```python
import numpy as np
import pandas as pd

leaves = pd.DataFrame({
    "employee": ["Asha", "Ravi"],
    "start_date": pd.to_datetime(["2026-03-02", "2026-03-04"]),
    "end_date": pd.to_datetime(["2026-03-13", "2026-03-10"]),
})

# busday_count leaves out the end date, so add 1 day to include it
end_inclusive = leaves["end_date"] + pd.Timedelta(days=1)
leaves["working_days"] = np.busday_count(
    leaves["start_date"].values.astype("datetime64[D]"),
    end_inclusive.values.astype("datetime64[D]"),
)
print(leaves)
```
**Output:**
```text
  employee start_date   end_date  working_days
0     Asha 2026-03-02 2026-03-13            10
1     Ravi 2026-03-04 2026-03-10             5
```
**What it means:** 2 to 13 March 2026 (Monday to Friday of the next week) has two full work weeks, so 10 days. Ravi's range has 5.
**Alternative:** `pd.bdate_range(start, end)` lists the business days; `len()` of it counts them, but only one row at a time.
**Likely follow-ups:**
1. How do I exclude holidays? `np.busday_count(..., holidays=["2026-03-04"])`.
2. Some countries work Saturday? Use the `weekmask` argument.
**Common mistakes:** Forgetting the end date is excluded (off by one). Subtracting dates and using `.dt.days` when asked for working days.

### Q38 ⭐ 🟡 Write code to find the gap in days between consecutive events (for example logins) for each employee.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you combine sorting, groupby, shift and date subtraction correctly.
**Say this in the interview:** "I sort by employee and date, use groupby with shift to get each person's previous login, and subtract. The first login of each employee has no previous one, so it stays empty."
**Explain simply:**
- `shift()` moves a column down one row, so each row sees the row above it.
- Doing it inside `groupby("employee")` stops one employee's last login from leaking into the next employee's first.
- Subtracting two dates gives a Timedelta (a length of time); `.dt.days` turns it into a plain number.
- Sorting first is essential; the shift just uses the row order.
**Sample data:** Five logins for two employees. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

logins = pd.DataFrame({
    "employee": ["Asha", "Asha", "Asha", "Ravi", "Ravi"],
    "login_date": pd.to_datetime(
        ["2026-01-01", "2026-01-04", "2026-01-10", "2026-01-02", "2026-01-03"]
    ),
})

logins = logins.sort_values(["employee", "login_date"])

# Previous login for the same employee, then the difference in days
logins["previous_login"] = logins.groupby("employee")["login_date"].shift()
logins["gap_days"] = (logins["login_date"] - logins["previous_login"]).dt.days
print(logins)
```
**Output:**
```text
  employee login_date previous_login  gap_days
0     Asha 2026-01-01            NaT       NaN
1     Asha 2026-01-04     2026-01-01       3.0
2     Asha 2026-01-10     2026-01-04       6.0
3     Ravi 2026-01-02            NaT       NaN
4     Ravi 2026-01-03     2026-01-02       1.0
```
**What it means:** Asha waited 3 days, then 6 days. Each employee's first login is NaT (not a time, the empty marker for dates).
**Alternative:** `logins.groupby("employee")["login_date"].diff().dt.days` does it in one line.
**Likely follow-ups:**
1. Why is gap_days a decimal? NaN forces a float column.
2. How to flag gaps over 7 days? `logins["gap_days"] > 7`.
**Common mistakes:** Shifting without groupby (mixing employees). Not sorting by date first.

### Q39 ⭐ 🟡 How do you compare this month with the same month last year in pandas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can build a year-over-year (YoY) comparison and know shift(12) needs complete monthly data.
**Say this in the interview:** "With one row per month in order, shift(12) brings in the value from 12 months earlier. Then growth is current divided by last year, minus one."
**Explain simply:**
- YoY (year over year) compares a month with the same month a year before, which removes seasonality (festival or year-end peaks).
- `shift(12)` moves values down 12 rows. It is only correct when there are no missing months.
- The first 12 rows have no last-year value, so they are NaN.
- If months can be missing, first resample to monthly so every month has a row (or merge on a year-ago date).
**Sample data:** Monthly sales from Jan 2025 to Mar 2026. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "month": pd.date_range("2025-01-01", periods=15, freq="MS"),
    "amount": [100, 110, 120, 130, 125, 140, 150, 145, 160, 170, 180, 200, 130, 132, 150],
})

# shift(12) brings the value from 12 rows (months) earlier
sales["same_month_last_year"] = sales["amount"].shift(12)
sales["yoy_growth_pct"] = ((sales["amount"] / sales["same_month_last_year"] - 1) * 100).round(1)
print(sales.tail(4))
```
**Output:**
```text
        month  amount  same_month_last_year  yoy_growth_pct
11 2025-12-01     200                   NaN             NaN
12 2026-01-01     130                 100.0            30.0
13 2026-02-01     132                 110.0            20.0
14 2026-03-01     150                 120.0            25.0
```
**What it means:** January 2026 sales are 30% above January 2025. December 2025 has no earlier year in the data, so it is empty.
**Alternative:** `sales["amount"].pct_change(12) * 100` gives the same growth in one step.
**Likely follow-ups:**
1. What if a month is missing? Resample to monthly first so every month has a row.
2. Why not compare with last month? Seasonality: December is always busy.
**Common mistakes:** Using shift(1) (that is month-on-month). Running shift(12) on unsorted or gappy data.

### Q40 ⭐ 🔴 How do you handle time zones in pandas using tz_localize and tz_convert?
**Asked at:** commonly asked (no company-specific report found); time zones appear as a talking point in a Coursera India pandas question list (snippet only).
**What the interviewer is checking:** Whether you know the difference between labelling a time with a zone and converting between zones.
**Say this in the interview:** "A normal datetime has no time zone. tz_localize attaches one, saying where the clock times were recorded. tz_convert then changes to another zone, which shows the same moment on a different clock."
**Explain simply:**
- Time zone naive means the time has no zone attached; "09:00" could be anywhere.
- `tz_localize("Asia/Kolkata")` means: these times were recorded in India. It does not change the clock value.
- `tz_convert("Europe/London")` converts an already-labelled time to another zone and changes the clock value.
- Order matters: localize first, convert second. Convert on a naive time raises an error.
**Sample data:** Two login times recorded in Indian time. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

logins = pd.DataFrame({
    "login_time": pd.to_datetime(["2026-03-01 09:00", "2026-03-01 17:30"]),
})

# Step 1: say which zone the clock times were recorded in
logins["india_time"] = logins["login_time"].dt.tz_localize("Asia/Kolkata")

# Step 2: convert to another zone (same moment, different clock)
logins["london_time"] = logins["india_time"].dt.tz_convert("Europe/London")
print(logins)
```
**Output:**
```text
           login_time                india_time               london_time
0 2026-03-01 09:00:00 2026-03-01 09:00:00+05:30 2026-03-01 03:30:00+00:00
1 2026-03-01 17:30:00 2026-03-01 17:30:00+05:30 2026-03-01 12:00:00+00:00
```
**What it means:** 9:00 in India is 3:30 in London (India is 5 hours 30 minutes ahead in March). The moment is identical, only the clock differs.
**Likely follow-ups:**
1. How do I remove the zone again? `.dt.tz_localize(None)`.
2. What about daylight saving? Named zones like Europe/London handle it; tz_localize can raise errors for clock times that are ambiguous or do not exist at the change.
**Common mistakes:** Using tz_convert on naive times. Using tz_localize when you meant to convert (it relabels, it does not shift).

### Q41 ⭐ 🔴 How do you convert Unix timestamps (epoch seconds) to readable dates in pandas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the `unit` argument and the common seconds vs milliseconds trap.
**Say this in the interview:** "A Unix timestamp is the number of seconds since 1 January 1970. I convert it with pd.to_datetime and unit='s'. If the numbers are milliseconds I use unit='ms'."
**Explain simply:**
- Epoch means the starting point, 1 Jan 1970 UTC; a Unix timestamp counts seconds from there.
- Systems and logs (app events, biometric machines, APIs) often store time this way.
- `unit="s"` for seconds (10 digits), `"ms"` for milliseconds (13 digits).
- The result is in UTC. For India, add `.dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")`.
**Sample data:** Three event timestamps in seconds. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

events = pd.DataFrame({"epoch_seconds": [1767225600, 1767312000, 1772323200]})

events["event_time"] = pd.to_datetime(events["epoch_seconds"], unit="s")
print(events)
```
**Output:**
```text
   epoch_seconds event_time
0     1767225600 2026-01-01
1     1767312000 2026-01-02
2     1772323200 2026-03-01
```
**What it means:** The big numbers are now normal dates (midnight UTC, so no time shows).
**Likely follow-ups:**
1. What if I forget unit? Pandas assumes nanoseconds and gives dates in 1970.
2. How do I go back to a number? Subtract the epoch and divide: `(dates - pd.Timestamp("1970-01-01")) // pd.Timedelta(seconds=1)`.
**Common mistakes:** Mixing up seconds and milliseconds (dates land in 1970 or in a far-future year such as 57971, both seen by running). Forgetting the result is UTC, not local time.

### Q42 ⭐ 🔴 How do you use pd.Grouper to group by month while also grouping by another column?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can mix a time bucket and a normal column inside one groupby.
**Say this in the interview:** "I pass a list to groupby: pd.Grouper with the date column and a frequency, plus the department column. That gives me counts per month per department without setting the date as the index."
**Explain simply:**
- `pd.Grouper(key="joining_date", freq="MS")` means: bucket this date column by month (MS is month start).
- It sits inside the groupby list next to normal column names.
- This is the way to do "resample plus groupby" in one go.
- Months with zero rows for a department simply do not appear, unlike resample on one series.
**Sample data:** Six hires with a joining date and department. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

hires = pd.DataFrame({
    "joining_date": pd.to_datetime(
        ["2026-01-05", "2026-01-20", "2026-02-03", "2026-02-10", "2026-02-25", "2026-03-01"]
    ),
    "department": ["HR", "IT", "HR", "IT", "IT", "HR"],
})

hires_per_month = hires.groupby(
    [pd.Grouper(key="joining_date", freq="MS"), "department"]
).size()
print(hires_per_month)
```
**Output:**
```text
joining_date  department
2026-01-01    HR            1
              IT            1
2026-02-01    HR            1
              IT            2
2026-03-01    HR            1
dtype: int64
```
**What it means:** IT hired 2 people in February; HR hired 1 in each month.
**Alternative:** Set the date as index, then `hires.set_index("joining_date").groupby("department").resample("MS").size()`.
**Likely follow-ups:**
1. How do I get departments as columns? Add `.unstack()`.
2. Can I group by quarter? Use `freq="QS"`.
**Common mistakes:** Forgetting `key=` for a column. Leaving the date as text, so Grouper fails.

### Q43 ⭐ 🔴 How do you detect and handle outliers or spikes in a daily time series?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can flag unusual days with a simple rule and handle them thoughtfully, not blindly delete.
**Say this in the interview:** "I flag days outside the IQR fences, meaning far from the middle 50% of values. Then I check the cause. If it is a data error I replace it with a rolling median, but if it is a real event I keep it and report it."
**Explain simply:**
- Outlier or spike: a value far from the usual range (a day with 200 orders when normal is 50).
- IQR rule: Q1 is the 25% mark, Q3 the 75% mark, IQR = Q3 - Q1. Anything below Q1 - 1.5 x IQR or above Q3 + 1.5 x IQR is flagged.
- A rolling median (middle value of nearby days) is a safe replacement because one spike cannot drag it.
- First ask why: a system double-count, a bulk hiring drive, a sale day?
**Sample data:** Ten days of orders with one spike of 200. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

orders = pd.Series(
    [50, 52, 49, 51, 200, 48, 53, 50, 47, 51],
    index=pd.date_range("2026-01-01", periods=10, freq="D"),
)

# IQR rule: anything far outside the middle 50% is a spike
q1 = orders.quantile(0.25)
q3 = orders.quantile(0.75)
iqr = q3 - q1
spikes = orders[(orders < q1 - 1.5 * iqr) | (orders > q3 + 1.5 * iqr)]
print(spikes)

# Handle: replace the spike with the median of its neighbours (rolling)
rolling_median = orders.rolling(3, center=True, min_periods=1).median()
cleaned = orders.where(~orders.index.isin(spikes.index), rolling_median)
print(cleaned)
```
**Output:**
```text
2026-01-05    200
Freq: D, dtype: int64
2026-01-01    50
2026-01-02    52
2026-01-03    49
2026-01-04    51
2026-01-05    51
2026-01-06    48
2026-01-07    53
2026-01-08    50
2026-01-09    47
2026-01-10    51
Freq: D, dtype: int64
```
**What it means:** Only 5 January was flagged, and it was replaced by 51, in line with its neighbours; all other days are untouched.
**Alternative:** A z-score (how many standard deviations from the mean) works, but one big spike inflates the standard deviation, so IQR is more robust.
**Likely follow-ups:**
1. Why not just delete the row? That leaves a hole in the calendar and may hide a real event.
2. What about seasonal peaks? Compare against the same weekday or month, not the whole series.
**Common mistakes:** Treating every outlier as an error. Using a mean-based rule that the spike itself distorts.

### Q44 ⭐ 🔴 How do you split a time series into train and test sets without shuffling, and why does order matter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand data leakage (using the future to predict the past).
**Say this in the interview:** "I sort by date and cut at a point: the earlier part is training and the later part is test. I never shuffle, because a random split would let the model see the future and give an unrealistically good score."
**Explain simply:**
- Train set: the data the model learns from. Test set: unseen data used to check it.
- In a forecast, the test set must be later than the train set, like real life where tomorrow is unknown.
- Shuffling mixes future rows into training. That is called data leakage, and the score looks great but fails in production.
- Cut by position with `iloc`, or by a date.
**Sample data:** Twelve months of sales. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

sales = pd.DataFrame({
    "month": pd.date_range("2024-01-01", periods=12, freq="MS"),
    "amount": [100, 105, 110, 108, 115, 120, 125, 130, 128, 135, 140, 150],
})

sales = sales.sort_values("month")
split_point = int(len(sales) * 0.75)    # first 75% for training

train = sales.iloc[:split_point]
test = sales.iloc[split_point:]
print(train["month"].max(), test["month"].min(), len(train), len(test))
```
**Output:**
```text
2024-09-01 00:00:00 2024-10-01 00:00:00 9 3
```
**What it means:** Training runs through September (9 months) and the test starts in October (3 months), so the test is entirely after the training.
**Alternative:** Split by date: `train = sales[sales["month"] < "2024-10-01"]`. scikit-learn's `train_test_split(..., shuffle=False)` does the same (not run here).
**Likely follow-ups:**
1. What is better than one split? Walk-forward (rolling) validation: train on a growing past, test on the next period, repeat.
2. Why is random split fine for other data? Rows there are independent; time series rows are not.
**Common mistakes:** Using the default shuffled train_test_split. Forgetting to sort by date first.

### Q45 ⭐ 🔴 What is a Period in pandas, and how does it differ from a Timestamp?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know a Period is a span of time (a whole month) and a Timestamp is one exact moment.
**Say this in the interview:** "A Timestamp is a single point in time, like 15 Jan 2026 10:30. A Period is a whole span, like January 2026. Periods are handy for monthly reporting because every date in the month maps to the same label."
**Explain simply:**
- Timestamp: one instant, with day and time.
- Period: a block with a frequency, such as month ("M"), quarter ("Q") or year ("Y").
- Converting dates with `.dt.to_period("M")` makes all January dates identical, which makes counting or grouping by month easy.
- Convert back with `.dt.start_time` (first moment of the span).
**Sample data:** Three joining dates. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

joining = pd.Series(pd.to_datetime(["2026-01-15", "2026-01-28", "2026-02-03"]))

months = joining.dt.to_period("M")
print(months)
print(months.value_counts().sort_index())
print(months.dt.start_time)
```
**Output:**
```text
0    2026-01
1    2026-01
2    2026-02
dtype: period[M]
2026-01    2
2026-02    1
Name: count, dtype: int64
0   2026-01-01
1   2026-01-01
2   2026-02-01
dtype: datetime64[us]
```
**What it means:** The two January joiners now share the label 2026-01, so counting hires per month is one line.
**Likely follow-ups:**
1. Why not always use Period? It cannot hold a time of day, and some plotting and merge tools prefer Timestamps.
2. How do I get the last moment of the span? `.dt.end_time`.
**Common mistakes:** Treating a Period like a date and doing date maths on it. Forgetting to convert back before merging with a Timestamp column.

### Q46 ⭐ 🔴 What is the difference between closed and label arguments in resample, and when do they matter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand how bucket edges are decided, a detail that shifts totals.
**Say this in the interview:** "resample cuts time into buckets. closed says which edge of the bucket owns a boundary timestamp, left or right. label says which edge is used as the bucket's name. They matter when data sits exactly on a boundary, like midnight or month-end."
**Explain simply:**
- A bucket has a left edge and a right edge, for example 00:00 to 03:00.
- `closed="left"`: the left edge belongs to the bucket (00:00 in, 03:00 out). `closed="right"`: the right edge belongs (03:00 in, 00:00 out).
- `label` only changes the name shown (the left or right edge); it never moves data.
- Defaults: left and left for hours, days and month-start; right and right for month-end (`ME`), quarter-end, year-end and weekly.
**Sample data:** Six hourly readings, each worth 1. (created inside the code)
**Code (what you write in the interview):**
```python
import pandas as pd

hours = pd.Series(
    1,
    index=pd.date_range("2026-01-01 00:00", periods=6, freq="h"),
)

# 3-hour buckets with the default settings, and with right-closed
print(hours.resample("3h").sum())
print(hours.resample("3h", closed="right", label="right").sum())
```
**Output:**
```text
2026-01-01 00:00:00    3
2026-01-01 03:00:00    3
Freq: 3h, dtype: int64
2026-01-01 00:00:00    1
2026-01-01 03:00:00    3
2026-01-01 06:00:00    2
Freq: 3h, dtype: int64
```
**What it means:** By default 00:00 to 02:00 form one bucket of 3. With closed on the right, the reading at exactly 00:00 sits alone in an earlier bucket, and 03:00 joins the bucket before it. Same data, different totals.
**Likely follow-ups:**
1. Why does month-end default to right? A month-end label like 31 Jan should include 31 Jan itself.
2. When do I need to change them? When timestamps are exact boundaries, such as midnight login times or a cut-off hour.
**Common mistakes:** Changing label and expecting totals to change (only closed moves data). Not noticing different defaults between `MS` and `ME`.
