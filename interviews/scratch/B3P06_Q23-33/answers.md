### Q23 ⭐⭐ 🟡 Cancellation rate by day (the LeetCode 262 pattern, Trips and Users): trips(id, client_id, driver_id, status, request_at) and users(user_id, banned, role). For request dates between 2013-10-01 and 2013-10-03 return the cancellation rate per day counting only trips whose client and driver are both unbanned, rounded to 2 decimals. Show the date filter (half-open on a timestamp), the double join to users, conditional aggregation, and a day with no trips (absent versus rate 0 versus NULL).
**Asked at:** public LeetCode-style problem bank (550 Game Play Analysis IV, 1193 Monthly Transactions I, 197 Rising Temperature and 262 Trips and Users known from search snippets and third-party write-ups, statements not opened), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Filter trips to the date range with a half-open timestamp range, inner-join `users` twice (client and driver, both `banned = 'No'`), then take `SUM(status <> 'completed') / COUNT(*)` per day; a day with no qualifying trips simply has no row, which is a choice I state (absent, 0 or NULL) rather than leave to the join.

**Schema and sample data:** two banned users (client 2, driver 13); `request_at` is a full timestamp so the date-filter trap is real. Date convention: the day is the first 10 characters of `request_at` as stored, no time-zone conversion (week start is not used in this question).
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, banned TEXT, role TEXT);
CREATE TABLE trips(id INTEGER PRIMARY KEY, client_id INTEGER, driver_id INTEGER,
                   status TEXT, request_at TEXT);
INSERT INTO users VALUES (1,'No','client'),(2,'Yes','client'),(3,'No','client'),(4,'No','client'),
  (10,'No','driver'),(11,'No','driver'),(12,'No','driver'),(13,'Yes','driver');
INSERT INTO trips VALUES
 (1,1,10,'completed','2013-10-01 08:00:00'),
 (2,2,11,'cancelled_by_driver','2013-10-01 09:00:00'),
 (3,3,12,'completed','2013-10-01 10:00:00'),
 (4,4,13,'cancelled_by_client','2013-10-01 11:00:00'),
 (5,1,11,'cancelled_by_client','2013-10-01 12:00:00'),
 (6,2,10,'cancelled_by_driver','2013-10-02 09:00:00'),
 (7,4,13,'completed','2013-10-02 10:00:00'),
 (8,3,12,'completed','2013-10-03 10:00:00'),
 (9,1,10,'cancelled_by_driver','2013-10-03 23:30:00'),
 (10,3,11,'completed','2013-10-04 09:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block, with `:lo` and `:hi` as parameters. The window is `request_at >= :lo AND request_at < date(:hi, '+1 day')`, so a trip at 23:30 on the last day is kept. `SQL_SPINE` adds a day spine to show the three options for an empty day.
```sql
SELECT substr(t.request_at, 1, 10) AS day,
       ROUND(1.0 * SUM(CASE WHEN t.status <> 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No' AND c.role = 'client'
JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No' AND d.role = 'driver'
WHERE t.request_at >= :lo AND t.request_at < date(:hi, '+1 day')
GROUP BY substr(t.request_at, 1, 10)
ORDER BY day
```

**pandas answer:** the same filter with Timestamps, `isin` on the unbanned client and driver ids, then the mean of a boolean (cancelled) per day. This is the `cancel_rate` function in the Code block; the key lines are:
```py
    ok_c = users.loc[(users["banned"] == "No") & (users["role"] == "client"), "user_id"]
    ok_d = users.loc[(users["banned"] == "No") & (users["role"] == "driver"), "user_id"]
    t = t[t["client_id"].isin(ok_c) & t["driver_id"].isin(ok_d)]
    g = t.assign(day=t["request_at"].dt.strftime("%Y-%m-%d"),
                 cancelled=(t["status"] != "completed")).groupby("day")["cancelled"].mean().round(2)
```

**Example:** banned: client 2 and driver 13. 2013-10-01: trips 1, 3 and 5 qualify (trip 2 has banned client 2, trip 4 has banned driver 13); 1 of 3 is cancelled (trip 5), so 1/3 = 0.33. 2013-10-02: trip 6 has banned client 2 and trip 7 has banned driver 13, so nothing qualifies and the day has no row. 2013-10-03: trip 8 completed, trip 9 (23:30) cancelled by the driver, so 1/2 = 0.50. Trip 10 on 2013-10-04 is outside the window.

**Code:** run with `python3 -I`.
```python
# Q23: cancellation rate by day (LeetCode 262 pattern), SQL vs pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, banned TEXT, role TEXT);
CREATE TABLE trips(id INTEGER PRIMARY KEY, client_id INTEGER, driver_id INTEGER,
                   status TEXT, request_at TEXT);
INSERT INTO users VALUES (1,'No','client'),(2,'Yes','client'),(3,'No','client'),(4,'No','client'),
  (10,'No','driver'),(11,'No','driver'),(12,'No','driver'),(13,'Yes','driver');
INSERT INTO trips VALUES
 (1,1,10,'completed','2013-10-01 08:00:00'),
 (2,2,11,'cancelled_by_driver','2013-10-01 09:00:00'),
 (3,3,12,'completed','2013-10-01 10:00:00'),
 (4,4,13,'cancelled_by_client','2013-10-01 11:00:00'),
 (5,1,11,'cancelled_by_client','2013-10-01 12:00:00'),
 (6,2,10,'cancelled_by_driver','2013-10-02 09:00:00'),
 (7,4,13,'completed','2013-10-02 10:00:00'),
 (8,3,12,'completed','2013-10-03 10:00:00'),
 (9,1,10,'cancelled_by_driver','2013-10-03 23:30:00'),
 (10,3,11,'completed','2013-10-04 09:00:00');
"""
SQL_MAIN = """
SELECT substr(t.request_at, 1, 10) AS day,
       ROUND(1.0 * SUM(CASE WHEN t.status <> 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancellation_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No' AND c.role = 'client'
JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No' AND d.role = 'driver'
WHERE t.request_at >= :lo AND t.request_at < date(:hi, '+1 day')
GROUP BY substr(t.request_at, 1, 10)
ORDER BY day
"""
SQL_BETWEEN = """
SELECT substr(request_at, 1, 10) AS day, COUNT(*) AS trips
FROM trips WHERE request_at BETWEEN :lo AND :hi GROUP BY 1 ORDER BY 1
"""
SQL_SPINE = """
WITH RECURSIVE days(day) AS (
  SELECT :lo UNION ALL SELECT date(day, '+1 day') FROM days WHERE day < :hi
), ok AS (
  SELECT substr(t.request_at, 1, 10) AS day, t.status
  FROM trips t
  JOIN users c ON c.user_id = t.client_id AND c.banned = 'No' AND c.role = 'client'
  JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No' AND d.role = 'driver'
)
SELECT days.day, COUNT(ok.day) AS trips,
       ROUND(1.0 * SUM(CASE WHEN ok.status <> 'completed' THEN 1 ELSE 0 END) / NULLIF(COUNT(ok.day), 0), 2) AS rate_null,
       COALESCE(ROUND(1.0 * SUM(CASE WHEN ok.status <> 'completed' THEN 1 ELSE 0 END) / NULLIF(COUNT(ok.day), 0), 2), 0) AS rate_zero
FROM days LEFT JOIN ok ON ok.day = days.day
GROUP BY days.day ORDER BY days.day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"lo": "2013-10-01", "hi": "2013-10-03"}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print("SQL (2013-10-01..2013-10-03):")
print(sql_df.to_string(index=False))
print("BETWEEN '2013-10-01' AND '2013-10-03' trips per day (drops the 23:30 trip on 10-03):")
print(pd.read_sql_query(SQL_BETWEEN, con, params=P).to_string(index=False))
print("SQL with day spine (absent day -> NULL or 0):")
print(pd.read_sql_query(SQL_SPINE, con, params=P).to_string(index=False))
print("same SQL, window widened to 2013-10-04:")
print(pd.read_sql_query(SQL_MAIN, con, params={"lo": "2013-10-01", "hi": "2013-10-04"}).to_string(index=False))

trips = pd.read_sql_query("SELECT * FROM trips", con)
users = pd.read_sql_query("SELECT * FROM users", con)

def cancel_rate(trips, users, lo, hi):
    t = trips.assign(request_at=pd.to_datetime(trips["request_at"]))
    t = t[(t["request_at"] >= pd.Timestamp(lo)) & (t["request_at"] < pd.Timestamp(hi) + pd.Timedelta(days=1))]
    ok_c = users.loc[(users["banned"] == "No") & (users["role"] == "client"), "user_id"]
    ok_d = users.loc[(users["banned"] == "No") & (users["role"] == "driver"), "user_id"]
    t = t[t["client_id"].isin(ok_c) & t["driver_id"].isin(ok_d)]
    g = t.assign(day=t["request_at"].dt.strftime("%Y-%m-%d"),
                 cancelled=(t["status"] != "completed")).groupby("day")["cancelled"].mean().round(2)
    return g.reset_index(name="cancellation_rate")

pd_df = cancel_rate(trips, users, "2013-10-01", "2013-10-03")
# compared after sorting by day
assert pd_df.sort_values("day").reset_index(drop=True).equals(sql_df.sort_values("day").reset_index(drop=True)), (pd_df, sql_df)
wide = pd.read_sql_query(SQL_MAIN, con, params={"lo": "2013-10-01", "hi": "2013-10-04"})
assert cancel_rate(trips, users, "2013-10-01", "2013-10-04").equals(wide)
print("pandas:")
print(pd_df.to_string(index=False))
print("asserts passed: SQL == pandas for both windows")
```

**Output (my run):**
```text
SQL (2013-10-01..2013-10-03):
       day  cancellation_rate
2013-10-01               0.33
2013-10-03               0.50
BETWEEN '2013-10-01' AND '2013-10-03' trips per day (drops the 23:30 trip on 10-03):
       day  trips
2013-10-01      5
2013-10-02      2
SQL with day spine (absent day -> NULL or 0):
       day  trips  rate_null  rate_zero
2013-10-01      3       0.33       0.33
2013-10-02      0        NaN       0.00
2013-10-03      2       0.50       0.50
same SQL, window widened to 2013-10-04:
       day  cancellation_rate
2013-10-01               0.33
2013-10-03               0.50
2013-10-04               0.00
pandas:
       day  cancellation_rate
2013-10-01               0.33
2013-10-03               0.50
asserts passed: SQL == pandas for both windows
```

**Edge cases:**
- Day with no qualifying trips (2013-10-02): the plain `GROUP BY` returns no row at all. With a day spine and `LEFT JOIN`, `COUNT(ok.day)` is 0 and the rate is NULL because I divide by `NULLIF(COUNT(...), 0)`; wrapping it in `COALESCE(..., 0)` gives 0.00, which says "nothing was cancelled" when the truth is "nothing happened". Which one to show is a reporting decision; I would show NULL (or a blank) and keep the trip count next to it.
- A day that does exist but has no cancellations is a real 0.00. In my run that day appears when I widen the window to 2013-10-04 (one completed trip, rate 0.00); that is the difference between "rate 0" and "no row".
- `BETWEEN '2013-10-01' AND '2013-10-03'` on a timestamp column drops the whole of 2013-10-03 (both the 10:00 and the 23:30 trips), because every time on that day is greater than the bare date string `'2013-10-03'`. The second printed table shows trips per day with that filter: 10-03 is missing.
- Rounding: SQLite `ROUND(x, 2)` and pandas `.round(2)` returned the same values here; I compared the rounded results with `equals`. If you compare unrounded floats, use a tolerance.
- Orphans: a trip whose client or driver id is missing from `users` is dropped by the inner joins, and by `isin` in pandas; a `LEFT JOIN` with `banned IS NULL` would keep it, so decide whether unknown users count as unbanned.
- Roles: I also test `role = 'client'` and `role = 'driver'` on the joins. If ids are unique across roles (as in the public problem, as I remember it) this is redundant but protects against a driver id being used as a client id.

**Then explain:**
- The two joins to `users` are inner joins, so the ban rule is also the filter; putting `banned = 'No'` in `ON` or in `WHERE` gives the same rows for inner joins.
- Conditional aggregation: `SUM(CASE WHEN status <> 'completed' THEN 1 ELSE 0 END)` counts both cancellation statuses; `1.0 *` forces float division in SQLite (integer division would give 0).
- Half-open range: `>= lo AND < next day` works for dates, timestamps with fractions, and composes with the next window; it also lets an index on `request_at` be used (not timed here).
- Dialect (not executed): MySQL versions of this problem often write `request_at BETWEEN '2013-10-01' AND '2013-10-03'` because the public table stores a date-like string; that is only safe if there is no time part. PostgreSQL and BigQuery can cast with `request_at::date` or `DATE(request_at)` but that hides the column from an index; the half-open form avoids it.
- The public problem statement and its expected output were not opened for this book; my sample data is my own.

**Follow-ups:**
- "Rate per day per city?" Add `city` to `GROUP BY`, and keep the spine as days x cities so empty cells are explicit.
- "Weekly instead of daily?" Change the bucket; state the week start (Part 6 Q5).
- "Count a banned user's trips separately?" Move the ban test into a `CASE` instead of the join, so banned trips are counted in a second column.

**Common mistakes:**
- `BETWEEN` with a bare end date on a timestamp column (loses the last day).
- Joining `users` once, so only the client (or only the driver) is checked.
- Dividing by all trips including banned-user trips, or counting `status = 'cancelled_by_client'` only.
- Integer division (`SUM(...) / COUNT(*)` without `1.0 *`) giving 0.
- `COALESCE(rate, 0)` that turns "no trips" into a perfect-looking 0.00.

### Q24 ⭐⭐ 🟡 Month-to-date versus prior month-to-date: daily_sales(sale_date, amount) and a fixed as-of date such as '2024-03-17'. Return revenue from the first of the as-of month to the as-of date, revenue from the first of the previous month to the same day number (handle a day number that does not exist in the shorter month, such as the 31st), and the percent difference. Show the half-open ranges built with date modifiers, and the pandas version with boolean masks and DateOffset. State why comparing a partial month to a full month is the classic error.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build both windows as half-open ranges from the as-of date: current is `[first of month, as_of + 1 day)`, prior is `[first of previous month, same day number + 1)` capped at the first of the as-of month; compare partial to partial, and note that SQLite's `'-1 month'` overflows (`2024-03-31` minus one month is `2024-03-02`), so I compute the prior end from the month start instead.

**Schema and sample data:** every day of February 2024 (29 days, leap year) at 100 and every day of March 2024 at 120, generated with a recursive CTE so the data is easy to check by hand. As-of dates are fixed in the code (never `now`). No time zone: `sale_date` is a plain date.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
WITH RECURSIVE d(x) AS (SELECT '2024-02-01' UNION ALL SELECT date(x, '+1 day') FROM d WHERE x < '2024-03-31')
INSERT INTO daily_sales SELECT x, CASE WHEN x < '2024-03-01' THEN 100 ELSE 120 END FROM d;
```

**SQL answer:** `SQL_MAIN` in the Code block with `:asof` as a parameter. The pieces are `date(:asof, 'start of month')` (first of the month), `date(:asof, '+1 day')` (exclusive current end), `date(:asof, 'start of month', '-1 month')` (first of the previous month; safe because it starts from the 1st) and the prior exclusive end `MIN(prev_start + day_number days, first of the as-of month)`, which clips the 31st to the end of a shorter month.
```sql
WITH b AS (
  SELECT date(:asof, 'start of month') AS cur_lo,
         date(:asof, '+1 day') AS cur_hi,
         date(:asof, 'start of month', '-1 month') AS prev_lo,
         MIN(date(:asof, 'start of month', '-1 month', '+' || CAST(strftime('%d', :asof) AS INTEGER) || ' days'),
             date(:asof, 'start of month')) AS prev_hi
), r AS (
  SELECT b.*,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= cur_lo AND sale_date < cur_hi) AS mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < prev_hi) AS prev_mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < cur_lo) AS prev_full
  FROM b
)
SELECT :asof AS asof, cur_lo, cur_hi, prev_lo, prev_hi, mtd, prev_mtd,
       ROUND(100.0 * (mtd - prev_mtd) / NULLIF(prev_mtd, 0), 1) AS pct_vs_prev_mtd,
       prev_full,
       ROUND(100.0 * (mtd - prev_full) / NULLIF(prev_full, 0), 1) AS pct_vs_full_prev_month
FROM r
```

**pandas answer:** boolean masks on `sale_date` with Timestamps. `asof - pd.DateOffset(months=1)` clips by itself to the last valid day, so the prior end needs no extra `MIN`:
```py
    asof = pd.Timestamp(asof)
    cur_lo = asof.replace(day=1)
    cur_hi = asof + pd.Timedelta(days=1)
    prev_asof = asof - pd.DateOffset(months=1)     # DateOffset clips: 2024-03-31 -> 2024-02-29
    prev_lo = cur_lo - pd.DateOffset(months=1)
    prev_hi = prev_asof + pd.Timedelta(days=1)
    m = lambda lo, hi: int(ds.loc[(ds["sale_date"] >= lo) & (ds["sale_date"] < hi), "amount"].sum())
    mt, pm = m(cur_lo, cur_hi), m(prev_lo, prev_hi)
    full = m(prev_lo, cur_lo)
```

**Example:** as-of 2024-03-17. Current window `[2024-03-01, 2024-03-18)` is 17 days at 120 = 2040. Prior window `[2024-02-01, 2024-02-18)` is 17 days at 100 = 1700. Difference (2040 - 1700) / 1700 = 20.0%. The wrong comparison is 2040 against all of February (2900): -29.7%, a decline that is only an artefact of 17 days versus 29. As-of 2024-03-31: the 31st does not exist in February, so the prior window is capped at `[2024-02-01, 2024-03-01)`, the whole of February (2900), against 31 days of March (3720): 28.3%. As-of 2024-03-01: one day each, 120 versus 100: 20.0%.

**Code:** run with `python3 -I`.
```python
# Q24: month-to-date vs prior month-to-date, fixed as-of dates
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
WITH RECURSIVE d(x) AS (SELECT '2024-02-01' UNION ALL SELECT date(x, '+1 day') FROM d WHERE x < '2024-03-31')
INSERT INTO daily_sales SELECT x, CASE WHEN x < '2024-03-01' THEN 100 ELSE 120 END FROM d;
"""
# ranges are half-open [lo, hi). The prior hi is the same day number + 1, capped at the first of the as-of month.
SQL_MAIN = """
WITH b AS (
  SELECT date(:asof, 'start of month') AS cur_lo,
         date(:asof, '+1 day') AS cur_hi,
         date(:asof, 'start of month', '-1 month') AS prev_lo,
         MIN(date(:asof, 'start of month', '-1 month', '+' || CAST(strftime('%d', :asof) AS INTEGER) || ' days'),
             date(:asof, 'start of month')) AS prev_hi
), r AS (
  SELECT b.*,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= cur_lo AND sale_date < cur_hi) AS mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < prev_hi) AS prev_mtd,
         (SELECT COALESCE(SUM(amount), 0) FROM daily_sales WHERE sale_date >= prev_lo AND sale_date < cur_lo) AS prev_full
  FROM b
)
SELECT :asof AS asof, cur_lo, cur_hi, prev_lo, prev_hi, mtd, prev_mtd,
       ROUND(100.0 * (mtd - prev_mtd) / NULLIF(prev_mtd, 0), 1) AS pct_vs_prev_mtd,
       prev_full,
       ROUND(100.0 * (mtd - prev_full) / NULLIF(prev_full, 0), 1) AS pct_vs_full_prev_month
FROM r
"""
SQL_NAIVE = "SELECT date(:asof, '-1 month') AS naive_prev_same_day"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
asofs = ["2024-03-17", "2024-03-31", "2024-03-01"]
sql_df = pd.concat([pd.read_sql_query(SQL_MAIN, con, params={"asof": a}) for a in asofs], ignore_index=True)
print(sql_df.T.to_string(header=False))
for a in ["2024-03-31", "2023-03-31"]:
    print("SQLite date('%s','-1 month') =" % a, con.execute(SQL_NAIVE, {"asof": a}).fetchone()[0])

ds = pd.read_sql_query("SELECT * FROM daily_sales", con)
ds["sale_date"] = pd.to_datetime(ds["sale_date"])

def mtd(ds, asof):
    asof = pd.Timestamp(asof)
    cur_lo = asof.replace(day=1)
    cur_hi = asof + pd.Timedelta(days=1)
    prev_asof = asof - pd.DateOffset(months=1)     # DateOffset clips: 2024-03-31 -> 2024-02-29
    prev_lo = cur_lo - pd.DateOffset(months=1)
    prev_hi = prev_asof + pd.Timedelta(days=1)
    m = lambda lo, hi: int(ds.loc[(ds["sale_date"] >= lo) & (ds["sale_date"] < hi), "amount"].sum())
    mt, pm = m(cur_lo, cur_hi), m(prev_lo, prev_hi)
    full = m(prev_lo, cur_lo)
    return dict(asof=asof.strftime("%Y-%m-%d"), cur_lo=cur_lo.strftime("%Y-%m-%d"), cur_hi=cur_hi.strftime("%Y-%m-%d"),
                prev_lo=prev_lo.strftime("%Y-%m-%d"), prev_hi=prev_hi.strftime("%Y-%m-%d"), mtd=mt, prev_mtd=pm,
                pct_vs_prev_mtd=round(100.0 * (mt - pm) / pm, 1), prev_full=full,
                pct_vs_full_prev_month=round(100.0 * (mt - full) / full, 1))
pd_df = pd.DataFrame([mtd(ds, a) for a in asofs])
# one row per as-of date, compared in the order of asofs
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas DateOffset: Timestamp('2024-03-31') - DateOffset(months=1) =", (pd.Timestamp("2024-03-31") - pd.DateOffset(months=1)).date())
print("asserts passed: SQL == pandas for", asofs)
```

**Output (my run):**
```text
asof                    2024-03-17  2024-03-31  2024-03-01
cur_lo                  2024-03-01  2024-03-01  2024-03-01
cur_hi                  2024-03-18  2024-04-01  2024-03-02
prev_lo                 2024-02-01  2024-02-01  2024-02-01
prev_hi                 2024-02-18  2024-03-01  2024-02-02
mtd                           2040        3720         120
prev_mtd                      1700        2900         100
pct_vs_prev_mtd               20.0        28.3        20.0
prev_full                     2900        2900        2900
pct_vs_full_prev_month       -29.7        28.3       -95.9
SQLite date('2024-03-31','-1 month') = 2024-03-02
SQLite date('2023-03-31','-1 month') = 2023-03-03
pandas DateOffset: Timestamp('2024-03-31') - DateOffset(months=1) = 2024-02-29
asserts passed: SQL == pandas for ['2024-03-17', '2024-03-31', '2024-03-01']
```

**Edge cases:**
- The 31st: the prior window is shorter in days than the current one (29 versus 31 in my run). That is a business decision to state; the alternative is to compare to the full previous month on the last day of the month.
- SQLite `date('2024-03-31', '-1 month')` returned `2024-03-02` and `date('2023-03-31', '-1 month')` returned `2023-03-03`, so using it as the prior end silently shifts the window. pandas `DateOffset(months=1)` returned `2024-02-29` (clipped).
- Days with no sales rows: `COALESCE(SUM(...), 0)` keeps the result at 0, but a missing day inside the window also shortens the comparison; check the day count if the feed can have gaps.
- Zero prior revenue: `NULLIF(prev_mtd, 0)` returns NULL instead of a division error (pandas would give `inf`; I did not hit it here).
- January as the as-of month: `'-1 month'` from the 1st goes to December of the previous year correctly, because it starts from day 1. I did not add January data to the sample, so this is stated, not run.

**Then explain:**
- Partial month versus full month is the classic error: on the 17th you have about half a month of sales on one side and a whole month on the other, so growth looks like a collapse (-29.7% above) even though the same-days comparison is +20.0%.
- Half-open ranges (`>= lo AND < hi`) make "through the as-of date inclusive" simply `hi = as_of + 1 day`, and they stay correct if `sale_date` ever becomes a timestamp.
- Do the month arithmetic from the first of the month; only day-of-month arithmetic from the 29th to the 31st misbehaves.
- Dialects (not executed): PostgreSQL `date_trunc('month', d)` and `d - INTERVAL '1 month'` clip to the end of the month; MySQL `DATE_SUB(d, INTERVAL 1 MONTH)` also clips; BigQuery `DATE_SUB(d, INTERVAL 1 MONTH)` clips; I am quoting these from memory.

**Follow-ups:**
- "Same-day-last-year (year-to-date)?" Same pattern with `'-1 year'`; 29 February needs the same capping rule.
- "Daily run-rate projection for the month?" That is a forecast; say it is, and keep it separate from the actuals.
- "Business-day-aligned comparison?" Join a calendar table (Q31) and compare the first n working days.

**Common mistakes:**
- Comparing the partial current month to the full previous month.
- `date(asof, '-1 month')` on the 31st (overflow into the wrong month).
- `BETWEEN` with the as-of date as a timestamp (loses the last day) or an exclusive end that is off by one.
- Using `now`/`today` so the figure changes on every run and can not be tested.

### Q25 ⭐⭐ 🟡 Fiscal years and quarters (India, April to March): orders(order_id, order_ts, amount). Derive the fiscal year label (FY2024-25 for April 2024 to March 2025), fiscal quarter (Q1 = April to June) and fiscal month number in SQLite with strftime and CASE or arithmetic, then total revenue per fiscal quarter. Give the pandas versions with dt.to_period('Q-MAR') and dt.qyear / dt.quarter, and a check on 31 March versus 1 April. Mention that quarter and DATE_TRUNC fiscal options in other engines differ (hedged, not executed).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Fiscal year starts in April: fiscal start year = calendar year minus 1 when the month is January to March, fiscal month = `(month + 8) % 12 + 1`, fiscal quarter = `(month + 8) % 12 / 3 + 1`; I label the year as `FY2024-25` for April 2024 to March 2025 and check the boundary rows 31 March and 1 April.

**Schema and sample data:** eight orders around the boundaries, ISO text timestamps. Convention: timestamps as stored (no time-zone conversion), fiscal year April to March (India), label uses the start year.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-31 23:59:59',100),(2,'2024-04-01 00:00:00',200),(3,'2024-06-30 12:00:00',300),
 (4,'2024-07-01 09:00:00',400),(5,'2024-12-25 10:00:00',500),(6,'2025-01-15 10:00:00',600),
 (7,'2025-03-31 18:00:00',700),(8,'2025-04-01 08:00:00',800);
```

**SQL answer:** `SQL_MAIN` for the quarter totals and `SQL_ROWS` for the row-level derivation, both in the Code block. `strftime('%m')` returns text, so I `CAST` it; in SQLite a comparison such as `month < 4` returns 1 or 0, which I subtract from the year.
```sql
WITH f AS (
  SELECT amount,
         CAST(strftime('%Y', order_ts) AS INTEGER) - (CAST(strftime('%m', order_ts) AS INTEGER) < 4) AS fy_start,
         (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 / 3 + 1 AS fq
  FROM orders
)
SELECT 'FY' || fy_start || '-' || substr(fy_start + 1, 3, 2) AS fiscal_year,
       'Q' || fq AS fiscal_quarter,
       SUM(amount) AS revenue, COUNT(*) AS orders
FROM f GROUP BY fy_start, fq ORDER BY fy_start, fq
```

**pandas answer:** `dt.to_period('Q-MAR')` gives fiscal quarters that end in March. The `Period` is labelled by the fiscal year END (April 2024 is `2025Q1`), `qyear` is that end year and `quarter` is the fiscal quarter number:
```py
p = orders["order_ts"].dt.to_period("Q-MAR")
print(pd.DataFrame({"d": orders["order_ts"].dt.strftime("%Y-%m-%d"), "period": p.astype(str),
                    "qyear": p.dt.qyear, "quarter": p.dt.quarter}).to_string(index=False))
fy_end = p.dt.qyear
pd_df = (orders.assign(fiscal_year="FY" + (fy_end - 1).astype(str) + "-" + (fy_end % 100).astype(str).str.zfill(2),
                       fiscal_quarter="Q" + p.dt.quarter.astype(str))
         .groupby(["fiscal_year", "fiscal_quarter"], as_index=False)
         .agg(revenue=("amount", "sum"), orders=("order_id", "count")))
```

**Example:** 2024-03-31 23:59:59 is month 3, so fiscal start year 2023 (FY2023-24), fiscal month 12, fiscal quarter `(3 + 8) % 12 / 3 + 1 = 11 / 3 + 1 = 4`. One second later, 2024-04-01 is month 4: start year 2024, fiscal month 1, quarter `12 % 12 / 3 + 1 = 1`. FY2024-25 Q1 (April to June) holds orders 2 and 3 (200 + 300 = 500); Q2 holds order 4 (400); Q3 holds order 5 (500); Q4 holds orders 6 and 7 (600 + 700 = 1300). Order 1 (100) is the last day of FY2023-24 and order 8 (800) is the first day of FY2025-26.

**Code:** run with `python3 -I`.
```python
# Q25: Indian fiscal year (April to March), fiscal quarter, fiscal month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-31 23:59:59',100),(2,'2024-04-01 00:00:00',200),(3,'2024-06-30 12:00:00',300),
 (4,'2024-07-01 09:00:00',400),(5,'2024-12-25 10:00:00',500),(6,'2025-01-15 10:00:00',600),
 (7,'2025-03-31 18:00:00',700),(8,'2025-04-01 08:00:00',800);
"""
SQL_ROWS = """
SELECT order_id, substr(order_ts, 1, 10) AS d,
       CAST(strftime('%Y', order_ts) AS INTEGER) - (CAST(strftime('%m', order_ts) AS INTEGER) < 4) AS fy_start,
       (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 + 1 AS fiscal_month,
       (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 / 3 + 1 AS fiscal_quarter
FROM orders ORDER BY order_id
"""
SQL_MAIN = """
WITH f AS (
  SELECT amount,
         CAST(strftime('%Y', order_ts) AS INTEGER) - (CAST(strftime('%m', order_ts) AS INTEGER) < 4) AS fy_start,
         (CAST(strftime('%m', order_ts) AS INTEGER) + 8) % 12 / 3 + 1 AS fq
  FROM orders
)
SELECT 'FY' || fy_start || '-' || substr(fy_start + 1, 3, 2) AS fiscal_year,
       'Q' || fq AS fiscal_quarter,
       SUM(amount) AS revenue, COUNT(*) AS orders
FROM f GROUP BY fy_start, fq ORDER BY fy_start, fq
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
rows = pd.read_sql_query(SQL_ROWS, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(rows.to_string(index=False))
print(sql_df.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
orders["order_ts"] = pd.to_datetime(orders["order_ts"])
p = orders["order_ts"].dt.to_period("Q-MAR")
print(pd.DataFrame({"d": orders["order_ts"].dt.strftime("%Y-%m-%d"), "period": p.astype(str),
                    "qyear": p.dt.qyear, "quarter": p.dt.quarter}).to_string(index=False))
fy_end = p.dt.qyear
pd_df = (orders.assign(fiscal_year="FY" + (fy_end - 1).astype(str) + "-" + (fy_end % 100).astype(str).str.zfill(2),
                       fiscal_quarter="Q" + p.dt.quarter.astype(str))
         .groupby(["fiscal_year", "fiscal_quarter"], as_index=False)
         .agg(revenue=("amount", "sum"), orders=("order_id", "count")))
# compared after sorting by fiscal_year, fiscal_quarter
pd_df = pd_df.sort_values(["fiscal_year", "fiscal_quarter"]).reset_index(drop=True)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
# row-level check of the arithmetic against pandas
fm = (orders["order_ts"].dt.month + 8) % 12 + 1
assert fm.tolist() == rows["fiscal_month"].tolist()
assert p.dt.quarter.tolist() == rows["fiscal_quarter"].tolist()
assert (fy_end - 1).tolist() == rows["fy_start"].tolist()
print("asserts passed: SQL fiscal arithmetic == pandas Q-MAR for 8 rows and for the quarter totals")
```

**Output (my run):**
```text
 order_id          d  fy_start  fiscal_month  fiscal_quarter
        1 2024-03-31      2023            12               4
        2 2024-04-01      2024             1               1
        3 2024-06-30      2024             3               1
        4 2024-07-01      2024             4               2
        5 2024-12-25      2024             9               3
        6 2025-01-15      2024            10               4
        7 2025-03-31      2024            12               4
        8 2025-04-01      2025             1               1
fiscal_year fiscal_quarter  revenue  orders
  FY2023-24             Q4      100       1
  FY2024-25             Q1      500       2
  FY2024-25             Q2      400       1
  FY2024-25             Q3      500       1
  FY2024-25             Q4     1300       2
  FY2025-26             Q1      800       1
         d period  qyear  quarter
2024-03-31 2024Q4   2024        4
2024-04-01 2025Q1   2025        1
2024-06-30 2025Q1   2025        1
2024-07-01 2025Q2   2025        2
2024-12-25 2025Q3   2025        3
2025-01-15 2025Q4   2025        4
2025-03-31 2025Q4   2025        4
2025-04-01 2026Q1   2026        1
asserts passed: SQL fiscal arithmetic == pandas Q-MAR for 8 rows and for the quarter totals
```

**Edge cases:**
- Boundary: the SQL and pandas results agree on the 31 March / 1 April pair (fiscal quarter 4 versus 1, different fiscal year). The assert covers all eight rows.
- Integer division: `(month + 8) % 12 / 3` is integer division in SQLite only because both operands are integers; `CAST(... AS INTEGER)` on the `strftime` text is what makes that true. In an engine with decimal division (some do), wrap it in `FLOOR` (not executed).
- Quarter labels differ by convention: pandas `Q-MAR` periods are named by the fiscal year they END in (`2025Q1` for April 2024), which many people read as calendar 2025. I label with `FY2024-25` instead.
- A partial fiscal year at the end of the data shows a total for only the loaded quarters; do not read it as a full year (Q32).
- Time zone: a UTC timestamp at 20:00 on 31 March is already 1 April in India (UTC+5:30), so the fiscal year of that order depends on the reporting zone; convert before classifying.

**Then explain:**
- The shift by 8 turns April into position 0: `(4 + 8) % 12 = 0`, `(3 + 8) % 12 = 11`. Divide by 3 for the quarter and add 1.
- Fiscal year for January to March belongs to the PREVIOUS calendar year's April start, hence `year - (month < 4)`.
- A calendar table (Q31) with `fiscal_year` and `fiscal_quarter` columns beats repeating this arithmetic in every query.
- Other engines (not executed): PostgreSQL `date_trunc('quarter', d)` and `EXTRACT(QUARTER FROM d)` are calendar quarters, so a fiscal shift needs an interval offset such as `d + INTERVAL '9 months'`; MySQL has `QUARTER(d)` (calendar); BigQuery and Snowflake have no built-in April fiscal option that I know of, and some tools expose a fiscal-year-start setting. I am quoting these from memory.

**Follow-ups:**
- "Fiscal week number?" Needs an agreed week definition (Part 6 Q5 and Q43).
- "Fiscal year-to-date comparisons?" That is Q32.
- "Fiscal year that starts in October (US federal) or July?" Change the 8 to 2 (October) or 6 (July) and the `< 4` test to match; same structure.

**Common mistakes:**
- Using calendar quarters (`(month + 2) / 3`) for a fiscal report.
- Labelling `FY2025` when the team means FY2024-25 without saying which end of the year names it.
- Off-by-one at the boundary (`month <= 4`, or `month > 3` wrongly applied to the year).
- Reading pandas `Q-MAR` period labels as calendar quarters.

### Q26 ⭐⭐ 🟡 Seasonality by day-of-week and hour: orders(order_id, order_ts, amount) in UTC. Return the average daily orders per day of week (Monday first), the hourly profile in IST, and weekend versus weekday share. Explain why you average over actual number of days (count distinct dates) rather than count rows (a month has more of some weekdays), the strftime('%w') Sunday = 0 ordering trick (CASE or (w + 6) % 7), and the pandas groupby on dt.dayofweek with day_name().
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Convert UTC to IST first (`+5 hours, +30 minutes`), then bucket by Monday-first day of week using `(strftime('%w') + 6) % 7 + 1`, and divide each weekday's orders by the number of calendar days of that weekday in the window (from a date spine), not by the number of distinct dates that happened to have orders.

**Schema and sample data:** 17 orders in UTC, window = IST dates 2024-03-04 (Monday) to 2024-03-18 (Monday) inclusive, so 15 days: three Mondays and two of every other weekday. Conventions: week starts Monday in the output (Mon = 1 ... Sun = 7); the reporting time zone is IST for day of week, hour and weekend share (UTC timestamps in, converted at the reporting edge). Order 8 (2024-03-09 18:45 UTC) is 00:15 on Sunday 10 March in IST and order 16 (2024-03-17 20:00 UTC) is 01:30 on Monday 18 March.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-04 03:30:00',10),(2,'2024-03-04 08:00:00',10),(3,'2024-03-05 04:30:00',10),
 (4,'2024-03-06 04:30:00',10),(5,'2024-03-06 12:00:00',10),(6,'2024-03-08 05:00:00',10),
 (7,'2024-03-09 06:30:00',10),(8,'2024-03-09 18:45:00',10),(9,'2024-03-10 09:00:00',10),
 (10,'2024-03-11 03:30:00',10),(11,'2024-03-12 04:30:00',10),(12,'2024-03-13 04:30:00',10),
 (13,'2024-03-14 04:30:00',10),(14,'2024-03-15 04:30:00',10),(15,'2024-03-16 06:30:00',10),
 (16,'2024-03-17 20:00:00',10),(17,'2024-03-18 03:30:00',10);
```

**SQL answer:** `SQL_DOW` (average per day of week), `SQL_HOUR` (hourly profile) and `SQL_SHARE` (weekend share) in the Code block. The IST conversion is the expression `datetime(order_ts, '+5 hours', '+30 minutes')`, repeated in each query; I do not use the `'localtime'` modifier because it uses the server's own zone.
```sql
WITH RECURSIVE days(d) AS (
  SELECT :lo UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < :hi
), n_days AS (
  SELECT (CAST(strftime('%w', d) AS INTEGER) + 6) % 7 + 1 AS dow, COUNT(*) AS days_in_window FROM days GROUP BY 1
), o AS (
  SELECT (CAST(strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) AS INTEGER) + 6) % 7 + 1 AS dow, date(datetime(order_ts, '+5 hours', '+30 minutes')) AS d FROM orders
  WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
)
SELECT n.dow,
       CASE n.dow WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu'
                  WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' ELSE 'Sun' END AS day_name,
       COUNT(o.d) AS orders, n.days_in_window,
       ROUND(1.0 * COUNT(o.d) / n.days_in_window, 2) AS avg_per_day,
       ROUND(1.0 * COUNT(o.d) / NULLIF(COUNT(DISTINCT o.d), 0), 2) AS naive_avg_distinct_dates
FROM n_days n LEFT JOIN o ON o.dow = n.dow
GROUP BY n.dow, n.days_in_window ORDER BY n.dow
```

**pandas answer:** shift the naive UTC timestamps by `Timedelta(hours=5, minutes=30)` (equivalent to `tz_localize('UTC').tz_convert('Asia/Kolkata')` for India, which has no DST), count orders per `dt.dayofweek + 1`, and take names from `day_name()` of the spine dates:
```py
o["ist"] = pd.to_datetime(o["order_ts"]) + pd.Timedelta(hours=5, minutes=30)   # naive timestamps hold UTC; shift = IST wall clock
o = o[(o["ist"] >= "2024-03-04") & (o["ist"] < "2024-03-19")]
spine = pd.DataFrame({"d": pd.date_range("2024-03-04", "2024-03-18", freq="D")})
spine["dow"] = spine["d"].dt.dayofweek + 1
n_days = spine.groupby("dow").size().rename("days_in_window")
o["dow"] = o["ist"].dt.dayofweek + 1
g = o.groupby("dow").agg(orders=("order_id", "count"), distinct_dates=("ist", lambda s: s.dt.normalize().nunique()))
pd_dow = n_days.to_frame().join(g, how="left").fillna(0).astype(int).reset_index()
names = spine.groupby("dow")["d"].first().dt.day_name().str[:3]   # day_name() from the spine dates
pd_dow["day_name"] = pd_dow["dow"].map(names)
```

**Example:** in IST, Monday 4 March has orders 1 and 2, Monday 11 March has order 10, Monday 18 March has orders 16 (shifted from Sunday UTC) and 17: five Monday orders over three Mondays = 1.67 per Monday. Sunday: order 8 (00:15 on 10 March) and order 9 (14:30 on 10 March) are both on the 10th; Sunday 17 March has no orders. Two Sundays in the window, 2 orders: 1.00 per Sunday, but dividing by distinct order dates (one Sunday) would give 2.00. Thursday: only 14 March has an order (7 March has none): 1 order over 2 Thursdays = 0.50, versus 1.00 by distinct dates. Weekend (Saturday or Sunday in IST): 4 of 17 orders, 23.5%.

**Code:** run with `python3 -I`.
```python
# Q26: seasonality by IST day of week and hour; window 2024-03-04 (Mon) .. 2024-03-18 (Mon) IST dates
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2024-03-04 03:30:00',10),(2,'2024-03-04 08:00:00',10),(3,'2024-03-05 04:30:00',10),
 (4,'2024-03-06 04:30:00',10),(5,'2024-03-06 12:00:00',10),(6,'2024-03-08 05:00:00',10),
 (7,'2024-03-09 06:30:00',10),(8,'2024-03-09 18:45:00',10),(9,'2024-03-10 09:00:00',10),
 (10,'2024-03-11 03:30:00',10),(11,'2024-03-12 04:30:00',10),(12,'2024-03-13 04:30:00',10),
 (13,'2024-03-14 04:30:00',10),(14,'2024-03-15 04:30:00',10),(15,'2024-03-16 06:30:00',10),
 (16,'2024-03-17 20:00:00',10),(17,'2024-03-18 03:30:00',10);
"""
# Monday-first day number: ((%w + 6) % 7) + 1 -> Mon=1 .. Sun=7
SQL_DOW = """
WITH RECURSIVE days(d) AS (
  SELECT :lo UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < :hi
), n_days AS (
  SELECT (CAST(strftime('%w', d) AS INTEGER) + 6) % 7 + 1 AS dow, COUNT(*) AS days_in_window FROM days GROUP BY 1
), o AS (
  SELECT (CAST(strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) AS INTEGER) + 6) % 7 + 1 AS dow, date(datetime(order_ts, '+5 hours', '+30 minutes')) AS d FROM orders
  WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
)
SELECT n.dow,
       CASE n.dow WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu'
                  WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' ELSE 'Sun' END AS day_name,
       COUNT(o.d) AS orders, n.days_in_window,
       ROUND(1.0 * COUNT(o.d) / n.days_in_window, 2) AS avg_per_day,
       ROUND(1.0 * COUNT(o.d) / NULLIF(COUNT(DISTINCT o.d), 0), 2) AS naive_avg_distinct_dates
FROM n_days n LEFT JOIN o ON o.dow = n.dow
GROUP BY n.dow, n.days_in_window ORDER BY n.dow
"""
SQL_HOUR = """
SELECT CAST(strftime('%H', datetime(order_ts, '+5 hours', '+30 minutes')) AS INTEGER) AS ist_hour, COUNT(*) AS orders,
       ROUND(1.0 * COUNT(*) / 15, 2) AS avg_per_day
FROM orders WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
GROUP BY 1 ORDER BY 1
"""
SQL_SHARE = """
SELECT SUM(CASE WHEN strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) IN ('0','6') THEN 1 ELSE 0 END) AS weekend_orders,
       COUNT(*) AS orders,
       ROUND(100.0 * SUM(CASE WHEN strftime('%w', datetime(order_ts, '+5 hours', '+30 minutes')) IN ('0','6') THEN 1 ELSE 0 END) / COUNT(*), 1) AS weekend_pct
FROM orders WHERE date(datetime(order_ts, '+5 hours', '+30 minutes')) BETWEEN :lo AND :hi
"""
SQL_UTC_DOW = """
SELECT (CAST(strftime('%w', order_ts) AS INTEGER) + 6) % 7 + 1 AS dow_utc, COUNT(*) AS orders
FROM orders GROUP BY 1 ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"lo": "2024-03-04", "hi": "2024-03-18"}
dow = pd.read_sql_query(SQL_DOW, con, params=P)
hour = pd.read_sql_query(SQL_HOUR, con, params=P)
share = pd.read_sql_query(SQL_SHARE, con, params=P)
print(dow.to_string(index=False)); print(hour.to_string(index=False)); print(share.to_string(index=False))
print("UTC day-of-week counts (same orders, different boundary):")
print(pd.read_sql_query(SQL_UTC_DOW, con).to_string(index=False))

o = pd.read_sql_query("SELECT * FROM orders", con)
o["ist"] = pd.to_datetime(o["order_ts"]) + pd.Timedelta(hours=5, minutes=30)   # naive timestamps hold UTC; shift = IST wall clock
o = o[(o["ist"] >= "2024-03-04") & (o["ist"] < "2024-03-19")]
spine = pd.DataFrame({"d": pd.date_range("2024-03-04", "2024-03-18", freq="D")})
spine["dow"] = spine["d"].dt.dayofweek + 1
n_days = spine.groupby("dow").size().rename("days_in_window")
o["dow"] = o["ist"].dt.dayofweek + 1
g = o.groupby("dow").agg(orders=("order_id", "count"), distinct_dates=("ist", lambda s: s.dt.normalize().nunique()))
pd_dow = n_days.to_frame().join(g, how="left").fillna(0).astype(int).reset_index()
names = spine.groupby("dow")["d"].first().dt.day_name().str[:3]   # day_name() from the spine dates
pd_dow["day_name"] = pd_dow["dow"].map(names)
pd_dow["avg_per_day"] = (pd_dow["orders"] / pd_dow["days_in_window"]).round(2)
pd_dow["naive_avg_distinct_dates"] = (pd_dow["orders"] / pd_dow["distinct_dates"]).round(2)
pd_dow = pd_dow[["dow", "day_name", "orders", "days_in_window", "avg_per_day", "naive_avg_distinct_dates"]]
# compared in Monday-first order (dow 1..7)
pd.testing.assert_frame_equal(pd_dow, dow, check_dtype=False)
pd_hour = o.groupby(o["ist"].dt.hour).size().rename("orders").rename_axis("ist_hour").reset_index()
pd_hour["avg_per_day"] = (pd_hour["orders"] / 15).round(2)
pd.testing.assert_frame_equal(pd_hour, hour, check_dtype=False)
wk = int((o["ist"].dt.dayofweek >= 5).sum())
assert (wk, len(o), round(100.0 * wk / len(o), 1)) == tuple(share.iloc[0])
print("pandas day_name:", pd_dow["day_name"].tolist())
print("asserts passed: SQL == pandas for day-of-week, hourly profile and weekend share")
```

**Output (my run):**
```text
 dow day_name  orders  days_in_window  avg_per_day  naive_avg_distinct_dates
   1      Mon       5               3         1.67                      1.67
   2      Tue       2               2         1.00                      1.00
   3      Wed       3               2         1.50                      1.50
   4      Thu       1               2         0.50                      1.00
   5      Fri       2               2         1.00                      1.00
   6      Sat       2               2         1.00                      1.00
   7      Sun       2               2         1.00                      2.00
 ist_hour  orders  avg_per_day
        0       1         0.07
        1       1         0.07
        9       3         0.20
       10       7         0.47
       12       2         0.13
       13       1         0.07
       14       1         0.07
       17       1         0.07
 weekend_orders  orders  weekend_pct
              4      17         23.5
UTC day-of-week counts (same orders, different boundary):
 dow_utc  orders
       1       4
       2       2
       3       3
       4       1
       5       2
       6       3
       7       2
pandas day_name: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
asserts passed: SQL == pandas for day-of-week, hourly profile and weekend share
```

**Edge cases:**
- Days with zero orders (Thursday 7 March, Sunday 17 March): they must be in the denominator, which is why `n_days` comes from a recursive date spine. Dividing by `COUNT(DISTINCT date)` overstates Thursday (1.00 instead of 0.50) and Sunday (2.00 instead of 1.00); those two columns are printed side by side.
- Window length: 15 days gives Monday three occurrences. A 14-day window would give every weekday two; the unequal count is exactly why you divide by days, not rows.
- Time zone moves orders between days: with UTC day-of-week the Monday count is 4 instead of 5 and Saturday is 3 instead of 2 in my data (the extra UTC-table printed in the output), because two orders cross midnight when converted. State the zone before comparing numbers.
- Hour 0 and hour 1 in the hourly profile come from the two orders that cross midnight in IST.
- `%w` is Sunday = 0: without the `(w + 6) % 7` shift, Sunday sorts first.
- Weekday versus weekend share is share of orders (23.5%), not share of days; a weekend has 2 of 7 days (about 28.6% of days), so compare to that.
- The hourly profile divides by 15 days in my window; for a window with a different length, parametrise it.

**Then explain:**
- Average per weekday = total orders on that weekday / number of that weekday in the window. It is a rate per day, so it is comparable across weekdays even when the counts of weekdays differ.
- Convert once at the reporting edge: all three outputs here use the same IST expression.
- pandas `dt.dayofweek` is Monday = 0 (I add 1 to match the SQL numbering); `day_name()` gives names but sorts alphabetically if you group on it, so group on the number and map to names.
- Hedged (not executed): PostgreSQL `EXTRACT(ISODOW FROM d)` is Monday = 1 and `EXTRACT(DOW FROM d)` is Sunday = 0; MySQL `WEEKDAY(d)` is Monday = 0 and `DAYOFWEEK(d)` is Sunday = 1; named zones use `AT TIME ZONE` in PostgreSQL and `CONVERT_TZ` in MySQL. From memory.

**Follow-ups:**
- "Heatmap of day of week by hour?" Group by both numbers; keep empty cells with a 7 x 24 spine.
- "Seasonality across months or festivals?" Needs several years and an indicator for movable dates; weekday averaging is only the first step.
- "Is the weekend difference significant?" That is a statistics question (Book 1); here I only describe the data.

**Common mistakes:**
- Dividing by rows or distinct order dates instead of calendar days.
- Grouping by UTC weekday and reporting it as local.
- Sunday = 0 ordering left in the output.
- Using `'localtime'` and getting the server's zone.
- Reading a weekday average from a short window as seasonality.

### Q27 ⭐⭐ 🟡 Business days and holidays: tasks(task_id, start_date, end_date) and holidays(holiday_date). Count working days (Monday to Friday, excluding holidays) between start and end inclusive using a recursive CTE calendar and LEFT JOIN or NOT EXISTS on holidays, and show the closed-form day arithmetic and why it fails with holidays. pandas: np.busday_count with holidays=, pd.bdate_range(freq='C', holidays=...), and CustomBusinessDay. State whether the end date is inclusive; that choice changes every answer by one.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** I count Monday-to-Friday days from a recursive date calendar, `LEFT JOIN`ed to each task over `BETWEEN start_date AND end_date` (end inclusive), excluding holidays with `NOT EXISTS`; the closed-form arithmetic (full weeks times 5 plus the leftover days) is faster but breaks as soon as a holiday falls on a weekend or repeats, so it is only a check for the no-holiday case.

**Schema and sample data:** five tasks (a normal week, a range containing a Monday holiday, a range containing a Saturday holiday, a Saturday-only task, and an end before the start) and two holidays, one Monday (2024-03-25) and one Saturday (2024-03-30). Convention: start and end dates are both inclusive; weekend = Saturday and Sunday; dates are plain dates with no time zone.
```sql
CREATE TABLE tasks(task_id INTEGER PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY);
INSERT INTO tasks VALUES (1,'2024-03-18','2024-03-22'),(2,'2024-03-22','2024-03-26'),
  (3,'2024-03-29','2024-04-02'),(4,'2024-03-23','2024-03-23'),(5,'2024-03-27','2024-03-26');
INSERT INTO holidays VALUES ('2024-03-25'),('2024-03-30');
```

**SQL answer:** `SQL_MAIN` (calendar CTE, `LEFT JOIN`, `NOT EXISTS`) and `SQL_CLOSED` (closed-form) in the Code block.
```sql
WITH RECURSIVE cal(d) AS (
  SELECT (SELECT MIN(start_date) FROM tasks)
  UNION ALL SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(end_date) FROM tasks)
)
SELECT t.task_id, t.start_date, t.end_date, COUNT(c.d) AS working_days
FROM tasks t
LEFT JOIN cal c
  ON c.d BETWEEN t.start_date AND t.end_date
 AND strftime('%w', c.d) NOT IN ('0', '6')
 AND NOT EXISTS (SELECT 1 FROM holidays h WHERE h.holiday_date = c.d)
GROUP BY t.task_id, t.start_date, t.end_date
ORDER BY t.task_id
```
```sql
WITH x AS (
  SELECT task_id,
         CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1 AS n,
         (CAST(strftime('%w', start_date) AS INTEGER) + 6) % 7 AS w,
         start_date, end_date
  FROM tasks WHERE end_date >= start_date
), y AS (
  SELECT task_id, n / 7 * 5
         + MAX(0, MIN(w + n % 7, 5) - w) + MAX(0, MIN(w + n % 7 - 7, 5)) AS weekdays,
         start_date, end_date
  FROM x
)
SELECT task_id, weekdays AS closed_form_no_holidays,
       weekdays - (SELECT COUNT(*) FROM holidays h WHERE h.holiday_date BETWEEN start_date AND end_date) AS naive_minus_holidays
FROM y ORDER BY task_id
```

**pandas answer:** `np.busday_count` counts up to but excluding the end date, so pass `end + 1 day` for an inclusive end; `bdate_range(..., freq='C', holidays=...)` and `date_range(freq=CustomBusinessDay(holidays=...))` include both ends:
```py
bc = np.clip(np.busday_count(s, e + np.timedelta64(1, "D"), holidays=hol), 0, None)
cbd = pd.offsets.CustomBusinessDay(holidays=hol)
bd = [len(pd.bdate_range(a, b, freq="C", holidays=hol)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
cb = [len(pd.date_range(a, b, freq=cbd)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
```

**Example:** task 1, Monday 18 to Friday 22 March: 5 weekdays, no holidays, 5. Task 2, Friday 22 to Tuesday 26: weekdays are Fri 22, Mon 25, Tue 26 = 3, and Monday 25 is a holiday, so 2. Task 3, Friday 29 March to Tuesday 2 April: weekdays Fri 29, Mon 1, Tue 2 = 3; the holiday is Saturday 30 March, which is not a working day anyway, so the answer stays 3. The naive "weekdays minus holidays in the range" gives 2, which is wrong. Task 4 (a Saturday) is 0 and task 5 (end before start) is 0 because the join finds no days.

**Code:** run with `python3 -I`.
```python
# Q27: working days (Mon-Fri, minus holidays), start and end both INCLUSIVE
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE tasks(task_id INTEGER PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY);
INSERT INTO tasks VALUES (1,'2024-03-18','2024-03-22'),(2,'2024-03-22','2024-03-26'),
  (3,'2024-03-29','2024-04-02'),(4,'2024-03-23','2024-03-23'),(5,'2024-03-27','2024-03-26');
INSERT INTO holidays VALUES ('2024-03-25'),('2024-03-30');
"""
SQL_MAIN = """
WITH RECURSIVE cal(d) AS (
  SELECT (SELECT MIN(start_date) FROM tasks)
  UNION ALL SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(end_date) FROM tasks)
)
SELECT t.task_id, t.start_date, t.end_date, COUNT(c.d) AS working_days
FROM tasks t
LEFT JOIN cal c
  ON c.d BETWEEN t.start_date AND t.end_date
 AND strftime('%w', c.d) NOT IN ('0', '6')
 AND NOT EXISTS (SELECT 1 FROM holidays h WHERE h.holiday_date = c.d)
GROUP BY t.task_id, t.start_date, t.end_date
ORDER BY t.task_id
"""
# closed form: full weeks * 5 + weekdays among the leftover days; w = Monday-based index of the start day
SQL_CLOSED = """
WITH x AS (
  SELECT task_id,
         CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1 AS n,
         (CAST(strftime('%w', start_date) AS INTEGER) + 6) % 7 AS w,
         start_date, end_date
  FROM tasks WHERE end_date >= start_date
), y AS (
  SELECT task_id, n / 7 * 5
         + MAX(0, MIN(w + n % 7, 5) - w) + MAX(0, MIN(w + n % 7 - 7, 5)) AS weekdays,
         start_date, end_date
  FROM x
)
SELECT task_id, weekdays AS closed_form_no_holidays,
       weekdays - (SELECT COUNT(*) FROM holidays h WHERE h.holiday_date BETWEEN start_date AND end_date) AS naive_minus_holidays
FROM y ORDER BY task_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
closed = pd.read_sql_query(SQL_CLOSED, con)
print(sql_df.to_string(index=False))
print(closed.to_string(index=False))

tasks = pd.read_sql_query("SELECT * FROM tasks", con)
hol = pd.read_sql_query("SELECT * FROM holidays", con)["holiday_date"].tolist()
s = tasks["start_date"].to_numpy("datetime64[D]")
e = tasks["end_date"].to_numpy("datetime64[D]")
# busday_count excludes the end date, so add one day for an inclusive end; end < start gives a negative count, clip at 0
bc = np.clip(np.busday_count(s, e + np.timedelta64(1, "D"), holidays=hol), 0, None)
cbd = pd.offsets.CustomBusinessDay(holidays=hol)
bd = [len(pd.bdate_range(a, b, freq="C", holidays=hol)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
cb = [len(pd.date_range(a, b, freq=cbd)) for a, b in zip(tasks["start_date"], tasks["end_date"])]
print("np.busday_count (end+1):", bc.tolist())
print("bdate_range freq='C':", bd)
print("date_range CustomBusinessDay:", cb)
# compared in task_id order
assert bc.tolist() == sql_df["working_days"].tolist() == bd == cb
print("exclusive end (busday_count without +1 day):", np.busday_count(s, e, holidays=hol).tolist())
# closed form (no holidays) checked against busday_count on 840 start/end pairs from 2024-03-01
con.execute("DELETE FROM tasks")
base = np.datetime64("2024-03-01", "D")
pairs = [(str(base + np.timedelta64(i, "D")), str(base + np.timedelta64(i + j, "D"))) for i in range(14) for j in range(60)]
con.executemany("INSERT INTO tasks(start_date, end_date) VALUES (?, ?)", pairs)
cf = dict(con.execute("SELECT task_id, closed_form_no_holidays FROM (" + SQL_CLOSED + ")").fetchall())
rows = con.execute("SELECT task_id, start_date, end_date FROM tasks").fetchall()
for tid, a, b in rows:
    assert cf[tid] == int(np.busday_count(np.datetime64(a, "D"), np.datetime64(b, "D") + np.timedelta64(1, "D"))), (a, b)
print("closed form (no holidays) matches busday_count on", len(rows), "start/end pairs")
print("asserts passed: SQL == busday_count == bdate_range('C') == CustomBusinessDay")
```

**Output (my run):**
```text
 task_id start_date   end_date  working_days
       1 2024-03-18 2024-03-22             5
       2 2024-03-22 2024-03-26             2
       3 2024-03-29 2024-04-02             3
       4 2024-03-23 2024-03-23             0
       5 2024-03-27 2024-03-26             0
 task_id  closed_form_no_holidays  naive_minus_holidays
       1                        5                     5
       2                        3                     2
       3                        3                     2
       4                        0                     0
np.busday_count (end+1): [5, 2, 3, 0, 0]
bdate_range freq='C': [5, 2, 3, 0, 0]
date_range CustomBusinessDay: [5, 2, 3, 0, 0]
exclusive end (busday_count without +1 day): [4, 1, 2, 0, -1]
closed form (no holidays) matches busday_count on 840 start/end pairs
asserts passed: SQL == busday_count == bdate_range('C') == CustomBusinessDay
```

**Edge cases:**
- Inclusive versus exclusive end: this changes every answer by one. With `busday_count(start, end)` and no `+ 1 day` the printed list is `[4, 1, 2, 0, -1]` instead of `[5, 2, 3, 0, 0]`. State the rule before coding.
- Holiday on a weekend (2024-03-30): the calendar join ignores it correctly; the closed-form minus holidays does not (task 3 gives 2). A holiday listed twice would also double-subtract in the closed form, which is why `holidays.holiday_date` is a primary key here.
- End before start (task 5): the `BETWEEN` join returns no calendar days, so `LEFT JOIN` keeps the task with count 0. `busday_count` can return a negative number for a reversed range (the exclusive form shows -1); I clip at 0 in the check.
- Tasks outside the calendar: the calendar runs from the earliest start to the latest end in `tasks`; with a fixed calendar table (Q31) make sure it covers the task dates.
- Different working week (Friday and Saturday weekend in some countries) needs a different weekend set; `weekmask` in numpy/pandas and a change to the `%w` test in SQL.
- Half-days, regional holidays, and time-of-day tasks are out of scope; state it.

**Then explain:**
- Calendar approach: generate one row per day, filter by weekday, filter by holiday, count per task. It is O(tasks x days) in the worst case but is easy to audit and to extend with a half-day rule.
- Closed form: `n / 7 * 5` plus the weekdays inside the `n % 7` leftover days, starting from the start day's weekday index. I checked it against `busday_count` on 840 start/end pairs (no holidays); it matches. Holidays are a set, not a count, so subtract only holidays that are weekdays and unique.
- pandas: `CustomBusinessDay(holidays=...)` is the object you reuse for offsets (`+ 5 * cbd`) as well as ranges; `freq='C'` is its alias in `bdate_range`.
- Hedged (not executed): PostgreSQL can use `generate_series(start, end, interval '1 day')` for the calendar and `EXTRACT(ISODOW FROM d) < 6`; MySQL 8 uses a recursive CTE as here; there is no portable built-in working-day function.

**Follow-ups:**
- "Add N working days to a start date?" Use the calendar with a row number over working days, or `start + N * CustomBusinessDay` in pandas.
- "Business days between timestamps?" Decide how partial days count first.
- "Holidays that differ by region?" Add `region` to `holidays` and to the join.

**Common mistakes:**
- Forgetting that `busday_count` excludes the end date.
- Subtracting the number of holidays instead of the number of weekday holidays.
- Counting `strftime('%w') BETWEEN 1 AND 5` with Sunday = 0 confusion (use `NOT IN ('0', '6')`).
- An inner join that silently drops tasks with zero working days.
- Mixing `DATE` strings with different formats so `BETWEEN` compares text wrongly.

### Q28 ⭐⭐ 🟡 pandas resample details versus SQL grouping: daily_sales(sale_date, amount) with gaps. Show resample('MS') (month start labels, left closed), resample('ME') (month end labels, closed and label right by default) and resample('W') (W-SUN, right closed and labelled), why resample('MS') creates empty months (sum 0, mean NaN) where SQL GROUP BY omits them, and the 'M' alias being gone in pandas 3 (use 'ME'). Reproduce a SQLite monthly sum and assert both frames match after reindexing the SQL result to the pandas spine.
**Asked at:** pandas time series user guide and DataFrame.resample reference (opened), official documentation and not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `resample('MS')` labels each month by its first day, closed left, and creates empty months (sum 0, mean NaN), while SQL `GROUP BY` omits months with no rows; `resample('ME')` labels by month end and is the pandas 3 spelling (`'M'` raises), and `resample('W')` is `W-SUN`, right closed and right labelled, so a week is named by the Sunday that ends it.

**Schema and sample data:** six sales days with gaps (nothing in February). Conventions: weeks end on Sunday for `W` (Monday start needs `closed='left', label='left'` on `W-MON`); no time zone, timestamps are naive.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-05',10),('2024-01-20',20),('2024-01-31',30),
  ('2024-03-03',40),('2024-03-15',50),('2024-04-01',60);
```

**SQL answer:** `SQL_MAIN` groups by month start and omits February. To compare with pandas I reindex the SQL result to the pandas month spine afterwards (in pandas), not inside SQL.
```sql
SELECT date(sale_date, 'start of month') AS month, SUM(amount) AS revenue, COUNT(*) AS n_days
FROM daily_sales GROUP BY 1 ORDER BY 1
```

**pandas answer:** the three resamples, then the reindex-and-compare step (full code below):
```py
ms = s.resample("MS").agg(["sum", "mean", "count"])
print("resample('MS') sum/mean/count:"); print(ms.to_string())
me = s.resample("ME").sum()
```
```py
spine = pd.date_range("2024-01-01", "2024-04-01", freq="MS")
sql_s = sql_df.assign(month=pd.to_datetime(sql_df["month"])).set_index("month")["revenue"].reindex(spine, fill_value=0)
pd_s = s.resample("MS").sum()
```

**Example:** daily sales: 5 Jan 10, 20 Jan 20, 31 Jan 30, 3 Mar 40, 15 Mar 50, 1 Apr 60. Months: January 60, February nothing, March 90, April 60. SQL returns three rows. `resample('MS')` returns four: 2024-02-01 has sum 0, mean NaN, count 0. `resample('ME')` returns the same four values labelled 01-31, 02-29, 03-31, 04-30. `resample('W')`: 31 Jan is a Wednesday, so its week runs Monday 29 Jan to Sunday 4 Feb and is labelled 2024-02-04, a February date for a January sale; 3 March is a Sunday and is labelled 2024-03-03 itself because the right edge is closed.

**Code:** run with `python3 -I`.
```python
# Q28: pandas resample (MS, ME, W) versus SQL GROUP BY; daily sales with gaps
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-05',10),('2024-01-20',20),('2024-01-31',30),
  ('2024-03-03',40),('2024-03-15',50),('2024-04-01',60);
"""
SQL_MAIN = """
SELECT date(sale_date, 'start of month') AS month, SUM(amount) AS revenue, COUNT(*) AS n_days
FROM daily_sales GROUP BY 1 ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (February is absent):"); print(sql_df.to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales", con)
s = ds.assign(sale_date=pd.to_datetime(ds["sale_date"])).set_index("sale_date")["amount"]

ms = s.resample("MS").agg(["sum", "mean", "count"])
print("resample('MS') sum/mean/count:"); print(ms.to_string())
me = s.resample("ME").sum()
print("resample('ME') sum:"); print(me.to_string())
w = s.resample("W").sum()
print("resample('W') (W-SUN, right closed, right label) sum, non-empty weeks:")
print(w[w > 0].to_string())
print("W-SUN week 2024-01-29..2024-02-04 label:", w.index[w.index == "2024-02-04"].tolist())
wm = s.resample("W-MON").sum()
print("resample('W-MON') defaults (right closed, right label), non-empty:", {str(k.date()): int(v) for k, v in wm[wm > 0].items()})
wm2 = s.resample("W-MON", closed="left", label="left").sum()
print("resample('W-MON', closed='left', label='left') non-empty:", {str(k.date()): int(v) for k, v in wm2[wm2 > 0].items()})
try:
    s.resample("M")
except Exception as ex:
    print("resample('M') ->", type(ex).__name__ + ":", ex)
print("defaults on this install: MS closed/label =", s.resample("MS").sum().index[0].date(), "(left); ME first label =", me.index[0].date(), "(right)")
# timestamps: does a 15:00 sale on the last day of the month stay in that month under 'ME'?
ts = pd.Series([1, 2], index=pd.to_datetime(["2024-01-31 15:00", "2024-02-01 00:00"]))
print("ME with a 15:00 timestamp on 31 Jan:", ts.resample("ME").sum().to_dict())
print("MS with a 15:00 timestamp on 31 Jan:", ts.resample("MS").sum().to_dict())

# SQL result reindexed to the pandas spine
spine = pd.date_range("2024-01-01", "2024-04-01", freq="MS")
sql_s = sql_df.assign(month=pd.to_datetime(sql_df["month"])).set_index("month")["revenue"].reindex(spine, fill_value=0)
pd_s = s.resample("MS").sum()
# compared on the monthly spine, index = month start
pd.testing.assert_series_equal(sql_s, pd_s, check_names=False, check_freq=False, check_dtype=False)
# ME and MS agree on values, only labels differ
assert me.to_numpy().tolist() == pd_s.to_numpy().tolist()
print("SQL reindexed to spine:", sql_s.to_dict())
print("asserts passed: SQL (reindexed to the MS spine) == resample('MS').sum() == resample('ME').sum() values")
```

**Output (my run):**
```text
SQL (February is absent):
     month  revenue  n_days
2024-01-01       60       3
2024-03-01       90       2
2024-04-01       60       1
resample('MS') sum/mean/count:
            sum  mean  count
sale_date                   
2024-01-01   60  20.0      3
2024-02-01    0   NaN      0
2024-03-01   90  45.0      2
2024-04-01   60  60.0      1
resample('ME') sum:
sale_date
2024-01-31    60
2024-02-29     0
2024-03-31    90
2024-04-30    60
Freq: ME
resample('W') (W-SUN, right closed, right label) sum, non-empty weeks:
sale_date
2024-01-07    10
2024-01-21    20
2024-02-04    30
2024-03-03    40
2024-03-17    50
2024-04-07    60
W-SUN week 2024-01-29..2024-02-04 label: [Timestamp('2024-02-04 00:00:00')]
resample('W-MON') defaults (right closed, right label), non-empty: {'2024-01-08': 10, '2024-01-22': 20, '2024-02-05': 30, '2024-03-04': 40, '2024-03-18': 50, '2024-04-01': 60}
resample('W-MON', closed='left', label='left') non-empty: {'2024-01-01': 10, '2024-01-15': 20, '2024-01-29': 30, '2024-02-26': 40, '2024-03-11': 50, '2024-04-01': 60}
resample('M') -> ValueError: Invalid frequency: M. Failed to parse with error message: ValueError("'M' is no longer supported for offsets. Please use 'ME' instead.")
defaults on this install: MS closed/label = 2024-01-01 (left); ME first label = 2024-01-31 (right)
ME with a 15:00 timestamp on 31 Jan: {Timestamp('2024-01-31 00:00:00'): 1, Timestamp('2024-02-29 00:00:00'): 2}
MS with a 15:00 timestamp on 31 Jan: {Timestamp('2024-01-01 00:00:00'): 1, Timestamp('2024-02-01 00:00:00'): 2}
SQL reindexed to spine: {Timestamp('2024-01-01 00:00:00'): 60, Timestamp('2024-02-01 00:00:00'): 0, Timestamp('2024-03-01 00:00:00'): 90, Timestamp('2024-04-01 00:00:00'): 60}
asserts passed: SQL (reindexed to the MS spine) == resample('MS').sum() == resample('ME').sum() values
```

**Edge cases:**
- Empty month: sum 0 (a convenience, but it can hide "no data loaded" as "zero sales"), mean NaN, count 0. In SQL the row is simply absent. Choose zero or NULL deliberately (Q6, Q7).
- `W` labels: the label is the week end, so month-level reporting from weekly buckets mislabels boundary weeks (the 31 Jan sale in a week labelled 4 Feb).
- `W-MON` defaults: I ran both; with defaults, `W-MON` is also right closed and right labelled (the 1 April sale falls in the bucket labelled 2024-04-01, a week that ends on that Monday and starts on Tuesday 26 March). To get Monday-to-Sunday weeks labelled by their Monday I had to pass `closed='left', label='left'` (printed above: 2024-04-01 bucket holds 1 April). This matches the docs' note that W is right-closed; I confirmed it by running.
- Timestamps at 15:00 on the last day of a month: under `ME` I tested a 31 Jan 15:00 value and it stayed in January (label 2024-01-31); under `MS` it also stayed in January (label 2024-01-01), so month resampling is by calendar day boundaries and the time of day does not push it into the next bin.
- `'M'`: pandas 3.0.5 raised `ValueError: Invalid frequency: M. Failed to parse with error message: ValueError("'M' is no longer supported for offsets. Please use 'ME' instead.")`. Period frequencies still use `'M'` (as in `to_period('M')`).

**Then explain:**
- `GROUP BY` can only return groups that exist in the data; `resample` builds the full range from the first to the last timestamp, so gaps in the middle become rows. The range runs from the first to the last timestamp present in the data.
- Default closure/label: left/left for `MS`, right/right for `ME`, `W` and `QE`/`YE` (the end-anchored ones), as in the pandas `resample` reference (opened for the sources note); I ran `MS`, `ME`, `W` and `W-MON` to confirm.
- To reproduce a SQL monthly sum in pandas, either `groupby(dt.to_period('M'))` (no empty months, like SQL) or `resample` plus `reindex` on the SQL side; the assert in the code compares on the `MS` spine with `fill_value=0`.
- Hedged (not executed): in other engines the equivalent spine is `generate_series` (PostgreSQL), `GENERATE_DATE_ARRAY` (BigQuery) or a calendar table; I have not run them.

**Follow-ups:**
- "Why did my weekly total not match the monthly total?" Weeks straddle month ends; sum daily data to months directly.
- "Sum versus mean on a resampled gap?" Mean of daily data over empty days is NaN, but a monthly average per calendar day needs the day count (spine), not the mean of existing days.
- "How do I resample timestamps with a time zone?" Convert to the reporting zone first (Q30, Q38).

**Common mistakes:**
- Using `'M'` in pandas 3 and getting a `ValueError` (use `'ME'`).
- Assuming `W` weeks start on Monday and are labelled by their first day.
- Treating an empty resampled month as zero when it really means data was not loaded.
- Comparing `MS`-labelled and `ME`-labelled frames by index.

### Q29 ⭐⭐ 🟡 SQL versus pandas date gotchas (translation table, each row demonstrated): week start defaults (SQLite %w Sunday = 0 versus pandas Monday = 0), integer versus float day differences (julianday versus Timedelta.days), NULL versus NaT in comparisons and groupby (pandas groupby drops NaT keys by default, SQL groups NULL together), string dates compared as text versus datetime64, ISO week year boundary (isocalendar().year versus calendar year), and Period('2024-01') versus Timestamp('2024-01-01') equality and merging. Run each side by side on a six-row frame.
**Asked at:** pandas time series user guide and DataFrame.resample reference (opened), official documentation and not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Same dates, different defaults: `%w` is Sunday = 0 but pandas `dayofweek` is Monday = 0; `julianday` differences are floats but `Timedelta.days` truncates; SQL comparisons with NULL are unknown but a pandas comparison with NaT is False (so its negation is True); SQL groups NULLs together but pandas drops NaT keys; text dates compare as text; the ISO year is not the calendar year near 1 January; and `Period('2024-01')` is not equal to `Timestamp('2024-01-01')`.

**Schema and sample data:** a six-row frame `t` with a clean ISO date `d`, a loosely formatted text date `d_loose` (row 6 is `'2024-1-02'`, not zero-padded) and a timestamp pair `a`, `b`. Row 5 is all NULL. Conventions: week start Sunday = 0 in SQLite `%w`, Monday = 0 in pandas; ISO weeks start Monday; no time zone (all naive).
```sql
CREATE TABLE t(id INTEGER PRIMARY KEY, d TEXT, d_loose TEXT, a TEXT, b TEXT);
INSERT INTO t VALUES
 (1,'2024-12-30','2024-12-30','2024-01-01 00:00:00','2024-01-02 12:00:00'),
 (2,'2021-01-01','2021-01-01','2024-03-01 10:00:00','2024-03-01 23:00:00'),
 (3,'2023-01-01','2023-01-01','2024-03-01 00:00:00','2024-03-04 00:00:00'),
 (4,'2024-02-29','2024-02-29','2024-03-01 23:00:00','2024-03-02 01:00:00'),
 (5,NULL,NULL,NULL,NULL),
 (6,'2024-01-02','2024-1-02','2024-03-05 00:00:00','2024-03-05 00:00:00');
```

**SQL answer:** four queries in the Code block, one per gotcha. The row-level one is `SQL_ROWS`:
```sql
SELECT id,
       CAST(strftime('%w', d) AS INTEGER) AS w_sql,
       ROUND(julianday(b) - julianday(a), 4) AS days_float,
       strftime('%Y', d) AS cal_year,
       strftime('%Y', date(d, '-3 days', 'weekday 4')) AS iso_year,
       (CAST(strftime('%j', date(d, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week
FROM t ORDER BY id
```

**pandas answer:** parse once with `pd.to_datetime`, then use the accessors. The key lines per gotcha are in the Code block; the mapping that makes the weekday numbers comparable is `(d.dt.dayofweek + 1) % 7` (Monday 0 becomes 1, Sunday 6 becomes 0).

**Example:** the translation table, each row demonstrated by the run below.

| Gotcha | SQLite | pandas | In my run |
|---|---|---|---|
| Week start | `%w`: Sunday = 0 | `dayofweek`: Monday = 0 | 2024-12-30 (Monday) is 1 in SQL and 0 in pandas; 2023-01-01 (Sunday) is 0 and 6 |
| Day difference | `julianday(b) - julianday(a)` float | `(b - a).dt.days` integer floor | 36 hours: 1.5 versus 1; 13 hours: 0.5417 versus 0 |
| NULL / NaT in a comparison | `d > x` is NULL, `NOT (d > x)` is NULL, row excluded both ways | `NaT > x` is False, `~(NaT > x)` is True | greater: 3 rows in both; not-greater: 2 in SQL, 3 in pandas |
| GROUP BY a missing key | NULL is its own group | `groupby` drops NaT keys by default (`dropna=False` keeps) | SQL 4 groups, pandas 3 groups by default |
| Text versus datetime | `'2024-1-02' < '2024-01-05'` is false (text order), `date('2024-1-02')` is NULL | parsed to Timestamp: true | SQL ids 2, 3; pandas ids 2, 3, 6 |
| ISO year | emulate with `strftime('%Y', date(d, '-3 days', 'weekday 4'))` | `isocalendar().year` | 2024-12-30 is ISO 2025-W01, 2021-01-01 is 2020-W53, 2023-01-01 is 2022-W52 |
| Period versus Timestamp | month is text `'2024-01'` | `Period('2024-01') == Timestamp('2024-01-01')` is False | merge on Period column versus datetime column: 0 rows |

Row 1 of the first printed table: id 1 is 2024-12-30, `%w` = 1, ISO year 2025, ISO week 1; the pair is 36 hours apart, so 1.5 days.

**Code:** run with `python3 -I`.
```python
# Q29: SQL versus pandas date gotchas on a six-row frame (week start: Sunday=0 in %w, Monday=0 in pandas; zone: none, all naive)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE t(id INTEGER PRIMARY KEY, d TEXT, d_loose TEXT, a TEXT, b TEXT);
INSERT INTO t VALUES
 (1,'2024-12-30','2024-12-30','2024-01-01 00:00:00','2024-01-02 12:00:00'),
 (2,'2021-01-01','2021-01-01','2024-03-01 10:00:00','2024-03-01 23:00:00'),
 (3,'2023-01-01','2023-01-01','2024-03-01 00:00:00','2024-03-04 00:00:00'),
 (4,'2024-02-29','2024-02-29','2024-03-01 23:00:00','2024-03-02 01:00:00'),
 (5,NULL,NULL,NULL,NULL),
 (6,'2024-01-02','2024-1-02','2024-03-05 00:00:00','2024-03-05 00:00:00');
"""
SQL_ROWS = """
SELECT id,
       CAST(strftime('%w', d) AS INTEGER) AS w_sql,
       ROUND(julianday(b) - julianday(a), 4) AS days_float,
       strftime('%Y', d) AS cal_year,
       strftime('%Y', date(d, '-3 days', 'weekday 4')) AS iso_year,
       (CAST(strftime('%j', date(d, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week
FROM t ORDER BY id
"""
SQL_NULLCMP = """
SELECT SUM(d > '2024-01-01') AS gt, SUM(NOT (d > '2024-01-01')) AS not_gt, COUNT(*) AS n,
       SUM(d IS NULL) AS null_rows
FROM t
"""
SQL_GROUP = "SELECT strftime('%Y', d) AS y, COUNT(*) AS n FROM t GROUP BY 1 ORDER BY 1"
SQL_TEXTCMP = "SELECT id, d_loose, d_loose < '2024-01-05' AS lt_text, date(d_loose) AS date_of_loose FROM t ORDER BY id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_rows = pd.read_sql_query(SQL_ROWS, con)
print(sql_rows.to_string(index=False))
t = pd.read_sql_query("SELECT * FROM t ORDER BY id", con)
d = pd.to_datetime(t["d"]); a = pd.to_datetime(t["a"]); b = pd.to_datetime(t["b"])

# 1 week start: SQLite Sunday = 0, pandas Monday = 0 -> (dayofweek + 1) % 7 maps pandas to %w
w_pd = (d.dt.dayofweek + 1) % 7
print("pandas dayofweek (Mon=0):", d.dt.dayofweek.tolist(), " mapped to Sunday=0:", w_pd.tolist())
# 2 day difference: julianday float vs Timedelta.days (floor) vs total seconds
diff = b - a
print("Timedelta.days (whole days):", diff.dt.days.tolist())
print("Timedelta / 1 day (float):", (diff / pd.Timedelta(days=1)).round(4).tolist())
# 3 NULL versus NaT
sql_null = pd.read_sql_query(SQL_NULLCMP, con)
print(sql_null.to_string(index=False))
pd_gt = int((d > pd.Timestamp("2024-01-01")).sum()); pd_not = int((~(d > pd.Timestamp("2024-01-01"))).sum())
print("pandas (d > ts).sum():", pd_gt, " (~(d > ts)).sum():", pd_not)
# 4 groupby with a missing key
sql_grp = pd.read_sql_query(SQL_GROUP, con)
print(sql_grp.to_string(index=False))
g_default = d.dt.year.groupby(d.dt.year).size()
g_keep = d.dt.year.groupby(d.dt.year, dropna=False).size()
print("pandas groupby default:", g_default.to_dict(), " dropna=False:", {str(k): int(v) for k, v in g_keep.items()})
# 5 text versus datetime
sql_txt = pd.read_sql_query(SQL_TEXTCMP, con)
print(sql_txt.to_string(index=False))
loose = pd.to_datetime(t["d_loose"])
print("pandas parsed d_loose < Timestamp('2024-01-05') ids:", t.loc[loose < pd.Timestamp("2024-01-05"), "id"].tolist(),
      "| SQL text compare ids:", sql_txt.loc[sql_txt["lt_text"] == 1, "id"].tolist())
# 6 ISO year
iso = d.dt.isocalendar()
print("pandas isocalendar year/week:", list(zip(iso["year"].astype("Int64").tolist(), iso["week"].astype("Int64").tolist())))
# 7 Period versus Timestamp
p = pd.Period("2024-01", "M"); ts = pd.Timestamp("2024-01-01")
print("Period('2024-01') == Timestamp('2024-01-01'):", p == ts, "| p.to_timestamp() == ts:", p.to_timestamp() == ts)
left = pd.DataFrame({"k": pd.period_range("2024-01", periods=2, freq="M"), "x": [1, 2]})
right = pd.DataFrame({"k": pd.to_datetime(["2024-01-01", "2024-02-01"]), "y": [3, 4]})
print("merge Period col with datetime col: rows =", len(left.merge(right, on="k")),
      "| after to_timestamp(): rows =", len(left.assign(k=left["k"].dt.to_timestamp()).merge(right, on="k")))
print("SQL text: '2024-01' = '2024-01-01' ->", con.execute("SELECT '2024-01' = '2024-01-01'").fetchone()[0],
      "| date('2024-01') ->", con.execute("SELECT date('2024-01')").fetchone()[0])

# asserts: the columns that are meant to agree
ok = t["d"].notna()
assert w_pd[ok].tolist() == sql_rows.loc[ok, "w_sql"].astype(int).tolist()
assert (diff / pd.Timedelta(days=1)).round(4).dropna().tolist() == sql_rows["days_float"].dropna().tolist()
assert sql_rows.loc[ok, "iso_year"].astype(int).tolist() == iso.loc[ok, "year"].astype(int).tolist()
assert sql_rows.loc[ok, "iso_week"].tolist() == iso.loc[ok, "week"].astype(int).tolist()
assert (int(sql_null["gt"][0]), int(sql_null["not_gt"][0])) == (pd_gt, pd_not - 1)   # NOT(NULL) is NULL, ~NaT-compare is True
assert dict(zip(sql_grp["y"].dropna().astype(int), sql_grp["n"][sql_grp["y"].notna()])) == g_default.to_dict()
# brute force: the ISO emulation against isocalendar() for every day 2000-01-01..2040-12-31
days = pd.date_range("2000-01-01", "2040-12-31", freq="D")
con.execute("CREATE TABLE cal(d TEXT)")
con.executemany("INSERT INTO cal VALUES (?)", [(x,) for x in days.strftime("%Y-%m-%d")])
emu = pd.read_sql_query("""SELECT d, CAST(strftime('%Y', date(d, '-3 days', 'weekday 4')) AS INTEGER) AS iso_year,
       (CAST(strftime('%j', date(d, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week FROM cal ORDER BY d""", con)
ref = days.isocalendar()
assert emu["iso_year"].tolist() == ref["year"].astype(int).tolist()
assert emu["iso_week"].tolist() == ref["week"].astype(int).tolist()
print("ISO emulation date(d,'-3 days','weekday 4') matches isocalendar() on all", len(days), "days 2000-2040")
print("asserts passed (compared in id order)")
```

**Output (my run):**
```text
 id  w_sql  days_float cal_year iso_year  iso_week
  1    1.0      1.5000     2024     2025       1.0
  2    5.0      0.5417     2021     2020      53.0
  3    0.0      3.0000     2023     2022      52.0
  4    4.0      0.0833     2024     2024       9.0
  5    NaN         NaN      NaN      NaN       NaN
  6    2.0      0.0000     2024     2024       1.0
pandas dayofweek (Mon=0): [0.0, 4.0, 6.0, 3.0, nan, 1.0]  mapped to Sunday=0: [1.0, 5.0, 0.0, 4.0, nan, 2.0]
Timedelta.days (whole days): [1.0, 0.0, 3.0, 0.0, nan, 0.0]
Timedelta / 1 day (float): [1.5, 0.5417, 3.0, 0.0833, nan, 0.0]
 gt  not_gt  n  null_rows
  3       2  6          1
pandas (d > ts).sum(): 3  (~(d > ts)).sum(): 3
   y  n
 NaN  1
2021  1
2023  1
2024  3
pandas groupby default: {2021.0: 1, 2023.0: 1, 2024.0: 3}  dropna=False: {'2021.0': 1, '2023.0': 1, '2024.0': 3, 'nan': 1}
 id    d_loose  lt_text date_of_loose
  1 2024-12-30      0.0    2024-12-30
  2 2021-01-01      1.0    2021-01-01
  3 2023-01-01      1.0    2023-01-01
  4 2024-02-29      0.0    2024-02-29
  5        NaN      NaN           NaN
  6  2024-1-02      0.0           NaN
pandas parsed d_loose < Timestamp('2024-01-05') ids: [2, 3, 6] | SQL text compare ids: [2, 3]
pandas isocalendar year/week: [(2025, 1), (2020, 53), (2022, 52), (2024, 9), (<NA>, <NA>), (2024, 1)]
Period('2024-01') == Timestamp('2024-01-01'): False | p.to_timestamp() == ts: True
merge Period col with datetime col: rows = 0 | after to_timestamp(): rows = 2
SQL text: '2024-01' = '2024-01-01' -> 0 | date('2024-01') -> None
ISO emulation date(d,'-3 days','weekday 4') matches isocalendar() on all 14976 days 2000-2040
asserts passed (compared in id order)
```

**Edge cases:**
- NULL row 5: SQL week, difference and ISO columns are NULL; pandas gives NaT, `NaN`, `<NA>`.
- The `NOT` trap: `~(d > x)` in pandas counted the NaT row (3 rows), the SQL `NOT (d > x)` did not (2 rows). That is why I wrote the assert as `pd_not - 1`: the one-row difference is the point.
- `d_loose`: SQL `date('2024-1-02')` returns NULL because SQLite only accepts zero-padded `YYYY-MM-DD`; a text comparison puts `'2024-1-02'` after `'2024-01-05'` (character `1` versus `0` at the sixth position), so the row is wrongly excluded, while pandas parsed it correctly (pandas 3.0.5 parsed `'2024-1-02'` in a column that contained it, as I ran it).
- Period merge: no error and no match; the frame just comes back empty. Convert with `to_timestamp()` first.
- ISO emulation: I ran `date(d, '-3 days', 'weekday 4')` (the Thursday of the ISO week) against `isocalendar()` for every day from 2000-01-01 to 2040-12-31 (14976 days) and both the ISO year and the ISO week (`(%j - 1) / 7 + 1` of that Thursday) matched. Per the Wave A sources note, SQLite 3.45.1 returns NULL for `%G`, `%V`, `%U` and `%g` (I did not re-run those codes here), so the emulation is needed; newer SQLite versions list ISO codes, which this build does not have.
- `%W` in SQLite (Monday-based, week 00 before the first Monday) is not the ISO week; I did not use it for the ISO assert.

**Then explain:**
- Always state: week start, whether differences are floats or whole days, how NULL/NaT are treated, and what zone the timestamps are in.
- `julianday` differences are floats; to get calendar days between dates, wrap both in `date()` first (or round after the subtraction) and decide whether midnight-aligned counts or elapsed time is meant.
- pandas parsing is more forgiving than SQLite, which can hide dirty text; validate with `errors='coerce'` and count the NaT.
- Hedged (not executed): PostgreSQL, MySQL, BigQuery have real date types, so the text-versus-date row mostly does not occur there; `DATEDIFF` arguments differ by engine (Q36).

**Follow-ups:**
- "How would you find mixed-format text dates in a column?" `WHERE date(col) IS NULL AND col IS NOT NULL`.
- "ISO week for 2021-01-01 in pandas?" `isocalendar()` gives year 2020, week 53.
- "Do `groupby` and SQL agree on empty groups?" Neither creates them; use a spine (Q6).

**Common mistakes:**
- Using `%w` and `dayofweek` interchangeably.
- Using `(b - a).dt.days` when elapsed hours matter, or `julianday` when whole days matter.
- Using `~` on a comparison with NaT and counting the missing rows.
- `groupby` without `dropna=False` and silently losing the NaT group.
- Grouping by calendar year and week number near 1 January.

### Q30 ⭐⭐ 🟡 Time zones in pandas: pd.to_datetime(['2024-11-03 01:30'], ...) in America/New_York is ambiguous (clock falls back) and 2024-03-10 02:30 does not exist (spring forward). Show tz_localize raising AmbiguousTimeError and NonExistentTimeError, and the fixes ambiguous='NaT' / True / False array, nonexistent='shift_forward'. Show tz_convert('Asia/Kolkata') (no DST), comparing tz-naive with tz-aware (TypeError), and why timestamps should be stored in UTC. Concept: SQLite has only the 'localtime' and 'utc' modifiers, no named zones.
**Asked at:** pandas time series user guide and DataFrame.resample reference (opened), official documentation and not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Storing naive local times is ambiguous around DST (a clock that falls back repeats 01:30, one that springs forward skips 02:30), so store UTC, convert at the reporting edge, and when you must localise use the `ambiguous` and `nonexistent` arguments; in pandas 3.0.5 here the default failures were plain `ValueError`s (with `ambiguous` / `nonexistent` hints), not the `AmbiguousTimeError` and `NonExistentTimeError` class names in the question, which come from pytz (not installed here).

**Schema and sample data:** no table needed for the pandas part: two naive timestamps (`2024-11-03 01:30` and `2024-03-10 02:30`) and three UTC instants. For SQLite I use text values with explicit offsets. Conventions: America/New_York for the DST cases, Asia/Kolkata (UTC+5:30, no DST) for the report, UTC for storage; no week start involved.

**SQL answer:** SQLite has no named zones, only fixed offsets, the `'utc'` modifier (treats the value as local time and converts to UTC using the host zone) and `'localtime'` (host zone). A trailing offset in the text is parsed and converted to UTC, which resolves the ambiguity explicitly. The query in the Code block:
```sql
SELECT datetime('2024-11-03 01:30:00-04:00') AS first_pass_utc,
       datetime('2024-11-03 01:30:00-05:00') AS second_pass_utc,
       datetime('2024-03-05 20:00:00', '+5 hours', '+30 minutes') AS ist_wall_clock
```

**pandas answer:** `tz_localize` for naive to aware, `tz_convert` for aware to aware. The error handling is a small helper `attempt(label, fn)` in the Code block, which prints the exception class and first line of the message. Fix arguments: `ambiguous='NaT'`, `ambiguous=[True]` (first pass, DST) or `[False]` (second pass, standard time), `nonexistent='shift_forward'`, `'shift_backward'`, `'NaT'` or a `Timedelta`.

**Example:** New York falls back on 2024-11-03 at 02:00 EDT to 01:00 EST. So 01:30 occurs twice: 01:30 EDT (UTC-4) is 05:30 UTC and 01:30 EST (UTC-5) is 06:30 UTC. `ambiguous=[True]` picks the first (05:30 UTC), `[False]` the second (06:30 UTC). On 2024-03-10 at 02:00 EST clocks jump to 03:00 EDT, so 02:30 does not exist: `shift_forward` gives 03:00 EDT, `shift_backward` gives 01:59:59.999999 EST, a `Timedelta('1h')` gives 03:30 EDT. Kolkata is +05:30 all year, so 20:00 UTC is 01:30 the next day in all three sample dates.

**Code:** run with `python3 -I`.
```python
# Q30: time zones in pandas (America/New_York DST edges, Asia/Kolkata); SQLite has only fixed offsets plus 'utc'/'localtime'
import sqlite3
import pandas as pd

def attempt(label, fn):
    try:
        r = fn()
        print(label, "->", r)
        return r
    except Exception as ex:
        print(label, "->", type(ex).__name__ + ":", str(ex).splitlines()[0])

amb = pd.to_datetime(["2024-11-03 01:30"])           # clock falls back: 01:30 happens twice
gap = pd.to_datetime(["2024-03-10 02:30"])           # clock springs forward: 02:30 never happens
print("naive dtype:", amb.dtype)
attempt("ambiguous 01:30 default", lambda: amb.tz_localize("America/New_York"))
attempt("nonexistent 02:30 default", lambda: gap.tz_localize("America/New_York"))
print("pd.errors has AmbiguousTimeError:", hasattr(pd.errors, "AmbiguousTimeError"), "| has NonExistentTimeError:", hasattr(pd.errors, "NonExistentTimeError"))
try:
    import pytz
except ImportError:
    print("pytz is not installed in this environment (pandas 3 uses zoneinfo)")
attempt("ambiguous='NaT'", lambda: amb.tz_localize("America/New_York", ambiguous="NaT"))
first = attempt("ambiguous=True (DST, first pass)", lambda: amb.tz_localize("America/New_York", ambiguous=[True]))
second = attempt("ambiguous=False (standard, second pass)", lambda: amb.tz_localize("America/New_York", ambiguous=[False]))
attempt("nonexistent='shift_forward'", lambda: gap.tz_localize("America/New_York", nonexistent="shift_forward"))
attempt("nonexistent='shift_backward'", lambda: gap.tz_localize("America/New_York", nonexistent="shift_backward"))
attempt("nonexistent='NaT'", lambda: gap.tz_localize("America/New_York", nonexistent="NaT"))
attempt("nonexistent=Timedelta('1h')", lambda: gap.tz_localize("America/New_York", nonexistent=pd.Timedelta("1h")))
print("UTC of the two 01:30s:", first.tz_convert("UTC")[0], "and", second.tz_convert("UTC")[0])

utc = pd.to_datetime(["2024-03-05 20:00:00", "2024-07-01 20:00:00", "2024-12-31 20:00:00"]).tz_localize("UTC")
ist = utc.tz_convert("Asia/Kolkata")
print("Kolkata (no DST, always +05:30):", [str(x) for x in ist])
naive = pd.Timestamp("2024-03-05 20:00:00")
attempt("naive < aware", lambda: naive < utc[0])
attempt("naive == aware", lambda: naive == utc[0])
attempt("Series naive vs aware compare", lambda: pd.Series(pd.to_datetime(["2024-03-05"])) < pd.Series(utc[:1]))
attempt("tz_localize on an already aware index", lambda: utc.tz_localize("Asia/Kolkata"))
print("same instant in two zones is equal:", utc[0] == ist[0])

# SQLite side: fixed offsets only. A text value with an explicit offset resolves the ambiguity by itself.
con = sqlite3.connect(":memory:")
SQL_OFFSET = """
SELECT datetime('2024-11-03 01:30:00-04:00') AS first_pass_utc,
       datetime('2024-11-03 01:30:00-05:00') AS second_pass_utc,
       datetime('2024-03-05 20:00:00', '+5 hours', '+30 minutes') AS ist_wall_clock
"""
row = con.execute(SQL_OFFSET).fetchone()
print("SQLite:", row)
assert row[0] == str(first.tz_convert("UTC")[0].tz_localize(None)).replace("T", " ")
assert row[1] == str(second.tz_convert("UTC")[0].tz_localize(None))
assert row[2] == str(ist[0].tz_localize(None))
print("SQLite datetime('2024-03-10 02:30:00-05:00') =", con.execute("SELECT datetime('2024-03-10 02:30:00-05:00')").fetchone()[0],
      "(SQLite does not know that 02:30 does not exist in New York)")
print("asserts passed: SQLite offset arithmetic == pandas tz_convert for the three instants")
```

**Output (my run):**
```text
naive dtype: datetime64[us]
ambiguous 01:30 default -> ValueError: Cannot infer dst time from 2024-11-03 01:30:00, try using the 'ambiguous' argument
nonexistent 02:30 default -> ValueError: 2024-03-10 02:30:00 is a nonexistent time due to daylight savings time. Try using the 'nonexistent' argument.
pd.errors has AmbiguousTimeError: False | has NonExistentTimeError: False
pytz is not installed in this environment (pandas 3 uses zoneinfo)
ambiguous='NaT' -> DatetimeIndex(['NaT'], dtype='datetime64[us, America/New_York]', freq=None)
ambiguous=True (DST, first pass) -> DatetimeIndex(['2024-11-03 01:30:00-04:00'], dtype='datetime64[us, America/New_York]', freq=None)
ambiguous=False (standard, second pass) -> DatetimeIndex(['2024-11-03 01:30:00-05:00'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent='shift_forward' -> DatetimeIndex(['2024-03-10 03:00:00-04:00'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent='shift_backward' -> DatetimeIndex(['2024-03-10 01:59:59.999999-05:00'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent='NaT' -> DatetimeIndex(['NaT'], dtype='datetime64[us, America/New_York]', freq=None)
nonexistent=Timedelta('1h') -> DatetimeIndex(['2024-03-10 03:30:00-04:00'], dtype='datetime64[us, America/New_York]', freq=None)
UTC of the two 01:30s: 2024-11-03 05:30:00+00:00 and 2024-11-03 06:30:00+00:00
Kolkata (no DST, always +05:30): ['2024-03-06 01:30:00+05:30', '2024-07-02 01:30:00+05:30', '2025-01-01 01:30:00+05:30']
naive < aware -> TypeError: Cannot compare tz-naive and tz-aware timestamps
naive == aware -> False
Series naive vs aware compare -> TypeError: Invalid comparison between dtype=datetime64[us] and DatetimeArray
tz_localize on an already aware index -> TypeError: Already tz-aware, use tz_convert to convert.
same instant in two zones is equal: True
SQLite: ('2024-11-03 05:30:00', '2024-11-03 06:30:00', '2024-03-06 01:30:00')
SQLite datetime('2024-03-10 02:30:00-05:00') = 2024-03-10 07:30:00 (SQLite does not know that 02:30 does not exist in New York)
asserts passed: SQLite offset arithmetic == pandas tz_convert for the three instants
```

**Edge cases:**
- Default behaviour: both ambiguous and nonexistent inputs raised `ValueError` with a hint to use the `ambiguous` or `nonexistent` argument. `pd.errors` in 3.0.5 has no `AmbiguousTimeError` or `NonExistentTimeError`, and pytz is not installed here. With pytz installed, the older class names may appear (not executed here).
- `ambiguous='NaT'` and `nonexistent='NaT'` return NaT, which then silently falls out of groupby (Q29); count them before dropping.
- Comparing naive with aware: `<` raised `TypeError: Cannot compare tz-naive and tz-aware timestamps`; `==` returned False without error. A Series comparison raised `TypeError: Invalid comparison between dtype=datetime64[us] and DatetimeArray`.
- `tz_localize` on an already aware index raised `TypeError: Already tz-aware, use tz_convert to convert.`
- The same instant in two zones is equal (`utc[0] == ist[0]` is True): equality is on the instant, not the wall clock.
- SQLite does not know that 02:30 does not exist: `datetime('2024-03-10 02:30:00-05:00')` simply returned 07:30:00 UTC.
- The `'localtime'` and `'utc'` modifiers depend on the host zone; I did not print their results because they would change with the machine.

**Then explain:**
- Store UTC (an unambiguous instant) and convert to the business zone at the edge; keep the zone name (not just the offset) when you must reproduce local rules in the future.
- Local wall-clock times need a zone name and a rule for the two bad cases; offsets alone resolve only the ambiguous case.
- India has no DST, so IST is a fixed `+05:30`; US/EU zones are not.
- pandas 3 default time unit for strings is microseconds (`datetime64[us]`), as printed.
- Hedged (not executed): PostgreSQL `AT TIME ZONE`, `timestamptz`; MySQL `CONVERT_TZ` (needs zone tables); BigQuery `TIMESTAMP`, `DATETIME(ts, 'Asia/Kolkata')`; I am quoting these from memory.

**Follow-ups:**
- "How do daily counts change with the time zone?" Q16 (the day boundary) and Q38 (DST days with 23 or 25 hours).
- "Why not store local times?" Ambiguity, nonexistence and rule changes.
- "How do I log events from several countries?" UTC plus the user's zone name if needed for reporting.

**Common mistakes:**
- Localising with a fixed offset (`-05:00`) and reading it as New York all year.
- Dropping the NaT rows from `ambiguous='NaT'` without counting them.
- Comparing naive and aware values and catching the `TypeError` with a blanket `except`.
- Using `'localtime'` in SQLite and assuming it is the business zone.

### Q31 ⭐⭐ 🟡 Calendar (date dimension) table: build calendar(cal_date, year, month, quarter, week_start_monday, day_of_week, is_weekend, fiscal_year, fiscal_quarter, is_holiday) for 2023-2024 with a recursive CTE in SQLite, load a small holidays table, and use it to fill zero-sales days and to compute revenue per working day. Explain why a physical calendar table beats generating the spine in every query, and show generate_series and pandas pd.date_range with dt accessors as the equivalents (generate_series hedged, not executed).
**Asked at:** search-result snippets of date-spine and churn guides (Galaxy cohort-churn glossary, a LinkedIn list of time-series SQL topics; not opened), guides and not candidate reports; analyst and data engineer screens
**Say this first (1 line):** A physical `calendar` table (one row per date with year, month, quarter, Monday week start, ISO-style day of week, weekend flag, fiscal year/quarter and holiday flag) is built once with a recursive CTE and then joined, so every report shares the same definitions and zero-sales days appear without rebuilding a spine each time.

**Schema and sample data:** holidays (five rows) and a small sales table (seven rows) with no sales on several days. Conventions: week starts Monday, `day_of_week` is Monday = 1 to Sunday = 7, fiscal year April to March labelled by start year (`FY2023-24`), dates are plain dates (no time zone), range 2023-01-01 to 2024-12-31 (731 days).
```sql
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY, name TEXT);
INSERT INTO holidays VALUES ('2023-01-26','Republic Day'),('2023-08-15','Independence Day'),
  ('2024-01-26','Republic Day'),('2024-08-15','Independence Day'),('2024-03-25','Holi');
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES ('2024-01-02',100),('2024-01-03',200),('2024-01-05',300),('2024-01-06',50),
  ('2024-01-26',70),('2024-02-01',400),('2024-02-02',600);
```

**SQL answer:** `SQL_CAL` builds the table; `SQL_ZERO` fills zero-sales days; `SQL_PER_WD` returns revenue per working day by month (Code block). The Monday week start uses `date(cal_date, 'weekday 0', '-6 days')`.
```sql
CREATE TABLE calendar AS
WITH RECURSIVE d(cal_date) AS (
  SELECT '2023-01-01' UNION ALL SELECT date(cal_date, '+1 day') FROM d WHERE cal_date < '2024-12-31'
), x AS (
  SELECT cal_date,
         CAST(strftime('%Y', cal_date) AS INTEGER) AS year,
         CAST(strftime('%m', cal_date) AS INTEGER) AS month,
         (CAST(strftime('%w', cal_date) AS INTEGER) + 6) % 7 + 1 AS day_of_week
  FROM d
)
SELECT x.cal_date, x.year, x.month,
       (x.month + 2) / 3 AS quarter,
       date(x.cal_date, 'weekday 0', '-6 days') AS week_start_monday,
       x.day_of_week,
       CASE WHEN x.day_of_week >= 6 THEN 1 ELSE 0 END AS is_weekend,
       'FY' || (x.year - (x.month < 4)) || '-' || substr(x.year - (x.month < 4) + 1, 3, 2) AS fiscal_year,
       (x.month + 8) % 12 / 3 + 1 AS fiscal_quarter,
       CASE WHEN h.holiday_date IS NULL THEN 0 ELSE 1 END AS is_holiday
FROM x LEFT JOIN holidays h ON h.holiday_date = x.cal_date
```
```sql
SELECT c.cal_date, c.day_of_week, COALESCE(SUM(s.amount), 0) AS revenue
FROM calendar c LEFT JOIN sales s ON s.sale_date = c.cal_date
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-01-08'
GROUP BY c.cal_date, c.day_of_week ORDER BY c.cal_date
```
```sql
SELECT substr(c.cal_date, 1, 7) AS month,
       COUNT(*) AS days,
       SUM(CASE WHEN c.is_weekend = 0 AND c.is_holiday = 0 THEN 1 ELSE 0 END) AS working_days,
       (SELECT COALESCE(SUM(s.amount), 0) FROM sales s WHERE substr(s.sale_date, 1, 7) = substr(c.cal_date, 1, 7)) AS revenue
FROM calendar c
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-03-01'
GROUP BY substr(c.cal_date, 1, 7) ORDER BY month
```

**pandas answer:** `pd.date_range` plus accessors, with `to_period('Q-MAR')` for the fiscal columns, built as a DataFrame of the same ten columns and compared whole:
```py
dr = pd.date_range("2023-01-01", "2024-12-31", freq="D")
fq = dr.to_period("Q-MAR")
cal_pd = pd.DataFrame({
    "cal_date": dr.strftime("%Y-%m-%d"), "year": dr.year, "month": dr.month, "quarter": dr.quarter,
    "week_start_monday": (dr - pd.to_timedelta(dr.dayofweek, unit="D")).strftime("%Y-%m-%d"),
    "day_of_week": dr.dayofweek + 1, "is_weekend": (dr.dayofweek >= 5).astype(int),
    "fiscal_year": ["FY%d-%02d" % (q.qyear - 1, q.qyear % 100) for q in fq],
    "fiscal_quarter": fq.quarter, "is_holiday": dr.isin(hol).astype(int)})
```

**Example:** 2024-03-31 is a Sunday: `day_of_week` 7, weekend 1, week start Monday 2024-03-25 (the same week as Holi on Monday 25 March, which is flagged `is_holiday`), fiscal year FY2023-24, fiscal quarter 4. 2024-04-01 is a Monday and the first day of FY2024-25 Q1. January 2024: 31 days, 23 weekdays (1 January is a Monday), minus the Friday 26 January holiday = 22 working days; revenue 100 + 200 + 300 + 50 + 70 = 720, so 720 / 22 = 32.73 per working day (the 6 January Saturday sale of 50 and the 26 January holiday sale of 70 are counted in revenue). February 2024: 29 days, 21 weekdays, no holiday; revenue 400 + 600 = 1000; 1000 / 21 = 47.62. In the first week of January the calendar join returns 0 for 1, 4 and 7 January (no sales rows) while the plain sales table would not show them.

**Code:** run with `python3 -I`.
```python
# Q31: calendar (date dimension) table 2023-2024; weeks start Monday; fiscal year April-March; all dates naive
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE holidays(holiday_date TEXT PRIMARY KEY, name TEXT);
INSERT INTO holidays VALUES ('2023-01-26','Republic Day'),('2023-08-15','Independence Day'),
  ('2024-01-26','Republic Day'),('2024-08-15','Independence Day'),('2024-03-25','Holi');
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES ('2024-01-02',100),('2024-01-03',200),('2024-01-05',300),('2024-01-06',50),
  ('2024-01-26',70),('2024-02-01',400),('2024-02-02',600);
"""
SQL_CAL = """
CREATE TABLE calendar AS
WITH RECURSIVE d(cal_date) AS (
  SELECT '2023-01-01' UNION ALL SELECT date(cal_date, '+1 day') FROM d WHERE cal_date < '2024-12-31'
), x AS (
  SELECT cal_date,
         CAST(strftime('%Y', cal_date) AS INTEGER) AS year,
         CAST(strftime('%m', cal_date) AS INTEGER) AS month,
         (CAST(strftime('%w', cal_date) AS INTEGER) + 6) % 7 + 1 AS day_of_week
  FROM d
)
SELECT x.cal_date, x.year, x.month,
       (x.month + 2) / 3 AS quarter,
       date(x.cal_date, 'weekday 0', '-6 days') AS week_start_monday,
       x.day_of_week,
       CASE WHEN x.day_of_week >= 6 THEN 1 ELSE 0 END AS is_weekend,
       'FY' || (x.year - (x.month < 4)) || '-' || substr(x.year - (x.month < 4) + 1, 3, 2) AS fiscal_year,
       (x.month + 8) % 12 / 3 + 1 AS fiscal_quarter,
       CASE WHEN h.holiday_date IS NULL THEN 0 ELSE 1 END AS is_holiday
FROM x LEFT JOIN holidays h ON h.holiday_date = x.cal_date
"""
SQL_ZERO = """
SELECT c.cal_date, c.day_of_week, COALESCE(SUM(s.amount), 0) AS revenue
FROM calendar c LEFT JOIN sales s ON s.sale_date = c.cal_date
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-01-08'
GROUP BY c.cal_date, c.day_of_week ORDER BY c.cal_date
"""
SQL_PER_WD = """
SELECT substr(c.cal_date, 1, 7) AS month,
       COUNT(*) AS days,
       SUM(CASE WHEN c.is_weekend = 0 AND c.is_holiday = 0 THEN 1 ELSE 0 END) AS working_days,
       (SELECT COALESCE(SUM(s.amount), 0) FROM sales s WHERE substr(s.sale_date, 1, 7) = substr(c.cal_date, 1, 7)) AS revenue
FROM calendar c
WHERE c.cal_date >= '2024-01-01' AND c.cal_date < '2024-03-01'
GROUP BY substr(c.cal_date, 1, 7) ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.execute(SQL_CAL)
cal_sql = pd.read_sql_query("SELECT * FROM calendar ORDER BY cal_date", con)
print("rows:", len(cal_sql), "from", cal_sql["cal_date"].iloc[0], "to", cal_sql["cal_date"].iloc[-1])
print(cal_sql[cal_sql["cal_date"].isin(["2023-12-31", "2024-01-01", "2024-03-31", "2024-04-01", "2024-03-25"])].to_string(index=False))
zero = pd.read_sql_query(SQL_ZERO, con)
print(zero.to_string(index=False))
per = pd.read_sql_query(SQL_PER_WD, con)
per["revenue_per_working_day"] = (per["revenue"] / per["working_days"]).round(2)
print(per.to_string(index=False))

# pandas calendar
hol = pd.to_datetime(pd.read_sql_query("SELECT holiday_date FROM holidays", con)["holiday_date"])
dr = pd.date_range("2023-01-01", "2024-12-31", freq="D")
fq = dr.to_period("Q-MAR")
cal_pd = pd.DataFrame({
    "cal_date": dr.strftime("%Y-%m-%d"), "year": dr.year, "month": dr.month, "quarter": dr.quarter,
    "week_start_monday": (dr - pd.to_timedelta(dr.dayofweek, unit="D")).strftime("%Y-%m-%d"),
    "day_of_week": dr.dayofweek + 1, "is_weekend": (dr.dayofweek >= 5).astype(int),
    "fiscal_year": ["FY%d-%02d" % (q.qyear - 1, q.qyear % 100) for q in fq],
    "fiscal_quarter": fq.quarter, "is_holiday": dr.isin(hol).astype(int)})
# compared on all 731 rows in cal_date order, every column
pd.testing.assert_frame_equal(cal_pd, cal_sql, check_dtype=False)
sales = pd.read_sql_query("SELECT * FROM sales", con)
sales["sale_date"] = pd.to_datetime(sales["sale_date"])
daily = sales.groupby("sale_date")["amount"].sum().reindex(pd.date_range("2024-01-01", "2024-01-07"), fill_value=0)
assert daily.tolist() == zero["revenue"].tolist()
c = cal_pd.assign(d=dr)
wd = c[(c["d"] >= "2024-01-01") & (c["d"] < "2024-03-01")]
wd = wd.assign(month=wd["d"].dt.strftime("%Y-%m"), working=((wd["is_weekend"] == 0) & (wd["is_holiday"] == 0)).astype(int))
pd_per = wd.groupby("month").agg(days=("d", "size"), working_days=("working", "sum")).reset_index()
pd_per["revenue"] = pd_per["month"].map(sales.groupby(sales["sale_date"].dt.strftime("%Y-%m"))["amount"].sum()).fillna(0).astype(int)
pd_per["revenue_per_working_day"] = (pd_per["revenue"] / pd_per["working_days"]).round(2)
pd.testing.assert_frame_equal(pd_per, per, check_dtype=False)
print(pd_per.to_string(index=False))
print("asserts passed: SQL calendar == pandas calendar (731 rows x 10 cols), zero-fill and per-working-day match")
```

**Output (my run):**
```text
rows: 731 from 2023-01-01 to 2024-12-31
  cal_date  year  month  quarter week_start_monday  day_of_week  is_weekend fiscal_year  fiscal_quarter  is_holiday
2023-12-31  2023     12        4        2023-12-25            7           1   FY2023-24               3           0
2024-01-01  2024      1        1        2024-01-01            1           0   FY2023-24               4           0
2024-03-25  2024      3        1        2024-03-25            1           0   FY2023-24               4           1
2024-03-31  2024      3        1        2024-03-25            7           1   FY2023-24               4           0
2024-04-01  2024      4        2        2024-04-01            1           0   FY2024-25               1           0
  cal_date  day_of_week  revenue
2024-01-01            1        0
2024-01-02            2      100
2024-01-03            3      200
2024-01-04            4        0
2024-01-05            5      300
2024-01-06            6       50
2024-01-07            7        0
  month  days  working_days  revenue  revenue_per_working_day
2024-01    31            22      720                    32.73
2024-02    29            21     1000                    47.62
  month  days  working_days  revenue  revenue_per_working_day
2024-01    31            22      720                    32.73
2024-02    29            21     1000                    47.62
asserts passed: SQL calendar == pandas calendar (731 rows x 10 cols), zero-fill and per-working-day match
```

**Edge cases:**
- Coverage: the calendar must span the data; a sale outside 2023 to 2024 would not match any calendar row on an inner join, and would be lost. Extend it (or check `MIN`/`MAX`) in the load job.
- Sales on non-working days (a Saturday, a holiday) still add revenue but not working days, so revenue per working day is inflated for those months; decide whether to include them.
- Duplicate holidays: `holiday_date` is a primary key, so the left join cannot fan out the calendar.
- Changing holidays: a physical table needs a maintenance step; the holidays table is the part that changes each year (state dates are not looked up here, these are sample rows).
- Time zones: a `sale_date` derived from UTC may differ from the local date (Q16); build the date column in the reporting zone.
- Leap years: 2024 has 366 days; the table has 731 rows for 2023 and 2024 together, as asserted.

**Then explain:**
- A physical table beats a generated spine because definitions (week start, fiscal year, holidays) live in one place, joins are index-friendly, and analysts do not re-derive them. The recursive CTE is a one-time loader, not a per-query tool.
- Zero-fill: `calendar LEFT JOIN sales` keeps the empty days; a plain `GROUP BY sale_date` cannot.
- Working-day denominators let you compare months of different length.
- Equivalents (generate_series hedged, not executed): PostgreSQL `generate_series('2023-01-01'::date, '2024-12-31'::date, interval '1 day')`; pandas `pd.date_range('2023-01-01', '2024-12-31', freq='D')` with `.dt.year`, `.dt.dayofweek`, and so on (run above).

**Follow-ups:**
- "Add ISO week numbers?" Use the Thursday emulation (Q29/Q43).
- "Multiple countries' holidays?" Add `country` to `holidays` and to the join; the calendar becomes a calendar x country table.
- "Fiscal weeks?" Needs a rule (4-4-5 or 52/53 week); state it first.

**Common mistakes:**
- Generating a spine in every query slightly differently.
- Forgetting the holiday flag for weekends (it still must not subtract twice).
- Hard-coding Sunday-start weeks in one report and Monday-start in another.
- Letting the calendar end before the latest data date.

### Q32 ⭐⭐ 🔴 Fiscal-year-over-year comparison with missing months: monthly_revenue(month, revenue) for FY2023-24 and FY2024-25 where some months are missing. Return for each fiscal month (April = 1 to March = 12) revenue this fiscal year, revenue last fiscal year, and YoY percent, plus fiscal year-to-date for both years up to the latest loaded month only (so a half-loaded FY2024-25 compares to the same months of the prior year, not the full year). Build with a fiscal calendar spine and conditional aggregation; pandas: pivot on fiscal month and fiscal year with reindex 1..12 and cumsum limited by the last loaded month.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Map each month to a fiscal year and a fiscal month (April = 1 ... March = 12), join onto a 1-to-12 fiscal-month spine, use conditional aggregation to put this year and last year side by side, and compute year-to-date only up to the latest loaded fiscal month of the current year so a half-loaded year is compared with the same months of the prior year, not with its full total.

**Schema and sample data:** FY2023-24 has no August 2023; FY2024-25 is loaded through September 2024 (fiscal month 6) and is missing July 2024. Conventions: fiscal year April to March labelled by start year (`fy` = 2024 means FY2024-25), fiscal month = `(month + 8) % 12 + 1`, `month` column stores the first of the month as text, no time zone.
```sql
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES
 ('2023-04-01',100),('2023-05-01',110),('2023-06-01',120),('2023-07-01',130),
 ('2023-09-01',150),('2023-10-01',160),('2023-11-01',170),('2023-12-01',180),
 ('2024-01-01',190),('2024-02-01',200),('2024-03-01',210),
 ('2024-04-01',120),('2024-05-01',121),('2024-06-01',132),
 ('2024-08-01',140),('2024-09-01',165);
```

**SQL answer:** `SQL_MAIN` in the Code block. `cur` is the latest fiscal year in the data, `latest` is its highest loaded fiscal month, `spine` is 1 to 12, `g` pivots the two years with `SUM(CASE ...)`, and the year-to-date columns are running sums that are blanked beyond the latest loaded month.
```sql
WITH f AS (
  SELECT revenue,
         CAST(strftime('%Y', month) AS INTEGER) - (CAST(strftime('%m', month) AS INTEGER) < 4) AS fy,
         (CAST(strftime('%m', month) AS INTEGER) + 8) % 12 + 1 AS fm
  FROM monthly_revenue
), cur AS (SELECT MAX(fy) AS fy FROM f),
latest AS (SELECT MAX(fm) AS fm FROM f WHERE fy = (SELECT fy FROM cur)),
spine(fm) AS (SELECT 1 UNION ALL SELECT fm + 1 FROM spine WHERE fm < 12),
g AS (
  SELECT s.fm,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) THEN f.revenue END) AS rev_this,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) - 1 THEN f.revenue END) AS rev_last
  FROM spine s LEFT JOIN f ON f.fm = s.fm
  GROUP BY s.fm
)
SELECT fm, rev_this, rev_last,
       ROUND(100.0 * (rev_this - rev_last) / NULLIF(rev_last, 0), 1) AS yoy_pct,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_this, 0)) OVER (ORDER BY fm) END AS ytd_this,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_last, 0)) OVER (ORDER BY fm) END AS ytd_last
FROM g ORDER BY fm
```

**pandas answer:** `pivot_table` on fiscal month and fiscal year, `reindex(range(1, 13))`, `cumsum` of `fillna(0)` and `where(fm <= latest_fm)`:
```py
p = mr["month"].dt.to_period("Q-MAR")
mr["fy"] = p.dt.qyear - 1
mr["fm"] = (mr["month"].dt.month + 8) % 12 + 1
piv = mr.pivot_table(index="fm", columns="fy", values="revenue", aggfunc="sum").reindex(range(1, 13))
cur_fy = mr["fy"].max()
rev_this, rev_last = piv[cur_fy], piv[cur_fy - 1]
latest_fm = int(mr.loc[mr["fy"] == cur_fy, "fm"].max())
pdf = pd.DataFrame({"fm": piv.index, "rev_this": rev_this.to_numpy(), "rev_last": rev_last.to_numpy()})
pdf["yoy_pct"] = (100.0 * (pdf["rev_this"] - pdf["rev_last"]) / pdf["rev_last"].replace(0, np.nan)).round(1)
mask = pdf["fm"] <= latest_fm
pdf["ytd_this"] = pdf["rev_this"].fillna(0).cumsum().where(mask)
pdf["ytd_last"] = pdf["rev_last"].fillna(0).cumsum().where(mask)
```

**Example:** this year (FY2024-25) by fiscal month: Apr 120, May 121, Jun 132, Jul missing, Aug 140, Sep 165. Last year: Apr 100, May 110, Jun 120, Jul 130, Aug missing, Sep 150, Oct 160 ... Mar 210. YoY for April: (120 - 100) / 100 = 20.0%; for July and August the result is NULL because one side is missing. Year-to-date through September (fiscal month 6): this year 120 + 121 + 132 + 0 + 140 + 165 = 678, last year 100 + 110 + 120 + 130 + 0 + 150 = 610, so 678 versus 610 is +11.1%. Comparing 678 to the full last year (1720) would give -60.6%.

**Code:** run with `python3 -I`.
```python
# Q32: fiscal-year-over-year with missing months; fiscal year April-March, label = start year; as-of = latest loaded month
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES
 ('2023-04-01',100),('2023-05-01',110),('2023-06-01',120),('2023-07-01',130),
 ('2023-09-01',150),('2023-10-01',160),('2023-11-01',170),('2023-12-01',180),
 ('2024-01-01',190),('2024-02-01',200),('2024-03-01',210),
 ('2024-04-01',120),('2024-05-01',121),('2024-06-01',132),
 ('2024-08-01',140),('2024-09-01',165);
"""
# 2023-08 (last year) and 2024-07 (this year) are missing. Latest loaded month: 2024-09 = fiscal month 6.
SQL_MAIN = """
WITH f AS (
  SELECT revenue,
         CAST(strftime('%Y', month) AS INTEGER) - (CAST(strftime('%m', month) AS INTEGER) < 4) AS fy,
         (CAST(strftime('%m', month) AS INTEGER) + 8) % 12 + 1 AS fm
  FROM monthly_revenue
), cur AS (SELECT MAX(fy) AS fy FROM f),
latest AS (SELECT MAX(fm) AS fm FROM f WHERE fy = (SELECT fy FROM cur)),
spine(fm) AS (SELECT 1 UNION ALL SELECT fm + 1 FROM spine WHERE fm < 12),
g AS (
  SELECT s.fm,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) THEN f.revenue END) AS rev_this,
         SUM(CASE WHEN f.fy = (SELECT fy FROM cur) - 1 THEN f.revenue END) AS rev_last
  FROM spine s LEFT JOIN f ON f.fm = s.fm
  GROUP BY s.fm
)
SELECT fm, rev_this, rev_last,
       ROUND(100.0 * (rev_this - rev_last) / NULLIF(rev_last, 0), 1) AS yoy_pct,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_this, 0)) OVER (ORDER BY fm) END AS ytd_this,
       CASE WHEN fm <= (SELECT fm FROM latest)
            THEN SUM(COALESCE(rev_last, 0)) OVER (ORDER BY fm) END AS ytd_last
FROM g ORDER BY fm
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_df["ytd_pct"] = (100.0 * (sql_df["ytd_this"] - sql_df["ytd_last"]) / sql_df["ytd_last"]).round(1)
print(sql_df.to_string(index=False))
last_row = sql_df.dropna(subset=["ytd_this"]).iloc[-1]
print("YTD through fiscal month %d: this FY %d vs last FY %d -> %.1f%%" % (last_row["fm"], last_row["ytd_this"], last_row["ytd_last"], last_row["ytd_pct"]))
full_last = pd.read_sql_query("SELECT SUM(revenue) AS s FROM monthly_revenue WHERE month < '2024-04-01'", con)["s"][0]
print("wrong comparison (this YTD vs the full last FY):", round(100.0 * (last_row["ytd_this"] - full_last) / full_last, 1), "% with last FY total", full_last)

mr = pd.read_sql_query("SELECT * FROM monthly_revenue", con)
mr["month"] = pd.to_datetime(mr["month"])
p = mr["month"].dt.to_period("Q-MAR")
mr["fy"] = p.dt.qyear - 1
mr["fm"] = (mr["month"].dt.month + 8) % 12 + 1
piv = mr.pivot_table(index="fm", columns="fy", values="revenue", aggfunc="sum").reindex(range(1, 13))
cur_fy = mr["fy"].max()
rev_this, rev_last = piv[cur_fy], piv[cur_fy - 1]
latest_fm = int(mr.loc[mr["fy"] == cur_fy, "fm"].max())
pdf = pd.DataFrame({"fm": piv.index, "rev_this": rev_this.to_numpy(), "rev_last": rev_last.to_numpy()})
pdf["yoy_pct"] = (100.0 * (pdf["rev_this"] - pdf["rev_last"]) / pdf["rev_last"].replace(0, np.nan)).round(1)
mask = pdf["fm"] <= latest_fm
pdf["ytd_this"] = pdf["rev_this"].fillna(0).cumsum().where(mask)
pdf["ytd_last"] = pdf["rev_last"].fillna(0).cumsum().where(mask)
pdf["ytd_pct"] = (100.0 * (pdf["ytd_this"] - pdf["ytd_last"]) / pdf["ytd_last"]).round(1)
# compared on fiscal month 1..12, NaN == NULL
pd.testing.assert_frame_equal(pdf, sql_df, check_dtype=False)
print("asserts passed: SQL == pandas pivot/reindex/cumsum for fiscal months 1..12; cur FY start year =", cur_fy, "latest fm =", latest_fm)
```

**Output (my run):**
```text
 fm  rev_this  rev_last  yoy_pct  ytd_this  ytd_last  ytd_pct
  1     120.0     100.0     20.0     120.0     100.0     20.0
  2     121.0     110.0     10.0     241.0     210.0     14.8
  3     132.0     120.0     10.0     373.0     330.0     13.0
  4       NaN     130.0      NaN     373.0     460.0    -18.9
  5     140.0       NaN      NaN     513.0     460.0     11.5
  6     165.0     150.0     10.0     678.0     610.0     11.1
  7       NaN     160.0      NaN       NaN       NaN      NaN
  8       NaN     170.0      NaN       NaN       NaN      NaN
  9       NaN     180.0      NaN       NaN       NaN      NaN
 10       NaN     190.0      NaN       NaN       NaN      NaN
 11       NaN     200.0      NaN       NaN       NaN      NaN
 12       NaN     210.0      NaN       NaN       NaN      NaN
YTD through fiscal month 6: this FY 678 vs last FY 610 -> 11.1%
wrong comparison (this YTD vs the full last FY): -60.6 % with last FY total 1720
asserts passed: SQL == pandas pivot/reindex/cumsum for fiscal months 1..12; cur FY start year = 2024 latest fm = 6
```

**Edge cases:**
- Missing month inside the loaded range (July 2024, August 2023): the monthly revenue and YoY are NULL for that month, and the YTD treats a missing month as 0. That is an assumption (no sales); if the month was simply not loaded, YTD is understated, and the per-month YTD percent is misleading at that point (fiscal month 4 shows -18.9%, a result of the missing July 2024, which then recovers to +11.5% at month 5 when last year's August is the missing one). Report the missing months next to the YTD.
- Future fiscal months (7 to 12): this-year columns are NULL and the YTD columns are NULL because they are beyond the latest loaded month; last year's later months are still shown in `rev_last` but not accumulated.
- Zero base: `NULLIF(rev_last, 0)` returns NULL instead of an error; pandas replaces 0 with NaN for the same effect.
- Duplicate month rows: `SUM(CASE ...)` would add them; the primary key on `month` prevents it. If the feed can restate months, deduplicate first.
- Fiscal year naming: here `fy` is the start year; do not mix with pandas `qyear` (end year) without the subtract of 1 (the code does).
- If the latest loaded month is mid-month (partial month), YTD for that month is partial; this question assumes complete loaded months.

**Then explain:**
- The spine guarantees 12 rows even if neither year has a row for a fiscal month; the join to the data is a `LEFT JOIN`.
- "Up to the latest loaded month only" is `latest_fm = MAX(fm)` for the current fiscal year, applied as a mask to both years' running totals so the comparison is like for like.
- Conditional aggregation (`SUM(CASE WHEN fy = ... THEN revenue END)`) is the SQL pivot; pandas does it with `pivot_table`.
- Hedged (not executed): engines with `PIVOT` clauses (SQL Server, Snowflake, Oracle) would shorten the pivot step; `generate_series` can supply the 1 to 12 spine in PostgreSQL.

**Follow-ups:**
- "Show all 12 months of last year as a forecast base?" Keep the columns but separate actual from baseline.
- "Quarter-level fiscal YoY?" Aggregate by fiscal quarter first (Q25), then compare.
- "What if the fiscal year changes definition?" Put the mapping in the calendar table (Q31).

**Common mistakes:**
- Comparing a half-loaded year with a full prior year.
- `LAG(revenue, 12)` on rows with gaps (Q17).
- Treating a missing month as 0 without saying so.
- Mixing fiscal year labels (start year versus end year).

### Q33 ⭐⭐ 🔴 Churn and resurrection by month: events(user_id, event_ts). Classify each user-month transition as new (first ever active month), retained (active in m-1 and m), churned (active in m-1 but not m), and resurrected (active in m, not in m-1, but active in some earlier month). Return counts per month in a reconciling table (previous active = retained + churned; active = new + retained + resurrected). Build from distinct user-month pairs and a first-active-month CTE; pandas with merge and set logic. Streak and island logic is Part 7; stay at the m-1 versus m level.
**Asked at:** search-result snippets of date-spine and churn guides (Galaxy cohort-churn glossary, a LinkedIn list of time-series SQL topics; not opened), guides and not candidate reports; analyst and data engineer screens
**Say this first (1 line):** Reduce the events to distinct (user, calendar month) pairs, compute each user's first active month, then for each month classify active users as new (first month), retained (active last month too) or resurrected (not active last month but active in some earlier month), count churned as last month's users missing from this month, and prove the two identities: previous active = retained + churned, and active = new + retained + resurrected.

**Schema and sample data:** six users over January to June 2024; nobody is active in April, which stresses the spine; user 2 has events at 23:59:59 on 31 January and 00:00:00 on 1 March (no February event). Conventions: month = calendar month of `event_ts` as stored (UTC, no conversion); a user is active in a month if they have at least one event; stay at the m-1 versus m level (streaks and islands are Part 7).
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-05 10:00:00'),(1,'2024-01-20 11:00:00'),(1,'2024-02-03 09:00:00'),(1,'2024-03-10 09:00:00'),
 (2,'2024-01-31 23:59:59'),(2,'2024-03-01 00:00:00'),(2,'2024-05-02 08:00:00'),
 (3,'2024-02-01 00:00:00'),(3,'2024-03-15 12:00:00'),
 (4,'2024-03-20 12:00:00'),(4,'2024-05-21 12:00:00'),(4,'2024-06-01 12:00:00'),
 (5,'2024-05-09 12:00:00'),
 (6,'2024-06-30 23:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block: `um` (distinct user-months), `first`, a month `spine`, `cur` (each user-month with a "was active last month" flag via `EXISTS`), `act` (new, retained, resurrected, active) and `lost` (churned, attributed to the month after their last active month).
```sql
WITH um AS (
  SELECT DISTINCT user_id, date(event_ts, 'start of month') AS m FROM events
), first AS (
  SELECT user_id, MIN(m) AS first_m FROM um GROUP BY user_id
), spine(m) AS (
  SELECT MIN(m) FROM um
  UNION ALL SELECT date(m, '+1 month') FROM spine WHERE m < (SELECT MAX(m) FROM um)
), cur AS (
  SELECT u.m, f.first_m,
         EXISTS (SELECT 1 FROM um p WHERE p.user_id = u.user_id AND p.m = date(u.m, '-1 month')) AS was_prev
  FROM um u JOIN first f ON f.user_id = u.user_id
), act AS (
  SELECT m, COUNT(*) AS active,
         SUM(CASE WHEN first_m = m THEN 1 ELSE 0 END) AS new,
         SUM(CASE WHEN first_m < m AND was_prev = 1 THEN 1 ELSE 0 END) AS retained,
         SUM(CASE WHEN first_m < m AND was_prev = 0 THEN 1 ELSE 0 END) AS resurrected
  FROM cur GROUP BY m
), lost AS (
  SELECT date(p.m, '+1 month') AS m, COUNT(*) AS churned
  FROM um p
  WHERE NOT EXISTS (SELECT 1 FROM um c WHERE c.user_id = p.user_id AND c.m = date(p.m, '+1 month'))
  GROUP BY 1
)
SELECT strftime('%Y-%m', s.m) AS month,
       COALESCE((SELECT active FROM act WHERE act.m = date(s.m, '-1 month')), 0) AS prev_active,
       COALESCE(a.new, 0) AS new, COALESCE(a.retained, 0) AS retained,
       COALESCE(l.churned, 0) AS churned, COALESCE(a.resurrected, 0) AS resurrected,
       COALESCE(a.active, 0) AS active
FROM spine s
LEFT JOIN act a ON a.m = s.m
LEFT JOIN lost l ON l.m = s.m
ORDER BY s.m
```

**pandas answer:** the same logic with merges: shift each pair forward one month to test "active last month" and backward to find users with no next month; `first_m` comes from `groupby(...).transform('min')`. A third check re-derives the counts with Python sets.
```py
um = ev.assign(m=ev["event_ts"].dt.to_period("M"))[["user_id", "m"]].drop_duplicates()
um["first_m"] = um.groupby("user_id")["m"].transform("min")
prev = um[["user_id", "m"]].assign(m=lambda x: x["m"] + 1, was_prev=True)          # shift each pair forward one month
cur = um.merge(prev, on=["user_id", "m"], how="left").fillna({"was_prev": False})
cur["kind"] = "new"
cur.loc[(cur["first_m"] < cur["m"]) & cur["was_prev"].astype(bool), "kind"] = "retained"
cur.loc[(cur["first_m"] < cur["m"]) & ~cur["was_prev"].astype(bool), "kind"] = "resurrected"
counts = cur.pivot_table(index="m", columns="kind", values="user_id", aggfunc="nunique").reindex(columns=["new", "retained", "resurrected"])
# churned: a pair (user, m) with no pair (user, m+1); attribute it to month m+1
nxt = um[["user_id", "m"]].assign(m=lambda x: x["m"] - 1, has_next=True)
lost = um[["user_id", "m"]].merge(nxt, on=["user_id", "m"], how="left")
churned = lost[lost["has_next"].isna()].assign(m=lambda x: x["m"] + 1).groupby("m")["user_id"].nunique().rename("churned")
```

**Example:** January: users 1 and 2 are new (2). February: user 1 retained, user 3 new, user 2 churned (active in January, not February). March: user 1 and user 3 retained (2), user 4 new, user 2 resurrected (first seen January, absent February, back in March): active 4. April: nobody active, so all four March users churned (4). May: user 5 new, users 2 and 4 resurrected (both were active in March, absent in April): active 3. June: user 4 retained, user 6 new, users 2 and 5 churned: active 2. Reconciliation for May: previous active 0 (April) = retained 0 + churned 0; active 3 = new 1 + retained 0 + resurrected 2.

**Code:** run with `python3 -I`.
```python
# Q33: new / retained / churned / resurrected per calendar month (UTC dates as stored; month = calendar month of event_ts)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-05 10:00:00'),(1,'2024-01-20 11:00:00'),(1,'2024-02-03 09:00:00'),(1,'2024-03-10 09:00:00'),
 (2,'2024-01-31 23:59:59'),(2,'2024-03-01 00:00:00'),(2,'2024-05-02 08:00:00'),
 (3,'2024-02-01 00:00:00'),(3,'2024-03-15 12:00:00'),
 (4,'2024-03-20 12:00:00'),(4,'2024-05-21 12:00:00'),(4,'2024-06-01 12:00:00'),
 (5,'2024-05-09 12:00:00'),
 (6,'2024-06-30 23:00:00');
"""
SQL_MAIN = """
WITH um AS (
  SELECT DISTINCT user_id, date(event_ts, 'start of month') AS m FROM events
), first AS (
  SELECT user_id, MIN(m) AS first_m FROM um GROUP BY user_id
), spine(m) AS (
  SELECT MIN(m) FROM um
  UNION ALL SELECT date(m, '+1 month') FROM spine WHERE m < (SELECT MAX(m) FROM um)
), cur AS (
  SELECT u.m, f.first_m,
         EXISTS (SELECT 1 FROM um p WHERE p.user_id = u.user_id AND p.m = date(u.m, '-1 month')) AS was_prev
  FROM um u JOIN first f ON f.user_id = u.user_id
), act AS (
  SELECT m, COUNT(*) AS active,
         SUM(CASE WHEN first_m = m THEN 1 ELSE 0 END) AS new,
         SUM(CASE WHEN first_m < m AND was_prev = 1 THEN 1 ELSE 0 END) AS retained,
         SUM(CASE WHEN first_m < m AND was_prev = 0 THEN 1 ELSE 0 END) AS resurrected
  FROM cur GROUP BY m
), lost AS (
  SELECT date(p.m, '+1 month') AS m, COUNT(*) AS churned
  FROM um p
  WHERE NOT EXISTS (SELECT 1 FROM um c WHERE c.user_id = p.user_id AND c.m = date(p.m, '+1 month'))
  GROUP BY 1
)
SELECT strftime('%Y-%m', s.m) AS month,
       COALESCE((SELECT active FROM act WHERE act.m = date(s.m, '-1 month')), 0) AS prev_active,
       COALESCE(a.new, 0) AS new, COALESCE(a.retained, 0) AS retained,
       COALESCE(l.churned, 0) AS churned, COALESCE(a.resurrected, 0) AS resurrected,
       COALESCE(a.active, 0) AS active
FROM spine s
LEFT JOIN act a ON a.m = s.m
LEFT JOIN lost l ON l.m = s.m
ORDER BY s.m
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
assert (sql_df["prev_active"] == sql_df["retained"] + sql_df["churned"]).all()
assert (sql_df["active"] == sql_df["new"] + sql_df["retained"] + sql_df["resurrected"]).all()

ev = pd.read_sql_query("SELECT * FROM events", con)
ev["event_ts"] = pd.to_datetime(ev["event_ts"])
um = ev.assign(m=ev["event_ts"].dt.to_period("M"))[["user_id", "m"]].drop_duplicates()
um["first_m"] = um.groupby("user_id")["m"].transform("min")
prev = um[["user_id", "m"]].assign(m=lambda x: x["m"] + 1, was_prev=True)          # shift each pair forward one month
cur = um.merge(prev, on=["user_id", "m"], how="left").fillna({"was_prev": False})
cur["kind"] = "new"
cur.loc[(cur["first_m"] < cur["m"]) & cur["was_prev"].astype(bool), "kind"] = "retained"
cur.loc[(cur["first_m"] < cur["m"]) & ~cur["was_prev"].astype(bool), "kind"] = "resurrected"
counts = cur.pivot_table(index="m", columns="kind", values="user_id", aggfunc="nunique").reindex(columns=["new", "retained", "resurrected"])
# churned: a pair (user, m) with no pair (user, m+1); attribute it to month m+1
nxt = um[["user_id", "m"]].assign(m=lambda x: x["m"] - 1, has_next=True)
lost = um[["user_id", "m"]].merge(nxt, on=["user_id", "m"], how="left")
churned = lost[lost["has_next"].isna()].assign(m=lambda x: x["m"] + 1).groupby("m")["user_id"].nunique().rename("churned")
spine = pd.period_range(um["m"].min(), um["m"].max(), freq="M")
pd_df = counts.join(churned, how="outer").reindex(spine).fillna(0).astype(int)
pd_df["active"] = pd_df["new"] + pd_df["retained"] + pd_df["resurrected"]
pd_df["prev_active"] = pd_df["active"].shift(1, fill_value=0)
pd_df = pd_df.rename_axis("month").reset_index()
pd_df["month"] = pd_df["month"].astype(str)
pd_df = pd_df[["month", "prev_active", "new", "retained", "churned", "resurrected", "active"]]
# compared in month order
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)

# third check: plain Python set logic per month
sets = um.groupby("m")["user_id"].agg(set)
seen = set()
for m in spine:
    c, p = sets.get(m, set()), sets.get(m - 1, set())
    row = sql_df[sql_df["month"] == str(m)].iloc[0]
    assert (len(c - seen), len(c & p), len(p - c), len((c - p) & seen)) == (row["new"], row["retained"], row["churned"], row["resurrected"])
    seen |= c
print("asserts passed: SQL == pandas merge logic == set logic; both reconciliations hold in every month")
```

**Output (my run):**
```text
  month  prev_active  new  retained  churned  resurrected  active
2024-01            0    2         0        0            0       2
2024-02            2    1         1        1            0       2
2024-03            2    1         2        0            1       4
2024-04            4    0         0        4            0       0
2024-05            0    1         0        0            2       3
2024-06            3    1         1        2            0       2
asserts passed: SQL == pandas merge logic == set logic; both reconciliations hold in every month
```

**Edge cases:**
- Empty month (April): the spine keeps it with active 0; without the spine the churn of four users would be invisible and May's two resurrected users would look like "returning after a gap" with no gap visible.
- Both identities are asserted for every month: `prev_active = retained + churned` and `active = new + retained + resurrected`. In May `prev_active` is 0 (April had no users), so nobody can be retained or churned.
- Churn is counted in the month after the user's last active month, so churn for the month after the last data month (July) is not reported; the final month's actives are not yet known to churn.
- Duplicate events in the same month: `DISTINCT` on (user, month) counts once (user 1 has two January events).
- A user active only in the latest month is new, not resurrected.
- Month boundary: user 2's 23:59:59 event on 31 January belongs to January; shifting the time zone (UTC versus IST) could move it to February and change the classification.
- A user whose events are exactly one month apart repeatedly is "retained" each time; a gap of one month flips them through "churned" then "resurrected" (user 2 in March, May).
- Definition caveat: "churned" here means absent for one calendar month; many products define churn after 30 or 90 days of inactivity, which is a different definition.

**Then explain:**
- Work with a distinct user-month table; everything is a membership test between month m-1 and month m.
- Resurrected = active in m, not active in m-1, but active in some earlier month (`first_m < m` and `was_prev = 0`). New = `first_m = m`.
- Month arithmetic on first-of-month dates with `date(m, '-1 month')` is safe, because day 1 never overflows (compare Q8).
- Hedged (not executed): PostgreSQL `date_trunc('month', event_ts)` and `generate_series` for the spine; BigQuery `DATE_TRUNC` and `GENERATE_DATE_ARRAY`; MySQL 8 uses a recursive CTE as here.

**Follow-ups:**
- "Add a rate?" retention = retained / prev_active, churn = churned / prev_active (NULLIF the denominator); Q18 has the month-over-month retention.
- "Resurrection after at least 3 months away?" That needs gap length (Part 7 territory).
- "By segment?" Add the segment to the pairs and the spine as in Q41.

**Common mistakes:**
- Calling every non-retained returning user new.
- No month spine, so empty months disappear and the identities fail.
- Counting events instead of distinct users.
- Attributing churn to the last active month instead of the first absent month (and then the identities do not reconcile).
- Treating the latest month's missing users as churned when the month is still open.
