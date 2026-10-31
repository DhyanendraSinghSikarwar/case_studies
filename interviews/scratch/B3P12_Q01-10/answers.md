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
