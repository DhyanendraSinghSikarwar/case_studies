### Q13 ⭐⭐⭐ 🟡 Rising Temperature (LeetCode 197 style) with LAG: weather(id, record_date, temperature). Return the dates on which the temperature was higher than on the previous calendar day. Show the LAG version, then explain why LAG compares the previous row and not the previous day, so a missing date gives a wrong answer unless you also check julianday(record_date) - julianday(prev_date) = 1, and give the self-join alternative and the pandas shift and diff version.
**Asked at:** public LeetCode-style problem bank (1321 Restaurant Growth statement seen in a search snippet; 1308 Running Total for Different Genders, 197 Rising Temperature and 180 Consecutive Numbers known only by title from third-party lists), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** `LAG` looks at the previous row in the sort order, not the previous calendar day, so I compare `temperature > prev_temp` and also check `julianday(record_date) - julianday(prev_date) = 1`; without the second test a missing date compares a day with the one before the gap.

**Schema and sample data:** nine days of readings, inserted with ids that do not follow date order. 2024-01-05 has no row, 2024-01-09 has a NULL temperature.
```sql
CREATE TABLE weather(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO weather VALUES (1,'2024-01-02',25),(2,'2024-01-01',10),(3,'2024-01-04',30),
  (4,'2024-01-03',20),(5,'2024-01-06',35),(6,'2024-01-07',35),(7,'2024-01-08',40),
  (8,'2024-01-09',NULL),(9,'2024-01-10',50);
```

**SQL answer:** LAG with the gap check (`SQL_MAIN`), the naive LAG without it, and the self-join alternative. Tie rule: `ORDER BY record_date, id`.
```sql
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp,
         LAG(record_date) OVER (ORDER BY record_date, id) AS prev_date
  FROM weather
)
SELECT record_date
FROM x
WHERE temperature > prev_temp
  AND julianday(record_date) - julianday(prev_date) = 1
ORDER BY record_date
```
```sql
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp
  FROM weather
)
SELECT record_date FROM x WHERE temperature > prev_temp ORDER BY record_date
```
```sql
SELECT t.record_date
FROM weather t
JOIN weather p ON p.record_date = date(t.record_date, '-1 day')
WHERE t.temperature > p.temperature
ORDER BY t.record_date
```

**pandas answer:** sort, then compare with `shift()` for the value and `diff()` for the date gap.
```py
w = weather.assign(record_date=pd.to_datetime(weather["record_date"])).sort_values(["record_date", "id"])
prev_temp = w["temperature"].shift()
gap_days = w["record_date"].diff()
pd_df = w.loc[(w["temperature"] > prev_temp) & (gap_days == pd.Timedelta(days=1)), ["record_date"]]
```

**Example:** sorted by date: 01-01=10, 01-02=25, 01-03=20, 01-04=30, 01-06=35, 01-07=35, 01-08=40, 01-09=NULL, 01-10=50.
- 01-02: 25 > 10 and the gap is 1 day, so it counts.
- 01-03: 20 < 25, no. 01-04: 30 > 20 and gap 1, yes.
- 01-06: 35 > 30, but the previous row is 01-04 (gap 2 days), so the gap check rejects it. The naive LAG query keeps it, which is the wrong row.
- 01-07: 35 = 35, not higher. 01-08: 40 > 35, gap 1, yes.
- 01-09: NULL is never greater than anything. 01-10: previous temperature is NULL, so `50 > NULL` is unknown and it is dropped.
- Result: 01-02, 01-04, 01-08.

**Code:** run with `python3 -I`.
```python
# Q13: Rising Temperature with LAG, gap check, self-join, pandas shift/diff
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE weather(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO weather VALUES (1,'2024-01-02',25),(2,'2024-01-01',10),(3,'2024-01-04',30),
  (4,'2024-01-03',20),(5,'2024-01-06',35),(6,'2024-01-07',35),(7,'2024-01-08',40),
  (8,'2024-01-09',NULL),(9,'2024-01-10',50);
"""
SQL_MAIN = """
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp,
         LAG(record_date) OVER (ORDER BY record_date, id) AS prev_date
  FROM weather
)
SELECT record_date
FROM x
WHERE temperature > prev_temp
  AND julianday(record_date) - julianday(prev_date) = 1
ORDER BY record_date
"""
SQL_NAIVE = """
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp
  FROM weather
)
SELECT record_date FROM x WHERE temperature > prev_temp ORDER BY record_date
"""
SQL_JOIN = """
SELECT t.record_date
FROM weather t
JOIN weather p ON p.record_date = date(t.record_date, '-1 day')
WHERE t.temperature > p.temperature
ORDER BY t.record_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
naive = [r[0] for r in con.execute(SQL_NAIVE)]
join = [r[0] for r in con.execute(SQL_JOIN)]
print("LAG with gap check:", sql_df["record_date"].tolist())
print("naive LAG (no gap check):", naive)
print("self-join:", join)
assert join == sql_df["record_date"].tolist()

weather = pd.read_sql_query("SELECT * FROM weather", con)
# pd:main
w = weather.assign(record_date=pd.to_datetime(weather["record_date"])).sort_values(["record_date", "id"])
prev_temp = w["temperature"].shift()
gap_days = w["record_date"].diff()
pd_df = w.loc[(w["temperature"] > prev_temp) & (gap_days == pd.Timedelta(days=1)), ["record_date"]]
# pd:end
pd_dates = pd_df["record_date"].dt.strftime("%Y-%m-%d").tolist()
# compared after sorting by record_date
assert pd_dates == sql_df["record_date"].tolist()
print("pandas shift + diff:", pd_dates)

# calendar-correct alternative: shift(freq='D') moves the index, not the data
s = w.set_index("record_date")["temperature"]
prev_day = s.shift(freq="D").reindex(s.index)
alt = s[s > prev_day]
print("pandas shift(freq='D'):", alt.index.strftime("%Y-%m-%d").tolist())
assert alt.index.strftime("%Y-%m-%d").tolist() == pd_dates

# duplicate dates: the question is ill-defined; the gap check at least rejects the pair itself
con.executescript("""
CREATE TABLE wdup(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO wdup VALUES (1,'2024-01-01',10),(2,'2024-01-02',20),(3,'2024-01-02',30),(4,'2024-01-03',40);
""")
dup_sql = SQL_MAIN.replace("FROM weather", "FROM wdup")
print("duplicate date 01-02 (ids 2,3):", [r[0] for r in con.execute(dup_sql)])
print("asserts passed: LAG+gap == self-join == pandas shift/diff == shift(freq='D')")
```

**Output (my run):**
```text
LAG with gap check: ['2024-01-02', '2024-01-04', '2024-01-08']
naive LAG (no gap check): ['2024-01-02', '2024-01-04', '2024-01-06', '2024-01-08']
self-join: ['2024-01-02', '2024-01-04', '2024-01-08']
pandas shift + diff: ['2024-01-02', '2024-01-04', '2024-01-08']
pandas shift(freq='D'): ['2024-01-02', '2024-01-04', '2024-01-08']
duplicate date 01-02 (ids 2,3): ['2024-01-02', '2024-01-03']
asserts passed: LAG+gap == self-join == pandas shift/diff == shift(freq='D')
```

**Edge cases:**
- Missing date: the naive query returned 01-06 as well (four dates instead of three); the gap check, the self-join and pandas all returned three.
- NULL temperature: the comparison is unknown, so the row is dropped, and the row after it is dropped too because its previous value is NULL. If the business wants to skip over NULL days, that is a different question.
- Duplicate dates: the problem assumes one row per date. I tested a table with two rows on 01-02 (ids 2 and 3): with the tie rule `id`, the second copy has a 0-day gap so it is rejected, but the next day then compares only with the higher-id copy and 01-03 was returned. Fix the data (aggregate to one row per date) before trusting the answer.
- Order: the ids are not in date order in my sample, so `ORDER BY id` would give wrong answers; the window must order by `record_date`.
- Dates stored as text must be ISO `YYYY-MM-DD`; otherwise `julianday` returns NULL and the gap check silently drops every row.

**Then explain:**
- `LAG(x)` is positional. It does not know about the calendar, so a gap makes "previous row" and "previous day" different things.
- Self-join: join each row to the row dated exactly one day before (`p.record_date = date(t.record_date, '-1 day')`). A missing day has no partner row, so it drops out by itself; it needs no gap test. The cost is a second scan (an index on `record_date` helps; I did not time it).
- pandas: `shift()` is also positional and `diff()` on a datetime column gives a `Timedelta`, so compare with `pd.Timedelta(days=1)`. `shift(freq="D")` is calendar-based: it moves the index labels by one day instead of moving the data, so `s.shift(freq="D").reindex(s.index)` is NaN where the previous day is missing. It returned the same three dates, but it needs a unique index (reindex raises on duplicate labels, from the documented behaviour; I did not test the error).
- Dialects (not executed here): PostgreSQL can subtract DATE values directly (`record_date - prev_date = 1`), MySQL uses `DATEDIFF(record_date, prev_date) = 1`, BigQuery uses `DATE_DIFF`. As I remember the LeetCode problem it is written for MySQL, so check the platform's dialect.

**Follow-ups:**
- *Temperature lower than the previous day?* Flip the comparison; same gap check.
- *Compare with the day before, whatever the row distance?* The self-join or `shift(freq='D')` form.
- *What if a date can repeat?* Aggregate first (`MAX` or `AVG` per date), then apply the logic.

**Common mistakes:**
- Using LAG alone and trusting it across a missing date.
- Ordering the window by `id` instead of by date.
- Comparing `julianday` differences with the wrong sign or against text dates in a non-ISO format.
- In pandas, forgetting to sort before `shift()` or `diff()`.

### Q14 ⭐⭐⭐ 🟡 Time since the previous order per customer: orders(order_id, customer_id, order_ts) with ISO timestamps text. Return each order with the number of days since the same customer's previous order (NULL for the first order) using LAG and julianday arithmetic, then the average gap per customer. Explain NULL for first orders, ties on order_ts, and give the pandas groupby().diff() version with pd.to_datetime and dt.total_seconds.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Partition by customer, order by timestamp with the order id as a tie-breaker, and subtract `julianday(LAG(order_ts))` from `julianday(order_ts)`; the first order of each customer has no previous row so the gap is NULL, and `AVG` of the gaps ignores those NULLs.

**Schema and sample data:** eight orders for three customers plus one customer (D) with a single order. Orders 2 and 3 for customer A have exactly the same timestamp. Rows for B and C are interleaved in id order, so the table is not stored grouped by customer.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
  (1,'A','2024-01-01 09:00:00'),(2,'A','2024-01-03 21:00:00'),(3,'A','2024-01-03 21:00:00'),
  (4,'A','2024-01-10 09:00:00'),(5,'B','2024-02-01 12:00:00'),(6,'C','2024-02-05 08:00:00'),
  (7,'C','2024-02-05 20:00:00'),(8,'B','2024-02-11 12:00:00'),(9,'D','2024-03-01 00:00:00');
```

**SQL answer:** per-order gap (`SQL_MAIN`) and average gap per customer (`SQL_AVG`).
```sql
WITH g AS (
  SELECT order_id, customer_id, order_ts,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS days_since_prev
  FROM orders
)
SELECT order_id, customer_id, order_ts, ROUND(days_since_prev, 4) AS days_since_prev
FROM g
ORDER BY customer_id, order_ts, order_id
```
```sql
WITH g AS (
  SELECT customer_id,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS d
  FROM orders
)
SELECT customer_id, COUNT(*) AS orders, COUNT(d) AS gaps, ROUND(AVG(d), 4) AS avg_gap_days
FROM g
GROUP BY customer_id
ORDER BY customer_id
```

**pandas answer:** parse the timestamps, sort, `groupby().diff()` gives a `Timedelta`, `dt.total_seconds() / 86400` converts to days.
```py
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"])).sort_values(["customer_id", "order_ts", "order_id"])
o["days_since_prev"] = o.groupby("customer_id")["order_ts"].diff().dt.total_seconds() / 86400
avg_gap = o.groupby("customer_id")["days_since_prev"].agg(orders="size", gaps="count", avg_gap_days="mean")
```

**Example:**
- Customer A: 01-01 09:00, 01-03 21:00, 01-03 21:00, 01-10 09:00. Gaps: NULL, 2.5 days, 0 days (same timestamp, order 3 sorts after order 2 by id), 6.5 days. Average of the three gaps = 9 / 3 = 3.0.
- Customer B: 02-01 12:00 then 02-11 12:00, gap 10.0 days, average 10.0.
- Customer C: 02-05 08:00 then 20:00, gap 0.5 days.
- Customer D: one order, no gap, so the average is NULL (`COUNT(d)` is 0).

**Code:** run with `python3 -I`.
```python
# Q14: days since the previous order per customer, average gap per customer
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
  (1,'A','2024-01-01 09:00:00'),(2,'A','2024-01-03 21:00:00'),(3,'A','2024-01-03 21:00:00'),
  (4,'A','2024-01-10 09:00:00'),(5,'B','2024-02-01 12:00:00'),(6,'C','2024-02-05 08:00:00'),
  (7,'C','2024-02-05 20:00:00'),(8,'B','2024-02-11 12:00:00'),(9,'D','2024-03-01 00:00:00');
"""
SQL_MAIN = """
WITH g AS (
  SELECT order_id, customer_id, order_ts,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS days_since_prev
  FROM orders
)
SELECT order_id, customer_id, order_ts, ROUND(days_since_prev, 4) AS days_since_prev
FROM g
ORDER BY customer_id, order_ts, order_id
"""
SQL_AVG = """
WITH g AS (
  SELECT customer_id,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS d
  FROM orders
)
SELECT customer_id, COUNT(*) AS orders, COUNT(d) AS gaps, ROUND(AVG(d), 4) AS avg_gap_days
FROM g
GROUP BY customer_id
ORDER BY customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_avg = pd.read_sql_query(SQL_AVG, con)
print(sql_df.to_string(index=False))
print()
print(sql_avg.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"])).sort_values(["customer_id", "order_ts", "order_id"])
o["days_since_prev"] = o.groupby("customer_id")["order_ts"].diff().dt.total_seconds() / 86400
avg_gap = o.groupby("customer_id")["days_since_prev"].agg(orders="size", gaps="count", avg_gap_days="mean")
# pd:end
out = o[["order_id", "customer_id", "days_since_prev"]].round({"days_since_prev": 4})
# compared after sorting by customer_id, order_ts, order_id (already sorted above)
pd.testing.assert_frame_equal(sql_df[["order_id", "customer_id", "days_since_prev"]].reset_index(drop=True),
                              out.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_avg.set_index("customer_id"), avg_gap.round({"avg_gap_days": 4}),
                              check_dtype=False)
print("\npandas avg gap:")
print(avg_gap.round(4).to_string())

# the trap: diff() without groupby crosses customer boundaries
wrong = orders.assign(order_ts=pd.to_datetime(orders["order_ts"])).sort_values(["order_ts", "order_id"])
wrong_gap = (wrong["order_ts"].diff().dt.total_seconds() / 86400).round(4)
print("\nungrouped diff() on the whole table gives (order_id order):",
      dict(zip(wrong["order_id"], wrong_gap.tolist())))
print("Timedelta(days=2.5).days gives", pd.Timedelta(days=2.5).days)
print("asserts passed: SQL LAG/julianday == pandas groupby().diff()")
```

**Output (my run):**
```text
 order_id customer_id            order_ts  days_since_prev
        1           A 2024-01-01 09:00:00              NaN
        2           A 2024-01-03 21:00:00              2.5
        3           A 2024-01-03 21:00:00              0.0
        4           A 2024-01-10 09:00:00              6.5
        5           B 2024-02-01 12:00:00              NaN
        8           B 2024-02-11 12:00:00             10.0
        6           C 2024-02-05 08:00:00              NaN
        7           C 2024-02-05 20:00:00              0.5
        9           D 2024-03-01 00:00:00              NaN

customer_id  orders  gaps  avg_gap_days
          A       4     3           3.0
          B       2     1          10.0
          C       2     1           0.5
          D       1     0           NaN

pandas avg gap:
             orders  gaps  avg_gap_days
customer_id                            
A                 4     3           3.0
B                 2     1          10.0
C                 2     1           0.5
D                 1     0           NaN

ungrouped diff() on the whole table gives (order_id order): {1: nan, 2: 2.5, 3: 0.0, 4: 6.5, 5: 22.125, 6: 3.8333, 7: 0.5, 8: 5.6667, 9: 18.5}
Timedelta(days=2.5).days gives 2
asserts passed: SQL LAG/julianday == pandas groupby().diff()
```

**Edge cases:**
- First order: `LAG` returns NULL, so the difference is NULL, not 0. Keep it NULL; 0 would pull the average down and would look like "ordered twice at the same moment".
- Ties on `order_ts` (orders 2 and 3): the second one gets a gap of 0. Without the `order_id` tie-breaker the engine may put either row first, so which order is labelled "the 0-day one" is not guaranteed. With the tie-breaker order 3 is always the repeat.
- Customer with one order: appears in the output with NULL average, because the gaps were computed per order and then grouped (a customer is not dropped).
- `AVG(d)` skips NULLs, so it divides by the number of gaps (3 for A), not by the number of orders (4). `COUNT(*)` versus `COUNT(d)` shows this.
- `julianday` differences are floating point, so I rounded to 4 places before comparing. Timestamps must be ISO text (`YYYY-MM-DD HH:MM:SS`) or `julianday` gives NULL; time zones are not handled (all values are treated as the same zone).
- pandas: `groupby("customer_id")["order_ts"].diff()` gives `NaT` for the first row, so `total_seconds()` gives NaN. Without `groupby`, `diff()` runs across customers; the output shows order 5 (customer B) getting 22.125 days because it was compared with customer A's last order.

**Then explain:**
- The window is `PARTITION BY customer_id ORDER BY order_ts, order_id`: partition so customers do not mix, order so "previous" is defined, tie-breaker so it is deterministic.
- It is two steps: gap per order in a CTE, then `AVG` per customer in the outer query.
- Other engines: PostgreSQL would subtract timestamps and use `EXTRACT(EPOCH FROM ...) / 86400`; MySQL `TIMESTAMPDIFF(SECOND, ...)`; BigQuery `TIMESTAMP_DIFF` (all not executed here).

**Follow-ups:**
- *Gap in hours?* Multiply the day difference by 24 (SQL) or use `total_seconds() / 3600` (pandas).
- *Median gap rather than average?* Needs a percentile function; SQLite has no percentile function; pandas has `median()`.
- *Repeat customers only?* `HAVING COUNT(d) >= 1` on the grouped query.

**Common mistakes:**
- Computing the gap without `PARTITION BY customer_id`.
- Treating the first order's NULL gap as 0.
- Ordering by `order_id`, which is not time order.
- Using `.days` on the `Timedelta` in pandas, which drops the fractional part (the run prints 2 for a 2.5 day Timedelta).

### Q15 ⭐⭐⭐ 🟡 Running count, running average and cumulative percent of total: daily_sales(sale_date, amount). Return for each day the running count of days, the running average (AVG OVER an ordered window, which is cumulative), the running total and the cumulative percent of the grand total using SUM(amount) OVER () as the denominator. Give the pandas cumcount()+1, expanding().mean() and cumsum()/sum() versions and explain that an AVG with ORDER BY in OVER is not a plain average.
**Asked at:** StrataScratch blog 'Top five SQL window functions for data science interviews' (month-over-month change with LEAD/LAG, cumulative cost with SUM, 10-day moving average, first visit with ROW_NUMBER), a guide and not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** All four are window aggregates over the same cumulative frame (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`) except the denominator, which is `SUM(amount) OVER ()` (whole table); `AVG(...) OVER (ORDER BY ...)` is a running average, not the plain average, because adding `ORDER BY` changes the frame.

**Schema and sample data:** six days of sales, one row per day, total 1000.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',100),('2024-01-02',50),('2024-01-03',150),
  ('2024-01-04',200),('2024-01-05',100),('2024-01-06',400);
```

**SQL answer:** I write the frame out so the intent is visible and duplicate dates cannot change it.
```sql
SELECT sale_date, amount,
       COUNT(*)    OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_days,
       ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_avg,
       SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 1.0
             / SUM(amount) OVER (), 4) AS cum_pct
FROM daily_sales
ORDER BY sale_date
```

**pandas answer:** `cumcount() + 1` needs a groupby, so I group by a constant key; `expanding().mean()` is the running average; `cumsum() / sum()` is the cumulative share.
```py
out = ds.copy()
out["running_days"] = out.assign(g=1).groupby("g").cumcount() + 1
out["running_avg"] = out["amount"].expanding().mean().round(2)
out["running_total"] = out["amount"].cumsum()
out["cum_pct"] = (out["amount"].cumsum() / out["amount"].sum()).round(4)
```

**Example:** amounts 100, 50, 150, 200, 100, 400.
- Running total: 100, 150, 300, 500, 600, 1000.
- Running average: 100/1 = 100, 150/2 = 75, 300/3 = 100, 500/4 = 125, 600/5 = 120, 1000/6 = 166.67.
- Cumulative percent of grand total 1000: 0.10, 0.15, 0.30, 0.50, 0.60, 1.00.
- Running count of days: 1 to 6.

**Code:** run with `python3 -I`.
```python
# Q15: running count, running average, running total, cumulative percent of total
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',100),('2024-01-02',50),('2024-01-03',150),
  ('2024-01-04',200),('2024-01-05',100),('2024-01-06',400);
"""
SQL_MAIN = """
SELECT sale_date, amount,
       COUNT(*)    OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_days,
       ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_avg,
       SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 1.0
             / SUM(amount) OVER (), 4) AS cum_pct
FROM daily_sales
ORDER BY sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
out = ds.copy()
out["running_days"] = out.assign(g=1).groupby("g").cumcount() + 1
out["running_avg"] = out["amount"].expanding().mean().round(2)
out["running_total"] = out["amount"].cumsum()
out["cum_pct"] = (out["amount"].cumsum() / out["amount"].sum()).round(4)
# pd:end
# compared in sale_date order (both sorted by sale_date)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)

# AVG(...) OVER (ORDER BY ...) is cumulative; AVG(...) OVER () is the plain average
plain = con.execute("SELECT AVG(amount) OVER () FROM daily_sales LIMIT 1").fetchone()[0]
cum_last = sql_df["running_avg"].iloc[-1]
print("\nplain average AVG() OVER ():", round(plain, 4), "| ordered AVG on the last row:", cum_last,
      "| ordered AVG on the first row:", sql_df["running_avg"].iloc[0])

# duplicate dates: default frame is RANGE through peers
con.executescript("""
CREATE TABLE sales_dup(id INTEGER PRIMARY KEY, sale_date TEXT, amount INTEGER);
INSERT INTO sales_dup VALUES (1,'2024-01-01',100),(2,'2024-01-02',50),(3,'2024-01-02',150),(4,'2024-01-03',200);
""")
for label, order in [("default frame, ORDER BY sale_date      ", "ORDER BY sale_date"),
                     ("ROWS frame, ORDER BY sale_date, id     ", "ORDER BY sale_date, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW")]:
    rows = con.execute(f"SELECT id, COUNT(*) OVER ({order}), SUM(amount) OVER ({order}) FROM sales_dup ORDER BY id").fetchall()
    print(label, "(id, running_count, running_sum):", rows)

# empty/zero denominator and NULL amount
con.executescript("""
CREATE TABLE zeros(d TEXT, amount INTEGER);
INSERT INTO zeros VALUES ('2024-01-01',0),('2024-01-02',0);
CREATE TABLE nulls(d TEXT, amount INTEGER);
INSERT INTO nulls VALUES ('2024-01-01',10),('2024-01-02',NULL),('2024-01-03',30);
""")
print("zero grand total, SQL cum_pct:", con.execute(
    "SELECT SUM(amount) OVER (ORDER BY d) * 1.0 / SUM(amount) OVER () FROM zeros").fetchall())
z = pd.Series([0, 0])
print("zero grand total, pandas cumsum()/sum():", (z.cumsum() / z.sum()).tolist())
print("NULL amount: COUNT(*) vs COUNT(amount) vs AVG, last row:", con.execute(
    "SELECT COUNT(*) OVER w, COUNT(amount) OVER w, AVG(amount) OVER w FROM nulls "
    "WINDOW w AS (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) ORDER BY d DESC LIMIT 1").fetchall())
n = pd.Series([10, None, 30])
print("NULL amount, pandas expanding().count() last / expanding().mean() last:",
      n.expanding().count().iloc[-1], n.expanding().mean().iloc[-1])
print("asserts passed: SQL running aggregates == pandas cumcount/expanding/cumsum")
```

**Output (my run):**
```text
 sale_date  amount  running_days  running_avg  running_total  cum_pct
2024-01-01     100             1       100.00            100     0.10
2024-01-02      50             2        75.00            150     0.15
2024-01-03     150             3       100.00            300     0.30
2024-01-04     200             4       125.00            500     0.50
2024-01-05     100             5       120.00            600     0.60
2024-01-06     400             6       166.67           1000     1.00

plain average AVG() OVER (): 166.6667 | ordered AVG on the last row: 166.67 | ordered AVG on the first row: 100.0
default frame, ORDER BY sale_date       (id, running_count, running_sum): [(1, 1, 100), (2, 3, 300), (3, 3, 300), (4, 4, 500)]
ROWS frame, ORDER BY sale_date, id      (id, running_count, running_sum): [(1, 1, 100), (2, 2, 150), (3, 3, 300), (4, 4, 500)]
zero grand total, SQL cum_pct: [(None,), (None,)]
zero grand total, pandas cumsum()/sum(): [nan, nan]
NULL amount: COUNT(*) vs COUNT(amount) vs AVG, last row: [(3, 2, 20.0)]
NULL amount, pandas expanding().count() last / expanding().mean() last: 2.0 20.0
asserts passed: SQL running aggregates == pandas cumcount/expanding/cumsum
```

**Edge cases:**
- Duplicate dates: with only `ORDER BY sale_date` and no frame, the default is `RANGE UNBOUNDED PRECEDING` through the last peer, so rows with the same date are included together. In my duplicate test (two rows on 01-02, ids 2 and 3) the default frame gave running counts 1, 3, 3, 4 and running sums 100, 300, 300, 500, so both peers showed the same total; `ORDER BY sale_date, id ROWS ...` gave 1, 2, 3, 4 and 100, 150, 300, 500. In this question's table the date is the primary key, so both agree, but I still write ROWS and a unique order.
- Zero grand total: the SQL divides by 0 and SQLite returns NULL (output shows `None`); pandas `0 / 0` gives NaN. A non-zero numerator over a zero total would be `inf` in pandas; other SQL engines may raise a division error (not executed here), so guard with `NULLIF(total, 0)`.
- NULL amount: the running count of days (`COUNT(*)`) still counts that day, but `COUNT(amount)` and `AVG` do not. In my test `[10, NULL, 30]` gave COUNT(*) 3, COUNT(amount) 2 and average 20.0 on the last row; pandas `expanding().count()` gave 2.0 and `expanding().mean()` 20.0 (both skip NaN). `cumcount() + 1` counts the NaN row, like `COUNT(*)`.
- Empty table: no rows, no output.

**Then explain:**
- `AVG(x) OVER ()` is the plain average of the whole table (one number repeated on every row). `AVG(x) OVER (ORDER BY d)` is the average from the first row to this row; it is the same number as the plain average only on the last row (166.67 and 166.6667 in the output).
- The denominator `SUM(amount) OVER ()` has no `ORDER BY`, so its frame is the whole partition: one grand total repeated on every row. That is how a window function gives "share of total" without a self-join.
- pandas: `expanding()` is the pandas name for the cumulative frame; `cumsum() / sum()` is the vectorised share. I rounded both sides to 4 places before asserting equality.
- Percent versus fraction: I return a fraction (0.10); multiply by 100 for a percentage.

**Follow-ups:**
- *Running average over the last 3 days only?* Change the frame (Q8).
- *Percent of total per month or per category?* Add `PARTITION BY` to the denominator window.
- *Why not `AVG(amount) OVER (ORDER BY d)` with no ROWS?* It works when dates are unique; with duplicates the default RANGE frame gives peers the same value.

**Common mistakes:**
- Thinking `AVG() OVER (ORDER BY ...)` is the overall average.
- Putting `ORDER BY` inside the denominator window, turning the "grand total" into another running total.
- Integer division: `SUM(amount) / SUM(amount) OVER ()` on two integers can truncate to 0; I multiplied by 1.0 to avoid it (how other engines behave is not executed here).
- Forgetting the `ORDER BY` on the outer query: window order and output order are separate.

### Q16 ⭐⭐⭐ 🟡 Month-over-month change with a missing month: monthly_revenue(month, revenue) where one month (for example March) has no row. Show that LAG(revenue) then compares April with February, explain why, and fix it by building a complete month calendar (a recursive CTE or a month table), LEFT JOIN the revenue, and COALESCE missing months to 0 or leave NULL as a deliberate choice. Give the pandas resample('MS') or reindex version and state what the percent change for the month after a zero month should be.
**Asked at:** LearnSQL revenue-growth and Craig Kerstiens month-over-month blog write-ups (LAG, percent change, gaps break LAG, divide by zero), guides and not candidate reports; analyst screens at product companies and startups
**Say this first (1 line):** `LAG` returns the previous row that exists, so with March missing it compares April with February and calls it month-over-month; build a full month calendar (recursive CTE), LEFT JOIN the revenue, and decide on purpose whether a missing month is NULL (unknown) or 0 (no sales).

**Schema and sample data:** four months, March has no row. Months are stored as first-of-month dates so both SQLite `date()` and pandas `resample('MS')` can use them.
```sql
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES ('2024-01-01',100),('2024-02-01',120),('2024-04-01',150),('2024-05-01',165);
```

**SQL answer:** the naive LAG, then the calendar version that leaves March NULL (`SQL_MAIN`), then the version that turns missing months into 0 (`SQL_ZERO`; it is `SQL_MAIN` with the line `SELECT c.month, r.revenue` replaced by `SELECT c.month, COALESCE(r.revenue, 0) AS revenue`, which is exactly what the Code block does).
```sql
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / LAG(revenue) OVER (ORDER BY month), 2) AS mom_pct
FROM monthly_revenue
ORDER BY month
```
```sql
WITH RECURSIVE cal(month) AS (
  SELECT MIN(month) FROM monthly_revenue
  UNION ALL
  SELECT date(month, '+1 month') FROM cal WHERE month < (SELECT MAX(month) FROM monthly_revenue)
), filled AS (
  SELECT c.month, r.revenue
  FROM cal c LEFT JOIN monthly_revenue r ON r.month = c.month
)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) AS mom_pct
FROM filled
ORDER BY month
```

**pandas answer:** `asfreq("MS")` creates the missing month as NaN; `pct_change()` then leaves NaN around it. For the zero version, `fillna(0)` and replace the infinity with NaN.
```py
s = mr.assign(month=pd.to_datetime(mr["month"])).set_index("month")["revenue"]
full = s.asfreq("MS")                       # complete month calendar, missing months become NaN
pd_null = (full.pct_change() * 100).round(2)
zero = full.fillna(0)
pd_zero = (zero.pct_change() * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
```

**Example:** revenue Jan 100, Feb 120, Apr 150, May 165.
- Naive LAG: Apr is compared with Feb, giving +25.0%; this is a two-month change shown as a month-over-month number. There is no March row at all, so nobody can see the problem.
- Calendar, March NULL: Mar = NULL, growth Mar = NULL (no revenue to compare), Apr = NULL (no previous month value), May = (165 - 150) / 150 = +10.0%.
- Calendar, March = 0: Mar = (0 - 120) / 120 = -100.0%, Apr = NULL because the base is 0 (`NULLIF` avoids dividing by zero), May = +10.0%.

**Code:** run with `python3 -I`.
```python
# Q16: month-over-month change when a month has no row
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES ('2024-01-01',100),('2024-02-01',120),('2024-04-01',150),('2024-05-01',165);
"""
SQL_NAIVE = """
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / LAG(revenue) OVER (ORDER BY month), 2) AS mom_pct
FROM monthly_revenue
ORDER BY month
"""
SQL_MAIN = """
WITH RECURSIVE cal(month) AS (
  SELECT MIN(month) FROM monthly_revenue
  UNION ALL
  SELECT date(month, '+1 month') FROM cal WHERE month < (SELECT MAX(month) FROM monthly_revenue)
), filled AS (
  SELECT c.month, r.revenue
  FROM cal c LEFT JOIN monthly_revenue r ON r.month = c.month
)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) AS mom_pct
FROM filled
ORDER BY month
"""
SQL_ZERO = SQL_MAIN.replace("SELECT c.month, r.revenue", "SELECT c.month, COALESCE(r.revenue, 0) AS revenue")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
naive = pd.read_sql_query(SQL_NAIVE, con)
sql_null = pd.read_sql_query(SQL_MAIN, con)
sql_zero = pd.read_sql_query(SQL_ZERO, con)
print("naive LAG on the table with a missing row:"); print(naive.to_string(index=False))
print("\ncalendar + LEFT JOIN, March left NULL:"); print(sql_null.to_string(index=False))
print("\ncalendar + COALESCE(revenue, 0), NULLIF on the divisor:"); print(sql_zero.to_string(index=False))

mr = pd.read_sql_query("SELECT * FROM monthly_revenue", con)
# pd:main
s = mr.assign(month=pd.to_datetime(mr["month"])).set_index("month")["revenue"]
full = s.asfreq("MS")                       # complete month calendar, missing months become NaN
pd_null = (full.pct_change() * 100).round(2)
zero = full.fillna(0)
pd_zero = (zero.pct_change() * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
# pd:end
# compared in month order
pd.testing.assert_series_equal(pd_null.reset_index(drop=True), sql_null["mom_pct"], check_names=False, check_dtype=False)
pd.testing.assert_series_equal(pd_zero.reset_index(drop=True), sql_zero["mom_pct"], check_names=False, check_dtype=False)
print("\npandas asfreq('MS') + pct_change (NaN kept):", pd_null.tolist())
print("pandas fillna(0).pct_change() raw (before replacing inf):", (zero.pct_change() * 100).round(2).tolist())

# alternatives and pitfalls
print("\nresample('MS').sum() turns the missing month into", s.resample("MS").sum().loc["2024-03-01"],
      "| resample('MS').mean() gives", s.resample("MS").mean().loc["2024-03-01"])
print("reindex(pd.date_range(..., freq='MS')) equals asfreq:",
      s.reindex(pd.date_range(s.index.min(), s.index.max(), freq="MS")).equals(full))
print("pct_change() on the table WITHOUT the calendar (pandas, same mistake as SQL LAG):",
      (s.pct_change() * 100).round(2).tolist())
try:
    full.pct_change(fill_method="ffill")
except Exception as e:
    print("pct_change(fill_method='ffill') in this pandas:", type(e).__name__, "-", e)
print("asserts passed: SQL calendar versions == pandas asfreq versions")
```

**Output (my run):**
```text
naive LAG on the table with a missing row:
     month  revenue  prev_rev  mom_pct
2024-01-01      100       NaN      NaN
2024-02-01      120     100.0     20.0
2024-04-01      150     120.0     25.0
2024-05-01      165     150.0     10.0

calendar + LEFT JOIN, March left NULL:
     month  revenue  prev_rev  mom_pct
2024-01-01    100.0       NaN      NaN
2024-02-01    120.0     100.0     20.0
2024-03-01      NaN     120.0      NaN
2024-04-01    150.0       NaN      NaN
2024-05-01    165.0     150.0     10.0

calendar + COALESCE(revenue, 0), NULLIF on the divisor:
     month  revenue  prev_rev  mom_pct
2024-01-01      100       NaN      NaN
2024-02-01      120     100.0     20.0
2024-03-01        0     120.0   -100.0
2024-04-01      150       0.0      NaN
2024-05-01      165     150.0     10.0

pandas asfreq('MS') + pct_change (NaN kept): [nan, 20.0, nan, nan, 10.0]
pandas fillna(0).pct_change() raw (before replacing inf): [nan, 20.0, -100.0, inf, 10.0]

resample('MS').sum() turns the missing month into 0 | resample('MS').mean() gives nan
reindex(pd.date_range(..., freq='MS')) equals asfreq: True
pct_change() on the table WITHOUT the calendar (pandas, same mistake as SQL LAG): [nan, 20.0, 25.0, 10.0]
pct_change(fill_method='ffill') in this pandas: ValueError - fill_method must be None; got fill_method='ffill'.
asserts passed: SQL calendar versions == pandas asfreq versions
```

**Edge cases:**
- Percent change after a zero month: undefined (divide by zero). I return NULL; pandas gives `inf` (shown in the output as the raw `fillna(0).pct_change()`), which I replaced with NaN to match. Do not show `inf` or a huge number on a dashboard; say "n/a" or "new".
- NULL versus 0 for the missing month is a business decision: no row because the store was closed (NULL) is different from no sales (0). I show both and let the question decide.
- Several missing months in a row: the calendar handles it; the NULL months then propagate as shown.
- Duplicate month rows: the primary key in this table prevents them; without it, aggregate to one row per month before the calendar join.
- `resample("MS").sum()` turns a missing month into 0 silently (output: 0), while `resample("MS").mean()` gives NaN. Use `asfreq` or `reindex` if you want NaN, and `.sum()` only if 0 is the intended answer.
- `pct_change` in this pandas (3.0.5): NaN is not forward-filled by default (April stayed NaN), and passing `fill_method="ffill"` raised `ValueError: fill_method must be None`. Older pandas filled NaN forward by default (from memory of the deprecation, not executed here).

**Then explain:**
- Why LAG fails: it is positional. A gap in the data is invisible to it.
- The recursive CTE generates one row per month from the minimum to the maximum month with `date(month, '+1 month')`. Other engines have `generate_series` (PostgreSQL), `GENERATE_DATE_ARRAY` (BigQuery) or a calendar table (not executed here).
- A permanent calendar table is the usual choice in a warehouse: you join to it for every report.
- pandas `reindex(pd.date_range(min, max, freq="MS"))` and `asfreq("MS")` gave the same result in my run.

**Follow-ups:**
- *Same for days or weeks?* Same pattern with a daily calendar.
- *Should the missing month be forward-filled with February's revenue?* Only for stock-like values (balance, price), not for flows like revenue.
- *Year-over-year with missing months?* Q23.

**Common mistakes:**
- Trusting LAG on gappy data.
- `COALESCE` to 0 and then dividing by it.
- Using `resample().sum()` and not realising it invented zeros.
- Calendar built from the data's own months (no help: the missing month must come from the calendar, not from the table).

### Q17 ⭐⭐⭐ 🟡 Running Total for Different Genders (LeetCode 1308 style): Scores(player_name, gender, day, score_points) with PRIMARY KEY (gender, day). Return gender, day and the running total of score_points per gender ordered by day, ordered by gender and day. Explain PARTITION BY gender versus ORDER BY day, and give the pandas groupby('gender')['score_points'].cumsum().
**Asked at:** public LeetCode-style problem bank (1321 Restaurant Growth statement seen in a search snippet; 1308 Running Total for Different Genders, 197 Rising Temperature and 180 Consecutive Numbers known only by title from third-party lists), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** `SUM(score_points) OVER (PARTITION BY gender ORDER BY day)`: `PARTITION BY gender` restarts the total for each gender, `ORDER BY day` makes it cumulative inside each gender; the final `ORDER BY gender, day` is a separate clause for the output.

**Schema and sample data:** seven scores, four for M and three for F, primary key `(gender, day)` so a gender never has two rows on the same day. The sample is not the LeetCode example data; the table shape follows the problem title.
```sql
CREATE TABLE Scores(player_name TEXT, gender TEXT, day TEXT, score_points INTEGER, PRIMARY KEY (gender, day));
INSERT INTO Scores VALUES ('Aron','F','2020-01-01',17),('Alice','F','2020-01-07',23),
  ('Cy','F','2020-01-10',5),('Joe','M','2019-12-18',2),('Bajrang','M','2019-12-25',7),
  ('Khali','M','2019-12-30',11),('Slaman','M','2019-12-31',13);
```

**SQL answer:** two broken variants are in the Code block for contrast.
```sql
SELECT gender, day,
       SUM(score_points) OVER (PARTITION BY gender ORDER BY day
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total
FROM Scores
ORDER BY gender, day
```

**pandas answer:** sort by gender and day, then `groupby('gender')['score_points'].cumsum()`.
```py
s = scores.sort_values(["gender", "day"])
s["total"] = s.groupby("gender")["score_points"].cumsum()
pd_df = s[["gender", "day", "total"]]
```

**Example:**
- F: 17 on 01-01, then 17 + 23 = 40 on 01-07, then 40 + 5 = 45 on 01-10.
- M: 2, 2 + 7 = 9, 9 + 11 = 20, 20 + 13 = 33.
- The two genders never mix: F restarts at its own first row.

**Code:** run with `python3 -I`.
```python
# Q17: running total per gender (LeetCode 1308 style)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE Scores(player_name TEXT, gender TEXT, day TEXT, score_points INTEGER, PRIMARY KEY (gender, day));
INSERT INTO Scores VALUES ('Aron','F','2020-01-01',17),('Alice','F','2020-01-07',23),
  ('Cy','F','2020-01-10',5),('Joe','M','2019-12-18',2),('Bajrang','M','2019-12-25',7),
  ('Khali','M','2019-12-30',11),('Slaman','M','2019-12-31',13);
"""
SQL_MAIN = """
SELECT gender, day,
       SUM(score_points) OVER (PARTITION BY gender ORDER BY day
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total
FROM Scores
ORDER BY gender, day
"""
SQL_NO_ORDER = """
SELECT gender, day, SUM(score_points) OVER (PARTITION BY gender) AS total
FROM Scores ORDER BY gender, day
"""
SQL_NO_PARTITION = """
SELECT gender, day, SUM(score_points) OVER (ORDER BY day) AS total
FROM Scores ORDER BY gender, day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nPARTITION BY gender, no ORDER BY (whole-partition total on every row):",
      [r[2] for r in con.execute(SQL_NO_ORDER)])
print("ORDER BY day, no PARTITION BY (genders mixed together):",
      [(r[0], r[2]) for r in con.execute(SQL_NO_PARTITION)])

scores = pd.read_sql_query("SELECT * FROM Scores", con)
# pd:main
s = scores.sort_values(["gender", "day"])
s["total"] = s.groupby("gender")["score_points"].cumsum()
pd_df = s[["gender", "day", "total"]]
# pd:end
# compared after sorting by gender, day
pd.testing.assert_frame_equal(sql_df, pd_df.reset_index(drop=True), check_dtype=False)

# without the sort, groupby().cumsum() follows the physical row order (here: rows reversed)
rev = scores.iloc[::-1]
unsorted = rev.assign(total=rev.groupby("gender")["score_points"].cumsum())
print("\npandas cumsum on a reversed, unsorted frame, M rows (day, total):",
      unsorted.loc[unsorted["gender"] == "M", ["day", "total"]].values.tolist())
print("asserts passed: SQL PARTITION BY/ORDER BY == pandas sort + groupby().cumsum()")
```

**Output (my run):**
```text
gender        day  total
     F 2020-01-01     17
     F 2020-01-07     40
     F 2020-01-10     45
     M 2019-12-18      2
     M 2019-12-25      9
     M 2019-12-30     20
     M 2019-12-31     33

PARTITION BY gender, no ORDER BY (whole-partition total on every row): [45, 45, 45, 33, 33, 33, 33]
ORDER BY day, no PARTITION BY (genders mixed together): [('F', 50), ('F', 73), ('F', 78), ('M', 2), ('M', 9), ('M', 20), ('M', 33)]

pandas cumsum on a reversed, unsorted frame, M rows (day, total): [['2019-12-31', 13], ['2019-12-30', 24], ['2019-12-25', 31], ['2019-12-18', 33]]
asserts passed: SQL PARTITION BY/ORDER BY == pandas sort + groupby().cumsum()
```

**Edge cases:**
- Ties: none possible, because `(gender, day)` is the primary key. If the key allowed two rows per gender-day, the default frame would give both rows the same total; add a tie-breaker and `ROWS` in that case (I tested this effect in Q15).
- Missing `ORDER BY`: every row gets the partition total (45 for all F rows, 33 for all M rows in my run), a non-running number.
- Missing `PARTITION BY`: one running total across both genders ordered by day (in the output the F rows show 50, 73 and 78, because the earlier M days, which total 33, were already added).
- NULL `score_points`: SQL `SUM` ignores NULL and the total carries on; pandas `cumsum()` leaves NaN at that row (details in Q18). The sample has no NULLs.
- Empty gender group: cannot appear; a gender with no rows has no output rows.
- pandas without the sort: `cumsum` follows physical row order. On a reversed copy of the frame the M totals came out 13, 24, 31, 33 instead of 2, 9, 20, 33.

**Then explain:**
- `PARTITION BY` is like `GROUP BY` for windows without collapsing rows: separate running totals per group.
- `ORDER BY` inside `OVER` defines the order of accumulation. `ORDER BY` at the end of the query only defines the order of the result.
- pandas `groupby(...).cumsum()` is the same idea; unlike SQL it does not take an order, so sort first.

**Follow-ups:**
- *Total across both genders too?* A second window with no partition (`SUM(...) OVER (ORDER BY day)`), as in the broken variant; here it is shown to be the wrong answer to this question but the right one for an overall total.
- *Percent of the gender's final total?* Divide by `SUM(...) OVER (PARTITION BY gender)`.
- *Only players on the same team?* Add the team column to `PARTITION BY`.

**Common mistakes:**
- Leaving out `PARTITION BY`, mixing genders.
- Leaving out `ORDER BY` in `OVER`, getting a partition total on every row.
- Ordering the final result only by `day`, when the problem asks for gender then day.
- Forgetting to sort in pandas before `cumsum`.

### Q18 ⭐⭐⭐ 🟡 SQL versus pandas NaN and NULL in running totals and lag: a series with a missing value (amount NULL on one day). Show SUM(amount) OVER (ORDER BY day) (NULL ignored, total carries on), COUNT(amount) versus COUNT(*) as a running count, then pandas cumsum() (skipna=True keeps NaN at that position but continues the sum) and cumsum(skipna=False), and shift() turning integer columns into float64 unless fill_value is passed. Run both and assert where they match.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** SQL aggregates skip NULL, so `SUM(amount) OVER (ORDER BY day)` carries the total across the missing day, and `COUNT(amount)` is one lower than `COUNT(*)` from then on; pandas `cumsum()` also skips NaN but leaves NaN in that row's own output, so `cumsum().ffill()` is what matches SQL, while `cumsum(skipna=False)` turns everything after the NaN into NaN.

**Schema and sample data:** five days, day 3 has a NULL amount.
```sql
CREATE TABLE s(day INTEGER PRIMARY KEY, amount INTEGER);
INSERT INTO s VALUES (1,10),(2,20),(3,NULL),(4,40),(5,50);
```

**SQL answer:**
```sql
SELECT day, amount,
       SUM(amount)   OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_sum,
       COUNT(*)      OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_rows,
       COUNT(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_nonnull,
       LAG(amount)   OVER (ORDER BY day) AS prev_amount
FROM s
ORDER BY day
```

**pandas answer:** `read_sql_query` returns the NULL as NaN in a float64 column, so the integer amounts arrive as floats.
```py
a = s["amount"]                                   # float64: NULL arrives as NaN
out = pd.DataFrame({"day": s["day"], "amount": a})
out["running_sum"] = a.cumsum().ffill()           # cumsum() keeps NaN at the NaN row; ffill restores SQL's carried total
out["n_rows"] = range(1, len(a) + 1)
out["n_nonnull"] = a.notna().cumsum()
out["prev_amount"] = a.shift()
```

**Example:** amounts 10, 20, NULL, 40, 50.
- SQL running sum: 10, 30, 30 (NULL adds nothing), 70, 120. `COUNT(*)`: 1 to 5. `COUNT(amount)`: 1, 2, 2, 3, 4. `LAG(amount)`: NULL, 10, 20, NULL (day 3 was NULL), 40.
- pandas `cumsum()`: 10, 30, NaN, 70, 120: the sum continues, but the NaN row shows NaN. `cumsum(skipna=False)`: 10, 30, NaN, NaN, NaN: NaN is sticky.
- `cumsum().ffill()` gives 10, 30, 30, 70, 120, the same as SQL. `fillna(0).cumsum()` gives the same numbers here too.

**Code:** run with `python3 -I`.
```python
# Q18: NULL versus NaN in running totals, running counts and lag
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE s(day INTEGER PRIMARY KEY, amount INTEGER);
INSERT INTO s VALUES (1,10),(2,20),(3,NULL),(4,40),(5,50);
"""
SQL_MAIN = """
SELECT day, amount,
       SUM(amount)   OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_sum,
       COUNT(*)      OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_rows,
       COUNT(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_nonnull,
       LAG(amount)   OVER (ORDER BY day) AS prev_amount
FROM s
ORDER BY day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

s = pd.read_sql_query("SELECT * FROM s ORDER BY day", con)
# pd:main
a = s["amount"]                                   # float64: NULL arrives as NaN
out = pd.DataFrame({"day": s["day"], "amount": a})
out["running_sum"] = a.cumsum().ffill()           # cumsum() keeps NaN at the NaN row; ffill restores SQL's carried total
out["n_rows"] = range(1, len(a) + 1)
out["n_nonnull"] = a.notna().cumsum()
out["prev_amount"] = a.shift()
# pd:end
# compared in day order (both ordered by day)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)

print("\npandas cumsum()              :", a.cumsum().tolist())
print("pandas cumsum(skipna=False)  :", a.cumsum(skipna=False).tolist())
print("pandas cumsum().ffill()      :", a.cumsum().ffill().tolist(), "(matches SQL SUM OVER)")
print("pandas fillna(0).cumsum()    :", a.fillna(0).cumsum().tolist())

# nullable dtypes (verified here on pandas 3.0.5)
n = pd.Series([1, None, 3], dtype="Int64")
print("\nInt64 cumsum()               :", n.cumsum().tolist(), "dtype", n.cumsum().dtype)
print("Int64 cumsum(skipna=False)   :", n.cumsum(skipna=False).tolist())
print("Int64 shift()                :", n.shift().tolist(), "dtype", n.shift().dtype)

# shift and dtype
ints = pd.Series([5, 6, 7])
print("\nint64 .shift() dtype         :", ints.shift().dtype, ints.shift().tolist())
print("int64 .shift(fill_value=0)   :", ints.shift(fill_value=0).dtype, ints.shift(fill_value=0).tolist())
print("SQL LAG(amount, 1, 0) day 1  :", con.execute("SELECT LAG(amount, 1, 0) OVER (ORDER BY day) FROM s ORDER BY day LIMIT 1").fetchone()[0])

# NULL in the first row: SQL SUM gives NULL until the first non-NULL value; pandas gives NaN
con.executescript("CREATE TABLE f(day INTEGER, amount INTEGER); INSERT INTO f VALUES (1,NULL),(2,5),(3,NULL);")
print("\nfirst-row NULL, SQL running sum :", [r[0] for r in con.execute(
    "SELECT SUM(amount) OVER (ORDER BY day) FROM f ORDER BY day")])
fa = pd.Series([None, 5, None], dtype="float64")
print("first-row NULL, pandas cumsum().ffill():", fa.cumsum().ffill().tolist())
print("asserts passed: SQL window == pandas cumsum().ffill(), notna().cumsum(), shift()")
```

**Output (my run):**
```text
 day  amount  running_sum  n_rows  n_nonnull  prev_amount
   1    10.0           10       1          1          NaN
   2    20.0           30       2          2         10.0
   3     NaN           30       3          2         20.0
   4    40.0           70       4          3          NaN
   5    50.0          120       5          4         40.0

pandas cumsum()              : [10.0, 30.0, nan, 70.0, 120.0]
pandas cumsum(skipna=False)  : [10.0, 30.0, nan, nan, nan]
pandas cumsum().ffill()      : [10.0, 30.0, 30.0, 70.0, 120.0] (matches SQL SUM OVER)
pandas fillna(0).cumsum()    : [10.0, 30.0, 30.0, 70.0, 120.0]

Int64 cumsum()               : [1, <NA>, 4] dtype Int64
Int64 cumsum(skipna=False)   : [1, <NA>, <NA>]
Int64 shift()                : [<NA>, 1, <NA>] dtype Int64

int64 .shift() dtype         : float64 [nan, 5.0, 6.0]
int64 .shift(fill_value=0)   : int64 [0, 5, 6]
SQL LAG(amount, 1, 0) day 1  : 0

first-row NULL, SQL running sum : [None, 5, 5]
first-row NULL, pandas cumsum().ffill(): [nan, 5.0, 5.0]
asserts passed: SQL window == pandas cumsum().ffill(), notna().cumsum(), shift()
```

**Edge cases:**
- Where they match: the SQL running sum equals pandas `cumsum().ffill()` on every row of my sample; SQL `COUNT(amount)` equals `notna().cumsum()`; SQL `LAG` equals `shift()` (NULL versus NaN); the asserts check all four. Where they differ before the fix: SQL shows 30 on the NULL day, plain `cumsum()` shows NaN.
- NULL in the first row: SQL `SUM` is NULL until the first non-NULL value (output: None, 5, 5); `cumsum().ffill()` gives NaN, 5.0, 5.0. A fully NULL partition in SQL gives NULL, not 0, whereas `fillna(0).cumsum()` would give 0, so the two zero-based versions differ in that corner.
- `shift()` and dtype: an int64 column becomes float64 after `shift()` because NaN needs a float; `shift(fill_value=0)` keeps int64. SQL `LAG(amount, 1, 0)` gives 0 on the first row, the same idea.
- Nullable dtypes: on pandas 3.0.5 an `Int64` series `[1, <NA>, 3]` gave `cumsum()` = `[1, <NA>, 4]` (dtype stays `Int64`), `cumsum(skipna=False)` = `[1, <NA>, <NA>]`, and `shift()` kept `Int64`, with `<NA>` in the first slot. So with nullable integers you keep integers and avoid the float conversion.
- Running count of rows: `COUNT(*)` counts the NULL row; `COUNT(amount)` does not. For "average so far", `AVG` uses the non-NULL count (Q15).
- Duplicate days: `day` is the primary key here. With duplicate days, add a tie-breaker and `ROWS` (Q15).

**Then explain:**
- NULL means unknown. SQL aggregates ignore it because it is not a number to add; they never invent a zero.
- pandas has two NA flavours: NaN in float64 columns, `pd.NA` in nullable dtypes. Both are skipped by default (`skipna=True`).
- `skipna=True` still keeps the NaN in its own position: it only means the running sum ignores it, not that the position is filled.
- Which to choose is a business question: treat missing as zero (`fillna(0)`), carry forward (`ffill`), or keep unknown (`skipna=False`).

**Follow-ups:**
- *How would you make SQL behave like `skipna=False`?* A running flag (`MAX(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)` over the same frame) and return NULL once it is 1; I did not run this one.
- *And `COALESCE(amount, 0)`?* Then the NULL day counts as a real zero for averages and counts.
- *Why did `shift()` change my integer column to float?* Because NaN cannot live in int64; use `fill_value` or `Int64`.

**Common mistakes:**
- Assuming `cumsum()` fills the NaN row.
- Comparing the SQL and pandas results with `==` on NaN (NaN is not equal to NaN; use `assert_frame_equal`).
- Using `COUNT(*)` when you mean the number of non-NULL values.
- Not noticing the dtype switch to float64 after `shift()` and then writing it back to an integer column.

### Q19 ⭐⭐ 🟢 NTH_VALUE and the second order per customer: orders(order_id, customer_id, order_date, amount). Return each customer's second order amount with NTH_VALUE(amount, 2) over a full-partition frame, explain that the answer is NULL when the customer has fewer than two orders and that the default frame also changes the result for the first row, and give the pandas groupby().nth(1) or iloc version. Mention that FROM LAST and IGNORE NULLS are not available in SQLite and PostgreSQL does not implement them.
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `NTH_VALUE(amount, 2)` returns the second row's value of the window frame, so it needs `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to see the whole partition; with the default frame the first row gets NULL, and a customer with fewer than two orders gets NULL everywhere.

**Schema and sample data:** four customers. Customer 1 has three orders, customer 2 has one, customer 3 has two orders on the same date, customer 4's second order has a NULL amount.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-01',100),(2,1,'2024-01-05',150),(3,1,'2024-01-09',90),
  (4,2,'2024-01-02',70),
  (5,3,'2024-01-03',40),(6,3,'2024-01-03',60),(7,3,'2024-01-10',80),
  (8,4,'2024-02-01',30),(9,4,'2024-02-02',NULL),(10,4,'2024-02-03',55);
```

**SQL answer:** tie rule: `order_date, order_id`. `DISTINCT` collapses the repeated per-row value to one row per customer.
```sql
WITH n AS (
  SELECT customer_id,
         NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id
                                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_amount
  FROM orders
)
SELECT DISTINCT customer_id, second_amount FROM n ORDER BY customer_id
```
```sql
SELECT order_id, customer_id,
       NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS second_default_frame
FROM orders WHERE customer_id = 1 ORDER BY order_date, order_id
```

**pandas answer:** `groupby().nth(1)` takes the second row of each group (0-based), but only for groups that have one, so reindex to bring back the short groups.
```py
o = orders.sort_values(["customer_id", "order_date", "order_id"])
nth = o.groupby("customer_id")["amount"].nth(1)          # rows only for customers with 2+ orders
second = (o.loc[nth.index].set_index("customer_id")["amount"]
            .reindex(sorted(orders["customer_id"].unique())))   # bring back customers with one order
pd_df = second.rename("second_amount").reset_index()
```

**Example:**
- Customer 1: amounts in date order 100, 150, 90, second is 150.
- Customer 2: one order, so there is no second one: NULL.
- Customer 3: two orders on 01-03 (ids 5 and 6) then 01-10. Tie-breaker `order_id` puts 40 first and 60 second, so the answer is 60. Without the tie-breaker the engine could return 40 or 60 for the second slot.
- Customer 4: the second row is the NULL amount, so the answer is NULL (the 55 is the third value, not the second non-NULL one).
- Default frame for customer 1, row by row: NULL, 150, 150. The first row cannot see its own second row yet.

**Code:** run with `python3 -I`.
```python
# Q19: NTH_VALUE and the second order per customer
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-01',100),(2,1,'2024-01-05',150),(3,1,'2024-01-09',90),
  (4,2,'2024-01-02',70),
  (5,3,'2024-01-03',40),(6,3,'2024-01-03',60),(7,3,'2024-01-10',80),
  (8,4,'2024-02-01',30),(9,4,'2024-02-02',NULL),(10,4,'2024-02-03',55);
"""
SQL_MAIN = """
WITH n AS (
  SELECT customer_id,
         NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id
                                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_amount
  FROM orders
)
SELECT DISTINCT customer_id, second_amount FROM n ORDER BY customer_id
"""
SQL_DEFAULT = """
SELECT order_id, customer_id,
       NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS second_default_frame
FROM orders WHERE customer_id = 1 ORDER BY order_date, order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\ndefault frame, customer 1 (row by row):", con.execute(SQL_DEFAULT).fetchall())

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.sort_values(["customer_id", "order_date", "order_id"])
nth = o.groupby("customer_id")["amount"].nth(1)          # rows only for customers with 2+ orders
second = (o.loc[nth.index].set_index("customer_id")["amount"]
            .reindex(sorted(orders["customer_id"].unique())))   # bring back customers with one order
pd_df = second.rename("second_amount").reset_index()
# pd:end
# compared after sorting by customer_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\npandas nth(1) returned original row labels:", nth.index.tolist(), "-> customer 2 is missing from nth")

# iloc version: explicit about the short group
iloc = o.groupby("customer_id")["amount"].apply(lambda g: g.iloc[1] if len(g) > 1 else float("nan"))
pd.testing.assert_series_equal(iloc.reset_index(drop=True), pd_df["second_amount"], check_names=False, check_dtype=False)
print("pandas groupby.apply(iloc[1]) :", iloc.tolist())

# NTH_VALUE and nth(1) both count the NULL row; they do not skip it
print("customer 4 second order amount is NULL, not 55 (SQL):", sql_df.loc[sql_df["customer_id"] == 4, "second_amount"].tolist())

# not available in SQLite 3.45
for label, sql in [("FROM LAST", "SELECT NTH_VALUE(amount,2) FROM LAST OVER (ORDER BY order_id) FROM orders"),
                   ("IGNORE NULLS", "SELECT NTH_VALUE(amount,2) IGNORE NULLS OVER (ORDER BY order_id) FROM orders")]:
    try:
        con.execute(sql).fetchall()
        print(label, "ran")
    except Exception as e:
        print(label, "->", type(e).__name__, e)
print("asserts passed: SQL NTH_VALUE == pandas groupby().nth(1) after reindex == iloc[1]")
```

**Output (my run):**
```text
 customer_id  second_amount
           1          150.0
           2            NaN
           3           60.0
           4            NaN

default frame, customer 1 (row by row): [(1, 1, None), (2, 1, 150), (3, 1, 150)]

pandas nth(1) returned original row labels: [1, 5, 8] -> customer 2 is missing from nth
pandas groupby.apply(iloc[1]) : [150.0, nan, 60.0, nan]
customer 4 second order amount is NULL, not 55 (SQL): [nan]
FROM LAST -> OperationalError near "(": syntax error
IGNORE NULLS -> OperationalError near "NULLS": syntax error
asserts passed: SQL NTH_VALUE == pandas groupby().nth(1) after reindex == iloc[1]
```

**Edge cases:**
- Fewer than two orders: NULL in SQL; `nth(1)` simply has no row for that group (customer 2 is missing from the labels `[1, 5, 8]`), so reindexing creates NaN. The `iloc[1]` version needs an explicit length check.
- NULL second value: `NTH_VALUE` counts rows, it does not skip NULLs, so customer 4 gives NULL. `nth(1)` in pandas 3.0.5 also kept the NaN row (label 8 is in the `nth` output labels), unlike `first()` which skips NaN. SQLite has no `IGNORE NULLS`: my run gave `syntax error near "NULLS"`; `FROM LAST` also gave a syntax error. PostgreSQL does not implement either (per the Wave A sources note on the PostgreSQL documentation; I did not run PostgreSQL); some other engines do (not executed here).
- Ties on `order_date`: customer 3, handled by `order_id`.
- pandas `nth` return shape: in this version it returns rows labelled by the original index (the output's `[1, 5, 8]`), like a filter, not a frame indexed by group key, so I looked the rows up with `loc` and set the index to `customer_id`. This is the behaviour I observed on pandas 3.0.5; older versions returned a different index (from memory, not executed).

**Then explain:**
- Frame matters because `NTH_VALUE` looks inside the frame, not the partition. The default frame with `ORDER BY` ends at the current row (including peers), so early rows cannot see later values.
- `DISTINCT` is a shortcut because the value is identical on every row of a customer when the frame is the whole partition. Alternatives: `ROW_NUMBER() = 2` in a CTE (Part 4) or a correlated subquery.
- pandas: `nth(1)` is 0-based; SQL's `NTH_VALUE(x, 2)` is 1-based. `iloc[1]` is the same 0-based position.

**Follow-ups:**
- *Second-highest instead of second-earliest?* Order by amount descending (Part 4, ranking; ties then matter).
- *Last value?* Use `LAST_VALUE` with the full frame or `ORDER BY ... DESC` and `FIRST_VALUE`; SQLite has no `FROM LAST`.
- *Why NULL for customer 2 and not an error?* The function returns NULL when the frame has fewer rows than N.

**Common mistakes:**
- Forgetting the frame and getting NULL on the first row.
- Treating `NTH_VALUE(x, 2)` as 0-based.
- Not breaking date ties, so the "second" order changes between runs.
- Using `nth(1)` and not noticing that short groups disappear from the output.

### Q20 ⭐⭐ 🟢 Running max and running min, and drawdown: stock_prices(trade_date, close_price). Return each day's running maximum close (all-time high so far), the running minimum, and the drawdown from the running high as close / running_max - 1. Give pandas cummax(), cummin() and the drawdown calculation, and explain why an ordered MAX OVER is cumulative.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `MAX(close) OVER (ORDER BY date)` is a running maximum because the ordered window is cumulative, `MIN` likewise, and drawdown is `close / running_max - 1`, which is 0 at a new high and negative below it; pandas has `cummax()` and `cummin()`.

**Schema and sample data:** seven daily closes with a new high on 01-02 and on 01-05, and a tie with the old high on 01-07.
```sql
CREATE TABLE stock_prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO stock_prices VALUES ('2024-01-01',100),('2024-01-02',110),('2024-01-03',99),
  ('2024-01-04',90),('2024-01-05',121),('2024-01-06',108.9),('2024-01-07',121);
```

**SQL answer:** the CTE computes the running max and min once; the drawdown divides by the running max. `SQL_MAXDD` finds the worst drawdown day (earliest day on a tie).
```sql
WITH r AS (
  SELECT trade_date, close_price,
         MAX(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max,
         MIN(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_min
  FROM stock_prices
)
SELECT trade_date, close_price, running_max, running_min,
       ROUND(close_price / running_max - 1, 4) AS drawdown
FROM r
ORDER BY trade_date
```
```sql
WITH r AS (
  SELECT trade_date, close_price / MAX(close_price) OVER (ORDER BY trade_date
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) - 1 AS dd
  FROM stock_prices
)
SELECT trade_date, ROUND(dd, 4) AS max_drawdown FROM r ORDER BY dd, trade_date LIMIT 1
```

**pandas answer:**
```py
out = px.copy()
out["running_max"] = px["close_price"].cummax()
out["running_min"] = px["close_price"].cummin()
out["drawdown"] = (px["close_price"] / out["running_max"] - 1).round(4)
dd_row = out.loc[out["drawdown"].idxmin(), ["trade_date", "drawdown"]]
```

**Example:** closes 100, 110, 99, 90, 121, 108.9, 121.
- Running max: 100, 110, 110, 110, 121, 121, 121. Running min: 100, 100, 99, 90, 90, 90, 90.
- Drawdown: 100/100 - 1 = 0; 110/110 - 1 = 0; 99/110 - 1 = -0.1; 90/110 - 1 = -0.1818; 121/121 - 1 = 0; 108.9/121 - 1 = -0.1; 121/121 - 1 = 0.
- Worst drawdown: -0.1818 on 01-04 (rounded to 4 places).

**Code:** run with `python3 -I`.
```python
# Q20: running max, running min and drawdown
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE stock_prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO stock_prices VALUES ('2024-01-01',100),('2024-01-02',110),('2024-01-03',99),
  ('2024-01-04',90),('2024-01-05',121),('2024-01-06',108.9),('2024-01-07',121);
"""
SQL_MAIN = """
WITH r AS (
  SELECT trade_date, close_price,
         MAX(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max,
         MIN(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_min
  FROM stock_prices
)
SELECT trade_date, close_price, running_max, running_min,
       ROUND(close_price / running_max - 1, 4) AS drawdown
FROM r
ORDER BY trade_date
"""
SQL_MAXDD = """
WITH r AS (
  SELECT trade_date, close_price / MAX(close_price) OVER (ORDER BY trade_date
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) - 1 AS dd
  FROM stock_prices
)
SELECT trade_date, ROUND(dd, 4) AS max_drawdown FROM r ORDER BY dd, trade_date LIMIT 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
maxdd = con.execute(SQL_MAXDD).fetchone()
print("\nmax drawdown (SQL):", maxdd)

px = pd.read_sql_query("SELECT * FROM stock_prices ORDER BY trade_date", con)
# pd:main
out = px.copy()
out["running_max"] = px["close_price"].cummax()
out["running_min"] = px["close_price"].cummin()
out["drawdown"] = (px["close_price"] / out["running_max"] - 1).round(4)
dd_row = out.loc[out["drawdown"].idxmin(), ["trade_date", "drawdown"]]
# pd:end
# compared in trade_date order (both sorted by trade_date)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)
assert (dd_row["trade_date"], float(dd_row["drawdown"])) == maxdd
print("pandas max drawdown:", (dd_row["trade_date"], float(dd_row["drawdown"])))

# the ordered MAX OVER is cumulative; without ORDER BY it is the whole-partition max
print("MAX() OVER ()            :", [r[0] for r in con.execute("SELECT MAX(close_price) OVER () FROM stock_prices ORDER BY trade_date")])
print("MAX() OVER (ORDER BY ...):", [r[0] for r in con.execute("SELECT MAX(close_price) OVER (ORDER BY trade_date) FROM stock_prices ORDER BY trade_date")])

# duplicate dates: peers share the default frame, a unique tie-breaker makes it deterministic
con.executescript("""
CREATE TABLE px2(id INTEGER PRIMARY KEY, d TEXT, c REAL);
INSERT INTO px2 VALUES (1,'2024-01-01',100),(2,'2024-01-02',90),(3,'2024-01-02',130),(4,'2024-01-03',120);
""")
print("dup date, default frame running max by id:", [r[1] for r in con.execute(
    "SELECT id, MAX(c) OVER (ORDER BY d) FROM px2 ORDER BY id")])
print("dup date, ORDER BY d, id ROWS         :", [r[1] for r in con.execute(
    "SELECT id, MAX(c) OVER (ORDER BY d, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM px2 ORDER BY id")])

# NULL close: MAX ignores it, drawdown for that row is NULL; pandas cummax keeps NaN at that row
con.executescript("CREATE TABLE px3(d TEXT, c REAL); INSERT INTO px3 VALUES ('2024-01-01',100),('2024-01-02',NULL),('2024-01-03',80);")
print("NULL close, SQL running max :", [r[0] for r in con.execute(
    "SELECT MAX(c) OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM px3 ORDER BY d")])
print("NULL close, pandas cummax() :", pd.Series([100, None, 80], dtype="float64").cummax().tolist())
print("asserts passed: SQL running MAX/MIN/drawdown == pandas cummax/cummin")
```

**Output (my run):**
```text
trade_date  close_price  running_max  running_min  drawdown
2024-01-01        100.0        100.0        100.0    0.0000
2024-01-02        110.0        110.0        100.0    0.0000
2024-01-03         99.0        110.0         99.0   -0.1000
2024-01-04         90.0        110.0         90.0   -0.1818
2024-01-05        121.0        121.0         90.0    0.0000
2024-01-06        108.9        121.0         90.0   -0.1000
2024-01-07        121.0        121.0         90.0    0.0000

max drawdown (SQL): ('2024-01-04', -0.1818)
pandas max drawdown: ('2024-01-04', -0.1818)
MAX() OVER ()            : [121.0, 121.0, 121.0, 121.0, 121.0, 121.0, 121.0]
MAX() OVER (ORDER BY ...): [100.0, 110.0, 110.0, 110.0, 121.0, 121.0, 121.0]
dup date, default frame running max by id: [100.0, 130.0, 130.0, 130.0]
dup date, ORDER BY d, id ROWS         : [100.0, 100.0, 130.0, 130.0]
NULL close, SQL running max : [100.0, 100.0, 100.0]
NULL close, pandas cummax() : [100.0, nan, 100.0]
asserts passed: SQL running MAX/MIN/drawdown == pandas cummax/cummin
```

**Edge cases:**
- `MAX() OVER ()` without ORDER BY is the whole-table max (121.0 on every row in the output); `MAX() OVER (ORDER BY date)` is the cumulative one. That is the cumulative-versus-total difference the question asks about.
- Duplicate dates: the default frame treats rows with the same date as peers, so both get the same running max. In my test (ids 1-4, two rows on 01-02 with closes 90 and 130) the default frame gave 100, 130, 130, 130 for ids 1 to 4, while `ORDER BY d, id` with `ROWS` gave 100, 100, 130, 130. Use the tie-breaker when the date is not unique.
- NULL close: SQL `MAX` ignores the NULL, so the NULL row still shows the earlier max (100.0, 100.0, 100.0); pandas `cummax()` leaves NaN on that row (100.0, nan, 100.0). The drawdown for that day is NULL in SQL.
- Ties for the worst drawdown: my sample has none. By construction `ORDER BY dd, trade_date LIMIT 1` takes the earliest day, and pandas `idxmin` returns the first label with the minimum, so both would pick the earliest.
- First row: drawdown is 0 (close equals the running max).
- Rounding: `close/max - 1` is floating point, so I round to 4 places before asserting.

**Then explain:**
- Adding `ORDER BY` inside `OVER` makes the default frame "start of partition to current row (and peers)", so aggregates become running aggregates. I write the `ROWS` frame to be explicit and to avoid the peer effect.
- Drawdown measures how far below the all-time high so far you are; the maximum drawdown is the most negative value.
- All-time high so far uses only past data, so it is usable live; no look-ahead.

**Follow-ups:**
- *Reset the high every year?* `PARTITION BY` the year.
- *Max drawdown as a number?* `MIN(drawdown)` (here -0.1818), as in the second query.
- *Duration of the drawdown?* That needs gap/island logic (Part 7).

**Common mistakes:**
- Forgetting `ORDER BY` and returning the global max on every row.
- Dividing by the wrong thing (`close / first_close`, which is return, not drawdown).
- Using `max_close - close` and calling it a percentage.
- Reporting drawdown as positive on one side and negative on another.

### Q21 ⭐⭐ 🟡 Centered moving average: daily_sales(sale_date, amount). Return a 3-day centered average with ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING, show that the first and last rows only average two values, how to blank them (COUNT = 3 check), and give pandas rolling(3, center=True) with min_periods. Explain why centered averages cannot be used for forecasting or live dashboards (they look into the future).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `AVG(amount) OVER (ORDER BY d ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)` averages yesterday, today and tomorrow; at the first and last rows the frame has only two rows so it quietly averages two, which I blank with `CASE WHEN COUNT(amount) = 3`; pandas `rolling(3, center=True)` does the same, and it needs `min_periods=1` to match SQL's partial windows.

**Schema and sample data:** seven daily totals, one row per day.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',10),('2024-01-02',20),('2024-01-03',60),
  ('2024-01-04',40),('2024-01-05',50),('2024-01-06',90),('2024-01-07',30);
```

**SQL answer:** the named window `w` is reused three times. `SQL_TRAILING` (the usual backward-looking average) is in the Code block for the future-looking test.
```sql
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER w, 2) AS avg_available,
       COUNT(amount) OVER w AS n_in_window,
       CASE WHEN COUNT(amount) OVER w = 3 THEN ROUND(AVG(amount) OVER w, 2) END AS centered_avg
FROM daily_sales
WINDOW w AS (ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
ORDER BY sale_date
```

**pandas answer:**
```py
out = ds.copy()
out["avg_available"] = ds["amount"].rolling(3, center=True, min_periods=1).mean().round(2)
out["n_in_window"] = ds["amount"].rolling(3, center=True, min_periods=1).count().astype(int)
out["centered_avg"] = ds["amount"].rolling(3, center=True).mean().round(2)   # min_periods defaults to 3
```

**Example:** amounts 10, 20, 60, 40, 50, 90, 30.
- 01-01: window is only 01-01 and 01-02, (10 + 20) / 2 = 15.0 with 2 rows, so the centered value is blanked.
- 01-02: (10 + 20 + 60) / 3 = 30.0. 01-03: (20 + 60 + 40) / 3 = 40.0. 01-04: (60 + 40 + 50) / 3 = 50.0. 01-05: (40 + 50 + 90) / 3 = 60.0. 01-06: (50 + 90 + 30) / 3 = 56.67.
- 01-07: window is 01-06 and 01-07, (90 + 30) / 2 = 60.0 with 2 rows, blanked.

**Code:** run with `python3 -I`.
```python
# Q21: centered 3-day moving average
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',10),('2024-01-02',20),('2024-01-03',60),
  ('2024-01-04',40),('2024-01-05',50),('2024-01-06',90),('2024-01-07',30);
"""
SQL_MAIN = """
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER w, 2) AS avg_available,
       COUNT(amount) OVER w AS n_in_window,
       CASE WHEN COUNT(amount) OVER w = 3 THEN ROUND(AVG(amount) OVER w, 2) END AS centered_avg
FROM daily_sales
WINDOW w AS (ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
ORDER BY sale_date
"""
SQL_TRAILING = """
SELECT sale_date, ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS trailing_avg
FROM daily_sales ORDER BY sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
out = ds.copy()
out["avg_available"] = ds["amount"].rolling(3, center=True, min_periods=1).mean().round(2)
out["n_in_window"] = ds["amount"].rolling(3, center=True, min_periods=1).count().astype(int)
out["centered_avg"] = ds["amount"].rolling(3, center=True).mean().round(2)   # min_periods defaults to 3
# pd:end
# compared in sale_date order (both sorted by sale_date)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)

# looking into the future: change the LAST day only and see which rows move
before = pd.read_sql_query(SQL_MAIN, con)["centered_avg"]
trail_before = pd.read_sql_query(SQL_TRAILING, con)["trailing_avg"]
con.execute("UPDATE daily_sales SET amount = 300 WHERE sale_date = '2024-01-07'")
after = pd.read_sql_query(SQL_MAIN, con)["centered_avg"]
trail_after = pd.read_sql_query(SQL_TRAILING, con)["trailing_avg"]
changed_c = [d for d, b, a in zip(ds["sale_date"], before, after) if not (pd.isna(b) and pd.isna(a)) and b != a]
changed_t = [d for d, b, a in zip(ds["sale_date"], trail_before, trail_after) if b != a]
print("\nafter changing 2024-01-07 from 30 to 300:")
print("  centered average changed on:", changed_c)
print("  trailing average changed on :", changed_t)
print("asserts passed: SQL ROWS 1 PRECEDING..1 FOLLOWING == pandas rolling(3, center=True)")
```

**Output (my run):**
```text
 sale_date  amount  avg_available  n_in_window  centered_avg
2024-01-01      10          15.00            2           NaN
2024-01-02      20          30.00            3         30.00
2024-01-03      60          40.00            3         40.00
2024-01-04      40          50.00            3         50.00
2024-01-05      50          60.00            3         60.00
2024-01-06      90          56.67            3         56.67
2024-01-07      30          60.00            2           NaN

after changing 2024-01-07 from 30 to 300:
  centered average changed on: ['2024-01-06']
  trailing average changed on : ['2024-01-07']
asserts passed: SQL ROWS 1 PRECEDING..1 FOLLOWING == pandas rolling(3, center=True)
```

**Edge cases:**
- Ends: both ends average only two values. `COUNT(amount) = 3` (not `COUNT(*)`) is the safer check because a NULL amount inside the window should also make the average unreliable; `AVG` skips NULL and would silently average two values. I expect pandas with its default `min_periods` (3) to give NaN for a window containing a NaN, but I did not run that case.
- Ties and duplicates: `ROWS` counts rows, so duplicate dates would be treated as separate rows and a "3-day" average would span fewer days. The table has a primary key on the date; with duplicates, aggregate to one row per day first.
- Missing days: `ROWS` frames count rows, not days. A missing date makes the window span a longer time. Use a calendar or `RANGE` over day numbers for calendar windows (Part 5 Q24).
- Window size must be odd to be centered. With an even size pandas and SQL both need a choice of which side gets the extra row (not run here).
- One or two rows in total: the centered value is NULL everywhere.

**Then explain:**
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` is symmetric: one row on each side plus the current row.
- Why it cannot be used live: the value for day t needs day t+1. When I changed only the last day (30 to 300) the centered average changed on 01-06, a day before; the trailing average changed only on 01-07. That is the look-ahead. For a forecast or a live dashboard, use the trailing average, which depends on the past only.
- Centered averages are good for smoothing historical charts because they do not lag the data.

**Follow-ups:**
- *5-day centered?* `2 PRECEDING AND 2 FOLLOWING`, `COUNT = 5`; pandas `rolling(5, center=True)`.
- *Why not `RANGE`?* `RANGE` with an offset works on values (day numbers), not row counts; see Q24.
- *Why does the centered value change when future data arrives?* Because it uses it; the trailing one does not change when later rows arrive.

**Common mistakes:**
- Showing the two-value ends as if they were 3-day averages.
- Using a centered average as a model feature, leaking the future into training.
- Using `COUNT(*)` and missing NULL gaps.
- Assuming rows equal days.

### Q22 ⭐⭐ 🟡 Inventory running stock: inventory_moves(move_id, sku, move_date, qty_in, qty_out). Return the running stock per sku after each move, flag the first move where stock drops below a reorder level of 10, and list SKUs that ever went negative. Use signed quantities, SUM() OVER (PARTITION BY sku ORDER BY move_date, move_id) and a MIN OVER check, with the pandas groupby cumsum version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Turn each move into a signed quantity (`COALESCE(qty_in,0) - COALESCE(qty_out,0)`), take `SUM() OVER (PARTITION BY sku ORDER BY move_date, move_id)` for the stock after each move, flag the first row whose stock is below 10 with a running count of "below 10" rows equal to 1, and list SKUs where the minimum running stock is negative.

**Schema and sample data:** three SKUs, eleven moves. NULL in `qty_in` or `qty_out` means "none". SKU C has an in and an out on the same date.
```sql
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_in INTEGER, qty_out INTEGER);
INSERT INTO inventory_moves VALUES
  (1,'A','2024-01-01',50,NULL),(2,'A','2024-01-03',NULL,20),(3,'A','2024-01-05',NULL,25),
  (4,'A','2024-01-07',30,NULL),(5,'A','2024-01-09',NULL,28),
  (6,'B','2024-01-02',10,NULL),(7,'B','2024-01-04',NULL,12),(8,'B','2024-01-06',20,NULL),
  (9,'C','2024-01-01',5,NULL),(10,'C','2024-01-01',NULL,2),(11,'C','2024-01-02',20,NULL);
```

**SQL answer:** tie rule: `move_date, move_id`. `SQL_NEG` lists SKUs that ever went negative by taking `MIN` of the running stock.
```sql
WITH s AS (
  SELECT move_id, sku, move_date,
         COALESCE(qty_in, 0) - COALESCE(qty_out, 0) AS delta,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
), f AS (
  SELECT *, SUM(CASE WHEN stock < 10 THEN 1 ELSE 0 END)
              OVER (PARTITION BY sku ORDER BY move_date, move_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS below_so_far
  FROM s
)
SELECT move_id, sku, move_date, delta, stock,
       CASE WHEN stock < 10 AND below_so_far = 1 THEN 1 ELSE 0 END AS first_below_10
FROM f
ORDER BY sku, move_date, move_id
```
```sql
WITH s AS (
  SELECT sku,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
)
SELECT sku, MIN(stock) AS min_stock FROM s GROUP BY sku HAVING MIN(stock) < 0 ORDER BY sku
```

**pandas answer:** same signed delta, `groupby().cumsum()`, and the first flag by counting below-10 rows per SKU.
```py
m = moves.sort_values(["sku", "move_date", "move_id"]).copy()
m["delta"] = m["qty_in"].fillna(0) - m["qty_out"].fillna(0)
m["stock"] = m.groupby("sku")["delta"].cumsum()
below = m["stock"] < 10
m["first_below_10"] = (below & (below.groupby(m["sku"]).cumsum() == 1)).astype(int)
pd_df = m[["move_id", "sku", "move_date", "delta", "stock", "first_below_10"]]
neg = m.groupby("sku")["stock"].min()
pd_neg = neg[neg < 0].rename("min_stock").reset_index()
```

**Example:**
- SKU A: +50 = 50, -20 = 30, -25 = 5 (first below 10, flagged), +30 = 35, -28 = 7 (below 10 again, but not the first).
- SKU B: +10 = 10 (not below 10: the test is `< 10`), -12 = -2 (first below 10 and negative), +20 = 18. B is the negative SKU, minimum -2.
- SKU C: +5 = 5 on the first move (already below 10, so the first move is flagged), -2 = 3, +20 = 23.

**Code:** run with `python3 -I`.
```python
# Q22: running stock per SKU, first move below the reorder level, SKUs that went negative
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_in INTEGER, qty_out INTEGER);
INSERT INTO inventory_moves VALUES
  (1,'A','2024-01-01',50,NULL),(2,'A','2024-01-03',NULL,20),(3,'A','2024-01-05',NULL,25),
  (4,'A','2024-01-07',30,NULL),(5,'A','2024-01-09',NULL,28),
  (6,'B','2024-01-02',10,NULL),(7,'B','2024-01-04',NULL,12),(8,'B','2024-01-06',20,NULL),
  (9,'C','2024-01-01',5,NULL),(10,'C','2024-01-01',NULL,2),(11,'C','2024-01-02',20,NULL);
"""
SQL_MAIN = """
WITH s AS (
  SELECT move_id, sku, move_date,
         COALESCE(qty_in, 0) - COALESCE(qty_out, 0) AS delta,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
), f AS (
  SELECT *, SUM(CASE WHEN stock < 10 THEN 1 ELSE 0 END)
              OVER (PARTITION BY sku ORDER BY move_date, move_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS below_so_far
  FROM s
)
SELECT move_id, sku, move_date, delta, stock,
       CASE WHEN stock < 10 AND below_so_far = 1 THEN 1 ELSE 0 END AS first_below_10
FROM f
ORDER BY sku, move_date, move_id
"""
SQL_NEG = """
WITH s AS (
  SELECT sku,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
)
SELECT sku, MIN(stock) AS min_stock FROM s GROUP BY sku HAVING MIN(stock) < 0 ORDER BY sku
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_neg = pd.read_sql_query(SQL_NEG, con)
print(sql_df.to_string(index=False))
print("\nSKUs that ever went negative:"); print(sql_neg.to_string(index=False))

moves = pd.read_sql_query("SELECT * FROM inventory_moves", con)
# pd:main
m = moves.sort_values(["sku", "move_date", "move_id"]).copy()
m["delta"] = m["qty_in"].fillna(0) - m["qty_out"].fillna(0)
m["stock"] = m.groupby("sku")["delta"].cumsum()
below = m["stock"] < 10
m["first_below_10"] = (below & (below.groupby(m["sku"]).cumsum() == 1)).astype(int)
pd_df = m[["move_id", "sku", "move_date", "delta", "stock", "first_below_10"]]
neg = m.groupby("sku")["stock"].min()
pd_neg = neg[neg < 0].rename("min_stock").reset_index()
# pd:end
# compared after sorting by sku, move_date, move_id
pd.testing.assert_frame_equal(sql_df, pd_df.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_neg, pd_neg, check_dtype=False)

# alternative reading of "drops below": a crossing from >= 10 to < 10 (SKU C starts below, so it never crosses)
cross = m.assign(prev=m.groupby("sku")["stock"].shift())
crossing = cross[(cross["stock"] < 10) & (cross["prev"] >= 10)][["move_id", "sku"]]
print("\ncrossing-based flag (prev >= 10 and now < 10), all crossings:", crossing.values.tolist())
print("first_below_10 flags:", sql_df.loc[sql_df["first_below_10"] == 1, ["move_id", "sku"]].values.tolist())
# tie rule matters: SKU C has an in and an out on the same date
alt = con.execute(SQL_NEG.replace("ORDER BY move_date, move_id", "ORDER BY move_date, move_id DESC")).fetchall()
print("with ties ordered move_id DESC the negative SKUs become:", alt)
print("asserts passed: SQL windows == pandas groupby cumsum")
```

**Output (my run):**
```text
 move_id sku  move_date  delta  stock  first_below_10
       1   A 2024-01-01     50     50               0
       2   A 2024-01-03    -20     30               0
       3   A 2024-01-05    -25      5               1
       4   A 2024-01-07     30     35               0
       5   A 2024-01-09    -28      7               0
       6   B 2024-01-02     10     10               0
       7   B 2024-01-04    -12     -2               1
       8   B 2024-01-06     20     18               0
       9   C 2024-01-01      5      5               1
      10   C 2024-01-01     -2      3               0
      11   C 2024-01-02     20     23               0

SKUs that ever went negative:
sku  min_stock
  B         -2

crossing-based flag (prev >= 10 and now < 10), all crossings: [[3, 'A'], [5, 'A'], [7, 'B']]
first_below_10 flags: [[3, 'A'], [7, 'B'], [9, 'C']]
with ties ordered move_id DESC the negative SKUs become: [('B', -2), ('C', -2)]
asserts passed: SQL windows == pandas groupby cumsum
```

**Edge cases:**
- Definition of "first move where stock drops below 10": I flag the first move whose stock after the move is below 10 (SKU C starts below, so it is flagged on move 9). If you want only crossings from 10 or above to below 10, the code also prints that variant: it flags moves 3 and 5 for A and 7 for B, and never flags C. Both readings are defensible; say which one you use.
- Same-date moves: the order matters. For SKU C the in (move 9) and out (move 10) share a date. With `move_id ASC` the stock never goes negative; when I reversed the tie order (`move_id DESC`) the out came first and C appeared as negative (minimum -2) in the SKU list as well as B. A real system should order by a timestamp or sequence number.
- NULL quantities: `COALESCE` to 0 before subtracting; otherwise `NULL - 20` is NULL and the running sum skips that move. In pandas `fillna(0)` does the same.
- Exactly 10: not below the reorder level (SKU B's first move).
- SKU with no moves: no rows, so it cannot appear; join to a SKU table for that.
- Opening stock is assumed to be 0: add an opening-balance row if it is not.

**Then explain:**
- Signed quantities turn a two-column in/out ledger into one number so a single running `SUM` works.
- "First time" = the running count of flagged rows equals 1 at a flagged row. Windows cannot be nested, so the stock window is in one CTE and the count of below-10 rows in the next.
- "Ever negative" is a `MIN` over the running stock, either `MIN() OVER (PARTITION BY sku)` or a `GROUP BY sku HAVING MIN(stock) < 0` over the CTE (the second form is in the code).
- pandas: `below.groupby(m["sku"]).cumsum() == 1` is the same running count; `groupby("sku")["stock"].min()` is the negative check.

**Follow-ups:**
- *When did each SKU first go negative?* Same trick with `stock < 0` instead of `< 10`.
- *Per warehouse too?* Add warehouse to `PARTITION BY`.
- *Days below the reorder level?* That is a streak problem (Part 7).

**Common mistakes:**
- Not ordering ties, so the stock order of same-day moves changes.
- Not handling NULL quantities.
- Using `<= 10` when the rule says below 10.
- Flagging every row below 10 rather than the first.

### Q23 ⭐⭐ 🟡 Year-over-year change: monthly_sales(month, revenue) where month is a text like '2024-03', with 24 consecutive months of data. Compute the YoY percent change with LAG(revenue, 12) and with a self-join on the same month a year earlier, and explain that LAG(12) is correct only when no month is missing (and when each month has exactly one row). Give pandas shift(12) and pct_change(12), and state what both return for the first 12 months.
**Asked at:** LearnSQL revenue-growth and Craig Kerstiens month-over-month blog write-ups (LAG, percent change, gaps break LAG, divide by zero), guides and not candidate reports; analyst screens at product companies and startups
**Say this first (1 line):** `LAG(revenue, 12) OVER (ORDER BY month)` fetches the row 12 rows back, which is the same month last year only when there are exactly 24 consecutive months with one row each; the self-join on "the same month minus one year" is safe against gaps and I show both.

**Schema and sample data:** 24 months, 2023-11 is deliberately 0 so the zero-base case shows up.
```sql
CREATE TABLE monthly_sales(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_sales VALUES
  ('2023-01',100),('2023-02',110),('2023-03',120),('2023-04',130),('2023-05',140),('2023-06',150),
  ('2023-07',160),('2023-08',170),('2023-09',180),('2023-10',190),('2023-11',0),('2023-12',210),
  ('2024-01',120),('2024-02',121),('2024-03',150),('2024-04',143),('2024-05',126),('2024-06',165),
  ('2024-07',176),('2024-08',170),('2024-09',162),('2024-10',228),('2024-11',220),('2024-12',252);
```

**SQL answer:** `LAG(12)` version, then the self-join (a LEFT JOIN so the first year is kept with NULLs).
```sql
SELECT month, revenue, LAG(revenue, 12) OVER (ORDER BY month) AS prev_year,
       ROUND((revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0), 2) AS yoy_pct
FROM monthly_sales
ORDER BY month
```
```sql
SELECT c.month, c.revenue, p.revenue AS prev_year,
       ROUND((c.revenue - p.revenue) * 100.0 / NULLIF(p.revenue, 0), 2) AS yoy_pct
FROM monthly_sales c
LEFT JOIN monthly_sales p
  ON p.month = (CAST(substr(c.month, 1, 4) AS INTEGER) - 1) || substr(c.month, 5)
ORDER BY c.month
```

**pandas answer:** `shift(12)` for the previous-year value, `pct_change(12)` for the ratio (inf where the base is 0, replaced by NaN to match `NULLIF`).
```py
s = ms.set_index("month")["revenue"]
pd_df = pd.DataFrame({"revenue": s, "prev_year": s.shift(12)})
pd_df["yoy_pct"] = (s.pct_change(12) * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
```

**Example:**
- 2024-01: 120 versus 2023-01: 100 gives +20.0%. 2024-03: 150 versus 120 gives +25.0%. 2024-05: 126 versus 140 gives -10.0%. 2024-08: 170 versus 170 gives 0.0%.
- 2024-11: the base 2023-11 is 0, so the percent is undefined: NULL (`NULLIF`).
- 2023-01 to 2023-12: there are no rows 12 months back, so `prev_year` and the percent are NULL (NaN in pandas), 12 rows in total.

**Code:** run with `python3 -I`.
```python
# Q23: year-over-year change with LAG(12), a self-join, and pandas shift(12) / pct_change(12)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_sales(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_sales VALUES
  ('2023-01',100),('2023-02',110),('2023-03',120),('2023-04',130),('2023-05',140),('2023-06',150),
  ('2023-07',160),('2023-08',170),('2023-09',180),('2023-10',190),('2023-11',0),('2023-12',210),
  ('2024-01',120),('2024-02',121),('2024-03',150),('2024-04',143),('2024-05',126),('2024-06',165),
  ('2024-07',176),('2024-08',170),('2024-09',162),('2024-10',228),('2024-11',220),('2024-12',252);
"""

SQL_MAIN = """
SELECT month, revenue, LAG(revenue, 12) OVER (ORDER BY month) AS prev_year,
       ROUND((revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0), 2) AS yoy_pct
FROM monthly_sales
ORDER BY month
"""
SQL_JOIN = """
SELECT c.month, c.revenue, p.revenue AS prev_year,
       ROUND((c.revenue - p.revenue) * 100.0 / NULLIF(p.revenue, 0), 2) AS yoy_pct
FROM monthly_sales c
LEFT JOIN monthly_sales p
  ON p.month = (CAST(substr(c.month, 1, 4) AS INTEGER) - 1) || substr(c.month, 5)
ORDER BY c.month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
join_df = pd.read_sql_query(SQL_JOIN, con)
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, join_df, check_dtype=False)
print("\nLAG(12) and self-join agree on all 24 rows")

ms = pd.read_sql_query("SELECT * FROM monthly_sales ORDER BY month", con)
# pd:main
s = ms.set_index("month")["revenue"]
pd_df = pd.DataFrame({"revenue": s, "prev_year": s.shift(12)})
pd_df["yoy_pct"] = (s.pct_change(12) * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
# pd:end
# compared in month order (both sorted by month)
pd.testing.assert_frame_equal(sql_df.set_index("month"), pd_df, check_dtype=False)
print("pandas first 12 prev_year:", pd_df["prev_year"].head(12).isna().all(), "| first 12 yoy_pct all NaN:", pd_df["yoy_pct"].head(12).isna().all())
print("raw pct_change(12) on 2024-11 (base 0):", (s.pct_change(12) * 100).loc["2024-11"])

# a missing month and a duplicated month break LAG(12) and shift(12), not the self-join
con.executescript("""
CREATE TABLE gap(month TEXT, revenue INTEGER);
INSERT INTO gap SELECT month, revenue FROM monthly_sales WHERE month <> '2023-03';
CREATE TABLE dup(month TEXT, revenue INTEGER);
INSERT INTO dup SELECT month, revenue FROM monthly_sales;
INSERT INTO dup VALUES ('2023-05', 1);
""")
JOIN_TMPL = """SELECT c.month, p.revenue FROM {t} c
               LEFT JOIN {t} p ON p.month = (CAST(substr(c.month, 1, 4) AS INTEGER) - 1) || substr(c.month, 5)
               WHERE c.month LIKE '2024-%' ORDER BY c.month, p.revenue"""
LAG_TMPL = """SELECT month, LAG(revenue, 12) OVER (ORDER BY month, revenue) FROM {t}
              ORDER BY month, revenue"""
for name in ("gap", "dup"):
    lag24 = [(m, v) for m, v in con.execute(LAG_TMPL.format(t=name)) if m.startswith("2024-")]
    jn24 = con.execute(JOIN_TMPL.format(t=name)).fetchall()
    print(f"\ntable {name}: LAG(12) 2024 rows:", [v for _, v in lag24])
    print(f"table {name}: self-join 2024 rows:", [v for _, v in jn24], "(" + str(len(jn24)) + " rows)")
g = pd.read_sql_query("SELECT * FROM gap ORDER BY month", con)
gs = g.set_index("month")["revenue"]
print("\npandas shift(12) on the gap table, 2024-03 sees:", gs.shift(12).loc["2024-03"], "(true 2023-03 is missing; 2023-02 is", gs.loc["2023-02"], ")")
p = gs.copy()
p.index = pd.PeriodIndex(p.index, freq="M")
prev_year = p.set_axis(p.index + 12).reindex(p.index)
print("pandas PeriodIndex calendar shift, 2024-03 sees:", prev_year.loc["2024-03"], "(NaN: no row a year earlier)")
print("SQLite 1.0/0 gives", con.execute("SELECT 1.0/0").fetchone()[0])
print("asserts passed: SQL LAG(12) == self-join == pandas shift(12)/pct_change(12) on the clean 24 months")
```

**Output (my run):**
```text
  month  revenue  prev_year  yoy_pct
2023-01      100        NaN      NaN
2023-02      110        NaN      NaN
2023-03      120        NaN      NaN
2023-04      130        NaN      NaN
2023-05      140        NaN      NaN
2023-06      150        NaN      NaN
2023-07      160        NaN      NaN
2023-08      170        NaN      NaN
2023-09      180        NaN      NaN
2023-10      190        NaN      NaN
2023-11        0        NaN      NaN
2023-12      210        NaN      NaN
2024-01      120      100.0     20.0
2024-02      121      110.0     10.0
2024-03      150      120.0     25.0
2024-04      143      130.0     10.0
2024-05      126      140.0    -10.0
2024-06      165      150.0     10.0
2024-07      176      160.0     10.0
2024-08      170      170.0      0.0
2024-09      162      180.0    -10.0
2024-10      228      190.0     20.0
2024-11      220        0.0      NaN
2024-12      252      210.0     20.0

LAG(12) and self-join agree on all 24 rows
pandas first 12 prev_year: True | first 12 yoy_pct all NaN: True
raw pct_change(12) on 2024-11 (base 0): inf

table gap: LAG(12) 2024 rows: [None, 100, 110, 130, 140, 150, 160, 170, 180, 190, 0, 210]
table gap: self-join 2024 rows: [100, 110, None, 130, 140, 150, 160, 170, 180, 190, 0, 210] (12 rows)

table dup: LAG(12) 2024 rows: [110, 120, 130, 1, 140, 150, 160, 170, 180, 190, 0, 210]
table dup: self-join 2024 rows: [100, 110, 120, 130, 1, 140, 150, 160, 170, 180, 190, 0, 210] (13 rows)

pandas shift(12) on the gap table, 2024-03 sees: 110.0 (true 2023-03 is missing; 2023-02 is 110 )
pandas PeriodIndex calendar shift, 2024-03 sees: nan (NaN: no row a year earlier)
SQLite 1.0/0 gives None
asserts passed: SQL LAG(12) == self-join == pandas shift(12)/pct_change(12) on the clean 24 months
```

**Edge cases:**
- First 12 months: NULL in SQL, NaN in pandas for both `shift(12)` and `pct_change(12)`; the output shows all 12 are NaN.
- Zero base: SQL with `NULLIF` returns NULL; pandas gave `inf` (raw value printed in the output) and I replaced it with NaN. Without `NULLIF`, SQLite also returns NULL for division by zero; other engines may raise an error (not executed here).
- Missing month: I removed 2023-03 to make a 23-row table. `LAG(12)` then returned NULL for 2024-01 (the right answer is 100), 100 for 2024-02 (right: 110) and 110 for 2024-03 (right: NULL, since 2023-03 has no row). From 2024-04 onward it re-aligned. The self-join returned the right values. pandas `shift(12)` on the same table gave 110.0 for 2024-03, which is 2023-02's value; a `PeriodIndex` shifted by 12 months gave NaN, the correct answer.
- Duplicate month: I added a second 2023-05 row (revenue 1). `LAG(12)` shifted every later row by one (for example 2024-01 got 110 instead of 100), and the self-join returned 13 rows for the 12 months of 2024 because 2024-05 matched both 2023-05 rows. Fix: aggregate to one row per month first.
- Ties: with duplicate months I ordered by `month, revenue` to make `LAG` deterministic; the right fix is still to remove the duplicates.
- Text months: `'2024-03'` sorts correctly as text. The self-join builds the previous year with `(CAST(substr(month,1,4) AS INTEGER) - 1) || substr(month,5)`.

**Then explain:**
- `LAG(x, 12)` is positional, like in Q13 and Q16: correct only if the rows are a complete, unique monthly series.
- The join is calendar-based. It needs an index on `month` to be fast on large tables (not timed here).
- pandas `shift(12)` and `pct_change(12)` are positional too. On a datetime or period index, shift the index (for example `PeriodIndex + 12`) and align, which is the join.
- State the first-year result plainly: no prior year, so no YoY value; do not fill with 0.

**Follow-ups:**
- *Month-over-month on the same table?* `LAG(revenue)` and the same gap caveat (Q16).
- *YoY for quarterly or daily data?* Change the offset (4 or 365 rows is only right with complete data; for days, leap years also break a 365-row shift).
- *Percent or percentage points?* Percent change here; for rates, subtract.

**Common mistakes:**
- Using `LAG(12)` on a gappy or duplicated table.
- Dividing by a zero base.
- Comparing months as text arithmetic.
- Reporting the first year as 0% growth.
