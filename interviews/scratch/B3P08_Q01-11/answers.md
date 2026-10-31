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
