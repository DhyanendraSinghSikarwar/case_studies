# Book 2 — SQL | Part 9: Retention, Cohorts, Funnels, MoM Growth 🔴

**Target:** 40 questions | **Actual:** 46 questions
**Scope:** MoM/YoY/QoQ growth, retention and churn, cohort tables, funnel conversion, DAU/WAU/MAU, new vs repeat customers, consecutive-day activity, sessions, repeat purchase. (Generic dedupe, nth-highest, recursive CTE and optimisation sit in Part 10; plain window-function basics in Parts 5-6.)

### Q1 ⭐⭐⭐ 🟢 Using an events table (user_id, event_time), calculate DAU, WAU and MAU (daily, weekly and monthly active users). Why must you use COUNT(DISTINCT user_id)?
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you count people instead of rows, and can group by day, week and month.
**Say this in the interview:** DAU, WAU and MAU are the number of different users active in a day, a week and a month. I group by the time bucket and use COUNT(DISTINCT user_id), because one user can create many event rows and I must count each person once.
**Explain simply:**
- **DAU/WAU/MAU** = Daily/Weekly/Monthly Active Users: how many *different people* did something in that day, week or month.
- `COUNT(*)` counts rows (events). A person who clicks 10 times would be counted 10 times. `COUNT(DISTINCT user_id)` counts each person once.
- You cannot add daily numbers to get the monthly number: the same person is active on many days, so MAU is usually much smaller than the sum of DAU.
- SQLite has no DATE_TRUNC, so the day is `date(event_time)`, the week start (Monday) is `date(event_time,'weekday 0','-6 days')` and the month is `strftime('%Y-%m', ...)`.
**Example:** Ravi opens the HR app twice on Monday 6 Jan. `COUNT(*)` says 2 but DAU is 1 for him. In the sample, 6 Jan has 3 events but only 2 active users.
**Sample data:**

`events`

| user_id | event_time |
|---|---|
| 1 | 2025-01-06 09:10:00 |
| 1 | 2025-01-06 18:30:00 |
| 2 | 2025-01-06 11:00:00 |
| 1 | 2025-01-07 10:00:00 |
| 3 | 2025-01-07 12:15:00 |
| 2 | 2025-01-08 08:45:00 |
| 2 | 2025-01-08 20:00:00 |
| 2 | 2025-01-14 09:00:00 |
| 4 | 2025-01-14 10:00:00 |
| 1 | 2025-01-15 09:30:00 |
| 1 | 2025-02-03 09:00:00 |
| 5 | 2025-02-03 13:00:00 |
**SQL:**
```sql
-- 1) DAU (daily)
SELECT date(event_time) AS day,
       COUNT(*)                AS events,
       COUNT(DISTINCT user_id) AS dau
FROM events
GROUP BY date(event_time)
ORDER BY day;
```
```sql
-- 2) WAU (week starts Monday)
SELECT date(event_time, 'weekday 0', '-6 days') AS week_start,
       COUNT(DISTINCT user_id)                    AS wau
FROM events
GROUP BY week_start
ORDER BY week_start;
```
```sql
-- 3) MAU (calendar month)
SELECT strftime('%Y-%m', event_time) AS month,
       COUNT(DISTINCT user_id)        AS mau
FROM events
GROUP BY month
ORDER BY month;
```
```sql
-- PostgreSQL (not run here): DATE_TRUNC('week', event_time)::date (ISO week, Monday start), DATE_TRUNC('month', event_time)
-- MySQL (not run here): DATE(event_time), YEARWEEK(event_time, 1), DATE_FORMAT(event_time, '%Y-%m')
-- SQL Server (not run here): CAST(event_time AS date), DATETRUNC(week, event_time) in SQL Server 2022+ (week start depends on DATEFIRST)
```
**Output:**

*1) DAU (daily)*

| day | events | dau |
|---|---|---|
| 2025-01-06 | 3 | 2 |
| 2025-01-07 | 2 | 2 |
| 2025-01-08 | 2 | 1 |
| 2025-01-14 | 2 | 2 |
| 2025-01-15 | 1 | 1 |
| 2025-02-03 | 2 | 2 |

*2) WAU (week starts Monday)*

| week_start | wau |
|---|---|
| 2025-01-06 | 3 |
| 2025-01-13 | 3 |
| 2025-02-03 | 2 |

*3) MAU (calendar month)*

| month | mau |
|---|---|
| 2025-01 | 4 |
| 2025-02 | 2 |
**pandas equivalent:**
```python
# 1) DAU (daily)
e = events.assign(ts=pd.to_datetime(events["event_time"]))
e["day"] = e["ts"].dt.strftime("%Y-%m-%d")
result = (e.groupby("day").agg(events=("user_id", "size"), dau=("user_id", "nunique"))
            .reset_index())
```
Result (actual run):
```text
       day  events  dau
2025-01-06       3    2
2025-01-07       2    2
2025-01-08       2    1
2025-01-14       2    2
2025-01-15       1    1
2025-02-03       2    2
```
```python
# 2) WAU (week starts Monday)
e = events.assign(ts=pd.to_datetime(events["event_time"]))
e["week_start"] = (e["ts"].dt.normalize() - pd.to_timedelta(e["ts"].dt.weekday, unit="D")).dt.strftime("%Y-%m-%d")
result = e.groupby("week_start").agg(wau=("user_id", "nunique")).reset_index()
```
Result (actual run):
```text
week_start  wau
2025-01-06    3
2025-01-13    3
2025-02-03    2
```
```python
# 3) MAU (calendar month)
e = events.assign(ts=pd.to_datetime(events["event_time"]))
e["month"] = e["ts"].dt.strftime("%Y-%m")
result = e.groupby("month").agg(mau=("user_id", "nunique")).reset_index()
```
Result (actual run):
```text
  month  mau
2025-01    4
2025-02    2
```
**Edge cases:** Users with several events in one day are counted once in DAU. A day with no events has no row at all (use a calendar table if you need a 0 row, see Q5). `event_time` must be a proper timestamp; if it is stored as text in another format, convert first. A rolling 7-day or 30-day active count is a different metric from the calendar week/month used here.
**Likely follow-ups:**
- Why is MAU not the sum of DAU? Because the same person is active on many days; summing counts them again and again.
- How do you get a rolling 30-day MAU? Self-join each date to events in the previous 30 days and count distinct users (heavier query).
- What if there are bots or test users? Filter them out before counting.
**Common mistakes:** Using `COUNT(user_id)` or `COUNT(*)` (counts events, not people), adding DAUs to get MAU, and grouping by the full timestamp instead of the date.

### Q2 ⭐⭐⭐ 🟢 Using an orders table (order_id, order_date, amount), calculate monthly revenue and the month-over-month (MoM) growth percentage using LAG.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you aggregate to one row per month first and then use LAG on the monthly totals, with the right growth formula.
**Say this in the interview:** First I total revenue per month. Then LAG(revenue) gives the previous month on the same row, and growth % is (this month minus last month) divided by last month, times 100.
**Explain simply:**
- **MoM** = month-over-month: how much this month changed compared with last month, as a percentage.
- **LAG(col)** is a window function that reads the value from the previous row in the order you choose, without a self-join.
- Order of work: group to months in a CTE (a named temporary result), then apply LAG on that small table. LAG on raw orders would compare orders, not months.
- The first month has no previous month, so LAG returns NULL and growth is NULL, which is the honest answer.
**Example:** Payroll cost or sales: Jan 1,200, Feb 1,500. Growth = (1,500 - 1,200) / 1,200 = 25%.
**Sample data:**

`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2025-01-05 | 500 |
| 2 | 2025-01-20 | 700 |
| 3 | 2025-02-03 | 900 |
| 4 | 2025-02-18 | 600 |
| 5 | 2025-03-07 | 1350 |
| 6 | 2025-04-02 | 1000 |
| 7 | 2025-04-25 | 800 |
**SQL:**
```sql
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month,
           SUM(amount)                   AS revenue
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
), with_prev AS (
    SELECT month, revenue,
           LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT month, revenue, prev_revenue,
       ROUND(100.0 * (revenue - prev_revenue) / prev_revenue, 1) AS mom_pct
FROM with_prev
ORDER BY month;
```
```sql
-- PostgreSQL (not run here): to_char(order_date, 'YYYY-MM')  or  date_trunc('month', order_date)
-- MySQL 8+ (not run here): DATE_FORMAT(order_date, '%Y-%m')
-- SQL Server (not run here): FORMAT(order_date, 'yyyy-MM')  or  EOMONTH(order_date)
-- LAG() itself works in PostgreSQL, MySQL 8+, SQL Server 2012+ (from memory).
```
**Output:**

| month | revenue | prev_revenue | mom_pct |
|---|---|---|---|
| 2025-01 | 1200 | NULL | NULL |
| 2025-02 | 1500 | 1200 | 25 |
| 2025-03 | 1350 | 1500 | -10 |
| 2025-04 | 1800 | 1350 | 33.3 |
**pandas equivalent:**
```python
m = (orders.assign(month=pd.to_datetime(orders["order_date"]).dt.strftime("%Y-%m"))
           .groupby("month", as_index=False)["amount"].sum()
           .rename(columns={"amount": "revenue"}))
m["prev_revenue"] = m["revenue"].shift(1)
m["mom_pct"] = ((m["revenue"] - m["prev_revenue"]) / m["prev_revenue"] * 100).round(1)
result = m
```
Result (actual run):
```text
  month  revenue  prev_revenue  mom_pct
2025-01     1200           NaN      NaN
2025-02     1500        1200.0     25.0
2025-03     1350        1500.0    -10.0
2025-04     1800        1350.0     33.3
```
**Edge cases:** First month = NULL (no previous). A month with no orders is simply missing, so LAG would compare with two months ago: fix with a calendar table (Q5). If last month is 0 the division fails: use NULLIF (Q5). Multiply by 100.0 (not 100) so integers do not use integer division.
**Likely follow-ups:**
- How do you do YoY? Compare with the same month last year (Q12).
- Why not LAG on orders directly? Each order row would be compared with the previous order, not the previous month.
- Percent points or percent? Growth is a percent change; if the metric is itself a percentage, report the difference in percentage points.
**Common mistakes:** Applying LAG before grouping, dividing by the current month instead of the previous, and integer division (`100 * (a-b) / b` with whole numbers can be fine but `(a-b)/b` alone gives 0).

### Q3 ⭐⭐⭐ 🟢 Given a funnel_events table (user_id, step: view/cart/purchase), count the users at each step and the overall conversion percentage from view to purchase.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you count distinct users per step and compute the conversion against the first step.
**Say this in the interview:** I count distinct users at each step, then divide the purchase users by the view users. Here 2 of 6 viewers bought, so overall conversion is 33.3%.
**Explain simply:**
- A **funnel** is the path users follow, for example view, then cart, then purchase. Each step has fewer people.
- **Conversion %** = users at a later step / users at the first step x 100.
- Count `DISTINCT user_id`, because a user can view the same product many times (user 1 has two view rows).
- Two ways to show it: one row per step (good for charts) or one row with conditional counts (good for a single KPI).
**Example:** Hiring funnel: 600 applied, 90 interviewed, 18 joined: 18/600 = 3% overall conversion.
**Sample data:**

`funnel_events`

| user_id | step |
|---|---|
| 1 | view |
| 1 | view |
| 2 | view |
| 3 | view |
| 4 | view |
| 5 | view |
| 6 | view |
| 1 | cart |
| 2 | cart |
| 3 | cart |
| 4 | cart |
| 1 | purchase |
| 2 | purchase |
**SQL:**
```sql
-- 1) Users per step
SELECT step,
       COUNT(DISTINCT user_id) AS users,
       ROUND(100.0 * COUNT(DISTINCT user_id)
             / (SELECT COUNT(DISTINCT user_id) FROM funnel_events WHERE step = 'view'), 1) AS pct_of_view
FROM funnel_events
GROUP BY step
ORDER BY CASE step WHEN 'view' THEN 1 WHEN 'cart' THEN 2 WHEN 'purchase' THEN 3 END;
```
```sql
-- 2) Overall view to purchase conversion
SELECT viewers, buyers,
       ROUND(100.0 * buyers / viewers, 1) AS view_to_purchase_pct
FROM (SELECT COUNT(DISTINCT CASE WHEN step = 'view'     THEN user_id END) AS viewers,
             COUNT(DISTINCT CASE WHEN step = 'purchase' THEN user_id END) AS buyers
      FROM funnel_events);
```
**Output:**

*1) Users per step*

| step | users | pct_of_view |
|---|---|---|
| view | 6 | 100 |
| cart | 4 | 66.7 |
| purchase | 2 | 33.3 |

*2) Overall view to purchase conversion*

| viewers | buyers | view_to_purchase_pct |
|---|---|---|
| 6 | 2 | 33.3 |
**pandas equivalent:**
```python
# 1) Users per step
g = (funnel_events.groupby("step")["user_id"].nunique()
       .reindex(["view", "cart", "purchase"]).rename("users").reset_index())
g["pct_of_view"] = (g["users"] / g["users"].iloc[0] * 100).round(1)
result = g
```
Result (actual run):
```text
    step  users  pct_of_view
    view      6        100.0
    cart      4         66.7
purchase      2         33.3
```
```python
# 2) Overall view to purchase conversion
viewers = funnel_events.loc[funnel_events["step"] == "view", "user_id"].nunique()
buyers = funnel_events.loc[funnel_events["step"] == "purchase", "user_id"].nunique()
result = pd.DataFrame({"viewers": [viewers], "buyers": [buyers],
                       "view_to_purchase_pct": [round(100.0 * buyers / viewers, 1)]})
```
Result (actual run):
```text
 viewers  buyers  view_to_purchase_pct
       6       2                  33.3
```
**Edge cases:** Duplicate rows are handled by DISTINCT. If a user has a purchase but no view row (tracking gap), the simple count can overstate conversion: use the order-aware version in Q10. If nobody viewed, `viewers` is 0 and the division fails: wrap with NULLIF(viewers, 0). Steps missing from the data simply have no row.
**Likely follow-ups:**
- How do you get step-to-step conversion? Divide each step by the previous one (Q10).
- Should a user be counted if they bought without a view? Usually only if they also did the earlier steps (strict funnel, Q10).
- Time window? Often you restrict the funnel to one session or 7 days.
**Common mistakes:** Using COUNT(*) (counts events), dividing by the wrong base (previous step instead of first step, or the reverse), and forgetting that percent needs `100.0` not `100`.

### Q4 ⭐⭐⭐ 🟢 Count new signups per month from a users table (user_id, signup_date) and show the change versus the previous month.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Basic grouping by month plus LAG for a previous-month comparison.
**Say this in the interview:** I group users by signup month with COUNT, then use LAG to bring last month's count next to this month's and subtract. I show both the absolute change and the percentage.
**Explain simply:**
- `strftime('%Y-%m', signup_date)` turns a date into a month label such as 2025-02, so GROUP BY puts every signup of that month together.
- One row per user, so `COUNT(*)` = signups. If the table could repeat a user, use `COUNT(DISTINCT user_id)`.
- **LAG** reads the previous month's signups into the current row. The first month has NULL.
- Show change in numbers (`+1`) and percent, because small bases make percent jump around.
**Example:** HR hiring: 3 joiners in Jan and 4 in Feb is +1 joiner, +33.3%.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-04 |
| 2 | 2025-01-18 |
| 3 | 2025-01-30 |
| 4 | 2025-02-02 |
| 5 | 2025-02-09 |
| 6 | 2025-02-15 |
| 7 | 2025-02-27 |
| 8 | 2025-03-11 |
| 9 | 2025-03-21 |
| 10 | 2025-04-01 |
| 11 | 2025-04-12 |
| 12 | 2025-04-29 |
**SQL:**
```sql
WITH monthly AS (
    SELECT strftime('%Y-%m', signup_date) AS month,
           COUNT(*)                       AS signups
    FROM users
    GROUP BY strftime('%Y-%m', signup_date)
), with_prev AS (
    SELECT month, signups,
           LAG(signups) OVER (ORDER BY month) AS prev_signups
    FROM monthly
)
SELECT month, signups, prev_signups,
       signups - prev_signups AS change,
       ROUND(100.0 * (signups - prev_signups) / prev_signups, 1) AS change_pct
FROM with_prev
ORDER BY month;
```
**Output:**

| month | signups | prev_signups | change | change_pct |
|---|---|---|---|---|
| 2025-01 | 3 | NULL | NULL | NULL |
| 2025-02 | 4 | 3 | 1 | 33.3 |
| 2025-03 | 2 | 4 | -2 | -50 |
| 2025-04 | 3 | 2 | 1 | 50 |
**pandas equivalent:**
```python
m = (users.assign(month=pd.to_datetime(users["signup_date"]).dt.strftime("%Y-%m"))
          .groupby("month", as_index=False).agg(signups=("user_id", "count")))
m["prev_signups"] = m["signups"].shift(1)
m["change"] = m["signups"] - m["prev_signups"]
m["change_pct"] = (m["change"] / m["prev_signups"] * 100).round(1)
result = m
```
Result (actual run):
```text
  month  signups  prev_signups  change  change_pct
2025-01        3           NaN     NaN         NaN
2025-02        4           3.0     1.0        33.3
2025-03        2           4.0    -2.0       -50.0
2025-04        3           2.0     1.0        50.0
```
**Edge cases:** First month: previous, change and percent are NULL. A month with zero signups has no row, so the next month would be compared with the wrong month (use a calendar spine, Q5). Duplicate user rows inflate the count unless you use DISTINCT. Signups with a NULL signup_date form their own NULL group: filter them out or report them.
**Likely follow-ups:**
- How do you show a running total of signups? `SUM(signups) OVER (ORDER BY month)`.
- Why compute change in the SQL rather than Excel? So the dashboard stays refreshable and consistent.
- What about a month with 0 signups? Build a month list and LEFT JOIN (Q5).
**Common mistakes:** Comparing with the previous row when a month is missing, grouping by full date, and dividing by zero when the previous month is 0.

### Q5 ⭐⭐⭐ 🟡 Calculate MoM growth safely: how do you handle the first month (no previous value), a previous month of zero (divide by zero) and months with no data at all?
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you think about NULL, divide-by-zero and missing months, not only the happy path.
**Say this in the interview:** I build a full list of months, LEFT JOIN revenue onto it and COALESCE gaps to 0. Then LAG gives the previous month, and I divide by NULLIF(previous, 0) so a zero base returns NULL instead of an error.
**Explain simply:**
- **First month**: LAG returns NULL, so growth is NULL. Show it as blank or 'n/a'.
- **Previous month = 0**: dividing by zero is an error in most databases. `NULLIF(x, 0)` turns a 0 into NULL, so the result is NULL (growth from nothing is undefined, not 'infinite').
- **Month with no data**: GROUP BY cannot invent a row. Create a **calendar spine** (list of all months, here a recursive CTE, a query that calls itself to generate rows) and LEFT JOIN revenue; `COALESCE(x, 0)` replaces NULL with 0.
- Add a note column so readers know why a growth value is blank.
**Example:** Revenue Jan 1,000, Feb no orders, Mar 600. Without a spine Mar is compared with Jan (-40%), which hides that Feb was zero. With a spine: Feb -100%, Mar is NULL (base 0).
**Sample data:**

`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2025-01-10 | 600 |
| 2 | 2025-01-25 | 400 |
| 3 | 2025-03-12 | 600 |
| 4 | 2025-04-08 | 0 |
| 5 | 2025-05-15 | 900 |
**SQL:**
```sql
WITH RECURSIVE spine(month_start) AS (
    SELECT '2025-01-01'
    UNION ALL
    SELECT date(month_start, '+1 month') FROM spine WHERE month_start < '2025-05-01'
), monthly AS (
    SELECT strftime('%Y-%m-01', order_date) AS month_start, SUM(amount) AS revenue
    FROM orders GROUP BY 1
), filled AS (
    SELECT strftime('%Y-%m', s.month_start) AS month,
           COALESCE(m.revenue, 0)           AS revenue
    FROM spine s LEFT JOIN monthly m ON m.month_start = s.month_start
), calc AS (
    SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM filled
)
SELECT month, revenue, prev_revenue,
       ROUND(100.0 * (revenue - prev_revenue) / NULLIF(prev_revenue, 0), 1) AS mom_pct,
       CASE WHEN prev_revenue IS NULL THEN 'first month'
            WHEN prev_revenue = 0     THEN 'no base (previous = 0)'
            ELSE '' END AS note
FROM calc
ORDER BY month;
```
```sql
-- PostgreSQL (not run here): SELECT generate_series(date '2025-01-01', date '2025-05-01', interval '1 month')
-- SQL Server (not run here): use a recursive CTE like the one above (no RECURSIVE keyword), or a numbers/calendar table
-- MySQL 8+ (not run here): WITH RECURSIVE ... DATE_ADD(month_start, INTERVAL 1 MONTH)
```
**Output:**

| month | revenue | prev_revenue | mom_pct | note |
|---|---|---|---|---|
| 2025-01 | 1000 | NULL | NULL | first month |
| 2025-02 | 0 | 1000 | -100 |  |
| 2025-03 | 600 | 0 | NULL | no base (previous = 0) |
| 2025-04 | 0 | 600 | -100 |  |
| 2025-05 | 900 | 0 | NULL | no base (previous = 0) |
**pandas equivalent:**
```python
monthly = (orders.assign(month=pd.to_datetime(orders["order_date"]).dt.strftime("%Y-%m"))
                .groupby("month")["amount"].sum())
idx = pd.period_range("2025-01", "2025-05", freq="M").astype(str)
f = monthly.reindex(idx, fill_value=0).rename_axis("month").reset_index(name="revenue")
f["prev_revenue"] = f["revenue"].shift(1)
f["mom_pct"] = ((f["revenue"] - f["prev_revenue"]) / f["prev_revenue"].replace(0, np.nan) * 100).round(1)
f["note"] = np.select([f["prev_revenue"].isna(), f["prev_revenue"] == 0],
                      ["first month", "no base (previous = 0)"], default="")
result = f
```
Result (actual run):
```text
  month  revenue  prev_revenue  mom_pct                   note
2025-01     1000           NaN      NaN            first month
2025-02        0        1000.0   -100.0                       
2025-03      600           0.0      NaN no base (previous = 0)
2025-04        0         600.0   -100.0                       
2025-05      900           0.0      NaN no base (previous = 0)
```
**Edge cases:** April has an order of amount 0 (a free promo), so it exists but its revenue is 0; May then divides by 0 and returns NULL. March follows an empty February (spine row, revenue 0). SQLite does not raise an error on divide by zero (it returns NULL), but PostgreSQL and SQL Server do, so NULLIF is the portable habit. The spine end date is hard-coded here; in real work take it from MAX(order_date).
**Likely follow-ups:**
- Should growth from 0 be shown as 100% or infinity? Neither: show NULL or 'new' and explain.
- Alternative to a spine? A permanent calendar/date dimension table.
- What if the first month is partial? Exclude it or mark it, because comparing a partial month is misleading.
**Common mistakes:** Trusting LAG when a month is missing, dividing without NULLIF, and treating NULL growth as 0%.

### Q6 ⭐⭐⭐ 🟡 Calculate month-1 retention: of the users who signed up in each month, what percentage were active again in the following month? (users + activity tables)
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Cohort thinking: group users by signup month, then check activity in exactly the next month, counting each user once and ignoring cohorts that are too young.
**Say this in the interview:** A cohort is everyone who signed up in the same month. For each cohort I count users with any activity in the next calendar month and divide by the cohort size. I leave out the latest cohort because its next month has not happened yet.
**Explain simply:**
- **Cohort** = a group of users who share a starting point (signup month). **Month-1 retention** = % of them active again the month after signup.
- LEFT JOIN keeps users who never came back (they become NULL and are not counted as retained).
- `COUNT(DISTINCT ...)` stops a user with many active days from being counted many times.
- **Immature cohort**: April signups cannot have May activity yet, so showing 0% would be wrong. The `WHERE` drops cohorts whose next month is beyond the data.
**Example:** Jan cohort has 4 joiners; 3 of them were active in February, so month-1 retention is 75%.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-05 |
| 2 | 2025-01-12 |
| 3 | 2025-01-20 |
| 4 | 2025-01-28 |
| 5 | 2025-02-03 |
| 6 | 2025-02-10 |
| 7 | 2025-02-17 |
| 8 | 2025-02-24 |
| 9 | 2025-03-02 |
| 10 | 2025-03-09 |
| 11 | 2025-03-14 |
| 12 | 2025-04-03 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-06 |
| 1 | 2025-02-10 |
| 1 | 2025-03-12 |
| 2 | 2025-01-13 |
| 3 | 2025-01-21 |
| 3 | 2025-02-02 |
| 3 | 2025-02-18 |
| 3 | 2025-03-05 |
| 4 | 2025-01-28 |
| 4 | 2025-02-15 |
| 5 | 2025-02-03 |
| 5 | 2025-03-08 |
| 6 | 2025-02-14 |
| 7 | 2025-02-21 |
| 8 | 2025-02-25 |
| 8 | 2025-03-22 |
| 8 | 2025-04-10 |
| 9 | 2025-03-04 |
| 9 | 2025-04-02 |
| 10 | 2025-03-09 |
| 11 | 2025-03-15 |
| 11 | 2025-04-20 |
| 12 | 2025-04-03 |
**SQL:**
```sql
WITH cohort AS (
    SELECT user_id, strftime('%Y-%m', signup_date) AS cohort_month FROM users
)
SELECT c.cohort_month,
       COUNT(DISTINCT c.user_id) AS cohort_size,
       COUNT(DISTINCT a.user_id) AS retained,
       ROUND(100.0 * COUNT(DISTINCT a.user_id) / COUNT(DISTINCT c.user_id), 1) AS month1_retention_pct
FROM cohort c
LEFT JOIN activity a
       ON a.user_id = c.user_id
      AND strftime('%Y-%m', a.activity_date) = strftime('%Y-%m', date(c.cohort_month || '-01', '+1 month'))
WHERE c.cohort_month < (SELECT strftime('%Y-%m', MAX(activity_date)) FROM activity)
GROUP BY c.cohort_month
ORDER BY c.cohort_month;
```
```sql
-- PostgreSQL (not run here): a.activity_date >= c.cohort_start + interval '1 month' AND a.activity_date < c.cohort_start + interval '2 months'
-- MySQL (not run here): DATE_ADD(c.cohort_start, INTERVAL 1 MONTH)   SQL Server (not run here): DATEADD(month, 1, c.cohort_start)
```
**Output:**

| cohort_month | cohort_size | retained | month1_retention_pct |
|---|---|---|---|
| 2025-01 | 4 | 3 | 75 |
| 2025-02 | 4 | 2 | 50 |
| 2025-03 | 3 | 2 | 66.7 |
**pandas equivalent:**
```python
u = users.assign(cohort=pd.to_datetime(users["signup_date"]).dt.to_period("M"))
a = activity.assign(am=pd.to_datetime(activity["activity_date"]).dt.to_period("M"))
m = u.merge(a, on="user_id", how="left")
m["hit"] = m["am"] == (m["cohort"] + 1)
per_user = m.groupby(["cohort", "user_id"], as_index=False)["hit"].max()
last = a["am"].max()
per_user = per_user[per_user["cohort"] < last]
r = per_user.groupby("cohort").agg(cohort_size=("user_id", "size"), retained=("hit", "sum")).reset_index()
r["cohort_month"] = r["cohort"].astype(str)
r["month1_retention_pct"] = (r["retained"] / r["cohort_size"] * 100).round(1)
result = r[["cohort_month", "cohort_size", "retained", "month1_retention_pct"]]
```
Result (actual run):
```text
cohort_month  cohort_size  retained  month1_retention_pct
     2025-01            4         3                  75.0
     2025-02            4         2                  50.0
     2025-03            3         2                  66.7
```
**Edge cases:** The April cohort (1 user) is excluded as immature. Users with no activity at all still count in the cohort size (LEFT JOIN from users). Duplicate activity rows are harmless thanks to DISTINCT. 'Active in the next month' means calendar month; some teams use 'within 30 days' instead, so state your definition.
**Likely follow-ups:**
- How do you get month 2, 3 ...? Build the full cohort table (Q11).
- Calendar month or 30 days? Say which; 30 days avoids month-length effects.
- What if activity includes the signup event itself? Exclude it, or retention is inflated.
**Common mistakes:** Counting rows not users, using an INNER JOIN (drops non-returners and gives 100%), and showing the newest cohort as 0% retention.

### Q7 ⭐⭐⭐ 🟡 For each month, split customers into new (first ever order that month) and repeat (ordered before), with their counts and revenue.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you find each customer's first order date first, then label every order as new or repeat by comparing months.
**Say this in the interview:** I get each customer's first order month with MIN(order_date). A customer is new in that month and repeat in any later month. Then I group by month and type, counting distinct customers and summing revenue.
**Explain simply:**
- Step 1: a CTE with `MIN(order_date)` per customer gives the first-ever order.
- Step 2: join it back to orders; if the order's month equals the first-order month, label `new`, else `repeat`.
- `COUNT(DISTINCT customer_id)` counts people; `SUM(amount)` is revenue.
- Definition used here: a customer is 'new' for the whole month of their first order (customer 101 ordered twice in January, both orders count as new).
**Example:** Customer 103 first orders in Feb (new, 250) and orders again in Mar (repeat, 150).
**Sample data:**

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 1 | 101 | 2025-01-05 | 500 |
| 2 | 102 | 2025-01-12 | 300 |
| 3 | 101 | 2025-01-28 | 200 |
| 4 | 101 | 2025-02-04 | 400 |
| 5 | 103 | 2025-02-10 | 250 |
| 6 | 102 | 2025-02-20 | 350 |
| 7 | 104 | 2025-03-03 | 600 |
| 8 | 103 | 2025-03-15 | 150 |
| 9 | 105 | 2025-03-22 | 100 |
**SQL:**
```sql
WITH first_order AS (
    SELECT customer_id, MIN(order_date) AS first_date
    FROM orders
    GROUP BY customer_id
), tagged AS (
    SELECT strftime('%Y-%m', o.order_date) AS month,
           o.customer_id, o.amount,
           CASE WHEN strftime('%Y-%m', o.order_date) = strftime('%Y-%m', f.first_date)
                THEN 'new' ELSE 'repeat' END AS customer_type
    FROM orders o
    JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT month, customer_type,
       COUNT(DISTINCT customer_id) AS customers,
       SUM(amount)                 AS revenue
FROM tagged
GROUP BY month, customer_type
ORDER BY month, customer_type;
```
**Output:**

| month | customer_type | customers | revenue |
|---|---|---|---|
| 2025-01 | new | 2 | 1000 |
| 2025-02 | new | 1 | 250 |
| 2025-02 | repeat | 2 | 750 |
| 2025-03 | new | 2 | 700 |
| 2025-03 | repeat | 1 | 150 |
**pandas equivalent:**
```python
o = orders.assign(od=pd.to_datetime(orders["order_date"]))
o["month"] = o["od"].dt.strftime("%Y-%m")
first = o.groupby("customer_id")["od"].min().dt.strftime("%Y-%m").rename("first_month")
o = o.join(first, on="customer_id")
o["customer_type"] = np.where(o["month"] == o["first_month"], "new", "repeat")
result = (o.groupby(["month", "customer_type"], as_index=False)
            .agg(customers=("customer_id", "nunique"), revenue=("amount", "sum"))
            .sort_values(["month", "customer_type"]).reset_index(drop=True))
```
Result (actual run):
```text
  month customer_type  customers  revenue
2025-01           new          2     1000
2025-02           new          1      250
2025-02        repeat          2      750
2025-03           new          2      700
2025-03        repeat          1      150
```
**Edge cases:** January has no repeat row because nobody had ordered before. Same-day or same-month second orders are 'new' under the month definition; if you want only the first order to be new, compare order_date to first_date instead. Ties on the first date are fine because only the month is used. NULL customer_id rows would group together: filter them out.
**Likely follow-ups:**
- How do you get the repeat share? repeat revenue / total revenue per month.
- Why not just check if the customer exists in an earlier month? You can, but MIN(order_date) is simpler and faster.
- What about data that starts mid-history? Everyone looks new in the first month of data: exclude that month.
**Common mistakes:** Using the current month's data to define 'new' (so everyone is new), counting orders instead of customers, and forgetting that the first month of the dataset is all 'new'.

### Q8 ⭐⭐⭐ 🟡 Find customers who bought in January but not in February (lost customers), and explain the LEFT JOIN / NOT EXISTS options.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Anti-join knowledge: finding rows in one set that are missing from another, and knowing the NOT IN / NULL trap.
**Say this in the interview:** I take customers with a January order and keep those with no February order, using NOT EXISTS. LEFT JOIN with `IS NULL` gives the same answer; I avoid NOT IN because a single NULL makes it return nothing.
**Explain simply:**
- This pattern is an **anti-join**: 'in A but not in B'.
- **NOT EXISTS**: for each January customer, check there is no February row. Safe with NULLs and usually fast.
- **LEFT JOIN ... WHERE right.key IS NULL**: join February rows to January customers; where no match exists the right side is NULL, so we keep those.
- Put the February date filter in the `ON` clause of the LEFT JOIN, not in `WHERE`, or you turn it back into an inner join.
- `DISTINCT` is needed because a customer may have several January orders.
**Example:** Employees who took leave in January but not in February: same shape, different table.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | 101 | 2025-01-05 |
| 2 | 102 | 2025-01-09 |
| 3 | 103 | 2025-01-15 |
| 4 | 104 | 2025-01-20 |
| 5 | 102 | 2025-01-25 |
| 6 | 101 | 2025-02-03 |
| 7 | 104 | 2025-02-11 |
| 8 | 105 | 2025-02-14 |
| 9 | 103 | 2025-03-02 |
**SQL:**
```sql
SELECT DISTINCT j.customer_id
FROM orders j
WHERE j.order_date >= '2025-01-01' AND j.order_date < '2025-02-01'
  AND NOT EXISTS (SELECT 1 FROM orders f
                  WHERE f.customer_id = j.customer_id
                    AND f.order_date >= '2025-02-01' AND f.order_date < '2025-03-01')
ORDER BY j.customer_id;
```
```sql
-- Alternative: LEFT JOIN ... IS NULL (also run here, same result)
SELECT DISTINCT j.customer_id
FROM orders j
LEFT JOIN orders f ON f.customer_id = j.customer_id AND f.order_date >= '2025-02-01' AND f.order_date < '2025-03-01'
WHERE j.order_date >= '2025-01-01' AND j.order_date < '2025-02-01'
  AND f.order_id IS NULL
ORDER BY j.customer_id;
```
```sql
-- Alternative: NOT IN (fine only if customer_id is never NULL) (also run here, same result)
SELECT DISTINCT j.customer_id
FROM orders j
WHERE j.order_date >= '2025-01-01' AND j.order_date < '2025-02-01'
  AND j.customer_id NOT IN (SELECT f.customer_id FROM orders f WHERE f.order_date >= '2025-02-01' AND f.order_date < '2025-03-01')
ORDER BY j.customer_id;
```
```sql
-- All three forms are standard SQL; date-range syntax differs only if you use DATE_TRUNC/MONTH() helpers (not run here).
```
**Output:**

| customer_id |
|---|
| 102 |
| 103 |
**pandas equivalent:**
```python
om = pd.to_datetime(orders["order_date"]).dt.strftime("%Y-%m")
jan_c = set(orders.loc[om == "2025-01", "customer_id"])
feb_c = set(orders.loc[om == "2025-02", "customer_id"])
result = pd.DataFrame({"customer_id": sorted(jan_c - feb_c)})
```
Result (actual run):
```text
 customer_id
         102
         103
```
**Edge cases:** Customer 103 ordered again in March, but still counts as lost for the Jan-vs-Feb question. Customers who are new in February (105) are not in the result. **NOT IN trap (actual run):** after adding one February order with a NULL customer_id, the NOT IN version returned 0 rows instead of 2, because `x NOT IN (..., NULL)` is never true. NOT EXISTS and LEFT JOIN are unaffected. Use half-open date ranges (`>= start AND < next start`) so timestamps on the last day are not lost.
**Likely follow-ups:**
- Which is fastest? Usually NOT EXISTS and LEFT JOIN plans are similar; check EXPLAIN on your database.
- How do you find new customers in February? Reverse the logic (in Feb, not before).
- Can you use EXCEPT? Yes: January customer ids EXCEPT February customer ids (not run here).
**Common mistakes:** Using NOT IN with a nullable column, putting the right-table filter in WHERE (kills the LEFT JOIN), and forgetting DISTINCT.

### Q9 ⭐⭐⭐ 🟡 Find users who were active on at least 3 consecutive days from a login table (user_id, login_date).
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified). The source for this exact pattern is a user-upload (unverified).
**What the interviewer is checking:** The 'gaps and islands' trick: whether you can spot consecutive dates without a loop, and dedupe repeat logins first.
**Say this in the interview:** I remove duplicate logins, number each user's dates with ROW_NUMBER, and subtract that number from the date. Consecutive days give the same result, so I group by it and keep groups with 3 or more days.
**Explain simply:**
- Take a user's sorted distinct dates: Jan 1, 2, 3, 4. Row numbers are 1, 2, 3, 4. Date minus row number is always Dec 31: same value = one unbroken streak (an 'island').
- If a day is skipped (Jan 1, 2, 4, 5) the subtracted value changes after the gap, so a new group starts.
- Group by user and that value, then `COUNT(*) >= 3` keeps streaks of 3+ days.
- Use DISTINCT first: two logins on the same day would otherwise break the numbering.
**Example:** Attendance: an employee badge-in on 5, 6, 7 Jan is a 3-day streak; 5, 6, 8 is not.
**Sample data:**

`logins`

| user_id | login_date |
|---|---|
| 1 | 2025-01-01 |
| 1 | 2025-01-02 |
| 1 | 2025-01-03 |
| 1 | 2025-01-04 |
| 1 | 2025-01-10 |
| 2 | 2025-01-01 |
| 2 | 2025-01-02 |
| 2 | 2025-01-04 |
| 2 | 2025-01-05 |
| 3 | 2025-01-05 |
| 3 | 2025-01-06 |
| 3 | 2025-01-07 |
| 3 | 2025-01-07 |
| 3 | 2025-01-12 |
| 3 | 2025-01-13 |
| 4 | 2025-01-08 |
| 5 | 2024-12-30 |
| 5 | 2024-12-31 |
| 5 | 2025-01-01 |
**SQL:**
```sql
WITH days AS (
    SELECT DISTINCT user_id, login_date FROM logins
), numbered AS (
    SELECT user_id, login_date,
           DATE(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
    FROM days
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*)        AS streak_days
FROM numbered
GROUP BY user_id, grp
HAVING COUNT(*) >= 3
ORDER BY user_id, streak_start;
```
```sql
-- Alternative: self-join on the next two days (also run here, same result)
WITH days AS (SELECT DISTINCT user_id, login_date FROM logins)
SELECT DISTINCT d1.user_id
FROM days d1
JOIN days d2 ON d2.user_id = d1.user_id AND d2.login_date = date(d1.login_date, '+1 day')
JOIN days d3 ON d3.user_id = d1.user_id AND d3.login_date = date(d1.login_date, '+2 days')
ORDER BY d1.user_id;
```
```sql
-- PostgreSQL (not run here): login_date - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date))::int AS grp
-- MySQL 8+ (not run here): DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) DAY)
-- SQL Server (not run here): DATEADD(day, -ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date), login_date)
```
**Output:**

| user_id | streak_start | streak_end | streak_days |
|---|---|---|---|
| 1 | 2025-01-01 | 2025-01-04 | 4 |
| 3 | 2025-01-05 | 2025-01-07 | 3 |
| 5 | 2024-12-30 | 2025-01-01 | 3 |
**pandas equivalent:**
```python
d = logins.drop_duplicates().copy()
d["dt"] = pd.to_datetime(d["login_date"])
d = d.sort_values(["user_id", "dt"])
d["rn"] = d.groupby("user_id").cumcount() + 1
d["grp"] = d["dt"] - pd.to_timedelta(d["rn"], unit="D")
r = (d.groupby(["user_id", "grp"])
       .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "count"))
       .reset_index())
result = r[r["streak_days"] >= 3].drop(columns="grp").sort_values(["user_id", "streak_start"])
```
Result (actual run):
```text
 user_id streak_start streak_end  streak_days
       1   2025-01-01 2025-01-04            4
       3   2025-01-05 2025-01-07            3
       5   2024-12-30 2025-01-01            3
```
**Edge cases:** User 3 logged in twice on 7 Jan: DISTINCT prevents a false break. User 5's streak crosses a month and year boundary and still works because we subtract days, not month numbers. User 2 has two 2-day runs, so no 3-day streak. A user with two separate 3-day streaks appears on two rows; use `SELECT DISTINCT user_id` for just the list. If login_date has times, cast to a date first.
**Likely follow-ups:**
- What if you need 7 consecutive days? Change `>= 3` to `>= 7` (the same query).
- Longest streak per user? `MAX(streak_days)` over the groups, without the HAVING.
- Why not LAG? You can check 2 gaps with LAG for exactly 3 days, but the row-number trick works for any length.
**Common mistakes:** Forgetting DISTINCT, comparing day-of-month numbers (breaks at month end), and checking only `date = previous date + 1` for one step, which finds 2-day runs.

### Q10 ⭐⭐⭐ 🟡 For a view -> cart -> checkout -> payment funnel, calculate the step-to-step conversion and the drop-off percentage at each stage.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Funnel maths: step-to-step conversion versus overall conversion, and drop-off as its complement.
**Say this in the interview:** I count distinct users per step, put the steps in order, and use LAG to get the previous step's count. Step conversion is this step divided by the previous one; drop-off is 100 minus that.
**Explain simply:**
- **Step-to-step conversion** = users at this step / users at the previous step. **Drop-off %** = 100 - conversion = the share lost at this step.
- **Overall conversion** divides by the first step (view) instead. FIRST_VALUE gets that base.
- Alphabetical order of step names is wrong, so a CASE gives each step a number (`step_no`).
- Simple counts trust the data. If a user has `payment` but no `checkout` row (tracking gap, user 5 here), the order-aware version in part 2 only counts users who did every earlier step.
**Example:** Hiring: 8 applied, 5 screened, 4 interviewed, 3 joined. Interview to joined = 75%, drop-off 25%.
**Sample data:**

`funnel_events`

| user_id | step |
|---|---|
| 1 | view |
| 2 | view |
| 3 | view |
| 4 | view |
| 5 | view |
| 6 | view |
| 7 | view |
| 8 | view |
| 1 | cart |
| 2 | cart |
| 3 | cart |
| 4 | cart |
| 5 | cart |
| 1 | checkout |
| 2 | checkout |
| 3 | checkout |
| 4 | checkout |
| 1 | payment |
| 2 | payment |
| 5 | payment |
**SQL:**
```sql
-- 1) Step conversion and drop-off
WITH s AS (
    SELECT CASE step WHEN 'view' THEN 1 WHEN 'cart' THEN 2 WHEN 'checkout' THEN 3 WHEN 'payment' THEN 4 END AS step_no,
           step, COUNT(DISTINCT user_id) AS users
    FROM funnel_events
    GROUP BY step
), c AS (
    SELECT step_no, step, users,
           LAG(users) OVER (ORDER BY step_no)          AS prev_users,
           FIRST_VALUE(users) OVER (ORDER BY step_no)  AS first_users
    FROM s
)
SELECT step_no, step, users, prev_users,
       ROUND(100.0 * users / prev_users, 1)       AS step_conv_pct,
       ROUND(100.0 - 100.0 * users / prev_users, 1) AS dropoff_pct,
       ROUND(100.0 * users / first_users, 1)      AS overall_pct
FROM c
ORDER BY step_no;
```
```sql
-- 2) Order-aware (strict) funnel: only users who did every earlier step
WITH u AS (
    SELECT user_id,
           MAX(step = 'view')     AS v,
           MAX(step = 'cart')     AS c,
           MAX(step = 'checkout') AS k,
           MAX(step = 'payment')  AS p
    FROM funnel_events
    GROUP BY user_id
)
SELECT SUM(v) AS viewed, SUM(v*c) AS carted, SUM(v*c*k) AS checked_out, SUM(v*c*k*p) AS paid
FROM u;
```
**Output:**

*1) Step conversion and drop-off*

| step_no | step | users | prev_users | step_conv_pct | dropoff_pct | overall_pct |
|---|---|---|---|---|---|---|
| 1 | view | 8 | NULL | NULL | NULL | 100 |
| 2 | cart | 5 | 8 | 62.5 | 37.5 | 62.5 |
| 3 | checkout | 4 | 5 | 80 | 20 | 50 |
| 4 | payment | 3 | 4 | 75 | 25 | 37.5 |

*2) Order-aware (strict) funnel: only users who did every earlier step*

| viewed | carted | checked_out | paid |
|---|---|---|---|
| 8 | 5 | 4 | 2 |
**pandas equivalent:**
```python
# 1) Step conversion and drop-off
order = ["view", "cart", "checkout", "payment"]
g = (funnel_events.groupby("step")["user_id"].nunique().reindex(order).rename("users").reset_index())
g.insert(0, "step_no", range(1, 5))
g["prev_users"] = g["users"].shift(1)
g["step_conv_pct"] = (g["users"] / g["prev_users"] * 100).round(1)
g["dropoff_pct"] = (100 - g["users"] / g["prev_users"] * 100).round(1)
g["overall_pct"] = (g["users"] / g["users"].iloc[0] * 100).round(1)
result = g
```
Result (actual run):
```text
 step_no     step  users  prev_users  step_conv_pct  dropoff_pct  overall_pct
       1     view      8         NaN            NaN          NaN        100.0
       2     cart      5         8.0           62.5         37.5         62.5
       3 checkout      4         5.0           80.0         20.0         50.0
       4  payment      3         4.0           75.0         25.0         37.5
```
```python
# 2) Order-aware (strict) funnel: only users who did every earlier step
flags = (funnel_events.assign(v=1)
        .pivot_table(index="user_id", columns="step", values="v", aggfunc="max", fill_value=0))
strict = flags[["view", "cart", "checkout", "payment"]].cumprod(axis=1).sum()
result = pd.DataFrame({"viewed": [strict["view"]], "carted": [strict["cart"]],
                       "checked_out": [strict["checkout"]], "paid": [strict["payment"]]})
```
Result (actual run):
```text
 viewed  carted  checked_out  paid
      8       5            4     2
```
**Edge cases:** The first step has NULL previous users, so its conversion and drop-off are NULL (not 0). A step with 0 users would divide the next step by zero: use NULLIF. Plain counts show payment = 3 but the strict funnel shows only 2 paid after a recorded checkout, because user 5 skipped a logged step: investigate tracking before trusting either. `MAX(step = 'view')` uses SQLite's 0/1 booleans; in other databases use `MAX(CASE WHEN step='view' THEN 1 ELSE 0 END)`. Users who do steps in a different order or across sessions need event times too.
**Likely follow-ups:**
- Where would you intervene? At the biggest drop-off: here view to cart (37.5% lost).
- Overall vs step conversion? Overall tells the end result, step conversion tells where it leaks.
- Can conversion exceed 100%? Only if the data is inconsistent (e.g. payment without checkout); that is a data-quality flag.
**Common mistakes:** Sorting steps alphabetically, dividing by the first step when asked for step-to-step, and ignoring users who skipped a logged step.

### Q11 ⭐⭐⭐ 🟡 Build a monthly cohort retention table: rows = signup month (cohort), columns = months since signup (0, 1, 2, ...), values = number of active users.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you can compute 'months since signup', pivot it with conditional aggregation, and avoid showing 0 for months that have not happened yet.
**Say this in the interview:** For each active user I compute how many months after signup the activity happened (0 = signup month). Then I pivot with COUNT(DISTINCT CASE WHEN month_no = k ...) into columns, and show NULL for months that are beyond the data.
**Explain simply:**
- **Cohort table**: rows are signup months; columns are months since signup (M0, M1, M2 ...). The triangular shape is normal: newer cohorts have fewer observable months.
- Months since signup = difference in month numbers. SQLite converts the text pieces from `strftime` to numbers when you subtract them (`'03'-'01' = 2`).
- **Pivot with CASE**: each column counts users whose month_no equals that column. `COUNT(DISTINCT CASE WHEN ... THEN user_id END)` counts each person once.
- A cell is NULL when cohort month + k is later than the last month in the data (not yet observable); 0 would wrongly say nobody came back.
**Example:** Jan cohort of 4 users: M0 = 4, M1 = 3 (still active a month later), M2 = 2 ...
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-05 |
| 2 | 2025-01-12 |
| 3 | 2025-01-20 |
| 4 | 2025-01-28 |
| 5 | 2025-02-03 |
| 6 | 2025-02-10 |
| 7 | 2025-02-17 |
| 8 | 2025-02-24 |
| 9 | 2025-03-02 |
| 10 | 2025-03-09 |
| 11 | 2025-03-14 |
| 12 | 2025-04-03 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-06 |
| 1 | 2025-02-10 |
| 1 | 2025-03-12 |
| 2 | 2025-01-13 |
| 3 | 2025-01-21 |
| 3 | 2025-02-02 |
| 3 | 2025-02-18 |
| 3 | 2025-03-05 |
| 4 | 2025-01-28 |
| 4 | 2025-02-15 |
| 5 | 2025-02-03 |
| 5 | 2025-03-08 |
| 6 | 2025-02-14 |
| 7 | 2025-02-21 |
| 8 | 2025-02-25 |
| 8 | 2025-03-22 |
| 8 | 2025-04-10 |
| 9 | 2025-03-04 |
| 9 | 2025-04-02 |
| 10 | 2025-03-09 |
| 11 | 2025-03-15 |
| 11 | 2025-04-20 |
| 12 | 2025-04-03 |
**SQL:**
```sql
WITH c AS (
    SELECT user_id, strftime('%Y-%m-01', signup_date) AS cohort_start FROM users
), act AS (
    SELECT DISTINCT c.cohort_start, c.user_id,
           (strftime('%Y', a.activity_date) - strftime('%Y', c.cohort_start)) * 12
         + (strftime('%m', a.activity_date) - strftime('%m', c.cohort_start)) AS month_no
    FROM c JOIN activity a ON a.user_id = c.user_id
), age AS (
    SELECT cohort_start, COUNT(*) AS cohort_size,
           (SELECT (strftime('%Y', MAX(activity_date)) - strftime('%Y', cohort_start)) * 12
                 + (strftime('%m', MAX(activity_date)) - strftime('%m', cohort_start)) FROM activity) AS max_age
    FROM c GROUP BY cohort_start
)
SELECT substr(g.cohort_start, 1, 7) AS cohort_month,
       g.cohort_size,
       CASE WHEN g.max_age >= 0 THEN COUNT(DISTINCT CASE WHEN a.month_no = 0 THEN a.user_id END) END AS m0,
       CASE WHEN g.max_age >= 1 THEN COUNT(DISTINCT CASE WHEN a.month_no = 1 THEN a.user_id END) END AS m1,
       CASE WHEN g.max_age >= 2 THEN COUNT(DISTINCT CASE WHEN a.month_no = 2 THEN a.user_id END) END AS m2,
       CASE WHEN g.max_age >= 3 THEN COUNT(DISTINCT CASE WHEN a.month_no = 3 THEN a.user_id END) END AS m3
FROM age g
LEFT JOIN act a ON a.cohort_start = g.cohort_start
GROUP BY g.cohort_start, g.cohort_size, g.max_age
ORDER BY g.cohort_start;
```
**Output:**

| cohort_month | cohort_size | m0 | m1 | m2 | m3 |
|---|---|---|---|---|---|
| 2025-01 | 4 | 4 | 3 | 2 | 0 |
| 2025-02 | 4 | 4 | 2 | 1 | NULL |
| 2025-03 | 3 | 3 | 2 | NULL | NULL |
| 2025-04 | 1 | 1 | NULL | NULL | NULL |
**pandas equivalent:**
```python
u = users.assign(cohort=pd.to_datetime(users["signup_date"]).dt.to_period("M"))
a = activity.assign(am=pd.to_datetime(activity["activity_date"]).dt.to_period("M"))
m = u.merge(a, on="user_id")
m["month_no"] = (m["am"] - m["cohort"]).apply(lambda x: x.n)
m = m[["cohort", "user_id", "month_no"]].drop_duplicates()
last = a["am"].max()
rows = []
for cohort, grp in u.groupby("cohort"):
    max_age = (last - cohort).n
    row = {"cohort_month": str(cohort), "cohort_size": len(grp)}
    for k in range(4):
        n_k = m[(m["cohort"] == cohort) & (m["month_no"] == k)]["user_id"].nunique()
        row["m%d" % k] = n_k if max_age >= k else None
    rows.append(row)
result = pd.DataFrame(rows)
```
Result (actual run):
```text
cohort_month  cohort_size  m0  m1  m2  m3
     2025-01            4   4 3.0 2.0 0.0
     2025-02            4   4 2.0 1.0 NaN
     2025-03            3   3 2.0 NaN NaN
     2025-04            1   1 NaN NaN NaN
```
**Edge cases:** Cells that are not observable yet are NULL (e.g. the Feb cohort in M3 and Apr cohort in M1). Because the data ends in April, the Apr cohort shows only M0. Cohort size comes from users, so M0 equals the cohort size here only because every sample user has activity in the signup month; if signup is not counted as activity, M0 can be smaller. Add more `m4, m5 ...` columns for a longer table, or return the long form (cohort_month, month_no, users) and let the BI tool pivot it.
**Likely follow-ups:**
- How do you turn counts into percentages? Divide each column by M0 (cohort size), as in Q6.
- Why not PIVOT? SQLite, PostgreSQL and MySQL have no PIVOT keyword; conditional aggregation works everywhere (SQL Server and Oracle do have PIVOT, not run here).
- Why a cohort per signup month and not per day? Daily cohorts are too small and noisy for most businesses.
**Common mistakes:** Counting rows instead of distinct users, showing 0 instead of NULL for future months, and computing month_no with only the month number (breaks across years).

### Q12 ⭐⭐⭐ 🟡 Calculate year-over-year (YoY) growth in monthly revenue by comparing each month with the same month last year.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you match on the same month a year earlier by date, not by row position.
**Say this in the interview:** I total revenue per month, then LEFT JOIN that table to itself on 'same month minus one year'. YoY % is (this year minus last year) divided by last year. A self-join is safer than LAG(12) when months can be missing.
**Explain simply:**
- **YoY** = year-over-year: compare a month with the same month last year, which removes seasonality (festival or year-end peaks).
- A **self-join** joins a table to itself. Here `cur` is this month and `prev` is the row whose month_start equals `date(cur.month_start, '-1 year')`.
- LEFT JOIN keeps months that have no last-year match; their growth is NULL.
- NULLIF protects against a last-year value of 0.
**Example:** Revenue Jan 2024 = Rs 1,00,000, Jan 2025 = Rs 1,30,000, so YoY = +30%.
**Sample data:**

`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2024-01-10 | 60000 |
| 2 | 2024-01-22 | 40000 |
| 3 | 2024-03-05 | 120000 |
| 4 | 2024-04-15 | 90000 |
| 5 | 2025-01-09 | 70000 |
| 6 | 2025-01-27 | 60000 |
| 7 | 2025-02-12 | 110000 |
| 8 | 2025-03-18 | 150000 |
| 9 | 2025-04-20 | 99000 |
**SQL:**
```sql
WITH m AS (
    SELECT strftime('%Y-%m-01', order_date) AS month_start, SUM(amount) AS revenue
    FROM orders
    GROUP BY 1
)
SELECT strftime('%Y-%m', cur.month_start) AS month,
       cur.revenue,
       prev.revenue                       AS revenue_last_year,
       ROUND(100.0 * (cur.revenue - prev.revenue) / NULLIF(prev.revenue, 0), 1) AS yoy_pct
FROM m cur
LEFT JOIN m prev ON prev.month_start = date(cur.month_start, '-1 year')
WHERE cur.month_start >= '2025-01-01'
ORDER BY cur.month_start;
```
```sql
-- PostgreSQL (not run here): prev.month_start = cur.month_start - interval '1 year'
-- MySQL (not run here): prev.month_start = DATE_SUB(cur.month_start, INTERVAL 1 YEAR)
-- SQL Server (not run here): prev.month_start = DATEADD(year, -1, cur.month_start)
```
**Output:**

| month | revenue | revenue_last_year | yoy_pct |
|---|---|---|---|
| 2025-01 | 130000 | 100000 | 30 |
| 2025-02 | 110000 | NULL | NULL |
| 2025-03 | 150000 | 120000 | 25 |
| 2025-04 | 99000 | 90000 | 10 |
**pandas equivalent:**
```python
s = (orders.assign(month=pd.to_datetime(orders["order_date"]).dt.to_period("M"))
          .groupby("month")["amount"].sum())
cur = s[s.index >= pd.Period("2025-01")]
prev = s.reindex(cur.index - 12).values
r = pd.DataFrame({"month": cur.index.astype(str), "revenue": cur.values, "revenue_last_year": prev})
r["yoy_pct"] = ((r["revenue"] - r["revenue_last_year"]) / r["revenue_last_year"] * 100).round(1)
result = r
```
Result (actual run):
```text
  month  revenue  revenue_last_year  yoy_pct
2025-01   130000           100000.0     30.0
2025-02   110000                NaN      NaN
2025-03   150000           120000.0     25.0
2025-04    99000            90000.0     10.0
```
**Edge cases:** February 2024 has no sales, so Feb 2025 has no comparison and shows NULL (growth from nothing is undefined). **LAG(revenue, 12) trap (actual run):** with missing months it looks 12 *rows* back, not 12 *months*; on this data it returned 0 non-NULL values for the 2025 months instead of 3, so it would have printed no growth at all. LAG(revenue, 12) is only safe on a complete month list (see the spine in Q5). Compare like with like: a partial current month against a full last-year month looks like a fall.
**Likely follow-ups:**
- What about QoQ? Same idea with quarters (`'-3 months'` for month-level, or quarter labels).
- Why compare to the same month and not the previous month? To remove seasonality; MoM mixes seasonality with real growth.
- How would you show YTD? Cumulative sum within the year, compared with last year's cumulative sum.
**Common mistakes:** Using LAG(12) with gaps, comparing partial months, and dividing by the current year instead of last year.

### Q13 ⭐⭐⭐ 🔴 Calculate weekly retention by cohort using window functions: for each signup week, the percentage of users active in week 0, 1, 2, 3 ...
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you can combine a calendar grid, week arithmetic and window functions (FIRST_VALUE) for a retention table, and avoid immature weeks.
**Say this in the interview:** I assign each user to a signup week (Monday start), compute week_no = weeks between the signup week and the activity week, count distinct active users per cohort and week_no, then divide by week 0 using FIRST_VALUE over each cohort.
**Explain simply:**
- **Weekly cohort**: users who signed up in the same week. `week_no` 0 is the signup week, 1 the next week and so on.
- Week start (Monday): `date(d, 'weekday 0', '-6 days')`. week_no = days between the two week starts divided by 7.
- **Window function**: `FIRST_VALUE(active_users) OVER (PARTITION BY cohort_week ORDER BY week_no)` copies the week-0 count onto every row of that cohort, so each row can compute its own percentage with no extra join.
- A small grid (cohort x week_no from a recursive CTE) guarantees a row even when 0 users were active that week, and the filter removes weeks that have not happened yet.
**Example:** Signup week of 6 Jan has 4 users. 3 of them are active in week 1, so week-1 retention = 75%.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-06 |
| 2 | 2025-01-07 |
| 3 | 2025-01-08 |
| 4 | 2025-01-10 |
| 5 | 2025-01-13 |
| 6 | 2025-01-14 |
| 7 | 2025-01-17 |
| 8 | 2025-01-21 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-06 |
| 1 | 2025-01-14 |
| 1 | 2025-01-22 |
| 1 | 2025-01-29 |
| 2 | 2025-01-07 |
| 2 | 2025-01-15 |
| 3 | 2025-01-08 |
| 3 | 2025-01-16 |
| 3 | 2025-01-17 |
| 3 | 2025-01-23 |
| 4 | 2025-01-10 |
| 5 | 2025-01-13 |
| 5 | 2025-01-21 |
| 5 | 2025-01-28 |
| 6 | 2025-01-14 |
| 6 | 2025-01-22 |
| 7 | 2025-01-17 |
| 8 | 2025-01-21 |
| 8 | 2025-01-28 |
**SQL:**
```sql
WITH cohort AS (
    SELECT user_id, date(signup_date, 'weekday 0', '-6 days') AS cohort_week FROM users
), weeks(week_no) AS (
    SELECT 0 UNION ALL SELECT week_no + 1 FROM weeks WHERE week_no < 3
), last_wk AS (
    SELECT date(MAX(activity_date), 'weekday 0', '-6 days') AS lw FROM activity
), grid AS (
    SELECT DISTINCT c.cohort_week, w.week_no
    FROM cohort c CROSS JOIN weeks w CROSS JOIN last_wk
    WHERE date(c.cohort_week, '+' || (w.week_no * 7) || ' days') <= last_wk.lw
), active AS (
    SELECT c.cohort_week,
           CAST((julianday(a.activity_date) - julianday(c.cohort_week)) / 7 AS INTEGER) AS week_no,
           COUNT(DISTINCT c.user_id) AS active_users
    FROM cohort c
    JOIN activity a ON a.user_id = c.user_id AND a.activity_date >= c.cohort_week
    GROUP BY 1, 2
), joined AS (
    SELECT g.cohort_week, g.week_no, COALESCE(x.active_users, 0) AS active_users
    FROM grid g
    LEFT JOIN active x ON x.cohort_week = g.cohort_week AND x.week_no = g.week_no
)
SELECT cohort_week, week_no, active_users,
       FIRST_VALUE(active_users) OVER (PARTITION BY cohort_week ORDER BY week_no) AS cohort_size,
       ROUND(100.0 * active_users
             / FIRST_VALUE(active_users) OVER (PARTITION BY cohort_week ORDER BY week_no), 1) AS retention_pct
FROM joined
ORDER BY cohort_week, week_no;
```
```sql
-- PostgreSQL (not run here): DATE_TRUNC('week', signup_date)::date AS cohort_week;  week_no = (activity_week - cohort_week) / 7
-- MySQL 8+ (not run here): DATE_SUB(d, INTERVAL WEEKDAY(d) DAY)   SQL Server (not run here): DATEADD(day, 1 - DATEPART(weekday, d), d) depends on DATEFIRST
-- FIRST_VALUE works in PostgreSQL, MySQL 8+, SQL Server 2012+ (from memory).
```
**Output:**

| cohort_week | week_no | active_users | cohort_size | retention_pct |
|---|---|---|---|---|
| 2025-01-06 | 0 | 4 | 4 | 100 |
| 2025-01-06 | 1 | 3 | 4 | 75 |
| 2025-01-06 | 2 | 2 | 4 | 50 |
| 2025-01-06 | 3 | 1 | 4 | 25 |
| 2025-01-13 | 0 | 3 | 3 | 100 |
| 2025-01-13 | 1 | 2 | 3 | 66.7 |
| 2025-01-13 | 2 | 1 | 3 | 33.3 |
| 2025-01-20 | 0 | 1 | 1 | 100 |
| 2025-01-20 | 1 | 1 | 1 | 100 |
**pandas equivalent:**
```python
u = users.assign(sd=pd.to_datetime(users["signup_date"]))
u["cohort_week"] = u["sd"] - pd.to_timedelta(u["sd"].dt.weekday, unit="D")
a = activity.assign(ad=pd.to_datetime(activity["activity_date"]))
m = u.merge(a, on="user_id")
m = m[m["ad"] >= m["cohort_week"]]
m["week_no"] = (m["ad"] - m["cohort_week"]).dt.days // 7
act = m.groupby(["cohort_week", "week_no"])["user_id"].nunique()
last_wk = a["ad"].max() - pd.Timedelta(days=a["ad"].max().weekday())
rows = []
for cw in sorted(u["cohort_week"].unique()):
    for k in range(4):
        if cw + pd.Timedelta(days=7 * k) <= last_wk:
            rows.append({"cohort_week": cw, "week_no": k, "active_users": int(act.get((cw, k), 0))})
r = pd.DataFrame(rows)
r["cohort_size"] = r.groupby("cohort_week")["active_users"].transform("first")
r["retention_pct"] = (r["active_users"] / r["cohort_size"] * 100).round(1)
r["cohort_week"] = r["cohort_week"].dt.strftime("%Y-%m-%d")
result = r
```
Result (actual run):
```text
cohort_week  week_no  active_users  cohort_size  retention_pct
 2025-01-06        0             4            4          100.0
 2025-01-06        1             3            4           75.0
 2025-01-06        2             2            4           50.0
 2025-01-06        3             1            4           25.0
 2025-01-13        0             3            3          100.0
 2025-01-13        1             2            3           66.7
 2025-01-13        2             1            3           33.3
 2025-01-20        0             1            1          100.0
 2025-01-20        1             1            1          100.0
```
**Edge cases:** Data ends in the week of 27 Jan, so the 20 Jan cohort has only weeks 0 and 1 and the 13 Jan cohort weeks 0 to 2: later weeks are left out, not shown as 0%. This query assumes every user is active in their signup week (so week 0 equals the cohort size); if not, take cohort size from the users table. A user with two events in one week (user 3, week 1) counts once. Week boundaries depend on the start day: this uses Monday (ISO-style).
**Likely follow-ups:**
- How do you turn it into a wide table? Conditional aggregation as in Q11, or pivot in pandas/BI.
- Why FIRST_VALUE instead of a join? It keeps the query to one pass and shows window functions.
- Rolling vs classic retention? Classic = active exactly in week k; rolling = active in week k or later. Say which one you mean.
**Common mistakes:** Letting the latest incomplete weeks show 0%, missing zero rows because there is no grid, and using different week-start rules for signup and activity.

### Q14 ⭐⭐ 🟢 Calculate the repeat purchase rate: the percentage of customers who placed more than one order.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Two-level aggregation: orders per customer first, then a share across customers.
**Say this in the interview:** I count orders per customer in a subquery, then count how many customers have more than 1, divided by all customers. Here 2 of 6 customers repeated, so 33.3%.
**Explain simply:**
- **Repeat purchase rate** = customers with 2 or more orders / all customers who ordered, x 100.
- Step 1: `GROUP BY customer_id` with `COUNT(DISTINCT order_id)` (DISTINCT guards against duplicated order rows).
- Step 2: `SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END)` counts repeaters; `COUNT(*)` counts customers.
- Say the denominator: customers who ordered at least once, not all registered users.
**Example:** Cafeteria card swipes: 6 employees bought lunch, 2 bought more than once: 33.3% repeat.
**Sample data:**

`orders`

| order_id | customer_id |
|---|---|
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 3 |
| 6 | 3 |
| 7 | 4 |
| 8 | 5 |
| 9 | 6 |
**SQL:**
```sql
SELECT COUNT(*) AS customers,
       SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END) AS repeat_customers,
       ROUND(100.0 * SUM(CASE WHEN n > 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_rate_pct
FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS n
      FROM orders
      GROUP BY customer_id);
```
**Output:**

| customers | repeat_customers | repeat_rate_pct |
|---|---|---|
| 6 | 2 | 33.3 |
**pandas equivalent:**
```python
n = orders.groupby("customer_id")["order_id"].nunique()
result = pd.DataFrame({"customers": [len(n)], "repeat_customers": [int((n > 1).sum())],
                       "repeat_rate_pct": [round(100.0 * (n > 1).sum() / len(n), 1)]})
```
Result (actual run):
```text
 customers  repeat_customers  repeat_rate_pct
         6                 2             33.3
```
**Edge cases:** Empty orders table: COUNT(*) is 0 and the division gives NULL in SQLite (an error in some databases): add NULLIF(COUNT(*), 0). NULL customer_id rows form one group and inflate it: filter them. Cancelled or returned orders may need removing first. Time window matters: a customer who ordered once last week may still return, so compare cohorts of equal age.
**Likely follow-ups:**
- Why does the time window matter? Repeat rate rises with time since first order; compare the same age (e.g. 90 days).
- Orders per customer on average? `AVG(n)`.
- Repeat rate by month? Group the first-order month (Q7) and count second orders.
**Common mistakes:** Dividing by all users instead of buyers, counting rows instead of distinct orders, and using `>= 1`.

### Q15 ⭐⭐ 🟢 Calculate stickiness (DAU/MAU ratio) for a given month and explain what a good value means.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you know the stickiness formula and divide average daily users by monthly users, over calendar days.
**Say this in the interview:** Stickiness is average DAU divided by MAU for the same month. It says what share of monthly users show up on a typical day. I sum daily distinct users, divide by the days in the month, then divide by the month's distinct users.
**Explain simply:**
- **DAU** = distinct users per day; **MAU** = distinct users in the month (Q1).
- **Stickiness = average DAU / MAU.** 20% means a typical monthly user is active about 6 days a month (20% x 30).
- Average over *calendar days* (31 for January), so days with no activity count as 0.
- The sample is tiny on purpose (4 users, 3 days), so the value is low; real products compare against their own history.
**Example:** If 1,000 employees use the HR app in a month and on average 200 use it daily, stickiness = 20%.
**Sample data:**

`events`

| user_id | event_time |
|---|---|
| 1 | 2025-01-01 09:00:00 |
| 1 | 2025-01-01 15:00:00 |
| 1 | 2025-01-02 10:00:00 |
| 2 | 2025-01-01 11:00:00 |
| 2 | 2025-01-03 08:30:00 |
| 3 | 2025-01-02 12:00:00 |
| 4 | 2025-01-03 18:00:00 |
| 1 | 2025-02-01 09:00:00 |
**SQL:**
```sql
WITH daily AS (
    SELECT date(event_time) AS d, COUNT(DISTINCT user_id) AS dau
    FROM events
    WHERE event_time >= '2025-01-01' AND event_time < '2025-02-01'
    GROUP BY date(event_time)
), mau AS (
    SELECT COUNT(DISTINCT user_id) AS mau
    FROM events
    WHERE event_time >= '2025-01-01' AND event_time < '2025-02-01'
), cal AS (
    SELECT CAST(strftime('%d', date('2025-01-01', '+1 month', '-1 day')) AS INTEGER) AS days
)
SELECT ROUND(1.0 * (SELECT SUM(dau) FROM daily) / cal.days, 2) AS avg_dau,
       mau.mau,
       ROUND(100.0 * (SELECT SUM(dau) FROM daily) / cal.days / mau.mau, 1) AS stickiness_pct
FROM mau CROSS JOIN cal;
```
**Output:**

| avg_dau | mau | stickiness_pct |
|---|---|---|
| 0.19 | 4 | 4.8 |
**pandas equivalent:**
```python
e = events.assign(ts=pd.to_datetime(events["event_time"]))
jan = e[(e["ts"] >= "2025-01-01") & (e["ts"] < "2025-02-01")]
days = pd.Period("2025-01").days_in_month
dau_sum = jan.assign(d=jan["ts"].dt.date).groupby("d")["user_id"].nunique().sum()
mau = jan["user_id"].nunique()
result = pd.DataFrame({"avg_dau": [round(dau_sum / days, 2)], "mau": [mau],
                       "stickiness_pct": [round(100.0 * dau_sum / days / mau, 1)]})
```
Result (actual run):
```text
 avg_dau  mau  stickiness_pct
    0.19    4             4.8
```
**Edge cases:** February's event for user 1 is excluded by the date range. If a month has no events MAU is 0 and the division fails (use NULLIF). Using only days that had activity instead of all calendar days overstates stickiness. Good value: there is no universal number; as a rule of thumb (from memory, not a sourced benchmark) around 20% is often called decent for consumer apps, and higher for daily-habit tools. Compare with your own trend and similar products.
**Likely follow-ups:**
- DAU/WAU or WAU/MAU? Same idea with other windows.
- Is high always good? For a daily tool yes; for an occasional one (payslip app) low is normal.
- Why average and not a single day's DAU? A single day can be a weekend or a campaign spike.
**Common mistakes:** Using the sum of DAU instead of the average, dividing by days with data only, and mixing months between numerator and denominator.

### Q16 ⭐⭐ 🟢 Calculate the signup-to-activation conversion rate: the percentage of signed-up users who completed a first key action (e.g. first order) within 7 days.
**Asked at:** commonly asked (no company-specific report found). Generic interview-prep lists name this as a standard product-analytics pattern (aggregator pages, unverified).
**What the interviewer is checking:** Whether you define the window clearly (inclusive of day 7), join on a date range, and exclude users whose 7 days are not over.
**Say this in the interview:** I LEFT JOIN each user to their orders that fall between signup date and signup date plus 7 days, then divide distinct users with such an order by all eligible users. Users who signed up less than 7 days before the data cut-off are excluded.
**Explain simply:**
- **Activation** = the first meaningful action (here an order). **Activation rate** = activated users / signed-up users.
- The date condition goes inside the LEFT JOIN `ON`, so users with no qualifying order stay in the denominator.
- `COUNT(DISTINCT o.user_id)` counts a user once even with two orders (user 6).
- **Definition used:** order on the signup day through day 7 inclusive (`<= signup + 7 days`); say this aloud or the interviewer may mean something else.
- **Eligible users**: data is loaded through 2025-02-10 (a parameter here), so user 8 (signed up 8 Feb) has not had 7 days yet and is left out.
**Example:** New hires: 7 joined in the pilot batch, 4 completed their first training within a week: 57.1% activation.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-02 |
| 2 | 2025-01-03 |
| 3 | 2025-01-05 |
| 4 | 2025-01-06 |
| 5 | 2025-01-10 |
| 6 | 2025-01-15 |
| 7 | 2025-01-20 |
| 8 | 2025-02-08 |

`orders`

| order_id | user_id | order_date |
|---|---|---|
| 1 | 1 | 2025-01-05 |
| 2 | 2 | 2025-01-12 |
| 3 | 4 | 2025-01-06 |
| 4 | 5 | 2025-01-17 |
| 5 | 6 | 2025-01-16 |
| 6 | 6 | 2025-01-18 |
| 7 | 8 | 2025-02-09 |
**SQL:**
```sql
SELECT COUNT(DISTINCT u.user_id) AS eligible_users,
       COUNT(DISTINCT o.user_id) AS activated_users,
       ROUND(100.0 * COUNT(DISTINCT o.user_id) / COUNT(DISTINCT u.user_id), 1) AS activation_pct
FROM users u
LEFT JOIN orders o
       ON o.user_id = u.user_id
      AND o.order_date >= u.signup_date
      AND o.order_date <= date(u.signup_date, '+7 days')
WHERE u.signup_date <= date('2025-02-10', '-7 days');   -- data loaded through 2025-02-10
```
```sql
-- PostgreSQL (not run here): o.order_date <= u.signup_date + 7   (date + integer days)
-- MySQL (not run here): o.order_date <= DATE_ADD(u.signup_date, INTERVAL 7 DAY)   SQL Server (not run here): DATEADD(day, 7, u.signup_date)
```
**Output:**

| eligible_users | activated_users | activation_pct |
|---|---|---|
| 7 | 4 | 57.1 |
**pandas equivalent:**
```python
cutoff = pd.Timestamp("2025-02-10") - pd.Timedelta(days=7)
u = users.assign(sd=pd.to_datetime(users["signup_date"]))
u = u[u["sd"] <= cutoff]
o = orders.assign(od=pd.to_datetime(orders["order_date"]))
m = u.merge(o, on="user_id", how="left")
ok = m[(m["od"] >= m["sd"]) & (m["od"] <= m["sd"] + pd.Timedelta(days=7))]
act = ok["user_id"].nunique()
result = pd.DataFrame({"eligible_users": [len(u)], "activated_users": [act],
                       "activation_pct": [round(100.0 * act / len(u), 1)]})
```
Result (actual run):
```text
 eligible_users  activated_users  activation_pct
              7                4            57.1
```
**Edge cases:** User 2 ordered on day 9 (not activated); user 5 ordered exactly on day 7 (activated, because the window is inclusive); user 6's two orders count once. Orders before the signup date (data errors) are excluded by the `>=`. Users with a NULL signup_date drop out of the WHERE. If nobody is eligible the rate is NULL. Whether 'within 7 days' means 7 or 8 calendar days is a definition choice: state it.
**Likely follow-ups:**
- How would you do it by signup month? Add `strftime('%Y-%m', u.signup_date)` and GROUP BY it.
- Time to activation? Days between signup and first order (see Q18 for first-to-second).
- Why exclude recent signups? Otherwise the rate is biased downward, like the immature cohort problem in Q6.
**Common mistakes:** Putting the date filter in WHERE (turns the LEFT JOIN into an inner join and inflates the rate), counting orders instead of users, and including users whose 7 days are not over.

### Q17 ⭐⭐ 🟢 Calculate the average number of orders per active customer per month.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can count orders and distinct customers in the same GROUP BY and divide them without integer-division surprises.
**Say this in the interview:** For each month I count all orders, count distinct customers who ordered that month (the active ones), and divide. I multiply by 1.0 so the division keeps decimals.
**Explain simply:**
- **Active customer** here means a customer with at least one order in that month, so we count each customer once with `COUNT(DISTINCT customer_id)`.
- **Orders per active customer** = total orders / active customers. It tells you how often buyers who showed up that month actually buy.
- In many databases `5 / 2` gives `2` (integer division). Multiplying by `1.0` first forces a decimal answer.
- Month is cut out of the date with `strftime('%Y-%m', order_date)` in SQLite.
**Example:** January: 6 orders from 3 different customers = 2.0 orders per active customer. Think of 3 employees raising 6 leave requests in total.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | C1 | 2025-01-03 |
| 2 | C1 | 2025-01-20 |
| 3 | C2 | 2025-01-11 |
| 4 | C3 | 2025-01-25 |
| 5 | C3 | 2025-01-28 |
| 6 | C3 | 2025-01-30 |
| 7 | C1 | 2025-02-02 |
| 8 | C2 | 2025-02-14 |
| 9 | C4 | 2025-02-19 |

**SQL:**
```sql
SELECT strftime('%Y-%m', order_date)             AS month,
       COUNT(*)                                  AS orders,
       COUNT(DISTINCT customer_id)               AS active_customers,
       ROUND(1.0 * COUNT(*) / COUNT(DISTINCT customer_id), 2) AS orders_per_active_customer
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;
```

**Output:**

| month | orders | active_customers | orders_per_active_customer |
|---|---|---|---|
| 2025-01 | 6 | 3 | 2.0 |
| 2025-02 | 3 | 3 | 1.0 |

**Other dialects (not run here / from memory):** PostgreSQL `TO_CHAR(order_date,'YYYY-MM')`; MySQL `DATE_FORMAT(order_date,'%Y-%m')`; SQL Server `FORMAT(order_date,'yyyy-MM')` or `EOMONTH(order_date)`. Cast to decimal (`1.0 *` or `CAST(... AS DECIMAL)`) in all of them.

**pandas equivalent:**
```python
# orders (DataFrames with the same columns as the SQL tables)
orders["month"] = pd.to_datetime(orders["order_date"]).dt.strftime("%Y-%m")
g = orders.groupby("month").agg(orders=("order_id", "count"),
                                active_customers=("customer_id", "nunique")).reset_index()
g["orders_per_active_customer"] = (g["orders"] / g["active_customers"]).round(2)
result = g
```
Result (actual run):
```text
  month  orders  active_customers  orders_per_active_customer
2025-01       6                 3                         2.0
2025-02       3                 3                         1.0
```
**Edge cases:** A customer with 0 orders is not 'active' and never appears. Cancelled orders: filter them out first if the business says they do not count. Counting `customer_id` without DISTINCT gives plain orders and the ratio is always 1. Months with no orders produce no row at all (add a calendar if you need a 0).
**Likely follow-ups:**
- Average over all months at once? Use total orders / distinct customers over the whole period, not the average of monthly ratios, and say which you chose.
- Same metric per category? Add `category` to SELECT and GROUP BY.
**Common mistakes:** Dividing `COUNT(*)` by `COUNT(customer_id)` (both count rows, ratio 1), integer division, and forgetting DISTINCT.

### Q18 ⭐⭐ 🟡 Find the average number of days between a customer's first and second order.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can rank each customer's orders with ROW_NUMBER and then compare rank 1 with rank 2 (a self-join on the ranked rows).
**Say this in the interview:** I number each customer's orders by date, take number 1 and number 2, subtract the dates and average the result. Customers with only one order have no second order, so they are left out.
**Explain simply:**
- **ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)** numbers the orders 1, 2, 3 separately for every customer.
- Joining rank 1 to rank 2 on the same customer puts first and second order dates side by side.
- `julianday(date)` turns a date into a day count, so subtracting two of them gives the gap in days (SQLite way).
- Add `order_id` as a tie-break so two orders on the same day are numbered in a stable order.
**Example:** Priya's first order is 1 Jan and her second is 11 Jan: gap 10 days. Averaging such gaps across customers tells marketing when to send a nudge.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | C1 | 2025-01-01 |
| 2 | C1 | 2025-01-11 |
| 3 | C1 | 2025-03-01 |
| 4 | C2 | 2025-01-05 |
| 5 | C2 | 2025-01-25 |
| 6 | C3 | 2025-02-01 |
| 7 | C4 | 2025-02-10 |
| 8 | C4 | 2025-02-10 |

**SQL:**
```sql
WITH ranked AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY order_date, order_id) AS rn
  FROM orders
)
SELECT ROUND(AVG(julianday(o2.order_date) - julianday(o1.order_date)), 2) AS avg_days_first_to_second,
       COUNT(*) AS customers_with_second_order
FROM ranked o1
JOIN ranked o2 ON o2.customer_id = o1.customer_id
              AND o1.rn = 1 AND o2.rn = 2;
```

**Output:**

| avg_days_first_to_second | customers_with_second_order |
|---|---|
| 10.0 | 3 |

**Other dialects (not run here / from memory):** MySQL `DATEDIFF(o2.order_date, o1.order_date)`; SQL Server `DATEDIFF(day, o1.order_date, o2.order_date)`; PostgreSQL `o2.order_date - o1.order_date` (date minus date gives days).

**pandas equivalent:**
```python
# orders (DataFrames with the same columns as the SQL tables)
o = orders.assign(d=pd.to_datetime(orders["order_date"])).sort_values(["customer_id", "d", "order_id"])
o["rn"] = o.groupby("customer_id").cumcount() + 1
first = o[o["rn"] == 1].set_index("customer_id")["d"]
second = o[o["rn"] == 2].set_index("customer_id")["d"]
gap = (second - first.reindex(second.index)).dt.days
result = pd.DataFrame({"avg_days_first_to_second": [round(gap.mean(), 2)],
                       "customers_with_second_order": [len(gap)]})
```
Result (actual run):
```text
 avg_days_first_to_second  customers_with_second_order
                     10.0                            3
```
**Edge cases:** C3 has one order, so is excluded (an inner join drops them; say so, and report how many customers that is). C4 placed two orders the same day: gap 0 pulls the average down; decide whether same-day orders count as one. If a customer's second order never happens, the average is only about repeat buyers.
**Likely follow-ups:**
- Median instead of average? Averages are pulled by a few very long gaps; compute the median with a window trick (see Q36).
- Gap between every consecutive pair? Use `LAG(order_date)` instead of ranks.
**Common mistakes:** Averaging all gaps instead of just first-to-second, forgetting a tie-break, and using `DATEDIFF` in SQLite (it does not exist).

### Q19 ⭐⭐ 🟡 Calculate the monthly churn rate: customers active last month who were not active this month, as a percentage of last month's active customers.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can compare two months' customer sets (an anti-join) and divide by last month's base, not this month's.
**Say this in the interview:** I list distinct customers per month, then for every customer active in month M I check if they are missing in month M+1. Churned divided by last month's active customers is the churn rate.
**Explain simply:**
- **Churn** = customers you had last month who did not come back this month.
- The denominator is **last month's active customers**, not this month's. Otherwise new customers distort the rate.
- A **LEFT JOIN ... IS NULL** (anti-join) finds the customers with no match in the next month.
- We stop at the last month that has data: otherwise the final 'next month' looks like 100% churn only because it has not happened yet.
**Example:** January had 3 active customers (C1, C2, C3). In February only C1 and C2 ordered again, so C3 churned: 1 / 3 = 33.33% churn for February.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | C1 | 2025-01-05 |
| 2 | C2 | 2025-01-09 |
| 3 | C3 | 2025-01-20 |
| 4 | C1 | 2025-02-03 |
| 5 | C2 | 2025-02-18 |
| 6 | C1 | 2025-03-07 |
| 7 | C4 | 2025-03-10 |
| 8 | C4 | 2025-04-01 |
| 9 | C5 | 2025-04-02 |
| 10 | C5 | 2025-04-20 |

**SQL:**
```sql
WITH cm AS (
  SELECT DISTINCT customer_id, strftime('%Y-%m', order_date) AS month FROM orders
),
last_m AS (SELECT MAX(month) AS mx FROM cm)
SELECT strftime('%Y-%m', p.month || '-01', '+1 month')   AS month,
       COUNT(*)                                          AS active_prev_month,
       SUM(CASE WHEN c.customer_id IS NULL THEN 1 ELSE 0 END) AS churned,
       ROUND(100.0 * SUM(CASE WHEN c.customer_id IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_pct
FROM cm p
LEFT JOIN cm c ON c.customer_id = p.customer_id
              AND c.month = strftime('%Y-%m', p.month || '-01', '+1 month')
WHERE strftime('%Y-%m', p.month || '-01', '+1 month') <= (SELECT mx FROM last_m)
GROUP BY 1
ORDER BY 1;
```

**Output:**

| month | active_prev_month | churned | churn_pct |
|---|---|---|---|
| 2025-02 | 3 | 1 | 33.33 |
| 2025-03 | 2 | 1 | 50.0 |
| 2025-04 | 2 | 1 | 50.0 |

**Other dialects (not run here / from memory):** PostgreSQL `DATE_TRUNC('month', d) + INTERVAL '1 month'`; MySQL `DATE_ADD(..., INTERVAL 1 MONTH)`; SQL Server `DATEADD(month, 1, ...)`. `NOT EXISTS` is an equivalent alternative to the LEFT JOIN.

**pandas equivalent:**
```python
# orders (DataFrames with the same columns as the SQL tables)
o = orders.assign(m=pd.to_datetime(orders["order_date"]).dt.to_period("M"))
cm = o[["customer_id", "m"]].drop_duplicates()
rows = []
for m in sorted(cm["m"].unique())[:-1]:
    prev = set(cm[cm["m"] == m]["customer_id"])
    cur = set(cm[cm["m"] == m + 1]["customer_id"])
    churned = len(prev - cur)
    rows.append([str(m + 1), len(prev), churned, round(100 * churned / len(prev), 2)])
result = pd.DataFrame(rows, columns=["month", "active_prev_month", "churned", "churn_pct"])
```
Result (actual run):
```text
  month  active_prev_month  churned  churn_pct
2025-02                  3        1      33.33
2025-03                  2        1      50.00
2025-04                  2        1      50.00
```
**Edge cases:** Reactivated customers (away a month, back later) count as churned in the gap month: that is a definition choice, say it. A month with zero data in the middle would divide by nothing; use a calendar and NULLIF. 'Active' might need a minimum spend: filter before `cm`.
**Likely follow-ups:**
- Retention rate? It is 100 minus churn for the same base.
- Churn by plan or city? Add that column to both CTE and GROUP BY.
**Common mistakes:** Dividing by this month's actives, counting new customers as churn, and treating the not-yet-finished last month as 100% churn.

### Q20 ⭐⭐ 🟡 Find users who were active in the past but have had no activity in the last 30 days (inactive/at-risk users) relative to a reference date.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can pick users by their LAST activity date (MAX + HAVING) against an explicit reference date rather than today's date.
**Say this in the interview:** I group events by user, take each user's latest activity date, and keep those whose latest date is more than 30 days before the reference date. Using a reference date makes the result repeatable.
**Explain simply:**
- **At-risk / inactive user**: someone who used to be active but has not done anything recently.
- `MAX(event_date)` per user gives the last activity; `HAVING` filters after grouping.
- Rule used here: the 30 days up to and including the reference date are the 'recent window'. Last activity on or before ref minus 30 days means inactive. State it, because '30 days' can be read two ways.
- A **reference date** (not `CURRENT_DATE`) lets you re-run last month's report and get the same answer.
**Example:** Reference date 30 June. Meena last logged in 20 April, which is 71 days ago: at risk. Arun logged in 25 June: fine.
**Sample data:**

`events`

| user_id | event_date |
|---|---|
| 1 | 2025-04-20 |
| 1 | 2025-03-01 |
| 2 | 2025-06-25 |
| 2 | 2025-06-01 |
| 3 | 2025-05-31 |
| 3 | 2025-02-10 |
| 4 | 2025-06-01 |
| 5 | 2025-01-15 |

**SQL:**
```sql
WITH params AS (SELECT '2025-06-30' AS ref_date)
SELECT e.user_id,
       MAX(e.event_date) AS last_active,
       CAST(julianday(p.ref_date) - julianday(MAX(e.event_date)) AS INTEGER) AS days_inactive
FROM events e CROSS JOIN params p
GROUP BY e.user_id, p.ref_date
HAVING MAX(e.event_date) <= date(p.ref_date, '-30 days')
ORDER BY days_inactive DESC;
```

**Output:**

| user_id | last_active | days_inactive |
|---|---|---|
| 5 | 2025-01-15 | 166 |
| 1 | 2025-04-20 | 71 |
| 3 | 2025-05-31 | 30 |

**Other dialects (not run here / from memory):** PostgreSQL `DATE '2025-06-30' - 30`; MySQL `DATE_SUB('2025-06-30', INTERVAL 30 DAY)`; SQL Server `DATEADD(day, -30, '2025-06-30')`.

**pandas equivalent:**
```python
# events (DataFrames with the same columns as the SQL tables)
ref = pd.Timestamp("2025-06-30")
last = (events.assign(d=pd.to_datetime(events["event_date"]))
              .groupby("user_id")["d"].max().reset_index())
last["days_inactive"] = (ref - last["d"]).dt.days
r = last[last["d"] <= ref - pd.Timedelta(days=30)].copy()
r["last_active"] = r["d"].dt.strftime("%Y-%m-%d")
result = (r[["user_id", "last_active", "days_inactive"]]
          .sort_values("days_inactive", ascending=False).reset_index(drop=True))
```
Result (actual run):
```text
 user_id last_active  days_inactive
       5  2025-01-15            166
       1  2025-04-20             71
       3  2025-05-31             30
```
**Edge cases:** User 3 last acted exactly 30 days before the reference date, so is flagged (the `<=` boundary); user 4 acted 29 days before and is not. Users with no events at all are invisible here: LEFT JOIN from the users table and test `MAX(...) IS NULL` to catch them. Future-dated events (after the reference) must be excluded or the maths goes negative.
**Likely follow-ups:**
- Make it a segment? Use `CASE WHEN days_inactive <= 30 THEN 'active' WHEN <= 90 THEN 'at risk' ELSE 'lost' END`.
- Why not `WHERE event_date < ...`? That filters rows, so a user with one old and one recent event would still show; you need the per-user MAX.
**Common mistakes:** Filtering with WHERE instead of HAVING on the max date, using today's date so the answer changes daily, and an off-by-one at the 30-day boundary.

### Q21 ⭐⭐ 🟡 Find reactivated (resurrected) users: customers who were inactive for 60+ days and then came back.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can use LAG to find the gap between a user's consecutive active dates and flag big gaps.
**Say this in the interview:** I take each user's distinct active dates, use LAG to fetch the previous active date, and keep rows where the gap is 60 days or more. That row's date is the day they came back.
**Explain simply:**
- **Reactivated (resurrected) user**: someone silent for a long stretch who then did something again.
- **LAG(date)** looks one row back inside the same user, ordered by date.
- Rule used: a gap of **60 days or more** between two consecutive active dates counts. A user's first ever activity has no previous row (NULL), so it is not a comeback.
- Distinct dates first, so several events on one day do not create 0-day gaps.
**Example:** User 1 was active on 20 January and then not until 20 April: 90 days away, so she is reactivated on 20 April.
**Sample data:**

`events`

| user_id | event_date |
|---|---|
| 1 | 2025-01-05 |
| 1 | 2025-01-20 |
| 1 | 2025-04-20 |
| 2 | 2025-01-10 |
| 2 | 2025-03-01 |
| 2 | 2025-03-02 |
| 3 | 2025-02-01 |
| 3 | 2025-02-01 |

**SQL:**
```sql
WITH d AS (SELECT DISTINCT user_id, event_date FROM events),
g AS (
  SELECT user_id, event_date,
         LAG(event_date) OVER (PARTITION BY user_id ORDER BY event_date) AS prev_date
  FROM d
)
SELECT user_id,
       prev_date AS last_active_before,
       event_date AS returned_on,
       CAST(julianday(event_date) - julianday(prev_date) AS INTEGER) AS days_away
FROM g
WHERE prev_date IS NOT NULL
  AND julianday(event_date) - julianday(prev_date) >= 60
ORDER BY user_id, returned_on;
```

**Output:**

| user_id | last_active_before | returned_on | days_away |
|---|---|---|---|
| 1 | 2025-01-20 | 2025-04-20 | 90 |

**Other dialects (not run here / from memory):** replace the `julianday` subtraction with `DATEDIFF(day, prev_date, event_date)` (SQL Server), `DATEDIFF(event_date, prev_date)` (MySQL) or `event_date - prev_date` (PostgreSQL).

**pandas equivalent:**
```python
# events (DataFrames with the same columns as the SQL tables)
d = events.drop_duplicates().assign(dt=lambda x: pd.to_datetime(x["event_date"]))
d = d.sort_values(["user_id", "dt"])
d["prev"] = d.groupby("user_id")["dt"].shift()
d["days_away"] = (d["dt"] - d["prev"]).dt.days
r = d[d["days_away"] >= 60]
result = pd.DataFrame({"user_id": r["user_id"],
                       "last_active_before": r["prev"].dt.strftime("%Y-%m-%d"),
                       "returned_on": r["dt"].dt.strftime("%Y-%m-%d"),
                       "days_away": r["days_away"].astype(int)}).reset_index(drop=True)
```
Result (actual run):
```text
 user_id last_active_before returned_on  days_away
       1         2025-01-20  2025-04-20         90
```
**Edge cases:** User 2 was away 50 days (10 Jan to 1 Mar): below 60, so not reactivated. User 3 has duplicate events on one day, handled by DISTINCT. A user never seen before is 'new', not reactivated. A user can be reactivated several times: one row per comeback. A user who left and never returned does not appear (that is churn).
**Likely follow-ups:**
- Only count a comeback if they were active before the gap? That is already implied by a previous row existing.
- Different threshold? Change 60 to a parameter.
**Common mistakes:** Forgetting DISTINCT dates, counting the first activity as a comeback, and using `>` when the definition says '60 or more'.

### Q22 ⭐⭐ 🟡 Calculate rolling 7-day active users for every date (a user is counted once in the window).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know a rolling distinct count cannot be done with a simple window SUM and needs a date-range join.
**Say this in the interview:** I build a calendar of dates, then for each date I count distinct users with activity in the 7 days ending that date. A user active on three of those days is still counted once.
**Explain simply:**
- **Rolling 7-day active users**: for date D, how many different users did something between D minus 6 and D (7 days including D).
- A window function like `COUNT(DISTINCT ...) OVER (...)` is not allowed in most databases, so we join the calendar to the events with a date range instead.
- A **recursive CTE** makes the calendar in SQLite (PostgreSQL has `generate_series`; not run here).
- Using a calendar means days with no events still get a row.
**Example:** On 8 Jan the window is 2 to 8 Jan. User 1 appears on 3 Jan and 8 Jan but is counted once, so users 1, 2 and 3 give 3.
**Sample data:**

`events`

| user_id | event_date |
|---|---|
| 1 | 2025-01-01 |
| 2 | 2025-01-01 |
| 1 | 2025-01-03 |
| 3 | 2025-01-05 |
| 2 | 2025-01-08 |
| 1 | 2025-01-08 |
| 4 | 2025-01-10 |
| 3 | 2025-01-10 |

**SQL:**
```sql
WITH RECURSIVE cal(d) AS (
  SELECT MIN(event_date) FROM events
  UNION ALL
  SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(event_date) FROM events)
)
SELECT cal.d AS date,
       COUNT(DISTINCT e.user_id) AS rolling_7d_active_users
FROM cal
LEFT JOIN events e
  ON e.event_date BETWEEN date(cal.d, '-6 days') AND cal.d
GROUP BY cal.d
ORDER BY cal.d;
```

**Output:**

| date | rolling_7d_active_users |
|---|---|
| 2025-01-01 | 2 |
| 2025-01-02 | 2 |
| 2025-01-03 | 2 |
| 2025-01-04 | 2 |
| 2025-01-05 | 3 |
| 2025-01-06 | 3 |
| 2025-01-07 | 3 |
| 2025-01-08 | 3 |
| 2025-01-09 | 3 |
| 2025-01-10 | 4 |

**Other dialects (not run here / from memory):** PostgreSQL calendar `generate_series(start, end, interval '1 day')`; MySQL 8 and SQL Server support the same recursive CTE idea (SQL Server omits the word `RECURSIVE`); date minus 6 is `d - 6` (PostgreSQL), `DATE_SUB(d, INTERVAL 6 DAY)` (MySQL), `DATEADD(day,-6,d)` (SQL Server).

**pandas equivalent:**
```python
# events (DataFrames with the same columns as the SQL tables)
e = events.assign(d=pd.to_datetime(events["event_date"]))
cal = pd.date_range(e["d"].min(), e["d"].max(), freq="D")
rows = []
for day in cal:
    w = e[(e["d"] >= day - pd.Timedelta(days=6)) & (e["d"] <= day)]
    rows.append([day.strftime("%Y-%m-%d"), w["user_id"].nunique()])
result = pd.DataFrame(rows, columns=["date", "rolling_7d_active_users"])
```
Result (actual run):
```text
      date  rolling_7d_active_users
2025-01-01                        2
2025-01-02                        2
2025-01-03                        2
2025-01-04                        2
2025-01-05                        3
2025-01-06                        3
2025-01-07                        3
2025-01-08                        3
2025-01-09                        3
2025-01-10                        4
```
**Edge cases:** Early dates have fewer than 7 days of history: the count is simply smaller, not wrong (note it on dashboards). The `BETWEEN` includes both ends, which is why it is -6 not -7. LEFT JOIN keeps quiet days (count 0). Timestamps instead of dates: cut to the date first.
**Likely follow-ups:**
- Why not COUNT(DISTINCT) OVER? Most engines reject DISTINCT inside window functions.
- Rolling 30-day (MAU style)? Change `-6 days` to `-29 days`.
**Common mistakes:** Summing daily active users over 7 days (double counts people), off-by-one window length, and no calendar so quiet days vanish.

### Q23 ⭐⭐ 🟡 Find the product categories with the highest MoM revenue growth last month, ignoring tiny-base categories.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you compute growth per group, add a minimum-base filter, and can explain why tiny bases give silly percentages.
**Say this in the interview:** I total revenue per category per month, join each category's last month to the month before, compute growth percent, and only keep categories whose previous-month revenue is above a minimum base. Then I sort by growth.
**Explain simply:**
- **MoM growth %** = (this month - last month) / last month x 100.
- **Tiny base problem**: a category that went from Rs 500 to Rs 5,000 shows +900%, which is noise, not a trend. A minimum previous-month revenue (here Rs 10,000, a business choice) removes it.
- Join on the actual previous month (not just 'the row above') so a missing month cannot be mistaken for the previous one.
- 'Last month' is a parameter here (2025-06) so the report is repeatable.
**Example:** Fashion: Rs 20,000 in May and Rs 30,000 in June = +50%. Toys: Rs 500 to Rs 5,000 = +900% but ignored because May was below Rs 10,000.
**Sample data:**

`sales`

| category | sale_date | amount |
|---|---|---|
| Electronics | 2025-05-15 | 50000 |
| Electronics | 2025-06-12 | 60000 |
| Fashion | 2025-05-10 | 20000 |
| Fashion | 2025-06-18 | 30000 |
| Grocery | 2025-05-05 | 40000 |
| Grocery | 2025-06-07 | 42000 |
| Toys | 2025-05-21 | 500 |
| Toys | 2025-06-22 | 5000 |
| Books | 2025-05-02 | 12000 |
| Books | 2025-06-30 | 15000 |

**SQL:**
```sql
WITH m AS (
  SELECT category, strftime('%Y-%m', sale_date) AS month, SUM(amount) AS revenue
  FROM sales GROUP BY category, strftime('%Y-%m', sale_date)
)
SELECT cur.category,
       prv.revenue AS prev_revenue,
       cur.revenue AS revenue,
       ROUND(100.0 * (cur.revenue - prv.revenue) / prv.revenue, 2) AS mom_growth_pct
FROM m cur
JOIN m prv ON prv.category = cur.category
          AND prv.month = strftime('%Y-%m', cur.month || '-01', '-1 month')
WHERE cur.month = '2025-06'
  AND prv.revenue >= 10000          -- minimum base
ORDER BY mom_growth_pct DESC;
```

**Output:**

| category | prev_revenue | revenue | mom_growth_pct |
|---|---|---|---|
| Fashion | 20000 | 30000 | 50.0 |
| Books | 12000 | 15000 | 25.0 |
| Electronics | 50000 | 60000 | 20.0 |
| Grocery | 40000 | 42000 | 5.0 |

**pandas equivalent:**
```python
# sales (DataFrames with the same columns as the SQL tables)
s = sales.assign(month=pd.to_datetime(sales["sale_date"]).dt.to_period("M"))
m = s.groupby(["category", "month"], as_index=False)["amount"].sum()
cur = m[m["month"] == pd.Period("2025-06")]
prv = m[m["month"] == pd.Period("2025-05")]
j = cur.merge(prv, on="category", suffixes=("", "_prev"))
j = j[j["amount_prev"] >= 10000].copy()
j["mom_growth_pct"] = (100 * (j["amount"] - j["amount_prev"]) / j["amount_prev"]).round(2)
result = (j.rename(columns={"amount": "revenue", "amount_prev": "prev_revenue"})
           [["category", "prev_revenue", "revenue", "mom_growth_pct"]]
           .sort_values("mom_growth_pct", ascending=False).reset_index(drop=True))
```
Result (actual run):
```text
   category  prev_revenue  revenue  mom_growth_pct
    Fashion         20000    30000            50.0
      Books         12000    15000            25.0
Electronics         50000    60000            20.0
    Grocery         40000    42000             5.0
```
**Edge cases:** A brand-new category (no previous month) has nothing to divide by and is dropped by the inner join; list it separately as 'new'. Ties in growth: add a second sort key. Previous revenue of 0 is blocked by the minimum base filter (no divide by zero). Pick the threshold with the business, and show it in the report.
**Likely follow-ups:**
- Absolute growth instead of percent? Sort by `cur.revenue - prv.revenue`: big categories then win; showing both is best.
- Top 3 only? Add `LIMIT 3` (SQLite/MySQL/PostgreSQL), `TOP 3` (SQL Server, not run here).
**Common mistakes:** Ranking by percent with no base filter, using LAG over rows when a month is missing, and dividing by the current month instead of the previous one.

### Q24 ⭐⭐ 🟡 Calculate quarter-over-quarter (QoQ) revenue growth, including fiscal quarters (April-March) for Indian companies.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can derive quarter and fiscal quarter labels from a date and then compare each quarter with the one before using LAG.
**Say this in the interview:** I map each order to a quarter, sum revenue per quarter and use LAG to fetch the previous quarter. For the Indian fiscal year I shift the date forward by nine months, so April becomes January, and reuse the same quarter logic.
**Explain simply:**
- **QoQ growth %** = (this quarter - previous quarter) / previous quarter x 100.
- **Fiscal year (India, April to March)**: FY 2025-26 runs 1 Apr 2025 to 31 Mar 2026. Q1 = Apr-Jun, Q2 = Jul-Sep, Q3 = Oct-Dec, Q4 = Jan-Mar.
- Trick: moving a date 9 months ahead turns April into January, so the calendar quarter and year of the shifted date are the fiscal quarter and fiscal-year-end. `'start of month'` first avoids month-end overflow.
- **LAG** reads the previous row's value; the first quarter has none (NULL). Sort by a numeric key, not the text label.
**Example:** FY25-26 Q1 (Apr-Jun 2025) revenue is 210 against FY24-25 Q4 (Jan-Mar 2025) revenue of 215, so QoQ is -2.33%.
**Sample data:**

`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2024-05-10 | 100 |
| 2 | 2024-08-20 | 120 |
| 3 | 2024-11-15 | 150 |
| 4 | 2025-01-20 | 90 |
| 5 | 2025-02-12 | 70 |
| 6 | 2025-03-25 | 55 |
| 7 | 2025-05-18 | 210 |
| 8 | 2025-08-22 | 230 |
| 9 | 2025-11-14 | 260 |
| 10 | 2026-02-09 | 300 |

**SQL:**
```sql
WITH q AS (
  SELECT CAST(strftime('%Y', date(order_date,'start of month','+9 months')) AS INTEGER) AS fy_end,
         (CAST(strftime('%m', date(order_date,'start of month','+9 months')) AS INTEGER) - 1) / 3 + 1 AS fq,
         SUM(amount) AS revenue
  FROM orders
  GROUP BY 1, 2
)
SELECT 'FY' || substr(fy_end - 1, 3, 2) || '-' || substr(fy_end, 3, 2) || ' Q' || fq AS fiscal_quarter,
       revenue,
       LAG(revenue) OVER (ORDER BY fy_end, fq) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY fy_end, fq))
             / LAG(revenue) OVER (ORDER BY fy_end, fq), 2) AS qoq_growth_pct
FROM q
ORDER BY fy_end, fq;
```

**Output:**

| fiscal_quarter | revenue | prev_revenue | qoq_growth_pct |
|---|---|---|---|
| FY24-25 Q1 | 100 | NULL | NULL |
| FY24-25 Q2 | 120 | 100.0 | 20.0 |
| FY24-25 Q3 | 150 | 120.0 | 25.0 |
| FY24-25 Q4 | 215 | 150.0 | 43.33 |
| FY25-26 Q1 | 210 | 215.0 | -2.33 |
| FY25-26 Q2 | 230 | 210.0 | 9.52 |
| FY25-26 Q3 | 260 | 230.0 | 13.04 |
| FY25-26 Q4 | 300 | 260.0 | 15.38 |

**Same logic for calendar quarters (Jan-Mar = Q1), real output:**
```sql
WITH q AS (
  SELECT CAST(strftime('%Y', order_date) AS INTEGER) AS yr,
         (CAST(strftime('%m', order_date) AS INTEGER) - 1) / 3 + 1 AS cq,
         SUM(amount) AS revenue
  FROM orders GROUP BY 1, 2
)
SELECT yr || '-Q' || cq AS calendar_quarter, revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY yr, cq))
             / LAG(revenue) OVER (ORDER BY yr, cq), 2) AS qoq_growth_pct
FROM q ORDER BY yr, cq;
```

| calendar_quarter | revenue | qoq_growth_pct |
|---|---|---|
| 2024-Q2 | 100 | NULL |
| 2024-Q3 | 120 | 20.0 |
| 2024-Q4 | 150 | 25.0 |
| 2025-Q1 | 215 | 43.33 |
| 2025-Q2 | 210 | -2.33 |
| 2025-Q3 | 230 | 9.52 |
| 2025-Q4 | 260 | 13.04 |
| 2026-Q1 | 300 | 15.38 |

**Other dialects (not run here / from memory):** calendar quarter is `EXTRACT(QUARTER FROM d)` (PostgreSQL), `QUARTER(d)` (MySQL), `DATEPART(quarter, d)` (SQL Server). The 9-month shift works the same way: `d + INTERVAL '9 months'` (PostgreSQL), `DATE_ADD(d, INTERVAL 9 MONTH)` (MySQL), `DATEADD(month, 9, d)` (SQL Server).

**pandas equivalent:**
```python
# orders (DataFrames with the same columns as the SQL tables)
o = orders.assign(d=pd.to_datetime(orders["order_date"]))
shifted = o["d"].dt.to_period("M").dt.to_timestamp() + pd.DateOffset(months=9)
o["fy_end"] = shifted.dt.year
o["fq"] = (shifted.dt.month - 1) // 3 + 1
q = o.groupby(["fy_end", "fq"], as_index=False)["amount"].sum().sort_values(["fy_end", "fq"])
q["fiscal_quarter"] = ("FY" + (q["fy_end"] - 1).astype(str).str[2:] + "-" +
                       q["fy_end"].astype(str).str[2:] + " Q" + q["fq"].astype(str))
q["prev_revenue"] = q["amount"].shift()
q["qoq_growth_pct"] = (100 * (q["amount"] - q["prev_revenue"]) / q["prev_revenue"]).round(2)
result = q.rename(columns={"amount": "revenue"})[["fiscal_quarter", "revenue", "prev_revenue", "qoq_growth_pct"]].reset_index(drop=True)
```
Result (actual run):
```text
fiscal_quarter  revenue  prev_revenue  qoq_growth_pct
    FY24-25 Q1      100           NaN             NaN
    FY24-25 Q2      120         100.0           20.00
    FY24-25 Q3      150         120.0           25.00
    FY24-25 Q4      215         150.0           43.33
    FY25-26 Q1      210         215.0           -2.33
    FY25-26 Q2      230         210.0            9.52
    FY25-26 Q3      260         230.0           13.04
    FY25-26 Q4      300         260.0           15.38
```
**Edge cases:** A quarter with no orders is missing, so LAG would compare with an older quarter: build a quarter calendar if gaps are possible. The first quarter has NULL growth. A partly finished current quarter looks like a drop: exclude it or label it. Previous revenue of 0 needs `NULLIF`. Some companies use other fiscal years: the shift value changes (e.g. 6 months for a July start).
**Likely follow-ups:**
- Year-over-year per quarter? Use `LAG(revenue, 4)` when no quarter is missing.
- Why not the label for sorting? Text like 'FY25-26 Q1' sorts correctly here, but a numeric key is safer.
**Common mistakes:** Using calendar quarters for an April-March company, sorting quarters by text across years, and comparing against a missing quarter.

### Q25 ⭐⭐ 🟡 Compare funnel conversion across segments (device, city or acquisition channel) in one query and identify the weakest segment.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can compute a whole funnel for each segment in one pass using conditional aggregation, and judge the weakest segment sensibly.
**Say this in the interview:** I group by device and use COUNT(DISTINCT CASE WHEN step = ... THEN user_id END) to count users at each step in one query, then divide step by step. The segment with the lowest view-to-purchase rate is the weakest, if it has enough users to trust.
**Explain simply:**
- **Funnel**: view -> cart -> purchase. Each step counts users who got that far.
- **Conditional aggregation** puts a CASE inside the COUNT so one GROUP BY gives every step as its own column.
- Divide by `NULLIF(x, 0)` so an empty step gives NULL, not an error.
- Small segments swing wildly (1 user = 33%). Always show the user count next to the rate.
**Example:** Web: 3 viewers and 0 buyers = 0% overall. Android: 3 viewers and 1 buyer = 33.33%. iOS: 2 viewers and 2 buyers = 100%, on very few users.
**Sample data:**

`funnel_events`

| user_id | device | step |
|---|---|---|
| 1 | android | view |
| 1 | android | cart |
| 1 | android | purchase |
| 2 | android | view |
| 2 | android | cart |
| 3 | android | view |
| 4 | ios | view |
| 4 | ios | cart |
| 4 | ios | purchase |
| 5 | ios | view |
| 5 | ios | cart |
| 5 | ios | purchase |
| 6 | web | view |
| 7 | web | view |
| 8 | web | view |
| 8 | web | cart |

**SQL:**
```sql
SELECT device,
       COUNT(DISTINCT CASE WHEN step = 'view'     THEN user_id END) AS viewers,
       COUNT(DISTINCT CASE WHEN step = 'cart'     THEN user_id END) AS carts,
       COUNT(DISTINCT CASE WHEN step = 'purchase' THEN user_id END) AS buyers,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN step = 'cart' THEN user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN step = 'view' THEN user_id END), 0), 2) AS view_to_cart_pct,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN step = 'purchase' THEN user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN step = 'cart' THEN user_id END), 0), 2) AS cart_to_purchase_pct,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN step = 'purchase' THEN user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN step = 'view' THEN user_id END), 0), 2) AS overall_pct
FROM funnel_events
GROUP BY device
ORDER BY overall_pct ASC;
```

**Output:**

| device | viewers | carts | buyers | view_to_cart_pct | cart_to_purchase_pct | overall_pct |
|---|---|---|---|---|---|---|
| web | 3 | 1 | 0 | 33.33 | 0.0 | 0.0 |
| android | 3 | 2 | 1 | 66.67 | 50.0 | 33.33 |
| ios | 2 | 2 | 2 | 100.0 | 100.0 | 100.0 |

**pandas equivalent:**
```python
# funnel_events (DataFrames with the same columns as the SQL tables)
g = funnel_events.groupby("device")
steps = pd.DataFrame({s: g.apply(lambda x, s=s: x.loc[x["step"] == s, "user_id"].nunique())
                      for s in ["view", "cart", "purchase"]}).reset_index()
steps.columns = ["device", "viewers", "carts", "buyers"]
steps["view_to_cart_pct"] = (100 * steps["carts"] / steps["viewers"]).round(2)
steps["cart_to_purchase_pct"] = (100 * steps["buyers"] / steps["carts"]).round(2)
steps["overall_pct"] = (100 * steps["buyers"] / steps["viewers"]).round(2)
result = steps.sort_values("overall_pct").reset_index(drop=True)
```
Result (actual run):
```text
 device  viewers  carts  buyers  view_to_cart_pct  cart_to_purchase_pct  overall_pct
    web        3      1       0             33.33                   0.0         0.00
android        3      2       1             66.67                  50.0        33.33
    ios        2      2       2            100.00                 100.0       100.00
```
**Edge cases:** A segment with zero carts gives NULL for cart-to-purchase (NULLIF). One user on two devices counts in both segments: decide attribution. The weakest segment by overall rate is web, but the biggest leak for android is cart to purchase, so say both. If the data contains users who skip steps (purchase without a view row), counts per step will not nest.
**Likely follow-ups:**
- Is the weakest segment significant? With 3 to 8 users, no: you would check sample size or a significance test first.
- Several segment columns? Add them to GROUP BY, or use `GROUP BY ROLLUP` where supported (not run here).
**Common mistakes:** Running one query per device, forgetting DISTINCT, dividing by total events instead of distinct users, and crowning a tiny segment as the weakest.

### Q26 ⭐⭐ 🟡 Calculate sessions per user and average session duration from a sessions table (session_id, user_id, start_time, end_time).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can compute durations from two timestamps, handle unfinished sessions (NULL end) and group per user.
**Say this in the interview:** Duration is end minus start, converted to minutes. I group by user, count sessions and average the durations. AVG ignores NULL, so open sessions without an end time do not distort it.
**Explain simply:**
- A **session** is one visit: it has a start and an end time.
- In SQLite `strftime('%s', t)` turns a timestamp into seconds, so (end - start) / 60.0 is minutes.
- `COUNT(*)` counts all sessions; `COUNT(end_time)` counts only finished ones. `AVG` ignores NULL automatically.
- An overall average of all sessions is not the same as the average of per-user averages. Say which you report.
**Example:** Asha had 3 sessions of 10, 20 and 30 minutes: 3 sessions, average 20 minutes.
**Sample data:**

`sessions`

| session_id | user_id | start_time | end_time |
|---|---|---|---|
| 1 | U1 | 2025-03-01 09:00:00 | 2025-03-01 09:10:00 |
| 2 | U1 | 2025-03-02 10:00:00 | 2025-03-02 10:20:00 |
| 3 | U1 | 2025-03-03 08:00:00 | 2025-03-03 08:30:00 |
| 4 | U2 | 2025-03-01 12:00:00 | 2025-03-01 12:05:00 |
| 5 | U2 | 2025-03-04 18:00:00 | NULL |
| 6 | U3 | 2025-03-02 07:30:00 | 2025-03-02 08:30:00 |

**SQL:**
```sql
SELECT user_id,
       COUNT(*) AS sessions,
       COUNT(end_time) AS finished_sessions,
       ROUND(AVG((strftime('%s', end_time) - strftime('%s', start_time)) / 60.0), 2) AS avg_minutes
FROM sessions
GROUP BY user_id
ORDER BY user_id;
```

**Output:**

| user_id | sessions | finished_sessions | avg_minutes |
|---|---|---|---|
| U1 | 3 | 3 | 20.0 |
| U2 | 2 | 1 | 5.0 |
| U3 | 1 | 1 | 60.0 |

**Overall figures across all sessions, real output:**
```sql
SELECT COUNT(*) AS sessions,
       COUNT(DISTINCT user_id) AS users,
       ROUND(1.0 * COUNT(*) / COUNT(DISTINCT user_id), 2) AS sessions_per_user,
       ROUND(AVG((strftime('%s', end_time) - strftime('%s', start_time)) / 60.0), 2) AS avg_minutes
FROM sessions;
```

| sessions | users | sessions_per_user | avg_minutes |
|---|---|---|---|
| 6 | 3 | 2.0 | 25.0 |

**Other dialects (not run here / from memory):** MySQL `TIMESTAMPDIFF(MINUTE, start_time, end_time)`; SQL Server `DATEDIFF(MINUTE, start_time, end_time)`; PostgreSQL `EXTRACT(EPOCH FROM end_time - start_time) / 60`. Note the integer minute functions truncate; use seconds / 60.0 for decimals.

**pandas equivalent:**
```python
# sessions (DataFrames with the same columns as the SQL tables)
s = sessions.assign(st=pd.to_datetime(sessions["start_time"]), en=pd.to_datetime(sessions["end_time"]))
s["minutes"] = (s["en"] - s["st"]).dt.total_seconds() / 60
result = (s.groupby("user_id").agg(sessions=("session_id", "count"),
                                    finished_sessions=("en", "count"),
                                    avg_minutes=("minutes", "mean"))
           .round(2).reset_index())
```
Result (actual run):
```text
user_id  sessions  finished_sessions  avg_minutes
     U1         3                  3         20.0
     U2         2                  1          5.0
     U3         1                  1         60.0
```
**Edge cases:** U2 has a session with no end time (still open or the app crashed): it counts as a session but not in the average. Negative durations (end before start) are bad data; filter with `end_time >= start_time`. Very long sessions (tab left open) can be capped. Users with no sessions do not appear unless you LEFT JOIN from a users table.
**Likely follow-ups:**
- Median duration? Averages are skewed by long sessions; use a window-function median (see Q36).
- Sessions per user per day? Group by user and date.
**Common mistakes:** Averaging averages, treating NULL end times as zero, and using minute-truncating DATEDIFF.

### Q27 ⭐⭐ 🟡 Calculate Day-1 and Day-7 retention: the percentage of new users who returned exactly 1 day and 7 days after signup.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you join users to their later activity on an exact day offset, and keep immature users out of the denominator.
**Say this in the interview:** For each new user I look for activity exactly 1 day and exactly 7 days after signup. Day-1 retention is users who came back on day 1 divided by new users. Users whose day 7 has not happened yet are excluded from the day-7 denominator.
**Explain simply:**
- **Day-N retention** = share of new users active **exactly** N days after signup (not 'within N days').
- The join condition uses the day difference (`julianday(activity) - julianday(signup)`), and `COUNT(DISTINCT CASE ...)` counts each returning user once.
- A user who signed up 3 days before the data ends cannot have day 7 yet. Counting them lowers retention unfairly, so we use a data-end date and only eligible users.
- A LEFT JOIN keeps users who never came back (they count in the denominator).
**Example:** 5 users are old enough for day 7, and 2 of them were active 7 days after signup: 40%. Day 1: 4 of 6 = 66.67%.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-01 |
| 2 | 2025-01-01 |
| 3 | 2025-01-01 |
| 4 | 2025-01-05 |
| 5 | 2025-01-05 |
| 6 | 2025-01-18 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-02 |
| 1 | 2025-01-08 |
| 2 | 2025-01-02 |
| 3 | 2025-01-05 |
| 4 | 2025-01-06 |
| 4 | 2025-01-12 |
| 5 | 2025-01-09 |
| 6 | 2025-01-19 |
| 6 | 2025-01-20 |

**SQL:**
```sql
WITH params AS (SELECT MAX(activity_date) AS data_end FROM activity),
j AS (
  SELECT u.user_id, u.signup_date,
         MAX(CASE WHEN julianday(a.activity_date) - julianday(u.signup_date) = 1 THEN 1 ELSE 0 END) AS d1,
         MAX(CASE WHEN julianday(a.activity_date) - julianday(u.signup_date) = 7 THEN 1 ELSE 0 END) AS d7
  FROM users u
  LEFT JOIN activity a ON a.user_id = u.user_id
  GROUP BY u.user_id, u.signup_date
)
SELECT COUNT(*) AS d1_eligible, SUM(d1) AS d1_returned,
       ROUND(100.0 * SUM(d1) / COUNT(*), 2) AS day1_pct,
       SUM(CASE WHEN date(signup_date, '+7 days') <= data_end THEN 1 ELSE 0 END) AS d7_eligible,
       SUM(CASE WHEN date(signup_date, '+7 days') <= data_end THEN d7 ELSE 0 END) AS d7_returned,
       ROUND(100.0 * SUM(CASE WHEN date(signup_date, '+7 days') <= data_end THEN d7 ELSE 0 END)
             / SUM(CASE WHEN date(signup_date, '+7 days') <= data_end THEN 1 ELSE 0 END), 2) AS day7_pct
FROM j CROSS JOIN params
WHERE date(signup_date, '+1 day') <= data_end;
```

**Output:**

| d1_eligible | d1_returned | day1_pct | d7_eligible | d7_returned | day7_pct |
|---|---|---|---|---|---|
| 6 | 4 | 66.67 | 5 | 2 | 40.0 |

**pandas equivalent:**
```python
# users, activity (DataFrames with the same columns as the SQL tables)
u = users.assign(s=pd.to_datetime(users["signup_date"]))
a = activity.assign(a=pd.to_datetime(activity["activity_date"]))
data_end = a["a"].max()
m = u.merge(a, on="user_id", how="left")
m["off"] = (m["a"] - m["s"]).dt.days
f = m.groupby("user_id").agg(s=("s", "first"), d1=("off", lambda x: int((x == 1).any())),
                              d7=("off", lambda x: int((x == 7).any()))).reset_index()
e1 = f[f["s"] + pd.Timedelta(days=1) <= data_end]
e7 = f[f["s"] + pd.Timedelta(days=7) <= data_end]
result = pd.DataFrame({"d1_eligible": [len(e1)], "d1_returned": [int(e1["d1"].sum())],
                       "day1_pct": [round(100 * e1["d1"].sum() / len(e1), 2)],
                       "d7_eligible": [len(e7)], "d7_returned": [int(e7["d7"].sum())],
                       "day7_pct": [round(100 * e7["d7"].sum() / len(e7), 2)]})
```
Result (actual run):
```text
 d1_eligible  d1_returned  day1_pct  d7_eligible  d7_returned  day7_pct
           6            4     66.67            5            2      40.0
```
**Edge cases:** 'Exactly day 7' misses a user who returned on day 6 or 8; that is the classic definition, and Q35 covers the 'on or after' version. Several events on the same day count once (MAX/DISTINCT). Timestamps must be cut to dates first. Which date is the 'data end' matters; use the latest loaded date, not today.
**Likely follow-ups:**
- Per signup cohort instead of overall? Add `signup_date` (or month) to GROUP BY.
- Why exclude recent users? Their day 7 is in the future, so they would show as lost when they are simply not old enough (see Q41).
**Common mistakes:** Using BETWEEN 1 AND 7 and calling it Day-7 retention, including immature users in the denominator, and an inner join that drops users who never returned.

### Q28 ⭐⭐ 🟡 Calculate cumulative new customers over time (running total by month) and the cumulative share of total.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can build a running total with a window SUM and compute a share against the grand total with an empty OVER().
**Say this in the interview:** I count new customers per month, use SUM(...) OVER (ORDER BY month) for the running total, and divide it by SUM(...) OVER () which is the grand total, for the cumulative share.
**Explain simply:**
- **Running (cumulative) total**: each row adds its own number to everything before it.
- `SUM(x) OVER (ORDER BY month ROWS UNBOUNDED PRECEDING)` is the running total. Writing the frame explicitly avoids surprises with ties.
- `SUM(x) OVER ()` with nothing inside is the total over all rows, the denominator for the share.
- Cumulative share ends at exactly 100% on the last month.
**Example:** Hires per month: 2, 3, 1, 4 = 10 hires in all. Running totals 2, 5, 6, 10 give cumulative shares 20%, 50%, 60%, 100%.
**Sample data:**

`customers`

| customer_id | signup_date |
|---|---|
| 1 | 2025-01-05 |
| 2 | 2025-01-18 |
| 3 | 2025-02-02 |
| 4 | 2025-02-14 |
| 5 | 2025-02-27 |
| 6 | 2025-03-09 |
| 7 | 2025-04-01 |
| 8 | 2025-04-12 |
| 9 | 2025-04-20 |
| 10 | 2025-04-30 |

**SQL:**
```sql
WITH m AS (
  SELECT strftime('%Y-%m', signup_date) AS month, COUNT(*) AS new_customers
  FROM customers GROUP BY strftime('%Y-%m', signup_date)
)
SELECT month, new_customers,
       SUM(new_customers) OVER (ORDER BY month ROWS UNBOUNDED PRECEDING) AS cumulative_customers,
       ROUND(100.0 * SUM(new_customers) OVER (ORDER BY month ROWS UNBOUNDED PRECEDING)
             / SUM(new_customers) OVER (), 2) AS cumulative_share_pct
FROM m
ORDER BY month;
```

**Output:**

| month | new_customers | cumulative_customers | cumulative_share_pct |
|---|---|---|---|
| 2025-01 | 2 | 2 | 20.0 |
| 2025-02 | 3 | 5 | 50.0 |
| 2025-03 | 1 | 6 | 60.0 |
| 2025-04 | 4 | 10 | 100.0 |

**pandas equivalent:**
```python
# customers (DataFrames with the same columns as the SQL tables)
c = customers.assign(month=pd.to_datetime(customers["signup_date"]).dt.strftime("%Y-%m"))
m = c.groupby("month").size().reset_index(name="new_customers")
m["cumulative_customers"] = m["new_customers"].cumsum()
m["cumulative_share_pct"] = (100 * m["cumulative_customers"] / m["new_customers"].sum()).round(2)
result = m
```
Result (actual run):
```text
  month  new_customers  cumulative_customers  cumulative_share_pct
2025-01              2                     2                  20.0
2025-02              3                     5                  50.0
2025-03              1                     6                  60.0
2025-04              4                    10                 100.0
```
**Edge cases:** A month with zero signups is missing, so the running total just carries on (add a calendar if the chart needs every month). Duplicate customer rows would inflate counts: `COUNT(DISTINCT customer_id)`. If 'new customers' means first order, take `MIN(order_date)` per customer first. The share is of the total in the data you loaded, so it changes when new data arrives.
**Likely follow-ups:**
- Restart each year? `PARTITION BY strftime('%Y', ...)` inside OVER.
- Why ROWS and not the default? The default RANGE frame treats equal sort values as one group; ROWS is explicit and usually faster.
**Common mistakes:** Forgetting ORDER BY inside OVER (the 'running' total becomes the grand total), dividing by the wrong total, and counting repeat customers as new.

### Q29 ⭐⭐ 🟡 Calculate cumulative revenue per signup cohort by month since signup (a simple customer lifetime value curve).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can compute 'months since signup', group by cohort and run a cumulative SUM per cohort (PARTITION BY).
**Say this in the interview:** I join orders to each customer's signup month, compute months since signup, sum revenue per cohort and month number, then take a running total inside each cohort. Dividing by cohort size gives revenue per customer, a simple lifetime value curve.
**Explain simply:**
- **Cohort** = customers who signed up in the same month. We follow each cohort over time.
- **Months since signup** (month 0, 1, 2...) = (order year x 12 + order month) - (signup year x 12 + signup month).
- **Cumulative revenue** per cohort uses `SUM(...) OVER (PARTITION BY cohort ORDER BY month_n)`: the running total restarts for every cohort.
- **Customer lifetime value (CLV/LTV)** curve here = cumulative revenue / customers in the cohort. It only counts revenue seen so far.
**Example:** January cohort has 2 customers. By month 1 they have paid 100 + 60 + 50 = 210 in total, so 105 per customer.
**Sample data:**

`customers`

| customer_id | signup_date |
|---|---|
| C1 | 2025-01-04 |
| C2 | 2025-01-20 |
| C3 | 2025-02-03 |
| C4 | 2025-02-16 |

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 1 | C1 | 2025-01-10 | 100 |
| 2 | C1 | 2025-02-12 | 50 |
| 3 | C1 | 2025-04-05 | 80 |
| 4 | C2 | 2025-01-25 | 60 |
| 5 | C2 | 2025-03-02 | 40 |
| 6 | C3 | 2025-02-08 | 120 |
| 7 | C3 | 2025-03-15 | 30 |
| 8 | C4 | 2025-02-20 | 90 |

**SQL:**
```sql
WITH j AS (
  SELECT strftime('%Y-%m', c.signup_date) AS cohort,
         (CAST(strftime('%Y', o.order_date) AS INTEGER) * 12 + CAST(strftime('%m', o.order_date) AS INTEGER))
       - (CAST(strftime('%Y', c.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', c.signup_date) AS INTEGER)) AS month_n,
         o.amount
  FROM orders o JOIN customers c ON c.customer_id = o.customer_id
),
rev AS (SELECT cohort, month_n, SUM(amount) AS revenue FROM j GROUP BY cohort, month_n),
sz AS (SELECT strftime('%Y-%m', signup_date) AS cohort, COUNT(*) AS cohort_size FROM customers GROUP BY 1)
SELECT r.cohort, r.month_n, r.revenue,
       SUM(r.revenue) OVER (PARTITION BY r.cohort ORDER BY r.month_n ROWS UNBOUNDED PRECEDING) AS cumulative_revenue,
       sz.cohort_size,
       ROUND(1.0 * SUM(r.revenue) OVER (PARTITION BY r.cohort ORDER BY r.month_n ROWS UNBOUNDED PRECEDING)
             / sz.cohort_size, 2) AS cum_revenue_per_customer
FROM rev r JOIN sz ON sz.cohort = r.cohort
ORDER BY r.cohort, r.month_n;
```

**Output:**

| cohort | month_n | revenue | cumulative_revenue | cohort_size | cum_revenue_per_customer |
|---|---|---|---|---|---|
| 2025-01 | 0 | 160 | 160 | 2 | 80.0 |
| 2025-01 | 1 | 50 | 210 | 2 | 105.0 |
| 2025-01 | 2 | 40 | 250 | 2 | 125.0 |
| 2025-01 | 3 | 80 | 330 | 2 | 165.0 |
| 2025-02 | 0 | 210 | 210 | 2 | 105.0 |
| 2025-02 | 1 | 30 | 240 | 2 | 120.0 |

**pandas equivalent:**
```python
# customers, orders (DataFrames with the same columns as the SQL tables)
c = customers.assign(sd=pd.to_datetime(customers["signup_date"]))
c["cohort"] = c["sd"].dt.strftime("%Y-%m")
o = orders.assign(od=pd.to_datetime(orders["order_date"])).merge(c, on="customer_id")
o["month_n"] = (o["od"].dt.year * 12 + o["od"].dt.month) - (o["sd"].dt.year * 12 + o["sd"].dt.month)
rev = o.groupby(["cohort", "month_n"], as_index=False)["amount"].sum().rename(columns={"amount": "revenue"})
rev["cumulative_revenue"] = rev.groupby("cohort")["revenue"].cumsum()
sz = c.groupby("cohort").size().rename("cohort_size").reset_index()
rev = rev.merge(sz, on="cohort")
rev["cum_revenue_per_customer"] = (rev["cumulative_revenue"] / rev["cohort_size"]).round(2)
result = rev.sort_values(["cohort", "month_n"]).reset_index(drop=True)
```
Result (actual run):
```text
 cohort  month_n  revenue  cumulative_revenue  cohort_size  cum_revenue_per_customer
2025-01        0      160                 160            2                      80.0
2025-01        1       50                 210            2                     105.0
2025-01        2       40                 250            2                     125.0
2025-01        3       80                 330            2                     165.0
2025-02        0      210                 210            2                     105.0
2025-02        1       30                 240            2                     120.0
```
**Edge cases:** Months with no revenue (e.g. Jan cohort, month 2) have no row, so the curve skips from month 1 to month 3 (the running total is still right; add a month-number grid for a smooth chart). Customers with no orders still count in cohort size (that is why size comes from `customers`). Recent cohorts have fewer months, so compare cohorts at the same month_n only. Refunds: net them off the amount first.
**Likely follow-ups:**
- Show it as a pivot (one column per month)? Use `SUM(CASE WHEN month_n = k THEN ...)`; see Q34.
- Why is this only a 'simple' LTV? It has no margin, discounting or future prediction.
**Common mistakes:** Taking cohort size from the orders table (loses silent customers), mixing cohorts at different ages, and forgetting PARTITION BY (one running total across all cohorts).

### Q30 ⭐⭐ 🟡 Find customers who ordered in 3 consecutive months.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the gaps-and-islands trick: month number minus row number stays constant inside a streak.
**Say this in the interview:** I reduce orders to one row per customer per month, convert months to a number, subtract ROW_NUMBER, and rows in an unbroken streak get the same value. Groups with 3 or more months are the answer.
**Explain simply:**
- **Consecutive months**: no month missing in between, such as Nov, Dec, Jan (this also works across a year boundary because we use year x 12 + month).
- Take **distinct months** first. Two orders in one month would otherwise break the arithmetic.
- **Trick**: in a streak the month number goes up by 1 and the row number goes up by 1, so `month_number - row_number` stays the same. A gap changes it, starting a new group.
- Group by that value and keep groups with `COUNT(*) >= 3`.
**Example:** Customer A orders in Jan, Feb and Mar: month numbers 24301, 24302, 24303 minus row numbers 1, 2, 3 give 24300 every time: one streak of 3.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | A | 2025-01-05 |
| 2 | A | 2025-01-28 |
| 3 | A | 2025-02-10 |
| 4 | A | 2025-03-03 |
| 5 | B | 2025-01-09 |
| 6 | B | 2025-03-15 |
| 7 | B | 2025-04-02 |
| 8 | C | 2024-11-20 |
| 9 | C | 2024-12-18 |
| 10 | C | 2025-01-07 |
| 11 | D | 2025-01-12 |
| 12 | D | 2025-02-12 |

**SQL:**
```sql
WITH cm AS (
  SELECT DISTINCT customer_id,
         strftime('%Y-%m', order_date) AS month,
         CAST(strftime('%Y', order_date) AS INTEGER) * 12 + CAST(strftime('%m', order_date) AS INTEGER) AS mnum
  FROM orders
),
g AS (
  SELECT customer_id, month, mnum,
         mnum - ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY mnum) AS grp
  FROM cm
)
SELECT customer_id,
       MIN(month) AS streak_start,
       MAX(month) AS streak_end,
       COUNT(*)   AS months_in_streak
FROM g
GROUP BY customer_id, grp
HAVING COUNT(*) >= 3
ORDER BY customer_id, streak_start;
```

**Output:**

| customer_id | streak_start | streak_end | months_in_streak |
|---|---|---|---|
| A | 2025-01 | 2025-03 | 3 |
| C | 2024-11 | 2025-01 | 3 |

**pandas equivalent:**
```python
# orders (DataFrames with the same columns as the SQL tables)
o = orders.assign(d=pd.to_datetime(orders["order_date"]))
cm = o.assign(month=o["d"].dt.strftime("%Y-%m"), mnum=o["d"].dt.year * 12 + o["d"].dt.month)
cm = cm[["customer_id", "month", "mnum"]].drop_duplicates().sort_values(["customer_id", "mnum"])
cm["grp"] = cm["mnum"] - (cm.groupby("customer_id").cumcount() + 1)
r = (cm.groupby(["customer_id", "grp"])
       .agg(streak_start=("month", "min"), streak_end=("month", "max"), months_in_streak=("month", "count"))
       .reset_index())
result = (r[r["months_in_streak"] >= 3].drop(columns="grp")
          .sort_values(["customer_id", "streak_start"]).reset_index(drop=True))
```
Result (actual run):
```text
customer_id streak_start streak_end  months_in_streak
          A      2025-01    2025-03                 3
          C      2024-11    2025-01                 3
```
**Edge cases:** B ordered in Jan, Mar and Apr: the gap in Feb splits it into streaks of 1 and 2, so B is not returned. D has only 2 months. C crosses the year boundary and is correctly found. A longer streak is reported once with its full length (not as several 3-month windows). A customer with two separate 3-month streaks gets two rows. Remember the data end: a streak that is still running is shown as it stands.
**Likely follow-ups:**
- Exactly 'at least 3' vs 'exactly 3'? Change `>= 3` to `= 3`.
- Alternative without the trick? Self-join the distinct months to themselves at +1 and +2 months (works for exactly 3, awkward for N).
**Common mistakes:** Not taking DISTINCT months, using only the month number (breaks across December to January), and comparing text months with `+1`.

### Q31 ⭐⭐ 🔴 Build sessions from raw events: start a new session when a user is idle for more than 30 minutes (sessionization with LAG and a running SUM).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can chain LAG, a CASE flag and a running SUM, and whether you pin down the exact timeout boundary.
**Say this in the interview:** I sort each user's events by time, use LAG to get the previous event time, flag an event as a new session when the gap is more than 30 minutes, and take a running SUM of those flags to give every event a session number. I state the boundary: strictly greater than 30 minutes starts a new session, so a gap of exactly 30 minutes stays in the same one.
**Explain simply:**
- **Sessionization**: turning a stream of clicks into visits. A new visit starts after a long enough idle gap (the 30-minute timeout is a common convention, a business choice).
- **Boundary rule used here: gap > 30 minutes (> 1800 seconds) starts a new session; a gap of exactly 30 minutes does not.** Some teams use `>=`: confirm which one the interviewer wants.
- Step 1 `LAG(event_time)` gives the previous time per user. Step 2 flag = 1 if there is no previous event (first ever) or the gap is more than 1800 seconds, else 0. Step 3 running `SUM(flag)` gives session 1, 2, 3 ... per user.
- We use seconds (`strftime('%s', t)`), not fractional days, so the 30-minute boundary is exact.
**Example:** User 1 clicks at 09:00, 09:10, 09:40, 10:20, 10:25. Gaps are 10, 30, 40, 5 minutes. Only the 40-minute gap is more than 30, so there are 2 sessions: 09:00 to 09:40 and 10:20 to 10:25.
**Sample data:**

`events`

| event_id | user_id | event_time |
|---|---|---|
| 1 | U1 | 2025-03-01 09:00:00 |
| 2 | U1 | 2025-03-01 09:10:00 |
| 3 | U1 | 2025-03-01 09:40:00 |
| 4 | U1 | 2025-03-01 10:20:00 |
| 5 | U1 | 2025-03-01 10:25:00 |
| 6 | U2 | 2025-03-01 11:00:00 |
| 7 | U2 | 2025-03-01 11:31:00 |
| 8 | U2 | 2025-03-01 11:35:00 |

**SQL:**
```sql
WITH g AS (
  SELECT event_id, user_id, event_time,
         strftime('%s', event_time) - strftime('%s',
           LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time, event_id)) AS gap_sec
  FROM events
),
f AS (
  SELECT *, CASE WHEN gap_sec IS NULL OR gap_sec > 1800 THEN 1 ELSE 0 END AS new_session   -- > 30 min
  FROM g
),
s AS (
  SELECT *, SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_time, event_id
                                   ROWS UNBOUNDED PRECEDING) AS session_no
  FROM f
)
SELECT user_id, session_no,
       MIN(event_time) AS session_start,
       MAX(event_time) AS session_end,
       COUNT(*)        AS events,
       (strftime('%s', MAX(event_time)) - strftime('%s', MIN(event_time))) / 60 AS minutes
FROM s
GROUP BY user_id, session_no
ORDER BY user_id, session_no;
```

**Output:**

| user_id | session_no | session_start | session_end | events | minutes |
|---|---|---|---|---|---|
| U1 | 1 | 2025-03-01 09:00:00 | 2025-03-01 09:40:00 | 3 | 40 |
| U1 | 2 | 2025-03-01 10:20:00 | 2025-03-01 10:25:00 | 2 | 5 |
| U2 | 1 | 2025-03-01 11:00:00 | 2025-03-01 11:00:00 | 1 | 0 |
| U2 | 2 | 2025-03-01 11:31:00 | 2025-03-01 11:35:00 | 2 | 4 |

**Event-level view (gap, flag, running session number), real output:**
```sql
WITH g AS (
  SELECT event_id, user_id, event_time,
         (strftime('%s', event_time) - strftime('%s',
           LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time, event_id))) / 60.0 AS gap_min
  FROM events
)
SELECT event_id, user_id, event_time, gap_min,
       CASE WHEN gap_min IS NULL OR gap_min > 30 THEN 1 ELSE 0 END AS new_session,
       SUM(CASE WHEN gap_min IS NULL OR gap_min > 30 THEN 1 ELSE 0 END)
         OVER (PARTITION BY user_id ORDER BY event_time, event_id ROWS UNBOUNDED PRECEDING) AS session_no
FROM g ORDER BY user_id, event_time, event_id;
```

| event_id | user_id | event_time | gap_min | new_session | session_no |
|---|---|---|---|---|---|
| 1 | U1 | 2025-03-01 09:00:00 | NULL | 1 | 1 |
| 2 | U1 | 2025-03-01 09:10:00 | 10.0 | 0 | 1 |
| 3 | U1 | 2025-03-01 09:40:00 | 30.0 | 0 | 1 |
| 4 | U1 | 2025-03-01 10:20:00 | 40.0 | 1 | 2 |
| 5 | U1 | 2025-03-01 10:25:00 | 5.0 | 0 | 2 |
| 6 | U2 | 2025-03-01 11:00:00 | NULL | 1 | 1 |
| 7 | U2 | 2025-03-01 11:31:00 | 31.0 | 1 | 2 |
| 8 | U2 | 2025-03-01 11:35:00 | 4.0 | 0 | 2 |

**Other dialects (not run here / from memory):** PostgreSQL `event_time - LAG(event_time) OVER (...) > INTERVAL '30 minutes'`; MySQL 8 `TIMESTAMPDIFF(SECOND, LAG(event_time) OVER (...), event_time) > 1800`; SQL Server `DATEDIFF(SECOND, LAG(event_time) OVER (...), event_time) > 1800`. For the `>=` rule, change `> 1800` to `>= 1800`.

**pandas equivalent:**
```python
# events (DataFrames with the same columns as the SQL tables)
e = events.assign(t=pd.to_datetime(events["event_time"])).sort_values(["user_id", "t", "event_id"])
e["gap_sec"] = e.groupby("user_id")["t"].diff().dt.total_seconds()
e["new_session"] = (e["gap_sec"].isna() | (e["gap_sec"] > 1800)).astype(int)   # > 30 min
e["session_no"] = e.groupby("user_id")["new_session"].cumsum()
r = e.groupby(["user_id", "session_no"]).agg(session_start=("t", "min"), session_end=("t", "max"),
                                             events=("event_id", "count")).reset_index()
r["minutes"] = ((r["session_end"] - r["session_start"]).dt.total_seconds() // 60).astype(int)
r["session_start"] = r["session_start"].dt.strftime("%Y-%m-%d %H:%M:%S")
r["session_end"] = r["session_end"].dt.strftime("%Y-%m-%d %H:%M:%S")
result = r
```
Result (actual run):
```text
user_id  session_no       session_start         session_end  events  minutes
     U1           1 2025-03-01 09:00:00 2025-03-01 09:40:00       3       40
     U1           2 2025-03-01 10:20:00 2025-03-01 10:25:00       2        5
     U2           1 2025-03-01 11:00:00 2025-03-01 11:00:00       1        0
     U2           2 2025-03-01 11:31:00 2025-03-01 11:35:00       2        4
```
**Edge cases:** Event 3 is exactly 30 minutes after event 2 and stays in session 1 under the `>` rule; with `>=` it would start a new session, so U1 would have 3 sessions. U2's gap of 31 minutes starts a new session. The first event of every user has a NULL gap and must be flagged 1 (otherwise session numbers start at 0). Two events at the same second: the `event_id` tie-break keeps the order stable. Session length here is first to last click, so a one-click session lasts 0 minutes. Time zones: all times must be in the same zone.
**Likely follow-ups:**
- Why not just GROUP BY date? A visit can cross midnight and a day can hold many visits.
- Why a running SUM? Each flag marks 'a new session begins here'; adding them up counts how many sessions have begun so far, which is the session number.
**Common mistakes:** Forgetting to flag the first event, mixing up `>` and `>=` without saying so, using fractional-day arithmetic that misses the exact boundary, and not partitioning the window by user.

### Q32 ⭐⭐ 🔴 Build a monthly active-user bridge: for each month, count new, retained, resurrected and churned users, and check that they reconcile to MAU.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can classify each user-month as new, retained or resurrected, count churn from the previous month, and prove the totals reconcile.
**Say this in the interview:** From distinct user-months I label each active user in a month as new (first month ever), retained (active the month before) or resurrected (came back after a gap). Churned users are last month's actives missing this month. Then MAU must equal new + retained + resurrected, and also last MAU - churned + new + resurrected.
**Explain simply:**
- **MAU** (monthly active users) = distinct users active in the month.
- **New**: first month ever. **Retained**: active this month and last month. **Resurrected**: active this month, not last month, but seen before. **Churned**: active last month, not this month.
- **Reconciliation**: `MAU = new + retained + resurrected` and `retained = previous MAU - churned`. If these fail, a user is being classified twice or missed.
- Months are assumed consecutive in the data. If a month is missing entirely, build a calendar first.
**Example:** March: 4 active users = 1 new + 2 retained + 1 resurrected. February had 3 actives and 1 churned, so retained = 3 - 1 = 2.
**Sample data:**

`events`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-15 |
| 2 | 2025-01-15 |
| 3 | 2025-01-15 |
| 1 | 2025-02-15 |
| 2 | 2025-02-15 |
| 4 | 2025-02-15 |
| 1 | 2025-03-15 |
| 3 | 2025-03-15 |
| 4 | 2025-03-15 |
| 5 | 2025-03-15 |
| 1 | 2025-04-15 |
| 5 | 2025-04-15 |
| 6 | 2025-04-15 |

**SQL:**
```sql
WITH um AS (SELECT DISTINCT user_id, strftime('%Y-%m', activity_date) AS m FROM events),
fm AS (SELECT user_id, MIN(m) AS first_m FROM um GROUP BY user_id),
cls AS (
  SELECT um.m,
         CASE WHEN um.m = fm.first_m THEN 'new'
              WHEN EXISTS (SELECT 1 FROM um p WHERE p.user_id = um.user_id
                           AND p.m = strftime('%Y-%m', um.m || '-01', '-1 month')) THEN 'retained'
              ELSE 'resurrected' END AS c
  FROM um JOIN fm ON fm.user_id = um.user_id
),
ch AS (
  SELECT strftime('%Y-%m', p.m || '-01', '+1 month') AS m, COUNT(*) AS churned
  FROM um p
  WHERE NOT EXISTS (SELECT 1 FROM um n WHERE n.user_id = p.user_id
                    AND n.m = strftime('%Y-%m', p.m || '-01', '+1 month'))
  GROUP BY 1
),
agg AS (
  SELECT m AS month, COUNT(*) AS mau,
         SUM(c = 'new') AS new_users, SUM(c = 'retained') AS retained, SUM(c = 'resurrected') AS resurrected
  FROM cls GROUP BY m
),
x AS (
  SELECT a.month, a.mau, a.new_users, a.retained, a.resurrected,
         COALESCE(ch.churned, 0) AS churned,
         LAG(a.mau) OVER (ORDER BY a.month) AS prev_mau
  FROM agg a LEFT JOIN ch ON ch.m = a.month
)
SELECT month, mau, new_users, retained, resurrected, churned, prev_mau,
       CASE WHEN mau = new_users + retained + resurrected
             AND retained = COALESCE(prev_mau, 0) - churned THEN 'yes' ELSE 'NO' END AS reconciles
FROM x ORDER BY month;
```

**Output:**

| month | mau | new_users | retained | resurrected | churned | prev_mau | reconciles |
|---|---|---|---|---|---|---|---|
| 2025-01 | 3 | 3 | 0 | 0 | 0 | NULL | yes |
| 2025-02 | 3 | 1 | 2 | 0 | 1 | 3.0 | yes |
| 2025-03 | 4 | 1 | 2 | 1 | 1 | 3.0 | yes |
| 2025-04 | 3 | 1 | 2 | 0 | 2 | 4.0 | yes |

**pandas equivalent:**
```python
# events (DataFrames with the same columns as the SQL tables)
e = events.assign(m=pd.to_datetime(events["activity_date"]).dt.to_period("M"))
um = e[["user_id", "m"]].drop_duplicates()
first = um.groupby("user_id")["m"].min()
rows, prev_set, prev_mau = [], set(), None
for m in sorted(um["m"].unique()):
    cur = set(um[um["m"] == m]["user_id"])
    new = {u for u in cur if first[u] == m}
    ret = cur & prev_set
    res = cur - prev_set - new
    churned = len(prev_set - cur)
    ok = "yes" if len(cur) == len(new) + len(ret) + len(res) and len(ret) == (prev_mau or 0) - churned else "NO"
    rows.append([str(m), len(cur), len(new), len(ret), len(res), churned, prev_mau, ok])
    prev_set, prev_mau = cur, len(cur)
result = pd.DataFrame(rows, columns=["month", "mau", "new_users", "retained", "resurrected", "churned", "prev_mau", "reconciles"])
```
Result (actual run):
```text
  month  mau  new_users  retained  resurrected  churned  prev_mau reconciles
2025-01    3          3         0            0        0       NaN        yes
2025-02    3          1         2            0        1       3.0        yes
2025-03    4          1         2            1        1       3.0        yes
2025-04    3          1         2            0        2       4.0        yes
```
**Edge cases:** First month: everyone is new, nothing is retained, and prev_mau is NULL (treated as 0 in the check). User 3 is active in Jan, absent in Feb (counted as churned in Feb) and back in Mar (resurrected): the same person moves through churned and then resurrected, which is correct. Churn for the month after the last data month is not shown because that month has not happened. Duplicate events are removed by DISTINCT. A missing calendar month breaks the 'previous month' logic.
**Likely follow-ups:**
- Quick-ratio? (new + resurrected) / churned shows growth quality.
- What if the check says NO? Look for users with NULL ids, test accounts, or months missing from the data.
**Common mistakes:** Counting resurrected users as new, computing churn against the current month's base, and skipping the reconciliation that proves the buckets add up.

### Q33 ⭐⭐ 🔴 Calculate a strict-order funnel: count a user at 'purchase' only if the purchase happened after the 'cart' event, which happened after the 'view' event.
**Asked at:** commonly asked (no company-specific report found); listed as a common product-analytics SQL pattern on study sites (research/Book02_Part09_sources.md)
**What the interviewer is checking:** Whether you understand that a funnel step must happen after the previous step (order of events), not just exist.
**Say this in the interview:** I take each user's first view, then only count a cart that happens after it, then only count a purchase that happens after that cart. Each step is built on the step before it, so out-of-order events do not count.
**Explain simply:**
- A **funnel** is a chain of steps (view, then cart, then purchase). We count how many people survive each step.
- A **loose** funnel only asks 'did this user ever have a purchase event?'. It wrongly counts someone who bought before ever adding to cart (for example a repeat buyer, or a logging bug).
- A **strict** funnel chains the steps: cart must be later than view, purchase must be later than cart. Use `MIN(time)` per step so each user is counted once.
- Timestamps here are text in `YYYY-MM-DD HH:MM` format, which sort correctly as text. Real DATETIME columns work the same way.
**Example:** Of 8 shoppers, everyone viewed. Loose logic says 6 purchased (75.0%). Strict logic says only 2 did it in the right order (25.0%). The other 4 bought before adding to cart, skipped the cart, or carted before viewing.
**Sample data:**

`funnel_events`

| user_id | step | event_time |
|---|---|---|
| u1 | view | 2025-03-01 09:00 |
| u1 | cart | 2025-03-01 09:05 |
| u1 | purchase | 2025-03-01 09:20 |
| u2 | view | 2025-03-01 10:00 |
| u2 | cart | 2025-03-01 10:10 |
| u3 | purchase | 2025-03-01 11:00 |
| u3 | view | 2025-03-01 11:30 |
| u3 | cart | 2025-03-01 11:40 |
| u4 | view | 2025-03-01 12:00 |
| u4 | purchase | 2025-03-01 12:30 |
| u5 | cart | 2025-03-01 13:00 |
| u5 | view | 2025-03-01 13:10 |
| u5 | purchase | 2025-03-01 13:20 |
| u6 | view | 2025-03-02 09:00 |
| u6 | cart | 2025-03-02 09:30 |
| u6 | purchase | 2025-03-02 10:00 |
| u7 | view | 2025-03-02 11:00 |
| u8 | view | 2025-03-02 15:00 |
| u8 | purchase | 2025-03-02 15:10 |
| u8 | cart | 2025-03-02 15:20 |

**SQL:**
```sql
WITH v AS (SELECT user_id, MIN(event_time) AS t
           FROM funnel_events WHERE step = 'view' GROUP BY user_id),
c AS (SELECT e.user_id, MIN(e.event_time) AS t        -- first cart AFTER the first view
      FROM funnel_events e JOIN v ON v.user_id = e.user_id
      WHERE e.step = 'cart' AND e.event_time > v.t GROUP BY e.user_id),
p AS (SELECT e.user_id, MIN(e.event_time) AS t        -- first purchase AFTER that cart
      FROM funnel_events e JOIN c ON c.user_id = e.user_id
      WHERE e.step = 'purchase' AND e.event_time > c.t GROUP BY e.user_id)
SELECT 'view' AS step, (SELECT COUNT(*) FROM v) AS strict_users,
       100.0 AS strict_pct_of_view,
       (SELECT COUNT(DISTINCT user_id) FROM funnel_events WHERE step='view') AS loose_users
UNION ALL
SELECT 'cart', (SELECT COUNT(*) FROM c),
       ROUND(100.0 * (SELECT COUNT(*) FROM c) / (SELECT COUNT(*) FROM v), 1),
       (SELECT COUNT(DISTINCT user_id) FROM funnel_events WHERE step='cart')
UNION ALL
SELECT 'purchase', (SELECT COUNT(*) FROM p),
       ROUND(100.0 * (SELECT COUNT(*) FROM p) / (SELECT COUNT(*) FROM v), 1),
       (SELECT COUNT(DISTINCT user_id) FROM funnel_events WHERE step='purchase');
```

**Output:**

| step | strict_users | strict_pct_of_view | loose_users |
|---|---|---|---|
| view | 8 | 100.0 | 8 |
| cart | 5 | 62.5 | 6 |
| purchase | 2 | 25.0 | 6 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
fe = funnel_events
v = fe[fe.step == "view"].groupby("user_id", as_index=False).event_time.min().rename(columns={"event_time": "vt"})
c = fe[fe.step == "cart"].merge(v, on="user_id")
c = c[c.event_time > c.vt].groupby("user_id", as_index=False).event_time.min().rename(columns={"event_time": "ct"})
p = fe[fe.step == "purchase"].merge(c, on="user_id")
p = p[p.event_time > p.ct].groupby("user_id").size()
n = [len(v), len(c), len(p)]
loose = [fe[fe.step == s].user_id.nunique() for s in ["view", "cart", "purchase"]]
result = pd.DataFrame({"step": ["view", "cart", "purchase"], "strict_users": n,
                       "strict_pct_of_view": [round(100.0 * x / n[0], 1) for x in n],
                       "loose_users": loose})
```
Result (actual run):
```text
    step  strict_users  strict_pct_of_view  loose_users
    view             8               100.0            8
    cart             5                62.5            6
purchase             2                25.0            6
```
**Edge cases:** Two events at the exact same time fail the `>` test (change to `>=` only if your business says a tie is fine). A user with several carts: taking the first cart after the first view is enough, but if a user views again later you may prefer to chain from the latest view (say which rule you chose). A user can reach purchase only if they reached cart, so strict counts always shrink step by step. Empty result: if nobody carts after a view, `c` is empty and `p` is empty (the counts are 0, and the pct is 0.0).
**Likely follow-ups:**
- How do you get step-to-step conversion? Divide the next step by the previous step, not by views (see Q10).
- What if the funnel has a time limit (purchase within 24 hours of view)? Add `AND e.event_time <= datetime(v.t, '+1 day')` to the join (SQLite syntax; other dialects use DATEADD / INTERVAL, not run here).
**Common mistakes:** Counting `COUNT(DISTINCT user_id)` per step without comparing times (the loose funnel), joining without taking `MIN`, which multiplies rows, and forgetting that the order can be broken by data issues like delayed logging.

### Q34 ⭐⭐ 🔴 Produce a cohort retention table as percentages in pivot form (one column per month since signup) using conditional aggregation.
**Asked at:** commonly asked (no company-specific report found); listed as a common product-analytics SQL pattern on study sites (research/Book02_Part09_sources.md)
**What the interviewer is checking:** Whether you can pivot with conditional aggregation (CASE inside an aggregate) and compute months-since-signup correctly.
**Say this in the interview:** I compute months since signup for every activity row, then use one COUNT(DISTINCT CASE WHEN n = k THEN user_id END) per column, divide by the cohort size, and multiply by 100. That gives one row per cohort and one column per month.
**Explain simply:**
- A **cohort** is a group of users who share a starting month (they signed up in January, say).
- **Months since signup** `n` = (activity year - signup year) x 12 + (activity month - signup month). Month 0 is the signup month itself.
- **Conditional aggregation** means putting a `CASE WHEN` inside `COUNT(DISTINCT ...)`: each column counts only the users whose `n` matches that column. This is how you pivot in SQL when there is no PIVOT keyword (SQLite has none).
- Divide by the cohort size (all users who signed up), not by month-0 active users.
**Example:** January cohort has 4 signups. 3 were active in January (75.0%), 3 in February (75.0%), 1 in March (25.0%), 1 in April (25.0%).
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-05 |
| 2 | 2025-01-12 |
| 3 | 2025-01-20 |
| 4 | 2025-01-28 |
| 5 | 2025-02-03 |
| 6 | 2025-02-14 |
| 7 | 2025-02-25 |
| 8 | 2025-03-02 |
| 9 | 2025-03-18 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-06 |
| 1 | 2025-02-10 |
| 1 | 2025-03-12 |
| 2 | 2025-01-15 |
| 2 | 2025-02-20 |
| 3 | 2025-01-21 |
| 4 | 2025-02-02 |
| 4 | 2025-04-03 |
| 5 | 2025-02-05 |
| 5 | 2025-03-08 |
| 5 | 2025-04-09 |
| 6 | 2025-02-20 |
| 6 | 2025-03-21 |
| 7 | 2025-02-26 |
| 8 | 2025-03-05 |
| 8 | 2025-04-11 |
| 9 | 2025-03-20 |

**SQL:**
```sql
WITH base AS (
  SELECT u.user_id,
         strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', a.activity_date) AS INT) - CAST(strftime('%Y', u.signup_date) AS INT)) * 12
         + CAST(strftime('%m', a.activity_date) AS INT) - CAST(strftime('%m', u.signup_date) AS INT) AS n
  FROM users u JOIN activity a ON a.user_id = u.user_id),
size AS (SELECT strftime('%Y-%m', signup_date) AS cohort_month, COUNT(*) AS cohort_users
         FROM users GROUP BY 1)
SELECT s.cohort_month, s.cohort_users,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.n = 0 THEN b.user_id END) / s.cohort_users, 1) AS m0,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.n = 1 THEN b.user_id END) / s.cohort_users, 1) AS m1,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.n = 2 THEN b.user_id END) / s.cohort_users, 1) AS m2,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN b.n = 3 THEN b.user_id END) / s.cohort_users, 1) AS m3
FROM size s LEFT JOIN base b ON b.cohort_month = s.cohort_month
GROUP BY s.cohort_month, s.cohort_users
ORDER BY s.cohort_month;
```

**Output:**

| cohort_month | cohort_users | m0 | m1 | m2 | m3 |
|---|---|---|---|---|---|
| 2025-01 | 4 | 75.0 | 75.0 | 25.0 | 25.0 |
| 2025-02 | 3 | 100.0 | 66.7 | 33.3 | 0.0 |
| 2025-03 | 2 | 100.0 | 50.0 | 0.0 | 0.0 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
u = users.assign(sd=pd.to_datetime(users.signup_date))
u["cohort_month"] = u.sd.dt.strftime("%Y-%m")
b = activity.merge(u, on="user_id")
b["n"] = (pd.to_datetime(b.activity_date).dt.year - b.sd.dt.year) * 12 + pd.to_datetime(b.activity_date).dt.month - b.sd.dt.month
size = u.groupby("cohort_month").size().rename("cohort_users")
cnt = (b[b.n.between(0, 3)].groupby(["cohort_month", "n"]).user_id.nunique()
        .unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0))
cnt = cnt.reindex(size.index, fill_value=0)
pct = cnt.div(size, axis=0).mul(100).round(1)
pct.columns = ["m0", "m1", "m2", "m3"]
result = pd.concat([size, pct], axis=1).reset_index()
```
Result (actual run):
```text
cohort_month  cohort_users    m0   m1   m2   m3
     2025-01             4  75.0 75.0 25.0 25.0
     2025-02             3 100.0 66.7 33.3  0.0
     2025-03             2 100.0 50.0  0.0  0.0
```
**Edge cases:** Cells for months that have not happened yet (the March cohort's m2 and m3, the February cohort's m3) show 0.0, which looks like 'everyone left'. The data simply ends in April 2025. See Q41 to blank those cells. Duplicates: `COUNT(DISTINCT ...)` stops a user with many activity rows from counting twice. A user with no activity at all still counts in the cohort size because of the LEFT JOIN. Months with zero activity give 0.0, not NULL.
**Likely follow-ups:**
- How do you make the column list dynamic? Plain SQL cannot; build the SQL string in the app/Python, or pivot in pandas/BI.
- How do you show it as heat-map-ready numbers? Export this table; the percentages already line up by month number.
**Common mistakes:** Dividing by the month-0 active count, using `COUNT(*)` instead of `COUNT(DISTINCT user_id)`, getting months-since wrong across a year boundary (subtracting only month numbers), and showing 0.0 for months that have not happened yet.

### Q35 ⭐⭐ 🔴 Calculate rolling N-day (bracket) retention: the percentage of users who were active on or after day N, versus classic day-N retention. Explain the difference.
**Asked at:** commonly asked (no company-specific report found); listed as a common product-analytics SQL pattern on study sites (research/Book02_Part09_sources.md)
**What the interviewer is checking:** Whether you know classic (exact day) retention versus bracket / unbounded (on or after day N) retention, and when each is used.
**Say this in the interview:** Classic day-7 retention counts users who came back exactly on day 7. Bracket, also called rolling or unbounded, retention counts users who came back on day 7 or any later day. Bracket is always the same or higher, and it forgives people who simply skipped one particular day.
**Explain simply:**
- **Day N** means N days after the signup date. Day 0 is signup day.
- **Classic** = was the user active on day N exactly? Strict and noisy: someone active on days 6 and 8 but not 7 is a miss.
- **Bracket (rolling / unbounded)** = was the user's last activity on or after day N? Compute each user's latest day offset with `MAX`, then count those with `max_d >= N`.
- Use classic for habit-forming apps (daily use). Use bracket for products people use occasionally, such as a payroll or leave app used once a month.
**Example:** Of 10 new users, 3 returned exactly on day 7 (30.0% classic) but 7 had some activity on day 7 or later (70.0% bracket). Same people, two honest answers to two different questions. Say which one a dashboard uses.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-01 |
| 2 | 2025-01-01 |
| 3 | 2025-01-01 |
| 4 | 2025-01-01 |
| 5 | 2025-01-01 |
| 6 | 2025-01-03 |
| 7 | 2025-01-03 |
| 8 | 2025-01-03 |
| 9 | 2025-01-03 |
| 10 | 2025-01-03 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-01 |
| 1 | 2025-01-02 |
| 1 | 2025-01-08 |
| 1 | 2025-01-15 |
| 2 | 2025-01-01 |
| 2 | 2025-01-04 |
| 2 | 2025-01-10 |
| 3 | 2025-01-01 |
| 3 | 2025-01-02 |
| 4 | 2025-01-01 |
| 4 | 2025-01-08 |
| 5 | 2025-01-01 |
| 5 | 2025-01-21 |
| 6 | 2025-01-03 |
| 6 | 2025-01-05 |
| 6 | 2025-01-09 |
| 7 | 2025-01-03 |
| 7 | 2025-01-04 |
| 7 | 2025-01-11 |
| 7 | 2025-01-18 |
| 8 | 2025-01-03 |
| 9 | 2025-01-03 |
| 9 | 2025-01-17 |
| 10 | 2025-01-03 |
| 10 | 2025-01-08 |
| 10 | 2025-01-10 |

**SQL:**
```sql
WITH act AS (
  SELECT u.user_id,
         CAST(ROUND(julianday(a.activity_date) - julianday(u.signup_date)) AS INT) AS d
  FROM users u JOIN activity a ON a.user_id = u.user_id),
last_seen AS (SELECT user_id, MAX(d) AS max_d FROM act GROUP BY user_id),
nn(day_n) AS (VALUES (1), (7), (14))
SELECT day_n,
       (SELECT COUNT(*) FROM users) AS total_users,
       (SELECT COUNT(DISTINCT user_id) FROM act WHERE d = day_n) AS classic_users,
       ROUND(100.0 * (SELECT COUNT(DISTINCT user_id) FROM act WHERE d = day_n)
             / (SELECT COUNT(*) FROM users), 1) AS classic_pct,
       (SELECT COUNT(*) FROM last_seen WHERE max_d >= day_n) AS bracket_users,
       ROUND(100.0 * (SELECT COUNT(*) FROM last_seen WHERE max_d >= day_n)
             / (SELECT COUNT(*) FROM users), 1) AS bracket_pct
FROM nn ORDER BY day_n;
```

**Output:**

| day_n | total_users | classic_users | classic_pct | bracket_users | bracket_pct |
|---|---|---|---|---|---|
| 1 | 10 | 3 | 30.0 | 9 | 90.0 |
| 7 | 10 | 3 | 30.0 | 7 | 70.0 |
| 14 | 10 | 2 | 20.0 | 4 | 40.0 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
a = activity.merge(users, on="user_id")
a["d"] = (pd.to_datetime(a.activity_date) - pd.to_datetime(a.signup_date)).dt.days
mx = a.groupby("user_id").d.max()
tot = len(users)
rows = []
for n in [1, 7, 14]:
    cl = a[a.d == n].user_id.nunique()
    br = int((mx >= n).sum())
    rows.append((n, tot, cl, round(100.0 * cl / tot, 1), br, round(100.0 * br / tot, 1)))
result = pd.DataFrame(rows, columns=["day_n", "total_users", "classic_users", "classic_pct", "bracket_users", "bracket_pct"])
```
Result (actual run):
```text
 day_n  total_users  classic_users  classic_pct  bracket_users  bracket_pct
     1           10              3         30.0              9         90.0
     7           10              3         30.0              7         70.0
    14           10              2         20.0              4         40.0
```
**Edge cases:** Users with only day-0 activity have `max_d = 0` so they fail every bracket test, which is correct. Every user must be old enough: here data runs 20+ days after signup; for recent signups use the immature-cohort fix in Q41. `classic_users` uses `COUNT(DISTINCT)` because a user can have several events on the same day.
**Likely follow-ups:**
- Which number is bigger? Bracket is always greater than or equal to classic for the same N.
- Why can bracket retention never go up as N increases? A user counted on day 14 is also counted on day 7, so the curve only falls.
**Common mistakes:** Mixing the two definitions in one report, forgetting to label which one is shown, computing classic with `>=`, and dividing by active users instead of all signed-up users.

### Q36 ⭐ 🟡 Find the median time taken by users to go from signup to first purchase.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can compute a median without a built-in function and know why median beats average for skewed waiting times.
**Say this in the interview:** I find each buyer's days from signup to first purchase, number the rows in order, and take the middle value, or the average of the two middle values when the count is even. I prefer median because a few very slow buyers drag the average up.
**Explain simply:**
- The **median** is the middle value after sorting. Half the users take less time, half take more.
- The **average** is pulled up by outliers. One user who took 59 days lifts the average, but barely moves the median.
- With `ROW_NUMBER()` and `COUNT(*) OVER ()` the middle positions are `(cnt+1)/2` and `(cnt+2)/2` (integer division). For an odd count both are the same row; for an even count they are the two middle rows, and `AVG` of them is the median.
- Use `MIN(purchase_date)` per user to get the first purchase.
**Example:** 6 buyers took 1, 2, 3, 4, 7 and 59 days. The median is (3 + 4) / 2 = 3.5 days; the average is 12.7 days, which wrongly suggests that a typical user waits almost two weeks.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-01 |
| 2 | 2025-01-03 |
| 3 | 2025-01-05 |
| 4 | 2025-01-08 |
| 5 | 2025-01-10 |
| 6 | 2025-01-12 |
| 7 | 2025-01-15 |

`purchases`

| user_id | purchase_date |
|---|---|
| 1 | 2025-01-02 |
| 1 | 2025-02-01 |
| 2 | 2025-01-06 |
| 3 | 2025-01-12 |
| 4 | 2025-01-10 |
| 5 | 2025-03-10 |
| 7 | 2025-01-19 |

**SQL:**
```sql
WITH d AS (
  SELECT u.user_id,
         CAST(ROUND(julianday(MIN(p.purchase_date)) - julianday(u.signup_date)) AS INT) AS days
  FROM users u JOIN purchases p ON p.user_id = u.user_id
  GROUP BY u.user_id, u.signup_date),
r AS (SELECT days, ROW_NUMBER() OVER (ORDER BY days) AS rn, COUNT(*) OVER () AS cnt FROM d)
SELECT MAX(cnt) AS buyers,
       AVG(days) AS median_days,                       -- average of the 1 or 2 middle rows
       (SELECT ROUND(AVG(days), 1) FROM d) AS avg_days
FROM r
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2);
```

Other dialects (not run here / from memory): PostgreSQL `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY days)`; SQL Server `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY days) OVER ()`; MySQL has no built-in median (use the ROW_NUMBER method above). SQLite has no percentile function, so the row-number method is the one run here.

**Output:**

| buyers | median_days | avg_days |
|---|---|---|
| 6 | 3.5 | 12.7 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
f = purchases.groupby("user_id", as_index=False).purchase_date.min().merge(users, on="user_id")
f["days"] = (pd.to_datetime(f.purchase_date) - pd.to_datetime(f.signup_date)).dt.days
result = pd.DataFrame({"buyers": [len(f)], "median_days": [f.days.median()], "avg_days": [round(f.days.mean(), 1)]})
```
Result (actual run):
```text
 buyers  median_days  avg_days
      6          3.5      12.7
```
**Edge cases:** Users who never purchased (user 6) are dropped by the inner join: say that the median is among buyers only, or the real median could be 'never'. Same-day purchase gives 0 days. NULLs in `days` would sort first, so filter them. Ties are fine because only the values matter.
**Likely follow-ups:**
- How would you get the 90th percentile? Use position `CEIL(0.9 * cnt)` instead of the middle (or PERCENTILE_CONT in PostgreSQL, not run here).
- What about users who have not purchased yet? Report the share of non-buyers separately, or use a survival-style view (see Q41).
**Common mistakes:** Reporting the average, taking the middle row without handling an even count, using all purchases instead of the first one, and ignoring users who never bought.

### Q37 ⭐ 🟡 Calculate week-over-week (WoW) growth correctly across the year boundary (week 52/53 to week 1).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you key weeks by a real date (week start) rather than a week number that resets on 1 January.
**Say this in the interview:** I convert every date to the Monday of its week and compare each week to the row seven days earlier. A date key keeps ordering and gaps correct across the year boundary, where week numbers reset or split.
**Explain simply:**
- **WoW growth** = (this week - last week) / last week x 100.
- Week numbers (`%W`) restart each year, and a week that straddles 31 December gets two labels. Comparing 'week 1' to 'week 52' by number breaks.
- Fix: use the **week start date** (Monday) as the key. Dates sort naturally and `date(week_start, '-7 days')` is exactly last week, even across years.
- Joining to 'the row 7 days earlier' is safer than `LAG`, because `LAG` would silently compare to a non-adjacent week if a week had no orders.
**Example:** The week of Mon 30 Dec 2024 holds orders on 30 Dec and 2 Jan. The naive label splits it into 2024-53 (120) and 2025-00 (140). The correct week is one row of 260, which is -31.6% against 380 the week before.
**Sample data:**

`orders`

| order_date | amount |
|---|---|
| 2024-12-16 | 100 |
| 2024-12-18 | 150 |
| 2024-12-23 | 200 |
| 2024-12-27 | 180 |
| 2024-12-30 | 120 |
| 2025-01-02 | 140 |
| 2025-01-06 | 300 |
| 2025-01-09 | 250 |
| 2025-01-13 | 400 |

**Why week numbers fail (SQLite, run here):**
```sql
-- WRONG way: label weeks with year + week number
SELECT strftime('%Y-%W', order_date) AS naive_week, SUM(amount) AS revenue
FROM orders GROUP BY 1 ORDER BY MIN(order_date);
```

| naive_week | revenue |
|---|---|
| 2024-51 | 250 |
| 2024-52 | 380 |
| 2024-53 | 120 |
| 2025-00 | 140 |
| 2025-01 | 550 |
| 2025-02 | 400 |

**SQL:**
```sql
WITH w AS (
  SELECT date(order_date, '-' || ((CAST(strftime('%w', order_date) AS INT) + 6) % 7) || ' days') AS week_start,
         SUM(amount) AS revenue
  FROM orders GROUP BY 1)                       -- Monday of each order's week
SELECT cur.week_start, cur.revenue, prev.revenue AS prev_revenue,
       ROUND(100.0 * (cur.revenue - prev.revenue) / NULLIF(prev.revenue, 0), 1) AS wow_pct
FROM w cur
LEFT JOIN w prev ON prev.week_start = date(cur.week_start, '-7 days')
ORDER BY cur.week_start;
```

Dialect notes (not run here / from memory): PostgreSQL `date_trunc('week', order_date)` gives the Monday; MySQL `DATE_SUB(d, INTERVAL WEEKDAY(d) DAY)`; SQL Server needs `DATEADD` with `DATEDIFF` (depends on `DATEFIRST`). SQLite has none of these, so the weekday arithmetic above is used.

**Output:**

| week_start | revenue | prev_revenue | wow_pct |
|---|---|---|---|
| 2024-12-16 | 250 | NULL | NULL |
| 2024-12-23 | 380 | 250 | 52.0 |
| 2024-12-30 | 260 | 380 | -31.6 |
| 2025-01-06 | 550 | 260 | 111.5 |
| 2025-01-13 | 400 | 550 | -27.3 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
o = orders.assign(d=pd.to_datetime(orders.order_date))
o["week_start"] = (o.d - pd.to_timedelta(o.d.dt.weekday, unit="D")).dt.strftime("%Y-%m-%d")
w = o.groupby("week_start", as_index=False).amount.sum().rename(columns={"amount": "revenue"})
prev = w.assign(week_start=(pd.to_datetime(w.week_start) + pd.Timedelta(days=7)).dt.strftime("%Y-%m-%d"))
prev = prev.rename(columns={"revenue": "prev_revenue"})
result = w.merge(prev, on="week_start", how="left")
result["wow_pct"] = ((result.revenue - result.prev_revenue) / result.prev_revenue * 100).round(1)
result = result.sort_values("week_start").reset_index(drop=True)
```
Result (actual run):
```text
week_start  revenue  prev_revenue  wow_pct
2024-12-16      250           NaN      NaN
2024-12-23      380         250.0     52.0
2024-12-30      260         380.0    -31.6
2025-01-06      550         260.0    111.5
2025-01-13      400         550.0    -27.3
```
**Edge cases:** First week has no previous week, so `prev_revenue` and `wow_pct` are NULL. A previous revenue of 0 gives NULL via `NULLIF`. A week with no orders at all is missing from the table: join to a calendar of weeks if you need a row for it (see Q43 for a generated calendar). ISO weeks (Monday start, week 1 contains 4 January) differ from `%W`; state which week definition you use.
**Likely follow-ups:**
- What about weeks that start on Sunday? Change the offset to `% 7` using `strftime('%w')` directly (Sunday = 0).
- Why not use LAG? It is fine if every week is present; the self-join is safer when weeks can be missing.
**Common mistakes:** Using `year` and `week number` as separate columns, assuming week 52 is followed by week 1 of the same year, and dividing by zero in a quiet week.

### Q38 ⭐ 🟡 Compare retention across acquisition channels (e.g. organic, paid, referral) using the same cohort logic.
**Asked at:** commonly asked (no company-specific report found); listed as a common product-analytics SQL pattern on study sites (research/Book02_Part09_sources.md)
**What the interviewer is checking:** Whether you can reuse the same retention logic and just add GROUP BY channel, with a LEFT JOIN so non-returners still count.
**Say this in the interview:** I keep the cohort rule the same for everyone, month-1 retention, and add the acquisition channel as the grouping column. The LEFT JOIN keeps users who never came back in the denominator.
**Explain simply:**
- **Acquisition channel** is where a user came from: organic (found us), paid (ads), referral (a friend).
- A fair comparison needs the **same definition** for every channel: active in the calendar month after the signup month.
- Put the month condition in the `ON` clause, not in `WHERE`. A `WHERE` filter would delete users with no activity and inflate the percentage.
- Use `'start of month', '+1 month'` in SQLite. Plain `'+1 month'` on 31 January gives 3 March, which is wrong (user 4 signed up on 31 Jan).
**Example:** Referral kept 3 of 3 (100.0%), organic 3 of 5 (60.0%) and paid 1 of 4 (25.0%). Paid brings volume but the users fade fast, so marketing should look at the cost per retained user.
**Sample data:**

`users`

| user_id | channel | signup_date |
|---|---|---|
| 1 | organic | 2025-01-03 |
| 2 | organic | 2025-01-05 |
| 3 | organic | 2025-01-07 |
| 4 | organic | 2025-01-31 |
| 5 | organic | 2025-01-11 |
| 6 | paid | 2025-01-13 |
| 7 | paid | 2025-01-15 |
| 8 | paid | 2025-01-17 |
| 9 | paid | 2025-01-19 |
| 10 | referral | 2025-01-21 |
| 11 | referral | 2025-01-23 |
| 12 | referral | 2025-01-25 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-04 |
| 1 | 2025-02-10 |
| 2 | 2025-02-20 |
| 3 | 2025-01-10 |
| 4 | 2025-02-15 |
| 5 | 2025-03-05 |
| 6 | 2025-01-09 |
| 7 | 2025-02-02 |
| 8 | 2025-03-01 |
| 9 | 2025-01-20 |
| 10 | 2025-02-11 |
| 11 | 2025-02-18 |
| 12 | 2025-02-27 |
| 12 | 2025-03-15 |

**SQL:**
```sql
SELECT u.channel,
       COUNT(DISTINCT u.user_id) AS users,
       COUNT(DISTINCT a.user_id) AS retained_m1,
       ROUND(100.0 * COUNT(DISTINCT a.user_id) / COUNT(DISTINCT u.user_id), 1) AS m1_retention_pct
FROM users u
LEFT JOIN activity a
  ON a.user_id = u.user_id
 AND strftime('%Y-%m', a.activity_date) = strftime('%Y-%m', u.signup_date, 'start of month', '+1 month')
GROUP BY u.channel
ORDER BY m1_retention_pct DESC, u.channel;
```

**Output:**

| channel | users | retained_m1 | m1_retention_pct |
|---|---|---|---|
| referral | 3 | 3 | 100.0 |
| organic | 5 | 3 | 60.0 |
| paid | 4 | 1 | 25.0 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
u = users.assign(nm=(pd.to_datetime(users.signup_date).dt.to_period("M") + 1).astype(str))
a = activity.assign(am=pd.to_datetime(activity.activity_date).dt.to_period("M").astype(str))
ret = a.merge(u, on="user_id")
ret = ret[ret.am == ret.nm].groupby("channel").user_id.nunique().rename("retained_m1")
g = u.groupby("channel").size().rename("users")
result = pd.concat([g, ret], axis=1).fillna(0).astype(int)
result["m1_retention_pct"] = (result.retained_m1 / result.users * 100).round(1)
result = result.reset_index().sort_values(["m1_retention_pct", "channel"], ascending=[False, True]).reset_index(drop=True)
```
Result (actual run):
```text
 channel  users  retained_m1  m1_retention_pct
referral      3            3             100.0
 organic      5            3              60.0
    paid      4            1              25.0
```
**Edge cases:** Small groups swing wildly: referral's 100.0% is only 3 users, so show the user counts next to the percentage. A channel with NULL value groups as its own NULL row (label it 'unknown'). Users with several activities in the target month are counted once by `COUNT(DISTINCT)`. If a channel's cohorts are different ages, compare cohort by cohort (see Q41).
**Likely follow-ups:**
- How do you add the cohort month? Add `strftime('%Y-%m', u.signup_date)` to the SELECT and GROUP BY.
- How do you know the difference is real? Check the sample size; a statistical test is beyond SQL.
**Common mistakes:** Moving the month condition to `WHERE`, dividing by retained users instead of all users, `+1 month` from month-end dates, and comparing channels with very different group sizes without noting it.

### Q39 ⭐ 🟡 For a quick-commerce app, calculate the percentage of customers who reorder within 30 days of their first order.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can anchor a time window to each customer's own first order, and whether you exclude customers who have not had 30 days yet.
**Say this in the interview:** I find each customer's first order date, check if any later order falls within the next 30 days, and divide by customers whose first order is at least 30 days old. Otherwise recent customers would drag the rate down unfairly.
**Explain simply:**
- **Reorder rate in 30 days** = customers who ordered again within 30 days of their first order / customers who had the chance (first order at least 30 days before the data end date).
- Quick commerce (groceries in minutes) lives on repeat habits, so the first month matters. This is the business reason for the metric.
- `order_date > first_date` skips a second order on the same day. Decide with the business whether same-day counts; many teams say it does not.
- `EXISTS` answers 'is there at least one such row?' and does not multiply rows.
**Example:** 10 customers; 4 reordered within 30 days, so the naive rate is 40.0%. But customers c7 and c8 first ordered on 5 and 20 March, so they have not had 30 days yet. Among the 8 eligible customers the rate is 4 / 8 = 50.0%.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | c1 | 2025-01-05 |
| 2 | c1 | 2025-01-20 |
| 3 | c2 | 2025-01-10 |
| 4 | c2 | 2025-03-01 |
| 5 | c3 | 2025-01-15 |
| 6 | c4 | 2025-02-01 |
| 7 | c4 | 2025-02-01 |
| 8 | c4 | 2025-03-10 |
| 9 | c5 | 2025-02-10 |
| 10 | c5 | 2025-03-12 |
| 11 | c6 | 2025-02-20 |
| 12 | c6 | 2025-02-22 |
| 13 | c7 | 2025-03-05 |
| 14 | c8 | 2025-03-20 |
| 15 | c9 | 2025-01-25 |
| 16 | c9 | 2025-02-24 |
| 17 | c10 | 2025-02-05 |

**SQL:**
```sql
WITH f AS (SELECT customer_id, MIN(order_date) AS first_date FROM orders GROUP BY customer_id),
flag AS (
  SELECT f.customer_id, f.first_date,
         EXISTS (SELECT 1 FROM orders o
                 WHERE o.customer_id = f.customer_id
                   AND o.order_date > f.first_date
                   AND o.order_date <= date(f.first_date, '+30 days')) AS reordered,
         f.first_date <= date('2025-03-31', '-30 days') AS mature      -- as-of date 2025-03-31
  FROM f)
SELECT COUNT(*) AS all_customers,
       SUM(reordered) AS reordered_all,
       ROUND(100.0 * SUM(reordered) / COUNT(*), 1) AS naive_pct,
       SUM(mature) AS eligible,
       SUM(reordered * mature) AS reordered_eligible,
       ROUND(100.0 * SUM(reordered * mature) / SUM(mature), 1) AS pct_eligible
FROM flag;
```

**Output:**

| all_customers | reordered_all | naive_pct | eligible | reordered_eligible | pct_eligible |
|---|---|---|---|---|---|
| 10 | 4 | 40.0 | 8 | 4 | 50.0 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
f = orders.groupby("customer_id", as_index=False).order_date.min().rename(columns={"order_date": "first_date"})
m = orders.merge(f, on="customer_id")
fd, od = pd.to_datetime(m.first_date), pd.to_datetime(m.order_date)
re_ids = set(m[(od > fd) & (od <= fd + pd.Timedelta(days=30))].customer_id)
f["reordered"] = f.customer_id.isin(re_ids).astype(int)
f["mature"] = (pd.to_datetime(f.first_date) <= pd.Timestamp("2025-03-31") - pd.Timedelta(days=30)).astype(int)
tot, mat = len(f), int(f.mature.sum())
rall = int(f.reordered.sum())
rel = int((f.reordered * f.mature).sum())
result = pd.DataFrame([(tot, rall, round(100.0 * rall / tot, 1), mat, rel, round(100.0 * rel / mat, 1))],
                      columns=["all_customers", "reordered_all", "naive_pct", "eligible", "reordered_eligible", "pct_eligible"])
```
Result (actual run):
```text
 all_customers  reordered_all  naive_pct  eligible  reordered_eligible  pct_eligible
            10              4       40.0         8                   4          50.0
```
**Edge cases:** Day 30 exactly counts (`<=`): c5 ordered on 10 Feb and again on 12 Mar, and c9 on 25 Jan and again on 24 Feb. Customer c4 has two orders on the same day: not a reorder here. Customers with one order never match, so they are correctly counted as non-reorderers. The as-of date is hard-coded; in practice use the latest loaded date, not today.
**Likely follow-ups:**
- What changes if the window is 7 days? Change `+30 days` and `-30 days`.
- How do you see it by first-order month? Add `strftime('%Y-%m', first_date)` and GROUP BY it.
**Common mistakes:** Counting the first order itself as a reorder, including customers who have not had 30 days yet, dividing by all orders instead of customers, and using the calendar month instead of 'days after own first order'.

### Q40 ⭐ 🟡 Clean raw event logs before computing active users: remove duplicate events, null user_ids and test accounts. What checks do you run?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you check data quality before trusting a metric, and can remove duplicates with ROW_NUMBER.
**Say this in the interview:** First I audit: count null user ids, test accounts and duplicate events. Then I build a clean set that drops them, keeping one row per duplicate group, and compare the metric before and after.
**Explain simply:**
- A **duplicate event** is the same user, event type and time logged twice (for example a double-firing tracker or an app retry).
- **Test accounts** (staff, QA, bots) are flagged in an accounts table. They inflate user counts.
- **NULL user_id** rows cannot be tied to a person. `COUNT(DISTINCT user_id)` silently ignores them, but event counts do not.
- `ROW_NUMBER() OVER (PARTITION BY user, type, time ORDER BY event_id)` numbers the copies; keep `rn = 1`.
- Use `NOT EXISTS` instead of `NOT IN` for test accounts: `NOT IN` returns nothing if the list contains a NULL.
**Example:** 11 raw rows: 2 have no user, 2 belong to test user u99, and 2 are repeated copies. Only 5 clean events remain. Daily active users on 1 March fall from 3 to 2.
**Sample data:**

`events`

| event_id | user_id | event_type | event_time |
|---|---|---|---|
| 1 | u1 | open | 2025-03-01 09:00 |
| 2 | u1 | open | 2025-03-01 09:00 |
| 3 | u2 | open | 2025-03-01 10:00 |
| 4 | NULL | open | 2025-03-01 10:05 |
| 5 | u99 | open | 2025-03-01 11:00 |
| 6 | u3 | order | 2025-03-02 09:30 |
| 7 | u3 | order | 2025-03-02 09:30 |
| 8 | u2 | open | 2025-03-02 12:00 |
| 9 | u99 | open | 2025-03-02 12:30 |
| 10 | NULL | order | 2025-03-02 13:00 |
| 11 | u1 | order | 2025-03-02 15:00 |

`accounts`

| user_id | is_test |
|---|---|
| u1 | 0 |
| u2 | 0 |
| u3 | 0 |
| u99 | 1 |

**SQL:**
```sql
-- Step 1: audit. Count the problems before fixing anything.
SELECT COUNT(*) AS total_rows,
       SUM(user_id IS NULL) AS null_user_rows,
       SUM(user_id IN (SELECT user_id FROM accounts WHERE is_test = 1)) AS test_rows,
       (SELECT COUNT(*) FROM events WHERE user_id IS NOT NULL)
       - (SELECT COUNT(*) FROM (SELECT DISTINCT user_id, event_type, event_time
                                FROM events WHERE user_id IS NOT NULL)) AS extra_duplicate_rows
FROM events;
```

**Output:**

| total_rows | null_user_rows | test_rows | extra_duplicate_rows |
|---|---|---|---|
| 11 | 2 | 2 | 2 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
e = events
dist = e[e.user_id.notna()][["user_id", "event_type", "event_time"]].drop_duplicates()
result = pd.DataFrame({
    "total_rows": [len(e)],
    "null_user_rows": [int(e.user_id.isna().sum())],
    "test_rows": [int(e.user_id.isin(accounts[accounts.is_test == 1].user_id).sum())],
    "extra_duplicate_rows": [int(e.user_id.notna().sum()) - len(dist)]})
```
Result (actual run):
```text
 total_rows  null_user_rows  test_rows  extra_duplicate_rows
         11               2          2                     2
```
**SQL:**
```sql
-- Step 2: clean, then count. Duplicate = same user, event type and time.
WITH clean AS (
  SELECT user_id, event_type, event_time
  FROM (SELECT e.*, ROW_NUMBER() OVER (PARTITION BY e.user_id, e.event_type, e.event_time
                                       ORDER BY e.event_id) AS rn
        FROM events e
        WHERE e.user_id IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM accounts a WHERE a.user_id = e.user_id AND a.is_test = 1))
  WHERE rn = 1),
r AS (SELECT date(event_time) AS day, COUNT(*) AS raw_events, COUNT(DISTINCT user_id) AS raw_dau
      FROM events GROUP BY 1),
c AS (SELECT date(event_time) AS day, COUNT(*) AS clean_events, COUNT(DISTINCT user_id) AS clean_dau
      FROM clean GROUP BY 1)
SELECT r.day, r.raw_events, r.raw_dau,
       COALESCE(c.clean_events, 0) AS clean_events, COALESCE(c.clean_dau, 0) AS clean_dau
FROM r LEFT JOIN c ON c.day = r.day ORDER BY r.day;
```

**Output:**

| day | raw_events | raw_dau | clean_events | clean_dau |
|---|---|---|---|---|
| 2025-03-01 | 5 | 3 | 2 | 2 |
| 2025-03-02 | 6 | 4 | 3 | 3 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
e = events.assign(day=events.event_time.str[:10])
raw = e.groupby("day").agg(raw_events=("event_id", "size"), raw_dau=("user_id", "nunique")).reset_index()
tests = set(accounts[accounts.is_test == 1].user_id)
cl = e[e.user_id.notna() & ~e.user_id.isin(tests)].drop_duplicates(["user_id", "event_type", "event_time"])
cln = cl.groupby("day").agg(clean_events=("event_id", "size"), clean_dau=("user_id", "nunique")).reset_index()
result = raw.merge(cln, on="day", how="left").fillna(0)
result[["clean_events", "clean_dau"]] = result[["clean_events", "clean_dau"]].astype(int)
```
Result (actual run):
```text
       day  raw_events  raw_dau  clean_events  clean_dau
2025-03-01           5        3             2          2
2025-03-02           6        4             3          3
```
**Edge cases:** Duplicates do not change `COUNT(DISTINCT user_id)` but they do inflate event counts and sums. Near-duplicates (same event 1 second apart) need a time-bucket rule, so agree on one with the data owner. Other checks to run: events with a future time, events before the user's signup, time zones (UTC versus IST), and users missing from the accounts table. A day that is entirely test traffic would be dropped, so the LEFT JOIN with `COALESCE` keeps it as 0.
**Likely follow-ups:**
- How do you spot test accounts without a flag? Look for email domains of your company, round user ids, or abnormally high event counts, and confirm with the owner.
- Should you delete the bad rows? No: filter in a view or CTE and keep the raw data.
**Common mistakes:** Deleting raw data, using `SELECT DISTINCT *` when `event_id` differs between copies, `NOT IN` with NULLs, and reporting the metric without saying what was excluded.

### Q41 ⭐ 🔴 Handle incomplete cohorts: how do you avoid showing artificially low retention for recent cohorts that have not yet had time to return?
**Asked at:** commonly asked (no company-specific report found). Immature cohorts are a known correctness pitfall in cohort-analysis study material; this is not a confirmed interview report
**What the interviewer is checking:** Whether you notice that recent cohorts have not had time to return, and can exclude or blank those cells instead of reporting a fake low number.
**Say this in the interview:** A cohort is only comparable for month N if month N is fully finished in the data. I add an as-of date, mark cells whose month ends after it as not yet measurable, and show NULL or a blank instead of 0%. I would also compare cohorts only at the same age.
**Explain simply:**
- An **immature cohort** is a group of users who signed up recently, so the follow-up period has not finished. April signups cannot have May activity yet.
- Counting them as 0% retained is wrong: they did not leave, we just have not seen the future. It makes the latest cohort look like a quality drop.
- Fix 1: find the **as-of date** (last day with complete data). A cell for month N counts only if the end of the cohort's month N is on or before it.
- Fix 2: show NULL for those cells, or compare cohorts only at an age they have all reached (for example only month 1 for all cohorts that have one).
- Fix 3 for day-based windows (Day-7, Day-30): only include users who signed up at least N days before the as-of date (see Q39).
**Example:** April's cohort has 2 users, and month 1 would be May, which has not happened. Naive output says 0.0% (looks like a collapse). The fair table shows NULL. March's 50.0% is real because April is complete.
**Sample data:**

`users`

| user_id | signup_date |
|---|---|
| 1 | 2025-01-05 |
| 2 | 2025-01-12 |
| 3 | 2025-01-20 |
| 4 | 2025-01-28 |
| 5 | 2025-02-03 |
| 6 | 2025-02-14 |
| 7 | 2025-02-25 |
| 8 | 2025-03-02 |
| 9 | 2025-03-18 |
| 10 | 2025-04-04 |
| 11 | 2025-04-20 |

`activity`

| user_id | activity_date |
|---|---|
| 1 | 2025-01-06 |
| 1 | 2025-02-10 |
| 1 | 2025-03-12 |
| 2 | 2025-01-15 |
| 2 | 2025-02-20 |
| 3 | 2025-01-21 |
| 4 | 2025-02-02 |
| 4 | 2025-04-03 |
| 5 | 2025-02-05 |
| 5 | 2025-03-08 |
| 5 | 2025-04-09 |
| 6 | 2025-02-20 |
| 6 | 2025-03-21 |
| 7 | 2025-02-26 |
| 8 | 2025-03-05 |
| 8 | 2025-04-11 |
| 9 | 2025-03-20 |
| 10 | 2025-04-06 |
| 11 | 2025-04-21 |

**SQL:**
```sql
-- Data is complete up to and including the as-of date 2025-04-30.
WITH base AS (
  SELECT u.user_id, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', a.activity_date) AS INT) - CAST(strftime('%Y', u.signup_date) AS INT)) * 12
         + CAST(strftime('%m', a.activity_date) AS INT) - CAST(strftime('%m', u.signup_date) AS INT) AS n
  FROM users u JOIN activity a ON a.user_id = u.user_id),
size AS (SELECT strftime('%Y-%m', signup_date) AS cohort_month, COUNT(*) AS cohort_users
         FROM users GROUP BY 1),
m1 AS (SELECT cohort_month, COUNT(DISTINCT user_id) AS retained_m1 FROM base WHERE n = 1 GROUP BY 1)
SELECT s.cohort_month, s.cohort_users, COALESCE(m1.retained_m1, 0) AS retained_m1,
       ROUND(100.0 * COALESCE(m1.retained_m1, 0) / s.cohort_users, 1) AS naive_pct,
       -- month 1 is complete only if the END of that month is on or before the as-of date
       CASE WHEN date(s.cohort_month || '-01', '+2 months', '-1 day') <= '2025-04-30'
            THEN ROUND(100.0 * COALESCE(m1.retained_m1, 0) / s.cohort_users, 1) END AS fair_pct
FROM size s LEFT JOIN m1 ON m1.cohort_month = s.cohort_month
ORDER BY s.cohort_month;
```

**Output:**

| cohort_month | cohort_users | retained_m1 | naive_pct | fair_pct |
|---|---|---|---|---|
| 2025-01 | 4 | 3 | 75.0 | 75.0 |
| 2025-02 | 3 | 2 | 66.7 | 66.7 |
| 2025-03 | 2 | 1 | 50.0 | 50.0 |
| 2025-04 | 2 | 0 | 0.0 | NULL |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
u = users.assign(sd=pd.to_datetime(users.signup_date))
u["cohort_month"] = u.sd.dt.strftime("%Y-%m")
b = activity.merge(u, on="user_id")
ad = pd.to_datetime(b.activity_date)
b["n"] = (ad.dt.year - b.sd.dt.year) * 12 + ad.dt.month - b.sd.dt.month
size = u.groupby("cohort_month").size().rename("cohort_users")
m1 = b[b.n == 1].groupby("cohort_month").user_id.nunique().rename("retained_m1")
result = pd.concat([size, m1], axis=1).fillna(0).astype({"retained_m1": int}).reset_index()
result["naive_pct"] = (result.retained_m1 / result.cohort_users * 100).round(1)
month_end_m1 = pd.to_datetime(result.cohort_month + "-01") + pd.DateOffset(months=2) - pd.Timedelta(days=1)
result["fair_pct"] = result.naive_pct.where(month_end_m1 <= pd.Timestamp("2025-04-30"))
```
Result (actual run):
```text
cohort_month  cohort_users  retained_m1  naive_pct  fair_pct
     2025-01             4            3       75.0      75.0
     2025-02             3            2       66.7      66.7
     2025-03             2            1       50.0      50.0
     2025-04             2            0        0.0       NaN
```
**Edge cases:** If the last month in the data is partial (data loaded up to the 15th), treat it as incomplete: pick the as-of date carefully. A cohort that is only partly mature (signup mid-month, window of 30 days) needs a day-level rule. NULL must stay NULL in charts and averages; never average NULL as 0. A cohort of size 2 is statistically meaningless, so also show cohort_users.
**Likely follow-ups:**
- How do you pick the as-of date? The latest date for which your pipeline finished loading; not 'today'.
- What about averaging retention across cohorts? Average only mature cells, ideally weighted by cohort size.
**Common mistakes:** Treating missing future data as zero, using the system date instead of the data's own last complete date, comparing a young cohort with an old one at different ages, and hiding the cohort size.

### Q42 ⭐ 🔴 Calculate net revenue retention (NRR): revenue this month from customers who existed last month, divided by their revenue last month.
**Asked at:** commonly asked (no company-specific report found); listed as a common product-analytics SQL pattern on study sites (research/Book02_Part09_sources.md)
**What the interviewer is checking:** Whether you restrict this month's revenue to customers who existed last month, so new customers do not inflate the number.
**Say this in the interview:** I start from last month's customers, LEFT JOIN their revenue this month, add it up, and divide by last month's revenue. New customers are left out by construction; churned customers count as zero.
**Explain simply:**
- **NRR (net revenue retention)** = revenue this month from last month's customers / those customers' revenue last month. Above 100% means growth from existing customers alone.
- It includes **expansion** (customer pays more), **contraction** (pays less) and **churn** (pays nothing). It excludes brand-new customers.
- The LEFT JOIN from last month to this month matters: a churned customer has no row this month and must count as 0, not disappear.
- **GRR (gross revenue retention)** is the stricter cousin: cap each customer at last month's amount, so expansion cannot hide churn (standard definition, from memory).
**Example:** Customers are client companies of an HR software product. January total is 450. In February the same clients pay 320 (A grew, B shrank, C left), so NRR = 71.1%. New client E (80) is ignored. GRR is 66.7%.
**Sample data:**

`monthly_revenue`

| customer_id | month | revenue |
|---|---|---|
| A | 2025-01 | 100 |
| A | 2025-02 | 120 |
| A | 2025-03 | 150 |
| B | 2025-01 | 200 |
| B | 2025-02 | 150 |
| B | 2025-03 | 150 |
| C | 2025-01 | 100 |
| D | 2025-01 | 50 |
| D | 2025-02 | 50 |
| E | 2025-02 | 80 |
| E | 2025-03 | 90 |
| F | 2025-03 | 60 |

**SQL:**
```sql
WITH p AS (
  SELECT customer_id, revenue,
         strftime('%Y-%m', month || '-01', '+1 month') AS next_month   -- month after this row's month
  FROM monthly_revenue)
SELECT p.next_month AS month,
       SUM(p.revenue) AS prev_revenue,
       COALESCE(SUM(c.revenue), 0) AS revenue_from_same_customers,
       ROUND(100.0 * COALESCE(SUM(c.revenue), 0) / SUM(p.revenue), 1) AS nrr_pct,
       ROUND(100.0 * SUM(MIN(p.revenue, COALESCE(c.revenue, 0))) / SUM(p.revenue), 1) AS grr_pct
FROM p
LEFT JOIN monthly_revenue c ON c.customer_id = p.customer_id AND c.month = p.next_month
WHERE p.next_month <= (SELECT MAX(month) FROM monthly_revenue)
GROUP BY p.next_month
ORDER BY p.next_month;
```

**Output:**

| month | prev_revenue | revenue_from_same_customers | nrr_pct | grr_pct |
|---|---|---|---|---|
| 2025-02 | 450 | 320 | 71.1 | 66.7 |
| 2025-03 | 400 | 390 | 97.5 | 87.5 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
mr = monthly_revenue
p = mr.assign(next_month=(pd.to_datetime(mr.month + "-01") + pd.DateOffset(months=1)).dt.strftime("%Y-%m"))
p = p[p.next_month <= mr.month.max()]
m = p.merge(mr.rename(columns={"month": "next_month", "revenue": "cur"}), on=["customer_id", "next_month"], how="left")
m["cur"] = m.cur.fillna(0)
m["capped"] = np.minimum(m.revenue, m.cur)
g = m.groupby("next_month").agg(prev_revenue=("revenue", "sum"), revenue_from_same_customers=("cur", "sum"), cap=("capped", "sum")).reset_index()
g["nrr_pct"] = (g.revenue_from_same_customers / g.prev_revenue * 100).round(1)
g["grr_pct"] = (g.cap / g.prev_revenue * 100).round(1)
result = g.rename(columns={"next_month": "month"})[["month", "prev_revenue", "revenue_from_same_customers", "nrr_pct", "grr_pct"]]
```
Result (actual run):
```text
  month  prev_revenue  revenue_from_same_customers  nrr_pct  grr_pct
2025-02           450                        320.0     71.1     66.7
2025-03           400                        390.0     97.5     87.5
```
**Edge cases:** A customer who skips a month and returns is treated as churned that month and 'new' on return (they are excluded the next time). Months with no previous month give no row, since `next_month` must exist in the data. Customers with 0 revenue rows in the prior month do not enter the base. If revenue can be negative (credits), say how you treat it. Divide-by-zero cannot occur because the base is a sum over existing customers, but guard with `NULLIF` if zero revenue rows exist.
**Likely follow-ups:**
- What is a healthy NRR? Above 100% is generally seen as good for subscription businesses; the exact benchmark depends on the industry (not sourced here).
- How do you split NRR into parts? Sum positive differences (expansion), negative differences (contraction) and churned amounts separately.
**Common mistakes:** Dividing this month's total revenue by last month's total (that includes new customers, so it is plain growth, not NRR), using an INNER JOIN so churned customers vanish, and mixing up NRR and GRR.

### Q43 ⭐ 🔴 Given a subscriptions table (user_id, start_date, end_date), count active subscribers at the end of each month, including months with no events (generated calendar).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can generate a calendar (recursive CTE) and join a date-range table to it so quiet months still appear.
**Say this in the interview:** I generate one row per month end with a recursive CTE, then LEFT JOIN subscriptions where the start is on or before that date and the end is empty or on or after it. COUNT of the joined users gives the snapshot.
**Explain simply:**
- A **snapshot** counts who is active at one moment (the last day of the month), unlike counting events that happened during the month.
- A **recursive CTE** starts with one row (January) and keeps adding the next month until a stop condition. It is how you make a calendar when the database has no `generate_series`.
- If you group the subscriptions table alone, a month with no starts or ends is missing. The calendar plus LEFT JOIN guarantees one row per month.
- Decide what `end_date` means. Here it is the last day of access, so a subscription ending on 30 April is still active at month end.
**Example:** June has no sign-ups or cancellations at all, yet it still shows 2 active subscribers (users 1 and 6). An event-only query would leave June out.
**Sample data:**

`subscriptions`

| user_id | start_date | end_date |
|---|---|---|
| 1 | 2025-01-10 | NULL |
| 2 | 2025-01-20 | 2025-02-15 |
| 3 | 2025-02-05 | 2025-04-30 |
| 4 | 2025-02-25 | 2025-02-28 |
| 5 | 2025-04-02 | 2025-04-20 |
| 6 | 2025-05-03 | NULL |

**SQL:**
```sql
WITH RECURSIVE months(month_start) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(month_start, '+1 month') FROM months WHERE month_start < '2025-06-01'),
cal AS (SELECT month_start, date(month_start, '+1 month', '-1 day') AS month_end FROM months)
SELECT strftime('%Y-%m', c.month_end) AS month, c.month_end,
       COUNT(s.user_id) AS active_subscribers
FROM cal c
LEFT JOIN subscriptions s
  ON s.start_date <= c.month_end
 AND (s.end_date IS NULL OR s.end_date >= c.month_end)   -- end_date = last day of access
GROUP BY c.month_end
ORDER BY c.month_end;
```

Alternatives (not run here / from memory): PostgreSQL builds the calendar with `generate_series('2025-01-01'::date, '2025-06-01', interval '1 month')`; MySQL 8 and SQL Server use a recursive CTE like the one above (SQL Server writes `WITH months AS (...)` without the word RECURSIVE and uses `EOMONTH()` for month end).

**Output:**

| month | month_end | active_subscribers |
|---|---|---|
| 2025-01 | 2025-01-31 | 2 |
| 2025-02 | 2025-02-28 | 3 |
| 2025-03 | 2025-03-31 | 2 |
| 2025-04 | 2025-04-30 | 2 |
| 2025-05 | 2025-05-31 | 2 |
| 2025-06 | 2025-06-30 | 2 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
ends = pd.date_range("2025-01-31", "2025-06-30", freq="ME")
sd = pd.to_datetime(subscriptions.start_date)
ed = pd.to_datetime(subscriptions.end_date)
rows = []
for me in ends:
    n = int(((sd <= me) & (ed.isna() | (ed >= me))).sum())
    rows.append((me.strftime("%Y-%m"), me.strftime("%Y-%m-%d"), n))
result = pd.DataFrame(rows, columns=["month", "month_end", "active_subscribers"])
```
Result (actual run):
```text
  month  month_end  active_subscribers
2025-01 2025-01-31                   2
2025-02 2025-02-28                   3
2025-03 2025-03-31                   2
2025-04 2025-04-30                   2
2025-05 2025-05-31                   2
2025-06 2025-06-30                   2
```
**Edge cases:** NULL end_date means still subscribed, so it needs the explicit `IS NULL` branch. A subscription that starts and ends within one month (user 5) is never counted at a month end, which is correct for a snapshot. The recursive stop condition must exist, or it loops forever. `COUNT(s.user_id)` returns 0 for empty months, while `COUNT(*)` would wrongly return 1. Re-subscribers have several rows; use `COUNT(DISTINCT s.user_id)` if ranges can overlap.
**Likely follow-ups:**
- How would you count at the start of the month instead? Use the day before the first day, or the first day with the same rule.
- Why not use `GROUP BY month` on the table? It misses months without events.
**Common mistakes:** Using `COUNT(*)` after a LEFT JOIN (an empty month shows 1), forgetting the NULL end date, off-by-one on inclusive or exclusive end dates, and a recursive CTE with no stop condition.

### Q44 ⭐ 🔴 Find peak concurrent users: given session start and end times, find the time with the most overlapping sessions.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the sweep-line trick (+1 at start, -1 at end, running total) and handle ties at the boundary.
**Say this in the interview:** I turn each session into two events, plus one at the start and minus one at the end, sort them by time, take a running sum, and the highest running sum is the peak. Ends sort before starts at the same time so back-to-back sessions do not overlap.
**Explain simply:**
- **Concurrent users** = sessions that are open at the same moment.
- Each session gives two events. The running total after each event is the number of open sessions at that time.
- **Boundary rule**: a session ending at 10:30 and another starting at 10:30 are not overlapping here. Sorting `delta` ascending puts -1 before +1. Say your rule out loud; a different business rule is possible.
- `LEAD(t)` gives the time the peak lasts until (the next event).
**Example:** Sessions s1 (10:00-10:30), s2 (10:10-10:40) and s3 (10:20-10:25) all overlap between 10:20 and 10:25, so peak = 3. s4 starts at 10:30 exactly when s1 ends, so it does not push the count to 4.
**Sample data:**

`sessions`

| session_id | start_time | end_time |
|---|---|---|
| s1 | 2025-03-01 10:00 | 2025-03-01 10:30 |
| s2 | 2025-03-01 10:10 | 2025-03-01 10:40 |
| s3 | 2025-03-01 10:20 | 2025-03-01 10:25 |
| s4 | 2025-03-01 10:30 | 2025-03-01 10:50 |
| s5 | 2025-03-01 10:45 | 2025-03-01 11:00 |
| s6 | 2025-03-01 11:00 | 2025-03-01 11:20 |
| s7 | 2025-03-01 09:50 | 2025-03-01 10:05 |

**SQL:**
```sql
WITH ev AS (
  SELECT start_time AS t, 1 AS delta FROM sessions
  UNION ALL
  SELECT end_time, -1 FROM sessions),
run AS (
  SELECT t, SUM(delta) OVER (ORDER BY t, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent,
         LEAD(t) OVER (ORDER BY t, delta) AS next_t
  FROM ev)                     -- -1 sorts before +1, so an end at 10:30 frees the seat before a start at 10:30
SELECT t AS peak_from, next_t AS peak_until, concurrent
FROM run
WHERE concurrent = (SELECT MAX(concurrent) FROM run);
```

**Output:**

| peak_from | peak_until | concurrent |
|---|---|---|
| 2025-03-01 10:20 | 2025-03-01 10:25 | 3 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
ev = pd.concat([sessions[["start_time"]].rename(columns={"start_time": "t"}).assign(delta=1),
                sessions[["end_time"]].rename(columns={"end_time": "t"}).assign(delta=-1)])
ev = ev.sort_values(["t", "delta"]).reset_index(drop=True)
ev["concurrent"] = ev.delta.cumsum()
ev["next_t"] = ev.t.shift(-1)
top = ev[ev.concurrent == ev.concurrent.max()]
result = top.rename(columns={"t": "peak_from", "next_t": "peak_until"})[["peak_from", "peak_until", "concurrent"]].reset_index(drop=True)
```
Result (actual run):
```text
       peak_from       peak_until  concurrent
2025-03-01 10:20 2025-03-01 10:25           3
```
**SQL:** (check, same answer)
```sql
-- Check (slower, O(n^2)): peak always happens at some session's start time
SELECT s.start_time AS peak_from, COUNT(*) AS concurrent
FROM sessions s
JOIN sessions o ON o.start_time <= s.start_time AND o.end_time > s.start_time
GROUP BY s.session_id
ORDER BY concurrent DESC, peak_from
LIMIT 1;
```

**Output:**

| peak_from | concurrent |
|---|---|
| 2025-03-01 10:20 | 3 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
j = sessions.merge(sessions, how="cross", suffixes=("", "_o"))
j = j[(j.start_time_o <= j.start_time) & (j.end_time_o > j.start_time)]
c = j.groupby(["session_id", "start_time"]).size().rename("concurrent").reset_index()
result = c.sort_values(["concurrent", "start_time"], ascending=[False, True]).head(1).rename(columns={"start_time": "peak_from"})[["peak_from", "concurrent"]].reset_index(drop=True)
```
Result (actual run):
```text
       peak_from  concurrent
2025-03-01 10:20           3
```
**Edge cases:** If several periods tie for the maximum, all appear (one row per period). Sessions with NULL end time (still open) need `COALESCE(end_time, 'as-of time')` first. Zero-length sessions cancel themselves out. Text timestamps in `YYYY-MM-DD HH:MM` sort correctly; real DATETIME columns behave the same. The self-join check scales badly because it compares every pair, so use it only for small data.
**Likely follow-ups:**
- Peak per day? Add `date(t)` to the PARTITION BY / ORDER BY of the window (and reset the sum each day).
- Why not just GROUP BY hour? A session that spans several hours would be counted in only one bucket, or double-counted, depending on what you pick.
**Common mistakes:** Counting session starts only (ignores sessions that ended), sorting +1 before -1 at equal times (overstates the peak), and using `RANGE` default frame with ties, which jumps the running sum for all tied rows at once.

### Q45 ⭐ 🔴 Find customers whose monthly spend increased every month for at least 3 months in a row.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can combine monthly aggregation, LAG, and the gaps-and-islands running-sum trick, including the calendar-adjacent check.
**Say this in the interview:** I total spend per customer per month, flag each month that is higher than the directly previous month, and start a new group every time the flag is 0. A group with at least three 'up' months is a streak.
**Explain simply:**
- **Premise note:** 'increased every month for at least 3 months' is ambiguous. I read it as 3 increases in a row (4 months of data, each higher than the one before). For 3 months with 2 increases, change `>= 3` to `>= 2`.
- First **aggregate to months**: a customer can place many orders in a month (C5 has two in January).
- `LAG(spend)` gives last row's spend. A month counts as 'up' only if it is higher AND the previous row is exactly the previous calendar month (`mi = LAG(mi) + 1`). Otherwise a missing month would join two separate runs.
- **Gaps and islands**: `SUM(1 - is_up)` as a running total goes up by 1 at every non-up month, so all months of one streak share the same group number.
**Example:** C1 spends 100, 150, 200, 260 from January to April (3 increases) then 240 in May (down). C3 rose 50, 60, 70, skipped April, then 80 in May, so only 2 increases and no streak. C2 dips in March, so its best run is 2 increases.
**Sample data:**

`orders`

| customer_id | order_date | amount |
|---|---|---|
| C1 | 2025-01-05 | 100 |
| C1 | 2025-02-05 | 150 |
| C1 | 2025-03-05 | 200 |
| C1 | 2025-04-05 | 260 |
| C1 | 2025-05-05 | 240 |
| C2 | 2025-01-05 | 100 |
| C2 | 2025-02-05 | 120 |
| C2 | 2025-03-05 | 110 |
| C2 | 2025-04-05 | 130 |
| C2 | 2025-05-05 | 150 |
| C3 | 2025-01-05 | 50 |
| C3 | 2025-02-05 | 60 |
| C3 | 2025-03-05 | 70 |
| C3 | 2025-05-05 | 80 |
| C4 | 2025-02-05 | 100 |
| C4 | 2025-03-05 | 110 |
| C4 | 2025-04-05 | 120 |
| C4 | 2025-05-05 | 130 |
| C4 | 2025-06-05 | 140 |
| C5 | 2025-01-05 | 40 |
| C5 | 2025-01-10 | 40 |
| C5 | 2025-02-05 | 100 |
| C5 | 2025-03-05 | 90 |
| C5 | 2025-03-10 | 30 |
| C5 | 2025-04-05 | 130 |

**SQL:**
```sql
WITH m AS (                      -- one row per customer per month
  SELECT customer_id, strftime('%Y-%m', order_date) AS month,
         CAST(strftime('%Y', order_date) AS INT) * 12 + CAST(strftime('%m', order_date) AS INT) AS mi,
         SUM(amount) AS spend
  FROM orders GROUP BY customer_id, month),
f AS (                           -- is this month higher than the directly previous month?
  SELECT *, CASE WHEN spend > LAG(spend) OVER w AND mi = LAG(mi) OVER w + 1 THEN 1 ELSE 0 END AS is_up
  FROM m WINDOW w AS (PARTITION BY customer_id ORDER BY mi)),
g AS (SELECT *, SUM(1 - is_up) OVER (PARTITION BY customer_id ORDER BY mi) AS grp FROM f)
SELECT customer_id, MIN(month) AS streak_from, MAX(month) AS streak_to, SUM(is_up) AS increases
FROM g
GROUP BY customer_id, grp
HAVING SUM(is_up) >= 3
ORDER BY customer_id, streak_from;
```

**Output:**

| customer_id | streak_from | streak_to | increases |
|---|---|---|---|
| C1 | 2025-01 | 2025-04 | 3 |
| C4 | 2025-02 | 2025-06 | 4 |
| C5 | 2025-01 | 2025-04 | 3 |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
o = orders.assign(month=orders.order_date.str[:7])
m = o.groupby(["customer_id", "month"], as_index=False).amount.sum().rename(columns={"amount": "spend"})
m["mi"] = m.month.str[:4].astype(int) * 12 + m.month.str[5:7].astype(int)
m = m.sort_values(["customer_id", "mi"]).reset_index(drop=True)
gb = m.groupby("customer_id")
m["is_up"] = ((m.spend > gb.spend.shift()) & (m.mi == gb.mi.shift() + 1)).astype(int)
m["grp"] = (1 - m.is_up).groupby(m.customer_id).cumsum()
g = m.groupby(["customer_id", "grp"]).agg(streak_from=("month", "min"), streak_to=("month", "max"), increases=("is_up", "sum")).reset_index()
result = g[g.increases >= 3].drop(columns="grp").sort_values(["customer_id", "streak_from"]).reset_index(drop=True)
```
Result (actual run):
```text
customer_id streak_from streak_to  increases
         C1     2025-01   2025-04          3
         C4     2025-02   2025-06          4
         C5     2025-01   2025-04          3
```
**Edge cases:** Equal spend is not an increase (`>` is strict). A customer's first month has no LAG (NULL), so it is flagged 0 and begins the group. Customer with a single order month never qualifies. Ties are not an issue. Months with zero orders are missing rows, not zeros; the `mi` check treats them as a break. A customer can have several streaks, and each shows as a row.
**Likely follow-ups:**
- How do you get only the longest streak per customer? Rank the streaks by `increases` desc and keep rank 1.
- Is there a version that treats a missing month as zero spend? Join to a customer-by-month calendar first (see Q43), then use the same logic.
**Common mistakes:** Not aggregating to month first, ignoring missing months, using `>=` instead of `>` for 'increased', and off-by-one on streak length (3 increases = 4 months).

### Q46 ⭐ 🔴 Find the largest gap (in days) between two consecutive visits for each user, and flag users with a gap above 30 days.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can use LAG to measure the gap to the previous visit and then take MAX per user, handling single-visit users and duplicate days.
**Say this in the interview:** I de-duplicate visits to one per day, use LAG to get each user's previous visit date, subtract to get the gap in days, take the maximum gap per user, and flag it if it is above 30.
**Explain simply:**
- `LAG(visit_date) OVER (PARTITION BY user_id ORDER BY visit_date)` looks at the previous visit of the same user.
- **Gap** = this visit date minus the previous visit date, in days. In SQLite use `julianday()`.
- `MAX(gap)` per user gives the biggest silence. `CASE WHEN ... > 30` turns it into a Yes/No flag.
- Strictly more than 30: a 30-day gap is not flagged (user u4).
**Example:** User u2 visited on 2 Jan and then 20 Feb: a 49-day gap, flagged Yes. User u1's biggest gap is 15 days: No. In HR terms: the longest stretch between an employee's badge swipes.
**Sample data:**

`visits`

| user_id | visit_date |
|---|---|
| u1 | 2025-01-01 |
| u1 | 2025-01-05 |
| u1 | 2025-01-20 |
| u2 | 2025-01-02 |
| u2 | 2025-02-20 |
| u2 | 2025-02-25 |
| u3 | 2025-01-10 |
| u4 | 2025-01-03 |
| u4 | 2025-01-03 |
| u4 | 2025-02-02 |
| u5 | 2025-01-01 |
| u5 | 2025-02-05 |
| u5 | 2025-03-10 |

**SQL:**
```sql
WITH v AS (SELECT DISTINCT user_id, visit_date FROM visits),      -- one row per user per day
g AS (
  SELECT user_id,
         CAST(ROUND(julianday(visit_date)
              - julianday(LAG(visit_date) OVER (PARTITION BY user_id ORDER BY visit_date))) AS INT) AS gap
  FROM v)
SELECT user_id,
       MAX(gap) AS max_gap_days,
       CASE WHEN MAX(gap) > 30 THEN 'Yes' ELSE 'No' END AS gap_over_30
FROM g
GROUP BY user_id
ORDER BY user_id;
```

Dialect notes (not run here / from memory): the day difference is `DATEDIFF(day, prev, cur)` in SQL Server, `DATEDIFF(cur, prev)` in MySQL, and `cur - prev` (dates subtract to an integer) in PostgreSQL.

**Output:**

| user_id | max_gap_days | gap_over_30 |
|---|---|---|
| u1 | 15 | No |
| u2 | 49 | Yes |
| u3 | NULL | No |
| u4 | 30 | No |
| u5 | 35 | Yes |

**pandas equivalent:**
```python
# DataFrames named like the tables hold the same data
v = visits.drop_duplicates().copy()
v["d"] = pd.to_datetime(v.visit_date)
v = v.sort_values(["user_id", "d"])
v["gap"] = v.groupby("user_id").d.diff().dt.days
r = v.groupby("user_id").gap.max().astype("Int64").rename("max_gap_days").reset_index()
r["gap_over_30"] = (r.max_gap_days > 30).fillna(False).map({True: "Yes", False: "No"})
result = r
```
Result (actual run):
```text
user_id  max_gap_days gap_over_30
     u1            15          No
     u2            49         Yes
     u3          <NA>          No
     u4            30          No
     u5            35         Yes
```
**Edge cases:** A user with one visit (u3) has no gap: NULL, and `NULL > 30` is not true so the CASE falls to 'No'. Say 'No data' if you want to show that. Duplicate visits on the same day would create a 0-day gap, hence `DISTINCT`. The gap since the last visit to today is not in this query: add it with a UNION against an as-of date if the business wants it. Ties are irrelevant.
**Likely follow-ups:**
- How do you get the gap's start and end dates? Keep `visit_date` and the previous date in the CTE and pick the row where `gap = MAX(gap)` (use `ROW_NUMBER` ordered by gap desc).
- How would you include the gap up to today? Add an extra row per user for the as-of date before applying LAG.
**Common mistakes:** Forgetting `PARTITION BY user_id` (compares different users), using `COUNT` instead of date subtraction, not de-duplicating same-day visits, and treating NULL (single visit) as a large gap.

