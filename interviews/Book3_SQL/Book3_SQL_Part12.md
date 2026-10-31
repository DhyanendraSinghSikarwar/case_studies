# Book 3 — Part 12: Company-style mixed mock sets (FAANG, fintech, e-commerce), SQL and pandas

**Topic:** timed mock SETS of five questions each that mix joins, subqueries, windows, date and cohort logic, islands and streaks, funnels, recursion and reshaping from Parts 1 to 10, always answered in SQL (SQLite 3.45) and pandas 3.0 with the two results asserted equal
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 16, ⭐⭐ 16, ⭐ 8)  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

How the sets work: there are 8 sets of 5 questions (3 FAANG-style, 3 fintech, 2 e-commerce). Each question is tagged `[Set F1, Q1 of 5, 5 min, 10 pts]`. Questions are listed by star rating (⭐⭐⭐ first) as the book requires, so the five questions of a set are scattered through the file; to run a set as a mock, collect its tag. Inside a set, Q1 is the warm-up (10 pts), Q2 and Q3 are the middle (20 pts each) and Q4 and Q5 are the hard pair (25 pts each): 100 points per set. Suggested scoring per question: 40 percent for a correct query on the stated seed data, 20 percent for naming and handling the edge case the prompt seeds (ties, NULLs, duplicates, empty groups), 20 percent for the pandas equivalent, 10 percent for saying the assumption out loud before coding, 10 percent for a one-line check (row count or total). Time budgets are practice targets set by this book, not any company's published rules.

| Set | Theme | Questions | Time | Points |
|---|---|---|---|---|
| E1 | E-commerce set E1: orders, returns and funnel | 5 | 45 min | 100 |
| E2 | E-commerce set E2: marketplace, promotions and inventory | 5 | 48 min | 100 |
| F1 | FAANG-style set F1: social product analytics (Meta-style) | 5 | 41 min | 100 |
| F2 | FAANG-style set F2: search and ads (Google-style) | 5 | 45 min | 100 |
| F3 | FAANG-style set F3: retail and org data (Amazon-style) | 5 | 45 min | 100 |
| T1 | Fintech set T1: payments, fraud and reconciliation | 5 | 45 min | 100 |
| T2 | Fintech set T2: lending, ledger and FX | 5 | 45 min | 100 |
| T3 | Fintech set T3: wallet growth and risk (pandas-first) | 5 | 48 min | 100 |

Scope note: this part integrates, it does not reteach. Each prompt names the earlier question it builds on (Part N Qn) and every such reference was checked against the headings of Book3_SQL_Part01 to Part11. Part 11 (plans and indexes) is not re-tested here; in a real round, finish with one sentence on which index you would add.

Evidence limits: no free source was found that reports the exact SQL questions asked by a named company, and the guides found could not be opened (see research_notes/Book3_Part12_sources.md). The sets are therefore expert designs in the style of publicly described formats (business-framed SQL, joins and aggregations first, then CASE, subqueries and windows; reconciliation, duplicates and fraud rules for payments; cohorts, returns and repeat purchase for e-commerce). 'Asked at' tags name source types, not companies that asked these exact questions. No salary figures. Anything on engines other than SQLite stays hedged text, not executed.

---

### Q1 ⭐⭐⭐ 🔴 [Set F1, Q5 of 5, 10 min, 25 pts] Friend suggestions (Meta-style social graph). friends(user_id, friend_id) stores each friendship once with user_id < friend_id; users(user_id, name). Return every pair (a, b) with a < b who are not friends but have at least 2 mutual friends, with the mutual-friend count, ordered by count descending then a, b. Seed 8 users and 11 friendships, including a user with no friends and a pair with exactly one mutual friend. Solve in SQL (UNION ALL to make the edge list symmetric, then a self join, as in Part 2 Q37 and Part 2 Q15) and in pandas (merge on the shared friend). State how you stop a pair appearing twice.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Make the friendship list symmetric with UNION ALL, self join it on the shared friend with `a < b` so each pair shows up once, drop pairs that are already friends with NOT EXISTS, and keep `HAVING COUNT(*) >= 2`.

**Schema and sample data:**
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE friends(user_id INTEGER, friend_id INTEGER);  -- stored once, user_id < friend_id
INSERT INTO users VALUES (1,'Asha'),(2,'Bala'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid'),(7,'Gita'),(8,'Hari');
INSERT INTO friends VALUES
 (1,2),(1,3),(2,4),(3,4),(2,5),(3,5),(4,5),(4,6),(5,6),(6,7),(1,7);
```

**SQL answer:** the query is `sql` in the Code block (`naive` and `one` are the wrong and the excluded-pairs variants).
`sql` in the Code block:
```sql
WITH e AS (                                   -- symmetric edge list: (person, friend)
  SELECT user_id AS p, friend_id AS f FROM friends
  UNION ALL
  SELECT friend_id, user_id FROM friends
)
SELECT e1.p AS a, e2.p AS b, COUNT(*) AS mutual
FROM e e1
JOIN e e2 ON e1.f = e2.f AND e1.p < e2.p      -- same friend, a < b: each pair once
WHERE NOT EXISTS (SELECT 1 FROM friends x WHERE x.user_id = e1.p AND x.friend_id = e2.p)
GROUP BY e1.p, e2.p
HAVING COUNT(*) >= 2
ORDER BY mutual DESC, a, b
```

**pandas answer:** the same steps with `concat`, a self `merge` on the shared friend, an anti-join through a left merge and `groupby().size()`.
```py
e = pd.concat([friends.rename(columns={"user_id": "p", "friend_id": "f"}),
               friends.rename(columns={"user_id": "f", "friend_id": "p"})], ignore_index=True)
m = e.merge(e, on="f", suffixes=("_1", "_2"))
m = m[m["p_1"] < m["p_2"]]                       # same rule as SQL: a < b, each pair once
m = m.merge(friends.assign(is_friend=True), left_on=["p_1", "p_2"], right_on=["user_id", "friend_id"], how="left")
m = m[m["is_friend"].isna()]                     # anti-join: drop pairs that are already friends
p = (m.groupby(["p_1", "p_2"]).size().rename("mutual").reset_index()
       .rename(columns={"p_1": "a", "p_2": "b"}))
p = p[p["mutual"] >= 2].sort_values(["mutual", "a", "b"], ascending=[False, True, True]).reset_index(drop=True)
print("pandas result:"); print(p.to_string(index=False)); print()
```

**Example:** Friendships: 1-2, 1-3, 2-4, 3-4, 2-5, 3-5, 4-5, 4-6, 5-6, 6-7, 1-7; user 8 has none. Friends of 2 are {1, 4, 5} and friends of 3 are {1, 4, 5}; 2 and 3 are not friends, and they share 1, 4 and 5, so (2, 3) has 3 mutual friends and tops the list. Friends of 1 are {2, 3, 7} and of 4 are {2, 3, 5, 6}: they share 2 and 3, so (1, 4) has 2. The same hand count gives (1, 5), (2, 6) and (3, 6) with 2 each. (1, 6) shares only 7, so it has exactly one mutual friend and is dropped by the HAVING. (4, 5) shares 2, 3 and 6 but they are already friends, so the NOT EXISTS removes them. Result: 5 rows, as in the output.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q1: friend suggestions: non-friend pairs with >= 2 mutual friends. SQL (UNION ALL edge list + self join) vs pandas merge.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE friends(user_id INTEGER, friend_id INTEGER);  -- stored once, user_id < friend_id
INSERT INTO users VALUES (1,'Asha'),(2,'Bala'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid'),(7,'Gita'),(8,'Hari');
INSERT INTO friends VALUES
 (1,2),(1,3),(2,4),(3,4),(2,5),(3,5),(4,5),(4,6),(5,6),(6,7),(1,7);
""")

sql = """
WITH e AS (                                   -- symmetric edge list: (person, friend)
  SELECT user_id AS p, friend_id AS f FROM friends
  UNION ALL
  SELECT friend_id, user_id FROM friends
)
SELECT e1.p AS a, e2.p AS b, COUNT(*) AS mutual
FROM e e1
JOIN e e2 ON e1.f = e2.f AND e1.p < e2.p      -- same friend, a < b: each pair once
WHERE NOT EXISTS (SELECT 1 FROM friends x WHERE x.user_id = e1.p AND x.friend_id = e2.p)
GROUP BY e1.p, e2.p
HAVING COUNT(*) >= 2
ORDER BY mutual DESC, a, b
"""
naive = """
WITH e AS (SELECT user_id AS p, friend_id AS f FROM friends UNION ALL SELECT friend_id, user_id FROM friends)
SELECT e1.p AS a, e2.p AS b, COUNT(*) AS mutual
FROM e e1 JOIN e e2 ON e1.f = e2.f AND e1.p <> e2.p
GROUP BY e1.p, e2.p HAVING COUNT(*) >= 2 ORDER BY a, b
"""
one = """
WITH e AS (SELECT user_id AS p, friend_id AS f FROM friends UNION ALL SELECT friend_id, user_id FROM friends)
SELECT e1.p AS a, e2.p AS b, COUNT(*) AS mutual
FROM e e1 JOIN e e2 ON e1.f = e2.f AND e1.p < e2.p
WHERE NOT EXISTS (SELECT 1 FROM friends x WHERE x.user_id = e1.p AND x.friend_id = e2.p)
GROUP BY e1.p, e2.p HAVING COUNT(*) = 1 ORDER BY a, b
"""
s = pd.read_sql(sql, con)
print("SQL result (non-friends, >= 2 mutual):"); print(s.to_string(index=False)); print()
print("pairs with exactly 1 mutual friend (excluded):"); print(pd.read_sql(one, con).to_string(index=False)); print()
n = pd.read_sql(naive, con)
print("naive p <> p version: %d rows (each pair twice, friends included)" % len(n)); print()

# pandas
friends = pd.read_sql("SELECT * FROM friends", con)
users = pd.read_sql("SELECT * FROM users", con)
e = pd.concat([friends.rename(columns={"user_id": "p", "friend_id": "f"}),
               friends.rename(columns={"user_id": "f", "friend_id": "p"})], ignore_index=True)
m = e.merge(e, on="f", suffixes=("_1", "_2"))
m = m[m["p_1"] < m["p_2"]]                       # same rule as SQL: a < b, each pair once
m = m.merge(friends.assign(is_friend=True), left_on=["p_1", "p_2"], right_on=["user_id", "friend_id"], how="left")
m = m[m["is_friend"].isna()]                     # anti-join: drop pairs that are already friends
p = (m.groupby(["p_1", "p_2"]).size().rename("mutual").reset_index()
       .rename(columns={"p_1": "a", "p_2": "b"}))
p = p[p["mutual"] >= 2].sort_values(["mutual", "a", "b"], ascending=[False, True, True]).reset_index(drop=True)
print("pandas result:"); print(p.to_string(index=False)); print()

# compare in the same order (mutual desc, a, b); both already sorted that way
pd.testing.assert_frame_equal(s, p, check_dtype=False)
named = s.merge(users, left_on="a", right_on="user_id").merge(users, left_on="b", right_on="user_id", suffixes=("_a", "_b"))
print("with names:"); print(named[["name_a", "name_b", "mutual"]].to_string(index=False))
print("asserts passed (same order: mutual desc, a, b)")
```

**Output (my run):**
```text
SQL result (non-friends, >= 2 mutual):
 a  b  mutual
 2  3       3
 1  4       2
 1  5       2
 2  6       2
 3  6       2

pairs with exactly 1 mutual friend (excluded):
 a  b  mutual
 1  6       1
 2  7       1
 3  7       1
 4  7       1
 5  7       1

naive p <> p version: 12 rows (each pair twice, friends included)

pandas result:
 a  b  mutual
 2  3       3
 1  4       2
 1  5       2
 2  6       2
 3  6       2

with names:
name_a name_b  mutual
  Bala Chitra       3
  Asha    Dev       2
  Asha   Esha       2
  Bala  Farid       2
Chitra  Farid       2
asserts passed (same order: mutual desc, a, b)
```

**Edge cases:**
- **Each pair once:** the join condition `e1.p < e2.p` keeps (2, 3) and drops (3, 2), and it also drops the self pair (2, 2). With `<>` instead, my run returned 12 rows: the 5 real pairs twice plus the already-friends pair (4, 5) twice.
- **Already friends:** the friends table stores only `user_id < friend_id`, so the anti-join can test `(e1.p, e2.p)` directly because `e1.p < e2.p` has the same orientation. If a table stored both directions this check would still work, but the edge list would be doubled.
- **Duplicate friendship rows** would inflate the count (the same mutual friend counted twice). Use `UNION` instead of `UNION ALL` for the edge list, or `COUNT(DISTINCT e1.f)`.
- **User with no friends** (user 8) never appears in any join, so never in the output. A user with one friend can never be in a pair with 2 mutual friends.
- **Ties:** pairs with equal counts are ordered by a then b, so the output is deterministic.

**Then explain:**
- **The symmetric list is the key idea.** One stored row (1, 4) means 1 is a friend of 4 and 4 is a friend of 1. `UNION ALL` of the table with its reverse gives (person, friend) rows in both directions, so one self join on `friend` finds everyone who shares that friend.
- **Why a < b stops duplicates:** the same two users meet on every shared friend, once as (a, b) and once as (b, a). Requiring the smaller id first keeps one of the two, and `GROUP BY a, b` then counts the shared friends.
- **Why the count is the mutual-friend count:** each shared friend produces exactly one joined row for the pair, so `COUNT(*)` after the join is the number of mutual friends (given no duplicate edges).
- **pandas:** `e.merge(e, on="f")` is the same self join; the anti-join is a left merge with a marker column, then keep rows where the marker is NaN.
- **Names:** `users` is only needed for display; the last lines of the Code block join it back (Bala and Chitra share 3 friends).
- **Other engines:** the same SQL works on PostgreSQL and MySQL 8 (not executed here, from memory). On a big graph the self join costs degree squared per user, which is the real scaling problem.
- **Scoring note (Set F1, Q5 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (symmetric edge list, `a < b`, anti-join, HAVING >= 2), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: a query that returns every pair twice or includes existing friends loses most of the 10 query points but keeps edge-case and pandas credit if stated; getting only the symmetric list right is about half the query points

**Follow-ups:**
- *Rank the suggestions per user, not per pair?* Make the pairs symmetric again (UNION ALL of (a, b) and (b, a)), then `ROW_NUMBER() OVER (PARTITION BY user ORDER BY mutual DESC, other)` and keep the top 3 (Part 4 style).
- *What if friendships are stored in both directions?* Then the UNION ALL is not needed (the table is already symmetric) but the `a < b` filter still is.
- *How would you make it faster?* An index on the friend column of the edge list, and skip users with very high degree or sample them; say it in one sentence, the plan itself is Part 11.

**Common mistakes:**
- Joining on `e1.p <> e2.p` and returning each pair twice.
- Forgetting the already-friends filter, so (4, 5) is suggested to people who are already friends.
- Counting rows before the filter, or using `COUNT(DISTINCT ...)` on the wrong column.
- Using `NOT IN (SELECT ...)` against a column that may contain NULL (use NOT EXISTS).
- Not saying how the duplicate pair is avoided; the prompt asks for it.

### Q2 ⭐⭐⭐ 🔴 [Set F2, Q5 of 5, 12 min, 25 pts] Campaign coverage (Google Ads-style). flights(advertiser_id, campaign_id, start_date, end_date) holds inclusive date ranges per campaign; ranges of one advertiser may overlap or touch. Return, per advertiser, the number of distinct calendar days with at least one live campaign, and the merged ranges. Seed 3 advertisers, one with nested ranges, one with ranges that touch (end 2025-03-10, next start 2025-03-11) and one with a single range. Solve in SQL (LAG running-max island technique from Part 7 Q16) and pandas (sort, cummax, cumsum groups from Part 7 Q28). Say how you treat touching ranges.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Sort each advertiser's ranges by start, compare each start with the running maximum of the earlier end dates (not the previous end), start a new island when the gap is more than one day, then merge by island and add up the days; I treat touching ranges (end 03-10, start 03-11) as one range because there is no uncovered day between them.

**Schema and sample data:**
```sql
CREATE TABLE flights(advertiser_id INTEGER, campaign_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO flights VALUES
 (1,11,'2025-03-01','2025-03-10'),
 (1,12,'2025-03-03','2025-03-05'),   -- nested inside 11
 (1,13,'2025-03-08','2025-03-15'),   -- overlaps 11, extends it
 (1,14,'2025-03-20','2025-03-22'),   -- separate island
 (2,21,'2025-03-01','2025-03-10'),
 (2,22,'2025-03-11','2025-03-15'),   -- touches 21 (end 03-10, start 03-11)
 (2,23,'2025-03-17','2025-03-18'),   -- one-day gap (03-16) so not merged
 (3,31,'2025-04-01','2025-04-07');
```

**SQL answer:** `merged_sql` and `days_sql` in the Code block (`naive_sql`, `strict_sql` and `lag_sql` are the comparison variants).
`merged_sql` in the Code block:
```sql
WITH o AS (
  SELECT *, MAX(end_date) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max_end
  FROM flights
), f AS (
  SELECT *, CASE WHEN prev_max_end IS NULL OR start_date > date(prev_max_end, '+1 day')
                 THEN 1 ELSE 0 END AS new_island
  FROM o
), g AS (
  SELECT *, SUM(new_island) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id) AS grp
  FROM f
)
SELECT advertiser_id, MIN(start_date) AS range_start, MAX(end_date) AS range_end,
       CAST(julianday(MAX(end_date)) - julianday(MIN(start_date)) AS INTEGER) + 1 AS days
FROM g
GROUP BY advertiser_id, grp
ORDER BY advertiser_id, range_start
```
`days_sql` in the Code block:
```sql
WITH m AS (%s)
SELECT advertiser_id, SUM(days) AS live_days, COUNT(*) AS ranges FROM m GROUP BY advertiser_id ORDER BY advertiser_id
```

**pandas answer:** sort, `cummax().shift()` per advertiser, a flag, `cumsum` for the island id, then `groupby` with min and max.
```py
fl = pd.read_sql("SELECT * FROM flights", con, parse_dates=["start_date", "end_date"])
fl = fl.sort_values(["advertiser_id", "start_date", "campaign_id"]).reset_index(drop=True)
fl["prev_max_end"] = fl.groupby("advertiser_id")["end_date"].transform(lambda s: s.cummax().shift())
fl["new_island"] = (fl["prev_max_end"].isna() | (fl["start_date"] > fl["prev_max_end"] + pd.Timedelta(days=1))).astype(int)
fl["grp"] = fl.groupby("advertiser_id")["new_island"].cumsum()
p_m = (fl.groupby(["advertiser_id", "grp"], as_index=False)
         .agg(range_start=("start_date", "min"), range_end=("end_date", "max")))
p_m["days"] = (p_m["range_end"] - p_m["range_start"]).dt.days + 1
p_m = p_m.drop(columns="grp")
p_m["range_start"] = p_m["range_start"].dt.strftime("%Y-%m-%d")
p_m["range_end"] = p_m["range_end"].dt.strftime("%Y-%m-%d")
p_d = p_m.groupby("advertiser_id", as_index=False).agg(live_days=("days", "sum"), ranges=("days", "size"))
```

**Example:** Advertiser 1 has 11 (03-01 to 03-10), 12 (03-03 to 03-05, nested), 13 (03-08 to 03-15) and 14 (03-20 to 03-22). Sorted by start, the running max of earlier ends is NULL, 03-10, 03-10, 03-15. Campaign 11 starts an island (no earlier end); 12 starts 03-03, not after 03-11, so it joins; 13 starts 03-08, joins and pushes the end to 03-15; 14 starts 03-20, later than 03-16, so a new island. Merged ranges: 03-01 to 03-15 (15 days) and 03-20 to 03-22 (3 days), 18 live days; summing the campaign lengths would say 24. Advertiser 2: 21 ends 03-10 and 22 starts 03-11, no day between them, so one range 03-01 to 03-15 (15 days); 23 starts 03-17 and 03-16 is uncovered, so a second range of 2 days, total 17. Advertiser 3 is one range of 7 days.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q2: campaign coverage: merged ranges and distinct live days per advertiser.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE flights(advertiser_id INTEGER, campaign_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO flights VALUES
 (1,11,'2025-03-01','2025-03-10'),
 (1,12,'2025-03-03','2025-03-05'),   -- nested inside 11
 (1,13,'2025-03-08','2025-03-15'),   -- overlaps 11, extends it
 (1,14,'2025-03-20','2025-03-22'),   -- separate island
 (2,21,'2025-03-01','2025-03-10'),
 (2,22,'2025-03-11','2025-03-15'),   -- touches 21 (end 03-10, start 03-11)
 (2,23,'2025-03-17','2025-03-18'),   -- one-day gap (03-16) so not merged
 (3,31,'2025-04-01','2025-04-07');
""")

merged_sql = """
WITH o AS (
  SELECT *, MAX(end_date) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max_end
  FROM flights
), f AS (
  SELECT *, CASE WHEN prev_max_end IS NULL OR start_date > date(prev_max_end, '+1 day')
                 THEN 1 ELSE 0 END AS new_island
  FROM o
), g AS (
  SELECT *, SUM(new_island) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id) AS grp
  FROM f
)
SELECT advertiser_id, MIN(start_date) AS range_start, MAX(end_date) AS range_end,
       CAST(julianday(MAX(end_date)) - julianday(MIN(start_date)) AS INTEGER) + 1 AS days
FROM g
GROUP BY advertiser_id, grp
ORDER BY advertiser_id, range_start
"""
days_sql = """
WITH m AS (%s)
SELECT advertiser_id, SUM(days) AS live_days, COUNT(*) AS ranges FROM m GROUP BY advertiser_id ORDER BY advertiser_id
""" % merged_sql
naive_sql = """
SELECT advertiser_id, SUM(CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1) AS naive_days
FROM flights GROUP BY advertiser_id ORDER BY advertiser_id
"""
strict_sql = merged_sql.replace("date(prev_max_end, '+1 day')", "prev_max_end")   # touching NOT merged (overlap only)

lag_sql = merged_sql.replace("MAX(end_date) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id\n                                ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)",
                             "LAG(end_date) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id)")
assert lag_sql != merged_sql
s_m = pd.read_sql(merged_sql, con)
s_d = pd.read_sql(days_sql, con)
print("SQL merged ranges (touching merged):"); print(s_m.to_string(index=False)); print()
print("SQL live days per advertiser:"); print(s_d.to_string(index=False)); print()
print("naive sum of campaign lengths (double counts overlaps):"); print(pd.read_sql(naive_sql, con).to_string(index=False)); print()
print("overlap-only rule (touching NOT merged), advertiser 2:")
print(pd.read_sql(strict_sql, con).query("advertiser_id == 2").to_string(index=False)); print()

print("wrong variant, LAG(end_date) instead of the running max, advertiser 1:")
print(pd.read_sql(lag_sql, con).query("advertiser_id == 1").to_string(index=False)); print()

# pandas
fl = pd.read_sql("SELECT * FROM flights", con, parse_dates=["start_date", "end_date"])
fl = fl.sort_values(["advertiser_id", "start_date", "campaign_id"]).reset_index(drop=True)
fl["prev_max_end"] = fl.groupby("advertiser_id")["end_date"].transform(lambda s: s.cummax().shift())
fl["new_island"] = (fl["prev_max_end"].isna() | (fl["start_date"] > fl["prev_max_end"] + pd.Timedelta(days=1))).astype(int)
fl["grp"] = fl.groupby("advertiser_id")["new_island"].cumsum()
p_m = (fl.groupby(["advertiser_id", "grp"], as_index=False)
         .agg(range_start=("start_date", "min"), range_end=("end_date", "max")))
p_m["days"] = (p_m["range_end"] - p_m["range_start"]).dt.days + 1
p_m = p_m.drop(columns="grp")
p_m["range_start"] = p_m["range_start"].dt.strftime("%Y-%m-%d")
p_m["range_end"] = p_m["range_end"].dt.strftime("%Y-%m-%d")
p_d = p_m.groupby("advertiser_id", as_index=False).agg(live_days=("days", "sum"), ranges=("days", "size"))
print("pandas merged ranges:"); print(p_m.to_string(index=False)); print()
print("pandas live days:"); print(p_d.to_string(index=False)); print()

pd.testing.assert_frame_equal(s_m, p_m, check_dtype=False)
pd.testing.assert_frame_equal(s_d, p_d, check_dtype=False)
print("asserts passed (compared in order advertiser_id, range_start)")
```

**Output (my run):**
```text
SQL merged ranges (touching merged):
 advertiser_id range_start  range_end  days
             1  2025-03-01 2025-03-15    15
             1  2025-03-20 2025-03-22     3
             2  2025-03-01 2025-03-15    15
             2  2025-03-17 2025-03-18     2
             3  2025-04-01 2025-04-07     7

SQL live days per advertiser:
 advertiser_id  live_days  ranges
             1         18       2
             2         17       2
             3          7       1

naive sum of campaign lengths (double counts overlaps):
 advertiser_id  naive_days
             1          24
             2          17
             3           7

overlap-only rule (touching NOT merged), advertiser 2:
 advertiser_id range_start  range_end  days
             2  2025-03-01 2025-03-10    10
             2  2025-03-11 2025-03-15     5
             2  2025-03-17 2025-03-18     2

wrong variant, LAG(end_date) instead of the running max, advertiser 1:
 advertiser_id range_start  range_end  days
             1  2025-03-01 2025-03-10    10
             1  2025-03-08 2025-03-15     8
             1  2025-03-20 2025-03-22     3

pandas merged ranges:
 advertiser_id range_start  range_end  days
             1  2025-03-01 2025-03-15    15
             1  2025-03-20 2025-03-22     3
             2  2025-03-01 2025-03-15    15
             2  2025-03-17 2025-03-18     2
             3  2025-04-01 2025-04-07     7

pandas live days:
 advertiser_id  live_days  ranges
             1         18       2
             2         17       2
             3          7       1

asserts passed (compared in order advertiser_id, range_start)
```

**Edge cases:**
- **Touching ranges:** my rule is `start > prev_max_end + 1 day` starts a new island, so touching merges. The overlap-only rule (`start > prev_max_end`) keeps 21 and 22 apart (3 ranges for advertiser 2 in my run). The live-day total is 17 either way, only the number of ranges changes, so say which one you chose.
- **Nested range:** campaign 12 lies inside 11. Because the comparison uses the running MAX of ends, it does not shorten the island. The wrong version with `LAG(end_date)` compares 13 with 12's end (03-05) and in my run produced two overlapping ranges for advertiser 1 (03-01 to 03-10 and 03-08 to 03-15).
- **Single range** (advertiser 3) works because the first row has no previous end (NULL), which is what starts the first island.
- **Ties on start_date:** ordering by `start_date, campaign_id` makes the order total, so the ROWS frame is deterministic.
- **Dates as text:** ISO `YYYY-MM-DD` text sorts and compares correctly, and `date(x, '+1 day')` stays text. NULL end dates (open campaigns) need a COALESCE to an as-of date before this runs; not seeded here.
- **Inclusive length:** days = end minus start plus 1, because both ends count.

**Then explain:**
- **Why a running max and not LAG:** an island ends only after the latest end seen so far, and a nested campaign does not extend it. `MAX(end_date) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)` is that latest end before the current row.
- **Why a cumulative flag:** the flag is 1 when a new island starts; `SUM(flag) OVER (ORDER BY ...)` turns it into an island id, the same trick as Part 7 Q16. Then ordinary `GROUP BY` takes `MIN(start)` and `MAX(end)`.
- **Distinct days:** once ranges are merged they cannot overlap, so summing their lengths counts each calendar day once. That is why you merge first instead of summing campaign lengths (24 versus 18 for advertiser 1).
- **pandas:** `groupby(...)["end_date"].cummax().shift()` is the running max of earlier ends; the island id is `groupby(...)["new_island"].cumsum()` (Part 7 Q28).
- **Other engines:** the same window SQL runs on PostgreSQL and others with their date arithmetic (`+ INTERVAL '1 day'`, not executed here).
- **Scoring note (Set F2, Q5 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (running-max island flag, merged ranges and live-day total), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: using LAG of the previous end earns roughly half of the query points because nested ranges break; summing campaign lengths gets the day count wrong and loses the edge-case points; stating the touching rule is the 2.5 assumption points

**Follow-ups:**
- *How do you count days per month?* Join the merged ranges to a day spine (recursive CTE) and count the days per month; or clip each range to the month and sum the lengths.
- *Open-ended campaigns (end NULL)?* `COALESCE(end_date, as_of_date)` before merging, and say it.
- *Is there a one-query alternative?* A day spine joined to flights with `EXISTS` counts distinct live days directly, but it is heavier for long ranges.

**Common mistakes:**
- Comparing with the previous row's end instead of the running maximum.
- Summing `end - start + 1` over campaigns and double counting overlaps.
- Forgetting the `+ 1` for inclusive end dates.
- Not saying how touching ranges are treated.
- Starting the island flag for the first row incorrectly (NULL comparison is not true, so it must be tested with IS NULL).

### Q3 ⭐⭐⭐ 🔴 [Set F3, Q5 of 5, 12 min, 25 pts] Org size roll-up (Amazon-style hierarchy). employees(emp_id, name, manager_id) with a CEO whose manager_id is NULL, 12 employees and 4 levels, plus one employee row whose manager_id points to an id that does not exist. For every manager return the number of direct reports and the number of all reports below them (any depth), and list the orphan row separately. Use a recursive CTE (Part 9 Q4 and Q9) and a pandas version using an iterative frame walk. Order by total reports descending, then emp_id.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Build the (manager, any report below) pairs with a recursive CTE that starts from the direct edges and walks one level down each step, then count with `SUM(depth = 1)` for direct reports and `COUNT(*)` for all reports; the orphan row is listed by a separate NOT EXISTS query.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'CEO',NULL),
 (2,'VP-A',1),(3,'VP-B',1),
 (4,'Dir-A1',2),(5,'Dir-A2',2),(6,'Dir-B1',3),(12,'Dir-B2',3),
 (7,'Mgr-1',4),(8,'Mgr-2',4),(9,'Mgr-3',5),
 (10,'Mgr-4',6),(11,'Mgr-5',6),
 (13,'Orphan',99);            -- manager 99 does not exist
```

**SQL answer:** `sql` (roll-up) and `orphan_sql` in the Code block.
`sql` in the Code block:
```sql
WITH RECURSIVE d(mgr, emp, depth) AS (
  SELECT e.manager_id, e.emp_id, 1                       -- direct edges, only when the manager exists
  FROM employees e JOIN employees m ON m.emp_id = e.manager_id
  UNION ALL
  SELECT d.mgr, e.emp_id, d.depth + 1                    -- walk one level further down
  FROM d JOIN employees e ON e.manager_id = d.emp
)
SELECT mgr AS emp_id,
       SUM(depth = 1) AS direct_reports,
       COUNT(*)       AS total_reports
FROM d
GROUP BY mgr
ORDER BY total_reports DESC, emp_id
```
`orphan_sql` in the Code block:
```sql
SELECT emp_id, name, manager_id FROM employees e
WHERE manager_id IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
```

**pandas answer:** an iterative walk: merge the current frame with the edge list on `emp` equal to `mgr`, collect each new level, stop when a merge returns nothing, then group.
```py
emp = pd.read_sql("SELECT * FROM employees", con)
edges = (emp[emp["manager_id"].isin(emp["emp_id"])][["manager_id", "emp_id"]]
         .rename(columns={"manager_id": "mgr", "emp_id": "emp"}).assign(depth=1))
frames, cur, level = [edges], edges, 1
while True:
    nxt = cur.merge(edges[["mgr", "emp"]], left_on="emp", right_on="mgr", suffixes=("", "_child"))
    nxt = nxt[["mgr", "emp_child"]].rename(columns={"emp_child": "emp"}).assign(depth=level + 1)
    if nxt.empty:
        break
    frames.append(nxt)
    cur, level = nxt, level + 1
    assert level <= len(emp), "cycle in manager_id"       # guard: a cycle would loop forever
closure = pd.concat(frames, ignore_index=True)
print("levels walked:", level)
closure["mgr"] = closure["mgr"].astype("int64")
p = (closure.groupby("mgr").agg(direct_reports=("depth", lambda d: int((d == 1).sum())),
                                total_reports=("depth", "size"))
            .reset_index().rename(columns={"mgr": "emp_id"})
            .sort_values(["total_reports", "emp_id"], ascending=[False, True]).reset_index(drop=True))
po = emp[emp["manager_id"].notna() & ~emp["manager_id"].isin(emp["emp_id"])][["emp_id", "name", "manager_id"]].reset_index(drop=True)
```

**Example:** Rows: 1 CEO; 2 and 3 report to 1; 4, 5 report to 2; 6, 12 report to 3; 7, 8 report to 4; 9 reports to 5; 10, 11 report to 6; 13 has manager 99, which does not exist. Employee 1 has 2 direct reports and every other employee below, 11 (12 employees minus the CEO). Employee 2 has direct 4 and 5, and below them 7, 8 and 9, so 2 direct and 5 total. Employee 3 has direct 6 and 12, plus 10 and 11 below 6: 2 direct, 4 total. Employee 4 has 7 and 8 (2 and 2), 6 has 10 and 11 (2 and 2), 5 has just 9 (1 and 1). The leaves have no reports, so they are not managers and are not listed. Row 13 is printed by the orphan query.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q3: org size roll-up: direct and total reports per manager, orphan listed separately.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'CEO',NULL),
 (2,'VP-A',1),(3,'VP-B',1),
 (4,'Dir-A1',2),(5,'Dir-A2',2),(6,'Dir-B1',3),(12,'Dir-B2',3),
 (7,'Mgr-1',4),(8,'Mgr-2',4),(9,'Mgr-3',5),
 (10,'Mgr-4',6),(11,'Mgr-5',6),
 (13,'Orphan',99);            -- manager 99 does not exist
""")
# 12 employees in 4 levels (CEO, 2 VPs, 4 Directors, 5 Managers) plus 1 orphan row = 13 rows

sql = """
WITH RECURSIVE d(mgr, emp, depth) AS (
  SELECT e.manager_id, e.emp_id, 1                       -- direct edges, only when the manager exists
  FROM employees e JOIN employees m ON m.emp_id = e.manager_id
  UNION ALL
  SELECT d.mgr, e.emp_id, d.depth + 1                    -- walk one level further down
  FROM d JOIN employees e ON e.manager_id = d.emp
)
SELECT mgr AS emp_id,
       SUM(depth = 1) AS direct_reports,
       COUNT(*)       AS total_reports
FROM d
GROUP BY mgr
ORDER BY total_reports DESC, emp_id
"""
orphan_sql = """
SELECT emp_id, name, manager_id FROM employees e
WHERE manager_id IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
"""
s = pd.read_sql(sql, con)
so = pd.read_sql(orphan_sql, con)
print("SQL roll-up:"); print(s.to_string(index=False)); print()
print("SQL orphan rows:"); print(so.to_string(index=False)); print()

# pandas: iterative frame walk
emp = pd.read_sql("SELECT * FROM employees", con)
edges = (emp[emp["manager_id"].isin(emp["emp_id"])][["manager_id", "emp_id"]]
         .rename(columns={"manager_id": "mgr", "emp_id": "emp"}).assign(depth=1))
frames, cur, level = [edges], edges, 1
while True:
    nxt = cur.merge(edges[["mgr", "emp"]], left_on="emp", right_on="mgr", suffixes=("", "_child"))
    nxt = nxt[["mgr", "emp_child"]].rename(columns={"emp_child": "emp"}).assign(depth=level + 1)
    if nxt.empty:
        break
    frames.append(nxt)
    cur, level = nxt, level + 1
    assert level <= len(emp), "cycle in manager_id"       # guard: a cycle would loop forever
closure = pd.concat(frames, ignore_index=True)
print("levels walked:", level)
closure["mgr"] = closure["mgr"].astype("int64")
p = (closure.groupby("mgr").agg(direct_reports=("depth", lambda d: int((d == 1).sum())),
                                total_reports=("depth", "size"))
            .reset_index().rename(columns={"mgr": "emp_id"})
            .sort_values(["total_reports", "emp_id"], ascending=[False, True]).reset_index(drop=True))
po = emp[emp["manager_id"].notna() & ~emp["manager_id"].isin(emp["emp_id"])][["emp_id", "name", "manager_id"]].reset_index(drop=True)
print("pandas roll-up:"); print(p.to_string(index=False)); print()
pd.testing.assert_frame_equal(s, p, check_dtype=False)
pd.testing.assert_frame_equal(so, po.astype({"manager_id": "int64"}), check_dtype=False)
print("asserts passed (order: total_reports desc, emp_id)")
```

**Output (my run):**
```text
SQL roll-up:
 emp_id  direct_reports  total_reports
      1               2             11
      2               2              5
      3               2              4
      4               2              2
      6               2              2
      5               1              1

SQL orphan rows:
 emp_id   name  manager_id
     13 Orphan          99

levels walked: 3
pandas roll-up:
 emp_id  direct_reports  total_reports
      1               2             11
      2               2              5
      3               2              4
      4               2              2
      6               2              2
      5               1              1

asserts passed (order: total_reports desc, emp_id)
```

**Edge cases:**
- **Orphan:** the base query joins to `employees` on the manager id, so 13 (manager 99) is not walked and 99 never shows up as a phantom manager. If you skipped that join, 99 would appear as a manager with 1 report (by reasoning, not run). The orphan list uses NOT EXISTS; `NOT IN (SELECT emp_id ...)` also works here only because `emp_id` is a non-NULL key, so prefer NOT EXISTS.
- **CEO:** NULL `manager_id` is not an edge, so the CEO has no manager row and is never listed as someone's report.
- **Leaves:** they have 0 reports and are not returned. If the prompt wants every employee with 0, LEFT JOIN `employees` to the result and COALESCE.
- **Cycles:** a manager loop (A reports to B, B to A) makes `UNION ALL` recursion run forever in SQL; add a depth limit (`WHERE d.depth < 20`) or track the path. The pandas loop has the same risk, so the code asserts that the level never exceeds the row count.
- **An orphan's own reports** would still be rolled up under the orphan (it exists as a row), as a separate detached tree.
- **Output type:** `read_sql` gives integers here; in pandas the manager id first becomes a float because the column holds NULL, so the code casts it back before comparing.

**Then explain:**
- **Recursive CTE shape:** an anchor (direct edges) plus a recursive step that joins the CTE to `employees` on `manager_id = d.emp`. The `mgr` column is carried unchanged, so every row says "this employee is somewhere below that manager".
- **Direct versus total:** `depth` starts at 1 in the anchor and grows by 1 per level, so `SUM(depth = 1)` counts direct reports and `COUNT(*)` counts everyone below. `SUM(CASE WHEN depth = 1 THEN 1 ELSE 0 END)` is the portable spelling of the same thing.
- **pandas walk:** the frame `cur` holds the pairs found at the latest level; merging it with the edges on `emp == mgr` yields the next level; concatenating all levels gives the same closure as the CTE. My run walked 3 levels of edges.
- **Order:** total reports descending then `emp_id`, as asked; both sides sort the same way before the assert.
- **Other engines:** PostgreSQL, MySQL 8 and SQL Server run recursive CTEs too (SQL Server without the RECURSIVE keyword); not executed here. Oracle also has CONNECT BY (hedged).
- **Scoring note (Set F3, Q5 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (closure CTE with direct and total counts), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: counting only direct reports (a GROUP BY) earns about a quarter of the query points; a correct total but a phantom manager 99 loses the orphan edge-case points

**Follow-ups:**
- *Employees per level?* `COUNT(*) GROUP BY depth` from the same CTE started at the CEO.
- *Path from an employee to the CEO?* Carry a text path in the recursive step (Part 9).
- *Many levels or millions of rows?* Say you would store a materialised path or closure table; the engine specifics are not executed here.

**Common mistakes:**
- Counting only `COUNT(*) GROUP BY manager_id`, which is direct reports only.
- Starting the anchor from the CEO only, so subtrees are counted from one root instead of every manager.
- Letting a missing manager id appear as a manager row.
- No cycle guard.
- Using `UNION` and expecting depth to dedupe (different depths are different rows).

### Q4 ⭐⭐⭐ 🔴 [Set F3, Q4 of 5, 12 min, 25 pts] Customers who bought every product on a list (Amazon-style relational division, Part 3 Q14 and Q35). orders(order_id, customer_id), order_items(order_id, product_id), featured(product_id) with 3 featured products. Return the customers who bought all 3 featured products at least once, including customers who bought one product twice and a customer with duplicate rows who bought only 2 products. Give the double NOT EXISTS version and the GROUP BY/HAVING COUNT(DISTINCT) version, plus pandas. Explain what changes if the featured list is empty.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Relational division: a customer qualifies when no featured product exists that they did not buy (double NOT EXISTS), or when the count of DISTINCT featured products they bought equals the number of featured products (GROUP BY and HAVING); both give customers 1 and 3 on the seed.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER);
CREATE TABLE featured(product_id INTEGER PRIMARY KEY);
INSERT INTO featured VALUES (101),(102),(103);
INSERT INTO orders VALUES (1,1),(2,1),(3,2),(4,2),(5,3),(6,4),(7,5);
INSERT INTO order_items VALUES
 (1,101),(1,102),(2,102),(2,103),   -- cust 1: all three, product 102 twice
 (3,101),(3,101),(3,102),           -- cust 2: duplicate rows, only 101 and 102
 (4,101),                           -- cust 2: 101 again
 (5,101),(5,102),(5,103),(5,999),   -- cust 3: all three plus a non-featured product
 (6,555),                           -- cust 4: no featured product
 (7,103);                           -- cust 5: one featured product
```

**SQL answer:** `not_exists` and `having` in the Code block (`wrong` shows the row-count trap).
`not_exists` in the Code block:
```sql
SELECT c.customer_id
FROM (SELECT DISTINCT customer_id FROM orders) c
WHERE NOT EXISTS (
  SELECT 1 FROM featured f
  WHERE NOT EXISTS (
    SELECT 1 FROM orders o JOIN order_items i ON i.order_id = o.order_id
    WHERE o.customer_id = c.customer_id AND i.product_id = f.product_id))
ORDER BY c.customer_id
```
`having` in the Code block:
```sql
SELECT o.customer_id
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
JOIN featured f ON f.product_id = i.product_id
GROUP BY o.customer_id
HAVING COUNT(DISTINCT f.product_id) = (SELECT COUNT(*) FROM featured)
ORDER BY o.customer_id
```

**pandas answer:** `division()` in the Code block: merge to featured, drop duplicates, `nunique` per customer, compare with `len(featured)`.
```py
# pandas
orders = pd.read_sql("SELECT * FROM orders", con); items = pd.read_sql("SELECT * FROM order_items", con)
featured = pd.read_sql("SELECT * FROM featured", con)
def division(orders, items, featured):
    hit = orders.merge(items, on="order_id").merge(featured, on="product_id")[["customer_id", "product_id"]].drop_duplicates()
    cnt = hit.groupby("customer_id")["product_id"].nunique()
    return sorted(cnt[cnt == len(featured)].index.tolist())
p = division(orders, items, featured)
print("pandas nunique == len(featured):", p)
assert a.customer_id.tolist() == b.customer_id.tolist() == p
print("asserts passed (compared as sorted customer_id lists)"); print()
```

**Example:** Featured products are 101, 102, 103. Customer 1 bought 101, 102 (order 1) and 102, 103 (order 2): all three, with 102 twice, so qualifies. Customer 2 has rows 101, 101, 102 and 101 again: 4 rows hit a featured product but only 2 distinct ones (103 is missing), so does not qualify. Customer 3 bought 101, 102, 103 and 999 in one order: qualifies. Customer 4 bought 555 only and customer 5 bought only 103. Answer: 1 and 3. A `COUNT(*) >= 3` check would wrongly pass customer 2 (4 rows) and the exact `= 3` check would wrongly fail customer 1 (4 rows), which is why DISTINCT matters.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q4: relational division: customers who bought ALL featured products. Double NOT EXISTS, HAVING COUNT(DISTINCT), pandas.
import sqlite3
import pandas as pd

def build():
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);
    CREATE TABLE order_items(order_id INTEGER, product_id INTEGER);
    CREATE TABLE featured(product_id INTEGER PRIMARY KEY);
    INSERT INTO featured VALUES (101),(102),(103);
    INSERT INTO orders VALUES (1,1),(2,1),(3,2),(4,2),(5,3),(6,4),(7,5);
    INSERT INTO order_items VALUES
     (1,101),(1,102),(2,102),(2,103),   -- cust 1: all three, product 102 twice
     (3,101),(3,101),(3,102),           -- cust 2: duplicate rows, only 101 and 102
     (4,101),                           -- cust 2: 101 again
     (5,101),(5,102),(5,103),(5,999),   -- cust 3: all three plus a non-featured product
     (6,555),                           -- cust 4: no featured product
     (7,103);                           -- cust 5: one featured product
    """)
    return con

con = build()
not_exists = """
SELECT c.customer_id
FROM (SELECT DISTINCT customer_id FROM orders) c
WHERE NOT EXISTS (
  SELECT 1 FROM featured f
  WHERE NOT EXISTS (
    SELECT 1 FROM orders o JOIN order_items i ON i.order_id = o.order_id
    WHERE o.customer_id = c.customer_id AND i.product_id = f.product_id))
ORDER BY c.customer_id
"""
having = """
SELECT o.customer_id
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
JOIN featured f ON f.product_id = i.product_id
GROUP BY o.customer_id
HAVING COUNT(DISTINCT f.product_id) = (SELECT COUNT(*) FROM featured)
ORDER BY o.customer_id
"""
wrong = """
SELECT o.customer_id, COUNT(*) AS rows_hit, COUNT(DISTINCT f.product_id) AS distinct_hit
FROM orders o JOIN order_items i ON i.order_id = o.order_id JOIN featured f ON f.product_id = i.product_id
GROUP BY o.customer_id ORDER BY o.customer_id
"""
a = pd.read_sql(not_exists, con); b = pd.read_sql(having, con)
print("double NOT EXISTS:", a.customer_id.tolist())
print("HAVING COUNT(DISTINCT):", b.customer_id.tolist())
print("rows vs distinct featured hits per customer (COUNT(*) >= 3 would wrongly pass customer 2):")
print(pd.read_sql(wrong, con).to_string(index=False)); print()

# pandas
orders = pd.read_sql("SELECT * FROM orders", con); items = pd.read_sql("SELECT * FROM order_items", con)
featured = pd.read_sql("SELECT * FROM featured", con)
def division(orders, items, featured):
    hit = orders.merge(items, on="order_id").merge(featured, on="product_id")[["customer_id", "product_id"]].drop_duplicates()
    cnt = hit.groupby("customer_id")["product_id"].nunique()
    return sorted(cnt[cnt == len(featured)].index.tolist())
p = division(orders, items, featured)
print("pandas nunique == len(featured):", p)
assert a.customer_id.tolist() == b.customer_id.tolist() == p
print("asserts passed (compared as sorted customer_id lists)"); print()

# empty featured list
con.execute("DELETE FROM featured")
a0 = pd.read_sql(not_exists, con).customer_id.tolist(); b0 = pd.read_sql(having, con).customer_id.tolist()
p0 = division(orders, items, featured.iloc[0:0])
sets = items.merge(orders, on="order_id").groupby("customer_id")["product_id"].agg(set)
p0_sets = sorted(sets[sets.apply(lambda s: set(featured.iloc[0:0]["product_id"]) <= s)].index.tolist())
print("empty featured -> NOT EXISTS:", a0, "| HAVING:", b0, "| pandas merge/nunique:", p0, "| pandas set subset:", p0_sets)
```

**Output (my run):**
```text
double NOT EXISTS: [1, 3]
HAVING COUNT(DISTINCT): [1, 3]
rows vs distinct featured hits per customer (COUNT(*) >= 3 would wrongly pass customer 2):
 customer_id  rows_hit  distinct_hit
           1         4             3
           2         4             2
           3         3             3
           5         1             1

pandas nunique == len(featured): [1, 3]
asserts passed (compared as sorted customer_id lists)

empty featured -> NOT EXISTS: [1, 2, 3, 4, 5] | HAVING: [] | pandas merge/nunique: [] | pandas set subset: [1, 2, 3, 4, 5]
```

**Edge cases:**
- **Duplicates:** duplicate item rows and the same product in two orders must collapse, so count DISTINCT products (HAVING) or test existence (NOT EXISTS, naturally duplicate-proof).
- **Non-featured items** (999, 555) are ignored by the join to `featured`.
- **Customers with no featured purchase** (4) never appear in the HAVING version because the join removes them; the NOT EXISTS version enumerates candidates from `orders` and rejects them.
- **Empty featured list:** in my run NOT EXISTS returned all 5 customers (no featured product is missing, so everyone qualifies vacuously) while HAVING returned nobody (the join to an empty table leaves no groups). pandas split the same way: the merge and `nunique` version returned nobody and a set-subset test returned everybody. The business rule decides; I would say it out loud and probably return nobody ("bought every product on an empty list" is not a useful target), which means adding a guard `AND EXISTS (SELECT 1 FROM featured)` to the NOT EXISTS form.
- **Candidates:** both versions treat a customer as someone with at least one order. A customer without orders is not in the data, so they cannot be returned.

**Then explain:**
- **Double NOT EXISTS reads as:** there is no featured product for which there is no purchase by this customer. It is the textbook division form and handles duplicates for free.
- **HAVING form:** join items to featured, group by customer, and compare `COUNT(DISTINCT f.product_id)` with `(SELECT COUNT(*) FROM featured)`. It is shorter and usually faster, but only correct with DISTINCT and fails differently on an empty list.
- **Which to pick:** HAVING when the list is a small stable table; NOT EXISTS when you must be vacuously correct or when the list is dynamic and you want the semantics to be obvious. Say both and the empty-list difference, which is what the prompt asks for.
- **pandas:** `drop_duplicates` before `nunique`, then compare with `len(featured)`; the set version `featured_set <= customer_set` is the NOT EXISTS reading.
- Part 3 Q14 and Q35 cover division in general; this question adds duplicates and the empty list.
- **Scoring note (Set F3, Q4 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (customers 1 and 3 by at least one of the two SQL forms), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: the HAVING form without DISTINCT passes the wrong customers and loses most query points; giving only one of the two SQL forms loses a few; the empty-list explanation is where the 5 edge-case points sit

**Follow-ups:**
- *Customers who bought at least two of the three?* Change HAVING to `>= 2`; NOT EXISTS no longer applies.
- *Within a time window?* Add the date filter in the join (or in the inner NOT EXISTS), not after the grouping.
- *What about a customer who returned a product?* Filter returns out before testing, and say what "bought" means.

**Common mistakes:**
- `COUNT(*)` instead of `COUNT(DISTINCT product_id)` so duplicate rows pass or fail the wrong people.
- Comparing to a hard-coded 3 instead of `(SELECT COUNT(*) FROM featured)`.
- Putting the featured filter in WHERE after a LEFT JOIN, silently turning it into an inner join.
- Not thinking about the empty featured list.

### Q5 ⭐⭐⭐ 🔴 [Set T1, Q5 of 5, 12 min, 25 pts] Velocity check (payments fraud rule). card_txns(txn_id, card_id, txn_ts TEXT 'YYYY-MM-DD HH:MM:SS', amount, status). Flag every card that has 3 or more APPROVED transactions inside any 10-minute window (window inclusive of the first transaction, 10:00:00 to 10:10:00 counts as 10 minutes), returning card_id, window start and count. Seed 4 cards including one with exactly 3 transactions spread over 10 minutes 1 second and one with a declined transaction that would otherwise make 3. Solve in SQL (LAG with offset 2 or a self join, Part 5 Q3 and Part 5 Q39) and pandas (shift or rolling on a time index). Note the SQLite 3.45 limit on RANGE frames over text timestamps.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Keep only APPROVED rows, turn the timestamp text into integer seconds, and for each approved transaction count approved transactions of the same card between its time and its time plus 600 seconds, inclusive; flag cards where that count is 3 or more.

**Schema and sample data:**
```sql
CREATE TABLE card_txns(txn_id INTEGER PRIMARY KEY, card_id INTEGER, txn_ts TEXT, amount INTEGER, status TEXT);
INSERT INTO card_txns VALUES
 (1,1,'2025-05-01 10:00:00',100,'APPROVED'),
 (2,1,'2025-05-01 10:04:00',100,'APPROVED'),
 (3,1,'2025-05-01 10:10:00',100,'APPROVED'),   -- exactly 10:00 after the first: counts
 (4,1,'2025-05-01 10:10:30',100,'APPROVED'),
 (5,2,'2025-05-01 11:00:00',100,'APPROVED'),
 (6,2,'2025-05-01 11:05:00',100,'APPROVED'),
 (7,2,'2025-05-01 11:10:01',100,'APPROVED'),   -- 10 min 1 sec after the first: too late
 (8,3,'2025-05-01 12:00:00',100,'APPROVED'),
 (9,3,'2025-05-01 12:02:00',100,'DECLINED'),   -- would be the third, but declined
 (10,3,'2025-05-01 12:04:00',100,'APPROVED'),
 (11,4,'2025-05-01 13:00:00',100,'APPROVED'),
 (12,4,'2025-05-01 13:01:00',100,'APPROVED'),
 (13,4,'2025-05-01 13:02:00',100,'APPROVED');
```

**SQL answer:** `windows_sql` in the Code block; `lag_sql` is the LAG offset 2 check and `range_sql` the RANGE frame over integer seconds.
`windows_sql` in the Code block:
```sql
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
)
SELECT x.card_id, x.txn_ts AS window_start, COUNT(*) AS txns
FROM a x JOIN a y ON y.card_id = x.card_id AND y.s BETWEEN x.s AND x.s + 600
GROUP BY x.card_id, x.txn_ts
HAVING COUNT(*) >= 3
ORDER BY x.card_id, x.txn_ts
```
`lag_sql` in the Code block:
```sql
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
), l AS (
  SELECT card_id, txn_ts, s, LAG(s, 2) OVER (PARTITION BY card_id ORDER BY s) AS s2,
         LAG(txn_ts, 2) OVER (PARTITION BY card_id ORDER BY s) AS ts2
  FROM a
)
SELECT card_id, MIN(ts2) AS first_window_start
FROM l WHERE s2 IS NOT NULL AND s - s2 <= 600
GROUP BY card_id ORDER BY card_id
```

**pandas answer:** per card, `searchsorted` on the sorted times counts how many fall inside `[t, t + 600s]`; `shift(2)` gives the LAG(2) version.
```py
# pandas: per card, sorted approved times; count txns in [t, t + 600s] with searchsorted
t = pd.read_sql("SELECT * FROM card_txns", con)
t = t[t["status"] == "APPROVED"].copy()
t["ts"] = pd.to_datetime(t["txn_ts"])
t = t.sort_values(["card_id", "ts"]).reset_index(drop=True)
def count_in_window(g):
    v = g["ts"].to_numpy()
    end = np.searchsorted(v, v + np.timedelta64(600, "s"), side="right")   # side=right keeps t+600s inclusive
    return pd.Series(end - np.arange(len(v)), index=g.index)
t["txns"] = t.groupby("card_id", group_keys=False).apply(count_in_window)
p = (t[t["txns"] >= 3][["card_id", "txn_ts", "txns"]]
     .rename(columns={"txn_ts": "window_start"}).reset_index(drop=True))
print("pandas windows:"); print(p.to_string(index=False)); print()
```

**Example:** Card 1 approved at 10:00:00, 10:04:00, 10:10:00 and 10:10:30. From the 10:00:00 start the window ends 10:10:00 and contains 3 rows (10:10:00 is exactly 600 seconds later and counts), so a flag with count 3. From 10:04:00 the window ends 10:14:00 and holds 10:04, 10:10 and 10:10:30, another 3. From 10:10:00 only 2. Card 2 has 11:00:00, 11:05:00 and 11:10:01: the third is 601 seconds after the first, so no window reaches 3. Card 3 has two approved rows and a declined one in between; after removing the decline only 2 remain. Card 4 has 13:00, 13:01 and 13:02, so 3. Flagged cards: 1 (two overlapping windows, first start 10:00:00) and 4.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q5: velocity check: >= 3 APPROVED txns in any 10-minute window (inclusive), per card.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE card_txns(txn_id INTEGER PRIMARY KEY, card_id INTEGER, txn_ts TEXT, amount INTEGER, status TEXT);
INSERT INTO card_txns VALUES
 (1,1,'2025-05-01 10:00:00',100,'APPROVED'),
 (2,1,'2025-05-01 10:04:00',100,'APPROVED'),
 (3,1,'2025-05-01 10:10:00',100,'APPROVED'),   -- exactly 10:00 after the first: counts
 (4,1,'2025-05-01 10:10:30',100,'APPROVED'),
 (5,2,'2025-05-01 11:00:00',100,'APPROVED'),
 (6,2,'2025-05-01 11:05:00',100,'APPROVED'),
 (7,2,'2025-05-01 11:10:01',100,'APPROVED'),   -- 10 min 1 sec after the first: too late
 (8,3,'2025-05-01 12:00:00',100,'APPROVED'),
 (9,3,'2025-05-01 12:02:00',100,'DECLINED'),   -- would be the third, but declined
 (10,3,'2025-05-01 12:04:00',100,'APPROVED'),
 (11,4,'2025-05-01 13:00:00',100,'APPROVED'),
 (12,4,'2025-05-01 13:01:00',100,'APPROVED'),
 (13,4,'2025-05-01 13:02:00',100,'APPROVED');
""")

windows_sql = """
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
)
SELECT x.card_id, x.txn_ts AS window_start, COUNT(*) AS txns
FROM a x JOIN a y ON y.card_id = x.card_id AND y.s BETWEEN x.s AND x.s + 600
GROUP BY x.card_id, x.txn_ts
HAVING COUNT(*) >= 3
ORDER BY x.card_id, x.txn_ts
"""
lag_sql = """
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
), l AS (
  SELECT card_id, txn_ts, s, LAG(s, 2) OVER (PARTITION BY card_id ORDER BY s) AS s2,
         LAG(txn_ts, 2) OVER (PARTITION BY card_id ORDER BY s) AS ts2
  FROM a
)
SELECT card_id, MIN(ts2) AS first_window_start
FROM l WHERE s2 IS NOT NULL AND s - s2 <= 600
GROUP BY card_id ORDER BY card_id
"""
range_sql = """
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
)
SELECT card_id, txn_ts AS window_start,
       COUNT(*) OVER (PARTITION BY card_id ORDER BY s RANGE BETWEEN CURRENT ROW AND 600 FOLLOWING) AS txns
FROM a ORDER BY card_id, txn_ts
"""
text_range = """
SELECT COUNT(*) OVER (PARTITION BY card_id ORDER BY txn_ts RANGE BETWEEN CURRENT ROW AND '10 minutes' FOLLOWING) FROM card_txns
"""
w = pd.read_sql(windows_sql, con)
print("SQL windows (self join on integer seconds):"); print(w.to_string(index=False)); print()
lg = pd.read_sql(lag_sql, con)
print("SQL LAG(...,2) cross-check, earliest window start per card:"); print(lg.to_string(index=False)); print()
rg = pd.read_sql(range_sql, con); rg = rg[rg.txns >= 3].reset_index(drop=True)
print("SQL RANGE frame over integer seconds (works):"); print(rg.to_string(index=False)); print()
try:
    con.execute(text_range).fetchall()
    print("RANGE with an interval string over text: no error")
except sqlite3.Error as e:
    print("RANGE with '10 minutes' over text timestamps ->", type(e).__name__, ":", e)
print()

# pandas: per card, sorted approved times; count txns in [t, t + 600s] with searchsorted
t = pd.read_sql("SELECT * FROM card_txns", con)
t = t[t["status"] == "APPROVED"].copy()
t["ts"] = pd.to_datetime(t["txn_ts"])
t = t.sort_values(["card_id", "ts"]).reset_index(drop=True)
def count_in_window(g):
    v = g["ts"].to_numpy()
    end = np.searchsorted(v, v + np.timedelta64(600, "s"), side="right")   # side=right keeps t+600s inclusive
    return pd.Series(end - np.arange(len(v)), index=g.index)
t["txns"] = t.groupby("card_id", group_keys=False).apply(count_in_window)
p = (t[t["txns"] >= 3][["card_id", "txn_ts", "txns"]]
     .rename(columns={"txn_ts": "window_start"}).reset_index(drop=True))
print("pandas windows:"); print(p.to_string(index=False)); print()
pd.testing.assert_frame_equal(w, p, check_dtype=False)
pd.testing.assert_frame_equal(w, rg, check_dtype=False)

# LAG(2) equivalent in pandas: shift(2), earliest start per card
t["ts2"] = t.groupby("card_id")["ts"].shift(2)
flag = t[(t["ts"] - t["ts2"]) <= pd.Timedelta(minutes=10)]
p_lag = flag.groupby("card_id", as_index=False)["ts2"].min()
p_lag["first_window_start"] = p_lag.pop("ts2").dt.strftime("%Y-%m-%d %H:%M:%S")
pd.testing.assert_frame_equal(lg, p_lag, check_dtype=False)
print("asserts passed (self join = RANGE-on-seconds = pandas searchsorted; LAG(2) = shift(2); order card_id, window_start)")
```

**Output (my run):**
```text
SQL windows (self join on integer seconds):
 card_id        window_start  txns
       1 2025-05-01 10:00:00     3
       1 2025-05-01 10:04:00     3
       4 2025-05-01 13:00:00     3

SQL LAG(...,2) cross-check, earliest window start per card:
 card_id  first_window_start
       1 2025-05-01 10:00:00
       4 2025-05-01 13:00:00

SQL RANGE frame over integer seconds (works):
 card_id        window_start  txns
       1 2025-05-01 10:00:00     3
       1 2025-05-01 10:04:00     3
       4 2025-05-01 13:00:00     3

RANGE with '10 minutes' over text timestamps -> OperationalError : frame ending offset must be a non-negative number

pandas windows:
 card_id        window_start  txns
       1 2025-05-01 10:00:00     3
       1 2025-05-01 10:04:00     3
       4 2025-05-01 13:00:00     3

asserts passed (self join = RANGE-on-seconds = pandas searchsorted; LAG(2) = shift(2); order card_id, window_start)
```

**Edge cases:**
- **Boundary:** `BETWEEN x.s AND x.s + 600` is inclusive at both ends, so exactly 10:00 apart counts and 10:01 apart does not (card 2). Say the inclusive rule before coding.
- **Declined rows must be removed before windowing,** not just before counting, otherwise the decline would still sit between rows and LAG(2) would look at the wrong transactions (card 3).
- **Overlapping windows:** card 1 has two flagged start times. Return all of them, or take `MIN(window_start)` per card if the output must be one row per card (the LAG check does that).
- **Same-second duplicates:** two rows with the same timestamp are both counted from each other (the self join is not affected by ties); LAG(2) needs a deterministic tiebreak such as txn_id.
- **Text timestamps:** the prompt's note: SQLite RANGE frames need a numeric ORDER BY. In my run `RANGE BETWEEN CURRENT ROW AND '10 minutes' FOLLOWING` over the text column raised `OperationalError: frame ending offset must be a non-negative number`; converting to integer seconds with `strftime('%s', ...)` made the RANGE frame work and match the self join. PostgreSQL has `RANGE BETWEEN CURRENT ROW AND INTERVAL '10 minutes' FOLLOWING` on timestamp columns (not executed here, from memory).
- **Time zones:** the text has no zone; assume one zone (UTC) for all cards.

**Then explain:**
- **Self join version:** it gives exactly the three things asked for: card, window start and count. It is O(rows per card squared), fine for a seeded test, and an index on (card, time) helps at scale (Part 11).
- **LAG with offset 2:** `LAG(s, 2)` is the time of the transaction two rows earlier on the same card; if `s - LAG(s, 2) <= 600`, then three approved transactions lie within 10 minutes. It flags the card cheaply and its window start is the lagged time, but it does not tell you a count above 3, which is why the self join is the main answer.
- **RANGE over seconds:** `COUNT(*) OVER (PARTITION BY card_id ORDER BY s RANGE BETWEEN CURRENT ROW AND 600 FOLLOWING)` ran and matched. It is concise but needs the numeric column.
- **pandas:** `searchsorted(..., side="right")` on the sorted times gives the index of the first row after the window, so the count is that index minus the row's own position. `rolling("10min")` on a time index is trailing (window ends at the row), so it answers the mirror question "window end" rather than "window start"; I did not use it here.
- The window definition and the inclusive rule are this book's assumptions, not a vendor rule.
- **Scoring note (Set T1, Q5 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (APPROVED filter, inclusive 10-minute window, windows and counts), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: a version that ignores the status filter, or uses a strict `<` at 10:00, loses most query points; LAG(2) with the right filter and boundary and no count is about three quarters of the query points

**Follow-ups:**
- *Flag the card once with the first window?* `MIN(window_start)` per card, as `lag_sql` does.
- *Rolling 24-hour limit on amount?* Same self join with `s + 86400` and `SUM(amount)`.
- *What about a streaming system?* A per-card sorted state of the last 2 timestamps is enough for the LAG(2) rule; not executed here.

**Common mistakes:**
- Counting declined transactions.
- Using `<` for the end of the window and missing the exact 10:00 case.
- Comparing text timestamps with arithmetic, or ordering by a non-ISO text.
- LAG(1) instead of LAG(2) for "3 or more".
- Reporting overlapping windows as separate fraud events without saying so.

### Q6 ⭐⭐⭐ 🔴 [Set T1, Q4 of 5, 12 min, 25 pts] Ledger versus bank settlement file (reconciliation). ledger(txn_id, amount_paise, txn_date) and bank_file(bank_ref, txn_id, amount_paise, settled_date). Produce one result with a status per txn_id: MATCHED, AMOUNT_MISMATCH, MISSING_IN_BANK, MISSING_IN_LEDGER or DUPLICATE_IN_BANK (bank_file lists the same txn_id twice). Seed 8 ledger rows and 9 bank rows covering every status. Emulate FULL OUTER JOIN in SQLite (Part 2 Q16 and Q32, compare Part 2 Q44) and use outer merge with indicator=True in pandas, deduplicating before the compare. Assert both give the same statuses.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Collapse the bank file to one row per txn_id first, then FULL OUTER JOIN it to the ledger and label each txn_id with a CASE in a fixed order: missing in bank, missing in ledger, duplicate in bank, amount mismatch, matched.

**Schema and sample data:**
```sql
CREATE TABLE ledger(txn_id TEXT, amount_paise INTEGER, txn_date TEXT);
CREATE TABLE bank_file(bank_ref TEXT, txn_id TEXT, amount_paise INTEGER, settled_date TEXT);
INSERT INTO ledger VALUES
 ('T1',10000,'2025-06-01'),('T2',25000,'2025-06-01'),('T3',5000,'2025-06-02'),('T4',7500,'2025-06-02'),
 ('T5',12000,'2025-06-03'),('T6',3000,'2025-06-03'),('T7',9900,'2025-06-04'),('T8',4000,'2025-06-04');
INSERT INTO bank_file VALUES
 ('B1','T1',10000,'2025-06-02'),('B2','T2',24500,'2025-06-02'),('B3','T3',5000,'2025-06-03'),
 ('B4','T4',7500,'2025-06-03'),('B5','T5',12000,'2025-06-04'),('B6','T5',12000,'2025-06-04'),
 ('B7','T6',3000,'2025-06-04'),('B8','T8',4000,'2025-06-05'),('B9','T9',1500,'2025-06-05');
```

**SQL answer:** `full_sql` (FULL OUTER JOIN, runs on SQLite 3.45) and `emul_sql` (LEFT JOIN plus UNION ALL anti-join, for engines without FULL JOIN) in the Code block.
`full_sql` in the Code block:
```sql
WITH b AS (                                    -- one row per txn_id: dedupe BEFORE comparing
  SELECT txn_id, COUNT(*) AS n_bank, MIN(amount_paise) AS bank_min, MAX(amount_paise) AS bank_max
  FROM bank_file GROUP BY txn_id
)
SELECT COALESCE(l.txn_id, b.txn_id) AS txn_id,
       l.amount_paise AS ledger_paise, b.bank_min AS bank_paise,
       CASE WHEN b.txn_id IS NULL THEN 'MISSING_IN_BANK'
            WHEN l.txn_id IS NULL THEN 'MISSING_IN_LEDGER'
            WHEN b.n_bank > 1 THEN 'DUPLICATE_IN_BANK'
            WHEN l.amount_paise <> b.bank_min THEN 'AMOUNT_MISMATCH'
            ELSE 'MATCHED' END AS status
FROM ledger l FULL OUTER JOIN b ON b.txn_id = l.txn_id
ORDER BY txn_id
```
`emul_sql` in the Code block:
```sql
WITH b AS (
  SELECT txn_id, COUNT(*) AS n_bank, MIN(amount_paise) AS bank_min FROM bank_file GROUP BY txn_id
), j AS (
  SELECT l.txn_id AS lid, b.txn_id AS bid, l.amount_paise AS lp, b.bank_min AS bp, b.n_bank AS n
  FROM ledger l LEFT JOIN b ON b.txn_id = l.txn_id
  UNION ALL
  SELECT NULL, b.txn_id, NULL, b.bank_min, b.n_bank FROM b WHERE NOT EXISTS (SELECT 1 FROM ledger l WHERE l.txn_id = b.txn_id)
)
SELECT COALESCE(lid, bid) AS txn_id, lp AS ledger_paise, bp AS bank_paise,
       CASE WHEN bid IS NULL THEN 'MISSING_IN_BANK'
            WHEN lid IS NULL THEN 'MISSING_IN_LEDGER'
            WHEN n > 1 THEN 'DUPLICATE_IN_BANK'
            WHEN lp <> bp THEN 'AMOUNT_MISMATCH'
            ELSE 'MATCHED' END AS status
FROM j ORDER BY txn_id
```

**pandas answer:** aggregate the bank file, outer merge with `indicator=True`, then `np.select` in the same order as the CASE.
```py
# pandas
ledger = pd.read_sql("SELECT * FROM ledger", con); bank = pd.read_sql("SELECT * FROM bank_file", con)
b = bank.groupby("txn_id", as_index=False).agg(n_bank=("bank_ref", "size"), bank_paise=("amount_paise", "min"))
m = ledger.merge(b, on="txn_id", how="outer", indicator=True)
m = m.rename(columns={"amount_paise": "ledger_paise"})
m["status"] = np.select(
    [m["_merge"] == "left_only", m["_merge"] == "right_only", m["n_bank"] > 1, m["ledger_paise"] != m["bank_paise"]],
    ["MISSING_IN_BANK", "MISSING_IN_LEDGER", "DUPLICATE_IN_BANK", "AMOUNT_MISMATCH"], default="MATCHED")
p = m[["txn_id", "ledger_paise", "bank_paise", "status"]].sort_values("txn_id").reset_index(drop=True)
print("pandas outer merge with indicator:"); print(p.to_string(index=False)); print()
```

**Example:** Ledger T1 to T8; bank has T1, T2, T3, T4, T5 (twice, B5 and B6), T6, T8 and T9. T1, T3, T4, T6, T8 have the same amount on both sides: MATCHED. T2 is 25000 in the ledger and 24500 in the bank: AMOUNT_MISMATCH. T5 appears twice in the bank: DUPLICATE_IN_BANK. T7 has no bank row: MISSING_IN_BANK. T9 has no ledger row: MISSING_IN_LEDGER. Counts: 5 matched, one of each other status, 9 txn_ids from 8 ledger and 9 bank rows (8 ledger ids plus T9).

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q6: ledger vs bank settlement file: one status per txn_id.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE ledger(txn_id TEXT, amount_paise INTEGER, txn_date TEXT);
CREATE TABLE bank_file(bank_ref TEXT, txn_id TEXT, amount_paise INTEGER, settled_date TEXT);
INSERT INTO ledger VALUES
 ('T1',10000,'2025-06-01'),('T2',25000,'2025-06-01'),('T3',5000,'2025-06-02'),('T4',7500,'2025-06-02'),
 ('T5',12000,'2025-06-03'),('T6',3000,'2025-06-03'),('T7',9900,'2025-06-04'),('T8',4000,'2025-06-04');
INSERT INTO bank_file VALUES
 ('B1','T1',10000,'2025-06-02'),('B2','T2',24500,'2025-06-02'),('B3','T3',5000,'2025-06-03'),
 ('B4','T4',7500,'2025-06-03'),('B5','T5',12000,'2025-06-04'),('B6','T5',12000,'2025-06-04'),
 ('B7','T6',3000,'2025-06-04'),('B8','T8',4000,'2025-06-05'),('B9','T9',1500,'2025-06-05');
""")

full_sql = """
WITH b AS (                                    -- one row per txn_id: dedupe BEFORE comparing
  SELECT txn_id, COUNT(*) AS n_bank, MIN(amount_paise) AS bank_min, MAX(amount_paise) AS bank_max
  FROM bank_file GROUP BY txn_id
)
SELECT COALESCE(l.txn_id, b.txn_id) AS txn_id,
       l.amount_paise AS ledger_paise, b.bank_min AS bank_paise,
       CASE WHEN b.txn_id IS NULL THEN 'MISSING_IN_BANK'
            WHEN l.txn_id IS NULL THEN 'MISSING_IN_LEDGER'
            WHEN b.n_bank > 1 THEN 'DUPLICATE_IN_BANK'
            WHEN l.amount_paise <> b.bank_min THEN 'AMOUNT_MISMATCH'
            ELSE 'MATCHED' END AS status
FROM ledger l FULL OUTER JOIN b ON b.txn_id = l.txn_id
ORDER BY txn_id
"""
emul_sql = """
WITH b AS (
  SELECT txn_id, COUNT(*) AS n_bank, MIN(amount_paise) AS bank_min FROM bank_file GROUP BY txn_id
), j AS (
  SELECT l.txn_id AS lid, b.txn_id AS bid, l.amount_paise AS lp, b.bank_min AS bp, b.n_bank AS n
  FROM ledger l LEFT JOIN b ON b.txn_id = l.txn_id
  UNION ALL
  SELECT NULL, b.txn_id, NULL, b.bank_min, b.n_bank FROM b WHERE NOT EXISTS (SELECT 1 FROM ledger l WHERE l.txn_id = b.txn_id)
)
SELECT COALESCE(lid, bid) AS txn_id, lp AS ledger_paise, bp AS bank_paise,
       CASE WHEN bid IS NULL THEN 'MISSING_IN_BANK'
            WHEN lid IS NULL THEN 'MISSING_IN_LEDGER'
            WHEN n > 1 THEN 'DUPLICATE_IN_BANK'
            WHEN lp <> bp THEN 'AMOUNT_MISMATCH'
            ELSE 'MATCHED' END AS status
FROM j ORDER BY txn_id
"""
naive_sql = "SELECT l.txn_id, COUNT(*) AS rows_out FROM ledger l JOIN bank_file b ON b.txn_id = l.txn_id GROUP BY l.txn_id HAVING COUNT(*) > 1"

s = pd.read_sql(full_sql, con)
e = pd.read_sql(emul_sql, con)
print("SQL FULL OUTER JOIN (SQLite 3.45):"); print(s.to_string(index=False)); print()
print("naive join without deduping bank_file, txn_ids that fan out:"); print(pd.read_sql(naive_sql, con).to_string(index=False)); print()
pd.testing.assert_frame_equal(s, e, check_dtype=False)

print("NULL trap in the compare:", con.execute("SELECT CASE WHEN 5 <> NULL THEN 'AMOUNT_MISMATCH' ELSE 'MATCHED' END, "
      "CASE WHEN 5 IS NOT NULL THEN 'AMOUNT_MISMATCH' ELSE 'MATCHED' END").fetchone(), "(<> vs IS NOT)"); print()

# pandas
ledger = pd.read_sql("SELECT * FROM ledger", con); bank = pd.read_sql("SELECT * FROM bank_file", con)
b = bank.groupby("txn_id", as_index=False).agg(n_bank=("bank_ref", "size"), bank_paise=("amount_paise", "min"))
m = ledger.merge(b, on="txn_id", how="outer", indicator=True)
m = m.rename(columns={"amount_paise": "ledger_paise"})
m["status"] = np.select(
    [m["_merge"] == "left_only", m["_merge"] == "right_only", m["n_bank"] > 1, m["ledger_paise"] != m["bank_paise"]],
    ["MISSING_IN_BANK", "MISSING_IN_LEDGER", "DUPLICATE_IN_BANK", "AMOUNT_MISMATCH"], default="MATCHED")
p = m[["txn_id", "ledger_paise", "bank_paise", "status"]].sort_values("txn_id").reset_index(drop=True)
print("pandas outer merge with indicator:"); print(p.to_string(index=False)); print()
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("status counts:", s["status"].value_counts().sort_index().to_dict())
print("asserts passed (FULL JOIN = UNION ALL emulation = pandas; compared after ordering by txn_id)")
```

**Output (my run):**
```text
SQL FULL OUTER JOIN (SQLite 3.45):
txn_id  ledger_paise  bank_paise            status
    T1       10000.0     10000.0           MATCHED
    T2       25000.0     24500.0   AMOUNT_MISMATCH
    T3        5000.0      5000.0           MATCHED
    T4        7500.0      7500.0           MATCHED
    T5       12000.0     12000.0 DUPLICATE_IN_BANK
    T6        3000.0      3000.0           MATCHED
    T7        9900.0         NaN   MISSING_IN_BANK
    T8        4000.0      4000.0           MATCHED
    T9           NaN      1500.0 MISSING_IN_LEDGER

naive join without deduping bank_file, txn_ids that fan out:
txn_id  rows_out
    T5         2

NULL trap in the compare: ('MATCHED', 'AMOUNT_MISMATCH') (<> vs IS NOT)

pandas outer merge with indicator:
txn_id  ledger_paise  bank_paise            status
    T1       10000.0     10000.0           MATCHED
    T2       25000.0     24500.0   AMOUNT_MISMATCH
    T3        5000.0      5000.0           MATCHED
    T4        7500.0      7500.0           MATCHED
    T5       12000.0     12000.0 DUPLICATE_IN_BANK
    T6        3000.0      3000.0           MATCHED
    T7        9900.0         NaN   MISSING_IN_BANK
    T8        4000.0      4000.0           MATCHED
    T9           NaN      1500.0 MISSING_IN_LEDGER

status counts: {'AMOUNT_MISMATCH': 1, 'DUPLICATE_IN_BANK': 1, 'MATCHED': 5, 'MISSING_IN_BANK': 1, 'MISSING_IN_LEDGER': 1}
asserts passed (FULL JOIN = UNION ALL emulation = pandas; compared after ordering by txn_id)
```

**Edge cases:**
- **Duplicates:** without pre-aggregating, T5 joins to two bank rows and appears twice (my run listed T5 with 2 rows out), which would double the reconciled amount. Collapse to one row per txn_id first, then test the count.
- **Order of the CASE matters:** a duplicate whose amounts also differ would be labelled DUPLICATE_IN_BANK because that test comes before the amount test. State that precedence. If duplicate rows can carry different amounts, add `COUNT(DISTINCT amount_paise)` to the aggregate.
- **NULL amounts:** `5 <> NULL` is NULL, so the CASE falls through to ELSE and says MATCHED (my run printed MATCHED for `<>` and AMOUNT_MISMATCH for `IS NOT`). Use `IS NOT` in SQLite (or `IS DISTINCT FROM` where available) if NULL amounts are possible; seed data has none.
- **Integers:** amounts are integer paise, so the compare is exact. With float rupees you would need a tolerance. The printed 10000.0 values in the output are only pandas turning integer columns into floats because the outer join created NaN.
- **Dates:** txn_date versus settled_date are different by design (settlement lag); they are not part of the status here. Late-arriving rows would show as MISSING_IN_BANK until they land.

**Then explain:**
- **FULL OUTER JOIN:** SQLite supports it from 3.39 (I ran it on 3.45.1). PostgreSQL supports it; MySQL does not and needs the UNION emulation (not executed here, from memory). `emul_sql` is the portable fallback and my run asserted it equals the real FULL JOIN (Part 2 Q16, Q32; compare Q44).
- **Dedupe before compare:** the bank side is aggregated to `n_bank` and an amount per txn_id, so the join is one to one and the status is per txn_id, one row each.
- **pandas:** `how="outer", indicator=True` gives `left_only`, `right_only` and `both`, which are exactly MISSING_IN_BANK, MISSING_IN_LEDGER and the rest. `np.select` evaluates conditions in order, like CASE.
- **Check:** count by status (my run printed 5 / 1 / 1 / 1 / 1) and make sure the total equals the number of distinct txn_ids on both sides, 9.
- Reconciliation, duplicates and idempotency are a common fintech theme, but this exact question is an expert design, not a verified company question.
- **Scoring note (Set T1, Q4 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (one status per txn_id with all five statuses), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: a plain INNER or LEFT JOIN that cannot show MISSING_IN_LEDGER loses about half the query points; forgetting to dedupe so T5 appears twice loses the duplicate status and the check points

**Follow-ups:**
- *Report the money gap?* Add the signed difference `ledger - bank` per status and total per status.
- *Match on txn_id and date?* Add the date to the join key and decide whether a one-day settlement lag is allowed.
- *Idempotent re-load?* A unique constraint on `(bank_ref)` or on `txn_id` plus a dedupe step; the DDL is not executed here.

**Common mistakes:**
- Joining without pre-aggregating the duplicate bank rows.
- LEFT JOIN only, which can never show bank rows missing from the ledger.
- Comparing amounts with `<>` when NULLs are possible.
- Putting the amount test before the duplicate test without saying it.
- Using `WHERE b.txn_id IS NULL OR l.txn_id IS NULL` and calling it a reconciliation (that shows only the missing ones).

### Q7 ⭐⭐⭐ 🔴 [Set T2, Q5 of 5, 12 min, 25 pts] Currency conversion at the rate valid on the day. fx_rates(currency, valid_from, rate_to_inr) is a history table (a rate applies from valid_from until the next row for that currency) and payments(payment_id, currency, paid_on, amount). Compute amount_inr using the latest rate on or before paid_on, show a payment with no earlier rate as NULL (not 0), and a payment made on the exact valid_from date. Seed 2 currencies with 3 rates each and 7 payments. Solve in SQL (correlated subquery or range join, Part 2 Q26, and the nearest-earlier idea of Part 2 Q36) and pandas merge_asof (Part 2 Q36). Assert both agree.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** For each payment take the latest fx row of the same currency with `valid_from <= paid_on` (correlated subquery with ORDER BY valid_from DESC LIMIT 1, or a LEAD-based range join) and multiply; no earlier rate leaves NULL, and pandas does the same with `merge_asof(by=currency, direction='backward')`.

**Schema and sample data:**
```sql
CREATE TABLE fx_rates(currency TEXT, valid_from TEXT, rate_to_inr REAL);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, currency TEXT, paid_on TEXT, amount REAL);
INSERT INTO fx_rates VALUES
 ('USD','2025-01-01',83.0),('USD','2025-02-01',84.5),('USD','2025-03-01',85.25),
 ('EUR','2025-01-15',90.0),('EUR','2025-02-15',91.5),('EUR','2025-03-15',93.0);
INSERT INTO payments VALUES
 (1,'USD','2025-01-10',100),   -- inside the first USD range
 (2,'USD','2025-02-01',200),   -- exactly on a valid_from: the new rate applies
 (3,'USD','2025-02-28',50),    -- day before the next change: still 84.5
 (4,'USD','2025-04-10',10),    -- after the last row: last rate carries on
 (5,'EUR','2025-01-10',100),   -- before the first EUR rate: NULL
 (6,'EUR','2025-03-15',40),    -- exactly on the last valid_from
 (7,'GBP','2025-02-01',10);    -- currency with no rate rows at all: NULL
```

**SQL answer:** `corr` (correlated subquery) and `rng` (LEAD-based range join) in the Code block; both gave the same rows.
`corr` in the Code block:
```sql
SELECT p.payment_id, p.currency, p.paid_on, p.amount,
       (SELECT r.rate_to_inr FROM fx_rates r
        WHERE r.currency = p.currency AND r.valid_from <= p.paid_on
        ORDER BY r.valid_from DESC LIMIT 1) AS rate,
       ROUND(p.amount * (SELECT r.rate_to_inr FROM fx_rates r
        WHERE r.currency = p.currency AND r.valid_from <= p.paid_on
        ORDER BY r.valid_from DESC LIMIT 1), 2) AS amount_inr
FROM payments p ORDER BY p.payment_id
```
`rng` in the Code block:
```sql
WITH r AS (
  SELECT currency, valid_from, rate_to_inr,
         LEAD(valid_from) OVER (PARTITION BY currency ORDER BY valid_from) AS valid_to   -- exclusive end
  FROM fx_rates
)
SELECT p.payment_id, p.currency, p.paid_on, p.amount, r.rate_to_inr AS rate,
       ROUND(p.amount * r.rate_to_inr, 2) AS amount_inr
FROM payments p
LEFT JOIN r ON r.currency = p.currency AND p.paid_on >= r.valid_from
           AND (r.valid_to IS NULL OR p.paid_on < r.valid_to)
ORDER BY p.payment_id
```

**pandas answer:** `merge_asof` on the date columns with `by="currency"`, both frames sorted on their key.
```py
# pandas merge_asof: both sides sorted on the date key, matched within currency
pay = pd.read_sql("SELECT * FROM payments", con, parse_dates=["paid_on"])
fx = pd.read_sql("SELECT * FROM fx_rates", con, parse_dates=["valid_from"])
m = pd.merge_asof(pay.sort_values("paid_on"), fx.sort_values("valid_from"),
                  left_on="paid_on", right_on="valid_from", by="currency",
                  direction="backward", allow_exact_matches=True)
m["amount_inr"] = (m["amount"] * m["rate_to_inr"]).round(2)
p = (m.rename(columns={"rate_to_inr": "rate"}).sort_values("payment_id").reset_index(drop=True))
p["paid_on"] = p["paid_on"].dt.strftime("%Y-%m-%d")
p = p[["payment_id", "currency", "paid_on", "amount", "rate", "amount_inr"]]
```

**Example:** USD rates: 83.0 from 01-01, 84.5 from 02-01, 85.25 from 03-01; EUR rates: 90.0 from 01-15, 91.5 from 02-15, 93.0 from 03-15. Payment 1 (USD, 01-10, 100) uses 83.0, so 8300. Payment 2 (USD, exactly 02-01, 200) uses the rate that starts that day, 84.5, so 16900. Payment 3 (USD, 02-28, 50) is still in the 84.5 period, 4225. Payment 4 (USD, 04-10, 10) is after the last row, so the last rate 85.25 applies, 852.5. Payment 5 (EUR, 01-10) is before the first EUR rate: NULL. Payment 6 (EUR, exactly 03-15, 40) uses 93.0, 3720. Payment 7 (GBP) has no rate rows at all: NULL.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q7: currency conversion at the rate valid on the payment day (latest rate on or before paid_on).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE fx_rates(currency TEXT, valid_from TEXT, rate_to_inr REAL);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, currency TEXT, paid_on TEXT, amount REAL);
INSERT INTO fx_rates VALUES
 ('USD','2025-01-01',83.0),('USD','2025-02-01',84.5),('USD','2025-03-01',85.25),
 ('EUR','2025-01-15',90.0),('EUR','2025-02-15',91.5),('EUR','2025-03-15',93.0);
INSERT INTO payments VALUES
 (1,'USD','2025-01-10',100),   -- inside the first USD range
 (2,'USD','2025-02-01',200),   -- exactly on a valid_from: the new rate applies
 (3,'USD','2025-02-28',50),    -- day before the next change: still 84.5
 (4,'USD','2025-04-10',10),    -- after the last row: last rate carries on
 (5,'EUR','2025-01-10',100),   -- before the first EUR rate: NULL
 (6,'EUR','2025-03-15',40),    -- exactly on the last valid_from
 (7,'GBP','2025-02-01',10);    -- currency with no rate rows at all: NULL
""")

corr = """
SELECT p.payment_id, p.currency, p.paid_on, p.amount,
       (SELECT r.rate_to_inr FROM fx_rates r
        WHERE r.currency = p.currency AND r.valid_from <= p.paid_on
        ORDER BY r.valid_from DESC LIMIT 1) AS rate,
       ROUND(p.amount * (SELECT r.rate_to_inr FROM fx_rates r
        WHERE r.currency = p.currency AND r.valid_from <= p.paid_on
        ORDER BY r.valid_from DESC LIMIT 1), 2) AS amount_inr
FROM payments p ORDER BY p.payment_id
"""
rng = """
WITH r AS (
  SELECT currency, valid_from, rate_to_inr,
         LEAD(valid_from) OVER (PARTITION BY currency ORDER BY valid_from) AS valid_to   -- exclusive end
  FROM fx_rates
)
SELECT p.payment_id, p.currency, p.paid_on, p.amount, r.rate_to_inr AS rate,
       ROUND(p.amount * r.rate_to_inr, 2) AS amount_inr
FROM payments p
LEFT JOIN r ON r.currency = p.currency AND p.paid_on >= r.valid_from
           AND (r.valid_to IS NULL OR p.paid_on < r.valid_to)
ORDER BY p.payment_id
"""
a = pd.read_sql(corr, con); b = pd.read_sql(rng, con)
print("SQL correlated subquery:"); print(a.to_string(index=False)); print()
pd.testing.assert_frame_equal(a, b, check_dtype=False)
print("range join with LEAD gives the same rows")

# pandas merge_asof: both sides sorted on the date key, matched within currency
pay = pd.read_sql("SELECT * FROM payments", con, parse_dates=["paid_on"])
fx = pd.read_sql("SELECT * FROM fx_rates", con, parse_dates=["valid_from"])
m = pd.merge_asof(pay.sort_values("paid_on"), fx.sort_values("valid_from"),
                  left_on="paid_on", right_on="valid_from", by="currency",
                  direction="backward", allow_exact_matches=True)
m["amount_inr"] = (m["amount"] * m["rate_to_inr"]).round(2)
p = (m.rename(columns={"rate_to_inr": "rate"}).sort_values("payment_id").reset_index(drop=True))
p["paid_on"] = p["paid_on"].dt.strftime("%Y-%m-%d")
p = p[["payment_id", "currency", "paid_on", "amount", "rate", "amount_inr"]]
print(); print("pandas merge_asof:"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("asserts passed (compared in payment_id order)")

# what goes wrong without allow_exact_matches
m2 = pd.merge_asof(pay.sort_values("paid_on"), fx.sort_values("valid_from"), left_on="paid_on",
                   right_on="valid_from", by="currency", allow_exact_matches=False).sort_values("payment_id")
print("with allow_exact_matches=False payment 2 gets rate", m2.loc[m2.payment_id == 2, "rate_to_inr"].iloc[0], "(should be 84.5)")
```

**Output (my run):**
```text
SQL correlated subquery:
 payment_id currency    paid_on  amount  rate  amount_inr
          1      USD 2025-01-10   100.0 83.00      8300.0
          2      USD 2025-02-01   200.0 84.50     16900.0
          3      USD 2025-02-28    50.0 84.50      4225.0
          4      USD 2025-04-10    10.0 85.25       852.5
          5      EUR 2025-01-10   100.0   NaN         NaN
          6      EUR 2025-03-15    40.0 93.00      3720.0
          7      GBP 2025-02-01    10.0   NaN         NaN

range join with LEAD gives the same rows

pandas merge_asof:
 payment_id currency    paid_on  amount  rate  amount_inr
          1      USD 2025-01-10   100.0 83.00      8300.0
          2      USD 2025-02-01   200.0 84.50     16900.0
          3      USD 2025-02-28    50.0 84.50      4225.0
          4      USD 2025-04-10    10.0 85.25       852.5
          5      EUR 2025-01-10   100.0   NaN         NaN
          6      EUR 2025-03-15    40.0 93.00      3720.0
          7      GBP 2025-02-01    10.0   NaN         NaN
asserts passed (compared in payment_id order)
with allow_exact_matches=False payment 2 gets rate 83.0 (should be 84.5)
```

**Edge cases:**
- **Exact valid_from date:** the rate applies from that day, so the test is `valid_from <= paid_on` (not `<`). In pandas this is `allow_exact_matches=True` (the default); with `False` my run gave payment 2 the older rate 83.0.
- **No earlier rate:** the subquery returns NULL, and `amount * NULL` is NULL, so the amount stays NULL, not 0 (payments 5 and 7). A 0 would silently understate revenue.
- **After the last row:** the last rate carries on forever (payment 4). In a real system decide on a staleness limit.
- **Duplicate valid_from for the same currency:** the subquery's LIMIT 1 would pick arbitrarily and the range join would return two rows per payment; add a unique key on `(currency, valid_from)`.
- **Rounding:** `ROUND(x, 2)` in SQLite and `Series.round(2)` in pandas can differ on exact halves (Part 10 found 703.125 gives 703.13 in SQLite and 703.12 in pandas); none of these seven products sits on a half. Money should be integer paise in a real table.
- **Types:** `merge_asof` needs matching key dtypes (both datetime here) and both frames sorted on their keys.

**Then explain:**
- **Correlated subquery:** the readable answer and it runs one lookup per payment. An index on `(currency, valid_from)` makes each lookup a seek (Part 11).
- **Range join:** `LEAD(valid_from)` turns the history into half-open ranges `[valid_from, valid_to)`; the payment matches the range that contains its date. A LEFT JOIN keeps unmatched payments with a NULL rate. It scales better when the payment table is large and the join can use the range.
- **pandas:** `merge_asof` is exactly the "nearest earlier" join (Part 2 Q36); the result order follows the sorted left frame, so the code sorts back by `payment_id` before comparing.
- **Why not a plain join:** an equality join on the date would match only payments made exactly on a rate change.
- **Other engines:** PostgreSQL, SQL Server and Snowflake accept the same correlated subquery (some prefer `TOP 1` or `FETCH FIRST 1 ROW ONLY`); ASOF JOIN exists in some engines (not executed here).
- **Scoring note (Set T2, Q5 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (all 7 payments with the right rate, NULL where none), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: joining on equality earns little; a subquery that uses `<` instead of `<=` fails payments 2 and 6 and loses the exact-date edge points; returning 0 instead of NULL loses the NULL points

**Follow-ups:**
- *Convert at the rate at month end instead?* Pick the rate with `valid_from <= month_end` and join on the month.
- *Payments in INR itself?* Add an `INR` row with rate 1.0 or a CASE; otherwise INR has no rate row and comes out NULL.
- *Many payments?* Index `(currency, valid_from)` and batch the lookup.

**Common mistakes:**
- Equality join on the date.
- Using the next rate (`>=` with ASC) instead of the previous one.
- `<` instead of `<=` for the exact valid_from day.
- Showing 0 for missing rates.
- Calling `merge_asof` on unsorted or differently typed keys.

### Q8 ⭐⭐⭐ 🔴 [Set T2, Q4 of 5, 12 min, 25 pts] Double-entry ledger audit. journal_lines(entry_id, line_no, account, debit_paise, credit_paise, posted_at) where every entry should sum debits equal credits, and account(account, kind). Return (a) entries that do not balance with the difference, and (b) for account 'WALLET' the first posting at which the running balance (credits minus debits) became negative, if ever, resolving two lines posted at the same second by (entry_id, line_no) (Part 5 Q6 and Q12). Seed 6 entries, one unbalanced and one with a tie in posted_at. Give SQL and pandas, and say why you must not use RANGE framing for the running balance.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** (a) GROUP BY entry_id and keep entries where SUM(debit) differs from SUM(credit); (b) for WALLET compute the running SUM of credit minus debit with an explicit ROWS frame ordered by posted_at, entry_id, line_no and take the first row below zero; never RANGE, because tied rows would get the same balance and hide the dip.

**Schema and sample data:**
```sql
CREATE TABLE account(account TEXT PRIMARY KEY, kind TEXT);
CREATE TABLE journal_lines(entry_id INTEGER, line_no INTEGER, account TEXT, debit_paise INTEGER, credit_paise INTEGER, posted_at TEXT);
INSERT INTO account VALUES ('WALLET','LIABILITY'),('CASH','ASSET'),('REVENUE','INCOME'),('BANK','ASSET');
INSERT INTO journal_lines VALUES
 (1,1,'CASH',   500,0,  '2025-06-01 09:00:00'),(1,2,'WALLET',0,500,'2025-06-01 09:00:00'),   -- wallet +500 = 500
 (2,1,'WALLET', 200,0,  '2025-06-01 10:00:00'),(2,2,'CASH',  0,200,'2025-06-01 10:00:00'),   -- wallet -200 = 300
 (3,1,'WALLET', 400,0,  '2025-06-01 11:00:00'),(3,2,'REVENUE',0,400,'2025-06-01 11:00:00'),  -- tie at 11:00:00, wallet -400
 (4,1,'BANK',   300,0,  '2025-06-01 11:00:00'),(4,2,'WALLET',0,300,'2025-06-01 11:00:00'),   -- tie at 11:00:00, wallet +300
 (5,1,'CASH',   100,0,  '2025-06-01 12:00:00'),(5,2,'REVENUE',0, 90,'2025-06-01 12:00:00'),  -- UNBALANCED by 10
 (6,1,'CASH',    50,0,  '2025-06-01 13:00:00'),(6,2,'WALLET',0, 50,'2025-06-01 13:00:00');
```

**SQL answer:** `unbal_sql`, `run_sql` and `first_neg_sql` in the Code block (`range_sql` is the RANGE version for comparison).
`unbal_sql` in the Code block:
```sql
SELECT entry_id, SUM(debit_paise) AS debits, SUM(credit_paise) AS credits,
       SUM(debit_paise) - SUM(credit_paise) AS diff
FROM journal_lines GROUP BY entry_id
HAVING SUM(debit_paise) <> SUM(credit_paise) ORDER BY entry_id
```
`run_sql` in the Code block:
```sql
SELECT j.entry_id, j.line_no, j.posted_at,
       SUM(j.credit_paise - j.debit_paise) OVER (ORDER BY j.posted_at, j.entry_id, j.line_no
                                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance
FROM journal_lines j JOIN account a ON a.account = j.account
WHERE j.account = 'WALLET' ORDER BY j.posted_at, j.entry_id, j.line_no
```
`first_neg_sql` in the Code block:
```sql
WITH r AS (%s)
SELECT entry_id, line_no, posted_at, balance FROM r WHERE balance < 0 ORDER BY posted_at, entry_id, line_no LIMIT 1
```

**pandas answer:** a groupby for the balance check, then sort by the three keys, `cumsum` of credit minus debit and the first row below zero.
```py
# pandas
jl = pd.read_sql("SELECT * FROM journal_lines", con)
g = jl.groupby("entry_id").agg(debits=("debit_paise", "sum"), credits=("credit_paise", "sum")).reset_index()
g["diff"] = g["debits"] - g["credits"]
pu = g[g["diff"] != 0].reset_index(drop=True)
w = jl[jl["account"] == "WALLET"].sort_values(["posted_at", "entry_id", "line_no"]).copy()
w["balance"] = (w["credit_paise"] - w["debit_paise"]).cumsum()
pr = w[["entry_id", "line_no", "posted_at", "balance"]].reset_index(drop=True)
pf = pr[pr["balance"] < 0].head(1).reset_index(drop=True)
```

**Example:** Six entries of two lines each. Entry 5 has debit 100 and credit 90, so it is unbalanced by 10. WALLET lines: entry 1 credit 500 at 09:00, balance 500; entry 2 debit 200 at 10:00, balance 300; entry 3 debit 400 at 11:00:00 and entry 4 credit 300 at the same 11:00:00; entry 6 credit 50 at 13:00. With the tie broken by entry_id, the 400 debit comes first: 300 minus 400 gives minus 100, the first negative posting (entry 3, line 1), then plus 300 gives 200, then plus 50 gives 250. If the tie were applied together, the net is minus 100 plus 300, and the balance would go straight from 300 to 200 and never be negative.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q8: double-entry audit: unbalanced entries, first negative WALLET balance, and why not RANGE.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE account(account TEXT PRIMARY KEY, kind TEXT);
CREATE TABLE journal_lines(entry_id INTEGER, line_no INTEGER, account TEXT, debit_paise INTEGER, credit_paise INTEGER, posted_at TEXT);
INSERT INTO account VALUES ('WALLET','LIABILITY'),('CASH','ASSET'),('REVENUE','INCOME'),('BANK','ASSET');
INSERT INTO journal_lines VALUES
 (1,1,'CASH',   500,0,  '2025-06-01 09:00:00'),(1,2,'WALLET',0,500,'2025-06-01 09:00:00'),   -- wallet +500 = 500
 (2,1,'WALLET', 200,0,  '2025-06-01 10:00:00'),(2,2,'CASH',  0,200,'2025-06-01 10:00:00'),   -- wallet -200 = 300
 (3,1,'WALLET', 400,0,  '2025-06-01 11:00:00'),(3,2,'REVENUE',0,400,'2025-06-01 11:00:00'),  -- tie at 11:00:00, wallet -400
 (4,1,'BANK',   300,0,  '2025-06-01 11:00:00'),(4,2,'WALLET',0,300,'2025-06-01 11:00:00'),   -- tie at 11:00:00, wallet +300
 (5,1,'CASH',   100,0,  '2025-06-01 12:00:00'),(5,2,'REVENUE',0, 90,'2025-06-01 12:00:00'),  -- UNBALANCED by 10
 (6,1,'CASH',    50,0,  '2025-06-01 13:00:00'),(6,2,'WALLET',0, 50,'2025-06-01 13:00:00');
""")

unbal_sql = """
SELECT entry_id, SUM(debit_paise) AS debits, SUM(credit_paise) AS credits,
       SUM(debit_paise) - SUM(credit_paise) AS diff
FROM journal_lines GROUP BY entry_id
HAVING SUM(debit_paise) <> SUM(credit_paise) ORDER BY entry_id
"""
run_sql = """
SELECT j.entry_id, j.line_no, j.posted_at,
       SUM(j.credit_paise - j.debit_paise) OVER (ORDER BY j.posted_at, j.entry_id, j.line_no
                                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance
FROM journal_lines j JOIN account a ON a.account = j.account
WHERE j.account = 'WALLET' ORDER BY j.posted_at, j.entry_id, j.line_no
"""
first_neg_sql = """
WITH r AS (%s)
SELECT entry_id, line_no, posted_at, balance FROM r WHERE balance < 0 ORDER BY posted_at, entry_id, line_no LIMIT 1
""" % run_sql
range_sql = """
SELECT entry_id, line_no, posted_at,
       SUM(credit_paise - debit_paise) OVER (ORDER BY posted_at) AS balance_default_range
FROM journal_lines WHERE account = 'WALLET' ORDER BY posted_at, entry_id, line_no
"""
u = pd.read_sql(unbal_sql, con); r = pd.read_sql(run_sql, con); f = pd.read_sql(first_neg_sql, con)
rg = pd.read_sql(range_sql, con)
print("(a) unbalanced entries:"); print(u.to_string(index=False)); print()
print("(b) WALLET running balance, ROWS frame, tie broken by entry_id, line_no:"); print(r.to_string(index=False)); print()
print("first negative posting:"); print(f.to_string(index=False)); print()
print("same data with ORDER BY posted_at only (default RANGE frame):"); print(rg.to_string(index=False))
print("min balance with RANGE:", rg["balance_default_range"].min(), "-> the dip is invisible"); print()

# pandas
jl = pd.read_sql("SELECT * FROM journal_lines", con)
g = jl.groupby("entry_id").agg(debits=("debit_paise", "sum"), credits=("credit_paise", "sum")).reset_index()
g["diff"] = g["debits"] - g["credits"]
pu = g[g["diff"] != 0].reset_index(drop=True)
w = jl[jl["account"] == "WALLET"].sort_values(["posted_at", "entry_id", "line_no"]).copy()
w["balance"] = (w["credit_paise"] - w["debit_paise"]).cumsum()
pr = w[["entry_id", "line_no", "posted_at", "balance"]].reset_index(drop=True)
pf = pr[pr["balance"] < 0].head(1).reset_index(drop=True)
print("pandas unbalanced:"); print(pu.to_string(index=False))
print("pandas first negative:"); print(pf.to_string(index=False))
pd.testing.assert_frame_equal(u, pu, check_dtype=False)
pd.testing.assert_frame_equal(r, pr, check_dtype=False)
pd.testing.assert_frame_equal(f, pf, check_dtype=False)
print("asserts passed (order posted_at, entry_id, line_no)")
```

**Output (my run):**
```text
(a) unbalanced entries:
 entry_id  debits  credits  diff
        5     100       90    10

(b) WALLET running balance, ROWS frame, tie broken by entry_id, line_no:
 entry_id  line_no           posted_at  balance
        1        2 2025-06-01 09:00:00      500
        2        1 2025-06-01 10:00:00      300
        3        1 2025-06-01 11:00:00     -100
        4        2 2025-06-01 11:00:00      200
        6        2 2025-06-01 13:00:00      250

first negative posting:
 entry_id  line_no           posted_at  balance
        3        1 2025-06-01 11:00:00     -100

same data with ORDER BY posted_at only (default RANGE frame):
 entry_id  line_no           posted_at  balance_default_range
        1        2 2025-06-01 09:00:00                    500
        2        1 2025-06-01 10:00:00                    300
        3        1 2025-06-01 11:00:00                    200
        4        2 2025-06-01 11:00:00                    200
        6        2 2025-06-01 13:00:00                    250
min balance with RANGE: 200 -> the dip is invisible

pandas unbalanced:
 entry_id  debits  credits  diff
        5     100       90    10
pandas first negative:
 entry_id  line_no           posted_at  balance
        3        1 2025-06-01 11:00:00     -100
asserts passed (order posted_at, entry_id, line_no)
```

**Edge cases:**
- **Tie rule:** two WALLET lines share 11:00:00. I order by `(entry_id, line_no)` as the prompt says. That is deterministic but arbitrary: with the credit first the balance would never dip. In real ledgers state which rule you use, or compare after netting everything with the same timestamp.
- **RANGE hides it:** with `ORDER BY posted_at` and the default frame (RANGE, peers included) both tied rows showed 200 in my run and the minimum was 200. The dip to minus 100 disappears.
- **Never negative:** the LIMIT 1 query returns no row, and the pandas `head(1)` returns an empty frame, so handle an empty result as "never".
- **Unbalanced detection** uses SUM, which skips NULL; a line with NULL debit and NULL credit is invisible. COALESCE if lines can carry NULLs. Rounding is not an issue because the amounts are integer paise.
- **Entries with lines on different posted_at** are fine for (a), which groups by entry only.
- **The `account` table** is joined in the running-balance query to validate accounts; use LEFT JOIN if a line with an unknown account must not vanish silently.

**Then explain:**
- **Why the ROWS frame:** ROWS counts physical rows in the order given, so each line gets its own running value. RANGE treats rows with the same ORDER BY value as one group (peers) and gives them the same value; the default frame when ORDER BY is present is RANGE UNBOUNDED PRECEDING, which is the usual trap (Part 5 Q6).
- **Why the order key has three parts:** `posted_at, entry_id, line_no` makes every row distinct, so the running balance is reproducible between runs.
- **(a) is plain aggregation:** `HAVING SUM(debit_paise) <> SUM(credit_paise)`; the difference column is debits minus credits (10 for entry 5).
- **pandas:** `cumsum` after `sort_values` is the ROWS frame; there is no RANGE behaviour to worry about unless you group by timestamp first.
- **Double entry:** every entry must sum debits equal to credits; this book's seed also keeps the sign rule (WALLET is a liability, so credits increase it) as a stated assumption.
- **Scoring note (Set T2, Q4 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (unbalanced entry 5 with diff 10 and the first negative WALLET posting at entry 3 line 1), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: (a) only is about half of the query points; a RANGE or timestamp-only ORDER BY running balance finds no negative and loses the tie points; naming the tie rule is the assumption credit

**Follow-ups:**
- *Which account balances are negative at the end of day?* Group the running balance per day, take the last row.
- *Enforce balance in the schema?* A deferred constraint or a check in the posting code; not executed here.
- *Net the tie instead?* Group by `posted_at` first, then cumulative sum; the dip would not be reported.

**Common mistakes:**
- `ORDER BY posted_at` alone with the default RANGE frame.
- Adding debits and credits on the wrong sign for the account kind.
- Comparing SUM(debit) with SUM(credit) over the whole table instead of per entry.
- Forgetting to state the tie rule.
- Returning the lowest balance instead of the first posting that went below zero (a different question).

### Q9 ⭐⭐⭐ 🔴 [Set T3, Q5 of 5, 15 min, 25 pts] pandas-first risk table (then the SQL). txns DataFrame(txn_id, customer_id, txn_date, amount) and customers DataFrame(customer_id, city) with a customer who has no transactions and a transaction whose customer_id is missing from customers. Build, per customer, the amount in the 30 days up to and including 2025-06-30, the share of that city's 30-day total, and the rank within city (ties share a rank, Part 4 Q2 and Q14, pandas Part 4 Q31). Keep customers with zero amount, treat the orphan transaction explicitly, and show the equivalent SQL on SQLite. Assert equal rows, order city then rank then customer_id.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Start from the pandas frames: filter the transactions to 2025-06-01 to 2025-06-30, sum per customer, map onto the customers table so a customer with no transactions gets 0, divide by the city total and rank within city with `method='min'`; the SQL is a LEFT JOIN from customers to the pre-aggregated window plus SUM() OVER and RANK() OVER.

**Schema and sample data (pandas DataFrames first; to_sql creates the SQLite tables):**
```sql
-- the DataFrames in the Code block are loaded into SQLite with to_sql, which creates these tables:
-- customers(customer_id INTEGER, city TEXT)
-- txns(txn_id INTEGER, customer_id INTEGER, txn_date TEXT, amount INTEGER)
customers = pd.DataFrame({"customer_id": [1, 2, 3, 4, 5, 6],
                          "city": ["Pune", "Pune", "Pune", "Delhi", "Delhi", "Delhi"]})
txns = pd.DataFrame({
    "txn_id": range(1, 12),
    "customer_id": [1, 1, 2, 3, 4, 4, 5, 2, 1, 99, 4],
    "txn_date": ["2025-06-05", "2025-06-30", "2025-06-10", "2025-06-12", "2025-06-01", "2025-06-20",
                 "2025-06-15", "2025-05-31", "2025-07-01", "2025-06-18", "2025-06-02"],
    "amount": [100, 50, 150, 100, 60, 40, 50, 999, 777, 300, 0]})
# customer 6 has no transactions; customer 99 (txn 10) is not in customers; txns 8 and 9 fall outside the window
```

**SQL answer:** `sql` and `orphan_sql` in the Code block.
`sql` in the Code block:
```sql
WITH a AS (
  SELECT customer_id, SUM(amount) AS amt FROM txns
  WHERE txn_date BETWEEN date('2025-06-30', '-29 days') AND '2025-06-30' GROUP BY customer_id
), r AS (
  SELECT c.customer_id, c.city, COALESCE(a.amt, 0) AS amount_30d
  FROM customers c LEFT JOIN a ON a.customer_id = c.customer_id
)
SELECT customer_id, city, amount_30d,
       ROUND(1.0 * amount_30d / NULLIF(SUM(amount_30d) OVER (PARTITION BY city), 0), 4) AS city_share,
       RANK() OVER (PARTITION BY city ORDER BY amount_30d DESC) AS city_rank
FROM r ORDER BY city, city_rank, customer_id
```
`orphan_sql` in the Code block:
```sql
SELECT t.customer_id, COUNT(*) AS txns, SUM(t.amount) AS amount_30d FROM txns t
WHERE t.txn_date BETWEEN date('2025-06-30', '-29 days') AND '2025-06-30'
  AND NOT EXISTS (SELECT 1 FROM customers c WHERE c.customer_id = t.customer_id)
GROUP BY t.customer_id
```

**pandas answer:** the pandas version is written first in the Code block (pandas-first, as the prompt says).
```py
# pandas first. Window = 2025-06-01 .. 2025-06-30 inclusive (30 days ending on the as-of date)
asof = pd.Timestamp("2025-06-30"); start = asof - pd.Timedelta(days=29)
t = txns.assign(txn_date=pd.to_datetime(txns["txn_date"]))
w = t[(t["txn_date"] >= start) & (t["txn_date"] <= asof)]
amt = w.groupby("customer_id")["amount"].sum()
risk = customers.assign(amount_30d=customers["customer_id"].map(amt).fillna(0).astype("int64"))
city_tot = risk.groupby("city")["amount_30d"].transform("sum")
risk["city_share"] = (risk["amount_30d"] / city_tot.where(city_tot != 0)).round(4)
risk["city_rank"] = risk.groupby("city")["amount_30d"].rank(method="min", ascending=False).astype("int64")
p = risk.sort_values(["city", "city_rank", "customer_id"]).reset_index(drop=True)
orphan_p = w[~w["customer_id"].isin(customers["customer_id"])].groupby("customer_id", as_index=False).agg(
    txns=("txn_id", "size"), amount_30d=("amount", "sum"))
```

**Example:** The window is 30 days ending 2025-06-30 inclusive: 2025-06-01 to 2025-06-30. Pune: customer 1 has 100 and 50 in the window (and a 777 on 07-01, outside) = 150; customer 2 has 150 in the window (and 999 on 05-31, outside) = 150; customer 3 has 100. City total 400, so shares 0.375, 0.375, 0.25. Customers 1 and 2 tie for rank 1 and customer 3 is rank 3 (RANK leaves a gap). Delhi: customer 4 has 60, 40 and a 0 amount = 100; customer 5 has 50; customer 6 has no transactions and shows 0. City total 150, shares 0.6667, 0.3333, 0.0. Transaction 10 belongs to customer 99, who is not in `customers`: it is not in any city table and is reported on its own (1 transaction, amount 300).

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q9: pandas-first risk table: 30-day amount per customer, share of city total, rank within city. Then the SQL.
import sqlite3
import pandas as pd

customers = pd.DataFrame({"customer_id": [1, 2, 3, 4, 5, 6],
                          "city": ["Pune", "Pune", "Pune", "Delhi", "Delhi", "Delhi"]})
txns = pd.DataFrame({
    "txn_id": range(1, 12),
    "customer_id": [1, 1, 2, 3, 4, 4, 5, 2, 1, 99, 4],
    "txn_date": ["2025-06-05", "2025-06-30", "2025-06-10", "2025-06-12", "2025-06-01", "2025-06-20",
                 "2025-06-15", "2025-05-31", "2025-07-01", "2025-06-18", "2025-06-02"],
    "amount": [100, 50, 150, 100, 60, 40, 50, 999, 777, 300, 0]})
# customer 6 has no transactions; customer 99 (txn 10) is not in customers; txns 8 and 9 fall outside the window

con = sqlite3.connect(":memory:")
customers.to_sql("customers", con, index=False)
txns.to_sql("txns", con, index=False)

# pandas first. Window = 2025-06-01 .. 2025-06-30 inclusive (30 days ending on the as-of date)
asof = pd.Timestamp("2025-06-30"); start = asof - pd.Timedelta(days=29)
t = txns.assign(txn_date=pd.to_datetime(txns["txn_date"]))
w = t[(t["txn_date"] >= start) & (t["txn_date"] <= asof)]
amt = w.groupby("customer_id")["amount"].sum()
risk = customers.assign(amount_30d=customers["customer_id"].map(amt).fillna(0).astype("int64"))
city_tot = risk.groupby("city")["amount_30d"].transform("sum")
risk["city_share"] = (risk["amount_30d"] / city_tot.where(city_tot != 0)).round(4)
risk["city_rank"] = risk.groupby("city")["amount_30d"].rank(method="min", ascending=False).astype("int64")
p = risk.sort_values(["city", "city_rank", "customer_id"]).reset_index(drop=True)
orphan_p = w[~w["customer_id"].isin(customers["customer_id"])].groupby("customer_id", as_index=False).agg(
    txns=("txn_id", "size"), amount_30d=("amount", "sum"))
print("window:", start.date(), "to", asof.date(), "(", (asof - start).days + 1, "days )")
print("pandas risk table:"); print(p.to_string(index=False)); print()
print("pandas orphan transactions (customer not in customers), reported separately:"); print(orphan_p.to_string(index=False)); print()

sql = """
WITH a AS (
  SELECT customer_id, SUM(amount) AS amt FROM txns
  WHERE txn_date BETWEEN date('2025-06-30', '-29 days') AND '2025-06-30' GROUP BY customer_id
), r AS (
  SELECT c.customer_id, c.city, COALESCE(a.amt, 0) AS amount_30d
  FROM customers c LEFT JOIN a ON a.customer_id = c.customer_id
)
SELECT customer_id, city, amount_30d,
       ROUND(1.0 * amount_30d / NULLIF(SUM(amount_30d) OVER (PARTITION BY city), 0), 4) AS city_share,
       RANK() OVER (PARTITION BY city ORDER BY amount_30d DESC) AS city_rank
FROM r ORDER BY city, city_rank, customer_id
"""
orphan_sql = """
SELECT t.customer_id, COUNT(*) AS txns, SUM(t.amount) AS amount_30d FROM txns t
WHERE t.txn_date BETWEEN date('2025-06-30', '-29 days') AND '2025-06-30'
  AND NOT EXISTS (SELECT 1 FROM customers c WHERE c.customer_id = t.customer_id)
GROUP BY t.customer_id
"""
off = pd.read_sql(sql.replace("'-29 days'", "'-30 days'"), con)
print("off-by-one check, window start minus 30 days (31 days): customer 2 amount =",
      int(off.loc[off.customer_id == 2, "amount_30d"].iloc[0]), "instead of 150"); print()
s = pd.read_sql(sql, con); so = pd.read_sql(orphan_sql, con)
print("SQL risk table:"); print(s.to_string(index=False)); print()
pd.testing.assert_frame_equal(s, p[s.columns], check_dtype=False)
pd.testing.assert_frame_equal(so, orphan_p, check_dtype=False)
print("asserts passed (order: city, city_rank, customer_id)")
```

**Output (my run):**
```text
window: 2025-06-01 to 2025-06-30 ( 30 days )
pandas risk table:
 customer_id  city  amount_30d  city_share  city_rank
           4 Delhi         100      0.6667          1
           5 Delhi          50      0.3333          2
           6 Delhi           0      0.0000          3
           1  Pune         150      0.3750          1
           2  Pune         150      0.3750          1
           3  Pune         100      0.2500          3

pandas orphan transactions (customer not in customers), reported separately:
 customer_id  txns  amount_30d
          99     1         300

off-by-one check, window start minus 30 days (31 days): customer 2 amount = 1149 instead of 150

SQL risk table:
 customer_id  city  amount_30d  city_share  city_rank
           4 Delhi         100      0.6667          1
           5 Delhi          50      0.3333          2
           6 Delhi           0      0.0000          3
           1  Pune         150      0.3750          1
           2  Pune         150      0.3750          1
           3  Pune         100      0.2500          3

asserts passed (order: city, city_rank, customer_id)
```

**Edge cases:**
- **Orphan transaction:** it has no city, so it cannot be in a city share. I keep it out of the city table, and print it in a separate result so the 300 is not lost. The alternative is an UNKNOWN city row; say which you chose. A plain inner join would drop it silently and a customers-only LEFT JOIN would too, so it needs its own anti-join check.
- **Customer with no transactions** stays because the join starts from `customers`; the amount is filled with 0 (`COALESCE` in SQL, `fillna(0)` in pandas).
- **Window boundary:** `as-of minus 29 days` through the as-of date is 30 days. My off-by-one check with minus 30 days (31 days) pulled in 05-31 and gave customer 2 an amount of 1149 instead of 150.
- **Ties:** equal amounts share a rank and the next rank skips (1, 1, 3); `method='dense'` or DENSE_RANK would give 1, 1, 2. A zero-amount customer still gets a rank.
- **City total zero:** the share would divide by zero; `NULLIF` in SQL and `where(total != 0)` in pandas give NULL/NaN. Not seeded here, since both cities have transactions.
- **Rounding:** `ROUND(..., 4)` in SQLite and `.round(4)` in pandas can differ on exact halves (Part 10); none of these shares is on a half. `map` plus `fillna` makes the amount a float in pandas, so the code casts it back to int.

**Then explain:**
- **Order of operations:** filter the window before aggregating; do the LEFT JOIN from the customers table after the aggregate, so customers without rows survive and the join cannot fan out.
- **Share:** `amount / SUM(amount) OVER (PARTITION BY city)`; the window function sees only the customer rows, not the orphan.
- **Rank:** `RANK() OVER (PARTITION BY city ORDER BY amount DESC)` equals `rank(method="min", ascending=False)` (Part 4 Q2 and Q14; pandas Part 4 Q31).
- **Equality of the two answers:** the assert compares the whole table in the order city, rank, customer_id, plus the orphan result.
- **Date handling:** pandas compares datetime values, SQL compares ISO text; both are right because ISO dates sort as text. If the column held timestamps, use `< as_of + 1 day` rather than `<= as_of`.
- **Scoring note (Set T3, Q5 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (the 6-row table with correct zero amounts, shares and tied ranks), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: a table that loses customer 6 (inner join) or ranks with ROW_NUMBER loses most query points; the explicit orphan result is the edge-case credit; writing the pandas version first and the SQL second is graded on equality, not order

**Follow-ups:**
- *Same table for a rolling 30 days each day?* Add a date spine and a range or self-join per day; the engine specifics are Part 5.
- *Orphans as a data-quality alert?* Run the orphan query on every load and fail on a threshold.
- *Dense rank instead?* Change `method="min"` to `"dense"` and `RANK` to `DENSE_RANK`.

**Common mistakes:**
- Inner join, so a customer with no transactions disappears.
- Filtering the window in WHERE after a LEFT JOIN, which turns it into an inner join.
- Including the orphan in a city total by accident.
- Off-by-one on the 30 days.
- ROW_NUMBER instead of RANK, so tied customers get different ranks.

### Q10 ⭐⭐⭐ 🔴 [Set T3, Q4 of 5, 12 min, 25 pts] Dormant then back (resurrection). wallet_activity(customer_id, activity_date) with possibly several rows per day. For each month of 2025 (spine of 6 months from Jan) return new customers, active customers who were also active the previous month, resurrected customers (active, not active last month, but active before that) and churned customers (active last month, not this month). Seed 8 customers. Builds on Part 6 Q33 and Part 6 Q18; SQL with a month spine and pandas with set operations on monthly sets. Define each bucket in one sentence first.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Define the buckets first: new (first ever active month is this one), retained (active this month and last month), resurrected (active this month, not last month, but active in some earlier month), churned (active last month and not this month); then compute each from monthly distinct customer sets over a month spine.

**Schema and sample data:**
```sql
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2024-12-20'),(1,'2025-01-05'),(1,'2025-01-20'),(1,'2025-02-03'),(1,'2025-03-03'),   -- Dec, Jan, Feb, Mar (two Jan rows)
 (2,'2025-01-10'),(2,'2025-04-02'),(2,'2025-05-01'),                                      -- Jan, gap Feb-Mar, back Apr: resurrected
 (3,'2025-02-14'),(3,'2025-03-14'),(3,'2025-03-15'),                                      -- new Feb, Mar, then churns
 (4,'2025-03-09'),(4,'2025-05-09'),                                                       -- new Mar, skips Apr, back May
 (5,'2025-01-30'),                                                                        -- Jan only: churned in Feb
 (6,'2024-10-11'),(6,'2025-03-21'),                                                       -- active in Oct 2024, back in Mar: resurrected
 (7,'2025-04-04'),(7,'2025-05-05'),(7,'2025-06-06'),                                      -- new Apr, retained
 (8,'2025-06-01');                                                                        -- new Jun
```

**SQL answer:** `sql` in the Code block (a VALUES CTE for the spine, `am` for distinct customer-months, `fst` for first months).
`sql` in the Code block:
```sql
WITH spine(m) AS (VALUES ('2025-01'),('2025-02'),('2025-03'),('2025-04'),('2025-05'),('2025-06')),
am AS (SELECT DISTINCT customer_id, substr(activity_date, 1, 7) AS m FROM wallet_activity),
fst AS (SELECT customer_id, MIN(m) AS fm FROM am GROUP BY customer_id),
s AS (SELECT m, strftime('%Y-%m', m || '-01', '-1 month') AS prev FROM spine)
SELECT s.m AS month,
  (SELECT COUNT(*) FROM am WHERE am.m = s.m) AS active,
  (SELECT COUNT(*) FROM fst WHERE fst.fm = s.m) AS new_customers,
  (SELECT COUNT(*) FROM am a WHERE a.m = s.m
     AND EXISTS (SELECT 1 FROM am p WHERE p.customer_id = a.customer_id AND p.m = s.prev)) AS retained,
  (SELECT COUNT(*) FROM am a WHERE a.m = s.m
     AND NOT EXISTS (SELECT 1 FROM am p WHERE p.customer_id = a.customer_id AND p.m = s.prev)
     AND EXISTS (SELECT 1 FROM am e WHERE e.customer_id = a.customer_id AND e.m < s.prev)) AS resurrected,
  (SELECT COUNT(*) FROM am p WHERE p.m = s.prev
     AND NOT EXISTS (SELECT 1 FROM am a WHERE a.customer_id = p.customer_id AND a.m = s.m)) AS churned
FROM s ORDER BY s.m
```

**pandas answer:** a dictionary of monthly sets, then set operations per month: `cur & prev`, `(cur - prev) & earlier`, `prev - cur`.
```py
# pandas: monthly sets
wa = pd.read_sql("SELECT * FROM wallet_activity", con)
wa["m"] = pd.to_datetime(wa["activity_date"]).dt.to_period("M")
sets = wa.groupby("m")["customer_id"].agg(set)
first = wa.groupby("customer_id")["m"].min()
rows = []
for m in pd.period_range("2025-01", "2025-06", freq="M"):
    cur = sets.get(m, set()); prev = sets.get(m - 1, set())
    earlier = set().union(*[v for k, v in sets.items() if k < m - 1])
    rows.append({"month": str(m), "active": len(cur),
                 "new_customers": int((first == m).sum()),
                 "retained": len(cur & prev),
                 "resurrected": len((cur - prev) & earlier),
                 "churned": len(prev - cur)})
```

**Example:** Active sets: Dec 2024 {1}; Jan {1, 2, 5}; Feb {1, 3}; Mar {1, 3, 4, 6}; Apr {2, 7}; May {2, 4, 7}; Jun {7, 8}. First months: customer 6 in Oct 2024 and customer 1 in Dec 2024, so neither is new in 2025. Jan: active 3, new {2, 5} = 2, retained {1} = 1 (active in Dec too), churned 0. Feb: active 2, new {3}, retained {1}, churned {2, 5} = 2. Mar: active 4, new {4}, retained {1, 3}, resurrected {6} (not in Feb, active back in Oct), churned 0. Apr: active 2, new {7}, resurrected {2} (seen in Jan), churned {1, 3, 4, 6} = 4. May: active 3, new 0, retained {2, 7}, resurrected {4}, churned 0. Jun: active 2, new {8}, retained {7}, churned {2, 4} = 2. The identity active = new + retained + resurrected holds every month.

**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.
```python
# Q10: new / retained / resurrected / churned customers per month of 2025.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2024-12-20'),(1,'2025-01-05'),(1,'2025-01-20'),(1,'2025-02-03'),(1,'2025-03-03'),   -- Dec, Jan, Feb, Mar (two Jan rows)
 (2,'2025-01-10'),(2,'2025-04-02'),(2,'2025-05-01'),                                      -- Jan, gap Feb-Mar, back Apr: resurrected
 (3,'2025-02-14'),(3,'2025-03-14'),(3,'2025-03-15'),                                      -- new Feb, Mar, then churns
 (4,'2025-03-09'),(4,'2025-05-09'),                                                       -- new Mar, skips Apr, back May
 (5,'2025-01-30'),                                                                        -- Jan only: churned in Feb
 (6,'2024-10-11'),(6,'2025-03-21'),                                                       -- active in Oct 2024, back in Mar: resurrected
 (7,'2025-04-04'),(7,'2025-05-05'),(7,'2025-06-06'),                                      -- new Apr, retained
 (8,'2025-06-01');                                                                        -- new Jun
""")

sql = """
WITH spine(m) AS (VALUES ('2025-01'),('2025-02'),('2025-03'),('2025-04'),('2025-05'),('2025-06')),
am AS (SELECT DISTINCT customer_id, substr(activity_date, 1, 7) AS m FROM wallet_activity),
fst AS (SELECT customer_id, MIN(m) AS fm FROM am GROUP BY customer_id),
s AS (SELECT m, strftime('%Y-%m', m || '-01', '-1 month') AS prev FROM spine)
SELECT s.m AS month,
  (SELECT COUNT(*) FROM am WHERE am.m = s.m) AS active,
  (SELECT COUNT(*) FROM fst WHERE fst.fm = s.m) AS new_customers,
  (SELECT COUNT(*) FROM am a WHERE a.m = s.m
     AND EXISTS (SELECT 1 FROM am p WHERE p.customer_id = a.customer_id AND p.m = s.prev)) AS retained,
  (SELECT COUNT(*) FROM am a WHERE a.m = s.m
     AND NOT EXISTS (SELECT 1 FROM am p WHERE p.customer_id = a.customer_id AND p.m = s.prev)
     AND EXISTS (SELECT 1 FROM am e WHERE e.customer_id = a.customer_id AND e.m < s.prev)) AS resurrected,
  (SELECT COUNT(*) FROM am p WHERE p.m = s.prev
     AND NOT EXISTS (SELECT 1 FROM am a WHERE a.customer_id = p.customer_id AND a.m = s.m)) AS churned
FROM s ORDER BY s.m
"""
s = pd.read_sql(sql, con)
print("SQL:"); print(s.to_string(index=False)); print()
assert (s["active"] == s["new_customers"] + s["retained"] + s["resurrected"]).all()
print("identity holds in SQL: active = new + retained + resurrected")

# pandas: monthly sets
wa = pd.read_sql("SELECT * FROM wallet_activity", con)
wa["m"] = pd.to_datetime(wa["activity_date"]).dt.to_period("M")
sets = wa.groupby("m")["customer_id"].agg(set)
first = wa.groupby("customer_id")["m"].min()
rows = []
for m in pd.period_range("2025-01", "2025-06", freq="M"):
    cur = sets.get(m, set()); prev = sets.get(m - 1, set())
    earlier = set().union(*[v for k, v in sets.items() if k < m - 1])
    rows.append({"month": str(m), "active": len(cur),
                 "new_customers": int((first == m).sum()),
                 "retained": len(cur & prev),
                 "resurrected": len((cur - prev) & earlier),
                 "churned": len(prev - cur)})
p = pd.DataFrame(rows)
print(); print("pandas:"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("asserts passed (order: month)")
```

**Output (my run):**
```text
SQL:
  month  active  new_customers  retained  resurrected  churned
2025-01       3              2         1            0        0
2025-02       2              1         1            0        2
2025-03       4              1         2            1        0
2025-04       2              1         0            1        4
2025-05       3              0         2            1        0
2025-06       2              1         1            0        2

identity holds in SQL: active = new + retained + resurrected

pandas:
  month  active  new_customers  retained  resurrected  churned
2025-01       3              2         1            0        0
2025-02       2              1         1            0        2
2025-03       4              1         2            1        0
2025-04       2              1         0            1        4
2025-05       3              0         2            1        0
2025-06       2              1         1            0        2
asserts passed (order: month)
```

**Edge cases:**
- **Several rows per day or month:** `SELECT DISTINCT customer_id, substr(activity_date, 1, 7)` collapses them first; customer 1 has two January rows and counts once.
- **Activity before the spine:** customers 1 and 6 were active in Oct and Dec 2024. They are not new in 2025, and January retained and Mar resurrected need those earlier months, so the activity table must not be cut at January.
- **Churn is per event:** customer 4 is churned in April and resurrected in May; customer 2 churned in Feb (not active) and appears again in Apr. A customer can be counted in churned many times over the year.
- **Month spine:** a CTE with VALUES gives the six months even if one had no activity. Previous month is computed with `strftime('%Y-%m', m || '-01', '-1 month')`; anchoring on the first of the month avoids month-end rollover (Part 10 found DATE('2024-02-30') rolls over).
- **Churned reading:** it counts customers active last month and not this month, not customers inactive for N days.
- **Empty month:** `sets.get(m, set())` in pandas and COUNT over an empty subquery in SQL both give 0.

**Then explain:**
- **Definitions:** new is about the first month ever; retained and resurrected are about the pair (this month, last month) plus earlier history; churned looks backwards from the last month. These four plus the identity let you check your own numbers.
- **SQL:** each bucket is a count of rows in `am` with an EXISTS or NOT EXISTS against the previous month or an earlier month. The correlated subqueries are small on this data; on a big table build one row per customer-month with LAG and a running first-month instead.
- **pandas:** monthly sets make the definitions almost literal. `(cur - prev) & earlier` is "not last month but earlier"; `earlier` is the union of all months before the previous one.
- **Sanity checks:** active this month equals new plus retained plus resurrected; and active last month equals retained plus churned. My run asserted the first on the SQL side.
- Part 6 Q33 and Q18 cover the building blocks; this question joins them.
- **Scoring note (Set T3, Q4 of 5, 25 pts, by the part header rubric):** 10 points for a correct query on the seed data (all four buckets for all six months), 5 for naming and handling the seeded edge case, 5 for the pandas version, 2.5 for stating the assumption before coding, 2.5 for a one-line check. Partial credit: new and retained only is about half of the query points; mixing up resurrected with new loses the edge points; the one-sentence definitions are the assumption credit and the identity is the one-line check

**Follow-ups:**
- *Reactivation after 90 days of silence?* Compare each activity month with the gap since the previous one (LAG on months) instead of fixed previous-month sets.
- *Quick-ratio style metric?* (new + resurrected) divided by churned per month, with a NULLIF guard.
- *Daily instead of monthly?* Same logic over a date spine, but the sets get large; use LAG over distinct days.

**Common mistakes:**
- Counting rows instead of distinct customers when there are several rows per month.
- Cutting the activity history at January so first months are wrong.
- Defining resurrected as 'new again' without the earlier-history test.
- Forgetting that prev for January is December of the previous year.
- Starting the spine from the first month with data, so empty months are missing.

### Q11 ⭐⭐⭐ 🔴 [Set E1, Q5 of 5, 12 min, 25 pts] Checkout funnel with order (e-commerce). events(user_id, event_ts, event_name) with names view, add_to_cart, checkout, purchase. Return the number of users reaching each step in strict order (a later step counts only if it happens after the earlier step for the same user, Part 8 Q7 and Q9), plus step-to-step and overall conversion. Seed 10 users, including a user who purchases before adding to cart and a user with two views. Solve in SQL (MIN(CASE) per step) and pandas (groupby min per step), assert equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** For each user take the earliest `view`, then the earliest `add_to_cart` that is strictly later than that view, then the earliest `checkout` later than that, then the earliest `purchase` later than that; count users who got through each step, and divide by the previous step and by step 1.

**Schema and sample data:** (assumption said out loud: a step only counts if its time is strictly later than the time of the step before it, so two events with the same timestamp do not count as "in order"; users who never viewed are not in the funnel.)
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 10:00:00','view'),(1,'2025-03-01 10:05:00','add_to_cart'),(1,'2025-03-01 10:10:00','checkout'),(1,'2025-03-01 10:15:00','purchase'),
 (2,'2025-03-01 10:00:00','view'),(2,'2025-03-01 10:05:00','add_to_cart'),(2,'2025-03-01 10:10:00','checkout'),
 (3,'2025-03-01 10:00:00','view'),(3,'2025-03-01 10:05:00','add_to_cart'),
 (4,'2025-03-01 10:00:00','view'),
 (5,'2025-03-01 09:00:00','view'),(5,'2025-03-01 09:10:00','checkout'),(5,'2025-03-01 09:20:00','purchase'),(5,'2025-03-01 09:30:00','add_to_cart'),
 (6,'2025-03-01 10:00:00','view'),(6,'2025-03-01 10:10:00','add_to_cart'),(6,'2025-03-01 10:20:00','view'),
 (7,'2025-03-01 09:00:00','add_to_cart'),(7,'2025-03-01 09:30:00','view'),(7,'2025-03-01 10:00:00','add_to_cart'),(7,'2025-03-01 10:10:00','checkout'),(7,'2025-03-01 10:20:00','purchase'),
 (8,'2025-03-01 10:00:00','add_to_cart'),(8,'2025-03-01 10:05:00','checkout'),(8,'2025-03-01 10:10:00','purchase'),
 (9,'2025-03-01 10:00:00','view'),(9,'2025-03-01 10:00:00','add_to_cart'),
 (10,'2025-03-02 11:00:00','view'),(10,'2025-03-02 11:05:00','add_to_cart'),(10,'2025-03-02 11:10:00','checkout'),(10,'2025-03-02 11:15:00','purchase'),(10,'2025-03-02 11:20:00','purchase');
```

**SQL answer:** the query `sql` in the Code block. It chains four CTEs: `s1` is the first view per user; `s2` joins `s1` back to `events` and keeps `add_to_cart` events with `event_ts > s1.t`, then takes the MIN; `s3` and `s4` repeat that for `checkout` and `purchase`. A `UNION ALL` of the four counts gives the funnel, and `LAG` and `FIRST_VALUE` give the step and overall conversion.

**pandas answer:** the loop in the Code block. It keeps a frame `cur` of (user_id, t) for the previous step, merges the next step's events on `user_id`, filters `event_ts > t`, and takes `groupby('user_id').min()`. The row count at each step is the funnel count.

**Example:** by hand, per user (V = view, C = cart, K = checkout, P = purchase):
- User 1 and user 10: V, C, K, P in order, so they reach step 4 (user 10 has two purchases, still one user).
- User 2: V, C, K, then stops: step 3. User 3: V, C: step 2. User 4: V only: step 1.
- User 5: V 09:00, checkout 09:10, purchase 09:20, cart 09:30. The cart is after the view, so step 2 is reached; no checkout is later than 09:30, so the funnel stops at step 2 even though a purchase exists (purchase before add_to_cart).
- User 6: two views (10:00 and 10:20) and a cart at 10:10; the first view is 10:00, so the cart counts: step 2.
- User 7: cart 09:00, view 09:30, cart 10:00, checkout, purchase. The first cart is before the view, but the cart at 10:00 is after it, so the strict funnel counts this user through step 4.
- User 8: never viewed: not in step 1. User 9: view and cart at the same second: the cart is not strictly later, so step 1 only.
- Totals: step 1 = 9 (users 1 to 7, 9, 10), step 2 = 7 (1, 2, 3, 5, 6, 7, 10), step 3 = 4 (1, 2, 7, 10), step 4 = 3 (1, 7, 10). Conversions: 7/9 = 0.7778, 4/7 = 0.5714, 3/4 = 0.75; overall 3/9 = 0.3333.

**Code:** run with `python3 -I`.
```python
# Q11: strict-order checkout funnel (SQL chained MIN per step, pandas groupby min per step)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 10:00:00','view'),(1,'2025-03-01 10:05:00','add_to_cart'),(1,'2025-03-01 10:10:00','checkout'),(1,'2025-03-01 10:15:00','purchase'),
 (2,'2025-03-01 10:00:00','view'),(2,'2025-03-01 10:05:00','add_to_cart'),(2,'2025-03-01 10:10:00','checkout'),
 (3,'2025-03-01 10:00:00','view'),(3,'2025-03-01 10:05:00','add_to_cart'),
 (4,'2025-03-01 10:00:00','view'),
 (5,'2025-03-01 09:00:00','view'),(5,'2025-03-01 09:10:00','checkout'),(5,'2025-03-01 09:20:00','purchase'),(5,'2025-03-01 09:30:00','add_to_cart'),
 (6,'2025-03-01 10:00:00','view'),(6,'2025-03-01 10:10:00','add_to_cart'),(6,'2025-03-01 10:20:00','view'),
 (7,'2025-03-01 09:00:00','add_to_cart'),(7,'2025-03-01 09:30:00','view'),(7,'2025-03-01 10:00:00','add_to_cart'),(7,'2025-03-01 10:10:00','checkout'),(7,'2025-03-01 10:20:00','purchase'),
 (8,'2025-03-01 10:00:00','add_to_cart'),(8,'2025-03-01 10:05:00','checkout'),(8,'2025-03-01 10:10:00','purchase'),
 (9,'2025-03-01 10:00:00','view'),(9,'2025-03-01 10:00:00','add_to_cart'),
 (10,'2025-03-02 11:00:00','view'),(10,'2025-03-02 11:05:00','add_to_cart'),(10,'2025-03-02 11:10:00','checkout'),(10,'2025-03-02 11:15:00','purchase'),(10,'2025-03-02 11:20:00','purchase');
""")

# strict order: each step uses the EARLIEST event of that step that is later than the previous step's time
sql = """
WITH s1 AS (SELECT user_id, MIN(event_ts) AS t FROM events WHERE event_name = 'view' GROUP BY user_id),
s2 AS (SELECT s1.user_id, MIN(e.event_ts) AS t FROM s1 JOIN events e
         ON e.user_id = s1.user_id AND e.event_name = 'add_to_cart' AND e.event_ts > s1.t GROUP BY s1.user_id),
s3 AS (SELECT s2.user_id, MIN(e.event_ts) AS t FROM s2 JOIN events e
         ON e.user_id = s2.user_id AND e.event_name = 'checkout' AND e.event_ts > s2.t GROUP BY s2.user_id),
s4 AS (SELECT s3.user_id, MIN(e.event_ts) AS t FROM s3 JOIN events e
         ON e.user_id = s3.user_id AND e.event_name = 'purchase' AND e.event_ts > s3.t GROUP BY s3.user_id),
f AS (
  SELECT 1 AS step, 'view' AS step_name, COUNT(*) AS users FROM s1
  UNION ALL SELECT 2, 'add_to_cart', COUNT(*) FROM s2
  UNION ALL SELECT 3, 'checkout', COUNT(*) FROM s3
  UNION ALL SELECT 4, 'purchase', COUNT(*) FROM s4)
SELECT step, step_name, users,
       ROUND(1.0 * users / LAG(users) OVER (ORDER BY step), 4) AS step_conv,
       ROUND(1.0 * users / FIRST_VALUE(users) OVER (ORDER BY step), 4) AS overall_conv
FROM f ORDER BY step
"""
a = pd.read_sql(sql, con)
print("SQL strict funnel"); print(a.to_string(index=False))

# the 'simple' MIN(CASE) per step, with and without chaining, to show where each goes wrong
simple = """
WITH t AS (SELECT user_id,
  MIN(CASE WHEN event_name='view' THEN event_ts END) AS v,
  MIN(CASE WHEN event_name='add_to_cart' THEN event_ts END) AS c,
  MIN(CASE WHEN event_name='checkout' THEN event_ts END) AS k,
  MIN(CASE WHEN event_name='purchase' THEN event_ts END) AS p
  FROM events GROUP BY user_id)
SELECT COUNT(v) AS view_n, COUNT(c) AS cart_any, COUNT(k) AS checkout_any, COUNT(p) AS purchase_any,
  SUM(c > v) AS cart_chain, SUM(c > v AND k > c) AS checkout_chain, SUM(c > v AND k > c AND p > k) AS purchase_chain
FROM t
"""
print("\nsimple MIN(CASE) counts (no order / chained min):")
print(pd.read_sql(simple, con).to_string(index=False))

# pandas: same chain, one merge per step
ev = pd.read_sql("SELECT * FROM events", con)
cur = ev[ev.event_name == "view"].groupby("user_id")["event_ts"].min().rename("t").reset_index()
counts = [("view", len(cur))]
for name in ["add_to_cart", "checkout", "purchase"]:
    nxt = ev[ev.event_name == name][["user_id", "event_ts"]].merge(cur, on="user_id")
    nxt = nxt[nxt.event_ts > nxt.t].groupby("user_id")["event_ts"].min().rename("t").reset_index()
    counts.append((name, len(nxt)))
    cur = nxt
p = pd.DataFrame(counts, columns=["step_name", "users"])
p.insert(0, "step", range(1, 5))
p["step_conv"] = (p.users / p.users.shift(1)).round(4)
p["overall_conv"] = (p.users / p.users.iloc[0]).round(4)
print("\npandas strict funnel"); print(p.to_string(index=False))
# compare in step order (both already ordered by step)
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: SQL == pandas, rows in step order")
```

**Output (my run):**
```text
SQL strict funnel
 step   step_name  users  step_conv  overall_conv
    1        view      9        NaN        1.0000
    2 add_to_cart      7     0.7778        0.7778
    3    checkout      4     0.5714        0.4444
    4    purchase      3     0.7500        0.3333

simple MIN(CASE) counts (no order / chained min):
 view_n  cart_any  checkout_any  purchase_any  cart_chain  checkout_chain  purchase_chain
      9         9             6             5           6               3               2

pandas strict funnel
 step   step_name  users  step_conv  overall_conv
    1        view      9        NaN        1.0000
    2 add_to_cart      7     0.7778        0.7778
    3    checkout      4     0.5714        0.4444
    4    purchase      3     0.7500        0.3333

assert passed: SQL == pandas, rows in step order
```

**Edge cases:**
- **Purchase before cart (user 5):** a plain count of users with a purchase event would include them; the strict chain does not. The "any event" counts in the second printed table (`cart_any` 9, `checkout_any` 6, `purchase_any` 5) show how far an unordered funnel overstates.
- **Earliest-after, not global MIN (user 7):** the "chained MIN(CASE)" version (`cart_chain`, `checkout_chain`, `purchase_chain`: 6, 3, 2) takes each step's overall first time and compares it with the previous one. User 7's first cart (09:00) is before the first view (09:30), so that version drops them, and undercounts steps 2 to 4 by one. The fix is to take the earliest event after the previous step, as the Code block does. The prompt's "MIN(CASE) per step" idea is fine for the first step and for a funnel where order is not enforced; for strict order it needs the "later than" join.
- **Ties in time (user 9):** a same-timestamp view and cart do not count here (`>`); say if your product would count them (`>=`).
- **Repeat events (users 6 and 10):** MIN per user collapses them, so counts are users, not events.
- **Empty step:** if no user reaches a step, the `JOIN` returns no rows and `COUNT(*)` returns 0, so the funnel row still appears.

**Then explain:**
- **Why strict order:** an unordered funnel counts a purchase that has no cart before it (data fix-ups, duplicated events, clock skew, or a re-order link), and conversion can then even look better than reality.
- **The conversion columns:** step conversion divides by the previous step (`LAG`), overall conversion divides by step 1 (`FIRST_VALUE`). The first step has no previous step, so its step conversion is NULL in SQL and NaN in pandas.
- **Dialects (not executed here):** the same SQL works on PostgreSQL, MySQL 8, BigQuery and Snowflake (they all have `LAG` and `FIRST_VALUE`); `ROUND` and the `1.0 *` cast to avoid integer division are the usual small changes.
- **Scoring note (Set E1, Q5 of 5, 25 pts):** about 10 points for the right counts on the seed (9, 7, 4, 3), 5 for handling the seeded trap (user 5 and user 7, or at least user 5), 5 for the pandas version asserted equal, 2.5 for saying the order and tie assumption before coding, 2.5 for a check such as "step 1 is never smaller than step 2". Full marks need the "later than the previous step" join; the global-MIN version with the right numbers on a lucky seed earns partial credit only.

**Follow-ups:**
- *Add a time limit (purchase within 24 hours of the view)?* Add `AND e.event_ts <= datetime(s1.t, '+1 day')` style conditions in the join, measured from step 1, and state whether the window starts at the first view.
- *Do it by session?* Replace `user_id` with `session_id` in every join; the logic does not change.
- *How do you break it down by channel?* Add the channel to the select and `GROUP BY`, keeping the user in the step CTEs, or compute per channel in pandas with a groupby around the loop.

**Common mistakes:**
- Counting users with any `purchase` event as step 4 and ignoring order.
- Comparing global minimums per step (loses users like user 7).
- Counting events rather than distinct users (user 10's two purchases).
- Dividing by the wrong denominator, or integer division in SQL (`3/9` gives 0 without `1.0 *`).
- Forgetting that the first step's step-conversion is undefined.

### Q12 ⭐⭐⭐ 🔴 [Set E1, Q4 of 5, 12 min, 25 pts] Net revenue after returns without fan-out. orders(order_id, customer_id, order_date, shipping_fee), order_items(item_id, order_id, product_id, qty, unit_price) and returns(return_id, item_id, qty_returned, refund_amount) where one item can have two partial returns. Return net revenue per order (items minus refunds, shipping excluded) and the share of orders with any return. Show the naive three-table join total, why it is wrong (Part 2 Q12, Part 8 Q10), then the pre-aggregated version in SQL and pandas. Seed 5 orders.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Aggregate each child table to the order grain first (item total per order, refund total per order), then join the two one-row-per-order results to `orders`; a direct three-table join repeats an item's line total once for every return row of that item and overstates revenue.

**Schema and sample data:** (assumption: net revenue = sum of `qty * unit_price` minus the sum of `refund_amount`, shipping excluded; "orders with any return" counts orders that have at least one return row.)
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, shipping_fee INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id TEXT, qty INTEGER, unit_price INTEGER);
CREATE TABLE returns(return_id INTEGER PRIMARY KEY, item_id INTEGER, qty_returned INTEGER, refund_amount INTEGER);
INSERT INTO orders VALUES (1,10,'2025-01-05',50),(2,11,'2025-01-06',0),(3,12,'2025-01-07',40),(4,10,'2025-01-08',30),(5,13,'2025-01-09',0);
INSERT INTO order_items VALUES (1,1,'P1',2,100),(2,1,'P2',1,200),(3,2,'P1',1,100),(4,3,'P3',3,50),(5,3,'P2',1,200),(6,4,'P1',1,100),(7,5,'P4',4,25);
INSERT INTO returns VALUES (1,1,1,100),(2,1,1,100),(3,4,1,50),(4,6,1,100);
```

**SQL answer:** `naive` (the broken three-table join), `sql` (pre-aggregated: CTE `item_tot` per order, CTE `ret_tot` per order through `order_items`, then two `LEFT JOIN`s from `orders` with `COALESCE`) and `share` (an `EXISTS` per order) are in the Code block.

**pandas answer:** the Code block computes the line value per item, `groupby('order_id').sum()` for items, merges `returns` to `order_items` to find each return's order, `groupby('order_id').sum()` for refunds, and left-merges both onto the orders frame with `fillna(0)`.

**Example:** by hand.
- Order 1: item 1 is 2 x 100 = 200, item 2 is 1 x 200 = 200, so items = 400. Item 1 has two partial returns of 100 each, so refunds = 200 and net = 200.
- Order 2: 1 x 100 = 100, no return, net 100.
- Order 3: 3 x 50 + 1 x 200 = 350, one refund of 50, net 300.
- Order 4: 100 with a full refund of 100, net 0. Order 5: 4 x 25 = 100, net 100.
- Total net = 200 + 100 + 300 + 0 + 100 = 700. Orders with a return: 1, 3, 4, so 3 of 5 = 0.6.
- The naive join has two rows for item 1 (one per return), so item 1's 200 appears twice: order 1 shows items = 600 and net 400, and the total net is 900 instead of 700, an overstatement of exactly 200.

**Code:** run with `python3 -I`.
```python
# Q12: net revenue per order after partial returns, without join fan-out
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, shipping_fee INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id TEXT, qty INTEGER, unit_price INTEGER);
CREATE TABLE returns(return_id INTEGER PRIMARY KEY, item_id INTEGER, qty_returned INTEGER, refund_amount INTEGER);
INSERT INTO orders VALUES (1,10,'2025-01-05',50),(2,11,'2025-01-06',0),(3,12,'2025-01-07',40),(4,10,'2025-01-08',30),(5,13,'2025-01-09',0);
INSERT INTO order_items VALUES (1,1,'P1',2,100),(2,1,'P2',1,200),(3,2,'P1',1,100),(4,3,'P3',3,50),(5,3,'P2',1,200),(6,4,'P1',1,100),(7,5,'P4',4,25);
INSERT INTO returns VALUES (1,1,1,100),(2,1,1,100),(3,4,1,50),(4,6,1,100);
""")

naive = """
SELECT o.order_id, SUM(i.qty * i.unit_price) AS items_total, SUM(COALESCE(r.refund_amount, 0)) AS refunds,
       SUM(i.qty * i.unit_price) - SUM(COALESCE(r.refund_amount, 0)) AS net
FROM orders o JOIN order_items i ON i.order_id = o.order_id
LEFT JOIN returns r ON r.item_id = i.item_id
GROUP BY o.order_id ORDER BY o.order_id
"""
sql = """
WITH item_tot AS (
  SELECT order_id, SUM(qty * unit_price) AS items_total FROM order_items GROUP BY order_id),
ret_tot AS (
  SELECT i.order_id, SUM(r.refund_amount) AS refunds, COUNT(*) AS return_rows
  FROM returns r JOIN order_items i ON i.item_id = r.item_id GROUP BY i.order_id)
SELECT o.order_id, COALESCE(t.items_total, 0) AS items_total, COALESCE(r.refunds, 0) AS refunds,
       COALESCE(t.items_total, 0) - COALESCE(r.refunds, 0) AS net
FROM orders o LEFT JOIN item_tot t ON t.order_id = o.order_id
LEFT JOIN ret_tot r ON r.order_id = o.order_id
ORDER BY o.order_id
"""
share = """
SELECT COUNT(*) AS orders,
       SUM(EXISTS (SELECT 1 FROM returns r JOIN order_items i ON i.item_id = r.item_id WHERE i.order_id = o.order_id)) AS orders_with_return,
       ROUND(1.0 * SUM(EXISTS (SELECT 1 FROM returns r JOIN order_items i ON i.item_id = r.item_id WHERE i.order_id = o.order_id)) / COUNT(*), 4) AS return_share
FROM orders o
"""
n = pd.read_sql(naive, con); a = pd.read_sql(sql, con); s = pd.read_sql(share, con)
print("naive three-table join"); print(n.to_string(index=False), "\nnaive total net:", n.net.sum())
print("\npre-aggregated SQL"); print(a.to_string(index=False), "\ntotal net:", a.net.sum())
print("\nshare of orders with any return (SQL)"); print(s.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con)
items = pd.read_sql("SELECT * FROM order_items", con)
rets = pd.read_sql("SELECT * FROM returns", con)
items["line"] = items.qty * items.unit_price
it = items.groupby("order_id")["line"].sum().rename("items_total")
rt = rets.merge(items[["item_id", "order_id"]], on="item_id").groupby("order_id").agg(refunds=("refund_amount", "sum"), return_rows=("return_id", "size"))
p = orders[["order_id"]].merge(it, on="order_id", how="left").merge(rt[["refunds"]], on="order_id", how="left")
p[["items_total", "refunds"]] = p[["items_total", "refunds"]].fillna(0).astype("int64")
p["net"] = p.items_total - p.refunds
pshare = pd.DataFrame({"orders": [len(orders)], "orders_with_return": [int(orders.order_id.isin(rt.index).sum())]})
pshare["return_share"] = (pshare.orders_with_return / pshare.orders).round(4)
print("\npandas"); print(p.to_string(index=False)); print(pshare.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
pd.testing.assert_frame_equal(s, pshare, check_dtype=False)
print("\nasserts passed: per-order table (ordered by order_id) and share row equal")
```

**Output (my run):**
```text
naive three-table join
 order_id  items_total  refunds  net
        1          600      200  400
        2          100        0  100
        3          350       50  300
        4          100      100    0
        5          100        0  100 
naive total net: 900

pre-aggregated SQL
 order_id  items_total  refunds  net
        1          400      200  200
        2          100        0  100
        3          350       50  300
        4          100      100    0
        5          100        0  100 
total net: 700

share of orders with any return (SQL)
 orders  orders_with_return  return_share
      5                   3           0.6

pandas
 order_id  items_total  refunds  net
        1          400      200  200
        2          100        0  100
        3          350       50  300
        4          100      100    0
        5          100        0  100
 orders  orders_with_return  return_share
      5                   3           0.6

asserts passed: per-order table (ordered by order_id) and share row equal
```

**Edge cases:**
- **Two returns on one item:** the case that breaks the naive join. The refund sum is right in the naive join (each refund appears once); the item total is what multiplies. A bug that hides because one of the two sums is correct.
- **Orders without items or returns:** `LEFT JOIN` plus `COALESCE(...,0)` keeps them. Without the `LEFT JOIN`, order 2 would vanish from the refunds side.
- **Refund larger than the item value, or a refund row with 0 amount:** a return row with a 0 refund still counts as "an order with a return" here (existence of a row). If your definition is "refund greater than 0", filter first.
- **NULL refund_amount:** `SUM` skips NULLs; if every refund is NULL the sum is NULL, hence the `COALESCE`.
- **Shipping:** excluded on purpose; if it were included and refunded it is a business rule to confirm.

**Then explain:**
- **Why fan-out happens:** joining order to items gives one row per item, and joining returns then gives one row per (item, return). Anything that lives at the item or order level is repeated per return row.
- **Fix pattern:** aggregate child tables to the grain you report (order), then join; or sum in a subquery. A `DISTINCT` on line items would be wrong, because two different items can have equal values.
- **The check:** the one-line sanity test is that the sum of item totals (1050 here) does not change when you join the returns table in; the naive join reports 1250.
- **Dialects (not executed here):** the same query runs on PostgreSQL, MySQL, BigQuery and Snowflake; `EXISTS` returns a boolean in those engines, so `SUM(EXISTS(...))` is a SQLite and MySQL habit; use `SUM(CASE WHEN EXISTS (...) THEN 1 ELSE 0 END)` or a join to the pre-aggregated `ret_tot` to be portable.
- **Scoring note (Set E1, Q4 of 5, 25 pts):** about 10 points for the correct per-order net and the 0.6 share, 5 for the fan-out explanation shown on the seed (the 900 versus 700 contrast), 5 for pandas asserted equal, 2.5 for stating that shipping is excluded and how a return is defined, 2.5 for a reconciliation check (1050 items, 350 refunds). Quoting the naive total but not saying why it is wrong gets partial credit only.

**Follow-ups:**
- *What if refunds are recorded per order, not per item?* Then join `returns` to `orders` directly; the same rule holds: aggregate it to one row per order before joining.
- *How would you get net revenue per product?* Aggregate returns per item, join to items, then group by product. Orders are no longer the grain.
- *Why not `COUNT(DISTINCT order_id)` and be done?* That fixes counts but not sums; sums double-count the repeated line.

**Common mistakes:**
- Summing item values after joining returns.
- `INNER JOIN` to returns, which drops every order without a return.
- Dividing the number of return rows (4 here) by orders instead of orders with a return (3 of 5).
- Letting a NULL refund turn net revenue NULL.

### Q13 ⭐⭐⭐ 🔴 [Set E2, Q5 of 5, 12 min, 25 pts] Stock never below zero. inventory_moves(move_id, sku, move_date, qty_change) with receipts positive, sales negative, several moves per day per sku. For each sku return the first date the running stock fell below zero, or NULL if it never did, and the lowest running stock (Part 5 Q22). Resolve same-day ordering by move_id and state the assumption. Seed 3 skus. SQL (running SUM, then MIN over a filter) and pandas (cumsum per group), assert equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Take a running sum of `qty_change` per sku ordered by `(move_date, move_id)`, then per sku return the earliest date among rows where the running total is below zero (NULL if none) and the minimum running total.

**Schema and sample data:** (assumption: moves on the same day are applied in `move_id` order, so a sale logged before a receipt on the same day is a real dip; the end-of-day view is a different question, shown for contrast. "Below zero" means strictly less than 0, so a stock of exactly 0 is fine.)
```sql
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_change INTEGER);
INSERT INTO inventory_moves VALUES
 (1,'A','2025-01-01',10),(2,'A','2025-01-02',-4),(3,'A','2025-01-02',-8),(4,'A','2025-01-03',20),
 (5,'B','2025-01-01',5),(6,'B','2025-01-02',-7),(7,'B','2025-01-02',10),
 (8,'C','2025-01-01',3),(9,'C','2025-01-02',-3);
```

**SQL answer:** `sql` in the Code block: a CTE `r` with `SUM(qty_change) OVER (PARTITION BY sku ORDER BY move_date, move_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`, then `MIN(CASE WHEN stock < 0 THEN move_date END)` and `MIN(stock)` grouped by sku. `eod` is the end-of-day variant.

**pandas answer:** sort by `sku, move_date, move_id`, `groupby('sku')['qty_change'].cumsum()`, then the minimum `move_date` among rows with `stock < 0` and the minimum `stock`, put side by side with `concat` (so skus that never went negative still get a row, with NaN).

**Example:** by hand.
- A: +10, -4, -8, +20 gives running 10, 6, -2, 18. The -8 on 2025-01-02 is the first move that takes it below zero, so the first negative date is 2025-01-02 and the lowest is -2.
- B: +5 on 01-01, then -7 (move 6) and +10 (move 7) both on 01-02. In move_id order the running totals are 5, -2, 8, so the stock dips below zero on 01-02 with lowest -2. By end of day the balance on 01-02 is 8, so the end-of-day variant says NULL and lowest 5.
- C: +3 then -3 gives 3, 0: it hits zero but never below, so NULL and lowest 0.

**Code:** run with `python3 -I`.
```python
# Q13: first date running stock fell below zero, and lowest running stock, per sku
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_change INTEGER);
INSERT INTO inventory_moves VALUES
 (1,'A','2025-01-01',10),(2,'A','2025-01-02',-4),(3,'A','2025-01-02',-8),(4,'A','2025-01-03',20),
 (5,'B','2025-01-01',5),(6,'B','2025-01-02',-7),(7,'B','2025-01-02',10),
 (8,'C','2025-01-01',3),(9,'C','2025-01-02',-3);
""")
sql = """
WITH r AS (
  SELECT sku, move_date,
         SUM(qty_change) OVER (PARTITION BY sku ORDER BY move_date, move_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves)
SELECT sku, MIN(CASE WHEN stock < 0 THEN move_date END) AS first_negative_date, MIN(stock) AS lowest_stock
FROM r GROUP BY sku ORDER BY sku
"""
eod = """
WITH d AS (SELECT sku, move_date, SUM(qty_change) AS day_qty FROM inventory_moves GROUP BY sku, move_date),
r AS (SELECT sku, move_date, SUM(day_qty) OVER (PARTITION BY sku ORDER BY move_date ROWS UNBOUNDED PRECEDING) AS stock FROM d)
SELECT sku, MIN(CASE WHEN stock < 0 THEN move_date END) AS first_negative_date, MIN(stock) AS lowest_stock
FROM r GROUP BY sku ORDER BY sku
"""
a = pd.read_sql(sql, con)
print("SQL (running stock per move, ties by move_id)"); print(a.to_string(index=False))
print("\nSQL end-of-day variant (not the answer)"); print(pd.read_sql(eod, con).to_string(index=False))

m = pd.read_sql("SELECT * FROM inventory_moves", con).sort_values(["sku", "move_date", "move_id"])
m["stock"] = m.groupby("sku")["qty_change"].cumsum()
first_neg = m[m.stock < 0].groupby("sku")["move_date"].min().rename("first_negative_date")
low = m.groupby("sku")["stock"].min().rename("lowest_stock")
p = pd.concat([first_neg, low], axis=1).reset_index().sort_values("sku").reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by sku (NULL and NaN normalised to None before comparing)")
```

**Output (my run):**
```text
SQL (running stock per move, ties by move_id)
sku first_negative_date  lowest_stock
  A          2025-01-02            -2
  B          2025-01-02            -2
  C                 NaN             0

SQL end-of-day variant (not the answer)
sku first_negative_date  lowest_stock
  A          2025-01-02            -2
  B                 NaN             5
  C                 NaN             0

pandas
sku first_negative_date  lowest_stock
  A          2025-01-02            -2
  B          2025-01-02            -2
  C                 NaN             0

assert passed: equal, rows ordered by sku (NULL and NaN normalised to None before comparing)
```

**Edge cases:**
- **Same-day ordering:** the result for B depends on it. If the receipt (move 7) were logged first, B would never go negative. This is a business assumption, so state it and, if the timestamps exist, use them rather than `move_id`.
- **Exactly zero (C):** not below zero; the lowest running stock is 0.
- **Never negative:** the `CASE` returns NULL for every row, `MIN` of all-NULL is NULL, and the sku is still returned. In pandas the filtered frame has no rows for C, so `concat` creates NaN (the Code block compares after turning NaN and NULL into None).
- **Frame choice:** the frame is explicit `ROWS`; the default frame with an `ORDER BY` is `RANGE` and treats equal sort keys as peers (here the key is two columns and unique, but the habit is the safer one; see Part 5 Q6).
- **Dates as text:** `MIN` on ISO `YYYY-MM-DD` text sorts correctly; other formats would not.
- **Opening stock:** if there is an opening balance not in the moves table, add it as a first move or start the running sum from it.

**Then explain:**
- **First negative date, not first negative move:** the filter plus `MIN(move_date)` gives the date; to also return the move, use `ROW_NUMBER` over the negative rows.
- **Why not `HAVING stock < 0`:** window results cannot be filtered in the same `SELECT`'s `WHERE`; that is why the running sum is a CTE and the filter sits in a `CASE`.
- **Dialects (not executed here):** the SQL is standard and runs unchanged on PostgreSQL, MySQL 8, BigQuery and Snowflake; SQL Server needs the window with `ROWS` as written.
- **Scoring note (Set E2, Q5 of 5, 25 pts):** about 10 points for the right first dates and lows on the seed (A: 01-02 and -2, B: 01-02 and -2, C: NULL and 0), 5 for a correct treatment of the seeded edge cases (the same-day tie and the exact zero), 5 for pandas asserted equal, 2.5 for stating the same-day assumption, 2.5 for a one-line check (the final running stock equals the plain `SUM`). Dropping sku C from the result, or returning 0 or an empty string instead of NULL, loses the edge-case points.

**Follow-ups:**
- *How long was it negative?* Find the first date back at or above zero with a second window; use islands (Part 7) on the negative flag.
- *What if you only want end-of-day balances?* Aggregate to one row per sku and day first (`eod` in the Code block) and then run the cumulative sum; the answer for B changes.
- *Which index helps?* `(sku, move_date, move_id)` lets the window read in order without a sort (Part 11); not tested here.

**Common mistakes:**
- Leaving out `move_id` in the order, so same-day rows run in an arbitrary order.
- Using `<= 0` for "below zero".
- Filtering the running total in `WHERE` and dropping skus that never went negative.
- Comparing a date-ordered running sum with a plain cumsum on unsorted data in pandas.

### Q14 ⭐⭐⭐ 🔴 [Set E2, Q4 of 5, 15 min, 25 pts] Seller scorecard in one query (Part 8 Q41 style). sellers(seller_id, name, tier), orders(order_id, seller_id, placed_at, delivered_at, promised_by, status), reviews(order_id, rating). For each seller return orders, cancel rate, late-delivery rate among delivered orders (delivered_at > promised_by), average rating (only rated orders), and rank by late rate within seller tier. Seed 4 sellers with a seller with zero delivered orders (rate NULL, not 0) and an order with two reviews rows. SQL with CTEs and pandas, asserts equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Build three small per-seller aggregates (order counts, per-order average rating, then rates with `NULLIF` on the denominators), left-join them from `sellers` so no seller disappears, and rank by late rate within tier with a `RANK()` that sorts NULLs last.

**Schema and sample data:** (assumptions said out loud: cancel rate = cancelled orders / all orders; late rate = orders with `delivered_at > promised_by` / delivered orders, so delivering exactly on the promised date is on time; an order with two review rows counts once, with the average of its ratings; rank 1 = highest late rate, i.e. worst, and a seller with no delivered orders gets no rank.)
```sql
CREATE TABLE sellers(seller_id INTEGER PRIMARY KEY, name TEXT, tier TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, seller_id INTEGER, placed_at TEXT, delivered_at TEXT, promised_by TEXT, status TEXT);
CREATE TABLE reviews(order_id INTEGER, rating INTEGER);
INSERT INTO sellers VALUES (1,'Alpha','GOLD'),(2,'Beta','GOLD'),(3,'Gamma','SILVER'),(4,'Delta','SILVER');
INSERT INTO orders VALUES
 (1,1,'2025-01-01','2025-01-04','2025-01-05','DELIVERED'),
 (2,1,'2025-01-02','2025-01-07','2025-01-05','DELIVERED'),
 (3,1,'2025-01-03',NULL,'2025-01-08','CANCELLED'),
 (4,1,'2025-01-04','2025-01-10','2025-01-10','DELIVERED'),
 (5,2,'2025-01-01','2025-01-09','2025-01-05','DELIVERED'),
 (6,2,'2025-01-02','2025-01-08','2025-01-06','DELIVERED'),
 (7,2,'2025-01-03','2025-01-05','2025-01-06','DELIVERED'),
 (8,3,'2025-01-01','2025-01-03','2025-01-04','DELIVERED'),
 (9,3,'2025-01-02',NULL,'2025-01-06','CANCELLED'),
 (10,4,'2025-01-01',NULL,'2025-01-05','CANCELLED'),
 (11,4,'2025-01-02',NULL,'2025-01-06','SHIPPED');
INSERT INTO reviews VALUES (1,5),(2,3),(4,4),(5,2),(6,4),(6,2),(8,5);
```

**SQL answer:** `sql` in the Code block. CTE `o` has the order counts per seller with conditional sums (`SUM(status = 'CANCELLED')` and so on), CTE `rv` averages ratings per order first and then per seller, CTE `card` left-joins both to `sellers` and computes the rates with `NULLIF`, and the final `SELECT` adds `RANK() OVER (PARTITION BY tier ORDER BY late_rate DESC NULLS LAST)`.

**pandas answer:** boolean columns `is_cancel`, `is_deliv`, `is_late` on `orders`, a `groupby('seller_id').agg(...)`, a per-order mean of `reviews` then a per-seller mean, left merges onto `sellers`, rates with `.where(denominator > 0)` so a zero denominator becomes NaN, and `groupby('tier')['late_rate'].rank(method='min', ascending=False, na_option='keep')`.

**Example:** by hand.
- Alpha (GOLD): 4 orders, 1 cancelled (0.25). Delivered: orders 1, 2, 4. Late: order 2 only (delivered 01-07, promised 01-05); order 4 delivered on the promised day is on time. Late rate 1/3 = 0.3333. Ratings 5, 3, 4 give 4.0.
- Beta (GOLD): 3 orders, none cancelled, all delivered; orders 5 and 6 are late: 2/3 = 0.6667. Order 6 has two reviews (4 and 2) so it counts as 3; order 5 has 2; order 7 has no review. Average (2 + 3) / 2 = 2.5. Averaging the three review rows instead gives (2 + 4 + 2) / 3 = 2.67.
- Gamma (SILVER): 2 orders, 1 cancelled (0.5); the one delivered order is on time, late rate 0.0 (a real zero); rating 5.0.
- Delta (SILVER): 2 orders (one cancelled, one shipped), cancel rate 0.5, zero delivered so late rate is NULL, no ratings so NULL average.
- Ranks within GOLD: Beta 1, Alpha 2. Within SILVER: Gamma 1, Delta none (NULL).

**Code:** run with `python3 -I`.
```python
# Q14: seller scorecard: cancel rate, late rate among delivered, average rating, rank by late rate within tier
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sellers(seller_id INTEGER PRIMARY KEY, name TEXT, tier TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, seller_id INTEGER, placed_at TEXT, delivered_at TEXT, promised_by TEXT, status TEXT);
CREATE TABLE reviews(order_id INTEGER, rating INTEGER);
INSERT INTO sellers VALUES (1,'Alpha','GOLD'),(2,'Beta','GOLD'),(3,'Gamma','SILVER'),(4,'Delta','SILVER');
INSERT INTO orders VALUES
 (1,1,'2025-01-01','2025-01-04','2025-01-05','DELIVERED'),
 (2,1,'2025-01-02','2025-01-07','2025-01-05','DELIVERED'),
 (3,1,'2025-01-03',NULL,'2025-01-08','CANCELLED'),
 (4,1,'2025-01-04','2025-01-10','2025-01-10','DELIVERED'),
 (5,2,'2025-01-01','2025-01-09','2025-01-05','DELIVERED'),
 (6,2,'2025-01-02','2025-01-08','2025-01-06','DELIVERED'),
 (7,2,'2025-01-03','2025-01-05','2025-01-06','DELIVERED'),
 (8,3,'2025-01-01','2025-01-03','2025-01-04','DELIVERED'),
 (9,3,'2025-01-02',NULL,'2025-01-06','CANCELLED'),
 (10,4,'2025-01-01',NULL,'2025-01-05','CANCELLED'),
 (11,4,'2025-01-02',NULL,'2025-01-06','SHIPPED');
INSERT INTO reviews VALUES (1,5),(2,3),(4,4),(5,2),(6,4),(6,2),(8,5);
""")
sql = """
WITH o AS (
  SELECT seller_id,
         COUNT(*) AS orders,
         SUM(status = 'CANCELLED') AS cancelled,
         SUM(status = 'DELIVERED' AND delivered_at IS NOT NULL) AS delivered,
         SUM(status = 'DELIVERED' AND delivered_at > promised_by) AS late
  FROM orders GROUP BY seller_id),
rv AS (  -- one rating per order first (an order can have two review rows)
  SELECT o.seller_id, AVG(x.avg_rating) AS avg_rating
  FROM (SELECT order_id, AVG(rating) AS avg_rating FROM reviews GROUP BY order_id) x
  JOIN orders o ON o.order_id = x.order_id GROUP BY o.seller_id),
card AS (
  SELECT s.seller_id, s.name, s.tier, COALESCE(o.orders, 0) AS orders,
         ROUND(1.0 * o.cancelled / NULLIF(o.orders, 0), 4) AS cancel_rate,
         ROUND(1.0 * o.late / NULLIF(o.delivered, 0), 4) AS late_rate,
         ROUND(rv.avg_rating, 2) AS avg_rating
  FROM sellers s LEFT JOIN o ON o.seller_id = s.seller_id LEFT JOIN rv ON rv.seller_id = s.seller_id)
SELECT seller_id, name, tier, orders, cancel_rate, late_rate, avg_rating,
       CASE WHEN late_rate IS NULL THEN NULL
            ELSE RANK() OVER (PARTITION BY tier ORDER BY late_rate DESC NULLS LAST) END AS late_rank
FROM card ORDER BY tier, late_rank NULLS LAST, seller_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

# what averaging over review ROWS (instead of per order) would give for Beta
print("\nBeta average over review rows:", con.execute(
    "SELECT ROUND(AVG(rating),2) FROM reviews r JOIN orders o ON o.order_id=r.order_id WHERE o.seller_id=2").fetchone()[0],
    "vs per order:", a.loc[a.name == "Beta", "avg_rating"].iloc[0])

sellers = pd.read_sql("SELECT * FROM sellers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
rev = pd.read_sql("SELECT * FROM reviews", con)
orders["is_cancel"] = orders.status == "CANCELLED"
orders["is_deliv"] = (orders.status == "DELIVERED") & orders.delivered_at.notna()
orders["is_late"] = (orders.status == "DELIVERED") & (orders.delivered_at > orders.promised_by)
g = orders.groupby("seller_id").agg(orders=("order_id", "size"), cancelled=("is_cancel", "sum"),
                                    delivered=("is_deliv", "sum"), late=("is_late", "sum")).reset_index()
per_order = rev.groupby("order_id")["rating"].mean().rename("r").reset_index().merge(orders[["order_id", "seller_id"]], on="order_id")
rv = per_order.groupby("seller_id")["r"].mean().rename("avg_rating").reset_index()
p = sellers.merge(g, on="seller_id", how="left").merge(rv, on="seller_id", how="left")
p["orders"] = p.orders.fillna(0).astype("int64")
p["cancel_rate"] = (p.cancelled / p.orders.where(p.orders > 0)).round(4)
p["late_rate"] = (p.late / p.delivered.where(p.delivered > 0)).round(4)
p["avg_rating"] = p.avg_rating.round(2)
p["late_rank"] = p.groupby("tier")["late_rate"].rank(method="min", ascending=False, na_option="keep")
p = p[["seller_id", "name", "tier", "orders", "cancel_rate", "late_rate", "avg_rating", "late_rank"]]
p = p.sort_values(["tier", "late_rank", "seller_id"], na_position="last").reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by tier, late_rank (NULL last), seller_id")
```

**Output (my run):**
```text
SQL
 seller_id  name   tier  orders  cancel_rate  late_rate  avg_rating  late_rank
         2  Beta   GOLD       3         0.00     0.6667         2.5        1.0
         1 Alpha   GOLD       4         0.25     0.3333         4.0        2.0
         3 Gamma SILVER       2         0.50     0.0000         5.0        1.0
         4 Delta SILVER       2         0.50        NaN         NaN        NaN

Beta average over review rows: 2.67 vs per order: 2.5

pandas
 seller_id  name   tier  orders  cancel_rate  late_rate  avg_rating  late_rank
         2  Beta   GOLD       3         0.00     0.6667         2.5        1.0
         1 Alpha   GOLD       4         0.25     0.3333         4.0        2.0
         3 Gamma SILVER       2         0.50     0.0000         5.0        1.0
         4 Delta SILVER       2         0.50        NaN         NaN        NaN

assert passed: equal, rows ordered by tier, late_rank (NULL last), seller_id
```

**Edge cases:**
- **Zero delivered (Delta):** late rate is NULL, not 0. A zero would rank Delta as a perfect seller. `NULLIF(delivered, 0)` makes the division NULL; pandas gets NaN from `.where(denominator > 0)`.
- **Two reviews on one order (order 6):** averaging rows weights that order double (2.67 versus 2.5). Collapse to one value per order first.
- **Unrated orders:** `AVG` skips them; do not turn missing ratings into 0.
- **Delivery exactly on the promise date:** on time (`>` not `>=`).
- **Cancelled order with a `delivered_at`:** not in the data; the code also requires `status = 'DELIVERED'` so a stray timestamp on a cancelled row cannot count as late.
- **NULL ordering in rank:** SQLite sorts NULL first in ascending order and last in descending; PostgreSQL does the opposite for DESC, hence the explicit `NULLS LAST`, which SQLite 3.30 and later accepts. Delta's rank is forced to NULL by the `CASE`.
- **Ties in rate:** `RANK` gives equal rates the same rank (pandas `method='min'` matches).
- **Sorting:** the final `ORDER BY` also uses `NULLS LAST` so the NULL-rank seller comes last in its tier; the pandas sort uses `na_position='last'`.

**Then explain:**
- **One query, several denominators:** orders, delivered orders and rated orders are three different bases; naming each denominator is the point of this question.
- **Why CTEs:** each CTE keeps one grain (order counts per seller, ratings per order then seller) so the joins do not fan out.
- **Dialects (not executed here):** `NULLS LAST` is in PostgreSQL and Oracle (from memory); MySQL 8 does not accept the keyword (use `ORDER BY late_rate IS NULL, late_rate DESC`). Boolean sums such as `SUM(status = 'CANCELLED')` work in SQLite and MySQL; PostgreSQL needs `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` or `COUNT(*) FILTER (WHERE ...)`.
- **Scoring note (Set E2, Q4 of 5, 25 pts):** about 10 points for the right scorecard on the seed, 5 for handling the seeded edge cases (Delta NULL not 0, order 6 counted once), 5 for pandas asserted equal, 2.5 for stating the denominators and the rank direction, 2.5 for a check (orders sum to 11, delivered orders 7, rated orders 6). A zero instead of NULL for Delta, or a late rate over all orders, loses most of the edge-case points.

**Follow-ups:**
- *Only the best seller per tier?* Filter `late_rank = 1` in an outer query; remember it returns all sellers tied for 1.
- *Late rate over the last 90 days?* Add the date condition to the conditional sums, not to a `WHERE` that would also remove sellers.
- *How would you make a single score?* Normalise each metric first; a weighted sum of rates with different denominators can mislead, so say what weights you chose.

**Common mistakes:**
- Joining `reviews` straight to `orders` and counting order 6 twice.
- Using total orders as the late-rate denominator.
- Showing 0 for a seller with no delivered orders.
- Putting the status filter in `WHERE`, which drops sellers with no matching orders.
- Ranking without saying which end is rank 1.

### Q15 ⭐⭐⭐ 🔴 [Set F1, Q4 of 5, 10 min, 25 pts] Seven-day rolling active users (Meta-style growth metric). events(user_id, event_date) over 14 days with several rows per user per day. For every day from day 7 to day 14 return the number of distinct users active in the trailing 7 days including that day, using a date spine so days with no events still appear (Part 8 Q33, Part 5 Q45). Solve in SQL (range join to the spine) and pandas, and say why a plain 7-row window on the daily distinct count is wrong.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Make a date spine for days 7 to 14, join each spine day to the events from the previous six days and itself (`BETWEEN d - 6 days AND d`), and count distinct users; summing daily distinct counts over a 7-row window is wrong because one user active on three days is counted three times.

**Schema and sample data:** (assumption: "trailing 7 days including that day" means the day itself and the six days before it; the data runs 2025-03-01 to 2025-03-14, with no events at all on 03-04, 03-07 and 03-11. The seed has 6 users and several rows per user per day.)
```sql
CREATE TABLE events(user_id INTEGER, event_date TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01'),(1,'2025-03-01'),(1,'2025-03-02'),(1,'2025-03-08'),(1,'2025-03-09'),
 (2,'2025-03-01'),(2,'2025-03-03'),
 (3,'2025-03-02'),(3,'2025-03-02'),(3,'2025-03-12'),
 (4,'2025-03-05'),(4,'2025-03-06'),(4,'2025-03-06'),(4,'2025-03-13'),
 (5,'2025-03-09'),(5,'2025-03-14'),
 (6,'2025-03-10');
```

**SQL answer:** `sql` in the Code block: a recursive CTE `spine(d)` from 2025-03-07 to 2025-03-14, a `LEFT JOIN` to `events` on `event_date BETWEEN date(s.d, '-6 days') AND s.d`, `COUNT(DISTINCT e.user_id)` grouped by `s.d`. `wrong` is the 7-row-window version, shown for contrast.

**pandas answer:** the Code block builds the spine with `pd.date_range`, does a `cross` merge with the events, keeps rows with `day - 6 days <= event_date <= day`, then `groupby('day')['user_id'].nunique()`, reindexed to the spine with `fill_value=0` so a day with an empty window would still show 0.

**Example:** by hand, the window for 03-07 is 03-01 to 03-07. Users with an event in it: 1 (03-01, 03-02), 2 (03-01, 03-03), 3 (03-02), 4 (03-05, 03-06). Users 5 and 6 are later. That is 4. The window for 03-12 is 03-06 to 03-12: user 4 (03-06), user 1 (03-08, 03-09), user 5 (03-09), user 6 (03-10), user 3 (03-12) gives 5. User 2's last event is on 03-03, so they drop out from 03-10 onward.

**Code:** run with `python3 -I`.
```python
# Q15: trailing 7-day distinct active users with a date spine
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_date TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01'),(1,'2025-03-01'),(1,'2025-03-02'),(1,'2025-03-08'),(1,'2025-03-09'),
 (2,'2025-03-01'),(2,'2025-03-03'),
 (3,'2025-03-02'),(3,'2025-03-02'),(3,'2025-03-12'),
 (4,'2025-03-05'),(4,'2025-03-06'),(4,'2025-03-06'),(4,'2025-03-13'),
 (5,'2025-03-09'),(5,'2025-03-14'),
 (6,'2025-03-10');
""")
sql = """
WITH RECURSIVE spine(d) AS (
  SELECT '2025-03-07' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2025-03-14')
SELECT s.d AS day, COUNT(DISTINCT e.user_id) AS active_7d
FROM spine s LEFT JOIN events e ON e.event_date BETWEEN date(s.d, '-6 days') AND s.d
GROUP BY s.d ORDER BY s.d
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

# the plain 7-row window on daily distinct counts: sums users more than once
wrong = """
WITH RECURSIVE spine(d) AS (
  SELECT '2025-03-01' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2025-03-14'),
daily AS (SELECT s.d, COUNT(DISTINCT e.user_id) AS dau FROM spine s LEFT JOIN events e ON e.event_date = s.d GROUP BY s.d),
daily_nospine AS (SELECT event_date AS d, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY event_date)
SELECT x.d AS day, x.w_spine, y.w_nospine FROM
 (SELECT d, SUM(dau) OVER (ORDER BY d ROWS 6 PRECEDING) AS w_spine FROM daily) x
 LEFT JOIN (SELECT d, SUM(dau) OVER (ORDER BY d ROWS 6 PRECEDING) AS w_nospine FROM daily_nospine) y ON y.d = x.d
WHERE x.d >= '2025-03-07' ORDER BY x.d
"""
w = pd.read_sql(wrong, con)
print("\nwrong windows (sum of daily distinct counts; w_nospine is NULL on days that have no events, 03-07 and 03-11, because that table has no row for them)")
print(w.to_string(index=False))

ev = pd.read_sql("SELECT * FROM events", con)
ev["event_date"] = pd.to_datetime(ev.event_date)
spine = pd.DataFrame({"day": pd.date_range("2025-03-07", "2025-03-14")})
m = spine.merge(ev, how="cross")
m = m[(m.event_date >= m.day - pd.Timedelta(days=6)) & (m.event_date <= m.day)]
cnt = m.groupby("day")["user_id"].nunique().reindex(spine.day, fill_value=0)
p = cnt.rename("active_7d").reset_index()
p["day"] = p.day.dt.strftime("%Y-%m-%d")
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows in day order")
```

**Output (my run):**
```text
SQL
       day  active_7d
2025-03-07          4
2025-03-08          4
2025-03-09          4
2025-03-10          4
2025-03-11          4
2025-03-12          5
2025-03-13          5
2025-03-14          5

wrong windows (sum of daily distinct counts; w_nospine is NULL on days that have no events, 03-07 and 03-11, because that table has no row for them)
       day  w_spine  w_nospine
2025-03-07        7        NaN
2025-03-08        6        8.0
2025-03-09        6       10.0
2025-03-10        6        9.0
2025-03-11        6        NaN
2025-03-12        6        8.0
2025-03-13        6        8.0
2025-03-14        7        8.0

pandas
       day  active_7d
2025-03-07          4
2025-03-08          4
2025-03-09          4
2025-03-10          4
2025-03-11          4
2025-03-12          5
2025-03-13          5
2025-03-14          5

assert passed: equal, rows in day order
```

**Edge cases:**
- **Days with no events (03-07 and 03-11 are the ones in the answer range):** the spine keeps them. A query that groups the events by day has no row for them, so it silently skips the day. Here the window of 03-11 (03-05 to 03-11) still has 4 active users.
- **Several rows per user per day:** `COUNT(DISTINCT user_id)` handles them; `COUNT(*)` would count events.
- **Empty window:** with a `LEFT JOIN` a spine day with no events in its window shows 0, because `COUNT(DISTINCT NULL)` is 0. In pandas the `reindex(fill_value=0)` does the same job.
- **First six days:** days 1 to 6 have partial windows, so the question asks only for day 7 onward; the events from 03-01 still feed day 7.
- **Dates as text:** `date(s.d, '-6 days')` returns an ISO string that compares correctly with the stored dates.

**Then explain:**
- **Why a 7-row window is wrong:** it adds up daily distinct counts. In the output the `w_spine` column (7-row sum with a full spine) shows 6 or 7 on days where the true 7-day distinct count is 4 or 5, because user 1 is counted on each day they were active. Distinct counts cannot be added across days; you need the distinct count of the union.
- **A 7-row window without a spine is wrong in a second way:** the frame is 7 *rows*, not 7 *days*; with missing days it reaches back further (`w_nospine`, 8 to 10 here), and the days without events have no row at all (NULL in the `LEFT JOIN`).
- **Cost:** the range join compares each spine day with up to 7 days of events; fine for a metric table, but at scale people keep a daily "user activity" table (user, day) first, then join that.
- **Dialects (not executed here):** PostgreSQL would build the spine with `generate_series`, BigQuery with `GENERATE_DATE_ARRAY`, and most engines do not allow `COUNT(DISTINCT ...)` as a window function (PostgreSQL rejects it, from memory), which is why the range join is the portable answer. SQLite does not allow it either.
- **Scoring note (Set F1, Q4 of 5, 25 pts):** about 10 points for the eight right counts (4, 4, 4, 4, 4, 5, 5, 5), 5 for the spine and the days-with-no-events handling, 5 for pandas asserted equal, 2.5 for stating that the window is the day plus six earlier days, 2.5 for the "why not a 7-row window" sentence (or a check that the metric never exceeds total distinct users, 6). Giving the 7-row-window numbers earns partial credit only.

**Follow-ups:**
- *Weekly and monthly actives together (WAU, MAU)?* Same pattern with `-6 days` and `-29 days`; stickiness is DAU divided by MAU (Part 8).
- *How do you make it incremental?* Keep a table of (user, last_active_date) and count users whose last active date falls in the window; this only works for the "active in window" count, not for retention-style questions.
- *What does it cost?* A (user_id, event_date) index (Part 11) lets each window read a range.

**Common mistakes:**
- Summing daily distinct counts.
- `ROWS 6 PRECEDING` on a table with missing days.
- Counting rows instead of distinct users.
- Off-by-one: using `-7 days` (an 8-day window).
- Starting the spine at day 1 and then reporting the partial windows of days 1 to 6.

### Q16 ⭐⭐⭐ 🔴 [Set F2, Q4 of 5, 12 min, 25 pts] Longest daily streak (Google-style engagement). searches(user_id, search_ts TEXT) with several searches per day. Return per user the longest run of consecutive calendar days with at least one search, with the run start and end, ties broken by the earlier run (Part 7 Q6 and Q7, and the duplicate-days trap of Part 7 Q8). Seed 5 users including one with a one-day gap and one with 3 searches on the same day. SQL (date minus ROW_NUMBER) and pandas, asserting equal.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Reduce searches to distinct (user, day), number each user's days with `ROW_NUMBER`, subtract that number of days from the date so every consecutive run shares one constant, group by that constant to get run start, end and length, and keep the longest run per user, earliest first on ties.

**Schema and sample data:** (assumption: a day counts if it has at least one search; the calendar day is the first 10 characters of the timestamp; a tie in length keeps the earlier run.)
```sql
CREATE TABLE searches(user_id INTEGER, search_ts TEXT);
INSERT INTO searches VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-02 09:00:00'),(1,'2025-03-02 12:30:00'),(1,'2025-03-02 23:59:59'),(1,'2025-03-03 08:00:00'),(1,'2025-03-05 10:00:00'),(1,'2025-03-06 10:00:00'),
 (2,'2025-03-01 09:00:00'),(2,'2025-03-02 09:00:00'),(2,'2025-03-04 09:00:00'),(2,'2025-03-05 09:00:00'),(2,'2025-03-06 09:00:00'),
 (3,'2025-03-07 10:00:00'),
 (4,'2025-03-01 09:00:00'),(4,'2025-03-02 09:00:00'),(4,'2025-03-10 09:00:00'),(4,'2025-03-11 09:00:00'),
 (5,'2025-01-30 20:00:00'),(5,'2025-01-31 20:00:00'),(5,'2025-02-01 20:00:00');
```

**SQL answer:** `sql` in the Code block: `days` (distinct user and day), `g` (the group key `date(d, '-' || (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) - 1) || ' days')`), `runs` (MIN, MAX and COUNT per group), and `best` (`ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, run_start ASC)`, keep `rn = 1`). SQLite cannot subtract an integer from a date, so the shift is written as a `date(..., '-n days')` modifier; the idea "date minus row number" is the same. The `raw` query is the version without the distinct-days step.

**pandas answer:** the Code block drops duplicate (user, day) pairs, sorts, marks a new run where the gap to the previous day is not exactly one day (`diff().ne(pd.Timedelta(days=1))`, which is also true for the first day of each user), runs a `cumsum` per user to make the run id, aggregates start, end and size, then sorts by `days` descending and `run_start` ascending and keeps the first row per user.

**Example:** by hand.
- User 1: searches on 03-01, 03-02 (three searches that day), 03-03, then 03-05 and 03-06. Distinct days: 1, 2, 3, 5, 6. Runs: 03-01 to 03-03 (3 days) and 03-05 to 03-06 (2 days). Best: 03-01 to 03-03.
- User 2: 03-01, 03-02, then a gap on 03-03, then 03-04, 03-05, 03-06. Runs of 2 and 3; best is 03-04 to 03-06.
- User 3: one day, 03-07: run of 1.
- User 4: 03-01 and 03-02, then 03-10 and 03-11. Two runs of length 2: the earlier one wins, 03-01 to 03-02.
- User 5: 01-30, 01-31, 02-01: one run of 3 across the month end.

**Code:** run with `python3 -I`.
```python
# Q16: longest daily streak per user with start and end, tie -> earlier run
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE searches(user_id INTEGER, search_ts TEXT);
INSERT INTO searches VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-02 09:00:00'),(1,'2025-03-02 12:30:00'),(1,'2025-03-02 23:59:59'),(1,'2025-03-03 08:00:00'),(1,'2025-03-05 10:00:00'),(1,'2025-03-06 10:00:00'),
 (2,'2025-03-01 09:00:00'),(2,'2025-03-02 09:00:00'),(2,'2025-03-04 09:00:00'),(2,'2025-03-05 09:00:00'),(2,'2025-03-06 09:00:00'),
 (3,'2025-03-07 10:00:00'),
 (4,'2025-03-01 09:00:00'),(4,'2025-03-02 09:00:00'),(4,'2025-03-10 09:00:00'),(4,'2025-03-11 09:00:00'),
 (5,'2025-01-30 20:00:00'),(5,'2025-01-31 20:00:00'),(5,'2025-02-01 20:00:00');
""")
sql = """
WITH days AS (SELECT DISTINCT user_id, date(search_ts) AS d FROM searches),
g AS (SELECT user_id, d, date(d, '-' || (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) - 1) || ' days') AS grp FROM days),
runs AS (SELECT user_id, MIN(d) AS run_start, MAX(d) AS run_end, COUNT(*) AS days FROM g GROUP BY user_id, grp),
best AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, run_start ASC) AS rn FROM runs)
SELECT user_id, run_start, run_end, days FROM best WHERE rn = 1 ORDER BY user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
raw = """
WITH g AS (SELECT date(search_ts) AS d,
  date(date(search_ts), '-' || (ROW_NUMBER() OVER (ORDER BY search_ts) - 1) || ' days') AS grp
  FROM searches WHERE user_id = 1)
SELECT MIN(d) AS run_start, MAX(d) AS run_end, COUNT(*) AS n FROM g GROUP BY grp ORDER BY run_start
"""
print("\nuser 1 without the DISTINCT-days step (row numbers over raw rows): the 3 searches on 03-02 split the run")
print(pd.read_sql(raw, con).to_string(index=False))

s = pd.read_sql("SELECT * FROM searches", con)
s["d"] = pd.to_datetime(s.search_ts.str[:10])
dd = s[["user_id", "d"]].drop_duplicates().sort_values(["user_id", "d"])
dd["new_run"] = dd.groupby("user_id")["d"].diff().ne(pd.Timedelta(days=1))
dd["grp"] = dd.groupby("user_id")["new_run"].cumsum()
runs = dd.groupby(["user_id", "grp"]).agg(run_start=("d", "min"), run_end=("d", "max"), days=("d", "size")).reset_index()
best = runs.sort_values(["user_id", "days", "run_start"], ascending=[True, False, True]).drop_duplicates("user_id")
p = best[["user_id", "run_start", "run_end", "days"]].sort_values("user_id").reset_index(drop=True)
p["run_start"] = p.run_start.dt.strftime("%Y-%m-%d"); p["run_end"] = p.run_end.dt.strftime("%Y-%m-%d")
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by user_id")
```

**Output (my run):**
```text
SQL
 user_id  run_start    run_end  days
       1 2025-03-01 2025-03-03     3
       2 2025-03-04 2025-03-06     3
       3 2025-03-07 2025-03-07     1
       4 2025-03-01 2025-03-02     2
       5 2025-01-30 2025-02-01     3

user 1 without the DISTINCT-days step (row numbers over raw rows): the 3 searches on 03-02 split the run
 run_start    run_end  n
2025-03-01 2025-03-02  2
2025-03-02 2025-03-03  2
2025-03-02 2025-03-06  3

pandas
 user_id  run_start    run_end  days
       1 2025-03-01 2025-03-03     3
       2 2025-03-04 2025-03-06     3
       3 2025-03-07 2025-03-07     1
       4 2025-03-01 2025-03-02     2
       5 2025-01-30 2025-02-01     3

assert passed: equal, rows ordered by user_id
```

**Edge cases:**
- **Several searches on one day (user 1, 03-02):** without the `DISTINCT` day step the row numbers advance faster than the dates. The second printed table shows what happens to user 1: the runs come out as 03-01 to 03-02 (2 rows), 03-02 to 03-03 (2 rows) and an absurd 03-02 to 03-06 (3 rows) that bridges the real gap on 03-04. This is the duplicate-days trap of Part 7 Q8.
- **A one-day gap (user 2):** splits the run; the answer comes from the second run.
- **Tie (user 4):** broken by the earlier start through `run_start ASC`.
- **Single day (user 3):** a run of length 1 is still a run.
- **Month and year boundaries (user 5):** date arithmetic handles them; do not compare day-of-month numbers.
- **Time zones:** `search_ts` is taken as one zone. A "calendar day" in the user's zone needs the conversion before `date()`. Not run here.
- **Users with no searches:** no row; add a `LEFT JOIN` from `users` if they must appear.

**Then explain:**
- **Why the trick works:** within a run of consecutive days, the day number and the row number rise together, so their difference is constant; a gap makes the day jump while the row number goes up by one, changing the constant.
- **pandas vs SQL:** both use the same idea; pandas `cumsum` of "starts a new run" is the common alternative to subtracting a row number.
- **Dialects (not executed here):** from memory, PostgreSQL can subtract an integer from a date directly (`d - (ROW_NUMBER() OVER (...))::int`); MySQL uses `DATE_SUB(d, INTERVAL n DAY)`; the `ROW_NUMBER` tie rule is standard.
- **Scoring note (Set F2, Q4 of 5, 25 pts):** about 10 points for the five right run rows, 5 for the seeded edge cases (the same-day duplicates handled by distinct days, the tie rule, the month crossing), 5 for pandas asserted equal, 2.5 for stating "day counts if at least one search" and the tie rule, 2.5 for a check such as "the run length never exceeds the user's number of distinct days". Counting search rows instead of days is the usual way to lose most points here.

**Follow-ups:**
- *Current streak as of today?* Keep only the run whose end is the as-of date (or the day before); everything else is a broken streak.
- *All users' longest streak overall?* Take the maximum of `days` from `runs`, with ties listed.
- *Streak that allows one missed day?* Use a gap threshold of 2 days (`diff <= 2`) in pandas, or a `LAG` flag in SQL; that is an islands variation (Part 7).

**Common mistakes:**
- Using `ROW_NUMBER` over raw searches instead of distinct days.
- Comparing `search_ts` strings instead of days, so two searches on one day look like different days.
- Breaking ties arbitrarily (no second order key) so the answer changes between runs.
- Forgetting that the `DENSE_RANK` or `ROW_NUMBER` order must be by day, not by user.

### Q17 ⭐⭐ 🟡 [Set F1, Q3 of 5, 8 min, 20 pts] Top 2 posters per country with ties (Meta-style). users(user_id, country), posts(post_id, user_id, created_at). Return the users whose post count in March 2025 is within the top 2 distinct counts of their country (dense rank, ties all kept, Part 4 Q4 and Q45). Seed 8 users in 3 countries with a three-way tie and a user with zero posts (excluded). SQL and pandas, order by country, count descending, user_id.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Count each user's March posts, then `DENSE_RANK()` those counts per country in descending order and keep rank 1 and 2: dense rank means ties share a rank and no rank number is skipped, so a three-way tie for second place keeps all three.

**Schema and sample data:** (assumptions: March means `created_at >= '2025-03-01'` and `< '2025-04-01'`, a half-open range that also catches a post at 23:59:59 on 03-31 and excludes one at 00:00:00 on 04-01; users with no March post are not ranked.) The 24 post rows are generated in the Code block from per-user counts, shown here as a table; the `users` rows are literal.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE posts(post_id INTEGER PRIMARY KEY, user_id INTEGER, created_at TEXT);
INSERT INTO users VALUES (1,'IN'),(2,'IN'),(3,'IN'),(4,'IN'),(5,'IN'),(6,'US'),(7,'US'),(8,'UK');
```
| user_id | country | posts in March | other posts |
|---|---|---|---|
| 1 | IN | 5 | none |
| 2 | IN | 3 | none |
| 3 | IN | 3 | none |
| 4 | IN | 3 (the last one at 2025-03-31 23:59:59) | none |
| 5 | IN | 1 | 2 in February |
| 6 | US | 4 | none |
| 7 | US | 2 | 1 at 2025-04-01 00:00:00 |
| 8 | UK | 0 | none |

**SQL answer:** `sql` in the Code block: CTE `c` counts March posts per (country, user), CTE `r` adds `DENSE_RANK() OVER (PARTITION BY country ORDER BY posts DESC)`, and the final `SELECT` keeps `rk <= 2` ordered by country, posts descending, user_id.

**pandas answer:** filter the posts to March with two string comparisons, merge with `users`, `groupby(['country', 'user_id']).size()`, then `groupby('country')['posts'].rank(method='dense', ascending=False)` and keep `rk <= 2`.

**Example:** by hand, India has March counts 5 (user 1), 3, 3, 3 (users 2, 3, 4) and 1 (user 5). Distinct counts in descending order: 5, 3, 1. Dense ranks: 1, 2, 2, 2, 3. Rank 3 is dropped, so IN keeps users 1, 2, 3, 4. US has 4 and 2: ranks 1 and 2, both kept. UK has no March posts, so no row. Total 6 rows.

**Code:** run with `python3 -I`.
```python
# Q17: users within the top 2 DISTINCT post counts of their country, March 2025
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE posts(post_id INTEGER PRIMARY KEY, user_id INTEGER, created_at TEXT);
INSERT INTO users VALUES (1,'IN'),(2,'IN'),(3,'IN'),(4,'IN'),(5,'IN'),(6,'US'),(7,'US'),(8,'UK');
""")
rows = []
pid = 0
def add(u, n, ts):
    global pid
    for _ in range(n):
        pid += 1
        rows.append((pid, u, ts))
add(1, 5, "2025-03-10 10:00:00"); add(2, 3, "2025-03-11 10:00:00"); add(3, 3, "2025-03-12 10:00:00"); add(4, 3, "2025-03-31 23:59:59")
add(5, 1, "2025-03-05 10:00:00"); add(5, 2, "2025-02-27 10:00:00")
add(6, 4, "2025-03-02 10:00:00"); add(7, 2, "2025-03-03 10:00:00"); add(7, 1, "2025-04-01 00:00:00")
con.executemany("INSERT INTO posts VALUES (?,?,?)", rows)

sql = """
WITH c AS (
  SELECT u.country, u.user_id, COUNT(*) AS posts
  FROM users u JOIN posts p ON p.user_id = u.user_id
  WHERE p.created_at >= '2025-03-01' AND p.created_at < '2025-04-01'
  GROUP BY u.country, u.user_id),
r AS (SELECT *, DENSE_RANK() OVER (PARTITION BY country ORDER BY posts DESC) AS rk FROM c)
SELECT country, user_id, posts, rk FROM r WHERE rk <= 2 ORDER BY country, posts DESC, user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
print("\nwith ROW_NUMBER instead of DENSE_RANK the kept (country, user_id) would be:",
      [(r[0], r[1]) for r in con.execute(sql.replace("DENSE_RANK()", "ROW_NUMBER()"))])

u = pd.read_sql("SELECT * FROM users", con); po = pd.read_sql("SELECT * FROM posts", con)
po = po[(po.created_at >= "2025-03-01") & (po.created_at < "2025-04-01")]
c = u.merge(po, on="user_id").groupby(["country", "user_id"]).size().rename("posts").reset_index()
c["rk"] = c.groupby("country")["posts"].rank(method="dense", ascending=False).astype("int64")
p = c[c.rk <= 2].sort_values(["country", "posts", "user_id"], ascending=[True, False, True]).reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by country, posts desc, user_id")
```

**Output (my run):**
```text
SQL
country  user_id  posts  rk
     IN        1      5   1
     IN        2      3   2
     IN        3      3   2
     IN        4      3   2
     US        6      4   1
     US        7      2   2

with ROW_NUMBER instead of DENSE_RANK the kept (country, user_id) would be: [('IN', 1), ('IN', 2), ('US', 6), ('US', 7)]

pandas
country  user_id  posts  rk
     IN        1      5   1
     IN        2      3   2
     IN        3      3   2
     IN        4      3   2
     US        6      4   1
     US        7      2   2

assert passed: equal, rows ordered by country, posts desc, user_id
```

**Edge cases:**
- **Three-way tie for second (users 2, 3, 4):** all kept by `DENSE_RANK`. `ROW_NUMBER` would keep exactly one of them arbitrarily: the printed line starting `with ROW_NUMBER` shows `ROW_NUMBER` keeping only users 1 and 2 for IN, and silently dropping 3 and 4.
- **`RANK` instead of `DENSE_RANK`:** the ranks would be 1, 2, 2, 2 and then 5. For "top 2" the kept rows are the same here, but `RANK` and "top 2 distinct counts" differ when the tie is at rank 1: `RANK` would skip rank 2 and return only the tied leaders. That is why the prompt says dense.
- **Zero-post user (user 8):** never in the count CTE because of the inner join; UK is absent from the result. To show UK as empty, left-join from `users` and handle NULL.
- **Date boundaries:** user 5's February posts and user 7's 04-01 midnight post must not count; the half-open range handles the timestamp boundary, whereas `<= '2025-03-31'` would drop the 23:59:59 post of user 4.
- **Posts per user as the only measure:** the count is a row count; if a post could be duplicated (retries), count distinct `post_id` (not needed here, `post_id` is the key).

**Then explain:**
- **Dense rank on counts, not on users:** ranking distinct counts means "the two highest levels of activity" rather than "two people".
- **pandas:** `rank(method='dense', ascending=False)` returns floats; the Code block casts to int to compare with SQL's integer rank.
- **Dialects (not executed here):** `DENSE_RANK` is standard (PostgreSQL, MySQL 8, SQL Server, BigQuery, Snowflake); `QUALIFY DENSE_RANK() ... <= 2` on BigQuery or Snowflake saves the extra CTE (not executed).
- **Scoring note (Set F1, Q3 of 5, 20 pts):** about 8 points for the six right rows, 4 for the seeded edge cases (three-way tie kept, zero-post user excluded), 4 for pandas asserted equal, 2 for stating dense versus row rank and the March boundary, 2 for a check (every kept user has posts, counts descend within a country). Using `ROW_NUMBER` or `LIMIT 2` per country is a wrong answer here, not a style choice.

**Follow-ups:**
- *Include countries with no posters as an empty row?* Left join from distinct countries and accept NULL user.
- *Top 2 per country per month?* Add the month to the grouping and partition; the code shape is the same.
- *What if you also need the rank of ties to be broken by earliest post?* Add `MIN(created_at)` as a secondary order key and use `ROW_NUMBER`, but that changes the question to "exactly two people".

**Common mistakes:**
- `ROW_NUMBER` or `LIMIT` and losing tied users.
- Filtering the rank in the same `SELECT` (window results are not available in `WHERE`).
- `<= '2025-03-31'` on a timestamp column.
- Ranking before filtering to March.

### Q18 ⭐⭐ 🟡 [Set F1, Q2 of 5, 8 min, 20 pts] Day-1 retention by signup date (Part 6 Q12, Q13). users(user_id, signup_date) and logins(user_id, login_date). For each signup date return signups, users who logged in exactly the next calendar day, and the rate rounded to 2 decimals; a signup date with zero retained users must still show 0.00. Seed 9 users over 3 days including a user who logs in two days after only and a user with duplicate login rows. SQL and pandas.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** For each signup date count distinct signups and count distinct users who have a login dated exactly signup date plus one day, with a `LEFT JOIN` to the logins and `COUNT(DISTINCT CASE ...)` so duplicate login rows are harmless and a date with nobody retained still appears with 0.00.
 
**Schema and sample data:** (assumption: day 1 means the next calendar day only; logging in on the signup day or two days later does not count; the rate is retained users divided by all users who signed up that day, and it is rounded to 2 decimals.)
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2025-03-01'),(2,'2025-03-01'),(3,'2025-03-01'),
                         (4,'2025-03-02'),(5,'2025-03-02'),(6,'2025-03-02'),
                         (7,'2025-03-03'),(8,'2025-03-03'),(9,'2025-03-03');
INSERT INTO logins VALUES (1,'2025-03-02'),(1,'2025-03-02'),(2,'2025-03-03'),(3,'2025-03-02'),
                          (4,'2025-03-03'),(6,'2025-03-09'),
                          (7,'2025-03-05'),(9,'2025-03-03');
```

**SQL answer:** `sql` in the Code block: `FROM users u LEFT JOIN logins l ON l.user_id = u.user_id`, grouped by `signup_date`, with `COUNT(DISTINCT u.user_id)` for signups, `COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END)` for retained, and `ROUND(1.0 * retained / signups, 2)` for the rate (the printout formats it with two decimals).

**pandas answer:** compute `next_day` for each user, merge with the de-duplicated logins on `(user_id, next_day = login_date)`, mark users found, then `groupby('signup_date').agg(signups=('user_id', 'nunique'), retained=('retained', 'sum'))` and `(retained / signups).round(2)`.

**Example:** by hand.
- Signup 03-01 (users 1, 2, 3): user 1 logs in on 03-02, twice (one retained user, not two); user 2 logs in only on 03-03 (two days later, not retained); user 3 logs in on 03-02. Retained 2 of 3: 0.67.
- Signup 03-02 (users 4, 5, 6): user 4 logs in on 03-03 (retained); user 5 never logs in; user 6 logs in only on 03-09. Retained 1 of 3: 0.33.
- Signup 03-03 (users 7, 8, 9): user 7 logs in on 03-05 (two days later), user 8 never, user 9 logs in on 03-03 itself (same day). None on 03-04, so 0 of 3: 0.00.

**Code:** run with `python3 -I`.
```python
# Q18: day-1 retention by signup date, 0.00 kept
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2025-03-01'),(2,'2025-03-01'),(3,'2025-03-01'),
                         (4,'2025-03-02'),(5,'2025-03-02'),(6,'2025-03-02'),
                         (7,'2025-03-03'),(8,'2025-03-03'),(9,'2025-03-03');
INSERT INTO logins VALUES (1,'2025-03-02'),(1,'2025-03-02'),(2,'2025-03-03'),(3,'2025-03-02'),
                          (4,'2025-03-03'),(6,'2025-03-09'),
                          (7,'2025-03-05'),(9,'2025-03-03');
""")
sql = """
SELECT u.signup_date,
       COUNT(DISTINCT u.user_id) AS signups,
       COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END) AS retained,
       ROUND(1.0 * COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END)
             / COUNT(DISTINCT u.user_id), 2) AS rate
FROM users u LEFT JOIN logins l ON l.user_id = u.user_id
GROUP BY u.signup_date ORDER BY u.signup_date
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.assign(rate=a.rate.map("{:.2f}".format)).to_string(index=False))
print("\nwithout DISTINCT, COUNT(*) of the joined rows for 2025-03-01 gives:",
      con.execute("SELECT COUNT(*) FROM users u JOIN logins l ON l.user_id=u.user_id AND l.login_date=date(u.signup_date,'+1 day') WHERE u.signup_date='2025-03-01'").fetchone()[0],
      "retained (user 1 has two login rows)")

u = pd.read_sql("SELECT * FROM users", con); lg = pd.read_sql("SELECT * FROM logins", con)
u["next_day"] = (pd.to_datetime(u.signup_date) + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d")
hit = u.merge(lg.drop_duplicates(), left_on=["user_id", "next_day"], right_on=["user_id", "login_date"])
u["retained"] = u.user_id.isin(hit.user_id)
p = u.groupby("signup_date").agg(signups=("user_id", "nunique"), retained=("retained", "sum")).reset_index()
p["rate"] = (p.retained / p.signups).round(2)
print("\npandas"); print(p.assign(rate=p.rate.map("{:.2f}".format)).to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by signup_date")
```

**Output (my run):**
```text
SQL
signup_date  signups  retained rate
 2025-03-01        3         2 0.67
 2025-03-02        3         1 0.33
 2025-03-03        3         0 0.00

without DISTINCT, COUNT(*) of the joined rows for 2025-03-01 gives: 3 retained (user 1 has two login rows)

pandas
signup_date  signups  retained rate
 2025-03-01        3         2 0.67
 2025-03-02        3         1 0.33
 2025-03-03        3         0 0.00

assert passed: equal, rows ordered by signup_date
```

**Edge cases:**
- **Duplicate login rows (user 1):** `COUNT(DISTINCT ...)` and `drop_duplicates()` collapse them. A plain count of joined rows gives 3 "retained" for 03-01 in the second printed line, instead of the true 2, and a rate above the truth.
- **Zero retained (03-03):** the date still appears because the denominator side comes from `users` and the `LEFT JOIN` keeps users with no logins; `COUNT(DISTINCT CASE ...)` returns 0, not NULL.
- **Users who never log in (users 5 and 8):** kept by the `LEFT JOIN`; their `login_date` is NULL, the comparison is not true, the `CASE` gives NULL, and `COUNT` ignores it.
- **Same-day logins (user 9) and day 2 logins (users 2, 7):** not day 1 by definition.
- **Matching the rule exactly:** a `login_date` compared with `date(signup_date, '+1 day')` works because both are `YYYY-MM-DD` text; with timestamps, take `date()` of the login first.
- **Immature cohorts:** if the latest signup date has not yet had its next day in the data, its rate is understated; mark or drop it in a real report (here the data covers up to 03-09).
- **Printing 0.00:** SQLite's `ROUND` returns the number 0.0; the two-decimal text is a formatting step (done in the printout).

**Then explain:**
- **Why a LEFT JOIN from users:** an inner join to logins would drop users who never came back and inflate the rate (and drop the 0.00 row).
- **Rounding:** `ROUND(2/3, 2)` is 0.67 in both engines. Rounding of exact halves can differ (SQLite and pandas disagree on, for example, 703.125, see Part 10), so keep the raw ratio if you need to compare cohorts.
- **Dialects (not executed here):** PostgreSQL would write `u.signup_date + 1` (date plus integer) and MySQL `DATE_ADD(u.signup_date, INTERVAL 1 DAY)`; `COUNT(DISTINCT CASE ...)` works in both.
- **Scoring note (Set F1, Q2 of 5, 20 pts):** about 8 points for the three right rows (0.67, 0.33, 0.00), 4 for the seeded edge cases (duplicate logins, the zero-retention date), 4 for pandas asserted equal, 2 for stating the day-1 definition and denominator, 2 for a check (retained never exceeds signups; signups add up to 9).

**Follow-ups:**
- *Day 7 retention?* Replace `+1 day` with `+7 days` (exactly day 7), or use a range if the product defines "within 7 days"; say which.
- *Retention by cohort week?* Group by week of signup; keep the same denominators.
- *Why did the number differ from the dashboard?* Check the definition (next day versus within a day), time zones, duplicate rows and whether test users are filtered.

**Common mistakes:**
- Counting login rows rather than distinct users.
- Using `INNER JOIN` and losing the cohort with no retention.
- Using `BETWEEN signup_date AND signup_date + 1` (includes day 0).
- Dividing by users who logged in at all, not by all signups.

### Q19 ⭐⭐ 🟡 [Set F2, Q3 of 5, 8 min, 20 pts] Sessions per user (Google-style). events(user_id, event_ts) and a 30-minute inactivity timeout; a gap of exactly 30 minutes starts a new session (Part 7 Q11, Q12). Return per user the session count and average events per session. Seed 3 users with a boundary gap exactly 30:00 and one with a single event. SQL (LAG then cumulative flag) and pandas (diff, gt, cumsum). Assert equal; state the rounding of the average.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Order each user's events by time, take the gap to the previous event in whole seconds, flag a new session when there is no previous event or the gap is at least 1800 seconds, take a running sum of the flags as the session id, then count sessions and events per user.

**Schema and sample data:** (assumption: timeout rule = a gap of 30:00 or more starts a new session, so exactly 30:00 is a new session and 29:59 is not; the average is events (rows) per session, rounded to 2 decimals; duplicate timestamps count as separate events.)
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-01 09:10:00'),(1,'2025-03-01 09:40:00'),(1,'2025-03-01 09:50:00'),(1,'2025-03-01 10:30:00'),
 (2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:29:59'),(2,'2025-03-01 11:00:00'),
 (3,'2025-03-01 12:00:00');
```

**SQL answer:** `sql` in the Code block: `l` computes the gap with `strftime('%s', event_ts) - strftime('%s', LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts))` (whole seconds, so there is no floating point rounding at the boundary), `f` makes the flag, `s` runs `SUM(new_sess) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`, `per` counts events per session, and the final query counts sessions and averages.

**pandas answer:** sort by user and time, `gap = groupby('user_id')['ts'].diff()`, `new_sess = gap.isna() | (gap >= pd.Timedelta(minutes=30))`, `groupby('user_id')['new_sess'].cumsum()` for the session id, then size per (user, session) and aggregate.

**Example:** by hand.
- User 1: 09:00, 09:10 (gap 10 min, same session), 09:40 (gap exactly 30:00, new session), 09:50 (10 min, same), 10:30 (40 min, new). Sessions: {09:00, 09:10}, {09:40, 09:50}, {10:30} = 3 sessions, 5 events, 5/3 = 1.67.
- User 2: 10:00, 10:00 (gap 0, same), 10:29:59 (29:59 after 10:00, same), 11:00:00 (30:01, new). Sessions: {3 events}, {1 event} = 2 sessions, 4 events, 2.00.
- User 3: one event: 1 session, 1 event, 1.00.

**Code:** run with `python3 -I`.
```python
# Q19: sessions per user with a 30-minute timeout (a gap of exactly 30:00 starts a new session)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-01 09:10:00'),(1,'2025-03-01 09:40:00'),(1,'2025-03-01 09:50:00'),(1,'2025-03-01 10:30:00'),
 (2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:29:59'),(2,'2025-03-01 11:00:00'),
 (3,'2025-03-01 12:00:00');
""")
sql = """
WITH l AS (
  SELECT user_id, event_ts,
         strftime('%s', event_ts) - strftime('%s', LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts)) AS gap_s
  FROM events),
f AS (SELECT user_id, event_ts, CASE WHEN gap_s IS NULL OR gap_s >= 1800 THEN 1 ELSE 0 END AS new_sess FROM l),
s AS (SELECT user_id, SUM(new_sess) OVER (PARTITION BY user_id ORDER BY event_ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sess FROM f),
per AS (SELECT user_id, sess, COUNT(*) AS n FROM s GROUP BY user_id, sess)
SELECT user_id, COUNT(*) AS sessions, SUM(n) AS events, ROUND(1.0 * SUM(n) / COUNT(*), 2) AS avg_events_per_session
FROM per GROUP BY user_id ORDER BY user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

e = pd.read_sql("SELECT * FROM events", con)
e["ts"] = pd.to_datetime(e.event_ts)
e = e.sort_values(["user_id", "ts"])
gap = e.groupby("user_id")["ts"].diff()
e["new_sess"] = gap.isna() | (gap >= pd.Timedelta(minutes=30))
e["sess"] = e.groupby("user_id")["new_sess"].cumsum()
per = e.groupby(["user_id", "sess"]).size().rename("n").reset_index()
p = per.groupby("user_id").agg(sessions=("sess", "size"), events=("n", "sum")).reset_index()
p["avg_events_per_session"] = (p.events / p.sessions).round(2)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by user_id")

# boundary check: > 1800 instead of >= 1800 would merge user 1's second session into the first
print("\nif the rule were gap > 30 min (strict), user 1 would have",
      int(((gap.isna()) | (gap > pd.Timedelta(minutes=30)))[e.user_id == 1].groupby(e.user_id).sum().iloc[0]), "sessions")
```

**Output (my run):**
```text
SQL
 user_id  sessions  events  avg_events_per_session
       1         3       5                    1.67
       2         2       4                    2.00
       3         1       1                    1.00

pandas
 user_id  sessions  events  avg_events_per_session
       1         3       5                    1.67
       2         2       4                    2.00
       3         1       1                    1.00

assert passed: equal, rows ordered by user_id

if the rule were gap > 30 min (strict), user 1 would have 2 sessions
```

**Edge cases:**
- **Exactly 30:00 (user 1, 09:10 to 09:40):** counts as a new session because the test is `>= 1800`. The last line of the output shows that a strict `>` rule would give user 1 only 2 sessions. Say which rule you use; the prompt fixes it.
- **29:59 (user 2):** stays in the session.
- **Single event (user 3):** `LAG` is NULL, so the flag is 1; one session of one event.
- **Duplicate timestamps (user 2):** gap 0, same session; the `ROWS` frame (not the default `RANGE`) makes the running sum count each row once. With the default frame and `ORDER BY event_ts`, peers with the same timestamp would get the same running total, which here is harmless for the session id but would be wrong for any running count.
- **Out-of-order rows:** the window sorts them; sort first in pandas as well.
- **Events from several days:** a gap across midnight is handled the same way; sessions are not cut at midnight unless the product says so.
- **NULL timestamps:** would sort first and break the gap; filter them.

**Then explain:**
- **Why integer seconds:** `julianday` differences are floating point, so a boundary test such as `(julianday(b) - julianday(a)) * 1440 >= 30` is fragile at exactly 30:00 (I did not test whether it misfires on this data). Seconds from `strftime('%s', ...)` are integers, so the boundary is exact.
- **Average events per session:** total events divided by total sessions per user (not an average of per-day averages). Rounded half away from zero in SQLite's `ROUND` and to even in pandas, which only matters on exact halves; none occur in this data.
- **Dialects (not executed here):** PostgreSQL would compute the gap as `event_ts - LAG(event_ts) OVER (...) >= INTERVAL '30 minutes'` on timestamp columns; MySQL uses `TIMESTAMPDIFF(SECOND, prev, ts)`; BigQuery `TIMESTAMP_DIFF(ts, prev, SECOND)`.
- **Scoring note (Set F2, Q3 of 5, 20 pts):** about 8 points for the right sessions and averages on the seed, 4 for the boundary and single-event handling (30:00 is new, 29:59 is not), 4 for pandas asserted equal, 2 for stating the rule and rounding, 2 for a check (the events column sums to the table's row count, 10).

**Follow-ups:**
- *Session length and duration?* `MIN` and `MAX` of `event_ts` per session; single-event sessions have zero duration, so say how you treat them.
- *Also cap sessions at 4 hours?* Add a second flag when the time since the session start exceeds the cap; that is harder in plain SQL (it needs a recursive CTE), so mention it as a limit.
- *Why not a self join?* It is quadratic; `LAG` is one ordered pass.

**Common mistakes:**
- Using `>` instead of `>=` at the boundary.
- Float date arithmetic that misses the exact boundary.
- A default `RANGE` frame for the running flag.
- Averaging per-session counts incorrectly (average of averages).
- Forgetting the first event of each user (NULL gap).

### Q20 ⭐⭐ 🟡 [Set F2, Q2 of 5, 8 min, 20 pts] Second most searched term per category (Part 4 Q5, Q46). searches(search_id, category, term). Return the second highest distinct count of searches per category and the term(s) at that rank, showing categories with only one distinct count as NULL rather than dropping them. Seed 3 categories with a tie for the top, a tie for second and a category with a single term. SQL and pandas.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Count searches per (category, term), `DENSE_RANK()` those counts per category in descending order, and `LEFT JOIN` the list of categories to the rows with rank 2, so a category with fewer than two distinct counts still appears, with NULL.

**Schema and sample data:** (assumption: "second most searched" means the second highest distinct count, so ties for first do not use up rank 2; terms tied at that count are all returned, one row each.) The 24 search rows are generated in the Code block from the counts below.
```sql
CREATE TABLE searches(search_id INTEGER PRIMARY KEY, category TEXT, term TEXT);
```
| category | term: searches |
|---|---|
| shoes | A: 5, B: 5, C: 3, D: 3, E: 1 |
| phones | X: 4, Y: 2 |
| books | novel: 3 |

**SQL answer:** `sql` in the Code block: `c` counts per (category, term), `r` adds `DENSE_RANK() OVER (PARTITION BY category ORDER BY n DESC)`, `cats` lists the distinct categories, and `cats LEFT JOIN r ON r.category = cats.category AND r.rk = 2` keeps every category. The condition `rk = 2` sits in `ON`, not in `WHERE`.

**pandas answer:** group and count, `rank(method='dense', ascending=False)` per category, take the rank-2 rows, and `merge(..., how='left')` them onto the unique categories.

**Example:** by hand.
- shoes: counts 5, 5, 3, 3, 1. Distinct counts: 5, 3, 1. Dense ranks: A and B are 1, C and D are 2, E is 3. Second highest distinct count = 3 and the terms are C and D (two rows).
- phones: X = 4 (rank 1), Y = 2 (rank 2): one row, (phones, 2, Y).
- books: one term, one distinct count, no rank 2: (books, NULL, NULL).
- A plain `LIMIT 1 OFFSET 1` or `ROW_NUMBER() = 2` over the terms would return one arbitrary term per category (for shoes, the second of the two tied leaders, B), not C and D, and nothing sensible for books.

**Code:** run with `python3 -I`.
```python
# Q20: second highest DISTINCT search count per category and the terms at that rank, NULL if none
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE searches(search_id INTEGER PRIMARY KEY, category TEXT, term TEXT);")
rows = []
sid = 0
for cat, term, n in [("shoes", "A", 5), ("shoes", "B", 5), ("shoes", "C", 3), ("shoes", "D", 3), ("shoes", "E", 1),
                     ("phones", "X", 4), ("phones", "Y", 2), ("books", "novel", 3)]:
    for _ in range(n):
        sid += 1
        rows.append((sid, cat, term))
con.executemany("INSERT INTO searches VALUES (?,?,?)", rows)

sql = """
WITH c AS (SELECT category, term, COUNT(*) AS n FROM searches GROUP BY category, term),
r AS (SELECT *, DENSE_RANK() OVER (PARTITION BY category ORDER BY n DESC) AS rk FROM c),
cats AS (SELECT DISTINCT category FROM searches)
SELECT cats.category, r.n AS second_count, r.term
FROM cats LEFT JOIN r ON r.category = cats.category AND r.rk = 2
ORDER BY cats.category, r.term
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
print("\ninner-join version (drops books):", [r[0] for r in con.execute(sql.replace("LEFT JOIN r ON r.category = cats.category AND r.rk = 2", "JOIN r ON r.category = cats.category AND r.rk = 2"))])

s = pd.read_sql("SELECT * FROM searches", con)
c = s.groupby(["category", "term"]).size().rename("n").reset_index()
c["rk"] = c.groupby("category")["n"].rank(method="dense", ascending=False)
cats = c[["category"]].drop_duplicates()
second = c[c.rk == 2][["category", "n", "term"]].rename(columns={"n": "second_count"})
p = cats.merge(second, on="category", how="left").sort_values(["category", "term"]).reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by category, term")
```

**Output (my run):**
```text
SQL
category  second_count term
   books           NaN  NaN
  phones           2.0    Y
   shoes           3.0    C
   shoes           3.0    D

inner-join version (drops books): ['phones', 'shoes', 'shoes']

pandas
category  second_count term
   books           NaN  NaN
  phones           2.0    Y
   shoes           3.0    C
   shoes           3.0    D

assert passed: equal, rows ordered by category, term
```

**Edge cases:**
- **Tie for the top (A, B):** dense rank keeps rank 2 for the next count (3), not skipping it; with `RANK` the next rank after two ties would be 3 and shoes would come back with nothing.
- **Tie for second (C, D):** both returned, two rows for shoes.
- **Single distinct count (books):** appears with NULL for count and term. The printed `inner-join version` line shows that an inner join silently drops books.
- **A category with several terms but all the same count:** also only one distinct count, so also NULL.
- **Order of output:** NULL term sorts first in SQLite ascending, last in some engines; the output here has one row for books so the order is not affected, but say it.
- **Empty table:** no categories, no rows.

**Then explain:**
- **Where the filter goes:** a `WHERE r.rk = 2` after the join would turn the left join into an inner join and drop books; the condition belongs in `ON`.
- **Dense vs plain rank for "second highest":** the same idea as the second highest salary question (Part 4 Q5 and Q46, the per-department version with NULL for a single distinct salary), with ties handled by rank on distinct values.
- **pandas detail:** `rank` returns floats; the comparison `rk == 2` works on them. The merged `second_count` is float with NaN, and the Code block compares after turning NaN and NULL into None.
- **Dialects (not executed here):** standard on PostgreSQL, MySQL 8, SQL Server, BigQuery and Snowflake; `QUALIFY` on BigQuery and Snowflake would shorten the rank filter (not executed).
- **Scoring note (Set F2, Q2 of 5, 20 pts):** about 8 points for the four right rows (shoes C and D, phones Y, books NULL), 4 for the seeded edge cases (both ties and the NULL category), 4 for pandas asserted equal, 2 for saying "second highest distinct count" and why it is dense, 2 for a check (every returned count is below the category maximum). Dropping books earns no edge-case points.

**Follow-ups:**
- *Top N distinct counts per category?* Change `rk = 2` to `rk <= N`.
- *Also return the first place?* Return both ranks with `rk IN (1, 2)` and keep the category list via the left join.
- *What if terms differ only by case?* Normalise with `LOWER(TRIM(term))` before counting (Part 10).

**Common mistakes:**
- `RANK` instead of `DENSE_RANK`.
- `LIMIT 1 OFFSET 1`, which returns one arbitrary tied term.
- `WHERE rk = 2` after a left join.
- Counting search rows when the question means distinct users; here each row is one search, as the prompt says.

### Q21 ⭐⭐ 🟡 [Set F3, Q3 of 5, 8 min, 20 pts] Month-over-month revenue with a missing month (Amazon-style, Part 5 Q16, Part 6 Q6). orders(order_id, order_date, amount) over Jan to May 2025 where April has no orders. Return month, revenue, previous month revenue and growth percent; April must appear with 0 and May's growth must be NULL when the previous month is zero. SQL with a month spine and pandas (resample or reindex), asserting equal.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Build a month spine (Jan to May) so April exists, LEFT JOIN the orders and `COALESCE` the sum to 0, then `LAG` the previous month and divide by `NULLIF(prev, 0)`, so growth is NULL when there is nothing to grow from.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2025-01-10',100),(2,'2025-01-31',50),
 (3,'2025-02-14',200),
 (4,'2025-03-01',150),(5,'2025-03-20',50),
 (6,'2025-05-05',120);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH RECURSIVE spine(m) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < '2025-05-01'
),
monthly AS (
  SELECT substr(s.m, 1, 7) AS month, COALESCE(SUM(o.amount), 0) AS revenue
  FROM spine s
  LEFT JOIN orders o ON substr(o.order_date, 1, 7) = substr(s.m, 1, 7)
  GROUP BY s.m
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
FROM monthly
ORDER BY month
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
m = orders.set_index("order_date")["amount"].resample("MS").sum()
m = m.reindex(pd.date_range("2025-01-01", "2025-05-01", freq="MS"), fill_value=0)
p = m.rename("revenue").to_frame()
p["month"] = p.index.strftime("%Y-%m")
p["prev_revenue"] = p["revenue"].shift(1)
p["growth_pct"] = (100.0 * (p["revenue"] - p["prev_revenue"])
                   / p["prev_revenue"].where(p["prev_revenue"] != 0)).round(1)
p = p[["month", "revenue", "prev_revenue", "growth_pct"]].reset_index(drop=True)
```

**Example:** Orders: Jan 100 + 50 = 150, Feb 200, Mar 150 + 50 = 200, Apr none, May 120. Spine row 2025-04 finds no orders, so the sum is NULL and `COALESCE` makes it 0. Growth Feb = (200 - 150) / 150 = 33.3 percent. Mar = (200 - 200) / 200 = 0.0. Apr = (0 - 200) / 200 = -100.0. May's previous month is 0, so `NULLIF(0, 0)` is NULL and the growth is NULL (not 0, not infinite). Jan has no previous row, so `LAG` gives NULL and growth is NULL too.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q21: month-over-month revenue with a missing month (April), spine in SQL and reindex in pandas.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2025-01-10',100),(2,'2025-01-31',50),
 (3,'2025-02-14',200),
 (4,'2025-03-01',150),(5,'2025-03-20',50),
 (6,'2025-05-05',120);
"""
SQL = """
WITH RECURSIVE spine(m) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < '2025-05-01'
),
monthly AS (
  SELECT substr(s.m, 1, 7) AS month, COALESCE(SUM(o.amount), 0) AS revenue
  FROM spine s
  LEFT JOIN orders o ON substr(o.order_date, 1, 7) = substr(s.m, 1, 7)
  GROUP BY s.m
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
FROM monthly
ORDER BY month
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con, parse_dates=["order_date"])
# PANDAS START
m = orders.set_index("order_date")["amount"].resample("MS").sum()
m = m.reindex(pd.date_range("2025-01-01", "2025-05-01", freq="MS"), fill_value=0)
p = m.rename("revenue").to_frame()
p["month"] = p.index.strftime("%Y-%m")
p["prev_revenue"] = p["revenue"].shift(1)
p["growth_pct"] = (100.0 * (p["revenue"] - p["prev_revenue"])
                   / p["prev_revenue"].where(p["prev_revenue"] != 0)).round(1)
p = p[["month", "revenue", "prev_revenue", "growth_pct"]].reset_index(drop=True)
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (same 5 rows, ordered by month; NULL in SQL equals NaN in pandas)")

# resample alone only spans the months that have orders: it stops at the last order
short = orders[orders["order_date"] < "2025-05-01"].set_index("order_date")["amount"].resample("MS").sum()
print("resample without reindex, orders before May only: rows", len(short), "ending at", short.index.max().strftime("%Y-%m"))
# naive growth without NULLIF would divide by zero
print("SQLite 100.0*(120-0)/0 gives (NULL, no error in SQLite):", con.execute("SELECT 100.0*(120-0)/0").fetchone()[0])
print("pandas 120.0 / 0.0 gives:", (pd.Series([120.0]) / pd.Series([0.0])).iloc[0], "(inf, not NaN, so the zero must be masked)")
```

**Output (my run):**
```text
  month  revenue  prev_revenue  growth_pct
2025-01      150           NaN         NaN
2025-02      200         150.0        33.3
2025-03      200         200.0         0.0
2025-04        0         200.0      -100.0
2025-05      120           0.0         NaN

  month  revenue  prev_revenue  growth_pct
2025-01      150           NaN         NaN
2025-02      200         150.0        33.3
2025-03      200         200.0         0.0
2025-04        0         200.0      -100.0
2025-05      120           0.0         NaN

asserts passed (same 5 rows, ordered by month; NULL in SQL equals NaN in pandas)
resample without reindex, orders before May only: rows 3 ending at 2025-03
SQLite 100.0*(120-0)/0 gives (NULL, no error in SQLite): None
pandas 120.0 / 0.0 gives: inf (inf, not NaN, so the zero must be masked)
```

**Edge cases:**
- Missing month: without the spine the April row simply does not exist, and May's `LAG` would then point at March (growth 120 versus 200 would be wrong). In pandas, `resample("MS")` fills inner gaps with 0 for free, but it stops at the last month that has data; the run shows a series with only orders before May ending at 2025-03. So reindex to an explicit `date_range` when the report must have a fixed set of months.
- Division by zero: SQLite returns NULL for `100.0 * 120 / 0` (the run printed None), so the guard is not needed for SQLite, but keep `NULLIF` anyway: PostgreSQL raises a division-by-zero error for this (not executed here). pandas float division gives `inf` (the run printed inf), so mask the zero with `where`.
- Boundary dates: 2025-01-31 and 2025-03-01 land in January and March because the month key is `substr(date, 1, 7)`; a timestamp column with a time part would still work for the text key but not for a `BETWEEN` on dates.
- Rounding: growth is rounded to one decimal here; SQLite `ROUND` and pandas `round` can differ on exact halves (Part 10), none occurs in this data.

**Then explain:**
- Spine first, then join: the spine owns the months, the orders table only contributes numbers. This is the Part 6 Q6 pattern and the Part 5 Q16 `LAG` growth.
- `LAG` after the aggregation, never over raw orders: it must see one row per month.
- In an interview say the growth definition out loud: (this - previous) / previous, NULL when previous is 0.
- Scoring note (Set F3, Q3 of 5, 20 pts, part-header rubric): about 8 pts for a query that returns April as 0 and the right growth on the seed; 4 pts for May NULL and January NULL (and not 0 or an error); 4 pts for the pandas version matching (resample or reindex); 2 pts for stating the growth formula and that April is a real zero; 2 pts for a one-line check such as 5 rows and revenue total 670. Partial credit: a query without a spine that gets Jan, Feb, Mar, May right but drops April earns the correctness points only up to about half.

**Follow-ups:**
- Year-over-year? Same spine but `LAG(revenue, 12)` over a 12-month-plus spine (Part 6 Q6); with a gap-free spine the offset is exact. Not executed on other engines: PostgreSQL could build the spine with `generate_series` and `date_trunc` (not executed here).
- Why not `LAG` over a table with a missing month? Because `LAG` goes by row position, not by calendar, so May would compare with March.
- What if the first month should show 0 growth instead of NULL? Say that is a business choice; NULL means not defined.

**Common mistakes:**
- Joining orders to the spine with the filter in `WHERE`, which turns the LEFT JOIN back into an inner join and drops April.
- Using `COALESCE(growth, 0)` and hiding the undefined growth.
- Computing growth with integer division in engines that truncate (the `100.0` multiplier avoids it).
- Relying on `resample` to cover a range it does not know about.

### Q22 ⭐⭐ 🟡 [Set F3, Q2 of 5, 8 min, 20 pts] Best-selling product per category per month (Part 4 Q15). order_items(order_id, product_id, qty), orders(order_id, order_date), products(product_id, category). Return per category and month the product with the most units, all products on ties, for Jan and Feb 2025 only. Seed 6 products in 2 categories with a tie in one month. SQL (RANK in a CTE) and pandas (groupby, rank method='min').
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Aggregate units per category, month and product, then `RANK()` descending inside each (category, month) and keep rank 1; `RANK` (not `ROW_NUMBER`) keeps every tied product.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'books'),(2,'books'),(3,'books'),(4,'toys'),(5,'toys'),(6,'toys');
INSERT INTO orders VALUES (1,'2025-01-05'),(2,'2025-01-20'),(3,'2025-02-03'),(4,'2025-02-18'),(5,'2025-03-02');
INSERT INTO order_items VALUES
 (1,1,3),(1,2,2),(1,4,1),
 (2,1,1),(2,2,2),(2,5,4),
 (3,3,5),(3,4,2),(3,5,2),
 (4,6,1),(4,4,0),
 (5,1,9);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH units AS (
  SELECT p.category, substr(o.order_date, 1, 7) AS month, p.product_id, SUM(oi.qty) AS units
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.order_date >= '2025-01-01' AND o.order_date < '2025-03-01'
  GROUP BY p.category, substr(o.order_date, 1, 7), p.product_id
),
ranked AS (
  SELECT *, RANK() OVER (PARTITION BY category, month ORDER BY units DESC) AS rnk
  FROM units
)
SELECT category, month, product_id, units
FROM ranked
WHERE rnk = 1
ORDER BY category, month, product_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
d = oi.merge(o, on="order_id").merge(pr, on="product_id")
d = d[(d["order_date"] >= "2025-01-01") & (d["order_date"] < "2025-03-01")].copy()
d["month"] = d["order_date"].str[:7]
u = d.groupby(["category", "month", "product_id"], as_index=False)["qty"].sum().rename(columns={"qty": "units"})
u["rnk"] = u.groupby(["category", "month"])["units"].rank(method="min", ascending=False)
p = (u[u["rnk"] == 1][["category", "month", "product_id", "units"]]
     .sort_values(["category", "month", "product_id"]).reset_index(drop=True))
```

**Example:** Jan books: product 1 sold 3 + 1 = 4, product 2 sold 2 + 2 = 4, so both rank 1 (tie). Jan toys: product 4 sold 1, product 5 sold 4, so product 5 wins. Feb books: only product 3 with 5. Feb toys: product 4 sold 2 + 0 = 2, product 5 sold 2, product 6 sold 1, so products 4 and 5 tie at 2. The March order (product 1, 9 units) is outside the date filter. That gives 6 rows: 2 for books Jan, 1 for books Feb, 1 for toys Jan, 2 for toys Feb.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q22: best-selling product per category per month, all products on ties.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'books'),(2,'books'),(3,'books'),(4,'toys'),(5,'toys'),(6,'toys');
INSERT INTO orders VALUES (1,'2025-01-05'),(2,'2025-01-20'),(3,'2025-02-03'),(4,'2025-02-18'),(5,'2025-03-02');
INSERT INTO order_items VALUES
 (1,1,3),(1,2,2),(1,4,1),
 (2,1,1),(2,2,2),(2,5,4),
 (3,3,5),(3,4,2),(3,5,2),
 (4,6,1),(4,4,0),
 (5,1,9);
"""
SQL = """
WITH units AS (
  SELECT p.category, substr(o.order_date, 1, 7) AS month, p.product_id, SUM(oi.qty) AS units
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.order_date >= '2025-01-01' AND o.order_date < '2025-03-01'
  GROUP BY p.category, substr(o.order_date, 1, 7), p.product_id
),
ranked AS (
  SELECT *, RANK() OVER (PARTITION BY category, month ORDER BY units DESC) AS rnk
  FROM units
)
SELECT category, month, product_id, units
FROM ranked
WHERE rnk = 1
ORDER BY category, month, product_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

oi = pd.read_sql("SELECT * FROM order_items", con)
o = pd.read_sql("SELECT * FROM orders", con)
pr = pd.read_sql("SELECT * FROM products", con)
# PANDAS START
d = oi.merge(o, on="order_id").merge(pr, on="product_id")
d = d[(d["order_date"] >= "2025-01-01") & (d["order_date"] < "2025-03-01")].copy()
d["month"] = d["order_date"].str[:7]
u = d.groupby(["category", "month", "product_id"], as_index=False)["qty"].sum().rename(columns={"qty": "units"})
u["rnk"] = u.groupby(["category", "month"])["units"].rank(method="min", ascending=False)
p = (u[u["rnk"] == 1][["category", "month", "product_id", "units"]]
     .sort_values(["category", "month", "product_id"]).reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (compared after sorting by category, month, product_id)")

# row_number would keep one of the tied products
rn = pd.read_sql(SQL.replace("RANK()", "ROW_NUMBER()"), con)
print("with ROW_NUMBER instead of RANK:", len(rn), "rows vs", len(s), "with RANK")
```

**Output (my run):**
```text
category   month  product_id  units
   books 2025-01           1      4
   books 2025-01           2      4
   books 2025-02           3      5
    toys 2025-01           5      4
    toys 2025-02           4      2
    toys 2025-02           5      2

category   month  product_id  units
   books 2025-01           1      4
   books 2025-01           2      4
   books 2025-02           3      5
    toys 2025-01           5      4
    toys 2025-02           4      2
    toys 2025-02           5      2

asserts passed (compared after sorting by category, month, product_id)
with ROW_NUMBER instead of RANK: 4 rows vs 6 with RANK
```

**Edge cases:**
- Ties: the run returns 6 rows with `RANK`, only 4 with `ROW_NUMBER` (one of each tied pair would be dropped, and which one is not defined without a tiebreaker).
- Date filter: `>= '2025-01-01' AND < '2025-03-01'` is a half-open range, so no end-of-month day is lost and March data (9 units of product 1) is excluded.
- Zero quantity rows (product 4 has a 0 line) add 0 and do not change the sum.
- A category with no sales in a month has no row at all (nothing to rank); add a spine if the report needs an empty line.
- pandas `rank(method="min", ascending=False)` matches `RANK`; `"dense"` would match `DENSE_RANK` and only differs beyond rank 1.

**Then explain:**
- Two steps: sum first (per product), rank second (per category and month); you cannot rank and sum in one pass without a window over an aggregate.
- The window is `PARTITION BY category, month ORDER BY units DESC`. Part 4 Q15 is the same shape.
- In engines with `QUALIFY` (Snowflake, BigQuery, not executed here) the rank filter can go in the same SELECT; in SQLite it needs the CTE.
- Scoring note (Set F3, Q2 of 5, 20 pts): about 8 pts for the right 6 rows; 4 pts for keeping both tied products (using `RANK`, not `ROW_NUMBER`) and excluding March; 4 pts for the pandas groupby and `rank(method="min")` matching; 2 pts for saying what ties mean for the business; 2 pts for a count check. Partial credit: `ROW_NUMBER` or `LIMIT 1` per group gets the structure right but loses the tie points.

**Follow-ups:**
- Top 2 products per category? `rnk <= 2` with `RANK` can return more than 2 rows on ties; with `DENSE_RANK` the ranks are consecutive (Part 4 Q4).
- Why not `MAX(units)` per group joined back? It also works and keeps ties; the window is shorter and extends to top N.
- A deterministic single winner? Add a tiebreaker such as `product_id` to the `ORDER BY` and use `ROW_NUMBER`.

**Common mistakes:**
- `ROW_NUMBER` silently drops one of two tied best sellers.
- Ranking raw order lines instead of per-product totals.
- Filtering the month in a way that includes 2025-03-01 or misses 2025-02-28 timestamps.
- In pandas, `rank()` default is `average`, which gives 1.5 for a tie and then `== 1` finds nothing.

### Q23 ⭐⭐ 🟡 [Set T1, Q3 of 5, 8 min, 20 pts] Latest transaction per user with the balance after it (Part 4 Q9, Part 5 Q12). bank_txns(txn_id, user_id, txn_ts, signed_amount). Return one row per user: last txn_id, last timestamp and the account balance after it. Two transactions can share the same timestamp (break by txn_id). Seed 3 users. SQL (window running sum plus ROW_NUMBER) and pandas (cumsum, groupby tail), asserting equal.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Compute the running balance with `SUM(...) OVER (PARTITION BY user ORDER BY txn_ts, txn_id ROWS ...)` and a `ROW_NUMBER()` in descending order of the same key, then keep row number 1; the `txn_id` in the order is the tiebreaker.

**Schema and sample data:**
```sql
CREATE TABLE bank_txns(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_ts TEXT, signed_amount INTEGER);
INSERT INTO bank_txns VALUES
 (1,1,'2025-06-01 09:00:00',1000),
 (2,1,'2025-06-02 10:00:00',-300),
 (3,1,'2025-06-02 10:00:00',-200),
 (4,2,'2025-06-01 12:00:00',500),
 (5,2,'2025-06-03 08:00:00',250),
 (6,3,'2025-06-05 15:30:00',-40);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH t AS (
  SELECT txn_id, user_id, txn_ts,
         SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts, txn_id
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_after,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_ts DESC, txn_id DESC) AS rn
  FROM bank_txns
)
SELECT user_id, txn_id AS last_txn_id, txn_ts AS last_ts, balance_after
FROM t
WHERE rn = 1
ORDER BY user_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
t = tx.sort_values(["user_id", "txn_ts", "txn_id"]).reset_index(drop=True)
t["balance_after"] = t.groupby("user_id")["signed_amount"].cumsum()
p = (t.groupby("user_id").tail(1)
     .rename(columns={"txn_id": "last_txn_id", "txn_ts": "last_ts"})
     [["user_id", "last_txn_id", "last_ts", "balance_after"]]
     .sort_values("user_id").reset_index(drop=True))
```

**Example:** User 1: txn 1 adds 1000, txn 2 takes 300 and txn 3 takes 200 at the same second (10:00:00). Sorted by (timestamp, txn_id) the balances are 1000, 700, 500, so the latest row is txn 3 with 500. User 2: 500 then 250 gives 750 on txn 5. User 3 has one row, txn 6 with -40, so a negative balance is allowed. The result is one row per user: (1, 3, 500), (2, 5, 750), (3, 6, -40).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q23: latest transaction per user with the balance after it; tie on timestamp broken by txn_id.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE bank_txns(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_ts TEXT, signed_amount INTEGER);
INSERT INTO bank_txns VALUES
 (1,1,'2025-06-01 09:00:00',1000),
 (2,1,'2025-06-02 10:00:00',-300),
 (3,1,'2025-06-02 10:00:00',-200),
 (4,2,'2025-06-01 12:00:00',500),
 (5,2,'2025-06-03 08:00:00',250),
 (6,3,'2025-06-05 15:30:00',-40);
"""
SQL = """
WITH t AS (
  SELECT txn_id, user_id, txn_ts,
         SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts, txn_id
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_after,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_ts DESC, txn_id DESC) AS rn
  FROM bank_txns
)
SELECT user_id, txn_id AS last_txn_id, txn_ts AS last_ts, balance_after
FROM t
WHERE rn = 1
ORDER BY user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

tx = pd.read_sql("SELECT * FROM bank_txns", con)
# PANDAS START
t = tx.sort_values(["user_id", "txn_ts", "txn_id"]).reset_index(drop=True)
t["balance_after"] = t.groupby("user_id")["signed_amount"].cumsum()
p = (t.groupby("user_id").tail(1)
     .rename(columns={"txn_id": "last_txn_id", "txn_ts": "last_ts"})
     [["user_id", "last_txn_id", "last_ts", "balance_after"]]
     .sort_values("user_id").reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (one row per user, ordered by user_id)")

# the tie trap: ORDER BY txn_ts DESC only picks either of txns 2 and 3 for user 1 (not defined)
# and a default-frame running sum gives both tied rows the SAME balance
r = con.execute("""SELECT txn_id, SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts) AS bal
                   FROM bank_txns WHERE user_id = 1 ORDER BY txn_id""").fetchall()
print("user 1, default frame, ORDER BY txn_ts only (txn_id, balance):", r)
```

**Output (my run):**
```text
 user_id  last_txn_id             last_ts  balance_after
       1            3 2025-06-02 10:00:00            500
       2            5 2025-06-03 08:00:00            750
       3            6 2025-06-05 15:30:00            -40

 user_id  last_txn_id             last_ts  balance_after
       1            3 2025-06-02 10:00:00            500
       2            5 2025-06-03 08:00:00            750
       3            6 2025-06-05 15:30:00            -40

asserts passed (one row per user, ordered by user_id)
user 1, default frame, ORDER BY txn_ts only (txn_id, balance): [(1, 1000), (2, 500), (3, 500)]
```

**Edge cases:**
- Tie on timestamp: which row is "last" depends on the tiebreaker. With `txn_id` ascending as the posting order, txn 3 is last for user 1; if you broke the tie the other way txn 2 would be last. The final balance (500) is the same either way, the reported `last_txn_id` is not.
- Default frame trap: with `ORDER BY txn_ts` only, the default frame is `RANGE` and tied rows share one balance; the run shows user 1 as (1, 1000), (2, 500), (3, 500), so txn 2 appears to leave 500, not 700.
- A user with a single transaction works (rank 1 is that row). A user with no transactions has no row at all; join from a users table if you need them.
- Timestamps are text in ISO format, which sorts correctly as text.

**Then explain:**
- Two windows with the same partition and the same ordering key, one ascending (running sum) and one descending (pick the last). Part 4 Q9 gives the latest row, Part 5 Q12 the running balance.
- The sum must be computed over all rows before filtering to the last row, so both live in a CTE and the filter is outside.
- pandas: sort, `groupby.cumsum`, then `groupby.tail(1)`; sort first or `cumsum` runs in file order.
- Scoring note (Set T1, Q3 of 5, 20 pts): about 8 pts for three correct rows with balances; 4 pts for a deterministic tiebreak (txn_id) and naming the tie; 4 pts for pandas `cumsum` plus `tail(1)` matching; 2 pts for stating the tie rule; 2 pts for checking that the last balance equals the sum of all amounts per user. Partial credit: a correct latest row without the balance, or a balance from a tie-unsafe frame.

**Follow-ups:**
- Balance before the last transaction? Use `LAG(balance_after)` or subtract the amount.
- Why `ROWS` rather than `RANGE`? `RANGE` treats equal timestamps as one group; `ROWS` counts physical rows in the given order.
- Why not `MAX(txn_ts)` joined back? It returns both tied rows for user 1 and still has no balance.

**Common mistakes:**
- Filtering to the last row first and then summing (the balance becomes just that one amount).
- Ordering by timestamp only and trusting the engine's order for ties.
- In pandas, calling `cumsum` before sorting, or `groupby.last()` which skips NaN per column instead of returning a whole row.

### Q24 ⭐⭐ 🟡 [Set T1, Q2 of 5, 8 min, 20 pts] Duplicate payment detector. payments(payment_id, user_id, merchant, amount, paid_at TEXT). A payment is a suspected duplicate if the same user paid the same merchant the same amount within 5 minutes of an earlier payment (Part 7 Q26 style for adjacent events). Return the later payment ids with the earlier payment id they duplicate. Seed 7 rows including a triple duplicate and a same-amount payment 6 minutes later. SQL (self join or LAG) and pandas (shift within groups).
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Partition by (user, merchant, amount), order by time, use `LAG` to get the previous matching payment and flag the row when the gap is 300 seconds or less; a self join over all earlier matches is the alternative but returns a pair for every earlier payment in the window.

**Schema and sample data:**
```sql
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, merchant TEXT, amount INTEGER, paid_at TEXT);
INSERT INTO payments VALUES
 (1,1,'m1',500,'2025-06-01 10:00:00'),
 (2,1,'m1',500,'2025-06-01 10:02:00'),
 (3,1,'m1',500,'2025-06-01 10:04:30'),
 (4,1,'m1',500,'2025-06-01 10:10:30'),
 (5,2,'m1',500,'2025-06-01 10:01:00'),
 (6,1,'m2',500,'2025-06-01 10:03:00'),
 (7,1,'m1',450,'2025-06-01 10:03:00');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH x AS (
  SELECT payment_id, paid_at,
         LAG(payment_id) OVER w AS earlier_id,
         LAG(paid_at)    OVER w AS earlier_at
  FROM payments
  WINDOW w AS (PARTITION BY user_id, merchant, amount ORDER BY paid_at, payment_id)
)
SELECT payment_id AS later_id, earlier_id,
       CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) AS gap_seconds
FROM x
WHERE earlier_id IS NOT NULL
  AND CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) <= 300
ORDER BY later_id
```
The all-pairs alternative is `SQL_ALL_PAIRS` in the Code block (a self join on the same keys with an earlier-than condition).

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
d = pay.assign(ts=pd.to_datetime(pay["paid_at"])).sort_values(["user_id", "merchant", "amount", "ts", "payment_id"])
g = d.groupby(["user_id", "merchant", "amount"])
d["earlier_id"] = g["payment_id"].shift(1)
d["gap_seconds"] = (d["ts"] - g["ts"].shift(1)).dt.total_seconds()
hit = d[d["earlier_id"].notna() & (d["gap_seconds"] <= 300)]
p = (hit.rename(columns={"payment_id": "later_id"})[["later_id", "earlier_id", "gap_seconds"]]
     .astype({"earlier_id": "int64", "gap_seconds": "int64"})
     .sort_values("later_id").reset_index(drop=True))
```

**Example:** User 1 pays merchant m1 an amount of 500 at 10:00:00 (payment 1), 10:02:00 (payment 2), 10:04:30 (payment 3) and 10:10:30 (payment 4). Payment 2 is 120 seconds after 1, so it duplicates 1. Payment 3 is 150 seconds after 2, so it duplicates 2. Payment 4 is 360 seconds (6 minutes) after 3, so it is not flagged. Payment 5 is another user, payment 6 another merchant and payment 7 another amount, so none of them join any chain. Result: (2 duplicates 1) and (3 duplicates 2).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q24: duplicate payment detector (same user, merchant, amount, within 5 minutes of the previous such payment).
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, merchant TEXT, amount INTEGER, paid_at TEXT);
INSERT INTO payments VALUES
 (1,1,'m1',500,'2025-06-01 10:00:00'),
 (2,1,'m1',500,'2025-06-01 10:02:00'),
 (3,1,'m1',500,'2025-06-01 10:04:30'),
 (4,1,'m1',500,'2025-06-01 10:10:30'),
 (5,2,'m1',500,'2025-06-01 10:01:00'),
 (6,1,'m2',500,'2025-06-01 10:03:00'),
 (7,1,'m1',450,'2025-06-01 10:03:00');
"""
SQL = """
WITH x AS (
  SELECT payment_id, paid_at,
         LAG(payment_id) OVER w AS earlier_id,
         LAG(paid_at)    OVER w AS earlier_at
  FROM payments
  WINDOW w AS (PARTITION BY user_id, merchant, amount ORDER BY paid_at, payment_id)
)
SELECT payment_id AS later_id, earlier_id,
       CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) AS gap_seconds
FROM x
WHERE earlier_id IS NOT NULL
  AND CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) <= 300
ORDER BY later_id
"""
SQL_ALL_PAIRS = """
SELECT b.payment_id AS later_id, a.payment_id AS earlier_id
FROM payments a
JOIN payments b
  ON b.user_id = a.user_id AND b.merchant = a.merchant AND b.amount = a.amount
 AND (b.paid_at > a.paid_at OR (b.paid_at = a.paid_at AND b.payment_id > a.payment_id))
 AND CAST(strftime('%s', b.paid_at) AS INTEGER) - CAST(strftime('%s', a.paid_at) AS INTEGER) <= 300
ORDER BY later_id, earlier_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

pay = pd.read_sql("SELECT * FROM payments", con)
# PANDAS START
d = pay.assign(ts=pd.to_datetime(pay["paid_at"])).sort_values(["user_id", "merchant", "amount", "ts", "payment_id"])
g = d.groupby(["user_id", "merchant", "amount"])
d["earlier_id"] = g["payment_id"].shift(1)
d["gap_seconds"] = (d["ts"] - g["ts"].shift(1)).dt.total_seconds()
hit = d[d["earlier_id"].notna() & (d["gap_seconds"] <= 300)]
p = (hit.rename(columns={"payment_id": "later_id"})[["later_id", "earlier_id", "gap_seconds"]]
     .astype({"earlier_id": "int64", "gap_seconds": "int64"})
     .sort_values("later_id").reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (compared after sorting by later_id)")

allp = pd.read_sql(SQL_ALL_PAIRS, con)
print("\nself join on every earlier match returns", len(allp), "pairs:", [(int(a), int(b)) for a, b in allp.values])
print("payment 4 is 6:00 after payment 3, so it is not flagged; gap in seconds:",
      con.execute("SELECT CAST(strftime('%s','2025-06-01 10:10:30') AS INTEGER) - CAST(strftime('%s','2025-06-01 10:04:30') AS INTEGER)").fetchone()[0])
```

**Output (my run):**
```text
 later_id  earlier_id  gap_seconds
        2           1          120
        3           2          150

 later_id  earlier_id  gap_seconds
        2           1          120
        3           2          150

asserts passed (compared after sorting by later_id)

self join on every earlier match returns 3 pairs: [(2, 1), (3, 1), (3, 2)]
payment 4 is 6:00 after payment 3, so it is not flagged; gap in seconds: 360
```

**Edge cases:**
- Triple duplicate: `LAG` links each payment to the previous matching one, so the triple gives 2 rows. A self join on every earlier match gives 3 pairs, (2,1), (3,1) and (3,2), because payment 3 is also within 5 minutes of payment 1 (270 seconds). Decide which one the business wants: one row per suspected duplicate payment (LAG) or every pair.
- Boundary: the rule is `<= 300` seconds, so a gap of exactly 5:00 is flagged; say so, since "within 5 minutes" is ambiguous. The 6:00 case (360 seconds) is not flagged.
- Chains: with `LAG` a stream of payments each 4 minutes apart is flagged all the way down, even though the first and last are far apart; that is usually what a fraud team wants, but say it.
- Same timestamp: `payment_id` breaks the tie so the earlier id is "earlier".
- Time arithmetic on text uses `strftime('%s', ts)` cast to integer seconds; on timestamp columns PostgreSQL would subtract directly (not executed here).

**Then explain:**
- Adjacent events in a group is a `LAG` problem (Part 7 Q26); the partition holds the equality conditions, the `ORDER BY` holds time.
- The 5-minute test is a difference in seconds so it has no calendar rounding.
- pandas: sort, `groupby(...).shift(1)` for the previous id and time, subtract timestamps.
- Scoring note (Set T1, Q2 of 5, 20 pts): about 8 pts for the two correct (later, earlier) pairs; 4 pts for rejecting the 6-minute payment and the different user, merchant and amount rows; 4 pts for pandas `shift` matching; 2 pts for stating inclusive or exclusive and LAG versus all-pairs; 2 pts for a count check (2 flagged of 7). Partial credit: a self join without the earlier-than condition returns each pair twice or pairs a row with itself.

**Follow-ups:**
- Count of duplicates per user? Group the flagged rows by user.
- Why not a `RANGE` window of 5 minutes? SQLite cannot do `RANGE` with an interval over text timestamps (Part 5 and the set note); PostgreSQL 11 and later accepts `RANGE BETWEEN INTERVAL '5 minutes' PRECEDING AND CURRENT ROW` on a timestamp column (not executed here).
- Make it idempotent for retries? That is a data-quality design point: a unique idempotency key beats detecting duplicates after the fact.

**Common mistakes:**
- Self join without `b.paid_at > a.paid_at` (each pair twice, plus a row paired with itself).
- Comparing text timestamps with `<` and forgetting the difference is not a number of minutes.
- Missing the amount (or merchant) in the partition.
- In pandas, shifting without sorting first, or shifting across groups instead of inside them.

### Q25 ⭐⭐ 🟡 [Set T2, Q3 of 5, 8 min, 20 pts] Days past due buckets (lending). loans(loan_id, due_date, paid_date NULL) as of 2025-06-30. Bucket each loan: PAID_ON_TIME, PAID_LATE, CURRENT, DPD_1_30, DPD_31_60, DPD_61_PLUS using days between due_date and paid_date or the as-of date (Part 6 Q3, Part 1 Q10). Seed 9 loans on every boundary (due exactly 30 and 31 days ago). SQL with CASE and julianday, pandas with pd.cut and an explicit as-of date; assert equal and state the boundary rule.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Compute days past due as the as-of date minus the due date for unpaid loans and map it with a CASE whose edges are 0, 30 and 60; paid loans are PAID_ON_TIME when `paid_date <= due_date`, else PAID_LATE.

**Schema and sample data:**
```sql
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, due_date TEXT, paid_date TEXT);
INSERT INTO loans VALUES
 (1,'2025-06-30',NULL),
 (2,'2025-07-15',NULL),
 (3,'2025-06-29',NULL),
 (4,'2025-05-31',NULL),
 (5,'2025-05-30',NULL),
 (6,'2025-05-01',NULL),
 (7,'2025-04-30',NULL),
 (8,'2025-05-10','2025-05-10'),
 (9,'2025-05-10','2025-05-11');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
SELECT loan_id, due_date, paid_date,
       CASE WHEN paid_date IS NULL
            THEN CAST(julianday(:as_of) - julianday(due_date) AS INTEGER) END AS dpd,
       CASE
         WHEN paid_date IS NOT NULL AND paid_date <= due_date THEN 'PAID_ON_TIME'
         WHEN paid_date IS NOT NULL THEN 'PAID_LATE'
         WHEN julianday(:as_of) - julianday(due_date) <= 0 THEN 'CURRENT'
         WHEN julianday(:as_of) - julianday(due_date) <= 30 THEN 'DPD_1_30'
         WHEN julianday(:as_of) - julianday(due_date) <= 60 THEN 'DPD_31_60'
         ELSE 'DPD_61_PLUS'
       END AS bucket
FROM loans
ORDER BY loan_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
as_of = pd.Timestamp("2025-06-30")
due = pd.to_datetime(loans["due_date"])
paid = pd.to_datetime(loans["paid_date"])
dpd = (as_of - due).dt.days
cut = pd.cut(dpd, bins=[-10**6, 0, 30, 60, 10**6],
             labels=["CURRENT", "DPD_1_30", "DPD_31_60", "DPD_61_PLUS"]).astype(object)
bucket = np.select([paid.notna() & (paid <= due), paid.notna()],
                   ["PAID_ON_TIME", "PAID_LATE"], default=cut)
p = loans[["loan_id", "due_date", "paid_date"]].copy()
p["dpd"] = dpd.where(paid.isna())
p["bucket"] = bucket
```

**Example:** As of 2025-06-30: loan 1 is due today (0 days) so CURRENT, loan 2 is due 2025-07-15 (-15) so CURRENT. Loan 3 is due 06-29 (1 day) so DPD_1_30, loan 4 due 05-31 is exactly 30 days so still DPD_1_30, loan 5 due 05-30 is 31 days so DPD_31_60, loan 6 due 05-01 is exactly 60 so DPD_31_60, loan 7 due 04-30 is 61 so DPD_61_PLUS. Loan 8 was paid on its due date so PAID_ON_TIME, loan 9 was paid a day later so PAID_LATE. Bucket counts: CURRENT 2, DPD_1_30 2, DPD_31_60 2, DPD_61_PLUS 1, one PAID_LATE, one PAID_ON_TIME.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q25: days-past-due buckets as of 2025-06-30.
import sqlite3
import numpy as np
import pandas as pd

AS_OF = "2025-06-30"
DDL = """
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, due_date TEXT, paid_date TEXT);
INSERT INTO loans VALUES
 (1,'2025-06-30',NULL),
 (2,'2025-07-15',NULL),
 (3,'2025-06-29',NULL),
 (4,'2025-05-31',NULL),
 (5,'2025-05-30',NULL),
 (6,'2025-05-01',NULL),
 (7,'2025-04-30',NULL),
 (8,'2025-05-10','2025-05-10'),
 (9,'2025-05-10','2025-05-11');
"""
SQL = """
SELECT loan_id, due_date, paid_date,
       CASE WHEN paid_date IS NULL
            THEN CAST(julianday(:as_of) - julianday(due_date) AS INTEGER) END AS dpd,
       CASE
         WHEN paid_date IS NOT NULL AND paid_date <= due_date THEN 'PAID_ON_TIME'
         WHEN paid_date IS NOT NULL THEN 'PAID_LATE'
         WHEN julianday(:as_of) - julianday(due_date) <= 0 THEN 'CURRENT'
         WHEN julianday(:as_of) - julianday(due_date) <= 30 THEN 'DPD_1_30'
         WHEN julianday(:as_of) - julianday(due_date) <= 60 THEN 'DPD_31_60'
         ELSE 'DPD_61_PLUS'
       END AS bucket
FROM loans
ORDER BY loan_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con, params={"as_of": AS_OF})
print(s.to_string(index=False))

loans = pd.read_sql("SELECT * FROM loans", con)
# PANDAS START
as_of = pd.Timestamp("2025-06-30")
due = pd.to_datetime(loans["due_date"])
paid = pd.to_datetime(loans["paid_date"])
dpd = (as_of - due).dt.days
cut = pd.cut(dpd, bins=[-10**6, 0, 30, 60, 10**6],
             labels=["CURRENT", "DPD_1_30", "DPD_31_60", "DPD_61_PLUS"]).astype(object)
bucket = np.select([paid.notna() & (paid <= due), paid.notna()],
                   ["PAID_ON_TIME", "PAID_LATE"], default=cut)
p = loans[["loan_id", "due_date", "paid_date"]].copy()
p["dpd"] = dpd.where(paid.isna())
p["bucket"] = bucket
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by loan_id; dpd NULL equals NaN for paid loans)")
print("pd.cut default is right-closed: 30 falls in (0, 30], 31 in (30, 60]; counts by bucket:")
print(p["bucket"].value_counts().sort_index().to_string())
```

**Output (my run):**
```text
 loan_id   due_date  paid_date   dpd       bucket
       1 2025-06-30        NaN   0.0      CURRENT
       2 2025-07-15        NaN -15.0      CURRENT
       3 2025-06-29        NaN   1.0     DPD_1_30
       4 2025-05-31        NaN  30.0     DPD_1_30
       5 2025-05-30        NaN  31.0    DPD_31_60
       6 2025-05-01        NaN  60.0    DPD_31_60
       7 2025-04-30        NaN  61.0  DPD_61_PLUS
       8 2025-05-10 2025-05-10   NaN PAID_ON_TIME
       9 2025-05-10 2025-05-11   NaN    PAID_LATE

 loan_id   due_date  paid_date   dpd       bucket
       1 2025-06-30        NaN   0.0      CURRENT
       2 2025-07-15        NaN -15.0      CURRENT
       3 2025-06-29        NaN   1.0     DPD_1_30
       4 2025-05-31        NaN  30.0     DPD_1_30
       5 2025-05-30        NaN  31.0    DPD_31_60
       6 2025-05-01        NaN  60.0    DPD_31_60
       7 2025-04-30        NaN  61.0  DPD_61_PLUS
       8 2025-05-10 2025-05-10   NaN PAID_ON_TIME
       9 2025-05-10 2025-05-11   NaN    PAID_LATE

asserts passed (ordered by loan_id; dpd NULL equals NaN for paid loans)
pd.cut default is right-closed: 30 falls in (0, 30], 31 in (30, 60]; counts by bucket:
bucket
CURRENT         2
DPD_1_30        2
DPD_31_60       2
DPD_61_PLUS     1
PAID_LATE       1
PAID_ON_TIME    1
```

**Edge cases:**
- Boundary rule written down: 0 days is CURRENT (due today is not late yet), 1 to 30 inclusive is DPD_1_30, 31 to 60 inclusive is DPD_31_60, 61 and above is DPD_61_PLUS. The run puts day 30 in the first bucket and day 31 in the next, day 60 in DPD_31_60 and day 61 in DPD_61_PLUS.
- `pd.cut` is right-closed by default, so bins `(-inf, 0], (0, 30], (30, 60], (60, inf)` reproduce those edges; `right=False` would move every boundary day into the next bucket.
- Paid loans have no days-past-due value (NULL in SQL, NaN in pandas); the unpaid-only `dpd` column avoids mixing the two meanings.
- A future due date gives a negative number (-15), which is CURRENT.
- Not in the seed: a loan paid after the as-of date would need `paid_date > as_of` treated as unpaid at that date; say so rather than silently labelling it paid.
- `julianday` differences are whole numbers for date-only text; with times they would be fractions and `CAST` truncates.

**Then explain:**
- Order the CASE branches so the paid cases come first; a paid loan must never reach the days-past-due branches.
- The as-of date is a parameter, not `date('now')`, so results are reproducible. The SQL binds it by name (`:as_of`).
- Part 6 Q3 is the date difference, Part 1 Q10 the CASE bucketing.
- Scoring note (Set T2, Q3 of 5, 20 pts): about 8 pts for all 9 buckets right; 4 pts for the boundary days (30, 31, 60, 61) landing correctly and paid loans handled before the DPD branches; 4 pts for pandas `pd.cut` (or `np.select`) matching; 2 pts for stating the boundary rule first; 2 pts for a count check (9 loans, bucket counts add to 9). Partial credit: correct buckets for unpaid loans only.

**Follow-ups:**
- Weighted exposure per bucket? Sum the outstanding amount per bucket (Part 2 Q5 style).
- Why a parameter instead of today's date? Reproducible reports and tests.
- Month-end snapshots for every month? Cross join the loans with a spine of as-of dates, not executed here.

**Common mistakes:**
- Using `<` where the rule says `<=` and moving day 30 into the next bucket.
- Treating due-today as late.
- `pd.cut` with default `right=True` misread as left-closed.
- Letting paid loans fall into the DPD branches because the NULL check came last.

### Q26 ⭐⭐ 🟡 [Set T2, Q2 of 5, 8 min, 20 pts] Running balance with same-timestamp ties (Part 5 Q6). acct_txns(txn_id, account_id, txn_ts, amount_paise) where deposits are positive. Return each transaction with a running balance per account in a deterministic order, and show what a RANGE-framed or ORDER BY txn_ts-only version returns when two rows share a timestamp. Seed 2 accounts with a tie. Give SQL and pandas and say which tie rule you chose.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Use `SUM(amount) OVER (PARTITION BY account ORDER BY txn_ts, txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`; ordering by the timestamp alone uses the default `RANGE` frame, which gives tied rows the same balance.

**Schema and sample data:**
```sql
CREATE TABLE acct_txns(txn_id INTEGER PRIMARY KEY, account_id INTEGER, txn_ts TEXT, amount_paise INTEGER);
INSERT INTO acct_txns VALUES
 (1,1,'2025-06-01 09:00:00',10000),
 (2,1,'2025-06-01 10:00:00',-2500),
 (3,1,'2025-06-01 10:00:00',-4000),
 (4,1,'2025-06-02 09:00:00',700),
 (5,2,'2025-06-01 11:00:00',3000),
 (6,2,'2025-06-01 12:00:00',-500);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
SELECT txn_id, account_id, txn_ts, amount_paise,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_rows,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts) AS balance_default_range
FROM acct_txns
ORDER BY account_id, txn_ts, txn_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
p = t.sort_values(["account_id", "txn_ts", "txn_id"]).reset_index(drop=True)
p["balance_rows"] = p.groupby("account_id")["amount_paise"].cumsum()
# RANGE-like: every row of a tied timestamp shows the balance after the whole tie group
p["balance_default_range"] = p.groupby(["account_id", "txn_ts"])["balance_rows"].transform("last")
```

**Example:** Account 1: +10000 at 09:00, then -2500 (txn 2) and -4000 (txn 3) both at 10:00:00, then +700 the next day. Deterministic order by (txn_ts, txn_id): 10000, 7500, 3500, 4200. With `ORDER BY txn_ts` only (default `RANGE` frame) rows 2 and 3 are peers, so both show 3500, the balance after the whole tie group; the intermediate 7500 never appears. Account 2: 3000 then -500 gives 3000, 2500 (no tie).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q26: running balance per account with a same-timestamp tie.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE acct_txns(txn_id INTEGER PRIMARY KEY, account_id INTEGER, txn_ts TEXT, amount_paise INTEGER);
INSERT INTO acct_txns VALUES
 (1,1,'2025-06-01 09:00:00',10000),
 (2,1,'2025-06-01 10:00:00',-2500),
 (3,1,'2025-06-01 10:00:00',-4000),
 (4,1,'2025-06-02 09:00:00',700),
 (5,2,'2025-06-01 11:00:00',3000),
 (6,2,'2025-06-01 12:00:00',-500);
"""
SQL = """
SELECT txn_id, account_id, txn_ts, amount_paise,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_rows,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts) AS balance_default_range
FROM acct_txns
ORDER BY account_id, txn_ts, txn_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

t = pd.read_sql("SELECT * FROM acct_txns", con)
# PANDAS START
p = t.sort_values(["account_id", "txn_ts", "txn_id"]).reset_index(drop=True)
p["balance_rows"] = p.groupby("account_id")["amount_paise"].cumsum()
# RANGE-like: every row of a tied timestamp shows the balance after the whole tie group
p["balance_default_range"] = p.groupby(["account_id", "txn_ts"])["balance_rows"].transform("last")
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by account_id, txn_ts, txn_id; both balance columns equal)")

# reversing txn_id inside the tie changes the intermediate balance but not the final one
alt = con.execute("""SELECT txn_id, SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id DESC
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM acct_txns
                     WHERE account_id = 1 ORDER BY txn_id""").fetchall()
print("account 1 with the tie broken by txn_id DESC (txn_id, balance):", alt)
```

**Output (my run):**
```text
 txn_id  account_id              txn_ts  amount_paise  balance_rows  balance_default_range
      1           1 2025-06-01 09:00:00         10000         10000                  10000
      2           1 2025-06-01 10:00:00         -2500          7500                   3500
      3           1 2025-06-01 10:00:00         -4000          3500                   3500
      4           1 2025-06-02 09:00:00           700          4200                   4200
      5           2 2025-06-01 11:00:00          3000          3000                   3000
      6           2 2025-06-01 12:00:00          -500          2500                   2500

 txn_id  account_id              txn_ts  amount_paise  balance_rows  balance_default_range
      1           1 2025-06-01 09:00:00         10000         10000                  10000
      2           1 2025-06-01 10:00:00         -2500          7500                   3500
      3           1 2025-06-01 10:00:00         -4000          3500                   3500
      4           1 2025-06-02 09:00:00           700          4200                   4200
      5           2 2025-06-01 11:00:00          3000          3000                   3000
      6           2 2025-06-01 12:00:00          -500          2500                   2500

asserts passed (ordered by account_id, txn_ts, txn_id; both balance columns equal)
account 1 with the tie broken by txn_id DESC (txn_id, balance): [(1, 10000), (2, 3500), (3, 6000), (4, 4200)]
```

**Edge cases:**
- Tie rule chosen: the ledger sequence `txn_id` ascending, because ids are assigned in posting order. If the tie were broken by `txn_id` DESC the run gives 10000, 3500, 6000, 4200 for account 1 (txn 3 first), so the intermediate balance changes while the end balance (4200) does not.
- A negative intermediate balance can appear or vanish depending on the tie order, which is why overdraft checks must use a defined order.
- RANGE-framed or ORDER BY txn_ts-only: peers share one value (shown in the last column). `ROWS` with only the timestamp in the order is a different trap: the order inside the tie is not defined, so I did not rely on it (not shown).
- Amounts are integer paise, so the sums are exact; floats would drift.
- pandas has no frame default: `cumsum` is always row by row after your sort, so it matches the `ROWS` column; the `RANGE` column needs `transform("last")` over the tied group.

**Then explain:**
- Same idea as Part 5 Q6: a running total needs a total order of rows, and timestamps alone are not one.
- `ROWS` counts physical rows; `RANGE` groups rows with equal ORDER BY values (peers). The standard's default frame when an ORDER BY is present is `RANGE UNBOUNDED PRECEDING` to `CURRENT ROW`, and PostgreSQL behaves the same (not executed here); SQLite showed it in the run.
- State the tie rule as a business rule, not a coincidence of `rowid` order.
- Scoring note (Set T2, Q2 of 5, 20 pts): about 8 pts for the correct deterministic running balance on all 6 rows; 4 pts for showing and explaining what the tie does under the default frame; 4 pts for pandas `cumsum` after a full sort matching (and, for a strong answer, the `transform("last")` for the peer behaviour); 2 pts for naming the tie rule; 2 pts for a check that the last balance per account equals the account total. Partial credit: a correct running sum that orders by timestamp only (right on the seed by luck, undefined on ties).

**Follow-ups:**
- Why does the default frame use RANGE? The standard says so; it is meant to treat equal sort keys as one position, which is surprising for ledgers.
- First moment the balance goes below zero? Filter the running balance (Part 5 Q22).
- What if two engines break ties differently? Then the results differ; only a total order (timestamp, id) is portable.

**Common mistakes:**
- `ORDER BY txn_ts` only, then reporting the same balance for two different transactions.
- Using floats for money.
- In pandas, sorting by timestamp only with an unstable sort and expecting a stable tie order (use a total key).
- Believing `ROWS` fixes ties by itself; it does not define the order inside the tie.

### Q27 ⭐⭐ 🟡 [Set T3, Q3 of 5, 8 min, 20 pts] Cohort retention counts, months 0 to 2 (Part 6 Q10, Q11). wallet_topups(customer_id, topup_date). Cohort = month of first top-up; return cohort_month, month_offset 0 to 2 and distinct customers active. Missing offsets must show 0, and cohorts too young to observe offset 2 must show NULL as of 2025-04-30. Seed 8 customers across Jan and Feb 2025 cohorts. SQL and pandas, asserting equal.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Find each customer's first top-up month, count distinct active customers per (cohort, month offset) from a 0 to 2 offsets list, return 0 where nobody was active, and return NULL where the offset month is not finished by the as-of date.

**Schema and sample data:**
```sql
CREATE TABLE wallet_topups(customer_id INTEGER, topup_date TEXT);
INSERT INTO wallet_topups VALUES
 (1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-12'),
 (2,'2025-01-20'),(2,'2025-03-03'),
 (3,'2025-01-15'),(3,'2025-01-25'),
 (4,'2025-01-31'),(4,'2025-02-01'),
 (5,'2025-01-02'),
 (6,'2025-02-03'),(6,'2025-03-04'),(6,'2025-04-05'),
 (7,'2025-02-14'),(7,'2025-04-20'),
 (8,'2025-02-28');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH t AS (
  SELECT DISTINCT customer_id, substr(topup_date, 1, 7) AS act_month
  FROM wallet_topups WHERE topup_date <= :as_of
),
first AS (
  SELECT customer_id, MIN(act_month) AS cohort_month FROM t GROUP BY customer_id
),
offs(month_offset) AS (VALUES (0), (1), (2)),
cohorts AS (
  SELECT cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY cohort_month
)
SELECT c.cohort_month, o.month_offset,
       CASE WHEN date(c.cohort_month || '-01', '+' || (o.month_offset + 1) || ' months', '-1 day') <= :as_of
            THEN (SELECT COUNT(*) FROM first f JOIN t
                    ON t.customer_id = f.customer_id
                   AND t.act_month = substr(date(f.cohort_month || '-01', '+' || o.month_offset || ' months'), 1, 7)
                  WHERE f.cohort_month = c.cohort_month)
       END AS active
FROM cohorts c CROSS JOIN offs o
ORDER BY c.cohort_month, o.month_offset
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
def pandas_version(raw, as_of):
    as_of = pd.Timestamp(as_of)
    d = raw.assign(m=pd.to_datetime(raw["topup_date"]).dt.to_period("M"))
    d = d[pd.to_datetime(raw["topup_date"]) <= as_of][["customer_id", "m"]].drop_duplicates()
    d["cohort"] = d.groupby("customer_id")["m"].transform("min")
    d["off"] = (d["m"] - d["cohort"]).apply(lambda x: x.n)
    counts = d.groupby(["cohort", "off"])["customer_id"].nunique()
    rows = []
    for c in sorted(d["cohort"].unique()):
        for off in range(3):
            done = (c + off).end_time.normalize() <= as_of
            rows.append((str(c), off, int(counts.get((c, off), 0)) if done else None))
    return pd.DataFrame(rows, columns=["cohort_month", "month_offset", "active"])
```

**Example:** January cohort: customers 1 to 5 (5 people). Active in January (offset 0): all 5. Active in February (offset 1): customers 1 and 4, so 2. Active in March (offset 2): customers 1 and 2, so 2. February cohort: customers 6, 7, 8 (3 people), offset 0 = 3, offset 1 (March) = customer 6 only = 1, offset 2 (April) = customers 6 and 7 = 2. As of 2025-04-30 that is 6 rows with no NULLs. The first run therefore shows the retention table; the second run (as of 2025-03-31) turns February offset 2 into NULL because April is not over; the third run deletes customers 1 and 4 to show a true zero (January offset 1 becomes 0).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q27: cohort retention counts for months 0 to 2, NULL where the offset month is not finished yet.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE wallet_topups(customer_id INTEGER, topup_date TEXT);
INSERT INTO wallet_topups VALUES
 (1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-12'),
 (2,'2025-01-20'),(2,'2025-03-03'),
 (3,'2025-01-15'),(3,'2025-01-25'),
 (4,'2025-01-31'),(4,'2025-02-01'),
 (5,'2025-01-02'),
 (6,'2025-02-03'),(6,'2025-03-04'),(6,'2025-04-05'),
 (7,'2025-02-14'),(7,'2025-04-20'),
 (8,'2025-02-28');
"""
SQL = """
WITH t AS (
  SELECT DISTINCT customer_id, substr(topup_date, 1, 7) AS act_month
  FROM wallet_topups WHERE topup_date <= :as_of
),
first AS (
  SELECT customer_id, MIN(act_month) AS cohort_month FROM t GROUP BY customer_id
),
offs(month_offset) AS (VALUES (0), (1), (2)),
cohorts AS (
  SELECT cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY cohort_month
)
SELECT c.cohort_month, o.month_offset,
       CASE WHEN date(c.cohort_month || '-01', '+' || (o.month_offset + 1) || ' months', '-1 day') <= :as_of
            THEN (SELECT COUNT(*) FROM first f JOIN t
                    ON t.customer_id = f.customer_id
                   AND t.act_month = substr(date(f.cohort_month || '-01', '+' || o.month_offset || ' months'), 1, 7)
                  WHERE f.cohort_month = c.cohort_month)
       END AS active
FROM cohorts c CROSS JOIN offs o
ORDER BY c.cohort_month, o.month_offset
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
raw = pd.read_sql("SELECT * FROM wallet_topups", con)

# PANDAS START
def pandas_version(raw, as_of):
    as_of = pd.Timestamp(as_of)
    d = raw.assign(m=pd.to_datetime(raw["topup_date"]).dt.to_period("M"))
    d = d[pd.to_datetime(raw["topup_date"]) <= as_of][["customer_id", "m"]].drop_duplicates()
    d["cohort"] = d.groupby("customer_id")["m"].transform("min")
    d["off"] = (d["m"] - d["cohort"]).apply(lambda x: x.n)
    counts = d.groupby(["cohort", "off"])["customer_id"].nunique()
    rows = []
    for c in sorted(d["cohort"].unique()):
        for off in range(3):
            done = (c + off).end_time.normalize() <= as_of
            rows.append((str(c), off, int(counts.get((c, off), 0)) if done else None))
    return pd.DataFrame(rows, columns=["cohort_month", "month_offset", "active"])
# PANDAS END

def run(as_of, raw):
    s = pd.read_sql(SQL, con, params={"as_of": as_of})
    p = pandas_version(raw, as_of)
    s["active"] = s["active"].astype("Float64"); p["active"] = p["active"].astype("Float64")
    print(s.to_string(index=False))
    pd.testing.assert_frame_equal(s, p, check_dtype=False)
    print("asserts passed (ordered by cohort_month, month_offset)\n")

print("as of 2025-04-30 (both cohorts fully observable)")
run("2025-04-30", raw)
print("as of 2025-03-31 (February cohort is too young for offset 2)")
run("2025-03-31", raw)
con.execute("DELETE FROM wallet_topups WHERE customer_id IN (1, 4)")
raw2 = pd.read_sql("SELECT * FROM wallet_topups", con)
print("as of 2025-04-30 after deleting customers 1 and 4 (nobody active in February from the January cohort)")
run("2025-04-30", raw2)
```

**Output (my run):**
```text
as of 2025-04-30 (both cohorts fully observable)
cohort_month  month_offset  active
     2025-01             0     5.0
     2025-01             1     2.0
     2025-01             2     2.0
     2025-02             0     3.0
     2025-02             1     1.0
     2025-02             2     2.0
asserts passed (ordered by cohort_month, month_offset)

as of 2025-03-31 (February cohort is too young for offset 2)
cohort_month  month_offset  active
     2025-01             0     5.0
     2025-01             1     2.0
     2025-01             2     2.0
     2025-02             0     3.0
     2025-02             1     1.0
     2025-02             2    <NA>
asserts passed (ordered by cohort_month, month_offset)

as of 2025-04-30 after deleting customers 1 and 4 (nobody active in February from the January cohort)
cohort_month  month_offset  active
     2025-01             0     3.0
     2025-01             1     0.0
     2025-01             2     1.0
     2025-02             0     3.0
     2025-02             1     1.0
     2025-02             2     2.0
asserts passed (ordered by cohort_month, month_offset)
```

**Edge cases:**
- Premise check: the question asks for NULL for cohorts too young as of 2025-04-30, but with only January and February cohorts and offsets 0 to 2, every offset month (the latest is April, which ends on 04-30) is already finished, so no NULL appears. I show the NULL rule with an earlier as-of date (2025-03-31) where February offset 2 is NULL. With a March cohort in the data, March offset 2 (May) would be NULL on 2025-04-30.
- Zero versus NULL: zero means observed and nobody came back (third run: January offset 1 is 0); NULL means not observable yet. Mixing them makes young cohorts look like churn.
- Observable rule used: the offset month is complete when its last day is on or before the as-of date, written `date(cohort || '-01', '+k months', '-1 day') <= :as_of` (so a mid-month as-of date makes that month NULL).
- Duplicates: a customer topping up three times in a month counts once (`DISTINCT` over customer and month); customer 3 has two January rows.
- Data after the as-of date is ignored (customer 6's April top-up is excluded in the March run).
- pandas returns `None` for the unobservable cells; the comparison uses the nullable Float64 type so NaN equals NULL.

**Then explain:**
- Three small tables: first month per customer (cohort), distinct customer-months (activity), and the offsets list (0, 1, 2). The result is cohort times offset, not only the offsets that happen to have data.
- Month offset is calendar months between first top-up month and activity month (Part 6 Q10); in pandas a `Period` subtraction gives it.
- The `VALUES` common table expression for offsets is standard in SQLite (`WITH offs(month_offset) AS (VALUES (0), (1), (2))`).
- Scoring note (Set T3, Q3 of 5, 20 pts): about 8 pts for the correct counts (5, 2, 2 and 3, 1, 2); 4 pts for the zero versus NULL distinction and the observable-month rule; 4 pts for the pandas version matching on all scenarios; 2 pts for saying what a month offset means and that active means at least one top-up; 2 pts for a check (offset 0 equals cohort size). Partial credit: counts without NULL handling, or offsets that exist only where there is data.

**Follow-ups:**
- Retention percent? Divide by the offset 0 count; keep NULL for unobserved cells (Part 6 Q11).
- Month offset when the cohort is defined by signup, not first top-up? Same shape, different source of the cohort month.
- Why not `DATEDIFF` in months? SQLite has none; Postgres `age` or `DATE_DIFF` variants exist (not executed here).

**Common mistakes:**
- Returning no row for an offset nobody reached, which hides a zero.
- Treating a young cohort's missing future as 0 retention.
- Counting rows instead of distinct customers.
- Off-by-one on the offset (month 1 is the month after the first top-up, not the same month).

### Q28 ⭐⭐ 🟡 [Set T3, Q2 of 5, 8 min, 20 pts] Chargeback rate by merchant category without fan-out (Part 8 Q10, Q11). merchants(merchant_id, category), card_payments(payment_id, merchant_id, amount), chargebacks(chargeback_id, payment_id, amount) with one payment having two chargeback rows. Return per category the payment count, the number of payments with any chargeback, the rate and the chargeback amount. Show the naive join count and then the correct one. SQL and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Pre-aggregate the chargebacks to one row per payment before joining, then count payments with `COUNT(*)` and payments with a chargeback with `COUNT(cb.payment_id)`; joining the raw chargebacks repeats the payment and inflates its counts.

**Schema and sample data:**
```sql
CREATE TABLE merchants(merchant_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE card_payments(payment_id INTEGER PRIMARY KEY, merchant_id INTEGER, amount INTEGER);
CREATE TABLE chargebacks(chargeback_id INTEGER PRIMARY KEY, payment_id INTEGER, amount INTEGER);
INSERT INTO merchants VALUES (1,'travel'),(2,'travel'),(3,'grocery'),(4,'gaming');
INSERT INTO card_payments VALUES
 (1,1,1000),(2,1,2000),(3,2,500),(4,2,700),(5,3,300),(6,3,400),(7,3,350),(8,3,250),(9,4,900);
INSERT INTO chargebacks VALUES (1,1,600),(2,1,400),(3,3,500),(4,5,300);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
Naive version (shows the fan-out):
```sql
SELECT m.category, COUNT(*) AS payments, SUM(c.amount) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN chargebacks c ON c.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
```
```sql
WITH cb AS (
  SELECT payment_id, SUM(amount) AS cb_amount
  FROM chargebacks
  GROUP BY payment_id
)
SELECT m.category,
       COUNT(*) AS payments,
       COUNT(cb.payment_id) AS payments_with_cb,
       ROUND(1.0 * COUNT(cb.payment_id) / COUNT(*), 4) AS cb_rate,
       COALESCE(SUM(cb.cb_amount), 0) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN cb ON cb.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
cb = cbs.groupby("payment_id", as_index=False)["amount"].sum().rename(columns={"amount": "cb_amount"})
d = pay.merge(mer, on="merchant_id").merge(cb, on="payment_id", how="left")
p = (d.groupby("category")
       .agg(payments=("payment_id", "size"),
            payments_with_cb=("cb_amount", "count"),
            chargeback_amount=("cb_amount", "sum"))
       .reset_index())
p["cb_rate"] = (p["payments_with_cb"] / p["payments"]).round(4)
p = p[["category", "payments", "payments_with_cb", "cb_rate", "chargeback_amount"]].sort_values("category").reset_index(drop=True)
```

**Example:** Payment 1 has two chargebacks (600 and 400). Naive join payment-to-chargeback: travel shows 5 payments instead of 4 because payment 1 appears twice. Pre-aggregated: travel has payments 1 to 4 (merchants 1 and 2), payments 1 and 3 have chargebacks, so 2 of 4 = 0.5 and the chargeback amount is 1000 + 500 = 1500. Grocery has payments 5 to 8, only payment 5 has a chargeback (300), so 1 of 4 = 0.25. Gaming has payment 9 with none: 0 of 1 = 0.00 and an amount of 0 (not NULL).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q28: chargeback rate by merchant category without fan-out.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE merchants(merchant_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE card_payments(payment_id INTEGER PRIMARY KEY, merchant_id INTEGER, amount INTEGER);
CREATE TABLE chargebacks(chargeback_id INTEGER PRIMARY KEY, payment_id INTEGER, amount INTEGER);
INSERT INTO merchants VALUES (1,'travel'),(2,'travel'),(3,'grocery'),(4,'gaming');
INSERT INTO card_payments VALUES
 (1,1,1000),(2,1,2000),(3,2,500),(4,2,700),(5,3,300),(6,3,400),(7,3,350),(8,3,250),(9,4,900);
INSERT INTO chargebacks VALUES (1,1,600),(2,1,400),(3,3,500),(4,5,300);
"""
SQL_NAIVE = """
SELECT m.category, COUNT(*) AS payments, SUM(c.amount) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN chargebacks c ON c.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
"""
SQL = """
WITH cb AS (
  SELECT payment_id, SUM(amount) AS cb_amount
  FROM chargebacks
  GROUP BY payment_id
)
SELECT m.category,
       COUNT(*) AS payments,
       COUNT(cb.payment_id) AS payments_with_cb,
       ROUND(1.0 * COUNT(cb.payment_id) / COUNT(*), 4) AS cb_rate,
       COALESCE(SUM(cb.cb_amount), 0) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN cb ON cb.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
naive = pd.read_sql(SQL_NAIVE, con)
print("naive join (payment 1 has two chargebacks):")
print(naive.to_string(index=False))
s = pd.read_sql(SQL, con)
print("\npre-aggregated:")
print(s.to_string(index=False))

pay = pd.read_sql("SELECT * FROM card_payments", con)
mer = pd.read_sql("SELECT * FROM merchants", con)
cbs = pd.read_sql("SELECT * FROM chargebacks", con)
# PANDAS START
cb = cbs.groupby("payment_id", as_index=False)["amount"].sum().rename(columns={"amount": "cb_amount"})
d = pay.merge(mer, on="merchant_id").merge(cb, on="payment_id", how="left")
p = (d.groupby("category")
       .agg(payments=("payment_id", "size"),
            payments_with_cb=("cb_amount", "count"),
            chargeback_amount=("cb_amount", "sum"))
       .reset_index())
p["cb_rate"] = (p["payments_with_cb"] / p["payments"]).round(4)
p = p[["category", "payments", "payments_with_cb", "cb_rate", "chargeback_amount"]].sort_values("category").reset_index(drop=True)
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by category)")

nv = pay.merge(mer, on="merchant_id").merge(cbs, on="payment_id", how="left")
print("pandas naive merge rows:", len(nv), "vs payments:", len(pay))
```

**Output (my run):**
```text
naive join (payment 1 has two chargebacks):
category  payments  chargeback_amount
  gaming         1                NaN
 grocery         4              300.0
  travel         5             1500.0

pre-aggregated:
category  payments  payments_with_cb  cb_rate  chargeback_amount
  gaming         1                 0     0.00                  0
 grocery         4                 1     0.25                300
  travel         4                 2     0.50               1500

category  payments  payments_with_cb  cb_rate  chargeback_amount
  gaming         1                 0     0.00                0.0
 grocery         4                 1     0.25              300.0
  travel         4                 2     0.50             1500.0

asserts passed (ordered by category)
pandas naive merge rows: 10 vs payments: 9
```

**Edge cases:**
- Fan-out: the naive query reports 5 travel payments (the run) and the pandas naive merge gives 10 rows for 9 payments. The chargeback sum itself (1500) survives in this seed because each chargeback row is counted once, but any payment-side measure would be double counted.
- Categories with no chargeback: NULL in the naive output (gaming), 0 after `COALESCE` in SQL; in pandas `sum` of an all-NaN group is 0.0, so the column is float (0.0 versus integer 0 in SQL, compared with `check_dtype=False`).
- A payment with two chargebacks counts once in `payments_with_cb`; if the business wants chargeback events, count chargeback rows instead and say so.
- A merchant with no payments would not appear (join from payments); start from merchants if empty categories must show.

**Then explain:**
- This is Part 8 Q10: aggregate the many side to the grain of the one side before the join, so the join is one-to-one.
- `COUNT(cb.payment_id)` counts non-NULL, so payments without chargebacks are not counted.
- pandas: `groupby("payment_id").sum()` then a left merge, then named aggregation (`count` skips NaN, `size` does not).
- Scoring note (Set T3, Q2 of 5, 20 pts): about 8 pts for the correct pre-aggregated table (4, 2, 0.5, 1500 for travel); 4 pts for demonstrating the naive count (5) and explaining the fan-out; 4 pts for pandas matching; 2 pts for stating payments versus chargeback events as the unit; 2 pts for a check that the payment counts add up to 9. Partial credit: `COUNT(DISTINCT payment_id)` on the naive join gets the counts right but still double counts any payment amount.

**Follow-ups:**
- Chargeback amount as a percent of payment volume? Sum payment amounts on the payment side first, then divide; never `SUM(p.amount)` after the fan-out join.
- `COUNT(DISTINCT)` fix? Works for counts, not for sums; pre-aggregation fixes both.
- Time lag between payment and chargeback? Bucket by months since payment, a cohort-style cut (Part 6).

**Common mistakes:**
- `COUNT(*)` after a one-to-many join.
- `SUM(payment.amount)` after the join, which counts payment 1's amount twice.
- Inner joining chargebacks and losing categories with no chargebacks.
- Reporting NULL instead of 0 for the chargeback amount.

### Q29 ⭐⭐ 🟡 [Set E1, Q3 of 5, 8 min, 20 pts] Repeat purchase and days to second order (Part 6 Q20, Part 8 Q21). orders(order_id, customer_id, order_date, status). Exclude CANCELLED orders. Return the share of customers with 2 or more orders and the average days between first and second order among them. Seed 8 customers including one whose first order was cancelled and a same-day second order. SQL and pandas, and state the denominator.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Drop CANCELLED orders first, number each customer's remaining orders by date, take the first and second dates per customer, and divide customers with a second order by customers with at least one non-cancelled order; the average gap uses only those repeaters.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2025-01-01','DELIVERED'),(2,1,'2025-01-31','DELIVERED'),
 (3,2,'2025-01-05','DELIVERED'),(4,2,'2025-01-05','DELIVERED'),
 (5,3,'2025-01-01','CANCELLED'),(6,3,'2025-01-10','DELIVERED'),(7,3,'2025-01-20','DELIVERED'),
 (8,4,'2025-02-01','DELIVERED'),
 (9,5,'2025-02-10','DELIVERED'),
 (10,6,'2025-03-01','DELIVERED'),(11,6,'2025-03-05','CANCELLED'),
 (12,7,'2025-01-15','DELIVERED'),(13,7,'2025-02-14','DELIVERED'),(14,7,'2025-03-16','DELIVERED'),
 (15,8,'2025-02-20','CANCELLED');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH ok AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
  WHERE status <> 'CANCELLED'
),
per AS (
  SELECT customer_id,
         MAX(CASE WHEN rn = 1 THEN order_date END) AS first_date,
         MAX(CASE WHEN rn = 2 THEN order_date END) AS second_date
  FROM ok
  GROUP BY customer_id
)
SELECT COUNT(*) AS customers,
       COUNT(second_date) AS repeaters,
       ROUND(1.0 * COUNT(second_date) / COUNT(*), 4) AS repeat_share,
       AVG(julianday(second_date) - julianday(first_date)) AS avg_days_to_second
FROM per
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
ok = o[o["status"] != "CANCELLED"].copy()
ok["order_date"] = pd.to_datetime(ok["order_date"])
ok = ok.sort_values(["customer_id", "order_date", "order_id"])
ok["rn"] = ok.groupby("customer_id").cumcount() + 1
first = ok[ok["rn"] == 1].set_index("customer_id")["order_date"]
second = ok[ok["rn"] == 2].set_index("customer_id")["order_date"]
days = (second - first.reindex(second.index)).dt.days
p = pd.DataFrame({"customers": [len(first)], "repeaters": [len(second)],
                  "repeat_share": [round(len(second) / len(first), 4)],
                  "avg_days_to_second": [days.mean()]})
```

**Example:** After dropping cancelled orders: customer 1 has 01-01 and 01-31 (30 days), customer 2 has two orders on 01-05 (0 days), customer 3 loses the cancelled 01-01 order and has 01-10 and 01-20 (10 days), customers 4 and 5 have one order each, customer 6 keeps only 03-01 (the second order was cancelled), customer 7 has 01-15, 02-14, 03-16 (first to second 30 days), customer 8 had only a cancelled order so disappears. That leaves 7 customers, 4 repeaters (1, 2, 3, 7), share 4/7 = 0.5714 and average (30 + 0 + 10 + 30) / 4 = 17.5 days.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q29: repeat purchase share and days from first to second order, cancelled orders excluded.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2025-01-01','DELIVERED'),(2,1,'2025-01-31','DELIVERED'),
 (3,2,'2025-01-05','DELIVERED'),(4,2,'2025-01-05','DELIVERED'),
 (5,3,'2025-01-01','CANCELLED'),(6,3,'2025-01-10','DELIVERED'),(7,3,'2025-01-20','DELIVERED'),
 (8,4,'2025-02-01','DELIVERED'),
 (9,5,'2025-02-10','DELIVERED'),
 (10,6,'2025-03-01','DELIVERED'),(11,6,'2025-03-05','CANCELLED'),
 (12,7,'2025-01-15','DELIVERED'),(13,7,'2025-02-14','DELIVERED'),(14,7,'2025-03-16','DELIVERED'),
 (15,8,'2025-02-20','CANCELLED');
"""
SQL = """
WITH ok AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
  WHERE status <> 'CANCELLED'
),
per AS (
  SELECT customer_id,
         MAX(CASE WHEN rn = 1 THEN order_date END) AS first_date,
         MAX(CASE WHEN rn = 2 THEN order_date END) AS second_date
  FROM ok
  GROUP BY customer_id
)
SELECT COUNT(*) AS customers,
       COUNT(second_date) AS repeaters,
       ROUND(1.0 * COUNT(second_date) / COUNT(*), 4) AS repeat_share,
       AVG(julianday(second_date) - julianday(first_date)) AS avg_days_to_second
FROM per
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

o = pd.read_sql("SELECT * FROM orders", con)
# PANDAS START
ok = o[o["status"] != "CANCELLED"].copy()
ok["order_date"] = pd.to_datetime(ok["order_date"])
ok = ok.sort_values(["customer_id", "order_date", "order_id"])
ok["rn"] = ok.groupby("customer_id").cumcount() + 1
first = ok[ok["rn"] == 1].set_index("customer_id")["order_date"]
second = ok[ok["rn"] == 2].set_index("customer_id")["order_date"]
days = (second - first.reindex(second.index)).dt.days
p = pd.DataFrame({"customers": [len(first)], "repeaters": [len(second)],
                  "repeat_share": [round(len(second) / len(first), 4)],
                  "avg_days_to_second": [days.mean()]})
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (single row)")
print("per-customer days to second order:", days.sort_index().to_dict())
print("customers with any order (incl. cancelled-only):", o["customer_id"].nunique(),
      "-> share on that denominator:", round(len(second) / o["customer_id"].nunique(), 4))
```

**Output (my run):**
```text
 customers  repeaters  repeat_share  avg_days_to_second
         7          4        0.5714                17.5

 customers  repeaters  repeat_share  avg_days_to_second
         7          4        0.5714                17.5

asserts passed (single row)
per-customer days to second order: {1: 30, 2: 0, 3: 10, 7: 30}
customers with any order (incl. cancelled-only): 8 -> share on that denominator: 0.5
```

**Edge cases:**
- Denominator: customers with at least one non-cancelled order (7). Using all customers in the table (8, including the cancelled-only customer 8) gives 0.5, as the run prints. Say which one, since both are defensible.
- First order cancelled: customer 3 is a repeater measured from the first surviving order, not from the cancelled one.
- Same-day second order: customer 2 gives 0 days and still counts as a repeater; `order_id` breaks the tie between the two same-day orders.
- AVG over days ignores NULL (non-repeaters) in SQL and NaN in pandas; do not fill them with 0.
- A customer with orders on two dates but one cancelled is a single-order customer (customer 6).

**Then explain:**
- Part 6 Q20 and Part 8 Q21 are the model: first and second order per customer through `ROW_NUMBER` and conditional `MAX`.
- Filter before numbering; otherwise a cancelled order takes position 1 or 2.
- pandas: filter, sort, `groupby.cumcount()`, pick positions 1 and 2, subtract dates.
- Scoring note (Set E1, Q3 of 5, 20 pts): about 8 pts for 7 customers, 4 repeaters, 0.5714 and 17.5; 4 pts for the cancelled-first and same-day cases handled and the denominator named; 4 pts for pandas matching; 2 pts for stating the denominator out loud; 2 pts for a check (repeaters at most customers). Partial credit: right repeat share but days measured from the cancelled order.

**Follow-ups:**
- Repeat within 30 days only? Add `days <= 30` to the numerator; the denominator question gets sharper because young customers cannot have repeated yet (Part 6).
- Median days instead of average? SQLite has no median function; use a `ROW_NUMBER` or percentile in pandas (not run here).
- Repeat rate by acquisition month? Group the same table by the first-order month.

**Common mistakes:**
- Counting cancelled orders toward the order count.
- Dividing by all customers when the cancelled-only customer never really bought.
- Counting two same-day orders as one visit without saying so.
- Averaging days over non-repeaters as 0.

### Q30 ⭐⭐ 🟡 [Set E1, Q2 of 5, 8 min, 20 pts] GMV, AOV and cancelled share (Part 8 Q4). orders(order_id, customer_id, order_date, status, amount) with statuses DELIVERED, CANCELLED, RETURNED. Report per month GMV (all orders), net revenue (DELIVERED only), AOV on net orders and the cancelled share by count. Seed 10 orders over 2 months. SQL with conditional aggregation and pandas with named aggregations; say which denominator each metric uses.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Group by month with conditional aggregation: GMV is the sum over all orders, net revenue the sum over DELIVERED only, AOV is net revenue divided by delivered orders, and the cancelled share is cancelled orders divided by all orders.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2025-01-03','DELIVERED',100),(2,2,'2025-01-09','DELIVERED',200),
 (3,3,'2025-01-15','CANCELLED',150),(4,1,'2025-01-20','RETURNED',120),
 (5,4,'2025-01-28','DELIVERED',300),
 (6,2,'2025-02-02','DELIVERED',250),(7,5,'2025-02-06','CANCELLED',80),
 (8,6,'2025-02-11','CANCELLED',90),(9,3,'2025-02-19','DELIVERED',100),
 (10,1,'2025-02-25','RETURNED',60);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
SELECT substr(order_date, 1, 7) AS month,
       COUNT(*) AS orders,
       SUM(amount) AS gmv,
       SUM(CASE WHEN status = 'DELIVERED' THEN amount ELSE 0 END) AS net_revenue,
       ROUND(1.0 * SUM(CASE WHEN status = 'DELIVERED' THEN amount END)
             / NULLIF(COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END), 0), 2) AS aov_net,
       ROUND(1.0 * COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) / COUNT(*), 4) AS cancelled_share
FROM orders
GROUP BY substr(order_date, 1, 7)
ORDER BY month
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
d = o.assign(month=o["order_date"].str[:7],
             delivered=o["status"].eq("DELIVERED"),
             cancelled=o["status"].eq("CANCELLED"))
d["net_amount"] = d["amount"].where(d["delivered"], 0)
p = (d.groupby("month")
       .agg(orders=("order_id", "size"), gmv=("amount", "sum"),
            net_revenue=("net_amount", "sum"),
            n_delivered=("delivered", "sum"), n_cancelled=("cancelled", "sum"))
       .reset_index())
p["aov_net"] = (p["net_revenue"] / p["n_delivered"].where(p["n_delivered"] != 0)).round(2)
p["cancelled_share"] = (p["n_cancelled"] / p["orders"]).round(4)
p = p[["month", "orders", "gmv", "net_revenue", "aov_net", "cancelled_share"]]
```

**Example:** January: 5 orders, 100 + 200 + 150 + 120 + 300 = 870 GMV. Delivered amounts are 100, 200, 300 so net revenue 600 over 3 delivered orders, AOV 200.00. One of 5 orders was cancelled: 0.2. February: 5 orders and 250 + 80 + 90 + 100 + 60 = 580 GMV, delivered 250 and 100 give net 350 over 2 orders, AOV 175.00, 2 of 5 cancelled = 0.4. The RETURNED orders are inside GMV but outside net revenue.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q30: GMV, net revenue, AOV and cancelled share per month.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2025-01-03','DELIVERED',100),(2,2,'2025-01-09','DELIVERED',200),
 (3,3,'2025-01-15','CANCELLED',150),(4,1,'2025-01-20','RETURNED',120),
 (5,4,'2025-01-28','DELIVERED',300),
 (6,2,'2025-02-02','DELIVERED',250),(7,5,'2025-02-06','CANCELLED',80),
 (8,6,'2025-02-11','CANCELLED',90),(9,3,'2025-02-19','DELIVERED',100),
 (10,1,'2025-02-25','RETURNED',60);
"""
SQL = """
SELECT substr(order_date, 1, 7) AS month,
       COUNT(*) AS orders,
       SUM(amount) AS gmv,
       SUM(CASE WHEN status = 'DELIVERED' THEN amount ELSE 0 END) AS net_revenue,
       ROUND(1.0 * SUM(CASE WHEN status = 'DELIVERED' THEN amount END)
             / NULLIF(COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END), 0), 2) AS aov_net,
       ROUND(1.0 * COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) / COUNT(*), 4) AS cancelled_share
FROM orders
GROUP BY substr(order_date, 1, 7)
ORDER BY month
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

o = pd.read_sql("SELECT * FROM orders", con)
# PANDAS START
d = o.assign(month=o["order_date"].str[:7],
             delivered=o["status"].eq("DELIVERED"),
             cancelled=o["status"].eq("CANCELLED"))
d["net_amount"] = d["amount"].where(d["delivered"], 0)
p = (d.groupby("month")
       .agg(orders=("order_id", "size"), gmv=("amount", "sum"),
            net_revenue=("net_amount", "sum"),
            n_delivered=("delivered", "sum"), n_cancelled=("cancelled", "sum"))
       .reset_index())
p["aov_net"] = (p["net_revenue"] / p["n_delivered"].where(p["n_delivered"] != 0)).round(2)
p["cancelled_share"] = (p["n_cancelled"] / p["orders"]).round(4)
p = p[["month", "orders", "gmv", "net_revenue", "aov_net", "cancelled_share"]]
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by month)")
print("AOV if you divide by ALL orders instead of delivered:",
      (p["net_revenue"] / p["orders"]).round(2).tolist())
```

**Output (my run):**
```text
  month  orders  gmv  net_revenue  aov_net  cancelled_share
2025-01       5  870          600    200.0              0.2
2025-02       5  580          350    175.0              0.4

  month  orders  gmv  net_revenue  aov_net  cancelled_share
2025-01       5  870          600    200.0              0.2
2025-02       5  580          350    175.0              0.4

asserts passed (ordered by month)
AOV if you divide by ALL orders instead of delivered: [120.0, 70.0]
```

**Edge cases:**
- Denominators differ by metric: GMV and the cancelled share use all orders (5 each month), AOV uses delivered orders (3 and 2). Dividing net revenue by all orders gives 120.00 and 70.00 instead, which is the common mistake (the run prints it).
- A month with no delivered orders: `NULLIF(..., 0)` makes AOV NULL (pandas masks the zero to NaN); it would be a 0 divided by 0 otherwise. Not in the seed.
- GMV definition varies by company (some exclude cancelled orders); here it is all orders as the question states, and RETURNED is kept in it.
- `SUM(CASE ... END)` with no ELSE is NULL when no row matches; I used `ELSE 0` for net revenue so it prints 0.
- Rounding: AOV is rounded to 2 decimals and the share to 4; the seed values are exact, so SQLite and pandas rounding agree.

**Then explain:**
- One scan with conditional aggregation (Part 8 Q4): `SUM(CASE WHEN status = ... THEN amount END)` and `COUNT(CASE WHEN ... THEN 1 END)`. PostgreSQL, SQLite 3.30 and later and others also have `FILTER (WHERE ...)` (I did not use it here; not executed).
- pandas named aggregation cannot take a condition, so add helper columns (`delivered`, `cancelled`, `net_amount`) first; booleans sum to counts.
- Say the denominator for each metric before coding, then the definitions are visible to the interviewer.
- Scoring note (Set E1, Q2 of 5, 20 pts): about 8 pts for the 2 correct rows (870, 600, 200.00, 0.2 and 580, 350, 175.00, 0.4); 4 pts for the right denominators and the NULL guard on AOV; 4 pts for pandas named aggregation matching; 2 pts for stating the GMV and net definitions; 2 pts for a check that GMV equals the sum of all amounts (1450). Partial credit: one scan with the right numerators but a single denominator for all metrics.

**Follow-ups:**
- AOV on all orders, or per customer? Different metrics; ask which the team uses.
- Return rate? RETURNED count over DELIVERED plus RETURNED, a definition to state first (Part 8).
- Month-over-month change in these metrics? Add a `LAG` over the monthly table as in Q21.

**Common mistakes:**
- Using `COUNT(*)` as the AOV denominator.
- Putting the status filter in `WHERE`, which also changes GMV and the cancelled share.
- Integer division for the share (the `1.0 *` avoids it).
- Silently excluding returned orders from GMV without saying so.

### Q31 ⭐⭐ 🟡 [Set E2, Q3 of 5, 8 min, 20 pts] Valid coupon on the order date (Part 6 Q39). coupons(code, start_date, end_date, pct_off) and orders(order_id, order_date, coupon_code, amount). Return each order with the coupon status VALID, EXPIRED, NOT_STARTED, UNKNOWN_CODE or NO_COUPON, and the discounted amount for valid ones. Seed 7 orders on the start and end dates (inclusive). SQL with a LEFT JOIN condition in ON, not WHERE (Part 2 Q3), and pandas.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Join on the coupon code only (in ON), keep every order, then decide the status with a CASE that compares the order date to the coupon window with inclusive ends; the date test never goes in WHERE.

**Schema and sample data:**
```sql
CREATE TABLE coupons(code TEXT PRIMARY KEY, start_date TEXT, end_date TEXT, pct_off INTEGER);
CREATE TABLE orders(order_id INTEGER, order_date TEXT, coupon_code TEXT, amount INTEGER);
INSERT INTO coupons VALUES ('SAVE10', '2025-03-01', '2025-03-31', 10), ('FLASH', '2025-03-10', '2025-03-12', 25);
INSERT INTO orders VALUES
 (1, '2025-03-01', 'SAVE10', 100),
 (2, '2025-03-31', 'SAVE10', 200),
 (3, '2025-02-28', 'SAVE10', 150),
 (4, '2025-04-01', 'SAVE10', 120),
 (5, '2025-03-12', 'FLASH',   80),
 (6, '2025-03-05', 'BOGUS',   90),
 (7, '2025-03-05', NULL,      60);
```
Orders 1 and 2 sit exactly on the start and end date of SAVE10, order 5 is on the last day of FLASH, order 3 is one day before the window and order 4 one day after.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT o.order_id, o.order_date, o.coupon_code,
       CASE WHEN o.coupon_code IS NULL THEN 'NO_COUPON'
            WHEN c.code IS NULL THEN 'UNKNOWN_CODE'
            WHEN o.order_date < c.start_date THEN 'NOT_STARTED'
            WHEN o.order_date > c.end_date THEN 'EXPIRED'
            ELSE 'VALID' END AS status,
       CASE WHEN o.order_date BETWEEN c.start_date AND c.end_date
            THEN ROUND(o.amount * (100 - c.pct_off) / 100.0, 2) END AS discounted
FROM orders o
LEFT JOIN coupons c ON c.code = o.coupon_code
ORDER BY o.order_id
```
The code match is the only join condition, so an order with a bad or missing code keeps its row and `c.code` is NULL. The date test is in the CASE (and inside the discount expression), not in WHERE. `BETWEEN` is inclusive on both ends, which is what makes the start and end dates VALID. ISO date text compares correctly as text; in a real schema the columns are DATE.

**pandas answer:** the same text as the pandas part of the Code block.
```py
orders = pd.read_sql("SELECT * FROM orders", con)
coupons = pd.read_sql("SELECT * FROM coupons", con)
m = orders.merge(coupons, how="left", left_on="coupon_code", right_on="code")
od, sd, ed = (pd.to_datetime(m[c]) for c in ("order_date", "start_date", "end_date"))
m["status"] = np.select(
    [m.coupon_code.isna(), m.code.isna(), od < sd, od > ed],
    ["NO_COUPON", "UNKNOWN_CODE", "NOT_STARTED", "EXPIRED"], default="VALID")
m["discounted"] = (m.amount * (100 - m.pct_off) / 100).where(m.status == "VALID").round(2)
want = m[["order_id", "order_date", "coupon_code", "status", "discounted"]]
```

**Example:** Order 1 is on 2025-03-01: the join finds SAVE10, `order_date < start_date` is false and `order_date > end_date` is false, so VALID, and 100 * (100 - 10) / 100.0 = 90. Order 2 on 2025-03-31 is the end date, not after it, so VALID, 180. Order 3 (02-28) is before the start: NOT_STARTED. Order 4 (04-01) is after the end: EXPIRED. Order 5 (FLASH, 03-12) is VALID, 80 * 0.75 = 60. Order 6's code BOGUS finds no coupon row: UNKNOWN_CODE. Order 7 has a NULL code: NO_COUPON, which must be tested first because the join then also has no coupon row.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q31: coupon status on the order date (LEFT JOIN with the code match in ON), discounted amount for valid ones.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE coupons(code TEXT PRIMARY KEY, start_date TEXT, end_date TEXT, pct_off INTEGER);
CREATE TABLE orders(order_id INTEGER, order_date TEXT, coupon_code TEXT, amount INTEGER);
INSERT INTO coupons VALUES ('SAVE10', '2025-03-01', '2025-03-31', 10), ('FLASH', '2025-03-10', '2025-03-12', 25);
INSERT INTO orders VALUES
 (1, '2025-03-01', 'SAVE10', 100),
 (2, '2025-03-31', 'SAVE10', 200),
 (3, '2025-02-28', 'SAVE10', 150),
 (4, '2025-04-01', 'SAVE10', 120),
 (5, '2025-03-12', 'FLASH',   80),
 (6, '2025-03-05', 'BOGUS',   90),
 (7, '2025-03-05', NULL,      60);
""")

sql_answer = """
SELECT o.order_id, o.order_date, o.coupon_code,
       CASE WHEN o.coupon_code IS NULL THEN 'NO_COUPON'
            WHEN c.code IS NULL THEN 'UNKNOWN_CODE'
            WHEN o.order_date < c.start_date THEN 'NOT_STARTED'
            WHEN o.order_date > c.end_date THEN 'EXPIRED'
            ELSE 'VALID' END AS status,
       CASE WHEN o.order_date BETWEEN c.start_date AND c.end_date
            THEN ROUND(o.amount * (100 - c.pct_off) / 100.0, 2) END AS discounted
FROM orders o
LEFT JOIN coupons c ON c.code = o.coupon_code
ORDER BY o.order_id
"""
# the two wrong versions, to show what they lose
sql_where = """
SELECT COUNT(*) FROM orders o LEFT JOIN coupons c ON c.code = o.coupon_code
WHERE o.order_date BETWEEN c.start_date AND c.end_date
"""
sql_date_in_on = """
SELECT o.order_id, c.code IS NOT NULL AS matched
FROM orders o LEFT JOIN coupons c
  ON c.code = o.coupon_code AND o.order_date BETWEEN c.start_date AND c.end_date
ORDER BY o.order_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nwith the date test in WHERE, rows left:", con.execute(sql_where).fetchone()[0], "of 7")
print("date test in ON, code match flag (cannot tell EXPIRED from UNKNOWN_CODE):",
      pd.read_sql(sql_date_in_on, con).matched.tolist())

# --- pandas
orders = pd.read_sql("SELECT * FROM orders", con)
coupons = pd.read_sql("SELECT * FROM coupons", con)
m = orders.merge(coupons, how="left", left_on="coupon_code", right_on="code")
od, sd, ed = (pd.to_datetime(m[c]) for c in ("order_date", "start_date", "end_date"))
m["status"] = np.select(
    [m.coupon_code.isna(), m.code.isna(), od < sd, od > ed],
    ["NO_COUPON", "UNKNOWN_CODE", "NOT_STARTED", "EXPIRED"], default="VALID")
m["discounted"] = (m.amount * (100 - m.pct_off) / 100).where(m.status == "VALID").round(2)
want = m[["order_id", "order_date", "coupon_code", "status", "discounted"]]
# --- end pandas
print()
print(want.to_string(index=False))
pd.testing.assert_frame_equal(got.sort_values("order_id").reset_index(drop=True),
                              want.sort_values("order_id").reset_index(drop=True), check_dtype=False)
assert len(want) == len(orders) == 7
print("assert passed: SQL equals pandas after sorting by order_id; 7 rows in, 7 rows out")
```

**Output (my run):**
```text
 order_id order_date coupon_code       status  discounted
        1 2025-03-01      SAVE10        VALID        90.0
        2 2025-03-31      SAVE10        VALID       180.0
        3 2025-02-28      SAVE10  NOT_STARTED         NaN
        4 2025-04-01      SAVE10      EXPIRED         NaN
        5 2025-03-12       FLASH        VALID        60.0
        6 2025-03-05       BOGUS UNKNOWN_CODE         NaN
        7 2025-03-05         NaN    NO_COUPON         NaN

with the date test in WHERE, rows left: 3 of 7
date test in ON, code match flag (cannot tell EXPIRED from UNKNOWN_CODE): [1, 1, 0, 0, 1, 0, 0]

 order_id order_date coupon_code       status  discounted
        1 2025-03-01      SAVE10        VALID        90.0
        2 2025-03-31      SAVE10        VALID       180.0
        3 2025-02-28      SAVE10  NOT_STARTED         NaN
        4 2025-04-01      SAVE10      EXPIRED         NaN
        5 2025-03-12       FLASH        VALID        60.0
        6 2025-03-05       BOGUS UNKNOWN_CODE         NaN
        7 2025-03-05         NaN    NO_COUPON         NaN
assert passed: SQL equals pandas after sorting by order_id; 7 rows in, 7 rows out
```

**Edge cases:**
- **WHERE instead of ON:** putting the date test in WHERE turns the LEFT JOIN into an inner join: only 3 of the 7 orders survive (orders 1, 2, 5). Cross-reference Part 2 Q3.
- **Date test inside ON:** it keeps all 7 rows but the coupon columns come back NULL for orders 3, 4 and 6 alike, so you cannot tell EXPIRED or NOT_STARTED from UNKNOWN_CODE. Put the code match in ON and classify afterwards.
- **Order of the CASE:** NO_COUPON before UNKNOWN_CODE, because both have a NULL `c.code`.
- **Duplicate code rows:** `code` is the primary key here. If a code could have several windows (re-runs of a campaign) the join would duplicate orders; then join on the window too and treat no match as the not-valid case, or pick one window per order with a window function.
- **Timestamps:** an `order_date` that carries a time of day breaks an inclusive `BETWEEN` against a pure date end (the end day after 00:00 would look expired). Compare against `end_date + 1 day` with `<` for timestamps (not executed here).
- **Case or spaces in codes:** 'save10' would be UNKNOWN_CODE; clean with `UPPER(TRIM())` if the data is user-typed (UPPER is ASCII-only in SQLite).

**Then explain:**
- **The WHERE-versus-ON rule:** a condition on the right table in WHERE removes the NULL-extended rows; a condition in ON only decides what matches. Here the code match belongs in ON and the classification is a CASE over the joined columns.
- **Inclusive ends** are the whole point of the seed: `<` and `>` for the invalid sides, so the boundary dates fall through to VALID.
- **pandas:** `merge(how="left")` then `np.select` with conditions in the same order as the CASE (first true wins, like CASE). The discount is `where(status == VALID)`, which gives NaN like the CASE without ELSE.
- **Scoring note (Set E2, 20 pts; this book's own rubric, not a company's):** 8 for a correct query, 4 for the seeded edge case, 4 for the pandas version, 2 for stating the assumption, 2 for the check. Full marks: all five statuses are right on the seeded boundary dates (orders 1, 2, 5 VALID), the join keeps 7 rows, and you say why the test is not in WHERE. Partial: a correct VALID/EXPIRED split but an inner join (the NO_COUPON and UNKNOWN_CODE orders lost) is about half of the query marks; date test in ON gets the rows but not the reasons.

**Follow-ups:**
- *What if the discount must be capped?* Wrap in `MIN(discount, cap)` using the scalar two-argument `MIN` in SQLite (a different function from the aggregate; other engines use `LEAST`, not executed here).
- *What if an order can carry several coupons?* Move codes to an `order_coupons` table; then the join fans out, so decide whether to stack or choose the best and aggregate per order.
- *How do you check the result?* Row count out equals row count in (7), and the VALID count equals the count from an inner join with the dates in ON.

**Common mistakes:**
- Date condition in WHERE, silently dropping the orders without a valid coupon.
- Using `BETWEEN` for the exclusive sides or `<=` on the end, making the boundary dates EXPIRED.
- Testing `coupon_code = NULL` instead of `IS NULL`.
- Computing the discount as `amount * pct_off / 100` (that is the discount, not the discounted amount) or with integer division.

### Q32 ⭐⭐ 🟡 [Set E2, Q2 of 5, 8 min, 20 pts] Frequently bought together pairs (Part 2 Q37). order_items(order_id, product_id) with duplicate rows possible for the same product in one order. Return the pairs of products bought together in at least 2 orders, each pair once with its order count, ordered by count descending. Seed 6 orders with a duplicate row. SQL (self join on a.product_id < b.product_id with DISTINCT orders) and pandas (merge or combinations). Assert equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** De-duplicate to distinct (order, product) first, self join on the same order with `a.product_id < b.product_id` so each pair appears once, group by the pair and keep `COUNT(*) >= 2`.

**Schema and sample data:**
```sql
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'B'),(3,'B'),
 (4,'B'),(4,'C'),
 (5,'A'),(5,'C'),
 (6,'D');
```
Order 3 holds product B twice (the duplicate row); order 6 has a single item.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH d AS (SELECT DISTINCT order_id, product_id FROM order_items)
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM d a
JOIN d b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
```
`DISTINCT` in the CTE makes one row per product per order, so every joined row is one order containing both products and `COUNT(*)` is the number of orders. The `<` condition keeps (A, B) and drops (B, A) and (A, A).

**pandas answer:** the same text as the pandas part of the Code block.
```py
items = pd.read_sql("SELECT * FROM order_items", con).drop_duplicates()
pairs = items.merge(items, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs.product_id_1 < pairs.product_id_2]
want = (pairs.groupby(["product_id_1", "product_id_2"]).size().rename("orders_together").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"}))
want = (want[want.orders_together >= 2]
        .sort_values(["orders_together", "p1", "p2"], ascending=[False, True, True]).reset_index(drop=True))
```

**Example:** Distinct items: order 1 {A,B,C}, 2 {A,B}, 3 {A,B}, 4 {B,C}, 5 {A,C}, 6 {D}. Pairs per order: order 1 gives AB, AC, BC; order 2 gives AB; order 3 gives AB; order 4 gives BC; order 5 gives AC; order 6 gives none. Totals: AB 3, AC 2, BC 2, all at least 2. Without the DISTINCT, order 3's two B rows pair with its A row twice, so AB becomes 4: the naive query overstates by exactly the duplicate.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q32: frequently bought together pairs, each pair once, distinct orders.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'B'),(3,'B'),
 (4,'B'),(4,'C'),
 (5,'A'),(5,'C'),
 (6,'D');
""")

sql_answer = """
WITH d AS (SELECT DISTINCT order_id, product_id FROM order_items)
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM d a
JOIN d b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
"""
sql_naive = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM order_items a
JOIN order_items b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
"""
got = pd.read_sql(sql_answer, con)
print("SQL answer"); print(got.to_string(index=False))
print("\nnaive (no DISTINCT), duplicate row counted twice"); print(pd.read_sql(sql_naive, con).to_string(index=False))

# --- pandas
items = pd.read_sql("SELECT * FROM order_items", con).drop_duplicates()
pairs = items.merge(items, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs.product_id_1 < pairs.product_id_2]
want = (pairs.groupby(["product_id_1", "product_id_2"]).size().rename("orders_together").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"}))
want = (want[want.orders_together >= 2]
        .sort_values(["orders_together", "p1", "p2"], ascending=[False, True, True]).reset_index(drop=True))
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: same rows in the same order (count desc, p1, p2)")
```

**Output (my run):**
```text
SQL answer
p1 p2  orders_together
 A  B                3
 A  C                2
 B  C                2

naive (no DISTINCT), duplicate row counted twice
p1 p2  orders_together
 A  B                4
 A  C                2
 B  C                2

pandas
p1 p2  orders_together
 A  B                3
 A  C                2
 B  C                2
assert passed: same rows in the same order (count desc, p1, p2)
```

**Edge cases:**
- **Duplicate rows:** the seeded duplicate moves AB from 3 to 4 without DISTINCT (shown in the output). Alternative: count `COUNT(DISTINCT a.order_id)` and skip the CTE.
- **Single-item orders** (order 6) create no pair, which is correct; they just do not appear.
- **Ties:** AC and BC both have 2, so the secondary sort `p1, p2` makes the order deterministic.
- **Scale:** the self join makes k*(k-1)/2 rows per order of k items, so a 50-item basket gives 1,225 rows; cap basket size or sample before running this on real data.
- **Empty result:** if no pair reaches 2 the query returns zero rows, not a row of zeros.

**Then explain:**
- **Why `<` and not `<>`:** `<>` returns both (A, B) and (B, A), doubling every count and needing a later de-duplication; `<` is a canonical ordering of the pair (Part 2 Q37).
- **Why distinct first:** the unit being counted is an order, and a duplicate line must not count twice.
- **pandas:** `drop_duplicates()`, merge the table with itself on `order_id`, filter `product_id_1 < product_id_2`, `groupby(...).size()`, then filter and sort. The assertion compares in the stated order: count descending, then p1, p2 (no re-sorting needed).
- **Alternative (not run):** `itertools.combinations` over each order's sorted distinct products and a `Counter`; same answer, better memory behaviour for big baskets.
- **Scoring note (Set E2, 20 pts; this book's own rubric, not a company's):** 8 for a correct query, 4 for the seeded edge case, 4 for the pandas version, 2 for stating the assumption, 2 for the check. Full marks: the pair list is AB 3, AC 2, BC 2 in that order, each pair once, with the duplicate handled and said aloud. Partial: a self join that returns both (A,B) and (B,A), or counts AB as 4, keeps most of the query marks but loses the edge-case marks.

**Follow-ups:**
- *What would you add for recommendations?* Support and lift: pair count divided by the number of orders containing each product (orders with A: 4, with B: 4 here), not just raw counts.
- *How do you make it faster?* An index on `(order_id, product_id)` and a pre-filter to products with at least 2 orders, since a pair needs both products to qualify.
- *Triples?* Add a third alias with `b.product_id < c.product_id`; the same duplicate rule applies.

**Common mistakes:**
- `a.product_id <> b.product_id`, which doubles the counts.
- Counting rows instead of distinct orders, so duplicates inflate the pair.
- Putting `COUNT(*) >= 2` in WHERE instead of HAVING.
- Forgetting the tie-break, so the printed order changes between runs.

### Q33 ⭐ 🟢 [Set F1, Q1 of 5, 5 min, 10 pts] Daily active users excluding test accounts (Part 8 Q1). users(user_id, is_test), events(user_id, event_ts TEXT). Return DAU per day for 5 days with days that only have test users shown as 0. Seed 6 users and 12 events including a user with several events per day and an event whose user_id is not in users (decide and state). SQL and pandas.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Inner join events to the non-test users, take `COUNT(DISTINCT user_id)` per day, and LEFT JOIN that onto a generated calendar so a day with only test users shows 0; an unknown user_id is excluded and I say so.

**Schema and sample data:**
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,1),(4,0),(5,1),(6,0);
INSERT INTO events VALUES
 (1,'2025-06-01 09:00:00'),(1,'2025-06-01 15:00:00'),(1,'2025-06-01 18:00:00'),
 (2,'2025-06-01 10:00:00'),
 (3,'2025-06-02 11:00:00'),(3,'2025-06-03 12:00:00'),
 (4,'2025-06-02 08:00:00'),(4,'2025-06-04 09:00:00'),
 (1,'2025-06-04 10:00:00'),
 (5,'2025-06-03 13:00:00'),
 (99,'2025-06-05 10:00:00'),
 (6,'2025-06-05 12:00:00');
```
Users 3 and 5 are test accounts; user 99 is not in `users`.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH RECURSIVE days(d) AS (
  SELECT '2025-06-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2025-06-05'
), real_events AS (
  SELECT e.user_id, date(e.event_ts) AS d
  FROM events e JOIN users u ON u.user_id = e.user_id AND u.is_test = 0
)
SELECT days.d AS day, COUNT(DISTINCT r.user_id) AS dau
FROM days LEFT JOIN real_events r ON r.d = days.d
GROUP BY days.d
ORDER BY days.d
```
The recursive CTE builds the 5-day calendar (Part 9 shape; a calendar table does the same). The join to `users` with `is_test = 0` is an inner join, so unknown users are dropped as well as test users. `date(event_ts)` cuts the text timestamp to the day.

**pandas answer:** the same text as the pandas part of the Code block.
```py
users = pd.read_sql("SELECT * FROM users", con)
events = pd.read_sql("SELECT * FROM events", con)
real = events.merge(users[users.is_test == 0], on="user_id", how="inner")
real["day"] = real.event_ts.str[:10]
want = (real.groupby("day").user_id.nunique()
        .reindex(pd.date_range("2025-06-01", "2025-06-05").strftime("%Y-%m-%d"), fill_value=0)
        .rename_axis("day").rename("dau").reset_index())
```

**Example:** 2025-06-01: events from users 1 (three of them) and 2, so 2 distinct users. 06-02: test user 3 is out, user 4 stays: 1. 06-03: only test users 3 and 5 are active, so after the filter no event is left and the LEFT JOIN from the calendar gives 0. 06-04: users 4 and 1: 2. 06-05: user 99 is unknown and dropped, user 6 stays: 1.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q33: DAU excluding test accounts, zero-filled calendar, unknown user_id decision.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,1),(4,0),(5,1),(6,0);
INSERT INTO events VALUES
 (1,'2025-06-01 09:00:00'),(1,'2025-06-01 15:00:00'),(1,'2025-06-01 18:00:00'),
 (2,'2025-06-01 10:00:00'),
 (3,'2025-06-02 11:00:00'),(3,'2025-06-03 12:00:00'),
 (4,'2025-06-02 08:00:00'),(4,'2025-06-04 09:00:00'),
 (1,'2025-06-04 10:00:00'),
 (5,'2025-06-03 13:00:00'),
 (99,'2025-06-05 10:00:00'),
 (6,'2025-06-05 12:00:00');
""")

sql_answer = """
WITH RECURSIVE days(d) AS (
  SELECT '2025-06-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2025-06-05'
), real_events AS (
  SELECT e.user_id, date(e.event_ts) AS d
  FROM events e JOIN users u ON u.user_id = e.user_id AND u.is_test = 0
)
SELECT days.d AS day, COUNT(DISTINCT r.user_id) AS dau
FROM days LEFT JOIN real_events r ON r.d = days.d
GROUP BY days.d
ORDER BY days.d
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nwith unknown user 99 kept (LEFT JOIN users, is_test IS NOT 1):")
print(con.execute("""SELECT date(e.event_ts), COUNT(DISTINCT e.user_id) FROM events e
  LEFT JOIN users u ON u.user_id = e.user_id WHERE u.is_test IS NOT 1 GROUP BY 1 ORDER BY 1""").fetchall())

# --- pandas
users = pd.read_sql("SELECT * FROM users", con)
events = pd.read_sql("SELECT * FROM events", con)
real = events.merge(users[users.is_test == 0], on="user_id", how="inner")
real["day"] = real.event_ts.str[:10]
want = (real.groupby("day").user_id.nunique()
        .reindex(pd.date_range("2025-06-01", "2025-06-05").strftime("%Y-%m-%d"), fill_value=0)
        .rename_axis("day").rename("dau").reset_index())
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: 5 rows, ordered by day; day 2025-06-03 is 0 because only test user 3 and 5 were active")
```

**Output (my run):**
```text
       day  dau
2025-06-01    2
2025-06-02    1
2025-06-03    0
2025-06-04    2
2025-06-05    1

with unknown user 99 kept (LEFT JOIN users, is_test IS NOT 1):
[('2025-06-01', 2), ('2025-06-02', 1), ('2025-06-04', 2), ('2025-06-05', 2)]

pandas
       day  dau
2025-06-01    2
2025-06-02    1
2025-06-03    0
2025-06-04    2
2025-06-05    1
assert passed: 5 rows, ordered by day; day 2025-06-03 is 0 because only test user 3 and 5 were active
```

**Edge cases:**
- **Several events per user per day:** `COUNT(DISTINCT user_id)`; plain `COUNT(*)` would give 4 for 06-01.
- **Day with no real activity:** the calendar LEFT JOIN is what produces the 0 for 06-03; without it the day is missing.
- **Unknown user_id (my decision):** excluded, because I cannot show it is not a test account. The alternative `LEFT JOIN users ... WHERE u.is_test IS NOT 1` keeps user 99 and gives 2 for 06-05 (printed in the output); say which you chose. A NULL `is_test` falls in the same fork: `is_test = 0` excludes it, `IS NOT 1` keeps it.
- **Time zones:** `date(event_ts)` cuts the stored text, so the day is whatever zone the text is in (assume UTC here).
- **Filter in ON, not WHERE:** the `is_test = 0` test is inside the inner join; putting a right-table filter in WHERE after the calendar LEFT JOIN would drop the zero day.

**Then explain:**
- **DAU definition:** distinct users with at least one event in the day (Part 8 Q1), not event count.
- **pandas:** inner `merge` to non-test users, `nunique` per day string, then `reindex` on a full `date_range` with `fill_value=0`; `reindex` is the pandas version of the calendar LEFT JOIN.
- **Scoring note (Set F1, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: DAU 2, 1, 0, 2, 1 with the zero day present, and the unknown-user decision stated. Partial: correct counts but a missing 06-03 row (no calendar) loses the edge-case marks; counting events instead of users fails the main query.

**Follow-ups:**
- *How would you do MAU?* Same shape on a month key, or a rolling 30-day distinct count (Part 8 Q7 style; windows with DISTINCT are not available in SQLite, so a self join or a pre-deduplicated day table is needed).
- *How do you flag unknown ids?* A separate query: events where `user_id NOT IN` (or NOT EXISTS) users, reported to the data owners.

**Common mistakes:**
- `COUNT(user_id)` instead of `COUNT(DISTINCT user_id)`.
- Filtering test users in WHERE after the calendar join, which deletes the zero days.
- Silently keeping unknown ids because a LEFT JOIN plus `is_test <> 1` ignores NULLs (NULL <> 1 is NULL, so the row disappears, the opposite of what many expect).

### Q34 ⭐ 🟢 [Set F2, Q1 of 5, 5 min, 10 pts] Click-through rate with a zero guard (Part 1 Q6). impressions(campaign_id, impressions), clicks(campaign_id, clicks) where one campaign has no click row and one has 0 impressions. Return CTR per campaign rounded to 4 decimals, NULL when impressions are 0, and 0 when there is no click row. SQL (LEFT JOIN, COALESCE, NULLIF) and pandas, assert equal.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** LEFT JOIN clicks onto impressions, `COALESCE(clicks, 0)` for the missing click row, divide by `NULLIF(impressions, 0)` so zero impressions gives NULL, then round to 4 decimals.

**Schema and sample data:**
```sql
CREATE TABLE impressions(campaign_id INTEGER, impressions INTEGER);
CREATE TABLE clicks(campaign_id INTEGER, clicks INTEGER);
INSERT INTO impressions VALUES (1,1000),(2,500),(3,0),(4,200),(5,7),(6,0);
INSERT INTO clicks VALUES (1,37),(3,0),(4,5),(5,3);
```
Campaign 2 has no click row; campaigns 3 and 6 have 0 impressions (6 also has no click row).

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT i.campaign_id,
       ROUND(COALESCE(c.clicks, 0) * 1.0 / NULLIF(i.impressions, 0), 4) AS ctr
FROM impressions i
LEFT JOIN clicks c ON c.campaign_id = i.campaign_id
ORDER BY i.campaign_id
```
`* 1.0` forces real division (integer division would give 0). Zero impressions makes `NULLIF` return NULL and the whole ratio NULL; a missing click row becomes 0 via `COALESCE`, which only affects the numerator.

**pandas answer:** the same text as the pandas part of the Code block.
```py
imp = pd.read_sql("SELECT * FROM impressions", con)
clk = pd.read_sql("SELECT * FROM clicks", con)
m = imp.merge(clk, on="campaign_id", how="left")
m["ctr"] = (m.clicks.fillna(0) / m.impressions.replace(0, np.nan)).round(4)
want = m[["campaign_id", "ctr"]]
```

**Example:** Campaign 1: 37 / 1000 = 0.037, printed 0.0370. Campaign 2: no click row, COALESCE gives 0, 0 / 500 = 0. Campaign 3: 0 impressions, so 0 / NULL = NULL. Campaign 4: 5 / 200 = 0.025. Campaign 5: 3 / 7 = 0.428571, rounded 0.4286. Campaign 6: no click row and 0 impressions: NULL (impressions rule wins).

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q34: CTR per campaign with zero guards.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE impressions(campaign_id INTEGER, impressions INTEGER);
CREATE TABLE clicks(campaign_id INTEGER, clicks INTEGER);
INSERT INTO impressions VALUES (1,1000),(2,500),(3,0),(4,200),(5,7),(6,0);
INSERT INTO clicks VALUES (1,37),(3,0),(4,5),(5,3);
""")

sql_answer = """
SELECT i.campaign_id,
       ROUND(COALESCE(c.clicks, 0) * 1.0 / NULLIF(i.impressions, 0), 4) AS ctr
FROM impressions i
LEFT JOIN clicks c ON c.campaign_id = i.campaign_id
ORDER BY i.campaign_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\nunguarded division in SQLite, 3 / 0 and 0 / 0:", con.execute("SELECT 3*1.0/0, 0*1.0/0").fetchone())

# --- pandas
imp = pd.read_sql("SELECT * FROM impressions", con)
clk = pd.read_sql("SELECT * FROM clicks", con)
m = imp.merge(clk, on="campaign_id", how="left")
m["ctr"] = (m.clicks.fillna(0) / m.impressions.replace(0, np.nan)).round(4)
want = m[["campaign_id", "ctr"]]
# --- end pandas
print("\npandas"); print(want.to_string(index=False, na_rep="NaN"))
print("unguarded pandas division 3 / 0 and 0 / 0:",
      (pd.Series([3.0, 0.0]) / pd.Series([0.0, 0.0])).tolist())
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: NULL in SQL equals NaN in pandas for campaigns 3 and 6")
```

**Output (my run):**
```text
 campaign_id    ctr
           1 0.0370
           2 0.0000
           3   NULL
           4 0.0250
           5 0.4286
           6   NULL

unguarded division in SQLite, 3 / 0 and 0 / 0: (None, None)

pandas
 campaign_id    ctr
           1 0.0370
           2 0.0000
           3    NaN
           4 0.0250
           5 0.4286
           6    NaN
unguarded pandas division 3 / 0 and 0 / 0: [inf, nan]
assert passed: NULL in SQL equals NaN in pandas for campaigns 3 and 6
```

**Edge cases:**
- **Zero impressions:** SQLite returns NULL for `x / 0` (shown: `3*1.0/0` and `0*1.0/0` both NULL); Postgres raises "division by zero" and MySQL returns NULL in default mode (both not executed here), so the `NULLIF` guard is the portable version.
- **No click row versus 0 clicks:** both end up 0; a missing row is an absent fact, and treating it as 0 is an assumption to say aloud.
- **Several click rows per campaign:** the join would duplicate impression rows; aggregate clicks per campaign first (Part 8 Q10).
- **Rounding:** `ROUND` in SQLite and pandas can differ on exact halves (Part 10 lesson: 703.125 rounds to 703.13 in SQLite and 703.12 in pandas); no seeded value here is a half, so the assertion is safe.

**Then explain:**
- **Why NULL, not 0, for no impressions:** the rate is undefined, and 0 would say the campaign performed badly (Part 1 Q6).
- **pandas difference:** `3.0 / 0.0` gives `inf`, not NaN (printed), so zero is replaced with NaN before dividing; `0/0` is NaN. SQL gives NULL for both without help.
- **Scoring note (Set F2, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: both guards in the right places (NULLIF on the denominator, COALESCE on the numerator) with 0.0370, 0, NULL, 0.0250, 0.4286, NULL. Partial: forgetting the `* 1.0` (all zeros) or a COALESCE on the whole ratio (returns 0 for zero impressions) is partial.

**Follow-ups:**
- *Why not `WHERE impressions > 0`?* It drops the campaign instead of reporting it as undefined.
- *CTR across campaigns?* Sum clicks over sum impressions (a weighted rate), not the mean of the per-campaign CTRs.

**Common mistakes:**
- Integer division giving 0.
- `COALESCE(ctr, 0)` around the ratio, hiding the undefined case as 0.
- Inner joining clicks, losing campaign 2.

### Q35 ⭐ 🟢 [Set F3, Q1 of 5, 5 min, 10 pts] Customers with no orders in 2025 (Part 2 Q2, Part 3 Q3). customers(customer_id, name) and orders(order_id, customer_id, order_date) where one order row has customer_id NULL. Return customers with no 2025 orders using NOT EXISTS, show that NOT IN returns nothing because of the NULL, and give the pandas version. Seed 6 customers.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** `NOT EXISTS` with the 2025 date range inside the subquery returns the right customers; `NOT IN` returns nothing as soon as the subquery contains one NULL, because `x NOT IN (..., NULL)` is never true.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_date TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid');
INSERT INTO orders VALUES
 (1, 1, '2025-01-10'), (2, 2, '2025-06-01'), (3, 3, '2024-12-31'),
 (4, NULL, '2025-03-03'), (5, 1, '2025-07-07'), (6, 5, '2026-01-01');
```
Order 4 is a 2025 order with a NULL customer_id.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id
                    AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01')
ORDER BY c.customer_id
```
The `NOT IN` version and its repaired form are in the Code block as `sql_not_in` and `sql_not_in_fixed`. The date range is `>= '2025-01-01' AND < '2026-01-01'` so it also works if `order_date` has a time part.

**pandas answer:** the same text as the pandas part of the Code block.
```py
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
in_2025 = orders[(orders.order_date >= "2025-01-01") & (orders.order_date < "2026-01-01")]
want = customers[~customers.customer_id.isin(in_2025.customer_id)].reset_index(drop=True)
```

**Example:** 2025 orders belong to customers 1 (two orders), 2 and NULL. So Asha and Ben have orders; Chitra's order is 2024-12-31 and Esha's is 2026-01-01, both outside 2025; Dev and Farid have none. The answer is Chitra, Dev, Esha, Farid. With NOT IN the list is (1, 2, NULL, 1): for Chitra, `3 NOT IN (1,2,NULL)` is `3<>1 AND 3<>2 AND 3<>NULL`, which is TRUE AND TRUE AND UNKNOWN = UNKNOWN, so no row is returned for anyone.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q35: customers with no orders in 2025: NOT EXISTS vs NOT IN with a NULL in the subquery.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_date TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid');
INSERT INTO orders VALUES
 (1, 1, '2025-01-10'), (2, 2, '2025-06-01'), (3, 3, '2024-12-31'),
 (4, NULL, '2025-03-03'), (5, 1, '2025-07-07'), (6, 5, '2026-01-01');
""")

sql_answer = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id
                    AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01')
ORDER BY c.customer_id
"""
sql_not_in = """
SELECT c.customer_id, c.name FROM customers c
WHERE c.customer_id NOT IN (SELECT customer_id FROM orders
                            WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01')
ORDER BY c.customer_id
"""
sql_not_in_fixed = sql_not_in.replace(
    "WHERE order_date >= '2025-01-01'", "WHERE customer_id IS NOT NULL AND order_date >= '2025-01-01'")
got = pd.read_sql(sql_answer, con)
print("NOT EXISTS"); print(got.to_string(index=False))
print("\nNOT IN with the NULL row inside 2025, rows returned:", len(pd.read_sql(sql_not_in, con)))
fixed = pd.read_sql(sql_not_in_fixed, con)
print("NOT IN with customer_id IS NOT NULL added, rows returned:", len(fixed))

# --- pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
in_2025 = orders[(orders.order_date >= "2025-01-01") & (orders.order_date < "2026-01-01")]
want = customers[~customers.customer_id.isin(in_2025.customer_id)].reset_index(drop=True)
# --- end pandas
print("\npandas ~isin (the NaN in the list does not poison it)"); print(want.to_string(index=False))
print("customer_id dtype after read_sql:", orders.customer_id.dtype, "(float because of the NULL)")
pd.testing.assert_frame_equal(got, want, check_dtype=False)
pd.testing.assert_frame_equal(got, fixed, check_dtype=False)
print("assert passed: NOT EXISTS = pandas ~isin = guarded NOT IN, ordered by customer_id")
```

**Output (my run):**
```text
NOT EXISTS
 customer_id   name
           3 Chitra
           4    Dev
           5   Esha
           6  Farid

NOT IN with the NULL row inside 2025, rows returned: 0
NOT IN with customer_id IS NOT NULL added, rows returned: 4

pandas ~isin (the NaN in the list does not poison it)
 customer_id   name
           3 Chitra
           4    Dev
           5   Esha
           6  Farid
customer_id dtype after read_sql: float64 (float because of the NULL)
assert passed: NOT EXISTS = pandas ~isin = guarded NOT IN, ordered by customer_id
```

**Edge cases:**
- **NULL in the subquery:** NOT IN returns 0 rows (printed); filtering `customer_id IS NOT NULL` inside the subquery fixes it (4 rows).
- **Empty subquery:** NOT IN on an empty list is TRUE for everyone, so the NULL trap only appears when there is data.
- **NULL on the outer side:** a customer with NULL id would also never match NOT IN; here the key is a primary key.
- **pandas:** `~isin` treats NaN as an ordinary value and does not poison the test, so pandas returns the right 4 rows even with the NaN in the list, a difference from SQL (printed). The column is float64 because read_sql turns a NULL integer into NaN.
- **Year boundary:** 2024-12-31 and 2026-01-01 are excluded by the range; a `BETWEEN '2025-01-01' AND '2025-12-31'` would miss 2025-12-31 18:00 on a timestamp column.

**Then explain:**
- **Three-valued logic:** NOT IN expands to a chain of `<>` joined by AND; one UNKNOWN makes the whole chain UNKNOWN, and WHERE keeps only TRUE (Part 2 Q2, Part 3 Q3).
- **NOT EXISTS** compares per row and ignores the NULL row because `o.customer_id = c.customer_id` is UNKNOWN for it, so it never matches.
- **Alternative:** `LEFT JOIN ... WHERE o.order_id IS NULL` with the 2025 test in ON (not run here separately).
- **Scoring note (Set F3, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: the 4 correct customers by NOT EXISTS, the demonstration that NOT IN returns 0 rows, and the one-line reason. Partial: the right customers but no explanation of the NULL, or a NOT IN answer that happens to work only because the seed has no NULL, is partial.

**Follow-ups:**
- *Can you keep NOT IN?* Yes if the subquery column is NOT NULL by constraint or filtered with `IS NOT NULL`, but NOT EXISTS is safer.
- *Performance?* Modern planners often turn NOT EXISTS into an anti-join; confirm with EXPLAIN (Part 11), engine-specific, not executed here for other engines.

**Common mistakes:**
- Using NOT IN on a nullable column.
- Putting the year filter in the outer WHERE instead of the subquery, which changes the meaning.
- Using `BETWEEN` with a year-end date on timestamps.

### Q36 ⭐ 🟢 [Set T1, Q1 of 5, 5 min, 10 pts] Payment success rate by merchant (Part 1 Q10). payments(payment_id, merchant_id, status) with status SUCCESS, FAILED or NULL. Return per merchant attempts, successes, and success rate counting NULL status as not success and in a second column excluding NULL from the denominator. Seed 8 payments over 3 merchants. SQL (conditional aggregation) and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Conditional aggregation: `COUNT(*)` for attempts, `SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)` for successes, then divide by `COUNT(*)` (NULL counted as not success) and by `NULLIF(COUNT(status), 0)` (NULL excluded).

**Schema and sample data:**
```sql
CREATE TABLE payments(payment_id INTEGER, merchant_id TEXT, status TEXT);
INSERT INTO payments VALUES
 (1,'m1','SUCCESS'),(2,'m1','SUCCESS'),(3,'m1','FAILED'),(4,'m1',NULL),
 (5,'m2','SUCCESS'),(6,'m2','FAILED'),
 (7,'m3',NULL),(8,'m3',NULL);
```
Merchant m3 has only NULL statuses.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT merchant_id,
       COUNT(*) AS attempts,
       SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successes,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS rate_all,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(status), 0), 4) AS rate_known
FROM payments
GROUP BY merchant_id
ORDER BY merchant_id
```
`COUNT(*)` counts rows, `COUNT(status)` counts non-NULL statuses. The CASE has an ELSE 0 so NULL status counts as not success (without ELSE the SUM would still ignore NULL; the ELSE makes the intent visible and keeps an all-NULL merchant at 0 instead of NULL).

**pandas answer:** the same text as the pandas part of the Code block.
```py
p = pd.read_sql("SELECT * FROM payments", con)
p["ok"] = (p.status == "SUCCESS").astype(int)
g = p.groupby("merchant_id").agg(attempts=("payment_id", "size"), successes=("ok", "sum"),
                                 known=("status", "count")).reset_index()
g["rate_all"] = (g.successes / g.attempts).round(4)
g["rate_known"] = (g.successes / g.known.replace(0, np.nan)).round(4)
want = g[["merchant_id", "attempts", "successes", "rate_all", "rate_known"]]
```

**Example:** m1: 4 attempts, successes = 2, rate_all = 2 / 4 = 0.5, known statuses = 3 (the NULL is out) so rate_known = 2 / 3 = 0.6667. m2: 2 attempts, 1 success, both rates 0.5. m3: 2 attempts, 0 successes, rate_all = 0 / 2 = 0, rate_known = 0 / NULLIF(0, 0) = NULL.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q36: payment success rate by merchant, NULL status counted two ways.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE payments(payment_id INTEGER, merchant_id TEXT, status TEXT);
INSERT INTO payments VALUES
 (1,'m1','SUCCESS'),(2,'m1','SUCCESS'),(3,'m1','FAILED'),(4,'m1',NULL),
 (5,'m2','SUCCESS'),(6,'m2','FAILED'),
 (7,'m3',NULL),(8,'m3',NULL);
""")

sql_answer = """
SELECT merchant_id,
       COUNT(*) AS attempts,
       SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successes,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS rate_all,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(status), 0), 4) AS rate_known
FROM payments
GROUP BY merchant_id
ORDER BY merchant_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\ntrap: WHERE status <> 'SUCCESS' returns", con.execute(
    "SELECT COUNT(*) FROM payments WHERE status <> 'SUCCESS'").fetchone()[0],
    "rows (FAILED only), the 3 NULL rows vanish")

# --- pandas
p = pd.read_sql("SELECT * FROM payments", con)
p["ok"] = (p.status == "SUCCESS").astype(int)
g = p.groupby("merchant_id").agg(attempts=("payment_id", "size"), successes=("ok", "sum"),
                                 known=("status", "count")).reset_index()
g["rate_all"] = (g.successes / g.attempts).round(4)
g["rate_known"] = (g.successes / g.known.replace(0, np.nan)).round(4)
want = g[["merchant_id", "attempts", "successes", "rate_all", "rate_known"]]
# --- end pandas
print("\npandas"); print(want.to_string(index=False, na_rep="NaN"))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: ordered by merchant_id; m3 has rate_all 0.0 and rate_known NULL/NaN")
```

**Output (my run):**
```text
merchant_id  attempts  successes  rate_all  rate_known
         m1         4          2       0.5      0.6667
         m2         2          1       0.5      0.5000
         m3         2          0       0.0        NULL

trap: WHERE status <> 'SUCCESS' returns 2 rows (FAILED only), the 3 NULL rows vanish

pandas
merchant_id  attempts  successes  rate_all  rate_known
         m1         4          2       0.5      0.6667
         m2         2          1       0.5      0.5000
         m3         2          0       0.0         NaN
assert passed: ordered by merchant_id; m3 has rate_all 0.0 and rate_known NULL/NaN
```

**Edge cases:**
- **NULL status:** a pending or unknown payment; the two columns are the two policies, and which one is right is a business decision (say it).
- **All-NULL merchant:** rate_all 0.0 but rate_known undefined (NULL/NaN), a distinction the output shows.
- **The trap:** `WHERE status <> 'SUCCESS'` returns only the 2 FAILED rows; the 3 NULL-status rows vanish because NULL <> 'SUCCESS' is UNKNOWN (printed).
- **Case or spelling** of status values ('Success') would count as not success; normalise first if the data is messy.

**Then explain:**
- **Denominators:** attempts (all rows) versus decided payments (non-NULL). Reporting both is the safe answer (Part 1 Q10).
- **pandas:** a 0/1 helper column, `agg` with named aggregations, `size` for rows and `count` for non-NaN; `count` on a column already excludes NaN, which is the pandas mirror of `COUNT(status)`. Zero is replaced by NaN before dividing, as in Q34.
- **Scoring note (Set T1, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: attempts 4/2/2, successes 2/1/0, both rate columns right including the NULL for m3. Partial: one rate column correct and the other wrong denominator, or ignoring the NULL status trap, is partial.

**Follow-ups:**
- *Where would failed-versus-pending matter?* In a payments funnel the NULL could mean in-flight; exclude payments newer than the settlement window rather than counting them as failures.
- *Can you use FILTER?* `COUNT(*) FILTER (WHERE status = 'SUCCESS')` runs on SQLite 3.30 and later and on PostgreSQL; MySQL has no FILTER (not executed here).

**Common mistakes:**
- `AVG(status = 'SUCCESS')`, which ignores NULL rows silently and gives the second policy by accident.
- Integer division in the rate.
- Dropping NULL rows in WHERE before counting attempts.

### Q37 ⭐ 🟢 [Set T2, Q1 of 5, 5 min, 10 pts] Outstanding balance per loan (Part 2 Q5). loans(loan_id, principal) and repayments(repayment_id, loan_id, amount). Return every loan including those with no repayment, the paid total (0 not NULL) and the outstanding amount, and mark overpaid loans. Seed 5 loans. SQL (LEFT JOIN with COALESCE, pre-aggregated to avoid fan-out) and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Aggregate repayments to one row per loan first, LEFT JOIN that to loans, `COALESCE(paid, 0)`, outstanding is principal minus paid and a loan is overpaid when paid is greater than principal.

**Schema and sample data:**
```sql
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal INTEGER);
CREATE TABLE repayments(repayment_id INTEGER, loan_id INTEGER, amount INTEGER);
INSERT INTO loans VALUES (1,1000),(2,500),(3,800),(4,600),(5,300);
INSERT INTO repayments VALUES (1,1,400),(2,1,300),(3,3,800),(4,4,700),(5,5,100),(6,99,50);
```
Loan 2 has no repayment, loan 4 is overpaid, and repayment 6 refers to a loan that does not exist.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT l.loan_id, l.principal,
       COALESCE(r.paid, 0) AS paid,
       l.principal - COALESCE(r.paid, 0) AS outstanding,
       CASE WHEN COALESCE(r.paid, 0) > l.principal THEN 1 ELSE 0 END AS overpaid
FROM loans l
LEFT JOIN (SELECT loan_id, SUM(amount) AS paid FROM repayments GROUP BY loan_id) r
       ON r.loan_id = l.loan_id
ORDER BY l.loan_id
```
The inner subquery makes one row per loan, so the join cannot multiply loans. `COALESCE` turns the missing aggregate for loan 2 into 0. The outstanding amount is negative for the overpaid loan; the flag marks it.

**pandas answer:** the same text as the pandas part of the Code block.
```py
loans = pd.read_sql("SELECT * FROM loans", con)
rep = pd.read_sql("SELECT * FROM repayments", con)
paid = rep.groupby("loan_id").amount.sum().rename("paid").reset_index()
want = loans.merge(paid, on="loan_id", how="left")
want["paid"] = want.paid.fillna(0).astype(int)
want["outstanding"] = want.principal - want.paid
want["overpaid"] = (want.paid > want.principal).astype(int)
want = want.sort_values("loan_id").reset_index(drop=True)
```

**Example:** Loan 1: repayments 400 + 300 = 700, outstanding 1000 - 700 = 300. Loan 2: no row, paid 0, outstanding 500. Loan 3: 800, outstanding 0, not overpaid (equal is fully paid). Loan 4: 700 against 600, outstanding -100, overpaid 1. Loan 5: 100, outstanding 200. The orphan repayment for loan 99 matches no loan and disappears from a LEFT JOIN starting at loans.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q37: outstanding balance per loan with pre-aggregated repayments.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal INTEGER);
CREATE TABLE repayments(repayment_id INTEGER, loan_id INTEGER, amount INTEGER);
INSERT INTO loans VALUES (1,1000),(2,500),(3,800),(4,600),(5,300);
INSERT INTO repayments VALUES (1,1,400),(2,1,300),(3,3,800),(4,4,700),(5,5,100),(6,99,50);
""")

sql_answer = """
SELECT l.loan_id, l.principal,
       COALESCE(r.paid, 0) AS paid,
       l.principal - COALESCE(r.paid, 0) AS outstanding,
       CASE WHEN COALESCE(r.paid, 0) > l.principal THEN 1 ELSE 0 END AS overpaid
FROM loans l
LEFT JOIN (SELECT loan_id, SUM(amount) AS paid FROM repayments GROUP BY loan_id) r
       ON r.loan_id = l.loan_id
ORDER BY l.loan_id
"""
sql_fanout = """
SELECT SUM(l.principal) FROM loans l LEFT JOIN repayments r ON r.loan_id = l.loan_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\ntotal principal, correct:", con.execute("SELECT SUM(principal) FROM loans").fetchone()[0],
      "| after joining raw repayments (fan-out):", con.execute(sql_fanout).fetchone()[0])

# --- pandas
loans = pd.read_sql("SELECT * FROM loans", con)
rep = pd.read_sql("SELECT * FROM repayments", con)
paid = rep.groupby("loan_id").amount.sum().rename("paid").reset_index()
want = loans.merge(paid, on="loan_id", how="left")
want["paid"] = want.paid.fillna(0).astype(int)
want["outstanding"] = want.principal - want.paid
want["overpaid"] = (want.paid > want.principal).astype(int)
want = want.sort_values("loan_id").reset_index(drop=True)
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
assert 99 not in want.loan_id.values
print("assert passed: 5 loans, ordered by loan_id; orphan repayment for loan 99 appears in neither")
```

**Output (my run):**
```text
 loan_id  principal  paid  outstanding  overpaid
       1       1000   700          300         0
       2        500     0          500         0
       3        800   800            0         0
       4        600   700         -100         1
       5        300   100          200         0

total principal, correct: 3200 | after joining raw repayments (fan-out): 4200

pandas
 loan_id  principal  paid  outstanding  overpaid
       1       1000   700          300         0
       2        500     0          500         0
       3        800   800            0         0
       4        600   700         -100         1
       5        300   100          200         0
assert passed: 5 loans, ordered by loan_id; orphan repayment for loan 99 appears in neither
```

**Edge cases:**
- **Fan-out:** joining raw repayments to loans repeats loan 1's principal on two rows, so `SUM(principal)` becomes 4,200 instead of 3,200 (printed). Pre-aggregation avoids it (Part 8 Q11).
- **No repayments:** loan 2 gets 0, not NULL, thanks to COALESCE; `principal - NULL` would otherwise be NULL.
- **Exactly paid:** paid equals principal is not overpaid (strict `>`).
- **Orphan rows:** repayment 99 is excluded here; reconciling it is a separate check (anti-join from repayments to loans).
- **Money types:** integers here; real money should be integer minor units or DECIMAL, not floats.

**Then explain:**
- **Why pre-aggregate:** the question wants one row per loan; aggregate the many side before the join (Part 2 Q5).
- **pandas:** `groupby.sum`, left `merge`, `fillna(0).astype(int)` (the merge makes `paid` float because of NaN), then vectorised arithmetic.
- **Scoring note (Set T2, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: all five loans including loan 2 at 0 paid and loan 4 flagged, without fan-out. Partial: correct numbers but NULL instead of 0 for loan 2, or an unflagged overpayment, is partial.

**Follow-ups:**
- *How do you find repayments for missing loans?* `LEFT JOIN repayments to loans WHERE l.loan_id IS NULL` (loan 99, amount 50).
- *Time-aware balance?* Add a running sum of repayments by date (Part 5), as of a cut-off date.

**Common mistakes:**
- Joining raw repayments and summing principal.
- Inner join, dropping unpaid loans.
- Using `>=` for overpaid.

### Q38 ⭐ 🟢 [Set T3, Q1 of 5, 5 min, 10 pts] New versus returning active customers per month (Part 6 Q14). wallet_activity(customer_id, activity_date) over Jan to Mar 2025. For each month return customers whose first ever activity month is that month (new) and those active earlier (returning). Seed 7 customers with duplicate rows per day. SQL and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Reduce to distinct (customer, month), get each customer's first month, then per month count customers whose month equals the first month (new) and those where it is later (returning).

**Schema and sample data:**
```sql
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2025-01-05'),(1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-02'),
 (2,'2025-01-20'),(2,'2025-03-15'),
 (3,'2025-02-01'),(3,'2025-02-01'),(3,'2025-02-14'),
 (4,'2025-02-20'),(4,'2025-03-01'),
 (5,'2025-03-05'),(5,'2025-03-05'),
 (6,'2025-01-31'),(6,'2025-02-01'),
 (7,'2025-03-30');
```
16 rows, 12 distinct customer-months, with duplicate rows on the same day and customer 2 silent in February.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH m AS (
  SELECT DISTINCT customer_id, SUBSTR(activity_date, 1, 7) AS ym FROM wallet_activity
), f AS (
  SELECT customer_id, MIN(ym) AS first_ym FROM m GROUP BY customer_id
)
SELECT m.ym,
       SUM(CASE WHEN m.ym = f.first_ym THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN m.ym > f.first_ym THEN 1 ELSE 0 END) AS returning_customers
FROM m JOIN f ON f.customer_id = m.customer_id
GROUP BY m.ym
ORDER BY m.ym
```
`SUBSTR(activity_date, 1, 7)` gives the 'YYYY-MM' key; the month strings sort correctly as text. `DISTINCT` removes the duplicate rows so a customer counts once per month.

**pandas answer:** the same text as the pandas part of the Code block.
```py
w = pd.read_sql("SELECT * FROM wallet_activity", con)
w["ym"] = w.activity_date.str[:7]
m = w[["customer_id", "ym"]].drop_duplicates()
m["first_ym"] = m.groupby("customer_id").ym.transform("min")
m["is_new"] = (m.ym == m.first_ym).astype(int)
m["is_ret"] = (m.ym > m.first_ym).astype(int)
want = (m.groupby("ym").agg(new_customers=("is_new", "sum"), returning_customers=("is_ret", "sum"))
        .reset_index())
```

**Example:** Distinct customer-months: January {1, 2, 6}, February {1, 3, 4, 6}, March {1, 2, 4, 5, 7}. First months: 1, 2 and 6 in January; 3 and 4 in February; 5 and 7 in March. January: 3 new, 0 returning. February: 3 and 4 are new, 1 and 6 are returning: 2 and 2. March: 5 and 7 are new, 1, 2 and 4 are returning (customer 2 skipped February and still counts as returning): 2 and 3.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q38: new vs returning active customers per month.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2025-01-05'),(1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-02'),
 (2,'2025-01-20'),(2,'2025-03-15'),
 (3,'2025-02-01'),(3,'2025-02-01'),(3,'2025-02-14'),
 (4,'2025-02-20'),(4,'2025-03-01'),
 (5,'2025-03-05'),(5,'2025-03-05'),
 (6,'2025-01-31'),(6,'2025-02-01'),
 (7,'2025-03-30');
""")

sql_answer = """
WITH m AS (
  SELECT DISTINCT customer_id, SUBSTR(activity_date, 1, 7) AS ym FROM wallet_activity
), f AS (
  SELECT customer_id, MIN(ym) AS first_ym FROM m GROUP BY customer_id
)
SELECT m.ym,
       SUM(CASE WHEN m.ym = f.first_ym THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN m.ym > f.first_ym THEN 1 ELSE 0 END) AS returning_customers
FROM m JOIN f ON f.customer_id = m.customer_id
GROUP BY m.ym
ORDER BY m.ym
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nsanity: raw rows", con.execute("SELECT COUNT(*) FROM wallet_activity").fetchone()[0],
      "| distinct customer-months", con.execute(
      "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, SUBSTR(activity_date,1,7) FROM wallet_activity)").fetchone()[0],
      "| sum of new + returning", int(got.new_customers.sum() + got.returning_customers.sum()))

# --- pandas
w = pd.read_sql("SELECT * FROM wallet_activity", con)
w["ym"] = w.activity_date.str[:7]
m = w[["customer_id", "ym"]].drop_duplicates()
m["first_ym"] = m.groupby("customer_id").ym.transform("min")
m["is_new"] = (m.ym == m.first_ym).astype(int)
m["is_ret"] = (m.ym > m.first_ym).astype(int)
want = (m.groupby("ym").agg(new_customers=("is_new", "sum"), returning_customers=("is_ret", "sum"))
        .reset_index())
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: 3 rows ordered by month")
```

**Output (my run):**
```text
     ym  new_customers  returning_customers
2025-01              3                    0
2025-02              2                    2
2025-03              2                    3

sanity: raw rows 16 | distinct customer-months 12 | sum of new + returning 12

pandas
     ym  new_customers  returning_customers
2025-01              3                    0
2025-02              2                    2
2025-03              2                    3
assert passed: 3 rows ordered by month
```

**Edge cases:**
- **Duplicates:** 16 rows collapse to 12 customer-months; the sanity line shows new + returning also totals 12.
- **Gap months:** customer 2 returns in March after a silent February; "returning" means active earlier, not active last month.
- **Month boundary:** customer 6 is active on 01-31 and 02-01, so one in each month.
- **First activity outside the window:** with only Jan to Mar data, a customer whose real first activity was in 2024 would be labelled new in January; the "first ever" needs full history, not just the window.
- **A month with no activity** would not appear; join to a month calendar if zero rows are needed (as in Q33).

**Then explain:**
- **Definition:** new = first ever activity month equals this month; returning = first month earlier than this month (Part 6 Q14).
- **pandas:** `drop_duplicates`, `groupby(...).transform('min')` for each customer's first month, two 0/1 helper columns and a grouped sum. `transform` keeps the row count, which is what a window `MIN() OVER` gives in SQL.
- **Scoring note (Set T3, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: 3/0, 2/2, 2/3 with duplicates removed and customer 2 counted as returning in March. Partial: a count that includes duplicate rows, or a returning definition that requires activity in the previous month, is partial.

**Follow-ups:**
- *Retention rate?* Returning customers in month m divided by active customers in month m-1 (a different definition, Part 6 Q10).
- *Why use the month text and not a date function?* Text `YYYY-MM` is portable and sorts; `DATE_TRUNC` exists in PostgreSQL, BigQuery and Snowflake but not in SQLite (not executed here).

**Common mistakes:**
- Counting rows instead of distinct customers.
- Calling someone new in every month because the first-month lookup is done per month instead of overall.
- Using the min over the filtered window only.

### Q39 ⭐ 🟢 [Set E1, Q1 of 5, 5 min, 10 pts] Orders and revenue by status (Part 1 Q4). orders(order_id, customer_id, status, amount) with some NULL amounts. Return orders, orders with an amount, revenue and average amount per status, showing how COUNT(*), COUNT(amount) and AVG treat the NULLs. Seed 8 orders. SQL and pandas (count versus size, mean skipna).
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** `COUNT(*)` counts rows, `COUNT(amount)` counts non-NULL amounts, `SUM` and `AVG` skip NULLs, so the average is over the orders that have an amount, not over all orders.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'DELIVERED',100),(2,2,'DELIVERED',200),(3,3,'DELIVERED',NULL),
 (4,4,'CANCELLED',NULL),(5,5,'CANCELLED',50),(6,6,'CANCELLED',NULL),
 (7,7,'RETURNED',80),
 (8,8,'SHIPPED',NULL);
```
SHIPPED has a single order with a NULL amount.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT status,
       COUNT(*) AS orders,
       COUNT(amount) AS orders_with_amount,
       SUM(amount) AS revenue,
       AVG(amount) AS avg_amount
FROM orders
GROUP BY status
ORDER BY status
```
No CASE needed: the aggregates' NULL rules do the work. The SHIPPED group is the one where every amount is NULL.

**pandas answer:** the same text as the pandas part of the Code block.
```py
o = pd.read_sql("SELECT * FROM orders", con)
want = (o.groupby("status").agg(orders=("order_id", "size"), orders_with_amount=("amount", "count"),
                                revenue=("amount", lambda s: s.sum(min_count=1)),
                                avg_amount=("amount", "mean"))
        .reset_index())
```

**Example:** DELIVERED: 3 orders, 2 with an amount (100, 200), revenue 300, average 300 / 2 = 150 (not 300 / 3 = 100). CANCELLED: 3 orders, 1 amount (50), revenue 50, average 50. RETURNED: 1 order, 80, 80. SHIPPED: 1 order, 0 amounts, SUM and AVG are NULL (no value, not 0).

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q39: orders and revenue by status with NULL amounts.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'DELIVERED',100),(2,2,'DELIVERED',200),(3,3,'DELIVERED',NULL),
 (4,4,'CANCELLED',NULL),(5,5,'CANCELLED',50),(6,6,'CANCELLED',NULL),
 (7,7,'RETURNED',80),
 (8,8,'SHIPPED',NULL);
""")

sql_answer = """
SELECT status,
       COUNT(*) AS orders,
       COUNT(amount) AS orders_with_amount,
       SUM(amount) AS revenue,
       AVG(amount) AS avg_amount
FROM orders
GROUP BY status
ORDER BY status
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\nwrong average, SUM / COUNT(*) for DELIVERED:",
      con.execute("SELECT SUM(amount) * 1.0 / COUNT(*) FROM orders WHERE status = 'DELIVERED'").fetchone()[0],
      "vs AVG:", con.execute("SELECT AVG(amount) FROM orders WHERE status = 'DELIVERED'").fetchone()[0])

# --- pandas
o = pd.read_sql("SELECT * FROM orders", con)
want = (o.groupby("status").agg(orders=("order_id", "size"), orders_with_amount=("amount", "count"),
                                revenue=("amount", lambda s: s.sum(min_count=1)),
                                avg_amount=("amount", "mean"))
        .reset_index())
# --- end pandas
print("\npandas (sum with min_count=1)"); print(want.to_string(index=False, na_rep="NaN"))
plain = o.groupby("status").amount.sum()
print("\npandas plain sum() for SHIPPED:", plain["SHIPPED"], "(SQL SUM gives NULL; pandas gives 0.0)")
print("amount.count() =", o.amount.count(), "| len(o) =", len(o), "| mean(skipna=False) =", o.amount.mean(skipna=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: ordered by status; SHIPPED revenue NULL equals NaN only with min_count=1")
```

**Output (my run):**
```text
   status  orders  orders_with_amount  revenue  avg_amount
CANCELLED       3                   1     50.0        50.0
DELIVERED       3                   2    300.0       150.0
 RETURNED       1                   1     80.0        80.0
  SHIPPED       1                   0     NULL        NULL

wrong average, SUM / COUNT(*) for DELIVERED: 100.0 vs AVG: 150.0

pandas (sum with min_count=1)
   status  orders  orders_with_amount  revenue  avg_amount
CANCELLED       3                   1     50.0        50.0
DELIVERED       3                   2    300.0       150.0
 RETURNED       1                   1     80.0        80.0
  SHIPPED       1                   0      NaN         NaN

pandas plain sum() for SHIPPED: 0.0 (SQL SUM gives NULL; pandas gives 0.0)
amount.count() = 4 | len(o) = 8 | mean(skipna=False) = nan
assert passed: ordered by status; SHIPPED revenue NULL equals NaN only with min_count=1
```

**Edge cases:**
- **All-NULL group:** SQL `SUM` is NULL and `AVG` is NULL for SHIPPED; pandas plain `sum()` gives 0.0 (printed). The assertion therefore uses `sum(min_count=1)`.
- **Wrong average:** `SUM / COUNT(*)` gives 100 for DELIVERED instead of 150 (printed); that treats a missing amount as 0, a decision, not a default.
- **Zero versus NULL:** an order with amount 0 would be counted by COUNT(amount) and lower the average; NULL would not.
- **pandas `mean(skipna=False)`** over the whole column gives NaN (printed), as one NULL poisons the result.

**Then explain:**
- **SQL rule:** aggregates ignore NULL inputs except `COUNT(*)`; with no non-NULL input `SUM` and `AVG` return NULL and `COUNT(col)` returns 0 (Part 1 Q4).
- **pandas:** `size` counts rows, `count` counts non-NaN (the `COUNT(*)` and `COUNT(col)` pair); `mean` skips NaN by default; `sum` skips NaN but returns 0.0 for an all-NaN group unless `min_count=1`.
- **Scoring note (Set E1, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: orders 3/3/1/1, with-amount 2/1/1/0, revenue 300/50/80/NULL, averages 150/50/80/NULL and the reason the DELIVERED average is 150. Partial: right counts but an average computed over all rows, or a 0 for SHIPPED revenue without comment, is partial.

**Follow-ups:**
- *How would you treat NULL as 0 on purpose?* `AVG(COALESCE(amount, 0))`, only if the business says a missing amount means free.
- *Why do the status groups not add to 8 with amounts?* Four orders have no amount; orders_with_amount sums to 4.

**Common mistakes:**
- Dividing `SUM` by `COUNT(*)`.
- Reading NULL revenue as 0 in a report.
- In pandas, using `len` or `size` when `count` is meant, or trusting `sum()` for an all-NaN group.

### Q40 ⭐ 🟢 [Set E2, Q1 of 5, 5 min, 10 pts] Cart abandonment rate (Part 8 Q27). events(session_id, event_name, event_ts) with add_to_cart and purchase events. Return the share of sessions with an add_to_cart that never reached purchase, and the share where purchase happened before add_to_cart (data anomaly). Seed 8 sessions. SQL (EXISTS or conditional aggregation) and pandas.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Per session take the first add_to_cart time and first purchase time with conditional aggregation; among sessions with an add, abandoned means no purchase at all and the anomaly means the first purchase is earlier than the first add.

**Schema and sample data:**
```sql
CREATE TABLE events(session_id TEXT, event_name TEXT, event_ts TEXT);
INSERT INTO events VALUES
 ('s1','add_to_cart','2025-05-01 10:00:00'),('s1','purchase','2025-05-01 10:05:00'),
 ('s2','add_to_cart','2025-05-01 11:00:00'),
 ('s3','add_to_cart','2025-05-01 12:00:00'),('s3','add_to_cart','2025-05-01 12:02:00'),
 ('s4','purchase','2025-05-01 09:00:00'),('s4','add_to_cart','2025-05-01 09:30:00'),
 ('s5','add_to_cart','2025-05-01 10:00:00'),('s5','purchase','2025-05-01 10:30:00'),('s5','add_to_cart','2025-05-01 10:40:00'),
 ('s6','page_view','2025-05-01 13:00:00'),
 ('s7','purchase','2025-05-01 14:00:00'),
 ('s8','add_to_cart','2025-05-01 15:00:00'),('s8','purchase','2025-05-01 15:00:00');
```
8 sessions: s6 never adds anything, s7 purchases without an add, s4 buys before it adds, s8 adds and buys at the same second.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH s AS (
  SELECT session_id,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_add,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY session_id
)
SELECT COUNT(*) AS carts,
       SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) AS abandoned,
       ROUND(SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS abandonment_rate,
       SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) AS purchase_before_add,
       ROUND(SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS anomaly_rate
FROM s
WHERE first_add IS NOT NULL
```
The denominator is sessions with at least one add_to_cart (6). Abandoned = no purchase event at all in the session; the EXISTS formulation (`sql_exists` in the Code block) gives the same counts.

**pandas answer:** the same text as the pandas part of the Code block.
```py
e = pd.read_sql("SELECT * FROM events", con)
s = (e.assign(add=e.event_ts.where(e.event_name == "add_to_cart"),
              buy=e.event_ts.where(e.event_name == "purchase"))
     .groupby("session_id").agg(first_add=("add", "min"), first_purchase=("buy", "min")))
carts = s[s.first_add.notna()]
abandoned = int(carts.first_purchase.isna().sum())
anomaly = int((carts.first_purchase < carts.first_add).sum())
want = pd.DataFrame({"carts": [len(carts)], "abandoned": [abandoned],
                     "abandonment_rate": [round(abandoned / len(carts), 4)],
                     "purchase_before_add": [anomaly], "anomaly_rate": [round(anomaly / len(carts), 4)]})
```

**Example:** Sessions with an add: s1, s2, s3, s4, s5, s8 = 6. s2 and s3 never purchase: abandoned 2, rate 2 / 6 = 0.3333 (s3's two adds still count as one session). s4's first purchase (09:00) is before its first add (09:30): 1 anomaly, 1 / 6 = 0.1667. s5 buys at 10:30 after its first add at 10:00 and re-adds at 10:40: not an anomaly. s8's add and purchase share a timestamp, a tie, so not counted as before. s6 and s7 have no add and stay out of the denominator.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q40: cart abandonment rate and purchase-before-add anomaly.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(session_id TEXT, event_name TEXT, event_ts TEXT);
INSERT INTO events VALUES
 ('s1','add_to_cart','2025-05-01 10:00:00'),('s1','purchase','2025-05-01 10:05:00'),
 ('s2','add_to_cart','2025-05-01 11:00:00'),
 ('s3','add_to_cart','2025-05-01 12:00:00'),('s3','add_to_cart','2025-05-01 12:02:00'),
 ('s4','purchase','2025-05-01 09:00:00'),('s4','add_to_cart','2025-05-01 09:30:00'),
 ('s5','add_to_cart','2025-05-01 10:00:00'),('s5','purchase','2025-05-01 10:30:00'),('s5','add_to_cart','2025-05-01 10:40:00'),
 ('s6','page_view','2025-05-01 13:00:00'),
 ('s7','purchase','2025-05-01 14:00:00'),
 ('s8','add_to_cart','2025-05-01 15:00:00'),('s8','purchase','2025-05-01 15:00:00');
""")

sql_answer = """
WITH s AS (
  SELECT session_id,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_add,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY session_id
)
SELECT COUNT(*) AS carts,
       SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) AS abandoned,
       ROUND(SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS abandonment_rate,
       SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) AS purchase_before_add,
       ROUND(SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS anomaly_rate
FROM s
WHERE first_add IS NOT NULL
"""
# second formulation with EXISTS, same two counts
sql_exists = """
SELECT COUNT(*) AS carts,
       SUM(NOT EXISTS (SELECT 1 FROM events p WHERE p.session_id = a.session_id AND p.event_name = 'purchase')) AS abandoned,
       SUM(EXISTS (SELECT 1 FROM events p WHERE p.session_id = a.session_id AND p.event_name = 'purchase'
                   AND p.event_ts < a.first_add)) AS purchase_before_add
FROM (SELECT session_id, MIN(event_ts) AS first_add FROM events WHERE event_name = 'add_to_cart' GROUP BY session_id) a
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
ex = pd.read_sql(sql_exists, con)
print("\nEXISTS version"); print(ex.to_string(index=False))

# --- pandas
e = pd.read_sql("SELECT * FROM events", con)
s = (e.assign(add=e.event_ts.where(e.event_name == "add_to_cart"),
              buy=e.event_ts.where(e.event_name == "purchase"))
     .groupby("session_id").agg(first_add=("add", "min"), first_purchase=("buy", "min")))
carts = s[s.first_add.notna()]
abandoned = int(carts.first_purchase.isna().sum())
anomaly = int((carts.first_purchase < carts.first_add).sum())
want = pd.DataFrame({"carts": [len(carts)], "abandoned": [abandoned],
                     "abandonment_rate": [round(abandoned / len(carts), 4)],
                     "purchase_before_add": [anomaly], "anomaly_rate": [round(anomaly / len(carts), 4)]})
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
assert (ex.iloc[0].tolist() == got[["carts", "abandoned", "purchase_before_add"]].iloc[0].tolist())
print("assert passed: one-row result equal in SQL (CASE and EXISTS) and pandas; 8 sessions, 6 with an add_to_cart")
```

**Output (my run):**
```text
 carts  abandoned  abandonment_rate  purchase_before_add  anomaly_rate
     6          2            0.3333                    1        0.1667

EXISTS version
 carts  abandoned  purchase_before_add
     6          2                    1

pandas
 carts  abandoned  abandonment_rate  purchase_before_add  anomaly_rate
     6          2            0.3333                    1        0.1667
assert passed: one-row result equal in SQL (CASE and EXISTS) and pandas; 8 sessions, 6 with an add_to_cart
```

**Edge cases:**
- **Denominator:** only sessions with an add; including s6 and s7 would give 2 / 8 = 0.25, a different metric.
- **Repeat adds:** `MIN` per session means a session counts once.
- **Purchase before add (s4):** it has a purchase, so it is not abandoned under this definition; it is a separate anomaly, probably clock skew or missing events, and I report it rather than fix it.
- **Ties:** equal timestamps are not "before" (strict `<`).
- **Purchase between adds (s5):** a later add after the purchase is allowed; the first-add rule ignores it.
- **Timestamps as text:** the same-format ISO text compares correctly; mixed formats would not.

**Then explain:**
- **Two equivalent forms:** conditional aggregation over a per-session CTE (above) or `EXISTS` for the purchase test; the EXISTS output matches (printed). I would pick the CTE when I also need the anomaly, as it computes both in one pass.
- **pandas:** put the timestamp in two helper columns with `where`, `groupby.agg(min)`, then boolean sums. `min` ignores NaN, like SQL `MIN`.
- **Say aloud:** abandonment means no purchase in the same session, not within some time window (Part 8 Q27).
- **Scoring note (Set E2, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: 6 carts, 2 abandoned (0.3333), 1 anomaly (0.1667) with the denominator stated. Partial: right abandoned count on all 8 sessions as the denominator, or the anomaly missing, is partial.

**Follow-ups:**
- *What about a time window?* Count a purchase only if it falls within, say, 24 hours of the first add; then the test becomes a timestamp difference, not just IS NULL (date arithmetic differs by engine, not executed here).
- *How do you quantify the anomaly?* Report it separately and check the instrumentation before cleaning.

**Common mistakes:**
- Using all sessions as the denominator.
- Counting events instead of sessions (s3 would count twice).
- Treating purchase-before-add as a normal conversion without a flag.

