### Q21 ⭐⭐ 🟡 Number of streaks per user: logins(user_id, login_date). Return per user the number of separate streaks, the average streak length, the longest and the number of streaks of at least 3 days, from one island CTE. Show why COUNT(DISTINCT island_key) alone is wrong without the user in the grouping (the key can repeat across users) and how a user with a single login behaves.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** Dedupe to one row per user and date, number each user's dates, subtract the number from the date to get an island key, group by user AND key to get one row per streak, then aggregate those streak rows per user (count, average, max, count of length at least 3).

**Schema and sample data:** fifteen login rows for five users, inserted out of date order on purpose. User 1 has dates 1, 2, 3, 5, 7, 8 January (streaks of 3, 1 and 2 days). User 2 has 1, 2, 3 January with 3 January duplicated. User 3 has a single login. User 4 has four consecutive days. User 5 has only a NULL date. Users 1 and 2 both start on 1 January, so they get the same island key, which is the trap.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-01-08'),(1,'2024-01-01'),(1,'2024-01-03'),(1,'2024-01-02'),(1,'2024-01-05'),(1,'2024-01-07'),
 (2,'2024-01-01'),(2,'2024-01-02'),(2,'2024-01-03'),(2,'2024-01-03'),
 (3,'2024-01-10'),
 (4,'2024-01-20'),(4,'2024-01-21'),(4,'2024-01-22'),(4,'2024-01-23'),
 (5,NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block. The island CTE `isl` has one row per (user, streak); the final SELECT is a plain GROUP BY on that CTE. Date arithmetic uses `date(login_date, '-' || rn || ' days')`, which yields an ISO date as the key.
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), n AS (
  SELECT user_id, login_date,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
  FROM d
), isl AS (
  SELECT user_id,
         date(login_date, '-' || rn || ' days') AS island_key,
         COUNT(*) AS len
  FROM n
  GROUP BY user_id, island_key
)
SELECT user_id,
       COUNT(*) AS streaks,
       ROUND(AVG(len), 2) AS avg_len,
       MAX(len) AS longest,
       SUM(len >= 3) AS streaks_3plus
FROM isl
GROUP BY user_id
ORDER BY user_id
```

**pandas answer:** identical logic, shown once here and the same text as in the Code block:
```py
d = logins.dropna(subset=["login_date"]).drop_duplicates()
d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["user_id", "login_date"])
d["rn"] = d.groupby("user_id").cumcount() + 1
d["island_key"] = d["login_date"] - pd.to_timedelta(d["rn"], unit="D")
isl = d.groupby(["user_id", "island_key"]).size().rename("len").reset_index()
pd_df = (isl.groupby("user_id")["len"]
            .agg(streaks="size", avg_len="mean", longest="max", streaks_3plus=lambda s: int((s >= 3).sum()))
            .round(2).reset_index())
```

**Example:** sorted and deduplicated, user 1 has dates 01, 02, 03, 05, 07, 08 with row numbers 1 to 6. Date minus row number gives 2023-12-31, 2023-12-31, 2023-12-31, 2024-01-01, 2024-01-02, 2024-01-02. Three distinct keys mean three streaks of lengths 3, 1 and 2, so streaks = 3, average = 6/3 = 2.0, longest = 3, streaks of at least 3 days = 1. User 2 (after dropping the duplicate) is 01, 02, 03 with a single key, so one streak of 3. User 3 has one row, key 2024-01-09, one streak of length 1, average 1.0, longest 1, zero long streaks. User 4 is one streak of 4. User 5 has no usable date, so no row at all.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas frames after sorting both by `user_id`. The last query checks day-number arithmetic over a recursive-CTE date spine.
```python
# Q21: streaks per user from one island CTE (count, average, longest, at least 3), with duplicates, NULLs, unsorted input
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-01-08'),(1,'2024-01-01'),(1,'2024-01-03'),(1,'2024-01-02'),(1,'2024-01-05'),(1,'2024-01-07'),
 (2,'2024-01-01'),(2,'2024-01-02'),(2,'2024-01-03'),(2,'2024-01-03'),
 (3,'2024-01-10'),
 (4,'2024-01-20'),(4,'2024-01-21'),(4,'2024-01-22'),(4,'2024-01-23'),
 (5,NULL);
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), n AS (
  SELECT user_id, login_date,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
  FROM d
), isl AS (
  SELECT user_id,
         date(login_date, '-' || rn || ' days') AS island_key,
         COUNT(*) AS len
  FROM n
  GROUP BY user_id, island_key
)
SELECT user_id,
       COUNT(*) AS streaks,
       ROUND(AVG(len), 2) AS avg_len,
       MAX(len) AS longest,
       SUM(len >= 3) AS streaks_3plus
FROM isl
GROUP BY user_id
ORDER BY user_id
"""
SQL_KEYS = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL),
n AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM d)
SELECT user_id, login_date, rn, date(login_date, '-' || rn || ' days') AS island_key
FROM n ORDER BY user_id, login_date
"""
SQL_WRONG_KEYONLY = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL),
n AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM d),
isl AS (SELECT date(login_date, '-' || rn || ' days') AS island_key, COUNT(*) AS len, COUNT(DISTINCT user_id) AS users_merged
        FROM n GROUP BY island_key)
SELECT island_key, len, users_merged FROM isl ORDER BY island_key
"""
SQL_WRONG_DISTINCT = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL),
n AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM d)
SELECT COUNT(DISTINCT date(login_date, '-' || rn || ' days')) AS distinct_keys_all_users,
       (SELECT COUNT(*) FROM (SELECT DISTINCT user_id, date(login_date, '-' || rn || ' days') FROM n)) AS true_streaks_all_users
FROM n
"""
SQL_NODEDUP = """
WITH n AS (
  SELECT user_id, login_date,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
  FROM logins WHERE login_date IS NOT NULL
)
SELECT user_id, COUNT(DISTINCT date(login_date, '-' || rn || ' days')) AS keys_without_dedupe
FROM n GROUP BY user_id ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer:")
print(sql_df.to_string(index=False))
print("island keys per login (user 1 and user 2 share the key 2023-12-31):")
print(pd.read_sql_query(SQL_KEYS, con).to_string(index=False))
print("wrong 1, island grouped by key only:")
print(pd.read_sql_query(SQL_WRONG_KEYONLY, con).to_string(index=False))
print("wrong 2, COUNT(DISTINCT key) over all users:")
print(pd.read_sql_query(SQL_WRONG_DISTINCT, con).to_string(index=False))
print("wrong 3, no DISTINCT on (user, date), user 2 has a duplicate date:")
print(pd.read_sql_query(SQL_NODEDUP, con).to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
d = logins.dropna(subset=["login_date"]).drop_duplicates()
d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["user_id", "login_date"])
d["rn"] = d.groupby("user_id").cumcount() + 1
d["island_key"] = d["login_date"] - pd.to_timedelta(d["rn"], unit="D")
isl = d.groupby(["user_id", "island_key"]).size().rename("len").reset_index()
pd_df = (isl.groupby("user_id")["len"]
            .agg(streaks="size", avg_len="mean", longest="max", streaks_3plus=lambda s: int((s >= 3).sum()))
            .round(2).reset_index())
# pd:end
print("pandas answer:")
print(pd_df.to_string(index=False))
a = sql_df.sort_values("user_id").reset_index(drop=True)
b = pd_df.sort_values("user_id").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)  # compared after sorting both by user_id

# edge: a user with no logins at all (or only a NULL date, user 5) has no row; join from users to get 0
print("user 5 (only a NULL date) in result:", 5 in set(sql_df["user_id"]))

# day numbers: julianday (float) versus unixepoch (integer seconds) over a recursive-CTE date spine of 40001 consecutive days
chk = con.execute("""
WITH RECURSIVE sp(d) AS (SELECT '1900-01-01' UNION ALL SELECT date(d, '+1 day') FROM sp WHERE d < '2009-06-16'),
n AS (SELECT d, ROW_NUMBER() OVER (ORDER BY d) AS rn FROM sp)
SELECT COUNT(*), MIN(d), MAX(d),
       COUNT(DISTINCT julianday(d) - rn),
       COUNT(DISTINCT CAST(julianday(d) AS INTEGER) - rn),
       COUNT(DISTINCT date(d, '-' || rn || ' days'))
FROM n""").fetchone()
print("spine rows, first, last, distinct keys by julianday(d)-rn, by CAST(julianday) - rn, by date(d, -rn days):", chk)
print("asserts passed")
```

**Output (my run):**
```text
SQL answer:
 user_id  streaks  avg_len  longest  streaks_3plus
       1        3      2.0        3              1
       2        1      3.0        3              1
       3        1      1.0        1              0
       4        1      4.0        4              1
island keys per login (user 1 and user 2 share the key 2023-12-31):
 user_id login_date  rn island_key
       1 2024-01-01   1 2023-12-31
       1 2024-01-02   2 2023-12-31
       1 2024-01-03   3 2023-12-31
       1 2024-01-05   4 2024-01-01
       1 2024-01-07   5 2024-01-02
       1 2024-01-08   6 2024-01-02
       2 2024-01-01   1 2023-12-31
       2 2024-01-02   2 2023-12-31
       2 2024-01-03   3 2023-12-31
       3 2024-01-10   1 2024-01-09
       4 2024-01-20   1 2024-01-19
       4 2024-01-21   2 2024-01-19
       4 2024-01-22   3 2024-01-19
       4 2024-01-23   4 2024-01-19
wrong 1, island grouped by key only:
island_key  len  users_merged
2023-12-31    6             2
2024-01-01    1             1
2024-01-02    2             1
2024-01-09    1             1
2024-01-19    4             1
wrong 2, COUNT(DISTINCT key) over all users:
 distinct_keys_all_users  true_streaks_all_users
                       5                       6
wrong 3, no DISTINCT on (user, date), user 2 has a duplicate date:
 user_id  keys_without_dedupe
       1                    3
       2                    2
       3                    1
       4                    1
pandas answer:
 user_id  streaks  avg_len  longest  streaks_3plus
       1        3      2.0        3              1
       2        1      3.0        3              1
       3        1      1.0        1              0
       4        1      4.0        4              1
user 5 (only a NULL date) in result: False
spine rows, first, last, distinct keys by julianday(d)-rn, by CAST(julianday) - rn, by date(d, -rn days): (39979, '1900-01-01', '2009-06-16', 1, 1, 1)
asserts passed
```

**Edge cases:**
- Wrong answer 1, island grouped by key only: the key `2023-12-31` is produced by both user 1 and user 2, so grouping by key alone merges them into one 6-day island with `users_merged = 2` in my run. The key is only unique inside a user, so the user must be in the GROUP BY (and in the PARTITION BY of the ROW_NUMBER).
- Wrong answer 2, `COUNT(DISTINCT island_key)` over all users: 5 in my run, but the real number of (user, streak) pairs is 6, because the shared key is counted once. Per user it happens to be correct only when you also `GROUP BY user_id`.
- Wrong answer 3, no dedupe: user 2's duplicated 3 January takes row numbers 3 and 4, so its key moves by one day and the 3-day streak is counted as two keys (2 in my run instead of 1). `SELECT DISTINCT user_id, login_date` first, or use DENSE_RANK on the date.
- Single login (user 3): one island, `streaks = 1`, average 1.0, longest 1, `streaks_3plus = 0`. The window functions need no special case.
- NULL dates: user 5 vanishes from the result. If every user must appear (with 0 streaks), LEFT JOIN from a users table and wrap the counts in COALESCE.
- Unsorted input is harmless because both ROW_NUMBER and pandas `sort_values` order by date first.
- The streak definition is consecutive calendar days with at least one login each; I assume dates are plain days with no time zone shift.
- Day numbers: over a recursive-CTE date spine of 39,979 consecutive days (1900-01-01 to 2009-06-16) `julianday(d) - rn`, `CAST(julianday(d) AS INTEGER) - rn` and `date(d, '-' || rn || ' days')` each produced exactly one distinct key. Date-only values give half-integer Julian day numbers, which floats store exactly, so the subtraction is safe for dates. For timestamps with a time of day it is not (see Q25); take the date part first.

**Then explain:**
- A run of consecutive days has date and row number rising together, so their difference is constant inside a run and jumps when a day is skipped.
- Build the island CTE once and aggregate it twice (per island, then per user) instead of nesting subqueries; that is what "from one island CTE" means.
- Average streak length is the average of per-streak lengths (2.0 for user 1), not total logins divided by days.
- `SUM(len >= 3)` works in SQLite because a comparison returns 0 or 1. `COUNT(*) FILTER (WHERE len >= 3)` also runs on SQLite 3.45 (I ran a probe), and PostgreSQL accepts it too (not executed here); MySQL has no FILTER, so the portable form is `SUM(CASE WHEN len >= 3 THEN 1 ELSE 0 END)`. PostgreSQL also allows `login_date - rn::int` on a DATE, and MySQL uses `DATE_SUB(login_date, INTERVAL rn DAY)` (not executed here).
- The 'at least N' filter is the pattern of Q9 (LeetCode 1454); the general-N follow-up only changes the threshold.

**Follow-ups:**
- Current streak (the island that contains the as-of date)? Filter islands by `end_date = as_of`, as in Q15.
- Longest streak per user with the dates? Add MIN and MAX of login_date to the island CTE (Q7). Duplicates debugging is Q8.
- Users with no logins? LEFT JOIN from users and COALESCE to 0.

**Common mistakes:**
- Forgetting `PARTITION BY user_id` in ROW_NUMBER, so row numbers run across users.
- Grouping islands by the key alone (shown: 6-day island merging two users).
- Not deduplicating (user, date) pairs.
- Using `COUNT(DISTINCT key)` as the streak count without the user in the grouping.
- Using `RANK` on dates, which leaves gaps when dates tie.

### Q22 ⭐⭐ 🟡 Longest Winning Streak (LeetCode 2173): matches(player_id, match_day, result) with result 'Win', 'Draw' or 'Lose'. Return each player's longest streak of consecutive wins (a draw or loss ends a streak), including 0 for players with no wins. Show the running count of non-wins method, the two ROW_NUMBER difference method, and why a LEFT JOIN from the players is needed so players without wins keep a row.
**Asked at:** public LeetCode-style problem bank (statements known from search snippets and mirrors such as doocs, walkccc and talentd; the leetcode.com pages returned HTTP 403 and were not opened), not candidate reports; analyst, data scientist and data engineer screens at product companies and GCCs
**Say this first (1 line):** Order each player's matches by day, keep a running count of non-wins (a draw, a loss or an unknown result), so every win in the same streak shares one count; count wins per (player, running count), take the max per player, and LEFT JOIN from the list of players with COALESCE to 0.

**Schema and sample data:** seventeen match rows, five players, one player per interesting case. Player 1: W, W, W, Draw, W (longest 3). Player 2: only losses (0). Player 3: inserted out of order, sorted it is W, L, W, W, W, W, with a large calendar gap before the last win (longest 4; the streak is about consecutive matches, not consecutive days). Player 4: a single win. Player 5: Win, NULL result, Win. I assume `(player_id, match_day)` is unique, as in the LeetCode statement.
```sql
CREATE TABLE matches(player_id INTEGER, match_day TEXT, result TEXT);
INSERT INTO matches VALUES
 (1,'2022-01-17','Win'),(1,'2022-01-18','Win'),(1,'2022-01-25','Win'),(1,'2022-01-31','Draw'),(1,'2022-02-08','Win'),
 (2,'2022-02-06','Lose'),(2,'2022-02-08','Lose'),
 (3,'2022-03-30','Win'),(3,'2022-03-01','Win'),(3,'2022-03-02','Lose'),(3,'2022-03-04','Win'),(3,'2022-03-05','Win'),(3,'2022-03-06','Win'),
 (4,'2022-04-01','Win'),
 (5,'2022-05-01','Win'),(5,'2022-05-02',NULL),(5,'2022-05-03','Win');
```

**SQL answer:** `SQL_MAIN` in the Code block is the running count of non-wins method. `SQL_RN` is the two ROW_NUMBER method (a row number over all of a player's matches minus a row number inside the player's matches of the same result).
```sql
WITH players AS (
  SELECT DISTINCT player_id FROM matches
), r AS (
  SELECT player_id, match_day, result,
         SUM(result IS NOT 'Win') OVER (
           PARTITION BY player_id ORDER BY match_day
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS non_wins_so_far
  FROM matches
), streaks AS (
  SELECT player_id, non_wins_so_far, COUNT(*) AS streak_len
  FROM r
  WHERE result = 'Win'
  GROUP BY player_id, non_wins_so_far
)
SELECT p.player_id, COALESCE(MAX(s.streak_len), 0) AS longest_streak
FROM players p
LEFT JOIN streaks s ON s.player_id = p.player_id
GROUP BY p.player_id
ORDER BY p.player_id
```
`SQL_RN` in the Code block replaces the running count with `ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_day) - ROW_NUMBER() OVER (PARTITION BY player_id, result ORDER BY match_day)` and groups the `result = 'Win'` rows by that difference.

**pandas answer:** same logic as the first method, identical to the Code block:
```py
mm = matches.sort_values(["player_id", "match_day"]).reset_index(drop=True)
mm["is_win"] = mm["result"].eq("Win")
mm["non_wins_so_far"] = (~mm["is_win"]).astype(int).groupby(mm["player_id"]).cumsum()
runs = (mm[mm["is_win"]].groupby(["player_id", "non_wins_so_far"]).size()
          .groupby("player_id").max())
pd_df = (runs.reindex(mm["player_id"].unique(), fill_value=0)
             .rename_axis("player_id").rename("longest_streak").reset_index())
```

**Example:** player 3 sorted: 03-01 W, 03-02 L, 03-04 W, 03-05 W, 03-06 W, 03-30 W. Non-wins so far: 0, 1, 1, 1, 1, 1. Wins with count 0: one (03-01). Wins with count 1: four (03-04, 03-05, 03-06, 03-30), so the longest is 4. Player 1: wins at counts 0, 0, 0 (three wins), the draw makes the count 1, and the last win has count 1 alone, so 3. Player 2 has no win rows, so it vanishes from the streak CTE and only the LEFT JOIN plus COALESCE brings it back as 0. By the two row number method for player 3: row number over all matches 1..6, row number among wins 1, 2, 3, 4, 5 for the five wins, differences 0 for the first win and 1, 1, 1, 1 for the four others (rows 3, 4, 5, 6 minus 2, 3, 4, 5), the same split.

**Code:** run with `python3 -I`. Both SQL methods are asserted equal, then pandas is asserted equal to SQL after sorting both by `player_id`.
```python
# Q22: longest winning streak (LeetCode 2173 pattern): running count of non-wins vs two ROW_NUMBERs, LEFT JOIN for zero-win players
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE matches(player_id INTEGER, match_day TEXT, result TEXT);
INSERT INTO matches VALUES
 (1,'2022-01-17','Win'),(1,'2022-01-18','Win'),(1,'2022-01-25','Win'),(1,'2022-01-31','Draw'),(1,'2022-02-08','Win'),
 (2,'2022-02-06','Lose'),(2,'2022-02-08','Lose'),
 (3,'2022-03-30','Win'),(3,'2022-03-01','Win'),(3,'2022-03-02','Lose'),(3,'2022-03-04','Win'),(3,'2022-03-05','Win'),(3,'2022-03-06','Win'),
 (4,'2022-04-01','Win'),
 (5,'2022-05-01','Win'),(5,'2022-05-02',NULL),(5,'2022-05-03','Win');
"""
SQL_MAIN = """
WITH players AS (
  SELECT DISTINCT player_id FROM matches
), r AS (
  SELECT player_id, match_day, result,
         SUM(result IS NOT 'Win') OVER (
           PARTITION BY player_id ORDER BY match_day
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS non_wins_so_far
  FROM matches
), streaks AS (
  SELECT player_id, non_wins_so_far, COUNT(*) AS streak_len
  FROM r
  WHERE result = 'Win'
  GROUP BY player_id, non_wins_so_far
)
SELECT p.player_id, COALESCE(MAX(s.streak_len), 0) AS longest_streak
FROM players p
LEFT JOIN streaks s ON s.player_id = p.player_id
GROUP BY p.player_id
ORDER BY p.player_id
"""
SQL_RN = """
WITH players AS (
  SELECT DISTINCT player_id FROM matches
), r AS (
  SELECT player_id, match_day, result,
         ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_day) AS rn_all,
         ROW_NUMBER() OVER (PARTITION BY player_id, result ORDER BY match_day) AS rn_res
  FROM matches
), streaks AS (
  SELECT player_id, rn_all - rn_res AS grp, COUNT(*) AS streak_len
  FROM r
  WHERE result = 'Win'
  GROUP BY player_id, rn_all - rn_res
)
SELECT p.player_id, COALESCE(MAX(s.streak_len), 0) AS longest_streak
FROM players p
LEFT JOIN streaks s ON s.player_id = p.player_id
GROUP BY p.player_id
ORDER BY p.player_id
"""
SQL_INNER = """
WITH r AS (
  SELECT player_id, match_day, result,
         SUM(result IS NOT 'Win') OVER (PARTITION BY player_id ORDER BY match_day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS g
  FROM matches
), streaks AS (SELECT player_id, g, COUNT(*) AS streak_len FROM r WHERE result = 'Win' GROUP BY player_id, g)
SELECT player_id, MAX(streak_len) AS longest_streak FROM streaks GROUP BY player_id ORDER BY player_id
"""
SQL_NEQ = """
WITH r AS (
  SELECT player_id, match_day, result,
         SUM(result <> 'Win') OVER (PARTITION BY player_id ORDER BY match_day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS g
  FROM matches
), streaks AS (SELECT player_id, g, COUNT(*) AS streak_len FROM r WHERE result = 'Win' GROUP BY player_id, g)
SELECT player_id, MAX(streak_len) AS longest_streak FROM streaks GROUP BY player_id ORDER BY player_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
m1 = pd.read_sql_query(SQL_MAIN, con)
m2 = pd.read_sql_query(SQL_RN, con)
print("method 1, running count of non-wins:")
print(m1.to_string(index=False))
print("method 2, two ROW_NUMBERs:")
print(m2.to_string(index=False))
assert m1.equals(m2)
print("wrong 1, INNER JOIN style (players 2 has no row):")
print(pd.read_sql_query(SQL_INNER, con).to_string(index=False))
print("wrong 2, result <> 'Win' with a NULL result (player 5 shows 2 instead of 1):")
print(pd.read_sql_query(SQL_NEQ, con).to_string(index=False))

matches = pd.read_sql_query("SELECT * FROM matches", con)
# pd:main
mm = matches.sort_values(["player_id", "match_day"]).reset_index(drop=True)
mm["is_win"] = mm["result"].eq("Win")
mm["non_wins_so_far"] = (~mm["is_win"]).astype(int).groupby(mm["player_id"]).cumsum()
runs = (mm[mm["is_win"]].groupby(["player_id", "non_wins_so_far"]).size()
          .groupby("player_id").max())
pd_df = (runs.reindex(mm["player_id"].unique(), fill_value=0)
             .rename_axis("player_id").rename("longest_streak").reset_index())
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(m1.sort_values("player_id").reset_index(drop=True),
                              pd_df.sort_values("player_id").reset_index(drop=True), check_dtype=False)  # sorted by player_id
print("asserts passed")
```

**Output (my run):**
```text
method 1, running count of non-wins:
 player_id  longest_streak
         1               3
         2               0
         3               4
         4               1
         5               1
method 2, two ROW_NUMBERs:
 player_id  longest_streak
         1               3
         2               0
         3               4
         4               1
         5               1
wrong 1, INNER JOIN style (players 2 has no row):
 player_id  longest_streak
         1               3
         3               4
         4               1
         5               1
wrong 2, result <> 'Win' with a NULL result (player 5 shows 2 instead of 1):
 player_id  longest_streak
         1               3
         3               4
         4               1
         5               2
pandas:
 player_id  longest_streak
         1               3
         2               0
         3               4
         4               1
         5               1
asserts passed
```

**Edge cases:**
- Players with no wins (player 2) disappear from any query that filters to wins. The INNER JOIN style (`SQL_INNER`) printed four rows in my run and lost player 2. LEFT JOIN from the players plus `COALESCE(MAX(streak_len), 0)` keeps the 0. There is no players table in the LeetCode statement, so I derive it with `SELECT DISTINCT player_id FROM matches`; a player with no matches at all is not in the data and cannot be returned.
- NULL result (player 5): with `result IS NOT 'Win'` the NULL counts as a streak breaker and the longest streak is 1. With `result <> 'Win'` the comparison is NULL, the SUM ignores it, the NULL row does not break the streak and the answer wrongly shows 2 (my run). State the rule: an unknown result is not a win.
- Ties on `match_day` for one player make the order arbitrary and the answer can change; the LeetCode problem guarantees unique days, otherwise add a match id to the ORDER BY.
- Unsorted input is fine; both methods order inside the window.
- A single-row player (player 4) gives streak 1 with a win and 0 with anything else.
- Gaps in calendar days do not break a streak here (player 3). If days without a match should break it, that is a different problem (add a calendar-day check as in Q6).

**Then explain:**
- A running count of non-wins is a streak label: it stays constant while wins continue and increments on each break.
- The two ROW_NUMBER difference only works if the compared rows are sorted the same way; here both use `match_day`, once over everything and once inside a result. Row numbers inside the 'Draw' or 'Lose' partitions are computed too but filtered away.
- The running count method needs one window and tolerates several result values naturally, which is why I prefer it; the two row number method generalises to "runs of the same result" when you drop the `WHERE result = 'Win'` filter.
- `SUM(result IS NOT 'Win')` relies on SQLite booleans being 0 or 1. The portable form is `SUM(CASE WHEN result = 'Win' THEN 0 ELSE 1 END)`. `IS NOT` with a string works in SQLite; PostgreSQL would use `IS DISTINCT FROM 'Win'` (not executed here).
- The LeetCode 2173 page returned HTTP 403 for Wave A, so the statement is as known from mirrors; I did not check the exact output order.

**Follow-ups:**
- Longest losing streak or longest streak of any result? Drop the filter and group by result too.
- Also return the start and end days? Add MIN and MAX of `match_day` to the streak CTE.
- Current winning streak? Take the streak that contains the player's latest match.

**Common mistakes:**
- INNER JOIN or filtering wins and losing the players without wins.
- Using `<>` and silently letting NULL results extend a streak.
- Subtracting row numbers that are not partitioned by player.
- Counting calendar days instead of matches.
- Taking `MAX(non_wins_so_far)` as the streak length instead of counting wins per group.

### Q23 ⭐⭐ 🟡 Stock up-streaks: prices(day, close) with one row per trading day, ISO dates, some NULL closes and some unchanged closes. Return the longest run of consecutive rising days (close > previous close), with its start and end day, and each up-streak of at least 3 days. Decide how a flat day and a NULL close break the streak, use LAG with a flag (up = 1 else 0) and the group-by-non-up running count, and say why calendar gaps (weekends) are not gaps here.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Order by day, flag a row as up only when `close > LAG(close)`, so a flat day, a drop, a NULL close and the first row all get 0, then label streaks with the running count of non-up rows and aggregate the up rows per label; calendar gaps do not matter because consecutive rows, not consecutive dates, define the sequence.

**Schema and sample data:** fifteen trading-day rows inserted partly out of order, ISO dates, `close` REAL. Rows jump from Friday to Monday (03-08 to 03-11, 03-15 to 03-18, 03-22 ends the data). 03-11 is flat (104 after 104), 03-13 is NULL, 03-20 is a drop. Rules I assume: a day is up only when its close and the previous row's close are both non-NULL and strictly higher; the day after a NULL close cannot be judged, so it is not up. The alternative (carry the last known close forward) is mentioned below.
```sql
CREATE TABLE prices(day TEXT, close REAL);
INSERT INTO prices VALUES
 ('2024-03-08',104),('2024-03-04',100),('2024-03-05',101),('2024-03-06',102),('2024-03-07',103),
 ('2024-03-11',104),('2024-03-12',105),('2024-03-13',NULL),('2024-03-14',105),('2024-03-15',106),
 ('2024-03-18',107),('2024-03-19',108),('2024-03-20',107),('2024-03-21',108),('2024-03-22',109);
```

**SQL answer:** `SQL_MAIN` in the Code block (it is the CTE chain `FLAGS` followed by the final SELECT). The streak length is the number of up days; the `start_day` is the first rising day, so the closing price on the day before it is the base.
```sql
WITH f AS (
  SELECT day, close,
         LAG(close) OVER (ORDER BY day) AS prev_close,
         CASE WHEN close > LAG(close) OVER (ORDER BY day) THEN 1 ELSE 0 END AS up
  FROM prices
), g AS (
  SELECT *, SUM(1 - up) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM f
)

SELECT MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS up_days
FROM g
WHERE up = 1
GROUP BY grp
HAVING COUNT(*) >= 3
ORDER BY start_day
```
`SQL_LONGEST` (Code block) returns the longest run and keeps all ties by comparing to `MAX(up_days)`.

**pandas answer:** identical to the Code block:
```py
p = prices.assign(day=pd.to_datetime(prices["day"])).sort_values("day").reset_index(drop=True)
p["up"] = p["close"].gt(p["close"].shift())
p["grp"] = (~p["up"]).cumsum()
pd_all = (p[p["up"]].groupby("grp")
            .agg(start_day=("day", "min"), end_day=("day", "max"), up_days=("day", "size"))
            .reset_index(drop=True))
pd_df = pd_all[pd_all["up_days"] >= 3].reset_index(drop=True)
```

**Example:** flags per row from the run: 03-04 first row (no previous, up 0), 03-05 to 03-08 up (101, 102, 103, 104 each above the previous), 03-11 flat so 0, 03-12 up (105 above 104), 03-13 NULL so 0, 03-14 follows the NULL so 0, 03-15 to 03-19 up (106, 107, 108 each above the previous: three days; 03-18 and 03-19 are Monday and Tuesday after the weekend), 03-20 down 0, 03-21 and 03-22 up. The running count of non-up rows (grp) is 1 for the first block, 2 for 03-11 and 03-12, 3 for 03-13, 4 for 03-14 to 03-19 and 5 from 03-20. Up rows grouped by grp: 4 days (03-05 to 03-08), 1 day (03-12), 3 days (03-15 to 03-19), 2 days (03-21 to 03-22). At least 3 days gives the first and third; the longest is the first with 4 up days (five closes).

**Code:** run with `python3 -I`. The assert compares the SQL and pandas streaks of at least 3 after sorting by `start_day`.
```python
# Q23: stock up-streaks with NULL closes, flat days, weekends; LAG flag + running count of non-up rows
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE prices(day TEXT, close REAL);
INSERT INTO prices VALUES
 ('2024-03-08',104),('2024-03-04',100),('2024-03-05',101),('2024-03-06',102),('2024-03-07',103),
 ('2024-03-11',104),('2024-03-12',105),('2024-03-13',NULL),('2024-03-14',105),('2024-03-15',106),
 ('2024-03-18',107),('2024-03-19',108),('2024-03-20',107),('2024-03-21',108),('2024-03-22',109);
"""
FLAGS = """
WITH f AS (
  SELECT day, close,
         LAG(close) OVER (ORDER BY day) AS prev_close,
         CASE WHEN close > LAG(close) OVER (ORDER BY day) THEN 1 ELSE 0 END AS up
  FROM prices
), g AS (
  SELECT *, SUM(1 - up) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM f
)
"""
SQL_MAIN = FLAGS + """
SELECT MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS up_days
FROM g
WHERE up = 1
GROUP BY grp
HAVING COUNT(*) >= 3
ORDER BY start_day
"""
SQL_LONGEST = FLAGS + """
, s AS (SELECT grp, MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS up_days FROM g WHERE up = 1 GROUP BY grp)
SELECT start_day, end_day, up_days FROM s WHERE up_days = (SELECT MAX(up_days) FROM s) ORDER BY start_day
"""
SQL_ALL = FLAGS + """
SELECT MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS up_days
FROM g WHERE up = 1 GROUP BY grp ORDER BY start_day
"""
SQL_DETAIL = FLAGS + "SELECT day, close, prev_close, up, grp FROM g ORDER BY day"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("flags per row:")
print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL, streaks of at least 3 up days:")
print(sql_df.to_string(index=False))
print("SQL, every up-streak:")
print(pd.read_sql_query(SQL_ALL, con).to_string(index=False))
print("SQL, longest (ties all returned):")
print(pd.read_sql_query(SQL_LONGEST, con).to_string(index=False))

prices = pd.read_sql_query("SELECT * FROM prices", con)
# pd:main
p = prices.assign(day=pd.to_datetime(prices["day"])).sort_values("day").reset_index(drop=True)
p["up"] = p["close"].gt(p["close"].shift())
p["grp"] = (~p["up"]).cumsum()
pd_all = (p[p["up"]].groupby("grp")
            .agg(start_day=("day", "min"), end_day=("day", "max"), up_days=("day", "size"))
            .reset_index(drop=True))
pd_df = pd_all[pd_all["up_days"] >= 3].reset_index(drop=True)
# pd:end
out = pd_df.assign(start_day=pd_df["start_day"].dt.strftime("%Y-%m-%d"), end_day=pd_df["end_day"].dt.strftime("%Y-%m-%d"))
print("pandas, at least 3:")
print(out.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.sort_values("start_day").reset_index(drop=True),
                              out.sort_values("start_day").reset_index(drop=True), check_dtype=False)  # sorted by start_day
# the longest in pandas, ties kept
longest = pd_all[pd_all["up_days"] == pd_all["up_days"].max()]
print("pandas longest rows:", len(longest), "up_days", int(longest["up_days"].iloc[0]))

# edge: an exact duplicate row for the same day looks like a flat day and breaks a streak
con.execute("INSERT INTO prices VALUES ('2024-03-06',102)")
print("after inserting a duplicate 2024-03-06 row:")
print(pd.read_sql_query(SQL_MAIN, con).to_string(index=False))
con.execute("DELETE FROM prices WHERE rowid IN (SELECT MAX(rowid) FROM prices)")
# edge: shift on an integer column upcasts to float64
s = pd.Series([1, 2, 3])
print("int shift dtype:", s.dtype, "->", s.shift().dtype, "; with fill_value=0:", s.shift(fill_value=0).dtype)
print("NaN > anything is False:", float("nan") > 1, pd.Series([1.0, float("nan")]).gt(0.5).tolist())
# edge: empty and single row
con.execute("DELETE FROM prices WHERE day <> '2024-03-04'")
print("single row, SQL rows:", len(pd.read_sql_query(SQL_ALL, con)))
print("asserts passed")
```

**Output (my run):**
```text
flags per row:
       day  close  prev_close  up  grp
2024-03-04  100.0         NaN   0    1
2024-03-05  101.0       100.0   1    1
2024-03-06  102.0       101.0   1    1
2024-03-07  103.0       102.0   1    1
2024-03-08  104.0       103.0   1    1
2024-03-11  104.0       104.0   0    2
2024-03-12  105.0       104.0   1    2
2024-03-13    NaN       105.0   0    3
2024-03-14  105.0         NaN   0    4
2024-03-15  106.0       105.0   1    4
2024-03-18  107.0       106.0   1    4
2024-03-19  108.0       107.0   1    4
2024-03-20  107.0       108.0   0    5
2024-03-21  108.0       107.0   1    5
2024-03-22  109.0       108.0   1    5
SQL, streaks of at least 3 up days:
 start_day    end_day  up_days
2024-03-05 2024-03-08        4
2024-03-15 2024-03-19        3
SQL, every up-streak:
 start_day    end_day  up_days
2024-03-05 2024-03-08        4
2024-03-12 2024-03-12        1
2024-03-15 2024-03-19        3
2024-03-21 2024-03-22        2
SQL, longest (ties all returned):
 start_day    end_day  up_days
2024-03-05 2024-03-08        4
pandas, at least 3:
 start_day    end_day  up_days
2024-03-05 2024-03-08        4
2024-03-15 2024-03-19        3
pandas longest rows: 1 up_days 4
after inserting a duplicate 2024-03-06 row:
 start_day    end_day  up_days
2024-03-15 2024-03-19        3
int shift dtype: int64 -> float64 ; with fill_value=0: int64
NaN > anything is False: False [True, False]
single row, SQL rows: 0
asserts passed
```

**Edge cases:**
- Flat day: `close > prev` is false, so a flat day ends the streak (03-11 in the data). If your business rule says flat does not break a streak ("non-decreasing"), use `>=` and say so.
- NULL close: the comparison is NULL, the CASE falls to ELSE 0, and the next row also compares against NULL so it is 0 too (03-13 and 03-14 both 0). The streak resumes only at 03-15. Forward-filling the last known close would change that; I did not do it, and `LAST_VALUE(close IGNORE NULLS)` is a syntax error in SQLite 3.45.1 (I ran it); other engines support it (not executed here).
- Weekends: the table has one row per trading day, so Friday and Monday are adjacent rows and LAG compares them. A `julianday` difference of 1 would wrongly split every weekend; do not add it here. If the table could miss real trading days (a data gap), that is a data-quality question, not part of this streak definition.
- Exact duplicate rows: after inserting a second `2024-03-06,102` row, the duplicate compares as flat against the original, which breaks the first streak (only the 03-15 streak survives in my run). Deduplicate by day first (`SELECT DISTINCT`, or the latest row per day).
- Ties for the longest: `SQL_LONGEST` returns all of them; `ORDER BY ... LIMIT 1` would silently pick one.
- Single-row table: no up days, no streaks (0 rows in my run). Unsorted input is fine because LAG and the running count sort by day.
- pandas: `shift()` on an integer column upcasts to float64 (int64 to float64 in my run; `fill_value=0` kept int64). A comparison against NaN is False, which matches the SQL NULL rule here.

**Then explain:**
- `LAG(close)` gives the previous row, so up/non-up is a per-row flag; `SUM(1 - up)` counts non-up rows so far, which is constant over a run of up rows.
- The grouping label counts breaks, not days; the up rows of one label are exactly one streak, and the break row itself shares its label with the up rows that follow it (so filter `up = 1` before aggregating).
- The streak is measured in rising days; if you want the number of closes involved, add one and start from the previous day.
- Dialects (not executed here): `IGNORE NULLS` exists in some engines (Oracle, BigQuery, Snowflake as I remember it); the SQL above avoids it.

**Follow-ups:**
- Down-streaks or flat-streaks? Change the flag; the pattern is identical.
- Include the base day in start and end? Take the previous row's day with `LAG(day)` for the first up day.
- Per ticker? Add `ticker` to PARTITION BY and to the GROUP BY.

**Common mistakes:**
- Using `julianday(day) - julianday(prev_day) = 1` and splitting every weekend.
- Treating NULL as 0 or as 'not changed' and letting a streak span a missing close.
- Forgetting to filter `up = 1` before counting, so the break row is counted in the next streak.
- `LIMIT 1` for the longest streak without a tie rule.
- Not removing duplicate rows per day.

### Q24 ⭐⭐ 🟡 Cumulative sum that resets by condition: txns(acct_id, txn_id, amount, is_reset) where a running total restarts at each row with is_reset = 1. Solve with a running SUM of is_reset as the group key and SUM(amount) OVER (PARTITION BY acct_id, group_key ORDER BY txn_id). Then state the harder variant (reset when the running total exceeds a threshold) is order-dependent and cannot be done with one window pass, and point to the recursive CTE answer in Part 9. Cross-reference Part 5 for the running total mechanics.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Turn the reset flag into a group key with a running SUM of `is_reset` (every reset row starts a new group, including itself), then take a running SUM of `amount` partitioned by account and that key; a rule that resets when the running total crosses a threshold depends on its own earlier output, so it needs a recursive CTE (Part 9) or a loop, not one window pass.

**Schema and sample data:** thirteen rows for three accounts, inserted out of order for account 1. Account 1: txn 1 to 7 with resets at txn 4 and txn 6. Account 2: a single row that is itself a reset. Account 3: has NULL amounts (txn 2 and 5) and a NULL `is_reset` (txn 3), and a reset at txn 4. For running total mechanics (frames, ROWS versus RANGE, ties) see Part 5; this question only adds the group key.
```sql
CREATE TABLE txns(acct_id INTEGER, txn_id INTEGER, amount INTEGER, is_reset INTEGER);
INSERT INTO txns VALUES
 (1,3,30,0),(1,1,10,0),(1,2,20,0),(1,4,5,1),(1,5,7,0),(1,6,8,1),(1,7,1,0),
 (2,1,50,1),
 (3,1,9,0),(3,2,NULL,0),(3,3,4,NULL),(3,4,6,1),(3,5,NULL,0);
```

**SQL answer:** `SQL_MAIN` in the Code block. The first window builds `grp`; the second restarts at each new `(acct_id, grp)`. A window function cannot sit inside another window's PARTITION BY (SQLite raised `misuse of window function SUM()` when I tried), so `grp` has to come from a CTE. `COALESCE` makes NULL amounts and NULL flags count as 0.
```sql
WITH k AS (
  SELECT acct_id, txn_id, amount, is_reset,
         SUM(COALESCE(is_reset, 0)) OVER (
           PARTITION BY acct_id ORDER BY txn_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM txns
)
SELECT acct_id, txn_id, amount, is_reset, grp,
       SUM(COALESCE(amount, 0)) OVER (
         PARTITION BY acct_id, grp ORDER BY txn_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_since_reset
FROM k
ORDER BY acct_id, txn_id
```

**pandas answer:** identical to the Code block:
```py
t = txns.sort_values(["acct_id", "txn_id"]).reset_index(drop=True)
t["grp"] = t["is_reset"].fillna(0).astype(int).groupby(t["acct_id"]).cumsum()
t["running_since_reset"] = t["amount"].fillna(0).groupby([t["acct_id"], t["grp"]]).cumsum().astype(int)
```

**Example:** account 1 sorted by txn_id: amounts 10, 20, 30, 5(reset), 7, 8(reset), 1. Running SUM of `is_reset` gives grp 0, 0, 0, 1, 1, 2, 2. Running totals inside each group: 10, 30, 60 | 5, 12 | 8, 9. The reset row restarts with its own amount (5, not 0 and not 65). Account 2: one row, grp 1, total 50. Account 3: amounts 9, NULL, 4, 6(reset), NULL with a NULL flag at txn 3 treated as 0: grp 0, 0, 0, 1, 1; totals 9, 9 (NULL counted as 0), 13, 6, 6.

**Code:** run with `python3 -I`. The assert compares `acct_id, txn_id, grp, running_since_reset` after ordering both by `acct_id, txn_id`. The end of the script runs the threshold variant as a plain loop to show why it is different.
```python
# Q24: cumulative sum that resets at flagged rows (running SUM of is_reset as group key)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE txns(acct_id INTEGER, txn_id INTEGER, amount INTEGER, is_reset INTEGER);
INSERT INTO txns VALUES
 (1,3,30,0),(1,1,10,0),(1,2,20,0),(1,4,5,1),(1,5,7,0),(1,6,8,1),(1,7,1,0),
 (2,1,50,1),
 (3,1,9,0),(3,2,NULL,0),(3,3,4,NULL),(3,4,6,1),(3,5,NULL,0);
"""
SQL_MAIN = """
WITH k AS (
  SELECT acct_id, txn_id, amount, is_reset,
         SUM(COALESCE(is_reset, 0)) OVER (
           PARTITION BY acct_id ORDER BY txn_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM txns
)
SELECT acct_id, txn_id, amount, is_reset, grp,
       SUM(COALESCE(amount, 0)) OVER (
         PARTITION BY acct_id, grp ORDER BY txn_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_since_reset
FROM k
ORDER BY acct_id, txn_id
"""
SQL_RAWNULL = """
WITH k AS (
  SELECT acct_id, txn_id, amount, SUM(COALESCE(is_reset, 0)) OVER (PARTITION BY acct_id ORDER BY txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM txns
)
SELECT acct_id, txn_id, SUM(amount) OVER (PARTITION BY acct_id, grp ORDER BY txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS raw_running
FROM k WHERE acct_id = 3 ORDER BY txn_id
"""
SQL_NOGROUP = """
SELECT acct_id, txn_id, SUM(COALESCE(amount, 0)) OVER (PARTITION BY acct_id ORDER BY txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS plain_running
FROM txns WHERE acct_id = 1 ORDER BY txn_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer:")
print(sql_df.to_string(index=False))
print("raw SUM(amount), NULL amounts, account 3:")
print(pd.read_sql_query(SQL_RAWNULL, con).to_string(index=False))
print("no reset (plain running total), account 1:")
print(pd.read_sql_query(SQL_NOGROUP, con).to_string(index=False))

txns = pd.read_sql_query("SELECT * FROM txns", con)
# pd:main
t = txns.sort_values(["acct_id", "txn_id"]).reset_index(drop=True)
t["grp"] = t["is_reset"].fillna(0).astype(int).groupby(t["acct_id"]).cumsum()
t["running_since_reset"] = t["amount"].fillna(0).groupby([t["acct_id"], t["grp"]]).cumsum().astype(int)
# pd:end
print("pandas answer:")
print(t.to_string(index=False))
cols = ["acct_id", "txn_id", "grp", "running_since_reset"]
pd.testing.assert_frame_equal(sql_df[cols].reset_index(drop=True), t[cols].reset_index(drop=True), check_dtype=False)  # sorted by acct_id, txn_id

# the honest difference: groupby cumsum on raw NaN keeps NaN on that row, SQL SUM skips the NULL
raw = txns.sort_values(["acct_id", "txn_id"]).reset_index(drop=True)
raw["grp"] = raw["is_reset"].fillna(0).astype(int).groupby(raw["acct_id"]).cumsum()
raw["raw_cumsum"] = raw["amount"].groupby([raw["acct_id"], raw["grp"]]).cumsum()
print("pandas raw cumsum, account 3:")
print(raw[raw["acct_id"] == 3][["txn_id", "amount", "raw_cumsum"]].to_string(index=False))

# the harder variant: reset when the running total EXCEEDS a threshold (state-dependent), plain loop as oracle
def reset_over(amounts, limit):
    out, tot = [], 0
    for a in amounts:
        tot += a
        out.append(tot)
        if tot > limit:
            tot = 0
    return out
amts = [40, 30, 50, 10, 60, 20, 90]
print("threshold 100 loop, running total after each row (resets after exceeding):", reset_over(amts, 100))
print("plain running total of the same rows:", list(pd.Series(amts).cumsum()))
print("SUM over only NULLs in SQLite:", con.execute("SELECT SUM(x) FROM (SELECT NULL AS x UNION ALL SELECT NULL)").fetchone()[0])
print("asserts passed")
```

**Output (my run):**
```text
SQL answer:
 acct_id  txn_id  amount  is_reset  grp  running_since_reset
       1       1    10.0       0.0    0                   10
       1       2    20.0       0.0    0                   30
       1       3    30.0       0.0    0                   60
       1       4     5.0       1.0    1                    5
       1       5     7.0       0.0    1                   12
       1       6     8.0       1.0    2                    8
       1       7     1.0       0.0    2                    9
       2       1    50.0       1.0    1                   50
       3       1     9.0       0.0    0                    9
       3       2     NaN       0.0    0                    9
       3       3     4.0       NaN    0                   13
       3       4     6.0       1.0    1                    6
       3       5     NaN       0.0    1                    6
raw SUM(amount), NULL amounts, account 3:
 acct_id  txn_id  raw_running
       3       1            9
       3       2            9
       3       3           13
       3       4            6
       3       5            6
no reset (plain running total), account 1:
 acct_id  txn_id  plain_running
       1       1             10
       1       2             30
       1       3             60
       1       4             65
       1       5             72
       1       6             80
       1       7             81
pandas answer:
 acct_id  txn_id  amount  is_reset  grp  running_since_reset
       1       1    10.0       0.0    0                   10
       1       2    20.0       0.0    0                   30
       1       3    30.0       0.0    0                   60
       1       4     5.0       1.0    1                    5
       1       5     7.0       0.0    1                   12
       1       6     8.0       1.0    2                    8
       1       7     1.0       0.0    2                    9
       2       1    50.0       1.0    1                   50
       3       1     9.0       0.0    0                    9
       3       2     NaN       0.0    0                    9
       3       3     4.0       NaN    0                   13
       3       4     6.0       1.0    1                    6
       3       5     NaN       0.0    1                    6
pandas raw cumsum, account 3:
 txn_id  amount  raw_cumsum
      1     9.0         9.0
      2     NaN         NaN
      3     4.0        13.0
      4     6.0         6.0
      5     NaN         NaN
threshold 100 loop, running total after each row (resets after exceeding): [40, 70, 120, 10, 70, 90, 180]
plain running total of the same rows: [40, 70, 120, 130, 190, 210, 300]
SUM over only NULLs in SQLite: None
asserts passed
```

**Edge cases:**
- A reset row belongs to the new group, so it starts with its own amount. If instead the total should restart after the reset row, shift the key by one row (`SUM(is_reset) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)`); not run here.
- Rows before the first reset form group 0, and a reset row first in an account (account 2) starts group 1 with no group 0.
- NULL `is_reset`: SUM ignores it, so it is the same as 0 unless wrapped in COALESCE (here wrapped). NULL amount: `SUM(amount)` ignores the NULL in the total, but a row sequence of only NULLs returns NULL in SQLite (the check printed `None`). I wrapped amounts in COALESCE so the output is a number.
- pandas difference: `groupby().cumsum()` on a raw NaN amount returns NaN on that row (account 3, txn 2 and 5 in my run), while SQL SUM returns the total so far. Filling with 0 first makes them match, which is what the main answer does.
- Ties in `txn_id` make the order and therefore the totals undefined; the window needs a unique ordering. I assume `txn_id` is unique per account.
- Single-row account: group key and total are the row itself (account 2). Unsorted input is fine because both windows order by `txn_id`.
- ROWS versus the default RANGE frame only matters with ties; I spell out ROWS.

**Then explain:**
- The key counts resets seen so far, so every row between two resets has the same key; this is the same running-count idea as islands, applied to flags instead of date gaps.
- The threshold variant (reset when the running total exceeds a limit) cannot be written as one SUM window, because whether a row resets depends on the total after the previous reset, which is the output you are computing. In my loop with limit 100 over 40, 30, 50, 10, 60, 20, 90 the totals are 40, 70, 120, 10, 70, 90, 180, while a plain running total is 40, 70, 120, 130, 190, 210, 300. Use a recursive CTE that carries the running total row by row; that answer is in Part 9, I only point to it here.
- Dialects (not executed here): the same two-window form works in PostgreSQL, MySQL 8, BigQuery and Snowflake; MySQL 5.7 has no window functions.

**Follow-ups:**
- Reset by threshold? Recursive CTE or a procedural loop (Part 9).
- Reset by calendar month? Replace the key with `strftime('%Y-%m', date)`; no running SUM needed.
- Cap the running total instead of resetting it? Also state-dependent, same answer as the threshold variant.

**Common mistakes:**
- Putting the group-key window and the total window in one SELECT (not allowed; use a CTE).
- Starting the new group on the row after the reset flag.
- Forgetting COALESCE when `is_reset` or `amount` can be NULL.
- Believing one window pass can reset on a threshold.
- Partitioning by the group key only, without the account.

### Q25 ⭐⭐ 🟡 Sessions per user per day, events per session and bounce sessions: from the 30 minute session CTE on events(user_id, event_ts, event_name), return per user per day the number of sessions, average events per session and the number of bounce sessions (exactly one event). Decide which date a session crossing midnight belongs to (its start) and show a session starting at 23:50 and ending at 00:20 to prove the rule.
**Asked at:** Dataiku sessionization tutorial (opened; vendor tutorial, uses a 30 minute timeout with >= and no tie handling) plus search snippets of Cube, DevGenius and LinkedIn sessionization posts (not opened); guides and not candidate reports; product analytics and data scientist rounds
**Say this first (1 line):** I assume a gap of more than 30 minutes starts a new session (convention A, exactly 30 minutes stays in the session); I flag new sessions with LAG, number them with a running SUM, aggregate to one row per session, and assign each session to the date of its first event, so a 23:50 to 00:20 session counts once, on its start day; I also show convention B (`>=`, exactly 30 minutes starts a new session).

**Schema and sample data:** sixteen event rows inserted out of order. User 1: 09:00, 09:10, 09:40 (a gap of exactly 30 minutes between 09:10 and 09:40) and a separate 15:00 event. User 2: 23:50 on 1 March, then 00:05 and 00:20 on 2 March (the midnight crossing), then 10:00 on 2 March. User 3: two events at the identical timestamp 12:00:00 plus 12:20. User 4: one event. User 5: a NULL timestamp (dropped) and one real event. User 6: 10:00 and 10:30:01 (one second over the threshold). Timestamps are ISO text in one time zone.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 09:40:00','view'),(1,'2024-03-01 09:00:00','open'),(1,'2024-03-01 09:10:00','view'),(1,'2024-03-01 15:00:00','open'),
 (2,'2024-03-01 23:50:00','open'),(2,'2024-03-02 00:05:00','view'),(2,'2024-03-02 00:20:00','click'),(2,'2024-03-02 10:00:00','open'),
 (3,'2024-03-01 12:00:00','open'),(3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:20:00','click'),
 (4,'2024-03-01 08:00:00','open'),
 (5,NULL,'open'),(5,'2024-03-01 08:00:00','open'),
 (6,'2024-03-01 10:00:00','open'),(6,'2024-03-01 10:30:01','view');
```

**SQL answer:** `SQL_A` in the Code block (convention A). `SQL_B` is the same text with `>=` instead of `>` on the line `t - LAG(t) ... > 1800`. Seconds come from `unixepoch()`, not `julianday()`.
```sql
WITH e AS (
  SELECT user_id, event_ts, unixepoch(event_ts) AS t
  FROM events
  WHERE event_ts IS NOT NULL
), f AS (
  SELECT user_id, event_ts, t,
         CASE WHEN LAG(t) OVER (PARTITION BY user_id ORDER BY t) IS NULL
                OR t - LAG(t) OVER (PARTITION BY user_id ORDER BY t) > 1800
              THEN 1 ELSE 0 END AS new_session
  FROM e
), g AS (
  SELECT user_id, event_ts,
         SUM(new_session) OVER (PARTITION BY user_id ORDER BY t
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_no
  FROM f
), s AS (
  SELECT user_id, session_no, MIN(event_ts) AS session_start, MAX(event_ts) AS session_end, COUNT(*) AS n_events
  FROM g
  GROUP BY user_id, session_no
)
SELECT user_id,
       date(session_start) AS day,
       COUNT(*) AS sessions,
       ROUND(AVG(n_events), 2) AS avg_events,
       SUM(n_events = 1) AS bounce_sessions
FROM s
GROUP BY user_id, date(session_start)
ORDER BY user_id, day
```

**pandas answer:** the Code block defines `sessions_pandas(events, ge)`; its body is identical to this text (`ge=False` is convention A, `ge=True` is B):
```py
e = events.dropna(subset=["event_ts"]).copy()
e["event_ts"] = pd.to_datetime(e["event_ts"])
e = e.sort_values(["user_id", "event_ts"], kind="stable")
gap = e.groupby("user_id")["event_ts"].diff()
limit = pd.Timedelta(minutes=30)
new = gap.isna() | ((gap >= limit) if ge else (gap > limit))
e["session_no"] = new.astype(int).groupby(e["user_id"]).cumsum()
s = (e.groupby(["user_id", "session_no"])
       .agg(session_start=("event_ts", "min"), n_events=("event_ts", "size"))
       .reset_index())
s["day"] = s["session_start"].dt.strftime("%Y-%m-%d")
out = (s.groupby(["user_id", "day"])
         .agg(sessions=("n_events", "size"), avg_events=("n_events", "mean"),
              bounce_sessions=("n_events", lambda x: int((x == 1).sum())))
         .round({"avg_events": 2}).reset_index())
```

**Example:** convention A. User 1: 09:00, 09:10, 09:40 are chained by gaps of 10 and 30 minutes (30 is not greater than 30), so session 1 has 3 events; 15:00 is 5 h 20 min later, session 2 has 1 event. Day 2024-03-01: 2 sessions, average (3+1)/2 = 2.0, bounce sessions 1. Convention B: the 30-minute gap starts a new session, so sessions are {09:00, 09:10}, {09:40}, {15:00}: 3 sessions, average 4/3 = 1.33, 2 bounces. User 2: gaps are 15, 15 minutes, so 23:50, 00:05, 00:20 form one session of 3 events that starts on 1 March, so 2024-03-01 gets 1 session with 3 events and 0 bounces, and the 10:00 event on 2 March is a separate bounce session dated 2024-03-02. Counting events by the event date instead would put 1 event on 1 March and 3 on 2 March, which is wrong for sessions.

**Code:** run with `python3 -I`. Both conventions are computed in SQL and pandas; the asserts compare each pair after sorting by `user_id, day`.
```python
# Q25: sessions per user per day, events per session, bounce sessions; both timeout conventions; midnight crossing
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 09:40:00','view'),(1,'2024-03-01 09:00:00','open'),(1,'2024-03-01 09:10:00','view'),(1,'2024-03-01 15:00:00','open'),
 (2,'2024-03-01 23:50:00','open'),(2,'2024-03-02 00:05:00','view'),(2,'2024-03-02 00:20:00','click'),(2,'2024-03-02 10:00:00','open'),
 (3,'2024-03-01 12:00:00','open'),(3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:20:00','click'),
 (4,'2024-03-01 08:00:00','open'),
 (5,NULL,'open'),(5,'2024-03-01 08:00:00','open'),
 (6,'2024-03-01 10:00:00','open'),(6,'2024-03-01 10:30:01','view');
"""
# {OP} is > (convention A: exactly 30 minutes still same session) or >= (convention B: exactly 30 minutes starts a new session)
SQL_TEMPLATE = """
WITH e AS (
  SELECT user_id, event_ts, unixepoch(event_ts) AS t
  FROM events
  WHERE event_ts IS NOT NULL
), f AS (
  SELECT user_id, event_ts, t,
         CASE WHEN LAG(t) OVER (PARTITION BY user_id ORDER BY t) IS NULL
                OR t - LAG(t) OVER (PARTITION BY user_id ORDER BY t) {OP} 1800
              THEN 1 ELSE 0 END AS new_session
  FROM e
), g AS (
  SELECT user_id, event_ts,
         SUM(new_session) OVER (PARTITION BY user_id ORDER BY t
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_no
  FROM f
), s AS (
  SELECT user_id, session_no, MIN(event_ts) AS session_start, MAX(event_ts) AS session_end, COUNT(*) AS n_events
  FROM g
  GROUP BY user_id, session_no
)
SELECT user_id,
       date(session_start) AS day,
       COUNT(*) AS sessions,
       ROUND(AVG(n_events), 2) AS avg_events,
       SUM(n_events = 1) AS bounce_sessions
FROM s
GROUP BY user_id, date(session_start)
ORDER BY user_id, day
"""
SQL_A = SQL_TEMPLATE.replace("{OP}", ">")
SQL_B = SQL_TEMPLATE.replace("{OP}", ">=")
SQL_WRONG_BYEVENTDAY = """
SELECT user_id, date(event_ts) AS day, COUNT(*) AS events_on_day
FROM events WHERE user_id = 2 GROUP BY user_id, date(event_ts) ORDER BY day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_a = pd.read_sql_query(SQL_A, con)
sql_b = pd.read_sql_query(SQL_B, con)
print("SQL convention A (gap > 30 min starts a new session):")
print(sql_a.to_string(index=False))
print("SQL convention B (gap >= 30 min starts a new session):")
print(sql_b.to_string(index=False))
print("user 2 events counted by event date (wrong way to date a session):")
print(pd.read_sql_query(SQL_WRONG_BYEVENTDAY, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
def sessions_pandas(events, ge):
    # pd:main
    e = events.dropna(subset=["event_ts"]).copy()
    e["event_ts"] = pd.to_datetime(e["event_ts"])
    e = e.sort_values(["user_id", "event_ts"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    limit = pd.Timedelta(minutes=30)
    new = gap.isna() | ((gap >= limit) if ge else (gap > limit))
    e["session_no"] = new.astype(int).groupby(e["user_id"]).cumsum()
    s = (e.groupby(["user_id", "session_no"])
           .agg(session_start=("event_ts", "min"), n_events=("event_ts", "size"))
           .reset_index())
    s["day"] = s["session_start"].dt.strftime("%Y-%m-%d")
    out = (s.groupby(["user_id", "day"])
             .agg(sessions=("n_events", "size"), avg_events=("n_events", "mean"),
                  bounce_sessions=("n_events", lambda x: int((x == 1).sum())))
             .round({"avg_events": 2}).reset_index())
    # pd:end
    return out
pa = sessions_pandas(events, ge=False)
pb = sessions_pandas(events, ge=True)
for sql, p in ((sql_a, pa), (sql_b, pb)):
    pd.testing.assert_frame_equal(sql.sort_values(["user_id", "day"]).reset_index(drop=True),
                                  p.sort_values(["user_id", "day"]).reset_index(drop=True), check_dtype=False)  # sorted by user_id, day
print("pandas convention A:")
print(pa.to_string(index=False))
print("pandas convention B:")
print(pb.to_string(index=False))

# julianday float arithmetic versus unixepoch integer seconds at the exact 30 minute threshold
n_bad_julian = con.execute("""
WITH RECURSIVE n(i) AS (SELECT 0 UNION ALL SELECT i + 1 FROM n WHERE i < 20000),
p AS (SELECT datetime('2020-01-01 00:00:00', '+' || (i * 7919) || ' seconds') AS a FROM n)
SELECT SUM((julianday(datetime(a, '+30 minutes')) - julianday(a)) * 1440 > 30),
       SUM((julianday(datetime(a, '+30 minutes')) - julianday(a)) * 1440 < 30),
       SUM((julianday(datetime(a, '+30 minutes')) - julianday(a)) * 1440 = 30),
       SUM(unixepoch(datetime(a, '+30 minutes')) - unixepoch(a) = 1800),
       COUNT(*)
FROM p""").fetchone()
print("20001 exact 30 minute pairs: julianday*1440 > 30, < 30, = 30; unixepoch diff = 1800; total:", n_bad_julian)
print("asserts passed")
```

**Output (my run):**
```text
SQL convention A (gap > 30 min starts a new session):
 user_id        day  sessions  avg_events  bounce_sessions
       1 2024-03-01         2         2.0                1
       2 2024-03-01         1         3.0                0
       2 2024-03-02         1         1.0                1
       3 2024-03-01         1         3.0                0
       4 2024-03-01         1         1.0                1
       5 2024-03-01         1         1.0                1
       6 2024-03-01         2         1.0                2
SQL convention B (gap >= 30 min starts a new session):
 user_id        day  sessions  avg_events  bounce_sessions
       1 2024-03-01         3        1.33                2
       2 2024-03-01         1        3.00                0
       2 2024-03-02         1        1.00                1
       3 2024-03-01         1        3.00                0
       4 2024-03-01         1        1.00                1
       5 2024-03-01         1        1.00                1
       6 2024-03-01         2        1.00                2
user 2 events counted by event date (wrong way to date a session):
 user_id        day  events_on_day
       2 2024-03-01              1
       2 2024-03-02              3
pandas convention A:
 user_id        day  sessions  avg_events  bounce_sessions
       1 2024-03-01         2         2.0                1
       2 2024-03-01         1         3.0                0
       2 2024-03-02         1         1.0                1
       3 2024-03-01         1         3.0                0
       4 2024-03-01         1         1.0                1
       5 2024-03-01         1         1.0                1
       6 2024-03-01         2         1.0                2
pandas convention B:
 user_id        day  sessions  avg_events  bounce_sessions
       1 2024-03-01         3        1.33                2
       2 2024-03-01         1        3.00                0
       2 2024-03-02         1        1.00                1
       3 2024-03-01         1        3.00                0
       4 2024-03-01         1        1.00                1
       5 2024-03-01         1        1.00                1
       6 2024-03-01         2        1.00                2
20001 exact 30 minute pairs: julianday*1440 > 30, < 30, = 30; unixepoch diff = 1800; total: (13333, 6668, 0, 20001, 20001)
asserts passed
```

**Edge cases:**
- Exactly 30 minutes (user 1): convention A gives 2 sessions, convention B gives 3 for the same data, so the choice changes the answer. Dataiku's tutorial uses `>=`, other guides use `>`; there is no standard, so state yours. A gap of 30 minutes and 1 second (user 6) starts a new session under both.
- Midnight crossing (user 2): the session belongs to the date of its start (`date(MIN(event_ts))`); it is one session, not two. A session spanning two days is not split by this rule; splitting at midnight is a different requirement.
- Same timestamp (user 3): the two 12:00:00 events have a gap of 0 and stay in one session regardless of their order, so the session count and size are stable. The order within the tie only matters if you pick the first event name; add an event id to the ORDER BY then.
- NULL `event_ts` (user 5): filtered out before LAG; otherwise NULL would sort first and break the gap arithmetic. User 5 still has one real event, so one bounce session.
- Single event (user 4): LAG is NULL, the first-row test flags it as a session start, and it is a bounce session. A bounce is a session with exactly one event, so a user with two events at the same timestamp is not a bounce.
- Unsorted input is fine, SQL and pandas both sort by time.
- julianday versus unixepoch: I generated 20,001 pairs exactly 30 minutes apart (one `+30 minutes` from a spread of timestamps). `(julianday(b) - julianday(a)) * 1440` was greater than 30 in 13,333 pairs, less than 30 in 6,668 and equal to 30 in none, while `unixepoch(b) - unixepoch(a) = 1800` held in all 20,001. A threshold test with julianday would therefore misclassify the exact-30-minute case in either direction; use integer seconds.
- Time zones: SQLite does no zone conversion here; daylight saving transitions are not modelled (not tested).

**Then explain:**
- Sessionization is three steps: flag (LAG gap above the timeout), label (running SUM of flags per user), aggregate (one row per session). Day-level metrics come from the session rows, so a session is dated once.
- Average events per session is the average of per-session counts, not events divided by days.
- `SUM(n_events = 1)` counts bounce sessions in SQLite; `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is the portable form.
- Dialects (not executed here): PostgreSQL would use `EXTRACT(EPOCH FROM ts)` or `ts - LAG(ts) > INTERVAL '30 minutes'`; MySQL `TIMESTAMPDIFF(SECOND, prev, ts)`; BigQuery `TIMESTAMP_DIFF`.

**Follow-ups:**
- Session duration? `MAX(t) - MIN(t)` per session (Q11 and Q12 cover the session id and the boundary).
- Daily active users based on session start? `COUNT(DISTINCT user_id)` on the session start dates.
- Session split at midnight? Add `date(event_ts)` to the PARTITION BY of the flag and label windows.

**Common mistakes:**
- Using `julianday` float arithmetic for the threshold.
- Assigning a session to the date of each event so one session appears on two days.
- Not stating the `>` versus `>=` convention.
- Not filtering NULL timestamps.
- Counting a user as a bounce user rather than a bounce session.

### Q26 ⭐⭐ 🟡 Dedup of back-to-back identical events: events(user_id, event_ts, event_name) where a client resends the same event_name. Remove consecutive repeats per user keeping the first of each run, but keep a later repeat that follows a different event (A, A, B, A keeps A, B, A). Use LAG(event_name) with IS NOT for the NULL-safe comparison, and show why DISTINCT or GROUP BY event_name would be wrong. Give the pandas shift version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Compare each event to the previous event of the same user with `LAG(event_name)` and keep the row when `event_name IS NOT prev_name` (or it is the user's first row); `DISTINCT` and `GROUP BY event_name` remove repeats everywhere, not only back-to-back, so A, A, B, A would become A, B.

**Schema and sample data:** I add an `event_id` to the stated columns as the tie-breaker (without one, same-timestamp rows have no defined order). Fourteen rows, inserted out of order. User 1: A, A, B, A, A, A by time (ids 1 to 6, id 6 inserted first). User 2: single row. User 3: B, B, C all at the same timestamp, ordered by id. User 4: NULL, NULL, A, NULL names.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (6,1,'2024-03-01 10:05:00','A'),
 (1,1,'2024-03-01 10:00:00','A'),
 (2,1,'2024-03-01 10:01:00','A'),
 (3,1,'2024-03-01 10:02:00','B'),
 (4,1,'2024-03-01 10:03:00','A'),
 (5,1,'2024-03-01 10:04:00','A'),
 (7,2,'2024-03-01 11:00:00','A'),
 (8,3,'2024-03-01 12:00:00','B'),
 (9,3,'2024-03-01 12:00:00','B'),
 (10,3,'2024-03-01 12:00:00','C'),
 (11,4,'2024-03-01 13:00:00',NULL),
 (12,4,'2024-03-01 13:01:00',NULL),
 (13,4,'2024-03-01 13:02:00','A'),
 (14,4,'2024-03-01 13:03:00',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block. `rn = 1` is the guard that keeps a user's first row even if its name is NULL (`NULL IS NOT NULL` is false).
```sql
WITH x AS (
  SELECT event_id, user_id, event_ts, event_name,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS rn,
         LAG(event_name) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_name
  FROM events
)
SELECT event_id, user_id, event_ts, event_name
FROM x
WHERE rn = 1 OR event_name IS NOT prev_name
ORDER BY user_id, event_ts, event_id
```

**pandas answer:** identical to the Code block:
```py
e = events.sort_values(["user_id", "event_ts", "event_id"]).reset_index(drop=True)
prev = e.groupby("user_id")["event_name"].shift()
first_of_user = e.groupby("user_id").cumcount().eq(0)
same_as_prev = e["event_name"].eq(prev) | (e["event_name"].isna() & prev.isna())
pd_df = e[first_of_user | ~same_as_prev].reset_index(drop=True)
```

**Example:** user 1 by time: A(1), A(2), B(3), A(4), A(5), A(6). Previous names: none, A, A, B, A, A. Event 1 is first, event 2 equals its previous A (dropped), event 3 is B after A (kept), event 4 is A after B (kept), events 5 and 6 repeat A (dropped). Kept A, B, A, which is the required result and the second A is kept because it follows B. `SELECT DISTINCT user_id, event_name` gives only A and B for user 1. User 3: B(8) is first, B(9) repeats, C(10) differs, so B and C are kept. User 4: NULL(11) is kept by the first-row guard, NULL(12) repeats a NULL and is dropped, A(13) is kept, NULL(14) after A is kept.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `user_id, event_ts, event_id`.
```python
# Q26: remove consecutive repeats per user (keep first of each run), NULL-safe with IS NOT
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (6,1,'2024-03-01 10:05:00','A'),
 (1,1,'2024-03-01 10:00:00','A'),
 (2,1,'2024-03-01 10:01:00','A'),
 (3,1,'2024-03-01 10:02:00','B'),
 (4,1,'2024-03-01 10:03:00','A'),
 (5,1,'2024-03-01 10:04:00','A'),
 (7,2,'2024-03-01 11:00:00','A'),
 (8,3,'2024-03-01 12:00:00','B'),
 (9,3,'2024-03-01 12:00:00','B'),
 (10,3,'2024-03-01 12:00:00','C'),
 (11,4,'2024-03-01 13:00:00',NULL),
 (12,4,'2024-03-01 13:01:00',NULL),
 (13,4,'2024-03-01 13:02:00','A'),
 (14,4,'2024-03-01 13:03:00',NULL);
"""
SQL_MAIN = """
WITH x AS (
  SELECT event_id, user_id, event_ts, event_name,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS rn,
         LAG(event_name) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_name
  FROM events
)
SELECT event_id, user_id, event_ts, event_name
FROM x
WHERE rn = 1 OR event_name IS NOT prev_name
ORDER BY user_id, event_ts, event_id
"""
SQL_DISTINCT = """
SELECT DISTINCT user_id, event_name FROM events WHERE user_id = 1 ORDER BY event_name
"""
SQL_NEQ = """
WITH x AS (
  SELECT event_id, user_id, event_name,
         LAG(event_name) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_name
  FROM events
)
SELECT event_id, user_id, event_name FROM x WHERE event_name != prev_name ORDER BY user_id, event_id
"""
SQL_NOGUARD = """
WITH x AS (
  SELECT event_id, user_id, event_name,
         LAG(event_name) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_name
  FROM events
)
SELECT event_id, user_id, event_name FROM x WHERE event_name IS NOT prev_name AND user_id = 4 ORDER BY event_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer (kept rows):")
print(sql_df.to_string(index=False))
print("wrong: SELECT DISTINCT user_id, event_name for user 1 (the second A is lost):")
print(pd.read_sql_query(SQL_DISTINCT, con).to_string(index=False))
print("wrong: != instead of IS NOT (first rows and NULL names vanish):")
print(pd.read_sql_query(SQL_NEQ, con).to_string(index=False))
print("IS NOT without the rn = 1 guard, user 4 (leading NULL name is dropped):")
print(pd.read_sql_query(SQL_NOGUARD, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.sort_values(["user_id", "event_ts", "event_id"]).reset_index(drop=True)
prev = e.groupby("user_id")["event_name"].shift()
first_of_user = e.groupby("user_id").cumcount().eq(0)
same_as_prev = e["event_name"].eq(prev) | (e["event_name"].isna() & prev.isna())
pd_df = e[first_of_user | ~same_as_prev].reset_index(drop=True)
# pd:end
print("pandas answer:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df, check_dtype=False)  # both ordered by user_id, event_ts, event_id

# the naive pandas comparison: NaN != NaN is True, so a run of NULL names is NOT collapsed
naive = e[first_of_user | e["event_name"].ne(prev)]
print("naive pandas ne(shift) keeps rows of user 4:", naive[naive["user_id"] == 4]["event_id"].tolist(), "vs SQL", sql_df[sql_df["user_id"] == 4]["event_id"].tolist())
# single row group and tie on timestamp are covered by users 2 and 3
print("asserts passed")
```

**Output (my run):**
```text
SQL answer (kept rows):
 event_id  user_id            event_ts event_name
        1        1 2024-03-01 10:00:00          A
        3        1 2024-03-01 10:02:00          B
        4        1 2024-03-01 10:03:00          A
        7        2 2024-03-01 11:00:00          A
        8        3 2024-03-01 12:00:00          B
       10        3 2024-03-01 12:00:00          C
       11        4 2024-03-01 13:00:00        NaN
       13        4 2024-03-01 13:02:00          A
       14        4 2024-03-01 13:03:00        NaN
wrong: SELECT DISTINCT user_id, event_name for user 1 (the second A is lost):
 user_id event_name
       1          A
       1          B
wrong: != instead of IS NOT (first rows and NULL names vanish):
 event_id  user_id event_name
        3        1          B
        4        1          A
       10        3          C
IS NOT without the rn = 1 guard, user 4 (leading NULL name is dropped):
 event_id  user_id event_name
       13        4          A
       14        4        NaN
pandas answer:
 event_id  user_id            event_ts event_name
        1        1 2024-03-01 10:00:00          A
        3        1 2024-03-01 10:02:00          B
        4        1 2024-03-01 10:03:00          A
        7        2 2024-03-01 11:00:00          A
        8        3 2024-03-01 12:00:00          B
       10        3 2024-03-01 12:00:00          C
       11        4 2024-03-01 13:00:00        NaN
       13        4 2024-03-01 13:02:00          A
       14        4 2024-03-01 13:03:00        NaN
naive pandas ne(shift) keeps rows of user 4: [11, 12, 13, 14] vs SQL [11, 13, 14]
asserts passed
```

**Edge cases:**
- NULL event names: `!=` against a NULL is NULL, so the row is dropped (`SQL_NEQ` lost user 1's first row, user 2's only row and every NULL row in my run). `IS NOT` is NULL-safe. Without the `rn = 1` guard a user's first row is lost when its name is NULL (user 4's first NULL event disappeared in `SQL_NOGUARD`).
- pandas: `s.ne(s.shift())` treats NaN as different from NaN, so a run of NULL names is not collapsed (user 4 kept ids 11, 12, 13, 14 instead of 11, 13, 14 in my run). The main answer therefore adds `| (isna & isna)` to the equality test and a separate first-row test.
- Ties on `event_ts` (user 3): ordering needs the extra column; the result for B, B, C depends on `event_id`. Without it, which row is first is arbitrary.
- Single-row user: kept by the first-row rule. Unsorted input is fine because both versions sort by time and id first.
- Exact duplicates (same user, time and name twice) are removed as repeats of the previous row, which is the intended behaviour here.
- A resend that is not adjacent (A, B, A) is deliberately kept; if you must drop resends within a time window instead, that is a different rule (compare timestamps too).

**Then explain:**
- Keeping the first of each run is "keep the rows that start a run", the same idea as island starts. `DISTINCT` asks "which names occurred", not "which rows changed".
- `GROUP BY user_id, event_name` with `MIN(event_ts)` also collapses the second A; it answers a first-occurrence question.
- `IS NOT` is NULL-safe in SQLite; `IS DISTINCT FROM` is the standard spelling (it also runs in SQLite 3.45.1, see Q27); PostgreSQL has `IS DISTINCT FROM` but, as I remember it, not a general `IS NOT` for non-boolean values, and MySQL uses `NOT (a <=> b)` (not executed here).
- The pandas version uses `groupby("user_id")["event_name"].shift()` so previous values never cross users.

**Follow-ups:**
- Keep the last of each run instead? Compare with `LEAD`.
- Collapse runs into one row with a count and the first and last time? Use the run key (running SUM of the change flag) and aggregate; see Q13.
- Only drop repeats within 5 seconds? Add a timestamp-gap condition to the keep test.

**Common mistakes:**
- `SELECT DISTINCT` or `GROUP BY event_name` (loses the second A).
- `!=` instead of `IS NOT` (drops first rows and NULL rows).
- Missing the first-row guard.
- No tie-breaker in the ORDER BY.
- In pandas, `shift()` without a groupby, so one user's last event is compared to the next user's first.

### Q27 ⭐⭐ 🟡 State-change detection: sensor_state(device_id, ts, state) with possible NULL states. Return the rows where the state differs from the previous row of the same device (the transition rows) and the first row of each run, using LAG and the NULL-safe comparison (IS NOT or IS DISTINCT FROM in SQLite 3.45.1; PostgreSQL and others hedged). Show what != gives with a NULL (the row is dropped) and what pandas != gives with NaN (NaN != NaN is True, so every NaN row starts a new run).
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Use `LAG(state)` per device and keep the rows where the state differs with a NULL-safe test (`IS NOT`, or `IS DISTINCT FROM` which SQLite 3.45.1 also accepts) plus each device's first row; `!=` silently drops every row touching a NULL, and in pandas `!=` goes the opposite way because NaN != NaN is True, so every NaN row looks like a new run.

**Schema and sample data:** twelve rows, four devices, inserted out of order for device 1. Device 1: on, on, off, on, off (three transitions after the first row). Device 2: NULL, NULL, on, NULL, on. Device 3: a single row. Device 4: a single NULL row. A run is a maximal sequence of consecutive rows with the same state, and I treat NULL as a state of its own ("unknown"), so consecutive NULLs form one run. The transition rows and the run starts are the same set of rows, so one query answers both.
```sql
CREATE TABLE sensor_state(device_id INTEGER, ts TEXT, state TEXT);
INSERT INTO sensor_state VALUES
 (1,'2024-03-01 00:03:00','on'),
 (1,'2024-03-01 00:00:00','on'),
 (1,'2024-03-01 00:01:00','on'),
 (1,'2024-03-01 00:02:00','off'),
 (1,'2024-03-01 00:04:00','off'),
 (2,'2024-03-01 00:00:00',NULL),
 (2,'2024-03-01 00:01:00',NULL),
 (2,'2024-03-01 00:02:00','on'),
 (2,'2024-03-01 00:03:00',NULL),
 (2,'2024-03-01 00:04:00','on'),
 (3,'2024-03-01 00:00:00','off'),
 (4,'2024-03-01 00:00:00',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block. `SQL_DISTINCT_FROM` replaces `state IS NOT prev_state` with `state IS DISTINCT FROM prev_state` and gives the same rows (asserted).
```sql
WITH x AS (
  SELECT device_id, ts, state,
         ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY ts) AS rn,
         LAG(state) OVER (PARTITION BY device_id ORDER BY ts) AS prev_state
  FROM sensor_state
)
SELECT device_id, ts, prev_state, state,
       CASE WHEN rn = 1 THEN 'first row' ELSE 'transition' END AS kind
FROM x
WHERE rn = 1 OR state IS NOT prev_state
ORDER BY device_id, ts
```

**pandas answer:** identical to the Code block:
```py
s = sensor.sort_values(["device_id", "ts"]).reset_index(drop=True)
prev = s.groupby("device_id")["state"].shift()
first_row = s.groupby("device_id").cumcount().eq(0)
differs = s["state"].ne(prev) & ~(s["state"].isna() & prev.isna())
out = s[first_row | differs].copy()
out["prev_state"] = prev[out.index]
out["kind"] = np.where(first_row[out.index], "first row", "transition")
pd_df = out[["device_id", "ts", "prev_state", "state", "kind"]].reset_index(drop=True)
```

**Example:** device 1 by time: on, on, off, on, off. Previous states: none, on, on, off, on. Rows kept: the first (on), 00:02 (on to off), 00:03 (off to on), 00:04 (on to off); 00:01 repeats on and is dropped. Device 2: NULL (first row, kept), NULL (same unknown state, dropped), on (kept, NULL to on), NULL (kept, on to NULL), on (kept, NULL to on). Device 3 and 4 each keep their one row. With `!=` only device 1's three transitions survive: the first rows have a NULL previous state and every comparison with NULL is NULL.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `device_id, ts`. The extra lines check `IS DISTINCT FROM`, NaN comparisons, groupby with NaN keys and `itertools.groupby` on NaN.
```python
# Q27: state-change detection with NULL states: IS NOT / IS DISTINCT FROM versus != ; pandas NaN != NaN
import itertools
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE sensor_state(device_id INTEGER, ts TEXT, state TEXT);
INSERT INTO sensor_state VALUES
 (1,'2024-03-01 00:03:00','on'),
 (1,'2024-03-01 00:00:00','on'),
 (1,'2024-03-01 00:01:00','on'),
 (1,'2024-03-01 00:02:00','off'),
 (1,'2024-03-01 00:04:00','off'),
 (2,'2024-03-01 00:00:00',NULL),
 (2,'2024-03-01 00:01:00',NULL),
 (2,'2024-03-01 00:02:00','on'),
 (2,'2024-03-01 00:03:00',NULL),
 (2,'2024-03-01 00:04:00','on'),
 (3,'2024-03-01 00:00:00','off'),
 (4,'2024-03-01 00:00:00',NULL);
"""
SQL_MAIN = """
WITH x AS (
  SELECT device_id, ts, state,
         ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY ts) AS rn,
         LAG(state) OVER (PARTITION BY device_id ORDER BY ts) AS prev_state
  FROM sensor_state
)
SELECT device_id, ts, prev_state, state,
       CASE WHEN rn = 1 THEN 'first row' ELSE 'transition' END AS kind
FROM x
WHERE rn = 1 OR state IS NOT prev_state
ORDER BY device_id, ts
"""
SQL_NEQ = """
WITH x AS (
  SELECT device_id, ts, state, LAG(state) OVER (PARTITION BY device_id ORDER BY ts) AS prev_state
  FROM sensor_state
)
SELECT device_id, ts, prev_state, state FROM x WHERE state != prev_state ORDER BY device_id, ts
"""
SQL_DISTINCT_FROM = """
WITH x AS (
  SELECT device_id, ts, state,
         ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY ts) AS rn,
         LAG(state) OVER (PARTITION BY device_id ORDER BY ts) AS prev_state
  FROM sensor_state
)
SELECT device_id, ts, prev_state, state,
       CASE WHEN rn = 1 THEN 'first row' ELSE 'transition' END AS kind
FROM x
WHERE rn = 1 OR state IS DISTINCT FROM prev_state
ORDER BY device_id, ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer (IS NOT):")
print(sql_df.to_string(index=False))
dist = pd.read_sql_query(SQL_DISTINCT_FROM, con)
assert dist.equals(sql_df)
print("IS DISTINCT FROM on SQLite 3.45.1 gives the same rows:", dist.equals(sql_df))
print("probes NULL != NULL, NULL IS NOT NULL, NULL IS DISTINCT FROM NULL, 1 IS NOT NULL:",
      con.execute("SELECT NULL != NULL, NULL IS NOT NULL, NULL IS DISTINCT FROM NULL, 1 IS NOT NULL").fetchone())
print("wrong: != (first rows and everything touching a NULL vanish):")
print(pd.read_sql_query(SQL_NEQ, con).to_string(index=False))

sensor = pd.read_sql_query("SELECT * FROM sensor_state", con)
# pd:main
s = sensor.sort_values(["device_id", "ts"]).reset_index(drop=True)
prev = s.groupby("device_id")["state"].shift()
first_row = s.groupby("device_id").cumcount().eq(0)
differs = s["state"].ne(prev) & ~(s["state"].isna() & prev.isna())
out = s[first_row | differs].copy()
out["prev_state"] = prev[out.index]
out["kind"] = np.where(first_row[out.index], "first row", "transition")
pd_df = out[["device_id", "ts", "prev_state", "state", "kind"]].reset_index(drop=True)
# pd:end
print("pandas answer:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df, check_dtype=False)  # both ordered by device_id, ts

naive = s[first_row | s["state"].ne(prev)]
print("naive pandas ne(shift) rows per device:", naive.groupby("device_id").size().to_dict(), "vs correct", pd_df.groupby("device_id").size().to_dict())
print("NaN != NaN:", np.nan != np.nan, "; Series ne:", pd.Series([np.nan]).ne(pd.Series([np.nan])).tolist())
print("groupby drops NaN keys:", s.groupby("state")["device_id"].size().to_dict(), "; with dropna=False:", s.groupby("state", dropna=False)["device_id"].size().to_dict())
# itertools.groupby run lengths: identity shortcut for the same NaN object, distinct objects are not equal
same_obj = [len(list(g)) for _, g in itertools.groupby([np.nan, np.nan, np.nan])]
list_of_floats = [float("nan"), float("nan"), float("nan")]
diff_obj = [len(list(g)) for _, g in itertools.groupby(list_of_floats)]
from_series = [len(list(g)) for _, g in itertools.groupby(pd.Series([np.nan, np.nan, np.nan]).tolist())]
print("itertools.groupby NaN run lengths: same object", same_obj, "; separate float objects", diff_obj, "; from Series.tolist()", from_series)
print("asserts passed")
```

**Output (my run):**
```text
SQL answer (IS NOT):
 device_id                  ts prev_state state       kind
         1 2024-03-01 00:00:00        NaN    on  first row
         1 2024-03-01 00:02:00         on   off transition
         1 2024-03-01 00:03:00        off    on transition
         1 2024-03-01 00:04:00         on   off transition
         2 2024-03-01 00:00:00        NaN   NaN  first row
         2 2024-03-01 00:02:00        NaN    on transition
         2 2024-03-01 00:03:00         on   NaN transition
         2 2024-03-01 00:04:00        NaN    on transition
         3 2024-03-01 00:00:00        NaN   off  first row
         4 2024-03-01 00:00:00        NaN   NaN  first row
IS DISTINCT FROM on SQLite 3.45.1 gives the same rows: True
probes NULL != NULL, NULL IS NOT NULL, NULL IS DISTINCT FROM NULL, 1 IS NOT NULL: (None, 0, 0, 1)
wrong: != (first rows and everything touching a NULL vanish):
 device_id                  ts prev_state state
         1 2024-03-01 00:02:00         on   off
         1 2024-03-01 00:03:00        off    on
         1 2024-03-01 00:04:00         on   off
pandas answer:
 device_id                  ts prev_state state       kind
         1 2024-03-01 00:00:00        NaN    on  first row
         1 2024-03-01 00:02:00         on   off transition
         1 2024-03-01 00:03:00        off    on transition
         1 2024-03-01 00:04:00         on   off transition
         2 2024-03-01 00:00:00        NaN   NaN  first row
         2 2024-03-01 00:02:00        NaN    on transition
         2 2024-03-01 00:03:00         on   NaN transition
         2 2024-03-01 00:04:00        NaN    on transition
         3 2024-03-01 00:00:00        NaN   off  first row
         4 2024-03-01 00:00:00        NaN   NaN  first row
naive pandas ne(shift) rows per device: {1: 4, 2: 5, 3: 1, 4: 1} vs correct {1: 4, 2: 4, 3: 1, 4: 1}
NaN != NaN: True ; Series ne: [True]
groupby drops NaN keys: {'off': 3, 'on': 5} ; with dropna=False: {'off': 3, 'on': 5, nan: 4}
itertools.groupby NaN run lengths: same object [3] ; separate float objects [1, 1, 1] ; from Series.tolist() [1, 1, 1]
asserts passed
```

**Edge cases:**
- NULL on either side: `NULL != x` and `NULL != NULL` are both NULL, so a WHERE clause drops those rows. The probe printed `(None, 0, 0, 1)` for `NULL != NULL`, `NULL IS NOT NULL`, `NULL IS DISTINCT FROM NULL` and `1 IS NOT NULL`.
- First row of each device (devices 3 and 4): LAG returns NULL, so a plain `IS NOT` would drop a first row whose state is NULL (device 4); the `rn = 1` guard keeps it. Whether the first row counts as a transition is a choice; the `kind` column separates 'first row' from 'transition'.
- pandas NaN: `np.nan != np.nan` is True and `Series.ne` returned `[True]`, so the naive `s.ne(s.shift())` kept 5 rows for device 2 instead of 4 (my run). The main answer uses `ne(prev) & ~(both NaN)`.
- pandas `groupby("state")` drops NaN keys by default (counts of 'off' 3 and 'on' 5 only, 8 of 12 rows); `dropna=False` keeps the NaN group (4 rows). A run-length count by state would otherwise lose the NULL runs.
- `itertools.groupby` run lengths: three NaN values of the same object `np.nan` gave one run of 3 (the identity shortcut), but three separate float objects or `Series.tolist()` values gave runs of 1, 1, 1 in my run. Do not rely on it for NaN; map NaN to a sentinel first.
- Duplicate timestamps within a device make the order ambiguous; add an id to the ORDER BY. Unsorted input is fine, both versions sort first.
- Time gaps between rows are ignored; only consecutive rows are compared.

**Then explain:**
- `IS NOT` (a SQLite spelling that works on any values) and `IS DISTINCT FROM` (the SQL standard form, runs in SQLite 3.45.1) are the NULL-safe inequality. PostgreSQL supports `IS DISTINCT FROM` and MySQL uses `NOT (a <=> b)` as I remember it; I did not run those.
- A transition row is by definition the first row of a new run, so "transitions" and "run starts" are one result.
- pandas and SQL disagree on NaN/NULL: SQL says unknown, pandas says unequal. Always decide what NULL means (a state of its own, or missing data to skip) before choosing the comparison.
- If NULL means "missing reading, carry on with the last state", forward-fill first (`ffill()` in pandas; SQLite has no `IGNORE NULLS`).

**Follow-ups:**
- Duration of each run? Add a run key and use `MAX(ts) - MIN(ts)`, or LEAD of the start rows.
- Count transitions per device? `COUNT(*) - 1` of the start rows, or sum the change flag.
- Treat NULL as missing? Forward-fill, then compare.

**Common mistakes:**
- `WHERE state != prev_state`, which drops the first row and every row next to a NULL.
- pandas `s != s.shift()` for runs of NaN, which makes every NaN row a new run.
- `groupby("state")` without `dropna=False`, which silently drops the NULL group.
- `shift()` across devices because the `groupby` was left out.
- Assuming `itertools.groupby` collapses NaNs.

### Q28 ⭐⭐ 🟡 pandas interval merging: bookings(room_id, start_ts, end_ts) as a DataFrame. Merge overlapping intervals per room with sort_values on start, a groupby cummax of end shifted by one, a new-block flag where start is greater than the previous cummax, a cumsum key, and groupby agg min start and max end. Assert it equals the SQL running-MAX answer, and show the contained-interval and touching-interval cases.
**Asked at:** oneuptime interval-merge write-up (opened; running max of end, strict > so touching intervals merge) and the DataDriven 'The Overlap' interval-merge problem (opened; a Python problem, labelled hard and L5, no company named); practice-site material and not candidate reports; data scientist and data engineer rounds
**Say this first (1 line):** Sort by room and start, compute the running maximum end of all earlier bookings in the room (`groupby("room_id")["end_ts"].cummax()` then shifted by one), start a new block when the start is strictly greater than that maximum, cumsum the flags into a block key, and aggregate min start and max end; strict `>` means touching intervals merge, and the running maximum (not just the previous end) is what keeps a contained interval from shrinking the block.

**Schema and sample data:** thirteen rows, inserted out of order, `TEXT` timestamps in one format so text order equals time order. Room 1: 09:00-12:00 contains 10:00-11:00; 11:30-12:30 overlaps the first; 12:30-12:45 touches it (starts exactly at 12:30); 13:00-14:00 is separate; 16:00-17:00 appears twice (exact duplicate). Room 2: 09:00-10:00 and 10:00-11:00 touch; 11:01-12:00 is one minute later. Room 3: a single booking. Room 4: a booking with a NULL end (open-ended) and one normal booking.
```sql
CREATE TABLE bookings(room_id INTEGER, start_ts TEXT, end_ts TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-01 13:00','2024-03-01 14:00'),
 (1,'2024-03-01 09:00','2024-03-01 12:00'),
 (1,'2024-03-01 10:00','2024-03-01 11:00'),
 (1,'2024-03-01 11:30','2024-03-01 12:30'),
 (1,'2024-03-01 12:30','2024-03-01 12:45'),
 (1,'2024-03-01 16:00','2024-03-01 17:00'),
 (1,'2024-03-01 16:00','2024-03-01 17:00'),
 (2,'2024-03-01 09:00','2024-03-01 10:00'),
 (2,'2024-03-01 10:00','2024-03-01 11:00'),
 (2,'2024-03-01 11:01','2024-03-01 12:00'),
 (3,'2024-03-01 08:00','2024-03-01 08:30'),
 (4,'2024-03-01 09:00',NULL),
 (4,'2024-03-01 10:00','2024-03-01 11:00');
```

**SQL answer:** `SQL_MAIN` in the Code block. Spelled out: running MAX of `end_ts` over all earlier rows, a flag, a running SUM of the flag, then min and max per block. `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING` ran on SQLite 3.45.1 and returns NULL for each room's first row, which the flag treats as a new block.
```sql
WITH o AS (
  SELECT room_id, start_ts, end_ts,
         MAX(end_ts) OVER (
           PARTITION BY room_id ORDER BY start_ts, end_ts
           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max_end
  FROM bookings
  WHERE end_ts IS NOT NULL
), f AS (
  SELECT *, CASE WHEN prev_max_end IS NULL OR start_ts > prev_max_end THEN 1 ELSE 0 END AS new_block
  FROM o
), g AS (
  SELECT *, SUM(new_block) OVER (
           PARTITION BY room_id ORDER BY start_ts, end_ts
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block
  FROM f
)
SELECT room_id, MIN(start_ts) AS start_ts, MAX(end_ts) AS end_ts, COUNT(*) AS n_merged
FROM g
GROUP BY room_id, block
ORDER BY room_id, start_ts
```

**pandas answer:** identical to the body of `merge_pandas` in the Code block:
```py
b = bookings.dropna(subset=["end_ts"]).copy()
b["start_ts"] = pd.to_datetime(b["start_ts"])
b["end_ts"] = pd.to_datetime(b["end_ts"])
b = b.sort_values(["room_id", "start_ts", "end_ts"]).reset_index(drop=True)
prev_max_end = b.groupby("room_id")["end_ts"].cummax().groupby(b["room_id"]).shift()
new_block = prev_max_end.isna() | (b["start_ts"] > prev_max_end)
b["block"] = new_block.astype(int).groupby(b["room_id"]).cumsum()
merged = (b.groupby(["room_id", "block"])
            .agg(start_ts=("start_ts", "min"), end_ts=("end_ts", "max"), n_merged=("start_ts", "size"))
            .reset_index().drop(columns="block"))
```

**Example:** room 1 sorted by start then end: 09:00-12:00, 10:00-11:00, 11:30-12:30, 12:30-12:45, 13:00-14:00, 16:00-17:00, 16:00-17:00. Previous maximum end: none, 12:00, 12:00, 12:30, 12:45, 14:00, 17:00. Start versus previous maximum: first row is new; 10:00 not greater than 12:00 (merge, contained); 11:30 not greater than 12:00 (merge); 12:30 is not strictly greater than 12:30 (merge, touching); 13:00 is greater than 12:45 (new); 16:00 is greater than 14:00 (new); the duplicate 16:00 is not greater than 17:00 (merge). Blocks: 09:00-12:45 (4 bookings), 13:00-14:00, 16:00-17:00 (2 bookings). Room 2: 10:00 equals the previous end 10:00 so it merges (09:00-11:00); 11:01 is later than 11:00 so it stays separate.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `room_id, start_ts`. The script also prints the touching-stays-separate variant, the wrong LAG version and the checks for `cummax` in groupby and sort stability.
```python
# Q28: merge overlapping intervals per room: SQL running MAX vs pandas groupby cummax shifted; contained and touching cases
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE bookings(room_id INTEGER, start_ts TEXT, end_ts TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-01 13:00','2024-03-01 14:00'),
 (1,'2024-03-01 09:00','2024-03-01 12:00'),
 (1,'2024-03-01 10:00','2024-03-01 11:00'),
 (1,'2024-03-01 11:30','2024-03-01 12:30'),
 (1,'2024-03-01 12:30','2024-03-01 12:45'),
 (1,'2024-03-01 16:00','2024-03-01 17:00'),
 (1,'2024-03-01 16:00','2024-03-01 17:00'),
 (2,'2024-03-01 09:00','2024-03-01 10:00'),
 (2,'2024-03-01 10:00','2024-03-01 11:00'),
 (2,'2024-03-01 11:01','2024-03-01 12:00'),
 (3,'2024-03-01 08:00','2024-03-01 08:30'),
 (4,'2024-03-01 09:00',NULL),
 (4,'2024-03-01 10:00','2024-03-01 11:00');
"""
SQL_MAIN = """
WITH o AS (
  SELECT room_id, start_ts, end_ts,
         MAX(end_ts) OVER (
           PARTITION BY room_id ORDER BY start_ts, end_ts
           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max_end
  FROM bookings
  WHERE end_ts IS NOT NULL
), f AS (
  SELECT *, CASE WHEN prev_max_end IS NULL OR start_ts > prev_max_end THEN 1 ELSE 0 END AS new_block
  FROM o
), g AS (
  SELECT *, SUM(new_block) OVER (
           PARTITION BY room_id ORDER BY start_ts, end_ts
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block
  FROM f
)
SELECT room_id, MIN(start_ts) AS start_ts, MAX(end_ts) AS end_ts, COUNT(*) AS n_merged
FROM g
GROUP BY room_id, block
ORDER BY room_id, start_ts
"""
SQL_TOUCH_SEPARATE = SQL_MAIN.replace("start_ts > prev_max_end", "start_ts >= prev_max_end")
SQL_NAIVE_PREV = """
WITH o AS (
  SELECT room_id, start_ts, end_ts,
         LAG(end_ts) OVER (PARTITION BY room_id ORDER BY start_ts, end_ts) AS prev_end
  FROM bookings WHERE end_ts IS NOT NULL
), f AS (SELECT *, CASE WHEN prev_end IS NULL OR start_ts > prev_end THEN 1 ELSE 0 END AS new_block FROM o),
g AS (SELECT *, SUM(new_block) OVER (PARTITION BY room_id ORDER BY start_ts, end_ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block FROM f)
SELECT room_id, MIN(start_ts) AS start_ts, MAX(end_ts) AS end_ts, COUNT(*) AS n_merged
FROM g GROUP BY room_id, block ORDER BY room_id, start_ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL merged (touching merges, strict >):")
print(sql_df.to_string(index=False))
print("SQL with >= (touching stays separate), room 2 only:")
print(pd.read_sql_query(SQL_TOUCH_SEPARATE, con).query("room_id == 2").to_string(index=False))
print("wrong: LAG(end_ts) instead of the running MAX, room 1 (contained booking shrinks the end):")
print(pd.read_sql_query(SQL_NAIVE_PREV, con).query("room_id == 1").to_string(index=False))

bookings = pd.read_sql_query("SELECT * FROM bookings", con)
def merge_pandas(bookings, touching_merges=True):
    # pd:main
    b = bookings.dropna(subset=["end_ts"]).copy()
    b["start_ts"] = pd.to_datetime(b["start_ts"])
    b["end_ts"] = pd.to_datetime(b["end_ts"])
    b = b.sort_values(["room_id", "start_ts", "end_ts"]).reset_index(drop=True)
    prev_max_end = b.groupby("room_id")["end_ts"].cummax().groupby(b["room_id"]).shift()
    new_block = prev_max_end.isna() | (b["start_ts"] > prev_max_end)
    b["block"] = new_block.astype(int).groupby(b["room_id"]).cumsum()
    merged = (b.groupby(["room_id", "block"])
                .agg(start_ts=("start_ts", "min"), end_ts=("end_ts", "max"), n_merged=("start_ts", "size"))
                .reset_index().drop(columns="block"))
    # pd:end
    return merged
pd_df = merge_pandas(bookings)
shown = pd_df.assign(start_ts=pd_df["start_ts"].dt.strftime("%Y-%m-%d %H:%M"), end_ts=pd_df["end_ts"].dt.strftime("%Y-%m-%d %H:%M"))
print("pandas merged:")
print(shown.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), shown.reset_index(drop=True), check_dtype=False)  # both ordered by room_id, start_ts

# checks for the unverified list
print("cummax in groupby on datetimes dtype:", bookings.assign(e=pd.to_datetime(bookings["end_ts"])).groupby("room_id")["e"].cummax().dtype)
print("first row of each group after shift is NaT:", int(pd.Series(pd.to_datetime(["2024-01-01","2024-01-02"])).shift().isna().sum()))
# sort_values stability: default kind on a single key with ties versus kind='stable'
rng = np.random.default_rng(0)
df = pd.DataFrame({"k": rng.integers(0, 5, 2000), "i": np.arange(2000)})
default_order = df.sort_values("k")["i"].tolist()
stable_order = df.sort_values("k", kind="stable")["i"].tolist()
two_key_order = df.sort_values(["k", "i"])["i"].tolist()
print("single-key default sort equals stable sort on 2000 rows with ties:", default_order == stable_order)
print("two-key sort equals stable sort:", two_key_order == stable_order)
print("asserts passed")
```

**Output (my run):**
```text
SQL merged (touching merges, strict >):
 room_id         start_ts           end_ts  n_merged
       1 2024-03-01 09:00 2024-03-01 12:45         4
       1 2024-03-01 13:00 2024-03-01 14:00         1
       1 2024-03-01 16:00 2024-03-01 17:00         2
       2 2024-03-01 09:00 2024-03-01 11:00         2
       2 2024-03-01 11:01 2024-03-01 12:00         1
       3 2024-03-01 08:00 2024-03-01 08:30         1
       4 2024-03-01 10:00 2024-03-01 11:00         1
SQL with >= (touching stays separate), room 2 only:
 room_id         start_ts           end_ts  n_merged
       2 2024-03-01 09:00 2024-03-01 10:00         1
       2 2024-03-01 10:00 2024-03-01 11:00         1
       2 2024-03-01 11:01 2024-03-01 12:00         1
wrong: LAG(end_ts) instead of the running MAX, room 1 (contained booking shrinks the end):
 room_id         start_ts           end_ts  n_merged
       1 2024-03-01 09:00 2024-03-01 12:00         2
       1 2024-03-01 11:30 2024-03-01 12:45         2
       1 2024-03-01 13:00 2024-03-01 14:00         1
       1 2024-03-01 16:00 2024-03-01 17:00         2
pandas merged:
 room_id         start_ts           end_ts  n_merged
       1 2024-03-01 09:00 2024-03-01 12:45         4
       1 2024-03-01 13:00 2024-03-01 14:00         1
       1 2024-03-01 16:00 2024-03-01 17:00         2
       2 2024-03-01 09:00 2024-03-01 11:00         2
       2 2024-03-01 11:01 2024-03-01 12:00         1
       3 2024-03-01 08:00 2024-03-01 08:30         1
       4 2024-03-01 10:00 2024-03-01 11:00         1
cummax in groupby on datetimes dtype: datetime64[us]
first row of each group after shift is NaT: 1
single-key default sort equals stable sort on 2000 rows with ties: False
two-key sort equals stable sort: True
asserts passed
```

**Edge cases:**
- Touching intervals: the strict `>` merges them (room 2 gives 09:00-11:00). With `>=` they stay separate (room 2 printed three rows). Pick one rule and say it; for rooms an end time normally equals the next start (half-open), so many schedulers want them separate.
- Contained interval: 10:00-11:00 inside 09:00-12:00 must not pull the end back. Using `LAG(end_ts)` (the previous row's end only) made the block end at 12:00 instead of 12:45 and split room 1 in two wrong blocks in my run; the running maximum fixes it.
- Exact duplicates (room 1, 16:00-17:00 twice) merge into one block with `n_merged = 2`.
- NULL `end_ts` (room 4): I filter those rows out in both versions, so room 4's open booking disappears and only its normal booking is returned. Without the filter, `MAX` ignores NULL and `start > NULL` is NULL, which would merge the open booking with the next one by accident. An open end needs an explicit rule (for example an as-of date or infinity).
- Single-row room: the shifted maximum is NaT or NULL, so the flag is 1 and the room returns its booking.
- Unsorted input: the sort puts bookings in order; ties on start are broken by end for a deterministic order. The pandas default `sort_values` on one key with ties is not guaranteed stable: on 2000 random rows with ties, `sort_values("k")` did not equal `kind="stable"` (False in my run), whereas sorting on two keys `["k", "i"]` matched the stable order (True). I sort on all three columns so no tie is left to chance.
- `groupby().cummax()` on datetimes keeps `datetime64` (the dtype printed `datetime64[us]`), and `shift()` fills each group's first row with NaT (one NaT in the two-row check).
- Timestamps as text work in SQL only because the format is fixed; mixed formats or time zones break the text comparison.

**Then explain:**
- The block starts when the next booking starts after everything seen so far has ended. That is the running maximum, not the previous row.
- `cummax` then `shift` equals SQL's `MAX(...) ... AND 1 PRECEDING`: the maximum of all earlier rows, excluding the current one.
- The key is a running count of block starts, the same idea as islands (date minus row number is not needed because ranges are compared explicitly).
- Dialects (not executed here): the running MAX window works in PostgreSQL, MySQL 8, BigQuery and Snowflake as I remember it; the oneuptime article I read shows ClickHouse syntax for the same idea. Dates would use `DATE` columns.

**Follow-ups:**
- Merge ranges with inclusive end dates (Q16)? Compare `start > date(prev_max_end, '+1 day')` to also merge adjacent days.
- Total booked time per room after merging? Sum the block lengths, which avoids double counting overlaps.
- Free time between blocks? The gap is block start minus the previous block end (Q37 covers coverage gaps).

**Common mistakes:**
- Comparing to the previous row's end instead of the running maximum (contained intervals shrink the block).
- Using `>=` and merging or not merging touching intervals without saying so.
- Not sorting by start (and end) before `cummax`.
- Running `cummax` without `groupby("room_id")`, so rooms leak into each other.
- Leaving NULL ends in the data.

### Q29 ⭐⭐ 🟡 pandas concurrent sessions: translate the +1/-1 sweep. Build the events frame with pd.concat of (login_ts, +1) and (logout_ts, -1), sort by time with ends before starts at ties, cumsum the deltas, take the maximum and the first time it is reached. Assert equality with the SQL peak. Explain why sorting by time alone gives an unstable result at ties and how to make it deterministic.
**Asked at:** Itzik Ben-Gan interval packing and gaps-and-islands articles (search snippets only, not opened) and the Oracle SQL blog on longest and current streaks (snippet only); guides and not candidate reports; senior analyst and data engineer rounds
**Say this first (1 line):** Turn each session into two events, +1 at login and -1 at logout, sort them by time with the -1 events first at equal times, take a running sum (the number of open sessions after each event), then the max of the running sum is the peak and the earliest time it equals the peak is when it first happens; sorting by time alone leaves the order of tied events to chance.

**Schema and sample data:** seven sessions, inserted out of order, half-open intervals [login, logout): a session that ends at 10:00 is not open at 10:00 for a session starting at 10:00. Users 1 and 7 both log in at 09:00 and out at 10:00 (an identical duplicate), user 2 is 09:30 to 10:30, user 3 is 10:00 to 11:00, user 4 is 10:00 to 10:15, so at 10:00 two sessions end and two start while one stays open. User 5 has a NULL logout and an as-of time of 12:30 (fixed, not today). User 6 is a zero-length session at 13:00.
```sql
CREATE TABLE sessions(user_id INTEGER, login_ts TEXT, logout_ts TEXT);
INSERT INTO sessions VALUES
 (3,'2024-03-01 10:00:00','2024-03-01 11:00:00'),
 (1,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (2,'2024-03-01 09:30:00','2024-03-01 10:30:00'),
 (4,'2024-03-01 10:00:00','2024-03-01 10:15:00'),
 (7,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (5,'2024-03-01 12:00:00',NULL),
 (6,'2024-03-01 13:00:00','2024-03-01 13:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block. The window uses `ORDER BY ts, delta` so a -1 comes before a +1 at the same timestamp.
```sql
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions
  UNION ALL
  SELECT COALESCE(logout_ts, '2024-03-01 12:30:00') AS ts, -1 AS delta FROM sessions
), r AS (
  SELECT ts, delta,
         SUM(delta) OVER (ORDER BY ts, delta
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
  FROM ev
)
SELECT (SELECT MAX(concurrent) FROM r) AS peak,
       (SELECT MIN(ts) FROM r WHERE concurrent = (SELECT MAX(concurrent) FROM r)) AS first_reached
```

**pandas answer:** the body of `peak_pandas` in the Code block (default arguments are the correct ordering):
```py
logout = sessions["logout_ts"].fillna(as_of)
starts = pd.DataFrame({"ts": pd.to_datetime(sessions["login_ts"]), "delta": 1})
ends = pd.DataFrame({"ts": pd.to_datetime(logout), "delta": -1})
parts = {"start": starts, "end": ends}
ev = pd.concat([parts[k] for k in concat_order], ignore_index=True)
ev = ev.sort_values(list(sort_cols), **({"kind": kind} if kind else {})).reset_index(drop=True)
ev["concurrent"] = ev["delta"].cumsum()
peak = int(ev["concurrent"].max())
first_reached = ev.loc[ev["concurrent"] == peak, "ts"].min()
```

**Example:** events in order (ends before starts at 10:00): 09:00 +1 (1), 09:00 +1 (2), 09:30 +1 (3), 10:00 -1 (2), 10:00 -1 (1), 10:00 +1 (2), 10:00 +1 (3), 10:15 -1 (2), 10:30 -1 (1), 11:00 -1 (0), 12:00 +1 (1), 12:30 -1 for the open session (0), 13:00 -1 then +1 for the zero-length one (-1 then 0). The maximum is 3, first reached at 09:30 (and again at 10:00 after the tie). If starts were placed before ends at 10:00 the sum would reach 3 + 2 = 5 before the ends are applied, which is wrong: sessions that end exactly at 10:00 are not open together with those that start at 10:00.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas results (peak and first time; scalar pair, no row order). The remaining lines run the tie variants.
```python
# Q29: concurrent sessions peak via the +1/-1 sweep in SQL and pandas; ties at the same timestamp
import sqlite3
import pandas as pd

AS_OF = "2024-03-01 12:30:00"
SCHEMA = """
CREATE TABLE sessions(user_id INTEGER, login_ts TEXT, logout_ts TEXT);
INSERT INTO sessions VALUES
 (3,'2024-03-01 10:00:00','2024-03-01 11:00:00'),
 (1,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (2,'2024-03-01 09:30:00','2024-03-01 10:30:00'),
 (4,'2024-03-01 10:00:00','2024-03-01 10:15:00'),
 (7,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (5,'2024-03-01 12:00:00',NULL),
 (6,'2024-03-01 13:00:00','2024-03-01 13:00:00');
"""
SQL_MAIN = """
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions
  UNION ALL
  SELECT COALESCE(logout_ts, '2024-03-01 12:30:00') AS ts, -1 AS delta FROM sessions
), r AS (
  SELECT ts, delta,
         SUM(delta) OVER (ORDER BY ts, delta
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
  FROM ev
)
SELECT (SELECT MAX(concurrent) FROM r) AS peak,
       (SELECT MIN(ts) FROM r WHERE concurrent = (SELECT MAX(concurrent) FROM r)) AS first_reached
"""
SQL_STARTS_FIRST = SQL_MAIN.replace("ORDER BY ts, delta\n", "ORDER BY ts, delta DESC\n")
SQL_TSONLY_ROWS = SQL_MAIN.replace("ORDER BY ts, delta\n", "ORDER BY ts\n")
SQL_TSONLY_RANGE = SQL_MAIN.replace("ORDER BY ts, delta\n", "ORDER BY ts\n").replace("ROWS BETWEEN", "RANGE BETWEEN")
SQL_TRACE = SQL_MAIN.split("SELECT (SELECT MAX")[0] + "SELECT ts, delta, concurrent FROM r ORDER BY ts, delta"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("event trace (ends before starts at equal timestamps):")
print(pd.read_sql_query(SQL_TRACE, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL peak:")
print(sql_df.to_string(index=False))
print("wrong, starts before ends at ties (ORDER BY ts, delta DESC):", con.execute(SQL_STARTS_FIRST).fetchone())
print("ORDER BY ts only with ROWS frame (arbitrary tie order):", con.execute(SQL_TSONLY_ROWS).fetchone())
print("ORDER BY ts only with the default-style RANGE frame (ties netted together):", con.execute(SQL_TSONLY_RANGE).fetchone())

sessions = pd.read_sql_query("SELECT * FROM sessions", con)
def peak_pandas(sessions, as_of=AS_OF, sort_cols=("ts", "delta"), concat_order=("start", "end"), kind=None):
    # pd:main
    logout = sessions["logout_ts"].fillna(as_of)
    starts = pd.DataFrame({"ts": pd.to_datetime(sessions["login_ts"]), "delta": 1})
    ends = pd.DataFrame({"ts": pd.to_datetime(logout), "delta": -1})
    parts = {"start": starts, "end": ends}
    ev = pd.concat([parts[k] for k in concat_order], ignore_index=True)
    ev = ev.sort_values(list(sort_cols), **({"kind": kind} if kind else {})).reset_index(drop=True)
    ev["concurrent"] = ev["delta"].cumsum()
    peak = int(ev["concurrent"].max())
    first_reached = ev.loc[ev["concurrent"] == peak, "ts"].min()
    # pd:end
    return peak, first_reached.strftime("%Y-%m-%d %H:%M:%S")
peak, first = peak_pandas(sessions)
print("pandas peak:", peak, first)
assert (peak, first) == (int(sql_df["peak"][0]), sql_df["first_reached"][0])  # scalar result, no row order
# ties: sorting by time alone depends on the input order of the concatenated frames
print("sort by ts only, stable, starts concatenated first:", peak_pandas(sessions, sort_cols=("ts",), concat_order=("start", "end"), kind="stable"))
print("sort by ts only, stable, ends concatenated first:", peak_pandas(sessions, sort_cols=("ts",), concat_order=("end", "start"), kind="stable"))
print("sort by ts only, default kind, starts first:", peak_pandas(sessions, sort_cols=("ts",), concat_order=("start", "end")))
print("sort by ts, delta, either concat order:", peak_pandas(sessions, concat_order=("start", "end")), peak_pandas(sessions, concat_order=("end", "start")))
# edge cases: empty and single row
one = sessions.iloc[:1]
print("single session:", peak_pandas(one))
print("asserts passed")
```

**Output (my run):**
```text
event trace (ends before starts at equal timestamps):
                 ts  delta  concurrent
2024-03-01 09:00:00      1           1
2024-03-01 09:00:00      1           2
2024-03-01 09:30:00      1           3
2024-03-01 10:00:00     -1           2
2024-03-01 10:00:00     -1           1
2024-03-01 10:00:00      1           2
2024-03-01 10:00:00      1           3
2024-03-01 10:15:00     -1           2
2024-03-01 10:30:00     -1           1
2024-03-01 11:00:00     -1           0
2024-03-01 12:00:00      1           1
2024-03-01 12:30:00     -1           0
2024-03-01 13:00:00     -1          -1
2024-03-01 13:00:00      1           0
SQL peak:
 peak       first_reached
    3 2024-03-01 09:30:00
wrong, starts before ends at ties (ORDER BY ts, delta DESC): (5, '2024-03-01 10:00:00')
ORDER BY ts only with ROWS frame (arbitrary tie order): (5, '2024-03-01 10:00:00')
ORDER BY ts only with the default-style RANGE frame (ties netted together): (3, '2024-03-01 09:30:00')
pandas peak: 3 2024-03-01 09:30:00
sort by ts only, stable, starts concatenated first: (5, '2024-03-01 10:00:00')
sort by ts only, stable, ends concatenated first: (3, '2024-03-01 09:30:00')
sort by ts only, default kind, starts first: (5, '2024-03-01 10:00:00')
sort by ts, delta, either concat order: (3, '2024-03-01 09:30:00') (3, '2024-03-01 09:30:00')
single session: (1, '2024-03-01 10:00:00')
asserts passed
```

**Edge cases:**
- Ties at one timestamp: with `ORDER BY ts, delta DESC` (starts first) SQL returned a peak of 5 at 10:00, and `ORDER BY ts` with a ROWS frame also returned 5 in my run, which is arbitrary tie order and not guaranteed. With a RANGE frame and `ORDER BY ts` ties are netted together (3 at 09:30), which is correct here but only because the frame treats equal timestamps as one group.
- pandas: sorting by `ts` only with `kind="stable"` keeps the concatenation order, so concatenating starts first gave 5 and ends first gave 3. The default `sort_values` kind on one key also gave 5 in this run, which is not a guarantee either way (see Q28 for the stability test). Sorting by `["ts", "delta"]` gave 3 for both concatenation orders.
- NULL logout (user 5): `COALESCE` to the fixed as-of time; without it the -1 event would have a NULL time (sorted first in SQLite) and the sum would be wrong. NaT would not sort the same way in pandas (`sort_values` puts NaT last by default), so fill it.
- Zero-length session (user 6): the -1 sorts before its +1, so the running sum dips to -1 for an instant (visible in the trace); the peak is unaffected. Remove zero-length sessions first if the dip matters.
- Duplicate sessions (users 1 and 7) count twice, as they should if they are two sessions.
- Single session: peak 1, first reached at its login (checked on one row in the script). Unsorted input is fine since the events are sorted.
- First time reached: `MIN(ts)` among events whose running sum equals the peak. If the peak is reached again later, only the first is reported.

**Then explain:**
- The running sum after an event is the number of open sessions at that moment; the max over events is the peak because the count only changes at events.
- Convention: half-open intervals (end excluded) are why -1 goes first; with closed intervals (a logout at 10:00 still counts at 10:00) the order would flip. State it.
- Equal-timestamp events form a group; the count inside that group is not meaningful, only the count after the whole group.
- `pd.concat` keeps the frame order, which matters for ties; `ignore_index=True` avoids duplicate index labels.
- The self-join alternative counts sessions overlapping each login and is O(n squared) (Q17 has the SQL version in this part).

**Follow-ups:**
- Peak per day or per room? Add the key to PARTITION BY (SQL) or groupby (pandas).
- All times when the count equals the peak? Return every row whose running sum equals the max.
- Count of concurrent sessions at a given instant? `COUNT(*) WHERE login <= t AND (logout IS NULL OR logout > t)`.

**Common mistakes:**
- Sorting by time only and letting ties decide the peak.
- Putting starts before ends for half-open intervals (peak overstated, 5 instead of 3 in the data).
- Forgetting `ignore_index=True` after `concat`.
- Leaving NULL logouts unfilled.
- Reporting the last, not the first, time the peak is reached.

### Q30 ⭐⭐ 🔴 Booking conflicts: bookings(booking_id, room_id, start_ts, end_ts). Find all pairs of bookings in the same room that overlap using a self join with a.start_ts < b.end_ts AND b.start_ts < a.end_ts AND a.booking_id < b.booking_id (why the last condition, and why the half-open overlap test is correct). Show a booking ending exactly when another starts (not a conflict) versus an inclusive end date convention (a conflict), and a booking fully inside another.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Two bookings in the same room overlap when `a.start < b.end AND b.start < a.end` (half-open intervals, so one ending exactly when the other starts is not a conflict), and `a.booking_id < b.booking_id` keeps each unordered pair once and drops the pairing of a booking with itself.

**Schema and sample data:** nine bookings inserted out of order. Room 1: booking 1 is 09:00-11:00; booking 2 is 11:00-12:00 (starts exactly when 1 ends); booking 3 is 09:30-10:00 (inside booking 1); booking 4 is 10:30-11:30 (overlaps both 1 and 2); booking 5 is 12:00-13:00 (starts exactly when 2 ends); booking 9 has a NULL end. Room 2: bookings 6 and 7 are identical 09:00-10:00. Room 3: a single booking. A second table `stays` uses inclusive end dates: stay 1 is 1 to 3 March, stay 2 is 3 to 5 March (they share the night of the 3rd), stay 3 is 6 to 7 March.
```sql
CREATE TABLE bookings(booking_id INTEGER, room_id INTEGER, start_ts TEXT, end_ts TEXT);
INSERT INTO bookings VALUES
 (5,1,'2024-03-01 12:00','2024-03-01 13:00'),
 (1,1,'2024-03-01 09:00','2024-03-01 11:00'),
 (2,1,'2024-03-01 11:00','2024-03-01 12:00'),
 (3,1,'2024-03-01 09:30','2024-03-01 10:00'),
 (4,1,'2024-03-01 10:30','2024-03-01 11:30'),
 (6,2,'2024-03-01 09:00','2024-03-01 10:00'),
 (7,2,'2024-03-01 09:00','2024-03-01 10:00'),
 (8,3,'2024-03-01 09:00','2024-03-01 10:00'),
 (9,1,'2024-03-01 14:00',NULL);
CREATE TABLE stays(booking_id INTEGER, room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO stays VALUES (1,1,'2024-03-01','2024-03-03'),(2,1,'2024-03-03','2024-03-05'),(3,1,'2024-03-06','2024-03-07');
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT a.booking_id AS booking_a, b.booking_id AS booking_b, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_ts < b.end_ts
 AND b.start_ts < a.end_ts
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
```

**pandas answer:** identical to the Code block (a merge on `room_id` is the self join):
```py
b = bookings.copy()
b["start_ts"] = pd.to_datetime(b["start_ts"])
b["end_ts"] = pd.to_datetime(b["end_ts"])
m = b.merge(b, on="room_id", suffixes=("_a", "_b"))
hit = m[(m["start_ts_a"] < m["end_ts_b"]) & (m["start_ts_b"] < m["end_ts_a"]) & (m["booking_id_a"] < m["booking_id_b"])]
pd_df = (hit[["booking_id_a", "booking_id_b", "room_id"]]
         .rename(columns={"booking_id_a": "booking_a", "booking_id_b": "booking_b"})
         .sort_values(["booking_a", "booking_b"]).reset_index(drop=True))
```

**Example:** pairs in room 1 with `a.id < b.id`. (1, 2): 09:00 < 12:00 is true, but 11:00 < 11:00 is false, so touching is not a conflict. (1, 3): 09:00 < 10:00 and 09:30 < 11:00, a conflict (3 is inside 1). (1, 4): 09:00 < 11:30 and 10:30 < 11:00, a conflict. (2, 4): 11:00 < 11:30 and 10:30 < 12:00, a conflict. (2, 5): 11:00 < 13:00 but 12:00 < 12:00 is false, not a conflict. (3, 4): 09:30 < 11:30 but 10:30 < 10:00 is false. Room 2: (6, 7) are identical, 09:00 < 10:00 both ways, a conflict. Booking 9 has a NULL end, so every comparison with it is NULL and it never matches. Result: (1,3), (1,4), (2,4), (6,7).

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `booking_a, booking_b`.
```python
# Q30: booking conflicts via self join; half-open overlap test; touching vs inclusive end dates; containment
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE bookings(booking_id INTEGER, room_id INTEGER, start_ts TEXT, end_ts TEXT);
INSERT INTO bookings VALUES
 (5,1,'2024-03-01 12:00','2024-03-01 13:00'),
 (1,1,'2024-03-01 09:00','2024-03-01 11:00'),
 (2,1,'2024-03-01 11:00','2024-03-01 12:00'),
 (3,1,'2024-03-01 09:30','2024-03-01 10:00'),
 (4,1,'2024-03-01 10:30','2024-03-01 11:30'),
 (6,2,'2024-03-01 09:00','2024-03-01 10:00'),
 (7,2,'2024-03-01 09:00','2024-03-01 10:00'),
 (8,3,'2024-03-01 09:00','2024-03-01 10:00'),
 (9,1,'2024-03-01 14:00',NULL);
CREATE TABLE stays(booking_id INTEGER, room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO stays VALUES (1,1,'2024-03-01','2024-03-03'),(2,1,'2024-03-03','2024-03-05'),(3,1,'2024-03-06','2024-03-07');
"""
SQL_MAIN = """
SELECT a.booking_id AS booking_a, b.booking_id AS booking_b, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_ts < b.end_ts
 AND b.start_ts < a.end_ts
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
SQL_NO_ORDER = """
SELECT a.booking_id AS booking_a, b.booking_id AS booking_b
FROM bookings a JOIN bookings b
  ON a.room_id = b.room_id AND a.start_ts < b.end_ts AND b.start_ts < a.end_ts
ORDER BY a.booking_id, b.booking_id
"""
SQL_INCLUSIVE_TS = """
SELECT a.booking_id AS booking_a, b.booking_id AS booking_b
FROM bookings a JOIN bookings b
  ON a.room_id = b.room_id AND a.start_ts <= b.end_ts AND b.start_ts <= a.end_ts AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
# stays use an inclusive end date: both the first and the last night are occupied
SQL_STAYS_INCLUSIVE = """
SELECT a.booking_id AS stay_a, b.booking_id AS stay_b
FROM stays a JOIN stays b
  ON a.room_id = b.room_id AND a.start_date <= b.end_date AND b.start_date <= a.end_date AND a.booking_id < b.booking_id
ORDER BY 1, 2
"""
SQL_STAYS_HALFOPEN_WRONG = """
SELECT a.booking_id AS stay_a, b.booking_id AS stay_b
FROM stays a JOIN stays b
  ON a.room_id = b.room_id AND a.start_date < b.end_date AND b.start_date < a.end_date AND a.booking_id < b.booking_id
ORDER BY 1, 2
"""
SQL_STAYS_NORMALISED = """
SELECT a.booking_id AS stay_a, b.booking_id AS stay_b
FROM stays a JOIN stays b
  ON a.room_id = b.room_id
 AND a.start_date < date(b.end_date, '+1 day')
 AND b.start_date < date(a.end_date, '+1 day')
 AND a.booking_id < b.booking_id
ORDER BY 1, 2
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL conflicts (half-open [start, end)):")
print(sql_df.to_string(index=False))
nb = pd.read_sql_query(SQL_NO_ORDER, con)
print("without a.booking_id < b.booking_id:", len(nb), "rows instead of", len(sql_df), "(self pairs and mirrored pairs)")
print(nb.head(8).to_string(index=False))
print("wrong: inclusive timestamp test <=, bookings 1 and 2 now collide:")
print(pd.read_sql_query(SQL_INCLUSIVE_TS, con).to_string(index=False))
print("stays with INCLUSIVE end dates, inclusive test (correct for that convention):")
print(pd.read_sql_query(SQL_STAYS_INCLUSIVE, con).to_string(index=False))
print("same stays with the half-open test (misses the shared 2024-03-03):")
print(pd.read_sql_query(SQL_STAYS_HALFOPEN_WRONG, con).to_string(index=False))
print("same stays normalised to half-open with date(end, '+1 day'):")
print(pd.read_sql_query(SQL_STAYS_NORMALISED, con).to_string(index=False))

bookings = pd.read_sql_query("SELECT * FROM bookings", con)
# pd:main
b = bookings.copy()
b["start_ts"] = pd.to_datetime(b["start_ts"])
b["end_ts"] = pd.to_datetime(b["end_ts"])
m = b.merge(b, on="room_id", suffixes=("_a", "_b"))
hit = m[(m["start_ts_a"] < m["end_ts_b"]) & (m["start_ts_b"] < m["end_ts_a"]) & (m["booking_id_a"] < m["booking_id_b"])]
pd_df = (hit[["booking_id_a", "booking_id_b", "room_id"]]
         .rename(columns={"booking_id_a": "booking_a", "booking_id_b": "booking_b"})
         .sort_values(["booking_a", "booking_b"]).reset_index(drop=True))
# pd:end
print("pandas conflicts:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df, check_dtype=False)  # both ordered by booking_a, booking_b
print("NaT comparisons are False, so booking 9 (NULL end) never conflicts:", 9 not in set(pd_df["booking_a"]) | set(pd_df["booking_b"]))
print("asserts passed")
```

**Output (my run):**
```text
SQL conflicts (half-open [start, end)):
 booking_a  booking_b  room_id
         1          3        1
         1          4        1
         2          4        1
         6          7        2
without a.booking_id < b.booking_id: 16 rows instead of 4 (self pairs and mirrored pairs)
 booking_a  booking_b
         1          1
         1          3
         1          4
         2          2
         2          4
         3          1
         3          3
         4          1
wrong: inclusive timestamp test <=, bookings 1 and 2 now collide:
 booking_a  booking_b
         1          2
         1          3
         1          4
         2          4
         2          5
         6          7
stays with INCLUSIVE end dates, inclusive test (correct for that convention):
 stay_a  stay_b
      1       2
same stays with the half-open test (misses the shared 2024-03-03):
Empty DataFrame
Columns: [stay_a, stay_b]
Index: []
same stays normalised to half-open with date(end, '+1 day'):
 stay_a  stay_b
      1       2
pandas conflicts:
 booking_a  booking_b  room_id
         1          3        1
         1          4        1
         2          4        1
         6          7        2
NaT comparisons are False, so booking 9 (NULL end) never conflicts: True
asserts passed
```

**Edge cases:**
- Why `a.booking_id < b.booking_id`: without it the join pairs every booking with itself (always overlapping itself) and returns each real conflict twice, once as (a, b) and once as (b, a): 16 rows in my run (8 self pairs plus 4 conflicts in both directions) instead of 4. `<>` would remove self pairs but still return mirrored pairs.
- Why the half-open test is the right one: `a.start < b.end AND b.start < a.end` is the negation of "a ends before b starts or b ends before a starts" when an end is exclusive. It covers partial overlap, containment (booking 3 inside booking 1) and identical intervals in one condition, with no case analysis.
- Touching (booking 1 ends at 11:00, booking 2 starts at 11:00): not a conflict under half-open. The inclusive `<=` test (`SQL_INCLUSIVE_TS`) turned it into a conflict, and also added (2, 5), in my run.
- Inclusive end dates (`stays`): stay 1 covers 3 March and stay 2 starts on 3 March, so they conflict, and the inclusive test `a.start <= b.end AND b.start <= a.end` finds (1, 2). The half-open test returned no rows, so it misses that conflict. A safe habit is to normalise to half-open: `date(end_date, '+1 day')` as the exclusive end, which returned (1, 2) as well. State which convention the table uses.
- Duplicates: identical bookings (6 and 7) conflict; identical `booking_id` values would make `<` skip them, so the id must be unique.
- NULL end (booking 9): never returned, in SQL (NULL comparison) and in pandas (NaT comparison is False). If an open booking should conflict with everything after its start, use `COALESCE(end_ts, '9999-12-31')`.
- Single booking room (room 3): no pairs. Unsorted input does not matter, a join has no order.
- Performance: the self join is quadratic within each room; an index on `(room_id, start_ts)` helps, and a running-MAX window finds whether any conflict exists without listing pairs (not benchmarked here).

**Then explain:**
- Overlap is easier to reason about as the opposite of "disjoint": two intervals are disjoint when one ends before (or when, for half-open) the other starts.
- The id condition is a de-duplication of unordered pairs; it is the same trick as `a.id < b.id` in other self joins.
- With timestamps, half-open is the norm; with whole days written as inclusive start and end dates, the inclusive form is natural. The two forms must not be mixed.
- Dialects (not executed here): PostgreSQL has range types with `&&` and exclusion constraints that can prevent conflicts at insert time; MySQL and SQL Server need the explicit test.

**Follow-ups:**
- Only list bookings that conflict with at least one other? `EXISTS` with the same condition.
- Prevent conflicts at insert time? A constraint or a locking check, not a query (engine specific).
- Merge the conflicting bookings into blocks? See Q28 and Q16.

**Common mistakes:**
- Omitting the id condition and getting self pairs and mirrored pairs.
- Using `<=` for timestamp intervals so back-to-back bookings conflict.
- Using the half-open test on inclusive end dates and missing conflicts that share a day.
- Writing only one of the two comparisons, which misses containment or partial overlaps.
- Forgetting `a.room_id = b.room_id`.
