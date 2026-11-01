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

### Q42 ⭐ 🔴 Rolling distinct active users in pandas: events DataFrame(user_id, event_ts) with daily timestamps. Compute the rolling 30-day distinct active users for each day in March 2024 and show that rolling().nunique does not exist, so build it with a date spine and a merge (cross join of days with the events dataframe filtered by the window, or a merge_asof alternative, or a per-day set union), then groupby().nunique(). Assert equality with the SQL range-join result, and comment on memory use (the spine times events merge is the cost) and the alternative of first-active-date flags for trailing counts of new actives.
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
