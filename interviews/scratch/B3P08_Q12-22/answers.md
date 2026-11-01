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
