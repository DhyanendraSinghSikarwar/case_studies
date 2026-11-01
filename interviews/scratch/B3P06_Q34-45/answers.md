### Q34 ⭐⭐ 🔴 Active subscriptions per month from date ranges: subscriptions(sub_id, user_id, plan_price, start_date, end_date) where end_date is NULL for active subscriptions. For each month return the number of subscriptions active at month end, new, ended, and monthly recurring revenue, using a month spine and a range join (start_date <= month_end AND (end_date IS NULL OR end_date >= month_end)). Discuss inclusive versus exclusive end_date and a subscription that starts and ends in the same month, then give the pandas version with date_range and a cross merge or interval masks.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build a month spine with a month_end for each row, join subscriptions on `start_date <= month_end AND (end_date IS NULL OR end_date >= month_end)` to get who is active at month end, count new and ended with separate range tests on the month itself, and sum plan_price over the active set for MRR.

**Schema and sample data:** six subscriptions. Sub 2 ends exactly on a month end, sub 3 starts and ends inside February, sub 4 starts on the leap day, user 2 comes back with a new subscription (sub 6). Convention: `end_date` is inclusive (the last day of service), dates are plain `YYYY-MM-DD` text, no time zone, no weeks involved.
```sql
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, plan_price INTEGER,
                           start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1, 1, 10, '2024-01-10', NULL),
 (2, 2, 20, '2024-01-20', '2024-03-31'),
 (3, 3, 30, '2024-02-05', '2024-02-20'),
 (4, 4, 15, '2024-02-29', NULL),
 (5, 5, 40, '2024-03-15', '2024-05-10'),
 (6, 2, 25, '2024-05-01', NULL);
```

**SQL answer:** the spine is a recursive CTE (`SQL_MAIN` in the Code block). Each measure is its own scalar subquery because the three measures use different membership rules; one join carrying all three would fan rows out and mix the rules.
```sql
WITH RECURSIVE spine(month_start) AS (
  SELECT '2024-01-01'
  UNION ALL
  SELECT date(month_start, '+1 month') FROM spine WHERE month_start < '2024-06-01'
), ms AS (
  SELECT strftime('%Y-%m', month_start) AS month,
         month_start,
         date(month_start, '+1 month', '-1 day') AS month_end
  FROM spine
)
SELECT ms.month,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS active_at_end,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date BETWEEN ms.month_start AND ms.month_end) AS new_subs,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.end_date BETWEEN ms.month_start AND ms.month_end) AS ended_subs,
  (SELECT COALESCE(SUM(s.plan_price), 0) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS mrr
FROM ms
ORDER BY ms.month
```
The exclusive-end_date variant changes one test, `s.end_date >= ms.month_end` becomes `s.end_date > ms.month_end` (`SQL_EXCL` in the code).

**pandas answer:** `date_range(..., freq="ME")` for the spine, a cross merge for the range join, boolean masks for each measure, then one `groupby`.
```py
spine = pd.DataFrame({"month_end": pd.date_range("2024-01-31", periods=6, freq="ME")})
spine["month_start"] = spine["month_end"].dt.to_period("M").dt.start_time
spine["month"] = spine["month_end"].dt.strftime("%Y-%m")
x = spine.merge(subs, how="cross")
x["active"] = (x["start_date"] <= x["month_end"]) & (x["end_date"].isna() | (x["end_date"] >= x["month_end"]))
x["new_subs"] = (x["start_date"] >= x["month_start"]) & (x["start_date"] <= x["month_end"])
x["ended_subs"] = x["end_date"].notna() & (x["end_date"] >= x["month_start"]) & (x["end_date"] <= x["month_end"])
x["mrr"] = x["plan_price"].where(x["active"], 0)
pd_df = (x.groupby("month", as_index=False)
          .agg(active_at_end=("active", "sum"), new_subs=("new_subs", "sum"),
               ended_subs=("ended_subs", "sum"), mrr=("mrr", "sum")))
```

**Example:**
- Jan (month end 01-31): sub 1 (start 01-10, open) and sub 2 (start 01-20, ends 03-31) are active, so active = 2 and MRR = 10 + 20 = 30. New = 2 (subs 1 and 2). Ended = 0.
- Feb (02-29): sub 3 started 02-05 and ended 02-20, so it is not active at month end. Active = subs 1, 2, 4 = 3, MRR = 10 + 20 + 15 = 45. New = 2 (subs 3 and 4), ended = 1 (sub 3).
- Mar (03-31): sub 5 starts 03-15. Sub 2 ends 03-31, which is inclusive, so it still counts: active = subs 1, 2, 4, 5 = 4, MRR = 85. Under an exclusive end_date sub 2 is gone at 03-31: active 3, MRR 65 (the `SQL_EXCL` output).
- May (05-31): sub 5 ended 05-10, sub 6 (user 2, 25) started 05-01: active = subs 1, 4, 6 = 3, MRR = 10 + 15 + 25 = 50.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q34: active subscriptions per month from date ranges (month spine + range join)
# Convention: end_date is INCLUSIVE (last day of service); dates are plain 'YYYY-MM-DD' text, no time zone.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, plan_price INTEGER,
                           start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1, 1, 10, '2024-01-10', NULL),
 (2, 2, 20, '2024-01-20', '2024-03-31'),
 (3, 3, 30, '2024-02-05', '2024-02-20'),
 (4, 4, 15, '2024-02-29', NULL),
 (5, 5, 40, '2024-03-15', '2024-05-10'),
 (6, 2, 25, '2024-05-01', NULL);
"""

SQL_MAIN = """
WITH RECURSIVE spine(month_start) AS (
  SELECT '2024-01-01'
  UNION ALL
  SELECT date(month_start, '+1 month') FROM spine WHERE month_start < '2024-06-01'
), ms AS (
  SELECT strftime('%Y-%m', month_start) AS month,
         month_start,
         date(month_start, '+1 month', '-1 day') AS month_end
  FROM spine
)
SELECT ms.month,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS active_at_end,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.start_date BETWEEN ms.month_start AND ms.month_end) AS new_subs,
  (SELECT COUNT(*) FROM subscriptions s
    WHERE s.end_date BETWEEN ms.month_start AND ms.month_end) AS ended_subs,
  (SELECT COALESCE(SUM(s.plan_price), 0) FROM subscriptions s
    WHERE s.start_date <= ms.month_end
      AND (s.end_date IS NULL OR s.end_date >= ms.month_end)) AS mrr
FROM ms
ORDER BY ms.month
"""

# Variant: end_date EXCLUSIVE (first day with no service): only the active test changes.
SQL_EXCL = SQL_MAIN.replace("s.end_date >= ms.month_end", "s.end_date > ms.month_end")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
subs = pd.read_sql_query("SELECT * FROM subscriptions", con,
                         parse_dates=["start_date", "end_date"])

# --- pandas ---
spine = pd.DataFrame({"month_end": pd.date_range("2024-01-31", periods=6, freq="ME")})
spine["month_start"] = spine["month_end"].dt.to_period("M").dt.start_time
spine["month"] = spine["month_end"].dt.strftime("%Y-%m")
x = spine.merge(subs, how="cross")
x["active"] = (x["start_date"] <= x["month_end"]) & (x["end_date"].isna() | (x["end_date"] >= x["month_end"]))
x["new_subs"] = (x["start_date"] >= x["month_start"]) & (x["start_date"] <= x["month_end"])
x["ended_subs"] = x["end_date"].notna() & (x["end_date"] >= x["month_start"]) & (x["end_date"] <= x["month_end"])
x["mrr"] = x["plan_price"].where(x["active"], 0)
pd_df = (x.groupby("month", as_index=False)
          .agg(active_at_end=("active", "sum"), new_subs=("new_subs", "sum"),
               ended_subs=("ended_subs", "sum"), mrr=("mrr", "sum")))
# --- end pandas ---

sql_df = pd.read_sql_query(SQL_MAIN, con)
excl_df = pd.read_sql_query(SQL_EXCL, con)
# compare after sorting by month, ignoring dtype (SQL int64 vs pandas int64/bool sums)
pd.testing.assert_frame_equal(sql_df.sort_values("month").reset_index(drop=True),
                              pd_df.sort_values("month").reset_index(drop=True), check_dtype=False)
print("SQL (end_date inclusive):")
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nSQL with EXCLUSIVE end_date (only active_at_end and mrr change):")
print(excl_df.to_string(index=False))
```

**Output (my run):**
```text
SQL (end_date inclusive):
  month  active_at_end  new_subs  ended_subs  mrr
2024-01              2         2           0   30
2024-02              3         2           1   45
2024-03              4         1           1   85
2024-04              3         0           0   65
2024-05              3         1           1   50
2024-06              3         0           0   50

pandas equals SQL: OK

SQL with EXCLUSIVE end_date (only active_at_end and mrr change):
  month  active_at_end  new_subs  ended_subs  mrr
2024-01              2         2           0   30
2024-02              3         2           1   45
2024-03              3         1           1   65
2024-04              3         0           0   65
2024-05              3         1           1   50
2024-06              3         0           0   50
```

**Edge cases:**
- Starts and ends in the same month (sub 3): it is counted in `new_subs` and `ended_subs` for February and never in `active_at_end`, so new minus ended does not equal the change in active when the month-end snapshot is used. Say which definition the report uses.
- End on the month-end day (sub 2): the single biggest source of off-by-one in this question. Inclusive end_date means active that day; exclusive means not. Ask which one the table uses, or read a few rows.
- `end_date IS NULL` must be tested explicitly, because `NULL >= month_end` is unknown and would drop every open subscription.
- A user with two subscriptions (user 2) is counted twice in `active_at_end` if both overlap; use `COUNT(DISTINCT user_id)` if the question is about users. `new_subs` also counts sub 6 as new although user 2 is a returning customer.
- A month with no active subscription still gets a row (zero) because the spine drives the query; `COALESCE(SUM(...), 0)` keeps MRR at 0 instead of NULL. `SUM` ignores a NULL plan_price.
- "Active at any time in the month" is a different definition (`start_date <= month_end AND (end_date IS NULL OR end_date >= month_start)`); do not mix the two in one report.
- Other engines (not executed here): the spine would come from `generate_series` in PostgreSQL or `GENERATE_DATE_ARRAY` in BigQuery instead of a recursive CTE, and `date(month_start, '+1 month', '-1 day')` becomes `LAST_DAY()` or `EOMONTH()` in some engines; see Q36.

**Then explain:**
- A range join matches a point (month end) to an interval (start to end); open-ended intervals use NULL, so the predicate must handle NULL on purpose.
- The spine is what makes empty months appear; without it a month with zero active subscriptions vanishes and any later LAG compares the wrong months (Part 5 and Q45).
- MRR here is the sum of the plan price of subscriptions active at month end; it ignores proration and mid-month changes, which is a modelling choice to state.
- pandas does the same with a cross merge (6 months x 6 subs = 36 rows here), which is fine for a toy but grows as months x subscriptions; at scale use `merge_asof`, an interval index or sort-based counting (start counts minus end counts, cumulated).

**Follow-ups:**
- How would you get monthly churn? Ended in month m divided by active at the end of month m-1 (cohort classification of new, retained, churned is Q33).
- What if the columns are timestamps? Then `end_date >= month_end` fails for an end at 14:00 on the last day; compare with a half-open `end_ts >= next_month_start` style bound (Q39, Q45).
- How do you avoid the cross merge in pandas? Count starts and ends per month with `value_counts`/`resample`, then `cumsum` the difference; that would give the active count without the 36-row product (not run here).

**Common mistakes:**
- Joining once and computing `new`, `ended` and `active` from the same joined rows, which multiplies rows.
- Forgetting `IS NULL` for open subscriptions.
- Using `BETWEEN` on timestamps for the month window.
- Building the spine from the data instead of a calendar, so quiet months disappear.

### Q35 ⭐ 🟡 Late-arriving data and event time versus processing time: events(event_id, user_id, event_ts, loaded_at). Explain why a daily report for yesterday changes tomorrow, show a query that reports by event_ts and a restated-total comparison versus the figures first published (using loaded_at <= a cut-off), and discuss lookback windows, reprocessing and how cohort retention for the latest month shifts as late rows land. Concept plus a small runnable example; no streaming tooling.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Rows arrive after the day they describe, so a report for yesterday is only a snapshot as of a load cut-off; I group by `event_ts` (not `loaded_at`), reproduce what was published with `loaded_at <= first_cutoff`, compare it with a later cut-off to see the restatement, and handle it with a lookback window that reprocesses the last few days.

**Schema and sample data:** twelve events. Events 3, 4, 7 and 8 land late (hours to days). Convention: `event_ts` and `loaded_at` are UTC text, the day is the UTC date, no week logic, and the cut-offs are fixed strings (never `now`) so the run is repeatable. Feb events 10 to 13 form a cohort of four users, March events 6, 7 and 8 are their return activity.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, loaded_at TEXT);
INSERT INTO events VALUES
 (10, 1, '2024-02-05 10:00:00', '2024-02-05 10:05:00'),
 (11, 2, '2024-02-06 11:00:00', '2024-02-06 11:05:00'),
 (12, 3, '2024-02-07 12:00:00', '2024-02-07 12:05:00'),
 (13, 4, '2024-02-08 13:00:00', '2024-02-08 13:05:00'),
 (1,  5, '2024-03-01 00:10:00', '2024-03-01 00:15:00'),
 (2,  6, '2024-03-01 10:00:00', '2024-03-01 10:05:00'),
 (3,  7, '2024-03-01 23:50:00', '2024-03-02 09:00:00'),
 (4,  8, '2024-03-01 12:00:00', '2024-03-04 08:00:00'),
 (5,  1, '2024-03-02 09:00:00', '2024-03-02 09:05:00'),
 (6,  2, '2024-03-10 09:00:00', '2024-03-10 09:05:00'),
 (7,  3, '2024-03-30 22:00:00', '2024-04-03 09:00:00'),
 (8,  4, '2024-03-31 21:00:00', '2024-04-05 09:00:00');
```

**SQL answer:** per event day, rows loaded by the first cut-off (`published`), rows loaded by the later cut-off (`restated`) and their difference (`SQL_MAIN`). `SUM(loaded_at <= :c1)` works in SQLite because a comparison is 0 or 1; other engines need `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` or `COUNT(*) FILTER (WHERE ...)` (PostgreSQL, not executed here).
```sql
SELECT date(event_ts) AS event_day,
       SUM(loaded_at <= :c1) AS published,
       SUM(loaded_at <= :c2) AS restated,
       SUM(loaded_at <= :c2) - SUM(loaded_at <= :c1) AS late_rows
FROM events
WHERE event_ts >= '2024-03-01' AND event_ts < '2024-03-03'
GROUP BY date(event_ts)
ORDER BY event_day
```
The retention-shift query (`SQL_RET`) takes the Feb-active users as the cohort and counts March activity that had been loaded by a cut-off.
```sql
WITH cohort AS (SELECT DISTINCT user_id FROM events WHERE event_ts >= '2024-02-01' AND event_ts < '2024-03-01'),
     back AS (SELECT DISTINCT user_id FROM events
              WHERE event_ts >= '2024-03-01' AND event_ts < '2024-04-01' AND loaded_at <= :cut)
SELECT COUNT(*) AS cohort_size, COUNT(b.user_id) AS retained,
       ROUND(100.0 * COUNT(b.user_id) / COUNT(*), 1) AS retention_pct
FROM cohort c LEFT JOIN back b ON b.user_id = c.user_id
```

**pandas answer:** boolean columns for "loaded by cut-off" and a `groupby` on the event day.
```py
ev = pd.read_sql_query("SELECT * FROM events", con, parse_dates=["event_ts", "loaded_at"])
win = ev[(ev["event_ts"] >= "2024-03-01") & (ev["event_ts"] < "2024-03-03")].copy()
win["event_day"] = win["event_ts"].dt.strftime("%Y-%m-%d")
win["published"] = win["loaded_at"] <= pd.Timestamp(C1)
win["restated"] = win["loaded_at"] <= pd.Timestamp(C2)
pd_df = win.groupby("event_day", as_index=False).agg(published=("published", "sum"), restated=("restated", "sum"))
pd_df["late_rows"] = pd_df["restated"] - pd_df["published"]
```

**Example:**
- Report for 2024-03-01, first published 2024-03-02 06:00:00: events 1 and 2 were loaded the same day, event 3 (event at 23:50) was loaded 03-02 09:00 and event 4 (event at 12:00) on 03-04. Published = 2. At the 03-06 cut-off all four are in, restated = 4, so the first number was 50% too low (2 late rows).
- 2024-03-02: event 5 occurred at 09:00, after the 06:00 publication, so published = 0 (a day still open) and restated = 1.
- Grouping the same rows by load date gives 2 and 2, which is the wrong axis: event 3 belongs to 03-01 but would be counted on 03-02.
- Largest arrival lags: event 8 is 4.5 days, event 7 is 3.46 days, event 4 is 2.83 days. A 3-day lookback would still miss events 7 and 8, so the window must be at least 5 days for this feed.
- Retention of the Feb cohort (users 1 to 4) in March: as of 2024-04-01 only users 1 and 2 have loaded March activity, 2 of 4 = 50.0%. As of 2024-04-10 users 3 and 4 have arrived (events 7 and 8, loaded 04-03 and 04-05): 4 of 4 = 100.0%. The latest month looked like a retention collapse that was a loading delay.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q35: late-arriving data, event time vs processing time (loaded_at)
# Convention: event_ts and loaded_at are UTC text 'YYYY-MM-DD HH:MM:SS'; the "day" is the UTC date; fixed cut-offs, never now().
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, loaded_at TEXT);
INSERT INTO events VALUES
 (10, 1, '2024-02-05 10:00:00', '2024-02-05 10:05:00'),
 (11, 2, '2024-02-06 11:00:00', '2024-02-06 11:05:00'),
 (12, 3, '2024-02-07 12:00:00', '2024-02-07 12:05:00'),
 (13, 4, '2024-02-08 13:00:00', '2024-02-08 13:05:00'),
 (1,  5, '2024-03-01 00:10:00', '2024-03-01 00:15:00'),
 (2,  6, '2024-03-01 10:00:00', '2024-03-01 10:05:00'),
 (3,  7, '2024-03-01 23:50:00', '2024-03-02 09:00:00'),
 (4,  8, '2024-03-01 12:00:00', '2024-03-04 08:00:00'),
 (5,  1, '2024-03-02 09:00:00', '2024-03-02 09:05:00'),
 (6,  2, '2024-03-10 09:00:00', '2024-03-10 09:05:00'),
 (7,  3, '2024-03-30 22:00:00', '2024-04-03 09:00:00'),
 (8,  4, '2024-03-31 21:00:00', '2024-04-05 09:00:00');
"""
C1 = "2024-03-02 06:00:00"   # when the report for 2024-03-01 was first published
C2 = "2024-03-06 00:00:00"   # the restatement cut-off

SQL_MAIN = """
SELECT date(event_ts) AS event_day,
       SUM(loaded_at <= :c1) AS published,
       SUM(loaded_at <= :c2) AS restated,
       SUM(loaded_at <= :c2) - SUM(loaded_at <= :c1) AS late_rows
FROM events
WHERE event_ts >= '2024-03-01' AND event_ts < '2024-03-03'
GROUP BY date(event_ts)
ORDER BY event_day
"""
SQL_BY_LOAD = """
SELECT date(loaded_at) AS load_day, COUNT(*) AS n
FROM events WHERE loaded_at >= '2024-03-01' AND loaded_at < '2024-03-03'
GROUP BY date(loaded_at) ORDER BY load_day
"""
SQL_LAG = """
SELECT event_id, ROUND(julianday(loaded_at) - julianday(event_ts), 2) AS lag_days
FROM events ORDER BY lag_days DESC, event_id LIMIT 3
"""
# Feb-active users (the cohort); retained = any March event LOADED by the cut-off
SQL_RET = """
WITH cohort AS (SELECT DISTINCT user_id FROM events WHERE event_ts >= '2024-02-01' AND event_ts < '2024-03-01'),
     back AS (SELECT DISTINCT user_id FROM events
              WHERE event_ts >= '2024-03-01' AND event_ts < '2024-04-01' AND loaded_at <= :cut)
SELECT COUNT(*) AS cohort_size, COUNT(b.user_id) AS retained,
       ROUND(100.0 * COUNT(b.user_id) / COUNT(*), 1) AS retention_pct
FROM cohort c LEFT JOIN back b ON b.user_id = c.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"c1": C1, "c2": C2})

# --- pandas ---
ev = pd.read_sql_query("SELECT * FROM events", con, parse_dates=["event_ts", "loaded_at"])
win = ev[(ev["event_ts"] >= "2024-03-01") & (ev["event_ts"] < "2024-03-03")].copy()
win["event_day"] = win["event_ts"].dt.strftime("%Y-%m-%d")
win["published"] = win["loaded_at"] <= pd.Timestamp(C1)
win["restated"] = win["loaded_at"] <= pd.Timestamp(C2)
pd_df = win.groupby("event_day", as_index=False).agg(published=("published", "sum"), restated=("restated", "sum"))
pd_df["late_rows"] = pd_df["restated"] - pd_df["published"]
# --- end pandas ---

pd.testing.assert_frame_equal(sql_df.sort_values("event_day").reset_index(drop=True),
                              pd_df.sort_values("event_day").reset_index(drop=True), check_dtype=False)
print("report by event_ts, first published at", C1, "vs restated at", C2)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nsame two days grouped by loaded_at date (wrong axis):")
print(pd.read_sql_query(SQL_BY_LOAD, con).to_string(index=False))
print("\nlargest arrival lags (days):")
print(pd.read_sql_query(SQL_LAG, con).to_string(index=False))
for cut in ("2024-04-01 00:00:00", "2024-04-10 00:00:00"):
    r = pd.read_sql_query(SQL_RET, con, params={"cut": cut})
    print("\nMarch retention of the Feb cohort as of", cut)
    print(r.to_string(index=False))
    # pandas cross-check
    feb = set(ev[(ev.event_ts >= "2024-02-01") & (ev.event_ts < "2024-03-01")].user_id)
    mar = set(ev[(ev.event_ts >= "2024-03-01") & (ev.event_ts < "2024-04-01") & (ev.loaded_at <= pd.Timestamp(cut))].user_id)
    assert (len(feb), len(feb & mar)) == (int(r.cohort_size[0]), int(r.retained[0]))
```

**Output (my run):**
```text
report by event_ts, first published at 2024-03-02 06:00:00 vs restated at 2024-03-06 00:00:00
 event_day  published  restated  late_rows
2024-03-01          2         4          2
2024-03-02          0         1          1

pandas equals SQL: OK

same two days grouped by loaded_at date (wrong axis):
  load_day  n
2024-03-01  2
2024-03-02  2

largest arrival lags (days):
 event_id  lag_days
        8      4.50
        7      3.46
        4      2.83

March retention of the Feb cohort as of 2024-04-01 00:00:00
 cohort_size  retained  retention_pct
           4         2           50.0

March retention of the Feb cohort as of 2024-04-10 00:00:00
 cohort_size  retained  retention_pct
           4         4          100.0
```

**Edge cases:**
- `loaded_at` NULL (not yet loaded): `NULL <= cut-off` is unknown, so the row is excluded, which is the right as-of behaviour.
- Duplicates from retries or replays: dedupe on `event_id` before counting, and keep the first `loaded_at`; if reprocessing overwrites `loaded_at`, you can no longer reproduce an old cut-off.
- Events whose `event_ts` is in the future (device clock skew) or before the load window: decide whether they are dropped or flagged.
- A restated figure can also go down (events deleted or deduplicated later), so do not assume only increases.
- Time zone: if event_ts is device local time and loaded_at is server UTC, lag arithmetic is wrong by the offset.

**Then explain:**
- Event time is when the thing happened; processing (load) time is when the warehouse knew about it. Daily jobs aggregate what is loaded, so day D is incomplete when first computed and grows afterwards.
- Keep the published numbers (a snapshot table with an `as_of` column) so a restatement can be shown; the `loaded_at <= cut-off` filter reproduces the old view from raw data.
- Lookback and reprocessing: each run recomputes the last N days from raw data and overwrites those days (idempotent, same result when re-run); N comes from the lag distribution (a high percentile of `loaded_at - event_ts`), and days older than N are called final.
- Cohort retention: the cohort (denominator) is fixed by earlier months; the numerator for the latest month keeps growing as late rows land, so retention for immature or recent periods is flagged provisional, or computed only for periods older than the lookback.
- No streaming tooling is needed to reason about this; it is a batch-reporting concern.

**Follow-ups:**
- How do you tell stakeholders a number changed? Show the first-published and restated figures side by side with the cut-offs, and publish the lookback policy.
- Should you report by loaded_at instead? It never changes, but it answers "what arrived today", not "what happened that day"; use it for pipeline monitoring, not business reporting.
- What about the "as of" timestamp in code? Pass it as a parameter, as here, never `now()`, so a past report can be re-run.

**Common mistakes:**
- Grouping by `loaded_at` and calling it the daily number.
- Comparing the latest, still-landing month with older complete months.
- Using the current time inside the query, so reruns give different answers.
- Treating the first published number as the truth, or silently overwriting it without a record.

### Q36 ⭐ 🟡 Dialect map for date functions (hedge everything not run on SQLite 3.45): DATE_TRUNC, EXTRACT, DATE_PART, DATEDIFF argument orders, DATE_ADD and INTERVAL, generate_series, AGE in PostgreSQL, DATE_FORMAT and TIMESTAMPDIFF in MySQL, DATE_TRUNC with TIMESTAMP_TRUNC and DATE_DIFF in BigQuery, DATEADD and DATEDIFF in Snowflake and SQL Server. Pair each with the SQLite expression that is run (strftime, date modifiers, julianday), stress that the sign and order of DATEDIFF arguments differ between engines, and label every non-SQLite line 'not executed'.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** The functions differ per engine, and the one that bites is DATEDIFF, because the argument order and the sign change between engines; in SQLite I use `julianday(b) - julianday(a)` for days, `strftime` for extraction and formatting, and date modifiers for truncation and addition, and I label every non-SQLite line below as not executed.

**Schema and sample data:** no table is needed, two fixed dates stand in for columns: A = `2024-01-31` and B = `2024-03-15` (2024 is a leap year). Convention: plain dates, no time zone, weeks start on Monday where a week appears.

**SQL answer:** these are the SQLite expressions that ran (the list `SQLITE` in the Code block), each paired with the engine function it stands in for. Output of the run is below.
| Concept (engine function it stands in for) | SQLite expression (run) | Result |
|---|---|---|
| truncate to month (DATE_TRUNC) | `date('2024-03-15', 'start of month')` | `2024-03-01` |
| truncate to Monday week | `date('2024-03-15', '-6 days', 'weekday 1')` | `2024-03-11` |
| EXTRACT(year) | `CAST(strftime('%Y', '2024-03-15') AS INTEGER)` | `2024` |
| EXTRACT(month) | `CAST(strftime('%m', '2024-03-15') AS INTEGER)` | `3` |
| day of week, Mon=1..Sun=7 (ISODOW) | `CAST(strftime('%u', '2024-03-15') AS INTEGER)` | `5` |
| format as YYYY-MM (DATE_FORMAT) | `strftime('%Y-%m', '2024-03-15')` | `2024-03` |
| days between: B - A (DATEDIFF) | `CAST(julianday('2024-03-15') - julianday('2024-01-31') AS INTEGER)` | `44` |
| days between: A - B (sign flipped) | `CAST(julianday('2024-01-31') - julianday('2024-03-15') AS INTEGER)` | `-44` |
| add one month (DATE_ADD/INTERVAL) | `date('2024-01-31', '+1 month')` | `2024-03-02` |
| end of month (LAST_DAY/EOMONTH) | `date('2024-03-15', 'start of month', '+1 month', '-1 day')` | `2024-03-31` |
| elapsed whole months A to B | `(CAST(strftime('%Y','2024-03-15') AS INT)-CAST(strftime('%Y','2024-01-31') AS INT))*12 + CAST(strftime('%m','2024-03-15') AS INT)-CAST(strftime('%m','2024-01-31') AS INT) - (strftime('%d','2024-03-15') < strftime('%d','2024-01-31'))` | `1` |
| month boundaries crossed A to B | `(CAST(strftime('%Y','2024-03-15') AS INT)-CAST(strftime('%Y','2024-01-31') AS INT))*12 + CAST(strftime('%m','2024-03-15') AS INT)-CAST(strftime('%m','2024-01-31') AS INT)` | `2` |

Dialect lines from memory, **not executed here** (I did not run any of these engines; check each against the vendor documentation):
- PostgreSQL: `DATE_TRUNC('month', ts)`; `EXTRACT(YEAR FROM ts)` and `DATE_PART('year', ts)`; `date_b - date_a` gives integer days (so B - A is positive); `AGE(b, a)` returns an interval in years, months, days; `ts + INTERVAL '1 month'`; `generate_series(start, stop, INTERVAL '1 day')`; `to_char(ts, 'YYYY-MM')`.
- MySQL: `DATE_FORMAT(d, '%Y-%m')`; `DATEDIFF(b, a)` is `b - a` in days (later date first, opposite to SQL Server); `TIMESTAMPDIFF(MONTH, a, b)` is `b - a` in the unit, earlier date first, whole units elapsed; `DATE_ADD(d, INTERVAL 1 MONTH)`; `EXTRACT(YEAR FROM d)`; `LAST_DAY(d)`; no `DATE_TRUNC` as far as I recall; a series needs a recursive CTE (MySQL 8).
- BigQuery: `DATE_TRUNC(d, MONTH)` for DATE and `TIMESTAMP_TRUNC(ts, MONTH)` for TIMESTAMP; `DATE_DIFF(b, a, DAY)` is `b - a` (later date first); `DATE_ADD(d, INTERVAL 1 MONTH)`; `EXTRACT(YEAR FROM d)`; `GENERATE_DATE_ARRAY(start, end, INTERVAL 1 DAY)` with `UNNEST`; `FORMAT_DATE('%Y-%m', d)`.
- Snowflake: `DATEDIFF(day, a, b)` is `b - a` (unit first, earlier date first); `DATEADD(month, 1, d)`; `DATE_TRUNC('month', d)`; I believe month and year differences count calendar boundaries crossed.
- SQL Server: `DATEDIFF(day, a, b)` is `b - a`, and it counts date-part boundaries crossed, so `DATEDIFF(month, '2024-01-31', '2024-02-01')` is 1; `DATEADD(month, 1, d)`; `EOMONTH(d)`; `DATETRUNC` exists only from SQL Server 2022 as far as I recall.
- Week start differs and must be stated: PostgreSQL `DATE_TRUNC('week', ...)` starts Monday; BigQuery `DATE_TRUNC(d, WEEK)` starts Sunday unless `WEEK(MONDAY)` is given; MySQL `WEEK()` takes a mode argument; Snowflake depends on a session parameter. All from memory, not executed.

**pandas answer:** the same quantities, which agree with SQLite on every row that can be compared (assert in the code). pandas has no DATEDIFF: subtract Timestamps for days, subtract Periods for calendar months.
```py
a, b = pd.Timestamp(A), pd.Timestamp(B)
pd_vals = {
 "truncate to month (DATE_TRUNC)": str(b.to_period("M").start_time.date()),
 "truncate to Monday week": str((b - pd.Timedelta(days=b.weekday())).date()),
 "EXTRACT(year)": b.year,
 "EXTRACT(month)": b.month,
 "day of week, Mon=1..Sun=7 (ISODOW)": b.isoweekday(),
 "format as YYYY-MM (DATE_FORMAT)": b.strftime("%Y-%m"),
 "days between: B - A (DATEDIFF)": (b - a).days,
 "days between: A - B (sign flipped)": (a - b).days,
 "add one month (DATE_ADD/INTERVAL)": "n/a (pandas clips instead, see below)",
 "end of month (LAST_DAY/EOMONTH)": str((b + pd.offsets.MonthEnd(0)).date()),
 "elapsed whole months A to B": (b.to_period("M") - a.to_period("M")).n - (b.day < a.day),
 "month boundaries crossed A to B": (b.to_period("M") - a.to_period("M")).n,
}
pd_series = [str(d.date()) for d in pd.date_range(A, periods=4, freq="D")]
```

**Example:** A = 2024-01-31, B = 2024-03-15.
- Days: 2024-01-31 to 2024-03-01 is 30 days (February has 29), plus 14 more to March 15 is 44. Swapping the operands gives -44: the same sign trap as `DATEDIFF` argument order.
- Month boundaries crossed: January to March is 2 (this is what SQL Server style `DATEDIFF(month, ...)` counts). Whole months elapsed: 2024-01-31 plus 1 month is 2024-02-29 (clipped), plus 2 months is 2024-03-31, which is after March 15, so 1.
- Truncations: month start 2024-03-01, Monday of the week 2024-03-11 (March 15 is a Friday, `%u` = 5), end of month 2024-03-31.
- Add one month to 2024-01-31: SQLite gives 2024-03-02 (overflow), pandas `DateOffset(months=1)` gives 2024-02-29 (clip).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q36: dialect map for date functions. ONLY the SQLite 3.45.1 and pandas 3.x lines below are executed.
# Convention: plain dates, no time zone; a week starts on Monday where a week matters.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
A, B = "2024-01-31", "2024-03-15"      # fixed example dates, never today

# (concept, SQLite expression that is run)
SQLITE = [
 ("truncate to month (DATE_TRUNC)",      f"date('{B}', 'start of month')"),
 ("truncate to Monday week",             f"date('{B}', '-6 days', 'weekday 1')"),
 ("EXTRACT(year)",                       f"CAST(strftime('%Y', '{B}') AS INTEGER)"),
 ("EXTRACT(month)",                      f"CAST(strftime('%m', '{B}') AS INTEGER)"),
 ("day of week, Mon=1..Sun=7 (ISODOW)",  f"CAST(strftime('%u', '{B}') AS INTEGER)"),
 ("format as YYYY-MM (DATE_FORMAT)",     f"strftime('%Y-%m', '{B}')"),
 ("days between: B - A (DATEDIFF)",      f"CAST(julianday('{B}') - julianday('{A}') AS INTEGER)"),
 ("days between: A - B (sign flipped)",  f"CAST(julianday('{A}') - julianday('{B}') AS INTEGER)"),
 ("add one month (DATE_ADD/INTERVAL)",   f"date('{A}', '+1 month')"),
 ("end of month (LAST_DAY/EOMONTH)",     f"date('{B}', 'start of month', '+1 month', '-1 day')"),
 ("elapsed whole months A to B",         f"(CAST(strftime('%Y','{B}') AS INT)-CAST(strftime('%Y','{A}') AS INT))*12"
                                         f" + CAST(strftime('%m','{B}') AS INT)-CAST(strftime('%m','{A}') AS INT)"
                                         f" - (strftime('%d','{B}') < strftime('%d','{A}'))"),
 ("month boundaries crossed A to B",     f"(CAST(strftime('%Y','{B}') AS INT)-CAST(strftime('%Y','{A}') AS INT))*12"
                                         f" + CAST(strftime('%m','{B}') AS INT)-CAST(strftime('%m','{A}') AS INT)"),
]
res = {c: con.execute("SELECT " + e).fetchone()[0] for c, e in SQLITE}
for c, v in res.items():
    print(f"{c:38s} {v}")

# generate_series emulation: recursive CTE (standard SQL, runs on SQLite)
SQL_SERIES = """
WITH RECURSIVE s(d) AS (SELECT '2024-01-31' UNION ALL SELECT date(d, '+1 day') FROM s WHERE d < '2024-02-03')
SELECT d FROM s
"""
series = [r[0] for r in con.execute(SQL_SERIES)]
print("\nrecursive-CTE series:", series)

# --- pandas ---
a, b = pd.Timestamp(A), pd.Timestamp(B)
pd_vals = {
 "truncate to month (DATE_TRUNC)": str(b.to_period("M").start_time.date()),
 "truncate to Monday week": str((b - pd.Timedelta(days=b.weekday())).date()),
 "EXTRACT(year)": b.year,
 "EXTRACT(month)": b.month,
 "day of week, Mon=1..Sun=7 (ISODOW)": b.isoweekday(),
 "format as YYYY-MM (DATE_FORMAT)": b.strftime("%Y-%m"),
 "days between: B - A (DATEDIFF)": (b - a).days,
 "days between: A - B (sign flipped)": (a - b).days,
 "add one month (DATE_ADD/INTERVAL)": "n/a (pandas clips instead, see below)",
 "end of month (LAST_DAY/EOMONTH)": str((b + pd.offsets.MonthEnd(0)).date()),
 "elapsed whole months A to B": (b.to_period("M") - a.to_period("M")).n - (b.day < a.day),
 "month boundaries crossed A to B": (b.to_period("M") - a.to_period("M")).n,
}
pd_series = [str(d.date()) for d in pd.date_range(A, periods=4, freq="D")]
# --- end pandas ---
for c, v in pd_vals.items():
    if not str(v).startswith("n/a"):
        assert res[c] == v, (c, res[c], v)
assert series == pd_series
print("\npandas equals SQLite on every comparable row: OK")

# the add-one-month difference between engines (SQLite overflows, pandas clips)
print("\nSQLite date('2024-01-31','+1 month') =", con.execute("SELECT date('2024-01-31','+1 month')").fetchone()[0])
print("SQLite date('2023-01-31','+1 month') =", con.execute("SELECT date('2023-01-31','+1 month')").fetchone()[0])
print("pandas Timestamp('2024-01-31') + DateOffset(months=1) =", (a + pd.DateOffset(months=1)).date())
print("pandas Timestamp('2023-01-31') + DateOffset(months=1) =", (pd.Timestamp("2023-01-31") + pd.DateOffset(months=1)).date())
print("SQLite 3.45.1 'end of month' modifier:", con.execute("SELECT date('2024-03-15','end of month')").fetchone()[0], "(NULL = not supported here)")
print("SQLite 3.45.1 strftime('%V'):", con.execute("SELECT strftime('%V','2024-03-15')").fetchone()[0], "(NULL = not supported here)")

# pandas extras from the hedge list
s = pd.Series(pd.to_datetime(["2024-03-15"]))
try:
    s.dt.floor("MS")
except Exception as e:
    print("\ndt.floor('MS') ->", type(e).__name__ + ":", e)
p = s.dt.to_period("Q-MAR")
print("to_period('Q-MAR'):", p.iloc[0], "| qyear:", p.dt.qyear.iloc[0], "| quarter:", p.dt.quarter.iloc[0])
print("np.busday_count('2024-01-01','2024-01-15') =", np.busday_count("2024-01-01", "2024-01-15"), "(end excluded, Mon-Fri)")
print("np.busday_count with holidays=['2024-01-02'] =", np.busday_count("2024-01-01", "2024-01-15", holidays=["2024-01-02"]))
bd = pd.bdate_range("2024-01-01", "2024-01-12", freq="C", holidays=["2024-01-02"])
print("bdate_range freq='C' with holiday:", [str(d.date()) for d in bd])
```

**Output (my run):**
```text
truncate to month (DATE_TRUNC)         2024-03-01
truncate to Monday week                2024-03-11
EXTRACT(year)                          2024
EXTRACT(month)                         3
day of week, Mon=1..Sun=7 (ISODOW)     5
format as YYYY-MM (DATE_FORMAT)        2024-03
days between: B - A (DATEDIFF)         44
days between: A - B (sign flipped)     -44
add one month (DATE_ADD/INTERVAL)      2024-03-02
end of month (LAST_DAY/EOMONTH)        2024-03-31
elapsed whole months A to B            1
month boundaries crossed A to B        2

recursive-CTE series: ['2024-01-31', '2024-02-01', '2024-02-02', '2024-02-03']

pandas equals SQLite on every comparable row: OK

SQLite date('2024-01-31','+1 month') = 2024-03-02
SQLite date('2023-01-31','+1 month') = 2023-03-03
pandas Timestamp('2024-01-31') + DateOffset(months=1) = 2024-02-29
pandas Timestamp('2023-01-31') + DateOffset(months=1) = 2023-02-28
SQLite 3.45.1 'end of month' modifier: None (NULL = not supported here)
SQLite 3.45.1 strftime('%V'): None (NULL = not supported here)

dt.floor('MS') -> ValueError: <MonthBegin> is a non-fixed frequency
to_period('Q-MAR'): 2024Q4 | qyear: 2024 | quarter: 4
np.busday_count('2024-01-01','2024-01-15') = 10 (end excluded, Mon-Fri)
np.busday_count with holidays=['2024-01-02'] = 9
bdate_range freq='C' with holiday: ['2024-01-01', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-08', '2024-01-09', '2024-01-10', '2024-01-11', '2024-01-12']
```

**Edge cases:**
- Month arithmetic: SQLite's `+1 month` overflows (`2023-01-31` gives `2023-03-03`), pandas clips to month end, and the engines above are said to clip as well (not executed). The result of "add a month" on day 29 to 31 is engine dependent.
- `strftime('%V')`, `%G`, `%U` return NULL on SQLite 3.45.1 (shown in the output), and the `end of month`, `floor` and negative `weekday` modifiers also return NULL here; they exist only in newer SQLite versions according to its documentation, so use `start of month` arithmetic and the `weekday 1` trick shown above.
- Timestamps versus dates: `julianday` differences are fractional days; cast or `ROUND` before comparing.
- NULL dates give NULL results everywhere; `DATEDIFF` of a NULL is NULL.
- In pandas, `dt.floor('MS')` fails (non-fixed frequency); use `dt.to_period('M').dt.start_time`.
- Fiscal quarters: `to_period('Q-MAR')` puts 2024-03-15 in fiscal quarter `2024Q4` with `qyear` 2024; fiscal year labelling and where the quarter number restarts is a policy choice to confirm.

**Then explain:**
- Truncate and extract: `DATE_TRUNC` is `date(x, 'start of month')` or `strftime`; `EXTRACT` is `CAST(strftime(...) AS INTEGER)`.
- Differences: SQLite has no `DATEDIFF`; days are a `julianday` subtraction. Months need a rule: boundaries crossed (SQL Server / Snowflake style) or whole months elapsed (MySQL `TIMESTAMPDIFF` style). They disagree (2 versus 1 here), so name the one you mean.
- Series: a recursive CTE is the portable spine; `generate_series` and `GENERATE_DATE_ARRAY` are shortcuts in other engines.
- Every dialect fact outside SQLite on this page comes from memory and is not executed.

**Follow-ups:**
- Why did your DATEDIFF give a negative number? The argument order is engine specific: MySQL and BigQuery take the later date first, SQL Server and Snowflake take the unit and then the earlier date first, PostgreSQL subtracts dates with `-`.
- How do you do business days? In pandas `np.busday_count('2024-01-01', '2024-01-15')` is 10 (Monday to Friday, end excluded) and 9 with `holidays=['2024-01-02']`; `pd.bdate_range(..., freq='C', holidays=[...])` skips the holiday (both ran).
- Does SQLite support the ISO week? Not via `%V` in 3.45.1; see Q43.

**Common mistakes:**
- Assuming `DATEDIFF(a, b)` means the same in every engine.
- Using `DATEDIFF(month, ...)` boundary counting as "months of tenure".
- Writing `date + 30 days` for "next month".
- Assuming SQLite honours functions from the newer docs (`%V`, `end of month`) on an older build.

### Q37 ⭐ 🟡 Unix timestamps, milliseconds and subseconds: events(event_id, event_ms) stores epoch milliseconds from an app. Show datetime(event_ms / 1000, 'unixepoch') versus the bug of passing milliseconds as seconds (year about 56000, NULL or nonsense), unixepoch(), the 'auto' modifier and its first-63-days-of-1970 caveat, the subsec modifier and %f, and timediff() (text result, calendar-style). pandas: pd.to_datetime(unit='ms'), the pandas 3 default time unit (us for strings), and float precision loss.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Divide epoch milliseconds by 1000 before the `'unixepoch'` modifier (use `/ 1000.0` with `'subsec'` to keep the milliseconds), because passing milliseconds as seconds means a year near 55,800, which SQLite 3.45.1 returns as NULL for current dates, and a nonsense but valid date for small values.

**Schema and sample data:** four events. Event 1 is 2023-11-14 22:13:20.123 UTC, events 2 and 3 straddle 2024-01-01 by 999 ms, event 4 is 10 days after the epoch. Convention: epoch values are UTC, no time-zone conversion, no weeks.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_ms INTEGER);
INSERT INTO events VALUES (1, 1700000000123), (2, 1704067200000), (3, 1704067200999), (4, 864000000);
```

**SQL answer:** integer division gives whole seconds, `/ 1000.0` plus `'subsec'` keeps milliseconds, and the last column is the bug (`SQL_MAIN`).
```sql
SELECT event_id,
       datetime(event_ms / 1000, 'unixepoch')               AS ts_seconds,
       datetime(event_ms / 1000.0, 'unixepoch', 'subsec')    AS ts_millis,
       datetime(event_ms, 'unixepoch')                       AS bug_ms_as_seconds
FROM events ORDER BY event_id
```
The other functions are probed one line each in the Code block (`unixepoch()`, `strftime('%s')`, `%f`, the `'auto'` modifier, `subsec`, `timediff`).

**pandas answer:** `pd.to_datetime(..., unit="ms")`, then format.
```py
ev = pd.read_sql_query("SELECT * FROM events ORDER BY event_id", con)
ts = pd.to_datetime(ev["event_ms"], unit="ms")
pd_df = pd.DataFrame({
    "event_id": ev["event_id"],
    "ts_seconds": ts.dt.strftime("%Y-%m-%d %H:%M:%S"),
    "ts_millis": ts.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3],
})
```

**Example:**
- Event 1: 1700000000123 / 1000 = 1700000000 s, which is 2023-11-14 22:13:20; the remaining 123 ms survive only with `subsec`, giving `...22:13:20.123`.
- Event 3: 1704067200999 is 2024-01-01 00:00:00.999; integer seconds show `00:00:00`, the same as event 2, which is why dropping the milliseconds can merge distinct moments.
- Bug: `datetime(1700000000123, 'unixepoch')` treats the number as seconds, about 1.7e12 s, roughly year 55,840; SQLite returns NULL for events 1 to 3. Event 4 (864000000 ms) read as seconds gives 1997-05-19: valid-looking and wrong, the dangerous case.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q37: epoch milliseconds, unixepoch(), 'auto', subsec, timediff; pandas unit='ms'
# Convention: epoch values are UTC; no time-zone conversion anywhere in this block.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_ms INTEGER);
INSERT INTO events VALUES (1, 1700000000123), (2, 1704067200000), (3, 1704067200999), (4, 864000000);
"""
SQL_MAIN = """
SELECT event_id,
       datetime(event_ms / 1000, 'unixepoch')               AS ts_seconds,
       datetime(event_ms / 1000.0, 'unixepoch', 'subsec')    AS ts_millis,
       datetime(event_ms, 'unixepoch')                       AS bug_ms_as_seconds
FROM events ORDER BY event_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

# --- pandas ---
ev = pd.read_sql_query("SELECT * FROM events ORDER BY event_id", con)
ts = pd.to_datetime(ev["event_ms"], unit="ms")
pd_df = pd.DataFrame({
    "event_id": ev["event_id"],
    "ts_seconds": ts.dt.strftime("%Y-%m-%d %H:%M:%S"),
    "ts_millis": ts.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3],
})
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df[["event_id", "ts_seconds", "ts_millis"]].sort_values("event_id").reset_index(drop=True),
                              pd_df.sort_values("event_id").reset_index(drop=True), check_dtype=False)
print("\npandas equals SQL (event_id, ts_seconds, ts_millis): OK; dtype of pd.to_datetime(unit='ms'):", ts.dtype)

# the arithmetic behind the bug: 1.7e12 seconds is about this many years after 1970
print("\nmilliseconds read as seconds = year about", round(1700000000123 / 31556952 + 1970))
for label, sql in [
    ("unixepoch(ts text)", "SELECT unixepoch('2024-01-01 00:00:00')"),
    ("unixepoch with subsec", "SELECT unixepoch('2024-01-01 00:00:00.500', 'subsec')"),
    ("unixepoch, no subsec (integer)", "SELECT unixepoch('2024-01-01 00:00:00.500')"),
    ("strftime('%s')", "SELECT strftime('%s', '2024-01-01 00:00:00')"),
    ("strftime('%f') SS.SSS", "SELECT strftime('%f', 1700000000.123, 'unixepoch')"),
    ("auto, a real unix time 1704067200", "SELECT datetime(1704067200, 'auto')"),
    ("auto, 864000 s (day 10 of 1970)", "SELECT datetime(864000, 'auto')"),
    ("unixepoch, 864000 s", "SELECT datetime(864000, 'unixepoch')"),
    ("auto, 8640000 s (day 100 of 1970)", "SELECT datetime(8640000, 'auto')"),
    ("auto, ms value 1704067200000", "SELECT datetime(1704067200000, 'auto')"),
    ("timediff later, earlier", "SELECT timediff('2024-03-01 12:00:00', '2024-01-31 00:00:00')"),
    ("timediff earlier, later", "SELECT timediff('2024-01-31 00:00:00', '2024-03-01 12:00:00')"),
    ("julianday diff in days", "SELECT julianday('2024-03-01 12:00:00') - julianday('2024-01-31 00:00:00')"),
]:
    print(f"{label:36s}", con.execute(sql).fetchone()[0])

# ms resolution through subsec vs float arithmetic
f = con.execute("SELECT event_ms / 1000.0 FROM events WHERE event_id = 3").fetchone()[0]
print("\n1704067200999 / 1000.0 =", repr(f), "| back to ms:", f * 1000)

# pandas: units and precision
print("\nto_datetime(strings) dtype:", pd.to_datetime(["2024-01-01 00:00:00.123456"]).dtype)
print("to_datetime(string with 9 fractional digits) dtype:", pd.to_datetime(["2024-01-01 00:00:00.123456789"]).dtype)
print("Timestamp('2024-01-01').unit:", pd.Timestamp("2024-01-01").unit)
print("to_datetime(ms int):", pd.to_datetime(1700000000123, unit="ms"), "| dtype:", pd.to_datetime([1700000000123], unit="ms").dtype)
try:
    print(pd.to_datetime(1700000000123, unit="s"))
except Exception as e:
    print("ms read as seconds in pandas ->", type(e).__name__ + ":", str(e)[:70])
ns = 1700000000123456789
print("ns as int:", pd.to_datetime(ns, unit="ns"), "| through float64:", pd.to_datetime(float(ns), unit="ns"))
print("float seconds 1700000000.123456:", pd.to_datetime(1700000000.123456, unit="s"))
print("int(float(ns)) =", int(float(ns)), "vs", ns)
```

**Output (my run):**
```text
 event_id          ts_seconds               ts_millis   bug_ms_as_seconds
        1 2023-11-14 22:13:20 2023-11-14 22:13:20.123                 NaN
        2 2024-01-01 00:00:00 2024-01-01 00:00:00.000                 NaN
        3 2024-01-01 00:00:00 2024-01-01 00:00:00.999                 NaN
        4 1970-01-11 00:00:00 1970-01-11 00:00:00.000 1997-05-19 00:00:00

pandas equals SQL (event_id, ts_seconds, ts_millis): OK; dtype of pd.to_datetime(unit='ms'): datetime64[ms]

milliseconds read as seconds = year about 55841
unixepoch(ts text)                   1704067200
unixepoch with subsec                1704067200.5
unixepoch, no subsec (integer)       1704067200
strftime('%s')                       1704067200
strftime('%f') SS.SSS                20.123
auto, a real unix time 1704067200    2024-01-01 00:00:00
auto, 864000 s (day 10 of 1970)      -2347-06-13 12:00:00
unixepoch, 864000 s                  1970-01-11 00:00:00
auto, 8640000 s (day 100 of 1970)    1970-04-11 00:00:00
auto, ms value 1704067200000         None
timediff later, earlier              +0000-00-30 12:00:00.000
timediff earlier, later              -0000-01-01 12:00:00.000
julianday diff in days               30.5

1704067200999 / 1000.0 = 1704067200.999 | back to ms: 1704067200999.0

to_datetime(strings) dtype: datetime64[us]
to_datetime(string with 9 fractional digits) dtype: datetime64[ns]
Timestamp('2024-01-01').unit: us
to_datetime(ms int): 2023-11-14 22:13:20.123000 | dtype: datetime64[ms]
55840-11-08 22:15:23
ns as int: 2023-11-14 22:13:20.123456789 | through float64: 2023-11-14 22:13:20.123456768
float seconds 1700000000.123456: 2023-11-14 22:13:20.123456001
int(float(ns)) = 1700000000123456768 vs 1700000000123456789
```

**Edge cases:**
- `'auto'` (a newer modifier, available in this 3.45.1): numbers are read as Julian day numbers if they are in the range roughly 0 to 5,373,484.5, otherwise as unix seconds. That range is about the first 63 days of 1970, so `datetime(864000, 'auto')` gives `-2347-06-13` (a Julian day) while `'unixepoch'` gives 1970-01-11. A millisecond value is out of range and returns NULL.
- `unixepoch('2024-01-01 00:00:00.500', 'subsec')` returns the float `1704067200.5`; without `subsec` the result is an integer.
- `strftime('%f', ...)` returns seconds with milliseconds (`SS.SSS`, `20.123` here), not just the fraction.
- `timediff(a, b)` is text, calendar-style (years, months, days, then time): `'+0000-00-30 12:00:00.000'` for 2024-03-01 12:00 minus 2024-01-31. Swapping the arguments did not give the mirror image: `'-0000-01-01 12:00:00.000'`. Do not parse it for logic; use `julianday` differences (30.5 days here) or integer second differences.
- ms through a float: `1704067200999 / 1000.0` is `1704067200.999` and multiplies back to `1704067200999.0`, so milliseconds are safe in a float64; nanosecond epochs (about 1.7e18) are not, see below.
- NULL `event_ms` stays NULL in every function; in pandas an integer column with NULLs becomes float64.

**Then explain:**
- Unix time is seconds since 1970-01-01 UTC; apps often send milliseconds, so check the magnitude: 10 digits is seconds, 13 is milliseconds, 16 microseconds, 19 nanoseconds.
- SQLite stores no time type; `'unixepoch'` tells `datetime()` the number means seconds.
- pandas 3: `pd.to_datetime(strings)` gives `datetime64[us]` by default (the output shows it; a string with nine fractional digits gives `ns`), `Timestamp('2024-01-01').unit` is `us`, and integers with `unit="ms"` give `datetime64[ms]`. The same milliseconds read with `unit="s"` produce `55840-11-08 22:15:23` in pandas 3 instead of raising an error (I did not run pandas 2 here).
- Precision: `float(1700000000123456789)` is `1700000000123456768`, so a nanosecond epoch that passed through a float is wrong in the last digits; float seconds `1700000000.123456` shows `...123456001`. Keep epochs as integers.

**Follow-ups:**
- How do you get milliseconds as text? `strftime('%Y-%m-%d %H:%M:%f', event_ms / 1000.0, 'unixepoch')`; `%f` gives `SS.SSS`.
- How do you bucket by hour? `event_ms / 3600000` with integer division gives an hour number without any date function (UTC).
- How do you know whether a column is ms or s? Look at `MIN` and `MAX` magnitudes; do not guess.

**Common mistakes:**
- Passing milliseconds as seconds.
- Dividing by 1000 as an integer and losing the milliseconds, or by 1000.0 and then comparing floats for equality.
- Trusting `'auto'` near 1970.
- Parsing the `timediff` text, or assuming it is symmetric.

### Q38 ⭐ 🟡 Day boundaries and DST in aggregation: hourly metrics for a US/Eastern day with 23 hours (2024-03-10) and 25 hours (2024-11-03). Show with pandas resample('D') on a tz-aware index that the day has 23 or 25 hourly buckets, why daily averages per hour differ, and that UTC date grouping avoids the issue but misaligns with the business day. SQLite cannot do named zones, so show the UTC-offset-by-date emulation (a small offsets table) as the workaround and label real DST rules in other engines as not executed.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Store UTC, convert to the business zone before bucketing, and divide by the real number of hours in the local day: on 2024-03-10 US/Eastern has 23 hourly buckets and on 2024-11-03 it has 25, so `total / 24` is wrong on both; pandas does it with `tz_convert` plus `resample('D')`, SQLite needs a small UTC-offset table because it has no named zones.

**Schema and sample data:** one reading per UTC hour with value 10, covering three local days around each switch (the rows are generated in the Code block; hand-checkable because every hour is worth 10). The offsets table hard-codes the 2024 US rules: Eastern Standard Time is UTC-5 (-300 minutes), Eastern Daylight Time is UTC-4 (-240 minutes), DST starts 2024-03-10 at 02:00 EST (07:00 UTC) and ends 2024-11-03 at 02:00 EDT (06:00 UTC). Convention: business day = US/Eastern calendar day, stored times are UTC, no week logic.
```sql
CREATE TABLE metrics(ts_utc TEXT PRIMARY KEY, value INTEGER);
CREATE TABLE tz_offsets(valid_from_utc TEXT PRIMARY KEY, utc_offset_min INTEGER);
INSERT INTO tz_offsets VALUES
  ('2024-01-01 00:00:00', -300),
  ('2024-03-10 07:00:00', -240),
  ('2024-11-03 06:00:00', -300);
```

**SQL answer:** for each reading pick the offset row with the latest `valid_from_utc` not after the reading, shift the instant by that many minutes, and take the date (`SQL_MAIN`). `SQL_UTC` shows the UTC-date alternative.
```sql
SELECT date(m.ts_utc, printf('%+d minutes', o.utc_offset_min)) AS local_day,
       COUNT(*)                     AS hours,
       SUM(m.value)                 AS total,
       ROUND(1.0 * SUM(m.value) / 24, 2)    AS naive_avg_div_24,
       ROUND(1.0 * SUM(m.value) / COUNT(*), 2) AS true_avg_per_hour
FROM metrics m
JOIN tz_offsets o
  ON o.valid_from_utc = (SELECT MAX(valid_from_utc) FROM tz_offsets WHERE valid_from_utc <= m.ts_utc)
GROUP BY local_day
ORDER BY local_day
```
```sql
SELECT date(ts_utc) AS utc_day, COUNT(*) AS hours, SUM(value) AS total
FROM metrics WHERE ts_utc >= '2024-03-10' AND ts_utc < '2024-03-11' GROUP BY utc_day
```

**pandas answer:** localize to UTC, convert to `America/New_York`, resample by day on the tz-aware index.
```py
m = pd.read_sql_query("SELECT * FROM metrics", con, parse_dates=["ts_utc"])
local = m.assign(ts=m["ts_utc"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")).set_index("ts")
daily = local["value"].resample("D").agg(["count", "sum"])
daily = daily[daily["count"] > 0].reset_index()
pd_df = pd.DataFrame({
    "local_day": daily["ts"].dt.strftime("%Y-%m-%d"),
    "hours": daily["count"],
    "total": daily["sum"],
})
pd_df["naive_avg_div_24"] = (pd_df["total"] / 24).round(2)
pd_df["true_avg_per_hour"] = (pd_df["total"] / pd_df["hours"]).round(2)
```

**Example:**
- 2024-03-10 local day: midnight EST is 05:00 UTC, midnight EDT on 03-11 is 04:00 UTC, so the day holds 23 hourly rows; total 23 x 10 = 230. Dividing by 24 gives 9.58; dividing by the 23 real hours gives 10.0.
- 2024-11-03: midnight EDT is 04:00 UTC and midnight EST on 11-04 is 05:00 UTC, 25 rows, total 250; `/24` gives 10.42, the real average is 10.0.
- The UTC date 2024-03-10 always has 24 rows (240), but it runs from 19:00 EST on Mar 9 to 19:59 EDT on Mar 10: it avoids 23/25-hour days and answers a different question.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q38: DST day boundaries. Business day = US/Eastern calendar day; stored timestamps are UTC.
# Offsets table below hard-codes the 2024 US rules (EST -300 min, EDT -240 min); SQLite has no named zones.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE metrics(ts_utc TEXT PRIMARY KEY, value INTEGER);
CREATE TABLE tz_offsets(valid_from_utc TEXT PRIMARY KEY, utc_offset_min INTEGER);
INSERT INTO tz_offsets VALUES
  ('2024-01-01 00:00:00', -300),   -- EST
  ('2024-03-10 07:00:00', -240),   -- DST starts: 02:00 EST = 07:00 UTC
  ('2024-11-03 06:00:00', -300);   -- DST ends:   02:00 EDT = 06:00 UTC
""")
# one reading per UTC hour with value 10; three local days around each switch
spring = pd.date_range("2024-03-09 05:00", "2024-03-12 03:00", freq="h")   # local midnight Mar 9 to end of Mar 11
fall = pd.date_range("2024-11-02 04:00", "2024-11-05 04:00", freq="h")     # local midnight Nov 2 to end of Nov 4
rows = [(t.strftime("%Y-%m-%d %H:%M:%S"), 10) for t in spring.append(fall)]
con.executemany("INSERT INTO metrics VALUES (?, ?)", rows)

SQL_MAIN = """
SELECT date(m.ts_utc, printf('%+d minutes', o.utc_offset_min)) AS local_day,
       COUNT(*)                     AS hours,
       SUM(m.value)                 AS total,
       ROUND(1.0 * SUM(m.value) / 24, 2)    AS naive_avg_div_24,
       ROUND(1.0 * SUM(m.value) / COUNT(*), 2) AS true_avg_per_hour
FROM metrics m
JOIN tz_offsets o
  ON o.valid_from_utc = (SELECT MAX(valid_from_utc) FROM tz_offsets WHERE valid_from_utc <= m.ts_utc)
GROUP BY local_day
ORDER BY local_day
"""
SQL_UTC = """
SELECT date(ts_utc) AS utc_day, COUNT(*) AS hours, SUM(value) AS total
FROM metrics WHERE ts_utc >= '2024-03-10' AND ts_utc < '2024-03-11' GROUP BY utc_day
"""
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

# --- pandas ---
m = pd.read_sql_query("SELECT * FROM metrics", con, parse_dates=["ts_utc"])
local = m.assign(ts=m["ts_utc"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")).set_index("ts")
daily = local["value"].resample("D").agg(["count", "sum"])
daily = daily[daily["count"] > 0].reset_index()
pd_df = pd.DataFrame({
    "local_day": daily["ts"].dt.strftime("%Y-%m-%d"),
    "hours": daily["count"],
    "total": daily["sum"],
})
pd_df["naive_avg_div_24"] = (pd_df["total"] / 24).round(2)
pd_df["true_avg_per_hour"] = (pd_df["total"] / pd_df["hours"]).round(2)
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values("local_day").reset_index(drop=True),
                              pd_df.sort_values("local_day").reset_index(drop=True), check_dtype=False)
print("\npandas resample('D') on a tz-aware index equals the offsets-table SQL: OK")
print("\nbucket labels with their UTC offsets (pandas):")
print([str(t) for t in daily["ts"].iloc[[1, 2, 4, 5]]])

print("\nUTC date grouping for 2024-03-10 (always 24 hours, but not the business day):")
print(pd.read_sql_query(SQL_UTC, con).to_string(index=False))
print("business day 2024-03-10 starts at 05:00 UTC and ends 03:59 UTC on 03-11; the UTC date 03-10 is 19:00 EST Mar 9 .. 19:59 EDT Mar 10")

# tz_localize on wall-clock times that do not exist or repeat
for label, s in [("2024-03-10 02:30 (skipped)", "2024-03-10 02:30"), ("2024-11-03 01:30 (repeated)", "2024-11-03 01:30")]:
    try:
        pd.Timestamp(s).tz_localize("America/New_York")
    except Exception as e:
        print(f"\ntz_localize {label} ->", type(e).__name__ + ":", e)
print("ambiguous='NaT' ->", pd.Timestamp("2024-11-03 01:30").tz_localize("America/New_York", ambiguous="NaT"))
print("ambiguous=True (first, DST) ->", pd.Timestamp("2024-11-03 01:30").tz_localize("America/New_York", ambiguous=True))
print("nonexistent='shift_forward' ->", pd.Timestamp("2024-03-10 02:30").tz_localize("America/New_York", nonexistent="shift_forward"))

# the resample day: Mar 10 has 23 hourly rows even though the index step is one hour
h = pd.Series(1, index=pd.date_range("2024-03-10", periods=48, freq="h", tz="America/New_York"))
print("\nrange of 48 hourly steps from local midnight 2024-03-10: counts per local day ->", h.resample("D").count().tolist())
```

**Output (my run):**
```text
 local_day  hours  total  naive_avg_div_24  true_avg_per_hour
2024-03-09     24    240             10.00               10.0
2024-03-10     23    230              9.58               10.0
2024-03-11     24    240             10.00               10.0
2024-11-02     24    240             10.00               10.0
2024-11-03     25    250             10.42               10.0
2024-11-04     24    240             10.00               10.0

pandas resample('D') on a tz-aware index equals the offsets-table SQL: OK

bucket labels with their UTC offsets (pandas):
['2024-03-10 00:00:00-05:00', '2024-03-11 00:00:00-04:00', '2024-11-03 00:00:00-04:00', '2024-11-04 00:00:00-05:00']

UTC date grouping for 2024-03-10 (always 24 hours, but not the business day):
   utc_day  hours  total
2024-03-10     24    240
business day 2024-03-10 starts at 05:00 UTC and ends 03:59 UTC on 03-11; the UTC date 03-10 is 19:00 EST Mar 9 .. 19:59 EDT Mar 10

tz_localize 2024-03-10 02:30 (skipped) -> ValueError: 2024-03-10 02:30:00 is a nonexistent time due to daylight savings time. Try using the 'nonexistent' argument.

tz_localize 2024-11-03 01:30 (repeated) -> ValueError: Cannot infer dst time from 2024-11-03 01:30:00, try using the 'ambiguous' argument
ambiguous='NaT' -> NaT
ambiguous=True (first, DST) -> 2024-11-03 01:30:00-04:00
nonexistent='shift_forward' -> 2024-03-10 03:00:00-04:00

range of 48 hourly steps from local midnight 2024-03-10: counts per local day -> [23, 24, 1]
```

**Edge cases:**
- Missing hours: compare the bucket's count with the expected 23, 24 or 25; a day with 24 rows on a spring-forward date means duplicates, with 23 rows on an ordinary day means a gap.
- pandas `resample('D')` on a tz-aware index makes empty days between the two datasets (counts of 0); the code keeps days with at least one row. Bucket labels change offset (`-05:00` then `-04:00`), as printed.
- Converting wall-clock times: `tz_localize` on a skipped time (2024-03-10 02:30) and on a repeated time (2024-11-03 01:30) both raised `ValueError` in this run, with messages that name the `nonexistent` and `ambiguous` arguments. `ambiguous='NaT'` returns `NaT`, `ambiguous=True` picks the first (DST) occurrence, `nonexistent='shift_forward'` gives 03:00-04:00. Storing UTC avoids the question.
- The offsets table only knows the rules you put in; a different year needs more rows, and other zones need their own table. The SQLite `'localtime'` modifier uses the host zone, so it is not used here.
- Other engines (not executed here): PostgreSQL `ts AT TIME ZONE 'America/New_York'`, MySQL `CONVERT_TZ(ts, 'UTC', 'America/New_York')` (needs the time-zone tables loaded), BigQuery `DATE(ts, 'America/New_York')`, Snowflake `CONVERT_TIMEZONE`, SQL Server `AT TIME ZONE`; all from memory and they apply the real rules.

**Then explain:**
- A "day" is a local-calendar concept; its length is 24 hours except at DST switches.
- Rates (per hour) need the actual hour count; totals are not affected, but "average per hour" and "hourly share of the day" are.
- UTC grouping is simple and stable but misaligns with the business day, so a daily revenue report shifts by hours.
- Shifting by a fixed offset (always -5 hours) is the common bug: it is right only for half the year.

**Follow-ups:**
- Why not use `localtime` in SQLite? It depends on the machine's time zone, so results change between hosts.
- What about half-hour zones? The offset is in minutes (`+330`), so India works the same way.
- How would you build the offsets table at scale? Generate it from the tz database, one row per transition, and join with a range (Q39).

**Common mistakes:**
- Dividing by 24 on every day.
- Converting with a fixed offset.
- Localizing naive local timestamps without handling the ambiguous hour.
- Grouping by UTC date and presenting it as the business day.

### Q39 ⭐ 🟡 Range joins on dates: promotions(promo_id, start_date, end_date) and orders(order_id, order_ts, amount). Attribute each order to the promotion running on its date with a BETWEEN-style join, show the timestamp trap on an inclusive end_date (an order at 14:00 on the end date), overlapping promotions fanning out rows (double counted revenue) and how to detect it, and the pandas options (merge_asof when ranges do not overlap, IntervalIndex, or a cross merge and filter).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join on `order_ts >= start_date AND order_ts < date(end_date, '+1 day')` instead of BETWEEN, because an order at 14:00 on the end date compares greater than the bare end date string; and count promotion matches per order, since overlapping promotions fan one order out into several rows and double count its revenue.

**Schema and sample data:** three promotions, P1 and P2 overlap on 2024-03-05 to 03-07, end dates are inclusive and are plain dates; six orders with timestamps (order 2 is at 14:00 on P1's end date and also inside P2, order 3 is at 14:00 on P2's end date, order 6 sits in the overlap). Convention: one time zone, no conversion, no week logic.
```sql
CREATE TABLE promotions(promo_id TEXT PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO promotions VALUES ('P1','2024-03-01','2024-03-07'),('P2','2024-03-05','2024-03-10'),('P3','2024-03-15','2024-03-20');
INSERT INTO orders VALUES (1,'2024-03-02 10:00:00',100),(2,'2024-03-07 14:00:00',50),(3,'2024-03-10 14:00:00',70),
  (4,'2024-03-12 09:00:00',30),(5,'2024-03-16 12:00:00',40),(6,'2024-03-06 10:00:00',20);
```

**SQL answer:** four queries in the Code block. `SQL_NAIVE` is the BETWEEN trap, `SQL_FANOUT` is the correct window but shows the duplicate matches, `SQL_DETECT` finds orders matching more than one promotion, and `SQL_MAIN` assigns one promotion per order with the rule "the most recently started promotion wins" (a business rule to confirm).
```sql
SELECT o.order_id, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts BETWEEN p.start_date AND p.end_date
ORDER BY o.order_id, p.promo_id
```
```sql
SELECT o.order_id, o.amount, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
ORDER BY o.order_id, p.promo_id
```
```sql
SELECT o.order_id, COUNT(*) AS matches
FROM orders o JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
GROUP BY o.order_id HAVING COUNT(*) > 1 ORDER BY o.order_id
```
```sql
SELECT o.order_id, o.amount, p.promo_id
FROM orders o
LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
 AND p.start_date = (SELECT MAX(p2.start_date) FROM promotions p2
                     WHERE o.order_ts >= p2.start_date AND o.order_ts < date(p2.end_date, '+1 day'))
ORDER BY o.order_id
```

**pandas answer:** a cross merge and filter shows every match; `merge_asof` gives one promotion per order using the same "latest start wins" rule as `SQL_MAIN` (then check the order is before the window end); an `IntervalIndex` works only when the intervals do not overlap.
```py
orders = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
promos = pd.read_sql_query("SELECT * FROM promotions", con, parse_dates=["start_date", "end_date"])
promos["end_excl"] = promos["end_date"] + pd.Timedelta(days=1)
# option A: cross merge and filter (shows every match, so fan-out is visible)
cross = orders.merge(promos, how="cross")
cross = cross[(cross["order_ts"] >= cross["start_date"]) & (cross["order_ts"] < cross["end_excl"])]
# option B: merge_asof = latest start <= order_ts, then check the window end (same rule as SQL_MAIN)
asof = pd.merge_asof(orders.sort_values("order_ts"), promos.sort_values("start_date"),
                     left_on="order_ts", right_on="start_date", direction="backward")
asof.loc[asof["order_ts"] >= asof["end_excl"], "promo_id"] = None
pd_df = asof[["order_id", "amount", "promo_id"]].sort_values("order_id").reset_index(drop=True)
```

**Example:**
- Order 3 (03-10 14:00, amount 70): `'2024-03-10 14:00:00' BETWEEN '2024-03-05' AND '2024-03-10'` is false because the text `2024-03-10 14:00:00` sorts after `2024-03-10`, so the naive query gives it no promotion. With `< date(end_date, '+1 day')` the bound is `2024-03-11` and it matches P2.
- Order 2 (03-07 14:00, 50): the same trap removes P1 (end `2024-03-07`), but it is inside P2 (03-05 to 03-10).
- Order 6 (03-06 10:00, 20) matches both P1 and P2. With the fan-out join the order appears twice; revenue becomes 310 + 50 + 20 = 380 (orders 2 and 6 each counted twice, as the output shows) against the true 310.
- With the latest start winning, orders 2, 3 and 6 go to P2; revenue by promotion: P1 100, P2 140, P3 40, none 30 (order 4, 03-12, has no promotion).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q39: range joins on dates (promotions with INCLUSIVE end_date; orders have timestamps)
# Convention: order_ts is a naive local-business-time text 'YYYY-MM-DD HH:MM:SS'; one time zone, no conversion.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE promotions(promo_id TEXT PRIMARY KEY, start_date TEXT, end_date TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO promotions VALUES ('P1','2024-03-01','2024-03-07'),('P2','2024-03-05','2024-03-10'),('P3','2024-03-15','2024-03-20');
INSERT INTO orders VALUES (1,'2024-03-02 10:00:00',100),(2,'2024-03-07 14:00:00',50),(3,'2024-03-10 14:00:00',70),
  (4,'2024-03-12 09:00:00',30),(5,'2024-03-16 12:00:00',40),(6,'2024-03-06 10:00:00',20);
"""
# 1. the naive BETWEEN: end_date is a bare date, so '2024-03-10 14:00:00' > '2024-03-10' and the order falls out
SQL_NAIVE = """
SELECT o.order_id, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts BETWEEN p.start_date AND p.end_date
ORDER BY o.order_id, p.promo_id
"""
# 2. right window (half-open at the next midnight), but overlaps fan rows out
SQL_FANOUT = """
SELECT o.order_id, o.amount, p.promo_id
FROM orders o LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
ORDER BY o.order_id, p.promo_id
"""
# 3. detection: one order matching more than one promotion
SQL_DETECT = """
SELECT o.order_id, COUNT(*) AS matches
FROM orders o JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
GROUP BY o.order_id HAVING COUNT(*) > 1 ORDER BY o.order_id
"""
# 4. main: one promotion per order, rule = the most recently started promotion wins
SQL_MAIN = """
SELECT o.order_id, o.amount, p.promo_id
FROM orders o
LEFT JOIN promotions p
  ON o.order_ts >= p.start_date AND o.order_ts < date(p.end_date, '+1 day')
 AND p.start_date = (SELECT MAX(p2.start_date) FROM promotions p2
                     WHERE o.order_ts >= p2.start_date AND o.order_ts < date(p2.end_date, '+1 day'))
ORDER BY o.order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
naive = pd.read_sql_query(SQL_NAIVE, con)
fan = pd.read_sql_query(SQL_FANOUT, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("naive BETWEEN (order 3, 14:00 on P2's end date, loses its promo; order 2 loses P1; order 6 still matches twice):")
print(naive.to_string(index=False))
print("\ndetect fan-out:")
print(pd.read_sql_query(SQL_DETECT, con).to_string(index=False))
print("\nrevenue: orders total =", con.execute("SELECT SUM(amount) FROM orders").fetchone()[0],
      "| sum after fan-out join =", int(fan["amount"].sum()))
print("\nmain (latest start wins):")
print(sql_df.to_string(index=False))
print("\nrevenue by promo, main:")
print(sql_df.groupby(sql_df["promo_id"].fillna("none"))["amount"].sum().to_string())

# --- pandas ---
orders = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
promos = pd.read_sql_query("SELECT * FROM promotions", con, parse_dates=["start_date", "end_date"])
promos["end_excl"] = promos["end_date"] + pd.Timedelta(days=1)
# option A: cross merge and filter (shows every match, so fan-out is visible)
cross = orders.merge(promos, how="cross")
cross = cross[(cross["order_ts"] >= cross["start_date"]) & (cross["order_ts"] < cross["end_excl"])]
# option B: merge_asof = latest start <= order_ts, then check the window end (same rule as SQL_MAIN)
asof = pd.merge_asof(orders.sort_values("order_ts"), promos.sort_values("start_date"),
                     left_on="order_ts", right_on="start_date", direction="backward")
asof.loc[asof["order_ts"] >= asof["end_excl"], "promo_id"] = None
pd_df = asof[["order_id", "amount", "promo_id"]].sort_values("order_id").reset_index(drop=True)
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values("order_id").reset_index(drop=True), pd_df, check_dtype=False)
print("\npandas merge_asof equals SQL_MAIN: OK")
print("cross-merge matches per order:", cross.groupby("order_id").size().to_dict())

# option C: IntervalIndex (needs NON-overlapping intervals)
iv = pd.IntervalIndex.from_arrays(promos["start_date"], promos["end_excl"], closed="left")
print("IntervalIndex is_overlapping:", iv.is_overlapping)
try:
    iv.get_indexer(orders["order_ts"])
except Exception as e:
    print("get_indexer on overlapping ->", type(e).__name__ + ":", str(e)[:75])
ok = promos[promos["promo_id"].isin(["P2", "P3"])]
iv2 = pd.IntervalIndex.from_arrays(ok["start_date"], ok["end_excl"], closed="left")
pos = iv2.get_indexer(orders["order_ts"])
print("P2+P3 only, positions per order (-1 = none):", pos.tolist(), "| overlapping:", iv2.is_overlapping)
```

**Output (my run):**
```text
naive BETWEEN (order 3, 14:00 on P2's end date, loses its promo; order 2 loses P1; order 6 still matches twice):
 order_id promo_id
        1       P1
        2       P2
        3      NaN
        4      NaN
        5       P3
        6       P1
        6       P2

detect fan-out:
 order_id  matches
        2        2
        6        2

revenue: orders total = 310 | sum after fan-out join = 380

main (latest start wins):
 order_id  amount promo_id
        1     100       P1
        2      50       P2
        3      70       P2
        4      30      NaN
        5      40       P3
        6      20       P2

revenue by promo, main:
promo_id
P1      100
P2      140
P3       40
none     30

pandas merge_asof equals SQL_MAIN: OK
cross-merge matches per order: {1: 1, 2: 2, 3: 1, 5: 1, 6: 2}
IntervalIndex is_overlapping: True
get_indexer on overlapping -> InvalidIndexError: cannot handle overlapping indices; use IntervalIndex.get_indexer_non_unique
P2+P3 only, positions per order (-1 = none): [-1, 0, 0, -1, 1, 0] | overlapping: False
```

**Edge cases:**
- Detect fan-out before trusting any total: `GROUP BY order_id HAVING COUNT(*) > 1`, and compare `SUM(amount)` after the join with `SUM(amount)` on the orders table (380 against 310 here).
- Choosing the winner is a business rule: latest start, highest discount, a priority column, or split the amount across promotions. If promotions can nest (a short promotion inside a long one) the "latest start" rule from `merge_asof` can miss a still-running earlier promotion once the later one has ended, so check the window end and, if needed, use the cross merge.
- `merge_asof` needs both sides sorted by the key and finds only one match; it does not detect overlaps.
- `IntervalIndex.get_indexer` raises `InvalidIndexError` on overlapping intervals (printed in the run); with only P2 and P3 it returns positions, `-1` for no match.
- Orders on the end date at midnight exactly are inside the window; an end_date of NULL (open promotion) needs `OR end_date IS NULL` and is not modelled here.
- Dates stored as text in a consistent `YYYY-MM-DD` format compare correctly as strings; mixed formats do not (Q45).

**Then explain:**
- BETWEEN is inclusive on both ends, which is right for dates and wrong for timestamps against a date end bound; convert to a half-open interval `[start, end + 1 day)`.
- A range join can multiply rows, unlike an equality join on a key; always check cardinality.
- In pandas, the cross merge is the transparent option (rows = orders x promotions, filter after), `merge_asof` is the efficient single-match option, `IntervalIndex` is the lookup option for non-overlapping ranges.
- The fix for revenue by promotion is to pick one promotion per order before aggregating, not after.

**Follow-ups:**
- What if one order should count toward every promotion it falls in? Then fan-out is the intent, but totals by promotion will no longer add up to total revenue; say so and report it separately.
- What if end_date is exclusive in the source? Compare with `< end_date` directly.
- How would you do it for 10 million orders? Sort-merge style (`merge_asof`) or a range-aware join, plus an index on start_date; plans are Part 11.

**Common mistakes:**
- BETWEEN with a timestamp and an inclusive date end.
- Summing revenue after a join that fans out.
- Using `merge_asof` on unsorted frames or overlapping ranges without checking.
- Forgetting the unmatched (no promotion) orders by using an inner join, which also silently drops revenue.

### Q40 ⭐ 🟡 Performance of date filters (SQLite runnable, other engines hedged): orders(order_id, order_ts, amount) with 1,000,000 rows conceptually. Compare WHERE strftime('%Y-%m', order_ts) = '2024-03' (function on the column, cannot use an index) with WHERE order_ts >= '2024-03-01' AND order_ts < '2024-04-01' (sargable), run EXPLAIN QUERY PLAN on both with an index on order_ts, and mention an expression index. Cross-reference Part 11 for plans; partitioning by month is a hedged concept.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** A function wrapped around the column (`strftime('%Y-%m', order_ts) = '2024-03'`) cannot use a plain index on `order_ts` and scans every row, while the range `order_ts >= '2024-03-01' AND order_ts < '2024-04-01'` is sargable and does an index search; an expression index on the function is the other fix.

**Schema and sample data:** `orders(order_id, order_ts, amount)` with `order_ts` as `YYYY-MM-DD HH:MM:SS` text; the Code block generates 200,000 rows one every 157 seconds from 2024-01-01 (a stand-in for the 1,000,000 conceptual rows; a row count of this size is enough to show the plan). A plain index `idx_orders_ts` is on `order_ts`. Convention: naive timestamps, one time zone, no weeks. The data are synthetic, not hand-checkable row by row, so the hand check is on the March range: 31 days x 86400 s / 157 s = 17,058.9, which matches the printed count of 17,059.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
CREATE INDEX idx_orders_ts ON orders(order_ts);
```

**SQL answer:** the function version, the sargable range (`SQL_MAIN`), and a BETWEEN with a bare last day for comparison.
```sql
SELECT COUNT(*), SUM(amount) FROM orders WHERE strftime('%Y-%m', order_ts) = '2024-03'
```
```sql
SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts >= '2024-03-01' AND order_ts < '2024-04-01'
```
```sql
SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts BETWEEN '2024-03-01' AND '2024-03-31'
```
The expression index (created in the Code block after the first plan is printed):
```sql
CREATE INDEX idx_orders_month ON orders(strftime('%Y-%m', order_ts));
```

**pandas answer:** the pandas equivalent of a range filter is a boolean mask, or a partial-string slice on a sorted `DatetimeIndex`; pandas has no index plan to inspect, both scan memory.
```py
df = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
mask = (df["order_ts"] >= "2024-03-01") & (df["order_ts"] < "2024-04-01")
pd_res = (int(mask.sum()), int(df.loc[mask, "amount"].sum()))
by_slice = df.set_index("order_ts").sort_index().loc["2024-03"]           # partial-string slice on a sorted DatetimeIndex
```

**Example:**
- Function on the column: the plan line is `SCAN orders`; SQLite must evaluate `strftime` for all 200,000 rows even though an index on `order_ts` exists.
- Range: `SEARCH orders USING INDEX idx_orders_ts (order_ts>? AND order_ts<?)`; it seeks to `2024-03-01` and stops at `2024-04-01`, touching about 17,059 index entries.
- The VM instruction counter (a rough count from `set_progress_handler`, in steps of 100) is about 851,200 for the scan against about 102,400 for the range, roughly 8 times; treat it as indicative, not a benchmark.
- After the expression index the function version is `SEARCH ... USING INDEX idx_orders_month (<expr>=?)` and costs about the same as the range. The expression must be written the same way: `strftime('%Y/%m', order_ts)` does not match the index and the plan falls back to a scan (printed, on a covering index scan).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q40: sargable date filters, EXPLAIN QUERY PLAN, expression index (SQLite 3.45.1 only; other engines hedged in prose)
# Convention: order_ts is naive text 'YYYY-MM-DD HH:MM:SS'; 200,000 synthetic rows stand in for 1,000,000.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER)")
base = pd.Timestamp("2024-01-01")
rows = [(i, (base + pd.Timedelta(seconds=157 * i)).strftime("%Y-%m-%d %H:%M:%S"), 1 + i % 50) for i in range(200_000)]
con.executemany("INSERT INTO orders VALUES (?,?,?)", rows)
con.execute("CREATE INDEX idx_orders_ts ON orders(order_ts)")
con.commit()

SQL_FUNC = "SELECT COUNT(*), SUM(amount) FROM orders WHERE strftime('%Y-%m', order_ts) = '2024-03'"
SQL_MAIN = "SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts >= '2024-03-01' AND order_ts < '2024-04-01'"
SQL_BAD_BETWEEN = "SELECT COUNT(*), SUM(amount) FROM orders WHERE order_ts BETWEEN '2024-03-01' AND '2024-03-31'"

def plan(sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

def vm_steps(sql):
    n = [0]
    def tick():
        n[0] += 1
        return 0
    con.set_progress_handler(tick, 100)       # callback every 100 VM instructions
    con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return n[0] * 100

r_func, r_main, r_bad = (con.execute(s).fetchone() for s in (SQL_FUNC, SQL_MAIN, SQL_BAD_BETWEEN))
print("rows, revenue  function-on-column:", r_func, "| range:", r_main, "| BETWEEN with last day as bare date:", r_bad)
assert r_func == r_main and r_bad != r_main

# --- pandas ---
df = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
mask = (df["order_ts"] >= "2024-03-01") & (df["order_ts"] < "2024-04-01")
pd_res = (int(mask.sum()), int(df.loc[mask, "amount"].sum()))
by_slice = df.set_index("order_ts").sort_index().loc["2024-03"]           # partial-string slice on a sorted DatetimeIndex
# --- end pandas ---
assert pd_res == tuple(r_main) and (len(by_slice), int(by_slice["amount"].sum())) == pd_res
print("pandas mask and .loc['2024-03'] equal SQL:", pd_res)

print("\nPLAN with plain index on order_ts")
print(" function on column :", plan(SQL_FUNC))
print(" range              :", plan(SQL_MAIN))
print("approx VM instructions  function:", vm_steps(SQL_FUNC), "| range:", vm_steps(SQL_MAIN))

con.execute("CREATE INDEX idx_orders_month ON orders(strftime('%Y-%m', order_ts))")
print("\nPLAN after expression index on strftime('%Y-%m', order_ts)")
print(" function on column :", plan(SQL_FUNC))
print(" range              :", plan(SQL_MAIN))
print("approx VM instructions  function:", vm_steps(SQL_FUNC), "| range:", vm_steps(SQL_MAIN))
try:
    print(" index on strftime with 'localtime' ->", con.execute("CREATE INDEX bad ON orders(strftime('%Y-%m', order_ts, 'localtime'))").fetchall())
except Exception as e:
    print(" index on strftime with 'localtime' ->", type(e).__name__ + ":", e)
print(" same filter written with a different format string:", plan("SELECT COUNT(*) FROM orders WHERE strftime('%Y/%m', order_ts) = '2024/03'"))
```

**Output (my run):**
```text
rows, revenue  function-on-column: (17059, 435000) | range: (17059, 435000) | BETWEEN with last day as bare date: (16509, 420975)
pandas mask and .loc['2024-03'] equal SQL: (17059, 435000)

PLAN with plain index on order_ts
 function on column : ['SCAN orders']
 range              : ['SEARCH orders USING INDEX idx_orders_ts (order_ts>? AND order_ts<?)']
approx VM instructions  function: 851200 | range: 102400

PLAN after expression index on strftime('%Y-%m', order_ts)
 function on column : ['SEARCH orders USING INDEX idx_orders_month (<expr>=?)']
 range              : ['SEARCH orders USING INDEX idx_orders_ts (order_ts>? AND order_ts<?)']
approx VM instructions  function: 102400 | range: 102400
 index on strftime with 'localtime' -> OperationalError: non-deterministic use of strftime() in an index
 same filter written with a different format string: ['SCAN orders USING COVERING INDEX idx_orders_ts']
```

**Edge cases:**
- BETWEEN `'2024-03-01' AND '2024-03-31'` is sargable but wrong for timestamps: it returned 16,509 rows against 17,059 (everything after midnight on 03-31 is lost); that is the same trap as Q39 and Q45.
- Index with a non-deterministic function is refused: `strftime(..., 'localtime')` raised `OperationalError: non-deterministic use of strftime() in an index`.
- If `order_ts` has mixed text formats the range comparison silently misorders; normalise on load.
- Planner behaviour depends on statistics, data volume and the SQLite version; on tiny tables a scan is also fine. Execution plans are covered in Part 11.
- Other engines (not executed here): the principle is the same in PostgreSQL, MySQL, BigQuery, Snowflake and SQL Server, wrapping the column in a function defeats a normal index unless there is a matching functional/expression index (PostgreSQL expression index, MySQL 8 functional index, SQL Server computed column). Partitioning by month (range partitions) lets the engine prune whole partitions when the filter is a range on the partition column; this is a concept here and I did not run it.

**Then explain:**
- Sargable means the predicate can be answered from the index order: a bare column compared with a constant range.
- Move the function to the constant side: compute `'2024-03-01'` and `'2024-04-01'` in the application or with `date()` on the constant, never on the column.
- Half-open ranges (`>= start AND < next_start`) also avoid the end-of-day trap.
- An expression index is the fallback when you cannot change the query, for example a BI tool that always emits `strftime`/`DATE_TRUNC`.

**Follow-ups:**
- How would you write "last 7 days" as of a fixed date? `order_ts >= date('2024-04-15', '-7 days') AND order_ts < '2024-04-16'`, with the as-of date passed as a parameter.
- Does an index on `(order_ts, amount)` help more? It can make the query covering (no table lookups); verify with the plan, not by assumption.
- Why can pandas filter by `.loc['2024-03']`? A sorted `DatetimeIndex` supports partial-string slicing; the slice includes the whole of March, end included.

**Common mistakes:**
- `WHERE DATE(order_ts) = ...` or `strftime` on the column.
- `BETWEEN` with a date end on a timestamp column.
- Creating an index and assuming every query uses it.
- Believing timings from a tiny table.

### Q41 ⭐ 🔴 Cohort retention by segment with a spine: users(user_id, signup_date, channel) and logins(user_id, login_date). Return one row per (channel, signup month, month offset 0 to 3) including offsets where nobody returned (0, not missing) by cross joining cohorts with an offset spine and LEFT JOINing activity. Explain why an INNER JOIN silently hides the zero cells that matter most and how to avoid mixing channels with different cohort sizes. pandas: reindex a MultiIndex pivot with fill_value=0.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build one row per (channel, signup month, offset 0 to 3) by cross joining the cohorts with an offset spine, then LEFT JOIN the activity counts and `COALESCE` to 0; an INNER JOIN to activity silently drops the zero cells, and a cohort with no returns at all disappears completely.

**Schema and sample data:** twelve users in five (channel, signup month) cohorts and 24 login rows. User 1 logs in twice in February (distinct counting needed), organic user 12 never logs in (the whole March organic cohort is zero). Convention: calendar months from the stored `YYYY-MM-DD` text, no time zone, no weeks; as-of date fixed at 2024-04-30; retained at offset k means at least one login in the calendar month k months after the signup month.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, channel TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2024-01-05','ads'),(2,'2024-01-20','ads'),(3,'2024-01-28','ads'),(4,'2024-01-31','ads'),
  (5,'2024-01-10','organic'),(6,'2024-01-15','organic'),(7,'2024-02-03','ads'),(8,'2024-02-14','ads'),(9,'2024-02-29','ads'),
  (10,'2024-02-02','organic'),(11,'2024-02-20','organic'),(12,'2024-03-10','organic');
INSERT INTO logins VALUES (1,'2024-01-05'),(1,'2024-02-10'),(1,'2024-02-25'),(1,'2024-03-02'),(2,'2024-01-20'),(2,'2024-02-02'),
  (3,'2024-01-28'),(4,'2024-01-31'),(4,'2024-02-01'),(5,'2024-01-10'),(5,'2024-02-11'),(5,'2024-03-12'),(5,'2024-04-01'),
  (6,'2024-01-15'),(6,'2024-02-20'),(7,'2024-02-03'),(7,'2024-03-05'),(8,'2024-02-14'),(9,'2024-02-29'),(9,'2024-03-01'),
  (10,'2024-02-02'),(10,'2024-03-03'),(10,'2024-04-04'),(11,'2024-02-20');
```

**SQL answer:** cohort sizes, an offset spine, distinct retained users per (channel, cohort, offset), then spine LEFT JOIN activity (`SQL_MAIN`). Cells whose calendar month is after the as-of date are not observed yet, so the percentage is NULL there rather than a false 0. `SQL_INNER` is the broken version.
```sql
WITH cohort AS (
  SELECT channel, strftime('%Y-%m', signup_date) AS cohort_month, COUNT(*) AS cohort_size
  FROM users GROUP BY channel, cohort_month
), offsets(month_offset) AS (VALUES (0), (1), (2), (3)),
act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id
  GROUP BY 1, 2, 3
)
SELECT c.channel, c.cohort_month, o.month_offset, c.cohort_size,
       COALESCE(a.retained_users, 0) AS retained_users,
       CASE WHEN date(c.cohort_month || '-01', '+' || o.month_offset || ' months') <= '2024-04-30'
            THEN ROUND(100.0 * COALESCE(a.retained_users, 0) / c.cohort_size, 1) END AS retention_pct
FROM cohort c CROSS JOIN offsets o
LEFT JOIN act a ON a.channel = c.channel AND a.cohort_month = c.cohort_month AND a.month_offset = o.month_offset
ORDER BY c.channel, c.cohort_month, o.month_offset
```
```sql
WITH act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id GROUP BY 1, 2, 3
)
SELECT * FROM act WHERE month_offset BETWEEN 0 AND 3 ORDER BY channel, cohort_month, month_offset
```

**pandas answer:** compute offsets with Period subtraction, `pivot_table` with `nunique`, then reindex the (channel, cohort) rows from the cohort sizes and the columns 0 to 3 with `fill_value=0`.
```py
users = pd.read_sql_query("SELECT * FROM users", con, parse_dates=["signup_date"])
logins = pd.read_sql_query("SELECT * FROM logins", con, parse_dates=["login_date"])
users["cohort_month"] = users["signup_date"].dt.to_period("M")
size = users.groupby(["channel", "cohort_month"])["user_id"].nunique().rename("cohort_size")
j = logins.merge(users, on="user_id")
j["month_offset"] = (j["login_date"].dt.to_period("M") - j["cohort_month"]).apply(lambda d: d.n)
j = j[j["month_offset"].between(0, 3)]
piv = j.pivot_table(index=["channel", "cohort_month"], columns="month_offset", values="user_id",
                    aggfunc="nunique", fill_value=0)
piv = piv.reindex(index=size.index, columns=[0, 1, 2, 3], fill_value=0)       # restores empty cells and empty cohorts
long = (piv.stack().rename("retained_users").reset_index()
          .merge(size.reset_index(), on=["channel", "cohort_month"]))
as_of_month = pd.Period("2024-04", "M")
long["observed"] = (long["cohort_month"] + long["month_offset"]) <= as_of_month
long["retention_pct"] = (100.0 * long["retained_users"] / long["cohort_size"]).round(1).where(long["observed"])
long["cohort_month"] = long["cohort_month"].astype(str)
pd_df = long[["channel", "cohort_month", "month_offset", "cohort_size", "retained_users", "retention_pct"]]
```

**Example:**
- Cohort ads / 2024-01 (users 1 to 4, size 4): month offset 0 (January) = everyone logged in on signup day, 4. Offset 1 (February): users 1, 2 and 4 logged in, user 3 did not, 3 of 4 = 75.0%. Offset 2 (March): only user 1, 1 of 4 = 25.0%. Offset 3 (April): nobody, 0 of 4 = 0.0%, a real zero that the spine keeps and an INNER JOIN removes.
- Cohort organic / 2024-03 (user 12, no logins): offsets 0 and 1 (March, April) are observed and are 0%; offsets 2 and 3 (May, June) are after the as-of date, so NULL.
- Spine version has 5 cohorts x 4 offsets = 20 rows; the INNER JOIN version has 12 rows (printed), and the organic 2024-03 cohort is not in it at all.
- Mixing channels: at offset 1, pooling all observed cells gives 8 retained of 12 users = 66.7%; the plain average of the five cell percentages is 58.3%. They differ because cohort sizes differ, so average counts, not percentages, and always keep channel in the grain.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q41: cohort retention by channel with a cohort x offset spine
# Convention: calendar months of the stored 'YYYY-MM-DD' text dates (no time zone); as-of date fixed at 2024-04-30.
# Retained at offset k = at least one login in the calendar month k months after the signup month.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, channel TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2024-01-05','ads'),(2,'2024-01-20','ads'),(3,'2024-01-28','ads'),(4,'2024-01-31','ads'),
  (5,'2024-01-10','organic'),(6,'2024-01-15','organic'),(7,'2024-02-03','ads'),(8,'2024-02-14','ads'),(9,'2024-02-29','ads'),
  (10,'2024-02-02','organic'),(11,'2024-02-20','organic'),(12,'2024-03-10','organic');
INSERT INTO logins VALUES (1,'2024-01-05'),(1,'2024-02-10'),(1,'2024-02-25'),(1,'2024-03-02'),(2,'2024-01-20'),(2,'2024-02-02'),
  (3,'2024-01-28'),(4,'2024-01-31'),(4,'2024-02-01'),(5,'2024-01-10'),(5,'2024-02-11'),(5,'2024-03-12'),(5,'2024-04-01'),
  (6,'2024-01-15'),(6,'2024-02-20'),(7,'2024-02-03'),(7,'2024-03-05'),(8,'2024-02-14'),(9,'2024-02-29'),(9,'2024-03-01'),
  (10,'2024-02-02'),(10,'2024-03-03'),(10,'2024-04-04'),(11,'2024-02-20');
"""
SQL_MAIN = """
WITH cohort AS (
  SELECT channel, strftime('%Y-%m', signup_date) AS cohort_month, COUNT(*) AS cohort_size
  FROM users GROUP BY channel, cohort_month
), offsets(month_offset) AS (VALUES (0), (1), (2), (3)),
act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id
  GROUP BY 1, 2, 3
)
SELECT c.channel, c.cohort_month, o.month_offset, c.cohort_size,
       COALESCE(a.retained_users, 0) AS retained_users,
       CASE WHEN date(c.cohort_month || '-01', '+' || o.month_offset || ' months') <= '2024-04-30'
            THEN ROUND(100.0 * COALESCE(a.retained_users, 0) / c.cohort_size, 1) END AS retention_pct
FROM cohort c CROSS JOIN offsets o
LEFT JOIN act a ON a.channel = c.channel AND a.cohort_month = c.cohort_month AND a.month_offset = o.month_offset
ORDER BY c.channel, c.cohort_month, o.month_offset
"""
# the same query with an INNER JOIN to activity and no spine
SQL_INNER = """
WITH act AS (
  SELECT u.channel, strftime('%Y-%m', u.signup_date) AS cohort_month,
         (CAST(strftime('%Y', l.login_date) AS INTEGER) * 12 + CAST(strftime('%m', l.login_date) AS INTEGER))
       - (CAST(strftime('%Y', u.signup_date) AS INTEGER) * 12 + CAST(strftime('%m', u.signup_date) AS INTEGER)) AS month_offset,
         COUNT(DISTINCT u.user_id) AS retained_users
  FROM users u JOIN logins l ON l.user_id = u.user_id GROUP BY 1, 2, 3
)
SELECT * FROM act WHERE month_offset BETWEEN 0 AND 3 ORDER BY channel, cohort_month, month_offset
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
inner = pd.read_sql_query(SQL_INNER, con)

# --- pandas ---
users = pd.read_sql_query("SELECT * FROM users", con, parse_dates=["signup_date"])
logins = pd.read_sql_query("SELECT * FROM logins", con, parse_dates=["login_date"])
users["cohort_month"] = users["signup_date"].dt.to_period("M")
size = users.groupby(["channel", "cohort_month"])["user_id"].nunique().rename("cohort_size")
j = logins.merge(users, on="user_id")
j["month_offset"] = (j["login_date"].dt.to_period("M") - j["cohort_month"]).apply(lambda d: d.n)
j = j[j["month_offset"].between(0, 3)]
piv = j.pivot_table(index=["channel", "cohort_month"], columns="month_offset", values="user_id",
                    aggfunc="nunique", fill_value=0)
piv = piv.reindex(index=size.index, columns=[0, 1, 2, 3], fill_value=0)       # restores empty cells and empty cohorts
long = (piv.stack().rename("retained_users").reset_index()
          .merge(size.reset_index(), on=["channel", "cohort_month"]))
as_of_month = pd.Period("2024-04", "M")
long["observed"] = (long["cohort_month"] + long["month_offset"]) <= as_of_month
long["retention_pct"] = (100.0 * long["retained_users"] / long["cohort_size"]).round(1).where(long["observed"])
long["cohort_month"] = long["cohort_month"].astype(str)
pd_df = long[["channel", "cohort_month", "month_offset", "cohort_size", "retained_users", "retention_pct"]]
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values(["channel", "cohort_month", "month_offset"]).reset_index(drop=True),
                              pd_df.sort_values(["channel", "cohort_month", "month_offset"]).reset_index(drop=True),
                              check_dtype=False)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nINNER JOIN version: rows =", len(inner), "(spine version has", len(sql_df), ")")
print(inner.to_string(index=False))
print("organic 2024-03 cohort present in the INNER JOIN version?", bool((inner["cohort_month"] == "2024-03").any()))

# mixing channels: pooled rate vs unweighted mean of channel rates, offset 1, observed cells only
o1 = sql_df[(sql_df["month_offset"] == 1) & sql_df["retention_pct"].notna()]
pooled = 100.0 * o1["retained_users"].sum() / o1["cohort_size"].sum()
print("\noffset 1, observed cells: pooled =", round(pooled, 1), "| mean of cell percentages =", round(o1["retention_pct"].mean(), 1))
```

**Output (my run):**
```text
channel cohort_month  month_offset  cohort_size  retained_users  retention_pct
    ads      2024-01             0            4               4          100.0
    ads      2024-01             1            4               3           75.0
    ads      2024-01             2            4               1           25.0
    ads      2024-01             3            4               0            0.0
    ads      2024-02             0            3               3          100.0
    ads      2024-02             1            3               2           66.7
    ads      2024-02             2            3               0            0.0
    ads      2024-02             3            3               0            NaN
organic      2024-01             0            2               2          100.0
organic      2024-01             1            2               2          100.0
organic      2024-01             2            2               1           50.0
organic      2024-01             3            2               1           50.0
organic      2024-02             0            2               2          100.0
organic      2024-02             1            2               1           50.0
organic      2024-02             2            2               1           50.0
organic      2024-02             3            2               0            NaN
organic      2024-03             0            1               0            0.0
organic      2024-03             1            1               0            0.0
organic      2024-03             2            1               0            NaN
organic      2024-03             3            1               0            NaN

pandas equals SQL: OK

INNER JOIN version: rows = 12 (spine version has 20 )
channel cohort_month  month_offset  retained_users
    ads      2024-01             0               4
    ads      2024-01             1               3
    ads      2024-01             2               1
    ads      2024-02             0               3
    ads      2024-02             1               2
organic      2024-01             0               2
organic      2024-01             1               2
organic      2024-01             2               1
organic      2024-01             3               1
organic      2024-02             0               2
organic      2024-02             1               1
organic      2024-02             2               1
organic 2024-03 cohort present in the INNER JOIN version? False

offset 1, observed cells: pooled = 66.7 | mean of cell percentages = 58.3
```

**Edge cases:**
- Distinct users, not logins: user 1 has two February logins; `COUNT(DISTINCT user_id)` gives 1.
- Unobserved versus zero: a young cohort has offsets that cannot be observed yet (NULL here); showing 0 would look like churn (the same censoring idea as Q44).
- A cohort with no logins at all (organic March) is a row of zeros, not a missing row; the pivot needs the reindex with the cohort sizes, otherwise it is absent in pandas too.
- A login before the signup date would give a negative offset; the spine filters offsets to 0 to 3, so it drops out, but check the data.
- Users with no signup-month login still count in the denominator (cohort size comes from `users`, not from logins).
- Month offset uses calendar months, not 30-day periods; a user who signs up on 01-31 and logs in on 02-01 is offset 1 (user 4).

**Then explain:**
- A retention matrix is a grid; the grid has to be built first (cohort x offset), and the activity is attached to it.
- INNER JOIN keeps only cells with at least one returning user, so exactly the weak cells (zeros) vanish, making retention look better and charts jagged.
- The denominator is the cohort size per (channel, month), calculated from the users table independently of the join.
- Channel stays in the grain; compare channels, do not pool them unless you pool counts.
- In pandas, `reindex(..., fill_value=0)` on a MultiIndex pivot is the spine, and `stack` puts it back in long form.

**Follow-ups:**
- Day-N versus month-N retention? Different definition; state which (Part 8 covers metric design).
- How would you add a "rolling" retention (any login on or after month k)? Different numerator, and it is not available for the youngest cohorts.
- Offsets beyond 3? Change the `VALUES` list or generate it recursively; the as-of rule keeps the table honest.

**Common mistakes:**
- INNER JOIN or a `WHERE` on the right table of a LEFT JOIN, which turns it back into an inner join.
- Counting logins instead of distinct users.
- Zero-filling cells that are not observed yet.
- Averaging percentages across cohorts of different size.

### Q42 ⭐ 🔴 Cohort lifetime value by month: orders(order_id, user_id, order_ts, amount). For each first-order cohort and months_since_first, return cumulative revenue per cohort user (revenue to date divided by cohort size), with zero-fill for months with no sales so the cumulative line does not break. Cross-reference Part 5 for the running total mechanics and show the pandas version with pivot_table, fillna(0), cumsum(axis=1) and division by cohort size.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Assign each user to the month of their first order, build a cohort x months_since_first spine, left join monthly revenue with zero fill, take a running total per cohort (Part 5 mechanics) and divide by the cohort size; only offsets that have actually happened by the as-of date are shown, so young cohorts do not get a false flat line.

**Schema and sample data:** ten orders from six users. Cohorts by first-order month: Jan = users 1 and 2 (size 2), Feb = users 3 and 4 (size 2), Mar = user 5, Apr = user 6. Users 1, 2 and 3 buy again later, with a gap month (no sales in the cohort's second month). Convention: calendar months from the stored timestamps, no time zone, no weeks; as-of date 2024-04-30, so the last observed calendar month is April and offsets run 0 to 3.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05 09:30:00',100),(2,1,'2024-03-10 18:00:00',50),(3,2,'2024-01-20 11:00:00',60),
 (4,3,'2024-02-03 10:15:00',80),(5,3,'2024-02-20 19:45:00',20),(6,3,'2024-04-15 08:00:00',40),
 (7,4,'2024-02-14 12:00:00',30),(8,5,'2024-03-08 21:00:00',90),(9,2,'2024-04-02 07:30:00',10),
 (10,6,'2024-04-10 13:00:00',70);
```

**SQL answer:** first month per user, cohort sizes, an offset spine limited to observed months, revenue per (cohort, offset), then `SUM(...) OVER (PARTITION BY cohort ORDER BY offset ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` over the zero-filled revenue (`SQL_MAIN`). Running totals over frames are the subject of Part 5.
```sql
WITH o AS (
  SELECT user_id, amount, strftime('%Y-%m', order_ts) AS m,
         CAST(strftime('%Y', order_ts) AS INTEGER) * 12 + CAST(strftime('%m', order_ts) AS INTEGER) AS mi
  FROM orders
), first AS (
  SELECT user_id, MIN(mi) AS first_mi, MIN(m) AS cohort_month FROM o GROUP BY user_id
), cohort AS (
  SELECT first_mi, cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY first_mi, cohort_month
), offsets(k) AS (VALUES (0), (1), (2), (3)),
spine AS (
  SELECT c.first_mi, c.cohort_month, c.cohort_size, k AS months_since_first
  FROM cohort c CROSS JOIN offsets
  WHERE c.first_mi + k <= 2024 * 12 + 4          -- observed only: calendar month <= as-of month
), rev AS (
  SELECT f.first_mi, o.mi - f.first_mi AS months_since_first, SUM(o.amount) AS revenue
  FROM o JOIN first f ON f.user_id = o.user_id GROUP BY 1, 2
)
SELECT s.cohort_month, s.months_since_first, s.cohort_size,
       COALESCE(r.revenue, 0) AS revenue,
       SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_revenue,
       ROUND(1.0 * SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / s.cohort_size, 2) AS ltv_per_user
FROM spine s LEFT JOIN rev r ON r.first_mi = s.first_mi AND r.months_since_first = s.months_since_first
ORDER BY s.cohort_month, s.months_since_first
```

**pandas answer:** `pivot_table`, `reindex` the offsets, `fillna(0)`, `cumsum(axis=1)`, divide by cohort size, then mask the unobserved cells (without the mask the zero fill creates a false flat tail).
```py
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
o["m"] = o["order_ts"].dt.to_period("M")
o["cohort"] = o.groupby("user_id")["m"].transform("min")
o["months_since_first"] = (o["m"] - o["cohort"]).apply(lambda d: d.n)
size = o.groupby("cohort")["user_id"].nunique()
rev = o.pivot_table(index="cohort", columns="months_since_first", values="amount", aggfunc="sum")
rev = rev.reindex(columns=[0, 1, 2, 3]).fillna(0)
cum = rev.cumsum(axis=1)
ltv = cum.div(size, axis=0)
last_obs = (pd.Period("2024-04", "M") - ltv.index).map(lambda d: d.n)           # highest observed offset per cohort
ltv = ltv.where(pd.DataFrame({k: last_obs >= k for k in ltv.columns}, index=ltv.index))   # mask unobserved cells
cum = cum.where(ltv.notna())
rev = rev.where(ltv.notna())
long = (rev.stack().rename("revenue").to_frame()
        .join(cum.stack().rename("cum_revenue")).join(ltv.stack().rename("ltv_per_user"))
        .dropna().reset_index())                      # pandas 3 stack() keeps NaN, so drop the unobserved cells
long["cohort_month"] = long["cohort"].astype(str)
long["cohort_size"] = long["cohort"].map(size).astype(int)
long[["revenue", "cum_revenue"]] = long[["revenue", "cum_revenue"]].astype(int)
long["ltv_per_user"] = long["ltv_per_user"].round(2)
pd_df = long[["cohort_month", "months_since_first", "cohort_size", "revenue", "cum_revenue", "ltv_per_user"]]
```

**Example:**
- Jan cohort (users 1 and 2): month 0 (January) revenue = 100 + 60 = 160. Month 1 (February) has no order: revenue 0 but the cumulative stays 160. Month 2 (March) = 50 (user 1), cumulative 210. Month 3 (April) = 10 (user 2), cumulative 220. Per cohort user: 80, 80, 105, 110.
- Feb cohort (users 3 and 4, size 2): month 0 = 80 + 20 + 30 = 130; month 1 (March) = 0; month 2 (April) = 40, cumulative 170, per user 65, 65, 85. Month 3 would be May, after the as-of date, so it is not reported.
- Mar cohort (user 5, 90): 90 then 90 (April had no order, cumulative stays). Apr cohort: 70 at month 0 only.
- The "wrong" table in the output zero-fills the unobserved cells and cumulates anyway: Feb shows 85.0 at month 3 and Mar and Apr show flat lines to month 3, which looks like a retained value that was never measured.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q42: cohort lifetime value (cumulative revenue per cohort user) with zero-filled months
# Convention: calendar months from stored text timestamps (no time zone); as-of date fixed at 2024-04-30, so only
# offsets whose calendar month is <= 2024-04 are reported. Cohort = month of the user's first order.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05 09:30:00',100),(2,1,'2024-03-10 18:00:00',50),(3,2,'2024-01-20 11:00:00',60),
 (4,3,'2024-02-03 10:15:00',80),(5,3,'2024-02-20 19:45:00',20),(6,3,'2024-04-15 08:00:00',40),
 (7,4,'2024-02-14 12:00:00',30),(8,5,'2024-03-08 21:00:00',90),(9,2,'2024-04-02 07:30:00',10),
 (10,6,'2024-04-10 13:00:00',70);
"""
SQL_MAIN = """
WITH o AS (
  SELECT user_id, amount, strftime('%Y-%m', order_ts) AS m,
         CAST(strftime('%Y', order_ts) AS INTEGER) * 12 + CAST(strftime('%m', order_ts) AS INTEGER) AS mi
  FROM orders
), first AS (
  SELECT user_id, MIN(mi) AS first_mi, MIN(m) AS cohort_month FROM o GROUP BY user_id
), cohort AS (
  SELECT first_mi, cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY first_mi, cohort_month
), offsets(k) AS (VALUES (0), (1), (2), (3)),
spine AS (
  SELECT c.first_mi, c.cohort_month, c.cohort_size, k AS months_since_first
  FROM cohort c CROSS JOIN offsets
  WHERE c.first_mi + k <= 2024 * 12 + 4          -- observed only: calendar month <= as-of month
), rev AS (
  SELECT f.first_mi, o.mi - f.first_mi AS months_since_first, SUM(o.amount) AS revenue
  FROM o JOIN first f ON f.user_id = o.user_id GROUP BY 1, 2
)
SELECT s.cohort_month, s.months_since_first, s.cohort_size,
       COALESCE(r.revenue, 0) AS revenue,
       SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_revenue,
       ROUND(1.0 * SUM(COALESCE(r.revenue, 0)) OVER (PARTITION BY s.cohort_month ORDER BY s.months_since_first
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / s.cohort_size, 2) AS ltv_per_user
FROM spine s LEFT JOIN rev r ON r.first_mi = s.first_mi AND r.months_since_first = s.months_since_first
ORDER BY s.cohort_month, s.months_since_first
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)

# --- pandas ---
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
o["m"] = o["order_ts"].dt.to_period("M")
o["cohort"] = o.groupby("user_id")["m"].transform("min")
o["months_since_first"] = (o["m"] - o["cohort"]).apply(lambda d: d.n)
size = o.groupby("cohort")["user_id"].nunique()
rev = o.pivot_table(index="cohort", columns="months_since_first", values="amount", aggfunc="sum")
rev = rev.reindex(columns=[0, 1, 2, 3]).fillna(0)
cum = rev.cumsum(axis=1)
ltv = cum.div(size, axis=0)
last_obs = (pd.Period("2024-04", "M") - ltv.index).map(lambda d: d.n)           # highest observed offset per cohort
ltv = ltv.where(pd.DataFrame({k: last_obs >= k for k in ltv.columns}, index=ltv.index))   # mask unobserved cells
cum = cum.where(ltv.notna())
rev = rev.where(ltv.notna())
long = (rev.stack().rename("revenue").to_frame()
        .join(cum.stack().rename("cum_revenue")).join(ltv.stack().rename("ltv_per_user"))
        .dropna().reset_index())                      # pandas 3 stack() keeps NaN, so drop the unobserved cells
long["cohort_month"] = long["cohort"].astype(str)
long["cohort_size"] = long["cohort"].map(size).astype(int)
long[["revenue", "cum_revenue"]] = long[["revenue", "cum_revenue"]].astype(int)
long["ltv_per_user"] = long["ltv_per_user"].round(2)
pd_df = long[["cohort_month", "months_since_first", "cohort_size", "revenue", "cum_revenue", "ltv_per_user"]]
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values(["cohort_month", "months_since_first"]).reset_index(drop=True),
                              pd_df.sort_values(["cohort_month", "months_since_first"]).reset_index(drop=True),
                              check_dtype=False)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
raw = (o.pivot_table(index="cohort", columns="months_since_first", values="amount", aggfunc="sum")
         .reindex(columns=[0, 1, 2, 3]).fillna(0))
print("\nWRONG: zero-fill everything and cumsum, no as-of mask (false flat tails for young cohorts):")
print(raw.cumsum(axis=1).div(size, axis=0).round(2).to_string())
```

**Output (my run):**
```text
cohort_month  months_since_first  cohort_size  revenue  cum_revenue  ltv_per_user
     2024-01                   0            2      160          160          80.0
     2024-01                   1            2        0          160          80.0
     2024-01                   2            2       50          210         105.0
     2024-01                   3            2       10          220         110.0
     2024-02                   0            2      130          130          65.0
     2024-02                   1            2        0          130          65.0
     2024-02                   2            2       40          170          85.0
     2024-03                   0            1       90           90          90.0
     2024-03                   1            1        0           90          90.0
     2024-04                   0            1       70           70          70.0

pandas equals SQL: OK

WRONG: zero-fill everything and cumsum, no as-of mask (false flat tails for young cohorts):
months_since_first     0     1      2      3
cohort                                      
2024-01             80.0  80.0  105.0  110.0
2024-02             65.0  65.0   85.0   85.0
2024-03             90.0  90.0   90.0   90.0
2024-04             70.0  70.0   70.0   70.0
```

**Edge cases:**
- A month with no sales: the spine and `COALESCE(revenue, 0)` keep the row, so the running total does not skip or break.
- Unobserved offsets: exclude (NULL or drop), never zero-fill; the SQL does this with the `WHERE first_mi + k <= as-of month` filter, pandas with the mask.
- Cohort size is the count of users with a first order in that month, not the count of buyers in the later month; a user with several orders in a month counts once.
- Refunds or negative amounts make the cumulative line go down; the arithmetic is the same.
- Users with no orders are not in any cohort here (the cohort is defined by a first order); if the cohort should be signups, take the denominator from the users table and the question changes.
- `ORDER BY` inside the window needs a unique key per partition (the offset is unique per cohort); otherwise state the frame explicitly, as done here with `ROWS`.

**Then explain:**
- LTV here is cumulative revenue per original cohort user (not per active user), so the line can only go up when revenue is non-negative, and it plateaus when buying stops.
- Zero-fill matters because a window function over only the rows that exist carries the previous value correctly for a running total, but the missing offset row itself would be absent from the output and from any chart.
- Months since first is a calendar-month difference (`year * 12 + month`), not 30-day periods.
- Revenue to date divided by cohort size is gross revenue, not margin or discounted value; LTV with margin or a discount rate is a different metric.

**Follow-ups:**
- How would you get LTV by channel? Add channel to the cohort key; the spine and the denominator then use that key (Q41).
- How do you compare cohorts of different age? Compare the same offset (for example month 2) across cohorts, and only where observed.
- How do you extrapolate? Fit the shape of older cohorts and project; that is modelling, not SQL.

**Common mistakes:**
- Dividing by the number of buyers in the month instead of the cohort size.
- Letting the cumulative line extend over months that have not happened.
- Running a window over the sparse rows and plotting gaps as if they were zero revenue.
- Cutting the cohort month from a UTC timestamp when the business month is in another time zone (Q45).

### Q43 ⭐ 🔴 ISO week and year-boundary traps in year-over-year weekly comparison: sales(sale_date, amount). 2024-12-30 belongs to ISO week 1 of 2025 and 2021-01-01 to ISO week 53 of 2020. Show a naive strftime('%Y') plus week grouping splitting or merging weeks, the SQLite %W result, the ISO year emulation with date(d, '-3 days', 'weekday 4') (Thursday of the ISO week determines the ISO year), and pandas isocalendar(). Explain the 52 versus 53 week year problem for same-week-last-year comparisons and the 364-day offset alternative.
**Asked at:** SQLite date and time functions documentation (lang_datefunc, opened), vendor documentation and not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Group weeks by ISO year and ISO week, not by the calendar year plus `%W`; in SQLite 3.45.1 `%V` and `%G` return NULL, so I take the Thursday of the week, `date(d, '-3 days', 'weekday 4')`, whose year is the ISO year, and for same-week-last-year I either match ISO year minus 1 (week 53 then has no partner) or use a 364-day offset that always lands on the same weekday.

**Schema and sample data:** sixteen daily sales rows chosen around the year boundaries 2019/2020, 2020/2021, 2023/2024 and 2024/2025. Convention: weeks start on Monday (ISO 8601: week 1 is the week with the first Thursday of the year), dates are plain text, no time zone. 2024-12-30 is a Monday in ISO week 1 of 2025; 2021-01-01 is a Friday in ISO week 53 of 2020 (both premises in the question are correct, and the code checks them).
```sql
CREATE TABLE sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO sales VALUES
 ('2019-12-29',3),('2019-12-30',4),('2020-01-06',8),('2020-12-31',5),('2021-01-01',7),('2021-01-03',9),('2021-01-04',11),
 ('2023-12-31',15),('2024-01-01',25),('2024-01-02',35),
 ('2024-12-29',10),('2024-12-30',20),('2024-12-31',30),('2025-01-01',40),('2025-01-05',50),('2025-01-06',60);
```

**SQL answer:** `SQL_DAYS` shows the keys per date, `SQL_NAIVE` the naive grouping, and `SQL_MAIN` the weekly totals with last year's comparison by ISO key and by 364 days. The Monday of the week is `date(d, '-6 days', 'weekday 1')`.
```sql
SELECT sale_date,
       strftime('%Y', sale_date) || '-' || strftime('%W', sale_date) AS naive_year_week,
       strftime('%Y', date(sale_date, '-3 days', 'weekday 4'))        AS iso_year,
       (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
       strftime('%V', sale_date)                                      AS native_V
FROM sales ORDER BY sale_date
```
```sql
SELECT strftime('%Y-%W', sale_date) AS naive_key, COUNT(*) AS days, SUM(amount) AS total
FROM sales WHERE sale_date >= '2024-12-23' GROUP BY 1 ORDER BY 1
```
```sql
WITH w AS (
  SELECT CAST(strftime('%Y', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) AS iso_year,
         (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
         date(sale_date, '-6 days', 'weekday 1') AS week_start,
         SUM(amount) AS total
  FROM sales GROUP BY 1, 2, 3
)
SELECT a.iso_year, a.iso_week, a.week_start, a.total,
       b.total AS iso_match_last_year,
       c.total AS offset_364_last_year
FROM w a
LEFT JOIN w b ON b.iso_year = a.iso_year - 1 AND b.iso_week = a.iso_week
LEFT JOIN w c ON c.week_start = date(a.week_start, '-364 days')
ORDER BY a.week_start
```

**pandas answer:** `dt.isocalendar()` gives year, week and day; the week start is the date minus its weekday; last year's totals are looked up by (year - 1, week) or by `week_start - 364 days`.
```py
s = pd.read_sql_query("SELECT * FROM sales", con, parse_dates=["sale_date"])
iso = s["sale_date"].dt.isocalendar()
s["iso_year"], s["iso_week"] = iso["year"].astype(int), iso["week"].astype(int)
s["week_start"] = s["sale_date"] - pd.to_timedelta(s["sale_date"].dt.weekday, unit="D")
wk = s.groupby(["iso_year", "iso_week", "week_start"], as_index=False)["amount"].sum().rename(columns={"amount": "total"})
iso_prev = wk.set_index(["iso_year", "iso_week"])["total"]
prev_key = pd.MultiIndex.from_arrays([wk["iso_year"] - 1, wk["iso_week"]])
wk["iso_match_last_year"] = iso_prev.reindex(prev_key).to_numpy()
off = wk.set_index("week_start")["total"]
wk["offset_364_last_year"] = off.reindex(wk["week_start"] - pd.Timedelta(days=364)).to_numpy()
pd_df = wk.sort_values("week_start")
pd_df["week_start"] = pd_df["week_start"].dt.strftime("%Y-%m-%d")
```

**Example:**
- 2024-12-30 and 2024-12-31 are in ISO 2025-W01, but `strftime('%Y-%W')` labels them `2024-53`; 2025-01-01 and 2025-01-05 get `2025-00`. One ISO week (total 20 + 30 + 40 + 50 = 140) is split into two naive groups (50 and 90), and `2024-53` is not an ISO week of 2024 at all.
- Thursday rule: 2024-12-30 minus 3 days is 2024-12-27 (a Friday), `weekday 4` moves forward to the next Thursday, 2025-01-02, whose year is 2025, and `%j` = 2, so week = (2 - 1) / 7 + 1 = 1. For 2021-01-01 the Thursday is 2020-12-31 (day 366 of a leap year), week = 365 / 7 + 1 = 53, year 2020.
- Same ISO week last year: 2025-W01 (140) against 2024-W01 (25 + 35 = 60). 2020-W53 (21) has no 2019-W53 because 2019 has 52 ISO weeks (pandas confirms: 2020 -> 53, 2019 -> 52), so the ISO match is NULL while the 364-day offset gives the week starting 2019-12-30 (4).
- The two methods disagree for 2021-W01 (starts 2021-01-04): ISO match is 2020-W01 (4, the week starting 2019-12-30), 364 days back is the week starting 2020-01-06 (8, ISO 2020-W02).

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q43: ISO weeks, year boundaries, same-week-last-year
# Convention: weeks start on MONDAY (ISO 8601); dates are plain text, no time zone.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO sales VALUES
 ('2019-12-29',3),('2019-12-30',4),('2020-01-06',8),('2020-12-31',5),('2021-01-01',7),('2021-01-03',9),('2021-01-04',11),
 ('2023-12-31',15),('2024-01-01',25),('2024-01-02',35),
 ('2024-12-29',10),('2024-12-30',20),('2024-12-31',30),('2025-01-01',40),('2025-01-05',50),('2025-01-06',60);
"""
SQL_DAYS = """
SELECT sale_date,
       strftime('%Y', sale_date) || '-' || strftime('%W', sale_date) AS naive_year_week,
       strftime('%Y', date(sale_date, '-3 days', 'weekday 4'))        AS iso_year,
       (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
       strftime('%V', sale_date)                                      AS native_V
FROM sales ORDER BY sale_date
"""
# weekly totals keyed by ISO year and week, then compared with the same ISO week one year earlier
SQL_MAIN = """
WITH w AS (
  SELECT CAST(strftime('%Y', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) AS iso_year,
         (CAST(strftime('%j', date(sale_date, '-3 days', 'weekday 4')) AS INTEGER) - 1) / 7 + 1 AS iso_week,
         date(sale_date, '-6 days', 'weekday 1') AS week_start,
         SUM(amount) AS total
  FROM sales GROUP BY 1, 2, 3
)
SELECT a.iso_year, a.iso_week, a.week_start, a.total,
       b.total AS iso_match_last_year,
       c.total AS offset_364_last_year
FROM w a
LEFT JOIN w b ON b.iso_year = a.iso_year - 1 AND b.iso_week = a.iso_week
LEFT JOIN w c ON c.week_start = date(a.week_start, '-364 days')
ORDER BY a.week_start
"""
SQL_NAIVE = """
SELECT strftime('%Y-%W', sale_date) AS naive_key, COUNT(*) AS days, SUM(amount) AS total
FROM sales WHERE sale_date >= '2024-12-23' GROUP BY 1 ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
days = pd.read_sql_query(SQL_DAYS, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(days.to_string(index=False))

# --- pandas ---
s = pd.read_sql_query("SELECT * FROM sales", con, parse_dates=["sale_date"])
iso = s["sale_date"].dt.isocalendar()
s["iso_year"], s["iso_week"] = iso["year"].astype(int), iso["week"].astype(int)
s["week_start"] = s["sale_date"] - pd.to_timedelta(s["sale_date"].dt.weekday, unit="D")
wk = s.groupby(["iso_year", "iso_week", "week_start"], as_index=False)["amount"].sum().rename(columns={"amount": "total"})
iso_prev = wk.set_index(["iso_year", "iso_week"])["total"]
prev_key = pd.MultiIndex.from_arrays([wk["iso_year"] - 1, wk["iso_week"]])
wk["iso_match_last_year"] = iso_prev.reindex(prev_key).to_numpy()
off = wk.set_index("week_start")["total"]
wk["offset_364_last_year"] = off.reindex(wk["week_start"] - pd.Timedelta(days=364)).to_numpy()
pd_df = wk.sort_values("week_start")
pd_df["week_start"] = pd_df["week_start"].dt.strftime("%Y-%m-%d")
# --- end pandas ---
# the emulated ISO key equals pandas isocalendar for every row
assert (days["iso_year"].astype(int).to_numpy() == s.sort_values("sale_date")["iso_year"].to_numpy()).all()
assert (days["iso_week"].to_numpy() == s.sort_values("sale_date")["iso_week"].to_numpy()).all()
print("\nemulation date(d,'-3 days','weekday 4') equals pandas isocalendar() on all", len(days), "dates: OK")
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df.reset_index(drop=True), check_dtype=False)
print("\nweekly totals with last-year comparisons:")
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")
print("\nnaive strftime('%Y-%W') grouping from 2024-12-23 on:")
print(pd.read_sql_query(SQL_NAIVE, con).to_string(index=False))

# resample anchors (pandas 3.0.5): which weekday ends the bin and which side is labelled
d = s.set_index("sale_date")["amount"]
d = d[d.index >= "2024-12-23"]
print("\nresample('W-SUN') (Mon..Sun bins, label = Sunday):", {str(k.date()): int(v) for k, v in d.resample("W-SUN").sum().items()})
print("resample('W-MON') (Tue..Mon bins, label = Monday):  ", {str(k.date()): int(v) for k, v in d.resample("W-MON").sum().items()})
print("resample('MS') labels:", [str(k.date()) for k in d.resample("MS").sum().index], "| (labels are the bin starts)")
print("weeks in ISO year: 2020 ->", pd.Timestamp("2020-12-28").isocalendar().week, "| 2019 ->", pd.Timestamp("2019-12-28").isocalendar().week,
      "| 2024 ->", pd.Timestamp("2024-12-28").isocalendar().week)
print("SQLite %V, %G on 3.45.1:", con.execute("SELECT strftime('%V','2024-12-30'), strftime('%G','2024-12-30'), strftime('%U','2024-12-30')").fetchone())
```

**Output (my run):**
```text
 sale_date naive_year_week iso_year  iso_week native_V
2019-12-29         2019-51     2019        52     None
2019-12-30         2019-52     2020         1     None
2020-01-06         2020-01     2020         2     None
2020-12-31         2020-52     2020        53     None
2021-01-01         2021-00     2020        53     None
2021-01-03         2021-00     2020        53     None
2021-01-04         2021-01     2021         1     None
2023-12-31         2023-52     2023        52     None
2024-01-01         2024-01     2024         1     None
2024-01-02         2024-01     2024         1     None
2024-12-29         2024-52     2024        52     None
2024-12-30         2024-53     2025         1     None
2024-12-31         2024-53     2025         1     None
2025-01-01         2025-00     2025         1     None
2025-01-05         2025-00     2025         1     None
2025-01-06         2025-01     2025         2     None

emulation date(d,'-3 days','weekday 4') equals pandas isocalendar() on all 16 dates: OK

weekly totals with last-year comparisons:
 iso_year  iso_week week_start  total  iso_match_last_year  offset_364_last_year
     2019        52 2019-12-23      3                  NaN                   NaN
     2020         1 2019-12-30      4                  NaN                   NaN
     2020         2 2020-01-06      8                  NaN                   NaN
     2020        53 2020-12-28     21                  NaN                   4.0
     2021         1 2021-01-04     11                  4.0                   8.0
     2023        52 2023-12-25     15                  NaN                   NaN
     2024         1 2024-01-01     60                  NaN                   NaN
     2024        52 2024-12-23     10                 15.0                  15.0
     2025         1 2024-12-30    140                 60.0                  60.0
     2025         2 2025-01-06     60                  NaN                   NaN

pandas equals SQL: OK

naive strftime('%Y-%W') grouping from 2024-12-23 on:
naive_key  days  total
  2024-52     1     10
  2024-53     2     50
  2025-00     2     90
  2025-01     1     60

resample('W-SUN') (Mon..Sun bins, label = Sunday): {'2024-12-29': 10, '2025-01-05': 140, '2025-01-12': 60}
resample('W-MON') (Tue..Mon bins, label = Monday):   {'2024-12-30': 30, '2025-01-06': 180}
resample('MS') labels: ['2024-12-01', '2025-01-01'] | (labels are the bin starts)
weeks in ISO year: 2020 -> 53 | 2019 -> 52 | 2024 -> 52
SQLite %V, %G on 3.45.1: (None, None, None)
```

**Edge cases:**
- 52 versus 53 week years: an ISO year has 53 weeks when 1 January is a Thursday, or a Wednesday in a leap year (2020 is the example here). Week 53 has no partner the year before, and week 1 can contain days from December.
- Never mix `%Y` with an ISO week: use the ISO year (Thursday's year) from the same expression. `%Y` of 2024-12-30 is 2024 but its ISO year is 2025.
- `%W` is the week number with Monday as the first day and days before the first Monday in week 00; it is not ISO (2024-12-30 gives 53). `%U` and `%V` and `%G` returned NULL in this run on SQLite 3.45.1.
- The 364-day offset (52 weeks) keeps weekday alignment, but after a few years the week drifts relative to the calendar (a 53-week year shifts it by one week), so holidays and seasons slide; fiscal calendars solve this with a 4-4-5 pattern (not executed or modelled here).
- Missing weeks: a LEFT JOIN returns NULL for the partner; in pandas `reindex` gives `NaN`. A week with partial data (as-of in mid-week) should not be compared with a full week.
- pandas resampling anchors: `resample('W-SUN')` makes Monday-to-Sunday bins labelled by the Sunday (matches ISO weeks); `resample('W-MON')` makes Tuesday-to-Monday bins labelled by the Monday and gives different totals (30 and 180 against 10, 140, 60 in the output). `resample('MS')` labels months by their first day.

**Then explain:**
- ISO 8601: weeks start Monday, week 1 contains the first Thursday, so the Thursday of a week decides which year it belongs to.
- Hence `date(d, '-3 days', 'weekday 4')`: step back 3 days, then move forward to a Thursday; for a Monday this is the same week's Thursday, for a Sunday it is the Thursday 3 days earlier.
- ISO week of year = `(day_of_year(Thursday) - 1) / 7 + 1`.
- Year-over-year weekly comparison has to choose: same ISO week (calendar aligned, 53-week gap) or same weekday 364 days earlier (weekday aligned, drifts). Say which and why.

**Follow-ups:**
- How would you compute ISO weeks on PostgreSQL, MySQL, BigQuery, Snowflake? Their functions (`EXTRACT(ISOYEAR ...)`, `YEARWEEK(d, 3)`, `ISOWEEK`, `WEEKISO`) exist as far as I know, not executed here; the logic is the same.
- What about weeks starting Sunday? Then it is a different convention (US); the Thursday trick does not apply; define the week start first.
- How do you handle the 53-week year in a chart? Compare 53 against 52 or use the 364-day offset and label the alignment.

**Common mistakes:**
- Grouping by `strftime('%Y')` plus a week number and splitting an ISO week across two years.
- Joining week 53 to a week that does not exist.
- Using `%W` and calling it ISO.
- Not stating the week-start convention.

### Q44 ⭐ 🔴 Tenure survival curve: subscriptions(sub_id, user_id, start_date, end_date) with NULL end_date for active. For each tenure month t (0 to 12) return the share of subscriptions that survived to month t, counting only subscriptions old enough to be observed at t (right-censoring: a subscription started two months ago cannot show month 6). Show the wrong version that treats unobserved as churned, with SQLite date arithmetic from an as-of date, and the pandas version with Timedelta months via DateOffset or period difference.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** For each tenure month t I compute every subscription's t-month anniversary, count a subscription as observed only if the anniversary is on or before the as-of date, and divide the survivors (end_date NULL or on or after the anniversary) by the observed count; dividing by all subscriptions treats the not-yet-observable ones as churned and understates survival.

**Schema and sample data:** ten subscriptions started between 2023-01 and 2024-05, some ended, some still active. Convention: as-of date `2024-06-30` (fixed, not today), end_date is inclusive (last day of service), dates are plain text, no time zone, no weeks; tenure month t is the t-month anniversary of start_date, clipped to the month end (2023-08-31 plus 6 months is 2024-02-29), and "survived to t" means still active on that anniversary.
```sql
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1,1,'2023-01-15',NULL),(2,2,'2023-01-20','2023-04-10'),(3,3,'2023-03-31','2023-05-15'),
 (4,4,'2023-05-10',NULL),(5,5,'2023-08-31','2023-12-31'),(6,6,'2023-09-05','2024-02-20'),
 (7,7,'2023-11-15',NULL),(8,8,'2024-01-31','2024-03-10'),(9,9,'2024-03-12',NULL),(10,10,'2024-05-20',NULL);
```

**SQL answer:** a `t` series 0 to 12 cross joined to subscriptions, the anniversary expression (the clip is a `CASE`, because SQLite's `+N months` overflows), then `observed`, `survived`, the correct share, and the wrong share (`SQL_MAIN`; the anniversary expression is built into the query text by the f-string in the Code block and printed here as evaluated).
```sql
WITH RECURSIVE t(t) AS (SELECT 0 UNION ALL SELECT t + 1 FROM t WHERE t < 12),
x AS (
  SELECT t.t, s.sub_id, s.end_date, CASE WHEN strftime('%d', date(s.start_date, '+' || t.t || ' months')) = strftime('%d', s.start_date)
        THEN date(s.start_date, '+' || t.t || ' months')
        ELSE date(s.start_date, 'start of month', '+' || (t.t + 1) || ' months', '-1 day') END AS anniv
  FROM t CROSS JOIN subscriptions s
)
SELECT t,
       SUM(anniv <= '2024-06-30')                                            AS observed,
       SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv)) AS survived,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / SUM(anniv <= '2024-06-30'), 1)                                AS survival_pct,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / COUNT(*), 1)                                                  AS wrong_pct_unobserved_as_churned
FROM x GROUP BY t HAVING SUM(anniv <= '2024-06-30') > 0 ORDER BY t
```

**pandas answer:** `start_date + pd.DateOffset(months=t)` (which clips by itself) per t, masks for observed and survived.
```py
subs = pd.read_sql_query("SELECT * FROM subscriptions", con, parse_dates=["start_date", "end_date"])
as_of = pd.Timestamp("2024-06-30")
rows = []
for t in range(13):
    anniv = subs["start_date"] + pd.DateOffset(months=t)          # DateOffset clips to month end
    observed = anniv <= as_of
    survived = observed & (subs["end_date"].isna() | (subs["end_date"] >= anniv))
    if observed.sum() > 0:
        rows.append({"t": t, "observed": int(observed.sum()), "survived": int(survived.sum()),
                     "survival_pct": round(100.0 * survived.sum() / observed.sum(), 1),
                     "wrong_pct_unobserved_as_churned": round(100.0 * survived.sum() / len(subs), 1)})
pd_df = pd.DataFrame(rows)
```

**Example:**
- t = 2: only subscription 10 (start 2024-05-20, anniversary 2024-07-20) is after the as-of date, so 9 are observed. Survivors: sub 2 ended 2023-04-10, after its anniversary 2023-03-20, so it survived month 2; sub 3 ended 2023-05-15, before 2023-05-31, did not; sub 8 ended 2024-03-10, before 2024-03-31, did not. Survivors 1, 2, 4, 5, 6, 7, 9 = 7, so 7 / 9 = 77.8%. The wrong version divides by 10 (all subscriptions): 70.0%.
- t = 12: observed are the four subscriptions that started on or before 2023-06-30 (subs 1, 2, 3, 4); survivors are subs 1 and 4, so 2 / 4 = 50.0%; the wrong version gives 2 / 10 = 20.0%.
- The wrong column keeps falling as t grows because the denominator never shrinks, even for subscriptions that are too young to be judged.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q44: tenure survival with right-censoring from a fixed as-of date
# Convention: dates are plain text, no time zone. as_of = 2024-06-30. end_date is INCLUSIVE (last day of service).
# A subscription "survives to month t" if it is still active on its t-month anniversary:
#   end_date IS NULL OR end_date >= anniversary. It is "observed at t" only if anniversary <= as_of.
# Anniversary = start_date + t months, clipped to the last day of the month (Aug 31 + 6 months = Feb 29, not Mar 2).
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE subscriptions(sub_id INTEGER PRIMARY KEY, user_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO subscriptions VALUES
 (1,1,'2023-01-15',NULL),(2,2,'2023-01-20','2023-04-10'),(3,3,'2023-03-31','2023-05-15'),
 (4,4,'2023-05-10',NULL),(5,5,'2023-08-31','2023-12-31'),(6,6,'2023-09-05','2024-02-20'),
 (7,7,'2023-11-15',NULL),(8,8,'2024-01-31','2024-03-10'),(9,9,'2024-03-12',NULL),(10,10,'2024-05-20',NULL);
"""
ANNIV = """CASE WHEN strftime('%d', date(s.start_date, '+' || t.t || ' months')) = strftime('%d', s.start_date)
        THEN date(s.start_date, '+' || t.t || ' months')
        ELSE date(s.start_date, 'start of month', '+' || (t.t + 1) || ' months', '-1 day') END"""
SQL_MAIN = f"""
WITH RECURSIVE t(t) AS (SELECT 0 UNION ALL SELECT t + 1 FROM t WHERE t < 12),
x AS (
  SELECT t.t, s.sub_id, s.end_date, {ANNIV} AS anniv
  FROM t CROSS JOIN subscriptions s
)
SELECT t,
       SUM(anniv <= '2024-06-30')                                            AS observed,
       SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv)) AS survived,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / SUM(anniv <= '2024-06-30'), 1)                                AS survival_pct,
       ROUND(100.0 * SUM(anniv <= '2024-06-30' AND (end_date IS NULL OR end_date >= anniv))
             / COUNT(*), 1)                                                  AS wrong_pct_unobserved_as_churned
FROM x GROUP BY t HAVING SUM(anniv <= '2024-06-30') > 0 ORDER BY t
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)

# --- pandas ---
subs = pd.read_sql_query("SELECT * FROM subscriptions", con, parse_dates=["start_date", "end_date"])
as_of = pd.Timestamp("2024-06-30")
rows = []
for t in range(13):
    anniv = subs["start_date"] + pd.DateOffset(months=t)          # DateOffset clips to month end
    observed = anniv <= as_of
    survived = observed & (subs["end_date"].isna() | (subs["end_date"] >= anniv))
    if observed.sum() > 0:
        rows.append({"t": t, "observed": int(observed.sum()), "survived": int(survived.sum()),
                     "survival_pct": round(100.0 * survived.sum() / observed.sum(), 1),
                     "wrong_pct_unobserved_as_churned": round(100.0 * survived.sum() / len(subs), 1)})
pd_df = pd.DataFrame(rows)
# --- end pandas ---
pd.testing.assert_frame_equal(sql_df.sort_values("t").reset_index(drop=True), pd_df.sort_values("t").reset_index(drop=True),
                              check_dtype=False)
print(sql_df.to_string(index=False))
print("\npandas equals SQL: OK")

print("\nplain date(start,'+t months') overflow vs clipped, subscription 5 (start 2023-08-31) and 8 (2024-01-31):")
for sid in (5, 8):
    st = con.execute("SELECT start_date FROM subscriptions WHERE sub_id = ?", (sid,)).fetchone()[0]
    for t in (1, 6):
        naive = con.execute("SELECT date(?, '+' || ? || ' months')", (st, t)).fetchone()[0]
        clip = (pd.Timestamp(st) + pd.DateOffset(months=t)).date()
        print(f"  sub {sid} start {st} +{t} months: SQLite plain modifier {naive} | pandas DateOffset {clip}")
# period arithmetic alternative: whole calendar-month difference, ignores the day of month
p = (as_of.to_period("M") - subs["start_date"].dt.to_period("M")).apply(lambda d: d.n)
print("\nperiod difference (calendar months from start month to as-of month):", p.tolist())
print("elapsed full months via DateOffset (max t with anniversary <= as_of):",
      [max(t for t in range(30) if st + pd.DateOffset(months=t) <= as_of) for st in subs["start_date"]])
```

**Output (my run):**
```text
 t  observed  survived  survival_pct  wrong_pct_unobserved_as_churned
 0        10        10         100.0                            100.0
 1        10        10         100.0                            100.0
 2         9         7          77.8                             70.0
 3         9         6          66.7                             60.0
 4         8         5          62.5                             50.0
 5         8         4          50.0                             40.0
 6         7         3          42.9                             30.0
 7         7         3          42.9                             30.0
 8         6         2          33.3                             20.0
 9         6         2          33.3                             20.0
10         5         2          40.0                             20.0
11         4         2          50.0                             20.0
12         4         2          50.0                             20.0

pandas equals SQL: OK

plain date(start,'+t months') overflow vs clipped, subscription 5 (start 2023-08-31) and 8 (2024-01-31):
  sub 5 start 2023-08-31 +1 months: SQLite plain modifier 2023-10-01 | pandas DateOffset 2023-09-30
  sub 5 start 2023-08-31 +6 months: SQLite plain modifier 2024-03-02 | pandas DateOffset 2024-02-29
  sub 8 start 2024-01-31 +1 months: SQLite plain modifier 2024-03-02 | pandas DateOffset 2024-02-29
  sub 8 start 2024-01-31 +6 months: SQLite plain modifier 2024-07-31 | pandas DateOffset 2024-07-31

period difference (calendar months from start month to as-of month): [17, 17, 15, 13, 10, 9, 7, 5, 3, 1]
elapsed full months via DateOffset (max t with anniversary <= as_of): [17, 17, 15, 13, 10, 9, 7, 5, 3, 1]
```

**Edge cases:**
- Right-censoring: an active subscription is not a survivor at t if it has not reached t yet; it is simply not in that month's denominator.
- The observed share is not monotone: it rises at t = 10 and 11 (40.0%, 50.0%) because the observed set changes with t (different, older subscriptions). A proper survival estimate (Kaplan-Meier) uses the at-risk set at each step; this simple "share of observed" is a teaching version, and I did not implement Kaplan-Meier here.
- Month-end starts: `date('2023-08-31', '+6 months')` is `2024-03-02` in SQLite (overflow) while `DateOffset` gives `2024-02-29`; the code clips in SQL so the two agree, and the output prints both for subscriptions 5 and 8.
- Start and end on the same day (tenure 0): `end_date >= anniversary` is true on day 0 with an inclusive end, so a same-day cancellation survives month 0 under this definition; decide whether that is wanted.
- NULL start_date is dropped (comparison unknown); NULL end_date means active.
- Period difference (`as_of.to_period('M') - start.to_period('M')`) counts calendar months, ignoring the day: it gave 17, 17, 15, ...; the `DateOffset` count of fully elapsed months is the same here, but they differ when the as-of day of month is before the start day (start on the 20th, as-of the 10th of the next month: period difference 1, fully elapsed months 0).

**Then explain:**
- Survival at t among those who could have reached t; every t has its own denominator.
- The wrong version makes churn look worse and the curve look steeper for recent cohorts; the censored ones are neither churned nor survived.
- SQLite month arithmetic overflows and has no `DATEDIFF`, so the anniversary is built with modifiers and compared as ISO text; pandas `DateOffset(months=t)` clips to month end.
- Everything is relative to a fixed as-of date; with `now` the numbers would change on each run.

**Follow-ups:**
- Why not use churn rate per month? That is a hazard (churned in month t divided by at risk at t), the building block of survival; it can be derived from the same table.
- Can you do it by start cohort? Group by the start month as well; small cohorts will be noisy.
- What about subscriptions with a pause or a reactivation? Not modelled; it changes the event definition (Part 7 owns streaks and islands).

**Common mistakes:**
- Dividing by all subscriptions at every t.
- Counting active subscriptions as survivors for months that have not happened.
- Using `date(start, '+t months')` without noticing the day-31 overflow.
- Using today's date instead of a fixed as-of date.

### Q45 ⭐ 🔴 Date report fault-finding drill: a monthly revenue report is wrong. List five suspects in the order you would check them (BETWEEN with timestamps, a missing month spine and LAG, a time-zone shift of the day or month boundary, text dates in mixed formats sorting wrongly, join fan-out before aggregation or a partial current month) and for each show a tiny reproducing SQLite query plus the pandas counterpart, finishing with a reconciliation query that proves monthly totals sum to the overall total.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** I check five suspects in order of how often they bite: BETWEEN with timestamps, a missing month spine with LAG, a time-zone shift of the month boundary, text dates in mixed formats, and join fan-out (plus a partial current month); then I run a reconciliation query that proves the monthly totals add up to the overall total and exposes any unassigned bucket.

**Schema and sample data:** three tiny tables. `orders` (UTC timestamps, six rows), `order_items` (orders 1 and 2 have several items, three orders have none) and `raw_orders` (four rows with mixed date formats). Convention: stored timestamps are UTC, the business month is India time (UTC+05:30, no daylight saving), no week logic, and the as-of date is fixed at 2024-04-15, so April is a partial month.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-10 09:00:00',100),(2,'2024-01-31 14:00:00',50),(3,'2024-01-31 20:00:00',40),
  (4,'2024-03-05 10:00:00',70),(5,'2024-03-31 23:30:00',30),(6,'2024-04-02 08:00:00',20);
CREATE TABLE order_items(order_id INTEGER, sku TEXT);
INSERT INTO order_items VALUES (1,'a'),(1,'b'),(1,'c'),(2,'a'),(2,'b'),(4,'a');
CREATE TABLE raw_orders(order_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO raw_orders VALUES (1,'2024-01-05',10),(2,'2024-1-6',20),(3,'06/02/2024',30),(4,'2024-02-07',40);
```

**SQL answer:** one tiny query per suspect plus the reconciliation (`SQL_MAIN`), all in the Code block:
1. BETWEEN: `SQL_S1_BAD` and `SQL_S1_OK`.
2. Spine and LAG: `SQL_S2_BAD` and `SQL_S2_OK`.
3. Time zone: `SQL_S3_UTC` and `SQL_S3_IST`.
4. Mixed text dates: `SQL_S4_SORT` and `SQL_S4_BAD`.
5. Fan-out and partial month: `SQL_S5_BAD`, `SQL_S5_OK` and `SQL_S5_PARTIAL`.
```sql
SELECT SUM(amount) AS jan FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31'
```
```sql
SELECT SUM(amount) AS jan FROM orders WHERE order_ts >= '2024-01-01' AND order_ts < '2024-02-01'
```
```sql
WITH m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT month, total, LAG(month) OVER (ORDER BY month) AS prev_month, LAG(total) OVER (ORDER BY month) AS prev_total FROM m
```
```sql
WITH RECURSIVE sp(ms) AS (SELECT '2024-01-01' UNION ALL SELECT date(ms, '+1 month') FROM sp WHERE ms < '2024-04-01'),
m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT strftime('%Y-%m', sp.ms) AS month, COALESCE(m.total, 0) AS total,
       LAG(COALESCE(m.total, 0)) OVER (ORDER BY sp.ms) AS prev_total
FROM sp LEFT JOIN m ON m.month = strftime('%Y-%m', sp.ms) ORDER BY sp.ms
```
```sql
SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1
```
```sql
SELECT strftime('%Y-%m', datetime(order_ts, '+330 minutes')) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1
```
```sql
SELECT order_date FROM raw_orders ORDER BY order_date
```
```sql
SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total FROM raw_orders GROUP BY 1 ORDER BY 1
```
```sql
SELECT SUM(o.amount) AS total FROM orders o JOIN order_items i ON i.order_id = o.order_id
```
```sql
SELECT SUM(o.amount) AS total
FROM orders o LEFT JOIN (SELECT order_id, COUNT(*) AS n_items FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id
```
```sql
SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total,
       MAX(CAST(strftime('%d', '2024-04-15') AS INTEGER)) AS days_covered
FROM orders WHERE order_ts >= '2024-04-01' AND order_ts < '2024-04-16' GROUP BY 1
```
The reconciliation, which adds an explicit bucket for unparseable months and compares the sum of the months with the overall total:
```sql
WITH m AS (
  SELECT COALESCE(strftime('%Y-%m', datetime(order_ts, '+330 minutes')), 'UNPARSED') AS month, SUM(amount) AS total
  FROM orders GROUP BY 1
)
SELECT (SELECT SUM(amount) FROM orders) AS overall, SUM(total) AS sum_of_months,
       (SELECT SUM(amount) FROM orders) - SUM(total) AS diff,
       SUM(month = 'UNPARSED') AS unparsed_buckets FROM m
```

**pandas answer:** the counterparts, in the same order (the printed lines at the end of the output give their values).
```py
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
items = pd.read_sql_query("SELECT * FROM order_items", con)
raw = pd.read_sql_query("SELECT * FROM raw_orders", con)
p1_bad = o.loc[o["order_ts"] <= pd.Timestamp("2024-01-31"), "amount"]             # timestamp compare loses the 31st
p1_ok = o.loc[(o["order_ts"] >= "2024-01-01") & (o["order_ts"] < "2024-02-01"), "amount"]
p1_slice = o.set_index("order_ts").sort_index().loc["2024-01-01":"2024-01-31", "amount"]   # string slice includes the whole last day
monthly = o.groupby(o["order_ts"].dt.to_period("M"))["amount"].sum()
filled = monthly.reindex(pd.period_range("2024-01", "2024-04", freq="M"), fill_value=0)
ist = o["order_ts"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
ist_month = o.groupby(ist.dt.strftime("%Y-%m"))["amount"].sum()
raw["d"] = pd.to_datetime(raw["order_date"], errors="coerce", format="ISO8601")
raw_month = raw.groupby(raw["d"].dt.strftime("%Y-%m"))["amount"].sum()            # NaT keys are dropped silently
raw_month_na = raw.groupby(raw["d"].dt.strftime("%Y-%m"), dropna=False)["amount"].sum()
fan = o.merge(items, on="order_id")["amount"].sum()
ok5 = o.merge(items.groupby("order_id").size().rename("n_items").reset_index(), on="order_id", how="left")["amount"].sum()
recon = (o["amount"].sum(), ist_month.sum(), o["amount"].sum() - ist_month.sum())
recon_raw = (raw["amount"].sum(), raw_month.sum(), raw["amount"].sum() - raw_month.sum())
```

**Example:** orders total 310 (100 + 50 + 40 + 70 + 30 + 20).
- Suspect 1: `BETWEEN '2024-01-01' AND '2024-01-31'` sees only order 1 (100); orders 2 and 3 are at `2024-01-31 14:00:00` and `20:00:00`, which sort after the string `2024-01-31`. The half-open range gives 190.
- Suspect 2: months with data are Jan 190, Mar 100, Apr 20; `LAG` puts January next to March (`prev_month` 2024-01), so the report says March fell by 90, when February was actually 0 and March rose by 100. With the spine February is a row of 0 and LAG for March is 0.
- Suspect 3: UTC months give 190 / 100 / 20. India time moves order 3 (UTC 01-31 20:00 = 02-01 01:30) into February and order 5 (UTC 03-31 23:30 = 04-01 05:00) into April: 150 / 40 / 70 / 50. Same grand total, different months.
- Suspect 4: `'2024-1-6'` and `'06/02/2024'` are not valid SQLite date text, so `strftime` gives NULL months (a NULL group of 50); the text sort order is `06/02/2024`, then `2024-01-05`, `2024-02-07`, `2024-1-6` (wrong order). pandas parses `'2024-1-6'` but not `'06/02/2024'`, so its monthly numbers differ from SQLite's (30 + 40 = 70 versus 10 + 40 = 50 in SQLite), and `groupby` drops the NaT key silently unless `dropna=False`.
- Suspect 5: an INNER JOIN to order_items multiplies orders 1 (3 items) and 2 (2 items) and drops the three orders without items: 3 x 100 + 2 x 50 + 70 = 470 against the true 310; pre-aggregating items before the join keeps 310. The partial month: April holds only 15 days of data (to 2024-04-15), so April revenue of 20 cannot be compared with a full month.
- Reconciliation: on `orders` (India months) overall 310, months 310, diff 0. On `raw_orders` overall 100, months 50, diff 50: the NULL-month rows are missing; pandas reports 30 missing for the same data.

**Code:** run with `python3 -I`; the pandas result is asserted equal to the SQL result after sorting as stated in the code.
```python
# Q45: fault-finding drill for a wrong monthly revenue report
# Convention: orders.order_ts is UTC text 'YYYY-MM-DD HH:MM:SS'; the business month is India time (UTC+05:30, no DST).
# Fixed as-of date 2024-04-15, so April is a PARTIAL month. All amounts are toy numbers.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-10 09:00:00',100),(2,'2024-01-31 14:00:00',50),(3,'2024-01-31 20:00:00',40),
  (4,'2024-03-05 10:00:00',70),(5,'2024-03-31 23:30:00',30),(6,'2024-04-02 08:00:00',20);
CREATE TABLE order_items(order_id INTEGER, sku TEXT);
INSERT INTO order_items VALUES (1,'a'),(1,'b'),(1,'c'),(2,'a'),(2,'b'),(4,'a');
CREATE TABLE raw_orders(order_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO raw_orders VALUES (1,'2024-01-05',10),(2,'2024-1-6',20),(3,'06/02/2024',30),(4,'2024-02-07',40);
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(sql, **p):
    return pd.read_sql_query(sql, con, params=p)

# Suspect 1: BETWEEN with timestamps
SQL_S1_BAD = "SELECT SUM(amount) AS jan FROM orders WHERE order_ts BETWEEN '2024-01-01' AND '2024-01-31'"
SQL_S1_OK = "SELECT SUM(amount) AS jan FROM orders WHERE order_ts >= '2024-01-01' AND order_ts < '2024-02-01'"
# Suspect 2: no month spine, LAG compares to the previous ROW
SQL_S2_BAD = """
WITH m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT month, total, LAG(month) OVER (ORDER BY month) AS prev_month, LAG(total) OVER (ORDER BY month) AS prev_total FROM m
"""
SQL_S2_OK = """
WITH RECURSIVE sp(ms) AS (SELECT '2024-01-01' UNION ALL SELECT date(ms, '+1 month') FROM sp WHERE ms < '2024-04-01'),
m AS (SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1)
SELECT strftime('%Y-%m', sp.ms) AS month, COALESCE(m.total, 0) AS total,
       LAG(COALESCE(m.total, 0)) OVER (ORDER BY sp.ms) AS prev_total
FROM sp LEFT JOIN m ON m.month = strftime('%Y-%m', sp.ms) ORDER BY sp.ms
"""
# Suspect 3: UTC month versus India-time month
SQL_S3_UTC = "SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1"
SQL_S3_IST = "SELECT strftime('%Y-%m', datetime(order_ts, '+330 minutes')) AS month, SUM(amount) AS total FROM orders GROUP BY 1 ORDER BY 1"
# Suspect 4: text dates in mixed formats
SQL_S4_SORT = "SELECT order_date FROM raw_orders ORDER BY order_date"
SQL_S4_BAD = "SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total FROM raw_orders GROUP BY 1 ORDER BY 1"
# Suspect 5: join fan-out before aggregation, then the partial month
SQL_S5_BAD = "SELECT SUM(o.amount) AS total FROM orders o JOIN order_items i ON i.order_id = o.order_id"
SQL_S5_OK = """
SELECT SUM(o.amount) AS total
FROM orders o LEFT JOIN (SELECT order_id, COUNT(*) AS n_items FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id
"""
SQL_S5_PARTIAL = """
SELECT strftime('%Y-%m', order_ts) AS month, SUM(amount) AS total,
       MAX(CAST(strftime('%d', '2024-04-15') AS INTEGER)) AS days_covered
FROM orders WHERE order_ts >= '2024-04-01' AND order_ts < '2024-04-16' GROUP BY 1
"""
# Reconciliation: months (with an explicit bucket for unparseable dates) must add up to the overall total
SQL_MAIN = """
WITH m AS (
  SELECT COALESCE(strftime('%Y-%m', datetime(order_ts, '+330 minutes')), 'UNPARSED') AS month, SUM(amount) AS total
  FROM orders GROUP BY 1
)
SELECT (SELECT SUM(amount) FROM orders) AS overall, SUM(total) AS sum_of_months,
       (SELECT SUM(amount) FROM orders) - SUM(total) AS diff,
       SUM(month = 'UNPARSED') AS unparsed_buckets FROM m
"""
SQL_RECON_RAW = """
WITH m AS (SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total FROM raw_orders GROUP BY 1)
SELECT (SELECT SUM(amount) FROM raw_orders) AS overall, SUM(total) AS sum_of_months,
       (SELECT SUM(amount) FROM raw_orders) - SUM(total) AS diff FROM m WHERE month IS NOT NULL
"""
def show(title, df):
    print(f"--- {title}")
    print(df.to_string(index=False))

show("S1 BETWEEN '2024-01-01' AND '2024-01-31' (loses 31 Jan after 00:00)", q(SQL_S1_BAD))
show("S1 half-open range", q(SQL_S1_OK))
show("S2 LAG without spine (March compared with January)", q(SQL_S2_BAD))
show("S2 with spine", q(SQL_S2_OK))
show("S3 UTC month", q(SQL_S3_UTC))
show("S3 India-time month", q(SQL_S3_IST))
print("--- S4 text sort:", [r[0] for r in con.execute(SQL_S4_SORT)])
show("S4 strftime on mixed formats (NULL month = silently unassigned)", q(SQL_S4_BAD))
show("S5 INNER JOIN to order_items before SUM (multiplies orders 1 and 2, drops orders without items)", q(SQL_S5_BAD))
show("S5 pre-aggregate the many side first", q(SQL_S5_OK))
show("S5b partial month as of 2024-04-15", q(SQL_S5_PARTIAL))
show("RECONCILIATION on orders (India-time months)", q(SQL_MAIN))
show("RECONCILIATION on raw_orders (mixed formats)", q(SQL_RECON_RAW))

# --- pandas ---
o = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_ts"])
items = pd.read_sql_query("SELECT * FROM order_items", con)
raw = pd.read_sql_query("SELECT * FROM raw_orders", con)
p1_bad = o.loc[o["order_ts"] <= pd.Timestamp("2024-01-31"), "amount"]             # timestamp compare loses the 31st
p1_ok = o.loc[(o["order_ts"] >= "2024-01-01") & (o["order_ts"] < "2024-02-01"), "amount"]
p1_slice = o.set_index("order_ts").sort_index().loc["2024-01-01":"2024-01-31", "amount"]   # string slice includes the whole last day
monthly = o.groupby(o["order_ts"].dt.to_period("M"))["amount"].sum()
filled = monthly.reindex(pd.period_range("2024-01", "2024-04", freq="M"), fill_value=0)
ist = o["order_ts"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
ist_month = o.groupby(ist.dt.strftime("%Y-%m"))["amount"].sum()
raw["d"] = pd.to_datetime(raw["order_date"], errors="coerce", format="ISO8601")
raw_month = raw.groupby(raw["d"].dt.strftime("%Y-%m"))["amount"].sum()            # NaT keys are dropped silently
raw_month_na = raw.groupby(raw["d"].dt.strftime("%Y-%m"), dropna=False)["amount"].sum()
fan = o.merge(items, on="order_id")["amount"].sum()
ok5 = o.merge(items.groupby("order_id").size().rename("n_items").reset_index(), on="order_id", how="left")["amount"].sum()
recon = (o["amount"].sum(), ist_month.sum(), o["amount"].sum() - ist_month.sum())
recon_raw = (raw["amount"].sum(), raw_month.sum(), raw["amount"].sum() - raw_month.sum())
# --- end pandas ---
assert int(p1_bad.sum()) == int(q(SQL_S1_BAD)["jan"][0]) == 100
assert int(p1_ok.sum()) == int(p1_slice.sum()) == int(q(SQL_S1_OK)["jan"][0]) == 190
assert filled.tolist() == q(SQL_S2_OK)["total"].tolist()
assert ist_month.to_dict() == dict(zip(*[q(SQL_S3_IST)[c] for c in ("month", "total")]))
assert int(fan) == int(q(SQL_S5_BAD)["total"][0]) and int(ok5) == int(q(SQL_S5_OK)["total"][0])
r = q(SQL_MAIN)
assert tuple(int(v) for v in r.iloc[0, :3]) == tuple(int(v) for v in recon)
r2 = q(SQL_RECON_RAW)
assert tuple(int(v) for v in r2.iloc[0, :3]) == (100, 50, 50)          # SQLite cannot parse two of the four dates
assert tuple(int(v) for v in recon_raw) == (100, 70, 30)               # pandas parses '2024-1-6' but not '06/02/2024'
print("\npandas equals SQL on suspects 1, 2, 3, 5 and both reconciliations on orders: OK; suspect 4 differs by design (see below)")
print("\npandas:")
print(" S1 <= Timestamp('2024-01-31'):", int(p1_bad.sum()), "| half-open:", int(p1_ok.sum()), "| .loc['2024-01-01':'2024-01-31']:", int(p1_slice.sum()))
print(" S2 monthly totals reindexed with fill_value=0:", filled.to_dict())
print(" S3 India-time months:", ist_month.to_dict())
print(" S4 parsed dates (errors='coerce', format='ISO8601'):", raw["d"].astype(str).tolist())
print(" S4 groupby months:", raw_month.to_dict(), "| with dropna=False:", raw_month_na.to_dict())
print(" S5 merge then sum:", int(fan), "| without the merge:", int(ok5))
print(" reconciliation orders:", tuple(int(v) for v in recon), "| raw_orders:", tuple(int(v) for v in recon_raw))
```

**Output (my run):**
```text
--- S1 BETWEEN '2024-01-01' AND '2024-01-31' (loses 31 Jan after 00:00)
 jan
 100
--- S1 half-open range
 jan
 190
--- S2 LAG without spine (March compared with January)
  month  total prev_month  prev_total
2024-01    190        NaN         NaN
2024-03    100    2024-01       190.0
2024-04     20    2024-03       100.0
--- S2 with spine
  month  total  prev_total
2024-01    190         NaN
2024-02      0       190.0
2024-03    100         0.0
2024-04     20       100.0
--- S3 UTC month
  month  total
2024-01    190
2024-03    100
2024-04     20
--- S3 India-time month
  month  total
2024-01    150
2024-02     40
2024-03     70
2024-04     50
--- S4 text sort: ['06/02/2024', '2024-01-05', '2024-02-07', '2024-1-6']
--- S4 strftime on mixed formats (NULL month = silently unassigned)
  month  total
    NaN     50
2024-01     10
2024-02     40
--- S5 INNER JOIN to order_items before SUM (multiplies orders 1 and 2, drops orders without items)
 total
   470
--- S5 pre-aggregate the many side first
 total
   310
--- S5b partial month as of 2024-04-15
  month  total  days_covered
2024-04     20            15
--- RECONCILIATION on orders (India-time months)
 overall  sum_of_months  diff  unparsed_buckets
     310            310     0                 0
--- RECONCILIATION on raw_orders (mixed formats)
 overall  sum_of_months  diff
     100             50    50

pandas equals SQL on suspects 1, 2, 3, 5 and both reconciliations on orders: OK; suspect 4 differs by design (see below)

pandas:
 S1 <= Timestamp('2024-01-31'): 100 | half-open: 190 | .loc['2024-01-01':'2024-01-31']: 190
 S2 monthly totals reindexed with fill_value=0: {Period('2024-01', 'M'): 190, Period('2024-02', 'M'): 0, Period('2024-03', 'M'): 100, Period('2024-04', 'M'): 20}
 S3 India-time months: {'2024-01': 150, '2024-02': 40, '2024-03': 70, '2024-04': 50}
 S4 parsed dates (errors='coerce', format='ISO8601'): ['2024-01-05', '2024-01-06', nan, '2024-02-07']
 S4 groupby months: {'2024-01': 30, '2024-02': 40} | with dropna=False: {'2024-01': 30, '2024-02': 40, nan: 30}
 S5 merge then sum: 470 | without the merge: 310
 reconciliation orders: (310, 310, 0) | raw_orders: (100, 70, 30)
```

**Edge cases:**
- The reconciliation catches lost or inflated rows (suspects 1, 4, 5) but not a shifted month (suspect 3, the sums still match) or a missing spine month (suspect 2); those need their own checks (compare the month list with the calendar, compare against a second source).
- Pandas partial-string slicing includes the whole last day (`.loc['2024-01-01':'2024-01-31']` gave 190), unlike `<= Timestamp('2024-01-31')` (100). That is a pandas versus plain comparison difference worth knowing.
- `groupby` on NaT keys drops them by default (the dropped 30 reappears with `dropna=False`); a SQL `GROUP BY` keeps the NULL group. The two tools fail differently.
- `fill_value=0` on `reindex` creates the zero months in pandas (the equivalent of the spine).
- Fixed as-of date: the partial-month flag compares the as-of day with the days in the month; with `now` the report changes on each run.
- The tz conversion used `Asia/Kolkata`, which has no DST; a zone with DST needs the offset table or a library (Q38).

**Then explain:**
- Order of suspicion: cheap and common first. Boundary filters and text dates produce silent row loss; the spine and the zone produce correct totals in the wrong months; fan-out produces a total that is too large.
- Reconcile first, localise second: if the monthly sum equals the overall total, rows are not lost or duplicated in the aggregation, and the problem is assignment (month, zone).
- State the grain of each table before joining; aggregate the many side first.
- Keep an explicit bucket for rows that do not parse so that they show up instead of disappearing.

**Follow-ups:**
- How would you prove a fix? Re-run the reconciliation, then compare to an independent total (finance ledger, raw table counts).
- How do you prevent the bug? Constraints and checks on load (date format, uniqueness), tests on reconciliation, a calendar table.
- What if the report is MoM? Complete the spine before `LAG` and compare like for like (partial months excluded).

**Common mistakes:**
- Trusting a report because the total looks plausible.
- Fixing one suspect and not re-reconciling.
- Using `BETWEEN` for timestamps, and `LAG` on sparse months.
- Ignoring NULL groups and dropped NaT keys.
