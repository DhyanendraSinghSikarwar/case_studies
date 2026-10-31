# Book 3 — Part 8: Funnels, conversion, DAU/MAU and product metrics in SQL, with pandas equivalents

**Topic:** the SQL of product and business metrics: funnel step counts with COUNT(DISTINCT user), strict versus any-order funnels, time-window funnels, step-to-step and overall conversion, drop-off by channel, cohort and device, first occurrence per step with MIN(CASE), skipped steps and repeated events; DAU, WAU and MAU at fixed as-of dates, stickiness and rolling 30-day active users with a date spine; activation rate, experiment-arm conversion tables and sample ratio mismatch as counts; first-touch, last-touch, linear and time-decay attribution; GMV, AOV, ARPU, ARPPU, LTV to date, repeat purchase rate, refund and cancellation rate, take rate and net revenue without fan-out; share of total and growth contribution; marketplace, search, notification and engagement metrics; metric-definition traps, dashboard reconciliation, KPI tables in one query; and the pandas counterparts (groupby, nunique, pivot_table, crosstab(normalize=), value_counts(normalize=), merge-based funnels, cumulative funnels, rolling distinct actives through a spine).
**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 18, ⭐⭐ 16, ⭐ 11)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers the SQL (and pandas) of metrics. Metric design and product sense belong to Book 6, A/B-test statistics (p-values, power, confidence intervals) to Books 1 and 6, retention and cohort tables to Part 6, sessionization and streaks to Part 7, ranking mechanics to Part 4, running totals to Part 5, and scalar subqueries and CTE style to Part 3; questions here point to those parts instead of repeating them. Every question states its tables so Wave B can build sample data; timestamps are ISO text, 'as of' dates are fixed and never CURRENT_DATE, and in SQLite 7-day and 30-day arithmetic should use datetime(x, '+7 days') or unixepoch, not julianday times a constant.

Evidence limits: no candidate-reported SQL questions were found. Sources are guides, vendor posts, practice-site material and documentation (PracHub funnel case, Basedash active-user pitfalls, letsdatascience e-commerce list, LearnSQL metrics article, StrataScratch blog, doocs LeetCode 1174, pandas pivot_table and crosstab reference; all opened) plus search snippets (LeetCode mirrors for 1633 and 262, attribution, SRM, search-analytics and ClickHouse DAU pages). leetcode.com pages were not opened. 'Asked at' tags are source types, not company reports. Engine notes (SQLite 3.45.1): no MEDIAN, no PIVOT, no DATE_TRUNC and no generate_series by default (use recursive CTEs for date spines); other engines are hedged as not executed.

---

### Q1 ⭐⭐⭐ 🟢 DAU, WAU and MAU with fixed as-of dates: events(user_id, event_ts, event_name) with ISO text timestamps and users(user_id, signup_date, country, is_test). For the as-of date 2024-03-31 return DAU (distinct users with any event on that date), WAU (distinct users in the 7 days ending that date, inclusive) and MAU (distinct users in the 30 days ending that date, inclusive), excluding is_test = 1 users. Explain why every one of these is COUNT(DISTINCT user_id) and not COUNT(*), why the as-of date is a parameter and never CURRENT_DATE, and what the window boundaries are (a 7-day window is as-of minus 6 days through as-of).
**Asked at:** active-user guides: Basedash DAU/WAU/MAU pitfalls article (opened; active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users) plus search snippets of oneuptime ClickHouse DAU/WAU/MAU and stickiness posts and Swace and pmtoolkit pages (not opened); guides, not candidate reports; product analytics and data scientist rounds at social, streaming and SaaS companies
**Say this first (1 line):** DAU, WAU and MAU are each a distinct-user count over a window ending at the as-of date (1, 7 and 30 days, inclusive of the as-of day), so I use `COUNT(DISTINCT user_id)` with the as-of date as a parameter, and I assume UTC timestamps, no week start (WAU is a rolling 7 days, not a calendar week) and test users removed.

**Conventions I state before writing anything:** as-of date 2024-03-31 is a parameter, never `CURRENT_DATE`, so the report can be re-run and reconciled. A "day" is the UTC date of the stored timestamp text (if the business runs on IST I convert first, see Q19 and Q36 in this part for the time-zone cases). WAU is the 7 days ending on the as-of date, so it starts on as-of minus 6 days (2024-03-25) and MAU starts on as-of minus 29 days (2024-03-02); this is a trailing window, so there is no week-start question, but if someone asks for the calendar week I ask whether it starts Monday or Sunday. "Active" means any event; a stricter definition (an intent event only) is a one-line `WHERE` change. Test users are excluded with `is_test = 0`. This schema has no bot flag, so bots are not filtered here; if a user-agent column or bot list exists it is excluded in the same place as test users (see Q37). Events whose user is missing from `users` drop out of the inner join; I would count them separately before trusting the number.

**Schema and sample data:** seven real users and one test user. User 1 has four events (three on the as-of day, one on 03-29). User 4 is active only on 03-24 at 23:59:59 (one second outside the 7-day window). User 6 is active at 2024-03-01 23:59:59 (one second outside the 30-day window). User 5 is active at 2024-03-02 00:00:00 (the first instant inside it). User 7 has an event on 2024-04-01, after the as-of date. One event has a NULL `user_id`.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-20','IN',0),(3,'2024-02-01','US',0),
 (4,'2024-02-10','IN',0),(5,'2024-02-15','IN',0),(6,'2024-02-20','IN',0),
 (7,'2024-03-01','US',0),(99,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-31 00:05:00','open'),(1,'2024-03-31 09:00:00','click'),(1,'2024-03-31 23:59:59','click'),
 (2,'2024-03-31 10:00:00','open'),
 (3,'2024-03-25 08:00:00','open'),
 (4,'2024-03-24 23:59:59','open'),
 (5,'2024-03-02 00:00:00','open'),
 (6,'2024-03-01 23:59:59','open'),
 (7,'2024-04-01 00:00:00','open'),
 (99,'2024-03-31 12:00:00','open'),
 (NULL,'2024-03-31 12:30:00','open'),
 (1,'2024-03-29 10:00:00','open');
```

**SQL answer:** `SQL_MAIN` in the Code block. One scan, three conditional distinct counts, half-open windows `[start, as_of + 1 day)` so the whole as-of day is included whatever its time of day:
```sql
SELECT
  COUNT(DISTINCT CASE WHEN e.event_ts >= :as_of
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS dau,
  COUNT(DISTINCT CASE WHEN e.event_ts >= date(:as_of, '-6 days')
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS wau,
  COUNT(DISTINCT CASE WHEN e.event_ts >= date(:as_of, '-29 days')
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS mau
FROM events e
JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
```

**pandas answer:** same logic, shown once and identical to the Code block:
```py
e = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
ts = pd.to_datetime(e["event_ts"])
end = pd.Timestamp(AS_OF) + pd.Timedelta(days=1)

def active(days):
    in_win = (ts >= end - pd.Timedelta(days=days)) & (ts < end)
    return e.loc[in_win, "user_id"].nunique()

pd_df = pd.DataFrame({"dau": [active(1)], "wau": [active(7)], "mau": [active(30)]})
```

**Example:** non-test events in the windows.
- DAU (03-31): users 1 (three events) and 2. User 99 is test, the NULL-user event never joins. DAU = 2.
- WAU (03-25 to 03-31): add user 3 (03-25) and user 1's 03-29 event (user 1 is already counted). User 4 at 03-24 23:59:59 is one second out. WAU = 3.
- MAU (03-02 to 03-31): add user 4 (03-24) and user 5 (03-02 00:00:00, first instant in). User 6 (03-01 23:59:59) is out, user 7 (04-01) is after the as-of date. MAU = 5.
- `COUNT(*)` instead of `COUNT(DISTINCT)` gives 4 for DAU (user 1 has three events) and 6 for WAU, which is why it is the wrong tool: it measures events, not people.

**Code:** run with `python3 -I`. One row each side; the assert compares the two one-row frames.
```python
# Q1: DAU, WAU, MAU at a fixed as-of date with COUNT(DISTINCT user_id), SQL and pandas
import sqlite3
import pandas as pd

AS_OF = "2024-03-31"
SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-20','IN',0),(3,'2024-02-01','US',0),
 (4,'2024-02-10','IN',0),(5,'2024-02-15','IN',0),(6,'2024-02-20','IN',0),
 (7,'2024-03-01','US',0),(99,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-31 00:05:00','open'),(1,'2024-03-31 09:00:00','click'),(1,'2024-03-31 23:59:59','click'),
 (2,'2024-03-31 10:00:00','open'),
 (3,'2024-03-25 08:00:00','open'),
 (4,'2024-03-24 23:59:59','open'),
 (5,'2024-03-02 00:00:00','open'),
 (6,'2024-03-01 23:59:59','open'),
 (7,'2024-04-01 00:00:00','open'),
 (99,'2024-03-31 12:00:00','open'),
 (NULL,'2024-03-31 12:30:00','open'),
 (1,'2024-03-29 10:00:00','open');
"""
# window = [start, as_of + 1 day), half-open on timestamps; start = as_of - (N-1) days
SQL_MAIN = """
SELECT
  COUNT(DISTINCT CASE WHEN e.event_ts >= :as_of
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS dau,
  COUNT(DISTINCT CASE WHEN e.event_ts >= date(:as_of, '-6 days')
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS wau,
  COUNT(DISTINCT CASE WHEN e.event_ts >= date(:as_of, '-29 days')
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS mau
FROM events e
JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
"""
SQL_COUNT_STAR = """
SELECT
  COUNT(CASE WHEN e.event_ts >= :as_of AND e.event_ts < date(:as_of, '+1 day') THEN 1 END) AS dau_rows,
  COUNT(CASE WHEN e.event_ts >= date(:as_of, '-6 days') AND e.event_ts < date(:as_of, '+1 day') THEN 1 END) AS wau_rows
FROM events e JOIN users u ON u.user_id = e.user_id WHERE u.is_test = 0
"""
# wrong boundary: BETWEEN on a date string against timestamp text drops the as-of day itself
SQL_BETWEEN = """
SELECT COUNT(DISTINCT e.user_id) AS dau_between
FROM events e JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0 AND e.event_ts BETWEEN :as_of AND :as_of
"""
SQL_WHO = """
SELECT e.user_id, MIN(e.event_ts) AS first_in_window, COUNT(*) AS rows_in_window
FROM events e JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0 AND e.event_ts >= date(:as_of, '-29 days') AND e.event_ts < date(:as_of, '+1 day')
GROUP BY e.user_id ORDER BY e.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
p = {"as_of": AS_OF}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=p)
print("SQL DAU/WAU/MAU as of", AS_OF)
print(sql_df.to_string(index=False))
print("COUNT(*) instead of DISTINCT:", con.execute(SQL_COUNT_STAR, p).fetchone())
print("BETWEEN as_of AND as_of (wrong, text timestamps):", con.execute(SQL_BETWEEN, p).fetchone())
print(pd.read_sql_query(SQL_WHO, con, params=p).to_string(index=False))
pa = {"a": AS_OF}
print("window starts: date() says", con.execute("SELECT date(:a,'-6 days'), date(:a,'-29 days')", pa).fetchone(),
      "| unixepoch says", con.execute(
          "SELECT date(unixepoch(:a) - 6*86400, 'unixepoch'), date(unixepoch(:a) - 29*86400, 'unixepoch')", pa).fetchone())

events = pd.read_sql_query("SELECT * FROM events", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
e = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
ts = pd.to_datetime(e["event_ts"])
end = pd.Timestamp(AS_OF) + pd.Timedelta(days=1)

def active(days):
    in_win = (ts >= end - pd.Timedelta(days=days)) & (ts < end)
    return e.loc[in_win, "user_id"].nunique()

pd_df = pd.DataFrame({"dau": [active(1)], "wau": [active(7)], "mau": [active(30)]})
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # one row, same columns
print("asserts passed")

# NULL user_id: SQL COUNT(DISTINCT) and pandas nunique both skip it; len(set()) does not
print("events with NULL user_id:", int(events["user_id"].isna().sum()),
      "| nunique:", events["user_id"].nunique(),
      "| len(set(...)):", len(set(events["user_id"])),
      "| SQL COUNT(DISTINCT):", con.execute("SELECT COUNT(DISTINCT user_id) FROM events").fetchone()[0])
# a window with nobody in it: counts are 0, not NULL
print("empty day:", con.execute(SQL_MAIN, {"as_of": "2023-01-01"}).fetchone())
```

**Output (my run):**
```text
SQL DAU/WAU/MAU as of 2024-03-31
 dau  wau  mau
   2    3    5
COUNT(*) instead of DISTINCT: (4, 6)
BETWEEN as_of AND as_of (wrong, text timestamps): (0,)
 user_id     first_in_window  rows_in_window
       1 2024-03-29 10:00:00               4
       2 2024-03-31 10:00:00               1
       3 2024-03-25 08:00:00               1
       4 2024-03-24 23:59:59               1
       5 2024-03-02 00:00:00               1
window starts: date() says ('2024-03-25', '2024-03-02') | unixepoch says ('2024-03-25', '2024-03-02')
pandas:
 dau  wau  mau
   2    3    5
asserts passed
events with NULL user_id: 1 | nunique: 8 | len(set(...)): 9 | SQL COUNT(DISTINCT): 8
empty day: (0, 0, 0)
```

**Edge cases:**
- Boundaries: `BETWEEN :as_of AND :as_of` on timestamp text returned 0 in my run, because `'2024-03-31 10:00:00'` sorts after `'2024-03-31'`. Use `>= as_of` and `< as_of + 1 day` (half-open) on timestamp columns.
- Date arithmetic: `date(:as_of, '-6 days')` and `date(unixepoch(:as_of) - 6*86400, 'unixepoch')` both gave 2024-03-25, and both gave 2024-03-02 for 29 days, in my run. Either works for whole days; never multiply `julianday` by a constant for sub-day windows (Part 7 Q11).
- NULL `user_id`: `COUNT(DISTINCT)` and pandas `nunique()` both skip it (8 and 8 in my run), but `len(set(...))` counted the NaN as a value (9). In pandas, NaN ids merge to nothing here because `users` has none.
- A window with no events returns 0, not NULL, because `COUNT(DISTINCT ...)` of nothing is 0 (my run printed `(0, 0, 0)` for 2023-01-01).
- Incomplete as-of day: if the pipeline has not finished loading 03-31, the DAU is understated. Fix the as-of to the last complete day.
- Test users with `is_test` NULL fail `= 0` and vanish; decide whether NULL means real and use `COALESCE(is_test, 0) = 0` if so.

**Then explain:**
- A user is a person; an event is an action. DAU, WAU and MAU count people, so every one is `COUNT(DISTINCT user_id)`, and a heavy user must count once however many events they fire.
- The as-of date is a parameter so the number is reproducible: run it tomorrow for the same date and get the same answer (late data aside). `CURRENT_DATE` makes yesterday's report change under you and makes tests impossible.
- A 7-day window ending on D inclusive starts on D minus 6; a 30-day window starts on D minus 29. Using minus 7 or minus 30 silently gives an 8-day or 31-day window.
- WAU is at most MAU and DAU is at most WAU by construction, which is a cheap sanity check on any dashboard.
- Dialects (not executed here): PostgreSQL would use `COUNT(DISTINCT user_id) FILTER (WHERE ...)` and `event_ts >= DATE '2024-03-31' - 6`; BigQuery `COUNT(DISTINCT IF(...))` or `COUNTIF` for non-distinct; MySQL `DATE_SUB(:as_of, INTERVAL 6 DAY)`.

**Follow-ups:**
- Calendar-month MAU instead of trailing 30 days? Window `[month_start, next_month_start)`; the two differ (Q15).
- DAU for every day of a month? Needs a date spine so zero days appear (Q15, Q33).
- Why not sum DAU over 7 days to get WAU? Because one person active on three days is counted three times; distinct counts are not additive.

**Common mistakes:**
- `COUNT(*)` (events) instead of `COUNT(DISTINCT user_id)`.
- `BETWEEN '2024-03-25' AND '2024-03-31'` on timestamp text, which drops most of the last day.
- Off-by-one windows (7 days ending D starting D minus 7).
- `CURRENT_DATE` in the query.
- Forgetting test users, or joining with a LEFT JOIN so orphan events inflate the count.
- Summing daily distinct counts to get a weekly number.

### Q2 ⭐⭐⭐ 🟢 Funnel step counts with COUNT(DISTINCT user): events(user_id, event_ts, event_name) with event_name in ('view', 'cart', 'purchase'). Return one row per step (view, cart, purchase) with users reaching that step at least once, the step-to-step conversion (cart over view, purchase over cart) and the overall conversion (purchase over view), as percentages rounded to 1 decimal. Use conditional aggregation in a single scan, say why COUNT(*) is wrong when users repeat events, and state what this any-order version does NOT check.
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** One scan with `COUNT(DISTINCT CASE WHEN event_name = ... THEN user_id END)` per step gives users per step; step-to-step conversion is each step over the previous one, overall conversion is each step over view users, and this any-order version only checks that a user did each thing at least once, not in order, not within a window, and not that they passed the earlier step.

**Schema and sample data:** eight users. User 1 views twice. User 4 carts twice and purchases twice. User 5 purchases with no view or cart (express checkout or a tracking gap). User 6 carts before viewing (an order violation). User 7 only views, three times.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:01:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),
 (3,'2024-03-01 12:00:00','view'),
 (4,'2024-03-02 09:00:00','view'),(4,'2024-03-02 09:05:00','cart'),(4,'2024-03-02 09:06:00','cart'),
 (4,'2024-03-02 09:10:00','purchase'),(4,'2024-03-02 09:11:00','purchase'),
 (5,'2024-03-02 13:00:00','purchase'),
 (6,'2024-03-02 14:00:00','cart'),(6,'2024-03-02 14:05:00','view'),(6,'2024-03-02 14:10:00','purchase'),
 (7,'2024-03-03 08:00:00','view'),(7,'2024-03-03 08:01:00','view'),(7,'2024-03-03 08:02:00','view'),
 (8,'2024-03-03 15:00:00','view'),(8,'2024-03-03 15:05:00','cart');
```

**SQL answer:** `SQL_MAIN` in the Code block. The `s` CTE is the single scan; the three-row result is built from it. `NULLIF` guards a zero denominator.
```sql
WITH s AS (
  SELECT COUNT(DISTINCT CASE WHEN event_name = 'view'     THEN user_id END) AS v,
         COUNT(DISTINCT CASE WHEN event_name = 'cart'     THEN user_id END) AS c,
         COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS p
  FROM events
)
SELECT 'view' AS step, 1 AS step_no, v AS users,
       NULL AS step_conv_pct, ROUND(100.0 * v / NULLIF(v, 0), 1) AS overall_conv_pct FROM s
UNION ALL
SELECT 'cart', 2, c, ROUND(100.0 * c / NULLIF(v, 0), 1), ROUND(100.0 * c / NULLIF(v, 0), 1) FROM s
UNION ALL
SELECT 'purchase', 3, p, ROUND(100.0 * p / NULLIF(c, 0), 1), ROUND(100.0 * p / NULLIF(v, 0), 1) FROM s
ORDER BY step_no
```

**pandas answer:** shown once, identical to the Code block:
```py
steps = ["view", "cart", "purchase"]
users = events.groupby("event_name")["user_id"].nunique().reindex(steps, fill_value=0)
pd_df = pd.DataFrame({"step": steps, "step_no": [1, 2, 3], "users": users.to_numpy()})
prev = pd_df["users"].shift(1)
pd_df["step_conv_pct"] = (100.0 * pd_df["users"] / prev).round(1)
pd_df["overall_conv_pct"] = (100.0 * pd_df["users"] / pd_df["users"].iloc[0]).round(1)
```

**Example:** users per step, any order.
- View: users 1, 2, 3, 4, 6, 7, 8 = 7 (user 5 never viewed).
- Cart: users 1, 2, 4, 6, 8 = 5.
- Purchase: users 1, 4, 5, 6 = 4.
- Cart over view = 5/7 = 71.4%. Purchase over cart = 4/5 = 80.0%. Overall = 4/7 = 57.1%.
- Counting rows gives 10 views, 6 carts and 5 purchases: cart over view 60.0%, purchase over cart 83.3%, overall 50.0%. Every one of those is wrong, because users 1, 4 and 7 repeat events.

**Code:** run with `python3 -I`. Rows are in step order (view, cart, purchase) on both sides; the missing first step conversion is NULL in SQL and NaN in pandas, which `assert_frame_equal` treats as equal.
```python
# Q2: funnel step counts with COUNT(DISTINCT user) in one scan, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:01:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),
 (3,'2024-03-01 12:00:00','view'),
 (4,'2024-03-02 09:00:00','view'),(4,'2024-03-02 09:05:00','cart'),(4,'2024-03-02 09:06:00','cart'),
 (4,'2024-03-02 09:10:00','purchase'),(4,'2024-03-02 09:11:00','purchase'),
 (5,'2024-03-02 13:00:00','purchase'),
 (6,'2024-03-02 14:00:00','cart'),(6,'2024-03-02 14:05:00','view'),(6,'2024-03-02 14:10:00','purchase'),
 (7,'2024-03-03 08:00:00','view'),(7,'2024-03-03 08:01:00','view'),(7,'2024-03-03 08:02:00','view'),
 (8,'2024-03-03 15:00:00','view'),(8,'2024-03-03 15:05:00','cart');
"""
SQL_MAIN = """
WITH s AS (
  SELECT COUNT(DISTINCT CASE WHEN event_name = 'view'     THEN user_id END) AS v,
         COUNT(DISTINCT CASE WHEN event_name = 'cart'     THEN user_id END) AS c,
         COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS p
  FROM events
)
SELECT 'view' AS step, 1 AS step_no, v AS users,
       NULL AS step_conv_pct, ROUND(100.0 * v / NULLIF(v, 0), 1) AS overall_conv_pct FROM s
UNION ALL
SELECT 'cart', 2, c, ROUND(100.0 * c / NULLIF(v, 0), 1), ROUND(100.0 * c / NULLIF(v, 0), 1) FROM s
UNION ALL
SELECT 'purchase', 3, p, ROUND(100.0 * p / NULLIF(c, 0), 1), ROUND(100.0 * p / NULLIF(v, 0), 1) FROM s
ORDER BY step_no
"""
# wrong: count events, not users
SQL_ROWS = """
SELECT event_name, COUNT(*) AS event_rows, COUNT(DISTINCT user_id) AS users
FROM events GROUP BY event_name ORDER BY CASE event_name WHEN 'view' THEN 1 WHEN 'cart' THEN 2 ELSE 3 END
"""
# what the any-order version cannot see
SQL_CHECK = """
SELECT user_id,
       MAX(event_name = 'view') AS has_view, MAX(event_name = 'cart') AS has_cart, MAX(event_name = 'purchase') AS has_purchase
FROM events GROUP BY user_id
HAVING MAX(event_name = 'purchase') = 1 AND (MAX(event_name = 'cart') = 0 OR MAX(event_name = 'view') = 0)
ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL funnel (users, any order):")
print(sql_df.to_string(index=False))
rows_df = pd.read_sql_query(SQL_ROWS, con)
print(rows_df.to_string(index=False))
r = rows_df.set_index("event_name")["event_rows"]
print("wrong, rows: cart/view %.1f  purchase/cart %.1f  overall %.1f" % (
    100 * r["cart"] / r["view"], 100 * r["purchase"] / r["cart"], 100 * r["purchase"] / r["view"]))
print("purchasers without a cart or a view event:")
print(pd.read_sql_query(SQL_CHECK, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
steps = ["view", "cart", "purchase"]
users = events.groupby("event_name")["user_id"].nunique().reindex(steps, fill_value=0)
pd_df = pd.DataFrame({"step": steps, "step_no": [1, 2, 3], "users": users.to_numpy()})
prev = pd_df["users"].shift(1)
pd_df["step_conv_pct"] = (100.0 * pd_df["users"] / prev).round(1)
pd_df["overall_conv_pct"] = (100.0 * pd_df["users"] / pd_df["users"].iloc[0]).round(1)
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
# compare after ordering by step_no (already in that order); NULL and NaN both read as NaN
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("asserts passed")

# rounding probe: SQLite ROUND rounds half away from zero, Python and numpy round half to even
print("probe ROUND(6.25,1), ROUND(2.5), ROUND(-2.5):", con.execute("SELECT ROUND(6.25,1), ROUND(2.5), ROUND(-2.5)").fetchone())
import numpy as np
print("probe python round(6.25,1), round(2.5), round(-2.5):", round(6.25, 1), round(2.5), round(-2.5),
      "| numpy:", np.round(6.25, 1), np.round(2.5), np.round(-2.5),
      "| pandas Series.round:", pd.Series([6.25]).round(1).iloc[0])
# empty table: NULLIF makes every rate NULL instead of an error
con.execute("DELETE FROM events")
print("empty table:", con.execute(SQL_MAIN).fetchall())
```

**Output (my run):**
```text
SQL funnel (users, any order):
    step  step_no  users  step_conv_pct  overall_conv_pct
    view        1      7            NaN             100.0
    cart        2      5           71.4              71.4
purchase        3      4           80.0              57.1
event_name  event_rows  users
      view          10      7
      cart           6      5
  purchase           5      4
wrong, rows: cart/view 60.0  purchase/cart 83.3  overall 50.0
purchasers without a cart or a view event:
 user_id  has_view  has_cart  has_purchase
       5         0         0             1
pandas:
    step  step_no  users  step_conv_pct  overall_conv_pct
    view        1      7            NaN             100.0
    cart        2      5           71.4              71.4
purchase        3      4           80.0              57.1
asserts passed
probe ROUND(6.25,1), ROUND(2.5), ROUND(-2.5): (6.3, 3.0, -3.0)
probe python round(6.25,1), round(2.5), round(-2.5): 6.2 2 -2 | numpy: 6.2 2.0 -2.0 | pandas Series.round: 6.2
empty table: [('view', 1, 0, None, None), ('cart', 2, 0, None, None), ('purchase', 3, 0, None, None)]
```

**Edge cases:**
- Honest weakness of the any-order version: the 80.0% purchase over cart is contaminated. User 5 purchased without carting, so the 4 purchasers include someone who is not among the 5 carters. Only users 1, 4 and 6 are carters who purchased, which is 3 of 5, or 60.0%. The cumulative fix is Q9 and Q35; the ordered fix is Q7.
- Order is not checked: user 6 carted before viewing and still counts in all three steps.
- No time window: a view in January and a purchase in March count as one converted user.
- Empty table: every `COUNT(DISTINCT ...)` is 0 and `NULLIF` turns the rates into NULL, not a division error (my run printed all NULL rates).
- Rounding: SQLite `ROUND` rounds half away from zero, Python, numpy and pandas `round` round half to even. In my run `ROUND(6.25,1)` gave 6.3 but Python `round(6.25, 1)` and `Series.round(1)` gave 6.2. The sample percentages here are not ties, so the assert passes, but a real tie would differ between the two engines.
- The funnel is only as good as the event names: a renamed event shows up as a sudden drop.

**Then explain:**
- `COUNT(*)` counts events, so a user who views five times counts five times and any step with more repeaters looks bigger. Distinct users is the funnel unit.
- Conditional aggregation computes all steps in one pass over `events`; the alternative of one subquery per step scans the table three times.
- Step-to-step shows where people drop; overall shows how many of the top of the funnel got to the end. Report both with the counts, not only the percentages.
- What it does not check: order, a time window, that earlier steps happened for the same user, session boundaries, and duplicate tracking events.
- Dialects (not executed here): BigQuery `COUNT(DISTINCT IF(event_name = 'view', user_id, NULL))`; PostgreSQL `COUNT(DISTINCT user_id) FILTER (WHERE event_name = 'view')`.

**Follow-ups:**
- Make it ordered? First-of-each or chained timestamps (Q7).
- Add a time window? Q17 (7 days after the first view).
- Per channel? Q8.

**Common mistakes:**
- `COUNT(*)` for steps (60.0, 83.3 and 50.0 above).
- Dividing by the wrong step (overall over the previous step).
- Treating this as a proper funnel when it is a presence table.
- Integer division: `c / v` in SQLite is integer division when both are integers; multiply by `100.0` first.
- Rounding before dividing, or comparing rounded percentages in tests.

### Q3 ⭐⭐⭐ 🟢 Denominator choice for conversion rate: users(user_id, signup_date, is_test) and orders(order_id, user_id, order_ts, amount, status) with status in ('completed', 'cancelled'). The product team asks for 'the paid conversion rate'. Compute three versions side by side: (a) users with at least one completed order over all non-test signups, (b) completed orders over all orders, (c) users with a completed order within 30 days of signup over signups at least 30 days old at the as-of date 2024-06-30. Show that all three differ on the same data, say which one answers what, and explain why a user-level numerator over an order-level denominator is a bug.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** There is no single paid conversion rate: I ask whether the numerator is users or orders, whether the denominator is all signups or a mature cohort, and over what window, then show (a) users with a completed order over non-test signups, (b) completed orders over orders, and (c) users who paid within 30 days of signup over signups old enough to have had 30 days, and the three differ.

**Clarifying questions and assumptions:** which population (non-test users only)? Does "paid" mean a completed order (cancelled does not count)? Is the denominator everyone who ever signed up, or only users whose window has finished? What window (ever, or 30 days after signup, days 0 to 30 inclusive)? As-of date fixed at 2024-06-30, and I assume data is complete through the end of that day. Time zone: dates are the stored dates; no conversion.

**Schema and sample data:** nine users, one is a test user (user 8, with a 500 order that must not leak in), user 6 signed up on 2024-06-10 (immature), user 9 signed up on 2024-05-31 (exactly 30 days before the as-of date, so mature, and paid on day 30). User 1 has several orders; user 7 never ordered.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-10',0),(2,'2024-02-01',0),(3,'2024-03-15',0),(4,'2024-04-01',0),
 (5,'2024-05-20',0),(6,'2024-06-10',0),(7,'2024-02-20',0),(8,'2024-01-05',1),(9,'2024-05-31',0);
INSERT INTO orders VALUES
 (101,1,'2024-01-12 10:00:00',100,'completed'),
 (102,1,'2024-04-02 10:00:00',50,'completed'),
 (103,1,'2024-04-03 10:00:00',70,'cancelled'),
 (104,2,'2024-04-15 10:00:00',80,'completed'),
 (105,3,'2024-03-20 10:00:00',60,'cancelled'),
 (106,3,'2024-03-25 10:00:00',90,'cancelled'),
 (107,4,'2024-04-20 10:00:00',40,'completed'),
 (108,4,'2024-04-21 10:00:00',40,'completed'),
 (109,5,'2024-06-05 10:00:00',55,'completed'),
 (110,6,'2024-06-12 10:00:00',30,'completed'),
 (111,8,'2024-01-06 10:00:00',500,'completed'),
 (113,1,'2024-05-01 10:00:00',25,'completed'),
 (114,9,'2024-06-30 15:00:00',35,'completed'),
 (115,9,'2024-06-02 10:00:00',20,'cancelled');
```

**SQL answer:** `SQL_MAIN` in the Code block, three scalar results side by side from CTEs that already exclude test users. The maturity rule is `signup_date <= date(:as_of, '-30 days')`, so the 30-day window has fully elapsed.
```sql
WITH nt AS (SELECT user_id, signup_date FROM users WHERE is_test = 0),
o AS (SELECT o.* FROM orders o JOIN nt ON nt.user_id = o.user_id),
mature AS (SELECT * FROM nt WHERE signup_date <= date(:as_of, '-30 days'))
SELECT
  ROUND(100.0 * (SELECT COUNT(DISTINCT user_id) FROM o WHERE status = 'completed')
        / (SELECT COUNT(*) FROM nt), 1) AS a_users_over_signups,
  ROUND(100.0 * (SELECT COUNT(*) FROM o WHERE status = 'completed')
        / (SELECT COUNT(*) FROM o), 1) AS b_orders_over_orders,
  ROUND(100.0 * (SELECT COUNT(*) FROM mature m WHERE EXISTS (
          SELECT 1 FROM o WHERE o.user_id = m.user_id AND o.status = 'completed'
            AND date(o.order_ts) >= m.signup_date
            AND date(o.order_ts) <= date(m.signup_date, '+30 days')))
        / (SELECT COUNT(*) FROM mature), 1) AS c_30d_window_mature
```
The bug query `SQL_BUG` in the Code block divides a user count by an order count (and an order count by a user count) to show what the mixed-grain versions give.

**pandas answer:** shown once, identical to the Code block:
```py
nt = users[users["is_test"] == 0]
o = orders.merge(nt[["user_id", "signup_date"]], on="user_id")
done = o[o["status"] == "completed"]
a = 100.0 * done["user_id"].nunique() / len(nt)
b = 100.0 * len(done) / len(o)
mature = nt[pd.to_datetime(nt["signup_date"]) <= pd.Timestamp(AS_OF) - pd.Timedelta(days=30)]
d = done.merge(mature[["user_id"]], on="user_id")
day = pd.to_datetime(d["order_ts"]).dt.normalize()
sign = pd.to_datetime(d["signup_date"])
hit = d[(day >= sign) & (day <= sign + pd.Timedelta(days=30))]
c = 100.0 * hit["user_id"].nunique() / len(mature)
pd_df = pd.DataFrame({"a_users_over_signups": [round(a, 1)], "b_orders_over_orders": [round(b, 1)],
                      "c_30d_window_mature": [round(c, 1)]})
```

**Example:** non-test users are 1 to 7 and 9 (8 users); 13 non-test orders, 9 completed.
- (a) Users with a completed order: 1, 2, 4, 5, 6, 9 = 6 of 8 = 75.0%.
- (b) Completed orders 9 of 13 = 69.2%.
- (c) Mature users (signup on or before 2024-05-31): 1, 2, 3, 4, 5, 7, 9 = 7 (user 6 is excluded as immature). Paid within 30 days: user 1 (01-12, day 2), user 4 (04-20, day 19), user 5 (06-05, day 16), user 9 (06-30, day 30, inclusive) = 4 of 7 = 57.1%. User 2 paid on day 74, too late.
- Bug: 6 users over 13 orders = 46.2%, which answers no question; completed orders over users = 9/8 = 112.5%, a "conversion" above 100%.

**Code:** run with `python3 -I`. The assert compares one-row frames.
```python
# Q3: three versions of "paid conversion rate" with different denominators, SQL and pandas
import sqlite3
import pandas as pd

AS_OF = "2024-06-30"
SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-10',0),(2,'2024-02-01',0),(3,'2024-03-15',0),(4,'2024-04-01',0),
 (5,'2024-05-20',0),(6,'2024-06-10',0),(7,'2024-02-20',0),(8,'2024-01-05',1),(9,'2024-05-31',0);
INSERT INTO orders VALUES
 (101,1,'2024-01-12 10:00:00',100,'completed'),
 (102,1,'2024-04-02 10:00:00',50,'completed'),
 (103,1,'2024-04-03 10:00:00',70,'cancelled'),
 (104,2,'2024-04-15 10:00:00',80,'completed'),
 (105,3,'2024-03-20 10:00:00',60,'cancelled'),
 (106,3,'2024-03-25 10:00:00',90,'cancelled'),
 (107,4,'2024-04-20 10:00:00',40,'completed'),
 (108,4,'2024-04-21 10:00:00',40,'completed'),
 (109,5,'2024-06-05 10:00:00',55,'completed'),
 (110,6,'2024-06-12 10:00:00',30,'completed'),
 (111,8,'2024-01-06 10:00:00',500,'completed'),
 (113,1,'2024-05-01 10:00:00',25,'completed'),
 (114,9,'2024-06-30 15:00:00',35,'completed'),
 (115,9,'2024-06-02 10:00:00',20,'cancelled');
"""
SQL_MAIN = """
WITH nt AS (SELECT user_id, signup_date FROM users WHERE is_test = 0),
o AS (SELECT o.* FROM orders o JOIN nt ON nt.user_id = o.user_id),
mature AS (SELECT * FROM nt WHERE signup_date <= date(:as_of, '-30 days'))
SELECT
  ROUND(100.0 * (SELECT COUNT(DISTINCT user_id) FROM o WHERE status = 'completed')
        / (SELECT COUNT(*) FROM nt), 1) AS a_users_over_signups,
  ROUND(100.0 * (SELECT COUNT(*) FROM o WHERE status = 'completed')
        / (SELECT COUNT(*) FROM o), 1) AS b_orders_over_orders,
  ROUND(100.0 * (SELECT COUNT(*) FROM mature m WHERE EXISTS (
          SELECT 1 FROM o WHERE o.user_id = m.user_id AND o.status = 'completed'
            AND date(o.order_ts) >= m.signup_date
            AND date(o.order_ts) <= date(m.signup_date, '+30 days')))
        / (SELECT COUNT(*) FROM mature), 1) AS c_30d_window_mature
"""
SQL_BUG = """
WITH nt AS (SELECT user_id FROM users WHERE is_test = 0),
o AS (SELECT o.* FROM orders o JOIN nt ON nt.user_id = o.user_id)
SELECT ROUND(100.0 * (SELECT COUNT(DISTINCT user_id) FROM o WHERE status = 'completed')
             / (SELECT COUNT(*) FROM o), 1) AS users_over_orders_bug,
       ROUND(100.0 * (SELECT COUNT(*) FROM o WHERE status = 'completed')
             / (SELECT COUNT(*) FROM nt), 1) AS orders_over_users_bug
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": AS_OF})
print(sql_df.to_string(index=False))
print(pd.read_sql_query(SQL_BUG, con).to_string(index=False))
print("maturity cutoff:", con.execute("SELECT date(:a,'-30 days')", {"a": AS_OF}).fetchone()[0])

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
nt = users[users["is_test"] == 0]
o = orders.merge(nt[["user_id", "signup_date"]], on="user_id")
done = o[o["status"] == "completed"]
a = 100.0 * done["user_id"].nunique() / len(nt)
b = 100.0 * len(done) / len(o)
mature = nt[pd.to_datetime(nt["signup_date"]) <= pd.Timestamp(AS_OF) - pd.Timedelta(days=30)]
d = done.merge(mature[["user_id"]], on="user_id")
day = pd.to_datetime(d["order_ts"]).dt.normalize()
sign = pd.to_datetime(d["signup_date"])
hit = d[(day >= sign) & (day <= sign + pd.Timedelta(days=30))]
c = 100.0 * hit["user_id"].nunique() / len(mature)
pd_df = pd.DataFrame({"a_users_over_signups": [round(a, 1)], "b_orders_over_orders": [round(b, 1)],
                      "c_30d_window_mature": [round(c, 1)]})
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # one row
print("asserts passed")
print("mature users:", len(mature), "| non-test signups:", len(nt), "| orders (non-test):", len(o),
      "| completed:", len(done))
# date() window and unixepoch window agree on this data
x = con.execute("""SELECT COUNT(*) FROM users u JOIN orders o ON o.user_id = u.user_id
 WHERE o.status='completed' AND date(o.order_ts) >= u.signup_date
   AND unixepoch(date(o.order_ts)) <= unixepoch(u.signup_date) + 30*86400""").fetchone()[0]
y = con.execute("""SELECT COUNT(*) FROM users u JOIN orders o ON o.user_id = u.user_id
 WHERE o.status='completed' AND date(o.order_ts) >= u.signup_date
   AND date(o.order_ts) <= date(u.signup_date,'+30 days')""").fetchone()[0]
print("rows in window, unixepoch vs date():", x, y)
```

**Output (my run):**
```text
 a_users_over_signups  b_orders_over_orders  c_30d_window_mature
                 75.0                  69.2                 57.1
 users_over_orders_bug  orders_over_users_bug
                  46.2                  112.5
maturity cutoff: 2024-05-31
 a_users_over_signups  b_orders_over_orders  c_30d_window_mature
                 75.0                  69.2                 57.1
asserts passed
mature users: 7 | non-test signups: 8 | orders (non-test): 13 | completed: 9
rows in window, unixepoch vs date(): 7 7
```

**Edge cases:**
- The test user's completed 500 order is excluded from every numerator and denominator by joining to the non-test list first. Excluding test users only from the denominator would inflate every rate.
- Window boundary: user 9 pays on exactly day 30 and counts because the window is inclusive; the maturity cutoff `date(:as_of, '-30 days')` is 2024-05-31 in my run. If the cutoff were exclusive user 9 would move out of the cohort.
- Orders before signup (data errors) are excluded from (c) by the `>= signup_date` condition.
- Window arithmetic: `date(signup, '+30 days')` and a `unixepoch(...) + 30*86400` comparison matched on this data (7 rows each in my run).
- Cohort with no mature users: the denominator is 0 and the rate is NULL via the scalar division (SQLite returns NULL for division by zero).
- Immature users in (a) and (b) are included, which is why they look better than (c) for young products; see Part 6 Q13 for the immature-cohort trap.

**Then explain:**
- (a) is a user-level ever-converted rate: "what share of everyone who signed up has paid at least once", which keeps rising as cohorts age.
- (b) is an order-level success rate: "what share of orders complete"; it is closer to payment success or cancellation, not to conversion.
- (c) is a fixed-window cohort conversion and is comparable across cohorts, but only for mature ones.
- A numerator and denominator must have the same grain: users over users or orders over orders. 6 users over 13 orders is a ratio with no meaning, and orders over users exceeds 100%.
- Name the metric in the answer: "paid conversion, 30-day, mature, non-test".
- Dialects (not executed here): MySQL `DATE_ADD(signup_date, INTERVAL 30 DAY)` and `DATEDIFF`; PostgreSQL `signup_date + 30`.

**Follow-ups:**
- Per signup month? Group (c) by the cohort month, and report the cohort size and the excluded immature count.
- Why not use a rolling window (any time)? It is the "ever" rate and cannot be compared between cohorts of different age.
- What if cancelled orders were retried? Then a user's first completed order matters, and the rate counts the user once.

**Common mistakes:**
- User numerator over order denominator.
- Not excluding test users from both sides.
- Including users whose 30 days have not elapsed in (c) and calling the recent cohorts bad.
- Counting cancelled orders as paid.
- Using the wrong boundary (days 1 to 30 versus 0 to 30) without saying so.

### Q4 ⭐⭐⭐ 🟢 GMV, AOV, ARPU and ARPPU on one schema: users(user_id, signup_date, country, is_test) and orders(order_id, user_id, order_ts, amount, status) with status in ('completed', 'cancelled', 'returned'). For 2024-03 compute GMV (gross merchandise value), AOV (average order value), ARPU (revenue per user) and ARPPU (revenue per paying user) and state each definition. Decide which statuses count for GMV versus net revenue, which users form the ARPU denominator (all registered, or active in the month) and show how the choice changes the number. Cover the empty-month case (NULL or 0, not a division error).
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** GMV is the gross value of orders placed in the month, net revenue is what stays after cancellations and returns, AOV is value per order, ARPU divides revenue by all users in scope and ARPPU by paying users only; I state each definition and denominator first and guard every division with `NULLIF`.

**Definitions and assumptions (stated before the query):** month is 2024-03, UTC dates, test users excluded everywhere. GMV = completed plus returned orders placed in the month (cancelled orders never became a sale, so they are out; some teams include returned orders in GMV and take them out in net revenue, which is exactly what this definition does). Net revenue = completed orders only. AOV = GMV over the number of orders in GMV. ARPU = net revenue over registered non-test users at month end (signup before the next month). I also show the "active" denominator (users who placed any order in the month, cancelled ones included, because this schema has no events table). ARPPU = net revenue over users with at least one completed order in the month. These are my assumptions; the interviewer may have others, and the point is to say them.

**Schema and sample data:** seven users (user 6 is a test user, user 5 signs up in April, user 7 never orders). Nine orders: a test order of 999, a February order of 300 and an April order of 70 must stay out of March; order 6 is at 2024-03-31 23:30, inside the month.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-02-10','IN',0),(3,'2024-03-05','IN',0),(4,'2024-03-20','US',0),
 (5,'2024-04-02','IN',0),(6,'2024-01-15','IN',1),(7,'2024-02-01','IN',0);
INSERT INTO orders VALUES
 (1,1,'2024-03-03 10:00:00',100,'completed'),
 (2,1,'2024-03-10 10:00:00',50,'completed'),
 (3,2,'2024-03-12 10:00:00',200,'returned'),
 (4,3,'2024-03-15 10:00:00',80,'completed'),
 (5,3,'2024-03-16 10:00:00',60,'cancelled'),
 (6,4,'2024-03-31 23:30:00',40,'completed'),
 (7,6,'2024-03-05 10:00:00',999,'completed'),
 (8,2,'2024-02-28 10:00:00',300,'completed'),
 (9,5,'2024-04-03 10:00:00',70,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block, parameterised by the month start. Each measure comes from its own aggregate at order grain, and the registered count comes from a separate CTE so the user count is not multiplied by orders.
```sql
WITH u AS (SELECT user_id, signup_date FROM users WHERE is_test = 0),
m AS (SELECT o.* FROM orders o JOIN u ON u.user_id = o.user_id
      WHERE o.order_ts >= :m_start AND o.order_ts < date(:m_start, '+1 month')),
agg AS (
  SELECT SUM(CASE WHEN status IN ('completed', 'returned') THEN amount END) AS gmv,
         COUNT(CASE WHEN status IN ('completed', 'returned') THEN 1 END) AS gmv_orders,
         SUM(CASE WHEN status = 'completed' THEN amount END) AS net_revenue,
         COUNT(DISTINCT user_id) AS active_users,
         COUNT(DISTINCT CASE WHEN status = 'completed' THEN user_id END) AS paying_users
  FROM m),
reg AS (SELECT COUNT(*) AS registered FROM u WHERE signup_date < date(:m_start, '+1 month'))
SELECT substr(:m_start, 1, 7) AS month,
       COALESCE(gmv, 0) AS gmv, gmv_orders,
       ROUND(1.0 * gmv / NULLIF(gmv_orders, 0), 2) AS aov,
       COALESCE(net_revenue, 0) AS net_revenue,
       registered, active_users, paying_users,
       ROUND(1.0 * COALESCE(net_revenue, 0) / NULLIF(registered, 0), 2) AS arpu_registered,
       ROUND(1.0 * net_revenue / NULLIF(active_users, 0), 2) AS arpu_active,
       ROUND(1.0 * net_revenue / NULLIF(paying_users, 0), 2) AS arppu
FROM agg CROSS JOIN reg
```

**pandas answer:** shown once, identical to the Code block (a function of the month start; `ratio` returns NaN for an empty denominator):
```py
start = pd.Timestamp(m_start)
end = start + pd.offsets.MonthBegin(1)
u = users[users["is_test"] == 0]
m = orders.merge(u[["user_id"]], on="user_id")
ts = pd.to_datetime(m["order_ts"])
m = m[(ts >= start) & (ts < end)]
gm = m[m["status"].isin(["completed", "returned"])]
paid = m[m["status"] == "completed"]
registered = int((pd.to_datetime(u["signup_date"]) < end).sum())
gmv, net = float(gm["amount"].sum()), float(paid["amount"].sum())
active, payers = m["user_id"].nunique(), paid["user_id"].nunique()
return {"month": m_start[:7], "gmv": gmv, "gmv_orders": len(gm), "aov": ratio(gmv, len(gm)),
        "net_revenue": net, "registered": registered, "active_users": active, "paying_users": payers,
        "arpu_registered": ratio(net, registered), "arpu_active": ratio(net, active),
        "arppu": ratio(net, payers)}
```

**Example:** March, non-test.
- Orders in March: 1 (100 completed), 2 (50 completed), 3 (200 returned), 4 (80 completed), 5 (60 cancelled), 6 (40 completed).
- GMV = 100 + 50 + 200 + 80 + 40 = 470 over 5 orders, so AOV = 94.0.
- Net revenue = 100 + 50 + 80 + 40 = 270.
- Registered at month end: users 1, 2, 3, 4, 7 = 5 (user 5 signs up in April, user 6 is test). ARPU = 270/5 = 54.0.
- Active users (any order in March): 1, 2, 3, 4 = 4, so revenue per active user = 67.5. Paying users: 1, 3, 4 = 3, so ARPPU = 90.0.
- Status choice moves GMV: all statuses 530, excluding cancelled 470, completed only 270 in my run.
- May has no orders: sums print 0, AOV, ARPU over active and ARPPU are NULL (not a division error), and ARPU over registered users is 0.0 because there are 6 registered users.

**Code:** run with `python3 -I`. Rows are in month order (2024-03, 2024-05); the SQL integer columns are cast to float before the compare because a NULL in a column makes it float.
```python
# Q4: GMV, AOV, ARPU, ARPPU for one month, with explicit status and denominator choices
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-02-10','IN',0),(3,'2024-03-05','IN',0),(4,'2024-03-20','US',0),
 (5,'2024-04-02','IN',0),(6,'2024-01-15','IN',1),(7,'2024-02-01','IN',0);
INSERT INTO orders VALUES
 (1,1,'2024-03-03 10:00:00',100,'completed'),
 (2,1,'2024-03-10 10:00:00',50,'completed'),
 (3,2,'2024-03-12 10:00:00',200,'returned'),
 (4,3,'2024-03-15 10:00:00',80,'completed'),
 (5,3,'2024-03-16 10:00:00',60,'cancelled'),
 (6,4,'2024-03-31 23:30:00',40,'completed'),
 (7,6,'2024-03-05 10:00:00',999,'completed'),
 (8,2,'2024-02-28 10:00:00',300,'completed'),
 (9,5,'2024-04-03 10:00:00',70,'completed');
"""
# assumptions: GMV = completed + returned orders placed in the month (cancelled excluded);
# net revenue = completed only; AOV = GMV / orders in GMV; test users out everywhere
SQL_MAIN = """
WITH u AS (SELECT user_id, signup_date FROM users WHERE is_test = 0),
m AS (SELECT o.* FROM orders o JOIN u ON u.user_id = o.user_id
      WHERE o.order_ts >= :m_start AND o.order_ts < date(:m_start, '+1 month')),
agg AS (
  SELECT SUM(CASE WHEN status IN ('completed', 'returned') THEN amount END) AS gmv,
         COUNT(CASE WHEN status IN ('completed', 'returned') THEN 1 END) AS gmv_orders,
         SUM(CASE WHEN status = 'completed' THEN amount END) AS net_revenue,
         COUNT(DISTINCT user_id) AS active_users,
         COUNT(DISTINCT CASE WHEN status = 'completed' THEN user_id END) AS paying_users
  FROM m),
reg AS (SELECT COUNT(*) AS registered FROM u WHERE signup_date < date(:m_start, '+1 month'))
SELECT substr(:m_start, 1, 7) AS month,
       COALESCE(gmv, 0) AS gmv, gmv_orders,
       ROUND(1.0 * gmv / NULLIF(gmv_orders, 0), 2) AS aov,
       COALESCE(net_revenue, 0) AS net_revenue,
       registered, active_users, paying_users,
       ROUND(1.0 * COALESCE(net_revenue, 0) / NULLIF(registered, 0), 2) AS arpu_registered,
       ROUND(1.0 * net_revenue / NULLIF(active_users, 0), 2) AS arpu_active,
       ROUND(1.0 * net_revenue / NULLIF(paying_users, 0), 2) AS arppu
FROM agg CROSS JOIN reg
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
months = ["2024-03-01", "2024-05-01"]  # May has no orders
sql_df = pd.concat([pd.read_sql_query(SQL_MAIN, con, params={"m_start": m}) for m in months], ignore_index=True)
sql_df[sql_df.columns[1:]] = sql_df[sql_df.columns[1:]].astype(float)  # None becomes NaN
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)

def ratio(n, d):
    return round(n / d, 2) if d else np.nan

def metrics(m_start):
    # pd:main
    start = pd.Timestamp(m_start)
    end = start + pd.offsets.MonthBegin(1)
    u = users[users["is_test"] == 0]
    m = orders.merge(u[["user_id"]], on="user_id")
    ts = pd.to_datetime(m["order_ts"])
    m = m[(ts >= start) & (ts < end)]
    gm = m[m["status"].isin(["completed", "returned"])]
    paid = m[m["status"] == "completed"]
    registered = int((pd.to_datetime(u["signup_date"]) < end).sum())
    gmv, net = float(gm["amount"].sum()), float(paid["amount"].sum())
    active, payers = m["user_id"].nunique(), paid["user_id"].nunique()
    return {"month": m_start[:7], "gmv": gmv, "gmv_orders": len(gm), "aov": ratio(gmv, len(gm)),
            "net_revenue": net, "registered": registered, "active_users": active, "paying_users": payers,
            "arpu_registered": ratio(net, registered), "arpu_active": ratio(net, active),
            "arppu": ratio(net, payers)}
    # pd:end

pd_df = pd.DataFrame([metrics(m) for m in months])
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # rows in month order
print("asserts passed")
# how the status choice moves GMV for March (non-test)
alt = con.execute("""SELECT SUM(amount), SUM(CASE WHEN status<>'cancelled' THEN amount END),
  SUM(CASE WHEN status='completed' THEN amount END) FROM orders o JOIN users u USING(user_id)
  WHERE u.is_test=0 AND order_ts >= '2024-03-01' AND order_ts < '2024-04-01'""").fetchone()
print("March GMV all statuses / excl cancelled / completed only:", alt)
```

**Output (my run):**
```text
  month   gmv  gmv_orders  aov  net_revenue  registered  active_users  paying_users  arpu_registered  arpu_active  arppu
2024-03 470.0         5.0 94.0        270.0         5.0           4.0           3.0             54.0         67.5   90.0
2024-05   0.0         0.0  NaN          0.0         6.0           0.0           0.0              0.0          NaN    NaN
  month   gmv  gmv_orders  aov  net_revenue  registered  active_users  paying_users  arpu_registered  arpu_active  arppu
2024-03 470.0           5 94.0        270.0           5             4             3             54.0         67.5   90.0
2024-05   0.0           0  NaN          0.0           6             0             0              0.0          NaN    NaN
asserts passed
March GMV all statuses / excl cancelled / completed only: (530.0, 470.0, 270.0)
```

**Edge cases:**
- Honest surprise found while testing: my first SQL used `net_revenue / registered`, which gave NULL for the empty month, while pandas gave 0.0. With 6 registered users and no revenue ARPU is 0, not unknown; I wrapped the numerator in `COALESCE(net_revenue, 0)`. ARPU over active users or payers really is undefined (0 divided by 0), so NULL is right there.
- Month boundary: order 6 at 23:30 on 03-31 is inside because the range is half-open `< date(:m_start, '+1 month')`; `BETWEEN '2024-03-01' AND '2024-03-31'` would lose it.
- Returned orders: a return that happens in a later month is a refund in that month (Q10 and Q11 handle the order-month versus cash views).
- The test order of 999 would have multiplied GMV by more than three if it leaked.
- Currency, taxes and shipping: GMV may or may not include them; say which.
- ARPU over registered users shrinks when signups surge (Q39).

**Then explain:**
- GMV measures activity (what was bought), net revenue measures what the business keeps; mixing them in one ratio is the main trap.
- AOV is an order-grain mean, ARPU and ARPPU are user-grain: the denominators differ by grain.
- ARPU over registered users answers "what does an average user bring", over active users "how engaged buyers spend", over payers "how much a payer pays". The same 270 gives 54.0, 67.5 or 90.0 in my run.
- `NULLIF(den, 0)` returns NULL instead of an error in engines that raise one; SQLite returns NULL for division by zero anyway, but PostgreSQL raises an error (hedged: not executed here).
- Dialects (not executed here): PostgreSQL `date_trunc('month', order_ts)`; BigQuery `SAFE_DIVIDE`; MySQL `DATE_FORMAT`.

**Follow-ups:**
- GMV per country? Add `country` to the group (orders joined to users once; users has one row per user, so no fan-out).
- ARPU for a rolling 30 days? Same query, different window; say whether the denominator is as of the window end.
- Net of refunds? See Q10.

**Common mistakes:**
- Averaging order amounts per user and then averaging again (an average of averages).
- Joining orders to users twice or to a many-row table before summing.
- Counting cancelled orders in GMV without saying so.
- Using all users ever (including future signups) as the ARPU denominator.
- Dividing without a zero guard.

### Q5 ⭐⭐⭐ 🟢 LeetCode 1174 Immediate Food Delivery II: delivery(delivery_id, customer_id, order_date, customer_pref_delivery_date) where an order is immediate when the preferred date equals the order date and each customer's first order is their earliest order_date (one per customer by the problem guarantee). Return the percentage of immediate orders among customers' first orders, rounded to 2 decimals. Show the join-to-MIN approach and the ROW_NUMBER approach, why comparing MIN(order_date) with MIN(preferred date) is wrong, and what you do if two orders tie on the earliest date.
**Asked at:** LeetCode SQL 50 style problem (statement known from the doocs mirror, opened for 1174, and from search snippets for the others; leetcode.com pages were not opened); public problem bank, not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Take each customer's first order (earliest `order_date`), mark it immediate when the preferred date equals the order date, and take the average of that flag times 100, rounded to 2 decimals; I show the join-to-MIN version and the `ROW_NUMBER` version, and they agree unless a customer has a tie on the earliest date.

**Schema and sample data:** six customers. The problem guarantees one earliest order per customer; I test the same code on clean data, on data with a preferred date earlier than the order date (a data error) and on a customer with two orders on the earliest date (breaking the guarantee). The statement follows the LeetCode 1174 text as I remember it from a mirror I opened; I did not open leetcode.com.
```sql
CREATE TABLE delivery(delivery_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, customer_pref_delivery_date TEXT);
INSERT INTO delivery VALUES
 (1,1,'2024-03-01','2024-03-01'),(2,1,'2024-03-05','2024-03-05'),
 (3,2,'2024-03-02','2024-03-04'),(4,2,'2024-03-10','2024-03-10'),
 (5,3,'2024-03-03','2024-03-03'),
 (6,4,'2024-03-04','2024-03-09'),(7,4,'2024-03-06','2024-03-06'),
 (8,5,'2024-03-07','2024-03-07'),
 (9,6,'2024-03-08','2024-03-12');
```
The extra rows for the other two scenarios are `(10,7,'2024-03-02','2024-03-04'),(11,7,'2024-03-09','2024-03-02')` (dirty) and `(12,8,'2024-03-11','2024-03-11'),(13,8,'2024-03-11','2024-03-15')` (tie); they are added in the Code block.

**SQL answer:** `SQL_JOIN` in the Code block (join each order to its customer's MIN date):
```sql
SELECT ROUND(100.0 * SUM(d.order_date = d.customer_pref_delivery_date) / COUNT(*), 2) AS immediate_pct
FROM delivery d
JOIN (SELECT customer_id, MIN(order_date) AS first_date
      FROM delivery GROUP BY customer_id) f
  ON f.customer_id = d.customer_id AND f.first_date = d.order_date
```
and `SQL_RN` (rank each customer's orders, keep row 1; the tie-breaker is `delivery_id`):
```sql
SELECT ROUND(100.0 * AVG(order_date = customer_pref_delivery_date), 2) AS immediate_pct
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, delivery_id) AS rn
      FROM delivery)
WHERE rn = 1
```

**pandas answer:** both versions, shown once and identical to the Code block:
```py
d = delivery.sort_values(["customer_id", "order_date", "delivery_id"])
first = d.groupby("customer_id").head(1)                       # ROW_NUMBER() = 1
rn = round(100 * (first["order_date"] == first["customer_pref_delivery_date"]).mean(), 2)
m = delivery.groupby("customer_id")["order_date"].transform("min")
f = delivery[delivery["order_date"] == m]                      # join to MIN keeps ties
jn = round(100 * (f["order_date"] == f["customer_pref_delivery_date"]).mean(), 2)
```

**Example:** clean data, first order per customer.
- Customer 1: first 03-01, preferred 03-01, immediate. Customer 2: first 03-02, preferred 03-04, scheduled. Customer 3: 03-03 and 03-03, immediate. Customer 4: first 03-04, preferred 03-09, scheduled (the later immediate order does not count). Customer 5: immediate. Customer 6: 03-08 and 03-12, scheduled.
- 3 immediate firsts out of 6 customers = 50.0%.
- Over all orders it would be 6 of 9 = 66.67%, which answers a different question.

**Code:** run with `python3 -I`. Each assert compares two scalars per scenario, so there is no row order.
```python
# Q5: LeetCode 1174 Immediate Food Delivery II: join-to-MIN and ROW_NUMBER, SQL and pandas
import sqlite3
import pandas as pd

BASE = """
 (1,1,'2024-03-01','2024-03-01'),(2,1,'2024-03-05','2024-03-05'),
 (3,2,'2024-03-02','2024-03-04'),(4,2,'2024-03-10','2024-03-10'),
 (5,3,'2024-03-03','2024-03-03'),
 (6,4,'2024-03-04','2024-03-09'),(7,4,'2024-03-06','2024-03-06'),
 (8,5,'2024-03-07','2024-03-07'),
 (9,6,'2024-03-08','2024-03-12')"""
DIRTY = ",\n (10,7,'2024-03-02','2024-03-04'),(11,7,'2024-03-09','2024-03-02')"      # a pref date before the order date
TIE = ",\n (12,8,'2024-03-11','2024-03-11'),(13,8,'2024-03-11','2024-03-15')"        # two orders on the earliest date
DDL = "CREATE TABLE delivery(delivery_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, customer_pref_delivery_date TEXT);\nINSERT INTO delivery VALUES"

SQL_JOIN = """
SELECT ROUND(100.0 * SUM(d.order_date = d.customer_pref_delivery_date) / COUNT(*), 2) AS immediate_pct
FROM delivery d
JOIN (SELECT customer_id, MIN(order_date) AS first_date
      FROM delivery GROUP BY customer_id) f
  ON f.customer_id = d.customer_id AND f.first_date = d.order_date
"""
SQL_RN = """
SELECT ROUND(100.0 * AVG(order_date = customer_pref_delivery_date), 2) AS immediate_pct
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, delivery_id) AS rn
      FROM delivery)
WHERE rn = 1
"""
SQL_MIN_MIN = """
SELECT ROUND(100.0 * SUM(min_order = min_pref) / COUNT(*), 2) AS immediate_pct
FROM (SELECT customer_id, MIN(order_date) AS min_order, MIN(customer_pref_delivery_date) AS min_pref
      FROM delivery GROUP BY customer_id)
"""
SQL_ALL_ORDERS = """
SELECT ROUND(100.0 * AVG(order_date = customer_pref_delivery_date), 2) FROM delivery
"""

def make(extra=""):
    con = sqlite3.connect(":memory:")
    con.executescript(DDL + BASE + extra + ";")
    return con

def pandas_versions(delivery):
    # pd:main
    d = delivery.sort_values(["customer_id", "order_date", "delivery_id"])
    first = d.groupby("customer_id").head(1)                       # ROW_NUMBER() = 1
    rn = round(100 * (first["order_date"] == first["customer_pref_delivery_date"]).mean(), 2)
    m = delivery.groupby("customer_id")["order_date"].transform("min")
    f = delivery[delivery["order_date"] == m]                      # join to MIN keeps ties
    jn = round(100 * (f["order_date"] == f["customer_pref_delivery_date"]).mean(), 2)
    # pd:end
    return jn, rn

for label, extra in [("clean data (guarantee holds)", ""), ("dirty: pref date before order date", DIRTY),
                     ("tie: two orders on the earliest date", TIE)]:
    con = make(extra)
    j = con.execute(SQL_JOIN).fetchone()[0]
    r = con.execute(SQL_RN).fetchone()[0]
    mm = con.execute(SQL_MIN_MIN).fetchone()[0]
    allo = con.execute(SQL_ALL_ORDERS).fetchone()[0]
    pj, pr = pandas_versions(pd.read_sql_query("SELECT * FROM delivery", con))
    assert (pj, pr) == (j, r)   # scalars, no row order
    print(f"{label}: join-to-MIN {j} | ROW_NUMBER {r} | MIN vs MIN {mm} | all orders {allo} | pandas {pj} / {pr}")
print("asserts passed")
```

**Output (my run):**
```text
clean data (guarantee holds): join-to-MIN 50.0 | ROW_NUMBER 50.0 | MIN vs MIN 50.0 | all orders 66.67 | pandas 50.0 / 50.0
dirty: pref date before order date: join-to-MIN 42.86 | ROW_NUMBER 42.86 | MIN vs MIN 57.14 | all orders 54.55 | pandas 42.86 / 42.86
tie: two orders on the earliest date: join-to-MIN 50.0 | ROW_NUMBER 57.14 | MIN vs MIN 57.14 | all orders 63.64 | pandas 50.0 / 57.14
asserts passed
```

**Edge cases:**
- Correction to the premise: comparing `MIN(order_date)` with `MIN(customer_pref_delivery_date)` per customer is not wrong on clean data. If every preferred date is on or after its order date, the two minimums are equal exactly when the first order is immediate, and my run gave 50.0 for it, the same as the correct answer. It is wrong when the data breaks that rule: with a preferred date earlier than an order date (customer 7) it gave 57.14 against the correct 42.86. It also asks the wrong question (is any preferred date equal to the first order date), so I avoid it.
- Tie on the earliest date: the join-to-MIN version keeps both rows, so the tied customer counts twice (rows, not customers) and gave 50.0; `ROW_NUMBER` with a tie-breaker keeps one row and gave 57.14. State the rule (first by `delivery_id`, or immediate if any earliest order is immediate) and make the denominator customers.
- `AVG(a = b)` works in SQLite because a comparison is 0 or 1; in PostgreSQL cast the boolean (`(a = b)::int`) (not executed here).
- A customer with no orders does not exist in this table, so no denominator issue; if a customers table exists, decide whether to include them.
- Empty table: `SUM(...) / COUNT(*)` gives NULL in SQLite; `AVG` also gives NULL.

**Then explain:**
- The unit is the customer's first order, so the denominator is customers.
- Join-to-MIN is two scans plus a join; `ROW_NUMBER` is one sort per partition and makes the tie rule explicit.
- `ROUND(..., 2)` in SQLite rounds half away from zero; pandas `round` rounds half to even. No value here is an exact tie.
- Dialects (not executed here): MySQL (the LeetCode default as far as I remember) `ROUND(AVG(order_date = customer_pref_delivery_date) * 100, 2)`; PostgreSQL needs the boolean cast; Snowflake and BigQuery have `QUALIFY` for the row-number filter.

**Follow-ups:**
- Per cohort month? Group the first-order table by the month of `first_date`.
- Why not `DISTINCT ON`? PostgreSQL only (not executed here).
- Ties in a real table? Add a deterministic tie-breaker and report how many ties exist.

**Common mistakes:**
- Averaging over all orders.
- `MIN(order_date) = MIN(pref)` as a general rule (works only under clean data).
- No tie-breaker in `ROW_NUMBER`, so the pick changes between runs.
- Integer division when writing `SUM(...) / COUNT(*)` without `100.0`.

### Q6 ⭐⭐⭐ 🟢 LeetCode 1633 Percentage of Users Attended a Contest: users(user_id, user_name) and register(contest_id, user_id). Return for each contest the percentage of all users who registered, rounded to 2 decimals, ordered by percentage descending then contest_id ascending. Show why the denominator is the Users table (not the register table), what happens with a duplicate register row (use COUNT(DISTINCT)), a contest nobody joined (absent from register, so it does not appear unless a contests table exists) and integer division in SQLite (multiply by 100.0).
**Asked at:** LeetCode SQL 50 style problem (statement known from the doocs mirror, opened for 1174, and from search snippets for the others; leetcode.com pages were not opened); public problem bank, not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** For each contest, count the distinct registered users and divide by the number of users in the Users table (not by rows in register), multiply by `100.0` to avoid integer division, round to 2 decimals, and order by percentage descending then contest id ascending.

**Schema and sample data:** eight users. Contest 100 has a duplicate register row for user 1. Contest 400 ties contest 100 at 50%. A `contests` table includes contest 500, which nobody joined. The statement follows LeetCode 1633 as I remember it from search snippets and a mirror; I did not open leetcode.com.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, user_name TEXT);
CREATE TABLE register(contest_id INTEGER, user_id INTEGER);
CREATE TABLE contests(contest_id INTEGER PRIMARY KEY);
INSERT INTO users VALUES (1,'A'),(2,'B'),(3,'C'),(4,'D'),(5,'E'),(6,'F'),(7,'G'),(8,'H');
INSERT INTO register VALUES
 (100,1),(100,2),(100,3),(100,4),(100,1),
 (200,2),(200,3),
 (300,5),(300,6),(300,7),
 (400,1),(400,2),(400,3),(400,4);
INSERT INTO contests VALUES (100),(200),(300),(400),(500);
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
SELECT contest_id,
       ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM users), 2) AS percentage
FROM register
GROUP BY contest_id
ORDER BY percentage DESC, contest_id
```
Variants in the Code block: `SQL_COUNT_ROWS` (counts rows), `SQL_WRONG_DENOM` (divides by register rows), `SQL_INT_DIV` (integer arithmetic) and `SQL_WITH_CONTESTS` (starts from a contests table).

**pandas answer:** shown once, identical to the Code block:
```py
n_users = users["user_id"].nunique()
pd_df = (register.groupby("contest_id")["user_id"].nunique().mul(100).div(n_users).round(2)
         .rename("percentage").reset_index()
         .sort_values(["percentage", "contest_id"], ascending=[False, True], kind="stable")
         .reset_index(drop=True))
```

**Example:** 8 users.
- Contest 100: distinct users 1, 2, 3, 4 = 4, so 50.0% (5 rows because of the duplicate, which would give 62.5%).
- Contest 400: 4 users, 50.0%. Tie with 100, so contest id decides: 100 first.
- Contest 300: 3 users = 37.5%. Contest 200: 2 users = 25.0%.
- Order: 100, 400, 300, 200.

**Code:** run with `python3 -I`. The assert compares frames after both are ordered by `percentage` descending, `contest_id` ascending.
```python
# Q6: LeetCode 1633 Percentage of Users Attended a Contest, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, user_name TEXT);
CREATE TABLE register(contest_id INTEGER, user_id INTEGER);
CREATE TABLE contests(contest_id INTEGER PRIMARY KEY);
INSERT INTO users VALUES (1,'A'),(2,'B'),(3,'C'),(4,'D'),(5,'E'),(6,'F'),(7,'G'),(8,'H');
INSERT INTO register VALUES
 (100,1),(100,2),(100,3),(100,4),(100,1),
 (200,2),(200,3),
 (300,5),(300,6),(300,7),
 (400,1),(400,2),(400,3),(400,4);
INSERT INTO contests VALUES (100),(200),(300),(400),(500);
"""
SQL_MAIN = """
SELECT contest_id,
       ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM users), 2) AS percentage
FROM register
GROUP BY contest_id
ORDER BY percentage DESC, contest_id
"""
SQL_COUNT_ROWS = """
SELECT contest_id, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM users), 2) AS percentage
FROM register GROUP BY contest_id ORDER BY percentage DESC, contest_id
"""
SQL_WRONG_DENOM = """
SELECT contest_id, ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM register), 2) AS percentage
FROM register GROUP BY contest_id ORDER BY percentage DESC, contest_id
"""
SQL_INT_DIV = """
SELECT contest_id, COUNT(DISTINCT user_id) * 100 / (SELECT COUNT(*) FROM users) AS percentage
FROM register GROUP BY contest_id ORDER BY percentage DESC, contest_id
"""
SQL_WITH_CONTESTS = """
SELECT c.contest_id,
       ROUND(100.0 * COUNT(DISTINCT r.user_id) / (SELECT COUNT(*) FROM users), 2) AS percentage
FROM contests c LEFT JOIN register r ON r.contest_id = c.contest_id
GROUP BY c.contest_id
ORDER BY percentage DESC, c.contest_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main:"); print(sql_df.to_string(index=False))
print("COUNT(*) with a duplicate row:", con.execute(SQL_COUNT_ROWS).fetchall())
print("denominator = register rows:", con.execute(SQL_WRONG_DENOM).fetchall())
print("integer division:", con.execute(SQL_INT_DIV).fetchall())
print("with a contests table:", con.execute(SQL_WITH_CONTESTS).fetchall())
print("SQLite 3/2 =", con.execute("SELECT 3/2, 3/2.0, 3*1.0/2").fetchone())

users = pd.read_sql_query("SELECT * FROM users", con)
register = pd.read_sql_query("SELECT * FROM register", con)
# pd:main
n_users = users["user_id"].nunique()
pd_df = (register.groupby("contest_id")["user_id"].nunique().mul(100).div(n_users).round(2)
         .rename("percentage").reset_index()
         .sort_values(["percentage", "contest_id"], ascending=[False, True], kind="stable")
         .reset_index(drop=True))
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # both ordered by percentage desc, contest_id asc
print("asserts passed")
# rounding on a tie: 100 * 1 / 16 = 6.25 percent, one decimal
print("ROUND(6.25, 1) in SQLite:", con.execute("SELECT ROUND(6.25, 1)").fetchone()[0],
      "| pandas round(1):", pd.Series([6.25]).round(1).iloc[0])
```

**Output (my run):**
```text
SQL main:
 contest_id  percentage
        100        50.0
        400        50.0
        300        37.5
        200        25.0
COUNT(*) with a duplicate row: [(100, 62.5), (400, 50.0), (300, 37.5), (200, 25.0)]
denominator = register rows: [(100, 28.57), (400, 28.57), (300, 21.43), (200, 14.29)]
integer division: [(100, 50), (400, 50), (300, 37), (200, 25)]
with a contests table: [(100, 50.0), (400, 50.0), (300, 37.5), (200, 25.0), (500, 0.0)]
SQLite 3/2 = (1, 1.5, 1.5)
pandas:
 contest_id  percentage
        100        50.0
        400        50.0
        300        37.5
        200        25.0
asserts passed
ROUND(6.25, 1) in SQLite: 6.3 | pandas round(1): 6.2
```

**Edge cases:**
- Duplicate register row: `COUNT(*)` gave 62.5 for contest 100 in my run; `COUNT(DISTINCT user_id)` gave 50.0.
- Wrong denominator: dividing by the 14 register rows gave 28.57, 28.57, 21.43, 14.29. The question is "of all users", so the denominator is `users`.
- Integer division: `COUNT(DISTINCT user_id) * 100 / (SELECT COUNT(*) FROM users)` returned 50, 50, 37, 25 in my run; the 37.5 was truncated to 37. In SQLite `3/2` is 1 and `3/2.0` is 1.5. `100.0 *` fixes it.
- A contest nobody joined is absent from `register`, so it is absent from the result. With a contests table, `LEFT JOIN` and `COUNT(DISTINCT r.user_id)` give 0.0 for contest 500 in my run.
- A register row for a user not in `users` (the problem guarantees this does not happen) would count toward the numerator and could push the percentage above 100; I did not run that case.
- Rounding: SQLite `ROUND` rounds half away from zero and pandas `round` half to even. In my run `ROUND(6.25, 1)` gave 6.3 while `Series.round(1)` gave 6.2. No value in this table is a tie at 2 decimals, so the assert holds, but a tie would differ.
- Empty `users`: the divisor is 0 and SQLite returns NULL.

**Then explain:**
- The question is a share of the whole user base, so the base is a scalar subquery; Part 3 covers scalar subqueries.
- Distinct protects against duplicate registrations; if the table has a primary key `(contest_id, user_id)` it is a no-op but harmless.
- Order is part of the contract: percentage descending, ties by contest id ascending.
- Dialects (not executed here): in PostgreSQL integer division also truncates, so keep `100.0`; MySQL divides to a decimal with `/`.

**Follow-ups:**
- Include contests with zero registrations? Start from a contests table (shown).
- Round to a string with two decimals? Format at the edge; `ROUND` returns a float.
- Percent of users who registered for at least one contest? A single `COUNT(DISTINCT user_id)` over register divided by users.

**Common mistakes:**
- Dividing by register rows.
- `COUNT(*)` with duplicate rows.
- Integer division (50, 37, 25 instead of 50.0, 37.5, 25.0).
- Ordering only by percentage and leaving ties in undefined order.

### Q7 ⭐⭐⭐ 🟡 Strictly ordered funnel with MIN(CASE): events(user_id, event_ts, event_name) with event_name in ('view', 'cart', 'purchase'). First compute one row per user with first_view, first_cart and first_purchase using MIN(CASE WHEN event_name = ... THEN event_ts END). Then count the users who completed view then cart then purchase in that strict order (first_view < first_cart < first_purchase), and compare with the any-order counts from the same table. Show a user who purchased before viewing, a user who carted twice, and say why 'first of each step' can wrongly reject a user whose first cart came before a later valid view-cart-purchase sequence (and when that matters).
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** Build one row per user with `MIN(CASE WHEN event_name = ... THEN event_ts END)` for each step, count a user in a step only when its first timestamp is strictly after the previous step's, and note that "first of each" can reject a user whose first cart came before a later valid view, cart, purchase sequence, so a chained version looks for the first cart after the first view and the first purchase after that cart.

**Schema and sample data:** eight users. User 2 purchased before viewing. User 3 carted twice. User 4 carted at 08:00 before their first view at 09:00, then viewed, carted again and purchased (a valid sequence hidden behind an early cart). User 5 skipped the cart. User 8 viewed and carted at the same second.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 09:00:00','purchase'),(2,'2024-03-01 09:30:00','view'),(2,'2024-03-01 09:40:00','cart'),
 (3,'2024-03-01 10:00:00','view'),(3,'2024-03-01 10:05:00','cart'),(3,'2024-03-01 10:07:00','cart'),(3,'2024-03-01 10:20:00','purchase'),
 (4,'2024-03-01 08:00:00','cart'),(4,'2024-03-01 09:00:00','view'),(4,'2024-03-01 09:10:00','cart'),(4,'2024-03-01 09:30:00','purchase'),
 (5,'2024-03-01 11:00:00','view'),(5,'2024-03-01 11:05:00','purchase'),
 (6,'2024-03-01 12:00:00','view'),(6,'2024-03-01 12:05:00','cart'),
 (7,'2024-03-01 13:00:00','view'),(7,'2024-03-01 13:01:00','view'),
 (8,'2024-03-01 12:00:00','view'),(8,'2024-03-01 12:00:00','cart'),(8,'2024-03-01 12:10:00','purchase');
```

**SQL answer:** `SQL_FIRST` in the Code block (the per-user first-timestamp table, then strict comparisons; a NULL timestamp makes the comparison NULL, so a missing step is not counted):
```sql
WITH f AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view'     THEN event_ts END) AS first_view,
         MIN(CASE WHEN event_name = 'cart'     THEN event_ts END) AS first_cart,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY user_id
)
SELECT COUNT(first_view) AS viewed,
       COUNT(CASE WHEN first_view < first_cart THEN 1 END) AS carted,
       COUNT(CASE WHEN first_view < first_cart AND first_cart < first_purchase THEN 1 END) AS purchased
FROM f
```
The any-order counts are `SQL_ANY` and the chained version is `SQL_CHAIN` in the Code block:
```sql
WITH v AS (SELECT user_id, MIN(event_ts) AS t1 FROM events WHERE event_name = 'view' GROUP BY user_id),
c AS (SELECT v.user_id, MIN(e.event_ts) AS t2
      FROM v JOIN events e ON e.user_id = v.user_id AND e.event_name = 'cart' AND e.event_ts > v.t1
      GROUP BY v.user_id),
p AS (SELECT c.user_id, MIN(e.event_ts) AS t3
      FROM c JOIN events e ON e.user_id = c.user_id AND e.event_name = 'purchase' AND e.event_ts > c.t2
      GROUP BY c.user_id)
SELECT (SELECT COUNT(*) FROM v) AS viewed, (SELECT COUNT(*) FROM c) AS carted, (SELECT COUNT(*) FROM p) AS purchased
```
`SQL_PER_USER` prints the first timestamps per user.

**pandas answer:** shown once, identical to the Code block (groupby/unstack for the first-timestamp table, then a merge-per-step chain):
```py
first = events.groupby(["user_id", "event_name"])["event_ts"].min().unstack()
any_order = first[["view", "cart", "purchase"]].notna().sum()
ok2 = first["view"] < first["cart"]
ok3 = ok2 & (first["cart"] < first["purchase"])
strict = pd.Series({"viewed": first["view"].notna().sum(), "carted": ok2.sum(), "purchased": ok3.sum()})
# chained: cart must be after the first view, purchase after that cart
v = first["view"].dropna().rename("t1").reset_index()
carts = events[events["event_name"] == "cart"][["user_id", "event_ts"]]
c = v.merge(carts, on="user_id")
c = c[c["event_ts"] > c["t1"]].groupby("user_id", as_index=False)["event_ts"].min().rename(columns={"event_ts": "t2"})
purchases = events[events["event_name"] == "purchase"][["user_id", "event_ts"]]
p = c.merge(purchases, on="user_id")
p = p[p["event_ts"] > p["t2"]].groupby("user_id", as_index=False)["event_ts"].min()
chain = pd.Series({"viewed": len(v), "carted": len(c), "purchased": len(p)})
```

**Example:** first timestamps per user (time of day):
- User 1: 10:00, 10:05, 10:10, in order. User 2: view 09:30, cart 09:40, purchase 09:00, so purchase before view: rejected at step 3. User 3: in order despite the second cart. User 4: view 09:00, first cart 08:00, purchase 09:30: first-of-each rejects (cart not after view). User 5: no cart. User 6: view and cart only. User 7: view only. User 8: view and cart at 12:00:00, equal, so `<` rejects.
- Any order: 8 viewed, 6 carted (1, 2, 3, 4, 6, 8), 6 purchased (1, 2, 3, 4, 5, 8).
- Strict first-of-each: 8, 4 (users 1, 2, 3, 6; user 4 and 8 fail), 2 (users 1 and 3).
- Chained after the first view: 8, 5 (user 4 now qualifies through the 09:10 cart; user 8 still fails on the tie), 3 (users 1, 3 and 4). User 2 still fails because the purchase at 09:00 is before the cart at 09:40.
- So the same table gives 6, 2 or 3 purchasers depending on the definition.

**Code:** run with `python3 -I`. The assert compares the three rows (any-order, strict, chained) in that order.
```python
# Q7: strictly ordered funnel with MIN(CASE): first-of-each versus a chained (greedy) funnel, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 09:00:00','purchase'),(2,'2024-03-01 09:30:00','view'),(2,'2024-03-01 09:40:00','cart'),
 (3,'2024-03-01 10:00:00','view'),(3,'2024-03-01 10:05:00','cart'),(3,'2024-03-01 10:07:00','cart'),(3,'2024-03-01 10:20:00','purchase'),
 (4,'2024-03-01 08:00:00','cart'),(4,'2024-03-01 09:00:00','view'),(4,'2024-03-01 09:10:00','cart'),(4,'2024-03-01 09:30:00','purchase'),
 (5,'2024-03-01 11:00:00','view'),(5,'2024-03-01 11:05:00','purchase'),
 (6,'2024-03-01 12:00:00','view'),(6,'2024-03-01 12:05:00','cart'),
 (7,'2024-03-01 13:00:00','view'),(7,'2024-03-01 13:01:00','view'),
 (8,'2024-03-01 12:00:00','view'),(8,'2024-03-01 12:00:00','cart'),(8,'2024-03-01 12:10:00','purchase');
"""
SQL_FIRST = """
WITH f AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view'     THEN event_ts END) AS first_view,
         MIN(CASE WHEN event_name = 'cart'     THEN event_ts END) AS first_cart,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY user_id
)
SELECT COUNT(first_view) AS viewed,
       COUNT(CASE WHEN first_view < first_cart THEN 1 END) AS carted,
       COUNT(CASE WHEN first_view < first_cart AND first_cart < first_purchase THEN 1 END) AS purchased
FROM f
"""
SQL_ANY = """
SELECT COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END) AS viewed,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END) AS carted,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchased
FROM events
"""
SQL_CHAIN = """
WITH v AS (SELECT user_id, MIN(event_ts) AS t1 FROM events WHERE event_name = 'view' GROUP BY user_id),
c AS (SELECT v.user_id, MIN(e.event_ts) AS t2
      FROM v JOIN events e ON e.user_id = v.user_id AND e.event_name = 'cart' AND e.event_ts > v.t1
      GROUP BY v.user_id),
p AS (SELECT c.user_id, MIN(e.event_ts) AS t3
      FROM c JOIN events e ON e.user_id = c.user_id AND e.event_name = 'purchase' AND e.event_ts > c.t2
      GROUP BY c.user_id)
SELECT (SELECT COUNT(*) FROM v) AS viewed, (SELECT COUNT(*) FROM c) AS carted, (SELECT COUNT(*) FROM p) AS purchased
"""
SQL_PER_USER = """
SELECT user_id,
       MIN(CASE WHEN event_name = 'view' THEN substr(event_ts, 12, 5) END) AS first_view,
       MIN(CASE WHEN event_name = 'cart' THEN substr(event_ts, 12, 5) END) AS first_cart,
       MIN(CASE WHEN event_name = 'purchase' THEN substr(event_ts, 12, 5) END) AS first_purchase
FROM events GROUP BY user_id ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print(pd.read_sql_query(SQL_PER_USER, con).to_string(index=False))
res = {}
for name, q in [("any-order", SQL_ANY), ("strict first-of-each", SQL_FIRST), ("chained after first view", SQL_CHAIN)]:
    res[name] = pd.read_sql_query(q, con).iloc[0]
sql_df = pd.DataFrame(res).T
print(sql_df.to_string())

events = pd.read_sql_query("SELECT * FROM events", con)
events["event_ts"] = pd.to_datetime(events["event_ts"])
# pd:main
first = events.groupby(["user_id", "event_name"])["event_ts"].min().unstack()
any_order = first[["view", "cart", "purchase"]].notna().sum()
ok2 = first["view"] < first["cart"]
ok3 = ok2 & (first["cart"] < first["purchase"])
strict = pd.Series({"viewed": first["view"].notna().sum(), "carted": ok2.sum(), "purchased": ok3.sum()})
# chained: cart must be after the first view, purchase after that cart
v = first["view"].dropna().rename("t1").reset_index()
carts = events[events["event_name"] == "cart"][["user_id", "event_ts"]]
c = v.merge(carts, on="user_id")
c = c[c["event_ts"] > c["t1"]].groupby("user_id", as_index=False)["event_ts"].min().rename(columns={"event_ts": "t2"})
purchases = events[events["event_name"] == "purchase"][["user_id", "event_ts"]]
p = c.merge(purchases, on="user_id")
p = p[p["event_ts"] > p["t2"]].groupby("user_id", as_index=False)["event_ts"].min()
chain = pd.Series({"viewed": len(v), "carted": len(c), "purchased": len(p)})
# pd:end
pd_df = pd.DataFrame({"any-order": any_order.to_numpy(), "strict first-of-each": strict.to_numpy(),
                      "chained after first view": chain.to_numpy()},
                     index=["viewed", "carted", "purchased"]).T
print(pd_df.to_string())
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # rows: any-order, strict, chained
print("asserts passed")
```

**Output (my run):**
```text
 user_id first_view first_cart first_purchase
       1      10:00      10:05          10:10
       2      09:30      09:40          09:00
       3      10:00      10:05          10:20
       4      09:00      08:00          09:30
       5      11:00        NaN          11:05
       6      12:00      12:05            NaN
       7      13:00        NaN            NaN
       8      12:00      12:00          12:10
                          viewed  carted  purchased
any-order                      8       6          6
strict first-of-each           8       4          2
chained after first view       8       5          3
                          viewed  carted  purchased
any-order                      8       6          6
strict first-of-each           8       4          2
chained after first view       8       5          3
asserts passed
```

**Edge cases:**
- Strict `<` versus `<=`: user 8's equal timestamps fail under `<`. With one-second timestamps ties are common in batched events; state the rule, and add an event id tie-breaker if the ordering of simultaneous events is known.
- Why "first of each" can be wrong: user 4's first cart (08:00) came before the first view, so the strict test fails, yet view 09:00, cart 09:10, purchase 09:30 is a valid sequence. It matters when carts can happen without a view in the same visit (saved carts, deep links, an app re-open); it does not matter if the product enforces the order.
- Greedy chaining is exact for "does a valid sequence exist": starting from the earliest view, then the earliest later cart, then the earliest later purchase can only help.
- A purchase before the first view (user 2) is excluded from the strict funnel but still counts in the any-order table; the gap between those two numbers is a data-quality signal.
- Repeated events (user 3's second cart) do not matter because only the first qualifying one is used.
- No time window yet: Q17 adds one.

**Then explain:**
- Conditional `MIN` is a pivot without PIVOT: one row per user, one column per step.
- `COUNT(col)` skips NULL, so users who never did the step fall out automatically.
- Comparisons with NULL are NULL, not false; `COUNT(CASE WHEN ... THEN 1 END)` handles that correctly.
- The three definitions answer different product questions; the interviewer expects you to name which one you computed.
- Dialects (not executed here): PostgreSQL and BigQuery can do the same with `MIN(...) FILTER (WHERE ...)` and `MIN(IF(...))`; some warehouses have a built-in funnel function (for example ClickHouse `windowFunnel`); not executed.

**Follow-ups:**
- Add a 7-day limit between steps? Add `AND e.event_ts <= datetime(v.t1, '+7 days')` (Q17).
- Do I need the first view as the anchor? The latest view before the purchase answers a different, attempt-level question (Q40).
- What about a step that is optional? Skip it from the chain and report it separately (Q35).

**Common mistakes:**
- Comparing first timestamps and thinking it handles every valid sequence.
- `<=` without thinking about same-second events.
- Counting any-order and strict on different populations.
- Using `MIN` of the wrong column (for example `MIN(event_name)`).

### Q8 ⭐⭐⭐ 🟡 Funnel by channel: events(user_id, event_ts, event_name, channel) with event_name in ('view', 'cart', 'purchase') and channel possibly NULL, and users(user_id, signup_date, country, is_test). Return one row per channel (NULL shown as 'unknown') with distinct users at each step and the view-to-purchase conversion, excluding test users, ordered by view users descending. Explain why channel must be taken from the same event (or from a defined attribution rule) and not joined from a table that can repeat a user, and what a user who appears in two channels does to the totals (the channel rows add up to more than the distinct user total).
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** Group the events by the channel on the event itself (NULL shown as 'unknown'), count distinct users per step with conditional `COUNT(DISTINCT ...)`, join only to `users` (one row per user) to drop test users, and remember that a user who appears in two channels is counted in both, so the channel rows add up to more than the distinct user total and a channel can even show more than 100% conversion.

**Schema and sample data:** seven real users and one test user (8). User 2 views from `ads` but carts and purchases from `email`. User 3 views and carts from `organic` and purchases from `partner` (a channel with no view). User 4 has NULL channels. User 6 views from two channels. `user_channel` is a deliberately bad helper table in which user 2 appears twice.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT, channel TEXT);
CREATE TABLE user_channel(user_id INTEGER, channel TEXT);
INSERT INTO users VALUES (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','IN',0),(4,'2024-01-01','IN',0),
 (5,'2024-01-01','IN',0),(6,'2024-01-01','IN',0),(7,'2024-01-01','IN',0),(8,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view','ads'),(1,'2024-03-01 10:05:00','cart','ads'),(1,'2024-03-01 10:10:00','purchase','ads'),
 (2,'2024-03-01 11:00:00','view','ads'),(2,'2024-03-02 09:00:00','cart','email'),(2,'2024-03-02 09:10:00','purchase','email'),
 (3,'2024-03-01 12:00:00','view','organic'),(3,'2024-03-01 12:05:00','cart','organic'),(3,'2024-03-01 12:30:00','purchase','partner'),
 (4,'2024-03-01 13:00:00','view',NULL),(4,'2024-03-01 13:10:00','purchase',NULL),
 (5,'2024-03-01 14:00:00','view','ads'),
 (6,'2024-03-01 15:00:00','view','organic'),(6,'2024-03-01 15:05:00','view','ads'),(6,'2024-03-01 15:10:00','purchase','organic'),
 (7,'2024-03-01 16:00:00','view','email'),(7,'2024-03-01 16:05:00','cart','email'),(7,'2024-03-01 16:10:00','purchase','email'),
 (8,'2024-03-01 17:00:00','view','ads'),(8,'2024-03-01 17:10:00','purchase','ads');
INSERT INTO user_channel VALUES (1,'ads'),(2,'ads'),(2,'email'),(3,'organic'),(4,'ads'),(5,'ads'),(6,'organic'),(7,'email');
```

**SQL answer:** `SQL_MAIN` in the Code block. `users` has one row per user, so the join cannot repeat events.
```sql
SELECT COALESCE(e.channel, 'unknown') AS channel,
       COUNT(DISTINCT CASE WHEN e.event_name = 'view'     THEN e.user_id END) AS view_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'cart'     THEN e.user_id END) AS cart_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END) AS purchase_users,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN e.event_name = 'view' THEN e.user_id END), 0), 1) AS view_to_purchase_pct
FROM events e
JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
GROUP BY COALESCE(e.channel, 'unknown')
ORDER BY view_users DESC, channel
```
`SQL_FIRST_TOUCH` in the Code block applies a defined attribution rule instead: each user gets the channel of their first event, so every user is in exactly one channel. `SQL_WRONG_JOIN` joins events to the repeating `user_channel` table.

**pandas answer:** shown once, identical to the Code block (`fillna('unknown')` before the groupby, because a default groupby drops NaN keys):
```py
e = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
e["channel"] = e["channel"].fillna("unknown")
cnt = (e.groupby(["channel", "event_name"])["user_id"].nunique().unstack(fill_value=0)
        .reindex(columns=["view", "cart", "purchase"], fill_value=0))
cnt.columns = ["view_users", "cart_users", "purchase_users"]
cnt["view_to_purchase_pct"] = (100.0 * cnt["purchase_users"] / cnt["view_users"].where(cnt["view_users"] > 0)).round(1)
pd_df = (cnt.reset_index().sort_values(["view_users", "channel"], ascending=[False, True])
            .reset_index(drop=True))
```

**Example:** non-test users 1 to 7.
- ads: view users 1, 2, 5, 6 = 4; cart user 1 = 1; purchase user 1 = 1; 25.0%.
- organic: view users 3, 6 = 2; cart 3; purchase user 6; 50.0%.
- email: view user 7 = 1; cart users 2 and 7 = 2; purchase users 2 and 7 = 2; 200.0% (two purchasers from one viewer, because user 2's view was in `ads`).
- unknown: view user 4 = 1, purchase user 4: 100.0%. partner: view 0, purchase user 3: NULL conversion (no views).
- Channel rows sum to 8 view users, but only 7 distinct users viewed (user 6 is in two channels); purchases sum to 6, which happens to equal the distinct purchasers here.
- Under the first-touch rule: ads 3 views, 2 purchasers, 66.7%; organic 2, 2, 100.0%; email 1, 1, 100.0%; unknown 1, 1, 100.0%. Views sum to 7, which is the distinct total. Conversion can no longer exceed 100%.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas frames after ordering by `view_users` descending then `channel` ascending (ties email/unknown by name, partner last with 0 views).
```python
# Q8: funnel by channel (channel taken from the same event, NULL shown as 'unknown'), SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT, channel TEXT);
CREATE TABLE user_channel(user_id INTEGER, channel TEXT);
INSERT INTO users VALUES (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','IN',0),(4,'2024-01-01','IN',0),
 (5,'2024-01-01','IN',0),(6,'2024-01-01','IN',0),(7,'2024-01-01','IN',0),(8,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view','ads'),(1,'2024-03-01 10:05:00','cart','ads'),(1,'2024-03-01 10:10:00','purchase','ads'),
 (2,'2024-03-01 11:00:00','view','ads'),(2,'2024-03-02 09:00:00','cart','email'),(2,'2024-03-02 09:10:00','purchase','email'),
 (3,'2024-03-01 12:00:00','view','organic'),(3,'2024-03-01 12:05:00','cart','organic'),(3,'2024-03-01 12:30:00','purchase','partner'),
 (4,'2024-03-01 13:00:00','view',NULL),(4,'2024-03-01 13:10:00','purchase',NULL),
 (5,'2024-03-01 14:00:00','view','ads'),
 (6,'2024-03-01 15:00:00','view','organic'),(6,'2024-03-01 15:05:00','view','ads'),(6,'2024-03-01 15:10:00','purchase','organic'),
 (7,'2024-03-01 16:00:00','view','email'),(7,'2024-03-01 16:05:00','cart','email'),(7,'2024-03-01 16:10:00','purchase','email'),
 (8,'2024-03-01 17:00:00','view','ads'),(8,'2024-03-01 17:10:00','purchase','ads');
INSERT INTO user_channel VALUES (1,'ads'),(2,'ads'),(2,'email'),(3,'organic'),(4,'ads'),(5,'ads'),(6,'organic'),(7,'email');
"""
SQL_MAIN = """
SELECT COALESCE(e.channel, 'unknown') AS channel,
       COUNT(DISTINCT CASE WHEN e.event_name = 'view'     THEN e.user_id END) AS view_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'cart'     THEN e.user_id END) AS cart_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END) AS purchase_users,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN e.event_name = 'view' THEN e.user_id END), 0), 1) AS view_to_purchase_pct
FROM events e
JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
GROUP BY COALESCE(e.channel, 'unknown')
ORDER BY view_users DESC, channel
"""
# defined attribution rule: the channel of the user's first event, one channel per user
SQL_FIRST_TOUCH = """
WITH ft AS (
  SELECT user_id, COALESCE(channel, 'unknown') AS channel,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts) AS rn
  FROM events
), c AS (SELECT user_id, channel FROM ft WHERE rn = 1)
SELECT c.channel,
       COUNT(DISTINCT CASE WHEN e.event_name = 'view'     THEN e.user_id END) AS view_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'cart'     THEN e.user_id END) AS cart_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END) AS purchase_users,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN e.event_name = 'view' THEN e.user_id END), 0), 1) AS view_to_purchase_pct
FROM events e JOIN c ON c.user_id = e.user_id JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
GROUP BY c.channel ORDER BY view_users DESC, c.channel
"""
SQL_TOTALS = """
SELECT COUNT(DISTINCT CASE WHEN e.event_name='view' THEN e.user_id END) AS distinct_viewers,
       COUNT(DISTINCT CASE WHEN e.event_name='purchase' THEN e.user_id END) AS distinct_purchasers,
       COUNT(CASE WHEN e.event_name='purchase' THEN 1 END) AS purchase_events
FROM events e JOIN users u ON u.user_id = e.user_id WHERE u.is_test = 0
"""
SQL_WRONG_JOIN = """
SELECT COUNT(*) AS purchase_rows_after_join
FROM events e JOIN users u ON u.user_id = e.user_id JOIN user_channel uc ON uc.user_id = e.user_id
WHERE u.is_test = 0 AND e.event_name = 'purchase'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("same-event channel:"); print(sql_df.to_string(index=False))
print("channel rows add up to: view", sql_df["view_users"].sum(), "cart", sql_df["cart_users"].sum(),
      "purchase", sql_df["purchase_users"].sum())
print(pd.read_sql_query(SQL_TOTALS, con).to_string(index=False))
print("one channel per user (first event):"); print(pd.read_sql_query(SQL_FIRST_TOUCH, con).to_string(index=False))
print(pd.read_sql_query(SQL_WRONG_JOIN, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
e = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
e["channel"] = e["channel"].fillna("unknown")
cnt = (e.groupby(["channel", "event_name"])["user_id"].nunique().unstack(fill_value=0)
        .reindex(columns=["view", "cart", "purchase"], fill_value=0))
cnt.columns = ["view_users", "cart_users", "purchase_users"]
cnt["view_to_purchase_pct"] = (100.0 * cnt["purchase_users"] / cnt["view_users"].where(cnt["view_users"] > 0)).round(1)
pd_df = (cnt.reset_index().sort_values(["view_users", "channel"], ascending=[False, True])
            .reset_index(drop=True))
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # ordered by view_users desc, channel asc
print("asserts passed")
# what a default groupby does with the NaN channel
lost = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
print("groupby default keeps channels:", sorted(lost.groupby("channel")["user_id"].nunique().index),
      "| dropna=False:", lost.groupby("channel", dropna=False)["user_id"].nunique().index.tolist())
```

**Output (my run):**
```text
same-event channel:
channel  view_users  cart_users  purchase_users  view_to_purchase_pct
    ads           4           1               1                  25.0
organic           2           1               1                  50.0
  email           1           2               2                 200.0
unknown           1           0               1                 100.0
partner           0           0               1                   NaN
channel rows add up to: view 8 cart 4 purchase 6
 distinct_viewers  distinct_purchasers  purchase_events
                7                    6                6
one channel per user (first event):
channel  view_users  cart_users  purchase_users  view_to_purchase_pct
    ads           3           2               2                  66.7
organic           2           1               2                 100.0
  email           1           1               1                 100.0
unknown           1           0               1                 100.0
 purchase_rows_after_join
                        7
pandas:
channel  view_users  cart_users  purchase_users  view_to_purchase_pct
    ads           4           1               1                  25.0
organic           2           1               1                  50.0
  email           1           2               2                 200.0
unknown           1           0               1                 100.0
partner           0           0               1                   NaN
asserts passed
groupby default keeps channels: ['ads', 'email', 'organic', 'partner'] | dropna=False: ['ads', 'email', 'organic', 'partner', nan]
```

**Edge cases:**
- Channel from the event is a definition, not a truth: it says where each action came from. A conversion above 100% (email 200.0%) is the signal that the steps are attributed to different channels; then a per-user rule (first touch, last touch before the purchase) is the right frame (Q20).
- NULL channel: `GROUP BY channel` keeps a NULL group in SQL; `COALESCE(channel, 'unknown')` names it. In pandas a default `groupby` drops NaN keys: in my run the default groupby on this data listed only ads, email, organic, partner, and `dropna=False` added the NaN group. The `fillna` in the answer is what keeps the unknown row.
- A channel with zero view users gives NULL conversion via `NULLIF`, not an error (partner).
- Joining a table that repeats users: joining events to `user_channel` gave 7 purchase rows for 6 purchase events in my run, because user 2 matched twice. Even `COUNT(DISTINCT user_id)` would hide this while `COUNT(*)` or `SUM(amount)` would not.
- Test users: the test user's view and purchase (both `ads`) would add 1 to ads views and 1 to ads purchases; the join with `is_test = 0` removes both.
- Users with no row in `users` drop out of the inner join.

**Then explain:**
- Take the channel from the event itself, or from one declared rule; do not join a user-to-channel table that can have several rows per user.
- Distinct users per channel are not additive across channels. Report the distinct total separately.
- Show counts next to the percentage; a rate on 1 viewer is noise.
- Dialects (not executed here): BigQuery `COUNT(DISTINCT IF(...))`, PostgreSQL `FILTER`; `COALESCE` is standard everywhere.

**Follow-ups:**
- Channel rows must add up to the total? Use a one-channel-per-user rule (shown).
- Order within the funnel? Combine with Q7.
- Conversion of NULL channel as a data-quality metric? Report the share of events with NULL channel.

**Common mistakes:**
- Joining a many-row channel table and counting rows.
- Dropping the NULL channel (silently in pandas).
- Reporting channel conversion above 100% without explaining it.
- Summing channel rows and calling it the total.

### Q9 ⭐⭐⭐ 🟡 Debugging: my funnel step 3 is bigger than step 2. events(user_id, event_ts, event_name) with steps 'view', 'cart', 'purchase'. A dashboard shows 1,000 view users, 150 cart users and 180 purchase users. List at least five causes (purchase without a cart event because of express checkout or a tracking gap, counting events instead of users, steps that were not restricted to users who passed the earlier step, duplicate purchase events, a different date filter on each step, test users in one step only), build a small table that reproduces three of them and show the corrected cumulative funnel where each step requires the previous one (or states clearly that it does not).
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** A later step can only be larger than an earlier one if the steps are not nested: purchases without a cart event (express checkout or tracking gaps), purchase events counted instead of users, test users in one step only, duplicate purchase events, and different filters per step all do it; the fix is to count distinct non-test users and make each step require the previous one, saying clearly that this checks presence, not time order.

**Causes (at least five):**
1. Purchase without a cart event: express checkout, buy-now button, a tracking gap or an ad blocker that drops the cart event.
2. Counting events instead of users: a retried or double-clicked purchase counts twice.
3. Steps not restricted to users who passed the earlier step: the purchase count includes users who never carted.
4. Duplicate purchase events from client retries or server and client both logging.
5. A different date filter on each step (purchases counted over a longer period than views).
6. Test or internal users filtered from one step only, or present only in the purchase step.
7. Identity changes: the same person counted under an anonymous id at the view and a logged-in id at the purchase (not reproduced here).

**Schema and sample data:** I reproduce three causes: express checkout (users 3 and 10 purchase without a cart), purchase events counted instead of users (user 2 purchases twice, two seconds apart) and a test user (9) who only purchases.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,1),(10,0);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),(2,'2024-03-01 11:10:00','purchase'),(2,'2024-03-01 11:10:02','purchase'),
 (3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:03:00','purchase'),
 (4,'2024-03-01 13:00:00','view'),(4,'2024-03-01 13:05:00','cart'),
 (5,'2024-03-01 14:00:00','view'),
 (6,'2024-03-01 15:00:00','view'),(6,'2024-03-01 15:05:00','cart'),(6,'2024-03-01 15:10:00','purchase'),
 (7,'2024-03-01 16:00:00','view'),(7,'2024-03-01 16:05:00','cart'),
 (8,'2024-03-01 17:00:00','view'),
 (9,'2024-03-01 18:00:00','purchase'),
 (10,'2024-03-01 19:00:00','view'),(10,'2024-03-01 19:02:00','purchase');
```

**SQL answer:** four queries in the Code block, one per row of the result: `SQL_NAIVE` (distinct users for view and cart but purchase events, test users in), `SQL_USERS` (distinct users everywhere), `SQL_NOTEST` (test users removed) and the corrected cumulative funnel `SQL_CUM`:
```sql
WITH f AS (
  SELECT e.user_id,
         MAX(e.event_name = 'view') AS v, MAX(e.event_name = 'cart') AS c, MAX(e.event_name = 'purchase') AS p
  FROM events e JOIN users u ON u.user_id = e.user_id
  WHERE u.is_test = 0
  GROUP BY e.user_id
)
SELECT 'cumulative: each step needs the previous (presence, not order)' AS version,
       SUM(v), SUM(v * c), SUM(v * c * p)
FROM f
```
`SQL_SKIP` lists the purchasers with no cart event.

**pandas answer:** shown once, identical to the Code block (`counts` for the first three rows, a user by step flag table from `crosstab` for the cumulative row):
```py
def counts(ev, purchase_as_events=False):
    n = ev.groupby("event_name")["user_id"].nunique()
    p = (ev["event_name"] == "purchase").sum() if purchase_as_events else n.get("purchase", 0)
    return [n.get("view", 0), n.get("cart", 0), p]

clean = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
flags = pd.crosstab(clean["user_id"], clean["event_name"]).clip(upper=1).reindex(
    columns=["view", "cart", "purchase"], fill_value=0)
cum = [flags["view"].sum(), (flags["view"] * flags["cart"]).sum(),
       (flags["view"] * flags["cart"] * flags["purchase"]).sum()]
rows = [["naive: purchase events, test users in"] + counts(events, True),
        ["distinct users, test users in"] + counts(events),
        ["distinct users, test users out"] + counts(clean),
        ["cumulative: each step needs the previous (presence, not order)"] + cum]
pd_df = pd.DataFrame(rows, columns=["version", "view_n", "cart_n", "purchase_n"])
```

**Example:** nine users have a view (1 to 8 and 10), five have a cart (1, 2, 4, 6, 7).
- Naive dashboard: 9 view users, 5 cart users, 7 purchase events (users 1, 2 twice, 3, 6, 9, 10): step 3 is bigger than step 2.
- Distinct users instead of events: 6 purchasers (1, 2, 3, 6, 9, 10): still more than 5 cart users.
- Drop the test user 9: 5 purchasers, no longer greater, but it includes users 3 and 10 who never carted.
- Cumulative (each step needs the previous one): 9 viewed, 5 carted, 3 purchased (users 1, 2, 6). The funnel is now monotone.
- Express-checkout purchasers (3 and 10) are not lost; report them as their own number (2 in my run), because they are real revenue.

**Code:** run with `python3 -I`. The assert compares the four rows in the printed order.
```python
# Q9: why funnel step 3 can exceed step 2: reproduce three causes, then a corrected cumulative funnel
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,1),(10,0);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),(2,'2024-03-01 11:10:00','purchase'),(2,'2024-03-01 11:10:02','purchase'),
 (3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:03:00','purchase'),
 (4,'2024-03-01 13:00:00','view'),(4,'2024-03-01 13:05:00','cart'),
 (5,'2024-03-01 14:00:00','view'),
 (6,'2024-03-01 15:00:00','view'),(6,'2024-03-01 15:05:00','cart'),(6,'2024-03-01 15:10:00','purchase'),
 (7,'2024-03-01 16:00:00','view'),(7,'2024-03-01 16:05:00','cart'),
 (8,'2024-03-01 17:00:00','view'),
 (9,'2024-03-01 18:00:00','purchase'),
 (10,'2024-03-01 19:00:00','view'),(10,'2024-03-01 19:02:00','purchase');
"""
# 1 naive: purchase EVENTS, test users in; 2 distinct users; 3 drop test users; 4 each step requires the previous one
SQL_NAIVE = """
SELECT 'naive: purchase events, test users in' AS version,
       COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END) AS view_n,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END) AS cart_n,
       COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) AS purchase_n
FROM events
"""
SQL_USERS = """
SELECT 'distinct users, test users in',
       COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END),
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END),
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END)
FROM events
"""
SQL_NOTEST = """
SELECT 'distinct users, test users out',
       COUNT(DISTINCT CASE WHEN e.event_name = 'view' THEN e.user_id END),
       COUNT(DISTINCT CASE WHEN e.event_name = 'cart' THEN e.user_id END),
       COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END)
FROM events e JOIN users u ON u.user_id = e.user_id WHERE u.is_test = 0
"""
SQL_CUM = """
WITH f AS (
  SELECT e.user_id,
         MAX(e.event_name = 'view') AS v, MAX(e.event_name = 'cart') AS c, MAX(e.event_name = 'purchase') AS p
  FROM events e JOIN users u ON u.user_id = e.user_id
  WHERE u.is_test = 0
  GROUP BY e.user_id
)
SELECT 'cumulative: each step needs the previous (presence, not order)' AS version,
       SUM(v), SUM(v * c), SUM(v * c * p)
FROM f
"""
SQL_SKIP = """
SELECT e.user_id FROM events e JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0 GROUP BY e.user_id
HAVING MAX(e.event_name = 'purchase') = 1 AND MAX(e.event_name = 'cart') = 0 ORDER BY e.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
cols = ["version", "view_n", "cart_n", "purchase_n"]
sql_rows = []
for q in (SQL_NAIVE, SQL_USERS, SQL_NOTEST, SQL_CUM):
    sql_rows.append(list(con.execute(q).fetchone()))
sql_df = pd.DataFrame(sql_rows, columns=cols)
print(sql_df.to_string(index=False))
print("purchasers with no cart event (express checkout), test users out:", [r[0] for r in con.execute(SQL_SKIP)])

events = pd.read_sql_query("SELECT * FROM events", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
def counts(ev, purchase_as_events=False):
    n = ev.groupby("event_name")["user_id"].nunique()
    p = (ev["event_name"] == "purchase").sum() if purchase_as_events else n.get("purchase", 0)
    return [n.get("view", 0), n.get("cart", 0), p]

clean = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
flags = pd.crosstab(clean["user_id"], clean["event_name"]).clip(upper=1).reindex(
    columns=["view", "cart", "purchase"], fill_value=0)
cum = [flags["view"].sum(), (flags["view"] * flags["cart"]).sum(),
       (flags["view"] * flags["cart"] * flags["purchase"]).sum()]
rows = [["naive: purchase events, test users in"] + counts(events, True),
        ["distinct users, test users in"] + counts(events),
        ["distinct users, test users out"] + counts(clean),
        ["cumulative: each step needs the previous (presence, not order)"] + cum]
pd_df = pd.DataFrame(rows, columns=["version", "view_n", "cart_n", "purchase_n"])
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # same four rows in the same order
print("asserts passed")
```

**Output (my run):**
```text
                                                       version  view_n  cart_n  purchase_n
                         naive: purchase events, test users in       9       5           7
                                 distinct users, test users in       9       5           6
                                distinct users, test users out       9       5           5
cumulative: each step needs the previous (presence, not order)       9       5           3
purchasers with no cart event (express checkout), test users out: [3, 10]
                                                       version  view_n  cart_n  purchase_n
                         naive: purchase events, test users in       9       5           7
                                 distinct users, test users in       9       5           6
                                distinct users, test users out       9       5           5
cumulative: each step needs the previous (presence, not order)       9       5           3
asserts passed
```

**Edge cases:**
- The cumulative funnel here needs the previous step's event to exist, but not to be earlier in time. Order is Q7, a cumulative funnel with a step index is Q35. If the product allows express checkout, forcing the cart step makes the funnel understate purchases; the honest answer is to show the main path and the bypass count.
- `MAX(event_name = 'view')` returns 0 or 1 per user, so the multiplication `v * c * p` is an AND.
- Duplicate purchase events are removed in the funnel by counting users; for purchase counts you need event-level dedup (Q38).
- Different date filter per step: not reproduced in the code, but the fix is one shared window applied once in a CTE before the step counts.
- An empty step makes every later cumulative count 0, not an error.

**Then explain:**
- A funnel step is a set of users, and a valid funnel has nested sets. If a later set is larger, the sets are not nested, and the debugging method is to list who is in step N but not in step N-1.
- Fix one cause at a time and print the table after each, so the 7, 6, 5 and 3 above explain the gap fully.
- Tell stakeholders that cumulative means "reached the step", not "did it in order".

**Follow-ups:**
- How do I find the users in step 3 but not step 2? A `NOT EXISTS` or a `HAVING MAX(purchase) = 1 AND MAX(cart) = 0` query (`SQL_SKIP`).
- Should express checkout count as a cart step? Product decision: either log a synthetic cart event or make the funnel start at checkout.
- How do I check tracking gaps? Compare against orders in the database.

**Common mistakes:**
- Counting events, not users.
- Test and internal users removed from only one step.
- Reporting a conversion above 100% without investigating.
- Different date ranges or filters per step.
- Forcing each step to include the previous one and hiding the users who bypass it.

### Q10 ⭐⭐⭐ 🟡 Net revenue after refunds without fan-out: orders(order_id, user_id, order_ts, amount, status) and refunds(refund_id, order_id, refund_ts, amount) where an order can have zero, one or several partial refunds. Return net revenue per month (order month) as gross completed amount minus refunded amount, and show the wrong query that joins orders to refunds first and then sums orders.amount (orders with two refunds are counted twice), then two correct fixes: pre-aggregate refunds to one row per order before the join, or use a scalar subquery. Say what you do with refunds that arrive in a later month than the order (cash view versus order-month view).
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** An order can have several refund rows, so joining orders to refunds and then summing `orders.amount` counts the order once per refund; I pre-aggregate refunds to one row per order (or use a scalar subquery) before summing, and I state whether refunds are charged to the order month or to the month they were paid.

**Schema and sample data:** six orders and four refunds. Order 1 (completed, 100) has two refunds, one in January and one in February. Order 3 is fully refunded. Order 5 (February) is refunded in March. Order 4 is cancelled and ignored.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
```

**SQL answer:** the wrong query `SQL_WRONG`, then fix 1 `SQL_PREAGG` and fix 2 `SQL_SCALAR`, and the cash view `SQL_CASH`, all in the Code block. Wrong:
```sql
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(o.amount) AS gross_wrong, SUM(COALESCE(r.amount, 0)) AS refunded,
       SUM(o.amount) - SUM(COALESCE(r.amount, 0)) AS net_wrong
FROM orders o LEFT JOIN refunds r ON r.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
```
Fix 1, pre-aggregate refunds to the order grain:
```sql
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(o.amount) AS gross,
       COALESCE(SUM(r.refunded), 0) AS refunded,
       SUM(o.amount) - COALESCE(SUM(r.refunded), 0) AS net
FROM orders o
LEFT JOIN (SELECT order_id, SUM(amount) AS refunded FROM refunds GROUP BY order_id) r
       ON r.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
```
Fix 2, scalar subquery per order (the same result, one correlated lookup per order):
```sql
WITH x AS (
  SELECT strftime('%Y-%m', o.order_ts) AS month, o.amount,
         COALESCE((SELECT SUM(r.amount) FROM refunds r WHERE r.order_id = o.order_id), 0) AS refunded
  FROM orders o WHERE o.status = 'completed'
)
SELECT month, SUM(amount) AS gross, SUM(refunded) AS refunded, SUM(amount) - SUM(refunded) AS net
FROM x GROUP BY month ORDER BY month
```
Cash view, each refund charged to the month it is paid:
```sql
WITH ev AS (
  SELECT strftime('%Y-%m', order_ts) AS month, amount AS a FROM orders WHERE status = 'completed'
  UNION ALL
  SELECT strftime('%Y-%m', r.refund_ts), -r.amount
  FROM refunds r JOIN orders o ON o.order_id = r.order_id WHERE o.status = 'completed'
)
SELECT month, SUM(a) AS net_cash FROM ev GROUP BY month ORDER BY month
```

**pandas answer:** shown once, identical to the Code block (sum refunds per order first, then a left merge):
```py
done = orders[orders["status"] == "completed"].copy()
done["month"] = done["order_ts"].str[:7]
per_order = refunds.groupby("order_id")["amount"].sum().rename("refunded")
j = done.merge(per_order, on="order_id", how="left").fillna({"refunded": 0.0})
pd_df = (j.groupby("month", as_index=False)
          .agg(gross=("amount", "sum"), refunded=("refunded", "sum")))
pd_df["net"] = pd_df["gross"] - pd_df["refunded"]
```

**Example:** order-month view.
- January: completed orders 1 (100) and 2 (200), gross 300. Refunds on January orders: 30 + 20 = 50 on order 1. Net = 250.
- February: orders 3 (150) and 5 (50), gross 200. Refunds: 150 (order 3) + 10 (order 5, paid in March) = 160. Net = 40.
- March: order 6 (120), no refunds. Net = 120.
- Wrong query: order 1 has two refund rows, so after the join it appears twice and January gross becomes 100 + 100 + 200 = 400, net 350 instead of 250. February and March are right only because their orders have at most one refund.
- Cash view: January 300 - 30 = 270, February 200 - 170 (20 for order 1 and 150 for order 3) = 30, March 120 - 10 = 110.

**Code:** run with `python3 -I`. Fix 1 and fix 2 are asserted equal, then pandas is asserted equal to fix 1, all ordered by month.
```python
# Q10: net revenue after refunds without fan-out (order-month view, plus a cash view), SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
"""
SQL_WRONG = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(o.amount) AS gross_wrong, SUM(COALESCE(r.amount, 0)) AS refunded,
       SUM(o.amount) - SUM(COALESCE(r.amount, 0)) AS net_wrong
FROM orders o LEFT JOIN refunds r ON r.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
"""
SQL_PREAGG = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(o.amount) AS gross,
       COALESCE(SUM(r.refunded), 0) AS refunded,
       SUM(o.amount) - COALESCE(SUM(r.refunded), 0) AS net
FROM orders o
LEFT JOIN (SELECT order_id, SUM(amount) AS refunded FROM refunds GROUP BY order_id) r
       ON r.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
"""
SQL_SCALAR = """
WITH x AS (
  SELECT strftime('%Y-%m', o.order_ts) AS month, o.amount,
         COALESCE((SELECT SUM(r.amount) FROM refunds r WHERE r.order_id = o.order_id), 0) AS refunded
  FROM orders o WHERE o.status = 'completed'
)
SELECT month, SUM(amount) AS gross, SUM(refunded) AS refunded, SUM(amount) - SUM(refunded) AS net
FROM x GROUP BY month ORDER BY month
"""
SQL_CASH = """
WITH ev AS (
  SELECT strftime('%Y-%m', order_ts) AS month, amount AS a FROM orders WHERE status = 'completed'
  UNION ALL
  SELECT strftime('%Y-%m', r.refund_ts), -r.amount
  FROM refunds r JOIN orders o ON o.order_id = r.order_id WHERE o.status = 'completed'
)
SELECT month, SUM(a) AS net_cash FROM ev GROUP BY month ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("wrong (join first, sum orders.amount):"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))
a = pd.read_sql_query(SQL_PREAGG, con)
b = pd.read_sql_query(SQL_SCALAR, con)
print("fix 1, pre-aggregate refunds:"); print(a.to_string(index=False))
pd.testing.assert_frame_equal(a, b)  # the two fixes agree, ordered by month
cash = pd.read_sql_query(SQL_CASH, con)
print("cash view (refund counted in the month it is paid):"); print(cash.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
done = orders[orders["status"] == "completed"].copy()
done["month"] = done["order_ts"].str[:7]
per_order = refunds.groupby("order_id")["amount"].sum().rename("refunded")
j = done.merge(per_order, on="order_id", how="left").fillna({"refunded": 0.0})
pd_df = (j.groupby("month", as_index=False)
          .agg(gross=("amount", "sum"), refunded=("refunded", "sum")))
pd_df["net"] = pd_df["gross"] - pd_df["refunded"]
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, a, check_dtype=False)  # ordered by month
# the fan-out in pandas: merging refund rows directly repeats order 1
wrong = done.merge(refunds[["order_id", "amount"]].rename(columns={"amount": "r"}), on="order_id", how="left")
print("pandas wrong gross by month:", wrong.groupby("month")["amount"].sum().to_dict())
print("asserts passed")
```

**Output (my run):**
```text
wrong (join first, sum orders.amount):
  month  gross_wrong  refunded  net_wrong
2024-01        400.0      50.0      350.0
2024-02        200.0     160.0       40.0
2024-03        120.0       0.0      120.0
fix 1, pre-aggregate refunds:
  month  gross  refunded   net
2024-01  300.0      50.0 250.0
2024-02  200.0     160.0  40.0
2024-03  120.0       0.0 120.0
cash view (refund counted in the month it is paid):
  month  net_cash
2024-01     270.0
2024-02      30.0
2024-03     110.0
pandas:
  month  gross  refunded   net
2024-01  300.0      50.0 250.0
2024-02  200.0     160.0  40.0
2024-03  120.0       0.0 120.0
pandas wrong gross by month: {'2024-01': 400.0, '2024-02': 200.0, '2024-03': 120.0}
asserts passed
```

**Edge cases:**
- `LEFT JOIN` is required, otherwise orders without refunds disappear from the gross (an inner join silently drops order 2 and order 6).
- The same fan-out happens in pandas: merging the raw refund rows into completed orders gave a January gross of 400.0 in my run, the same wrong number.
- Order-month view versus cash view: the order-month view assigns a refund back to the month of its order, so January net changes after February's refund arrives (restatement); the cash view books the refund when it is paid, so history does not move but a month's net can be low because of old orders. Finance often wants cash, product often wants order-month; say which one and label it.
- A refund larger than the order, or a refund on a cancelled order: I excluded cancelled orders from both views; I would flag over-refunds as data errors instead of letting them go negative.
- Orders with no refunds: `COALESCE(..., 0)` is needed because a NULL refund would make `gross - NULL` NULL.
- Currency or partial refund of shipping only: out of scope here.

**Then explain:**
- Fan-out: joining a parent to a many-row child repeats the parent's columns, so any parent-level SUM is multiplied. Aggregate the child to the parent's grain first.
- Pre-aggregation keeps one join and is easy to index; the scalar subquery is clearer but runs once per order (the engine may optimise it, not executed beyond SQLite).
- Check the result by recomputing gross from the orders table alone: it must not change after the join.
- Dialects (not executed here): the same two fixes work in PostgreSQL, MySQL, BigQuery and Snowflake; `strftime` becomes `date_trunc('month', ...)` or `DATE_FORMAT`.

**Follow-ups:**
- Refund rates? See Q11.
- Net revenue per user (LTV net of refunds)? Q22.
- Refunds with no matching order? A `LEFT JOIN` from refunds to orders finds them (data-quality check).

**Common mistakes:**
- Join first, then `SUM(orders.amount)`.
- Inner join that drops unrefunded orders.
- Mixing month bases: orders by order month, refunds by refund month, in one net figure.
- Forgetting `COALESCE`.

### Q11 ⭐⭐⭐ 🟡 Refund rate and cancellation rate: orders(order_id, user_id, order_ts, amount, status) with status in ('completed', 'cancelled') and refunds(refund_id, order_id, refund_ts, amount). Return per month the cancellation rate (cancelled orders over all orders), the refund rate by count (completed orders with at least one refund over completed orders) and the refund rate by value (refunded amount over completed amount). Use EXISTS (or a pre-aggregated join) so an order with two refunds counts once in the count rate, and say why a refund rate is wrong if refunds are counted by refund_ts month while orders are counted by order_ts month.
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** Group orders by order month; cancellation rate is cancelled over all orders, refund rate by count is completed orders with at least one refund over completed orders (pre-aggregate or `EXISTS` so two refunds count once), and refund rate by value is refunded amount over completed amount, with the refund assigned to its order's month so numerator and denominator describe the same orders.

**Schema and sample data:** eleven orders and four refunds. Order 1 has two refunds. April has only a cancelled order, so there are no completed orders at all in that month.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (7,6,'2024-01-25 10:00:00',60,'cancelled'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed'),
 (9,5,'2024-03-20 10:00:00',60,'completed'),
 (8,7,'2024-03-09 10:00:00',40,'cancelled'),
 (10,7,'2024-03-12 10:00:00',25,'cancelled'),
 (11,1,'2024-04-02 10:00:00',70,'cancelled');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
```

**SQL answer:** `SQL_MAIN` in the Code block (refunds pre-aggregated to one row per order, then one pass over orders):
```sql
WITH ref AS (SELECT order_id, SUM(amount) AS refunded FROM refunds GROUP BY order_id)
SELECT strftime('%Y-%m', o.order_ts) AS month,
       COUNT(*) AS orders,
       SUM(o.status = 'cancelled') AS cancelled,
       ROUND(100.0 * SUM(o.status = 'cancelled') / COUNT(*), 1) AS cancel_rate,
       SUM(o.status = 'completed') AS completed,
       SUM(o.status = 'completed' AND r.order_id IS NOT NULL) AS refunded_orders,
       ROUND(100.0 * SUM(o.status = 'completed' AND r.order_id IS NOT NULL)
             / NULLIF(SUM(o.status = 'completed'), 0), 1) AS refund_rate_count,
       ROUND(100.0 * SUM(CASE WHEN o.status = 'completed' THEN COALESCE(r.refunded, 0) END)
             / NULLIF(SUM(CASE WHEN o.status = 'completed' THEN o.amount END), 0), 1) AS refund_rate_value
FROM orders o
LEFT JOIN ref r ON r.order_id = o.order_id
GROUP BY month
ORDER BY month
```
The `EXISTS` form for the count rate is `SQL_EXISTS` in the Code block; the wrong refund-month version is `SQL_WRONG`:
```sql
SELECT strftime('%Y-%m', o.order_ts) AS month,
       ROUND(100.0 * SUM(EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = o.order_id))
             / NULLIF(COUNT(*), 0), 1) AS refund_rate_count
FROM orders o
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
```

**pandas answer:** shown once, identical to the Code block:
```py
o = orders.assign(month=orders["order_ts"].str[:7])
per_order = refunds.groupby("order_id")["amount"].sum().rename("refunded")
o = o.merge(per_order, on="order_id", how="left")
o["is_cancelled"] = o["status"] == "cancelled"
o["is_completed"] = o["status"] == "completed"
o["has_refund"] = o["is_completed"] & o["refunded"].notna()
o["done_amount"] = o["amount"].where(o["is_completed"], 0.0)
o["done_refunded"] = o["refunded"].fillna(0.0).where(o["is_completed"], 0.0)
g = o.groupby("month", as_index=False).agg(
    orders=("order_id", "size"), cancelled=("is_cancelled", "sum"), completed=("is_completed", "sum"),
    refunded_orders=("has_refund", "sum"), done_amount=("done_amount", "sum"), done_refunded=("done_refunded", "sum"))
den = g["completed"].where(g["completed"] > 0)
amt = g["done_amount"].where(g["done_amount"] > 0)
g["cancel_rate"] = (100.0 * g["cancelled"] / g["orders"]).round(1)
g["refund_rate_count"] = (100.0 * g["refunded_orders"] / den).round(1)
g["refund_rate_value"] = (100.0 * g["done_refunded"] / amt).round(1)
pd_df = g[["month", "orders", "cancelled", "cancel_rate", "completed", "refunded_orders",
           "refund_rate_count", "refund_rate_value"]]
```

**Example:** per order month.
- January: 3 orders, 1 cancelled = 33.3% cancellation. Completed 2 (orders 1, 2); order 1 has two refunds, so 1 refunded order of 2 = 50.0% by count. By value: refunded 30 + 20 = 50 over completed 300 = 16.7%.
- February: 3 orders, 1 cancelled = 33.3%. Completed 2 (orders 3, 5), both refunded = 100.0% by count; value (150 + 10) over 200 = 80.0%.
- March: 4 orders, 2 cancelled = 50.0%; 2 completed, none refunded = 0.0% and 0.0%.
- April: 1 order, cancelled = 100.0%; no completed orders, so both refund rates are NULL (undefined), not 0.
- If the refund is joined by refund month instead (wrong), January value is 10.0 (only the 30 paid in January, over 300), February 85.0 (170 over 200: order 1's 20 and order 3's 150) and March count 50.0 and value 5.6 (the 10 paid in March over 180), even though no March order was refunded.

**Code:** run with `python3 -I`. The assert compares pandas to the SQL main result ordered by month; the `EXISTS` rate column is also asserted equal for the three months that have completed orders.
```python
# Q11: cancellation rate, refund rate by count and by value, per order month, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (7,6,'2024-01-25 10:00:00',60,'cancelled'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed'),
 (9,5,'2024-03-20 10:00:00',60,'completed'),
 (8,7,'2024-03-09 10:00:00',40,'cancelled'),
 (10,7,'2024-03-12 10:00:00',25,'cancelled'),
 (11,1,'2024-04-02 10:00:00',70,'cancelled');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
"""
SQL_MAIN = """
WITH ref AS (SELECT order_id, SUM(amount) AS refunded FROM refunds GROUP BY order_id)
SELECT strftime('%Y-%m', o.order_ts) AS month,
       COUNT(*) AS orders,
       SUM(o.status = 'cancelled') AS cancelled,
       ROUND(100.0 * SUM(o.status = 'cancelled') / COUNT(*), 1) AS cancel_rate,
       SUM(o.status = 'completed') AS completed,
       SUM(o.status = 'completed' AND r.order_id IS NOT NULL) AS refunded_orders,
       ROUND(100.0 * SUM(o.status = 'completed' AND r.order_id IS NOT NULL)
             / NULLIF(SUM(o.status = 'completed'), 0), 1) AS refund_rate_count,
       ROUND(100.0 * SUM(CASE WHEN o.status = 'completed' THEN COALESCE(r.refunded, 0) END)
             / NULLIF(SUM(CASE WHEN o.status = 'completed' THEN o.amount END), 0), 1) AS refund_rate_value
FROM orders o
LEFT JOIN ref r ON r.order_id = o.order_id
GROUP BY month
ORDER BY month
"""
SQL_EXISTS = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       ROUND(100.0 * SUM(EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = o.order_id))
             / NULLIF(COUNT(*), 0), 1) AS refund_rate_count
FROM orders o
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
"""
# wrong: refunds bucketed by refund_ts month over completed orders by order_ts month
SQL_WRONG = """
WITH o AS (SELECT strftime('%Y-%m', order_ts) AS month, COUNT(*) AS completed, SUM(amount) AS amt
           FROM orders WHERE status = 'completed' GROUP BY month),
r AS (SELECT strftime('%Y-%m', r.refund_ts) AS month, COUNT(*) AS refund_rows, SUM(r.amount) AS refunded
      FROM refunds r JOIN orders x ON x.order_id = r.order_id WHERE x.status = 'completed' GROUP BY month)
SELECT o.month, ROUND(100.0 * COALESCE(r.refund_rows, 0) / o.completed, 1) AS refund_rate_count_wrong,
       ROUND(100.0 * COALESCE(r.refunded, 0) / o.amt, 1) AS refund_rate_value_wrong
FROM o LEFT JOIN r ON r.month = o.month ORDER BY o.month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
ex = pd.read_sql_query(SQL_EXISTS, con)
print("EXISTS version of the count rate:"); print(ex.to_string(index=False))
print("wrong (refund month over order month):"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
o = orders.assign(month=orders["order_ts"].str[:7])
per_order = refunds.groupby("order_id")["amount"].sum().rename("refunded")
o = o.merge(per_order, on="order_id", how="left")
o["is_cancelled"] = o["status"] == "cancelled"
o["is_completed"] = o["status"] == "completed"
o["has_refund"] = o["is_completed"] & o["refunded"].notna()
o["done_amount"] = o["amount"].where(o["is_completed"], 0.0)
o["done_refunded"] = o["refunded"].fillna(0.0).where(o["is_completed"], 0.0)
g = o.groupby("month", as_index=False).agg(
    orders=("order_id", "size"), cancelled=("is_cancelled", "sum"), completed=("is_completed", "sum"),
    refunded_orders=("has_refund", "sum"), done_amount=("done_amount", "sum"), done_refunded=("done_refunded", "sum"))
den = g["completed"].where(g["completed"] > 0)
amt = g["done_amount"].where(g["done_amount"] > 0)
g["cancel_rate"] = (100.0 * g["cancelled"] / g["orders"]).round(1)
g["refund_rate_count"] = (100.0 * g["refunded_orders"] / den).round(1)
g["refund_rate_value"] = (100.0 * g["done_refunded"] / amt).round(1)
pd_df = g[["month", "orders", "cancelled", "cancel_rate", "completed", "refunded_orders",
           "refund_rate_count", "refund_rate_value"]]
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # ordered by month
pd.testing.assert_series_equal(ex["refund_rate_count"].iloc[:3].reset_index(drop=True),
                               sql_df["refund_rate_count"].iloc[:3].reset_index(drop=True))
print("asserts passed")
```

**Output (my run):**
```text
  month  orders  cancelled  cancel_rate  completed  refunded_orders  refund_rate_count  refund_rate_value
2024-01       3          1         33.3          2                1               50.0               16.7
2024-02       3          1         33.3          2                2              100.0               80.0
2024-03       4          2         50.0          2                0                0.0                0.0
2024-04       1          1        100.0          0                0                NaN                NaN
EXISTS version of the count rate:
  month  refund_rate_count
2024-01               50.0
2024-02              100.0
2024-03                0.0
wrong (refund month over order month):
  month  refund_rate_count_wrong  refund_rate_value_wrong
2024-01                     50.0                     10.0
2024-02                    100.0                     85.0
2024-03                     50.0                      5.6
pandas:
  month  orders  cancelled  cancel_rate  completed  refunded_orders  refund_rate_count  refund_rate_value
2024-01       3          1         33.3          2                1               50.0               16.7
2024-02       3          1         33.3          2                2              100.0               80.0
2024-03       4          2         50.0          2                0                0.0                0.0
2024-04       1          1        100.0          0                0                NaN                NaN
asserts passed
```

**Edge cases:**
- Two refunds on one order (order 1) count once in the count rate because of the pre-aggregation or `EXISTS`; a plain join would count the order twice in the numerator and could push the rate above 100%.
- A month with no completed orders: `NULLIF(..., 0)` returns NULL; in pandas I mask the zero denominator to get NaN. Show it as "n/a", not 0%.
- Refund on a cancelled order (should not happen): the status filter ignores it; I would also list such rows as data errors.
- Refunds lag orders: recent months are incomplete (a March order may still be refunded in May), so the latest months understate the refund rate; use a mature window or cohort by age (Part 6 Q13 covers the immature-cohort idea for retention).
- Cancellation rate is order-level over all orders in the month; a cancellation that happens in a later month is still charged to the order month here.
- Partial refunds: the count rate treats a 10 refund like a 150 refund; the value rate does not, so report both.

**Then explain:**
- Refund rate by count answers "how many orders have a problem"; by value answers "how much revenue is lost"; they differ (50.0 versus 16.7 in January).
- Numerator and denominator must be about the same set of orders. Counting refunds by `refund_ts` month over orders by `order_ts` month mixes two populations and makes the March rate nonzero when no March order was refunded.
- `SUM(boolean)` counts true values in SQLite; in PostgreSQL use `COUNT(*) FILTER (WHERE ...)` or `SUM(CASE ...)` (not executed here).
- Dialects (not executed here): BigQuery `COUNTIF`, `SAFE_DIVIDE`; MySQL `DATE_FORMAT(order_ts, '%Y-%m')`.

**Follow-ups:**
- Net revenue per month? Q10.
- Refund rate by cohort age rather than calendar month? Group by months since order and use only mature ages (Part 6).
- Cancellations by reason or by side? Add the dimension to the group; see Q23 for who cancelled.

**Common mistakes:**
- Joining refunds to orders and counting rows (order 1 twice).
- Bucketing refunds by refund month over orders by order month.
- Treating a month with no completed orders as a 0% refund rate.
- Dividing refunded amount by gross including cancelled orders.
- Integer division.

### Q12 ⭐⭐⭐ 🟡 Activation rate within N days: users(user_id, signup_date, is_test) and events(user_id, event_ts, event_name) where activation means at least one 'create_project' event within 7 days of signup (days 0 to 7, inclusive of signup day). Return the activation rate per signup month at the fixed as-of date 2024-06-30, counting only users whose 7-day window is fully mature at the as-of date, plus the number of immature users excluded. Explain the denominator (all non-test signups in the cohort that are mature), what happens with an event before signup, and why including immature users understates recent cohorts.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** Activation rate = activated users over mature users, per signup month, where activated means at least one `create_project` event dated from the signup day to signup + 7 days (8 calendar days), mature means signup + 7 days is on or before the as-of date (so signups up to 2024-06-23), and I report the immature users separately instead of leaving them in the denominator.

Conventions I state out loud: dates are UTC calendar dates, the as-of day 2024-06-30 is treated as complete, test users (`is_test = 1`) are excluded, no bot filter is needed because the only event that counts is `create_project`.

**Schema and sample data:** twelve users in three signup months and a handful of events. User 5 is a test user. User 12 creates a project at exactly 00:00:00 on the signup day; user 2 creates one on day 7 at 23:59:59 (inside); user 3 on day 8 (outside); user 4 only before signing up (outside); user 10 creates two projects (counts once). Users 8 and 9 signed up too recently to be mature.
```sql
CREATE TABLE users(user_id INTEGER, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (10,'2024-04-15',0),(11,'2024-04-20',0),(12,'2024-04-22',0),
 (1,'2024-05-10',0),(2,'2024-05-20',0),(3,'2024-05-25',0),(4,'2024-05-28',0),(5,'2024-05-30',1),
 (6,'2024-06-10',0),(7,'2024-06-23',0),(8,'2024-06-24',0),(9,'2024-06-29',0);
INSERT INTO events VALUES
 (10,'2024-04-16 09:00:00','create_project'),(10,'2024-04-17 09:00:00','create_project'),
 (11,'2024-04-21 09:00:00','login'),
 (12,'2024-04-22 00:00:00','create_project'),
 (1,'2024-05-10 08:00:00','create_project'),
 (2,'2024-05-27 23:59:59','create_project'),
 (3,'2024-06-02 00:00:00','create_project'),
 (4,'2024-05-27 12:00:00','create_project'),(4,'2024-05-29 12:00:00','login'),
 (5,'2024-05-31 10:00:00','create_project'),
 (6,'2024-06-13 10:00:00','create_project'),
 (7,'2024-06-25 10:00:00','login');
```

**SQL answer:** `SQL_MAIN` in the Code block, with the as-of date as a named parameter:
```sql
WITH cohort AS (
  SELECT u.user_id,
         strftime('%Y-%m', u.signup_date) AS signup_month,
         CASE WHEN date(u.signup_date, '+7 days') <= :as_of THEN 1 ELSE 0 END AS mature,
         CASE WHEN EXISTS (
                SELECT 1 FROM events e
                WHERE e.user_id = u.user_id
                  AND e.event_name = 'create_project'
                  AND date(e.event_ts) BETWEEN u.signup_date AND date(u.signup_date, '+7 days')
              ) THEN 1 ELSE 0 END AS activated
  FROM users u
  WHERE u.is_test = 0
)
SELECT signup_month,
       SUM(mature)                                              AS mature_users,
       SUM(mature * activated)                                  AS activated_users,
       ROUND(100.0 * SUM(mature * activated) / NULLIF(SUM(mature), 0), 1) AS activation_pct,
       SUM(1 - mature)                                          AS immature_excluded,
       ROUND(100.0 * SUM(activated) / COUNT(*), 1)              AS naive_pct_all_signups
FROM cohort
GROUP BY signup_month
ORDER BY signup_month
```

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
u = users[users["is_test"] == 0].copy()
u["signup"] = pd.to_datetime(u["signup_date"])
u["win_end"] = u["signup"] + pd.Timedelta(days=7)
e = events[events["event_name"] == "create_project"].copy()
e["day"] = pd.to_datetime(e["event_ts"]).dt.normalize()
m = u.merge(e[["user_id", "day"]], on="user_id", how="left")
m["hit"] = (m["day"] >= m["signup"]) & (m["day"] <= m["win_end"])
u["activated"] = u["user_id"].map(m.groupby("user_id")["hit"].max()).astype(int)
u["mature"] = (u["win_end"] <= pd.Timestamp(AS_OF)).astype(int)
u["act_mature"] = u["activated"] * u["mature"]
u["signup_month"] = u["signup"].dt.strftime("%Y-%m")
g = u.groupby("signup_month").agg(
    mature_users=("mature", "sum"),
    activated_users=("act_mature", "sum"),
    n=("user_id", "size"),
    act_all=("activated", "sum"),
)
g["activation_pct"] = (100.0 * g["activated_users"] / g["mature_users"].where(g["mature_users"] > 0)).round(1)
g["immature_excluded"] = g["n"] - g["mature_users"]
g["naive_pct_all_signups"] = (100.0 * g["act_all"] / g["n"]).round(1)
pd_df = g.reset_index()[["signup_month", "mature_users", "activated_users", "activation_pct",
                         "immature_excluded", "naive_pct_all_signups"]]
```

**Example:** mature cutoff: signup + 7 days must be <= 2024-06-30, so signup <= 2024-06-23.
- April: users 10, 11, 12 are all mature. User 10 activated (day 1, two events but one user), 11 only logged in, 12 activated at 00:00:00 on day 0. 2 of 3 = 66.7 percent.
- May (test user 5 dropped): users 1, 2, 3, 4. User 1 day 0 yes, user 2 day 7 yes, user 3 day 8 no, user 4 had the event before signup so no. 2 of 4 = 50.0 percent.
- June: users 6 and 7 are mature (user 7's day 7 is exactly 2024-06-30), user 6 activated, user 7 did not: 1 of 2 = 50.0 percent. Users 8 and 9 are immature (their day 7 is 07-01 and 07-06), so `immature_excluded` is 2.
- If I left immature users in, June would read 1 of 4 = 25.0 percent, which is the naive column: the recent cohort looks half as good only because two users have not had their 7 days yet.

**Code:** run with `python3 -I`. The assert compares the two result frames after ordering by `signup_month` (they come out sorted already); dtypes are ignored because SQL returns integers and pandas sums can differ in width.
```python
# Q12: activation rate within 7 days of signup, mature cohorts only (as-of 2024-06-30)
import sqlite3
import pandas as pd

AS_OF = "2024-06-30"   # data is complete through the end of this day

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (10,'2024-04-15',0),(11,'2024-04-20',0),(12,'2024-04-22',0),
 (1,'2024-05-10',0),(2,'2024-05-20',0),(3,'2024-05-25',0),(4,'2024-05-28',0),(5,'2024-05-30',1),
 (6,'2024-06-10',0),(7,'2024-06-23',0),(8,'2024-06-24',0),(9,'2024-06-29',0);
INSERT INTO events VALUES
 (10,'2024-04-16 09:00:00','create_project'),(10,'2024-04-17 09:00:00','create_project'),
 (11,'2024-04-21 09:00:00','login'),
 (12,'2024-04-22 00:00:00','create_project'),
 (1,'2024-05-10 08:00:00','create_project'),
 (2,'2024-05-27 23:59:59','create_project'),
 (3,'2024-06-02 00:00:00','create_project'),
 (4,'2024-05-27 12:00:00','create_project'),(4,'2024-05-29 12:00:00','login'),
 (5,'2024-05-31 10:00:00','create_project'),
 (6,'2024-06-13 10:00:00','create_project'),
 (7,'2024-06-25 10:00:00','login');
"""

SQL_MAIN = """
WITH cohort AS (
  SELECT u.user_id,
         strftime('%Y-%m', u.signup_date) AS signup_month,
         CASE WHEN date(u.signup_date, '+7 days') <= :as_of THEN 1 ELSE 0 END AS mature,
         CASE WHEN EXISTS (
                SELECT 1 FROM events e
                WHERE e.user_id = u.user_id
                  AND e.event_name = 'create_project'
                  AND date(e.event_ts) BETWEEN u.signup_date AND date(u.signup_date, '+7 days')
              ) THEN 1 ELSE 0 END AS activated
  FROM users u
  WHERE u.is_test = 0
)
SELECT signup_month,
       SUM(mature)                                              AS mature_users,
       SUM(mature * activated)                                  AS activated_users,
       ROUND(100.0 * SUM(mature * activated) / NULLIF(SUM(mature), 0), 1) AS activation_pct,
       SUM(1 - mature)                                          AS immature_excluded,
       ROUND(100.0 * SUM(activated) / COUNT(*), 1)              AS naive_pct_all_signups
FROM cohort
GROUP BY signup_month
ORDER BY signup_month
"""

SQL_INTDIV = """
SELECT 2 / 3 AS integer_division, 2.0 / 3 AS float_division
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": AS_OF})
print(sql_df.to_string(index=False))
print("integer division demo (2 / 3, 2.0 / 3):", con.execute(SQL_INTDIV).fetchone())

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
u = users[users["is_test"] == 0].copy()
u["signup"] = pd.to_datetime(u["signup_date"])
u["win_end"] = u["signup"] + pd.Timedelta(days=7)
e = events[events["event_name"] == "create_project"].copy()
e["day"] = pd.to_datetime(e["event_ts"]).dt.normalize()
m = u.merge(e[["user_id", "day"]], on="user_id", how="left")
m["hit"] = (m["day"] >= m["signup"]) & (m["day"] <= m["win_end"])
u["activated"] = u["user_id"].map(m.groupby("user_id")["hit"].max()).astype(int)
u["mature"] = (u["win_end"] <= pd.Timestamp(AS_OF)).astype(int)
u["act_mature"] = u["activated"] * u["mature"]
u["signup_month"] = u["signup"].dt.strftime("%Y-%m")
g = u.groupby("signup_month").agg(
    mature_users=("mature", "sum"),
    activated_users=("act_mature", "sum"),
    n=("user_id", "size"),
    act_all=("activated", "sum"),
)
g["activation_pct"] = (100.0 * g["activated_users"] / g["mature_users"].where(g["mature_users"] > 0)).round(1)
g["immature_excluded"] = g["n"] - g["mature_users"]
g["naive_pct_all_signups"] = (100.0 * g["act_all"] / g["n"]).round(1)
pd_df = g.reset_index()[["signup_month", "mature_users", "activated_users", "activation_pct",
                         "immature_excluded", "naive_pct_all_signups"]]
# pd:end
print(pd_df.to_string(index=False))
# compare after ordering by signup_month (both are already sorted by it)
pd.testing.assert_frame_equal(sql_df.sort_values("signup_month").reset_index(drop=True),
                              pd_df.sort_values("signup_month").reset_index(drop=True),
                              check_dtype=False)

# who is activated, user by user (the hand walk-through)
detail = u[["user_id", "signup_date", "mature", "activated"]].sort_values("user_id")
print(detail.to_string(index=False))

# edge: text comparison trap, event_ts <= '2024-06-30' would drop events later on the 30th
print("trap:", con.execute("SELECT '2024-06-30 10:00:00' <= '2024-06-30', date('2024-06-30 10:00:00') <= '2024-06-30'").fetchone())
print("asserts passed")
```

**Output (my run):**
```text
signup_month  mature_users  activated_users  activation_pct  immature_excluded  naive_pct_all_signups
     2024-04             3                2            66.7                  0                   66.7
     2024-05             4                2            50.0                  0                   50.0
     2024-06             2                1            50.0                  2                   25.0
integer division demo (2 / 3, 2.0 / 3): (0, 0.6666666666666666)
signup_month  mature_users  activated_users  activation_pct  immature_excluded  naive_pct_all_signups
     2024-04             3                2            66.7                  0                   66.7
     2024-05             4                2            50.0                  0                   50.0
     2024-06             2                1            50.0                  2                   25.0
 user_id signup_date  mature  activated
       1  2024-05-10       1          1
       2  2024-05-20       1          1
       3  2024-05-25       1          0
       4  2024-05-28       1          0
       6  2024-06-10       1          1
       7  2024-06-23       1          0
       8  2024-06-24       0          0
       9  2024-06-29       0          0
      10  2024-04-15       1          1
      11  2024-04-20       1          0
      12  2024-04-22       1          1
trap: (0, 1)
asserts passed
```

**Edge cases:**
- Event before signup (user 4): excluded by the lower bound; it is usually a tracking or identity-merge artefact, so I would also report how many users have such events.
- Day-0 inclusive: the window is 8 calendar days (days 0 to 7); "within 7 days" is ambiguous, so I state it. A different convention (day 1 to 7, or 168 hours from the signup timestamp) changes users such as 12 and 2.
- Compare with `date(event_ts)`, not with the raw text: `'2024-06-30 10:00:00' <= '2024-06-30'` is false in SQLite (printed above), so a bare text comparison silently drops events on the last day.
- A month with no mature users gives `NULLIF(..., 0)` so the rate is NULL, not a division error; pandas gives NaN through `.where`.
- Integer division: SQLite `2 / 3` is 0 (both integers) while `2.0 / 3` is 0.666...; the demo line prints both. Without `100.0 *` the whole rate column would be 0.
- Duplicates (user 10 has two events) are harmless because `EXISTS` answers yes or no.
- Test users are filtered in the cohort CTE so they leave numerator and denominator together; `is_test` NULL would fall out of `is_test = 0`, so say how you treat NULL.

**Then explain:**
- Denominator: all non-test signups in the cohort month whose full window is observable. Numerator: those among them who activated. Rows are users, so one user cannot count twice.
- Immature users understate recent cohorts because a user signing up yesterday has had one day, not eight, to activate; the most recent month always looks worse until it matures. Show the excluded count (as here) so a reader sees how thin the latest rate is.
- Mature is decided from signup date and as-of date only, never from whether the user activated (that would inflate the rate).
- `EXISTS` keeps one row per user, so there is no fan-out and no `DISTINCT` needed.
- Other engines (not executed here): Postgres `signup_date + 7`, MySQL `DATE_ADD(signup_date, INTERVAL 7 DAY)`, BigQuery `DATE_ADD(signup_date, INTERVAL 7 DAY)`; the logic is the same.
- Retention versions of this idea are in Part 6 Q12 and Q13; this question is only the activation rate.

**Follow-ups:**
- Activation within 24 hours of signup instead? Compare timestamps with `unixepoch` differences, not dates, and decide whether the signup is a date or a timestamp.
- Do you show partial cohorts? Yes, but flagged: a "so far" rate beside the mature rate, never mixed.
- Should the first create_project event define activation time? Then take `MIN(event_ts)` per user and compare it with signup + 7 days.

**Common mistakes:**
- Leaving immature users in the denominator.
- Counting events or joining users to events and dividing row counts.
- Not excluding events before signup.
- Comparing `event_ts <= '2024-06-30'` as text.
- Forgetting test users in either numerator or denominator.
- Dividing integers (0 percent everywhere).

### Q13 ⭐⭐⭐ 🟡 Conversion rate by experiment arm: experiments(user_id, arm, assigned_ts) with arm in ('control', 'treatment') and orders(order_id, user_id, order_ts, amount, status). For each arm return users assigned, users with at least one completed order after assignment, the conversion rate, the revenue per assigned user, and the absolute and relative uplift of treatment over control (no p-values or confidence intervals; those belong to Book 1 and Book 6). Show why orders before assigned_ts must be excluded, why the denominator is assigned users and not users who ordered, and what a join that repeats users does to the counts.
**Asked at:** experiment-metrics guides (PracHub and Statsig SRM pages and abtestly docs, search snippets only, not opened; SRM is a chi-square goodness-of-fit on distinct-user counts against the planned split, strict thresholds such as p < 0.001 in practice); the statistics belong to Book 1 and Book 6 and this question stays on counts, rates and uplift in SQL; guides, not candidate reports; experimentation and data scientist rounds
**Say this first (1 line):** Per arm, count assigned users (the denominator), count how many of them have at least one completed order at or after their own assignment time, divide, add revenue per assigned user, and report treatment minus control in percentage points and as a percentage of control; counts and rates only, the significance test belongs to Books 1 and 6.

Conventions: one assignment row per user here (contamination and double assignment are Q32 and Q44), an order at exactly `assigned_ts` counts (`>=`), only status `completed` converts, timestamps are UTC text.

**Schema and sample data:** twelve assigned users, six per arm. User 1 has two completed orders after assignment, user 2 orders at exactly the assignment second, user 3 and user 9 have a big order before assignment only, user 4 has only a cancelled order, users 5, 6, 11, 12 have no orders.
```sql
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 10:00:00'),(2,'control','2024-03-01 11:00:00'),
 (3,'control','2024-03-02 09:00:00'),(4,'control','2024-03-02 12:00:00'),
 (5,'control','2024-03-03 08:00:00'),(6,'control','2024-03-03 09:00:00'),
 (7,'treatment','2024-03-01 10:30:00'),(8,'treatment','2024-03-01 12:00:00'),
 (9,'treatment','2024-03-02 10:00:00'),(10,'treatment','2024-03-02 13:00:00'),
 (11,'treatment','2024-03-03 08:30:00'),(12,'treatment','2024-03-03 10:00:00');
INSERT INTO orders VALUES
 (101,1,'2024-03-02 10:00:00',100,'completed'),(102,1,'2024-03-05 10:00:00',50,'completed'),
 (103,2,'2024-03-01 11:00:00',80,'completed'),
 (104,3,'2024-02-20 09:00:00',200,'completed'),
 (105,4,'2024-03-03 12:00:00',60,'cancelled'),
 (106,7,'2024-03-02 09:00:00',120,'completed'),(107,7,'2024-03-04 09:00:00',30,'completed'),
 (108,8,'2024-03-01 12:30:00',90,'completed'),
 (109,9,'2024-03-01 10:00:00',500,'completed'),
 (110,10,'2024-03-03 13:00:00',70,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block. Users stay as the grain: the join to orders is collapsed to one row per user before arms are counted.
```sql
WITH per_user AS (
  SELECT x.user_id, x.arm,
         COUNT(o.order_id)            AS n_orders,
         COALESCE(SUM(o.amount), 0)   AS revenue
  FROM experiments x
  LEFT JOIN orders o
    ON o.user_id = x.user_id
   AND o.status = 'completed'
   AND o.order_ts >= x.assigned_ts
  GROUP BY x.user_id, x.arm
), arms AS (
  SELECT arm,
         COUNT(*)                                   AS assigned_users,
         SUM(CASE WHEN n_orders > 0 THEN 1 ELSE 0 END) AS converters,
         SUM(revenue)                               AS revenue
  FROM per_user
  GROUP BY arm
), r AS (
  SELECT arm, assigned_users, converters, revenue,
         100.0 * converters / assigned_users AS conv_pct,
         1.0 * revenue / assigned_users      AS rev_per_user
  FROM arms
)
SELECT t.arm, t.assigned_users, t.converters,
       ROUND(t.conv_pct, 1)     AS conv_pct,
       ROUND(t.rev_per_user, 2) AS rev_per_assigned_user,
       CASE WHEN t.arm <> 'control' THEN ROUND(t.conv_pct - c.conv_pct, 1) END AS abs_uplift_pp,
       CASE WHEN t.arm <> 'control'
            THEN ROUND(100.0 * (t.conv_pct - c.conv_pct) / NULLIF(c.conv_pct, 0), 1) END AS rel_uplift_pct
FROM r t CROSS JOIN (SELECT conv_pct FROM r WHERE arm = 'control') c
ORDER BY t.arm
```

**pandas answer:** the order filter is applied after pairing each order with its user's assignment time, then results are mapped back onto all assigned users so non-buyers stay in the denominator:
```py
x = experiments.assign(assigned_ts=pd.to_datetime(experiments["assigned_ts"]))
o = orders[orders["status"] == "completed"].copy()
o["order_ts"] = pd.to_datetime(o["order_ts"])
j = o.merge(x[["user_id", "assigned_ts"]], on="user_id")
j = j[j["order_ts"] >= j["assigned_ts"]]
per = j.groupby("user_id").agg(n_orders=("order_id", "size"), revenue=("amount", "sum"))
pu = x.merge(per, on="user_id", how="left").fillna({"n_orders": 0, "revenue": 0})
a = pu.groupby("arm").agg(assigned_users=("user_id", "nunique"),
                          converters=("n_orders", lambda s: int((s > 0).sum())),
                          revenue=("revenue", "sum"))
a["conv_pct"] = 100.0 * a["converters"] / a["assigned_users"]
a["rev_per_user"] = a["revenue"] / a["assigned_users"]
ctl = a.loc["control", "conv_pct"]
a["abs_uplift_pp"] = (a["conv_pct"] - ctl).where(a.index != "control").round(1)
a["rel_uplift_pct"] = (100.0 * (a["conv_pct"] - ctl) / (ctl if ctl != 0 else float("nan"))).where(a.index != "control").round(1)
a["conv_pct"] = a["conv_pct"].round(1)
a["rev_per_assigned_user"] = a["rev_per_user"].round(2)
pd_df = a.reset_index()[["arm", "assigned_users", "converters", "conv_pct",
                         "rev_per_assigned_user", "abs_uplift_pp", "rel_uplift_pct"]]
```

**Example:**
- Control, counting only completed orders at or after assignment: user 1 yes (100 + 50 = 150), user 2 yes (80, at the exact assignment second), user 3 no (order was before assignment), user 4 no (cancelled), users 5 and 6 no. 2 of 6 = 33.3 percent, revenue 230 / 6 = 38.33 per assigned user.
- Treatment: user 7 yes (120 + 30 = 150), user 8 yes (90), user 9 no (the 500 order was before assignment), user 10 yes (70), users 11 and 12 no. 3 of 6 = 50.0 percent, revenue 310 / 6 = 51.67.
- Uplift: 50.0 minus 33.3 = 16.7 percentage points absolute; 16.7 / 33.3 = 50.0 percent relative. Rates are computed from unrounded values, then rounded for display.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas frames after ordering by `arm`; the wrong variants are printed but not asserted.
```python
# Q13: conversion rate by experiment arm (counts, rates, uplift; no p-values)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 10:00:00'),(2,'control','2024-03-01 11:00:00'),
 (3,'control','2024-03-02 09:00:00'),(4,'control','2024-03-02 12:00:00'),
 (5,'control','2024-03-03 08:00:00'),(6,'control','2024-03-03 09:00:00'),
 (7,'treatment','2024-03-01 10:30:00'),(8,'treatment','2024-03-01 12:00:00'),
 (9,'treatment','2024-03-02 10:00:00'),(10,'treatment','2024-03-02 13:00:00'),
 (11,'treatment','2024-03-03 08:30:00'),(12,'treatment','2024-03-03 10:00:00');
INSERT INTO orders VALUES
 (101,1,'2024-03-02 10:00:00',100,'completed'),(102,1,'2024-03-05 10:00:00',50,'completed'),
 (103,2,'2024-03-01 11:00:00',80,'completed'),
 (104,3,'2024-02-20 09:00:00',200,'completed'),
 (105,4,'2024-03-03 12:00:00',60,'cancelled'),
 (106,7,'2024-03-02 09:00:00',120,'completed'),(107,7,'2024-03-04 09:00:00',30,'completed'),
 (108,8,'2024-03-01 12:30:00',90,'completed'),
 (109,9,'2024-03-01 10:00:00',500,'completed'),
 (110,10,'2024-03-03 13:00:00',70,'completed');
"""

SQL_MAIN = """
WITH per_user AS (
  SELECT x.user_id, x.arm,
         COUNT(o.order_id)            AS n_orders,
         COALESCE(SUM(o.amount), 0)   AS revenue
  FROM experiments x
  LEFT JOIN orders o
    ON o.user_id = x.user_id
   AND o.status = 'completed'
   AND o.order_ts >= x.assigned_ts
  GROUP BY x.user_id, x.arm
), arms AS (
  SELECT arm,
         COUNT(*)                                   AS assigned_users,
         SUM(CASE WHEN n_orders > 0 THEN 1 ELSE 0 END) AS converters,
         SUM(revenue)                               AS revenue
  FROM per_user
  GROUP BY arm
), r AS (
  SELECT arm, assigned_users, converters, revenue,
         100.0 * converters / assigned_users AS conv_pct,
         1.0 * revenue / assigned_users      AS rev_per_user
  FROM arms
)
SELECT t.arm, t.assigned_users, t.converters,
       ROUND(t.conv_pct, 1)     AS conv_pct,
       ROUND(t.rev_per_user, 2) AS rev_per_assigned_user,
       CASE WHEN t.arm <> 'control' THEN ROUND(t.conv_pct - c.conv_pct, 1) END AS abs_uplift_pp,
       CASE WHEN t.arm <> 'control'
            THEN ROUND(100.0 * (t.conv_pct - c.conv_pct) / NULLIF(c.conv_pct, 0), 1) END AS rel_uplift_pct
FROM r t CROSS JOIN (SELECT conv_pct FROM r WHERE arm = 'control') c
ORDER BY t.arm
"""

# three wrong versions, for the walk-through
SQL_NO_TIME_FILTER = """
SELECT x.arm, COUNT(DISTINCT x.user_id) AS assigned_users,
       COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN x.user_id END) AS converters
FROM experiments x
LEFT JOIN orders o ON o.user_id = x.user_id AND o.status = 'completed'
GROUP BY x.arm ORDER BY x.arm
"""
SQL_WHERE_FILTER = """
SELECT x.arm, COUNT(DISTINCT x.user_id) AS assigned_users
FROM experiments x
LEFT JOIN orders o ON o.user_id = x.user_id
WHERE o.status = 'completed' AND o.order_ts >= x.assigned_ts
GROUP BY x.arm ORDER BY x.arm
"""
SQL_ROWS = """
SELECT x.arm, COUNT(*) AS joined_rows, COUNT(DISTINCT x.user_id) AS users
FROM experiments x
LEFT JOIN orders o ON o.user_id = x.user_id AND o.status = 'completed' AND o.order_ts >= x.assigned_ts
GROUP BY x.arm ORDER BY x.arm
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("wrong 1, no time filter (orders before assignment count):")
print(pd.read_sql_query(SQL_NO_TIME_FILTER, con).to_string(index=False))
print("wrong 2, time filter in WHERE (LEFT JOIN turns into inner join, non-buyers vanish):")
print(pd.read_sql_query(SQL_WHERE_FILTER, con).to_string(index=False))
print("wrong 3, COUNT(*) on the joined rows:")
print(pd.read_sql_query(SQL_ROWS, con).to_string(index=False))

experiments = pd.read_sql_query("SELECT * FROM experiments", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
x = experiments.assign(assigned_ts=pd.to_datetime(experiments["assigned_ts"]))
o = orders[orders["status"] == "completed"].copy()
o["order_ts"] = pd.to_datetime(o["order_ts"])
j = o.merge(x[["user_id", "assigned_ts"]], on="user_id")
j = j[j["order_ts"] >= j["assigned_ts"]]
per = j.groupby("user_id").agg(n_orders=("order_id", "size"), revenue=("amount", "sum"))
pu = x.merge(per, on="user_id", how="left").fillna({"n_orders": 0, "revenue": 0})
a = pu.groupby("arm").agg(assigned_users=("user_id", "nunique"),
                          converters=("n_orders", lambda s: int((s > 0).sum())),
                          revenue=("revenue", "sum"))
a["conv_pct"] = 100.0 * a["converters"] / a["assigned_users"]
a["rev_per_user"] = a["revenue"] / a["assigned_users"]
ctl = a.loc["control", "conv_pct"]
a["abs_uplift_pp"] = (a["conv_pct"] - ctl).where(a.index != "control").round(1)
a["rel_uplift_pct"] = (100.0 * (a["conv_pct"] - ctl) / (ctl if ctl != 0 else float("nan"))).where(a.index != "control").round(1)
a["conv_pct"] = a["conv_pct"].round(1)
a["rev_per_assigned_user"] = a["rev_per_user"].round(2)
pd_df = a.reset_index()[["arm", "assigned_users", "converters", "conv_pct",
                         "rev_per_assigned_user", "abs_uplift_pp", "rel_uplift_pct"]]
# pd:end
print(pd_df.to_string(index=False))
# compare after ordering by arm
pd.testing.assert_frame_equal(sql_df.sort_values("arm").reset_index(drop=True),
                              pd_df.sort_values("arm").reset_index(drop=True), check_dtype=False)
print("asserts passed")
```

**Output (my run):**
```text
      arm  assigned_users  converters  conv_pct  rev_per_assigned_user  abs_uplift_pp  rel_uplift_pct
  control               6           2      33.3                  38.33            NaN             NaN
treatment               6           3      50.0                  51.67           16.7            50.0
wrong 1, no time filter (orders before assignment count):
      arm  assigned_users  converters
  control               6           3
treatment               6           4
wrong 2, time filter in WHERE (LEFT JOIN turns into inner join, non-buyers vanish):
      arm  assigned_users
  control               2
treatment               3
wrong 3, COUNT(*) on the joined rows:
      arm  joined_rows  users
  control            7      6
treatment            7      6
      arm  assigned_users  converters  conv_pct  rev_per_assigned_user  abs_uplift_pp  rel_uplift_pct
  control               6           2      33.3                  38.33            NaN             NaN
treatment               6           3      50.0                  51.67           16.7            50.0
asserts passed
```

**Edge cases:**
- Orders before `assigned_ts` (users 3 and 9): they reflect behaviour that the treatment could not have caused. Wrong 1 above counts them and lifts both arms (control 3 of 6, treatment 4 of 6 in my run).
- Putting the time filter in `WHERE` after a `LEFT JOIN` turns the join into an inner join, so non-buyers vanish and the denominator becomes buyers only (wrong 2 prints 2 and 3 users). The filter must be in the `ON` clause (SQL) or applied before mapping back (pandas).
- A join that repeats users: `COUNT(*)` over the joined rows gives 7 rows for 6 users in each arm (wrong 3), which also inflates any rate or revenue per user built on it. Fix: one row per user first (`per_user`), or `COUNT(DISTINCT user_id)`.
- Control rate zero: relative uplift needs `NULLIF` (SQL) or a NaN guard (pandas); absolute uplift is still defined.
- Revenue per assigned user divides by assigned users, so non-buyers pull it down on purpose; revenue per buyer is a different metric.
- Unequal arm sizes are fine for rates, but a very unequal split would itself be a sample ratio problem (Q32).

**Then explain:**
- Denominator is assigned users because the experiment randomised users, not buyers; dividing by buyers conditions on the outcome and hides the effect on the number of buyers.
- Exclude orders before assignment: they cannot be an outcome of the treatment. If assignment is not the first exposure (a late exposure), a stricter version anchors on first exposure time (not available in this schema).
- Window choice (here "any time after assignment up to the data cut") should be fixed in advance and the same for both arms; a fixed N-day window per user is Q44.
- Absolute uplift in percentage points answers "how many more users per 100 convert"; relative uplift answers "how large compared with control". Say both and never mix them.
- No p-values here: whether 16.7 points on 12 users means anything is a Book 1 and Book 6 question (with 6 users per arm it clearly does not mean much).

**Follow-ups:**
- What if users appear in both arms? Remove and count them separately (Q44), and check the split first (Q32).
- Conversion within 14 days of assignment instead of any time? Add `AND o.order_ts <= datetime(x.assigned_ts, '+14 days')` and drop users whose window is not yet complete.
- Which rate would you put on a dashboard? Conversion per assigned user plus revenue per assigned user, with the sample size beside it.

**Common mistakes:**
- Dividing by users who ordered.
- Not excluding pre-assignment orders.
- Filtering the outer table with `WHERE` after a `LEFT JOIN`.
- Counting joined rows instead of distinct users.
- Mixing up percentage points and percent.
- Reporting uplift from rounded rates.

### Q14 ⭐⭐⭐ 🟡 Share of total and growth contribution by segment: orders(order_id, user_id, order_ts, amount, status) and users(user_id, signup_date, country, is_test). For months 2024-02 and 2024-03, return per country the completed revenue in each month, its share of that month's total, the month-over-month change in rupees, and its contribution to total growth (the country's change divided by the total change). Do the share with a window SUM() OVER () and show the scalar-subquery alternative (see Part 3 and Part 5); state what happens when total growth is zero or negative (contributions above 100 percent and sign flips) and when a country is missing in one month.
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** Build one row per country with February and March completed revenue (filling a missing month with 0), take share as the country's revenue over `SUM() OVER ()` for the month, change as March minus February, and contribution as the country's change over the total change, guarded with `NULLIF` because the total change can be zero.

Conventions: completed orders only, test users out, month from `order_ts` (UTC text), amounts in rupees, a country with no completed orders in a month counts as 0 for that month.

**Schema and sample data:** five real users in four countries, one test user (user 6, IN, a 900 order that must not count). UK has only a cancelled order in March, so UK is missing from March; SG has no February order. One IN order is at 2024-03-31 23:30, which a `BETWEEN '2024-03-01' AND '2024-03-31'` filter would lose.
```sql
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-12-01','IN',0),(2,'2023-12-05','IN',0),(3,'2023-12-10','US',0),
 (4,'2023-12-15','UK',0),(5,'2024-01-05','SG',0),(6,'2023-11-01','IN',1);
INSERT INTO orders VALUES
 (1,1,'2024-02-05 10:00:00',600,'completed'),(2,2,'2024-02-20 11:00:00',400,'completed'),
 (3,3,'2024-02-10 09:00:00',600,'completed'),(4,4,'2024-02-12 15:00:00',400,'completed'),
 (5,1,'2024-02-14 12:00:00',300,'cancelled'),(6,6,'2024-02-15 12:00:00',900,'completed'),
 (7,1,'2024-03-03 10:00:00',900,'completed'),(8,2,'2024-03-31 23:30:00',600,'completed'),
 (9,3,'2024-03-09 09:00:00',500,'completed'),(10,5,'2024-03-15 10:00:00',200,'completed'),
 (11,4,'2024-03-20 10:00:00',250,'cancelled');
```

**SQL answer:** `SQL_MAIN` in the Code block, shares with a window `SUM() OVER ()`:
```sql
WITH m AS (
  SELECT u.country, strftime('%Y-%m', o.order_ts) AS month, SUM(o.amount) AS rev
  FROM orders o
  JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed'
    AND u.is_test = 0
    AND strftime('%Y-%m', o.order_ts) IN ('2024-02', '2024-03')
  GROUP BY u.country, strftime('%Y-%m', o.order_ts)
), countries AS (
  SELECT DISTINCT country FROM m
), g AS (
  SELECT c.country,
         COALESCE(f.rev, 0) AS feb,
         COALESCE(r.rev, 0) AS mar
  FROM countries c
  LEFT JOIN m f ON f.country = c.country AND f.month = '2024-02'
  LEFT JOIN m r ON r.country = c.country AND r.month = '2024-03'
)
SELECT country,
       feb AS rev_feb,
       mar AS rev_mar,
       ROUND(100.0 * feb / SUM(feb) OVER (), 1) AS share_feb_pct,
       ROUND(100.0 * mar / SUM(mar) OVER (), 1) AS share_mar_pct,
       mar - feb AS change,
       ROUND(100.0 * (mar - feb) / NULLIF(SUM(mar - feb) OVER (), 0), 1) AS contribution_pct
FROM g
ORDER BY country
```
The scalar-subquery alternative `SQL_ALT` (same result, asserted equal in the Code block) replaces each window with `(SELECT SUM(...) FROM g)`; scalar subqueries are in Part 3 Q9 and window total mechanics in Part 5.
```sql
WITH m AS (
  SELECT u.country, strftime('%Y-%m', o.order_ts) AS month, SUM(o.amount) AS rev
  FROM orders o
  JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed'
    AND u.is_test = 0
    AND strftime('%Y-%m', o.order_ts) IN ('2024-02', '2024-03')
  GROUP BY u.country, strftime('%Y-%m', o.order_ts)
), g AS (
  SELECT c.country,
         COALESCE((SELECT rev FROM m WHERE m.country = c.country AND m.month = '2024-02'), 0) AS feb,
         COALESCE((SELECT rev FROM m WHERE m.country = c.country AND m.month = '2024-03'), 0) AS mar
  FROM (SELECT DISTINCT country FROM m) c
)
SELECT country, feb AS rev_feb, mar AS rev_mar,
       ROUND(100.0 * feb / (SELECT SUM(feb) FROM g), 1) AS share_feb_pct,
       ROUND(100.0 * mar / (SELECT SUM(mar) FROM g), 1) AS share_mar_pct,
       mar - feb AS change,
       ROUND(100.0 * (mar - feb) / NULLIF((SELECT SUM(mar - feb) FROM g), 0), 1) AS contribution_pct
FROM g
ORDER BY country
```

**pandas answer:** a function so the zero and negative scenarios can be rerun, shown once here and identical to the Code block:
```py
def pd_growth(orders, users):
    d = orders.merge(users, on="user_id")
    d = d[(d["status"] == "completed") & (d["is_test"] == 0)].copy()
    d["month"] = pd.to_datetime(d["order_ts"]).dt.strftime("%Y-%m")
    d = d[d["month"].isin(["2024-02", "2024-03"])]
    p = d.pivot_table(index="country", columns="month", values="amount", aggfunc="sum", fill_value=0)
    p = p.reindex(columns=["2024-02", "2024-03"], fill_value=0)
    out = pd.DataFrame({"country": p.index, "rev_feb": p["2024-02"].to_numpy(), "rev_mar": p["2024-03"].to_numpy()})
    out["share_feb_pct"] = (100.0 * out["rev_feb"] / out["rev_feb"].sum()).round(1)
    out["share_mar_pct"] = (100.0 * out["rev_mar"] / out["rev_mar"].sum()).round(1)
    out["change"] = out["rev_mar"] - out["rev_feb"]
    total_change = out["change"].sum()
    denom = total_change if total_change != 0 else np.nan
    out["contribution_pct"] = (100.0 * out["change"] / denom).round(1)
    return out.sort_values("country").reset_index(drop=True)
```

**Example:**
- Completed, non-test revenue: February IN 600 + 400 = 1000, US 600, UK 400, total 2000. March IN 900 + 600 = 1500, US 500, SG 200, total 2200 (the UK 250 order is cancelled, so UK is 0 in March).
- Shares: February IN 50.0, US 30.0, UK 20.0, SG 0.0. March IN 68.2, US 22.7, SG 9.1, UK 0.0.
- Change: IN +500, US -100, UK -400, SG +200; total change +200.
- Contribution: IN 500 / 200 = 250.0 percent, SG 100.0, UK -200.0, US -50.0; they add up to 100 percent. A contribution above 100 percent is normal when other segments fall.

**Code:** run with `python3 -I`. The asserts compare SQL and pandas after ordering by `country`; the window and scalar-subquery SQL are asserted identical row by row. Two extra runs change the data to show zero and negative total growth.
```python
# Q14: share of total and growth contribution by country, Feb vs Mar 2024
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-12-01','IN',0),(2,'2023-12-05','IN',0),(3,'2023-12-10','US',0),
 (4,'2023-12-15','UK',0),(5,'2024-01-05','SG',0),(6,'2023-11-01','IN',1);
INSERT INTO orders VALUES
 (1,1,'2024-02-05 10:00:00',600,'completed'),(2,2,'2024-02-20 11:00:00',400,'completed'),
 (3,3,'2024-02-10 09:00:00',600,'completed'),(4,4,'2024-02-12 15:00:00',400,'completed'),
 (5,1,'2024-02-14 12:00:00',300,'cancelled'),(6,6,'2024-02-15 12:00:00',900,'completed'),
 (7,1,'2024-03-03 10:00:00',900,'completed'),(8,2,'2024-03-31 23:30:00',600,'completed'),
 (9,3,'2024-03-09 09:00:00',500,'completed'),(10,5,'2024-03-15 10:00:00',200,'completed'),
 (11,4,'2024-03-20 10:00:00',250,'cancelled');
"""

SQL_MAIN = """
WITH m AS (
  SELECT u.country, strftime('%Y-%m', o.order_ts) AS month, SUM(o.amount) AS rev
  FROM orders o
  JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed'
    AND u.is_test = 0
    AND strftime('%Y-%m', o.order_ts) IN ('2024-02', '2024-03')
  GROUP BY u.country, strftime('%Y-%m', o.order_ts)
), countries AS (
  SELECT DISTINCT country FROM m
), g AS (
  SELECT c.country,
         COALESCE(f.rev, 0) AS feb,
         COALESCE(r.rev, 0) AS mar
  FROM countries c
  LEFT JOIN m f ON f.country = c.country AND f.month = '2024-02'
  LEFT JOIN m r ON r.country = c.country AND r.month = '2024-03'
)
SELECT country,
       feb AS rev_feb,
       mar AS rev_mar,
       ROUND(100.0 * feb / SUM(feb) OVER (), 1) AS share_feb_pct,
       ROUND(100.0 * mar / SUM(mar) OVER (), 1) AS share_mar_pct,
       mar - feb AS change,
       ROUND(100.0 * (mar - feb) / NULLIF(SUM(mar - feb) OVER (), 0), 1) AS contribution_pct
FROM g
ORDER BY country
"""

# the same shares and contributions with scalar subqueries instead of window functions
SQL_ALT = """
WITH m AS (
  SELECT u.country, strftime('%Y-%m', o.order_ts) AS month, SUM(o.amount) AS rev
  FROM orders o
  JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed'
    AND u.is_test = 0
    AND strftime('%Y-%m', o.order_ts) IN ('2024-02', '2024-03')
  GROUP BY u.country, strftime('%Y-%m', o.order_ts)
), g AS (
  SELECT c.country,
         COALESCE((SELECT rev FROM m WHERE m.country = c.country AND m.month = '2024-02'), 0) AS feb,
         COALESCE((SELECT rev FROM m WHERE m.country = c.country AND m.month = '2024-03'), 0) AS mar
  FROM (SELECT DISTINCT country FROM m) c
)
SELECT country, feb AS rev_feb, mar AS rev_mar,
       ROUND(100.0 * feb / (SELECT SUM(feb) FROM g), 1) AS share_feb_pct,
       ROUND(100.0 * mar / (SELECT SUM(mar) FROM g), 1) AS share_mar_pct,
       mar - feb AS change,
       ROUND(100.0 * (mar - feb) / NULLIF((SELECT SUM(mar - feb) FROM g), 0), 1) AS contribution_pct
FROM g
ORDER BY country
"""

def make():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c

# pd:main
def pd_growth(orders, users):
    d = orders.merge(users, on="user_id")
    d = d[(d["status"] == "completed") & (d["is_test"] == 0)].copy()
    d["month"] = pd.to_datetime(d["order_ts"]).dt.strftime("%Y-%m")
    d = d[d["month"].isin(["2024-02", "2024-03"])]
    p = d.pivot_table(index="country", columns="month", values="amount", aggfunc="sum", fill_value=0)
    p = p.reindex(columns=["2024-02", "2024-03"], fill_value=0)
    out = pd.DataFrame({"country": p.index, "rev_feb": p["2024-02"].to_numpy(), "rev_mar": p["2024-03"].to_numpy()})
    out["share_feb_pct"] = (100.0 * out["rev_feb"] / out["rev_feb"].sum()).round(1)
    out["share_mar_pct"] = (100.0 * out["rev_mar"] / out["rev_mar"].sum()).round(1)
    out["change"] = out["rev_mar"] - out["rev_feb"]
    total_change = out["change"].sum()
    denom = total_change if total_change != 0 else np.nan
    out["contribution_pct"] = (100.0 * out["change"] / denom).round(1)
    return out.sort_values("country").reset_index(drop=True)
# pd:end

def same(sql_df, pd_df):
    sql_df = sql_df.assign(contribution_pct=sql_df["contribution_pct"].astype(float))  # NULL -> NaN
    pd.testing.assert_frame_equal(sql_df.sort_values("country").reset_index(drop=True),
                                  pd_df.sort_values("country").reset_index(drop=True), check_dtype=False)

con = make()
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("main (windows):"); print(sql_df.to_string(index=False))
alt_df = pd.read_sql_query(SQL_ALT, con)
pd.testing.assert_frame_equal(sql_df, alt_df)
users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
pd_df = pd_growth(orders, users)
print("pandas:"); print(pd_df.to_string(index=False))
same(sql_df, pd_df)

# scenario A: total growth is zero (drop the SG order of 200 in March)
a = make(); a.execute("DELETE FROM orders WHERE order_id = 10")
a_sql = pd.read_sql_query(SQL_MAIN, a)
print("zero total growth:"); print(a_sql.to_string(index=False))
same(a_sql, pd_growth(pd.read_sql_query("SELECT * FROM orders", a), users))
# scenario B: total growth is negative (IN falls to 1200 in March)
b = make(); b.execute("UPDATE orders SET amount = 600 WHERE order_id = 7")
b_sql = pd.read_sql_query(SQL_MAIN, b)
print("negative total growth:"); print(b_sql.to_string(index=False))
same(b_sql, pd_growth(pd.read_sql_query("SELECT * FROM orders", b), users))
print("asserts passed")
```

**Output (my run):**
```text
main (windows):
country  rev_feb  rev_mar  share_feb_pct  share_mar_pct  change  contribution_pct
     IN   1000.0   1500.0           50.0           68.2   500.0             250.0
     SG      0.0    200.0            0.0            9.1   200.0             100.0
     UK    400.0      0.0           20.0            0.0  -400.0            -200.0
     US    600.0    500.0           30.0           22.7  -100.0             -50.0
pandas:
country  rev_feb  rev_mar  share_feb_pct  share_mar_pct  change  contribution_pct
     IN   1000.0   1500.0           50.0           68.2   500.0             250.0
     SG      0.0    200.0            0.0            9.1   200.0             100.0
     UK    400.0      0.0           20.0            0.0  -400.0            -200.0
     US    600.0    500.0           30.0           22.7  -100.0             -50.0
zero total growth:
country  rev_feb  rev_mar  share_feb_pct  share_mar_pct  change contribution_pct
     IN   1000.0   1500.0           50.0           75.0   500.0             None
     UK    400.0      0.0           20.0            0.0  -400.0             None
     US    600.0    500.0           30.0           25.0  -100.0             None
negative total growth:
country  rev_feb  rev_mar  share_feb_pct  share_mar_pct  change  contribution_pct
     IN   1000.0   1200.0           50.0           63.2   200.0            -200.0
     SG      0.0    200.0            0.0           10.5   200.0            -200.0
     UK    400.0      0.0           20.0            0.0  -400.0             400.0
     US    600.0    500.0           30.0           26.3  -100.0             100.0
asserts passed
```

**Edge cases:**
- Country missing in a month (UK in March, SG in February): needs the `COALESCE(..., 0)` from a country list; a plain `GROUP BY country, month` gives no row and the pivot or join silently loses it. Shares then correctly show 0.0.
- Total change zero (scenario A, SG's only order removed, so SG has no rows at all and drops out of the country list): the denominator is 0, contribution is NULL (SQL) or NaN (pandas); the individual changes (+500, -100, -400) still print. I show "n/a" rather than a made-up percentage.
- Total change negative (scenario B, IN's March revenue falls to 1200, so the total goes from 2000 to 1900, a change of -100): every sign flips relative to the segment's own change. IN rises by 200 and shows -200.0 percent, UK falls by 400 and shows +400.0 percent. The small total change also blows the magnitudes up. State this in words when presenting.
- Close-to-zero total change gives huge contributions (a total change of +1 would make IN 50000 percent); in that case present absolute changes only.
- `BETWEEN '2024-03-01' AND '2024-03-31'` on timestamps loses the 23:30 order on 31 March; I use `strftime('%Y-%m', ...)`.
- Rounded shares may sum to 99.9 or 100.1; compute from unrounded values.

**Then explain:**
- Share = part / total of the same period; a window `SUM() OVER ()` over the already grouped rows gives the total without a second query. The scalar-subquery version is equivalent and works on engines without windows.
- Contribution to growth = segment change / total change, so contributions add up to 100 percent (when the total change is non-zero). Share change in percentage points is a different, mix-only measure.
- Month-over-month change for a longer series would use `LAG` (Part 5 Q4); here two months in columns are simpler.
- Other engines (not executed here): Postgres, MySQL 8, BigQuery and Snowflake all support `SUM() OVER ()` the same way; month bucketing differs (`DATE_TRUNC`, `DATE_FORMAT`), see Part 6 Q2.

**Follow-ups:**
- Growth contribution when a segment is new (SG)? Its change equals its full March revenue; say it is new rather than "infinite growth".
- Which is better to show, share or contribution? Share describes mix; contribution explains why the total moved; show both.
- Do cancelled orders belong? Only if the metric is GMV including cancellations; here the metric is completed revenue.

**Common mistakes:**
- Dividing by the wrong total (all countries across both months) instead of the same month.
- Dropping countries that exist in only one month.
- Dividing by a zero or near-zero total change.
- Treating a contribution above 100 percent as a bug.
- Including test users and cancelled orders.
- Date filters that lose the last day of the month.

### Q15 ⭐⭐⭐ 🟡 Stickiness as DAU/MAU for a fixed month: events(user_id, event_ts, event_name) and users(user_id, signup_date, country, is_test). For March 2024 return the average DAU over the 31 days, the calendar-month MAU, and stickiness as average DAU divided by MAU, excluding test users. Show the two common definitions (average of daily DAU over MAU, versus the DAU of the last day over a trailing 30-day MAU) and why they differ, how zero-activity days affect the average (days with no events must count as 0, which needs a date spine), and what a stickiness of 0.2 means in words.
**Asked at:** active-user guides: Basedash DAU/WAU/MAU pitfalls article (opened; active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users) plus search snippets of oneuptime ClickHouse DAU/WAU/MAU and stickiness posts and Swace and pmtoolkit pages (not opened); guides, not candidate reports; product analytics and data scientist rounds at social, streaming and SaaS companies
**Say this first (1 line):** For March 2024 I take the number of distinct non-test users active on each of the 31 days (days with no activity count as 0, which needs a date spine), average those 31 numbers for average DAU, divide by the calendar-month MAU (distinct non-test users active at least once in March), and call that stickiness; the other common version uses the last day's DAU over a trailing 30-day MAU and gives a different number.

Conventions: UTC calendar days, test users excluded, any event counts as active (an "active" definition to agree on), March calendar month for MAU, the as-of day 2024-03-31 is complete.

**Schema and sample data:** five real users and one test user (user 6, active on 03-01 and 03-02 and must not count). User 3 has two events on 03-02 (one active day). User 2 has an event on 04-01 (outside March). User 5 has events on 02-28 and 03-01.
```sql
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','US',0),
 (4,'2024-01-01','US',0),(5,'2024-01-01','UK',0),(6,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-01 09:00:00','open'),(1,'2024-03-02 09:00:00','open'),(1,'2024-03-03 09:00:00','open'),
 (1,'2024-03-10 09:00:00','open'),(1,'2024-03-31 09:00:00','open'),
 (2,'2024-03-01 10:00:00','open'),(2,'2024-03-10 10:00:00','open'),(2,'2024-03-15 10:00:00','open'),
 (2,'2024-04-01 10:00:00','open'),
 (3,'2024-03-02 11:00:00','open'),(3,'2024-03-02 11:30:00','click'),(3,'2024-03-31 11:00:00','open'),
 (4,'2024-03-31 12:00:00','open'),
 (5,'2024-02-28 08:00:00','open'),(5,'2024-03-01 08:00:00','open'),
 (6,'2024-03-01 07:00:00','open'),(6,'2024-03-02 07:00:00','open');
```

**SQL answer:** `SQL_MAIN` in the Code block: a recursive-CTE date spine, one row per user and active day (`DISTINCT`), a left join so empty days survive as 0, then both definitions in one row:
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), act AS (
  SELECT DISTINCT e.user_id, date(e.event_ts) AS d
  FROM events e
  JOIN users u ON u.user_id = e.user_id
  WHERE u.is_test = 0
    AND date(e.event_ts) BETWEEN '2024-02-01' AND '2024-03-31'
), daily AS (
  SELECT s.d, COUNT(a.user_id) AS dau
  FROM spine s
  LEFT JOIN act a ON a.d = s.d
  GROUP BY s.d
)
SELECT (SELECT COUNT(*) FROM daily)                                   AS days,
       (SELECT SUM(dau) FROM daily)                                   AS user_days,
       ROUND((SELECT AVG(dau) FROM daily), 4)                         AS avg_dau,
       (SELECT COUNT(DISTINCT user_id) FROM act
         WHERE d BETWEEN '2024-03-01' AND '2024-03-31')               AS mau_calendar,
       ROUND((SELECT AVG(dau) FROM daily) * 1.0 /
             (SELECT COUNT(DISTINCT user_id) FROM act
               WHERE d BETWEEN '2024-03-01' AND '2024-03-31'), 4)     AS stickiness_avg_dau,
       (SELECT dau FROM daily WHERE d = '2024-03-31')                 AS dau_last_day,
       (SELECT COUNT(DISTINCT user_id) FROM act
         WHERE d BETWEEN date('2024-03-31', '-29 days') AND '2024-03-31') AS mau_trailing_30,
       ROUND(1.0 * (SELECT dau FROM daily WHERE d = '2024-03-31') /
             (SELECT COUNT(DISTINCT user_id) FROM act
               WHERE d BETWEEN date('2024-03-31', '-29 days') AND '2024-03-31'), 4) AS stickiness_last_day
```

**pandas answer:** the spine is `pd.date_range`, and `reindex(..., fill_value=0)` plays the role of the left join:
```py
a = events.merge(users[users["is_test"] == 0], on="user_id")
a["d"] = pd.to_datetime(a["event_ts"]).dt.normalize()
a = a[(a["d"] >= pd.Timestamp("2024-02-01")) & (a["d"] <= pd.Timestamp("2024-03-31"))]
a = a[["user_id", "d"]].drop_duplicates()
spine = pd.date_range("2024-03-01", "2024-03-31", freq="D")
dau = a.groupby("d")["user_id"].nunique().reindex(spine, fill_value=0)
in_month = a[a["d"] >= pd.Timestamp("2024-03-01")]
mau = in_month["user_id"].nunique()
trail = a[a["d"] >= pd.Timestamp("2024-03-31") - pd.Timedelta(days=29)]["user_id"].nunique()
pd_df = pd.DataFrame([{
    "days": len(dau), "user_days": int(dau.sum()), "avg_dau": round(dau.mean(), 4),
    "mau_calendar": mau, "stickiness_avg_dau": round(dau.mean() / mau, 4),
    "dau_last_day": int(dau.iloc[-1]), "mau_trailing_30": trail,
    "stickiness_last_day": round(dau.iloc[-1] / trail, 4)}])
```

**Example:** active user-days in March (non-test): 03-01 users 1, 2, 5 (3); 03-02 users 1, 3 (2); 03-03 user 1 (1); 03-10 users 1, 2 (2); 03-15 user 2 (1); 03-31 users 1, 3, 4 (3). Every other day is 0.
- User-days = 3 + 2 + 1 + 2 + 1 + 3 = 12 over 31 days, so average DAU = 12 / 31 = 0.3871.
- MAU (calendar March) = users 1, 2, 3, 4, 5 = 5. Stickiness = 0.3871 / 5 = 0.0774, about 7.7 percent.
- Trailing 30 days ending 03-31 starts on 03-02, so user 5 (only active 03-01) drops out: trailing MAU = 4. Last-day DAU is 3, so the last-day version is 3 / 4 = 0.75.
- Same data, two definitions: 7.7 percent versus 75 percent. This toy data is built to make the point loudly; on real data the two are usually closer but still not interchangeable.
- Without the spine, averaging only the 6 days that have events gives 2.0, then 2.0 / 5 = 40 percent, which is the zero-day error.

**Code:** run with `python3 -I`. The assert compares the one-row SQL result with the one-row pandas result (same columns, no ordering needed).
```python
# Q15: stickiness (DAU/MAU) for March 2024 with a date spine
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','US',0),
 (4,'2024-01-01','US',0),(5,'2024-01-01','UK',0),(6,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-01 09:00:00','open'),(1,'2024-03-02 09:00:00','open'),(1,'2024-03-03 09:00:00','open'),
 (1,'2024-03-10 09:00:00','open'),(1,'2024-03-31 09:00:00','open'),
 (2,'2024-03-01 10:00:00','open'),(2,'2024-03-10 10:00:00','open'),(2,'2024-03-15 10:00:00','open'),
 (2,'2024-04-01 10:00:00','open'),
 (3,'2024-03-02 11:00:00','open'),(3,'2024-03-02 11:30:00','click'),(3,'2024-03-31 11:00:00','open'),
 (4,'2024-03-31 12:00:00','open'),
 (5,'2024-02-28 08:00:00','open'),(5,'2024-03-01 08:00:00','open'),
 (6,'2024-03-01 07:00:00','open'),(6,'2024-03-02 07:00:00','open');
"""

SQL_MAIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), act AS (
  SELECT DISTINCT e.user_id, date(e.event_ts) AS d
  FROM events e
  JOIN users u ON u.user_id = e.user_id
  WHERE u.is_test = 0
    AND date(e.event_ts) BETWEEN '2024-02-01' AND '2024-03-31'
), daily AS (
  SELECT s.d, COUNT(a.user_id) AS dau
  FROM spine s
  LEFT JOIN act a ON a.d = s.d
  GROUP BY s.d
)
SELECT (SELECT COUNT(*) FROM daily)                                   AS days,
       (SELECT SUM(dau) FROM daily)                                   AS user_days,
       ROUND((SELECT AVG(dau) FROM daily), 4)                         AS avg_dau,
       (SELECT COUNT(DISTINCT user_id) FROM act
         WHERE d BETWEEN '2024-03-01' AND '2024-03-31')               AS mau_calendar,
       ROUND((SELECT AVG(dau) FROM daily) * 1.0 /
             (SELECT COUNT(DISTINCT user_id) FROM act
               WHERE d BETWEEN '2024-03-01' AND '2024-03-31'), 4)     AS stickiness_avg_dau,
       (SELECT dau FROM daily WHERE d = '2024-03-31')                 AS dau_last_day,
       (SELECT COUNT(DISTINCT user_id) FROM act
         WHERE d BETWEEN date('2024-03-31', '-29 days') AND '2024-03-31') AS mau_trailing_30,
       ROUND(1.0 * (SELECT dau FROM daily WHERE d = '2024-03-31') /
             (SELECT COUNT(DISTINCT user_id) FROM act
               WHERE d BETWEEN date('2024-03-31', '-29 days') AND '2024-03-31'), 4) AS stickiness_last_day
"""

SQL_NO_SPINE = """
SELECT ROUND(AVG(dau), 4) AS avg_dau_active_days_only, COUNT(*) AS days_counted
FROM (SELECT date(e.event_ts) AS d, COUNT(DISTINCT e.user_id) AS dau
      FROM events e JOIN users u ON u.user_id = e.user_id
      WHERE u.is_test = 0 AND date(e.event_ts) BETWEEN '2024-03-01' AND '2024-03-31'
      GROUP BY date(e.event_ts))
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.T.to_string(header=False))
print("wrong, no spine (average only over days that have events):")
print(pd.read_sql_query(SQL_NO_SPINE, con).to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
a = events.merge(users[users["is_test"] == 0], on="user_id")
a["d"] = pd.to_datetime(a["event_ts"]).dt.normalize()
a = a[(a["d"] >= pd.Timestamp("2024-02-01")) & (a["d"] <= pd.Timestamp("2024-03-31"))]
a = a[["user_id", "d"]].drop_duplicates()
spine = pd.date_range("2024-03-01", "2024-03-31", freq="D")
dau = a.groupby("d")["user_id"].nunique().reindex(spine, fill_value=0)
in_month = a[a["d"] >= pd.Timestamp("2024-03-01")]
mau = in_month["user_id"].nunique()
trail = a[a["d"] >= pd.Timestamp("2024-03-31") - pd.Timedelta(days=29)]["user_id"].nunique()
pd_df = pd.DataFrame([{
    "days": len(dau), "user_days": int(dau.sum()), "avg_dau": round(dau.mean(), 4),
    "mau_calendar": mau, "stickiness_avg_dau": round(dau.mean() / mau, 4),
    "dau_last_day": int(dau.iloc[-1]), "mau_trailing_30": trail,
    "stickiness_last_day": round(dau.iloc[-1] / trail, 4)}])
# pd:end
print(pd_df.T.to_string(header=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # one row, same column order
print("pandas without the spine reindex, mean over active days only:",
      round(a[a["d"] >= pd.Timestamp("2024-03-01")].groupby("d")["user_id"].nunique().mean(), 4))
print("days with DAU > 0:", {k.strftime("%m-%d"): int(v) for k, v in dau[dau > 0].items()})
print("asserts passed")
```

**Output (my run):**
```text
days                 31.0000
user_days            12.0000
avg_dau               0.3871
mau_calendar          5.0000
stickiness_avg_dau    0.0774
dau_last_day          3.0000
mau_trailing_30       4.0000
stickiness_last_day   0.7500
wrong, no spine (average only over days that have events):
 avg_dau_active_days_only  days_counted
                      2.0             6
days                 31.0000
user_days            12.0000
avg_dau               0.3871
mau_calendar          5.0000
stickiness_avg_dau    0.0774
dau_last_day          3.0000
mau_trailing_30       4.0000
stickiness_last_day   0.7500
pandas without the spine reindex, mean over active days only: 2.0
days with DAU > 0: {'03-01': 3, '03-02': 2, '03-03': 1, '03-10': 2, '03-15': 1, '03-31': 3}
asserts passed
```

**Edge cases:**
- Days with no events: they must count as 0. `GROUP BY date` on events alone only has 6 rows here, so `AVG` is 2.0 instead of 0.3871 (printed as the wrong version).
- Test user 6: excluded from DAU and MAU together; keeping them would add 2 user-days and 1 MAU.
- Multiple events a day (user 3): `DISTINCT user, day` first, so a user is one active user per day.
- Events on 04-01 and 02-28: outside March, removed by the date range for the calendar MAU. The activity CTE keeps February so a trailing window that started before March could use it; here the trailing window starts 03-02, so it makes no difference.
- A month with 30 days or a partial current month: the number of spine days changes; for a partial month, either stop the spine at the last complete day or label it month-to-date.
- Zero MAU: `NULLIF` in SQL (not needed here), a guard in pandas, otherwise division by zero.

**Then explain:**
- Average of daily DAU over calendar MAU: sum of daily actives is total active user-days, so this equals (average number of active days per monthly-active user) / (days in the month). Stickiness 0.2 in words: on an average day one in five of the month's active users shows up, or equivalently the average monthly-active user is active on roughly one day in five (about 6 of 31). This identity holds only for calendar-month MAU.
- Last-day DAU over trailing MAU: a single day's snapshot over a rolling window; it is noisy (weekday or weekend, month-end) and the numerator and denominator are not built from the same period. Choose one definition, write it on the dashboard and never mix inputs.
- I do not quote a "good" DAU/MAU level: published rules of thumb are vendor heuristics and depend on the product's natural usage frequency; compare a product with its own history and with similar products.
- The per-day rolling version (every day gets a 30-day window) is Q33; retention tables are Part 6.
- Other engines (not executed here): Postgres `generate_series(date '2024-03-01', date '2024-03-31', interval '1 day')` for the spine, BigQuery `GENERATE_DATE_ARRAY`, MySQL 8 recursive CTE like SQLite.

**Follow-ups:**
- Why not `COUNT(*)` of events for DAU? Because heavy users and multi-event sessions inflate it; DAU counts users.
- Weekly stickiness? Replace the 31-day spine with weeks (state the week start; Monday here) and WAU; the same identity holds with days per week.
- What if the product has weekend-only usage? Then DAU/MAU understates its health; use a metric matched to usage frequency (metric design is Book 6).

**Common mistakes:**
- Averaging DAU over only days that appear in the data.
- Using MAU for a different period or window than the DAU average.
- Summing daily active users to get MAU.
- Counting events instead of distinct users.
- Forgetting test and internal users.
- Quoting a benchmark percentage as if it were a law.

### Q16 ⭐⭐⭐ 🟡 A metric defined in words, with ambiguity handling: you are told 'give me the monthly active buyer rate for last month'. Tables: users(user_id, signup_date, country, is_test) and orders(order_id, user_id, order_ts, amount, status). Write the clarifying questions you would ask (active buyer: any order or completed order; denominator: registered, active or monthly-active users; which month and time zone; test users; cancelled orders), then state your assumptions and write the query for the as-of month 2024-03, with the assumptions as comments, and show how the number moves when you flip each assumption on the sample data.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** Before writing SQL I ask what counts as a buyer, what the denominator is, which month in which time zone, and whether test users and cancelled orders count; then I state my assumptions, put them in the query as parameters, and show how much the number moves when each one flips.

**Clarifying questions I would ask:**
- Active buyer: any order placed, or a completed (paid) order? Do returned or cancelled orders count?
- Denominator: all registered users, users registered at the start of the month, or monthly active users (needs an events table, which this schema does not have)? Must the numerator be a subset of the denominator?
- Which month: "last month" relative to today is not reproducible, so I fix it to March 2024 as-of 2024-03-31; which time zone defines the month boundary (UTC or IST)?
- Test and internal users in or out? Is `is_test` ever NULL?
- Is the metric a user-level rate (distinct users) or order-level? A "rate" with distinct buyers on top suggests user-level.

**Assumptions I state (base case):**
- A1: buyer = at least one completed order in the month; cancelled orders do not count.
- A2: denominator = all non-test users registered on or before 2024-03-31.
- A3: test users excluded from numerator and denominator.
- A4: month boundaries in UTC (order_ts is UTC text); the month is [2024-03-01, 2024-04-01).
- A5: user-level: each user counts once.

**Schema and sample data:** ten users (user 10 is a test user, user 9 signs up in April, users 7 and 8 sign up in March) and seven orders. User 2 ordered at 2024-03-31 20:00 UTC, which is 2024-04-01 01:30 in IST; user 3 has only a cancelled order; user 5 has a completed order in January only; user 8 has only a cancelled order in March; the test user has a 500 order in March.
```sql
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-11-01','IN',0),(2,'2023-11-05','IN',0),(3,'2023-12-01','US',0),(4,'2023-12-10','UK',0),
 (5,'2024-01-15','IN',0),(6,'2024-02-10','US',0),(7,'2024-03-10','IN',0),(8,'2024-03-20','IN',0),
 (9,'2024-04-05','IN',0),(10,'2023-10-01','IN',1);
INSERT INTO orders VALUES
 (1,1,'2024-03-05 10:00:00',100,'completed'),
 (2,2,'2024-03-31 20:00:00',80,'completed'),
 (3,3,'2024-03-12 09:00:00',60,'cancelled'),
 (4,5,'2024-01-10 09:00:00',90,'completed'),
 (5,7,'2024-03-22 09:00:00',70,'completed'),
 (6,8,'2024-03-25 09:00:00',50,'cancelled'),
 (7,10,'2024-03-08 09:00:00',500,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block. The assumptions are named parameters and are written as comments at the top of the query:
```sql
-- A1 buyer: :any_status = 0 means a completed order is needed, 1 means any order counts
-- A2 denominator: :denom_mode = 'registered' means users with signup_date < :signup_before
-- A3 test users: dropped unless :incl_test = 1
-- A4 month: local time = UTC + :tz_min minutes, window [:m_start, :m_end)
-- A5 user level: DISTINCT users, numerator counted only among denominator users
WITH base AS (
  SELECT user_id, signup_date FROM users
  WHERE :incl_test = 1 OR is_test = 0
), o AS (
  SELECT user_id, status
  FROM orders
  WHERE datetime(order_ts, '+' || :tz_min || ' minutes') >= :m_start
    AND datetime(order_ts, '+' || :tz_min || ' minutes') <  :m_end
), buyers AS (
  SELECT DISTINCT user_id FROM o WHERE :any_status = 1 OR status = 'completed'
), denom AS (
  SELECT user_id FROM base WHERE :denom_mode = 'registered' AND signup_date < :signup_before
  UNION
  SELECT user_id FROM base WHERE :denom_mode = 'orderers' AND user_id IN (SELECT user_id FROM o)
)
SELECT COUNT(*) AS denominator,
       SUM(CASE WHEN d.user_id IN (SELECT user_id FROM buyers) THEN 1 ELSE 0 END) AS buyers,
       ROUND(100.0 * SUM(CASE WHEN d.user_id IN (SELECT user_id FROM buyers) THEN 1 ELSE 0 END)
             / NULLIF(COUNT(*), 0), 1) AS rate_pct
FROM denom d
```

**pandas answer:** the same parameters, as a function (shown once here and identical to the Code block):
```py
def pd_rate(users, orders, tz_min, any_status, incl_test, denom_mode, m_start, m_end, signup_before):
    base = users if incl_test == 1 else users[users["is_test"] == 0]
    o = orders.copy()
    o["local"] = pd.to_datetime(o["order_ts"]) + pd.Timedelta(minutes=tz_min)
    o = o[(o["local"] >= pd.Timestamp(m_start)) & (o["local"] < pd.Timestamp(m_end))]
    buyers = set(o[(o["status"] == "completed") | (any_status == 1)]["user_id"])
    if denom_mode == "registered":
        denom = set(base[base["signup_date"] < signup_before]["user_id"])
    else:
        denom = set(base["user_id"]) & set(o["user_id"])
    n_buy = len(denom & buyers)
    rate = round(100.0 * n_buy / len(denom), 1) if denom else float("nan")
    return len(denom), n_buy, rate
```

**Example:**
- Base case: completed orders in March UTC by non-test users are user 1 (03-05), user 2 (03-31 20:00 UTC) and user 7 (03-22), so 3 buyers. Registered non-test users up to 03-31: users 1 to 8, so the denominator is 8. 3 / 8 = 37.5 percent.
- Flip 1, any status: adds user 3 and user 8, 5 / 8 = 62.5 percent.
- Flip 2, denominator = registered before March: users 1 to 6; buyers must also be in the denominator, so user 7 drops out: 2 / 6 = 33.3 percent.
- Flip 3, denominator = users who placed any order in March (1, 2, 3, 7, 8): 3 / 5 = 60.0 percent. This is a different question (how many order-placers completed), not a share of the user base.
- Flip 4, IST month: user 2's order moves to 1 April, so buyers are users 1 and 7, 2 / 8 = 25.0 percent.
- Flip 5, test users in: 4 / 9 = 44.4 percent.

**Code:** run with `python3 -I`. Each scenario is run in SQL and in pandas and the three numbers (denominator, buyers, rate) are asserted equal; the scenario table is printed.
```python
# Q16: "monthly active buyer rate for last month" with assumptions as parameters (as-of month 2024-03)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-11-01','IN',0),(2,'2023-11-05','IN',0),(3,'2023-12-01','US',0),(4,'2023-12-10','UK',0),
 (5,'2024-01-15','IN',0),(6,'2024-02-10','US',0),(7,'2024-03-10','IN',0),(8,'2024-03-20','IN',0),
 (9,'2024-04-05','IN',0),(10,'2023-10-01','IN',1);
INSERT INTO orders VALUES
 (1,1,'2024-03-05 10:00:00',100,'completed'),
 (2,2,'2024-03-31 20:00:00',80,'completed'),
 (3,3,'2024-03-12 09:00:00',60,'cancelled'),
 (4,5,'2024-01-10 09:00:00',90,'completed'),
 (5,7,'2024-03-22 09:00:00',70,'completed'),
 (6,8,'2024-03-25 09:00:00',50,'cancelled'),
 (7,10,'2024-03-08 09:00:00',500,'completed');
"""

# Assumptions are parameters:
#   :m_start / :m_end   local month [start, end) as text; local time = UTC + :tz_min minutes
#   :any_status         0 = buyer needs a completed order, 1 = any order counts
#   :incl_test          0 = drop is_test users (assumption A3)
#   :denom_mode         'registered' = users with signup_date < :signup_before
#                       'orderers'   = users with any order in the month
SQL_MAIN = """
-- A1 buyer: :any_status = 0 means a completed order is needed, 1 means any order counts
-- A2 denominator: :denom_mode = 'registered' means users with signup_date < :signup_before
-- A3 test users: dropped unless :incl_test = 1
-- A4 month: local time = UTC + :tz_min minutes, window [:m_start, :m_end)
-- A5 user level: DISTINCT users, numerator counted only among denominator users
WITH base AS (
  SELECT user_id, signup_date FROM users
  WHERE :incl_test = 1 OR is_test = 0
), o AS (
  SELECT user_id, status
  FROM orders
  WHERE datetime(order_ts, '+' || :tz_min || ' minutes') >= :m_start
    AND datetime(order_ts, '+' || :tz_min || ' minutes') <  :m_end
), buyers AS (
  SELECT DISTINCT user_id FROM o WHERE :any_status = 1 OR status = 'completed'
), denom AS (
  SELECT user_id FROM base WHERE :denom_mode = 'registered' AND signup_date < :signup_before
  UNION
  SELECT user_id FROM base WHERE :denom_mode = 'orderers' AND user_id IN (SELECT user_id FROM o)
)
SELECT COUNT(*) AS denominator,
       SUM(CASE WHEN d.user_id IN (SELECT user_id FROM buyers) THEN 1 ELSE 0 END) AS buyers,
       ROUND(100.0 * SUM(CASE WHEN d.user_id IN (SELECT user_id FROM buyers) THEN 1 ELSE 0 END)
             / NULLIF(COUNT(*), 0), 1) AS rate_pct
FROM denom d
"""

BASE = dict(tz_min=0, any_status=0, incl_test=0, denom_mode="registered",
            m_start="2024-03-01 00:00:00", m_end="2024-04-01 00:00:00", signup_before="2024-04-01")
SCENARIOS = [
    ("base: completed orders, registered by 03-31, no test, UTC", {}),
    ("flip 1: any order status counts", {"any_status": 1}),
    ("flip 2: denominator = registered at the start of March", {"signup_before": "2024-03-01"}),
    ("flip 3: denominator = users who placed any order in March", {"denom_mode": "orderers"}),
    ("flip 4: month in IST (UTC + 330 minutes)", {"tz_min": 330}),
    ("flip 5: test users included", {"incl_test": 1}),
]

# pd:main
def pd_rate(users, orders, tz_min, any_status, incl_test, denom_mode, m_start, m_end, signup_before):
    base = users if incl_test == 1 else users[users["is_test"] == 0]
    o = orders.copy()
    o["local"] = pd.to_datetime(o["order_ts"]) + pd.Timedelta(minutes=tz_min)
    o = o[(o["local"] >= pd.Timestamp(m_start)) & (o["local"] < pd.Timestamp(m_end))]
    buyers = set(o[(o["status"] == "completed") | (any_status == 1)]["user_id"])
    if denom_mode == "registered":
        denom = set(base[base["signup_date"] < signup_before]["user_id"])
    else:
        denom = set(base["user_id"]) & set(o["user_id"])
    n_buy = len(denom & buyers)
    rate = round(100.0 * n_buy / len(denom), 1) if denom else float("nan")
    return len(denom), n_buy, rate
# pd:end

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
rows = []
for name, change in SCENARIOS:
    p = {**BASE, **change}
    den, buy, rate = con.execute(SQL_MAIN, p).fetchone()
    pden, pbuy, prate = pd_rate(users, orders, **p)
    assert (den, buy, rate) == (pden, pbuy, prate), (name, (den, buy, rate), (pden, pbuy, prate))
    rows.append({"scenario": name, "denominator": den, "buyers": buy, "rate_pct": rate})
print(pd.DataFrame(rows).to_string(index=False))

# who is behind the base number and the IST flip
print("base buyers:", sorted(r[0] for r in con.execute(
    "SELECT DISTINCT user_id FROM orders o WHERE status='completed' AND order_ts >= '2024-03-01' AND order_ts < '2024-04-01' "
    "AND user_id IN (SELECT user_id FROM users WHERE is_test = 0)")))
print("IST buyers:", sorted(r[0] for r in con.execute(
    "SELECT DISTINCT user_id FROM orders o WHERE status='completed' "
    "AND datetime(order_ts, '+330 minutes') >= '2024-03-01 00:00:00' AND datetime(order_ts, '+330 minutes') < '2024-04-01 00:00:00' "
    "AND user_id IN (SELECT user_id FROM users WHERE is_test = 0)")))
print("asserts passed")
```

**Output (my run):**
```text
                                                 scenario  denominator  buyers  rate_pct
base: completed orders, registered by 03-31, no test, UTC            8       3      37.5
                          flip 1: any order status counts            8       5      62.5
   flip 2: denominator = registered at the start of March            6       2      33.3
flip 3: denominator = users who placed any order in March            5       3      60.0
                 flip 4: month in IST (UTC + 330 minutes)            8       2      25.0
                              flip 5: test users included            9       4      44.4
base buyers: [1, 2, 7]
IST buyers: [1, 7]
asserts passed
```

**Edge cases:**
- The numerator must be a subset of the denominator: flip 2 drops user 7 from the numerator too, because a user registered in March is not in a start-of-month base.
- Time zone: with the IST month the rate falls from 37.5 to 25.0 percent and the buyer set changes (printed lists). The count of buyers can also stay the same while the members change, so check members, not only counts.
- Empty denominator (no users yet): `NULLIF` returns NULL in SQL; the pandas function returns NaN.
- `is_test` NULL: `is_test = 0` drops those users; decide and say so (`COALESCE(is_test, 0) = 0` keeps them).
- Users who order but are not in `users` (orphans) never reach the numerator here because the denominator is built from `users`; count them separately as a data-quality check.

**Then explain:**
- Fixed as-of month, never "last month" computed from the current date, so the answer is reproducible.
- Write assumptions in the query comments and in the reply; a number without its definition cannot be reconciled with another dashboard (Q19).
- Distinct users in the numerator, a user-level denominator, and numerator within denominator is what makes it a rate between 0 and 100.
- Six flips on eight users move the answer between 25.0 and 62.5 percent, so the definition matters more than the arithmetic.
- Metric design (is this the right metric?) is Book 6; this answer is only the SQL and the definitions.

**Follow-ups:**
- The product has an events table: what is "active"? Then the denominator can be monthly active users and the rate becomes the share of active users who bought (see Q39 for the several denominators side by side).
- Last month relative to today: pass the month as a parameter from the scheduler; do not call a current-date function in the query.
- Day of week or week-based "month" (4-4-5 calendar)? Ask for the calendar table (Part 6 Q31).

**Common mistakes:**
- Not asking which denominator and silently choosing one.
- Counting users with any order and calling them buyers.
- A numerator not restricted to the denominator users.
- Using current date for "last month".
- Ignoring the time zone of the month boundary.
- Forgetting test users.

### Q17 ⭐⭐⭐ 🔴 Time-window funnel with ordering: events(user_id, event_ts, event_name) with steps 'view' and 'purchase'. Count the users who purchased within 7 days after their first view (purchase_ts >= first_view_ts and purchase_ts <= first_view_ts plus 7 days), compute the conversion over all viewers who have a mature 7-day window at the as-of date 2024-03-31, and show a user who purchased 7 days and 1 minute later, a user who purchased exactly at 7 days (inclusive or not, state it), and a purchase before the first view. Use unixepoch arithmetic or datetime(first_view, '+7 days') (not julianday multiplication). Mention the difference between anchoring on the first view and on the latest view before the purchase.
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** For each user take the first view, keep only viewers whose 7-day window is fully observed by the as-of date (first view + 7 days before 2024-04-01 00:00), and count those with a purchase at or after the first view and no later than first view + 7 days (inclusive); I add the interval with `datetime(first_view, '+7 days')`, not `julianday` times a constant.

Conventions: timestamps are UTC ISO text, a purchase at exactly 7 days counts (inclusive), data is complete through the end of 2024-03-31, the window is anchored on the first view, and "converted" means any purchase inside the window.

**Schema and sample data:** nine users. User 1 purchases exactly 7 days after the first view; user 2 purchases 7 days and 1 minute after; user 3 purchased an hour before the first view; user 4 purchases next day; user 5 viewed and never bought; user 6 viewed on 03-28 and bought next day, but the window is not complete; user 7 views twice and buys the day after the second view; user 8 bought before and after his first view; user 9 purchased without any view.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-08 10:00:00','purchase'),
 (2,'2024-03-01 10:00:00','view'),(2,'2024-03-08 10:01:00','purchase'),
 (3,'2024-03-01 09:00:00','purchase'),(3,'2024-03-01 10:00:00','view'),
 (4,'2024-03-02 08:00:00','view'),(4,'2024-03-03 08:00:00','purchase'),
 (5,'2024-03-20 12:00:00','view'),
 (6,'2024-03-28 12:00:00','view'),(6,'2024-03-29 12:00:00','purchase'),
 (7,'2024-03-05 09:00:00','view'),(7,'2024-03-12 09:00:00','view'),(7,'2024-03-13 09:00:00','purchase'),
 (8,'2024-02-28 10:00:00','purchase'),(8,'2024-03-10 10:00:00','view'),(8,'2024-03-12 10:00:00','purchase'),
 (9,'2024-03-15 10:00:00','purchase');
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
WITH fv AS (
  SELECT user_id, MIN(event_ts) AS first_view
  FROM events
  WHERE event_name = 'view'
  GROUP BY user_id
), mature AS (
  SELECT user_id, first_view
  FROM fv
  WHERE datetime(first_view, '+7 days') < :as_of_end
), flagged AS (
  SELECT m.user_id,
         CASE WHEN EXISTS (
                SELECT 1 FROM events p
                WHERE p.user_id = m.user_id
                  AND p.event_name = 'purchase'
                  AND p.event_ts >= m.first_view
                  AND p.event_ts <= datetime(m.first_view, '+7 days')
              ) THEN 1 ELSE 0 END AS converted
  FROM mature m
)
SELECT COUNT(*) AS mature_viewers,
       SUM(converted) AS converted_7d,
       ROUND(100.0 * SUM(converted) / COUNT(*), 1) AS conversion_pct
FROM flagged
```

**pandas answer:** same logic with `Timedelta`, shown once here and identical to the Code block:
```py
ev = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
fv = (ev[ev["event_name"] == "view"].groupby("user_id", as_index=False)["event_ts"].min()
        .rename(columns={"event_ts": "first_view"}))
fv = fv[fv["first_view"] + pd.Timedelta(days=7) < pd.Timestamp(AS_OF_END)]
pu = ev[ev["event_name"] == "purchase"][["user_id", "event_ts"]].rename(columns={"event_ts": "purchase_ts"})
j = fv.merge(pu, on="user_id", how="left")
j["ok"] = (j["purchase_ts"] >= j["first_view"]) & (j["purchase_ts"] <= j["first_view"] + pd.Timedelta(days=7))
converted = int(j.groupby("user_id")["ok"].max().sum())
pd_df = pd.DataFrame([{"mature_viewers": len(fv), "converted_7d": converted,
                       "conversion_pct": round(100.0 * converted / len(fv), 1)}])
```

**Example:**
- First views: users 1 to 8 (user 9 never viewed, so is not a viewer). Mature if first view + 7 days is before 2024-04-01: user 6 (03-28 + 7 = 04-04) is not; all others are. So 7 mature viewers.
- User 1: window ends 03-08 10:00:00, purchase at exactly that second, counts (inclusive). User 2: purchase 10:01:00 is 60 seconds too late, no. User 3: the purchase is before the first view, no. User 4: yes. User 5: no purchase. User 7: first view 03-05 09:00, window ends 03-12 09:00, purchase on 03-13 is outside, no. User 8: the 02-28 purchase is before the view and does not count, the 03-12 purchase is inside the window (03-10 + 2 days), yes.
- Converted = users 1, 4, 8 = 3 of 7 = 42.9 percent.
- Without the maturity rule, user 6 joins the denominator and the numerator: 4 of 8 = 50.0 percent, a rate that looks better only because the immature user happened to buy quickly. Dropping every immature viewer, converted or not, is the consistent rule.
- Anchor on the latest view before each purchase instead: user 7's 03-13 purchase has a view one day earlier (03-12), so user 7 converts and the result is 4 of 7 = 57.1 percent (printed). With first-view anchoring, a user who views repeatedly and buys later is counted as a failure.

**Code:** run with `python3 -I`. The assert compares the one-row SQL result with the one-row pandas result.
```python
# Q17: purchase within 7 days after the first view, mature viewers only (as-of 2024-03-31)
import sqlite3
import pandas as pd

AS_OF_END = "2024-04-01 00:00:00"   # data complete up to (not including) this instant

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-08 10:00:00','purchase'),
 (2,'2024-03-01 10:00:00','view'),(2,'2024-03-08 10:01:00','purchase'),
 (3,'2024-03-01 09:00:00','purchase'),(3,'2024-03-01 10:00:00','view'),
 (4,'2024-03-02 08:00:00','view'),(4,'2024-03-03 08:00:00','purchase'),
 (5,'2024-03-20 12:00:00','view'),
 (6,'2024-03-28 12:00:00','view'),(6,'2024-03-29 12:00:00','purchase'),
 (7,'2024-03-05 09:00:00','view'),(7,'2024-03-12 09:00:00','view'),(7,'2024-03-13 09:00:00','purchase'),
 (8,'2024-02-28 10:00:00','purchase'),(8,'2024-03-10 10:00:00','view'),(8,'2024-03-12 10:00:00','purchase'),
 (9,'2024-03-15 10:00:00','purchase');
"""

SQL_MAIN = """
WITH fv AS (
  SELECT user_id, MIN(event_ts) AS first_view
  FROM events
  WHERE event_name = 'view'
  GROUP BY user_id
), mature AS (
  SELECT user_id, first_view
  FROM fv
  WHERE datetime(first_view, '+7 days') < :as_of_end
), flagged AS (
  SELECT m.user_id,
         CASE WHEN EXISTS (
                SELECT 1 FROM events p
                WHERE p.user_id = m.user_id
                  AND p.event_name = 'purchase'
                  AND p.event_ts >= m.first_view
                  AND p.event_ts <= datetime(m.first_view, '+7 days')
              ) THEN 1 ELSE 0 END AS converted
  FROM mature m
)
SELECT COUNT(*) AS mature_viewers,
       SUM(converted) AS converted_7d,
       ROUND(100.0 * SUM(converted) / COUNT(*), 1) AS conversion_pct
FROM flagged
"""

# per-user detail for the walk-through (includes the julianday check)
SQL_DETAIL = """
WITH fv AS (SELECT user_id, MIN(event_ts) AS first_view FROM events WHERE event_name = 'view' GROUP BY user_id)
SELECT fv.user_id, fv.first_view,
       datetime(fv.first_view, '+7 days') AS window_end,
       CASE WHEN datetime(fv.first_view, '+7 days') < :as_of_end THEN 1 ELSE 0 END AS mature,
       (SELECT MIN(p.event_ts) FROM events p WHERE p.user_id = fv.user_id AND p.event_name = 'purchase'
          AND p.event_ts >= fv.first_view) AS first_purchase_after_view,
       (SELECT MIN(unixepoch(p.event_ts) - unixepoch(fv.first_view)) FROM events p
         WHERE p.user_id = fv.user_id AND p.event_name = 'purchase' AND p.event_ts >= fv.first_view) AS secs_after_view
FROM fv ORDER BY fv.user_id
"""

# anchoring on the latest view before each purchase: a purchase converts if ANY view lies in the 7 days before it
SQL_LATEST_VIEW = """
WITH fv AS (SELECT user_id, MIN(event_ts) AS first_view FROM events WHERE event_name = 'view' GROUP BY user_id),
mature AS (SELECT user_id FROM fv WHERE datetime(first_view, '+7 days') < :as_of_end)
SELECT COUNT(*) AS mature_viewers,
       SUM(CASE WHEN EXISTS (
             SELECT 1 FROM events p JOIN events v
               ON v.user_id = p.user_id AND v.event_name = 'view'
              AND v.event_ts <= p.event_ts AND p.event_ts <= datetime(v.event_ts, '+7 days')
             WHERE p.user_id = m.user_id AND p.event_name = 'purchase'
           ) THEN 1 ELSE 0 END) AS converted_latest_view_anchor
FROM mature m
"""

# the julianday version for comparison
SQL_JULIAN = """
SELECT user_id, (julianday(p) - julianday(v)) * 86400 AS secs, (julianday(p) - julianday(v)) <= 7 AS within_7_julianday
FROM (SELECT e.user_id, MIN(CASE WHEN e.event_name='view' THEN e.event_ts END) AS v,
             MIN(CASE WHEN e.event_name='purchase' THEN e.event_ts END) AS p
      FROM events e GROUP BY e.user_id) WHERE user_id = 1
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"as_of_end": AS_OF_END}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))
print(pd.read_sql_query(SQL_DETAIL, con, params=P).to_string(index=False))
print("latest-view anchor:", pd.read_sql_query(SQL_LATEST_VIEW, con, params=P).to_dict("records"))
print("julianday check, user 1 (exactly 7 days):", con.execute(SQL_JULIAN).fetchall())

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
ev = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
fv = (ev[ev["event_name"] == "view"].groupby("user_id", as_index=False)["event_ts"].min()
        .rename(columns={"event_ts": "first_view"}))
fv = fv[fv["first_view"] + pd.Timedelta(days=7) < pd.Timestamp(AS_OF_END)]
pu = ev[ev["event_name"] == "purchase"][["user_id", "event_ts"]].rename(columns={"event_ts": "purchase_ts"})
j = fv.merge(pu, on="user_id", how="left")
j["ok"] = (j["purchase_ts"] >= j["first_view"]) & (j["purchase_ts"] <= j["first_view"] + pd.Timedelta(days=7))
converted = int(j.groupby("user_id")["ok"].max().sum())
pd_df = pd.DataFrame([{"mature_viewers": len(fv), "converted_7d": converted,
                       "conversion_pct": round(100.0 * converted / len(fv), 1)}])
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # one row
# without the maturity rule, everyone who viewed counts, including user 6
fv_all = (ev[ev["event_name"] == "view"].groupby("user_id", as_index=False)["event_ts"].min()
            .rename(columns={"event_ts": "first_view"}))
j2 = fv_all.merge(pu, on="user_id", how="left")
j2["ok"] = (j2["purchase_ts"] >= j2["first_view"]) & (j2["purchase_ts"] <= j2["first_view"] + pd.Timedelta(days=7))
print("no maturity rule: viewers", len(fv_all), "converted", int(j2.groupby("user_id")["ok"].max().sum()),
      "rate", round(100.0 * int(j2.groupby("user_id")["ok"].max().sum()) / len(fv_all), 1))
print("asserts passed")
```

**Output (my run):**
```text
 mature_viewers  converted_7d  conversion_pct
              7             3            42.9
 user_id          first_view          window_end  mature first_purchase_after_view  secs_after_view
       1 2024-03-01 10:00:00 2024-03-08 10:00:00       1       2024-03-08 10:00:00         604800.0
       2 2024-03-01 10:00:00 2024-03-08 10:00:00       1       2024-03-08 10:01:00         604860.0
       3 2024-03-01 10:00:00 2024-03-08 10:00:00       1                       NaN              NaN
       4 2024-03-02 08:00:00 2024-03-09 08:00:00       1       2024-03-03 08:00:00          86400.0
       5 2024-03-20 12:00:00 2024-03-27 12:00:00       1                       NaN              NaN
       6 2024-03-28 12:00:00 2024-04-04 12:00:00       0       2024-03-29 12:00:00          86400.0
       7 2024-03-05 09:00:00 2024-03-12 09:00:00       1       2024-03-13 09:00:00         691200.0
       8 2024-03-10 10:00:00 2024-03-17 10:00:00       1       2024-03-12 10:00:00         172800.0
latest-view anchor: [{'mature_viewers': 7, 'converted_latest_view_anchor': 4}]
julianday check, user 1 (exactly 7 days): [(1, 604800.0, 1)]
 mature_viewers  converted_7d  conversion_pct
              7             3            42.9
no maturity rule: viewers 8 converted 4 rate 50.0
asserts passed
```

**Edge cases:**
- Exactly 7 days: included by `<=`; use `<` if the product definition says "within fewer than 7 days". 7 days and 1 minute is out either way. Say which you chose.
- `julianday` check printed above for user 1 (exactly 7 days apart): on this machine and this pair the float difference came out as exactly 604800 seconds and the comparison was true, so here julianday happened to work. It is not guaranteed for other timestamps (Part 7 Q11 shows a 30-minute case where a julianday threshold misfired), so I use `datetime()` text comparison or `unixepoch` integers.
- Purchase before the first view (user 3, and user 8's early purchase): not in the window; user 8 still converts through a later purchase.
- User with a purchase and no view (user 9): not a viewer, not in the denominator.
- Several purchases in the window count once (`EXISTS`).
- Text comparison works only because all timestamps have the same `YYYY-MM-DD HH:MM:SS` shape and `datetime()` produces that shape; an ISO value with a `T` separator would compare wrongly.
- Time zone: all UTC here; a local-time window would add an offset first (Part 6 Q16).

**Then explain:**
- Maturity: a viewer is only counted when the whole 7-day window has been observed, otherwise recent viewers drag the rate down (same idea as Q12). Never mark mature by "has purchased".
- First-view anchoring treats the funnel as one attempt per user; per-attempt conversion (every view starts its own window) is Q40, and the latest-view anchor is the same EXISTS with a self-join, as shown.
- The order condition `purchase_ts >= first_view` is the ordering requirement; the any-order funnel in Q2 does not check it, the strict MIN(CASE) funnel is in Q7.
- Other engines (not executed here): Postgres `first_view + INTERVAL '7 days'`, MySQL `DATE_ADD(first_view, INTERVAL 7 DAY)`, BigQuery `TIMESTAMP_ADD(first_view, INTERVAL 7 DAY)`, Snowflake `DATEADD(day, 7, first_view)`.

**Follow-ups:**
- Rolling conversion by view-date cohort? Group the mature viewers by `date(first_view)` and keep only dates old enough.
- Window starts at the first view or at the first session? Anchor choice is a definition to confirm.
- Cost: the correlated `EXISTS` can use an index on `(user_id, event_name, event_ts)`; I did not benchmark it here.

**Common mistakes:**
- Not requiring `purchase_ts >= first_view`.
- Keeping immature viewers in the denominator.
- Multiplying a julianday difference by a constant and comparing for equality or a tight threshold.
- Counting purchases instead of users.
- Leaving out the boundary decision (inclusive or not).

### Q18 ⭐⭐⭐ 🔴 pandas funnel on the same data as SQL: events DataFrame with columns user_id, event_ts, event_name, channel (channel can be NaN). Build the funnel step counts with groupby and nunique, the strict ordered funnel via a per-user first-timestamp table (pivot_table with aggfunc='min' or groupby().min() on a pivot) and a merge-per-step version, and show the by-channel conversion with pivot_table(dropna=...). Assert the pandas result equals the SQL result from a sqlite3 run of the same data. Explain why nunique skips NaN user ids, why groupby drops NaN channel keys unless dropna=False, and why pivot_table with its default aggfunc='mean' is a trap for counts.
**Asked at:** pandas reference pages for pivot_table and crosstab (both opened: pivot_table dropna=True drops NaN keys and all-NaN columns, observed default True in 3.0.0; crosstab normalize accepts all/index/columns and dropna drops empty categories) plus expert gap-check on groupby, nunique and rounding behaviour; documentation, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Step counts are `groupby("event_name")["user_id"].nunique()`, the strict funnel is a per-user table of first timestamps (a `pivot_table` with `aggfunc="min"`) compared column by column, the by-channel table is a `pivot_table` with `aggfunc="nunique"` after turning NaN channels into an explicit label, and every result is asserted equal to the SQL run on the same rows.

Conventions: UTC timestamps, no test-user column in this table, strict means first view < first cart < first purchase (the Q7 definition), a channel is the channel of the event itself, and an event with a missing user id cannot be a user.

**Schema and sample data:** sixteen events. User 3 carts twice and has a purchase before the view; user 4 has NULL channel on all events; user 5 is in two channels; the last row has a NULL user id (an anonymous event). Loaded through `pd.read_sql_query`, the NULL makes `user_id` a float column.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT, channel TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view','ads'),(1,'2024-03-01 10:05:00','cart','ads'),(1,'2024-03-01 10:10:00','purchase','ads'),
 (2,'2024-03-01 11:00:00','view','organic'),(2,'2024-03-01 11:30:00','cart','organic'),
 (3,'2024-03-02 09:00:00','view','ads'),(3,'2024-03-02 09:30:00','cart','ads'),(3,'2024-03-02 09:40:00','cart','ads'),
 (3,'2024-03-02 08:00:00','purchase','ads'),
 (4,'2024-03-02 10:00:00','view',NULL),(4,'2024-03-02 10:10:00','cart',NULL),(4,'2024-03-02 10:20:00','purchase',NULL),
 (5,'2024-03-03 12:00:00','view','ads'),(5,'2024-03-03 12:05:00','view','organic'),(5,'2024-03-03 12:30:00','purchase','organic'),
 (NULL,'2024-03-03 13:00:00','view','ads');
```

**SQL answer:** three queries in the Code block. Step counts (any order):
```sql
SELECT COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)     AS view_users,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END)     AS cart_users,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchase_users
FROM events
```
Strict ordered funnel (cumulative: each step needs the previous one, in time order):
```sql
WITH t AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view' THEN event_ts END)     AS t_view,
         MIN(CASE WHEN event_name = 'cart' THEN event_ts END)     AS t_cart,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS t_purchase
  FROM events
  WHERE user_id IS NOT NULL
  GROUP BY user_id
)
SELECT COUNT(t_view)                                                       AS viewers,
       SUM(CASE WHEN t_cart > t_view THEN 1 ELSE 0 END)                    AS then_cart,
       SUM(CASE WHEN t_cart > t_view AND t_purchase > t_cart THEN 1 ELSE 0 END) AS then_purchase
FROM t
```
By channel, NULL shown as `unknown`:
```sql
SELECT COALESCE(channel, 'unknown') AS channel,
       COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)     AS view,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END)     AS cart,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchase,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END), 0), 1) AS conv_pct
FROM events
GROUP BY COALESCE(channel, 'unknown')
ORDER BY view DESC, channel
```

**pandas answer:** four snippets, identical to the Code block. Step counts:
```py
counts = ev.groupby("event_name")["user_id"].nunique().reindex(steps)
pd_steps = pd.DataFrame([{"view_users": counts["view"], "cart_users": counts["cart"],
                          "purchase_users": counts["purchase"]}])
```
Strict funnel through a per-user first-timestamp table (the `groupby().min().unstack()` form is asserted identical):
```py
first = ev.pivot_table(index="user_id", columns="event_name", values="event_ts", aggfunc="min")
first_g = ev.groupby(["user_id", "event_name"])["event_ts"].min().unstack()   # same table, groupby form
assert first.equals(first_g.reindex(columns=first.columns))
ok_cart = first["cart"] > first["view"]
ok_purchase = ok_cart & (first["purchase"] > first["cart"])
pd_strict = pd.DataFrame([{"viewers": int(first["view"].notna().sum()),
                           "then_cart": int(ok_cart.sum()), "then_purchase": int(ok_purchase.sum())}])
```
Merge-per-step version (each step is its own per-user table, merged and filtered in order):
```py
def step_first(name):
    s = ev[ev["event_name"] == name].groupby("user_id")["event_ts"].min()
    return s.rename("t_" + name).reset_index()
m1 = step_first("view").merge(step_first("cart"), on="user_id")
m1 = m1[m1["t_cart"] > m1["t_view"]]
m2 = m1.merge(step_first("purchase"), on="user_id")
m2 = m2[m2["t_purchase"] > m2["t_cart"]]
merge_counts = (step_first("view")["user_id"].nunique(), len(m1), len(m2))
```
By channel, with the NaN channel made explicit before pivoting:
```py
ch = ev.assign(channel=ev["channel"].fillna("unknown"))
pv = ch.pivot_table(index="channel", columns="event_name", values="user_id",
                    aggfunc="nunique", fill_value=0)[steps]
pv["conv_pct"] = (100.0 * pv["purchase"] / pv["view"].where(pv["view"] > 0)).round(1)
pd_channel = (pv.reset_index().sort_values(["view", "channel"], ascending=[False, True])
                .reset_index(drop=True))
```

**Example:**
- Any-order steps: view users 1, 2, 3, 4, 5 = 5 (the NULL-user row is not a user); cart users 1, 2, 3, 4 = 4; purchase users 1, 3, 4, 5 = 4.
- Strict: user 1 passes view, cart (10:05 > 10:00) and purchase (10:10 > 10:05). User 2 has no purchase. User 3 has a first cart 09:30 after the first view 09:00, but the purchase at 08:00 is before the cart, so stops after cart. User 4 passes everything. User 5 has no cart. Result 5 viewers, 4 with a later cart (users 1, 2, 3, 4), 2 with a later purchase (users 1, 4).
- By channel: ads view users 1, 3, 5 (3); organic view users 2, 5 (2); unknown view user 4 (1). Channel view rows add to 6 but there are 5 distinct viewers, because user 5 viewed in two channels. Conversion view to purchase: ads 2 / 3 = 66.7, organic 1 / 2 = 50.0, unknown 1 / 1 = 100.0 (any-order inside each channel, so user 3's earlier purchase counts for ads).

**Code:** run with `python3 -I`. Asserts: step counts, strict counts (both the pivot version and the merge version) and the channel table all equal the SQL results; the channel table is compared after ordering by `view` descending, then `channel`.
```python
# Q18: the funnel in pandas, checked against SQL on the same data
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT, channel TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view','ads'),(1,'2024-03-01 10:05:00','cart','ads'),(1,'2024-03-01 10:10:00','purchase','ads'),
 (2,'2024-03-01 11:00:00','view','organic'),(2,'2024-03-01 11:30:00','cart','organic'),
 (3,'2024-03-02 09:00:00','view','ads'),(3,'2024-03-02 09:30:00','cart','ads'),(3,'2024-03-02 09:40:00','cart','ads'),
 (3,'2024-03-02 08:00:00','purchase','ads'),
 (4,'2024-03-02 10:00:00','view',NULL),(4,'2024-03-02 10:10:00','cart',NULL),(4,'2024-03-02 10:20:00','purchase',NULL),
 (5,'2024-03-03 12:00:00','view','ads'),(5,'2024-03-03 12:05:00','view','organic'),(5,'2024-03-03 12:30:00','purchase','organic'),
 (NULL,'2024-03-03 13:00:00','view','ads');
"""

SQL_STEPS = """
SELECT COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)     AS view_users,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END)     AS cart_users,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchase_users
FROM events
"""

SQL_STRICT = """
WITH t AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view' THEN event_ts END)     AS t_view,
         MIN(CASE WHEN event_name = 'cart' THEN event_ts END)     AS t_cart,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS t_purchase
  FROM events
  WHERE user_id IS NOT NULL
  GROUP BY user_id
)
SELECT COUNT(t_view)                                                       AS viewers,
       SUM(CASE WHEN t_cart > t_view THEN 1 ELSE 0 END)                    AS then_cart,
       SUM(CASE WHEN t_cart > t_view AND t_purchase > t_cart THEN 1 ELSE 0 END) AS then_purchase
FROM t
"""

SQL_CHANNEL = """
SELECT COALESCE(channel, 'unknown') AS channel,
       COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)     AS view,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END)     AS cart,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchase,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END), 0), 1) AS conv_pct
FROM events
GROUP BY COALESCE(channel, 'unknown')
ORDER BY view DESC, channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_steps = pd.read_sql_query(SQL_STEPS, con)
sql_strict = pd.read_sql_query(SQL_STRICT, con)
sql_channel = pd.read_sql_query(SQL_CHANNEL, con)
print(sql_steps.to_string(index=False)); print(sql_strict.to_string(index=False)); print(sql_channel.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)   # user_id becomes float64 because of the NULL
print(events.dtypes.to_dict())
steps = ["view", "cart", "purchase"]
ev = events.assign(event_ts=pd.to_datetime(events["event_ts"]))

# pd:steps
counts = ev.groupby("event_name")["user_id"].nunique().reindex(steps)
pd_steps = pd.DataFrame([{"view_users": counts["view"], "cart_users": counts["cart"],
                          "purchase_users": counts["purchase"]}])
# pd:end
pd.testing.assert_frame_equal(sql_steps, pd_steps, check_dtype=False)

# pd:strict
first = ev.pivot_table(index="user_id", columns="event_name", values="event_ts", aggfunc="min")
first_g = ev.groupby(["user_id", "event_name"])["event_ts"].min().unstack()   # same table, groupby form
assert first.equals(first_g.reindex(columns=first.columns))
ok_cart = first["cart"] > first["view"]
ok_purchase = ok_cart & (first["purchase"] > first["cart"])
pd_strict = pd.DataFrame([{"viewers": int(first["view"].notna().sum()),
                           "then_cart": int(ok_cart.sum()), "then_purchase": int(ok_purchase.sum())}])
# pd:end
pd.testing.assert_frame_equal(sql_strict, pd_strict, check_dtype=False)

# pd:merge
def step_first(name):
    s = ev[ev["event_name"] == name].groupby("user_id")["event_ts"].min()
    return s.rename("t_" + name).reset_index()
m1 = step_first("view").merge(step_first("cart"), on="user_id")
m1 = m1[m1["t_cart"] > m1["t_view"]]
m2 = m1.merge(step_first("purchase"), on="user_id")
m2 = m2[m2["t_purchase"] > m2["t_cart"]]
merge_counts = (step_first("view")["user_id"].nunique(), len(m1), len(m2))
# pd:end
assert merge_counts == tuple(sql_strict.iloc[0]), merge_counts

# pd:channel
ch = ev.assign(channel=ev["channel"].fillna("unknown"))
pv = ch.pivot_table(index="channel", columns="event_name", values="user_id",
                    aggfunc="nunique", fill_value=0)[steps]
pv["conv_pct"] = (100.0 * pv["purchase"] / pv["view"].where(pv["view"] > 0)).round(1)
pd_channel = (pv.reset_index().sort_values(["view", "channel"], ascending=[False, True])
                .reset_index(drop=True))
# pd:end
pd.testing.assert_frame_equal(sql_channel, pd_channel[["channel", "view", "cart", "purchase", "conv_pct"]],
                              check_dtype=False, check_names=False)
print(pd_channel.to_string(index=False))

print("--- behaviours demonstrated ---")
print("nunique skips NaN:", events["user_id"].nunique(), "| nunique(dropna=False):", events["user_id"].nunique(dropna=False),
      "| len(set(...)):", len(set(events["user_id"])))
print("groupby default drops the NaN channel:", events.groupby("channel")["user_id"].size().to_dict())
print("groupby(dropna=False) keeps it:", events.groupby("channel", dropna=False)["user_id"].size().to_dict())
print("SQL GROUP BY keeps a NULL group:", con.execute("SELECT channel, COUNT(*) FROM events GROUP BY channel ORDER BY channel").fetchall())
raw = events.pivot_table(index="channel", columns="event_name", values="user_id", aggfunc="nunique")
print("pivot_table on raw channel (default dropna=True), index:", list(raw.index))
raw2 = events.pivot_table(index="channel", columns="event_name", values="user_id", aggfunc="nunique", dropna=False)
print("pivot_table(dropna=False), index:", list(raw2.index))
trap = events.pivot_table(index="channel", columns="event_name", values="user_id")
print("pivot_table with the default aggfunc='mean' on user_id:")
print(trap.to_string())
print("merge on NaN keys matches NaN with NaN:",
      len(pd.DataFrame({"k": [1.0, np.nan]}).merge(pd.DataFrame({"k": [np.nan, 2.0]}), on="k")),
      "| SQL join on NULL keys:",
      con.execute("SELECT COUNT(*) FROM (SELECT NULL AS k) a JOIN (SELECT NULL AS k) b ON a.k = b.k").fetchone()[0])
print("total of channel view rows:", int(pd_channel["view"].sum()), "vs distinct viewers:", int(pd_steps["view_users"].iloc[0]))
print("asserts passed")
```

**Output (my run):**
```text
 view_users  cart_users  purchase_users
          5           4               4
 viewers  then_cart  then_purchase
       5          4              2
channel  view  cart  purchase  conv_pct
    ads     3     2         2      66.7
organic     2     1         1      50.0
unknown     1     1         1     100.0
{'user_id': dtype('float64'), 'event_ts': <StringDtype(storage='python', na_value=nan)>, 'event_name': <StringDtype(storage='python', na_value=nan)>, 'channel': <StringDtype(storage='python', na_value=nan)>}
channel  view  cart  purchase  conv_pct
    ads     3     2         2      66.7
organic     2     1         1      50.0
unknown     1     1         1     100.0
--- behaviours demonstrated ---
nunique skips NaN: 5 | nunique(dropna=False): 6 | len(set(...)): 6
groupby default drops the NaN channel: {'ads': 9, 'organic': 4}
groupby(dropna=False) keeps it: {'ads': 9, 'organic': 4, nan: 3}
SQL GROUP BY keeps a NULL group: [(None, 3), ('ads', 9), ('organic', 4)]
pivot_table on raw channel (default dropna=True), index: ['ads', 'organic']
pivot_table(dropna=False), index: ['ads', 'organic', nan]
pivot_table with the default aggfunc='mean' on user_id:
event_name      cart  purchase  view
channel                             
ads         2.333333       2.0   3.0
organic     2.000000       5.0   3.5
merge on NaN keys matches NaN with NaN: 1 | SQL join on NULL keys: 0
total of channel view rows: 6 vs distinct viewers: 5
asserts passed
```

**Edge cases:**
- Missing user id: `nunique()` skips NaN (5 users), `nunique(dropna=False)` and `len(set(...))` count the NaN as one more (6). SQL `COUNT(DISTINCT user_id)` also skips NULL, so pandas `nunique()` and SQL agree; `len(set())` does not. The anonymous row is dropped from every funnel step, which is right for a user funnel but should be reported as a count of events lost.
- NaN channel: `groupby("channel")` drops the NaN group by default (4 and 9 events for organic and ads, the 3 unknown events vanish); `dropna=False` keeps it. SQL `GROUP BY` keeps a NULL group. `pivot_table` with the default `dropna=True` also loses the NaN channel (index shows only ads and organic); with `dropna=False` it keeps a NaN row (printed). My choice is to `fillna("unknown")` first, which works the same everywhere.
- `pivot_table` default `aggfunc="mean"`: on `user_id` it returns the mean of user ids per cell (2.33, 5.0, 3.5 in the printout), a plausible-looking but meaningless number. Always pass `aggfunc="nunique"` or `"size"` for counts.
- `merge` on NaN keys: pandas matches NaN with NaN (1 matched row printed) whereas a SQL join on NULL keys matches nothing (0). The funnel merges are safe here because the NaN user was already dropped by the `groupby`, but a merge built on a raw column is not.
- A step that never occurs (no purchases) would give a missing column in `pivot_table`; `reindex(columns=steps)` or the `[steps]` selection should be guarded for that case.
- Repeated cart events (user 3) collapse into one first timestamp, so repeated events do not matter for the strict funnel.

**Then explain:**
- Why `nunique` skips NaN user ids: it counts distinct non-missing values, the pandas equivalent of `COUNT(DISTINCT col)`; a missing id is not an identifiable user.
- Why `groupby` drops NaN channel keys: the default `dropna=True` excludes them; set `dropna=False` or fill them, or the by-channel totals silently shrink.
- Why `pivot_table` with the default `aggfunc="mean"` is a trap for counts: it averages the values column. For counts of users use `aggfunc="nunique"`, for rows `"size"` or `"count"`.
- The strict funnel uses a per-user table of first timestamps; the merge-per-step version gives the same counts and is easier to extend with "within 7 days" conditions (Q17) or other per-step filters.
- `pivot_table` defaults depend on the pandas version (`observed` default True from 3.0 for categorical keys, as the docs page I read states); I ran everything on pandas 3.0.5 and the default `dropna=True` behaviour above is what the run printed.
- Other engines for the SQL (not executed here): BigQuery `COUNTIF` and Snowflake `COUNT(DISTINCT IFF(...))` replace the CASE forms; the logic is the same.

**Follow-ups:**
- Time window per step? Add `& (t_cart <= t_view + pd.Timedelta(days=7))` in the merge version.
- Why does the strict funnel give fewer users than the any-order funnel? Because it also checks order; the any-order funnel counts user 3's purchase, the strict one does not (Q7).
- Large data: pivoting minima is a single pass; a merge per step shuffles the data once per step.

**Common mistakes:**
- `pivot_table` without `aggfunc` on an ID column.
- Counting rows instead of `nunique`.
- Forgetting that `groupby` drops NaN keys, so channel totals do not add to the funnel.
- Assuming a pandas merge behaves like a SQL join on missing keys.
- Rounding before comparing pandas with SQL.
- Pivoting with a step that is missing in some slice and then indexing a column that is not there.

### Q19 ⭐⭐ 🟡 Two dashboards disagree on DAU: a growth dashboard shows 1,250 DAU for 2024-03-05 and a finance dashboard shows 1,190. events(user_id, event_ts_utc, event_name) and users(user_id, signup_date, country, is_test). Build a reconciliation query on small data that isolates the differences one at a time: UTC day versus IST day (event_ts_utc plus 330 minutes), test and internal users, background events versus intent events (event_name filter), duplicate user ids from a merged or anonymous id, and counting events versus users. Show a table of DAU after each filter step so the gap is fully explained, and say what you ask each dashboard owner.
**Asked at:** active-user guides: Basedash DAU/WAU/MAU pitfalls article (opened; active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users) plus search snippets of oneuptime ClickHouse DAU/WAU/MAU and stickiness posts and Swace and pmtoolkit pages (not opened); guides, not candidate reports; product analytics and data scientist rounds at social, streaming and SaaS companies
**Say this first (1 line):** I list every definition choice that could differ (day boundary, test users, event types, identity merging, events versus users), put each behind a parameter of one DAU query, and print DAU after each switch so the gap from the growth number to the finance number is fully explained, then ask each owner which choice their dashboard makes.

The 1,250 and 1,190 in the question are the dashboards' numbers; I cannot reproduce them, so the table below is a small stand-in that shows the method. I assume `identity_map(alias_id, user_id)` exists (the question mentions merged and anonymous ids but lists no mapping table), with one row per alias, otherwise the join itself would fan out.

**Schema and sample data:** nine users (7 and 8 are test users), two alias ids (101 is user 1 before login, 102 is user 3), thirteen events on or near 2024-03-05 in UTC. `heartbeat` is a background event, `open` and `click` are intent events. User 4's click at 20:00 UTC is 01:30 on 6 March in IST; user 5's click at 19:00 UTC on 4 March is 00:30 on 5 March in IST; user 9's at 22:00 UTC is on 6 March in IST. User 6 has two events (events versus users), user 2 has two heartbeats.
```sql
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE identity_map(alias_id INTEGER, user_id INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts_utc TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','IN',0),(4,'2024-01-01','IN',0),
 (5,'2024-01-01','IN',0),(6,'2024-01-01','IN',0),(7,'2024-01-01','IN',1),(8,'2024-01-01','IN',1),
 (9,'2024-01-01','IN',0);
INSERT INTO identity_map VALUES (101,1),(102,3);
INSERT INTO events VALUES
 (1,'2024-03-05 04:00:00','open'),
 (2,'2024-03-05 05:00:00','heartbeat'),(2,'2024-03-05 05:30:00','heartbeat'),
 (3,'2024-03-05 06:00:00','click'),
 (4,'2024-03-05 20:00:00','click'),
 (5,'2024-03-04 19:00:00','click'),
 (7,'2024-03-05 07:00:00','open'),
 (101,'2024-03-05 08:00:00','open'),
 (102,'2024-03-05 09:00:00','click'),
 (6,'2024-03-05 12:00:00','click'),(6,'2024-03-05 13:00:00','click'),
 (8,'2024-03-05 10:00:00','heartbeat'),
 (9,'2024-03-05 22:00:00','click');
```

**SQL answer:** `SQL_MAIN` in the Code block, with five parameters. It returns both the event count and the distinct user count for one day:
```sql
WITH ev AS (
  SELECT CASE WHEN :merge = 1 THEN COALESCE(m.user_id, e.user_id) ELSE e.user_id END AS uid,
         e.event_name,
         date(datetime(e.event_ts_utc, '+' || :tz_min || ' minutes')) AS d
  FROM events e
  LEFT JOIN identity_map m ON m.alias_id = e.user_id
)
SELECT COUNT(*) AS events, COUNT(DISTINCT ev.uid) AS users
FROM ev
LEFT JOIN users u ON u.user_id = ev.uid
WHERE ev.d = :day
  AND (:excl_test = 0 OR COALESCE(u.is_test, 0) = 0)
  AND (:intent_only = 0 OR ev.event_name <> 'heartbeat')
```

**pandas answer:** the same parameters as a function (shown once here and identical to the Code block):
```py
def pd_dau(events, users, idmap, day, tz_min, excl_test, intent_only, merge):
    e = events.merge(idmap, left_on="user_id", right_on="alias_id", how="left", suffixes=("", "_m"))
    e["uid"] = e["user_id_m"].fillna(e["user_id"]) if merge == 1 else e["user_id"]
    e["d"] = (pd.to_datetime(e["event_ts_utc"]) + pd.Timedelta(minutes=tz_min)).dt.strftime("%Y-%m-%d")
    e = e.merge(users[["user_id", "is_test"]].rename(columns={"user_id": "uid"}), on="uid", how="left")
    e["is_test"] = e["is_test"].fillna(0)
    e = e[e["d"] == day]
    if excl_test == 1:
        e = e[e["is_test"] == 0]
    if intent_only == 1:
        e = e[e["event_name"] != "heartbeat"]
    return len(e), e["uid"].nunique()
```

**Example:** growth definition (UTC day 2024-03-05, every event, raw ids, test users in):
- 12 events on that UTC day (user 5's event is on the 4th). Distinct raw ids: users 1, 2, 3, 4, 6, 7, 8, 9 and aliases 101, 102 = 10.
- Excluding test users 7 and 8 gives 8. Intent events only removes user 2, who only sent heartbeats, giving 7. Merging aliases 101 and 102 into users 1 and 3 gives 5 (users 1, 3, 4, 6, 9).
- Switching to the IST day removes users 4 and 9 and adds user 5, giving 4 (users 1, 3, 5, 6).
- Cumulative path 10, 8, 7, 5, 4. The events column starts at 12 because it counts events, not users: even the first dashboard difference could just be events versus users.

**Code:** run with `python3 -I`. Every row of both tables is run in SQL and pandas and the (events, users) pairs are asserted equal.
```python
# Q19: reconcile two DAU numbers for 2024-03-05, one cause at a time
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE identity_map(alias_id INTEGER, user_id INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts_utc TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','IN',0),(4,'2024-01-01','IN',0),
 (5,'2024-01-01','IN',0),(6,'2024-01-01','IN',0),(7,'2024-01-01','IN',1),(8,'2024-01-01','IN',1),
 (9,'2024-01-01','IN',0);
INSERT INTO identity_map VALUES (101,1),(102,3);
INSERT INTO events VALUES
 (1,'2024-03-05 04:00:00','open'),
 (2,'2024-03-05 05:00:00','heartbeat'),(2,'2024-03-05 05:30:00','heartbeat'),
 (3,'2024-03-05 06:00:00','click'),
 (4,'2024-03-05 20:00:00','click'),
 (5,'2024-03-04 19:00:00','click'),
 (7,'2024-03-05 07:00:00','open'),
 (101,'2024-03-05 08:00:00','open'),
 (102,'2024-03-05 09:00:00','click'),
 (6,'2024-03-05 12:00:00','click'),(6,'2024-03-05 13:00:00','click'),
 (8,'2024-03-05 10:00:00','heartbeat'),
 (9,'2024-03-05 22:00:00','click');
"""

# parameters: :day (local day), :tz_min (0 = UTC day, 330 = IST day), :excl_test, :intent_only, :merge
SQL_MAIN = """
WITH ev AS (
  SELECT CASE WHEN :merge = 1 THEN COALESCE(m.user_id, e.user_id) ELSE e.user_id END AS uid,
         e.event_name,
         date(datetime(e.event_ts_utc, '+' || :tz_min || ' minutes')) AS d
  FROM events e
  LEFT JOIN identity_map m ON m.alias_id = e.user_id
)
SELECT COUNT(*) AS events, COUNT(DISTINCT ev.uid) AS users
FROM ev
LEFT JOIN users u ON u.user_id = ev.uid
WHERE ev.d = :day
  AND (:excl_test = 0 OR COALESCE(u.is_test, 0) = 0)
  AND (:intent_only = 0 OR ev.event_name <> 'heartbeat')
"""

BASE = dict(day="2024-03-05", tz_min=0, excl_test=0, intent_only=0, merge=0)
CUM = [
    ("growth dashboard: UTC day, every event, raw ids, test users in", {}),
    ("+ exclude test users", {"excl_test": 1}),
    ("+ intent events only (drop heartbeat)", {"intent_only": 1}),
    ("+ merge alias ids (identity_map)", {"merge": 1}),
    ("+ IST day instead of UTC day (finance definition)", {"tz_min": 330}),
]
ALONE = [("UTC day only", {}), ("IST day only", {"tz_min": 330}), ("excl test only", {"excl_test": 1}),
         ("intent only", {"intent_only": 1}), ("merge ids only", {"merge": 1})]

# pd:main
def pd_dau(events, users, idmap, day, tz_min, excl_test, intent_only, merge):
    e = events.merge(idmap, left_on="user_id", right_on="alias_id", how="left", suffixes=("", "_m"))
    e["uid"] = e["user_id_m"].fillna(e["user_id"]) if merge == 1 else e["user_id"]
    e["d"] = (pd.to_datetime(e["event_ts_utc"]) + pd.Timedelta(minutes=tz_min)).dt.strftime("%Y-%m-%d")
    e = e.merge(users[["user_id", "is_test"]].rename(columns={"user_id": "uid"}), on="uid", how="left")
    e["is_test"] = e["is_test"].fillna(0)
    e = e[e["d"] == day]
    if excl_test == 1:
        e = e[e["is_test"] == 0]
    if intent_only == 1:
        e = e[e["event_name"] != "heartbeat"]
    return len(e), e["uid"].nunique()
# pd:end

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
users = pd.read_sql_query("SELECT * FROM users", con)
idmap = pd.read_sql_query("SELECT * FROM identity_map", con)
events = pd.read_sql_query("SELECT * FROM events", con)

def run(change):
    p = {**BASE, **change}
    s = con.execute(SQL_MAIN, p).fetchone()
    q = pd_dau(events, users, idmap, **p)
    assert s == q, (change, s, q)
    return s

cum, acc, rows = [], {}, []
for name, change in CUM:
    acc.update(change)
    ev_n, us_n = run(acc)
    rows.append({"step (cumulative)": name, "events": ev_n, "users": us_n})
print(pd.DataFrame(rows).to_string(index=False))
base_users = run({})[1]
rows = []
for name, change in ALONE:
    ev_n, us_n = run(change)
    rows.append({"one change from the growth definition": name, "events": ev_n, "users": us_n, "delta_users": us_n - base_users})
print(pd.DataFrame(rows).to_string(index=False))
print("sum of the four single-cause deltas:", sum(r["delta_users"] for r in rows[1:]),
      "| actual cumulative gap:", run({})[1] - run({"excl_test": 1, "intent_only": 1, "merge": 1, "tz_min": 330})[1])
print("who is active on the IST day:", sorted(r[0] for r in con.execute(
    "SELECT DISTINCT COALESCE(m.user_id, e.user_id) FROM events e LEFT JOIN identity_map m ON m.alias_id = e.user_id "
    "LEFT JOIN users u ON u.user_id = COALESCE(m.user_id, e.user_id) "
    "WHERE date(datetime(e.event_ts_utc,'+330 minutes')) = '2024-03-05' AND COALESCE(u.is_test,0)=0 AND e.event_name <> 'heartbeat'")))
print("asserts passed")
```

**Output (my run):**
```text
                                             step (cumulative)  events  users
growth dashboard: UTC day, every event, raw ids, test users in      12     10
                                          + exclude test users      10      8
                         + intent events only (drop heartbeat)       8      7
                              + merge alias ids (identity_map)       8      5
             + IST day instead of UTC day (finance definition)       7      4
one change from the growth definition  events  users  delta_users
                         UTC day only      12     10            0
                         IST day only      11      9           -1
                       excl test only      10      8           -2
                          intent only       9      8           -2
                       merge ids only      12      8           -2
sum of the four single-cause deltas: -7 | actual cumulative gap: 6
who is active on the IST day: [1, 3, 5, 6]
asserts passed
```

**Edge cases:**
- Order matters: each step's effect depends on the earlier ones, and the one-at-a-time deltas do not add up to the total gap (printed: the four single-cause effects add up to 7 users, the actual gap from 10 to 4 is 6) because the causes overlap. For example, a test user's heartbeat is both a test-user and a background-event difference.
- Day boundary: the IST day is the UTC timestamp plus 330 minutes; users near midnight move between days (users 4, 5 and 9 here). Which dashboard is "right" depends on the business day definition, not on correctness.
- Alias merging without a unique `identity_map` (two rows for one alias) would double rows in the join and inflate events; check `COUNT(*) = COUNT(DISTINCT alias_id)` on the map first.
- Test flag is looked up after merging the id, so an alias of a test user is dropped too; if the alias has no row in `users` it is treated as non-test (`COALESCE`).
- Late-arriving events and different cut-off times also change a day's DAU; a snapshot taken at 10:00 versus 18:00 can differ for the same day (Part 6 Q35). I did not model this here.

**Then explain:**
- The reconciliation is a waterfall: start from the larger definition, apply one change at a time, show the number after each. Whatever is left unexplained at the end is a data issue, not a definition one.
- Typical causes in rough order of size: events versus users, time zone day, test and internal users, background events counted as activity, duplicate or merged ids. The order in my table is a choice; in real data I would try the biggest suspect first.
- Questions for the growth owner: what is the day boundary and time zone, which events count as active, are internal and test accounts in, is the id the raw device or the resolved user? Same questions to finance, plus: is the 1,190 an IST day or a billing day, and does it count only paying or logged-in users?
- Write the agreed definition once (a metric definition table) so both dashboards read it; metric governance is Book 6.

**Follow-ups:**
- Both dashboards match after all filters but still differ by a few users? Compare user id lists with an anti-join (`EXCEPT`) and inspect examples.
- Multiple time zones per user? Use each event's local day or a fixed company day; do not mix.
- Why not just pick one? Because each answers a different question; I would document both with names.

**Common mistakes:**
- Changing several definitions at once, so the gap cannot be attributed.
- Calling DAU what is really an event count.
- Forgetting the time zone offset when comparing dashboards.
- Merging ids with a non-unique mapping table.
- Treating a definition difference as a data bug, or the reverse.

### Q20 ⭐⭐ 🟡 First-touch versus last-touch attribution: touches(user_id, touch_ts, channel) and orders(order_id, user_id, order_ts, amount, status). Attribute each completed order's amount to the first channel and the last channel that the same user touched before the order timestamp within a 30-day lookback, using ROW_NUMBER partitioned by order. Return revenue by channel under both models side by side, add an 'unattributed' row for orders without a touch, and check that both models sum to total completed revenue. Cover ties on touch_ts (add a tie-breaker) and touches after the order (excluded).
**Asked at:** attribution guides (Cometly multi-touch SQL post, oneuptime ClickHouse attribution post, Adobe and Amplitude docs; search snippets only, not opened; linear = equal credit per touch, first touch = full credit to the earliest touch in the lookback window); vendor guides, not candidate reports; marketing analytics and growth analyst rounds
**Say this first (1 line):** For each completed order, join the same user's touches that happened at or before the order and no earlier than 30 days before it, rank them per order with `ROW_NUMBER` (oldest first for first touch, newest first for last touch, channel name as a tie-breaker), keep rank 1, label orders with no touch `unattributed`, and check that each model's revenue adds up to total completed revenue.

Conventions: lookback is 30 days inclusive at both ends (`touch_ts >= order_ts - 30 days` and `touch_ts <= order_ts`), only `completed` orders carry revenue, a touch at exactly the order timestamp counts, touches after the order are excluded, ties on `touch_ts` are broken by channel name alphabetically (arbitrary but deterministic; a real touch table should have a `touch_id`).

**Schema and sample data:** seven orders, six completed. Order 1 and 2 (user 1) have touches seo, email, ads, and a later social touch after both orders. Order 3 (user 2): the ads touch is 49 days before, outside the lookback; email is inside. Order 4 (user 3) has no touches at all. Order 5 (user 4): social earlier, then two touches at the same second, ads and email (tie). Order 6 is cancelled (no revenue). Order 7 (user 6): an ads touch exactly 30 days before (2024-02-09 10:00, a leap year so 30 days before 03-10) and a push touch at exactly the order timestamp.
```sql
CREATE TABLE touches(user_id INTEGER, touch_ts TEXT, channel TEXT);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO touches VALUES
 (1,'2024-03-01 09:00:00','seo'),(1,'2024-03-10 09:00:00','email'),(1,'2024-03-19 09:00:00','ads'),
 (1,'2024-03-26 09:00:00','social'),
 (2,'2024-02-01 09:00:00','ads'),(2,'2024-03-05 09:00:00','email'),
 (4,'2024-03-10 09:00:00','social'),(4,'2024-03-14 10:00:00','ads'),(4,'2024-03-14 10:00:00','email'),
 (6,'2024-02-09 10:00:00','ads'),(6,'2024-03-10 10:00:00','push'),
 (5,'2024-03-01 09:00:00','seo');
INSERT INTO orders VALUES
 (1,1,'2024-03-20 12:00:00',100,'completed'),
 (2,1,'2024-03-25 09:00:00',50,'completed'),
 (3,2,'2024-03-22 10:00:00',200,'completed'),
 (4,3,'2024-03-18 10:00:00',80,'completed'),
 (5,4,'2024-03-15 08:00:00',60,'completed'),
 (6,5,'2024-03-16 08:00:00',70,'cancelled'),
 (7,6,'2024-03-10 10:00:00',40,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
WITH co AS (
  SELECT order_id, user_id, order_ts, amount FROM orders WHERE status = 'completed'
), cand AS (
  SELECT co.order_id, t.channel,
         ROW_NUMBER() OVER (PARTITION BY co.order_id ORDER BY t.touch_ts ASC,  t.channel ASC) AS rn_first,
         ROW_NUMBER() OVER (PARTITION BY co.order_id ORDER BY t.touch_ts DESC, t.channel ASC) AS rn_last
  FROM co
  JOIN touches t
    ON t.user_id = co.user_id
   AND t.touch_ts <= co.order_ts
   AND t.touch_ts >= datetime(co.order_ts, '-30 days')
), ord AS (
  SELECT co.order_id, co.amount,
         COALESCE(f.channel, 'unattributed') AS first_channel,
         COALESCE(l.channel, 'unattributed') AS last_channel
  FROM co
  LEFT JOIN cand f ON f.order_id = co.order_id AND f.rn_first = 1
  LEFT JOIN cand l ON l.order_id = co.order_id AND l.rn_last = 1
), chan AS (
  SELECT first_channel AS channel FROM ord
  UNION
  SELECT last_channel FROM ord
)
SELECT c.channel,
       COALESCE((SELECT SUM(amount) FROM ord WHERE first_channel = c.channel), 0) AS first_touch_rev,
       COALESCE((SELECT SUM(amount) FROM ord WHERE last_channel  = c.channel), 0) AS last_touch_rev
FROM chan c
ORDER BY c.channel = 'unattributed', c.channel
```

**pandas answer:** the join, the window filter and the sorts replace `ROW_NUMBER`; shown once here and identical to the Code block:
```py
co = orders[orders["status"] == "completed"].copy()
co["order_ts"] = pd.to_datetime(co["order_ts"])
t = touches.assign(touch_ts=pd.to_datetime(touches["touch_ts"]))
j = co.merge(t, on="user_id")
j = j[(j["touch_ts"] <= j["order_ts"]) & (j["touch_ts"] >= j["order_ts"] - pd.Timedelta(days=30))]
first = (j.sort_values(["order_id", "touch_ts", "channel"], ascending=[True, True, True])
          .drop_duplicates("order_id").set_index("order_id")["channel"])
last = (j.sort_values(["order_id", "touch_ts", "channel"], ascending=[True, False, True])
         .drop_duplicates("order_id").set_index("order_id")["channel"])
co["first_channel"] = co["order_id"].map(first).fillna("unattributed")
co["last_channel"] = co["order_id"].map(last).fillna("unattributed")
a = co.groupby("first_channel")["amount"].sum().rename("first_touch_rev")
b = co.groupby("last_channel")["amount"].sum().rename("last_touch_rev")
pd_df = pd.concat([a, b], axis=1).fillna(0).rename_axis("channel").reset_index()
pd_df = (pd_df.assign(_u=pd_df["channel"] == "unattributed")
              .sort_values(["_u", "channel"]).drop(columns="_u").reset_index(drop=True))
```

**Example:**
- Order 1 (100, user 1, 03-20): touches in window seo 03-01, email 03-10, ads 03-19 (social 03-26 is after the order). First touch seo, last touch ads. Order 2 (50, 03-25): same three touches (social is still after), so seo and ads again.
- Order 3 (200): the ads touch is 49 days earlier, outside the lookback; email is the only one, so first and last are both email.
- Order 4 (80): no touch, so `unattributed` in both models.
- Order 5 (60): social 03-10, then ads and email both at 03-14 10:00. First touch social. Last touch: the tie is broken by channel name, ads.
- Order 7 (40): ads exactly 30 days before (included) and push at exactly the order time (included): first ads, last push.
- First-touch revenue: seo 150, email 200, social 60, ads 40, unattributed 80 = 530. Last-touch revenue: ads 210 (orders 1, 2 and 5), email 200, push 40, unattributed 80 = 530. Total completed revenue is 530, and the cancelled order is ignored.

**Code:** run with `python3 -I`. The assert compares SQL with pandas, in the SQL's row order (channels alphabetically, `unattributed` last); it also asserts each model sums to the total completed revenue.
```python
# Q20: first-touch versus last-touch attribution with a 30-day lookback
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE touches(user_id INTEGER, touch_ts TEXT, channel TEXT);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO touches VALUES
 (1,'2024-03-01 09:00:00','seo'),(1,'2024-03-10 09:00:00','email'),(1,'2024-03-19 09:00:00','ads'),
 (1,'2024-03-26 09:00:00','social'),
 (2,'2024-02-01 09:00:00','ads'),(2,'2024-03-05 09:00:00','email'),
 (4,'2024-03-10 09:00:00','social'),(4,'2024-03-14 10:00:00','ads'),(4,'2024-03-14 10:00:00','email'),
 (6,'2024-02-09 10:00:00','ads'),(6,'2024-03-10 10:00:00','push'),
 (5,'2024-03-01 09:00:00','seo');
INSERT INTO orders VALUES
 (1,1,'2024-03-20 12:00:00',100,'completed'),
 (2,1,'2024-03-25 09:00:00',50,'completed'),
 (3,2,'2024-03-22 10:00:00',200,'completed'),
 (4,3,'2024-03-18 10:00:00',80,'completed'),
 (5,4,'2024-03-15 08:00:00',60,'completed'),
 (6,5,'2024-03-16 08:00:00',70,'cancelled'),
 (7,6,'2024-03-10 10:00:00',40,'completed');
"""

SQL_MAIN = """
WITH co AS (
  SELECT order_id, user_id, order_ts, amount FROM orders WHERE status = 'completed'
), cand AS (
  SELECT co.order_id, t.channel,
         ROW_NUMBER() OVER (PARTITION BY co.order_id ORDER BY t.touch_ts ASC,  t.channel ASC) AS rn_first,
         ROW_NUMBER() OVER (PARTITION BY co.order_id ORDER BY t.touch_ts DESC, t.channel ASC) AS rn_last
  FROM co
  JOIN touches t
    ON t.user_id = co.user_id
   AND t.touch_ts <= co.order_ts
   AND t.touch_ts >= datetime(co.order_ts, '-30 days')
), ord AS (
  SELECT co.order_id, co.amount,
         COALESCE(f.channel, 'unattributed') AS first_channel,
         COALESCE(l.channel, 'unattributed') AS last_channel
  FROM co
  LEFT JOIN cand f ON f.order_id = co.order_id AND f.rn_first = 1
  LEFT JOIN cand l ON l.order_id = co.order_id AND l.rn_last = 1
), chan AS (
  SELECT first_channel AS channel FROM ord
  UNION
  SELECT last_channel FROM ord
)
SELECT c.channel,
       COALESCE((SELECT SUM(amount) FROM ord WHERE first_channel = c.channel), 0) AS first_touch_rev,
       COALESCE((SELECT SUM(amount) FROM ord WHERE last_channel  = c.channel), 0) AS last_touch_rev
FROM chan c
ORDER BY c.channel = 'unattributed', c.channel
"""

SQL_TOTAL = "SELECT SUM(amount) FROM orders WHERE status = 'completed'"

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
total = con.execute(SQL_TOTAL).fetchone()[0]
print(sql_df.to_string(index=False))
print("completed revenue:", total, "| first-touch sum:", sql_df["first_touch_rev"].sum(), "| last-touch sum:", sql_df["last_touch_rev"].sum())
assert sql_df["first_touch_rev"].sum() == total and sql_df["last_touch_rev"].sum() == total

touches = pd.read_sql_query("SELECT * FROM touches", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
co = orders[orders["status"] == "completed"].copy()
co["order_ts"] = pd.to_datetime(co["order_ts"])
t = touches.assign(touch_ts=pd.to_datetime(touches["touch_ts"]))
j = co.merge(t, on="user_id")
j = j[(j["touch_ts"] <= j["order_ts"]) & (j["touch_ts"] >= j["order_ts"] - pd.Timedelta(days=30))]
first = (j.sort_values(["order_id", "touch_ts", "channel"], ascending=[True, True, True])
          .drop_duplicates("order_id").set_index("order_id")["channel"])
last = (j.sort_values(["order_id", "touch_ts", "channel"], ascending=[True, False, True])
         .drop_duplicates("order_id").set_index("order_id")["channel"])
co["first_channel"] = co["order_id"].map(first).fillna("unattributed")
co["last_channel"] = co["order_id"].map(last).fillna("unattributed")
a = co.groupby("first_channel")["amount"].sum().rename("first_touch_rev")
b = co.groupby("last_channel")["amount"].sum().rename("last_touch_rev")
pd_df = pd.concat([a, b], axis=1).fillna(0).rename_axis("channel").reset_index()
pd_df = (pd_df.assign(_u=pd_df["channel"] == "unattributed")
              .sort_values(["_u", "channel"]).drop(columns="_u").reset_index(drop=True))
# pd:end
print(pd_df.to_string(index=False))
# compare with unattributed last, then channel name ascending (same ORDER BY as the SQL)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert pd_df["first_touch_rev"].sum() == total and pd_df["last_touch_rev"].sum() == total

# per-order detail for the walk-through
print(pd.DataFrame({"order_id": co["order_id"], "amount": co["amount"],
                    "first": co["first_channel"], "last": co["last_channel"]}).to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
     channel  first_touch_rev  last_touch_rev
         ads             40.0           210.0
       email            200.0           200.0
        push              0.0            40.0
         seo            150.0             0.0
      social             60.0             0.0
unattributed             80.0            80.0
completed revenue: 530.0 | first-touch sum: 530.0 | last-touch sum: 530.0
     channel  first_touch_rev  last_touch_rev
         ads             40.0           210.0
       email            200.0           200.0
        push              0.0            40.0
         seo            150.0             0.0
      social             60.0             0.0
unattributed             80.0            80.0
 order_id  amount        first         last
        1   100.0          seo          ads
        2    50.0          seo          ads
        3   200.0        email        email
        4    80.0 unattributed unattributed
        5    60.0       social          ads
        7    40.0          ads         push
asserts passed
```

**Edge cases:**
- Ties on `touch_ts` (order 5): without the second sort key the picked channel is arbitrary and can change between runs or engines; the tie-breaker makes it deterministic. The tie-break itself is a business choice: alternatives are to split credit between tied channels or to pick by a touch priority.
- Touches after the order (user 1's social touch, `touch_ts <= order_ts`) are excluded; they cannot have caused the purchase.
- Touch exactly 30 days earlier, and exactly at order time: both are included by `>=` and `<=`; say which bounds you use.
- Orders without touches: the `LEFT JOIN` keeps them, `COALESCE` labels them, so totals reconcile.
- Several orders by one user reuse the same touches (orders 1 and 2): fine for last or first touch, but be aware the same touch gets credit for two orders.
- The join from orders to touches fans out to several rows per order before ranking; `ROW_NUMBER = 1` collapses them again, which is why revenue is summed after the ranking, not before.
- Cancelled orders are filtered at the start, so they cannot appear in either model.

**Then explain:**
- First touch gives all credit to the earliest touch in the lookback window, last touch to the most recent before the order. Both are single-credit models, so each order's amount appears exactly once, which is why both sums equal total revenue.
- A touch outside the lookback is treated as not existing; the window length changes results (49 days in order 3) and is a definition to confirm.
- Linear and time-decay multi-touch versions are Q45.
- Other engines (not executed here): the date arithmetic would be `order_ts - INTERVAL '30 days'` in Postgres, `DATE_SUB` in MySQL, `TIMESTAMP_SUB` in BigQuery; `ROW_NUMBER` is the same.

**Follow-ups:**
- How to do last non-direct touch? Filter `channel <> 'direct'` in `cand` before ranking and fall back to direct when nothing remains.
- Revenue per channel by month? Group `ord` by order month as well; the maturity of touches does not matter for last touch.
- Why can first and last touch differ so much? First touch rewards top-of-funnel channels, last touch rewards closing channels; here seo wins first touch and ads wins last touch.

**Common mistakes:**
- Summing revenue after joining orders to all their touches, so each order is counted once per touch.
- Including touches after the order.
- No tie-breaker, so results are non-deterministic.
- Dropping orders without touches and then not reconciling to total revenue.
- Forgetting to restrict to completed orders.
- Using `ROW_NUMBER` partitioned by user instead of by order.

### Q21 ⭐⭐ 🟡 Repeat purchase rate and time to first purchase: users(user_id, signup_date, is_test) and orders(order_id, user_id, order_ts, amount, status). Return (a) the share of purchasers (users with a completed order) who placed a second completed order within 60 days of their first, using a mature cohort rule at the as-of date 2024-06-30, and (b) the distribution of days from signup to first completed purchase in buckets (same day, 1-7, 8-30, over 30, never). Say why order-level counting (two orders on the same day) differs from day-level counting, and how users who never buy are shown in (b).
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** (a) Rank each purchaser's completed orders, take the first and second order times, keep only purchasers whose first order is at least 60 days old at the as-of date, and count those whose second order is within 60 days of the first; (b) bucket the days from signup to first completed purchase with a `CASE`, and keep users who never bought in their own `never` bucket by starting from `users` with a `LEFT JOIN`.

Conventions: as-of 2024-06-30 with the whole day complete, only `completed` orders, test users out, the 60 days are counted from the first order timestamp and are inclusive, the second order is the second row by `order_ts` (ties broken by `order_id`), "mature" means first order + 60 days is before 2024-07-01 00:00:00.

**Schema and sample data:** twelve users (user 12 is a test user) and nineteen orders.
- User 1 buys twice on the same day (two orders, one day). User 2 repeats after 46 days. User 3's second order is 69 days later (too late). User 4 has a single order. User 5's first order is cancelled and its only completed order is on day 7 after signup. User 6 repeats but is not mature. Users 7 and 8 never buy. User 9's second order is exactly 60 days after the first (boundary). User 10 has an order before signup (data issue). User 11 has two completed orders at the same second (ids 201 and 202).
```sql
CREATE TABLE users(user_id INTEGER, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-03-01',0),(2,'2024-03-01',0),(3,'2024-03-10',0),(4,'2024-03-15',0),(5,'2024-04-01',0),
 (6,'2024-05-01',0),(7,'2024-02-01',0),(8,'2024-06-20',0),(9,'2024-02-10',0),(10,'2024-06-01',0),
 (11,'2024-03-20',0),(12,'2024-03-01',1);
INSERT INTO orders VALUES
 (1,1,'2024-03-01 10:00:00',100,'completed'),(2,1,'2024-03-01 18:00:00',40,'completed'),
 (3,2,'2024-03-05 10:00:00',90,'completed'),(4,2,'2024-04-20 10:00:00',60,'completed'),
 (5,3,'2024-03-12 10:00:00',70,'completed'),(6,3,'2024-05-20 10:00:00',30,'completed'),
 (7,4,'2024-04-20 10:00:00',80,'completed'),
 (8,5,'2024-04-02 10:00:00',50,'cancelled'),(9,5,'2024-04-08 10:00:00',50,'completed'),(10,5,'2024-04-20 10:00:00',20,'cancelled'),
 (11,6,'2024-05-15 10:00:00',60,'completed'),(12,6,'2024-05-20 10:00:00',25,'completed'),
 (13,9,'2024-03-01 12:00:00',55,'completed'),(14,9,'2024-04-30 12:00:00',45,'completed'),
 (15,10,'2024-05-30 10:00:00',35,'completed'),
 (201,11,'2024-03-20 09:00:00',65,'completed'),(202,11,'2024-03-20 09:00:00',65,'completed'),
 (16,12,'2024-03-02 10:00:00',999,'completed'),(17,12,'2024-03-03 10:00:00',999,'completed');
```

**SQL answer:** (a) at order level, `SQL_REPEAT` in the Code block:
```sql
WITH co AS (
  SELECT o.user_id, o.order_ts,
         ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY o.order_ts, o.order_id) AS rn
  FROM orders o JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed' AND u.is_test = 0
), f AS (
  SELECT user_id,
         MIN(CASE WHEN rn = 1 THEN order_ts END) AS t1,
         MIN(CASE WHEN rn = 2 THEN order_ts END) AS t2
  FROM co GROUP BY user_id
), m AS (
  SELECT * FROM f WHERE datetime(t1, '+60 days') < :as_of_end
)
SELECT COUNT(*) AS mature_purchasers,
       SUM(CASE WHEN t2 IS NOT NULL AND t2 <= datetime(t1, '+60 days') THEN 1 ELSE 0 END) AS repeaters,
       ROUND(100.0 * SUM(CASE WHEN t2 IS NOT NULL AND t2 <= datetime(t1, '+60 days') THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS repeat_pct
FROM m
```
(a) at day level, `SQL_REPEAT_DAYS` (distinct purchase days; same maturity set):
```sql
WITH days AS (
  SELECT DISTINCT o.user_id, date(o.order_ts) AS d
  FROM orders o JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed' AND u.is_test = 0
), r AS (
  SELECT user_id, d, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) AS rn FROM days
), f AS (
  SELECT user_id, MIN(CASE WHEN rn = 1 THEN d END) AS d1, MIN(CASE WHEN rn = 2 THEN d END) AS d2
  FROM r GROUP BY user_id
), m AS (
  SELECT * FROM f WHERE date(d1, '+60 days') <= :as_of
)
SELECT COUNT(*) AS mature_purchasers,
       SUM(CASE WHEN d2 IS NOT NULL AND d2 <= date(d1, '+60 days') THEN 1 ELSE 0 END) AS repeaters,
       ROUND(100.0 * SUM(CASE WHEN d2 IS NOT NULL AND d2 <= date(d1, '+60 days') THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS repeat_pct
FROM m
```
(b) buckets, `SQL_BUCKETS`, built from a small `labels` table so empty buckets still show:
```sql
WITH fp AS (
  SELECT u.user_id, u.signup_date, MIN(o.order_ts) AS first_ts
  FROM users u
  LEFT JOIN orders o ON o.user_id = u.user_id AND o.status = 'completed'
  WHERE u.is_test = 0
  GROUP BY u.user_id, u.signup_date
), b AS (
  SELECT user_id,
         CASE WHEN first_ts IS NULL THEN 5
              WHEN date(first_ts) < signup_date THEN 6
              ELSE CASE
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) = 0 THEN 1
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) <= 7 THEN 2
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) <= 30 THEN 3
                ELSE 4 END
         END AS k
  FROM fp
), labels(k, bucket) AS (
  VALUES (1,'same day'),(2,'1-7 days'),(3,'8-30 days'),(4,'over 30 days'),(5,'never'),(6,'before signup (data issue)')
)
SELECT l.bucket,
       COUNT(b.user_id) AS users,
       ROUND(100.0 * COUNT(b.user_id) / (SELECT COUNT(*) FROM fp), 1) AS pct_of_signups
FROM labels l LEFT JOIN b ON b.k = l.k
GROUP BY l.k, l.bucket
ORDER BY l.k
```

**pandas answer:** one snippet for all three, identical to the Code block:
```py
co = orders.merge(users[users["is_test"] == 0], on="user_id")
co = co[co["status"] == "completed"].copy()
co["order_ts"] = pd.to_datetime(co["order_ts"])
co = co.sort_values(["user_id", "order_ts", "order_id"])
co["rn"] = co.groupby("user_id").cumcount() + 1
t1 = co[co["rn"] == 1].set_index("user_id")["order_ts"].rename("t1")
t2 = co[co["rn"] == 2].set_index("user_id")["order_ts"].rename("t2")
f = pd.concat([t1, t2], axis=1)
m = f[f["t1"] + pd.Timedelta(days=60) < pd.Timestamp(AS_OF_END)]
rep_ok = m["t2"].notna() & (m["t2"] <= m["t1"] + pd.Timedelta(days=60))
pd_rep = pd.DataFrame([{"mature_purchasers": len(m), "repeaters": int(rep_ok.sum()),
                        "repeat_pct": round(100.0 * rep_ok.sum() / len(m), 1)}])
# day-level: distinct purchase days
days = co.assign(d=co["order_ts"].dt.normalize())[["user_id", "d"]].drop_duplicates().sort_values(["user_id", "d"])
days["rn"] = days.groupby("user_id").cumcount() + 1
d1 = days[days["rn"] == 1].set_index("user_id")["d"].rename("d1")
d2 = days[days["rn"] == 2].set_index("user_id")["d"].rename("d2")
fd = pd.concat([d1, d2], axis=1)
md = fd[fd["d1"] + pd.Timedelta(days=60) <= pd.Timestamp(AS_OF)]
rep_day_ok = md["d2"].notna() & (md["d2"] <= md["d1"] + pd.Timedelta(days=60))
pd_rep_day = pd.DataFrame([{"mature_purchasers": len(md), "repeaters": int(rep_day_ok.sum()),
                            "repeat_pct": round(100.0 * rep_day_ok.sum() / len(md), 1)}])
# (b) buckets
u = users[users["is_test"] == 0].copy()
u["first_day"] = u["user_id"].map(t1.dt.normalize())
u["gap"] = (u["first_day"] - pd.to_datetime(u["signup_date"])).dt.days
k = np.select([u["first_day"].isna(), u["gap"] < 0, u["gap"] == 0, u["gap"] <= 7, u["gap"] <= 30],
              [5, 6, 1, 2, 3], default=4)
labels = {1: "same day", 2: "1-7 days", 3: "8-30 days", 4: "over 30 days", 5: "never", 6: "before signup (data issue)"}
cnt = pd.Series(k).value_counts().reindex(list(labels), fill_value=0)
pd_bk = pd.DataFrame({"bucket": list(labels.values()), "users": cnt.to_numpy(),
                      "pct_of_signups": (100.0 * cnt / len(u)).round(1).to_numpy()})
```

**Example:**
- Purchasers (non-test, at least one completed order): users 1, 2, 3, 4, 5, 6, 9, 10, 11. First order + 60 days must be before 2024-07-01: user 6 (05-15 + 60 = 07-14) and user 10 (05-30 + 60 = 07-29) are immature. Mature purchasers = 7 (users 1, 2, 3, 4, 5, 9, 11).
- Order level, second order within 60 days of the first: user 1 yes (same day), user 2 yes (46 days), user 3 no (69 days), user 4 no, user 5 no (cancelled orders do not count, only one completed order), user 9 yes (exactly 60 days, inclusive), user 11 yes (second order at the same second). 4 of 7 = 57.1 percent.
- Day level (second distinct purchase day): user 1 no (both orders on 03-01), user 2 yes, user 9 yes, user 11 no (both on 03-20). 2 of 7 = 28.6 percent. Order-level counting rewards same-day multiple orders, which is often a basket split or a double submit, not repeat behaviour.
- Buckets (11 non-test users): same day 2 (users 1, 11), 1-7 days 3 (users 2, 3, 5), 8-30 days 2 (users 6, 9), over 30 days 1 (user 4), never 2 (users 7, 8), before signup 1 (user 10). Percentages of all 11 signups: 18.2, 27.3, 18.2, 9.1, 18.2, 9.1.

**Code:** run with `python3 -I`. Asserts: the two one-row results (order level and day level) equal the pandas rows; the bucket table is compared in bucket order 1 to 6 (the SQL `ORDER BY` and the pandas label order).
```python
# Q21: repeat purchase rate within 60 days (mature cohort) and days from signup to first purchase
import sqlite3
import numpy as np
import pandas as pd

AS_OF = "2024-06-30"
AS_OF_END = "2024-07-01 00:00:00"

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-03-01',0),(2,'2024-03-01',0),(3,'2024-03-10',0),(4,'2024-03-15',0),(5,'2024-04-01',0),
 (6,'2024-05-01',0),(7,'2024-02-01',0),(8,'2024-06-20',0),(9,'2024-02-10',0),(10,'2024-06-01',0),
 (11,'2024-03-20',0),(12,'2024-03-01',1);
INSERT INTO orders VALUES
 (1,1,'2024-03-01 10:00:00',100,'completed'),(2,1,'2024-03-01 18:00:00',40,'completed'),
 (3,2,'2024-03-05 10:00:00',90,'completed'),(4,2,'2024-04-20 10:00:00',60,'completed'),
 (5,3,'2024-03-12 10:00:00',70,'completed'),(6,3,'2024-05-20 10:00:00',30,'completed'),
 (7,4,'2024-04-20 10:00:00',80,'completed'),
 (8,5,'2024-04-02 10:00:00',50,'cancelled'),(9,5,'2024-04-08 10:00:00',50,'completed'),(10,5,'2024-04-20 10:00:00',20,'cancelled'),
 (11,6,'2024-05-15 10:00:00',60,'completed'),(12,6,'2024-05-20 10:00:00',25,'completed'),
 (13,9,'2024-03-01 12:00:00',55,'completed'),(14,9,'2024-04-30 12:00:00',45,'completed'),
 (15,10,'2024-05-30 10:00:00',35,'completed'),
 (201,11,'2024-03-20 09:00:00',65,'completed'),(202,11,'2024-03-20 09:00:00',65,'completed'),
 (16,12,'2024-03-02 10:00:00',999,'completed'),(17,12,'2024-03-03 10:00:00',999,'completed');
"""

SQL_REPEAT = """
WITH co AS (
  SELECT o.user_id, o.order_ts,
         ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY o.order_ts, o.order_id) AS rn
  FROM orders o JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed' AND u.is_test = 0
), f AS (
  SELECT user_id,
         MIN(CASE WHEN rn = 1 THEN order_ts END) AS t1,
         MIN(CASE WHEN rn = 2 THEN order_ts END) AS t2
  FROM co GROUP BY user_id
), m AS (
  SELECT * FROM f WHERE datetime(t1, '+60 days') < :as_of_end
)
SELECT COUNT(*) AS mature_purchasers,
       SUM(CASE WHEN t2 IS NOT NULL AND t2 <= datetime(t1, '+60 days') THEN 1 ELSE 0 END) AS repeaters,
       ROUND(100.0 * SUM(CASE WHEN t2 IS NOT NULL AND t2 <= datetime(t1, '+60 days') THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS repeat_pct
FROM m
"""

SQL_REPEAT_DAYS = """
WITH days AS (
  SELECT DISTINCT o.user_id, date(o.order_ts) AS d
  FROM orders o JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed' AND u.is_test = 0
), r AS (
  SELECT user_id, d, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) AS rn FROM days
), f AS (
  SELECT user_id, MIN(CASE WHEN rn = 1 THEN d END) AS d1, MIN(CASE WHEN rn = 2 THEN d END) AS d2
  FROM r GROUP BY user_id
), m AS (
  SELECT * FROM f WHERE date(d1, '+60 days') <= :as_of
)
SELECT COUNT(*) AS mature_purchasers,
       SUM(CASE WHEN d2 IS NOT NULL AND d2 <= date(d1, '+60 days') THEN 1 ELSE 0 END) AS repeaters,
       ROUND(100.0 * SUM(CASE WHEN d2 IS NOT NULL AND d2 <= date(d1, '+60 days') THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS repeat_pct
FROM m
"""

SQL_BUCKETS = """
WITH fp AS (
  SELECT u.user_id, u.signup_date, MIN(o.order_ts) AS first_ts
  FROM users u
  LEFT JOIN orders o ON o.user_id = u.user_id AND o.status = 'completed'
  WHERE u.is_test = 0
  GROUP BY u.user_id, u.signup_date
), b AS (
  SELECT user_id,
         CASE WHEN first_ts IS NULL THEN 5
              WHEN date(first_ts) < signup_date THEN 6
              ELSE CASE
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) = 0 THEN 1
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) <= 7 THEN 2
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) <= 30 THEN 3
                ELSE 4 END
         END AS k
  FROM fp
), labels(k, bucket) AS (
  VALUES (1,'same day'),(2,'1-7 days'),(3,'8-30 days'),(4,'over 30 days'),(5,'never'),(6,'before signup (data issue)')
)
SELECT l.bucket,
       COUNT(b.user_id) AS users,
       ROUND(100.0 * COUNT(b.user_id) / (SELECT COUNT(*) FROM fp), 1) AS pct_of_signups
FROM labels l LEFT JOIN b ON b.k = l.k
GROUP BY l.k, l.bucket
ORDER BY l.k
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
rep = pd.read_sql_query(SQL_REPEAT, con, params={"as_of_end": AS_OF_END})
rep_day = pd.read_sql_query(SQL_REPEAT_DAYS, con, params={"as_of": AS_OF})
bk = pd.read_sql_query(SQL_BUCKETS, con)
print("(a) order level:"); print(rep.to_string(index=False))
print("(a) day level:"); print(rep_day.to_string(index=False))
print("(b) buckets:"); print(bk.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
co = orders.merge(users[users["is_test"] == 0], on="user_id")
co = co[co["status"] == "completed"].copy()
co["order_ts"] = pd.to_datetime(co["order_ts"])
co = co.sort_values(["user_id", "order_ts", "order_id"])
co["rn"] = co.groupby("user_id").cumcount() + 1
t1 = co[co["rn"] == 1].set_index("user_id")["order_ts"].rename("t1")
t2 = co[co["rn"] == 2].set_index("user_id")["order_ts"].rename("t2")
f = pd.concat([t1, t2], axis=1)
m = f[f["t1"] + pd.Timedelta(days=60) < pd.Timestamp(AS_OF_END)]
rep_ok = m["t2"].notna() & (m["t2"] <= m["t1"] + pd.Timedelta(days=60))
pd_rep = pd.DataFrame([{"mature_purchasers": len(m), "repeaters": int(rep_ok.sum()),
                        "repeat_pct": round(100.0 * rep_ok.sum() / len(m), 1)}])
# day-level: distinct purchase days
days = co.assign(d=co["order_ts"].dt.normalize())[["user_id", "d"]].drop_duplicates().sort_values(["user_id", "d"])
days["rn"] = days.groupby("user_id").cumcount() + 1
d1 = days[days["rn"] == 1].set_index("user_id")["d"].rename("d1")
d2 = days[days["rn"] == 2].set_index("user_id")["d"].rename("d2")
fd = pd.concat([d1, d2], axis=1)
md = fd[fd["d1"] + pd.Timedelta(days=60) <= pd.Timestamp(AS_OF)]
rep_day_ok = md["d2"].notna() & (md["d2"] <= md["d1"] + pd.Timedelta(days=60))
pd_rep_day = pd.DataFrame([{"mature_purchasers": len(md), "repeaters": int(rep_day_ok.sum()),
                            "repeat_pct": round(100.0 * rep_day_ok.sum() / len(md), 1)}])
# (b) buckets
u = users[users["is_test"] == 0].copy()
u["first_day"] = u["user_id"].map(t1.dt.normalize())
u["gap"] = (u["first_day"] - pd.to_datetime(u["signup_date"])).dt.days
k = np.select([u["first_day"].isna(), u["gap"] < 0, u["gap"] == 0, u["gap"] <= 7, u["gap"] <= 30],
              [5, 6, 1, 2, 3], default=4)
labels = {1: "same day", 2: "1-7 days", 3: "8-30 days", 4: "over 30 days", 5: "never", 6: "before signup (data issue)"}
cnt = pd.Series(k).value_counts().reindex(list(labels), fill_value=0)
pd_bk = pd.DataFrame({"bucket": list(labels.values()), "users": cnt.to_numpy(),
                      "pct_of_signups": (100.0 * cnt / len(u)).round(1).to_numpy()})
# pd:end
print(pd_rep.to_string(index=False)); print(pd_rep_day.to_string(index=False)); print(pd_bk.to_string(index=False))
pd.testing.assert_frame_equal(rep, pd_rep, check_dtype=False)          # one row
pd.testing.assert_frame_equal(rep_day, pd_rep_day, check_dtype=False)  # one row
pd.testing.assert_frame_equal(bk, pd_bk, check_dtype=False)            # compared in bucket order 1..6
print("asserts passed")
```

**Output (my run):**
```text
(a) order level:
 mature_purchasers  repeaters  repeat_pct
                 7          4        57.1
(a) day level:
 mature_purchasers  repeaters  repeat_pct
                 7          2        28.6
(b) buckets:
                    bucket  users  pct_of_signups
                  same day      2            18.2
                  1-7 days      3            27.3
                 8-30 days      2            18.2
              over 30 days      1             9.1
                     never      2            18.2
before signup (data issue)      1             9.1
 mature_purchasers  repeaters  repeat_pct
                 7          4        57.1
 mature_purchasers  repeaters  repeat_pct
                 7          2        28.6
                    bucket  users  pct_of_signups
                  same day      2            18.2
                  1-7 days      3            27.3
                 8-30 days      2            18.2
              over 30 days      1             9.1
                     never      2            18.2
before signup (data issue)      1             9.1
asserts passed
```

**Edge cases:**
- Order versus day counting: 57.1 versus 28.6 percent on the same data. Pick one and name it ("second order" or "second purchase day"); I would show the day version when same-day orders are common.
- Ties on the first order's timestamp (user 11): `ROW_NUMBER` needs the `order_id` tie-breaker, otherwise which row is first or second is arbitrary; here the tie makes the second order count as a repeat at order level, a likely duplicate submission.
- Boundary: exactly 60 days later counts (user 9); a strict `<` rule would drop that user, so say which one you use.
- Immature purchasers (users 6 and 10) are excluded, not counted as non-repeaters. User 6 already has a second order, but keeping only the mature users keeps the rule independent of the outcome.
- Cancelled first order (user 5): the first completed order is the first order for this metric; counting the cancelled one would change days to first purchase from 7 to 1.
- Order before signup (user 10): shown in a separate bucket, never in `same day`; it usually means a signup date set later than the first order (guest checkout, imported accounts).
- Never-buyers in (b): shown as `never` out of all signups. A recent signup who has not bought yet is not a real never; strictly, "never" is only meaningful for users old enough, so I would also report users who signed up within 30 days of the as-of date separately (user 8 here signed up on 06-20, ten days before the as-of date, so it is not a real never), but I do not split that out in the query above.
- Integer rounding: percentages use `100.0 *`; none of these percentages is a .x5 tie, so SQL and pandas rounding agree here.
- The days-between value uses `julianday` on whole dates, wrapped in `ROUND` to make it an exact integer; for timestamps I would use `unixepoch` (Part 7 Q11).

**Then explain:**
- The denominator is purchasers (people who could repeat), not all signups; a rate over all signups answers a different question.
- Maturity: a purchaser whose 60 days are not complete would look like a non-repeater; leave them out of both numerator and denominator.
- For several repeat intervals (second order, third order), the same `ROW_NUMBER` ranking works; the time between first and second purchase and a repeat rate by order ranking is also in Part 6 Q20, so I do not repeat that here.
- Other engines (not executed here): Postgres `t1 + INTERVAL '60 days'`, MySQL `DATE_ADD`, BigQuery `TIMESTAMP_ADD`; day difference via `DATE_DIFF` or `DATEDIFF`. Not executed.

**Follow-ups:**
- Repeat within 30 and 90 days, side by side? Repeat the final `SUM(CASE ...)` with different intervals on the same `f` table, with each interval's own maturity rule.
- Repeat rate by signup month? Group the mature purchasers by the month of first order or signup, and say which.
- What about refunds? A refunded first order may be excluded; that needs the refunds table (Q22).

**Common mistakes:**
- Dividing by all users instead of purchasers.
- Counting any user with two orders without the 60-day window.
- Including immature purchasers.
- Not tie-breaking `ROW_NUMBER`.
- Dropping never-buyers from the distribution (they vanish with an inner join).
- Counting cancelled orders as purchases.

### Q22 ⭐⭐ 🟡 LTV to date by signup cohort, simple version: users(user_id, signup_date, country, is_test) and orders(order_id, user_id, order_ts, amount, status) plus refunds(refund_id, order_id, refund_ts, amount). For each signup month return cohort size, revenue to date at the as-of date 2024-06-30 net of refunds, and LTV-to-date per signed-up user (not per buyer). Say why older cohorts are not comparable with younger ones without a fixed age (point to Part 6 for cohort-age tables), and how you avoid fan-out when joining refunds.
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** Group refunds to one row per order first, left join that to completed orders up to the as-of date, collapse to one row per user, then left join to the non-test signups of each month so every cohort member counts in the denominator, and divide net revenue by cohort size (signed-up users, not buyers).

Conventions: as-of 2024-06-30 with the whole day included (`< 2024-07-01`), LTV to date is gross completed revenue minus refunds dated on or before the as-of date, refunds are attached to the order they belong to (cash view by refund date, only through the as-of date), test users out, signup month from `signup_date`.

**Schema and sample data:** six real users in four cohorts, one test user, one user (8) in April with no orders. User 1's first order has two partial refunds (100 and 150). User 3's order is fully refunded (600). An order on 2024-07-02 and a refund on 2024-07-03 are after the as-of date and must be ignored. A refund (id 5) points at a cancelled order and must not count.
```sql
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO users VALUES
 (1,'2024-01-10','IN',0),(2,'2024-01-20','IN',0),(3,'2024-02-05','US',0),(4,'2024-02-25','UK',0),
 (5,'2024-05-15','IN',0),(6,'2024-05-28','US',0),(7,'2024-01-15','IN',1),(8,'2024-04-01','IN',0);
INSERT INTO orders VALUES
 (1,1,'2024-01-12 10:00:00',1000,'completed'),(2,1,'2024-03-10 10:00:00',500,'completed'),
 (3,2,'2024-02-01 10:00:00',800,'completed'),(4,3,'2024-02-06 10:00:00',600,'completed'),
 (5,4,'2024-03-15 10:00:00',400,'cancelled'),(6,4,'2024-04-10 10:00:00',700,'completed'),
 (7,5,'2024-05-20 10:00:00',300,'completed'),(8,6,'2024-06-05 10:00:00',200,'completed'),
 (9,7,'2024-01-20 10:00:00',5000,'completed'),(10,2,'2024-07-02 10:00:00',100,'completed');
INSERT INTO refunds VALUES
 (1,1,'2024-01-20 10:00:00',100),(2,1,'2024-02-05 10:00:00',150),
 (3,4,'2024-03-01 10:00:00',600),(4,8,'2024-07-03 10:00:00',50),(5,5,'2024-03-20 10:00:00',40);
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
WITH rf AS (
  SELECT order_id, SUM(amount) AS refunded
  FROM refunds
  WHERE refund_ts < :as_of_end
  GROUP BY order_id
), ord AS (
  SELECT o.user_id,
         SUM(o.amount)                  AS gross,
         SUM(COALESCE(rf.refunded, 0))  AS refunded
  FROM orders o
  LEFT JOIN rf ON rf.order_id = o.order_id
  WHERE o.status = 'completed'
    AND o.order_ts < :as_of_end
  GROUP BY o.user_id
)
SELECT strftime('%Y-%m', u.signup_date)                              AS signup_month,
       COUNT(*)                                                      AS cohort_size,
       COALESCE(SUM(ord.gross), 0)                                   AS gross,
       COALESCE(SUM(ord.refunded), 0)                                AS refunded,
       COALESCE(SUM(ord.gross - ord.refunded), 0)                    AS net_revenue,
       ROUND(1.0 * COALESCE(SUM(ord.gross - ord.refunded), 0) / COUNT(*), 2) AS ltv_per_signup,
       (CAST(strftime('%Y', :as_of) AS INTEGER) * 12 + CAST(strftime('%m', :as_of) AS INTEGER))
       - (CAST(strftime('%Y', MIN(u.signup_date)) AS INTEGER) * 12
          + CAST(strftime('%m', MIN(u.signup_date)) AS INTEGER))     AS cohort_age_months
FROM users u
LEFT JOIN ord ON ord.user_id = u.user_id
WHERE u.is_test = 0
  AND u.signup_date < :as_of_end
GROUP BY strftime('%Y-%m', u.signup_date)
ORDER BY signup_month
```

**pandas answer:** same steps, shown once here and identical to the Code block:
```py
cut = pd.Timestamp(AS_OF_END)
rf = refunds[pd.to_datetime(refunds["refund_ts"]) < cut].groupby("order_id", as_index=False)["amount"].sum()
rf = rf.rename(columns={"amount": "refunded"})
o = orders[(orders["status"] == "completed") & (pd.to_datetime(orders["order_ts"]) < cut)]
o = o.merge(rf, on="order_id", how="left").fillna({"refunded": 0})
per_user = o.groupby("user_id", as_index=False).agg(gross=("amount", "sum"), refunded=("refunded", "sum"))
u = users[(users["is_test"] == 0) & (pd.to_datetime(users["signup_date"]) < cut)].copy()
u = u.merge(per_user, on="user_id", how="left").fillna({"gross": 0, "refunded": 0})
u["signup_month"] = pd.to_datetime(u["signup_date"]).dt.strftime("%Y-%m")
g = u.groupby("signup_month").agg(cohort_size=("user_id", "size"), gross=("gross", "sum"),
                                  refunded=("refunded", "sum"), first_signup=("signup_date", "min"))
g["net_revenue"] = g["gross"] - g["refunded"]
g["ltv_per_signup"] = (g["net_revenue"] / g["cohort_size"]).round(2)
asof = pd.Timestamp(AS_OF)
fs = pd.to_datetime(g["first_signup"])
g["cohort_age_months"] = (asof.year * 12 + asof.month) - (fs.dt.year * 12 + fs.dt.month)
pd_df = g.reset_index()[["signup_month", "cohort_size", "gross", "refunded", "net_revenue",
                         "ltv_per_signup", "cohort_age_months"]]
```

**Example:**
- January cohort (users 1 and 2; the test user 7 is ignored): user 1 completed 1000 + 500 = 1500, refunds 100 + 150 = 250, net 1250. User 2 has 800 (the 100 order on 07-02 is after the as-of date). Net revenue 2050 over cohort size 2 = LTV 1025.0.
- February cohort (users 3 and 4): user 3 net 600 - 600 = 0; user 4's 400 order is cancelled, and its 40 refund is ignored because it is attached to a cancelled order, but the 04-10 order of 700 counts. Net 700, LTV 700 / 2 = 350.0.
- April cohort (user 8 only, no orders): net 0, LTV 0.0. The `LEFT JOIN` from users is what keeps this row.
- May cohort (users 5 and 6): 300 + 200 = 500; the refund of 50 on 07-03 is after the as-of date, so it is not subtracted. LTV 250.0.
- Cohort ages at 2024-06-30 are 5, 4, 2 and 1 months. The January LTV of 1025 and the May LTV of 250 are not comparable: January had five months to accumulate revenue.

**Code:** run with `python3 -I`. The assert compares SQL with pandas after ordering by `signup_month`. The wrong fan-out query is printed for comparison.
```python
# Q22: LTV to date by signup cohort, net of refunds, without fan-out (as-of 2024-06-30)
import sqlite3
import pandas as pd

AS_OF = "2024-06-30"
AS_OF_END = "2024-07-01 00:00:00"

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO users VALUES
 (1,'2024-01-10','IN',0),(2,'2024-01-20','IN',0),(3,'2024-02-05','US',0),(4,'2024-02-25','UK',0),
 (5,'2024-05-15','IN',0),(6,'2024-05-28','US',0),(7,'2024-01-15','IN',1),(8,'2024-04-01','IN',0);
INSERT INTO orders VALUES
 (1,1,'2024-01-12 10:00:00',1000,'completed'),(2,1,'2024-03-10 10:00:00',500,'completed'),
 (3,2,'2024-02-01 10:00:00',800,'completed'),(4,3,'2024-02-06 10:00:00',600,'completed'),
 (5,4,'2024-03-15 10:00:00',400,'cancelled'),(6,4,'2024-04-10 10:00:00',700,'completed'),
 (7,5,'2024-05-20 10:00:00',300,'completed'),(8,6,'2024-06-05 10:00:00',200,'completed'),
 (9,7,'2024-01-20 10:00:00',5000,'completed'),(10,2,'2024-07-02 10:00:00',100,'completed');
INSERT INTO refunds VALUES
 (1,1,'2024-01-20 10:00:00',100),(2,1,'2024-02-05 10:00:00',150),
 (3,4,'2024-03-01 10:00:00',600),(4,8,'2024-07-03 10:00:00',50),(5,5,'2024-03-20 10:00:00',40);
"""

SQL_MAIN = """
WITH rf AS (
  SELECT order_id, SUM(amount) AS refunded
  FROM refunds
  WHERE refund_ts < :as_of_end
  GROUP BY order_id
), ord AS (
  SELECT o.user_id,
         SUM(o.amount)                  AS gross,
         SUM(COALESCE(rf.refunded, 0))  AS refunded
  FROM orders o
  LEFT JOIN rf ON rf.order_id = o.order_id
  WHERE o.status = 'completed'
    AND o.order_ts < :as_of_end
  GROUP BY o.user_id
)
SELECT strftime('%Y-%m', u.signup_date)                              AS signup_month,
       COUNT(*)                                                      AS cohort_size,
       COALESCE(SUM(ord.gross), 0)                                   AS gross,
       COALESCE(SUM(ord.refunded), 0)                                AS refunded,
       COALESCE(SUM(ord.gross - ord.refunded), 0)                    AS net_revenue,
       ROUND(1.0 * COALESCE(SUM(ord.gross - ord.refunded), 0) / COUNT(*), 2) AS ltv_per_signup,
       (CAST(strftime('%Y', :as_of) AS INTEGER) * 12 + CAST(strftime('%m', :as_of) AS INTEGER))
       - (CAST(strftime('%Y', MIN(u.signup_date)) AS INTEGER) * 12
          + CAST(strftime('%m', MIN(u.signup_date)) AS INTEGER))     AS cohort_age_months
FROM users u
LEFT JOIN ord ON ord.user_id = u.user_id
WHERE u.is_test = 0
  AND u.signup_date < :as_of_end
GROUP BY strftime('%Y-%m', u.signup_date)
ORDER BY signup_month
"""

# the fan-out mistake: join orders to refunds first, then sum the order amount
SQL_WRONG = """
SELECT strftime('%Y-%m', u.signup_date) AS signup_month,
       SUM(o.amount) AS wrong_gross, SUM(COALESCE(r.amount, 0)) AS refunded
FROM users u
JOIN orders o ON o.user_id = u.user_id AND o.status = 'completed' AND o.order_ts < :as_of_end
LEFT JOIN refunds r ON r.order_id = o.order_id AND r.refund_ts < :as_of_end
WHERE u.is_test = 0
GROUP BY strftime('%Y-%m', u.signup_date)
ORDER BY signup_month
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"as_of_end": AS_OF_END, "as_of": AS_OF}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))
print("wrong (orders joined to refunds first):")
print(pd.read_sql_query(SQL_WRONG, con, params={"as_of_end": AS_OF_END}).to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
cut = pd.Timestamp(AS_OF_END)
rf = refunds[pd.to_datetime(refunds["refund_ts"]) < cut].groupby("order_id", as_index=False)["amount"].sum()
rf = rf.rename(columns={"amount": "refunded"})
o = orders[(orders["status"] == "completed") & (pd.to_datetime(orders["order_ts"]) < cut)]
o = o.merge(rf, on="order_id", how="left").fillna({"refunded": 0})
per_user = o.groupby("user_id", as_index=False).agg(gross=("amount", "sum"), refunded=("refunded", "sum"))
u = users[(users["is_test"] == 0) & (pd.to_datetime(users["signup_date"]) < cut)].copy()
u = u.merge(per_user, on="user_id", how="left").fillna({"gross": 0, "refunded": 0})
u["signup_month"] = pd.to_datetime(u["signup_date"]).dt.strftime("%Y-%m")
g = u.groupby("signup_month").agg(cohort_size=("user_id", "size"), gross=("gross", "sum"),
                                  refunded=("refunded", "sum"), first_signup=("signup_date", "min"))
g["net_revenue"] = g["gross"] - g["refunded"]
g["ltv_per_signup"] = (g["net_revenue"] / g["cohort_size"]).round(2)
asof = pd.Timestamp(AS_OF)
fs = pd.to_datetime(g["first_signup"])
g["cohort_age_months"] = (asof.year * 12 + asof.month) - (fs.dt.year * 12 + fs.dt.month)
pd_df = g.reset_index()[["signup_month", "cohort_size", "gross", "refunded", "net_revenue",
                         "ltv_per_signup", "cohort_age_months"]]
# pd:end
print(pd_df.to_string(index=False))
# compare after ordering by signup_month
pd.testing.assert_frame_equal(sql_df.sort_values("signup_month").reset_index(drop=True),
                              pd_df.sort_values("signup_month").reset_index(drop=True), check_dtype=False)
print("asserts passed")
```

**Output (my run):**
```text
signup_month  cohort_size  gross  refunded  net_revenue  ltv_per_signup  cohort_age_months
     2024-01            2 2300.0     250.0       2050.0          1025.0                  5
     2024-02            2 1300.0     600.0        700.0           350.0                  4
     2024-04            1    0.0       0.0          0.0             0.0                  2
     2024-05            2  500.0       0.0        500.0           250.0                  1
wrong (orders joined to refunds first):
signup_month  wrong_gross  refunded
     2024-01       3300.0     250.0
     2024-02       1300.0     600.0
     2024-05        500.0       0.0
signup_month  cohort_size  gross  refunded  net_revenue  ltv_per_signup  cohort_age_months
     2024-01            2 2300.0     250.0       2050.0          1025.0                  5
     2024-02            2 1300.0     600.0        700.0           350.0                  4
     2024-04            1    0.0       0.0          0.0             0.0                  2
     2024-05            2  500.0       0.0        500.0           250.0                  1
asserts passed
```

**Edge cases:**
- Fan-out: joining orders to refunds before summing repeats an order once per refund. User 1's 1000 order has two refunds, so the wrong query counts it twice (printed: the January wrong gross is 3300 against the correct 2300, exactly the extra 1000; the wrong query also loses the April cohort because it inner joins orders). Pre-aggregating refunds to one row per order removes the repeat; a scalar subquery per order does the same.
- Cohort with no orders (April): shows `0` through `COALESCE`, not a missing row, and LTV is 0.0, not NULL.
- Refund after the as-of date (order 8 refunded on 07-03): excluded by the `refund_ts` filter, so the to-date figure is reproducible. Using the order month instead of the refund date would be the order-month view (same discussion as Q10).
- Refund larger than the order or a refund for a non-completed order (refund 5): the second is dropped by the `LEFT JOIN` onto completed orders only; for the first I would flag the data and cap or investigate, not silently net it.
- Test users are filtered from the cohort so they do not enter the denominator.
- Customers whose first order is in a later month than signup are in their signup cohort here; a first-order cohort is Part 6 Q9.
- Per signed-up user versus per buyer: dividing by buyers raises every number and hides conversion; here "per signed-up user" is what the question asks.

**Then explain:**
- LTV to date is realised net revenue so far, not a forecast; "to date" must be fixed to an as-of date.
- Older cohorts have had more time to buy, so a table of LTV by signup month mixes cohort quality with cohort age. A fair comparison uses revenue at a fixed age (for example, first 30 or 90 days), which is the cohort-age table in Part 6 Q42.
- Grain discipline: refunds to one row per order, orders to one row per user, users to one row per cohort; each join then preserves the grain.
- Net of refunds here is gross completed amount minus partial refunds; cost, discounts and margin are outside this table, so say "revenue LTV", not profit.
- Other engines (not executed here): the same CTE structure works in Postgres, MySQL 8, BigQuery and Snowflake; only the month bucket (`DATE_TRUNC`, `DATE_FORMAT`) and date arithmetic change.

**Follow-ups:**
- LTV at 90 days for every cohort? Add `o.order_ts < datetime(u.signup_date, '+90 days')` and keep only cohorts that are at least 90 days old (maturity rule as in Q12).
- Include the cohort's buyers and payer rate? Add `COUNT(CASE WHEN ord.gross > 0 THEN 1 END)` and show revenue per buyer beside LTV per signup.
- Currency or multi-country? Convert at a stated rate per order before summing.

**Common mistakes:**
- Joining refunds to orders and summing the order amount.
- Dividing by buyers instead of cohort size.
- Comparing cohorts of different ages as if they were comparable.
- Letting orders or refunds after the as-of date into the total.
- Inner joining orders, so cohorts with no orders disappear.
- Counting refunds on cancelled orders.

### Q23 ⭐⭐ 🟡 LeetCode 262 Trips and Users style cancellation by side: trips(trip_id, client_id, driver_id, city, status, request_date) with status in ('completed', 'cancelled_by_driver', 'cancelled_by_client') and users(user_id, banned, role). Return per request_date the cancellation rate (any cancellation over all requests, rounded to 2 decimals) counting only trips where both client and driver are unbanned, and show the rate split by who cancelled. Join users twice (once for the client, once for the driver), explain why filtering only the client is wrong, and handle days with zero qualifying trips (the row should not appear).
**Asked at:** LeetCode 262 Trips and Users (search snippets of doocs, tencent and velog mirrors; not opened; statement: daily cancellation rate, both client and driver unbanned) plus the marketplace framing (fill rate, cancellation by side) as an expert extension; public problem bank, not a candidate report; ride-hailing, food-delivery and marketplace analyst rounds
**Say this first (1 line):** Join `users` twice, once as client and once as driver, keep only trips where both are unbanned, then per `request_date` divide cancelled trips (any status other than completed) by all qualifying trips, using `* 1.0` so SQLite does not do integer division; a day with no qualifying trip has no group, so it simply does not appear.

**Schema and sample data:** twelve trips, seven users, `banned` stored as 'Yes' or 'No' (the LeetCode 262 convention; I state that as an assumption). Trip 3 has a banned client, trip 4 a banned driver, trip 9 is the only trip on 2024-03-03 and it involves two banned users, trip 12 has a client id (99) that is not in `users`. The `city` column is carried but not used.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, banned TEXT, role TEXT);
CREATE TABLE trips(trip_id INTEGER PRIMARY KEY, client_id INTEGER, driver_id INTEGER, city TEXT,
                   status TEXT, request_date TEXT);
INSERT INTO users VALUES
 (1,'No','client'),(2,'No','client'),(3,'Yes','client'),(7,'No','client'),
 (4,'No','driver'),(5,'No','driver'),(6,'Yes','driver');
INSERT INTO trips VALUES
 (1, 1,4,'Pune','completed',          '2024-03-01'),
 (2, 2,5,'Pune','cancelled_by_driver','2024-03-01'),
 (3, 3,4,'Pune','cancelled_by_client','2024-03-01'),
 (4, 1,6,'Pune','cancelled_by_client','2024-03-01'),
 (5, 2,4,'Pune','completed',          '2024-03-01'),
 (6, 1,4,'Pune','completed',          '2024-03-02'),
 (7, 7,5,'Pune','cancelled_by_client','2024-03-02'),
 (8, 2,4,'Pune','cancelled_by_client','2024-03-02'),
 (9, 3,6,'Pune','cancelled_by_driver','2024-03-03'),
 (10,1,4,'Pune','completed',          '2024-03-04'),
 (11,2,5,'Pune','completed',          '2024-03-04'),
 (12,99,4,'Pune','cancelled_by_client','2024-03-04');
```

**SQL answer:** `SQL_MAIN` in the Code block (two joins to `users`, the ban test inside each join so it is applied to the right side):
```sql
SELECT t.request_date,
       COUNT(*) AS requests,
       SUM(t.status <> 'completed') AS cancelled,
       ROUND(SUM(t.status <> 'completed') * 1.0 / COUNT(*), 2) AS cancel_rate,
       ROUND(SUM(t.status = 'cancelled_by_driver') * 1.0 / COUNT(*), 2) AS by_driver_rate,
       ROUND(SUM(t.status = 'cancelled_by_client') * 1.0 / COUNT(*), 2) AS by_client_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No'
JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No'
GROUP BY t.request_date
ORDER BY t.request_date
```
The wrong version (`SQL_WRONG` in the Code block) joins `users` once, for the client only. It is printed in the output so you can see the number move.

**pandas answer:** the same logic, shown once here and identical to the Code block. Two merges against the unbanned users, one renamed to `client_id` and one to `driver_id`:
```py
def daily_cancellation(trips, users):
    ok = users.loc[users["banned"] == "No", ["user_id"]]
    t = (trips.merge(ok.rename(columns={"user_id": "client_id"}), on="client_id")
              .merge(ok.rename(columns={"user_id": "driver_id"}), on="driver_id"))
    t = t.assign(cancelled=t["status"] != "completed",
                 by_driver=t["status"] == "cancelled_by_driver",
                 by_client=t["status"] == "cancelled_by_client")
    g = t.groupby("request_date")
    out = g.agg(requests=("trip_id", "size"), cancelled=("cancelled", "sum"),
                by_driver=("by_driver", "sum"), by_client=("by_client", "sum")).reset_index()
    out["cancel_rate"] = (out["cancelled"] / out["requests"]).round(2)
    out["by_driver_rate"] = (out["by_driver"] / out["requests"]).round(2)
    out["by_client_rate"] = (out["by_client"] / out["requests"]).round(2)
    return out[["request_date", "requests", "cancelled", "cancel_rate",
                "by_driver_rate", "by_client_rate"]]
```

**Example:** walk through the sample data by hand.
- Day 2024-03-01 has five trips. Trip 3 (banned client 3) and trip 4 (banned driver 6) drop out, leaving trips 1, 2 and 5: one completed, one cancelled by the driver, one completed. 3 requests, 1 cancellation, rate 1/3 = 0.33, all of it driver-side (0.33 by driver, 0.00 by client).
- Day 2024-03-02 has three qualifying trips (6, 7, 8): two are cancelled by the client, so 2/3 = 0.67 and the split is 0.00 driver, 0.67 client.
- Day 2024-03-03 has one trip and both of its users are banned, so zero qualifying trips and no output row. Trip 12 on 2024-03-04 has a client id that is not in `users`; an inner join drops it, so that day has 2 qualifying trips and rate 0.00.
- Wrong version (client filter only): on 2024-03-01 the banned-driver trip 4 stays in, giving 4 requests and 2 cancellations, 0.50 instead of 0.33. Days where only a driver is banned are the ones that move.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q23: Trips and Users style daily cancellation rate, both sides unbanned, split by who cancelled
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, banned TEXT, role TEXT);
CREATE TABLE trips(trip_id INTEGER PRIMARY KEY, client_id INTEGER, driver_id INTEGER, city TEXT,
                   status TEXT, request_date TEXT);
INSERT INTO users VALUES
 (1,'No','client'),(2,'No','client'),(3,'Yes','client'),(7,'No','client'),
 (4,'No','driver'),(5,'No','driver'),(6,'Yes','driver');
INSERT INTO trips VALUES
 (1, 1,4,'Pune','completed',          '2024-03-01'),
 (2, 2,5,'Pune','cancelled_by_driver','2024-03-01'),
 (3, 3,4,'Pune','cancelled_by_client','2024-03-01'),
 (4, 1,6,'Pune','cancelled_by_client','2024-03-01'),
 (5, 2,4,'Pune','completed',          '2024-03-01'),
 (6, 1,4,'Pune','completed',          '2024-03-02'),
 (7, 7,5,'Pune','cancelled_by_client','2024-03-02'),
 (8, 2,4,'Pune','cancelled_by_client','2024-03-02'),
 (9, 3,6,'Pune','cancelled_by_driver','2024-03-03'),
 (10,1,4,'Pune','completed',          '2024-03-04'),
 (11,2,5,'Pune','completed',          '2024-03-04'),
 (12,99,4,'Pune','cancelled_by_client','2024-03-04');
"""

SQL_MAIN = """
SELECT t.request_date,
       COUNT(*) AS requests,
       SUM(t.status <> 'completed') AS cancelled,
       ROUND(SUM(t.status <> 'completed') * 1.0 / COUNT(*), 2) AS cancel_rate,
       ROUND(SUM(t.status = 'cancelled_by_driver') * 1.0 / COUNT(*), 2) AS by_driver_rate,
       ROUND(SUM(t.status = 'cancelled_by_client') * 1.0 / COUNT(*), 2) AS by_client_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No'
JOIN users d ON d.user_id = t.driver_id AND d.banned = 'No'
GROUP BY t.request_date
ORDER BY t.request_date
"""
# wrong: only the client is checked
SQL_WRONG = """
SELECT t.request_date,
       COUNT(*) AS requests,
       ROUND(SUM(t.status <> 'completed') * 1.0 / COUNT(*), 2) AS cancel_rate
FROM trips t
JOIN users c ON c.user_id = t.client_id AND c.banned = 'No'
GROUP BY t.request_date
ORDER BY t.request_date
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_MAIN, con)
sql_wrong = pd.read_sql_query(SQL_WRONG, con)
print("SQL, both client and driver unbanned:")
print(sql_res.to_string(index=False))
print("SQL, wrong (client filtered only):")
print(sql_wrong.to_string(index=False))

trips = pd.read_sql_query("SELECT * FROM trips", con)
users = pd.read_sql_query("SELECT * FROM users", con)

# pd:main
def daily_cancellation(trips, users):
    ok = users.loc[users["banned"] == "No", ["user_id"]]
    t = (trips.merge(ok.rename(columns={"user_id": "client_id"}), on="client_id")
              .merge(ok.rename(columns={"user_id": "driver_id"}), on="driver_id"))
    t = t.assign(cancelled=t["status"] != "completed",
                 by_driver=t["status"] == "cancelled_by_driver",
                 by_client=t["status"] == "cancelled_by_client")
    g = t.groupby("request_date")
    out = g.agg(requests=("trip_id", "size"), cancelled=("cancelled", "sum"),
                by_driver=("by_driver", "sum"), by_client=("by_client", "sum")).reset_index()
    out["cancel_rate"] = (out["cancelled"] / out["requests"]).round(2)
    out["by_driver_rate"] = (out["by_driver"] / out["requests"]).round(2)
    out["by_client_rate"] = (out["by_client"] / out["requests"]).round(2)
    return out[["request_date", "requests", "cancelled", "cancel_rate",
                "by_driver_rate", "by_client_rate"]]
# pd:end

pd_res = daily_cancellation(trips, users)
# compare after sorting by request_date (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_res.sort_values("request_date").reset_index(drop=True),
                              sql_res, check_dtype=False)
print("pandas:")
print(pd_res.to_string(index=False))
print("days in trips:", trips["request_date"].nunique(), "; days in result:", len(pd_res))
print("asserts passed")
```

**Output (my run):**
```text
SQL, both client and driver unbanned:
request_date  requests  cancelled  cancel_rate  by_driver_rate  by_client_rate
  2024-03-01         3          1         0.33            0.33            0.00
  2024-03-02         3          2         0.67            0.00            0.67
  2024-03-04         2          0         0.00            0.00            0.00
SQL, wrong (client filtered only):
request_date  requests  cancel_rate
  2024-03-01         4         0.50
  2024-03-02         3         0.67
  2024-03-04         2         0.00
pandas:
request_date  requests  cancelled  cancel_rate  by_driver_rate  by_client_rate
  2024-03-01         3          1         0.33            0.33            0.00
  2024-03-02         3          2         0.67            0.00            0.67
  2024-03-04         2          0         0.00            0.00            0.00
days in trips: 4 ; days in result: 3
asserts passed
```

**Edge cases:**
- A day with zero qualifying trips has no group, so no row and no division by zero. If the report must show every day with 0 or NULL, start from a date list and LEFT JOIN, and say which you want.
- A user id missing from `users` (trip 12): with inner joins the trip is dropped; with a LEFT JOIN plus `banned = 'No'` in the WHERE it is also dropped; with `banned <> 'Yes'` it would be kept. Pick and state the rule.
- `banned` NULL: `banned = 'No'` is not true for NULL, so the user is treated as not provably unbanned and the trip is dropped; the opposite rule is `COALESCE(banned,'No') = 'No'`.
- Rounding: values here are 1/3 and 2/3, no exact half; for a value like 0.125 SQLite ROUND and pandas round disagree (see Q31).

**Then explain:**
- Both parties must be unbanned: banning is a property of a user, a trip has two users, and the question's rule needs both. Filtering only the client leaves trips with a banned driver in the numerator and denominator.
- The denominator is all qualifying requests (completed plus both cancel types), not only completed trips.
- `SUM(status <> 'completed')` works in SQLite because a comparison is 0 or 1; in Postgres you would write `COUNT(*) FILTER (WHERE ...)` or `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`, in BigQuery `COUNTIF(...)` (not executed here). The CASE form is portable.
- Put the ban condition in the join (`ON ... AND c.banned = 'No'`) for an inner join; it is equivalent to a WHERE there. With a LEFT JOIN it must stay in the WHERE or the row survives with NULLs.
- Round the final ratio only; do not round counts first.

**Follow-ups:**
- Also show the days with zero qualifying trips? Generate a date spine (recursive CTE, see Q33) and LEFT JOIN the daily result, returning NULL or 0 as agreed.
- Cancellation rate by city as well? Add `t.city` to the GROUP BY; the double join is unchanged.
- Split by who cancelled but over cancellations only? Use `NULLIF(SUM(status <> 'completed'), 0)` as the denominator; Q24 does this for a marketplace.

**Common mistakes:**
- Filtering only the client side (shown in the output).
- Joining `users` once and checking `client_id` and `driver_id` against the same alias.
- Integer division: `SUM(...) / COUNT(*)` gives 0 in SQLite when the ratio is below 1; multiply by 1.0 first.
- Putting the ban filter in WHERE after a LEFT JOIN and then wondering why unmatched trips vanish (or the reverse).
- Counting only 'cancelled_by_client' as cancellations.

### Q24 ⭐⭐ 🟡 Supply and demand marketplace metrics: ride_requests(request_id, rider_id, driver_id, city, request_ts, status, fare, commission) with status in ('completed', 'cancelled_by_rider', 'cancelled_by_driver', 'no_driver_found') and driver_id NULL when no driver was assigned. Return per city the fill rate (requests that ended completed over all requests), the cancellation share by side, completed rides per active driver (drivers with at least one assigned request), and the take rate (commission over fare on completed rides). Say why 'no_driver_found' belongs in the fill-rate denominator and not in the cancellation numerator, and which denominator rides per driver should use.
**Asked at:** LeetCode 262 Trips and Users (search snippets of doocs, tencent and velog mirrors; not opened; statement: daily cancellation rate, both client and driver unbanned) plus the marketplace framing (fill rate, cancellation by side) as an expert extension; public problem bank, not a candidate report; ride-hailing, food-delivery and marketplace analyst rounds
**Say this first (1 line):** Per city: fill rate is completed over all requests (including no_driver_found), cancellation share is rider-cancelled and driver-cancelled over cancellations, rides per active driver is completed rides over distinct drivers with an assigned request, and take rate is summed commission over summed fare on completed rides only; every ratio gets `NULLIF` so an empty denominator is NULL, not an error.

**Schema and sample data:** thirteen requests in three cities. Mumbai has all four statuses and one rider cancellation after a driver was assigned (driver 12). Pune has two completed rides by the same driver. Delhi has only `no_driver_found`, so cancellations, active drivers and fare are all zero there. `fare` and `commission` are NULL on rows that did not complete. All fares and commissions are made-up toy values.
```sql
CREATE TABLE ride_requests(request_id INTEGER PRIMARY KEY, rider_id INTEGER, driver_id INTEGER, city TEXT,
                           request_ts TEXT, status TEXT, fare REAL, commission REAL);
INSERT INTO ride_requests VALUES
 (1, 1, 10,  'Mumbai','2024-03-01 08:00:00','completed',          200, 40),
 (2, 2, 10,  'Mumbai','2024-03-01 09:00:00','completed',          100, 20),
 (3, 3, 11,  'Mumbai','2024-03-01 09:30:00','cancelled_by_driver',NULL,NULL),
 (4, 4, NULL,'Mumbai','2024-03-01 10:00:00','cancelled_by_rider', NULL,NULL),
 (5, 5, NULL,'Mumbai','2024-03-01 10:30:00','no_driver_found',    NULL,NULL),
 (6, 6, 11,  'Mumbai','2024-03-01 11:00:00','completed',          300, 48),
 (7, 7, 12,  'Mumbai','2024-03-01 12:00:00','cancelled_by_rider', NULL,NULL),
 (8, 8, NULL,'Pune',  '2024-03-01 08:00:00','no_driver_found',    NULL,NULL),
 (9, 9, NULL,'Pune',  '2024-03-01 09:00:00','cancelled_by_rider', NULL,NULL),
 (10,10,20,  'Pune',  '2024-03-01 10:00:00','completed',          150, 30),
 (11,11,20,  'Pune',  '2024-03-01 11:00:00','completed',          250, 50),
 (12,12,NULL,'Delhi', '2024-03-01 08:00:00','no_driver_found',    NULL,NULL),
 (13,13,NULL,'Delhi', '2024-03-01 09:00:00','no_driver_found',    NULL,NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
SELECT city,
       COUNT(*) AS requests,
       SUM(status = 'completed') AS completed,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 2) AS fill_rate,
       SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')) AS cancelled,
       ROUND(SUM(status = 'cancelled_by_rider') * 1.0 /
             NULLIF(SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')), 0), 2) AS rider_share,
       ROUND(SUM(status = 'cancelled_by_driver') * 1.0 /
             NULLIF(SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')), 0), 2) AS driver_share,
       COUNT(DISTINCT driver_id) AS active_drivers,
       ROUND(SUM(status = 'completed') * 1.0 / NULLIF(COUNT(DISTINCT driver_id), 0), 2) AS rides_per_driver,
       ROUND(SUM(CASE WHEN status = 'completed' THEN commission END) * 1.0 /
             NULLIF(SUM(CASE WHEN status = 'completed' THEN fare END), 0), 2) AS take_rate
FROM ride_requests
GROUP BY city
ORDER BY city
```

**pandas answer:** the same logic as one function (`nz` turns a zero denominator into NaN, the counterpart of `NULLIF`):
```py
def city_metrics(rr):
    done = rr["status"] == "completed"
    canc = rr["status"].isin(["cancelled_by_rider", "cancelled_by_driver"])
    t = rr.assign(completed=done, cancelled=canc,
                  by_rider=rr["status"] == "cancelled_by_rider",
                  by_driver=rr["status"] == "cancelled_by_driver",
                  fare_done=rr["fare"].where(done), comm_done=rr["commission"].where(done))
    g = t.groupby("city")
    out = g.agg(requests=("request_id", "size"), completed=("completed", "sum"),
                cancelled=("cancelled", "sum"), by_rider=("by_rider", "sum"),
                by_driver=("by_driver", "sum"), active_drivers=("driver_id", "nunique"),
                fare=("fare_done", "sum"), comm=("comm_done", "sum")).reset_index()
    nz = lambda s: s.where(s != 0)          # zero denominator -> NaN (SQL NULLIF)
    out["fill_rate"] = (out["completed"] / out["requests"]).round(2)
    out["rider_share"] = (out["by_rider"] / nz(out["cancelled"])).round(2)
    out["driver_share"] = (out["by_driver"] / nz(out["cancelled"])).round(2)
    out["rides_per_driver"] = (out["completed"] / nz(out["active_drivers"])).round(2)
    out["take_rate"] = (out["comm"] / nz(out["fare"])).round(2)
    return out[["city", "requests", "completed", "fill_rate", "cancelled", "rider_share",
                "driver_share", "active_drivers", "rides_per_driver", "take_rate"]]
```

**Example:** walk through the sample data by hand.
- Mumbai: 7 requests, 3 completed (requests 1, 2, 6) so fill rate 3/7 = 0.43. Cancellations are requests 3 (driver), 4 (rider) and 7 (rider): 3 in all, rider share 2/3 = 0.67, driver share 1/3 = 0.33. The request with `no_driver_found` is in the fill-rate denominator but not among the cancellations.
- Active drivers in Mumbai are the distinct non-NULL driver ids: 10, 11, 12, so 3. Rides per active driver is 3 completed / 3 = 1.0. `COUNT(DISTINCT driver_id)` ignores the two NULL rows by itself.
- Take rate: commissions 40 + 20 + 48 = 108 over fares 200 + 100 + 300 = 600, 0.18.
- Pune: fill 2/4 = 0.50, one cancellation (rider), so shares 1.00 and 0.00, one active driver (20), 2.0 rides per driver, take rate 80/400 = 0.20.
- Delhi: fill 0.00, no cancellations, no drivers, no fare: the four ratios are NULL (NaN in pandas), not 0 and not an error.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q24: marketplace supply and demand metrics per city: fill rate, cancellation share, rides per driver, take rate
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE ride_requests(request_id INTEGER PRIMARY KEY, rider_id INTEGER, driver_id INTEGER, city TEXT,
                           request_ts TEXT, status TEXT, fare REAL, commission REAL);
INSERT INTO ride_requests VALUES
 (1, 1, 10,  'Mumbai','2024-03-01 08:00:00','completed',          200, 40),
 (2, 2, 10,  'Mumbai','2024-03-01 09:00:00','completed',          100, 20),
 (3, 3, 11,  'Mumbai','2024-03-01 09:30:00','cancelled_by_driver',NULL,NULL),
 (4, 4, NULL,'Mumbai','2024-03-01 10:00:00','cancelled_by_rider', NULL,NULL),
 (5, 5, NULL,'Mumbai','2024-03-01 10:30:00','no_driver_found',    NULL,NULL),
 (6, 6, 11,  'Mumbai','2024-03-01 11:00:00','completed',          300, 48),
 (7, 7, 12,  'Mumbai','2024-03-01 12:00:00','cancelled_by_rider', NULL,NULL),
 (8, 8, NULL,'Pune',  '2024-03-01 08:00:00','no_driver_found',    NULL,NULL),
 (9, 9, NULL,'Pune',  '2024-03-01 09:00:00','cancelled_by_rider', NULL,NULL),
 (10,10,20,  'Pune',  '2024-03-01 10:00:00','completed',          150, 30),
 (11,11,20,  'Pune',  '2024-03-01 11:00:00','completed',          250, 50),
 (12,12,NULL,'Delhi', '2024-03-01 08:00:00','no_driver_found',    NULL,NULL),
 (13,13,NULL,'Delhi', '2024-03-01 09:00:00','no_driver_found',    NULL,NULL);
"""

SQL_MAIN = """
SELECT city,
       COUNT(*) AS requests,
       SUM(status = 'completed') AS completed,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 2) AS fill_rate,
       SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')) AS cancelled,
       ROUND(SUM(status = 'cancelled_by_rider') * 1.0 /
             NULLIF(SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')), 0), 2) AS rider_share,
       ROUND(SUM(status = 'cancelled_by_driver') * 1.0 /
             NULLIF(SUM(status IN ('cancelled_by_rider', 'cancelled_by_driver')), 0), 2) AS driver_share,
       COUNT(DISTINCT driver_id) AS active_drivers,
       ROUND(SUM(status = 'completed') * 1.0 / NULLIF(COUNT(DISTINCT driver_id), 0), 2) AS rides_per_driver,
       ROUND(SUM(CASE WHEN status = 'completed' THEN commission END) * 1.0 /
             NULLIF(SUM(CASE WHEN status = 'completed' THEN fare END), 0), 2) AS take_rate
FROM ride_requests
GROUP BY city
ORDER BY city
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_MAIN, con)
print("SQL:")
print(sql_res.to_string(index=False))

rr = pd.read_sql_query("SELECT * FROM ride_requests", con)

# pd:main
def city_metrics(rr):
    done = rr["status"] == "completed"
    canc = rr["status"].isin(["cancelled_by_rider", "cancelled_by_driver"])
    t = rr.assign(completed=done, cancelled=canc,
                  by_rider=rr["status"] == "cancelled_by_rider",
                  by_driver=rr["status"] == "cancelled_by_driver",
                  fare_done=rr["fare"].where(done), comm_done=rr["commission"].where(done))
    g = t.groupby("city")
    out = g.agg(requests=("request_id", "size"), completed=("completed", "sum"),
                cancelled=("cancelled", "sum"), by_rider=("by_rider", "sum"),
                by_driver=("by_driver", "sum"), active_drivers=("driver_id", "nunique"),
                fare=("fare_done", "sum"), comm=("comm_done", "sum")).reset_index()
    nz = lambda s: s.where(s != 0)          # zero denominator -> NaN (SQL NULLIF)
    out["fill_rate"] = (out["completed"] / out["requests"]).round(2)
    out["rider_share"] = (out["by_rider"] / nz(out["cancelled"])).round(2)
    out["driver_share"] = (out["by_driver"] / nz(out["cancelled"])).round(2)
    out["rides_per_driver"] = (out["completed"] / nz(out["active_drivers"])).round(2)
    out["take_rate"] = (out["comm"] / nz(out["fare"])).round(2)
    return out[["city", "requests", "completed", "fill_rate", "cancelled", "rider_share",
                "driver_share", "active_drivers", "rides_per_driver", "take_rate"]]
# pd:end

pd_res = city_metrics(rr)
# compare after sorting by city; NaN in pandas equals NULL in SQL for this comparison
pd.testing.assert_frame_equal(pd_res.sort_values("city").reset_index(drop=True), sql_res, check_dtype=False)
print("pandas:")
print(pd_res.to_string(index=False))

# Mumbai alternatives for the rides-per-driver denominator
m = rr[rr["city"] == "Mumbai"]
print("Mumbai drivers with an assigned request:", m["driver_id"].nunique(),
      "; drivers with a completed ride:", m.loc[m["status"] == "completed", "driver_id"].nunique(),
      "; rows with a NULL driver:", int(m["driver_id"].isna().sum()))
print("asserts passed")
```

**Output (my run):**
```text
SQL:
  city  requests  completed  fill_rate  cancelled  rider_share  driver_share  active_drivers  rides_per_driver  take_rate
 Delhi         2          0       0.00          0          NaN           NaN               0               NaN        NaN
Mumbai         7          3       0.43          3         0.67          0.33               3               1.0       0.18
  Pune         4          2       0.50          1         1.00          0.00               1               2.0       0.20
pandas:
  city  requests  completed  fill_rate  cancelled  rider_share  driver_share  active_drivers  rides_per_driver  take_rate
 Delhi         2          0       0.00          0          NaN           NaN               0               NaN        NaN
Mumbai         7          3       0.43          3         0.67          0.33               3               1.0       0.18
  Pune         4          2       0.50          1         1.00          0.00               1               2.0       0.20
Mumbai drivers with an assigned request: 3 ; drivers with a completed ride: 2 ; rows with a NULL driver: 2
asserts passed
```

**Edge cases:**
- Zero denominators give NULL here. In SQLite `x / 0` also returns NULL rather than raising (Q31 runs it), but PostgreSQL and others raise a division error (not executed here), so `NULLIF` is the portable habit.
- Driver NULL on a cancelled_by_rider row (rider left before assignment, request 4) versus a driver assigned (request 7): the first does not count toward active drivers, the second does. That is a business rule to confirm.
- A driver with one completed ride and one driver-cancelled request is one active driver; counting rows instead of distinct ids would double count.
- Drivers who were online but never got a request are not in this table at all, so they cannot be in the denominator; that needs a supply table.

**Then explain:**
- no_driver_found belongs in the fill-rate denominator because fill rate measures how much of the demand you served; a request nobody could serve is the clearest failure of supply. It is not a cancellation: nobody cancelled, the platform failed to match.
- Cancellation share by side is a share of cancellations here (rider plus driver = 1). If the interviewer means each side's cancellations over all requests, change the denominator to `COUNT(*)`; say which you used.
- Rides per active driver uses distinct drivers with at least one assigned request (3 in Mumbai). The alternatives are drivers with a completed ride (2 in Mumbai, which would give 1.5) or drivers logged in from a supply table. All are defensible; the choice changes the number, so name it.
- Take rate is a ratio of sums over completed rides, not an average of per-ride ratios; the average of ratios weights a 100 fare ride like a 1000 fare ride.
- Metric design (is fill rate the right goal?) belongs to Book 6; this answer stays on the SQL.

**Follow-ups:**
- Per day or per hour instead of per city? Add the truncated `request_ts` to the GROUP BY; with few rows per bucket the ratios get noisy.
- Why not average per-ride commission rates? Because that is a different, unweighted number (see above).
- How would you split cancellations before and after driver assignment? Use `driver_id IS NULL` on cancelled_by_rider rows as the proxy and say it is a proxy.

**Common mistakes:**
- Putting `no_driver_found` in the cancellation numerator.
- Dividing rides by all drivers in the company instead of drivers active in that city and period.
- Summing fares over all rows (including cancelled) for the take-rate denominator.
- Averaging per-ride take rates.
- Dividing by zero instead of `NULLIF` for a city with no completed rides.

### Q25 ⭐⭐ 🟡 Search metrics: searches(search_id, user_id, search_ts, query, result_count) and clicks(click_id, search_id, click_ts, position). Return per day the search count, the click-through rate (searches with at least one click over searches, not clicks over searches), the zero-result rate, and the distribution of clicked positions (1, 2, 3, 4 to 10, 11 and above) as a percentage of clicks. Show why joining searches to clicks first and counting rows inflates CTR (fan-out) and use EXISTS or a distinct count instead, and what you do with searches that have zero results and therefore cannot get a click.
**Asked at:** search-analytics guides (Elastic ES|QL click-tracking post, oneuptime ClickHouse search analytics, Algolia and SearchStax metric definitions; search snippets only, not opened: CTR = searches with at least one click over searches, zero-result rate, average click position, MRR); vendor guides, not candidate reports; search and marketplace analyst rounds
**Say this first (1 line):** Decide the grain first: CTR is searches that got at least one click over searches, so mark each search with `EXISTS` on `clicks` (one row per search, no fan-out) and average that flag per day; clicks per search is a different number and joining first inflates it.

**Schema and sample data:** eight searches over three days and six clicks. Search 1 gets two clicks (positions 1 and 3), search 2 has zero results so it cannot be clicked, search 7 has `result_count` NULL (a logging gap, not the same as zero), search 8 is the only search on 2024-03-03 and has no click at all.
```sql
CREATE TABLE searches(search_id INTEGER PRIMARY KEY, user_id INTEGER, search_ts TEXT, query TEXT, result_count INTEGER);
CREATE TABLE clicks(click_id INTEGER PRIMARY KEY, search_id INTEGER, click_ts TEXT, position INTEGER);
INSERT INTO searches VALUES
 (1,1,'2024-03-01 09:00:00','shoes',   5),
 (2,2,'2024-03-01 09:05:00','shooes',  0),
 (3,3,'2024-03-01 10:00:00','bag',    10),
 (4,4,'2024-03-01 11:00:00','watch',   4),
 (5,1,'2024-03-02 09:00:00','phone',  20),
 (6,2,'2024-03-02 09:30:00','case',    3),
 (7,3,'2024-03-02 10:00:00','charger',NULL),
 (8,4,'2024-03-03 08:00:00','lamp',    6);
INSERT INTO clicks VALUES
 (1,1,'2024-03-01 09:00:10',1),(2,1,'2024-03-01 09:00:40',3),
 (3,4,'2024-03-01 11:00:05',2),
 (4,5,'2024-03-02 09:00:07',1),(5,5,'2024-03-02 09:00:30',12),
 (6,6,'2024-03-02 09:30:09',5);
```

**SQL answer:** `SQL_MAIN` (daily metrics) and `SQL_POS` (click-position distribution) in the Code block. `SQL_MAIN`:
```sql
WITH s AS (
  SELECT search_id, date(search_ts) AS d, result_count,
         EXISTS (SELECT 1 FROM clicks c WHERE c.search_id = searches.search_id) AS clicked
  FROM searches
)
SELECT d AS day,
       COUNT(*) AS searches,
       SUM(clicked) AS searches_with_click,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(result_count = 0) AS zero_result,
       ROUND(SUM(result_count = 0) * 1.0 / COUNT(*), 2) AS zero_result_rate
FROM s
GROUP BY d
ORDER BY d
```
```sql
WITH b(bucket, ord) AS (VALUES ('1',1),('2',2),('3',3),('4-10',4),('11+',5)),
d AS (SELECT DISTINCT date(search_ts) AS day FROM searches),
k AS (
  SELECT date(s.search_ts) AS day,
         CASE WHEN c.position = 1 THEN '1' WHEN c.position = 2 THEN '2' WHEN c.position = 3 THEN '3'
              WHEN c.position BETWEEN 4 AND 10 THEN '4-10' ELSE '11+' END AS bucket
  FROM clicks c JOIN searches s ON s.search_id = c.search_id
)
SELECT d.day, b.bucket,
       (SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) AS clicks,
       ROUND((SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) * 100.0 /
             NULLIF((SELECT COUNT(*) FROM k WHERE k.day = d.day), 0), 2) AS pct_of_clicks
FROM d CROSS JOIN b
ORDER BY d.day, b.ord
```
`SQL_WRONG` in the Code block is the join-first version, printed in the output for comparison.

**pandas answer:** both results come from one function, identical to the Code block (`isin` is the `EXISTS`; `pd.cut` makes the position buckets):
```py
def search_metrics(searches, clicks):
    s = searches.assign(day=searches["search_ts"].str[:10],
                        clicked=searches["search_id"].isin(clicks["search_id"]),
                        zero=searches["result_count"] == 0)
    daily = (s.groupby("day").agg(searches=("search_id", "size"), searches_with_click=("clicked", "sum"),
                                  zero_result=("zero", "sum")).reset_index())
    daily["ctr"] = (daily["searches_with_click"] / daily["searches"]).round(2)
    daily["zero_result_rate"] = (daily["zero_result"] / daily["searches"]).round(2)
    daily = daily[["day", "searches", "searches_with_click", "ctr", "zero_result", "zero_result_rate"]]

    k = clicks.merge(s[["search_id", "day"]], on="search_id")
    k["bucket"] = pd.cut(k["position"], bins=[0, 1, 2, 3, 10, 10**9],
                         labels=["1", "2", "3", "4-10", "11+"]).astype(str)
    grid = pd.MultiIndex.from_product([sorted(s["day"].unique()), ["1", "2", "3", "4-10", "11+"]],
                                      names=["day", "bucket"]).to_frame(index=False)
    cnt = k.groupby(["day", "bucket"]).size().rename("clicks").reset_index()
    pos = grid.merge(cnt, on=["day", "bucket"], how="left").fillna({"clicks": 0})
    pos["clicks"] = pos["clicks"].astype(int)
    total = pos.groupby("day")["clicks"].transform("sum")
    pos["pct_of_clicks"] = (pos["clicks"] * 100.0 / total.where(total != 0)).round(2)
    return daily, pos
```

**Example:** walk through the sample data by hand.
- 2024-03-01: four searches (1 to 4). Search 1 has two clicks, search 4 has one, searches 2 and 3 none, so searches with a click = 2 and CTR = 2/4 = 0.50. One of the four has `result_count = 0`, zero-result rate 0.25.
- Joining first: search 1 becomes two rows, so the joined table has 5 rows for 4 searches. Counting clicks over true searches gives 3/4 = 0.75, counting click rows over joined rows gives 3/5 = 0.60. Neither is the CTR. On 2024-03-02 the clicks-over-searches version reaches 1.00 although one search in three got no click.
- Zero-result search 2 stays in the denominator (it is a search that could not succeed); the search with `result_count` NULL is in the denominator and not counted as zero-result, so 2024-03-02 shows zero-result rate 0.00.
- Positions on 2024-03-01: clicked positions 1, 3, 2 give 33.33 percent each for buckets 1, 2 and 3 and 0 for the others. On 2024-03-02 positions 1, 12, 5 land in buckets 1, 11+ and 4-10 at 33.33 each. On 2024-03-03 there are no clicks, so the percentages are NULL (NaN in pandas), not 0.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q25: search metrics: searches, CTR (searches with a click), zero-result rate, clicked position distribution
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE searches(search_id INTEGER PRIMARY KEY, user_id INTEGER, search_ts TEXT, query TEXT, result_count INTEGER);
CREATE TABLE clicks(click_id INTEGER PRIMARY KEY, search_id INTEGER, click_ts TEXT, position INTEGER);
INSERT INTO searches VALUES
 (1,1,'2024-03-01 09:00:00','shoes',   5),
 (2,2,'2024-03-01 09:05:00','shooes',  0),
 (3,3,'2024-03-01 10:00:00','bag',    10),
 (4,4,'2024-03-01 11:00:00','watch',   4),
 (5,1,'2024-03-02 09:00:00','phone',  20),
 (6,2,'2024-03-02 09:30:00','case',    3),
 (7,3,'2024-03-02 10:00:00','charger',NULL),
 (8,4,'2024-03-03 08:00:00','lamp',    6);
INSERT INTO clicks VALUES
 (1,1,'2024-03-01 09:00:10',1),(2,1,'2024-03-01 09:00:40',3),
 (3,4,'2024-03-01 11:00:05',2),
 (4,5,'2024-03-02 09:00:07',1),(5,5,'2024-03-02 09:00:30',12),
 (6,6,'2024-03-02 09:30:09',5);
"""

SQL_MAIN = """
WITH s AS (
  SELECT search_id, date(search_ts) AS d, result_count,
         EXISTS (SELECT 1 FROM clicks c WHERE c.search_id = searches.search_id) AS clicked
  FROM searches
)
SELECT d AS day,
       COUNT(*) AS searches,
       SUM(clicked) AS searches_with_click,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(result_count = 0) AS zero_result,
       ROUND(SUM(result_count = 0) * 1.0 / COUNT(*), 2) AS zero_result_rate
FROM s
GROUP BY d
ORDER BY d
"""
SQL_WRONG = """
SELECT date(s.search_ts) AS day,
       COUNT(*) AS searches_after_join,
       COUNT(DISTINCT s.search_id) AS searches_true,
       ROUND(COUNT(c.click_id) * 1.0 / COUNT(DISTINCT s.search_id), 2) AS clicks_over_searches,
       ROUND(COUNT(c.click_id) * 1.0 / COUNT(*), 2) AS click_rows_over_joined_rows
FROM searches s LEFT JOIN clicks c ON c.search_id = s.search_id
GROUP BY date(s.search_ts)
ORDER BY day
"""
SQL_POS = """
WITH b(bucket, ord) AS (VALUES ('1',1),('2',2),('3',3),('4-10',4),('11+',5)),
d AS (SELECT DISTINCT date(search_ts) AS day FROM searches),
k AS (
  SELECT date(s.search_ts) AS day,
         CASE WHEN c.position = 1 THEN '1' WHEN c.position = 2 THEN '2' WHEN c.position = 3 THEN '3'
              WHEN c.position BETWEEN 4 AND 10 THEN '4-10' ELSE '11+' END AS bucket
  FROM clicks c JOIN searches s ON s.search_id = c.search_id
)
SELECT d.day, b.bucket,
       (SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) AS clicks,
       ROUND((SELECT COUNT(*) FROM k WHERE k.day = d.day AND k.bucket = b.bucket) * 100.0 /
             NULLIF((SELECT COUNT(*) FROM k WHERE k.day = d.day), 0), 2) AS pct_of_clicks
FROM d CROSS JOIN b
ORDER BY d.day, b.ord
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_pos = pd.read_sql_query(SQL_POS, con)
print("SQL daily metrics:")
print(sql_main.to_string(index=False))
print("SQL wrong CTR (join first, count rows):")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))
print("SQL click position distribution:")
print(sql_pos.to_string(index=False))

searches = pd.read_sql_query("SELECT * FROM searches", con)
clicks = pd.read_sql_query("SELECT * FROM clicks", con)

# pd:main
def search_metrics(searches, clicks):
    s = searches.assign(day=searches["search_ts"].str[:10],
                        clicked=searches["search_id"].isin(clicks["search_id"]),
                        zero=searches["result_count"] == 0)
    daily = (s.groupby("day").agg(searches=("search_id", "size"), searches_with_click=("clicked", "sum"),
                                  zero_result=("zero", "sum")).reset_index())
    daily["ctr"] = (daily["searches_with_click"] / daily["searches"]).round(2)
    daily["zero_result_rate"] = (daily["zero_result"] / daily["searches"]).round(2)
    daily = daily[["day", "searches", "searches_with_click", "ctr", "zero_result", "zero_result_rate"]]

    k = clicks.merge(s[["search_id", "day"]], on="search_id")
    k["bucket"] = pd.cut(k["position"], bins=[0, 1, 2, 3, 10, 10**9],
                         labels=["1", "2", "3", "4-10", "11+"]).astype(str)
    grid = pd.MultiIndex.from_product([sorted(s["day"].unique()), ["1", "2", "3", "4-10", "11+"]],
                                      names=["day", "bucket"]).to_frame(index=False)
    cnt = k.groupby(["day", "bucket"]).size().rename("clicks").reset_index()
    pos = grid.merge(cnt, on=["day", "bucket"], how="left").fillna({"clicks": 0})
    pos["clicks"] = pos["clicks"].astype(int)
    total = pos.groupby("day")["clicks"].transform("sum")
    pos["pct_of_clicks"] = (pos["clicks"] * 100.0 / total.where(total != 0)).round(2)
    return daily, pos
# pd:end

pd_main, pd_pos = search_metrics(searches, clicks)
# both results are already in (day, bucket order) order, which matches the SQL ORDER BY
pd.testing.assert_frame_equal(pd_main, sql_main, check_dtype=False)
pd.testing.assert_frame_equal(pd_pos, sql_pos, check_dtype=False)
print("pandas daily:")
print(pd_main.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
SQL daily metrics:
       day  searches  searches_with_click  ctr  zero_result  zero_result_rate
2024-03-01         4                    2 0.50            1              0.25
2024-03-02         3                    2 0.67            0              0.00
2024-03-03         1                    0 0.00            0              0.00
SQL wrong CTR (join first, count rows):
       day  searches_after_join  searches_true  clicks_over_searches  click_rows_over_joined_rows
2024-03-01                    5              4                  0.75                         0.60
2024-03-02                    4              3                  1.00                         0.75
2024-03-03                    1              1                  0.00                         0.00
SQL click position distribution:
       day bucket  clicks  pct_of_clicks
2024-03-01      1       1          33.33
2024-03-01      2       1          33.33
2024-03-01      3       1          33.33
2024-03-01   4-10       0           0.00
2024-03-01    11+       0           0.00
2024-03-02      1       1          33.33
2024-03-02      2       0           0.00
2024-03-02      3       0           0.00
2024-03-02   4-10       1          33.33
2024-03-02    11+       1          33.33
2024-03-03      1       0            NaN
2024-03-03      2       0            NaN
2024-03-03      3       0            NaN
2024-03-03   4-10       0            NaN
2024-03-03    11+       0            NaN
pandas daily:
       day  searches  searches_with_click  ctr  zero_result  zero_result_rate
2024-03-01         4                    2 0.50            1              0.25
2024-03-02         3                    2 0.67            0              0.00
2024-03-03         1                    0 0.00            0              0.00
asserts passed
```

**Edge cases:**
- Zero-result searches cannot get a click, so they pull CTR down. Many teams also report CTR over searches that returned results; that is `WHERE result_count > 0` on the denominator and numerator, stated explicitly.
- NULL `result_count` is unknown; `result_count = 0` is false for it, so it is not zero-result.
- A day with searches but no clicks: CTR 0.00 (the flag is 0), positions NaN.
- Click rows whose `search_id` is not in `searches` are ignored by the `EXISTS` form and by the inner merge in the position table.
- Buckets with no clicks need the `CROSS JOIN` against the bucket list, otherwise the row is absent rather than 0.

**Then explain:**
- Two different grains: CTR is per search, position distribution is per click. Do not put them in one join.
- `EXISTS` (or `COUNT(DISTINCT search_id)` after a join) keeps one row per search. `EXISTS` is cheaper because it can stop at the first click.
- Percent of clicks uses clicks as the denominator, so a search with three clicks weighs three times in that table; that is intended and worth saying.
- Click-position metrics such as mean click position or MRR need a decision on searches with no click; not computed here.
- Dialect: the same shape works in Postgres and MySQL; BigQuery would use `COUNTIF` and `DATE(search_ts)` (not executed here).

**Follow-ups:**
- CTR by query? Group by `query`; low volume per query makes it noisy, so show the search count next to it.
- First-click position only? Take `MIN(position)` per search first, then bucket.
- Abandonment (no click and no refinement)? Needs a session notion, see Part 7.

**Common mistakes:**
- Joining searches to clicks and counting rows (shown in the output).
- Using `COUNT(DISTINCT click_id) / COUNT(DISTINCT search_id)`, which is clicks per search, not CTR.
- Treating NULL `result_count` as zero results.
- Dropping the zero-result searches from the denominator without saying so.
- Leaving out zero-count buckets so the distribution does not show them.

### Q26 ⭐⭐ 🟡 Notification and email funnel: sends(send_id, user_id, channel, sent_ts) with channel in ('push', 'email'), opens(send_id, open_ts) and clicks(send_id, click_ts), where opens and clicks can repeat per send. Return per channel sent, unique opens, unique clicks, open rate, click-to-open rate (CTOR) and click-through rate over sent, counting each send once. Explain why raw event counts overstate rates, why a click without an open row can occur (image blocking, Apple mail privacy prefetch inflating opens) and how that makes click-to-open above 100 percent possible, and what a send-level versus user-level rate means.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** Collapse opens and clicks to one flag per send with `EXISTS`, then count sends: open rate is opened sends over sent, click-to-open is clicked sends over opened sends, and click-through is clicked sends over sent; raw event counts overstate every rate when a send is opened or clicked several times.

**Schema and sample data:** eight sends over two channels (`push` and `email`) to three users. Send 1 has two open rows, send 5 has three open rows and two click rows, so event counts exceed send counts. Sends 3, 6 and 8 have a click and no open row. Send 4 has no open and no click. All data is made up.
```sql
CREATE TABLE sends(send_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, sent_ts TEXT);
CREATE TABLE opens(send_id INTEGER, open_ts TEXT);
CREATE TABLE clicks(send_id INTEGER, click_ts TEXT);
INSERT INTO sends VALUES
 (1,1,'push', '2024-03-01 09:00:00'),(2,1,'push', '2024-03-02 09:00:00'),
 (3,2,'push', '2024-03-01 09:00:00'),(4,3,'push', '2024-03-01 09:00:00'),
 (5,1,'email','2024-03-01 08:00:00'),(6,2,'email','2024-03-01 08:00:00'),
 (7,2,'email','2024-03-02 08:00:00'),(8,3,'email','2024-03-01 08:00:00');
INSERT INTO opens VALUES
 (1,'2024-03-01 09:01:00'),(1,'2024-03-01 20:00:00'),(2,'2024-03-02 09:02:00'),
 (5,'2024-03-01 08:05:00'),(5,'2024-03-01 08:06:00'),(5,'2024-03-02 07:00:00'),
 (7,'2024-03-02 08:10:00');
INSERT INTO clicks VALUES
 (1,'2024-03-01 09:01:30'),
 (3,'2024-03-01 09:30:00'),
 (5,'2024-03-01 08:05:30'),(5,'2024-03-01 08:07:00'),
 (6,'2024-03-01 12:00:00'),
 (8,'2024-03-01 13:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block (`SQL_RAW` for the wrong raw-count rates and `SQL_USER` for the user-level open rate are in the Code block too):
```sql
WITH f AS (
  SELECT s.send_id, s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens  o WHERE o.send_id = s.send_id) AS opened,
         EXISTS (SELECT 1 FROM clicks c WHERE c.send_id = s.send_id) AS clicked
  FROM sends s
)
SELECT channel,
       COUNT(*) AS sent,
       SUM(opened) AS unique_opens,
       SUM(clicked) AS unique_clicks,
       ROUND(SUM(opened) * 1.0 / COUNT(*), 2) AS open_rate,
       ROUND(SUM(clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(clicked AND NOT opened) AS click_without_open,
       ROUND(SUM(opened AND clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor_clicked_and_opened
FROM f
GROUP BY channel
ORDER BY channel
```
```sql
WITH f AS (
  SELECT s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens o WHERE o.send_id = s.send_id) AS opened
  FROM sends s
)
SELECT channel, COUNT(DISTINCT user_id) AS users_sent,
       COUNT(DISTINCT CASE WHEN opened THEN user_id END) AS users_opened,
       ROUND(COUNT(DISTINCT CASE WHEN opened THEN user_id END) * 1.0 / COUNT(DISTINCT user_id), 2) AS user_open_rate
FROM f GROUP BY channel ORDER BY channel
```

**pandas answer:** the send-level function, identical to the Code block:
```py
def notification_funnel(sends, opens, clicks):
    f = sends.assign(opened=sends["send_id"].isin(opens["send_id"]),
                     clicked=sends["send_id"].isin(clicks["send_id"]))
    f["both"] = f["opened"] & f["clicked"]
    f["click_no_open"] = f["clicked"] & ~f["opened"]
    out = f.groupby("channel").agg(sent=("send_id", "size"), unique_opens=("opened", "sum"),
                                   unique_clicks=("clicked", "sum"),
                                   click_without_open=("click_no_open", "sum"),
                                   both=("both", "sum")).reset_index()
    opened = out["unique_opens"].where(out["unique_opens"] != 0)
    out["open_rate"] = (out["unique_opens"] / out["sent"]).round(2)
    out["ctor"] = (out["unique_clicks"] / opened).round(2)
    out["ctr"] = (out["unique_clicks"] / out["sent"]).round(2)
    out["ctor_clicked_and_opened"] = (out["both"] / opened).round(2)
    return out[["channel", "sent", "unique_opens", "unique_clicks", "open_rate", "ctor", "ctr",
                "click_without_open", "ctor_clicked_and_opened"]]
```

**Example:** walk through the sample data by hand.
- Push has sends 1 to 4. Opened: sends 1 (two open rows) and 2, so unique opens 2. Clicked: sends 1 and 3, unique clicks 2. Open rate 2/4 = 0.50, CTOR 2/2 = 1.00, CTR over sent 2/4 = 0.50. Send 3 is a click with no open row.
- Email has sends 5 to 8. Opened: sends 5 (three open rows) and 7, so 2. Clicked: sends 5, 6 and 8, so 3. Open rate 2/4 = 0.50, CTR 3/4 = 0.75, CTOR 3/2 = 1.50, which is above 100 percent because two of the three clicked sends (6 and 8) have no open row.
- Restricting CTOR to clicks on sends that were also opened gives 1/2 = 0.50 for email and 1/2 = 0.50 for push; that is the alternative "clean" definition.
- Raw event counts: email has 4 open events and 4 click events for 4 sends, so a raw open rate of 1.00 and a raw click-over-open of 1.00 instead of 0.50 and 1.50; the unit is wrong.
- User level: push went to users 1, 2 and 3; only user 1 opened (both of their sends), so 1/3 = 0.33 users opened against a send-level 0.50. Email is 2/3 = 0.67 at user level against 0.50 at send level.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q26: notification and email funnel: unique opens, unique clicks, open rate, CTOR, CTR over sent
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sends(send_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, sent_ts TEXT);
CREATE TABLE opens(send_id INTEGER, open_ts TEXT);
CREATE TABLE clicks(send_id INTEGER, click_ts TEXT);
INSERT INTO sends VALUES
 (1,1,'push', '2024-03-01 09:00:00'),(2,1,'push', '2024-03-02 09:00:00'),
 (3,2,'push', '2024-03-01 09:00:00'),(4,3,'push', '2024-03-01 09:00:00'),
 (5,1,'email','2024-03-01 08:00:00'),(6,2,'email','2024-03-01 08:00:00'),
 (7,2,'email','2024-03-02 08:00:00'),(8,3,'email','2024-03-01 08:00:00');
INSERT INTO opens VALUES
 (1,'2024-03-01 09:01:00'),(1,'2024-03-01 20:00:00'),(2,'2024-03-02 09:02:00'),
 (5,'2024-03-01 08:05:00'),(5,'2024-03-01 08:06:00'),(5,'2024-03-02 07:00:00'),
 (7,'2024-03-02 08:10:00');
INSERT INTO clicks VALUES
 (1,'2024-03-01 09:01:30'),
 (3,'2024-03-01 09:30:00'),
 (5,'2024-03-01 08:05:30'),(5,'2024-03-01 08:07:00'),
 (6,'2024-03-01 12:00:00'),
 (8,'2024-03-01 13:00:00');
"""

SQL_MAIN = """
WITH f AS (
  SELECT s.send_id, s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens  o WHERE o.send_id = s.send_id) AS opened,
         EXISTS (SELECT 1 FROM clicks c WHERE c.send_id = s.send_id) AS clicked
  FROM sends s
)
SELECT channel,
       COUNT(*) AS sent,
       SUM(opened) AS unique_opens,
       SUM(clicked) AS unique_clicks,
       ROUND(SUM(opened) * 1.0 / COUNT(*), 2) AS open_rate,
       ROUND(SUM(clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(clicked AND NOT opened) AS click_without_open,
       ROUND(SUM(opened AND clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor_clicked_and_opened
FROM f
GROUP BY channel
ORDER BY channel
"""
SQL_RAW = """
SELECT s.channel,
       (SELECT COUNT(*) FROM opens  o JOIN sends x ON x.send_id = o.send_id WHERE x.channel = s.channel) AS open_events,
       (SELECT COUNT(*) FROM clicks c JOIN sends x ON x.send_id = c.send_id WHERE x.channel = s.channel) AS click_events,
       COUNT(*) AS sent
FROM sends s GROUP BY s.channel ORDER BY s.channel
"""
SQL_USER = """
WITH f AS (
  SELECT s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens o WHERE o.send_id = s.send_id) AS opened
  FROM sends s
)
SELECT channel, COUNT(DISTINCT user_id) AS users_sent,
       COUNT(DISTINCT CASE WHEN opened THEN user_id END) AS users_opened,
       ROUND(COUNT(DISTINCT CASE WHEN opened THEN user_id END) * 1.0 / COUNT(DISTINCT user_id), 2) AS user_open_rate
FROM f GROUP BY channel ORDER BY channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, each send counted once:")
print(sql_main.to_string(index=False))
raw = pd.read_sql_query(SQL_RAW, con)
raw["raw_open_rate"] = (raw["open_events"] / raw["sent"]).round(2)
raw["raw_click_over_open_events"] = (raw["click_events"] / raw["open_events"]).round(2)
print("SQL, raw event counts (wrong rates):")
print(raw.to_string(index=False))
sql_user = pd.read_sql_query(SQL_USER, con)
print("SQL, user-level open rate:")
print(sql_user.to_string(index=False))

sends = pd.read_sql_query("SELECT * FROM sends", con)
opens = pd.read_sql_query("SELECT * FROM opens", con)
clicks = pd.read_sql_query("SELECT * FROM clicks", con)

# pd:main
def notification_funnel(sends, opens, clicks):
    f = sends.assign(opened=sends["send_id"].isin(opens["send_id"]),
                     clicked=sends["send_id"].isin(clicks["send_id"]))
    f["both"] = f["opened"] & f["clicked"]
    f["click_no_open"] = f["clicked"] & ~f["opened"]
    out = f.groupby("channel").agg(sent=("send_id", "size"), unique_opens=("opened", "sum"),
                                   unique_clicks=("clicked", "sum"),
                                   click_without_open=("click_no_open", "sum"),
                                   both=("both", "sum")).reset_index()
    opened = out["unique_opens"].where(out["unique_opens"] != 0)
    out["open_rate"] = (out["unique_opens"] / out["sent"]).round(2)
    out["ctor"] = (out["unique_clicks"] / opened).round(2)
    out["ctr"] = (out["unique_clicks"] / out["sent"]).round(2)
    out["ctor_clicked_and_opened"] = (out["both"] / opened).round(2)
    return out[["channel", "sent", "unique_opens", "unique_clicks", "open_rate", "ctor", "ctr",
                "click_without_open", "ctor_clicked_and_opened"]]
# pd:end

pd_main = notification_funnel(sends, opens, clicks)
# compare after sorting by channel (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_main.sort_values("channel").reset_index(drop=True), sql_main, check_dtype=False)
u = sends.assign(opened=sends["send_id"].isin(opens["send_id"]))
pd_user = (u.groupby("channel").apply(lambda g: pd.Series({
    "users_sent": g["user_id"].nunique(), "users_opened": g.loc[g["opened"], "user_id"].nunique()}),
    include_groups=False).reset_index())
pd_user["user_open_rate"] = (pd_user["users_opened"] / pd_user["users_sent"]).round(2)
pd.testing.assert_frame_equal(pd_user, sql_user, check_dtype=False)
print("pandas:")
print(pd_main.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
SQL, each send counted once:
channel  sent  unique_opens  unique_clicks  open_rate  ctor  ctr  click_without_open  ctor_clicked_and_opened
  email     4             2              3        0.5   1.5 0.75                   2                      0.5
   push     4             2              2        0.5   1.0 0.50                   1                      0.5
SQL, raw event counts (wrong rates):
channel  open_events  click_events  sent  raw_open_rate  raw_click_over_open_events
  email            4             4     4           1.00                        1.00
   push            3             2     4           0.75                        0.67
SQL, user-level open rate:
channel  users_sent  users_opened  user_open_rate
  email           3             2            0.67
   push           3             1            0.33
pandas:
channel  sent  unique_opens  unique_clicks  open_rate  ctor  ctr  click_without_open  ctor_clicked_and_opened
  email     4             2              3        0.5   1.5 0.75                   2                      0.5
   push     4             2              2        0.5   1.0 0.50                   1                      0.5
asserts passed
```

**Edge cases:**
- A click with no open row: possible when images are blocked (the open pixel never loads), when the open tracking fails, or in push when the app records the tap without an open event. The result is CTOR above 1.
- Apple Mail Privacy Protection: general knowledge, not sourced here and not tested, is that it can preload email content on behalf of the user, which is widely reported to inflate email open counts; treat email open rate as an upper bound and lean on clicks.
- Opens and clicks that arrive before `sent_ts` or for unknown send ids point to a data problem; here they would be ignored by the `EXISTS` form.
- Zero opened sends gives CTOR NULL through `NULLIF`.
- Repeated rows per send (re-opens) are why distinct sends, not rows, are counted.

**Then explain:**
- Unit: one send is one chance to open. Open rate, CTOR and CTR all count sends, so each send is counted once no matter how many open or click rows it has.
- `EXISTS` per send avoids joining opens and clicks to sends together, which would multiply rows (opens times clicks per send).
- CTOR above 100 percent is a symptom, not a bug in the SQL: the click numerator and the open denominator are measured by different tracking.
- Send-level versus user-level: a user who got two pushes and opened both is two sends opened but one user opened. User-level rates answer 'how many people engaged'; send-level rates answer 'how well does a message perform'.
- Dialect: `EXISTS` and `COUNT(DISTINCT ...)` are portable; BigQuery or Postgres users might prefer `COUNTIF` or `FILTER` (not executed here).

**Follow-ups:**
- Which rate do you trust for email? Clicks over sent, because opens may be prefetched; say it is a judgement.
- Per campaign? Group by campaign id; keep the per-send flag CTE.
- Unsubscribes or bounces in the denominator? Define delivered sends and use that as the denominator; bounces are not in this table.

**Common mistakes:**
- Dividing event counts (open rows, click rows) by sends.
- Joining sends to opens and to clicks in one query without pre-aggregating.
- Computing CTOR as clicks over sends or opens over clicks.
- Treating CTOR above 1 as a bug and clipping it without explaining.
- Mixing user-level numerators with send-level denominators.

### Q27 ⭐⭐ 🟡 Cart abandonment and bounce rate: events(session_id, user_id, event_ts, event_name) with event_name in ('page_view', 'add_to_cart', 'purchase'). Return the cart abandonment rate (sessions with an add_to_cart and no purchase over sessions with an add_to_cart) and the bounce rate (sessions with exactly one event over all sessions), per day of the first event. Show a session with a purchase before the add_to_cart, the effect of a purchase in a later session (a different session id, so the first session still counts as abandoned) and why bounce depends on the event definition (one page_view only versus one event of any kind).
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** Collapse events to one row per session with flags (`MAX(event_name = ...)`), take the day from the session's first event, then abandonment is cart sessions without a purchase over cart sessions and bounce is sessions with exactly one event over all sessions; the definitions of 'no purchase' and of 'one event' are the two things to state out loud.

**Schema and sample data:** fifteen events in nine sessions. Session D has the purchase before the add_to_cart. User 6 adds to cart in session F and buys in a different session G. Session E is a single add_to_cart. Session H has two page views. Session I (2024-03-03) is a single page view and there is no cart session that day.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, session_id TEXT, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 'A',1,'2024-03-01 09:00:00','page_view'),
 (2, 'A',1,'2024-03-01 09:01:00','add_to_cart'),
 (3, 'A',1,'2024-03-01 09:02:00','purchase'),
 (4, 'B',2,'2024-03-01 10:00:00','page_view'),
 (5, 'B',2,'2024-03-01 10:01:00','add_to_cart'),
 (6, 'C',3,'2024-03-01 11:00:00','page_view'),
 (7, 'D',4,'2024-03-01 12:00:00','purchase'),
 (8, 'D',4,'2024-03-01 12:01:00','add_to_cart'),
 (9, 'E',5,'2024-03-01 13:00:00','add_to_cart'),
 (10,'F',6,'2024-03-02 09:00:00','page_view'),
 (11,'F',6,'2024-03-02 09:01:00','add_to_cart'),
 (12,'G',6,'2024-03-02 18:00:00','purchase'),
 (13,'H',7,'2024-03-02 10:00:00','page_view'),
 (14,'H',7,'2024-03-02 10:01:00','page_view'),
 (15,'I',8,'2024-03-03 10:00:00','page_view');
```

**SQL answer:** `SQL_MAIN` in the Code block (literal definition: a cart session is abandoned when it has no purchase anywhere in the session), and `SQL_ORDERED` for the variant where the purchase must come at or after the first add_to_cart:
```sql
WITH s AS (
  SELECT session_id,
         date(MIN(event_ts)) AS day,
         COUNT(*) AS n_events,
         MAX(event_name = 'add_to_cart') AS has_cart,
         MAX(event_name = 'purchase') AS has_purchase,
         MAX(event_name = 'page_view') AS has_view
  FROM events
  GROUP BY session_id
)
SELECT day,
       COUNT(*) AS sessions,
       SUM(has_cart) AS cart_sessions,
       SUM(has_cart = 1 AND has_purchase = 0) AS abandoned,
       ROUND(SUM(has_cart = 1 AND has_purchase = 0) * 1.0 / NULLIF(SUM(has_cart), 0), 2) AS abandonment_rate,
       SUM(n_events = 1) AS bounce_any_event,
       ROUND(SUM(n_events = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_any,
       SUM(n_events = 1 AND has_view = 1) AS bounce_one_page_view,
       ROUND(SUM(n_events = 1 AND has_view = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_pv
FROM s
GROUP BY day
ORDER BY day
```
```sql
WITH s AS (
  SELECT session_id, date(MIN(event_ts)) AS day,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_cart,
         MAX(CASE WHEN event_name = 'purchase' THEN event_ts END) AS last_purchase
  FROM events GROUP BY session_id
)
SELECT day,
       SUM(first_cart IS NOT NULL) AS cart_sessions,
       SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) AS abandoned,
       ROUND(SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) * 1.0 /
             NULLIF(SUM(first_cart IS NOT NULL), 0), 2) AS abandonment_rate_ordered
FROM s GROUP BY day ORDER BY day
```

**pandas answer:** the same logic for the main definition, identical to the Code block:
```py
def session_metrics(events):
    e = events.assign(cart=events["event_name"] == "add_to_cart",
                      buy=events["event_name"] == "purchase",
                      view=events["event_name"] == "page_view")
    s = e.groupby("session_id").agg(first_ts=("event_ts", "min"), n_events=("event_id", "size"),
                                    has_cart=("cart", "max"), has_purchase=("buy", "max"),
                                    has_view=("view", "max")).reset_index()
    s["day"] = s["first_ts"].str[:10]
    s["abandon"] = s["has_cart"] & ~s["has_purchase"]
    s["bounce_any"] = s["n_events"] == 1
    s["bounce_pv"] = s["bounce_any"] & s["has_view"]
    out = s.groupby("day").agg(sessions=("session_id", "size"), cart_sessions=("has_cart", "sum"),
                               abandoned=("abandon", "sum"), bounce_any_event=("bounce_any", "sum"),
                               bounce_one_page_view=("bounce_pv", "sum")).reset_index()
    out["abandonment_rate"] = (out["abandoned"] / out["cart_sessions"].where(out["cart_sessions"] != 0)).round(2)
    out["bounce_rate_any"] = (out["bounce_any_event"] / out["sessions"]).round(2)
    out["bounce_rate_pv"] = (out["bounce_one_page_view"] / out["sessions"]).round(2)
    return out[["day", "sessions", "cart_sessions", "abandoned", "abandonment_rate",
                "bounce_any_event", "bounce_rate_any", "bounce_one_page_view", "bounce_rate_pv"]]
```

**Example:** walk through the sample data by hand.
- 2024-03-01 has sessions A to E. Cart sessions: A, B, D, E (4). With the literal definition A (bought) and D (bought, earlier) are not abandoned; B and E are, so 2/4 = 0.50.
- With the ordered variant D counts as abandoned (its purchase came before the cart), so 3/4 = 0.75. One session moves the rate by 25 points.
- 2024-03-02: F has a cart and no purchase in F; the purchase is in session G (a different id), so F is abandoned: 1/1 = 1.00. If you stitched sessions per user within a day the answer would differ, but the question says sessions stay separate.
- Bounce on 2024-03-01: session C (one page_view) and session E (one add_to_cart) have exactly one event, so 2/5 = 0.40 under 'one event of any kind'; only C is a single page view, so 1/5 = 0.20 under 'one page_view only'.
- 2024-03-02: G (one purchase) is the only single-event session, 1/3 = 0.33 under the any-event rule and 0 under the page_view rule. H has two page views so it is not a bounce here.
- 2024-03-03: no cart session, so abandonment is NULL (not 0); the one session is a bounce, 1.00.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q27: cart abandonment rate and bounce rate per day of the session's first event
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, session_id TEXT, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 'A',1,'2024-03-01 09:00:00','page_view'),
 (2, 'A',1,'2024-03-01 09:01:00','add_to_cart'),
 (3, 'A',1,'2024-03-01 09:02:00','purchase'),
 (4, 'B',2,'2024-03-01 10:00:00','page_view'),
 (5, 'B',2,'2024-03-01 10:01:00','add_to_cart'),
 (6, 'C',3,'2024-03-01 11:00:00','page_view'),
 (7, 'D',4,'2024-03-01 12:00:00','purchase'),
 (8, 'D',4,'2024-03-01 12:01:00','add_to_cart'),
 (9, 'E',5,'2024-03-01 13:00:00','add_to_cart'),
 (10,'F',6,'2024-03-02 09:00:00','page_view'),
 (11,'F',6,'2024-03-02 09:01:00','add_to_cart'),
 (12,'G',6,'2024-03-02 18:00:00','purchase'),
 (13,'H',7,'2024-03-02 10:00:00','page_view'),
 (14,'H',7,'2024-03-02 10:01:00','page_view'),
 (15,'I',8,'2024-03-03 10:00:00','page_view');
"""

SQL_MAIN = """
WITH s AS (
  SELECT session_id,
         date(MIN(event_ts)) AS day,
         COUNT(*) AS n_events,
         MAX(event_name = 'add_to_cart') AS has_cart,
         MAX(event_name = 'purchase') AS has_purchase,
         MAX(event_name = 'page_view') AS has_view
  FROM events
  GROUP BY session_id
)
SELECT day,
       COUNT(*) AS sessions,
       SUM(has_cart) AS cart_sessions,
       SUM(has_cart = 1 AND has_purchase = 0) AS abandoned,
       ROUND(SUM(has_cart = 1 AND has_purchase = 0) * 1.0 / NULLIF(SUM(has_cart), 0), 2) AS abandonment_rate,
       SUM(n_events = 1) AS bounce_any_event,
       ROUND(SUM(n_events = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_any,
       SUM(n_events = 1 AND has_view = 1) AS bounce_one_page_view,
       ROUND(SUM(n_events = 1 AND has_view = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_pv
FROM s
GROUP BY day
ORDER BY day
"""
# variant: a purchase only completes the cart if it happens at or after the first add_to_cart
SQL_ORDERED = """
WITH s AS (
  SELECT session_id, date(MIN(event_ts)) AS day,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_cart,
         MAX(CASE WHEN event_name = 'purchase' THEN event_ts END) AS last_purchase
  FROM events GROUP BY session_id
)
SELECT day,
       SUM(first_cart IS NOT NULL) AS cart_sessions,
       SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) AS abandoned,
       ROUND(SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) * 1.0 /
             NULLIF(SUM(first_cart IS NOT NULL), 0), 2) AS abandonment_rate_ordered
FROM s GROUP BY day ORDER BY day
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_ord = pd.read_sql_query(SQL_ORDERED, con)
print("SQL (abandoned = cart and no purchase anywhere in the session):")
print(sql_main.to_string(index=False))
print("SQL variant (purchase must be at or after the first add_to_cart):")
print(sql_ord.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def session_metrics(events):
    e = events.assign(cart=events["event_name"] == "add_to_cart",
                      buy=events["event_name"] == "purchase",
                      view=events["event_name"] == "page_view")
    s = e.groupby("session_id").agg(first_ts=("event_ts", "min"), n_events=("event_id", "size"),
                                    has_cart=("cart", "max"), has_purchase=("buy", "max"),
                                    has_view=("view", "max")).reset_index()
    s["day"] = s["first_ts"].str[:10]
    s["abandon"] = s["has_cart"] & ~s["has_purchase"]
    s["bounce_any"] = s["n_events"] == 1
    s["bounce_pv"] = s["bounce_any"] & s["has_view"]
    out = s.groupby("day").agg(sessions=("session_id", "size"), cart_sessions=("has_cart", "sum"),
                               abandoned=("abandon", "sum"), bounce_any_event=("bounce_any", "sum"),
                               bounce_one_page_view=("bounce_pv", "sum")).reset_index()
    out["abandonment_rate"] = (out["abandoned"] / out["cart_sessions"].where(out["cart_sessions"] != 0)).round(2)
    out["bounce_rate_any"] = (out["bounce_any_event"] / out["sessions"]).round(2)
    out["bounce_rate_pv"] = (out["bounce_one_page_view"] / out["sessions"]).round(2)
    return out[["day", "sessions", "cart_sessions", "abandoned", "abandonment_rate",
                "bounce_any_event", "bounce_rate_any", "bounce_one_page_view", "bounce_rate_pv"]]
# pd:end

pd_main = session_metrics(events)
# compare after sorting by day (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_main.sort_values("day").reset_index(drop=True), sql_main, check_dtype=False)
print("pandas:")
print(pd_main.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
SQL (abandoned = cart and no purchase anywhere in the session):
       day  sessions  cart_sessions  abandoned  abandonment_rate  bounce_any_event  bounce_rate_any  bounce_one_page_view  bounce_rate_pv
2024-03-01         5              4          2               0.5                 2             0.40                     1             0.2
2024-03-02         3              1          1               1.0                 1             0.33                     0             0.0
2024-03-03         1              0          0               NaN                 1             1.00                     1             1.0
SQL variant (purchase must be at or after the first add_to_cart):
       day  cart_sessions  abandoned  abandonment_rate_ordered
2024-03-01              4          3                      0.75
2024-03-02              1          1                      1.00
2024-03-03              0          0                       NaN
pandas:
       day  sessions  cart_sessions  abandoned  abandonment_rate  bounce_any_event  bounce_rate_any  bounce_one_page_view  bounce_rate_pv
2024-03-01         5              4          2               0.5                 2             0.40                     1             0.2
2024-03-02         3              1          1               1.0                 1             0.33                     0             0.0
2024-03-03         1              0          0               NaN                 1             1.00                     1             1.0
asserts passed
```

**Edge cases:**
- No cart sessions on a day: `NULLIF(SUM(has_cart), 0)` returns NULL; reporting 0 would suggest nobody abandoned.
- Sessions that cross midnight belong to the day of their first event (`date(MIN(event_ts))`), not split by day.
- Session id reuse across users or days would merge unrelated rows; assume the id is unique and, if it is not, group by (user_id, session_id).
- Ties on `event_ts` do not matter for these flags except in the ordered variant, where a purchase and a cart at the same timestamp counts as completed (`<` test).
- Bounce is also sometimes defined with time on page; not available here.

**Then explain:**
- Grain: the rate is a ratio of sessions, so build one row per session first and aggregate that. Counting events gives different, wrong, numbers.
- 'Abandoned' must be defined: literal (no purchase in the session) versus ordered (no purchase after the cart). They differ when purchases can precede carts (for example a re-order flow).
- A purchase in a later session does not rescue the earlier session in this metric; a user-level or time-windowed cart abandonment would, and is a different metric.
- Bounce depends on the event definition: with 'one page_view only' a single `add_to_cart` or `purchase` session is not a bounce; with 'one event of any kind' it is. Many analytics tools define bounce differently again (engagement based); state which one you use.
- Dialect: `MAX(boolean)` as a flag works in SQLite and MySQL; in Postgres use `BOOL_OR(...)` or `MAX(CASE WHEN ... THEN 1 ELSE 0 END)` (not executed here).

**Follow-ups:**
- Cart abandonment at user-day level? Group by user and day first, then apply the flags.
- Add checkout steps? That is a funnel; keep the per-session flags and add one flag per step.
- Abandonment value (cart value lost)? Needs cart contents; not in this table.

**Common mistakes:**
- Computing abandonment over all sessions instead of cart sessions.
- Counting events, not sessions, in numerator or denominator.
- Not saying whether a purchase before the cart counts.
- Defining bounce by `COUNT(*) = 1` and then reporting it as 'single page_view'.
- Reporting 0 when the denominator is empty.

### Q28 ⭐⭐ 🟡 Engagement distribution and power users: events(user_id, event_ts, event_name) and users(user_id, signup_date, country, is_test). For March 2024 return events per active user (mean and median, SQLite has no MEDIAN so use a window or ORDER BY LIMIT approach), the power-user cut using NTILE(10) over users ranked by event count (see Part 4 for NTILE), and the share of all events produced by the top decile. Explain why the mean is misleading for skewed usage, how ties across a decile boundary behave, and how users with zero events in the month are handled (included or excluded changes every number).
**Asked at:** StrataScratch product-analytics blog (opened; lists five questions such as Meta Users By Average Session Time and Salesforce User Growth Rate, none labelled candidate-reported) and DataLemur and Interview Query pages (search snippets only); practice-site material, not candidate reports; product analytics and data scientist rounds
**Say this first (1 line):** Count March events per user, take the mean with `AVG` and the median from `ROW_NUMBER` and `COUNT(*) OVER ()` (SQLite has no MEDIAN), cut `NTILE(10)` over users ordered by event count with a `user_id` tie-breaker, and divide the top decile's events by all events; whether zero-event users are in the population changes every one of these numbers, so say which one you use.

**Schema and sample data:** thirteen users (user 13 is a test user, user 12 and user 11 have no March events). The `events` rows are generated in the Code block: March counts per user are 1, 1, 2, 2, 3, 4, 5, 8, 20, 60 for users 1 to 10 (106 events), plus four rows that must be ignored: a February event for user 1, an April 1st event for user 2 (the upper bound is exclusive), a February event for user 11 and a March event for test user 13. Dates and counts are toy values.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-06','IN',0),(3,'2024-01-07','IN',0),(4,'2024-01-08','IN',0),
 (5,'2024-01-09','IN',0),(6,'2024-01-10','IN',0),(7,'2024-01-11','IN',0),(8,'2024-01-12','IN',0),
 (9,'2024-01-13','IN',0),(10,'2024-01-14','IN',0),(11,'2024-01-15','IN',0),(12,'2024-01-16','IN',0),
 (13,'2024-01-17','IN',1);
```

**SQL answer:** `SQL_TEMPLATE` in the Code block, with `{JOIN}` replaced by `JOIN` (active users only, `SQL_ACTIVE`) or `LEFT JOIN` (all non-test registered users, `SQL_ALL`). The median is the average of the rows at positions `(cnt + 1) / 2` and `(cnt + 2) / 2` (integer division, see Part 4 Q38 for the median pattern in full). `SQL_TEMPLATE`:
```sql
WITH u AS (
  SELECT us.user_id, COUNT(e.event_id) AS n
  FROM users us
  {JOIN} events e ON e.user_id = us.user_id
       AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
  WHERE us.is_test = 0
  GROUP BY us.user_id
), r AS (
  SELECT user_id, n,
         NTILE(10) OVER (ORDER BY n DESC, user_id) AS decile,
         ROW_NUMBER() OVER (ORDER BY n, user_id) AS rn,
         COUNT(*) OVER () AS cnt
  FROM u
), med AS (
  SELECT AVG(n) AS median FROM r WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
)
SELECT COUNT(*) AS users,
       SUM(n) AS events,
       ROUND(AVG(n), 2) AS mean_events,
       (SELECT median FROM med) AS median_events,
       SUM(decile = 1) AS top_decile_users,
       SUM(CASE WHEN decile = 1 THEN n END) AS top_decile_events,
       ROUND(SUM(CASE WHEN decile = 1 THEN n END) * 100.0 / SUM(n), 2) AS top_decile_share_pct
FROM r
```
NTILE itself is explained in Part 4 Q21 and pandas `qcut` versus NTILE in Part 4 Q33; here pandas needs a hand-written NTILE (`ntile` in the function below), because `qcut` splits by value, not by position.

**pandas answer:** the same logic (`keep_zero` is the INNER versus LEFT join choice; `ntile` reproduces positional NTILE):
```py
def ntile(n_rows, k):
    # NTILE: the first (n_rows % k) buckets get one extra row; assigned by position
    base, extra = divmod(n_rows, k)
    out = []
    for i in range(n_rows):
        if i < extra * (base + 1):
            out.append(i // (base + 1) + 1)
        else:
            out.append(extra + (i - extra * (base + 1)) // base + 1)
    return out

def engagement(users, events, keep_zero):
    m = events[(events["event_ts"] >= "2024-03-01") & (events["event_ts"] < "2024-04-01")]
    cnt = m.groupby("user_id").size().rename("n")
    u = users.loc[users["is_test"] == 0, ["user_id"]].merge(cnt, on="user_id", how="left")
    u["n"] = u["n"].fillna(0).astype(int)
    if not keep_zero:
        u = u[u["n"] > 0]
    u = u.sort_values(["n", "user_id"], ascending=[False, True]).reset_index(drop=True)
    u["decile"] = ntile(len(u), 10) if len(u) >= 10 else range(1, len(u) + 1)
    top = u[u["decile"] == 1]
    return pd.DataFrame({"users": [len(u)], "events": [u["n"].sum()], "mean_events": [round(u["n"].mean(), 2)],
                         "median_events": [float(u["n"].median())], "top_decile_users": [len(top)],
                         "top_decile_events": [top["n"].sum()],
                         "top_decile_share_pct": [round(top["n"].sum() * 100.0 / u["n"].sum(), 2)]}), u
```

**Example:** walk through the sample data by hand.
- Active users only (users 1 to 10; users 11 and 12 and test user 13 excluded): total 106 events, mean 106/10 = 10.6. Sorted counts are 1, 1, 2, 2, 3, 4, 5, 8, 20, 60; the median is the average of the 5th and 6th, (3 + 4)/2 = 3.5. NTILE(10) over 10 rows gives one user per decile, so the top decile is user 10 with 60 events, 60/106 = 56.60 percent.
- All 12 non-test users (zero-event users 11 and 12 kept): same 106 events, mean 106/12 = 8.83, median is the average of the 6th and 7th of 0, 0, 1, 1, 2, 2, 3, 4, 5, 8, 20, 60, that is (2 + 3)/2 = 2.5. NTILE(10) over 12 rows makes the first two buckets hold two users each (12 = 10 x 1 + 2 extra), so the top decile is users 10 and 9 with 80 events, 80/106 = 75.47 percent.
- Decile boundary and ties: users 3 and 4 both have 2 events, yet user 3 is in decile 5 and user 4 in decile 6 because NTILE is positional and the `user_id` tie-breaker decides. Without a tie-breaker the split of tied users would be arbitrary and could change between runs.
- The mean (10.6) is three times the median (3.5): the two heaviest users make most of the volume.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q28: engagement distribution: mean and median events per user, NTILE(10) power users, top decile share
import sqlite3
import pandas as pd

def build_events():
    # events per March user: u1 1, u2 1, u3 2, u4 2, u5 3, u6 4, u7 5, u8 8, u9 20, u10 60
    counts = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 8, 9: 20, 10: 60}
    rows, i = [], 0
    for u, n in counts.items():
        for k in range(n):
            i += 1
            rows.append((i, u, "2024-03-%02d 10:%02d:00" % (1 + (k % 28), k % 60), "click"))
    rows += [(1001, 1, "2024-02-28 10:00:00", "click"), (1002, 11, "2024-02-29 10:00:00", "click"),
             (1003, 2, "2024-04-01 10:00:00", "click"), (1004, 13, "2024-03-05 10:00:00", "click")]
    return rows

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-06','IN',0),(3,'2024-01-07','IN',0),(4,'2024-01-08','IN',0),
 (5,'2024-01-09','IN',0),(6,'2024-01-10','IN',0),(7,'2024-01-11','IN',0),(8,'2024-01-12','IN',0),
 (9,'2024-01-13','IN',0),(10,'2024-01-14','IN',0),(11,'2024-01-15','IN',0),(12,'2024-01-16','IN',0),
 (13,'2024-01-17','IN',1);
"""

# {BASE} is replaced: active users only (INNER JOIN) or all non-test registered users (LEFT JOIN, zeros kept)
SQL_TEMPLATE = """
WITH u AS (
  SELECT us.user_id, COUNT(e.event_id) AS n
  FROM users us
  {JOIN} events e ON e.user_id = us.user_id
       AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
  WHERE us.is_test = 0
  GROUP BY us.user_id
), r AS (
  SELECT user_id, n,
         NTILE(10) OVER (ORDER BY n DESC, user_id) AS decile,
         ROW_NUMBER() OVER (ORDER BY n, user_id) AS rn,
         COUNT(*) OVER () AS cnt
  FROM u
), med AS (
  SELECT AVG(n) AS median FROM r WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
)
SELECT COUNT(*) AS users,
       SUM(n) AS events,
       ROUND(AVG(n), 2) AS mean_events,
       (SELECT median FROM med) AS median_events,
       SUM(decile = 1) AS top_decile_users,
       SUM(CASE WHEN decile = 1 THEN n END) AS top_decile_events,
       ROUND(SUM(CASE WHEN decile = 1 THEN n END) * 100.0 / SUM(n), 2) AS top_decile_share_pct
FROM r
"""
SQL_ACTIVE = SQL_TEMPLATE.replace("{JOIN}", "JOIN")
SQL_ALL = SQL_TEMPLATE.replace("{JOIN}", "LEFT JOIN")
SQL_DECILES = """
SELECT us.user_id, COUNT(e.event_id) AS n,
       NTILE(10) OVER (ORDER BY COUNT(e.event_id) DESC, us.user_id) AS decile
FROM users us LEFT JOIN events e ON e.user_id = us.user_id
     AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
WHERE us.is_test = 0
GROUP BY us.user_id
ORDER BY decile, us.user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.executemany("INSERT INTO events VALUES (?,?,?,?)", build_events())
print("integer division check, (12 + 1) / 2 and (12 + 2) / 2:", con.execute("SELECT (12+1)/2, (12+2)/2").fetchone())
a = pd.read_sql_query(SQL_ACTIVE, con)
b = pd.read_sql_query(SQL_ALL, con)
print("SQL, active users only (zero-event users excluded):")
print(a.to_string(index=False))
print("SQL, all non-test registered users (zero-event users kept):")
print(b.to_string(index=False))
dec = pd.read_sql_query(SQL_DECILES, con)
print("SQL, deciles over all non-test users (NTILE(10) over 12 rows):")
print(dec.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def ntile(n_rows, k):
    # NTILE: the first (n_rows % k) buckets get one extra row; assigned by position
    base, extra = divmod(n_rows, k)
    out = []
    for i in range(n_rows):
        if i < extra * (base + 1):
            out.append(i // (base + 1) + 1)
        else:
            out.append(extra + (i - extra * (base + 1)) // base + 1)
    return out

def engagement(users, events, keep_zero):
    m = events[(events["event_ts"] >= "2024-03-01") & (events["event_ts"] < "2024-04-01")]
    cnt = m.groupby("user_id").size().rename("n")
    u = users.loc[users["is_test"] == 0, ["user_id"]].merge(cnt, on="user_id", how="left")
    u["n"] = u["n"].fillna(0).astype(int)
    if not keep_zero:
        u = u[u["n"] > 0]
    u = u.sort_values(["n", "user_id"], ascending=[False, True]).reset_index(drop=True)
    u["decile"] = ntile(len(u), 10) if len(u) >= 10 else range(1, len(u) + 1)
    top = u[u["decile"] == 1]
    return pd.DataFrame({"users": [len(u)], "events": [u["n"].sum()], "mean_events": [round(u["n"].mean(), 2)],
                         "median_events": [float(u["n"].median())], "top_decile_users": [len(top)],
                         "top_decile_events": [top["n"].sum()],
                         "top_decile_share_pct": [round(top["n"].sum() * 100.0 / u["n"].sum(), 2)]}), u
# pd:end

pd_a, _ = engagement(users, events, keep_zero=False)
pd_b, pu = engagement(users, events, keep_zero=True)
# one-row results, so no sort is needed
pd.testing.assert_frame_equal(pd_a, a, check_dtype=False)
pd.testing.assert_frame_equal(pd_b, b, check_dtype=False)
pd.testing.assert_frame_equal(pu[["user_id", "n", "decile"]].sort_values(["decile", "user_id"]).reset_index(drop=True),
                              dec, check_dtype=False)
print("pandas, keep_zero=True:")
print(pd_b.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
integer division check, (12 + 1) / 2 and (12 + 2) / 2: (6, 7)
SQL, active users only (zero-event users excluded):
 users  events  mean_events  median_events  top_decile_users  top_decile_events  top_decile_share_pct
    10     106         10.6            3.5                 1                 60                  56.6
SQL, all non-test registered users (zero-event users kept):
 users  events  mean_events  median_events  top_decile_users  top_decile_events  top_decile_share_pct
    12     106         8.83            2.5                 2                 80                 75.47
SQL, deciles over all non-test users (NTILE(10) over 12 rows):
 user_id  n  decile
       9 20       1
      10 60       1
       7  5       2
       8  8       2
       6  4       3
       5  3       4
       3  2       5
       4  2       6
       1  1       7
       2  1       8
      11  0       9
      12  0      10
pandas, keep_zero=True:
 users  events  mean_events  median_events  top_decile_users  top_decile_events  top_decile_share_pct
    12     106         8.83            2.5                 2                 80                 75.47
asserts passed
```

**Edge cases:**
- Zero-event users: included or excluded changes users, mean, median, the decile sizes and the top share (all four printed). 'Events per active user' by definition excludes them.
- Even count: median averages two middle rows; odd count: both positions point at the same row, so the average is that row.
- Fewer than 10 users: NTILE(10) makes buckets of size 1 or 0 (the pandas helper falls back to `range(1, n+1)` in that case, matching NTILE for 10 or fewer rows).
- Ties at the decile boundary: add a deterministic tie-breaker and state that equal users can land in different deciles; alternatives are `PERCENT_RANK` or rank-based cuts that keep ties together (Part 4 Q36).
- Test users and the date range: the range uses `>= '2024-03-01' AND < '2024-04-01'`, so the whole of March 31 is included whatever the time part.

**Then explain:**
- Mean versus median: usage is skewed (a few heavy users), so the mean is pulled up and says little about a typical user. Report the median and a high percentile, or the share held by the top decile.
- NTILE(10) splits by position, not by value: with 12 rows two buckets get an extra row. Top decile is therefore 'the first 10 percent of users in rank order', not 'users above the 90th percentile value'.
- Power-user share: top-decile events over all events (56.6 percent active-only, 75.47 percent with zero users). This is a concentration measure; the Pareto version with revenue is in Part 4 Q49.
- Median without MEDIAN: `ROW_NUMBER() OVER (ORDER BY n)` and `COUNT(*) OVER ()`; SQLite integer division makes `(cnt + 1) / 2` the lower middle position (12 gives 6 and 7, confirmed in my run). PostgreSQL has `PERCENTILE_CONT(0.5)` and BigQuery `PERCENTILE_CONT` as a window function (not executed here).
- Population choice belongs in the definition: say 'active users in March, non-test'.

**Follow-ups:**
- Show the whole decile table? `SQL_DECILES` in the Code block prints every user's decile.
- Top 1 percent instead? Use `NTILE(100)`, but note small populations make that meaningless.
- Median events per user per day? Compute per user-day first, then the median; the grain changes.

**Common mistakes:**
- Reporting the mean as the typical user.
- NTILE without a tie-breaker, so tied users move between runs.
- Mixing populations: mean over active users and top-decile share over all registered users.
- Forgetting the test-user filter, or using `<= '2024-03-31'` on a timestamp and losing most of March 31.
- Using `qcut` as if it were NTILE (it cuts by value quantiles, can raise on duplicate edges unless told to drop them, and does not break ties by position).

### Q29 ⭐⭐ 🟡 Top products per category metrics: order_items(order_id, product_id, qty, unit_price), products(product_id, category, name) and orders(order_id, user_id, order_ts, status). Return for each category the top 2 products by completed revenue, with units, revenue, share of category revenue and rank (ties kept with DENSE_RANK; ranking mechanics are in Part 4). Compute revenue at line-item grain (qty times unit_price), not by joining an order total onto each item, and say how cancelled orders, a product without a category, and a category with fewer than two products are treated.
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** Compute revenue at line-item grain (`qty * unit_price`) from completed orders only, aggregate to product, add `SUM(revenue) OVER (PARTITION BY category)` for the share and `DENSE_RANK` within category, then keep rank 2 or better; with `DENSE_RANK` a tie at second place returns three products, which is the intended 'ties kept' behaviour.

**Schema and sample data:** eight products (product 7 has no category, product 8 is alone in its category), five orders (order 4 is cancelled) and thirteen line items. The last item references product 99, which is not in `products`. Electronics is built so that products 2 and 3 tie at 200.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, status TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER, unit_price REAL);
INSERT INTO products VALUES
 (1,'Electronics','Phone'),(2,'Electronics','Case'),(3,'Electronics','Cable'),(4,'Electronics','Charger'),
 (5,'Books','Novel'),(6,'Books','Notebook'),(7,NULL,'Gift card'),(8,'Home','Lamp');
INSERT INTO orders VALUES
 (1,1,'2024-03-01','completed'),(2,2,'2024-03-02','completed'),(3,3,'2024-03-03','completed'),
 (4,4,'2024-03-04','cancelled'),(5,5,'2024-03-05','completed');
INSERT INTO order_items VALUES
 (1,1,1,500),(1,2,2,50),
 (2,1,1,500),(2,3,1,100),(2,5,3,20),
 (3,2,2,50),(3,4,1,50),(3,6,5,10),
 (4,4,10,50),
 (5,3,1,100),(5,7,1,30),(5,8,2,40),
 (5,99,1,10);
```

**SQL answer:** `SQL_MAIN` in the Code block (`SQL_WRONG` is the order-total-on-every-row version):
```sql
WITH p AS (
  SELECT COALESCE(pr.category, 'Uncategorised') AS category, pr.name,
         SUM(oi.qty) AS units, SUM(oi.qty * oi.unit_price) AS revenue
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  JOIN products pr ON pr.product_id = oi.product_id
  GROUP BY COALESCE(pr.category, 'Uncategorised'), pr.product_id, pr.name
), r AS (
  SELECT category, name, units, revenue,
         ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) AS share_pct,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
  FROM p
)
SELECT category, name, units, revenue, share_pct, rnk
FROM r
WHERE rnk <= 2
ORDER BY category, rnk, name
```

**pandas answer:** the same logic, identical to the Code block (`rank(method='dense', ascending=False)` is `DENSE_RANK`):
```py
def top_products(products, orders, items, n=2):
    d = (items.merge(orders.loc[orders["status"] == "completed", ["order_id"]], on="order_id")
              .merge(products, on="product_id"))
    d["category"] = d["category"].fillna("Uncategorised")
    d["revenue"] = d["qty"] * d["unit_price"]
    p = d.groupby(["category", "product_id", "name"], as_index=False).agg(units=("qty", "sum"),
                                                                           revenue=("revenue", "sum"))
    p["share_pct"] = (p["revenue"] * 100.0 / p.groupby("category")["revenue"].transform("sum")).round(2)
    p["rnk"] = p.groupby("category")["revenue"].rank(method="dense", ascending=False).astype(int)
    out = p[p["rnk"] <= n].sort_values(["category", "rnk", "name"]).reset_index(drop=True)
    return out[["category", "name", "units", "revenue", "share_pct", "rnk"]]
```

**Example:** walk through the sample data by hand.
- Completed line items only: order 4 (cancelled) is excluded, which removes 10 units of product 4 (500) and leaves the Charger at 50.
- Electronics: Phone 2 x 500 = 1000, Case 2 + 2 units x 50 = 200 (4 units), Cable 100 + 100 = 200 (2 units), Charger 50. Category total 1450. Dense ranks: Phone 1, Case and Cable 2 (tie), Charger 3. The top-2 filter keeps Phone, Cable and Case: three rows. Shares: 1000/1450 = 68.97, 200/1450 = 13.79 each.
- Books: Novel 3 x 20 = 60, Notebook 5 x 10 = 50, so ranks 1 and 2, shares 54.55 and 45.45.
- Product 7 (Gift card) has no category and goes to an explicit 'Uncategorised' group with share 100; Home has one product (Lamp, 80), so it returns one row, not two.
- The item for product 99 is dropped by the inner join to `products`.
- Wrong version: joining an order total onto every item row makes product revenue 880 for Cable (the whole order 2 and order 5 totals) instead of 200, and 1260 for Phone instead of 1000, because every product in the order is credited with the order's total.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q29: top 2 products per category by completed revenue at line-item grain, DENSE_RANK keeps ties
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, status TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER, unit_price REAL);
INSERT INTO products VALUES
 (1,'Electronics','Phone'),(2,'Electronics','Case'),(3,'Electronics','Cable'),(4,'Electronics','Charger'),
 (5,'Books','Novel'),(6,'Books','Notebook'),(7,NULL,'Gift card'),(8,'Home','Lamp');
INSERT INTO orders VALUES
 (1,1,'2024-03-01','completed'),(2,2,'2024-03-02','completed'),(3,3,'2024-03-03','completed'),
 (4,4,'2024-03-04','cancelled'),(5,5,'2024-03-05','completed');
INSERT INTO order_items VALUES
 (1,1,1,500),(1,2,2,50),
 (2,1,1,500),(2,3,1,100),(2,5,3,20),
 (3,2,2,50),(3,4,1,50),(3,6,5,10),
 (4,4,10,50),
 (5,3,1,100),(5,7,1,30),(5,8,2,40),
 (5,99,1,10);
"""

SQL_MAIN = """
WITH p AS (
  SELECT COALESCE(pr.category, 'Uncategorised') AS category, pr.name,
         SUM(oi.qty) AS units, SUM(oi.qty * oi.unit_price) AS revenue
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  JOIN products pr ON pr.product_id = oi.product_id
  GROUP BY COALESCE(pr.category, 'Uncategorised'), pr.product_id, pr.name
), r AS (
  SELECT category, name, units, revenue,
         ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) AS share_pct,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
  FROM p
)
SELECT category, name, units, revenue, share_pct, rnk
FROM r
WHERE rnk <= 2
ORDER BY category, rnk, name
"""
# wrong: an order total joined onto every item row
SQL_WRONG = """
WITH ot AS (SELECT order_id, SUM(qty * unit_price) AS order_total FROM order_items GROUP BY order_id)
SELECT pr.name, SUM(ot.order_total) AS wrong_revenue, SUM(oi.qty * oi.unit_price) AS line_revenue
FROM order_items oi
JOIN ot ON ot.order_id = oi.order_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
JOIN products pr ON pr.product_id = oi.product_id
WHERE pr.category = 'Electronics'
GROUP BY pr.product_id, pr.name ORDER BY pr.name
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL:")
print(sql_main.to_string(index=False))
print("SQL wrong (order total on every item row), Electronics:")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

products = pd.read_sql_query("SELECT * FROM products", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
items = pd.read_sql_query("SELECT * FROM order_items", con)

# pd:main
def top_products(products, orders, items, n=2):
    d = (items.merge(orders.loc[orders["status"] == "completed", ["order_id"]], on="order_id")
              .merge(products, on="product_id"))
    d["category"] = d["category"].fillna("Uncategorised")
    d["revenue"] = d["qty"] * d["unit_price"]
    p = d.groupby(["category", "product_id", "name"], as_index=False).agg(units=("qty", "sum"),
                                                                           revenue=("revenue", "sum"))
    p["share_pct"] = (p["revenue"] * 100.0 / p.groupby("category")["revenue"].transform("sum")).round(2)
    p["rnk"] = p.groupby("category")["revenue"].rank(method="dense", ascending=False).astype(int)
    out = p[p["rnk"] <= n].sort_values(["category", "rnk", "name"]).reset_index(drop=True)
    return out[["category", "name", "units", "revenue", "share_pct", "rnk"]]
# pd:end

pd_res = top_products(products, orders, items)
# compare after sorting by category, rnk, name (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_res, sql_main, check_dtype=False)
print("pandas rows:", len(pd_res), "; SQL rows:", len(sql_main))
print("asserts passed")
```

**Output (my run):**
```text
SQL:
     category      name  units  revenue  share_pct  rnk
        Books     Novel      3     60.0      54.55    1
        Books  Notebook      5     50.0      45.45    2
  Electronics     Phone      2   1000.0      68.97    1
  Electronics     Cable      2    200.0      13.79    2
  Electronics      Case      4    200.0      13.79    2
         Home      Lamp      2     80.0     100.00    1
Uncategorised Gift card      1     30.0     100.00    1
SQL wrong (order total on every item row), Electronics:
   name  wrong_revenue  line_revenue
  Cable          880.0         200.0
   Case          800.0         200.0
Charger          200.0          50.0
  Phone         1260.0        1000.0
pandas rows: 7 ; SQL rows: 7
asserts passed
```

**Edge cases:**
- Cancelled orders: excluded here (status filter). Returned or partially refunded lines would need a refunds table; not in this question.
- NULL category: `COALESCE(category, 'Uncategorised')` makes it a group; leaving it NULL would still group it (GROUP BY and window PARTITION BY treat NULLs as one group) but print NULL.
- Category with fewer than two products: returns what it has (Home: one row). No padding.
- Ties: `DENSE_RANK` keeps all tied products, so the result can exceed 2 rows per category; `ROW_NUMBER` would pick one arbitrarily unless a tie-breaker is added (Part 4 Q2 and Q12).
- Products with no completed sales are absent (inner join on items); to list them with 0, start from `products` and LEFT JOIN.
- Share uses the category total before the top-2 filter, so shares of the shown rows need not add to 100.

**Then explain:**
- Grain: revenue belongs to the order line, so multiply and sum at that grain. An order-level total joined to lines is repeated once per line.
- Window functions run after GROUP BY, so aggregate to product first, then rank and take shares in the same query (ranking aggregates is Part 4 Q13).
- The rank filter has to be in an outer query or CTE because window results cannot be used in WHERE.
- Units and revenue come from the same filtered rows; do not mix completed-only revenue with all-status units.
- Dialect: Snowflake and BigQuery have `QUALIFY` to filter on the rank directly (not executed here).

**Follow-ups:**
- Top 2 per category with exactly two rows? Use `ROW_NUMBER` with a tie-breaker (`name`), and say which product is dropped.
- Net of discounts? Needs a discount column; subtract at line level.
- Share of total company revenue as well? Add a second window `SUM(revenue) OVER ()`.

**Common mistakes:**
- Joining an order total (or order amount) to each item and summing it.
- Including cancelled orders in revenue or units.
- Using `RANK` and then filtering `<= 2`, which behaves like `DENSE_RANK` only until a tie occurs before the cut (a tie at rank 1 skips rank 2).
- Dropping uncategorised products silently through an inner join on a category table.
- Taking share after the top-2 filter, so shares add to 100 by accident.

### Q30 ⭐⭐ 🟡 pandas pivot_table and crosstab for conversion by channel: orders DataFrame with columns user_id, order_id, channel (some NaN) and status, and a users DataFrame with signup channel. Produce (a) counts of orders by channel and status with pivot_table and fill_value, (b) row-normalised shares with pd.crosstab(..., normalize='index'), (c) value_counts(normalize=True) for the channel mix and say how dropna changes each of them (pivot_table and crosstab drop NaN keys by default, value_counts drops NaN unless dropna=False). Assert the shares equal a SQL GROUP BY result from sqlite3 on the same data and say which one silently loses the NaN-channel rows.
**Asked at:** pandas reference pages for pivot_table and crosstab (both opened: pivot_table dropna=True drops NaN keys and all-NaN columns, observed default True in 3.0.0; crosstab normalize accepts all/index/columns and dropna drops empty categories) plus expert gap-check on groupby, nunique and rounding behaviour; documentation, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `pivot_table` and `pd.crosstab` both drop NaN keys by default and `value_counts` drops NaN unless `dropna=False`, so a NaN channel silently disappears from all three; a SQL `GROUP BY` keeps a NULL group, which is why I fill the key (`'unknown'`) first and then assert the pandas shares equal the SQL result.

**Schema and sample data:** ten orders for five users. Three orders have a NULL channel (orders 6, 7, 8). `users.signup_channel` is complete and is used for a fallback rule at the end. Everything here is made-up toy data.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, status TEXT);
INSERT INTO users VALUES (1,'ads'),(2,'organic'),(3,'referral'),(4,'ads'),(5,'organic');
INSERT INTO orders VALUES
 (1,1,'ads','completed'),(2,1,'ads','cancelled'),(3,2,'organic','completed'),
 (4,2,'organic','completed'),(5,3,'referral','cancelled'),(6,4,NULL,'completed'),
 (7,4,NULL,'cancelled'),(8,5,NULL,'completed'),(9,3,'referral','completed'),
 (10,1,'ads','completed');
```

**SQL answer:** `SQL_COUNTS` in the Code block (NULL channel shown as 'unknown' with `COALESCE`, which turns the NULL group into a labelled row):
```sql
SELECT COALESCE(channel, 'unknown') AS channel,
       SUM(status = 'cancelled') AS cancelled,
       SUM(status = 'completed') AS completed,
       COUNT(*) AS orders,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 4) AS completed_share,
       ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM orders), 4) AS channel_mix
FROM orders
GROUP BY COALESCE(channel, 'unknown')
ORDER BY channel
```

**pandas answer:** there is no single function here; the pandas steps are printed in the Code block. The core calls are `pd.pivot_table(orders, index="channel", columns="status", values="order_id", aggfunc="count", fill_value=0)` for counts, `pd.crosstab(orders["channel_f"], orders["status"], normalize="index")` for row shares and `orders["channel"].value_counts(normalize=True, dropna=False)` for the mix, where `channel_f` is `channel.fillna("unknown")`.

**Example:** walk through the sample data by hand.
- SQL on the ten orders: ads 3 orders (2 completed, 1 cancelled), organic 2 (both completed), referral 2 (1 and 1), NULL 3 (2 completed, 1 cancelled). Completed share is 0.6667, 1.0, 0.5 and 0.6667; channel mix is 0.3, 0.2, 0.2, 0.3.
- pandas `pivot_table` default: the NaN-channel rows are gone, 7 of 10 rows are counted and there is no 'unknown' row.
- `crosstab(..., normalize='index')` default: the same three rows only; normalising by `'all'` makes the shares add to 1.0 but over the 7 kept rows, not over 10.
- `value_counts(normalize=True)` default gives ads 0.4286, organic 0.2857, referral 0.2857: shares of 7, so ads looks like 43 percent of orders instead of 30 percent. With `dropna=False` the NaN row appears with 0.3 and every share matches SQL.
- After `fillna('unknown')` the pivot, the crosstab and the mix all match SQL, which the Code block asserts (compared after sorting by channel).
- Fallback rule: filling the NaN order channel from the user's signup channel (merge, then `fillna`) leaves no NaN: ads 5, organic 3, referral 2. That is a different, defined attribution rule, not the same as 'unknown'.

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q30: pandas pivot_table, crosstab and value_counts with a NaN channel, checked against SQL GROUP BY
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, status TEXT);
INSERT INTO users VALUES (1,'ads'),(2,'organic'),(3,'referral'),(4,'ads'),(5,'organic');
INSERT INTO orders VALUES
 (1,1,'ads','completed'),(2,1,'ads','cancelled'),(3,2,'organic','completed'),
 (4,2,'organic','completed'),(5,3,'referral','cancelled'),(6,4,NULL,'completed'),
 (7,4,NULL,'cancelled'),(8,5,NULL,'completed'),(9,3,'referral','completed'),
 (10,1,'ads','completed');
"""

SQL_COUNTS = """
SELECT COALESCE(channel, 'unknown') AS channel,
       SUM(status = 'cancelled') AS cancelled,
       SUM(status = 'completed') AS completed,
       COUNT(*) AS orders,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 4) AS completed_share,
       ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM orders), 4) AS channel_mix
FROM orders
GROUP BY COALESCE(channel, 'unknown')
ORDER BY channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_COUNTS, con)
print("SQL GROUP BY (NULL channel kept as 'unknown'):")
print(sql_res.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
users = pd.read_sql_query("SELECT * FROM users", con)
print("channel dtype:", orders["channel"].dtype, "; NaN rows:", int(orders["channel"].isna().sum()))

# (a) counts: default drops NaN keys
pv = pd.pivot_table(orders, index="channel", columns="status", values="order_id",
                    aggfunc="count", fill_value=0)
print("(a) pivot_table, default dropna=True:")
print(pv)
print("    rows kept:", int(pv.to_numpy().sum()), "of", len(orders))
# the aggfunc='mean' default trap
trap = pd.pivot_table(orders, index="channel", columns="status", values="order_id")
print("(a') pivot_table with the default aggfunc='mean' on order_id (not a count):")
print(trap)
# explicit NaN bucket
orders["channel_f"] = orders["channel"].fillna("unknown")
pv_f = pd.pivot_table(orders, index="channel_f", columns="status", values="order_id",
                      aggfunc="count", fill_value=0)
print("(a'') pivot_table after fillna('unknown'):")
print(pv_f)

# (b) crosstab row shares
ct = pd.crosstab(orders["channel"], orders["status"], normalize="index")
ct_f = pd.crosstab(orders["channel_f"], orders["status"], normalize="index")
print("(b) crosstab normalize='index', NaN channel silently absent:")
print(ct.round(4))
print("(b') crosstab after fillna('unknown'):")
print(ct_f.round(4))
ct_all = pd.crosstab(orders["channel"], orders["status"], normalize="all")
print("(b'') crosstab normalize='all' sums to", round(float(ct_all.to_numpy().sum()), 4),
      "(shares of the 7 kept rows, not of 10)")

# (c) value_counts
vc = orders["channel"].value_counts(normalize=True)
vc_na = orders["channel"].value_counts(normalize=True, dropna=False)
print("(c) value_counts(normalize=True):")
print(vc.round(4).to_string())
print("(c') value_counts(normalize=True, dropna=False):")
print(vc_na.round(4).to_string())

# assertions against SQL
pd_res = pd.DataFrame({"channel": pv_f.index, "cancelled": pv_f["cancelled"].to_numpy(),
                       "completed": pv_f["completed"].to_numpy()})
pd_res["orders"] = pd_res["cancelled"] + pd_res["completed"]
pd_res["completed_share"] = ct_f.loc[pd_res["channel"], "completed"].round(4).to_numpy()
mix = orders["channel_f"].value_counts(normalize=True, dropna=False)
pd_res["channel_mix"] = mix.loc[pd_res["channel"]].round(4).to_numpy()
# compare after sorting by channel (SQL ORDER BY channel)
pd.testing.assert_frame_equal(pd_res.sort_values("channel").reset_index(drop=True), sql_res, check_dtype=False)

# crosstab or pivot on a categorical key: observed / dropna defaults
cat = orders.assign(channel_c=pd.Categorical(orders["channel_f"],
                    categories=["ads", "organic", "referral", "unknown", "affiliate"]))
print("categorical key with an unused category 'affiliate':")
print("  pivot_table default rows:", list(pd.pivot_table(cat, index="channel_c", columns="status",
      values="order_id", aggfunc="count", fill_value=0).index))
print("  pivot_table observed=False rows:", list(pd.pivot_table(cat, index="channel_c", columns="status",
      values="order_id", aggfunc="count", fill_value=0, observed=False).index))
print("  crosstab default rows:", list(pd.crosstab(cat["channel_c"], cat["status"]).index))
print("  crosstab dropna=False rows:", list(pd.crosstab(cat["channel_c"], cat["status"], dropna=False).index))

# fallback to the signup channel through a merge
m = orders.merge(users, on="user_id", how="left")
m["channel_fb"] = m["channel"].fillna(m["signup_channel"])
print("after fallback to signup channel, NaN left:", int(m["channel_fb"].isna().sum()))
print(m["channel_fb"].value_counts().to_string())
print("asserts passed")
```

**Output (my run):**
```text
SQL GROUP BY (NULL channel kept as 'unknown'):
 channel  cancelled  completed  orders  completed_share  channel_mix
     ads          1          2       3           0.6667          0.3
 organic          0          2       2           1.0000          0.2
referral          1          1       2           0.5000          0.2
 unknown          1          2       3           0.6667          0.3
channel dtype: str ; NaN rows: 3
(a) pivot_table, default dropna=True:
status    cancelled  completed
channel                       
ads               1          2
organic           0          2
referral          1          1
    rows kept: 7 of 10
(a') pivot_table with the default aggfunc='mean' on order_id (not a count):
status    cancelled  completed
channel                       
ads             2.0        5.5
organic         NaN        3.5
referral        5.0        9.0
(a'') pivot_table after fillna('unknown'):
status     cancelled  completed
channel_f                      
ads                1          2
organic            0          2
referral           1          1
unknown            1          2
(b) crosstab normalize='index', NaN channel silently absent:
status    cancelled  completed
channel                       
ads          0.3333     0.6667
organic      0.0000     1.0000
referral     0.5000     0.5000
(b') crosstab after fillna('unknown'):
status     cancelled  completed
channel_f                      
ads           0.3333     0.6667
organic       0.0000     1.0000
referral      0.5000     0.5000
unknown       0.3333     0.6667
(b'') crosstab normalize='all' sums to 1.0 (shares of the 7 kept rows, not of 10)
(c) value_counts(normalize=True):
channel
ads         0.4286
organic     0.2857
referral    0.2857
(c') value_counts(normalize=True, dropna=False):
channel
ads         0.3
NaN         0.3
organic     0.2
referral    0.2
categorical key with an unused category 'affiliate':
  pivot_table default rows: ['ads', 'organic', 'referral', 'unknown']
  pivot_table observed=False rows: ['ads', 'organic', 'referral', 'unknown', 'affiliate']
  crosstab default rows: ['ads', 'organic', 'referral', 'unknown']
  crosstab dropna=False rows: ['ads', 'organic', 'referral', 'unknown', 'affiliate']
after fallback to signup channel, NaN left: 0
channel_fb
ads         5
organic     3
referral    2
asserts passed
```

**Edge cases:**
- Default aggfunc: `pivot_table` defaults to `aggfunc='mean'`. On `order_id` it printed means such as 5.5, not counts, and an NaN cell for organic cancelled; always pass `aggfunc='count'` (non-null values) or `'size'`.
- `aggfunc='count'` counts non-null values of `values`; if the values column has NaN the counts are short. Use a never-null column such as the order id.
- Unused categories: with a categorical channel that has an unused category 'affiliate', `pivot_table` omitted it (the `observed=True` default in pandas 3.0, as run here) and `observed=False` showed it; `crosstab` omitted it by default and `dropna=False` showed it. Whether this matches older pandas versions I did not test.
- `fill_value=0` fills empty cells (organic, cancelled) but does not recreate NaN-key rows.
- Dtype: with pandas 3.0 the channel column is the string dtype and missing values are NaN; the behaviours above were run on 3.0.5.

**Then explain:**
- Which one silently loses the NaN-channel rows: all three pandas calls by default (`pivot_table`, `crosstab`, `value_counts`); SQL `GROUP BY` does not, it returns the NULL group, so SQL and pandas disagree by 3 of 10 rows until you fill or set `dropna=False`.
- `crosstab(normalize='index')` rows add to 1 over the kept rows; the dropped rows silently change the denominators of `'all'` and `'columns'` normalisation, but not of `'index'` for the channels kept.
- `value_counts(normalize=True)` divides by the non-null count by default, so shares change when NaN is dropped. This is the one that changes the mix, not only the table.
- Counts versus mean: forgetting `aggfunc` gives averages of an id column and looks like a table of numbers.
- Safer habit: make missing an explicit value (`fillna('unknown')`) before any pivot, or pass `dropna=False` where the function supports it, and assert row totals equal `len(orders)`.

**Follow-ups:**
- Does `groupby` behave the same? It also drops NaN keys unless `dropna=False` (Q31 runs it).
- How do you add row and column totals? `margins=True` on both functions; check the margin label does not clash with a real category.
- Same table in SQL with columns per status? `SUM(status = 'completed')` conditional aggregation, as in `SQL_COUNTS`; SQLite has no PIVOT.

**Common mistakes:**
- Relying on the default `aggfunc='mean'`.
- Not noticing that NaN-key rows vanished (7 of 10).
- Comparing pandas shares to SQL shares computed over a different row set.
- Using `normalize=True` on `crosstab` and reading it as row shares (it is `'all'`).
- Filling with 0 instead of a label, which merges unknown orders with a real channel called 0.

### Q31 ⭐⭐ 🟡 SQL versus pandas differences in metric code, a translation table with each row demonstrated on tiny data: nunique skips NaN while COUNT(DISTINCT) skips NULL (same) but len(set()) does not, groupby drops NaN keys while SQL GROUP BY keeps a NULL group, integer division (SQLite 3 / 2 gives 1; pandas / gives 1.5), rounding (SQLite ROUND half away from zero; Python round and numpy round half to even), division by an empty denominator (NULL or error in SQL; NaN or inf in pandas), and merge on keys with NaN. Say which rows were run.
**Asked at:** pandas reference pages for pivot_table and crosstab (both opened: pivot_table dropna=True drops NaN keys and all-NaN columns, observed default True in 3.0.0; crosstab normalize accepts all/index/columns and dropna drops empty categories) plus expert gap-check on groupby, nunique and rounding behaviour; documentation, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Most differences are NULL versus NaN handling and number types: `nunique` and `COUNT(DISTINCT)` skip missing values but `len(set(series))` does not, `groupby` drops NaN keys while `GROUP BY` keeps a NULL group, SQLite `3/2` is 1 while pandas gives 1.5, SQLite rounds halves away from zero while Python and numpy round halves to even (and numpy and Python can still disagree), SQLite returns NULL for division by zero while pandas gives inf or NaN, and pandas `merge` matches NaN keys to each other while SQL joins never match NULLs. I ran every row below.

**Schema and sample data:** a five-row table `t(id, k, u, v)` with a NULL in each of `k`, `u` and `v` (k is a, a, NULL, NULL, b; u is 10, NULL, 10, NULL, 20), and two two-row tables `l` and `r` that each have a NULL key. There is no single query and pandas function pair here; every row is a small printed demonstration, so the SQL and pandas answers are the statements in the Code block.
```sql
CREATE TABLE t(id INTEGER, k TEXT, u INTEGER, v REAL);
INSERT INTO t VALUES (1,'a',10,1.0),(2,'a',NULL,2.0),(3,NULL,10,3.0),(4,NULL,NULL,NULL),(5,'b',20,4.0);
CREATE TABLE l(k TEXT, lv INTEGER);
CREATE TABLE r(k TEXT, rv INTEGER);
INSERT INTO l VALUES ('a',1),(NULL,2);
INSERT INTO r VALUES ('a',10),(NULL,20);
```

**SQL answer:** the statements are in the Code block (for example `SELECT COUNT(DISTINCT u) FROM t`, `SELECT 3/2`, `SELECT ROUND(2.5)`, `SELECT 1/0`, `SELECT l.k, lv, rv FROM l JOIN r ON l.k = r.k`).

**pandas answer:** the pandas calls are in the Code block (`df['u'].nunique()`, `df.groupby('k')`, `pd.Series([3]) / 2`, `pd.Series(vals).round()`, `L.merge(R, on='k')`).

**Example:** walk through the sample data by hand.
Translation table, every cell from my run (SQLite 3.45.1, pandas 3.0.5, numpy 2.5.3):

| Topic | SQL (SQLite) | pandas / Python |
|---|---|---|
| Distinct count of u (10, NULL, 10, NULL, 20) | `COUNT(DISTINCT u)` = 2; `COUNT(u)` = 3; `COUNT(*)` = 5 | `nunique()` = 2; `nunique(dropna=False)` = 3; `len(set(series))` = 4 (each NaN is a separate object); `len(unique())` = 3 |
| Group on k (a, a, NULL, NULL, b) | `GROUP BY k` returns three groups: NULL 2, a 2, b 1 | `groupby('k')` gives a 2, b 1 (NaN group dropped); `dropna=False` adds NaN 2; `value_counts()` drops NaN, `dropna=False` keeps it |
| Integer division | `3/2` = 1, `-3/2` = -1 (truncates toward zero), `3/2.0` = 1.5 | `3/2` = 1.5; `3//2` = 1; `-3//2` = -2 (floors); `int(-3/2)` = -1; Series `/` and `//` match Python |
| Rounding halves | `ROUND(0.5)`, `ROUND(2.5)`, `ROUND(-2.5)` = 1.0, 3.0, -3.0 | Python `round(2.5)` = 2, `round(0.5)` = 0, `round(-2.5)` = -2; numpy and `Series.round()` the same (half to even) |
| Rounding to 2 places | `ROUND(0.125, 2)` = 0.13, `ROUND(2.675, 2)` = 2.67, `ROUND(1.005, 2)` = 1.0 | Python 0.12, 2.67, 1.0; numpy and `Series.round(2)` 0.12, **2.68**, 1.0 |
| Division by zero | `1/0`, `1.0/0`, `0.0/0` all NULL; `1/NULLIF(0,0)` NULL; `SUM` and `AVG` of no rows NULL, `COUNT` 0 | Python `1/0` raises `ZeroDivisionError`; float Series gives inf (1/0) and NaN (0/0); empty `sum()` = 0.0, `mean()` = NaN |
| Join or merge on a NULL key | `INNER JOIN` returns only the 'a' row; `LEFT JOIN` keeps the NULL row with no match; `NULL = NULL` is NULL | `merge(on='k')` **matches NaN to NaN**: the inner merge returned the NaN row with rv 20 |
| Rolling distinct | no window `COUNT(DISTINCT ...)` in SQLite (range join, Q33) | `Series.rolling(n).nunique` exists in pandas 3.0.5 (docstring says added in 3.0.0), see Q33 |

What the run showed that I did not expect:
- `len(set(series))` is 4 and not 3: a float column with two NaN values gives two separate NaN objects, and a Python set treats each NaN as different from every other. `nunique()` and `unique()` handle this properly.
- `ROUND(2.675, 2)` agrees with Python's 2.67 but numpy and pandas give 2.68, so numpy is not the same as Python's `round` either. Neither is 'wrong'; they scale and round differently on binary floats.
- `rolling().nunique` is available in pandas 3.0.5, which contradicts the Wave A premise of its absence (checked here by `hasattr` and by a real call in Q33).

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q31: SQL versus pandas differences in metric code, each row run on tiny data
import sqlite3
import warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE t(id INTEGER, k TEXT, u INTEGER, v REAL);
INSERT INTO t VALUES (1,'a',10,1.0),(2,'a',NULL,2.0),(3,NULL,10,3.0),(4,NULL,NULL,NULL),(5,'b',20,4.0);
CREATE TABLE l(k TEXT, lv INTEGER);
CREATE TABLE r(k TEXT, rv INTEGER);
INSERT INTO l VALUES ('a',1),(NULL,2);
INSERT INTO r VALUES ('a',10),(NULL,20);
""")
df = pd.read_sql_query("SELECT * FROM t", con)
print("sqlite", sqlite3.sqlite_version, "pandas", pd.__version__, "numpy", np.__version__)

def q(sql):
    return con.execute(sql).fetchall()

print("\nRow 1: distinct count with a missing user id (column u: 10, NULL, 10, NULL, 20)")
print("  SQL COUNT(DISTINCT u):", q("SELECT COUNT(DISTINCT u) FROM t")[0][0],
      "| SQL COUNT(*):", q("SELECT COUNT(*) FROM t")[0][0],
      "| SQL COUNT(u):", q("SELECT COUNT(u) FROM t")[0][0])
print("  pandas nunique():", df["u"].nunique(), "| nunique(dropna=False):", df["u"].nunique(dropna=False),
      "| len(set(series)):", len(set(df["u"])), "| len(df['u'].unique()):", len(df["u"].unique()))
print("  SQL DISTINCT rows incl NULL group:", len(q("SELECT DISTINCT u FROM t")))

print("\nRow 2: grouping on a key with a missing value (k: a, a, NULL, NULL, b)")
print("  SQL GROUP BY k:", q("SELECT k, COUNT(*) FROM t GROUP BY k ORDER BY k"))
print("  pandas groupby default:", df.groupby("k").size().to_dict())
print("  pandas groupby dropna=False:", df.groupby("k", dropna=False).size().to_dict())
print("  value_counts default:", df["k"].value_counts().to_dict(), "| dropna=False:",
      df["k"].value_counts(dropna=False).to_dict())

print("\nRow 3: integer division and sign")
print("  SQLite 3 / 2 =", q("SELECT 3/2")[0][0], "| 3 / 2.0 =", q("SELECT 3/2.0")[0][0],
      "| -3 / 2 =", q("SELECT -3/2")[0][0], "| 3 * 1.0 / 2 =", q("SELECT 3*1.0/2")[0][0])
print("  Python 3 / 2 =", 3 / 2, "| 3 // 2 =", 3 // 2, "| -3 // 2 =", -3 // 2, "| int(-3 / 2) =", int(-3 / 2))
print("  pandas Series([3]) / 2 =", float((pd.Series([3]) / 2).iloc[0]), "| // 2 =", int((pd.Series([3]) // 2).iloc[0]),
      "| Series([-3]) // 2 =", int((pd.Series([-3]) // 2).iloc[0]))

print("\nRow 4: rounding (SQLite ROUND versus Python round, numpy and pandas)")
vals = [0.5, 1.5, 2.5, -2.5]
print("  SQLite ROUND(x):", [q(f"SELECT ROUND({x})")[0][0] for x in vals])
print("  Python round(x):", [round(x) for x in vals])
print("  numpy np.round(x):", [float(np.round(x)) for x in vals])
print("  pandas Series.round():", pd.Series(vals).round().tolist())
two = [0.125, 0.375, 2.675, 1.005]
print("  to 2 places:", two)
print("  SQLite ROUND(x, 2):", [q(f"SELECT ROUND({x}, 2)")[0][0] for x in two])
print("  Python round(x, 2):", [round(x, 2) for x in two])
print("  numpy np.round(x, 2):", [float(np.round(x, 2)) for x in two])
print("  pandas Series.round(2):", pd.Series(two).round(2).tolist())

print("\nRow 5: division by an empty or zero denominator")
print("  SQLite 1 / 0 =", q("SELECT 1/0")[0][0], "| 1.0 / 0 =", q("SELECT 1.0/0")[0][0],
      "| 0.0 / 0 =", q("SELECT 0.0/0")[0][0], "| 1 / NULLIF(0, 0) =", q("SELECT 1/NULLIF(0,0)")[0][0])
print("  SQLite SUM over zero rows:", q("SELECT SUM(v) FROM t WHERE id > 99")[0][0],
      "| COUNT over zero rows:", q("SELECT COUNT(*) FROM t WHERE id > 99")[0][0],
      "| AVG over zero rows:", q("SELECT AVG(v) FROM t WHERE id > 99")[0][0])
s = pd.Series([1.0, 0.0, 5.0]); z = pd.Series([0.0, 0.0, 5.0])
print("  pandas float Series 1/0, 0/0, 5/5:", (s / z).tolist())
print("  pandas int Series [1, 0] / [0, 0]:", (pd.Series([1, 0]) / pd.Series([0, 0])).tolist())
try:
    1 / 0
except ZeroDivisionError as e:
    print("  Python 1 / 0 raises ZeroDivisionError:", e)
empty = df[df["id"] > 99]
print("  pandas sum of empty:", empty["v"].sum(), "| mean of empty:", empty["v"].mean(), "| count:", int(empty["v"].count()))

print("\nRow 6: merge / join on keys that contain a missing value")
print("  SQL INNER JOIN on k:", q("SELECT l.k, lv, rv FROM l JOIN r ON l.k = r.k"))
print("  SQL LEFT JOIN on k:", q("SELECT l.k, lv, rv FROM l LEFT JOIN r ON l.k = r.k ORDER BY lv"))
L = pd.read_sql_query("SELECT * FROM l", con); R = pd.read_sql_query("SELECT * FROM r", con)
print("  pandas merge inner on k:")
print(L.merge(R, on="k").to_string(index=False))
print("  SQL NULL = NULL:", q("SELECT NULL = NULL")[0][0], "| NULL IS NULL:", q("SELECT NULL IS NULL")[0][0])

print("\nRow 7: rolling().nunique")
print("  hasattr(Series.rolling(2), 'nunique'):", hasattr(pd.Series([1, 2]).rolling(2), "nunique"))
print("  hasattr(Series.rolling(2), 'count'):", hasattr(pd.Series([1, 2]).rolling(2), "count"))

# assertions behind the table
assert q("SELECT COUNT(DISTINCT u) FROM t")[0][0] == df["u"].nunique() == 2
assert q("SELECT 3/2")[0][0] == 1 and 3 / 2 == 1.5
assert q("SELECT ROUND(2.5)")[0][0] == 3.0 and round(2.5) == 2
print("\nasserts passed")
```

**Output (my run):**
```text
sqlite 3.45.1 pandas 3.0.5 numpy 2.5.3

Row 1: distinct count with a missing user id (column u: 10, NULL, 10, NULL, 20)
  SQL COUNT(DISTINCT u): 2 | SQL COUNT(*): 5 | SQL COUNT(u): 3
  pandas nunique(): 2 | nunique(dropna=False): 3 | len(set(series)): 4 | len(df['u'].unique()): 3
  SQL DISTINCT rows incl NULL group: 3

Row 2: grouping on a key with a missing value (k: a, a, NULL, NULL, b)
  SQL GROUP BY k: [(None, 2), ('a', 2), ('b', 1)]
  pandas groupby default: {'a': 2, 'b': 1}
  pandas groupby dropna=False: {'a': 2, 'b': 1, nan: 2}
  value_counts default: {'a': 2, 'b': 1} | dropna=False: {'a': 2, nan: 2, 'b': 1}

Row 3: integer division and sign
  SQLite 3 / 2 = 1 | 3 / 2.0 = 1.5 | -3 / 2 = -1 | 3 * 1.0 / 2 = 1.5
  Python 3 / 2 = 1.5 | 3 // 2 = 1 | -3 // 2 = -2 | int(-3 / 2) = -1
  pandas Series([3]) / 2 = 1.5 | // 2 = 1 | Series([-3]) // 2 = -2

Row 4: rounding (SQLite ROUND versus Python round, numpy and pandas)
  SQLite ROUND(x): [1.0, 2.0, 3.0, -3.0]
  Python round(x): [0, 2, 2, -2]
  numpy np.round(x): [0.0, 2.0, 2.0, -2.0]
  pandas Series.round(): [0.0, 2.0, 2.0, -2.0]
  to 2 places: [0.125, 0.375, 2.675, 1.005]
  SQLite ROUND(x, 2): [0.13, 0.38, 2.67, 1.0]
  Python round(x, 2): [0.12, 0.38, 2.67, 1.0]
  numpy np.round(x, 2): [0.12, 0.38, 2.68, 1.0]
  pandas Series.round(2): [0.12, 0.38, 2.68, 1.0]

Row 5: division by an empty or zero denominator
  SQLite 1 / 0 = None | 1.0 / 0 = None | 0.0 / 0 = None | 1 / NULLIF(0, 0) = None
  SQLite SUM over zero rows: None | COUNT over zero rows: 0 | AVG over zero rows: None
  pandas float Series 1/0, 0/0, 5/5: [inf, nan, 1.0]
  pandas int Series [1, 0] / [0, 0]: [inf, nan]
  Python 1 / 0 raises ZeroDivisionError: division by zero
  pandas sum of empty: 0.0 | mean of empty: nan | count: 0

Row 6: merge / join on keys that contain a missing value
  SQL INNER JOIN on k: [('a', 1, 10)]
  SQL LEFT JOIN on k: [('a', 1, 10), (None, 2, None)]
  pandas merge inner on k:
  k  lv  rv
  a   1  10
NaN   2  20
  SQL NULL = NULL: None | NULL IS NULL: 1

Row 7: rolling().nunique
  hasattr(Series.rolling(2), 'nunique'): True
  hasattr(Series.rolling(2), 'count'): True

asserts passed
```

**Edge cases:**
- `COUNT(DISTINCT col)`, `AVG(col)`, `SUM(col)` ignore NULL; `COUNT(*)` does not. pandas `size()` counts rows, `count()` counts non-null, like `COUNT(*)` and `COUNT(col)`.
- `SELECT DISTINCT u` returns the NULL as one distinct row (3 rows) while `COUNT(DISTINCT u)` gives 2: the two differ on NULL by design.
- Rounding a percentage like 12.5 percent to a whole number gives 13 in SQLite and 12 in pandas; in a reconciliation this shows as a one-unit mismatch that is not a data bug.
- A pandas integer Series divided by a zero Series gave inf and NaN in my run (no exception); Python integers raise.
- Other engines: PostgreSQL integer division also truncates and division by zero raises an error; MySQL `/` returns a decimal and `DIV` is integer division; BigQuery `/` returns a float and `SAFE_DIVIDE` returns NULL on zero (all from memory, not executed here).

**Then explain:**
- Rule of thumb: SQL treats NULL as unknown (never equal to anything, including NULL), pandas treats NaN as a value that most aggregations skip but that `merge`, `set` and sorting treat in their own way.
- For metric code, make the rule explicit: fill or filter missing keys before grouping, `dropna=False` where a NaN group matters, `* 1.0` or `/` for ratios, and one agreed rounding helper.
- If a pandas result must equal SQL to the cent, do not rely on `round`; round once at the end the same way (half away from zero needs a helper) or compare with a tolerance.
- Rows were run in the Code block; the three asserts at the bottom pin the claims 'COUNT(DISTINCT) equals nunique', '3/2 is 1 versus 1.5' and 'ROUND(2.5) is 3.0 versus Python 2'.

**Follow-ups:**
- How do you make pandas merge behave like SQL on NaN keys? Drop or mask the NaN-key rows before the merge (`dropna(subset=['k'])`); then an inner merge matches SQL.
- How do you round half away from zero in pandas? Use `np.sign(x) * np.floor(np.abs(x) * 100 + 0.5) / 100`, accepting binary float effects; I did not run this helper here.
- Why did the NULL group show in SQL but not in pandas by default? Different design: SQL groups NULLs together, pandas drops them unless `dropna=False`.

**Common mistakes:**
- Assuming `groupby` totals add to the table total when the key has NaN.
- Using `len(set(...))` on a float column for distinct users.
- Expecting `/` to be integer division in SQLite or float division in older engines without checking.
- Rounding in pandas and SQL separately and then 'finding a bug' of 0.01.
- Merging on a key with NaN and getting extra rows that SQL would not return.

### Q32 ⭐⭐ 🟡 Sample ratio mismatch (SRM) check as counts: experiments(user_id, arm, assigned_ts) with a planned 50/50 split, and some users assigned in both arms or twice. Return per arm distinct users, the observed share, the expected count, the difference, and the chi-square statistic computed in plain arithmetic in the query (the p-value and threshold choice belong to Book 1 and Book 6; state a typical strict threshold only as a pointer). Explain the counting unit (distinct users, not rows), how users in both arms are found and reported, and why an SRM invalidates the conversion table from the earlier experiment question.
**Asked at:** experiment-metrics guides (PracHub and Statsig SRM pages and abtestly docs, search snippets only, not opened; SRM is a chi-square goodness-of-fit on distinct-user counts against the planned split, strict thresholds such as p < 0.001 in practice); the statistics belong to Book 1 and Book 6 and this question stays on counts, rates and uplift in SQL; guides, not candidate reports; experimentation and data scientist rounds
**Say this first (1 line):** Count distinct users per arm (not rows), compare each count with the planned share times the total, and the chi-square statistic is the sum of (observed - expected)^2 / expected over the arms, computed in plain arithmetic in the query; users assigned to both arms are found with `HAVING COUNT(DISTINCT arm) > 1` and reported separately, and the p-value and the strictness of the threshold are left to Books 1 and 6 (teams commonly use strict thresholds such as p < 0.001 for SRM, which varies by team and is only a pointer here).

**Schema and sample data:** seventeen assignment rows, fourteen distinct users. User 2 is assigned to control twice, user 11 to treatment twice, and user 14 appears in both arms. The planned split is 50/50. A second, generated table of 10,000 control and 10,600 treatment users is used in the Code block for the arithmetic at scale.
```sql
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 09:00:00'),(2,'control','2024-03-01 09:01:00'),(2,'control','2024-03-02 09:00:00'),
 (3,'control','2024-03-01 09:02:00'),(4,'control','2024-03-01 09:03:00'),(5,'control','2024-03-01 09:04:00'),
 (6,'control','2024-03-01 09:05:00'),(7,'control','2024-03-01 09:06:00'),(8,'control','2024-03-01 09:07:00'),
 (9,'control','2024-03-01 09:08:00'),
 (10,'treatment','2024-03-01 09:09:00'),(11,'treatment','2024-03-01 09:10:00'),(11,'treatment','2024-03-03 09:00:00'),
 (12,'treatment','2024-03-01 09:11:00'),(13,'treatment','2024-03-01 09:12:00'),
 (14,'control','2024-03-01 09:13:00'),(14,'treatment','2024-03-02 09:13:00');
```

**SQL answer:** `SQL_MAIN` in the Code block (the planned split is a small `plan` table so it can change; `SQL_BOTH`, `SQL_ROWS`, `SQL_DUP` and `SQL_CLEAN` are the supporting queries):
```sql
WITH plan(arm, planned) AS (VALUES ('control', 0.5), ('treatment', 0.5)),
obs AS (
  SELECT arm, COUNT(DISTINCT user_id) AS users FROM experiments GROUP BY arm
), tot AS (SELECT SUM(users) AS n FROM obs),
x AS (
  SELECT p.arm, o.users, o.users * 1.0 / t.n AS observed_share, p.planned * t.n AS expected,
         o.users - p.planned * t.n AS diff,
         (o.users - p.planned * t.n) * (o.users - p.planned * t.n) / (p.planned * t.n) AS chi_part
  FROM plan p JOIN obs o ON o.arm = p.arm CROSS JOIN tot t
)
SELECT arm, users, ROUND(observed_share, 4) AS observed_share, expected, diff,
       ROUND(chi_part, 4) AS chi_part, ROUND((SELECT SUM(chi_part) FROM x), 4) AS chi_square
FROM x ORDER BY arm
```
```sql
SELECT user_id, COUNT(DISTINCT arm) AS arms, COUNT(*) AS rows_
FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1
```

**pandas answer:** the same logic as a function, identical to the Code block (`clean=True` removes users in both arms first):
```py
def srm_counts(exp, planned={"control": 0.5, "treatment": 0.5}, clean=False):
    e = exp
    if clean:
        arms_per_user = e.groupby("user_id")["arm"].nunique()
        e = e[~e["user_id"].isin(arms_per_user[arms_per_user > 1].index)]
    obs = e.groupby("arm")["user_id"].nunique().rename("users").reset_index()
    n = obs["users"].sum()
    obs["planned"] = obs["arm"].map(planned)
    obs["observed_share"] = (obs["users"] / n).round(4)
    obs["expected"] = obs["planned"] * n
    obs["diff"] = obs["users"] - obs["expected"]
    chi_part = obs["diff"] ** 2 / obs["expected"]
    obs["chi_part"] = chi_part.round(4)
    obs["chi_square"] = round(float(chi_part.sum()), 4)
    return obs[["arm", "users", "observed_share", "expected", "diff", "chi_part", "chi_square"]]
```

**Example:** walk through the sample data by hand.
- Rows: control has 11 rows (users 1 to 9 with user 2 twice, plus user 14), treatment has 6 rows (users 10 to 13 with user 11 twice, plus user 14). Distinct users: control 10, treatment 5 (user 14 is in both). The row count of 17 against 14 distinct users shows three users with repeated rows (2, 11, 14).
- Per arm, counting user 14 in each arm: total 15, expected 7.5 each, observed shares 0.6667 and 0.3333, difference +2.5 and -2.5, chi parts 2.5^2/7.5 = 0.8333 each, chi-square 1.6667.
- Counting rows instead (wrong unit): 11 and 6, total 17, expected 8.5, chi-square 1.4706. The statistic changes because duplicates changed both the counts and the total.
- Removing the one user in both arms: 9 versus 4, total 13, expected 6.5, chi-square 1.9231.
- At scale (generated): 10,000 versus 10,600, total 20,600, expected 10,300, difference -300 and +300, chi parts 8.7379 each, chi-square 17.4757. Comparing that statistic with a threshold is out of scope here (Book 1 and Book 6).

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q32: sample ratio mismatch as counts: distinct users per arm, expected, difference, chi-square arithmetic
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 09:00:00'),(2,'control','2024-03-01 09:01:00'),(2,'control','2024-03-02 09:00:00'),
 (3,'control','2024-03-01 09:02:00'),(4,'control','2024-03-01 09:03:00'),(5,'control','2024-03-01 09:04:00'),
 (6,'control','2024-03-01 09:05:00'),(7,'control','2024-03-01 09:06:00'),(8,'control','2024-03-01 09:07:00'),
 (9,'control','2024-03-01 09:08:00'),
 (10,'treatment','2024-03-01 09:09:00'),(11,'treatment','2024-03-01 09:10:00'),(11,'treatment','2024-03-03 09:00:00'),
 (12,'treatment','2024-03-01 09:11:00'),(13,'treatment','2024-03-01 09:12:00'),
 (14,'control','2024-03-01 09:13:00'),(14,'treatment','2024-03-02 09:13:00');
"""

# planned split is a parameter table; chi-square = sum over arms of (observed - expected)^2 / expected
SQL_MAIN = """
WITH plan(arm, planned) AS (VALUES ('control', 0.5), ('treatment', 0.5)),
obs AS (
  SELECT arm, COUNT(DISTINCT user_id) AS users FROM experiments GROUP BY arm
), tot AS (SELECT SUM(users) AS n FROM obs),
x AS (
  SELECT p.arm, o.users, o.users * 1.0 / t.n AS observed_share, p.planned * t.n AS expected,
         o.users - p.planned * t.n AS diff,
         (o.users - p.planned * t.n) * (o.users - p.planned * t.n) / (p.planned * t.n) AS chi_part
  FROM plan p JOIN obs o ON o.arm = p.arm CROSS JOIN tot t
)
SELECT arm, users, ROUND(observed_share, 4) AS observed_share, expected, diff,
       ROUND(chi_part, 4) AS chi_part, ROUND((SELECT SUM(chi_part) FROM x), 4) AS chi_square
FROM x ORDER BY arm
"""
# the same arithmetic on rows, to show the wrong counting unit
SQL_ROWS = SQL_MAIN.replace("COUNT(DISTINCT user_id)", "COUNT(*)")
assert SQL_ROWS != SQL_MAIN
SQL_BOTH = """
SELECT user_id, COUNT(DISTINCT arm) AS arms, COUNT(*) AS rows_
FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1
"""
SQL_DUP = """
SELECT COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS distinct_users,
       (SELECT COUNT(*) FROM (SELECT user_id FROM experiments GROUP BY user_id HAVING COUNT(*) > 1)) AS users_with_repeat_rows
FROM experiments
"""
# clean: users that appear in exactly one arm
SQL_CLEAN = SQL_MAIN.replace("FROM experiments GROUP BY arm",
    "FROM experiments WHERE user_id NOT IN (SELECT user_id FROM experiments GROUP BY user_id HAVING COUNT(DISTINCT arm) > 1) GROUP BY arm")
assert SQL_CLEAN != SQL_MAIN

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, distinct users per arm (users in both arms counted in each arm):")
print(sql_main.to_string(index=False))
print("SQL, same arithmetic on rows (wrong unit):")
print(pd.read_sql_query(SQL_ROWS, con).to_string(index=False))
print("SQL, after removing users that appear in both arms:")
sql_clean = pd.read_sql_query(SQL_CLEAN, con)
print(sql_clean.to_string(index=False))
print("users in both arms:")
print(pd.read_sql_query(SQL_BOTH, con).to_string(index=False))
print("row versus distinct counts:")
print(pd.read_sql_query(SQL_DUP, con).to_string(index=False))

exp = pd.read_sql_query("SELECT * FROM experiments", con)

# pd:main
def srm_counts(exp, planned={"control": 0.5, "treatment": 0.5}, clean=False):
    e = exp
    if clean:
        arms_per_user = e.groupby("user_id")["arm"].nunique()
        e = e[~e["user_id"].isin(arms_per_user[arms_per_user > 1].index)]
    obs = e.groupby("arm")["user_id"].nunique().rename("users").reset_index()
    n = obs["users"].sum()
    obs["planned"] = obs["arm"].map(planned)
    obs["observed_share"] = (obs["users"] / n).round(4)
    obs["expected"] = obs["planned"] * n
    obs["diff"] = obs["users"] - obs["expected"]
    chi_part = obs["diff"] ** 2 / obs["expected"]
    obs["chi_part"] = chi_part.round(4)
    obs["chi_square"] = round(float(chi_part.sum()), 4)
    return obs[["arm", "users", "observed_share", "expected", "diff", "chi_part", "chi_square"]]
# pd:end

pd_main = srm_counts(exp)
pd_clean = srm_counts(exp, clean=True)
# compare after sorting by arm (SQL ORDER BY arm)
pd.testing.assert_frame_equal(pd_main.sort_values("arm").reset_index(drop=True), sql_main, check_dtype=False)
pd.testing.assert_frame_equal(pd_clean.sort_values("arm").reset_index(drop=True), sql_clean, check_dtype=False)

# the same query on a generated table: 10,000 control and 10,600 treatment users (arithmetic at scale)
con.execute("DELETE FROM experiments")
con.executemany("INSERT INTO experiments VALUES (?, ?, '2024-03-01 00:00:00')",
                [(i, "control") for i in range(1, 10001)] + [(i, "treatment") for i in range(10001, 20601)])
big = pd.read_sql_query(SQL_MAIN, con)
print("generated 10,000 vs 10,600 users:")
print(big.to_string(index=False))
pd.testing.assert_frame_equal(srm_counts(pd.read_sql_query("SELECT * FROM experiments", con))
                              .sort_values("arm").reset_index(drop=True), big, check_dtype=False)
print("asserts passed")
```

**Output (my run):**
```text
SQL, distinct users per arm (users in both arms counted in each arm):
      arm  users  observed_share  expected  diff  chi_part  chi_square
  control     10          0.6667       7.5   2.5    0.8333      1.6667
treatment      5          0.3333       7.5  -2.5    0.8333      1.6667
SQL, same arithmetic on rows (wrong unit):
      arm  users  observed_share  expected  diff  chi_part  chi_square
  control     11          0.6471       8.5   2.5    0.7353      1.4706
treatment      6          0.3529       8.5  -2.5    0.7353      1.4706
SQL, after removing users that appear in both arms:
      arm  users  observed_share  expected  diff  chi_part  chi_square
  control      9          0.6923       6.5   2.5    0.9615      1.9231
treatment      4          0.3077       6.5  -2.5    0.9615      1.9231
users in both arms:
 user_id  arms  rows_
      14     2      2
row versus distinct counts:
 rows_  distinct_users  users_with_repeat_rows
    17              14                       3
generated 10,000 vs 10,600 users:
      arm  users  observed_share  expected   diff  chi_part  chi_square
  control  10000          0.4854   10300.0 -300.0    8.7379     17.4757
treatment  10600          0.5146   10300.0  300.0    8.7379     17.4757
asserts passed
```

**Edge cases:**
- Users in both arms: reported by `SQL_BOTH` (user 14). Whether to count them in each arm, drop them, or keep their first assignment is a decision; the raw and clean versions are both printed.
- Repeat rows for the same user and arm (users 2 and 11) inflate row counts but not distinct counts, which is why distinct users are the unit.
- An arm with zero users would make `plan` and `obs` not join; use a LEFT JOIN from `plan` if an arm can be missing.
- Expected counts below about 5 make a chi-square approximation unreliable (rule of thumb from statistics, not checked here); the toy data is only for arithmetic.
- Assignment time: late assignment or filtering on users who reached a page can itself cause an imbalance; this query only counts.

**Then explain:**
- Counting unit: distinct users, because the randomisation unit is the user. Rows include retries and re-assignments.
- Expected count is the planned share times the total distinct users, not the planned share times the larger arm.
- The chi-square statistic here is just arithmetic on counts; turning it into a p-value (1 degree of freedom for two arms) and choosing a threshold belongs to Books 1 and 6, and thresholds differ between vendors and teams.
- Why an SRM invalidates the conversion table from Q13: if assignment counts are off from the plan, something other than the treatment (a bug, a filter, a redirect) decided who ended up in each arm, so the two arms are no longer comparable populations and uplift in the Q13 table could come from that, not from the treatment. Fix the cause before reading any metric (contamination handling is Q44).
- Dialect: the `VALUES` plan table works in SQLite and Postgres; in BigQuery or Snowflake use a CTE with `SELECT ... UNION ALL` (not executed here).

**Follow-ups:**
- Three arms? Add a row to `plan`; the chi-square sum is unchanged (degrees of freedom change, a Book 1 point).
- Check SRM per day or per segment? Group the observed CTE by day or segment, and compare each to its own total.
- What do you do when SRM is flagged? Stop reading results, find the cause, rerun or exclude the affected segment.

**Common mistakes:**
- Counting rows instead of distinct users.
- Computing expected counts from the larger arm.
- Ignoring users in both arms.
- Reading a small chi-square as proof of no problem on tiny samples.
- Computing the p-value here and skipping the cause analysis.

### Q33 ⭐⭐ 🔴 Rolling 30-day active users per day with a date spine: events(user_id, event_ts, event_name). For every day from 2024-03-01 to 2024-03-31 return the DAU and the rolling MAU (distinct users active in the 30 days ending that day, inclusive), using a date spine (recursive CTE or a calendar table) and a range join on e.event_date between spine_date minus 29 days and spine_date. Return stickiness per day. Explain why ROWS BETWEEN 29 PRECEDING over daily counts is wrong (distinct users cannot be summed across days), why days with no events need the spine, and the cost of the range join on a large table (hedge: not executed beyond SQLite).
**Asked at:** active-user guides: Basedash DAU/WAU/MAU pitfalls article (opened; active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users) plus search snippets of oneuptime ClickHouse DAU/WAU/MAU and stickiness posts and Swace and pmtoolkit pages (not opened); guides, not candidate reports; product analytics and data scientist rounds at social, streaming and SaaS companies
**Say this first (1 line):** Build a 31-row date spine with a recursive CTE, reduce events to distinct (user, date) rows, range-join each spine day to the user-days in `[day - 29, day]`, and take `COUNT(DISTINCT user_id)` for the rolling MAU and the distinct users on the day itself for DAU; stickiness is DAU over rolling MAU per day, and `ROWS BETWEEN 29 PRECEDING` over daily counts is wrong because a user active on five days would be counted five times.

**Schema and sample data:** fourteen events from 2024-01-31 to 2024-03-31 for five users. Conventions: the timestamps are UTC text, the day is the UTC date, and no test-user or bot table exists in this question so none is filtered (a real report would join `users` and filter, as in Q1). Events before March matter because the 30-day window reaches into February (2024 is a leap year). User 4's January 31 event is just outside the window of 2024-03-01; user 3's February 1 event is just inside. User 1 has two events on 2024-03-02, so one user-day.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 4,'2024-01-31 10:00:00','open'),
 (2, 3,'2024-02-01 23:30:00','open'),
 (3, 1,'2024-02-05 09:00:00','open'),
 (4, 2,'2024-02-20 09:00:00','open'),
 (5, 1,'2024-03-01 08:00:00','open'),
 (6, 1,'2024-03-02 08:00:00','open'),
 (7, 1,'2024-03-02 21:00:00','click'),
 (8, 2,'2024-03-02 12:00:00','open'),
 (9, 1,'2024-03-03 08:00:00','open'),
 (10,5,'2024-03-05 08:00:00','open'),
 (11,3,'2024-03-15 08:00:00','open'),
 (12,4,'2024-03-20 08:00:00','open'),
 (13,1,'2024-03-31 08:00:00','open'),
 (14,2,'2024-03-31 09:00:00','open');
```

**SQL answer:** `SQL_MAIN` in the Code block (`SQL_WRONG` is the window-frame version, printed for comparison):
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), ud AS (
  SELECT DISTINCT user_id, date(event_ts) AS event_date FROM events
)
SELECT s.d AS day,
       COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) AS dau,
       COUNT(DISTINCT ud.user_id) AS rolling_mau,
       ROUND(COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) * 1.0 /
             NULLIF(COUNT(DISTINCT ud.user_id), 0), 4) AS stickiness
FROM spine s
LEFT JOIN ud ON ud.event_date BETWEEN date(s.d, '-29 days') AND s.d
GROUP BY s.d
ORDER BY s.d
```

**pandas answer:** the same logic as a function, identical to the Code block (cross merge of the spine with user-days, then filter to the window, then `nunique`):
```py
def rolling_active(events, start="2024-03-01", end="2024-03-31", window=30):
    ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
                [["user_id", "event_date"]].drop_duplicates())
    spine = pd.DataFrame({"day": pd.date_range(start, end)})
    m = spine.merge(ud, how="cross")
    lo = m["day"] - pd.Timedelta(days=window - 1)
    m = m[(m["event_date"] >= lo) & (m["event_date"] <= m["day"])]
    out = pd.DataFrame({
        "dau": m[m["event_date"] == m["day"]].groupby("day")["user_id"].nunique(),
        "rolling_mau": m.groupby("day")["user_id"].nunique()}).reindex(spine["day"]).fillna(0).astype(int)
    out["stickiness"] = (out["dau"] / out["rolling_mau"].where(out["rolling_mau"] != 0)).round(4)
    out = out.reset_index()
    out["day"] = out["day"].dt.strftime("%Y-%m-%d")
    return out
```

**Example:** walk through the sample data by hand.
- 2024-03-01: window is 2024-02-01 to 2024-03-01 (30 days: 29 in February because of the leap year, plus 1 March). Active users in it: user 3 (Feb 1, the first day of the window), user 2 (Feb 20), user 1 (Feb 5 and Mar 1). User 4 (Jan 31) is out. Rolling MAU = 3, DAU = 1 (user 1), stickiness 1/3 = 0.3333.
- 2024-03-02: window 2024-02-02 to 2024-03-02. User 3's last event (Feb 1) has dropped out, so users 1 and 2: MAU 2. DAU is 2 (user 1 twice on that day is one, plus user 2), stickiness 1.0.
- 2024-03-04: no events, DAU 0, but the rolling MAU is still 2 (users 1 and 2 are in the window). Without the spine this day would not exist; with it the row shows stickiness 0.0.
- 2024-03-15: user 3 returns; window is Feb 15 to Mar 15 so users 1, 2, 3, 5 give MAU 4, DAU 1, stickiness 0.25. 2024-03-31: window Mar 2 to Mar 31: users 1, 2, 3, 4, 5 are all in, MAU 5, DAU 2 (users 1 and 2), stickiness 0.4.
- Window-frame version: on 2024-03-31 summing daily DAU over 30 rows gives 8, not 5, because users 1 and 2 are counted on several days; on 2024-03-02 it gives 3 against a true 2. (That version also only sees March because the spine starts on March 1, a second flaw.)

**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.
```python
# Q33: rolling 30-day active users per day with a recursive-CTE date spine and a range join
import sqlite3
import pandas as pd

# Conventions: timestamps are UTC text, the day is the UTC date, no test-user table exists here so none is filtered.
SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 4,'2024-01-31 10:00:00','open'),
 (2, 3,'2024-02-01 23:30:00','open'),
 (3, 1,'2024-02-05 09:00:00','open'),
 (4, 2,'2024-02-20 09:00:00','open'),
 (5, 1,'2024-03-01 08:00:00','open'),
 (6, 1,'2024-03-02 08:00:00','open'),
 (7, 1,'2024-03-02 21:00:00','click'),
 (8, 2,'2024-03-02 12:00:00','open'),
 (9, 1,'2024-03-03 08:00:00','open'),
 (10,5,'2024-03-05 08:00:00','open'),
 (11,3,'2024-03-15 08:00:00','open'),
 (12,4,'2024-03-20 08:00:00','open'),
 (13,1,'2024-03-31 08:00:00','open'),
 (14,2,'2024-03-31 09:00:00','open');
"""

SQL_MAIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), ud AS (
  SELECT DISTINCT user_id, date(event_ts) AS event_date FROM events
)
SELECT s.d AS day,
       COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) AS dau,
       COUNT(DISTINCT ud.user_id) AS rolling_mau,
       ROUND(COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) * 1.0 /
             NULLIF(COUNT(DISTINCT ud.user_id), 0), 4) AS stickiness
FROM spine s
LEFT JOIN ud ON ud.event_date BETWEEN date(s.d, '-29 days') AND s.d
GROUP BY s.d
ORDER BY s.d
"""
# wrong: sum the daily distinct counts over 30 rows
SQL_WRONG = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), daily AS (
  SELECT date(event_ts) AS d, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY date(event_ts)
)
SELECT s.d AS day, COALESCE(daily.dau, 0) AS dau,
       SUM(COALESCE(daily.dau, 0)) OVER (ORDER BY s.d ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS wrong_sum_of_daus
FROM spine s LEFT JOIN daily ON daily.d = s.d
ORDER BY s.d
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, 31 spine days (first 5 and every day with activity shown below):")
print(sql_main.head(5).to_string(index=False))
print(sql_main[sql_main["dau"] > 0].to_string(index=False))
print("rows returned:", len(sql_main), "; days with rolling_mau = 0:", int((sql_main["rolling_mau"] == 0).sum()))
wrong = pd.read_sql_query(SQL_WRONG, con)
cmp = wrong.merge(sql_main[["day", "rolling_mau"]], on="day")
print("wrong sum of DAUs versus distinct rolling MAU on selected days:")
print(cmp[cmp["day"].isin(["2024-03-02", "2024-03-03", "2024-03-31"])].to_string(index=False))

# date arithmetic: datetime/date modifiers versus unixepoch, across the leap day
chk = con.execute("SELECT date('2024-03-01','-29 days'), date(unixepoch('2024-03-01') - 29*86400,'unixepoch'), "
                  "datetime('2024-03-08 10:00:00','+7 days'), datetime(unixepoch('2024-03-08 10:00:00') + 7*86400,'unixepoch')").fetchone()
print("date arithmetic check:", chk)
assert chk[0] == chk[1] and chk[2] == chk[3]

events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def rolling_active(events, start="2024-03-01", end="2024-03-31", window=30):
    ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
                [["user_id", "event_date"]].drop_duplicates())
    spine = pd.DataFrame({"day": pd.date_range(start, end)})
    m = spine.merge(ud, how="cross")
    lo = m["day"] - pd.Timedelta(days=window - 1)
    m = m[(m["event_date"] >= lo) & (m["event_date"] <= m["day"])]
    out = pd.DataFrame({
        "dau": m[m["event_date"] == m["day"]].groupby("day")["user_id"].nunique(),
        "rolling_mau": m.groupby("day")["user_id"].nunique()}).reindex(spine["day"]).fillna(0).astype(int)
    out["stickiness"] = (out["dau"] / out["rolling_mau"].where(out["rolling_mau"] != 0)).round(4)
    out = out.reset_index()
    out["day"] = out["day"].dt.strftime("%Y-%m-%d")
    return out
# pd:end

pd_res = rolling_active(events)
# compare in day order (SQL ORDER BY day); NaN stickiness equals NULL
pd.testing.assert_frame_equal(pd_res, sql_main, check_dtype=False)

# pandas 3.0 has Rolling.nunique: cross-check on days that have a row, using a time-based 30D window
ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
            [["user_id", "event_date"]].drop_duplicates().sort_values("event_date").set_index("event_date"))
rn = ud["user_id"].astype(float).rolling("30D").nunique()
last = rn.groupby(level=0).last()
chk_days = last.loc["2024-03-01":"2024-03-31"]
cmp2 = sql_main.set_index(pd.to_datetime(sql_main["day"])).loc[chk_days.index, "rolling_mau"]
assert (chk_days.astype(int).to_numpy() == cmp2.to_numpy()).all()
print("Rolling('30D').nunique matches rolling_mau on the", len(chk_days), "days that have event rows; spine days without events:",
      31 - len(chk_days))

# SQLite plan for the range join (no index): shows a scan, hedged for other engines
plan = con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN).fetchall()
print("EXPLAIN QUERY PLAN rows:", [p[3] for p in plan])
print("asserts passed")
```

**Output (my run):**
```text
SQL, 31 spine days (first 5 and every day with activity shown below):
       day  dau  rolling_mau  stickiness
2024-03-01    1            3      0.3333
2024-03-02    2            2      1.0000
2024-03-03    1            2      0.5000
2024-03-04    0            2      0.0000
2024-03-05    1            3      0.3333
       day  dau  rolling_mau  stickiness
2024-03-01    1            3      0.3333
2024-03-02    2            2      1.0000
2024-03-03    1            2      0.5000
2024-03-05    1            3      0.3333
2024-03-15    1            4      0.2500
2024-03-20    1            5      0.2000
2024-03-31    2            5      0.4000
rows returned: 31 ; days with rolling_mau = 0: 0
wrong sum of DAUs versus distinct rolling MAU on selected days:
       day  dau  wrong_sum_of_daus  rolling_mau
2024-03-02    2                  3            2
2024-03-03    1                  4            2
2024-03-31    2                  8            5
date arithmetic check: ('2024-02-01', '2024-02-01', '2024-03-15 10:00:00', '2024-03-15 10:00:00')
Rolling('30D').nunique matches rolling_mau on the 7 days that have event rows; spine days without events: 24
EXPLAIN QUERY PLAN rows: ['CO-ROUTINE spine', 'SETUP', 'SCAN CONSTANT ROW', 'RECURSIVE STEP', 'SCAN spine', 'MATERIALIZE ud', 'SCAN events', 'USE TEMP B-TREE FOR DISTINCT', 'SCAN s', 'SCAN ud LEFT-JOIN', 'USE TEMP B-TREE FOR GROUP BY', 'USE TEMP B-TREE FOR count(DISTINCT)', 'USE TEMP B-TREE FOR count(DISTINCT)']
asserts passed
```

**Edge cases:**
- Days with no events: the LEFT JOIN from the spine keeps them (DAU 0). If the window had no users at all, MAU would be 0 and stickiness NULL through `NULLIF`; no such day occurs in this data (days with MAU 0: 0 in the output).
- Window length: a 30-day window ending on the day is `date(day, '-29 days')` to `day` inclusive. A 30-day window with `-30 days` is 31 days and a common off-by-one.
- Date arithmetic: I checked `date('2024-03-01','-29 days')` and `datetime('2024-03-08 10:00:00','+7 days')` against `unixepoch` arithmetic with 86400 seconds; they agree across the leap day (the Code block asserts it). Unlike `julianday` times a constant, this keeps whole days exact.
- Time zone: the day is the UTC date; a user in IST has evening events that fall on the next UTC date, so DAU by IST day differs (Q19, Q36).
- Duplicate events in a day are collapsed by the `DISTINCT` in the `ud` CTE; the range join then sees one row per user-day.
- pandas `Rolling.nunique`: exists in pandas 3.0.5 (the docstring says added in 3.0.0), so the premise that it does not exist is wrong for this version. It works on a time-indexed series with a `'30D'` window, but only produces values at rows that exist, so days without events still need the spine; the Code block checks it on the 7 days that have event rows.

**Then explain:**
- A rolling distinct count cannot be built from daily distinct counts: the same user appears on many days, so summing `DAU` over 30 days is a count of user-days, not users. The only fix is to look at the underlying user-days.
- The spine guarantees one output row per day, including quiet days, and supplies the right edge of each window. Without it you get rows only for days with events and a row-based frame such as `ROWS BETWEEN 29 PRECEDING` would silently span more than 30 calendar days.
- Range join cost: each spine day matches up to 30 days of user-days, so the work is roughly spine days times window rows. On a large table you pre-aggregate to user-days first (done in `ud`), index or sort on date, and limit the spine. SQLite's plan here shows a scan with a temporary B-tree for the distinct counts, which I printed; I did not benchmark anything, and other engines (hedged: not executed) have their own range-join and distinct-count strategies, for example approximate distinct functions.
- An alternative that avoids the range join is to track each user's last active date and compare, or to use first-active-date flags for trailing new-user counts; not run here.
- Stickiness is DAU over the same day's rolling MAU here. The calendar-month version (average DAU over calendar MAU) is Q15; fixed-date DAU/WAU/MAU is Q1.

**Follow-ups:**
- Rolling WAU instead? Change `-29 days` to `-6 days`; the rest is identical.
- Calendar MAU instead of rolling? Fix the window to the month, as in Q15.
- Faster for a big table? Pre-aggregate to user-days (already done), partition by date, and in warehouses consider approximate distinct counts and say it is approximate.

**Common mistakes:**
- `ROWS BETWEEN 29 PRECEDING` over daily distinct counts (shown, wrong).
- No spine, so quiet days vanish and the frame is not 30 calendar days.
- Off-by-one window (`-30 days`).
- Range joining raw events instead of distinct user-days.
- Mixing time zones between the spine and the events.

### Q34 ⭐⭐ 🔴 New, returning and resurrected users per day: users(user_id, signup_date, is_test) and events(user_id, event_ts, event_name). For each day from 2024-03-01 to 2024-03-07 classify the active users as new (active on their signup date), returning (active that day and on at least one of the previous 7 days) and resurrected (active that day, not new, with no activity in the previous 7 days but some earlier activity), and return the three counts with their sum equal to DAU. Use one pass with a per-user-day table and a previous-active-date lookup (LAG over distinct active dates), say why the classes must be mutually exclusive, and point to Part 6 for retention tables instead of repeating them.
**Asked at:** active-user guides: Basedash DAU/WAU/MAU pitfalls article (opened; active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users) plus search snippets of oneuptime ClickHouse DAU/WAU/MAU and stickiness posts and Swace and pmtoolkit pages (not opened); guides, not candidate reports; product analytics and data scientist rounds at social, streaming and SaaS companies
**Say this first (1 line):** Build one table of distinct (user, active day) rows, get each row's previous active day with `LAG`, and label every row with a `CASE` that is evaluated in a fixed order (new, then no previous day, then gap of 7 days or less, else resurrected), so each user-day gets exactly one label and the three counts add up to DAU.

**Schema and sample data:** ten users, one of them a test user (6) and one with `is_test` NULL (10). Events are ISO UTC text. Questions I would ask first, and the answers I assume: (1) "new" means active on the signup date itself, as the question says, not "first event ever"; (2) "previous 7 days" means the 7 calendar days before the day, so a previous active day exactly 7 days earlier is still returning and 8 days earlier is resurrected; (3) a day is a UTC calendar day (no IST shift, see Q36 for that); (4) test users are removed, and a NULL `is_test` is treated as not test; (5) no bot filter here because the table has no user agent (Q37 adds one); (6) fixed as-of date 2024-03-07, so the 2024-03-12 and 2024-03-10 events are outside the report and never used. Week start does not appear in this question.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-02-20',0),(2,'2024-03-01',0),(3,'2024-03-03',0),(4,'2024-02-10',0),
 (5,'2024-02-25',0),(6,'2024-03-01',1),(7,'2024-03-05',0),(8,'2024-02-28',0),
 (9,'2024-02-20',0),(10,'2024-03-02',NULL);
INSERT INTO events VALUES
 (1,'2024-02-20 08:00:00','open'),(1,'2024-03-01 09:00:00','open'),(1,'2024-03-02 09:00:00','open'),
 (1,'2024-03-05 09:00:00','open'),(1,'2024-03-12 09:00:00','open'),
 (2,'2024-03-01 10:00:00','open'),(2,'2024-03-02 10:00:00','open'),(2,'2024-03-02 18:00:00','open'),
 (2,'2024-03-04 10:00:00','open'),(2,'2024-03-07 10:00:00','open'),
 (3,'2024-03-03 11:00:00','open'),(3,'2024-03-10 11:00:00','open'),
 (4,'2024-02-12 12:00:00','open'),(4,'2024-03-07 12:00:00','open'),
 (5,'2024-03-04 13:00:00','open'),(5,'2024-03-05 13:00:00','open'),
 (6,'2024-03-01 14:00:00','open'),(6,'2024-03-02 14:00:00','open'),
 (7,'2024-03-05 15:00:00','open'),(7,'2024-03-07 15:00:00','open'),
 (8,'2024-02-28 16:00:00','open'),(8,'2024-03-06 16:00:00','open'),(8,'2024-03-07 16:00:00','open'),
 (9,'2024-02-27 17:00:00','open'),(9,'2024-03-06 17:00:00','open'),
 (10,'2024-03-02 19:00:00','open');
```

**SQL answer:** `SQL_MAIN` in the Code block (the `LAG` runs over all history up to the as-of date, so day 2024-03-01 can look back into February; the date filter is applied only after the label is computed):
```sql
WITH d AS (                                   -- one row per user and active day, test users out
  SELECT DISTINCT e.user_id, date(e.event_ts) AS day
  FROM events e JOIN users u ON u.user_id = e.user_id
  WHERE COALESCE(u.is_test, 0) = 0
    AND date(e.event_ts) <= '2024-03-07'      -- fixed as-of, never today
), l AS (                                     -- previous active day, looking back past the window start
  SELECT user_id, day,
         LAG(day) OVER (PARTITION BY user_id ORDER BY day) AS prev_day
  FROM d
), c AS (
  SELECT l.day,
         CASE WHEN l.day = u.signup_date            THEN 'new'
              WHEN l.prev_day IS NULL               THEN 'first_seen_late'
              WHEN l.prev_day >= date(l.day, '-7 days') THEN 'returning'
              ELSE 'resurrected' END AS cls
  FROM l JOIN users u ON u.user_id = l.user_id
  WHERE l.day BETWEEN '2024-03-01' AND '2024-03-07'
)
SELECT day,
       SUM(cls = 'new')             AS new_users,
       SUM(cls = 'returning')       AS returning_users,
       SUM(cls = 'resurrected')     AS resurrected_users,
       SUM(cls = 'first_seen_late') AS first_seen_late,
       COUNT(*)                     AS dau
FROM c
GROUP BY day
ORDER BY day
```
One fact the question text does not cover: a user who signed up earlier but whose first-ever event comes later (user 5: signed up 02-25, first event 03-04) is not new, has no previous day, and so is neither returning nor resurrected. I give that case its own column `first_seen_late` so the four columns sum to DAU. If the data guarantees that everyone is active on their signup date, that column is always 0 and you have exactly the three classes asked for.

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
test_ids = users.loc[users["is_test"].fillna(0).eq(1), "user_id"]
ev = events[~events["user_id"].isin(test_ids)].copy()
ev["day"] = pd.to_datetime(ev["event_ts"]).dt.normalize()
ev = ev[ev["day"] <= "2024-03-07"]
d = ev[["user_id", "day"]].drop_duplicates().sort_values(["user_id", "day"])
d["prev_day"] = d.groupby("user_id")["day"].shift()
d = d.merge(users.assign(signup=pd.to_datetime(users["signup_date"]))[["user_id", "signup"]], on="user_id")
d["cls"] = np.select(
    [d["day"].eq(d["signup"]), d["prev_day"].isna(), d["prev_day"] >= d["day"] - pd.Timedelta(days=7)],
    ["new", "first_seen_late", "returning"], default="resurrected")
w = d[(d["day"] >= "2024-03-01") & (d["day"] <= "2024-03-07")]
pd_df = (pd.crosstab(w["day"], w["cls"])
           .reindex(columns=["new", "returning", "resurrected", "first_seen_late"], fill_value=0))
pd_df["dau"] = pd_df.sum(axis=1)
pd_df = pd_df.reset_index()
pd_df["day"] = pd_df["day"].dt.strftime("%Y-%m-%d")
pd_df.columns = ["day", "new_users", "returning_users", "resurrected_users", "first_seen_late", "dau"]
```

**Example:** the as-of cut keeps events up to 2024-03-07; user 6 is a test user and is dropped. Day by day:
- 03-01: user 2 signs up and is active (new). User 1's previous active day is 02-20, 10 days earlier, so resurrected. DAU 2.
- 03-02: user 10 signs up (new, kept because NULL `is_test` is treated as not test). Users 1 (prev 03-01) and 2 (prev 03-01, two events that day, one distinct day) are returning. DAU 3.
- 03-03: user 3 is new. DAU 1.
- 03-04: user 2 returns (prev 03-02, gap 2). User 5 has no earlier activity and did not sign up today, so first_seen_late. DAU 2.
- 03-05: user 7 new; user 1 returning (prev 03-02, gap 3); user 5 returning (prev 03-04). DAU 3.
- 03-06: user 8 returning (prev 02-28, gap exactly 7); user 9 resurrected (prev 02-27, gap 8). DAU 2.
- 03-07: users 2 (prev 03-04), 7 (prev 03-05) and 8 (prev 03-06) returning; user 4 resurrected (prev 02-12). DAU 4.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas frames after sorting by `day` (compared by value, not dtype), and a second assert checks that the class columns add up to a raw `COUNT(DISTINCT user_id)` DAU computed separately.
```python
# Q34: new, returning and resurrected active users per day (one pass, LAG over distinct active dates)
import sqlite3
import pandas as pd
import numpy as np

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-02-20',0),(2,'2024-03-01',0),(3,'2024-03-03',0),(4,'2024-02-10',0),
 (5,'2024-02-25',0),(6,'2024-03-01',1),(7,'2024-03-05',0),(8,'2024-02-28',0),
 (9,'2024-02-20',0),(10,'2024-03-02',NULL);
INSERT INTO events VALUES
 (1,'2024-02-20 08:00:00','open'),(1,'2024-03-01 09:00:00','open'),(1,'2024-03-02 09:00:00','open'),
 (1,'2024-03-05 09:00:00','open'),(1,'2024-03-12 09:00:00','open'),
 (2,'2024-03-01 10:00:00','open'),(2,'2024-03-02 10:00:00','open'),(2,'2024-03-02 18:00:00','open'),
 (2,'2024-03-04 10:00:00','open'),(2,'2024-03-07 10:00:00','open'),
 (3,'2024-03-03 11:00:00','open'),(3,'2024-03-10 11:00:00','open'),
 (4,'2024-02-12 12:00:00','open'),(4,'2024-03-07 12:00:00','open'),
 (5,'2024-03-04 13:00:00','open'),(5,'2024-03-05 13:00:00','open'),
 (6,'2024-03-01 14:00:00','open'),(6,'2024-03-02 14:00:00','open'),
 (7,'2024-03-05 15:00:00','open'),(7,'2024-03-07 15:00:00','open'),
 (8,'2024-02-28 16:00:00','open'),(8,'2024-03-06 16:00:00','open'),(8,'2024-03-07 16:00:00','open'),
 (9,'2024-02-27 17:00:00','open'),(9,'2024-03-06 17:00:00','open'),
 (10,'2024-03-02 19:00:00','open');
"""
SQL_MAIN = """
WITH d AS (                                   -- one row per user and active day, test users out
  SELECT DISTINCT e.user_id, date(e.event_ts) AS day
  FROM events e JOIN users u ON u.user_id = e.user_id
  WHERE COALESCE(u.is_test, 0) = 0
    AND date(e.event_ts) <= '2024-03-07'      -- fixed as-of, never today
), l AS (                                     -- previous active day, looking back past the window start
  SELECT user_id, day,
         LAG(day) OVER (PARTITION BY user_id ORDER BY day) AS prev_day
  FROM d
), c AS (
  SELECT l.day,
         CASE WHEN l.day = u.signup_date            THEN 'new'
              WHEN l.prev_day IS NULL               THEN 'first_seen_late'
              WHEN l.prev_day >= date(l.day, '-7 days') THEN 'returning'
              ELSE 'resurrected' END AS cls
  FROM l JOIN users u ON u.user_id = l.user_id
  WHERE l.day BETWEEN '2024-03-01' AND '2024-03-07'
)
SELECT day,
       SUM(cls = 'new')             AS new_users,
       SUM(cls = 'returning')       AS returning_users,
       SUM(cls = 'resurrected')     AS resurrected_users,
       SUM(cls = 'first_seen_late') AS first_seen_late,
       COUNT(*)                     AS dau
FROM c
GROUP BY day
ORDER BY day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
test_ids = users.loc[users["is_test"].fillna(0).eq(1), "user_id"]
ev = events[~events["user_id"].isin(test_ids)].copy()
ev["day"] = pd.to_datetime(ev["event_ts"]).dt.normalize()
ev = ev[ev["day"] <= "2024-03-07"]
d = ev[["user_id", "day"]].drop_duplicates().sort_values(["user_id", "day"])
d["prev_day"] = d.groupby("user_id")["day"].shift()
d = d.merge(users.assign(signup=pd.to_datetime(users["signup_date"]))[["user_id", "signup"]], on="user_id")
d["cls"] = np.select(
    [d["day"].eq(d["signup"]), d["prev_day"].isna(), d["prev_day"] >= d["day"] - pd.Timedelta(days=7)],
    ["new", "first_seen_late", "returning"], default="resurrected")
w = d[(d["day"] >= "2024-03-01") & (d["day"] <= "2024-03-07")]
pd_df = (pd.crosstab(w["day"], w["cls"])
           .reindex(columns=["new", "returning", "resurrected", "first_seen_late"], fill_value=0))
pd_df["dau"] = pd_df.sum(axis=1)
pd_df = pd_df.reset_index()
pd_df["day"] = pd_df["day"].dt.strftime("%Y-%m-%d")
pd_df.columns = ["day", "new_users", "returning_users", "resurrected_users", "first_seen_late", "dau"]
# pd:end
print(pd_df.to_string(index=False))
a = sql_df.sort_values("day").reset_index(drop=True)
b = pd_df.sort_values("day").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)  # compared after sorting by day
assert (a["new_users"] + a["returning_users"] + a["resurrected_users"] + a["first_seen_late"] == a["dau"]).all()

# raw DAU straight from events (distinct users, test users out) must equal the class total
raw = con.execute("""
SELECT date(e.event_ts) AS day, COUNT(DISTINCT e.user_id) FROM events e JOIN users u USING(user_id)
WHERE COALESCE(u.is_test,0)=0 AND date(e.event_ts) BETWEEN '2024-03-01' AND '2024-03-07'
GROUP BY 1 ORDER BY 1""").fetchall()
assert [r[1] for r in raw] == a["dau"].tolist()
print("raw DAU check:", [r[1] for r in raw])

# trap: is_test = 0 instead of COALESCE keeps NULL is_test out
n_naive = con.execute("""
SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u USING(user_id)
WHERE u.is_test = 0 AND date(e.event_ts) = '2024-03-02'""").fetchone()[0]
n_ok = con.execute("""
SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u USING(user_id)
WHERE COALESCE(u.is_test,0) = 0 AND date(e.event_ts) = '2024-03-02'""").fetchone()[0]
print("DAU 2024-03-02 with is_test = 0:", n_naive, "| with COALESCE:", n_ok)

# the 7-day boundary: user 8 (gap exactly 7 days) vs user 9 (gap 8 days) on 2024-03-06
print(pd.read_sql_query("""
WITH d AS (SELECT DISTINCT user_id, date(event_ts) AS day FROM events WHERE user_id IN (8,9)),
l AS (SELECT user_id, day, LAG(day) OVER (PARTITION BY user_id ORDER BY day) AS prev_day FROM d)
SELECT user_id, day, prev_day, CAST(julianday(day) - julianday(prev_day) AS INTEGER) AS gap_days
FROM l WHERE day = '2024-03-06' ORDER BY user_id""", con).to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
       day  new_users  returning_users  resurrected_users  first_seen_late  dau
2024-03-01          1                0                  1                0    2
2024-03-02          1                2                  0                0    3
2024-03-03          1                0                  0                0    1
2024-03-04          0                1                  0                1    2
2024-03-05          1                2                  0                0    3
2024-03-06          0                1                  1                0    2
2024-03-07          0                3                  1                0    4
       day  new_users  returning_users  resurrected_users  first_seen_late  dau
2024-03-01          1                0                  1                0    2
2024-03-02          1                2                  0                0    3
2024-03-03          1                0                  0                0    1
2024-03-04          0                1                  0                1    2
2024-03-05          1                2                  0                0    3
2024-03-06          0                1                  1                0    2
2024-03-07          0                3                  1                0    4
raw DAU check: [2, 3, 1, 2, 3, 2, 4]
DAU 2024-03-02 with is_test = 0: 2 | with COALESCE: 3
 user_id        day   prev_day  gap_days
       8 2024-03-06 2024-02-28         7
       9 2024-03-06 2024-02-27         8
asserts passed
```

**Edge cases:**
- Two events on the same day (user 2 on 03-02) are one user-day because of `SELECT DISTINCT`; without it `LAG` would return the same day as the "previous" day and mark the user returning with a gap of 0.
- The 7-day boundary is a coin flip unless you state it: user 8 (gap 7) is returning and user 9 (gap 8) is resurrected in my run. Use `>= date(day, '-7 days')` or `< ` the other way, but say which.
- NULL `is_test`: `WHERE u.is_test = 0` silently drops user 10, so DAU on 03-02 is 2 instead of 3 in my run. `COALESCE(is_test, 0) = 0` keeps them.
- Days with nobody active would simply be missing from the output; for a chart, join to a date spine (Part 8 Q33, Part 7 Q19).
- Events dated before the signup date are data errors; with `new` tested first they do not change the signup-day label, but fix them upstream.
- An event after the as-of date does not matter for the label of earlier days because `LAG` looks backwards only, but filter it anyway so a rerun later gives the same report.

**Then explain:**
- Mutually exclusive by construction: one `CASE` per user-day, branches tested in order, each branch only reached when the earlier ones fail. If you instead computed three separate queries ("active and signed up today", "active and some activity in the last 7 days", ...) the sets overlap (a user who signed up yesterday and is active today could pass two tests) and the counts would not add up to DAU.
- Why `LAG` over distinct active days: one pass over the user-day table gives each row its previous active day, instead of a self join per day (7 joins) or a correlated subquery with a 7-day range.
- The class matters because the same DAU number can mean growth by new signups, healthy returning use or reactivation campaigns. Retention tables and cohort curves are in Part 6 (Q10, Q11, Q13), not repeated here.
- Dialects (not executed here): PostgreSQL `LAG` and `DATE` subtraction (`day - prev_day <= 7`) work the same; BigQuery uses `DATE_SUB(day, INTERVAL 7 DAY)`; MySQL 8 has `LAG` and `DATE_SUB`.

**Follow-ups:**
- Weekly or monthly version? Replace the day by a week or month key and the 7 days by one period; the logic is the same but state the week start (I would use Monday, as in Q41).
- Is "resurrected" with a 30-day gap different? Only the constant changes; ask the product owner for the definition.
- How would you chart it? Stacked bars per day, with test users and bots already removed.

**Common mistakes:**
- Classifying with three independent filters, so classes overlap or leave gaps.
- Forgetting `DISTINCT` per user-day and counting events.
- Applying the date window before `LAG`, so the first day of the window has no previous day and everyone looks new or late.
- `is_test = 0` dropping NULL users.
- Calling the leftover users "new" when they are late first-time users.

### Q35 ⭐ 🟡 Skipped steps and cumulative funnel logic: events(user_id, event_ts, event_name) with steps view, cart, checkout, purchase in that order. Find the users who skipped a step (reached purchase with no cart or no checkout event) and build the cumulative funnel where reaching a later step counts a user in all earlier steps (step number as MAX of the step index per user, then counts of users with max index >= k). Compare with the strict ordered funnel, and show the pandas version with a boolean column per step and cumulative logic (isin, cumprod on booleans or comparison with the max step), asserting equality with SQL.
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** Skipped-step users are those with a `purchase` event but no `cart` or no `checkout` event; the cumulative funnel gives each user one number, the highest step index they reached, and counts users with that number at or above each step, so a later step can never exceed an earlier one, while the strict ordered funnel needs the step timestamps to increase.

**Schema and sample data:** nine users, one unknown event name (`login`) that must be ignored. Assumptions I would confirm first: the funnel is view, cart, checkout, purchase for all time in the table (no time window, see Q17 for windows); "skipped" means the event is absent, not that it came later; a user is counted once per step; test users and bots are assumed already removed (Q37 shows how); timestamps are UTC text, no week or day bucketing is needed.
- User 1 does all four in order. User 2 skips checkout. User 3 skips cart and checkout. User 4 stops after cart. User 5 has only a purchase (maybe the earlier events are lost or came from another device). User 6 stops after checkout. User 7 has all four events but checkout comes before cart. User 8 starts at cart (no view). User 9 has a view and a `login`.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:01:00','cart'),(1,'2024-03-01 10:02:00','checkout'),(1,'2024-03-01 10:03:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:01:00','cart'),(2,'2024-03-01 11:03:00','purchase'),
 (3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:05:00','purchase'),
 (4,'2024-03-01 13:00:00','view'),(4,'2024-03-01 13:01:00','cart'),
 (5,'2024-03-01 14:00:00','purchase'),
 (6,'2024-03-01 15:00:00','view'),(6,'2024-03-01 15:01:00','cart'),(6,'2024-03-01 15:02:00','checkout'),
 (7,'2024-03-01 16:00:00','view'),(7,'2024-03-01 16:05:00','checkout'),(7,'2024-03-01 16:10:00','cart'),(7,'2024-03-01 16:20:00','purchase'),
 (8,'2024-03-01 17:01:00','cart'),(8,'2024-03-01 17:02:00','checkout'),
 (9,'2024-03-01 18:00:00','view'),(9,'2024-03-01 18:01:00','login');
```

**SQL answer:** `SQL_MAIN` in the Code block (cumulative funnel via the maximum step index per user), plus `SQL_SKIP` for the skipped-step users, `SQL_PRESENCE` for the any-order distinct counts and `SQL_STRICT` for the strict ordered funnel:
```sql
WITH s AS (
  SELECT user_id,
         MAX(CASE event_name WHEN 'view' THEN 1 WHEN 'cart' THEN 2
                             WHEN 'checkout' THEN 3 WHEN 'purchase' THEN 4 END) AS max_step
  FROM events
  GROUP BY user_id
), k(step, step_name) AS (
  VALUES (1,'view'),(2,'cart'),(3,'checkout'),(4,'purchase')
)
SELECT k.step, k.step_name,
       COUNT(s.user_id) AS users_cumulative
FROM k LEFT JOIN s ON s.max_step >= k.step
GROUP BY k.step, k.step_name
ORDER BY k.step
```
Unknown event names give a NULL index in the `CASE`, and `MAX` ignores NULL, so `login` does nothing (user 9 has max step 1 from the view).

**pandas answer:** one boolean column per step (crosstab, then `> 0`), the maximum step index with `map` and `groupby().max()`, and skipped users from the boolean columns. Shown once here, identical to the Code block:
```py
steps = ["view", "cart", "checkout", "purchase"]
ev = events[events["event_name"].isin(steps)]
flags = (pd.crosstab(ev["user_id"], ev["event_name"]).gt(0)
           .reindex(columns=steps, fill_value=False))
max_step = ev["event_name"].map({s: i + 1 for i, s in enumerate(steps)}).groupby(ev["user_id"]).max()
cum = pd.DataFrame({"step": range(1, 5), "step_name": steps,
                    "users_cumulative": [int((max_step >= k).sum()) for k in range(1, 5)]})
skipped = flags[flags["purchase"] & ~(flags["cart"] & flags["checkout"])]
skip_pd = (skipped.astype(int).rename(columns={"cart": "has_cart", "checkout": "has_checkout"})
           [["has_cart", "has_checkout"]].rename_axis(columns=None).reset_index())
```
Two other idioms are in the Code block and are asserted or printed: `flags.astype(int).cumprod(axis=1)` (a user counts at step k only if every step up to k is present, which is a "no skipped step" funnel) and a strict ordered funnel from `pivot_table(..., aggfunc="min")` timestamps.

**Example:** maximum step per user: u1 4, u2 4, u3 4, u4 2, u5 4, u6 3, u7 4, u8 3, u9 1.
- Users with max at least 1: all 9. At least 2: all except u9, so 8. At least 3: u1, u2, u3, u5, u6, u7, u8 = 7. At least 4: u1, u2, u3, u5, u7 = 5.
- Skipped users: u2 (no checkout), u3 (no cart, no checkout), u5 (no cart, no checkout). User 7 is not a skipper: all four events exist.
- Any-order presence: view 7 (u1, 2, 3, 4, 6, 7, 9), cart 6, checkout 4, purchase 5. Cumulative view is 9, larger than 7, because u5 and u8 count as having passed the view step although they have no view event: that is the cost of "reaching a later step counts in all earlier ones".
- Strict ordered (each step's first timestamp after the previous step's): 7, 5, 2, 1. Cart after view: u1, u2, u4, u6, u7 = 5. Checkout after cart: u1 and u6 (u7's checkout is before its cart). Purchase after checkout: only u1.
- Cumprod chain (all earlier steps present, order ignored): 7, 5, 3, 2, between presence and strict.

**Code:** run with `python3 -I`. Asserts: SQL cumulative funnel equals the pandas one (compared after sorting by step), SQL skipped users equal pandas (sorted by user_id), strict SQL tuple equals the strict pandas tuple.
```python
# Q35: skipped steps, cumulative (max step) funnel versus strict ordered funnel
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:01:00','cart'),(1,'2024-03-01 10:02:00','checkout'),(1,'2024-03-01 10:03:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:01:00','cart'),(2,'2024-03-01 11:03:00','purchase'),
 (3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:05:00','purchase'),
 (4,'2024-03-01 13:00:00','view'),(4,'2024-03-01 13:01:00','cart'),
 (5,'2024-03-01 14:00:00','purchase'),
 (6,'2024-03-01 15:00:00','view'),(6,'2024-03-01 15:01:00','cart'),(6,'2024-03-01 15:02:00','checkout'),
 (7,'2024-03-01 16:00:00','view'),(7,'2024-03-01 16:05:00','checkout'),(7,'2024-03-01 16:10:00','cart'),(7,'2024-03-01 16:20:00','purchase'),
 (8,'2024-03-01 17:01:00','cart'),(8,'2024-03-01 17:02:00','checkout'),
 (9,'2024-03-01 18:00:00','view'),(9,'2024-03-01 18:01:00','login');
"""
SQL_MAIN = """
WITH s AS (
  SELECT user_id,
         MAX(CASE event_name WHEN 'view' THEN 1 WHEN 'cart' THEN 2
                             WHEN 'checkout' THEN 3 WHEN 'purchase' THEN 4 END) AS max_step
  FROM events
  GROUP BY user_id
), k(step, step_name) AS (
  VALUES (1,'view'),(2,'cart'),(3,'checkout'),(4,'purchase')
)
SELECT k.step, k.step_name,
       COUNT(s.user_id) AS users_cumulative
FROM k LEFT JOIN s ON s.max_step >= k.step
GROUP BY k.step, k.step_name
ORDER BY k.step
"""
SQL_SKIP = """
SELECT user_id,
       MAX(event_name = 'cart')     AS has_cart,
       MAX(event_name = 'checkout') AS has_checkout
FROM events
GROUP BY user_id
HAVING MAX(event_name = 'purchase') = 1
   AND (MAX(event_name = 'cart') = 0 OR MAX(event_name = 'checkout') = 0)
ORDER BY user_id
"""
SQL_PRESENCE = """
SELECT event_name, COUNT(DISTINCT user_id) AS users_any_order
FROM events WHERE event_name IN ('view','cart','checkout','purchase')
GROUP BY event_name
"""
SQL_STRICT = """
WITH t AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view'     THEN event_ts END) AS t1,
         MIN(CASE WHEN event_name = 'cart'     THEN event_ts END) AS t2,
         MIN(CASE WHEN event_name = 'checkout' THEN event_ts END) AS t3,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS t4
  FROM events GROUP BY user_id
)
SELECT COUNT(t1) AS s1,
       SUM(t1 IS NOT NULL AND t2 > t1) AS s2,
       SUM(t1 IS NOT NULL AND t2 > t1 AND t3 > t2) AS s3,
       SUM(t1 IS NOT NULL AND t2 > t1 AND t3 > t2 AND t4 > t3) AS s4
FROM t
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("cumulative funnel (SQL):"); print(sql_df.to_string(index=False))
skip_sql = pd.read_sql_query(SQL_SKIP, con)
print("users who reached purchase but skipped a step (SQL):"); print(skip_sql.to_string(index=False))
print("any-order presence per step (SQL):"); print(pd.read_sql_query(SQL_PRESENCE, con).to_string(index=False))
strict_sql = con.execute(SQL_STRICT).fetchone()
print("strict ordered funnel s1..s4 (SQL):", strict_sql)

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
steps = ["view", "cart", "checkout", "purchase"]
ev = events[events["event_name"].isin(steps)]
flags = (pd.crosstab(ev["user_id"], ev["event_name"]).gt(0)
           .reindex(columns=steps, fill_value=False))
max_step = ev["event_name"].map({s: i + 1 for i, s in enumerate(steps)}).groupby(ev["user_id"]).max()
cum = pd.DataFrame({"step": range(1, 5), "step_name": steps,
                    "users_cumulative": [int((max_step >= k).sum()) for k in range(1, 5)]})
skipped = flags[flags["purchase"] & ~(flags["cart"] & flags["checkout"])]
skip_pd = (skipped.astype(int).rename(columns={"cart": "has_cart", "checkout": "has_checkout"})
           [["has_cart", "has_checkout"]].rename_axis(columns=None).reset_index())
# pd:end
print(cum.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.sort_values("step").reset_index(drop=True), cum, check_dtype=False)
pd.testing.assert_frame_equal(skip_sql.sort_values("user_id").reset_index(drop=True),
                              skip_pd.sort_values("user_id").reset_index(drop=True), check_dtype=False)
# alternative idiom 1: row-wise cumprod of the presence booleans = "no skipped step" chain
chain = flags.astype(int).cumprod(axis=1).sum()
print("cumprod of presence booleans (no skipped step):", chain.to_dict())
# alternative idiom 2: strict ordered, from the first timestamp of each step
t = (ev.assign(event_ts=pd.to_datetime(ev["event_ts"]))
       .pivot_table(index="user_id", columns="event_name", values="event_ts", aggfunc="min")
       .reindex(columns=steps))
s1 = t["view"].notna()
s2 = s1 & (t["cart"] > t["view"])
s3 = s2 & (t["checkout"] > t["cart"])
s4 = s3 & (t["purchase"] > t["checkout"])
strict_pd = tuple(int(x.sum()) for x in (s1, s2, s3, s4))
print("strict ordered funnel s1..s4 (pandas):", strict_pd)
assert strict_pd == tuple(int(x) for x in strict_sql)
print("any-order presence (pandas):", flags.sum().to_dict())
print("asserts passed")
```

**Output (my run):**
```text
cumulative funnel (SQL):
 step step_name  users_cumulative
    1      view                 9
    2      cart                 8
    3  checkout                 7
    4  purchase                 5
users who reached purchase but skipped a step (SQL):
 user_id  has_cart  has_checkout
       2         1             0
       3         0             0
       5         0             0
any-order presence per step (SQL):
event_name  users_any_order
      cart                6
  checkout                4
  purchase                5
      view                7
strict ordered funnel s1..s4 (SQL): (7, 5, 2, 1)
 step step_name  users_cumulative
    1      view                 9
    2      cart                 8
    3  checkout                 7
    4  purchase                 5
cumprod of presence booleans (no skipped step): {'view': 7, 'cart': 5, 'checkout': 3, 'purchase': 2}
strict ordered funnel s1..s4 (pandas): (7, 5, 2, 1)
any-order presence (pandas): {'view': 7, 'cart': 6, 'checkout': 4, 'purchase': 5}
asserts passed
```

**Edge cases:**
- Cumulative counts are monotone by construction (4 steps: 9, 8, 7, 5), the any-order counts are not guaranteed to be (view 7, cart 6, checkout 4, purchase 5 in my run: purchase 5 is bigger than checkout 4, the same symptom as Part 8 Q9).
- A purchase-only user (u5) lifts every earlier step in the cumulative funnel. That is right for "how many got at least this far" and wrong for "how many viewed". Say which one you report, and investigate skipped users for tracking gaps (events lost, purchase through another path such as one-click buy).
- User 7 shows that "has all events" is not "went in order"; use timestamps for the strict funnel (Q7 has the `MIN(CASE)` version).
- Users with no event in the four steps do not appear at all; the denominator for step 1 is a choice (users with a view, or all registered users).
- Repeated events are harmless for `MAX`, `MIN` and `COUNT(DISTINCT)`; they would matter for counting rows (Q38).

**Then explain:**
- The max-step idea turns a funnel into a histogram: count users per maximum step, then a reverse cumulative sum gives the funnel. In SQL, `COUNT(...)` joined on `max_step >= step` does the reverse cumulative sum without a window.
- Three funnels, three questions: any-order presence (did the event ever happen), cumulative (how far did they get, skipping allowed), strict (did they do it in order). Interviewers want you to name the one you built.
- Dialects (not executed here): PostgreSQL, BigQuery and Snowflake write the boolean sums as `COUNT(*) FILTER (WHERE ...)`, `COUNTIF(...)` and `COUNT_IF(...)`; the SQLite `SUM(cond)` / `MAX(cond)` shortcut relies on comparisons returning 0 or 1, which MySQL also does but PostgreSQL does not (cast needed).

**Follow-ups:**
- What share of purchasers skipped a step? 3 of 5 here; the denominator is purchasers.
- Should skipped purchasers count in the funnel? In the cumulative view yes; report them as their own number as well.
- Funnel per cohort or channel? Add the group column to the `GROUP BY` (Q8).

**Common mistakes:**
- Using distinct event counts and calling it a funnel (step 3 larger than step 2).
- Using `MAX(event_name)` strings (alphabetical order is not step order).
- Assuming presence means order.
- `NOT IN` for the skipped check with NULL user ids in the subquery (Q37).

### Q36 ⭐ 🟡 Incomplete current period and time zone day boundaries: orders(order_id, user_id, order_ts_utc, amount, status). The report is run on 2024-03-18 (fixed as-of) and shows March GMV down 40 percent against February. Rebuild it as month-to-date versus the same day-of-month window of the previous month, compute daily revenue by the IST day (order_ts_utc plus 330 minutes) and by the UTC day, and show an order at 19:00 UTC on 17 March that lands on 18 March in IST. Say why the last, partial day should be dropped or flagged, and why late-arriving data makes recent days look low.
**Asked at:** active-user guides: Basedash DAU/WAU/MAU pitfalls article (opened; active definition, bots and internal accounts, time zone drift, incomplete periods, calendar vs rolling MAU, events vs users) plus search snippets of oneuptime ClickHouse DAU/WAU/MAU and stickiness posts and Swace and pmtoolkit pages (not opened); guides, not candidate reports; product analytics and data scientist rounds at social, streaming and SaaS companies
**Say this first (1 line):** The report compares a 17-day-old March with a complete February; compare the same day-of-month window instead (1 to 17 March against 1 to 17 February), build the day in the business time zone (IST, UTC plus 330 minutes), and drop or flag 18 March because it is still partial.

**Schema and sample data:** nineteen orders, one cancelled. Assumptions I would confirm first: GMV counts completed orders only; the business day is the IST day; timestamps are stored as UTC text; the report is run on 2024-03-18 with a fixed as-of date (never `now`), so only IST days before 2024-03-18 are complete; refunds are ignored here (Q41); no test or bot filter in this table (Q37). Week start does not appear.
- February is front-loaded to the 17th; orders 2, 3, 7, 11 and 14 are placed late evening UTC, so their IST date is the next day. Order 7 (22:00 UTC on 29 Feb) is already 1 March in IST, order 14 (19:00 UTC on 17 March) is already 18 March in IST.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts_utc TEXT, amount REAL, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2024-02-03 10:00:00',400,'completed'),
 (2,2,'2024-02-10 20:00:00',500,'completed'),
 (3,3,'2024-02-17 19:30:00',350,'completed'),
 (4,1,'2024-02-18 09:00:00',300,'completed'),
 (5,4,'2024-02-25 12:00:00',600,'completed'),
 (6,2,'2024-02-28 08:00:00',550,'completed'),
 (7,5,'2024-02-29 22:00:00',400,'completed'),
 (8,3,'2024-02-12 11:00:00',90,'cancelled'),
 (9,6,'2024-03-02 10:00:00',500,'completed'),
 (10,7,'2024-03-05 12:00:00',450,'completed'),
 (11,8,'2024-03-10 18:30:00',600,'completed'),
 (12,2,'2024-03-14 09:00:00',350,'completed'),
 (13,9,'2024-03-17 08:00:00',400,'completed'),
 (14,4,'2024-03-17 19:00:00',300,'completed'),
 (15,6,'2024-03-18 03:00:00',200,'completed'),
 (16,10,'2024-02-05 09:00:00',600,'completed'),
 (17,11,'2024-02-08 09:00:00',450,'completed'),
 (18,12,'2024-02-14 09:00:00',500,'completed'),
 (19,13,'2024-02-16 09:00:00',300,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block returns the three numbers (current MTD, previous-month same-window, previous full month). The window is `ist_day >= month start AND ist_day < as_of`, a half-open range that leaves out the partial as-of day; the previous-month window has the same number of days (17) via `date(prev_start, '+17 days')`:
```sql
WITH o AS (
  SELECT order_id, amount,
         date(order_ts_utc, '+330 minutes') AS ist_day
  FROM orders
  WHERE status = 'completed'
), p AS (
  SELECT '2024-03-18'                                      AS as_of,
         date('2024-03-18', 'start of month')              AS cur_start,
         date('2024-03-18', 'start of month', '-1 month')  AS prev_start,
         CAST(strftime('%d', '2024-03-18') AS INTEGER) - 1 AS full_days   -- 17 complete days
)
SELECT
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.cur_start AND ist_day < p.as_of) AS mtd_cur,
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.prev_start
                              AND ist_day < date(p.prev_start, '+' || p.full_days || ' days')) AS mtd_prev,
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.prev_start AND ist_day < p.cur_start) AS feb_full_ist
FROM p
```
`SQL_DAILY` in the Code block builds daily revenue for 14 to 18 March on both bases from a recursive-CTE date spine (this works on SQLite 3.45 in my run), so days with no orders show 0 instead of vanishing.

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
o = orders[orders["status"].eq("completed")].copy()
ts = pd.to_datetime(o["order_ts_utc"])
o["ist_day"] = (ts + pd.Timedelta(minutes=330)).dt.normalize()
o["utc_day"] = ts.dt.normalize()
cur = o[(o["ist_day"] >= "2024-03-01") & (o["ist_day"] < "2024-03-18")]["amount"].sum()
prev = o[(o["ist_day"] >= "2024-02-01") & (o["ist_day"] < "2024-02-18")]["amount"].sum()
utc_daily = o.groupby("utc_day")["amount"].sum()
ist_daily = o.groupby("ist_day")["amount"].sum()
days = pd.date_range("2024-03-14", "2024-03-18")
pd_daily = pd.DataFrame({"d": days.strftime("%Y-%m-%d"),
                         "utc_revenue": utc_daily.reindex(days, fill_value=0).to_numpy(),
                         "ist_revenue": ist_daily.reindex(days, fill_value=0).to_numpy()})
```
`tz_localize("UTC").tz_convert("Asia/Kolkata")` gave the same IST day in my run (asserted in the Code block); the fixed `+330 minutes` works even where time zone data is missing, and India has no daylight saving time.

**Example:**
- Naive report on UTC days: March so far 2800 (500 + 450 + 600 + 350 + 400 + 300 + 200) against February's full month 4950: 43.4 percent down. That is mostly 17 days against 29.
- Same window on UTC days, 1 to 17 for both months: March 2600, February 3100, 16.1 percent down.
- Same window on IST days, complete days only: March 2700 (order 7 now belongs to 1 March, order 14 to the open day 18), February 2750 (order 3 moves to 18 Feb and is outside the window), so 1.8 percent down. The alarming 40 percent is an artefact of the window; the time zone choice moves the answer by about 14 points here.
- Order 14 at 19:00 UTC on 17 March is 00:30 on 18 March in IST (`date(ts, '+330 minutes')`). On UTC days 17 March has 700 and 18 March 200; on IST days 17 March has 400 and 18 March 500, a partial day that is excluded from the complete-day window.

**Code:** run with `python3 -I`. The asserts compare the SQL month-to-date pair with pandas, the SQL daily table (ordered by day) with pandas, and the `+330 minutes` day with `tz_convert`.
```python
# Q36: month-to-date versus same day-of-month window, IST day versus UTC day, as-of 2024-03-18
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts_utc TEXT, amount REAL, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2024-02-03 10:00:00',400,'completed'),
 (2,2,'2024-02-10 20:00:00',500,'completed'),
 (3,3,'2024-02-17 19:30:00',350,'completed'),
 (4,1,'2024-02-18 09:00:00',300,'completed'),
 (5,4,'2024-02-25 12:00:00',600,'completed'),
 (6,2,'2024-02-28 08:00:00',550,'completed'),
 (7,5,'2024-02-29 22:00:00',400,'completed'),
 (8,3,'2024-02-12 11:00:00',90,'cancelled'),
 (9,6,'2024-03-02 10:00:00',500,'completed'),
 (10,7,'2024-03-05 12:00:00',450,'completed'),
 (11,8,'2024-03-10 18:30:00',600,'completed'),
 (12,2,'2024-03-14 09:00:00',350,'completed'),
 (13,9,'2024-03-17 08:00:00',400,'completed'),
 (14,4,'2024-03-17 19:00:00',300,'completed'),
 (15,6,'2024-03-18 03:00:00',200,'completed'),
 (16,10,'2024-02-05 09:00:00',600,'completed'),
 (17,11,'2024-02-08 09:00:00',450,'completed'),
 (18,12,'2024-02-14 09:00:00',500,'completed'),
 (19,13,'2024-02-16 09:00:00',300,'completed');
"""
SQL_MAIN = """
WITH o AS (
  SELECT order_id, amount,
         date(order_ts_utc, '+330 minutes') AS ist_day
  FROM orders
  WHERE status = 'completed'
), p AS (
  SELECT '2024-03-18'                                      AS as_of,
         date('2024-03-18', 'start of month')              AS cur_start,
         date('2024-03-18', 'start of month', '-1 month')  AS prev_start,
         CAST(strftime('%d', '2024-03-18') AS INTEGER) - 1 AS full_days   -- 17 complete days
)
SELECT
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.cur_start AND ist_day < p.as_of) AS mtd_cur,
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.prev_start
                              AND ist_day < date(p.prev_start, '+' || p.full_days || ' days')) AS mtd_prev,
  (SELECT SUM(amount) FROM o WHERE ist_day >= p.prev_start AND ist_day < p.cur_start) AS feb_full_ist
FROM p
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
r = con.execute(SQL_MAIN).fetchone()
mtd_cur, mtd_prev, feb_full = r
naive = con.execute("""SELECT SUM(amount) FROM orders WHERE status='completed'
                       AND order_ts_utc >= '2024-03-01' AND order_ts_utc < '2024-04-01'""").fetchone()[0]
feb_utc = con.execute("""SELECT SUM(amount) FROM orders WHERE status='completed'
                         AND order_ts_utc >= '2024-02-01' AND order_ts_utc < '2024-03-01'""").fetchone()[0]
print("naive (UTC) March so far:", naive, "| February full month:", feb_utc, "| change: %.1f%%" % (100 * (naive / feb_utc - 1)))
u = con.execute("""SELECT SUM(CASE WHEN date(order_ts_utc) BETWEEN '2024-03-01' AND '2024-03-17' THEN amount END),
                          SUM(CASE WHEN date(order_ts_utc) BETWEEN '2024-02-01' AND '2024-02-17' THEN amount END)
                   FROM orders WHERE status='completed'""").fetchone()
print("MTD on UTC days 1-17: March", u[0], "| February 1-17:", u[1], "| change: %.1f%%" % (100 * (u[0] / u[1] - 1)))
print("MTD IST complete days 1-17: March", mtd_cur, "| February 1-17:", mtd_prev, "| change: %.1f%%" % (100 * (mtd_cur / mtd_prev - 1)))

DAILY = """
SELECT date(order_ts_utc) AS utc_day, date(order_ts_utc, '+330 minutes') AS ist_day, order_id, order_ts_utc, amount
FROM orders WHERE status='completed' AND date(order_ts_utc) <> date(order_ts_utc, '+330 minutes')
ORDER BY order_ts_utc
"""
print("orders whose IST day differs from the UTC day:")
print(pd.read_sql_query(DAILY, con).to_string(index=False))
SQL_DAILY = """
WITH RECURSIVE sp(d) AS (SELECT '2024-03-14' UNION ALL SELECT date(d, '+1 day') FROM sp WHERE d < '2024-03-18')
SELECT sp.d,
       COALESCE((SELECT SUM(amount) FROM orders WHERE status='completed' AND date(order_ts_utc) = sp.d), 0) AS utc_revenue,
       COALESCE((SELECT SUM(amount) FROM orders WHERE status='completed'
                   AND date(order_ts_utc, '+330 minutes') = sp.d), 0) AS ist_revenue
FROM sp ORDER BY sp.d
"""
sql_daily = pd.read_sql_query(SQL_DAILY, con)
print(sql_daily.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders[orders["status"].eq("completed")].copy()
ts = pd.to_datetime(o["order_ts_utc"])
o["ist_day"] = (ts + pd.Timedelta(minutes=330)).dt.normalize()
o["utc_day"] = ts.dt.normalize()
cur = o[(o["ist_day"] >= "2024-03-01") & (o["ist_day"] < "2024-03-18")]["amount"].sum()
prev = o[(o["ist_day"] >= "2024-02-01") & (o["ist_day"] < "2024-02-18")]["amount"].sum()
utc_daily = o.groupby("utc_day")["amount"].sum()
ist_daily = o.groupby("ist_day")["amount"].sum()
days = pd.date_range("2024-03-14", "2024-03-18")
pd_daily = pd.DataFrame({"d": days.strftime("%Y-%m-%d"),
                         "utc_revenue": utc_daily.reindex(days, fill_value=0).to_numpy(),
                         "ist_revenue": ist_daily.reindex(days, fill_value=0).to_numpy()})
# pd:end
assert (cur, prev) == (mtd_cur, mtd_prev)
pd.testing.assert_frame_equal(sql_daily.reset_index(drop=True), pd_daily, check_dtype=False)  # sorted by day
print(pd_daily.to_string(index=False))
# same IST day through a real time zone
tz = pd.to_datetime(o["order_ts_utc"]).dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata").dt.tz_localize(None).dt.normalize()
assert (tz == o["ist_day"]).all()
print("tz_convert('Asia/Kolkata') matches +330 minutes; asserts passed")
```

**Output (my run):**
```text
naive (UTC) March so far: 2800.0 | February full month: 4950.0 | change: -43.4%
MTD on UTC days 1-17: March 2600.0 | February 1-17: 3100.0 | change: -16.1%
MTD IST complete days 1-17: March 2700.0 | February 1-17: 2750.0 | change: -1.8%
orders whose IST day differs from the UTC day:
   utc_day    ist_day  order_id        order_ts_utc  amount
2024-02-10 2024-02-11         2 2024-02-10 20:00:00   500.0
2024-02-17 2024-02-18         3 2024-02-17 19:30:00   350.0
2024-02-29 2024-03-01         7 2024-02-29 22:00:00   400.0
2024-03-10 2024-03-11        11 2024-03-10 18:30:00   600.0
2024-03-17 2024-03-18        14 2024-03-17 19:00:00   300.0
         d  utc_revenue  ist_revenue
2024-03-14        350.0        350.0
2024-03-15          0.0          0.0
2024-03-16          0.0          0.0
2024-03-17        700.0        400.0
2024-03-18        200.0        500.0
         d  utc_revenue  ist_revenue
2024-03-14        350.0        350.0
2024-03-15          0.0          0.0
2024-03-16          0.0          0.0
2024-03-17        700.0        400.0
2024-03-18        200.0        500.0
tz_convert('Asia/Kolkata') matches +330 minutes; asserts passed
```

**Edge cases:**
- Previous month shorter than the day count (as-of 31 March against February): clamp the end with `MIN(date(prev_start, '+N days'), cur_start)`, or say you compare to the full previous month.
- Same-weekday comparison: 1 to 17 March is not the same mix of weekdays as 1 to 17 February; for weekly products compare the same number of full weeks.
- Cancelled orders (order 8) are out; status changes later (a completed order refunded or cancelled) also move past GMV.
- Daylight saving does not exist for IST, but for a US time zone a day can have 23 or 25 hours and a fixed offset is wrong; use a named time zone there.
- Month ends in different time zones: order 7 is February in UTC and March in IST; a monthly report must name its zone.
- Late-arriving data: orders and payments land in the warehouse minutes to days after they happened (async ingestion, retries, delayed settlements), so the most recent days are always incomplete and look low until they fill in; see Part 6 Q35 for event time versus load time.

**Then explain:**
- Why drop or flag the partial day: the day is not over and its orders have not all arrived; including it pulls the last bar down and creates a fake dip. Either cut at the last complete day (as here) or show it in a different style with an "incomplete" flag.
- Month-to-date versus the same day-of-month window of the previous month removes the length bias; year-over-year on the same window removes seasonality.
- The business time zone decides which day an order belongs to; keep timestamps in UTC in storage and convert once, at the reporting layer.
- `datetime` modifiers `'+330 minutes'` are exact for whole-minute offsets; the other engines use `AT TIME ZONE` (PostgreSQL), `CONVERT_TZ` (MySQL), `DATETIME(ts, 'Asia/Kolkata')` (BigQuery) and `CONVERT_TIMEZONE` (Snowflake); these are from memory and not executed here.

**Follow-ups:**
- How do you get a fair number on the day itself? Compare with the same hour of the day on previous days, or wait for a load watermark.
- Which time zone do I pick for a global product? The one finance uses, and say it in the chart subtitle.
- How would you alert on a drop? Compare against the expected value for the same elapsed time, not against a full day.

**Common mistakes:**
- Comparing a part-month with a full month.
- Using the UTC date for an India-based business (evening orders land on the wrong day).
- Keeping the current, incomplete day in the daily series.
- Using `BETWEEN` with a date upper bound on a timestamp column (it drops everything after midnight of the last day); use a half-open range.

### Q37 ⭐ 🟡 NULL attribution, test users and bots in metrics: orders(order_id, user_id, order_ts, amount, status, channel) with NULL channel on some rows, users(user_id, signup_date, is_test) and events with a user_agent column. Return revenue by channel with an explicit 'unknown' bucket, filtering test users and a bot list (user_agent LIKE '%bot%' or a bot_users table) from both numerator and denominator of the conversion rate. Show NOT IN with a NULL user_id in the bot table silently returning no rows, a LEFT JOIN that drops orders with NULL users, and the effect of excluding bots only from the numerator.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** Define one `clean` user set (not test, not in the bot list, no bot user agent) and apply it to both the numerator and the denominator, put orders with a NULL channel in an explicit `'unknown'` bucket, and use `NOT EXISTS` instead of `NOT IN` because a single NULL in the bot table makes `NOT IN` return nothing.

**Schema and sample data:** eight users, eight events (one visit each), eight orders. Questions and assumptions: (1) is revenue for guest orders (NULL `user_id`) wanted? I keep guest revenue in the channel table and leave guests out of the user conversion rate, because a guest has no user to count; (2) test users are `is_test = 1`, and NULL `is_test` counts as not test; (3) bots are users in `bot_users` or with any event whose user agent contains `bot`; (4) conversion = clean buyers (completed order) divided by clean active users (any event) on the sample period; (5) cancelled orders are not revenue; (6) UTC timestamps, no week bucketing.
- User 3 is a test user. User 4 has a `Googlebot` user agent. User 5 is only in `bot_users` (and `bot_users` also holds a NULL row). User 7 has the user agent `AbbottApp/1.0`, which contains the letters "bot" by accident (a false positive; the only order of user 7 is cancelled). Order 7 is a guest order (NULL user) and orders 2 and 5 have NULL channel.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT, channel TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT, user_agent TEXT);
CREATE TABLE bot_users(user_id INTEGER);
INSERT INTO users VALUES (1,'2024-03-01',0),(2,'2024-03-01',0),(3,'2024-03-02',1),(4,'2024-03-02',0),
                         (5,'2024-03-03',0),(6,'2024-03-03',0),(7,'2024-03-04',0),(8,'2024-03-04',0);
INSERT INTO bot_users VALUES (5),(NULL);
INSERT INTO events VALUES
 (1,1,'2024-03-05 10:00:00','visit','Mozilla/5.0'),(2,2,'2024-03-05 10:05:00','visit','Mozilla/5.0'),
 (3,3,'2024-03-05 10:10:00','visit','Mozilla/5.0'),(4,4,'2024-03-05 10:15:00','visit','Googlebot/2.1'),
 (5,5,'2024-03-05 10:20:00','visit','Mozilla/5.0'),(6,6,'2024-03-05 10:25:00','visit','Mozilla/5.0'),
 (7,7,'2024-03-05 10:30:00','visit','AbbottApp/1.0'),(8,8,'2024-03-05 10:35:00','visit','Mozilla/5.0');
INSERT INTO orders VALUES
 (1,1,'2024-03-06 09:00:00',100,'completed','ads'),
 (2,2,'2024-03-06 09:10:00',200,'completed',NULL),
 (3,3,'2024-03-06 09:20:00',300,'completed','ads'),
 (4,4,'2024-03-06 09:30:00',400,'completed','email'),
 (5,5,'2024-03-06 09:40:00',500,'completed',NULL),
 (6,6,'2024-03-06 09:50:00',600,'completed','email'),
 (7,NULL,'2024-03-06 10:00:00',700,'completed','ads'),
 (8,7,'2024-03-06 10:10:00',50,'cancelled','ads');
```

**SQL answer:** `SQL_MAIN` in the Code block (the `clean` CTE is the single filter; the extra `CLEAN_USERS` text in the Code block is the same definition used by the conversion queries):
```sql
WITH clean AS (
  SELECT u.user_id FROM users u
  WHERE COALESCE(u.is_test, 0) = 0
    AND NOT EXISTS (SELECT 1 FROM bot_users b WHERE b.user_id = u.user_id)
    AND NOT EXISTS (SELECT 1 FROM events e WHERE e.user_id = u.user_id AND e.user_agent LIKE '%bot%')
)
SELECT COALESCE(o.channel, 'unknown') AS channel,
       COUNT(*)                       AS orders,
       SUM(o.amount)                  AS revenue
FROM orders o
WHERE o.status = 'completed'
  AND (o.user_id IS NULL OR o.user_id IN (SELECT user_id FROM clean))   -- guest orders stay in revenue
GROUP BY COALESCE(o.channel, 'unknown')
ORDER BY revenue DESC
```
`SQL_CONV` computes buyers over active users on the clean set, and `SQL_CONV_NUM_ONLY` shows the wrong version that removes bots from the buyers only. `SQL_NOTIN`, `SQL_NOTEXISTS`, `SQL_LEFT_DROP` and `SQL_LEFT_OK` show the two traps.

**pandas answer:** same logic, shown once here and identical to the Code block (the bot list drops its NaN with `dropna()`; `str.contains(..., case=False, na=False)` mirrors SQLite's case-insensitive `LIKE`):
```py
bot_ids = set(bots["user_id"].dropna().astype(int)) | set(
    events.loc[events["user_agent"].str.contains("bot", case=False, na=False), "user_id"])
clean_ids = set(users.loc[users["is_test"].fillna(0).eq(0), "user_id"]) - bot_ids
oc = orders[orders["status"].eq("completed") & (orders["user_id"].isna() | orders["user_id"].isin(clean_ids))]
pd_df = (oc.assign(channel=oc["channel"].fillna("unknown"))
           .groupby("channel", as_index=False)
           .agg(orders=("order_id", "size"), revenue=("amount", "sum"))
           .sort_values("revenue", ascending=False, kind="stable").reset_index(drop=True))
active = events.loc[events["user_id"].isin(clean_ids), "user_id"].nunique()
buyers = orders.loc[orders["status"].eq("completed") & orders["user_id"].isin(clean_ids), "user_id"].nunique()
```

**Example:**
- Clean users: remove test user 3, bot-list user 5 and user-agent bot user 4, and the false positive user 7, leaving users 1, 2, 6, 8.
- Completed orders kept: order 1 (user 1, ads, 100), order 2 (user 2, NULL channel, 200), order 6 (user 6, email, 600) and the guest order 7 (ads, 700). Revenue: ads 800, email 600, unknown 200, total 1600 out of 2800 completed revenue overall.
- Conversion: buyers 1, 2, 6 = 3, active users 1, 2, 6, 8 = 4, rate 0.75.
- Bots removed from the numerator only: the numerator is still 3 but the denominator now contains bots (7 non-test active users: 1, 2, 4, 5, 6, 7, 8), so the rate is 3/7 = 0.4286 instead of 0.75. The filters must be symmetric.
- `NOT IN` against a bot table holding a NULL: `user_id NOT IN (5, NULL)` is never true (it evaluates to NULL for every row not equal to 5), so zero users came back in my run; `NOT EXISTS` returned 7.
- `LEFT JOIN users` followed by `WHERE u.is_test = 0` drops the guest order and any order whose user is missing from `users`: 5 orders and 1800 instead of 6 orders and 2500 with `COALESCE(u.is_test, 0) = 0`. The 2500 still contains two orders from bot users 4 and 5, which is why the main query filters bots by user too.

**Code:** run with `python3 -I`. The assert compares the SQL channel table with the pandas one (both ordered by revenue descending, no ties here) and the conversion numbers.
```python
# Q37: NULL channel, test users, bots, NOT IN with NULL, LEFT JOIN drops, bots only in the numerator
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT, channel TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT, user_agent TEXT);
CREATE TABLE bot_users(user_id INTEGER);
INSERT INTO users VALUES (1,'2024-03-01',0),(2,'2024-03-01',0),(3,'2024-03-02',1),(4,'2024-03-02',0),
                         (5,'2024-03-03',0),(6,'2024-03-03',0),(7,'2024-03-04',0),(8,'2024-03-04',0);
INSERT INTO bot_users VALUES (5),(NULL);
INSERT INTO events VALUES
 (1,1,'2024-03-05 10:00:00','visit','Mozilla/5.0'),(2,2,'2024-03-05 10:05:00','visit','Mozilla/5.0'),
 (3,3,'2024-03-05 10:10:00','visit','Mozilla/5.0'),(4,4,'2024-03-05 10:15:00','visit','Googlebot/2.1'),
 (5,5,'2024-03-05 10:20:00','visit','Mozilla/5.0'),(6,6,'2024-03-05 10:25:00','visit','Mozilla/5.0'),
 (7,7,'2024-03-05 10:30:00','visit','AbbottApp/1.0'),(8,8,'2024-03-05 10:35:00','visit','Mozilla/5.0');
INSERT INTO orders VALUES
 (1,1,'2024-03-06 09:00:00',100,'completed','ads'),
 (2,2,'2024-03-06 09:10:00',200,'completed',NULL),
 (3,3,'2024-03-06 09:20:00',300,'completed','ads'),
 (4,4,'2024-03-06 09:30:00',400,'completed','email'),
 (5,5,'2024-03-06 09:40:00',500,'completed',NULL),
 (6,6,'2024-03-06 09:50:00',600,'completed','email'),
 (7,NULL,'2024-03-06 10:00:00',700,'completed','ads'),
 (8,7,'2024-03-06 10:10:00',50,'cancelled','ads');
"""
# clean = not a test user (NULL is_test counts as not test), user_agent has no 'bot', not in bot_users
CLEAN_USERS = """
SELECT u.user_id FROM users u
WHERE COALESCE(u.is_test, 0) = 0
  AND NOT EXISTS (SELECT 1 FROM bot_users b WHERE b.user_id = u.user_id)
  AND NOT EXISTS (SELECT 1 FROM events e WHERE e.user_id = u.user_id AND e.user_agent LIKE '%bot%')
"""
SQL_MAIN = """
WITH clean AS (
  SELECT u.user_id FROM users u
  WHERE COALESCE(u.is_test, 0) = 0
    AND NOT EXISTS (SELECT 1 FROM bot_users b WHERE b.user_id = u.user_id)
    AND NOT EXISTS (SELECT 1 FROM events e WHERE e.user_id = u.user_id AND e.user_agent LIKE '%bot%')
)
SELECT COALESCE(o.channel, 'unknown') AS channel,
       COUNT(*)                       AS orders,
       SUM(o.amount)                  AS revenue
FROM orders o
WHERE o.status = 'completed'
  AND (o.user_id IS NULL OR o.user_id IN (SELECT user_id FROM clean))   -- guest orders stay in revenue
GROUP BY COALESCE(o.channel, 'unknown')
ORDER BY revenue DESC
"""
SQL_CONV = """
WITH clean AS (%s),
a AS (SELECT DISTINCT user_id FROM events WHERE user_id IN (SELECT user_id FROM clean)),
b AS (SELECT DISTINCT user_id FROM orders WHERE status='completed' AND user_id IN (SELECT user_id FROM clean))
SELECT (SELECT COUNT(*) FROM b) AS buyers, (SELECT COUNT(*) FROM a) AS active,
       ROUND(1.0 * (SELECT COUNT(*) FROM b) / (SELECT COUNT(*) FROM a), 4) AS conv
""" % CLEAN_USERS
SQL_CONV_NUM_ONLY = """
WITH clean AS (%s),
b AS (SELECT DISTINCT user_id FROM orders WHERE status='completed' AND user_id IN (SELECT user_id FROM clean))
SELECT (SELECT COUNT(*) FROM b) AS buyers,
       (SELECT COUNT(DISTINCT user_id) FROM events WHERE user_id IN (SELECT user_id FROM users WHERE COALESCE(is_test,0)=0)) AS active_with_bots,
       ROUND(1.0 * (SELECT COUNT(*) FROM b) / (SELECT COUNT(DISTINCT user_id) FROM events
             WHERE user_id IN (SELECT user_id FROM users WHERE COALESCE(is_test,0)=0)), 4) AS conv
""" % CLEAN_USERS
SQL_NOTIN = "SELECT COUNT(*) FROM users WHERE user_id NOT IN (SELECT user_id FROM bot_users)"
SQL_NOTEXISTS = "SELECT COUNT(*) FROM users u WHERE NOT EXISTS (SELECT 1 FROM bot_users b WHERE b.user_id = u.user_id)"
SQL_LEFT_DROP = """
SELECT COUNT(*) AS orders, SUM(o.amount) AS revenue FROM orders o LEFT JOIN users u ON u.user_id = o.user_id
WHERE o.status='completed' AND u.is_test = 0
"""
SQL_LEFT_OK = """
SELECT COUNT(*) AS orders, SUM(o.amount) AS revenue FROM orders o LEFT JOIN users u ON u.user_id = o.user_id
WHERE o.status='completed' AND COALESCE(u.is_test, 0) = 0
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("revenue by channel, clean (SQL):"); print(sql_df.to_string(index=False))
print("all completed revenue, no filter:", con.execute("SELECT SUM(amount) FROM orders WHERE status='completed'").fetchone()[0])
print("clean users:", [r[0] for r in con.execute(CLEAN_USERS + " ORDER BY 1")])
conv = con.execute(SQL_CONV).fetchone()
conv_bad = con.execute(SQL_CONV_NUM_ONLY).fetchone()
print("conversion, bots out of both (buyers, active, rate):", conv)
print("conversion, bots out of numerator only (buyers, active incl bots, rate):", conv_bad)
print("NOT IN with a NULL in bot_users -> users returned:", con.execute(SQL_NOTIN).fetchone()[0],
      "| NOT EXISTS ->", con.execute(SQL_NOTEXISTS).fetchone()[0])
print("LEFT JOIN + u.is_test = 0 (orders, revenue):", con.execute(SQL_LEFT_DROP).fetchone(),
      "| with COALESCE:", con.execute(SQL_LEFT_OK).fetchone())
print("LIKE '%bot%' matches:", [r for r in con.execute("SELECT user_id, user_agent FROM events WHERE user_agent LIKE '%bot%' ORDER BY 1")])

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
events = pd.read_sql_query("SELECT * FROM events", con)
bots = pd.read_sql_query("SELECT * FROM bot_users", con)
# pd:main
bot_ids = set(bots["user_id"].dropna().astype(int)) | set(
    events.loc[events["user_agent"].str.contains("bot", case=False, na=False), "user_id"])
clean_ids = set(users.loc[users["is_test"].fillna(0).eq(0), "user_id"]) - bot_ids
oc = orders[orders["status"].eq("completed") & (orders["user_id"].isna() | orders["user_id"].isin(clean_ids))]
pd_df = (oc.assign(channel=oc["channel"].fillna("unknown"))
           .groupby("channel", as_index=False)
           .agg(orders=("order_id", "size"), revenue=("amount", "sum"))
           .sort_values("revenue", ascending=False, kind="stable").reset_index(drop=True))
active = events.loc[events["user_id"].isin(clean_ids), "user_id"].nunique()
buyers = orders.loc[orders["status"].eq("completed") & orders["user_id"].isin(clean_ids), "user_id"].nunique()
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # both ordered by revenue desc (no ties here)
assert (buyers, active, round(buyers / active, 4)) == tuple(conv)
assert "bot" in "AbbottApp/1.0".lower()  # the false positive is real
print("pandas conversion:", buyers, active, round(buyers / active, 4))
print("asserts passed")
```

**Output (my run):**
```text
revenue by channel, clean (SQL):
channel  orders  revenue
    ads       2    800.0
  email       1    600.0
unknown       1    200.0
all completed revenue, no filter: 2800.0
clean users: [1, 2, 6, 8]
conversion, bots out of both (buyers, active, rate): (3, 4, 0.75)
conversion, bots out of numerator only (buyers, active incl bots, rate): (3, 7, 0.4286)
NOT IN with a NULL in bot_users -> users returned: 0 | NOT EXISTS -> 7
LEFT JOIN + u.is_test = 0 (orders, revenue): (5, 1800.0) | with COALESCE: (6, 2500.0)
LIKE '%bot%' matches: [(4, 'Googlebot/2.1'), (7, 'AbbottApp/1.0')]
channel  orders  revenue
    ads       2    800.0
  email       1    600.0
unknown       1    200.0
pandas conversion: 3 4 0.75
asserts passed
```

**Edge cases:**
- `LIKE '%bot%'` is case-insensitive for ASCII in SQLite (it matched `Googlebot` and `AbbottApp`); in PostgreSQL `LIKE` is case-sensitive and `ILIKE` is the insensitive form, and other engines differ by collation (not executed here). Substring matching has false positives (user 7), so prefer a maintained bot list or a stricter pattern (such as `'%bot/%'` or a regular expression), and say what you used.
- A guest order is revenue but not a user; decide it explicitly. Dropping it silently changes revenue by 700 here.
- NULL channel is not a channel: group it as `'unknown'`, and check the share of unknown (1 of 4 clean orders here); `GROUP BY channel` alone would also work (NULL forms its own group) but would print an empty label.
- Test and bot users can also have `events` but no row in `users`; an inner join to `users` then removes them, which may be what you want or may hide data.
- Bots that buy (users 4 and 5 have completed orders): they inflate both revenue and the buyer count if not removed.

**Then explain:**
- Same population on both sides: the numerator is a subset of the denominator, so remove bots from both, or the rate is biased down (0.4286 instead of 0.75 here, a toy exaggeration).
- Three-valued logic: `x NOT IN (list with NULL)` is UNKNOWN, never true; `NOT EXISTS` and `LEFT JOIN ... IS NULL` do not have this problem (Part 2 anti-join questions cover it).
- `LEFT JOIN` then a filter on the right table in `WHERE` turns it into an inner join; put right-table conditions in `ON`, or use `COALESCE`.
- Bot and test filters belong in one shared view or CTE so every metric uses the same definition (see Q19 on dashboards that disagree).

**Follow-ups:**
- How do you find bots in the first place? Request rate, no JavaScript events, user-agent lists, data-centre IP ranges; this question only applies a list.
- Should refunded orders count? Not here; see Q10 and Q41.
- How large is the bias? Print the metric with and without the filter, as done here.

**Common mistakes:**
- `NOT IN (SELECT user_id FROM bot_users)` with a possible NULL.
- Filtering bots only in the numerator or only in the denominator.
- `WHERE u.is_test = 0` after a `LEFT JOIN`.
- Dropping NULL-channel orders so channel revenue no longer adds to total revenue.
- Trusting `LIKE '%bot%'` without checking false positives.

### Q38 ⭐ 🟡 Repeated events and dedup in funnels: events(event_id, user_id, event_ts, event_name) where the client retries and the same event_id can arrive twice, and a user can also legitimately fire 'purchase' twice. Return funnel step counts and purchase counts after (a) exact duplicate removal by event_id with ROW_NUMBER, (b) deduplication to one row per user and step, and (c) a 5-second near-duplicate rule using LAG. Explain why DISTINCT * is safe only when the duplicate rows are identical, and how the three choices change purchases per purchaser.
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** Name what a duplicate is before removing anything: the same `event_id` (a client retry, remove with `ROW_NUMBER` over `event_id`), a second event of the same user and step (collapse for a funnel, keep for a purchase count), or a near-duplicate within 5 seconds (compare with `LAG`); each choice gives a different purchases-per-purchaser number.
**Schema and sample data:** thirteen rows, three users, no primary key on `event_id` (a retry can repeat it). Assumptions: steps are view, cart, purchase; "retry" means the same `event_id`; for the near-duplicate rule, "within 5 seconds" means a gap of 5 seconds or less to the previous kept-or-not row of the same user and step; UTC, no test or bot filter here (Q37).
- Event 3 (a purchase) arrives twice with an identical timestamp. Event 7 (a cart) arrives twice but the retry has a timestamp one second later, so the rows are not identical. User 1 legitimately buys twice (event 3 at 10:02 and event 4 at 13:00). User 2 has a cart at 11:00:00, a retry-like cart at :04 (event 7, twice) and another at :08 (event 8). User 3 has two purchase events 2 seconds apart with different ids (a double click).
```sql
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,1,'2024-03-01 10:00:00','view'),
 (2,1,'2024-03-01 10:01:00','cart'),
 (3,1,'2024-03-01 10:02:00','purchase'),
 (3,1,'2024-03-01 10:02:00','purchase'),
 (4,1,'2024-03-01 13:00:00','purchase'),
 (5,2,'2024-03-01 11:00:00','view'),
 (6,2,'2024-03-01 11:00:00','cart'),
 (7,2,'2024-03-01 11:00:04','cart'),
 (7,2,'2024-03-01 11:00:05','cart'),
 (8,2,'2024-03-01 11:00:08','cart'),
 (9,3,'2024-03-01 12:00:00','view'),
 (10,3,'2024-03-01 12:05:00','purchase'),
 (11,3,'2024-03-01 12:05:02','purchase');
```

**SQL answer:** `SQL_MAIN` in the Code block, which stacks four summaries (raw, a, b, c). The three dedup queries are built from these pieces, shown here as they appear in the Code block:
- (a) exact duplicates by `event_id`: `SELECT ... FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY event_ts) AS rn FROM events) WHERE rn = 1` (the earliest row per `event_id` wins; add a deterministic tiebreaker such as arrival time if you have one).
- (b) one row per user and step: `SELECT user_id, event_name, MIN(event_ts) FROM events GROUP BY user_id, event_name`.
- (c) 5-second rule: start from (a), then `LAG(event_ts) OVER (PARTITION BY user_id, event_name ORDER BY event_ts, event_id)` and keep a row when there is no previous row or `unixepoch(event_ts) - unixepoch(prev_ts) > 5`.
Final summary per method: view rows, cart rows, purchases (rows), purchasers (distinct users), purchases per purchaser.
```sql
WITH raw AS (SELECT 'raw' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users FROM events GROUP BY event_name),
a AS (SELECT 'a_event_id' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name),
b AS (SELECT 'b_user_step' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name),
c AS (SELECT 'c_5s_lag' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name)
SELECT method,
       SUM(CASE WHEN event_name='view' THEN rows_ END)     AS view_rows,
       SUM(CASE WHEN event_name='cart' THEN rows_ END)     AS cart_rows,
       SUM(CASE WHEN event_name='purchase' THEN rows_ END) AS purchases,
       SUM(CASE WHEN event_name='purchase' THEN users END) AS purchasers,
       ROUND(1.0 * SUM(CASE WHEN event_name='purchase' THEN rows_ END)
                 / SUM(CASE WHEN event_name='purchase' THEN users END), 2) AS per_purchaser
FROM (SELECT * FROM raw UNION ALL SELECT * FROM a UNION ALL SELECT * FROM b UNION ALL SELECT * FROM c)
GROUP BY method
ORDER BY CASE method WHEN 'raw' THEN 0 WHEN 'a_event_id' THEN 1 WHEN 'b_user_step' THEN 2 ELSE 3 END
```

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
def summarise(df, method):
    g = df.groupby("event_name")
    rows, users = g.size(), g["user_id"].nunique()
    return {"method": method, "view_rows": int(rows.get("view", 0)), "cart_rows": int(rows.get("cart", 0)),
            "purchases": int(rows.get("purchase", 0)), "purchasers": int(users.get("purchase", 0)),
            "per_purchaser": round(rows.get("purchase", 0) / users.get("purchase", 1), 2)}
ev = events.assign(ts=pd.to_datetime(events["event_ts"]))
a = ev.sort_values("ts", kind="stable").drop_duplicates("event_id", keep="first")
b = ev.drop_duplicates(["user_id", "event_name"], keep="first")
c = a.sort_values(["user_id", "event_name", "ts", "event_id"], kind="stable")
prev = c.groupby(["user_id", "event_name"])["ts"].shift()
c = c[prev.isna() | ((c["ts"] - prev).dt.total_seconds() > 5)]
pd_df = pd.DataFrame([summarise(ev, "raw"), summarise(a, "a_event_id"),
                      summarise(b, "b_user_step"), summarise(c, "c_5s_lag")])
```

**Example:** raw rows: view 3, cart 5 (ids 2, 6, 7, 7, 8), purchase 5 (ids 3, 3, 4, 10, 11), purchasers 2 (users 1 and 3), so 5 / 2 = 2.5 purchases per purchaser.
- (a) event_id: one copy of event 3 and one copy of event 7 go, leaving cart 4 and purchases 4 (ids 3, 4, 10, 11): 4 / 2 = 2.0. User 1's second purchase and user 3's double click both stay.
- (b) one row per user and step: carts 2 (users 1 and 2), purchases 2 (users 1 and 3), so exactly 1.0 purchase per purchaser. This is right for a funnel (who reached the step) and wrong for "how many purchases".
- (c) 5-second rule on top of (a): user 3's second purchase is 2 seconds after the first and goes; user 1's purchases are 3 hours apart and stay: 3 purchases, 3 / 2 = 1.5. For user 2's carts, event 7 is 4 seconds after event 6 and goes, and event 8 is 4 seconds after event 7 (itself dropped) so it goes as well: only event 6 survives, even though event 8 is 8 seconds after event 6.
- `SELECT DISTINCT *` leaves 12 of 13 rows: it removes the identical copy of event 3 but not the retry of event 7, because its timestamp differs.

**Code:** run with `python3 -I`. The assert compares the SQL summary with the pandas one (rows in the same method order: raw, a, b, c) and a second assert shows that `DISTINCT *` is the same as dropping duplicates over all four columns.
```python
# Q38: duplicates and dedup in funnels: (a) event_id, (b) one row per user and step, (c) 5-second near-duplicate with LAG
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,1,'2024-03-01 10:00:00','view'),
 (2,1,'2024-03-01 10:01:00','cart'),
 (3,1,'2024-03-01 10:02:00','purchase'),
 (3,1,'2024-03-01 10:02:00','purchase'),
 (4,1,'2024-03-01 13:00:00','purchase'),
 (5,2,'2024-03-01 11:00:00','view'),
 (6,2,'2024-03-01 11:00:00','cart'),
 (7,2,'2024-03-01 11:00:04','cart'),
 (7,2,'2024-03-01 11:00:05','cart'),
 (8,2,'2024-03-01 11:00:08','cart'),
 (9,3,'2024-03-01 12:00:00','view'),
 (10,3,'2024-03-01 12:05:00','purchase'),
 (11,3,'2024-03-01 12:05:02','purchase');
"""
# (a) exact duplicates by event_id: keep the earliest row per event_id
A = """
SELECT event_id, user_id, event_ts, event_name FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY event_ts) AS rn FROM events
) WHERE rn = 1
"""
# (b) one row per user and step
B = """
SELECT user_id, event_name, MIN(event_ts) AS event_ts, COUNT(*) AS raw_rows FROM events GROUP BY user_id, event_name
"""
# (c) 5-second rule: drop a row if the previous row of the same user and step is 5 seconds or less earlier
C = """
SELECT event_id, user_id, event_ts, event_name FROM (
  SELECT *, LAG(event_ts) OVER (PARTITION BY user_id, event_name ORDER BY event_ts, event_id) AS prev_ts
  FROM (SELECT event_id, user_id, event_ts, event_name FROM (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY event_ts) AS rn FROM events) WHERE rn = 1)
) WHERE prev_ts IS NULL OR unixepoch(event_ts) - unixepoch(prev_ts) > 5
"""
SQL_MAIN = """
WITH raw AS (SELECT 'raw' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users FROM events GROUP BY event_name),
a AS (SELECT 'a_event_id' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name),
b AS (SELECT 'b_user_step' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name),
c AS (SELECT 'c_5s_lag' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name)
SELECT method,
       SUM(CASE WHEN event_name='view' THEN rows_ END)     AS view_rows,
       SUM(CASE WHEN event_name='cart' THEN rows_ END)     AS cart_rows,
       SUM(CASE WHEN event_name='purchase' THEN rows_ END) AS purchases,
       SUM(CASE WHEN event_name='purchase' THEN users END) AS purchasers,
       ROUND(1.0 * SUM(CASE WHEN event_name='purchase' THEN rows_ END)
                 / SUM(CASE WHEN event_name='purchase' THEN users END), 2) AS per_purchaser
FROM (SELECT * FROM raw UNION ALL SELECT * FROM a UNION ALL SELECT * FROM b UNION ALL SELECT * FROM c)
GROUP BY method
ORDER BY CASE method WHEN 'raw' THEN 0 WHEN 'a_event_id' THEN 1 WHEN 'b_user_step' THEN 2 ELSE 3 END
""" % (A, B, C)
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("SELECT DISTINCT * rows:", con.execute("SELECT COUNT(*) FROM (SELECT DISTINCT * FROM events)").fetchone()[0],
      "| rows:", con.execute("SELECT COUNT(*) FROM events").fetchone()[0],
      "| distinct event_id:", con.execute("SELECT COUNT(DISTINCT event_id) FROM events").fetchone()[0])
print("cart rows kept by (c) for user 2 (event_ids):", [r[0] for r in con.execute("SELECT event_id FROM (%s) WHERE user_id=2 AND event_name='cart' ORDER BY event_ts" % C)])

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
def summarise(df, method):
    g = df.groupby("event_name")
    rows, users = g.size(), g["user_id"].nunique()
    return {"method": method, "view_rows": int(rows.get("view", 0)), "cart_rows": int(rows.get("cart", 0)),
            "purchases": int(rows.get("purchase", 0)), "purchasers": int(users.get("purchase", 0)),
            "per_purchaser": round(rows.get("purchase", 0) / users.get("purchase", 1), 2)}
ev = events.assign(ts=pd.to_datetime(events["event_ts"]))
a = ev.sort_values("ts", kind="stable").drop_duplicates("event_id", keep="first")
b = ev.drop_duplicates(["user_id", "event_name"], keep="first")
c = a.sort_values(["user_id", "event_name", "ts", "event_id"], kind="stable")
prev = c.groupby(["user_id", "event_name"])["ts"].shift()
c = c[prev.isna() | ((c["ts"] - prev).dt.total_seconds() > 5)]
pd_df = pd.DataFrame([summarise(ev, "raw"), summarise(a, "a_event_id"),
                      summarise(b, "b_user_step"), summarise(c, "c_5s_lag")])
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # same method order in both
assert len(ev.drop_duplicates(["event_id", "user_id", "event_ts", "event_name"])) == 12  # same as SELECT DISTINCT *: event 7 survives twice
print("asserts passed")
```

**Output (my run):**
```text
     method  view_rows  cart_rows  purchases  purchasers  per_purchaser
        raw          3          5          5           2            2.5
 a_event_id          3          4          4           2            2.0
b_user_step          3          2          2           2            1.0
   c_5s_lag          3          2          3           2            1.5
SELECT DISTINCT * rows: 12 | rows: 13 | distinct event_id: 11
cart rows kept by (c) for user 2 (event_ids): [6]
     method  view_rows  cart_rows  purchases  purchasers  per_purchaser
        raw          3          5          5           2            2.5
 a_event_id          3          4          4           2            2.0
b_user_step          3          2          2           2            1.0
   c_5s_lag          3          2          3           2            1.5
asserts passed
```

**Edge cases:**
- `DISTINCT *` is safe only if every duplicate is byte-for-byte identical (same event_id, timestamp, user, name and any extra columns such as a received-at time or an app version). One differing column, and it keeps both rows (12 rows left here, the retry of event 7 survives).
- Which row to keep with `ROW_NUMBER`: ordering by `event_ts` keeps the earliest; if event time can tie, add a second sort column, else the choice is arbitrary and the run is not reproducible.
- The `LAG` rule compares to the previous row, not to the last kept row, so a chain of events each 4 seconds apart collapses entirely (user 2: only event 6 survives out of 6, 7, 8). An anchored rule (compare to the last kept event) needs a recursive CTE or a loop in pandas; not executed here.
- Legitimate repeats: two purchases by one user are a business fact; dedup by user and step would erase one (view (b) vs (a)).
- Funnel step counts (distinct users) are unchanged by (a), (b) and (c) here: view users stay 3 and cart or purchase user counts stay the same; only row counts move.

**Then explain:**
- Different questions need different dedup: funnel conversion is about users (distinct users per step; duplicates mostly do not matter), purchases per purchaser and revenue are about rows (duplicates inflate them).
- Prefer fixing duplicates by id (a); use near-duplicate time rules (c) only when ids are not trustworthy, and state the threshold.
- The 5-second rule also removes some real double purchases; the right threshold comes from data (distribution of gaps between same-step events).
- Dialects (not executed here): PostgreSQL has `DISTINCT ON (event_id)` and BigQuery/Snowflake have `QUALIFY ROW_NUMBER() ... = 1`; timestamp differences use `EXTRACT(EPOCH FROM ...)` or `TIMESTAMP_DIFF`/`DATEDIFF`.

**Follow-ups:**
- How do you detect duplicates? `GROUP BY event_id HAVING COUNT(*) > 1` and look at which columns differ.
- Could you also prevent them? Idempotency keys on the server, dedup at ingestion; this question is about SQL on what already landed.
- What about the same event arriving late with a new load time? Part 6 Q35 covers event time versus load time.

**Common mistakes:**
- `SELECT DISTINCT *` on rows that differ in one column.
- Collapsing to one row per user and step and then reporting purchases per purchaser (always 1.0).
- Counting funnel steps with `COUNT(*)` instead of `COUNT(DISTINCT user_id)`.
- Dropping repeated purchases as "duplicates".
- A `LAG` rule without a tiebreaker or without noticing the chain effect.

### Q39 ⭐ 🟡 Revenue per active user versus ARPU versus ARPPU over time: users(user_id, signup_date, is_test), events(user_id, event_ts, event_name) and orders(order_id, user_id, order_ts, amount, status). Return per month the registered users to date, monthly active users, paying users, revenue, ARPU (over registered to date), revenue per active user (over MAU) and ARPPU (over payers), plus the payer share of MAU. Explain the three denominators in one line each, why they move in different directions when signups surge, and why a payer who was not active that month (renewal by auto-debit) can make payers exceed the buyers among active users.
**Asked at:** e-commerce and marketplace metric lists: letsdatascience e-commerce SQL list (opened; repeat purchase rate, cart abandonment, top products by category, fan-out and grain pitfalls) and LearnSQL 'SQL metrics in real interviews' (opened; metric patterns breakdown, ratio, KPI, with joins that inflate results and division by zero as pitfalls; one author's own 11 interviews, no questions published); guides, not candidate reports; e-commerce, fintech and marketplace analyst rounds
**Say this first (1 line):** One revenue number, three denominators: ARPU divides by everyone registered to date, revenue per active user divides by that month's active users, ARPPU divides by that month's paying users; build the numerator and each denominator in its own CTE per month, and put the month spine first so empty months do not vanish.

**Schema and sample data:** twelve users (user 6 is a test user), sixteen events, eleven orders (user 6's order and one cancelled order must not count). Questions and assumptions: (1) is revenue completed orders only (yes, and gross of refunds, see Q41 for net); (2) "registered to date" counts non-test users with a signup date before the month ends (users who signed up and later churned still count); (3) "active" is any event in the calendar month; (4) a payer is a user with a completed order in the month, whether or not they had an event that month; (5) calendar months in UTC, fixed range 2024-01 to 2024-03 (the report is as of 2024-03-31, so March is complete); (6) test users are removed from every table, NULL `is_test` counts as not test. No week bucketing here.
- User 2 pays every month (an auto-debit style renewal) but has no event in February or March, so she is a payer who is not active. Users 7 to 12 are the March signup surge: six signups, all active in March, only user 7 pays.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-12-10',0),(2,'2023-12-20',0),(3,'2024-01-05',0),(4,'2024-01-20',0),
 (5,'2024-02-10',0),(6,'2024-02-12',1),
 (7,'2024-03-02',0),(8,'2024-03-03',0),(9,'2024-03-05',0),(10,'2024-03-08',0),(11,'2024-03-09',0),(12,'2024-03-20',0);
INSERT INTO events VALUES
 (1,'2024-01-03 10:00:00','open'),(2,'2024-01-07 10:00:00','open'),(3,'2024-01-08 10:00:00','open'),(4,'2024-01-21 10:00:00','open'),
 (1,'2024-02-02 10:00:00','open'),(3,'2024-02-03 10:00:00','open'),(5,'2024-02-11 10:00:00','open'),(6,'2024-02-13 10:00:00','open'),
 (1,'2024-03-02 10:00:00','open'),(3,'2024-03-04 10:00:00','open'),(7,'2024-03-02 11:00:00','open'),(8,'2024-03-03 11:00:00','open'),
 (9,'2024-03-05 11:00:00','open'),(10,'2024-03-08 11:00:00','open'),(11,'2024-03-09 11:00:00','open'),(12,'2024-03-20 11:00:00','open');
INSERT INTO orders VALUES
 (1,1,'2024-01-04 09:00:00',100,'completed'),(2,3,'2024-01-09 09:00:00',200,'completed'),
 (3,2,'2024-01-15 09:00:00',100,'completed'),
 (4,1,'2024-02-04 09:00:00',100,'completed'),(5,5,'2024-02-12 09:00:00',300,'completed'),
 (6,2,'2024-02-15 09:00:00',100,'completed'),(7,6,'2024-02-14 09:00:00',999,'completed'),
 (8,1,'2024-03-05 09:00:00',100,'completed'),(9,7,'2024-03-06 09:00:00',100,'completed'),
 (10,2,'2024-03-15 09:00:00',100,'completed'),(11,3,'2024-03-16 09:00:00',50,'cancelled');
```

**SQL answer:** `SQL_MAIN` in the Code block. A recursive month spine (`'2024-01-01'`, then `date(ms, '+1 month')`, which worked on SQLite 3.45 in my run) drives the result, each metric has its own CTE at the month grain, and every division uses `NULLIF` so an empty month gives NULL instead of an error:
```sql
WITH RECURSIVE m(ms) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(ms, '+1 month') FROM m WHERE ms < '2024-03-01'
), u AS (SELECT user_id, signup_date FROM users WHERE COALESCE(is_test, 0) = 0),
reg AS (SELECT m.ms, COUNT(u.user_id) AS registered
        FROM m LEFT JOIN u ON u.signup_date < date(m.ms, '+1 month') GROUP BY m.ms),
act AS (SELECT date(e.event_ts, 'start of month') AS ms, COUNT(DISTINCT e.user_id) AS mau
        FROM events e JOIN u ON u.user_id = e.user_id GROUP BY 1),
pay AS (SELECT date(o.order_ts, 'start of month') AS ms, COUNT(DISTINCT o.user_id) AS payers,
               SUM(o.amount) AS revenue
        FROM orders o JOIN u ON u.user_id = o.user_id WHERE o.status = 'completed' GROUP BY 1),
pa AS (SELECT date(o.order_ts, 'start of month') AS ms, COUNT(DISTINCT o.user_id) AS active_payers
       FROM orders o JOIN u ON u.user_id = o.user_id
       WHERE o.status = 'completed'
         AND EXISTS (SELECT 1 FROM events e WHERE e.user_id = o.user_id
                       AND date(e.event_ts, 'start of month') = date(o.order_ts, 'start of month'))
       GROUP BY 1)
SELECT strftime('%Y-%m', m.ms) AS month, reg.registered, COALESCE(act.mau, 0) AS mau,
       COALESCE(pay.payers, 0) AS payers, COALESCE(pa.active_payers, 0) AS active_payers,
       COALESCE(pay.revenue, 0) AS revenue,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(reg.registered, 0), 2)  AS arpu,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(act.mau, 0), 2)         AS rev_per_active,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(pay.payers, 0), 2)      AS arppu,
       ROUND(1.0 * COALESCE(pa.active_payers, 0) / NULLIF(act.mau, 0), 3)    AS payer_share_of_mau,
       ROUND(1.0 * COALESCE(pay.payers, 0) / NULLIF(act.mau, 0), 3)          AS naive_payers_over_mau
FROM m JOIN reg ON reg.ms = m.ms LEFT JOIN act ON act.ms = m.ms
       LEFT JOIN pay ON pay.ms = m.ms LEFT JOIN pa ON pa.ms = m.ms
ORDER BY m.ms
```
One extra CTE `pa` counts payers who were also active in the same month (`active_payers`). The column `payer_share_of_mau` uses it (a share must have its numerator inside its denominator); `naive_payers_over_mau` is the same ratio with all payers on top, to show the trap.

**pandas answer:** same logic with sets per month, shown once here and identical to the Code block:
```py
real = users[users["is_test"].fillna(0).eq(0)]
ids = set(real["user_id"])
ev = events[events["user_id"].isin(ids)].assign(month=lambda d: pd.to_datetime(d["event_ts"]).dt.strftime("%Y-%m"))
oc = orders[orders["user_id"].isin(ids) & orders["status"].eq("completed")].assign(
    month=lambda d: pd.to_datetime(d["order_ts"]).dt.strftime("%Y-%m"))
rows = []
for month in ["2024-01", "2024-02", "2024-03"]:
    month_end = (pd.Timestamp(month + "-01") + pd.offsets.MonthBegin(1)).strftime("%Y-%m-%d")
    registered = int((real["signup_date"] < month_end).sum())
    active = set(ev.loc[ev["month"].eq(month), "user_id"])
    m_orders = oc[oc["month"].eq(month)]
    payers = set(m_orders["user_id"])
    revenue = float(m_orders["amount"].sum())
    rows.append({"month": month, "registered": registered, "mau": len(active), "payers": len(payers),
                 "active_payers": len(payers & active), "revenue": revenue,
                 "arpu": round(revenue / registered, 2), "rev_per_active": round(revenue / len(active), 2),
                 "arppu": round(revenue / len(payers), 2),
                 "payer_share_of_mau": round(len(payers & active) / len(active), 3),
                 "naive_payers_over_mau": round(len(payers) / len(active), 3)})
pd_df = pd.DataFrame(rows)
```

**Example:**
- January: registered 4 (users 1 to 4), MAU 4, payers 3 (users 1, 2, 3), revenue 100 + 200 + 100 = 400. ARPU 400 / 4 = 100, revenue per active user 100, ARPPU 400 / 3 = 133.33, payer share of MAU 3 / 4 = 0.75.
- February: registered 5 (user 5 joined; user 6 is test), MAU 3 (users 1, 3, 5), payers 3 (users 1, 2, 5), revenue 100 + 300 + 100 = 500 (user 6's 999 is excluded). ARPU 100, revenue per active user 166.67, ARPPU 166.67. User 2 paid but was not active: only 2 of the 3 payers are in the 3 actives, so the share of MAU is 0.667, while the naive payers / MAU is 1.0 (every active user "paid", which is false).
- March: registered 11, MAU 8, payers 3 (users 1, 2, 7), revenue 300. ARPU 27.27, revenue per active user 37.5, ARPPU 100, payer share of MAU 2 / 8 = 0.25 (users 1 and 7 are active payers).
- The surge: revenue fell from 500 to 300 and the registered base more than doubled (5 to 11) while MAU went 3 to 8 and payers stayed at 3. ARPU dropped by 73 percent, revenue per active user by 78 percent and ARPPU by 40 percent, because the denominators grew (or the payer mix changed) faster than revenue.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas frames (both ordered by month, compared by value).
```python
# Q39: registered users, MAU, payers, revenue, ARPU, revenue per active user, ARPPU by month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-12-10',0),(2,'2023-12-20',0),(3,'2024-01-05',0),(4,'2024-01-20',0),
 (5,'2024-02-10',0),(6,'2024-02-12',1),
 (7,'2024-03-02',0),(8,'2024-03-03',0),(9,'2024-03-05',0),(10,'2024-03-08',0),(11,'2024-03-09',0),(12,'2024-03-20',0);
INSERT INTO events VALUES
 (1,'2024-01-03 10:00:00','open'),(2,'2024-01-07 10:00:00','open'),(3,'2024-01-08 10:00:00','open'),(4,'2024-01-21 10:00:00','open'),
 (1,'2024-02-02 10:00:00','open'),(3,'2024-02-03 10:00:00','open'),(5,'2024-02-11 10:00:00','open'),(6,'2024-02-13 10:00:00','open'),
 (1,'2024-03-02 10:00:00','open'),(3,'2024-03-04 10:00:00','open'),(7,'2024-03-02 11:00:00','open'),(8,'2024-03-03 11:00:00','open'),
 (9,'2024-03-05 11:00:00','open'),(10,'2024-03-08 11:00:00','open'),(11,'2024-03-09 11:00:00','open'),(12,'2024-03-20 11:00:00','open');
INSERT INTO orders VALUES
 (1,1,'2024-01-04 09:00:00',100,'completed'),(2,3,'2024-01-09 09:00:00',200,'completed'),
 (3,2,'2024-01-15 09:00:00',100,'completed'),
 (4,1,'2024-02-04 09:00:00',100,'completed'),(5,5,'2024-02-12 09:00:00',300,'completed'),
 (6,2,'2024-02-15 09:00:00',100,'completed'),(7,6,'2024-02-14 09:00:00',999,'completed'),
 (8,1,'2024-03-05 09:00:00',100,'completed'),(9,7,'2024-03-06 09:00:00',100,'completed'),
 (10,2,'2024-03-15 09:00:00',100,'completed'),(11,3,'2024-03-16 09:00:00',50,'cancelled');
"""
SQL_MAIN = """
WITH RECURSIVE m(ms) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(ms, '+1 month') FROM m WHERE ms < '2024-03-01'
), u AS (SELECT user_id, signup_date FROM users WHERE COALESCE(is_test, 0) = 0),
reg AS (SELECT m.ms, COUNT(u.user_id) AS registered
        FROM m LEFT JOIN u ON u.signup_date < date(m.ms, '+1 month') GROUP BY m.ms),
act AS (SELECT date(e.event_ts, 'start of month') AS ms, COUNT(DISTINCT e.user_id) AS mau
        FROM events e JOIN u ON u.user_id = e.user_id GROUP BY 1),
pay AS (SELECT date(o.order_ts, 'start of month') AS ms, COUNT(DISTINCT o.user_id) AS payers,
               SUM(o.amount) AS revenue
        FROM orders o JOIN u ON u.user_id = o.user_id WHERE o.status = 'completed' GROUP BY 1),
pa AS (SELECT date(o.order_ts, 'start of month') AS ms, COUNT(DISTINCT o.user_id) AS active_payers
       FROM orders o JOIN u ON u.user_id = o.user_id
       WHERE o.status = 'completed'
         AND EXISTS (SELECT 1 FROM events e WHERE e.user_id = o.user_id
                       AND date(e.event_ts, 'start of month') = date(o.order_ts, 'start of month'))
       GROUP BY 1)
SELECT strftime('%Y-%m', m.ms) AS month, reg.registered, COALESCE(act.mau, 0) AS mau,
       COALESCE(pay.payers, 0) AS payers, COALESCE(pa.active_payers, 0) AS active_payers,
       COALESCE(pay.revenue, 0) AS revenue,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(reg.registered, 0), 2)  AS arpu,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(act.mau, 0), 2)         AS rev_per_active,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(pay.payers, 0), 2)      AS arppu,
       ROUND(1.0 * COALESCE(pa.active_payers, 0) / NULLIF(act.mau, 0), 3)    AS payer_share_of_mau,
       ROUND(1.0 * COALESCE(pay.payers, 0) / NULLIF(act.mau, 0), 3)          AS naive_payers_over_mau
FROM m JOIN reg ON reg.ms = m.ms LEFT JOIN act ON act.ms = m.ms
       LEFT JOIN pay ON pay.ms = m.ms LEFT JOIN pa ON pa.ms = m.ms
ORDER BY m.ms
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
real = users[users["is_test"].fillna(0).eq(0)]
ids = set(real["user_id"])
ev = events[events["user_id"].isin(ids)].assign(month=lambda d: pd.to_datetime(d["event_ts"]).dt.strftime("%Y-%m"))
oc = orders[orders["user_id"].isin(ids) & orders["status"].eq("completed")].assign(
    month=lambda d: pd.to_datetime(d["order_ts"]).dt.strftime("%Y-%m"))
rows = []
for month in ["2024-01", "2024-02", "2024-03"]:
    month_end = (pd.Timestamp(month + "-01") + pd.offsets.MonthBegin(1)).strftime("%Y-%m-%d")
    registered = int((real["signup_date"] < month_end).sum())
    active = set(ev.loc[ev["month"].eq(month), "user_id"])
    m_orders = oc[oc["month"].eq(month)]
    payers = set(m_orders["user_id"])
    revenue = float(m_orders["amount"].sum())
    rows.append({"month": month, "registered": registered, "mau": len(active), "payers": len(payers),
                 "active_payers": len(payers & active), "revenue": revenue,
                 "arpu": round(revenue / registered, 2), "rev_per_active": round(revenue / len(active), 2),
                 "arppu": round(revenue / len(payers), 2),
                 "payer_share_of_mau": round(len(payers & active) / len(active), 3),
                 "naive_payers_over_mau": round(len(payers) / len(active), 3)})
pd_df = pd.DataFrame(rows)
# pd:end
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # both ordered by month
print("asserts passed")
```

**Output (my run):**
```text
  month  registered  mau  payers  active_payers  revenue   arpu  rev_per_active  arppu  payer_share_of_mau  naive_payers_over_mau
2024-01           4    4       3              3    400.0 100.00          100.00 133.33               0.750                  0.750
2024-02           5    3       3              2    500.0 100.00          166.67 166.67               0.667                  1.000
2024-03          11    8       3              2    300.0  27.27           37.50 100.00               0.250                  0.375
asserts passed
```

**Edge cases:**
- Test user 6: active and paying in February; leaving the filter out would make February revenue 1499 and MAU 4.
- Cancelled order 11 is not revenue and not a payer.
- Months with no activity or no payers (a quiet month) give 0 revenue and NULL ratios thanks to the spine and `NULLIF`; a plain `GROUP BY` on orders would drop the month.
- `registered` uses `signup_date < start of next month`; with a timestamp column and a closing-date literal, `<=` would drop the last day.
- Payers per month, not per user: user 2 appears in all three months; summing monthly payers across months overcounts unique payers.
- A user who signed up on the last day of the month counts in registered but is not yet in anyone else's numerator; the same day split affects only the denominators.

**Then explain:**
- The three denominators: ARPU = revenue per registered user (what each signup is worth, diluted by inactive users); revenue per active user = revenue divided by MAU (monetisation of the engaged base); ARPPU = revenue per payer (price level and basket of those who pay).
- A signup surge enlarges the registered base immediately, raises MAU when the new users are active, and leaves payers and revenue flat until they convert, so ARPU and revenue per active user fall while ARPPU is about the mix of payers; the three metrics move in different directions because they answer different questions. Metric choice belongs to Book 6; here the point is to name the denominator.
- Payers can exceed or fail to line up with active buyers when a payment happens without activity: auto-debit renewals, subscriptions billed by the app store, invoices settled by an operations team. Then payers / MAU can reach or pass 1 although fewer than all actives paid; define the share on the payers who were active.
- Related definitions on one schema: Q4 (GMV, AOV, ARPU, ARPPU), Q22 (LTV to date), Q15 (stickiness).

**Follow-ups:**
- Why not use the average over the month's average registered base? Possible; say which you use and be consistent.
- Net of refunds? Subtract refunds in a separate CTE at the order grain (Q10, Q41).
- Per cohort? Group by signup month; retention-style tables are in Part 6.

**Common mistakes:**
- Joining users, events and orders in one query and summing revenue (fan-out: each order is repeated once per event row).
- Dividing by `COUNT(*)` of joined rows instead of distinct users.
- Using users who signed up in the month instead of registered to date for ARPU.
- Forgetting the test filter on one of the three tables.
- Reporting payers over MAU when payers include people who were not active.

### Q40 ⭐ 🔴 Time-window funnel per attempt, not per user: sessions-style events(user_id, event_ts, event_name) where a user can view many times and purchase later. Count each purchase once and attribute it to the most recent view by the same user in the preceding 7 days (so a user with three views and one purchase gives one converted attempt and two unconverted), using a join with ROW_NUMBER or a correlated MAX(view_ts). Return view attempts, converted attempts and the attempt-level conversion, and show how it differs from the user-level first-view conversion on the same data. Explain the cost of the self join.
**Asked at:** funnel guides: PracHub product-analyst funnel case (opened; an original practice case, explicitly not a candidate report; three funnel definitions give 62.5%, 25%, 50% on the same 8 users), DataVidhya funnel-analysis lesson (opened; only the intro was visible), Quadratic funnel blog and letsdatascience e-commerce marketplace SQL list (the latter opened; says it reflects patterns candidates have reported, no company-specific claims); guides, not candidate reports; analyst and data scientist rounds at e-commerce, fintech and product companies
**Say this first (1 line):** Treat each view as an attempt, attribute each purchase to the latest view by the same user before it (and at most 7 days earlier), count the views that received at least one purchase as converted attempts, and compare 3 of 10 attempts with the user-level number (3 of 6 users on first-view conversion) to show how the denominator changes the story.

**Schema and sample data:** seventeen events, seven users. Clarifying questions and my assumptions: (1) the 7 days are measured back from the purchase, and exactly 7 days (604800 seconds) is inside the window; (2) a view must be strictly before the purchase (a view at the same second does not count; I say so because ties need a rule); (3) a purchase with no view in the previous 7 days is unattributed and not a conversion; (4) two purchases after the same view are two attributed purchases but one converted attempt; (5) views are distinct on (user, timestamp); (6) UTC, no test or bot filter in this table (Q37), no week bucketing.
- User 1: three views and one purchase on the third day (one converted attempt, two not). User 2: two views, no purchase. User 3: view then a purchase exactly 7 days later. User 4: view, then a purchase 9 days later (too late). User 5: one view, two purchases after it. User 6: purchase with no view. User 7: a view and a purchase at the same second, then a later view.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-02 10:00:00','view'),(1,'2024-03-03 10:00:00','view'),(1,'2024-03-03 12:00:00','purchase'),
 (2,'2024-03-01 09:00:00','view'),(2,'2024-03-05 09:00:00','view'),
 (3,'2024-03-01 08:00:00','view'),(3,'2024-03-08 08:00:00','purchase'),
 (4,'2024-03-01 08:00:00','view'),(4,'2024-03-10 08:00:00','purchase'),
 (5,'2024-03-02 09:00:00','view'),(5,'2024-03-04 09:00:00','purchase'),(5,'2024-03-05 09:00:00','purchase'),
 (6,'2024-03-06 09:00:00','purchase'),
 (7,'2024-03-07 09:00:00','view'),(7,'2024-03-07 09:00:00','purchase'),(7,'2024-03-09 09:00:00','view');
```

**SQL answer:** `SQL_MAIN` in the Code block (join each purchase to the views in its window, `ROW_NUMBER()` by view time descending, keep row 1). The correlated-subquery variant with `MAX(view_ts)` is `SQL_MAXV` in the Code block and gives the same counts:
```sql
WITH v AS (SELECT DISTINCT user_id, event_ts AS view_ts FROM events WHERE event_name = 'view'),
p AS (SELECT user_id, event_ts AS buy_ts FROM events WHERE event_name = 'purchase'),
m AS (                                         -- each purchase to its most recent earlier view within 7 days
  SELECT p.user_id, p.buy_ts, v.view_ts,
         ROW_NUMBER() OVER (PARTITION BY p.user_id, p.buy_ts ORDER BY v.view_ts DESC) AS rn
  FROM p JOIN v ON v.user_id = p.user_id
               AND v.view_ts < p.buy_ts
               AND unixepoch(p.buy_ts) - unixepoch(v.view_ts) <= 7 * 86400
), a AS (SELECT user_id, buy_ts, view_ts FROM m WHERE rn = 1)
SELECT (SELECT COUNT(*) FROM v)                          AS view_attempts,
       (SELECT COUNT(DISTINCT user_id || '|' || view_ts) FROM a) AS converted_attempts,
       (SELECT COUNT(*) FROM a)                          AS attributed_purchases,
       (SELECT COUNT(*) FROM p) - (SELECT COUNT(*) FROM a) AS unattributed_purchases,
       ROUND(1.0 * (SELECT COUNT(DISTINCT user_id || '|' || view_ts) FROM a) / (SELECT COUNT(*) FROM v), 4) AS attempt_conversion
```
Window arithmetic uses `unixepoch` differences in whole seconds; `datetime(x, '-7 days')` gives the same boundary here (both are printed, user 3 sits on the boundary). `unixepoch` needs SQLite 3.38 or later (version from memory; it ran on 3.45.1 here) and ISO timestamps without a time zone suffix.

**pandas answer:** the join plus window is `merge_asof` with `by="user_id"`, `direction="backward"`, `allow_exact_matches=False` and a 7-day tolerance (which includes exactly 7 days in my run). Shown once here and identical to the Code block:
```py
e = events.assign(ts=pd.to_datetime(events["event_ts"]))
views = e.loc[e["event_name"].eq("view"), ["user_id", "ts"]].drop_duplicates().rename(columns={"ts": "view_ts"})
buys = e.loc[e["event_name"].eq("purchase"), ["user_id", "ts"]].rename(columns={"ts": "buy_ts"})
att = pd.merge_asof(buys.sort_values("buy_ts"), views.sort_values("view_ts"),
                    left_on="buy_ts", right_on="view_ts", by="user_id",
                    direction="backward", allow_exact_matches=False,
                    tolerance=pd.Timedelta(days=7))
n_views = len(views)
conv = att.dropna(subset=["view_ts"]).drop_duplicates(["user_id", "view_ts"])
pd_df = pd.DataFrame({"view_attempts": [n_views], "converted_attempts": [len(conv)],
                      "attributed_purchases": [int(att["view_ts"].notna().sum())],
                      "unattributed_purchases": [int(att["view_ts"].isna().sum())],
                      "attempt_conversion": [round(len(conv) / n_views, 4)]})
first = views.groupby("user_id")["view_ts"].min().rename("first_view").reset_index()
j = first.merge(buys, on="user_id", how="left")
hit = j[(j["buy_ts"] > j["first_view"]) & ((j["buy_ts"] - j["first_view"]) <= pd.Timedelta(days=7))]
user_conv = hit["user_id"].nunique() / len(first)
```

**Example:**
- Views (attempts): user 1 has 3, user 2 has 2, user 3 has 1, user 4 has 1, user 5 has 1, user 7 has 2, user 6 none, total 10. Purchases: 7 (users 1, 3, 4, 5 twice, 6, 7).
- Attribution: user 1's purchase goes to the 03-03 10:00 view (the latest before it), so one converted attempt and two unconverted. User 3's purchase is exactly 7 days after its only view: attributed. User 4's is 9 days after: unattributed. User 5's two purchases both go to the same view: two attributed purchases, one converted attempt. User 6 has no view: unattributed. User 7's purchase has no strictly earlier view (the 03-09 view is later): unattributed.
- Result: 10 view attempts, 3 converted attempts (users 1, 3, 5), 4 attributed purchases, 3 unattributed purchases, attempt conversion 3 / 10 = 0.3.
- User level on the same data, first-view conversion (a purchase after the first view within 7 days): users with a view 6 (1, 2, 3, 4, 5, 7), converted 3 (users 1, 3, 5), 0.5. Same numerator, different denominator: a user with many views is many attempts, so the attempt rate is lower for heavy browsers.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas one-row frames (by value), the correlated-`MAX` query with the pandas counts, and the user-level conversion in SQL with pandas.
```python
# Q40: attempt-level funnel: each purchase attributed to the most recent view in the previous 7 days
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-02 10:00:00','view'),(1,'2024-03-03 10:00:00','view'),(1,'2024-03-03 12:00:00','purchase'),
 (2,'2024-03-01 09:00:00','view'),(2,'2024-03-05 09:00:00','view'),
 (3,'2024-03-01 08:00:00','view'),(3,'2024-03-08 08:00:00','purchase'),
 (4,'2024-03-01 08:00:00','view'),(4,'2024-03-10 08:00:00','purchase'),
 (5,'2024-03-02 09:00:00','view'),(5,'2024-03-04 09:00:00','purchase'),(5,'2024-03-05 09:00:00','purchase'),
 (6,'2024-03-06 09:00:00','purchase'),
 (7,'2024-03-07 09:00:00','view'),(7,'2024-03-07 09:00:00','purchase'),(7,'2024-03-09 09:00:00','view');
"""
SQL_MAIN = """
WITH v AS (SELECT DISTINCT user_id, event_ts AS view_ts FROM events WHERE event_name = 'view'),
p AS (SELECT user_id, event_ts AS buy_ts FROM events WHERE event_name = 'purchase'),
m AS (                                         -- each purchase to its most recent earlier view within 7 days
  SELECT p.user_id, p.buy_ts, v.view_ts,
         ROW_NUMBER() OVER (PARTITION BY p.user_id, p.buy_ts ORDER BY v.view_ts DESC) AS rn
  FROM p JOIN v ON v.user_id = p.user_id
               AND v.view_ts < p.buy_ts
               AND unixepoch(p.buy_ts) - unixepoch(v.view_ts) <= 7 * 86400
), a AS (SELECT user_id, buy_ts, view_ts FROM m WHERE rn = 1)
SELECT (SELECT COUNT(*) FROM v)                          AS view_attempts,
       (SELECT COUNT(DISTINCT user_id || '|' || view_ts) FROM a) AS converted_attempts,
       (SELECT COUNT(*) FROM a)                          AS attributed_purchases,
       (SELECT COUNT(*) FROM p) - (SELECT COUNT(*) FROM a) AS unattributed_purchases,
       ROUND(1.0 * (SELECT COUNT(DISTINCT user_id || '|' || view_ts) FROM a) / (SELECT COUNT(*) FROM v), 4) AS attempt_conversion
"""
SQL_MAXV = """
WITH v AS (SELECT DISTINCT user_id, event_ts AS view_ts FROM events WHERE event_name = 'view'),
p AS (SELECT user_id, event_ts AS buy_ts FROM events WHERE event_name = 'purchase'),
a AS (
  SELECT p.user_id, p.buy_ts,
         (SELECT MAX(v.view_ts) FROM v WHERE v.user_id = p.user_id AND v.view_ts < p.buy_ts
            AND unixepoch(p.buy_ts) - unixepoch(v.view_ts) <= 7 * 86400) AS view_ts
  FROM p
)
SELECT COUNT(DISTINCT user_id || '|' || view_ts) AS converted_attempts, COUNT(view_ts) AS attributed_purchases FROM a
"""
SQL_USER = """
WITH f AS (SELECT user_id, MIN(event_ts) AS first_view FROM events WHERE event_name = 'view' GROUP BY user_id)
SELECT COUNT(*) AS users_with_view,
       SUM(EXISTS (SELECT 1 FROM events e WHERE e.user_id = f.user_id AND e.event_name = 'purchase'
                   AND e.event_ts > f.first_view
                   AND unixepoch(e.event_ts) - unixepoch(f.first_view) <= 7 * 86400)) AS converted_users,
       ROUND(1.0 * SUM(EXISTS (SELECT 1 FROM events e WHERE e.user_id = f.user_id AND e.event_name = 'purchase'
                   AND e.event_ts > f.first_view
                   AND unixepoch(e.event_ts) - unixepoch(f.first_view) <= 7 * 86400)) / COUNT(*), 4) AS user_conversion
FROM f
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("attempt level (join + ROW_NUMBER):"); print(sql_df.to_string(index=False))
print("correlated MAX:", con.execute(SQL_MAXV).fetchone())
print("user level, first view:"); print(pd.read_sql_query(SQL_USER, con).to_string(index=False))
# window arithmetic: datetime(x,'-7 days') versus unixepoch seconds on the exact 7-day boundary (user 3 buys 7 days after the view)
print("boundary user 3, datetime modifier says in window:",
      con.execute("SELECT '2024-03-01 08:00:00' >= datetime('2024-03-08 08:00:00','-7 days')").fetchone()[0],
      "| unixepoch diff <= 604800:", con.execute("SELECT unixepoch('2024-03-08 08:00:00') - unixepoch('2024-03-01 08:00:00') <= 7*86400").fetchone()[0])

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.assign(ts=pd.to_datetime(events["event_ts"]))
views = e.loc[e["event_name"].eq("view"), ["user_id", "ts"]].drop_duplicates().rename(columns={"ts": "view_ts"})
buys = e.loc[e["event_name"].eq("purchase"), ["user_id", "ts"]].rename(columns={"ts": "buy_ts"})
att = pd.merge_asof(buys.sort_values("buy_ts"), views.sort_values("view_ts"),
                    left_on="buy_ts", right_on="view_ts", by="user_id",
                    direction="backward", allow_exact_matches=False,
                    tolerance=pd.Timedelta(days=7))
n_views = len(views)
conv = att.dropna(subset=["view_ts"]).drop_duplicates(["user_id", "view_ts"])
pd_df = pd.DataFrame({"view_attempts": [n_views], "converted_attempts": [len(conv)],
                      "attributed_purchases": [int(att["view_ts"].notna().sum())],
                      "unattributed_purchases": [int(att["view_ts"].isna().sum())],
                      "attempt_conversion": [round(len(conv) / n_views, 4)]})
first = views.groupby("user_id")["view_ts"].min().rename("first_view").reset_index()
j = first.merge(buys, on="user_id", how="left")
hit = j[(j["buy_ts"] > j["first_view"]) & ((j["buy_ts"] - j["first_view"]) <= pd.Timedelta(days=7))]
user_conv = hit["user_id"].nunique() / len(first)
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # one row each
assert round(user_conv, 4) == pd.read_sql_query(SQL_USER, con)["user_conversion"][0]
mx = con.execute(SQL_MAXV).fetchone()
assert mx == (len(conv), int(att["view_ts"].notna().sum()))
print("pandas user-level conversion:", round(user_conv, 4), "| asserts passed")
```

**Output (my run):**
```text
attempt level (join + ROW_NUMBER):
 view_attempts  converted_attempts  attributed_purchases  unattributed_purchases  attempt_conversion
            10                   3                     4                       3                 0.3
correlated MAX: (3, 4)
user level, first view:
 users_with_view  converted_users  user_conversion
               6                3              0.5
boundary user 3, datetime modifier says in window: 1 | unixepoch diff <= 604800: 1
 view_attempts  converted_attempts  attributed_purchases  unattributed_purchases  attempt_conversion
            10                   3                     4                       3                 0.3
pandas user-level conversion: 0.5 | asserts passed
```

**Edge cases:**
- Boundary: exactly 7 days is included by `<= 7 * 86400`; with `<` user 3 would turn into unattributed and attempts converted would be 2.
- Ties on the same timestamp: user 7's view and purchase share a second; strict `<` ignores that view. Whichever you choose, state it.
- Identical view timestamps for one user would give duplicate view rows; the `DISTINCT` on (user, view time) treats them as one attempt (without an event id there is no way to tell them apart).
- Several purchases after one view: converted attempts count the view once, attributed purchases count both.
- Purchases with no view are kept in a separate unattributed count so the totals reconcile (7 purchases = 4 + 3).
- A view can be the most recent view for a purchase and also be 6 days old: attribution by recency does not mean the view caused the purchase.

**Then explain:**
- Attempt-level conversion answers "how often does a view lead to a purchase"; user-level answers "how many people buy". Both are legitimate; the first is lower when users view repeatedly and moves with browsing frequency.
- The self join is the cost: for each purchase the engine pairs it with all views of the same user, so rows grow with views times purchases per user; an index on (user_id, event_ts) makes each lookup a range scan, and a window or `merge_asof` approach is closer to sorting once. I did not time these, so I do not quote numbers; check the query plan on real data (Part 11).
- The `ROW_NUMBER` form keeps the matched pair, which you need for a breakdown by view source; the correlated `MAX` form is shorter when you need only the view time.
- Dialects (not executed here): PostgreSQL could use `LEFT JOIN LATERAL (... ORDER BY view_ts DESC LIMIT 1)`; BigQuery and Snowflake would use `QUALIFY ROW_NUMBER() ...`; intervals are `INTERVAL '7 days'` or `TIMESTAMP_SUB`.

**Follow-ups:**
- Time windows at user level (first view then a purchase inside N days)? See Q17.
- Sessions instead of views as attempts? Sessionize first (Part 7 Q11) and use the session as the attempt.
- What if purchases can be attributed to several views (multi-touch)? That is attribution, Q45 and Q20.

**Common mistakes:**
- Joining purchases to all views in the window without keeping the latest (a user with 3 views and 1 purchase becomes 3 conversions).
- Counting attributed purchases and calling them converted attempts.
- No window bound, so a purchase months later is credited to an old view.
- Dividing by distinct users and calling it attempt conversion.
- Using `<=` against the purchase time without thinking about same-second events.

### Q41 ⭐ 🔴 A KPI table in one query with several CTEs: users(user_id, signup_date, country, is_test), events(user_id, event_ts, event_name), orders(order_id, user_id, order_ts, amount, status) and refunds(refund_id, order_id, refund_ts, amount). For the week 2024-03-04 to 2024-03-10 return one row with new signups, WAU, orders, GMV (completed), AOV, refund amount, net revenue, paying users, paid conversion over WAU and revenue per active user, each from its own CTE at its own grain, combined with CROSS JOIN of one-row CTEs. Explain why a single big join of all tables double counts and how you test the result (each CTE alone against a hand count).
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** Compute each KPI in its own CTE at its own grain (signups per user, WAU per distinct active user, orders per order, refunds per refund), make each CTE return exactly one row, and `CROSS JOIN` them; a single join of users, events, orders and refunds repeats every order once per event and per refund and inflates every sum.

**Schema and sample data:** eight users (user 7 is a test user), nine events, eight orders, four refunds. Clarifying questions and assumptions: (1) the week runs Monday 2024-03-04 00:00 to Sunday 2024-03-10 23:59:59, written as a half-open range `>= '2024-03-04' AND < '2024-03-11'`, in UTC (no IST shift); (2) "orders" and AOV mean completed orders, so AOV = GMV / completed orders; (3) refund amount is refunds whose refund date is in the week, whichever week the order was in (the alternative, refunds of this week's orders, is a different and also valid metric, say which one); (4) "paying users" are distinct buyers with a completed order in the week; (5) paid conversion = paying users who were also active that week / WAU, so the numerator sits inside the denominator; (6) revenue per active user = GMV / WAU; (7) test users removed everywhere; no bot column in this schema (Q37).
- User 8 pays but has no event in the week (not in WAU). User 6's only event is at 00:30 on 11 March (outside the week), user 1's earlier event at 23:00 on 3 March is outside. Order 2 has two partial refunds. Order 8 was placed on 3 March (last week) and refunded on 4 March, so it enters the refund total but not GMV.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO users VALUES
 (1,'2024-02-01','IN',0),(2,'2024-02-10','IN',0),(3,'2024-03-04','IN',0),(4,'2024-03-06','US',0),
 (5,'2024-03-10','IN',0),(6,'2024-03-11','IN',0),(7,'2024-03-05','IN',1),(8,'2024-02-20','US',0);
INSERT INTO events VALUES
 (1,'2024-03-04 09:00:00','open'),(1,'2024-03-05 09:00:00','open'),(2,'2024-03-06 09:00:00','open'),
 (3,'2024-03-04 10:00:00','open'),(4,'2024-03-06 10:00:00','open'),(5,'2024-03-10 23:30:00','open'),
 (6,'2024-03-11 00:30:00','open'),(7,'2024-03-05 10:00:00','open'),(1,'2024-03-03 23:00:00','open');
INSERT INTO orders VALUES
 (1,1,'2024-03-04 12:00:00',100,'completed'),(2,1,'2024-03-05 12:00:00',200,'completed'),
 (3,2,'2024-03-06 12:00:00',300,'completed'),(4,3,'2024-03-07 12:00:00',50,'cancelled'),
 (5,4,'2024-03-08 12:00:00',400,'completed'),(6,8,'2024-03-09 12:00:00',150,'completed'),
 (7,7,'2024-03-05 12:00:00',999,'completed'),(8,1,'2024-03-03 12:00:00',500,'completed');
INSERT INTO refunds VALUES
 (1,2,'2024-03-06 08:00:00',50),(2,2,'2024-03-07 08:00:00',30),(3,5,'2024-03-09 08:00:00',100),(4,8,'2024-03-04 08:00:00',500);
```

**SQL answer:** `SQL_MAIN` in the Code block, five one-row CTEs (`signups`, `wau`, `ord`, `ref`, `pa`) plus a shared `u` CTE of non-test users:
```sql
WITH u AS (SELECT user_id, signup_date FROM users WHERE COALESCE(is_test, 0) = 0),
signups AS (SELECT COUNT(*) AS new_signups FROM u WHERE signup_date BETWEEN '2024-03-04' AND '2024-03-10'),
wau AS (SELECT COUNT(DISTINCT e.user_id) AS wau
        FROM events e JOIN u ON u.user_id = e.user_id
        WHERE e.event_ts >= '2024-03-04 00:00:00' AND e.event_ts < '2024-03-11 00:00:00'),
ord AS (SELECT COUNT(*) AS orders, COALESCE(SUM(o.amount), 0) AS gmv, COUNT(DISTINCT o.user_id) AS paying_users
        FROM orders o JOIN u ON u.user_id = o.user_id
        WHERE o.status = 'completed'
          AND o.order_ts >= '2024-03-04 00:00:00' AND o.order_ts < '2024-03-11 00:00:00'),
ref AS (SELECT COALESCE(SUM(r.amount), 0) AS refund_amount
        FROM refunds r JOIN orders o ON o.order_id = r.order_id JOIN u ON u.user_id = o.user_id
        WHERE r.refund_ts >= '2024-03-04 00:00:00' AND r.refund_ts < '2024-03-11 00:00:00'),
pa AS (SELECT COUNT(DISTINCT o.user_id) AS active_payers
       FROM orders o JOIN u ON u.user_id = o.user_id
       WHERE o.status = 'completed' AND o.order_ts >= '2024-03-04 00:00:00' AND o.order_ts < '2024-03-11 00:00:00'
         AND o.user_id IN (SELECT e.user_id FROM events e
                           WHERE e.event_ts >= '2024-03-04 00:00:00' AND e.event_ts < '2024-03-11 00:00:00'))
SELECT signups.new_signups, wau.wau, ord.orders, ord.gmv,
       ROUND(1.0 * ord.gmv / NULLIF(ord.orders, 0), 2)                     AS aov,
       ref.refund_amount, ord.gmv - ref.refund_amount                      AS net_revenue,
       ord.paying_users,
       ROUND(1.0 * pa.active_payers / NULLIF(wau.wau, 0), 4)               AS paid_conversion,
       ROUND(1.0 * ord.gmv / NULLIF(wau.wau, 0), 2)                        AS revenue_per_active
FROM signups CROSS JOIN wau CROSS JOIN ord CROSS JOIN ref CROSS JOIN pa
```
`SQL_BIG` in the Code block is the tempting single join (users, events, orders, refunds) for the same week.

**pandas answer:** one scalar per KPI from its own filtered frame, shown once here and identical to the Code block:
```py
lo, hi = pd.Timestamp("2024-03-04"), pd.Timestamp("2024-03-11")       # half-open week, Monday start, UTC
real = users[users["is_test"].fillna(0).eq(0)]
ids = set(real["user_id"])
in_week = lambda s: (pd.to_datetime(s) >= lo) & (pd.to_datetime(s) < hi)
wau_ids = set(events.loc[in_week(events["event_ts"]) & events["user_id"].isin(ids), "user_id"])
oc = orders[orders["status"].eq("completed") & in_week(orders["order_ts"]) & orders["user_id"].isin(ids)]
ref = refunds.merge(orders[["order_id", "user_id"]], on="order_id")
ref = ref[in_week(ref["refund_ts"]) & ref["user_id"].isin(ids)]
gmv = float(oc["amount"].sum())
pd_df = pd.DataFrame([{
    "new_signups": int(pd.to_datetime(real["signup_date"]).between(lo, hi - pd.Timedelta(days=1)).sum()),
    "wau": len(wau_ids), "orders": len(oc), "gmv": gmv, "aov": round(gmv / len(oc), 2),
    "refund_amount": float(ref["amount"].sum()), "net_revenue": gmv - float(ref["amount"].sum()),
    "paying_users": oc["user_id"].nunique(),
    "paid_conversion": round(len(set(oc["user_id"]) & wau_ids) / len(wau_ids), 4),
    "revenue_per_active": round(gmv / len(wau_ids), 2)}])
```

**Example (each CTE by hand):**
- New signups: users 3 (03-04), 4 (03-06) and 5 (03-10) are in the week; user 7 (03-05) is a test user, user 6 signed up on 03-11: 3.
- WAU: users 1, 2, 3, 4, 5 have a non-test event in the week: 5.
- Completed orders: order 1 (100), 2 (200), 3 (300), 5 (400, user 4), 6 (150, user 8) = 5 orders, GMV 1150, AOV 230. Not counted: order 4 (cancelled), order 7 (test user), order 8 (03-03).
- Refunds in the week: 50 + 30 + 100 + 500 = 680 (the 500 belongs to last week's order 8), so net revenue 1150 - 680 = 470. If refunds of this week's orders were wanted instead, it would be 180 and net 970; the choice matters more than any rounding.
- Paying users: users 1, 2, 4, 8 = 4. Active payers: users 1, 2, 4 = 3, so paid conversion over WAU 3 / 5 = 0.6. Revenue per active user 1150 / 5 = 230.
- Single big join for the same week: 8 joined rows and a GMV of 1700 instead of 1150, with 8 order rows for 4 distinct orders. Order 1 is repeated once per active day (2 events), order 2 is repeated 2 events times 2 refunds = 4 times, and order 6 (user 8, no event) disappears because the inner join to events needs an event.

**Code:** run with `python3 -I`. The assert compares the SQL row with the pandas row (one row, compared by value), and a second assert checks every KPI against the hand counts above.
```python
# Q41: weekly KPI row from several one-row CTEs, week 2024-03-04 (Mon) to 2024-03-10 (Sun)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO users VALUES
 (1,'2024-02-01','IN',0),(2,'2024-02-10','IN',0),(3,'2024-03-04','IN',0),(4,'2024-03-06','US',0),
 (5,'2024-03-10','IN',0),(6,'2024-03-11','IN',0),(7,'2024-03-05','IN',1),(8,'2024-02-20','US',0);
INSERT INTO events VALUES
 (1,'2024-03-04 09:00:00','open'),(1,'2024-03-05 09:00:00','open'),(2,'2024-03-06 09:00:00','open'),
 (3,'2024-03-04 10:00:00','open'),(4,'2024-03-06 10:00:00','open'),(5,'2024-03-10 23:30:00','open'),
 (6,'2024-03-11 00:30:00','open'),(7,'2024-03-05 10:00:00','open'),(1,'2024-03-03 23:00:00','open');
INSERT INTO orders VALUES
 (1,1,'2024-03-04 12:00:00',100,'completed'),(2,1,'2024-03-05 12:00:00',200,'completed'),
 (3,2,'2024-03-06 12:00:00',300,'completed'),(4,3,'2024-03-07 12:00:00',50,'cancelled'),
 (5,4,'2024-03-08 12:00:00',400,'completed'),(6,8,'2024-03-09 12:00:00',150,'completed'),
 (7,7,'2024-03-05 12:00:00',999,'completed'),(8,1,'2024-03-03 12:00:00',500,'completed');
INSERT INTO refunds VALUES
 (1,2,'2024-03-06 08:00:00',50),(2,2,'2024-03-07 08:00:00',30),(3,5,'2024-03-09 08:00:00',100),(4,8,'2024-03-04 08:00:00',500);
"""
SQL_MAIN = """
WITH u AS (SELECT user_id, signup_date FROM users WHERE COALESCE(is_test, 0) = 0),
signups AS (SELECT COUNT(*) AS new_signups FROM u WHERE signup_date BETWEEN '2024-03-04' AND '2024-03-10'),
wau AS (SELECT COUNT(DISTINCT e.user_id) AS wau
        FROM events e JOIN u ON u.user_id = e.user_id
        WHERE e.event_ts >= '2024-03-04 00:00:00' AND e.event_ts < '2024-03-11 00:00:00'),
ord AS (SELECT COUNT(*) AS orders, COALESCE(SUM(o.amount), 0) AS gmv, COUNT(DISTINCT o.user_id) AS paying_users
        FROM orders o JOIN u ON u.user_id = o.user_id
        WHERE o.status = 'completed'
          AND o.order_ts >= '2024-03-04 00:00:00' AND o.order_ts < '2024-03-11 00:00:00'),
ref AS (SELECT COALESCE(SUM(r.amount), 0) AS refund_amount
        FROM refunds r JOIN orders o ON o.order_id = r.order_id JOIN u ON u.user_id = o.user_id
        WHERE r.refund_ts >= '2024-03-04 00:00:00' AND r.refund_ts < '2024-03-11 00:00:00'),
pa AS (SELECT COUNT(DISTINCT o.user_id) AS active_payers
       FROM orders o JOIN u ON u.user_id = o.user_id
       WHERE o.status = 'completed' AND o.order_ts >= '2024-03-04 00:00:00' AND o.order_ts < '2024-03-11 00:00:00'
         AND o.user_id IN (SELECT e.user_id FROM events e
                           WHERE e.event_ts >= '2024-03-04 00:00:00' AND e.event_ts < '2024-03-11 00:00:00'))
SELECT signups.new_signups, wau.wau, ord.orders, ord.gmv,
       ROUND(1.0 * ord.gmv / NULLIF(ord.orders, 0), 2)                     AS aov,
       ref.refund_amount, ord.gmv - ref.refund_amount                      AS net_revenue,
       ord.paying_users,
       ROUND(1.0 * pa.active_payers / NULLIF(wau.wau, 0), 4)               AS paid_conversion,
       ROUND(1.0 * ord.gmv / NULLIF(wau.wau, 0), 2)                        AS revenue_per_active
FROM signups CROSS JOIN wau CROSS JOIN ord CROSS JOIN ref CROSS JOIN pa
"""
SQL_BIG = """
SELECT COUNT(*) AS joined_rows, SUM(o.amount) AS gmv_wrong, COUNT(DISTINCT o.order_id) AS orders_ok, COUNT(o.order_id) AS orders_wrong
FROM users u JOIN events e ON e.user_id = u.user_id
             JOIN orders o ON o.user_id = u.user_id AND o.status = 'completed'
             LEFT JOIN refunds r ON r.order_id = o.order_id
WHERE COALESCE(u.is_test,0)=0
  AND e.event_ts >= '2024-03-04' AND e.event_ts < '2024-03-11'
  AND o.order_ts >= '2024-03-04' AND o.order_ts < '2024-03-11'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.T.to_string(header=False))
print("big join, same week:", con.execute(SQL_BIG).fetchone(), "(joined_rows, GMV, correct order count, wrong order count)")

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
lo, hi = pd.Timestamp("2024-03-04"), pd.Timestamp("2024-03-11")       # half-open week, Monday start, UTC
real = users[users["is_test"].fillna(0).eq(0)]
ids = set(real["user_id"])
in_week = lambda s: (pd.to_datetime(s) >= lo) & (pd.to_datetime(s) < hi)
wau_ids = set(events.loc[in_week(events["event_ts"]) & events["user_id"].isin(ids), "user_id"])
oc = orders[orders["status"].eq("completed") & in_week(orders["order_ts"]) & orders["user_id"].isin(ids)]
ref = refunds.merge(orders[["order_id", "user_id"]], on="order_id")
ref = ref[in_week(ref["refund_ts"]) & ref["user_id"].isin(ids)]
gmv = float(oc["amount"].sum())
pd_df = pd.DataFrame([{
    "new_signups": int(pd.to_datetime(real["signup_date"]).between(lo, hi - pd.Timedelta(days=1)).sum()),
    "wau": len(wau_ids), "orders": len(oc), "gmv": gmv, "aov": round(gmv / len(oc), 2),
    "refund_amount": float(ref["amount"].sum()), "net_revenue": gmv - float(ref["amount"].sum()),
    "paying_users": oc["user_id"].nunique(),
    "paid_conversion": round(len(set(oc["user_id"]) & wau_ids) / len(wau_ids), 4),
    "revenue_per_active": round(gmv / len(wau_ids), 2)}])
# pd:end
print(pd_df.T.to_string(header=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # single row
# each CTE alone against a hand count (counted on paper from the INSERTs)
hand = {"new_signups": 3, "wau": 5, "orders": 5, "gmv": 1150.0, "refund_amount": 680.0,
        "net_revenue": 470.0, "paying_users": 4, "aov": 230.0, "paid_conversion": 0.6, "revenue_per_active": 230.0}
for k, v in hand.items():
    assert sql_df.iloc[0][k] == v, (k, sql_df.iloc[0][k], v)
print("hand counts match; asserts passed")
```

**Output (my run):**
```text
new_signups            3.0
wau                    5.0
orders                 5.0
gmv                 1150.0
aov                  230.0
refund_amount        680.0
net_revenue          470.0
paying_users           4.0
paid_conversion        0.6
revenue_per_active   230.0
big join, same week: (8, 1700.0, 4, 8) (joined_rows, GMV, correct order count, wrong order count)
new_signups            3.0
wau                    5.0
orders                 5.0
gmv                 1150.0
aov                  230.0
refund_amount        680.0
net_revenue          470.0
paying_users           4.0
paid_conversion        0.6
revenue_per_active   230.0
hand counts match; asserts passed
```

**Edge cases:**
- Boundaries: a half-open range on timestamps keeps the 23:30 event of 10 March and drops the 00:30 event on 11 March; `BETWEEN '2024-03-04' AND '2024-03-10'` on a timestamp would lose all of 10 March after midnight.
- A week with no orders: `ord` still returns one row (an aggregate without `GROUP BY` returns one row), with `COALESCE(SUM(...), 0)` giving 0 and `NULLIF` giving NULL ratios. A CTE with a `GROUP BY` can return zero rows, and then `CROSS JOIN` returns zero rows for the whole KPI table: keep every CTE aggregate-without-group.
- Payers who are not active (user 8) and active users who never pay: the two denominators in the ratios differ, so state them.
- Test user 7: removed from signups, WAU and orders; the filter lives in the shared `u` CTE so all KPIs agree.
- Refund timing across weeks (order 8) is a definition choice, not a bug.

**Then explain:**
- Fan-out: joining tables with different grains (one user, many events, many orders, many refunds) makes a row for every combination, so a sum over the order amount is multiplied by the number of events and refunds. The fix is to aggregate each table to the grain of its metric first, then combine one-row results.
- Why `CROSS JOIN` is safe here: each side has exactly one row, so the result has exactly one row; there is no join key to get wrong.
- How to test: run each CTE alone and compare to a hand count from a few rows (done above and asserted), compare GMV to a plain `SELECT SUM(amount)` on the orders table with the same filters, and check that ratios use numerators that are subsets of denominators (conversion at most 1).
- Dialects (not executed here): the same CTE and `CROSS JOIN` pattern works in PostgreSQL, MySQL 8, BigQuery and Snowflake; boolean sums become `COUNTIF` or `FILTER`.

**Follow-ups:**
- Weeks for a whole quarter? Group by a week key in each CTE and join on the week (not cross), with a week spine for missing weeks; state Monday as week start.
- How to keep it in sync with another dashboard? Reconcile definitions (Q19).
- Net revenue by order week rather than refund week? Aggregate refunds to the order, join to orders at the order grain, then group by order week.

**Common mistakes:**
- One big join and `SUM(o.amount)`.
- Inner joining orders to events, which silently drops payers who were not active.
- A CTE with `GROUP BY` that returns no rows in an empty week, wiping the whole KPI row.
- Mixing definitions (refunds by refund date, GMV by order date) without saying so.
- `BETWEEN` on timestamps with a date upper bound.

### Q42 ⭐ 🔴 Rolling distinct active users in pandas: events DataFrame(user_id, event_ts) with daily timestamps. Compute the rolling 30-day distinct active users for each day in March 2024 and check whether rolling().nunique exists in your pandas version (it does in pandas 3.0.5, but only yields values at rows that exist) and build it with a date spine and a merge (cross join of days with the events dataframe filtered by the window, or a merge_asof alternative, or a per-day set union), then groupby().nunique(). Assert equality with the SQL range-join result, and comment on memory use (the spine times events merge is the cost) and the alternative of first-active-date flags for trailing counts of new actives.
**Asked at:** pandas reference pages for pivot_table and crosstab (both opened: pivot_table dropna=True drops NaN keys and all-NaN columns, observed default True in 3.0.0; crosstab normalize accepts all/index/columns and dropna drops empty categories) plus expert gap-check on groupby, nunique and rounding behaviour; documentation, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Premise check first: in my run `Rolling.nunique` does exist in pandas 3.0.5, but it works on the event rows you give it, so for a per-day answer you still need a daily spine (a cross merge with a window filter and `groupby().nunique()`, which is the robust method), or spine rows with a NaN user inside `rolling("30D")`, or a difference array that is linear in the number of events.

**Schema and sample data:** ten raw events for five users (user 3 has two events on 2024-03-02, so distinct user-days are 9). Clarifying questions and assumptions: (1) the window for day D is the 30 calendar days D-29 to D inclusive (a user active on D-29 counts, D-30 does not); (2) a "day" is the UTC calendar date of `event_ts`; (3) no test or bot users in this table (Q37 shows the filters); (4) report days 2024-03-01 to 2024-03-31, with a fixed as-of date of 2024-03-31, so events before March are needed for the lookback; (5) no week bucketing. In SQL (the reference) the same rule is `d.day BETWEEN date(sp.day, '-29 days') AND sp.day`.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-28 09:00:00'),(1,'2024-02-20 09:00:00'),(1,'2024-03-15 09:00:00'),
 (2,'2024-02-05 10:00:00'),(2,'2024-02-06 10:00:00'),
 (3,'2024-03-01 11:00:00'),(3,'2024-03-02 11:00:00'),(3,'2024-03-02 15:00:00'),
 (4,'2024-02-02 12:00:00'),
 (5,'2024-03-20 13:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block (recursive date spine on SQLite 3.45, range join, `COUNT(DISTINCT user_id)`):
```sql
WITH RECURSIVE sp(day) AS (
  SELECT '2024-03-01' UNION ALL SELECT date(day, '+1 day') FROM sp WHERE day < '2024-03-31'
), d AS (SELECT DISTINCT user_id, date(event_ts) AS day FROM events)
SELECT sp.day, COUNT(DISTINCT d.user_id) AS rolling_30d_users
FROM sp LEFT JOIN d ON d.day BETWEEN date(sp.day, '-29 days') AND sp.day
GROUP BY sp.day
ORDER BY sp.day
```
The same range join is in Part 8 Q33; here it is the reference for the pandas methods.

**pandas answer:** four methods in one block, all asserted equal to the SQL result. Shown once here and identical to the Code block:
```py
ev = events.assign(day=pd.to_datetime(events["event_ts"]).dt.normalize())[["user_id", "day"]].drop_duplicates()
spine = pd.DataFrame({"day": pd.date_range("2024-03-01", "2024-03-31")})
# (1) spine x events merge, filter to the 30-day window, groupby().nunique()
x = spine.merge(ev, how="cross", suffixes=("", "_ev"))
x = x[(x["day_ev"] <= x["day"]) & (x["day_ev"] >= x["day"] - pd.Timedelta(days=29))]
merge_df = (x.groupby("day")["user_id"].nunique().reindex(spine["day"], fill_value=0)
              .rename("rolling_30d_users").reset_index())
# (2) per-day set union over a sliding window of daily user sets
by_day = ev.groupby("day")["user_id"].agg(set)
sets_df = pd.DataFrame({"day": spine["day"], "rolling_30d_users": [
    len(set().union(*[by_day.get(t, set()) for t in pd.date_range(dd - pd.Timedelta(days=29), dd)]))
    for dd in spine["day"]]})
# (3) difference array: a user is counted from an active day until 30 days after it, or until their next active day
e = ev.sort_values(["user_id", "day"]).copy()
e["nxt"] = e.groupby("user_id")["day"].shift(-1)
e["end"] = np.minimum(e["day"] + pd.Timedelta(days=30), e["nxt"].fillna(pd.Timestamp.max))
idx = pd.date_range("2024-01-01", "2024-04-30")
delta = pd.Series(0, index=idx, dtype="int64")
delta = delta.add(e.groupby("day").size(), fill_value=0).sub(e.groupby("end").size(), fill_value=0)
diff_df = (delta.cumsum().reindex(spine["day"]).astype(int).rename("rolling_30d_users").reset_index())
# (4) rolling('30D').nunique over events plus one spine row (NaN user) at the end of each day
rows = pd.concat([ev.assign(ts=ev["day"]), pd.DataFrame({"user_id": np.nan, "ts": spine["day"] + pd.Timedelta(hours=23, minutes=59)})])
rows = rows.sort_values("ts", kind="stable")
r = rows.rolling("30D", on="ts")["user_id"].nunique()
roll_df = (rows.assign(n=r)[rows["user_id"].isna()][["ts", "n"]]
              .assign(day=lambda d: d["ts"].dt.normalize())[["day", "n"]]
              .rename(columns={"n": "rolling_30d_users"}).reset_index(drop=True))
roll_df["rolling_30d_users"] = roll_df["rolling_30d_users"].astype(int)
```
`Rolling.nunique` exists here: the premise in the question is outdated for pandas 3 (the coordinator reports it was added in pandas 3.0.0; I verified it runs on 3.0.5 and did not check older releases, which would presumably raise `AttributeError`; not executed here). The `rolling("30D")` method is cross-checked against the SQL range join in the Code block, and the merge/spine method stays as the portable alternative that also works on older pandas. A plain `rolling("30D")` on event rows gives one value per event row, so days without events have no row; forward-filling those days is wrong (users must expire), and the Code block prints the days where that naive approach disagrees with SQL. Adding one NaN-user row per day to the spine makes the rolling window evaluate on every day (`nunique` ignores NaN).

**Example:** distinct user-days: user 1 on 01-28, 02-20, 03-15; user 2 on 02-05, 02-06; user 3 on 03-01, 03-02; user 4 on 02-02; user 5 on 03-20.
- 03-01 (window 02-01 to 03-01): user 1 (02-20), user 2, user 3 (03-01), user 4 (02-02): 4.
- 03-02: user 4 (02-02) is still in (02-02 plus 29 days is 03-02): 4. 03-03: user 4 has expired: 3. 03-06: user 2's last event 02-06 is the last day in: 3. 03-07: user 2 is out: 2.
- 03-20 user 5 appears: 3 (users 1, 3, 5), and it stays 3 to 03-31 (user 3's 03-02 stays in until 03-31).
- A user is in the count for 30 days after each active day, so the number can only fall when someone's last active day leaves the window, which is why the difference array works: +1 at each active day, -1 when coverage ends (30 days later, or at the next active day to avoid double counting).

**Code:** run with `python3 -I`. All four pandas methods are asserted equal to the SQL result after sorting by day (compared by value); the memory comparison is printed as row counts, not timings.
```python
# Q42: rolling 30-day distinct active users in pandas: spine + merge, rolling().nunique, difference array; versus SQL range join
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-28 09:00:00'),(1,'2024-02-20 09:00:00'),(1,'2024-03-15 09:00:00'),
 (2,'2024-02-05 10:00:00'),(2,'2024-02-06 10:00:00'),
 (3,'2024-03-01 11:00:00'),(3,'2024-03-02 11:00:00'),(3,'2024-03-02 15:00:00'),
 (4,'2024-02-02 12:00:00'),
 (5,'2024-03-20 13:00:00');
"""
SQL_MAIN = """
WITH RECURSIVE sp(day) AS (
  SELECT '2024-03-01' UNION ALL SELECT date(day, '+1 day') FROM sp WHERE day < '2024-03-31'
), d AS (SELECT DISTINCT user_id, date(event_ts) AS day FROM events)
SELECT sp.day, COUNT(DISTINCT d.user_id) AS rolling_30d_users
FROM sp LEFT JOIN d ON d.day BETWEEN date(sp.day, '-29 days') AND sp.day
GROUP BY sp.day
ORDER BY sp.day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
events = pd.read_sql_query("SELECT * FROM events", con)

# does rolling().nunique exist in this pandas?
print("pandas", pd.__version__, "| Rolling has nunique:", hasattr(pd.Series([1]).rolling(2), "nunique"))

# pd:main
ev = events.assign(day=pd.to_datetime(events["event_ts"]).dt.normalize())[["user_id", "day"]].drop_duplicates()
spine = pd.DataFrame({"day": pd.date_range("2024-03-01", "2024-03-31")})
# (1) spine x events merge, filter to the 30-day window, groupby().nunique()
x = spine.merge(ev, how="cross", suffixes=("", "_ev"))
x = x[(x["day_ev"] <= x["day"]) & (x["day_ev"] >= x["day"] - pd.Timedelta(days=29))]
merge_df = (x.groupby("day")["user_id"].nunique().reindex(spine["day"], fill_value=0)
              .rename("rolling_30d_users").reset_index())
# (2) per-day set union over a sliding window of daily user sets
by_day = ev.groupby("day")["user_id"].agg(set)
sets_df = pd.DataFrame({"day": spine["day"], "rolling_30d_users": [
    len(set().union(*[by_day.get(t, set()) for t in pd.date_range(dd - pd.Timedelta(days=29), dd)]))
    for dd in spine["day"]]})
# (3) difference array: a user is counted from an active day until 30 days after it, or until their next active day
e = ev.sort_values(["user_id", "day"]).copy()
e["nxt"] = e.groupby("user_id")["day"].shift(-1)
e["end"] = np.minimum(e["day"] + pd.Timedelta(days=30), e["nxt"].fillna(pd.Timestamp.max))
idx = pd.date_range("2024-01-01", "2024-04-30")
delta = pd.Series(0, index=idx, dtype="int64")
delta = delta.add(e.groupby("day").size(), fill_value=0).sub(e.groupby("end").size(), fill_value=0)
diff_df = (delta.cumsum().reindex(spine["day"]).astype(int).rename("rolling_30d_users").reset_index())
# (4) rolling('30D').nunique over events plus one spine row (NaN user) at the end of each day
rows = pd.concat([ev.assign(ts=ev["day"]), pd.DataFrame({"user_id": np.nan, "ts": spine["day"] + pd.Timedelta(hours=23, minutes=59)})])
rows = rows.sort_values("ts", kind="stable")
r = rows.rolling("30D", on="ts")["user_id"].nunique()
roll_df = (rows.assign(n=r)[rows["user_id"].isna()][["ts", "n"]]
              .assign(day=lambda d: d["ts"].dt.normalize())[["day", "n"]]
              .rename(columns={"n": "rolling_30d_users"}).reset_index(drop=True))
roll_df["rolling_30d_users"] = roll_df["rolling_30d_users"].astype(int)
# pd:end
sql_cmp = sql_df.assign(day=pd.to_datetime(sql_df["day"]))
for name, got in [("merge", merge_df), ("sets", sets_df), ("diff array", diff_df), ("rolling.nunique + spine", roll_df)]:
    pd.testing.assert_frame_equal(sql_cmp.sort_values("day").reset_index(drop=True),
                                  got.sort_values("day").reset_index(drop=True), check_dtype=False, check_freq=False)
    print("equal to SQL:", name)
print(sql_df.to_string(index=False))
print("cross-merge rows:", len(spine.merge(ev, how="cross")), "| after window filter:", len(x), "| distinct user-days:", len(ev))
# naive wrong version: rolling('30D').nunique over event rows only, then ffill onto the spine (users never expire on quiet days)
naive = (ev.sort_values("day").rolling("30D", on="day")["user_id"].nunique().groupby(ev.sort_values("day")["day"]).last())
naive = naive.reindex(spine["day"]).ffill().fillna(0).astype(int)
bad = (naive.to_numpy() != sql_df["rolling_30d_users"].to_numpy())
print("days where the event-only rolling + ffill is wrong:", [str(d.date()) for d in spine["day"][bad]])
print("asserts passed")
```

**Output (my run):**
```text
pandas 3.0.5 | Rolling has nunique: True
equal to SQL: merge
equal to SQL: sets
equal to SQL: diff array
equal to SQL: rolling.nunique + spine
       day  rolling_30d_users
2024-03-01                  4
2024-03-02                  4
2024-03-03                  3
2024-03-04                  3
2024-03-05                  3
2024-03-06                  3
2024-03-07                  2
2024-03-08                  2
2024-03-09                  2
2024-03-10                  2
2024-03-11                  2
2024-03-12                  2
2024-03-13                  2
2024-03-14                  2
2024-03-15                  2
2024-03-16                  2
2024-03-17                  2
2024-03-18                  2
2024-03-19                  2
2024-03-20                  3
2024-03-21                  3
2024-03-22                  3
2024-03-23                  3
2024-03-24                  3
2024-03-25                  3
2024-03-26                  3
2024-03-27                  3
2024-03-28                  3
2024-03-29                  3
2024-03-30                  3
2024-03-31                  3
cross-merge rows: 279 | after window filter: 122 | distinct user-days: 9
days where the event-only rolling + ffill is wrong: ['2024-03-03', '2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08', '2024-03-09', '2024-03-10', '2024-03-11', '2024-03-12', '2024-03-13', '2024-03-14']
asserts passed
```

**Edge cases:**
- Several events on the same day (user 3) must be deduplicated to user-days first for the difference array; the merge and set methods are insensitive to it.
- Users inactive for more than 30 days drop out (user 4 after 03-02, user 2 after 03-06 in the toy data) and would count again if they came back; the count is distinct users in the window, not "ever active".
- Days with no events at all still need a row: the spine (and `reindex(..., fill_value=0)`) provides it. The ffill shortcut is wrong on 12 days of my sample (03-03 to 03-14).
- Rolling windows in pandas are right-closed by default: `rolling("30D")` covers `(t - 30 days, t]`. With day-end spine timestamps it equals 30 calendar days; with day-start timestamps ties at the same timestamp matter, so I used 23:59 for the spine rows.
- Time zones: build the day from the timestamp in the reporting zone (Q36) before everything else.

**Then explain:**
- Memory and cost: the spine times events cross merge has days x events rows before filtering (279 in the toy case, 31 x 9). For 31 report days and 100 million events that is billions of rows, so first filter events to the 29-day lookback plus the report range and deduplicate to user-days; the cost then grows with days x user-days in range. The window filter keeps 122 rows here.
- `merge_asof` does not fit directly because it finds one nearest row, not all rows in a window; a per-day set union is simple but loops in Python.
- First-active-date flags for trailing new actives: if the question were "how many users were first active in the last 30 days", compute each user's first active day (`groupby().min()`), then a trailing 30-day sum of daily new-user counts (`rolling(30).sum()` over a gap-free daily series); that works because each user counts once, whereas rolling distinct actives needs the interval logic above.
- A cumulative or windowed `COUNT(DISTINCT ...) OVER` is not allowed in SQLite (DISTINCT is not supported in window functions); the range join is the portable way. Other engines (not executed here) have approximate distinct counts for large data.
- Related: Part 5 Q45 (rolling 7-day active customers) and Part 8 Q33.

**Follow-ups:**
- Rolling 7-day or calendar-month active users? Change 29 to 6, or group by month (Part 6 Q15); state calendar versus rolling.
- At 100 million rows? Pre-aggregate to user-days and use the difference array, or do it in the warehouse with the range join on a user-day table.
- Do you want an approximation? Sketches (HyperLogLog) are available in some warehouses; not executed here.

**Common mistakes:**
- Assuming rolling distinct counts are a one-liner over the event rows and forward-filling quiet days.
- Window off by one (30 days back versus 29).
- Merging the spine with all events and filtering later without bounding the events first.
- Counting events instead of distinct users.
- Dropping days with zero actives.

### Q43 ⭐ 🔴 Funnel drop-off by cohort and device with step lag: users(user_id, signup_date, device), events(user_id, event_ts, event_name) with steps 'signup_done', 'kyc_done', 'first_payment'. Return per signup month and device the users at each step, the step-to-step drop-off and the median hours between kyc_done and first_payment (SQLite has no MEDIAN; use a window ROW_NUMBER approach or NTILE(2), see Part 4). Hedge that the exact median definition (lower, average of two middles) is a choice, handle users who never reach a step (NULL lag, excluded from the median) and cohorts too young to have finished.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and product analytics rounds at product companies and GCCs
**Say this first (1 line):** Pivot the events to one row per user with the first time of each step (`MIN(CASE ...)`), flag the strict chain signup, then KYC, then first payment, count users per step by signup month and device, take drop-off as one minus next over previous, and compute the median hours from KYC to payment with `ROW_NUMBER` and `COUNT` windows over only the users who have both timestamps; I say which median I use and mark cohorts that are too young.

**Schema and sample data:** thirteen users, three signup months, two devices. Questions and assumptions: (1) a user is counted at a step only if they reached the previous step first (strict chain, `kyc_done` not before `signup_done`, `first_payment` not before `kyc_done`); a payment without KYC (user 6) is therefore not counted at the payment step and has no lag; (2) steps are counted as reached by the as-of date 2024-04-05 (fixed, never today), with no per-user time window; (3) a cohort is mature when its month end plus 30 days is on or before the as-of date, so January and February are mature and March is not; (4) the lag is in hours from `kyc_done` to `first_payment`, only for users who have both, and the median is computed over those users; (5) UTC, no test or bot users here (Q37), the month is the signup month, no week bucketing.
- Jan ios (users 1, 2, 3, 4, 13): lags 6 h, 24 h, 72 h and 12 h, user 4 does KYC but never pays (NULL lag). Jan android: user 5 (2 h) and user 6, who pays without KYC. Feb ios: user 7 (2 h) and user 8 (no payment). Feb android: user 9 signs up only, user 10 has a 2 h lag. March: user 11 (1 h lag) and user 12 (signup only).
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, device TEXT);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','ios'),(2,'2024-01-06','ios'),(3,'2024-01-07','ios'),(4,'2024-01-10','ios'),
 (5,'2024-01-12','android'),(6,'2024-01-15','android'),
 (7,'2024-02-03','ios'),(8,'2024-02-04','ios'),(9,'2024-02-10','android'),(10,'2024-02-11','android'),
 (11,'2024-03-05','ios'),(12,'2024-03-06','android'),(13,'2024-01-20','ios');
INSERT INTO events VALUES
 (1,'2024-01-05 10:00:00','signup_done'),(1,'2024-01-05 11:00:00','kyc_done'),(1,'2024-01-05 17:00:00','first_payment'),
 (2,'2024-01-06 10:00:00','signup_done'),(2,'2024-01-06 12:00:00','kyc_done'),(2,'2024-01-07 12:00:00','first_payment'),
 (3,'2024-01-07 10:00:00','signup_done'),(3,'2024-01-07 12:00:00','kyc_done'),(3,'2024-01-10 12:00:00','first_payment'),
 (4,'2024-01-10 10:00:00','signup_done'),(4,'2024-01-10 13:00:00','kyc_done'),
 (5,'2024-01-12 10:00:00','signup_done'),(5,'2024-01-12 14:00:00','kyc_done'),(5,'2024-01-12 16:00:00','first_payment'),
 (6,'2024-01-15 10:00:00','signup_done'),(6,'2024-01-16 10:00:00','first_payment'),
 (7,'2024-02-03 10:00:00','signup_done'),(7,'2024-02-03 12:00:00','kyc_done'),(7,'2024-02-03 14:00:00','first_payment'),
 (8,'2024-02-04 10:00:00','signup_done'),(8,'2024-02-04 12:00:00','kyc_done'),
 (9,'2024-02-10 10:00:00','signup_done'),
 (10,'2024-02-11 10:00:00','signup_done'),(10,'2024-02-11 11:00:00','kyc_done'),(10,'2024-02-11 13:00:00','first_payment'),
 (11,'2024-03-05 10:00:00','signup_done'),(11,'2024-03-05 11:00:00','kyc_done'),(11,'2024-03-05 12:00:00','first_payment'),
 (12,'2024-03-06 10:00:00','signup_done'),
 (13,'2024-01-20 10:00:00','signup_done'),(13,'2024-01-20 11:00:00','kyc_done'),(13,'2024-01-20 23:00:00','first_payment');
```

**SQL answer:** `SQL_MAIN` in the Code block. The median is a pair of columns: `median_lower` takes the row with `rn = (n + 1) / 2` (integer division, so for 4 values it is the 2nd) and `median_avg` averages the rows at `(n + 1) / 2` and `(n + 2) / 2` (the usual statistical median: for 4 values the mean of the 2nd and 3rd, for an odd count the same single row twice):
```sql
WITH t AS (
  SELECT u.user_id, strftime('%Y-%m', u.signup_date) AS cohort, u.device,
         MIN(CASE WHEN e.event_name = 'signup_done'   THEN e.event_ts END) AS t1,
         MIN(CASE WHEN e.event_name = 'kyc_done'      THEN e.event_ts END) AS t2,
         MIN(CASE WHEN e.event_name = 'first_payment' THEN e.event_ts END) AS t3
  FROM users u LEFT JOIN events e ON e.user_id = u.user_id AND e.event_ts <= '2024-04-05 23:59:59'
  GROUP BY u.user_id
), s AS (                                   -- strict chain: each step needs the previous one, in time order
  SELECT cohort, device, user_id,
         COALESCE(t1 IS NOT NULL, 0)                                      AS s1,
         COALESCE(t1 IS NOT NULL AND t2 >= t1, 0)                        AS s2,
         COALESCE(t1 IS NOT NULL AND t2 >= t1 AND t3 >= t2, 0)           AS s3,
         CASE WHEN t2 >= t1 AND t3 >= t2
              THEN (unixepoch(t3) - unixepoch(t2)) / 3600.0 END          AS lag_h
  FROM t
), r AS (
  SELECT cohort, device, lag_h,
         ROW_NUMBER() OVER (PARTITION BY cohort, device ORDER BY lag_h) AS rn,
         COUNT(lag_h)  OVER (PARTITION BY cohort, device)               AS n
  FROM s WHERE lag_h IS NOT NULL
), med AS (
  SELECT cohort, device,
         MAX(CASE WHEN rn = (n + 1) / 2 THEN lag_h END)                          AS median_lower,
         AVG(CASE WHEN rn IN ((n + 1) / 2, (n + 2) / 2) THEN lag_h END)          AS median_avg
  FROM r GROUP BY cohort, device
)
SELECT s.cohort, s.device,
       SUM(s1) AS signup_done, SUM(s2) AS kyc_done, SUM(s3) AS first_payment,
       ROUND(1.0 - 1.0 * SUM(s2) / SUM(s1), 3) AS drop_signup_kyc,
       ROUND(1.0 - 1.0 * SUM(s3) / NULLIF(SUM(s2), 0), 3) AS drop_kyc_payment,
       med.median_lower, med.median_avg,
       CASE WHEN date(s.cohort || '-01', '+1 month', '+30 days') <= '2024-04-05' THEN 1 ELSE 0 END AS mature
FROM s LEFT JOIN med ON med.cohort = s.cohort AND med.device = s.device
GROUP BY s.cohort, s.device
ORDER BY s.cohort, s.device
```
`NTILE(2)` is not a median: for 3 values its first bucket has 2 rows (printed in the Code block), so you would still need the largest value of the lower half and the smallest of the upper half. The ranking and median patterns are in Part 4 (Q21 for `NTILE`, Q38 for a median per group); this answer only reuses them.

**pandas answer:** same logic, shown once here and identical to the Code block (the `median` aggregate skips NaN, which is the "no lag, excluded" rule; the lower median is picked with a sorted `iloc`):
```py
asof = pd.Timestamp("2024-04-05 23:59:59")
ev = events.assign(ts=pd.to_datetime(events["event_ts"]))
ev = ev[ev["ts"] <= asof]
t = (ev.pivot_table(index="user_id", columns="event_name", values="ts", aggfunc="min")
       .reindex(columns=["signup_done", "kyc_done", "first_payment"])
       .rename(columns={"signup_done": "t1", "kyc_done": "t2", "first_payment": "t3"})
       .reindex(users["user_id"]).reset_index())
t = t.merge(users, on="user_id")
t["cohort"] = pd.to_datetime(t["signup_date"]).dt.strftime("%Y-%m")
t["s1"] = t["t1"].notna()
t["s2"] = t["s1"] & (t["t2"] >= t["t1"])
t["s3"] = t["s2"] & (t["t3"] >= t["t2"])
t["lag_h"] = np.where(t["s3"], (t["t3"] - t["t2"]).dt.total_seconds() / 3600.0, np.nan)
g = t.groupby(["cohort", "device"])
pd_df = g.agg(signup_done=("s1", "sum"), kyc_done=("s2", "sum"), first_payment=("s3", "sum"),
              median_avg=("lag_h", "median")).reset_index()
pd_df["median_lower"] = g["lag_h"].apply(lambda s: s.dropna().sort_values().iloc[(len(s.dropna()) - 1) // 2]
                                         if s.notna().any() else np.nan).to_numpy()
pd_df["drop_signup_kyc"] = (1 - pd_df["kyc_done"] / pd_df["signup_done"]).round(3)
pd_df["drop_kyc_payment"] = (1 - pd_df["first_payment"] / pd_df["kyc_done"].replace(0, np.nan)).round(3)
month_end = pd.to_datetime(pd_df["cohort"] + "-01") + pd.offsets.MonthBegin(1)
pd_df["mature"] = ((month_end + pd.Timedelta(days=30)) <= pd.Timestamp("2024-04-05")).astype(int)
pd_df = pd_df[["cohort", "device", "signup_done", "kyc_done", "first_payment", "drop_signup_kyc",
               "drop_kyc_payment", "median_lower", "median_avg", "mature"]]
```

**Example:**
- January ios: 5 users sign up, all 5 reach KYC (drop 0.0), 4 pay (user 4 does not), so KYC to payment drop-off is 1 - 4/5 = 0.2. The lags are 6, 12, 24 and 72 hours: the lower median is 12 h (second value) and the average median is (12 + 24) / 2 = 18 h. This is the case where the definition matters.
- January android: user 5 and user 6 sign up (2), only user 5 does KYC (1, drop 0.5) and pays (drop 0.0, lag 2 h); user 6's payment without KYC is excluded from step 3 and from the lag.
- February ios: 2 sign up, 2 KYC, 1 pays (drop 0.5), median 2 h. February android: 2, 1, 1, medians 2 h.
- March ios: 1, 1, 1, lag 1 h; March android: 1 signup, 0 KYC (drop 1.0), NaN afterwards. Both March rows are marked `mature = 0`: the users have not had 30 days to finish, so the drop-offs are too high and the median hours is biased low (only the fast payers are visible).

**Code:** run with `python3 -I`. The assert compares the SQL and pandas tables after sorting by cohort and device (compared by value; NULL and NaN are treated as equal).
```python
# Q43: signup_done -> kyc_done -> first_payment by signup month and device, with median hours kyc -> payment
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, device TEXT);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','ios'),(2,'2024-01-06','ios'),(3,'2024-01-07','ios'),(4,'2024-01-10','ios'),
 (5,'2024-01-12','android'),(6,'2024-01-15','android'),
 (7,'2024-02-03','ios'),(8,'2024-02-04','ios'),(9,'2024-02-10','android'),(10,'2024-02-11','android'),
 (11,'2024-03-05','ios'),(12,'2024-03-06','android'),(13,'2024-01-20','ios');
INSERT INTO events VALUES
 (1,'2024-01-05 10:00:00','signup_done'),(1,'2024-01-05 11:00:00','kyc_done'),(1,'2024-01-05 17:00:00','first_payment'),
 (2,'2024-01-06 10:00:00','signup_done'),(2,'2024-01-06 12:00:00','kyc_done'),(2,'2024-01-07 12:00:00','first_payment'),
 (3,'2024-01-07 10:00:00','signup_done'),(3,'2024-01-07 12:00:00','kyc_done'),(3,'2024-01-10 12:00:00','first_payment'),
 (4,'2024-01-10 10:00:00','signup_done'),(4,'2024-01-10 13:00:00','kyc_done'),
 (5,'2024-01-12 10:00:00','signup_done'),(5,'2024-01-12 14:00:00','kyc_done'),(5,'2024-01-12 16:00:00','first_payment'),
 (6,'2024-01-15 10:00:00','signup_done'),(6,'2024-01-16 10:00:00','first_payment'),
 (7,'2024-02-03 10:00:00','signup_done'),(7,'2024-02-03 12:00:00','kyc_done'),(7,'2024-02-03 14:00:00','first_payment'),
 (8,'2024-02-04 10:00:00','signup_done'),(8,'2024-02-04 12:00:00','kyc_done'),
 (9,'2024-02-10 10:00:00','signup_done'),
 (10,'2024-02-11 10:00:00','signup_done'),(10,'2024-02-11 11:00:00','kyc_done'),(10,'2024-02-11 13:00:00','first_payment'),
 (11,'2024-03-05 10:00:00','signup_done'),(11,'2024-03-05 11:00:00','kyc_done'),(11,'2024-03-05 12:00:00','first_payment'),
 (12,'2024-03-06 10:00:00','signup_done'),
 (13,'2024-01-20 10:00:00','signup_done'),(13,'2024-01-20 11:00:00','kyc_done'),(13,'2024-01-20 23:00:00','first_payment');
"""
# as-of 2024-04-05; a cohort is mature when its month end plus 30 days is on or before the as-of date
SQL_MAIN = """
WITH t AS (
  SELECT u.user_id, strftime('%Y-%m', u.signup_date) AS cohort, u.device,
         MIN(CASE WHEN e.event_name = 'signup_done'   THEN e.event_ts END) AS t1,
         MIN(CASE WHEN e.event_name = 'kyc_done'      THEN e.event_ts END) AS t2,
         MIN(CASE WHEN e.event_name = 'first_payment' THEN e.event_ts END) AS t3
  FROM users u LEFT JOIN events e ON e.user_id = u.user_id AND e.event_ts <= '2024-04-05 23:59:59'
  GROUP BY u.user_id
), s AS (                                   -- strict chain: each step needs the previous one, in time order
  SELECT cohort, device, user_id,
         COALESCE(t1 IS NOT NULL, 0)                                      AS s1,
         COALESCE(t1 IS NOT NULL AND t2 >= t1, 0)                        AS s2,
         COALESCE(t1 IS NOT NULL AND t2 >= t1 AND t3 >= t2, 0)           AS s3,
         CASE WHEN t2 >= t1 AND t3 >= t2
              THEN (unixepoch(t3) - unixepoch(t2)) / 3600.0 END          AS lag_h
  FROM t
), r AS (
  SELECT cohort, device, lag_h,
         ROW_NUMBER() OVER (PARTITION BY cohort, device ORDER BY lag_h) AS rn,
         COUNT(lag_h)  OVER (PARTITION BY cohort, device)               AS n
  FROM s WHERE lag_h IS NOT NULL
), med AS (
  SELECT cohort, device,
         MAX(CASE WHEN rn = (n + 1) / 2 THEN lag_h END)                          AS median_lower,
         AVG(CASE WHEN rn IN ((n + 1) / 2, (n + 2) / 2) THEN lag_h END)          AS median_avg
  FROM r GROUP BY cohort, device
)
SELECT s.cohort, s.device,
       SUM(s1) AS signup_done, SUM(s2) AS kyc_done, SUM(s3) AS first_payment,
       ROUND(1.0 - 1.0 * SUM(s2) / SUM(s1), 3) AS drop_signup_kyc,
       ROUND(1.0 - 1.0 * SUM(s3) / NULLIF(SUM(s2), 0), 3) AS drop_kyc_payment,
       med.median_lower, med.median_avg,
       CASE WHEN date(s.cohort || '-01', '+1 month', '+30 days') <= '2024-04-05' THEN 1 ELSE 0 END AS mature
FROM s LEFT JOIN med ON med.cohort = s.cohort AND med.device = s.device
GROUP BY s.cohort, s.device
ORDER BY s.cohort, s.device
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("NTILE(2) is not a median: first NTILE(2) bucket of 3 values has", con.execute(
    "SELECT COUNT(*) FROM (SELECT NTILE(2) OVER (ORDER BY x) AS b FROM (SELECT 6 AS x UNION ALL SELECT 24 UNION ALL SELECT 72)) WHERE b=1").fetchone()[0], "rows")
print("integer division 7/2 in SQLite:", con.execute("SELECT 7/2, 8/2, (3+1)/2, (3+2)/2").fetchone())

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
asof = pd.Timestamp("2024-04-05 23:59:59")
ev = events.assign(ts=pd.to_datetime(events["event_ts"]))
ev = ev[ev["ts"] <= asof]
t = (ev.pivot_table(index="user_id", columns="event_name", values="ts", aggfunc="min")
       .reindex(columns=["signup_done", "kyc_done", "first_payment"])
       .rename(columns={"signup_done": "t1", "kyc_done": "t2", "first_payment": "t3"})
       .reindex(users["user_id"]).reset_index())
t = t.merge(users, on="user_id")
t["cohort"] = pd.to_datetime(t["signup_date"]).dt.strftime("%Y-%m")
t["s1"] = t["t1"].notna()
t["s2"] = t["s1"] & (t["t2"] >= t["t1"])
t["s3"] = t["s2"] & (t["t3"] >= t["t2"])
t["lag_h"] = np.where(t["s3"], (t["t3"] - t["t2"]).dt.total_seconds() / 3600.0, np.nan)
g = t.groupby(["cohort", "device"])
pd_df = g.agg(signup_done=("s1", "sum"), kyc_done=("s2", "sum"), first_payment=("s3", "sum"),
              median_avg=("lag_h", "median")).reset_index()
pd_df["median_lower"] = g["lag_h"].apply(lambda s: s.dropna().sort_values().iloc[(len(s.dropna()) - 1) // 2]
                                         if s.notna().any() else np.nan).to_numpy()
pd_df["drop_signup_kyc"] = (1 - pd_df["kyc_done"] / pd_df["signup_done"]).round(3)
pd_df["drop_kyc_payment"] = (1 - pd_df["first_payment"] / pd_df["kyc_done"].replace(0, np.nan)).round(3)
month_end = pd.to_datetime(pd_df["cohort"] + "-01") + pd.offsets.MonthBegin(1)
pd_df["mature"] = ((month_end + pd.Timedelta(days=30)) <= pd.Timestamp("2024-04-05")).astype(int)
pd_df = pd_df[["cohort", "device", "signup_done", "kyc_done", "first_payment", "drop_signup_kyc",
               "drop_kyc_payment", "median_lower", "median_avg", "mature"]]
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.sort_values(["cohort", "device"]).reset_index(drop=True),
                              pd_df.sort_values(["cohort", "device"]).reset_index(drop=True), check_dtype=False)
print("asserts passed")
```

**Output (my run):**
```text
 cohort  device  signup_done  kyc_done  first_payment  drop_signup_kyc  drop_kyc_payment  median_lower  median_avg  mature
2024-01 android            2         1              1              0.5               0.0           2.0         2.0       1
2024-01     ios            5         5              4              0.0               0.2          12.0        18.0       1
2024-02 android            2         1              1              0.5               0.0           2.0         2.0       1
2024-02     ios            2         2              1              0.0               0.5           2.0         2.0       1
2024-03 android            1         0              0              1.0               NaN           NaN         NaN       0
2024-03     ios            1         1              1              0.0               0.0           1.0         1.0       0
NTILE(2) is not a median: first NTILE(2) bucket of 3 values has 2 rows
integer division 7/2 in SQLite: (3, 4, 2, 2)
 cohort  device  signup_done  kyc_done  first_payment  drop_signup_kyc  drop_kyc_payment  median_lower  median_avg  mature
2024-01 android            2         1              1              0.5               0.0           2.0         2.0       1
2024-01     ios            5         5              4              0.0               0.2          12.0        18.0       1
2024-02 android            2         1              1              0.5               0.0           2.0         2.0       1
2024-02     ios            2         2              1              0.0               0.5           2.0         2.0       1
2024-03 android            1         0              0              1.0               NaN           NaN         NaN       0
2024-03     ios            1         1              1              0.0               0.0           1.0         1.0       0
asserts passed
```

**Edge cases:**
- Users who never reach a step: their timestamp is NULL, the lag is NULL, `COUNT(lag_h)` and the median ignore them. A `LEFT JOIN` from users keeps users with no events at all (user 9 and 12 still count at signup).
- A group where nobody reaches the step (March android): the median is NULL in SQL and NaN in pandas, and the drop-off to payment uses `NULLIF` or `replace(0, nan)` to avoid division by zero.
- Immature cohorts: report them but flag them, or exclude them from comparisons; do not read their drop-off as final.
- Median definition: lower median (the value at position (n + 1) / 2), average of the two middles (the statistical default, and what pandas `median` returns), or an interpolated percentile (what `PERCENTILE_CONT` does in PostgreSQL; not executed here). In my data they differ only for an even count (12 h against 18 h).
- Hours via `unixepoch` differences divided by 3600.0 are exact for whole seconds; `julianday` differences times 24 are floats that are not exact (Part 7 lesson).
- Right censoring again: the median among those who paid is not the median time to pay of everyone; say so.

**Then explain:**
- Step counts use a strict chain so the funnel is monotone; counting each step on its own would give a bigger payment step than KYC step for users like user 6.
- SQLite integer division: `(n + 1) / 2` is integer division on integers (the Code block prints `7/2` as 3), which is what makes the rank trick work; in PostgreSQL integer division also truncates, in other engines it can return a decimal (hedge: not executed here), so cast explicitly.
- No `MEDIAN` function in SQLite: use window ranks (this answer), or `PERCENTILE_CONT` in PostgreSQL and Snowflake and `PERCENTILE_CONT ... OVER` in BigQuery (not executed here).
- The per-device cut shows whether the drop-off is a product problem on one platform (a device-specific bug) rather than everywhere.

**Follow-ups:**
- Median per cohort only? Drop `device` from the partition and the `GROUP BY`.
- Want the 90th percentile? `rn = CEIL(0.9 * n)` with a nearest-rank convention (Part 4 Q41).
- Time-bounded steps (within 7 days of signup)? Add the bound to the step flags, as in Q17.

**Common mistakes:**
- Taking `AVG` of the hours and calling it the median (skewed by the 72 h user: 28.5 h average against 18 h median in January ios).
- Computing the lag for users without KYC or payment (NULL arithmetic or a wrong default of 0).
- Dividing by zero in empty groups.
- Treating young cohorts as final.
- `NTILE(2)` as a median.

### Q44 ⭐ 🔴 Experiment contamination and late conversions: experiments(user_id, arm, assigned_ts) where some users appear in both arms or are assigned twice, orders(order_id, user_id, order_ts, amount, status) and a 14-day conversion window per user after assignment. Return per arm the clean assigned users (first assignment only, users in both arms removed and counted separately), conversions inside the window, conversion rate and uplift, and the same table without cleaning to show the bias. Report the excluded counts as their own rows. Statistical testing is out of scope (Book 1 and Book 6).
**Asked at:** experiment-metrics guides (PracHub and Statsig SRM pages and abtestly docs, search snippets only, not opened; SRM is a chi-square goodness-of-fit on distinct-user counts against the planned split, strict thresholds such as p < 0.001 in practice); the statistics belong to Book 1 and Book 6 and this question stays on counts, rates and uplift in SQL; guides, not candidate reports; experimentation and data scientist rounds
**Say this first (1 line):** Collapse the assignment log to one row per user (first assignment), remove and count separately the users who appear in both arms, also set aside users whose 14-day window is not yet closed at the as-of date, then count completed orders from `assigned_ts` up to but not including `assigned_ts + 14 days`, per arm; show the same table without cleaning next to it to see the bias, and leave the significance test to Book 1 and Book 6.
**Schema and sample data:** fourteen users, seventeen assignment rows, twelve orders. Clarifying questions and assumptions: (1) the unit is the user, and the first assignment time starts the clock; (2) "in both arms" means the log has the user in control and in treatment at any time; those users are excluded and reported as their own row, not silently dropped; (3) a conversion is at least one completed order with `assigned_ts <= order_ts < assigned_ts + 14 days` (an order exactly 14 days later is outside; I state it because the boundary changes counts); (4) as-of date 2024-03-25 (fixed): a user is immature when the 14 days after assignment are not finished by 2024-03-25 00:00; immature users are reported in their own row, not counted as non-converters; (5) cancelled orders do not count; (6) UTC, no test or bot filter here (Q37), no week bucketing; (7) counts and rates only, the sample is far too small to say anything statistical.
- User 3 and user 13 are assigned twice in the same arm. User 4 is in control and later in treatment. User 5 ordered before assignment. User 6's order is cancelled. User 3's order is on day 15 (late). User 7's order is exactly 14 days after assignment. Users 9 and 10 were assigned on 20 and 21 March (window not closed at the as-of date); user 9 already has an order. User 12 has two orders and counts once.
```sql
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 10:00:00'),(2,'treatment','2024-03-01 10:00:00'),
 (3,'control','2024-03-01 10:00:00'),(3,'control','2024-03-03 10:00:00'),
 (4,'control','2024-03-02 10:00:00'),(4,'treatment','2024-03-04 10:00:00'),
 (5,'treatment','2024-03-02 10:00:00'),(6,'control','2024-03-02 10:00:00'),
 (7,'treatment','2024-03-02 10:00:00'),(8,'treatment','2024-03-03 10:00:00'),
 (9,'control','2024-03-20 10:00:00'),(10,'treatment','2024-03-21 10:00:00'),
 (11,'control','2024-03-05 10:00:00'),(12,'treatment','2024-03-05 10:00:00'),
 (13,'treatment','2024-03-06 10:00:00'),(13,'treatment','2024-03-07 10:00:00'),
 (14,'control','2024-03-03 10:00:00');
INSERT INTO orders VALUES
 (1,1,'2024-03-03 09:00:00',100,'completed'),(2,2,'2024-03-04 09:00:00',100,'completed'),
 (3,3,'2024-03-16 12:00:00',100,'completed'),(4,4,'2024-03-05 09:00:00',100,'completed'),
 (5,5,'2024-03-01 09:00:00',100,'completed'),(6,6,'2024-03-04 09:00:00',100,'cancelled'),
 (7,7,'2024-03-16 10:00:00',100,'completed'),(8,8,'2024-03-10 09:00:00',100,'completed'),
 (9,9,'2024-03-22 09:00:00',100,'completed'),(10,12,'2024-03-06 09:00:00',100,'completed'),
 (11,12,'2024-03-07 09:00:00',100,'completed'),(12,13,'2024-03-08 09:00:00',100,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block (`per` counts rows and distinct arms per user, `fa` keeps the first assignment with `ROW_NUMBER`, `f` classifies each user as clean, both_arms or immature, `c` adds the conversion flag with `EXISTS`, then the arm rows and the excluded rows are stacked with `UNION ALL`):
```sql
WITH per AS (
  SELECT user_id, COUNT(*) AS n_rows, COUNT(DISTINCT arm) AS n_arms, MIN(assigned_ts) AS first_ts
  FROM experiments GROUP BY user_id
), fa AS (
  SELECT x.user_id, x.arm, x.assigned_ts, per.n_rows, per.n_arms,
         ROW_NUMBER() OVER (PARTITION BY x.user_id ORDER BY x.assigned_ts) AS rn
  FROM experiments x JOIN per ON per.user_id = x.user_id
), f AS (
  SELECT user_id, arm, assigned_ts, n_rows, n_arms,
         CASE WHEN n_arms > 1 THEN 'both_arms'
              WHEN unixepoch(assigned_ts) + 14 * 86400 > unixepoch('2024-03-25 00:00:00') THEN 'immature'
              ELSE 'clean' END AS status
  FROM fa WHERE rn = 1
), c AS (
  SELECT f.*, EXISTS (SELECT 1 FROM orders o WHERE o.user_id = f.user_id AND o.status = 'completed'
                      AND o.order_ts >= f.assigned_ts
                      AND unixepoch(o.order_ts) < unixepoch(f.assigned_ts) + 14 * 86400) AS conv
  FROM f
)
SELECT grp, users, conversions, conv_rate FROM (
  SELECT CASE arm WHEN 'control' THEN 0 ELSE 1 END AS ord, arm AS grp, COUNT(*) AS users,
         SUM(conv) AS conversions, ROUND(1.0 * SUM(conv) / COUNT(*), 4) AS conv_rate
  FROM c WHERE status = 'clean' GROUP BY arm
  UNION ALL SELECT 2, 'excluded_both_arms', COUNT(*), NULL, NULL FROM c WHERE status = 'both_arms'
  UNION ALL SELECT 3, 'excluded_immature', COUNT(*), NULL, NULL FROM c WHERE status = 'immature'
  UNION ALL SELECT 4, 'dropped_duplicate_rows', SUM(n_rows - 1), NULL, NULL FROM c WHERE status <> 'both_arms'
) ORDER BY ord
```
`SQL_DIRTY` in the Code block is the uncleaned version: every assignment row is a "user", the window is applied per row, immature windows are included.

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
ex = experiments.assign(ts=pd.to_datetime(experiments["assigned_ts"]))
oc = orders[orders["status"].eq("completed")].assign(ots=pd.to_datetime(orders["order_ts"]))
per = ex.groupby("user_id").agg(n_rows=("arm", "size"), n_arms=("arm", "nunique")).reset_index()
first = ex.sort_values(["user_id", "ts"], kind="stable").drop_duplicates("user_id").merge(per, on="user_id")
first["status"] = "clean"
first.loc[first["ts"] + pd.Timedelta(days=14) > pd.Timestamp("2024-03-25"), "status"] = "immature"
first.loc[first["n_arms"] > 1, "status"] = "both_arms"
def converted(frame):
    m = frame[["user_id", "ts"]].reset_index().merge(oc[["user_id", "ots"]], on="user_id", how="left")
    ok = m[(m["ots"] >= m["ts"]) & (m["ots"] < m["ts"] + pd.Timedelta(days=14))]
    return frame.index.isin(ok["index"])
first["conv"] = converted(first)
clean = first[first["status"].eq("clean")]
arm_rows = (clean.groupby("arm").agg(users=("user_id", "size"), conversions=("conv", "sum")).reset_index()
                 .rename(columns={"arm": "grp"}))
arm_rows["conv_rate"] = (arm_rows["conversions"] / arm_rows["users"]).round(4)
extra = pd.DataFrame({"grp": ["excluded_both_arms", "excluded_immature", "dropped_duplicate_rows"],
                      "users": [int(first["status"].eq("both_arms").sum()), int(first["status"].eq("immature").sum()),
                                int((first.loc[first["status"].ne("both_arms"), "n_rows"] - 1).sum())]})
pd_df = pd.concat([arm_rows, extra], ignore_index=True)
ex["conv"] = converted(ex)
pd_dirty = (ex.groupby("arm").agg(rows_as_users=("user_id", "size"), conversions=("conv", "sum")).reset_index()
              .rename(columns={"arm": "grp"}))
pd_dirty["conv_rate"] = (pd_dirty["conversions"] / pd_dirty["rows_as_users"]).round(4)
```

**Example:**
- Clean assigned users (first assignment only, one arm, window closed): control users 1, 3, 6, 11, 14 = 5; treatment users 2, 5, 7, 8, 12, 13 = 6. User 4 (both arms) is excluded and counted in `excluded_both_arms` = 1. Users 9 and 10 are `excluded_immature` = 2. Duplicate assignment rows dropped (users 3 and 13) = 2.
- Control conversions: user 1 (order on day 2) = 1; user 3's order is on day 15 (late, no), user 6's is cancelled, users 11 and 14 have none. Rate 1 / 5 = 0.2.
- Treatment conversions: users 2, 8, 12, 13 = 4; user 5's order is before assignment, user 7's is exactly at 14 days (outside). Rate 4 / 6 = 0.6667.
- Uplift: 0.4667 absolute, 233.3 percent relative (a toy number; real data would be small percentages).
- Without cleaning: control has 8 rows (user 3 twice, user 4's control row, immature user 9) and 4 conversions, because user 3's second assignment (03-03) opens a new window that reaches the 16 March order, user 4 counts, and user 9 converts early: 0.5. Treatment has 9 rows and 6 conversions (user 4 again, user 13 twice): 0.6667. The uplift shrinks from 0.4667 to 0.1667 (33.3 percent relative): the control rate is inflated by duplicated and contaminated users and the comparison is no longer between independent groups. Direction and size of the bias depend on the data; here it hides most of the effect.

**Code:** run with `python3 -I`. The asserts compare SQL with pandas for the clean table (in the printed row order: control, treatment, then the excluded rows) and for the dirty table (ordered by arm).
```python
# Q44: experiment contamination, first assignment only, 14-day window, excluded counts as rows, dirty versus clean
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 10:00:00'),(2,'treatment','2024-03-01 10:00:00'),
 (3,'control','2024-03-01 10:00:00'),(3,'control','2024-03-03 10:00:00'),
 (4,'control','2024-03-02 10:00:00'),(4,'treatment','2024-03-04 10:00:00'),
 (5,'treatment','2024-03-02 10:00:00'),(6,'control','2024-03-02 10:00:00'),
 (7,'treatment','2024-03-02 10:00:00'),(8,'treatment','2024-03-03 10:00:00'),
 (9,'control','2024-03-20 10:00:00'),(10,'treatment','2024-03-21 10:00:00'),
 (11,'control','2024-03-05 10:00:00'),(12,'treatment','2024-03-05 10:00:00'),
 (13,'treatment','2024-03-06 10:00:00'),(13,'treatment','2024-03-07 10:00:00'),
 (14,'control','2024-03-03 10:00:00');
INSERT INTO orders VALUES
 (1,1,'2024-03-03 09:00:00',100,'completed'),(2,2,'2024-03-04 09:00:00',100,'completed'),
 (3,3,'2024-03-16 12:00:00',100,'completed'),(4,4,'2024-03-05 09:00:00',100,'completed'),
 (5,5,'2024-03-01 09:00:00',100,'completed'),(6,6,'2024-03-04 09:00:00',100,'cancelled'),
 (7,7,'2024-03-16 10:00:00',100,'completed'),(8,8,'2024-03-10 09:00:00',100,'completed'),
 (9,9,'2024-03-22 09:00:00',100,'completed'),(10,12,'2024-03-06 09:00:00',100,'completed'),
 (11,12,'2024-03-07 09:00:00',100,'completed'),(12,13,'2024-03-08 09:00:00',100,'completed');
"""
# as-of 2024-03-25: an assignment is mature when assigned_ts + 14 days <= as-of end of day 2024-03-25 00:00
SQL_MAIN = """
WITH per AS (
  SELECT user_id, COUNT(*) AS n_rows, COUNT(DISTINCT arm) AS n_arms, MIN(assigned_ts) AS first_ts
  FROM experiments GROUP BY user_id
), fa AS (
  SELECT x.user_id, x.arm, x.assigned_ts, per.n_rows, per.n_arms,
         ROW_NUMBER() OVER (PARTITION BY x.user_id ORDER BY x.assigned_ts) AS rn
  FROM experiments x JOIN per ON per.user_id = x.user_id
), f AS (
  SELECT user_id, arm, assigned_ts, n_rows, n_arms,
         CASE WHEN n_arms > 1 THEN 'both_arms'
              WHEN unixepoch(assigned_ts) + 14 * 86400 > unixepoch('2024-03-25 00:00:00') THEN 'immature'
              ELSE 'clean' END AS status
  FROM fa WHERE rn = 1
), c AS (
  SELECT f.*, EXISTS (SELECT 1 FROM orders o WHERE o.user_id = f.user_id AND o.status = 'completed'
                      AND o.order_ts >= f.assigned_ts
                      AND unixepoch(o.order_ts) < unixepoch(f.assigned_ts) + 14 * 86400) AS conv
  FROM f
)
SELECT grp, users, conversions, conv_rate FROM (
  SELECT CASE arm WHEN 'control' THEN 0 ELSE 1 END AS ord, arm AS grp, COUNT(*) AS users,
         SUM(conv) AS conversions, ROUND(1.0 * SUM(conv) / COUNT(*), 4) AS conv_rate
  FROM c WHERE status = 'clean' GROUP BY arm
  UNION ALL SELECT 2, 'excluded_both_arms', COUNT(*), NULL, NULL FROM c WHERE status = 'both_arms'
  UNION ALL SELECT 3, 'excluded_immature', COUNT(*), NULL, NULL FROM c WHERE status = 'immature'
  UNION ALL SELECT 4, 'dropped_duplicate_rows', SUM(n_rows - 1), NULL, NULL FROM c WHERE status <> 'both_arms'
) ORDER BY ord
"""
SQL_DIRTY = """
SELECT x.arm AS grp, COUNT(*) AS rows_as_users,
       SUM(EXISTS (SELECT 1 FROM orders o WHERE o.user_id = x.user_id AND o.status = 'completed'
                   AND o.order_ts >= x.assigned_ts
                   AND unixepoch(o.order_ts) < unixepoch(x.assigned_ts) + 14 * 86400)) AS conversions,
       ROUND(1.0 * SUM(EXISTS (SELECT 1 FROM orders o WHERE o.user_id = x.user_id AND o.status = 'completed'
                   AND o.order_ts >= x.assigned_ts
                   AND unixepoch(o.order_ts) < unixepoch(x.assigned_ts) + 14 * 86400)) / COUNT(*), 4) AS conv_rate
FROM experiments x GROUP BY x.arm ORDER BY x.arm
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("clean table with excluded rows:"); print(sql_df.to_string(index=False))
dirty = pd.read_sql_query(SQL_DIRTY, con)
print("no cleaning (every assignment row, immature windows included):"); print(dirty.to_string(index=False))
cl = sql_df.set_index("grp")
print("clean: absolute uplift %.4f, relative uplift %.1f%%" % (
    cl.loc["treatment", "conv_rate"] - cl.loc["control", "conv_rate"],
    100 * (cl.loc["treatment", "conv_rate"] / cl.loc["control", "conv_rate"] - 1)))
d = dirty.set_index("grp")
print("dirty: absolute uplift %.4f, relative uplift %.1f%%" % (
    d.loc["treatment", "conv_rate"] - d.loc["control", "conv_rate"],
    100 * (d.loc["treatment", "conv_rate"] / d.loc["control", "conv_rate"] - 1)))

experiments = pd.read_sql_query("SELECT * FROM experiments", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
ex = experiments.assign(ts=pd.to_datetime(experiments["assigned_ts"]))
oc = orders[orders["status"].eq("completed")].assign(ots=pd.to_datetime(orders["order_ts"]))
per = ex.groupby("user_id").agg(n_rows=("arm", "size"), n_arms=("arm", "nunique")).reset_index()
first = ex.sort_values(["user_id", "ts"], kind="stable").drop_duplicates("user_id").merge(per, on="user_id")
first["status"] = "clean"
first.loc[first["ts"] + pd.Timedelta(days=14) > pd.Timestamp("2024-03-25"), "status"] = "immature"
first.loc[first["n_arms"] > 1, "status"] = "both_arms"
def converted(frame):
    m = frame[["user_id", "ts"]].reset_index().merge(oc[["user_id", "ots"]], on="user_id", how="left")
    ok = m[(m["ots"] >= m["ts"]) & (m["ots"] < m["ts"] + pd.Timedelta(days=14))]
    return frame.index.isin(ok["index"])
first["conv"] = converted(first)
clean = first[first["status"].eq("clean")]
arm_rows = (clean.groupby("arm").agg(users=("user_id", "size"), conversions=("conv", "sum")).reset_index()
                 .rename(columns={"arm": "grp"}))
arm_rows["conv_rate"] = (arm_rows["conversions"] / arm_rows["users"]).round(4)
extra = pd.DataFrame({"grp": ["excluded_both_arms", "excluded_immature", "dropped_duplicate_rows"],
                      "users": [int(first["status"].eq("both_arms").sum()), int(first["status"].eq("immature").sum()),
                                int((first.loc[first["status"].ne("both_arms"), "n_rows"] - 1).sum())]})
pd_df = pd.concat([arm_rows, extra], ignore_index=True)
ex["conv"] = converted(ex)
pd_dirty = (ex.groupby("arm").agg(rows_as_users=("user_id", "size"), conversions=("conv", "sum")).reset_index()
              .rename(columns={"arm": "grp"}))
pd_dirty["conv_rate"] = (pd_dirty["conversions"] / pd_dirty["rows_as_users"]).round(4)
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # same fixed row order (control, treatment, excluded rows)
pd.testing.assert_frame_equal(dirty, pd_dirty, check_dtype=False)  # ordered by arm
print("asserts passed")
```

**Output (my run):**
```text
clean table with excluded rows:
                   grp  users  conversions  conv_rate
               control      5          1.0     0.2000
             treatment      6          4.0     0.6667
    excluded_both_arms      1          NaN        NaN
     excluded_immature      2          NaN        NaN
dropped_duplicate_rows      2          NaN        NaN
no cleaning (every assignment row, immature windows included):
      grp  rows_as_users  conversions  conv_rate
  control              8            4     0.5000
treatment              9            6     0.6667
clean: absolute uplift 0.4667, relative uplift 233.3%
dirty: absolute uplift 0.1667, relative uplift 33.3%
                   grp  users  conversions  conv_rate
               control      5          1.0     0.2000
             treatment      6          4.0     0.6667
    excluded_both_arms      1          NaN        NaN
     excluded_immature      2          NaN        NaN
dropped_duplicate_rows      2          NaN        NaN
asserts passed
```

**Edge cases:**
- A user assigned twice to the same arm is one user; the second assignment must not reset the clock (user 3 would otherwise convert).
- Users in both arms cannot be assigned to either; excluding them is the standard choice, but report how many (here 1 of 14), because a large number is a bug in assignment, not a data nuisance. A sample ratio check on the counts is in Q32.
- Late conversions: an order after the window (day 15, or exactly day 14 here) is not a conversion; widening the window changes the rate, so state it and fix it before looking at results.
- Immature users: counting them as non-converters biases the rate down; excluding them, as here, means the table changes as the as-of date moves. Report the row.
- Orders before assignment are not conversions (user 5).
- A user whose order is cancelled stays assigned and unconverted.

**Then explain:**
- Why first assignment only: the exposure time defines the window; a later duplicate assignment is a logging artefact or a re-randomisation, and counting it makes one user into two with an overlapping window.
- Why users in both arms are removed: they were exposed to both treatments, so their outcome cannot be attributed; keep them as a counted row so the reader sees the size of the problem.
- The uncleaned table is the check that cleaning matters: different denominators (8 and 9 instead of 5 and 6) and different numerators.
- Dialects (not executed here): the same pattern works in PostgreSQL, BigQuery and Snowflake with `INTERVAL '14 days'` or `DATE_ADD`/`TIMESTAMP_ADD`; `COUNT(DISTINCT arm)` as the both-arms test is portable.

**Follow-ups:**
- How do you test the difference? Out of scope here: Book 1 (testing) and Book 6 (experiment design).
- What if assignment is by session or device rather than user? Then the unit changes; ask what the randomisation unit is.
- Do you want per-day cumulative conversion? Use days since assignment as a group key and a cumulative sum (Part 5).

**Common mistakes:**
- Joining orders to the raw assignment table (duplicate rows multiply conversions).
- Counting an order from before assignment or after the window.
- Silently dropping contaminated users without reporting how many.
- Counting immature users as non-converters.
- Using `BETWEEN` on the window and including the exact end.

### Q45 ⭐ 🔴 Linear and time-decay multi-touch attribution: touches(user_id, touch_ts, channel) and orders(order_id, user_id, order_ts, amount, status). For each completed order split its amount equally across all touches by the same user in the 30 days before the order (linear), and also with weights proportional to 0.5 raised to the touch age in days divided by 7 (time decay, SQLite power via a precomputed exp/ln or a LUT; state what you used). Return revenue by channel for both, assert that each model sums back to completed revenue, and handle orders with no touches (the unattributed row) without dividing by zero.
**Asked at:** attribution guides (Cometly multi-touch SQL post, oneuptime ClickHouse attribution post, Adobe and Amplitude docs; search snippets only, not opened; linear = equal credit per touch, first touch = full credit to the earliest touch in the lookback window); vendor guides, not candidate reports; marketing analytics and growth analyst rounds
**Say this first (1 line):** Join each completed order to the same user's touches in the 30 days up to the order, give each touch a weight (linear: 1 divided by the number of touches; time decay: 0.5 to the power of age in days divided by 7, then divided by the sum of weights of that order), sum amount times weight by channel, and add an explicit `unattributed` row for completed orders with no touch so both models add back to completed revenue.

**Schema and sample data:** eight touches, five orders. Questions and assumptions: (1) the lookback is 30 days measured back from the order time, inclusive of the boundary (`<= 30 * 86400` seconds), and a touch at the same instant as the order counts (`touch_ts <= order_ts`); (2) a touch after the order never counts; (3) only completed orders carry revenue, so the cancelled order (4) is excluded; (4) time decay uses a half-life of 7 days: the weight is `0.5 ^ (age_days / 7)`, with the age measured in fractional days from seconds; (5) several touches by the same channel are separate touches (each gets its own weight, then they add up by channel); (6) UTC, no test or bot filter in this schema (Q37), no week bucketing; (7) this is attribution as arithmetic, not causal impact.
- Order 1 (user 1, 120): touches at 31 days (outside), 29 days (ads), 7 days (email) and 1 hour (search) before the order. Order 2 (user 2, 60): ads 7 days before and social at the same instant as the order. Order 3 (user 3, 80): no touches at all. Order 4 (cancelled). Order 5 (user 5, 90): its only touch is after the order.
```sql
CREATE TABLE touches(user_id INTEGER, touch_ts TEXT, channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO touches VALUES
 (1,'2024-02-28 10:00:00','social'),(1,'2024-03-02 10:00:00','ads'),(1,'2024-03-24 10:00:00','email'),(1,'2024-03-31 09:00:00','search'),
 (2,'2024-03-10 12:00:00','ads'),(2,'2024-03-17 12:00:00','social'),
 (4,'2024-03-18 12:00:00','ads'),(5,'2024-03-25 12:00:00','email');
INSERT INTO orders VALUES
 (1,1,'2024-03-31 10:00:00',120,'completed'),(2,2,'2024-03-17 12:00:00',60,'completed'),
 (3,3,'2024-03-20 12:00:00',80,'completed'),(4,4,'2024-03-20 12:00:00',500,'cancelled'),
 (5,5,'2024-03-20 12:00:00',90,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block. The model weights are normalised per order with window functions over `order_id`. The `unattributed` row comes from orders with no joined touch, so there is never a division by a zero count or a zero weight sum (the orders simply have no row in the weight CTEs):
```sql
WITH j AS (                                  -- touches in the 30 days up to and including the order time
  SELECT o.order_id, o.amount, t.channel,
         (unixepoch(o.order_ts) - unixepoch(t.touch_ts)) / 86400.0 AS age_days
  FROM orders o JOIN touches t
    ON t.user_id = o.user_id
   AND t.touch_ts <= o.order_ts
   AND unixepoch(o.order_ts) - unixepoch(t.touch_ts) <= 30 * 86400
  WHERE o.status = 'completed'
), w AS (
  SELECT order_id, amount, channel, power(0.5, age_days / 7.0) AS decay_w FROM j
), s AS (
  SELECT order_id, amount, channel,
         1.0 / COUNT(*) OVER (PARTITION BY order_id)                 AS lin_w,
         decay_w / SUM(decay_w) OVER (PARTITION BY order_id)         AS dec_w
  FROM w
)
SELECT channel, ROUND(SUM(amount * lin_w), 4) AS linear, ROUND(SUM(amount * dec_w), 4) AS time_decay
FROM s GROUP BY channel
UNION ALL
SELECT 'unattributed', SUM(amount), SUM(amount)
FROM orders o WHERE o.status = 'completed' AND NOT EXISTS (SELECT 1 FROM j WHERE j.order_id = o.order_id)
ORDER BY channel
```
Power in SQLite: this Python's SQLite 3.45.1 was built with the math functions (the compile option check prints 1 in my run), so `power(0.5, x)` works; builds without them have no `power` or `exp`. The fallback in the Code block is a lookup table `lut(age_day, w)` of weights for whole days 0 to 30 built outside SQL (in the Code block from Python); an alternative would be `exp(-age_days * ln(2) / 7)` if `exp` and `ln` exist, which has the same dependency. The lookup table truncates the age to whole days, so it is slightly different (printed below). Other engines (not executed here) have `POWER` or `POW`.

**pandas answer:** same logic with a merge, filter and `groupby().transform`, shown once here and identical to the Code block:
```py
o = orders[orders["status"].eq("completed")].assign(ots=pd.to_datetime(orders["order_ts"]))
t = touches.assign(tts=pd.to_datetime(touches["touch_ts"]))
j = o.merge(t, on="user_id")
j["age_days"] = (j["ots"] - j["tts"]).dt.total_seconds() / 86400.0
j = j[(j["tts"] <= j["ots"]) & (j["age_days"] <= 30)].copy()
j["lin_w"] = 1.0 / j.groupby("order_id")["order_id"].transform("size")
j["decay_w"] = 0.5 ** (j["age_days"] / 7.0)
j["dec_w"] = j["decay_w"] / j.groupby("order_id")["decay_w"].transform("sum")
by_ch = (j.assign(linear=j["amount"] * j["lin_w"], time_decay=j["amount"] * j["dec_w"])
           .groupby("channel", as_index=False)[["linear", "time_decay"]].sum())
unatt = o.loc[~o["order_id"].isin(j["order_id"]), "amount"].sum()
pd_df = pd.concat([by_ch, pd.DataFrame({"channel": ["unattributed"], "linear": [unatt], "time_decay": [unatt]})],
                  ignore_index=True).sort_values("channel").reset_index(drop=True)
pd_df[["linear", "time_decay"]] = pd_df[["linear", "time_decay"]].round(4)
```

**Example:**
- Linear: order 1 has 3 touches in the window (ads, email, search), 40 each; order 2 has 2 touches (ads, social), 30 each. Order 3 and order 5 are unattributed (80 + 90 = 170). By channel: ads 70, email 40, search 40, social 30, unattributed 170, total 350 = completed revenue (120 + 60 + 80 + 90).
- Time decay, order 1: ages 29 days, 7 days and 1 hour (0.0417 days), weights 0.0567, 0.5 and 0.9959, sum 1.5526, so normalised shares 0.0365, 0.3221 and 0.6415 and amounts 4.38 (ads), 38.65 (email), 76.98 (search). Order 2: ages 7 days and 0, weights 0.5 and 1, shares 1/3 and 2/3, so ads 20 and social 40. By channel: ads 24.3755, email 38.6476, search 76.9769, social 40, unattributed 170; the total is again 350.
- The two models disagree most for search (40 under linear, 76.98 under time decay) because that touch happened an hour before the order, and for ads (70 against 24.38) because its touches were old.
- LUT fallback: ages are cut to whole days (29, 7, 0), giving slightly different numbers (for example ads 24.3639, search 77.0907); the largest difference to the exact weights is 0.1138 here.

**Code:** run with `python3 -I`. Asserts: the SQL and pandas tables are equal after sorting by channel (compared by value, rounded to 4 decimals), and both models sum to completed revenue with a tolerance of 1e-6 (floats).
```python
# Q45: linear and time-decay (half-life 7 days) multi-touch attribution, 30-day lookback, unattributed row
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE touches(user_id INTEGER, touch_ts TEXT, channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO touches VALUES
 (1,'2024-02-28 10:00:00','social'),(1,'2024-03-02 10:00:00','ads'),(1,'2024-03-24 10:00:00','email'),(1,'2024-03-31 09:00:00','search'),
 (2,'2024-03-10 12:00:00','ads'),(2,'2024-03-17 12:00:00','social'),
 (4,'2024-03-18 12:00:00','ads'),(5,'2024-03-25 12:00:00','email');
INSERT INTO orders VALUES
 (1,1,'2024-03-31 10:00:00',120,'completed'),(2,2,'2024-03-17 12:00:00',60,'completed'),
 (3,3,'2024-03-20 12:00:00',80,'completed'),(4,4,'2024-03-20 12:00:00',500,'cancelled'),
 (5,5,'2024-03-20 12:00:00',90,'completed');
"""
SQL_MAIN = """
WITH j AS (                                  -- touches in the 30 days up to and including the order time
  SELECT o.order_id, o.amount, t.channel,
         (unixepoch(o.order_ts) - unixepoch(t.touch_ts)) / 86400.0 AS age_days
  FROM orders o JOIN touches t
    ON t.user_id = o.user_id
   AND t.touch_ts <= o.order_ts
   AND unixepoch(o.order_ts) - unixepoch(t.touch_ts) <= 30 * 86400
  WHERE o.status = 'completed'
), w AS (
  SELECT order_id, amount, channel, power(0.5, age_days / 7.0) AS decay_w FROM j
), s AS (
  SELECT order_id, amount, channel,
         1.0 / COUNT(*) OVER (PARTITION BY order_id)                 AS lin_w,
         decay_w / SUM(decay_w) OVER (PARTITION BY order_id)         AS dec_w
  FROM w
)
SELECT channel, ROUND(SUM(amount * lin_w), 4) AS linear, ROUND(SUM(amount * dec_w), 4) AS time_decay
FROM s GROUP BY channel
UNION ALL
SELECT 'unattributed', SUM(amount), SUM(amount)
FROM orders o WHERE o.status = 'completed' AND NOT EXISTS (SELECT 1 FROM j WHERE j.order_id = o.order_id)
ORDER BY channel
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("math functions compiled in:", con.execute("SELECT sqlite_compileoption_used('ENABLE_MATH_FUNCTIONS')").fetchone()[0],
      "| power(0.5, 2) =", con.execute("SELECT power(0.5, 2)").fetchone()[0],
      "| exp(-2*ln(2)) =", round(con.execute("SELECT exp(-2 * ln(2))").fetchone()[0], 12))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
total = con.execute("SELECT SUM(amount) FROM orders WHERE status='completed'").fetchone()[0]
assert abs(sql_df["linear"].sum() - total) < 1e-6 and abs(sql_df["time_decay"].sum() - total) < 1e-6
print("completed revenue:", total, "| linear sum:", round(sql_df["linear"].sum(), 6), "| time-decay sum:", round(sql_df["time_decay"].sum(), 6))

# fallback without power()/exp(): a lookup table of weights by whole days of age (0..30), built outside SQL
con.execute("CREATE TABLE lut(age_day INTEGER PRIMARY KEY, w REAL)")
con.executemany("INSERT INTO lut VALUES (?, ?)", [(d, 0.5 ** (d / 7.0)) for d in range(31)])
SQL_LUT = SQL_MAIN.replace("power(0.5, age_days / 7.0) AS decay_w FROM j",
                           "(SELECT w FROM lut WHERE age_day = CAST(age_days AS INTEGER)) AS decay_w FROM j")
lut_df = pd.read_sql_query(SQL_LUT, con)
print("LUT fallback (age truncated to whole days):"); print(lut_df.to_string(index=False))
print("largest difference to the exact weights: %.4f" % (lut_df["time_decay"] - sql_df["time_decay"]).abs().max())

touches = pd.read_sql_query("SELECT * FROM touches", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders[orders["status"].eq("completed")].assign(ots=pd.to_datetime(orders["order_ts"]))
t = touches.assign(tts=pd.to_datetime(touches["touch_ts"]))
j = o.merge(t, on="user_id")
j["age_days"] = (j["ots"] - j["tts"]).dt.total_seconds() / 86400.0
j = j[(j["tts"] <= j["ots"]) & (j["age_days"] <= 30)].copy()
j["lin_w"] = 1.0 / j.groupby("order_id")["order_id"].transform("size")
j["decay_w"] = 0.5 ** (j["age_days"] / 7.0)
j["dec_w"] = j["decay_w"] / j.groupby("order_id")["decay_w"].transform("sum")
by_ch = (j.assign(linear=j["amount"] * j["lin_w"], time_decay=j["amount"] * j["dec_w"])
           .groupby("channel", as_index=False)[["linear", "time_decay"]].sum())
unatt = o.loc[~o["order_id"].isin(j["order_id"]), "amount"].sum()
pd_df = pd.concat([by_ch, pd.DataFrame({"channel": ["unattributed"], "linear": [unatt], "time_decay": [unatt]})],
                  ignore_index=True).sort_values("channel").reset_index(drop=True)
pd_df[["linear", "time_decay"]] = pd_df[["linear", "time_decay"]].round(4)
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # both sorted by channel
assert abs(pd_df["linear"].sum() - total) < 1e-6 and abs(pd_df["time_decay"].sum() - total) < 1e-6
print("order 1 time-decay weights:", j[j["order_id"].eq(1)][["channel", "age_days", "dec_w"]].round(4).to_dict("records"))
print("asserts passed")
```

**Output (my run):**
```text
math functions compiled in: 1 | power(0.5, 2) = 0.25 | exp(-2*ln(2)) = 0.25
     channel  linear  time_decay
         ads    70.0     24.3755
       email    40.0     38.6476
      search    40.0     76.9769
      social    30.0     40.0000
unattributed   170.0    170.0000
completed revenue: 350.0 | linear sum: 350.0 | time-decay sum: 350.0
LUT fallback (age truncated to whole days):
     channel  linear  time_decay
         ads    70.0     24.3639
       email    40.0     38.5454
      search    40.0     77.0907
      social    30.0     40.0000
unattributed   170.0    170.0000
largest difference to the exact weights: 0.1138
     channel  linear  time_decay
         ads    70.0     24.3755
       email    40.0     38.6476
      search    40.0     76.9769
      social    30.0     40.0000
unattributed   170.0    170.0000
order 1 time-decay weights: [{'channel': 'ads', 'age_days': 29.0, 'dec_w': 0.0365}, {'channel': 'email', 'age_days': 7.0, 'dec_w': 0.3221}, {'channel': 'search', 'age_days': 0.0417, 'dec_w': 0.6415}]
asserts passed
```

**Edge cases:**
- Orders with no touches: reported as `unattributed`; if you left them out, the models would sum to less than revenue (180 here instead of 350 for the two orders that have touches). With a `LEFT JOIN` design the count of touches would be 0 for them and `1.0 / COUNT(t.channel)` would divide by zero (NULL in SQLite, an error in some engines); the anti-join form avoids it.
- Touches outside the window (the 31-day social touch of user 1) and after the order (user 5) are ignored.
- The same touch can be credited to several orders of the same user (each order has its own window); that is fine for revenue by channel, but touch counts are then not unique.
- Cancelled orders carry no revenue (order 4); refunds would be a separate adjustment (Q10).
- Same-timestamp ties: the touch at the order instant has age 0 and weight 1; if it should not count, use `<`.
- First-touch and last-touch versions of this table are in Q20; this answer does not repeat them.

**Then explain:**
- Linear gives each touch equal credit, so a very old touch is worth as much as one an hour before; time decay gives recent touches more credit with a half-life: a touch 7 days old counts half as much as one at the order time.
- Normalising weights per order keeps the credit of one order at its amount (the weights of an order sum to 1), which is why totals reconcile.
- The model is a convention. It does not measure causal effect; incrementality needs experiments (Book 1 and Book 6).
- Choose the lookback and half-life with the business and state them (30 and 7 are my assumptions).
- Dialects (not executed here): PostgreSQL `power(0.5, x)` or `0.5 ^ x`, MySQL `POW`, BigQuery `POW`/`POWER`, Snowflake `POWER`; interval filters would be `order_ts - INTERVAL '30 days'`.

**Follow-ups:**
- Position-based (40/20/40) weights? Replace the weight with a `CASE` on `ROW_NUMBER` of the touch within the order, and handle one- and two-touch orders.
- Per-channel cost and ROAS? Join to a spend table at the channel grain after attribution (aggregate first, then join, to avoid fan-out).
- Do touches span devices? Identity resolution is a data-engineering problem (Book 4).

**Common mistakes:**
- Not normalising decay weights, so the totals exceed revenue.
- Dropping orders without touches and then quoting attributed revenue as total revenue.
- Dividing by the touch count with a `LEFT JOIN`.
- Counting touches after the order or beyond the lookback.
- Using whole-day ages for a model that needs a fractional age (or forgetting to say that the table is an approximation).

