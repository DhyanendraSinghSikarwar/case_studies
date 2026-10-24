### Q1 ⭐⭐⭐ 🟢 Why does date minus ROW_NUMBER identify islands? logins(user_id, login_date) with one row per user per day. Explain with a worked table why login_date minus ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) is constant inside a run of consecutive days and changes when a day is skipped, and return each user's islands as streak_start, streak_end and days using julianday(login_date) - ROW_NUMBER() as the day-number key in SQLite (SQLite date arithmetic gives no integer day type, so state why julianday is used). Say what breaks if the rows are not unique per day.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** Inside a run of consecutive days the date goes up by 1 and `ROW_NUMBER()` also goes up by 1, so their difference is constant; a skipped day moves the date by 2 but the row number by 1, so the difference jumps, and that constant is the island id.

**Schema and sample data:** three users, inserted out of order. User 1 has 03-01..03-03 then a gap (03-04 missing) then 03-05..03-06; user 2 has one day; user 3 spans a year end (2024-12-30 to 2025-01-02). One row per user per day (duplicates are Q8).
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-05'),(1,'2024-03-01'),(1,'2024-03-03'),(1,'2024-03-06'),(1,'2024-03-02'),
 (2,'2024-03-10'),
 (3,'2025-01-02'),(3,'2024-12-30'),(3,'2025-01-01'),(3,'2024-12-31');
```

**SQL answer:** `SQL_MAIN` in the Code block. The day number is `julianday(login_date)`, the key is day number minus the per-user row number, and each island is one `GROUP BY user_id, grp`:
```sql
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
```
Why `julianday`: SQLite has no date type, so `'2024-03-02' - '2024-03-01'` is text coerced to the number 2024 minus 2024, which is 0, not 1 (shown in the Code block as wrong 1). `julianday()` turns an ISO date into a real day number (midnight dates end in `.5`, for example 2460370.5), so subtracting an integer row number is meaningful. An integer-only variant is `unixepoch(login_date) / 86400 - ROW_NUMBER() ...` (`SQL_EPOCH`); both gave identical islands in my run.

**pandas answer:** same logic, shown once here and identical to the Code block. `cumcount()` is the zero-based row number, so add 1; subtracting a timedelta of `rn` days from the date gives the same constant key.
```py
l = logins.assign(login_date=pd.to_datetime(logins["login_date"])).sort_values(["user_id", "login_date"])
l["rn"] = l.groupby("user_id").cumcount() + 1
l["key"] = l["login_date"] - pd.to_timedelta(l["rn"], unit="D")
pd_df = (l.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), days=("login_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
```

**Example (by hand):** user 1, sorted: 03-01, 03-02, 03-03, 03-05, 03-06 with row numbers 1..5.
- Day numbers (julianday) are 2460370.5, 371.5, 372.5, 374.5, 375.5 (the gap at 373.5 is the missing 03-04).
- Day number minus row number: 369.5, 369.5, 369.5, 370.5, 370.5 (shown with the leading 2460 dropped). Three equal values, then a jump of exactly 1, then two equal values.
- So two islands: 03-01 to 03-03 (3 days) and 03-05 to 03-06 (2 days).
- User 2: one row, key 2460378.5, one island of 1 day.
- User 3: 2024-12-30, 2024-12-31, 2025-01-01, 2025-01-02 have day numbers 674.5, 675.5, 676.5, 677.5 (2460000 dropped) and row numbers 1..4, so one constant key and one island of 4 days. The day arithmetic does not care about the month or year change.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas islands after sorting both by `user_id, streak_start, streak_end` (dates formatted back to `YYYY-MM-DD` text).
```python
# Q1: why date minus ROW_NUMBER identifies islands (SQLite julianday key) + pandas twin
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-05'),(1,'2024-03-01'),(1,'2024-03-03'),(1,'2024-03-06'),(1,'2024-03-02'),
 (2,'2024-03-10'),
 (3,'2025-01-02'),(3,'2024-12-30'),(3,'2025-01-01'),(3,'2024-12-31');
"""
SQL_KEYS = """
SELECT user_id, login_date,
       ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn,
       julianday(login_date) AS day_no,
       julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
FROM logins
ORDER BY user_id, login_date
"""
SQL_MAIN = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_EPOCH = """
WITH x AS (
  SELECT user_id, login_date,
         unixepoch(login_date) / 86400
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_WRONG_TEXT = """
WITH x AS (
  SELECT user_id, login_date,
         login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_WRONG_YMD = """
WITH x AS (
  SELECT user_id, login_date,
         CAST(strftime('%Y%m%d', login_date) AS INTEGER)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("key table (day_no is julianday, grp = day_no - rn):")
print(pd.read_sql_query(SQL_KEYS, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nislands (SQL julianday):")
print(sql_df.to_string(index=False))
epoch_df = pd.read_sql_query(SQL_EPOCH, con)
pd.testing.assert_frame_equal(epoch_df, sql_df)
print("\nunixepoch/86400 integer key gives the same islands: True")
print("\nwrong 1, login_date - rn (text coerced to 2024 / 2025):")
print(pd.read_sql_query(SQL_WRONG_TEXT, con).to_string(index=False))
print("\nwrong 2, yyyymmdd - rn (breaks at month and year ends):")
print(pd.read_sql_query(SQL_WRONG_YMD, con).query("user_id == 3").to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
l = logins.assign(login_date=pd.to_datetime(logins["login_date"])).sort_values(["user_id", "login_date"])
l["rn"] = l.groupby("user_id").cumcount() + 1
l["key"] = l["login_date"] - pd.to_timedelta(l["rn"], unit="D")
pd_df = (l.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), days=("login_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
# pd:end
for c in ("streak_start", "streak_end"):
    pd_df[c] = pd_df[c].dt.strftime("%Y-%m-%d")
# compared after sorting by user_id, streak_start, streak_end
pd.testing.assert_frame_equal(pd_df, sql_df)
print("\npandas islands equal SQL islands: True")

# duplicates in the date column: the key splits the run
con.executescript("""
CREATE TABLE dup(user_id INTEGER, login_date TEXT);
INSERT INTO dup VALUES (9,'2024-03-01'),(9,'2024-03-01'),(9,'2024-03-02');
""")
print("\nduplicate day 03-01 (one user, run is really 2 days):")
print(pd.read_sql_query(SQL_MAIN.replace("FROM logins", "FROM dup"), con).to_string(index=False))

# NULL date and empty table
con.execute("INSERT INTO logins VALUES (2, NULL)")
print("\nwith a NULL login_date for user 2, no filter:")
print(pd.read_sql_query(SQL_MAIN, con).query("user_id == 2").to_string(index=False))
sql_null = pd.read_sql_query(SQL_MAIN.replace("FROM logins", "FROM logins WHERE login_date IS NOT NULL"), con)
pd.testing.assert_frame_equal(sql_null, sql_df)
lp = pd.read_sql_query("SELECT * FROM logins", con)
lp = lp.assign(login_date=pd.to_datetime(lp["login_date"])).sort_values(["user_id", "login_date"])
lp["rn"] = lp.groupby("user_id").cumcount() + 1
lp["key"] = lp["login_date"] - pd.to_timedelta(lp["rn"], unit="D")
g = lp.groupby(["user_id", "key"]).size()
print("pandas, NULL kept, groups for user 2:", len(g.loc[2]), "(NaT key group silently dropped)")
con.execute("DELETE FROM logins")
print("empty table, SQL rows:", len(con.execute(SQL_MAIN).fetchall()))
# precision check: float julianday key vs integer unixepoch key on timestamps (3 consecutive days, same clock time)
import random
random.seed(7)
split_jd = split_ux = trials = 0
for _ in range(2000):
    start = "%04d-%02d-%02d %02d:%02d:%02d.%03d" % (random.choice([2020, 2024, 2026]), random.randint(1, 12),
            random.randint(1, 25), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59), random.randint(0, 999))
    jd, ux = set(), set()
    for i in range(3):
        ts = con.execute("SELECT strftime('%Y-%m-%d %H:%M:%f', ?, ?)", (start, "+%d day" % i)).fetchone()[0]
        jd.add(con.execute("SELECT julianday(?) - ?", (ts, i + 1)).fetchone()[0])
        ux.add(con.execute("SELECT unixepoch(?, 'subsec') - 86400 * ?", (ts, i + 1)).fetchone()[0])
    trials += 1
    split_jd += len(jd) > 1
    split_ux += len(ux) > 1
print("timestamp trials:", trials, "| julianday key split a run:", split_jd, "| unixepoch subsec key split a run:", split_ux)
print("asserts passed")
```

**Output (my run):**
```text
key table (day_no is julianday, grp = day_no - rn):
 user_id login_date  rn    day_no       grp
       1 2024-03-01   1 2460370.5 2460369.5
       1 2024-03-02   2 2460371.5 2460369.5
       1 2024-03-03   3 2460372.5 2460369.5
       1 2024-03-05   4 2460374.5 2460370.5
       1 2024-03-06   5 2460375.5 2460370.5
       2 2024-03-10   1 2460379.5 2460378.5
       3 2024-12-30   1 2460674.5 2460673.5
       3 2024-12-31   2 2460675.5 2460673.5
       3 2025-01-01   3 2460676.5 2460673.5
       3 2025-01-02   4 2460677.5 2460673.5

islands (SQL julianday):
 user_id streak_start streak_end  days
       1   2024-03-01 2024-03-03     3
       1   2024-03-05 2024-03-06     2
       2   2024-03-10 2024-03-10     1
       3   2024-12-30 2025-01-02     4

unixepoch/86400 integer key gives the same islands: True

wrong 1, login_date - rn (text coerced to 2024 / 2025):
 user_id streak_start streak_end  days
       1   2024-03-01 2024-03-01     1
       1   2024-03-02 2024-03-02     1
       1   2024-03-03 2024-03-03     1
       1   2024-03-05 2024-03-05     1
       1   2024-03-06 2024-03-06     1
       2   2024-03-10 2024-03-10     1
       3   2024-12-30 2024-12-30     1
       3   2024-12-31 2025-01-01     2
       3   2025-01-02 2025-01-02     1

wrong 2, yyyymmdd - rn (breaks at month and year ends):
 user_id streak_start streak_end  days
       3   2024-12-30 2024-12-31     2
       3   2025-01-01 2025-01-02     2

pandas islands equal SQL islands: True

duplicate day 03-01 (one user, run is really 2 days):
 user_id streak_start streak_end  days
       9   2024-03-01 2024-03-01     1
       9   2024-03-01 2024-03-02     2

with a NULL login_date for user 2, no filter:
 user_id streak_start streak_end  days
       2          NaN        NaN     1
       2   2024-03-10 2024-03-10     1
pandas, NULL kept, groups for user 2: 1 (NaT key group silently dropped)
empty table, SQL rows: 0
timestamp trials: 2000 | julianday key split a run: 0 | unixepoch subsec key split a run: 0
asserts passed
```

**Edge cases:**
- Skipped day: exact threshold. Dates exactly 1 day apart join the island (user 1, 03-01 to 03-02); dates exactly 2 days apart split it (03-03 to 03-05), because the key jumps by 1 per missing day.
- Two string-arithmetic mistakes, both in my run. `login_date - rn` coerces the text to 2024 or 2025, so the key falls by 1 on every row and every day becomes its own island (user 1 got five islands of 1; user 3 got a 2-day island only because the 2024 to 2025 change happens to cancel one step). `yyyymmdd - rn` works inside a month but cuts user 3's year-end run into two 2-day islands, because 20241231 to 20250101 is a jump of 8870, not 1.
- Duplicate days: the row number advances but the date does not, so the key moves. User 9 with 03-01 twice and 03-02 once came back as two islands (03-01 alone and 03-01 to 03-02, with `days = 2` counting the duplicate row, not two distinct days). Fix is in Q8.
- Unsorted input is fine: the window's `ORDER BY` defines the order, not the insertion order. In pandas the explicit `sort_values` is required, because `cumcount` follows the frame's current order.
- Single-row user: one island, start = end, days = 1 (user 2).
- NULL `login_date`: `julianday(NULL)` is NULL, SQLite sorts NULL first, so the NULL row got row number 1 and shifted the others by one equally (still constant) but formed its own island with NULL start and end (user 2 in my run). Filter `WHERE login_date IS NOT NULL` first. pandas behaves differently: `groupby` dropped the NaT-key group silently by default, so the NULL row just vanished (see the last lines of the output). Both end up equal once SQL filters NULLs, but know which one you are relying on.
- Empty table: SQL returns zero rows (the script printed 0 rows).
- Precision: `julianday` returns a float. With date-only values the `.5` values are exact in binary, so the equality in `GROUP BY` is safe. I also ran 2,000 random millisecond timestamps (three consecutive days at the same clock time): the float `julianday` key never split a run (0 of 2,000, last lines of the output). SQLite stores julianday internally as integer milliseconds, which is probably why; a float key is still a risk I cannot rule out in other engines (not executed), so for day numbers prefer an integer (`unixepoch()/86400` or, in other engines, a date-to-integer function). If timestamps (not dates) are stored, truncate to the date first with `date(ts)`.

**Then explain:**
- Why the trick works: `ROW_NUMBER()` counts how many logins came so far; the date counts calendar days. While nothing is skipped they move together, so their difference is frozen. A skipped day makes the date move ahead of the count, and the difference steps up for the rest of the run.
- The key itself is meaningless (2460369.5); only equality inside a user matters, so always `GROUP BY user_id, grp`, never `grp` alone.
- It needs one row per user per day. Same-day duplicates must be removed first (Q8).
- This is a variant of consecutive-value gaps; for plain `LAG` mechanics see Part 5, for ranking functions see Part 4.
- Dialects (not executed here): PostgreSQL can subtract an integer from a `DATE` directly (`login_date - ROW_NUMBER() OVER (...)::int`) and returns a date key; MySQL 8 uses `DATE_SUB(login_date, INTERVAL rn DAY)`; BigQuery uses `DATE_SUB(login_date, INTERVAL rn DAY)` (with `rn` as an integer expression). I did not run any of these.

**Follow-ups:**
- Longest streak per user? Reduce the islands with `ROW_NUMBER` ordered by `days DESC` (Q7).
- Users with at least N days? Filter `HAVING COUNT(*) >= N` (Q9).
- Why not use `LAG` and a flag? That works too (flag when gap > 1, then running `SUM`), and is the form that handles timestamps; the subtraction trick needs one pass less.

**Common mistakes:**
- Subtracting dates as strings (shown above) or as `yyyymmdd` numbers.
- Grouping by the key without the user id, which merges different users' islands that happen to share a key.
- Forgetting to remove duplicate days or NULL dates first.
- Using `RANK` or `DENSE_RANK` without thinking: `DENSE_RANK` is fine for duplicates (Q8), `RANK` is not (ties skip numbers).
- In pandas, using `cumcount()` without sorting first, or forgetting the `+ 1` (harmless here, since only constancy matters, but easy to get wrong when you print the key).

### Q2 ⭐⭐⭐ 🟢 Islands of consecutive integers: logs(log_id) holds ids such as 1,2,3,7,8,10 (unsorted insertion order, no duplicates) and a single-row island must be allowed. Return start_id, end_id and the count of each island using log_id - ROW_NUMBER() OVER (ORDER BY log_id) (the LeetCode 1285 Find the Start and End Number of Continuous Ranges pattern), and show what happens with an empty table, a single row and a NULL log_id (decide whether to drop it).
**Asked at:** public LeetCode-style problem bank (statements known from search snippets and mirrors such as doocs, walkccc and talentd; the leetcode.com pages returned HTTP 403 and were not opened), not candidate reports; analyst, data scientist and data engineer screens at product companies and GCCs
**Say this first (1 line):** Number the sorted ids with `ROW_NUMBER()`, subtract that from the id, and every run of consecutive ids shares one constant; `GROUP BY` that constant and take `MIN`, `MAX` and `COUNT` per island.

**Schema and sample data:** six ids inserted out of order; no duplicates. Sorted they are 1,2,3 | 7,8 | 10, so three islands, the last of one row.
```sql
CREATE TABLE logs(log_id INTEGER);
INSERT INTO logs VALUES (8),(1),(10),(3),(7),(2);
```

**SQL answer:** `SQL_MAIN` in the Code block. NULL ids are dropped before numbering (decision stated below):
```sql
WITH x AS (
  SELECT log_id,
         log_id - ROW_NUMBER() OVER (ORDER BY log_id) AS grp
  FROM logs
  WHERE log_id IS NOT NULL
)
SELECT MIN(log_id) AS start_id,
       MAX(log_id) AS end_id,
       COUNT(*) AS cnt
FROM x
GROUP BY grp
ORDER BY start_id
```
LeetCode 1285 itself asks for just `start_id` and `end_id`; I kept `cnt` as the question asks. I wrote this from the statement as I remember it (the page returned HTTP 403 in the research phase and was not opened).

**pandas answer:** same logic, shown once here and identical to the Code block. The sorted series is reindexed 0..n-1, so `s.index + 1` is the row number.
```py
    s = logs["log_id"].dropna().astype("int64").sort_values().reset_index(drop=True)
    grp = s - (s.index + 1)
    pd_df = (s.groupby(grp)
              .agg(start_id="min", end_id="max", cnt="size")
              .sort_values("start_id").reset_index(drop=True))
    
```
A second idiom that does not need a row number: `s.diff().ne(1).cumsum()` is the run key (a new island starts wherever the step from the previous id is not exactly 1). It is in the Code block and gave the same three islands.

**Example (by hand):** sorted ids 1,2,3,7,8,10 get row numbers 1..6.
- id minus row number: 0, 0, 0, 3, 3, 4.
- Key 0: ids 1..3, count 3. Key 3: ids 7..8, count 2. Key 4: id 10, count 1.
- The step from 3 to 7 (4 apart) and from 8 to 10 (exactly 2 apart, one id missing) both raise the key; 7 to 8 (exactly 1 apart) does not.
- Result: (1,3,3), (7,8,2), (10,10,1).

**Code:** run with `python3 -I`. The assert compares SQL and pandas after sorting both by `start_id` (the SQL has `ORDER BY start_id`; pandas sorts by `start_id`).
```python
# Q2: islands of consecutive integers (LeetCode 1285 pattern): log_id - ROW_NUMBER, plus pandas twins
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logs(log_id INTEGER);
INSERT INTO logs VALUES (8),(1),(10),(3),(7),(2);
"""
SQL_MAIN = """
WITH x AS (
  SELECT log_id,
         log_id - ROW_NUMBER() OVER (ORDER BY log_id) AS grp
  FROM logs
  WHERE log_id IS NOT NULL
)
SELECT MIN(log_id) AS start_id,
       MAX(log_id) AS end_id,
       COUNT(*) AS cnt
FROM x
GROUP BY grp
ORDER BY start_id
"""
SQL_NO_FILTER = SQL_MAIN.replace("  WHERE log_id IS NOT NULL\n", "")
SQL_DISTINCT = SQL_MAIN.replace("FROM logs", "FROM (SELECT DISTINCT log_id FROM logs)")

def sql_islands(con, sql=SQL_MAIN):
    return pd.read_sql_query(sql, con)

def pd_islands(logs):
    # pd:main
    s = logs["log_id"].dropna().astype("int64").sort_values().reset_index(drop=True)
    grp = s - (s.index + 1)
    pd_df = (s.groupby(grp)
              .agg(start_id="min", end_id="max", cnt="size")
              .sort_values("start_id").reset_index(drop=True))
    # pd:end
    return pd_df

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = sql_islands(con)
print("SQL islands:")
print(sql_df.to_string(index=False))
logs = pd.read_sql_query("SELECT * FROM logs", con)
pd_df = pd_islands(logs)
# compared after sorting by start_id
pd.testing.assert_frame_equal(pd_df, sql_df)
print("pandas islands equal SQL islands: True")

# second pandas idiom: diff().ne(1).cumsum() as run key (diff is float64 because the first value is NaN)
s = logs["log_id"].sort_values().reset_index(drop=True)
print("diff dtype:", s.diff().dtype, "| first diff:", s.diff().iloc[0], "| first diff != 1:", bool(s.diff().iloc[0] != 1))
run = s.diff().ne(1).cumsum()
alt = s.groupby(run).agg(start_id="min", end_id="max", cnt="size").reset_index(drop=True)
pd.testing.assert_frame_equal(alt, sql_df)
print("diff().ne(1).cumsum() version equals SQL: True")

# edge: single row, empty table, NULL, duplicate id
con.execute("CREATE TABLE one(log_id INTEGER)")
con.execute("INSERT INTO one VALUES (42)")
print("single row:", con.execute(SQL_MAIN.replace("FROM logs", "FROM one")).fetchall())
con.execute("INSERT INTO logs VALUES (NULL)")
print("NULL row, filtered:", len(sql_islands(con)), "islands")
print("NULL row, no filter:")
print(sql_islands(con, SQL_NO_FILTER).to_string(index=False))
logs_n = pd.read_sql_query("SELECT * FROM logs", con)
print("pandas column dtype with a NULL:", logs_n["log_id"].dtype)
pd.testing.assert_frame_equal(pd_islands(logs_n), sql_df)
con.execute("INSERT INTO logs VALUES (2)")
print("duplicate id 2, no DISTINCT:")
print(sql_islands(con).to_string(index=False))
dist = sql_islands(con, SQL_DISTINCT)
pd.testing.assert_frame_equal(dist, sql_df)
print("with SELECT DISTINCT: equals the clean result")
con.execute("DELETE FROM logs")
print("empty table, SQL rows:", len(sql_islands(con)))
empty = pd_islands(pd.read_sql_query("SELECT * FROM logs", con))
print("empty table, pandas rows:", len(empty), "| columns:", list(empty.columns))
print("asserts passed")
```

**Output (my run):**
```text
SQL islands:
 start_id  end_id  cnt
        1       3    3
        7       8    2
       10      10    1
pandas islands equal SQL islands: True
diff dtype: float64 | first diff: nan | first diff != 1: True
diff().ne(1).cumsum() version equals SQL: True
single row: [(42, 42, 1)]
NULL row, filtered: 3 islands
NULL row, no filter:
 start_id  end_id  cnt
      NaN     NaN    1
      1.0     3.0    3
      7.0     8.0    2
     10.0    10.0    1
pandas column dtype with a NULL: float64
duplicate id 2, no DISTINCT:
 start_id  end_id  cnt
        1       2    2
        2       3    2
        7       8    2
       10      10    1
with SELECT DISTINCT: equals the clean result
empty table, SQL rows: 0
empty table, pandas rows: 0 | columns: ['start_id', 'end_id', 'cnt']
asserts passed
```

**Edge cases:**
- Single row: one island, start = end, count 1 (id 42 in my run). A single-row island needs no special code; it is just a group of one.
- Empty table: SQL returns zero rows; pandas returned an empty frame with the three columns (tested, no error).
- NULL id: I drop it, because a missing id is not a log. Without the filter SQLite sorts the NULL first, gives it row number 1, and `NULL - 1` is NULL, so it became its own island with NULL start and end (output shows `NaN` because pandas converted the NULL). The other keys all shift by one together, so they are unchanged. In pandas a NULL turns the integer column into `float64`, which is why `dropna().astype("int64")` is in the code; `groupby` would also drop NaN keys silently, but I drop them explicitly.
- Duplicate id: not allowed by the question, but I tested it. A second id 2 made the row number run ahead of the id and the islands came out as (1,2), (2,3), which is wrong. `SELECT DISTINCT log_id` first restores the clean answer. Same bug class as Q8.
- Unsorted insertion order: irrelevant, the window `ORDER BY` sorts; pandas needs the explicit `sort_values`.
- Exact-threshold gaps: ids exactly 1 apart stay together, exactly 2 apart (8 and 10, one id missing) split.
- `diff()` in pandas returns `float64` because the first element has no previous value (NaN), and `NaN != 1` is `True`, so the first row correctly starts the first island. I ran this: the first diff printed `nan` and the comparison was `True`.

**Then explain:**
- Same idea as Q1 but with ids: the id plays the role of the day number, so no `julianday` is needed.
- Integer ids make the key exact; there is no float concern.
- The output is "ranges", which is the compact way to report which ids are present; the gaps between them are the missing ranges (Q3).
- Dialects (not executed here): the query uses only standard window syntax, so I expect it to run on PostgreSQL, MySQL 8, BigQuery and Snowflake; MySQL 5.7 has no window functions, so there you would use a variable-based or self-join solution. I did not run any of them.

**Follow-ups:**
- *Gaps instead of islands?* The gap between island i and island i+1 is `end_id + 1` to `next_start - 1` (Q3).
- *Ids as text?* Cast to integer first, otherwise `'10'` sorts before `'2'`.
- *Large table?* One sort and one scan; an index on `log_id` lets the sort be skipped (I did not time it).

**Common mistakes:**
- Forgetting `ORDER BY` inside the window, or ordering by something other than the id.
- Not removing NULLs or duplicates before numbering.
- Grouping by the id instead of the key.
- Assuming the table is already sorted in pandas (`s - range(...)` on unsorted data gives nonsense keys).

### Q3 ⭐⭐⭐ 🟢 Missing ids and gaps between consecutive values: invoices(invoice_no) with numbers 1,2,3,7,8,10,15. Return each gap as gap_start and gap_end (the missing numbers) using LEAD or LAG with the test next - current > 1, and explain why the first row's LAG is NULL and how that is handled. Show a second way with a NOT EXISTS anti join against a number spine, and say which one scales and which reports ranges instead of single missing values.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** Sort the numbers, look at the next one with `LEAD`, and wherever `next - current > 1` the missing numbers are `current + 1` through `next - 1`; the last row has no next, its `NULL` fails the test, and that is the right outcome.

**Schema and sample data:** seven invoice numbers inserted out of order. Missing: 4,5,6 | 9 | 11,12,13,14.
```sql
CREATE TABLE invoices(invoice_no INTEGER);
INSERT INTO invoices VALUES (15),(2),(1),(7),(10),(3),(8);
```

**SQL answer:** `SQL_MAIN` in the Code block (LEAD form). `SQL_LAG` is the mirror image and gave the same rows.
```sql
WITH x AS (
  SELECT invoice_no,
         LEAD(invoice_no) OVER (ORDER BY invoice_no) AS next_no
  FROM invoices
  WHERE invoice_no IS NOT NULL
)
SELECT invoice_no + 1 AS gap_start,
       next_no - 1   AS gap_end
FROM x
WHERE next_no - invoice_no > 1
ORDER BY gap_start
```
Second way, in the Code block as `SQL_SPINE`: build a number spine from `MIN` to `MAX` with a recursive CTE (depth is Part 9; here it is only a counter), then keep the spine numbers with no matching invoice:
```sql
WITH RECURSIVE spine(n) AS (
  SELECT MIN(invoice_no) FROM invoices
  UNION ALL
  SELECT n + 1 FROM spine WHERE n < (SELECT MAX(invoice_no) FROM invoices)
)
SELECT n AS missing_no
FROM spine s
WHERE NOT EXISTS (SELECT 1 FROM invoices i WHERE i.invoice_no = s.n)
ORDER BY n
```
This lists single missing numbers (4,5,6,9,11,12,13,14), not ranges. `SQL_SPINE_RANGES` re-groups them into ranges with the Q2 trick (`n - ROW_NUMBER()`), and matched the LEAD output exactly.

**pandas answer:** same logic as the LEAD form, shown once here and identical to the Code block. `shift(-1)` is the "next value".
```py
    s = inv["invoice_no"].dropna().astype("int64").sort_values().reset_index(drop=True)
    nxt = s.shift(-1)
    mask = (nxt - s) > 1
    pd_df = pd.DataFrame({"gap_start": s[mask] + 1, "gap_end": (nxt[mask] - 1).astype("int64")}).reset_index(drop=True)
    
```

**Example (by hand):** sorted: 1,2,3,7,8,10,15 with their next values 2,3,7,8,10,15,NULL.
- 1 to 2 and 2 to 3: difference 1, no gap. 3 to 7: difference 4 (greater than 1), gap_start 4, gap_end 6.
- 7 to 8: difference 1, no gap. 8 to 10: difference exactly 2, so one number is missing: gap 9 to 9.
- 10 to 15: difference 5, gap 11 to 14. 15 has next NULL, `NULL - 15 > 1` is unknown, row dropped.
- Result: (4,6), (9,9), (11,14).

**Code:** run with `python3 -I`. The assert compares SQL and pandas after sorting by `gap_start` (SQL has `ORDER BY gap_start`; the pandas input is sorted by `invoice_no`, which gives the same order).
```python
# Q3: missing ids and gaps: LEAD/LAG test next - current > 1, and NOT EXISTS against a number spine
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE invoices(invoice_no INTEGER);
INSERT INTO invoices VALUES (15),(2),(1),(7),(10),(3),(8);
"""
SQL_MAIN = """
WITH x AS (
  SELECT invoice_no,
         LEAD(invoice_no) OVER (ORDER BY invoice_no) AS next_no
  FROM invoices
  WHERE invoice_no IS NOT NULL
)
SELECT invoice_no + 1 AS gap_start,
       next_no - 1   AS gap_end
FROM x
WHERE next_no - invoice_no > 1
ORDER BY gap_start
"""
SQL_LAG = """
WITH x AS (
  SELECT invoice_no,
         LAG(invoice_no) OVER (ORDER BY invoice_no) AS prev_no
  FROM invoices
  WHERE invoice_no IS NOT NULL
)
SELECT prev_no + 1 AS gap_start,
       invoice_no - 1 AS gap_end
FROM x
WHERE invoice_no - prev_no > 1
ORDER BY gap_start
"""
SQL_LAG_FROM_ONE = """
WITH x AS (
  SELECT invoice_no,
         COALESCE(LAG(invoice_no) OVER (ORDER BY invoice_no), 0) AS prev_no
  FROM invoices
  WHERE invoice_no IS NOT NULL
)
SELECT prev_no + 1 AS gap_start,
       invoice_no - 1 AS gap_end
FROM x
WHERE invoice_no - prev_no > 1
ORDER BY gap_start
"""
SQL_SPINE = """
WITH RECURSIVE spine(n) AS (
  SELECT MIN(invoice_no) FROM invoices
  UNION ALL
  SELECT n + 1 FROM spine WHERE n < (SELECT MAX(invoice_no) FROM invoices)
)
SELECT n AS missing_no
FROM spine s
WHERE NOT EXISTS (SELECT 1 FROM invoices i WHERE i.invoice_no = s.n)
ORDER BY n
"""
SQL_SPINE_RANGES = """
WITH RECURSIVE spine(n) AS (
  SELECT MIN(invoice_no) FROM invoices
  UNION ALL
  SELECT n + 1 FROM spine WHERE n < (SELECT MAX(invoice_no) FROM invoices)
),
missing AS (
  SELECT n FROM spine s
  WHERE NOT EXISTS (SELECT 1 FROM invoices i WHERE i.invoice_no = s.n)
),
y AS (
  SELECT n, n - ROW_NUMBER() OVER (ORDER BY n) AS grp FROM missing
)
SELECT MIN(n) AS gap_start, MAX(n) AS gap_end
FROM y
GROUP BY grp
ORDER BY gap_start
"""

def pd_gaps(inv):
    # pd:main
    s = inv["invoice_no"].dropna().astype("int64").sort_values().reset_index(drop=True)
    nxt = s.shift(-1)
    mask = (nxt - s) > 1
    pd_df = pd.DataFrame({"gap_start": s[mask] + 1, "gap_end": (nxt[mask] - 1).astype("int64")}).reset_index(drop=True)
    # pd:end
    return pd_df

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("LEAD version (gap ranges):")
print(sql_df.to_string(index=False))
lag_df = pd.read_sql_query(SQL_LAG, con)
pd.testing.assert_frame_equal(lag_df, sql_df)
print("LAG version equals LEAD version: True")
print("\nnumber spine + NOT EXISTS (single missing numbers):", [r[0] for r in con.execute(SQL_SPINE)])
spine_ranges = pd.read_sql_query(SQL_SPINE_RANGES, con)
pd.testing.assert_frame_equal(spine_ranges, sql_df)
print("spine singles re-grouped into ranges equals LEAD version: True")

inv = pd.read_sql_query("SELECT * FROM invoices", con)
pd_df = pd_gaps(inv)
# compared after sorting by gap_start (SQL ORDER BY gap_start; pandas input sorted by invoice_no)
pd.testing.assert_frame_equal(pd_df, sql_df)
print("pandas equals SQL: True")
s = inv["invoice_no"].sort_values().reset_index(drop=True)
print("shift(-1) dtype:", s.shift(-1).dtype, "| last value:", s.shift(-1).iloc[-1])
spine = pd.Series(range(int(s.min()), int(s.max()) + 1))
print("pandas spine, missing singles:", spine[~spine.isin(s)].tolist())

# edge cases
con.executescript("""
CREATE TABLE inv_b(invoice_no INTEGER);
INSERT INTO inv_b VALUES (3),(4),(6);
""")
print("\nnumbering should start at 1, table 3,4,6:")
print("  plain LAG (first row dropped):", con.execute(SQL_LAG.replace("FROM invoices", "FROM inv_b")).fetchall())
print("  COALESCE(LAG, 0):", con.execute(SQL_LAG_FROM_ONE.replace("FROM invoices", "FROM inv_b")).fetchall())
con.execute("INSERT INTO invoices VALUES (7)")
print("duplicate 7 added, LEAD version unchanged:", pd.read_sql_query(SQL_MAIN, con).equals(sql_df))
con.execute("INSERT INTO invoices VALUES (NULL)")
print("NULL added (filtered out), LEAD version unchanged:", pd.read_sql_query(SQL_MAIN, con).equals(sql_df))
nul = con.execute(SQL_MAIN.replace("  WHERE invoice_no IS NOT NULL\n", "")).fetchall()
print("NULL added, filter removed:", nul)
con.execute("DELETE FROM invoices")
print("empty table, LEAD rows:", con.execute(SQL_MAIN).fetchall())
print("empty table, spine rows:", con.execute(SQL_SPINE).fetchall())
con.execute("INSERT INTO invoices VALUES (5)")
print("single row, LEAD rows:", con.execute(SQL_MAIN).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
LEAD version (gap ranges):
 gap_start  gap_end
         4        6
         9        9
        11       14
LAG version equals LEAD version: True

number spine + NOT EXISTS (single missing numbers): [4, 5, 6, 9, 11, 12, 13, 14]
spine singles re-grouped into ranges equals LEAD version: True
pandas equals SQL: True
shift(-1) dtype: float64 | last value: nan
pandas spine, missing singles: [4, 5, 6, 9, 11, 12, 13, 14]

numbering should start at 1, table 3,4,6:
  plain LAG (first row dropped): [(5, 5)]
  COALESCE(LAG, 0): [(1, 2), (5, 5)]
duplicate 7 added, LEAD version unchanged: True
NULL added (filtered out), LEAD version unchanged: True
NULL added, filter removed: [(4, 6), (9, 9), (11, 14)]
empty table, LEAD rows: []
empty table, spine rows: [(None,)]
single row, LEAD rows: []
asserts passed
```

**Edge cases:**
- First row with LAG: nothing precedes the smallest number, so `LAG` is `NULL`, `invoice_no - NULL` is `NULL`, the `WHERE` drops it. That is usually right (no gap before the first invoice). If the series is supposed to start at 1, use `COALESCE(LAG(...), 0)`: on a second table with 3,4,6 plain LAG found only (5,5) and the COALESCE version found (1,2) and (5,5). I used the LEAD form as the main answer because the last row has no gap after it either way.
- Exact threshold: difference 1 means no gap (7 to 8), exactly 2 means one missing number (8 to 10, gap_start = gap_end = 9). With `> 1` there is no off-by-one; `>= 1` would flag every row.
- Duplicates: I added a second 7. The LEAD output did not change (7 to 7 is difference 0, then 7 to 8 is 1), so this method tolerates duplicates, unlike the `ROW_NUMBER` island key of Q2.
- NULL invoice number: filtered in `SQL_MAIN`. I also removed the filter: the output was unchanged, because the NULL sorts first, its LEAD is a real number but `next - NULL` is unknown. Filtering is still clearer.
- Empty table: LEAD returns zero rows. The spine version returned one row with `NULL` (`MIN` of nothing is NULL, so the spine starts at NULL, and nothing matches NULL), which is a bug to guard against (for example `WHERE n IS NOT NULL`, or wrap the whole thing in a check that the table is non-empty). Single row: zero gaps in both.
- Unsorted input: handled by the window `ORDER BY`; pandas needs the explicit `sort_values`.
- pandas: `shift(-1)` turned the integer column into `float64` (the last value is NaN), so I cast the end value back to `int64` after masking, otherwise `gap_end` prints as 6.0 and does not equal the SQL integers.

**Then explain:**
- Which scales: LEAD/LAG is one sorted pass and its cost depends on the number of rows, not on how large the numbers are. The spine is as long as `MAX - MIN`; for ids that jump from 1 to 1,000,000,000 the spine has a billion rows. Use the spine when the range is small and dense, or when you need an explicit row per missing value.
- Which reports ranges: LEAD/LAG reports ranges directly (gap_start to gap_end). The spine anti join reports single missing values; get ranges from it with a second grouping step, as `SQL_SPINE_RANGES` does.
- `NOT EXISTS` and `LEFT JOIN ... IS NULL` give the same rows here; `NOT IN` is dangerous if the subquery can return `NULL` (Part 2 and Part 10 cover why).
- The recursive CTE is the portable spine in SQLite; other engines have `generate_series` (PostgreSQL), `GENERATE_ARRAY` with `UNNEST` (BigQuery) and so on (not executed here, details in Part 9). A numbers table works anywhere.
- Gaps and islands are the same information: islands are the present ranges (Q2), gaps are the absent ranges between them.

**Follow-ups:**
- *Which number is missing from 1..N when exactly one is missing?* `N*(N+1)/2 - SUM(x)` or the spine version.
- *How many missing in total?* `MAX - MIN + 1 - COUNT(DISTINCT x)`.
- *Gaps per department or per series?* `PARTITION BY` the series in the `LEAD`.

**Common mistakes:**
- Using `>= 1` instead of `> 1`, or reporting `current` and `next` instead of `current + 1` and `next - 1`.
- Not filtering or handling the NULL last row and then wondering why it vanishes.
- Building the spine from 1 instead of `MIN`, or building an enormous spine for sparse ids.
- Ordering the window by something other than the number (for example the insertion id).
- In pandas, comparing after `shift` without noticing the float upcast.

### Q4 ⭐⭐⭐ 🟢 Consecutive Numbers (LeetCode 180): logs(id, num) where id is an auto-increment. Return every num that appears at least three times in a row. Show a self join on ids l1.id + 1 = l2.id, a LEAD(num, 1) and LEAD(num, 2) version with DISTINCT, and the ROW_NUMBER difference version that generalises to N in a row. State the assumption that consecutive means consecutive ids, and show what changes when ids have gaps (use ROW_NUMBER over id instead of id arithmetic).
**Asked at:** public LeetCode-style problem bank (statements known from search snippets and mirrors such as doocs, walkccc and talentd; the leetcode.com pages returned HTTP 403 and were not opened), not candidate reports; analyst, data scientist and data engineer screens at product companies and GCCs
**Say this first (1 line):** I assume "in a row" means consecutive ids; the simple answer is a three-way self join on `id + 1` and `id + 2` with `DISTINCT`, and the version that generalises to N is `ROW_NUMBER() OVER (ORDER BY id) - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id)` grouped with `HAVING COUNT(*) >= N`.

**Schema and sample data:** fourteen rows, ids 1 to 14 with no gaps. Value 1 appears three times in a row (ids 1-3) and once more later; value 2 has a run of four (ids 6-9); value 3 has a run of two; ids 12-14 hold NULL three times.
```sql
CREATE TABLE logs(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs VALUES
 (1,1),(2,1),(3,1),(4,2),(5,1),(6,2),(7,2),(8,2),(9,2),(10,3),(11,3),(12,NULL),(13,NULL),(14,NULL);
```

**SQL answer:** three versions, all in the Code block. Self join (`SQL_JOIN`):
```sql
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l2.id = l1.id + 1 AND l2.num = l1.num
JOIN logs l3 ON l3.id = l1.id + 2 AND l3.num = l1.num
ORDER BY consecutive_num
```
`LEAD` version (`SQL_LEAD`):
```sql
WITH x AS (
  SELECT num,
         LEAD(num, 1) OVER (ORDER BY id) AS n1,
         LEAD(num, 2) OVER (ORDER BY id) AS n2
  FROM logs
)
SELECT DISTINCT num AS consecutive_num
FROM x
WHERE num = n1 AND num = n2
ORDER BY consecutive_num
```
ROW_NUMBER difference, N as a bound parameter (`SQL_ISLAND`; the `?` is N):
```sql
WITH x AS (
  SELECT id, num,
         ROW_NUMBER() OVER (ORDER BY id)
           - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS grp
  FROM logs
  WHERE num IS NOT NULL
)
SELECT DISTINCT num AS consecutive_num
FROM x
GROUP BY num, grp
HAVING COUNT(*) >= ?
ORDER BY consecutive_num
```
Two row numbers: one over the whole table, one inside each `num`. Within a run of equal values both advance by 1, so their difference is constant; when another value interrupts, only the whole-table counter moves, and the difference changes.

**pandas answer:** run key from the shift comparison, one group per run, keep runs of length at least N. Shown once, identical to the Code block (the `respect_ids` branch adds a break wherever the id step is not exactly 1):
```py
    d = logs.sort_values("id")
    run = (d["num"] != d["num"].shift()).cumsum()
    if respect_ids:
        run = run + (d["id"].diff() != 1).cumsum()
    g = d.groupby(run).agg(num=("num", "first"), n=("id", "size"))
    out = sorted(int(v) for v in g.loc[(g["n"] >= n) & g["num"].notna(), "num"].unique())
    
```

**Example (by hand):** ordered by id, nums are 1,1,1,2,1,2,2,2,2,3,3,NULL,NULL,NULL.
- Runs of equal value: 1x3 (ids 1-3), 2x1 (id 4), 1x1 (id 5), 2x4 (ids 6-9), 3x2, then NULL.
- Runs of length 3 or more: value 1 (the first run) and value 2 (the run of four).
- Self join: start ids 1 (for 1), 6 and 7 (for 2: ids 6-8 and 7-9). Two start rows for the same value, so without `DISTINCT` the value 2 would be returned twice.
- Result: 1 and 2. Value 3 has only two in a row; the NULLs never count.

**Code:** run with `python3 -I`. The asserts compare lists of `num` values sorted ascending (SQL `ORDER BY consecutive_num`, pandas `sorted`).
```python
# Q4: Consecutive Numbers (LeetCode 180 pattern): self join, LEAD, ROW_NUMBER difference, pandas run key
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logs(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs VALUES
 (1,1),(2,1),(3,1),(4,2),(5,1),(6,2),(7,2),(8,2),(9,2),(10,3),(11,3),(12,NULL),(13,NULL),(14,NULL);
"""
SQL_JOIN = """
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l2.id = l1.id + 1 AND l2.num = l1.num
JOIN logs l3 ON l3.id = l1.id + 2 AND l3.num = l1.num
ORDER BY consecutive_num
"""
SQL_JOIN_NO_DISTINCT = SQL_JOIN.replace("SELECT DISTINCT", "SELECT")
SQL_LEAD = """
WITH x AS (
  SELECT num,
         LEAD(num, 1) OVER (ORDER BY id) AS n1,
         LEAD(num, 2) OVER (ORDER BY id) AS n2
  FROM logs
)
SELECT DISTINCT num AS consecutive_num
FROM x
WHERE num = n1 AND num = n2
ORDER BY consecutive_num
"""
SQL_ISLAND = """
WITH x AS (
  SELECT id, num,
         ROW_NUMBER() OVER (ORDER BY id)
           - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS grp
  FROM logs
  WHERE num IS NOT NULL
)
SELECT DISTINCT num AS consecutive_num
FROM x
GROUP BY num, grp
HAVING COUNT(*) >= ?
ORDER BY consecutive_num
"""
SQL_ISLAND_NO_FILTER = SQL_ISLAND.replace("  WHERE num IS NOT NULL\n", "")
SQL_ISLAND_IDS = """
WITH x AS (
  SELECT id, num,
         id - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS grp
  FROM logs
  WHERE num IS NOT NULL
)
SELECT DISTINCT num AS consecutive_num
FROM x
GROUP BY num, grp
HAVING COUNT(*) >= ?
ORDER BY consecutive_num
"""

def col(con, sql, *params):
    return [r[0] for r in con.execute(sql, params)]

def pd_consec(logs, n=3, respect_ids=False):
    # pd:main
    d = logs.sort_values("id")
    run = (d["num"] != d["num"].shift()).cumsum()
    if respect_ids:
        run = run + (d["id"].diff() != 1).cumsum()
    g = d.groupby(run).agg(num=("num", "first"), n=("id", "size"))
    out = sorted(int(v) for v in g.loc[(g["n"] >= n) & g["num"].notna(), "num"].unique())
    # pd:end
    return out

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
j = col(con, SQL_JOIN)
print("self join:", j)
print("self join without DISTINCT:", col(con, SQL_JOIN_NO_DISTINCT), "(num 2 has a run of 4, so two start rows)")
l = col(con, SQL_LEAD)
i3 = col(con, SQL_ISLAND, 3)
print("LEAD + DISTINCT:", l)
print("ROW_NUMBER difference, N=3:", i3)
assert j == l == i3
logs = pd.read_sql_query("SELECT * FROM logs", con)
print("pandas, N=3:", pd_consec(logs, 3))
# compared as sorted lists of num values
assert pd_consec(logs, 3) == i3
for n in (2, 3, 4, 5):
    s = col(con, SQL_ISLAND, n)
    p = pd_consec(logs, n)
    assert s == p
    print("N =", n, "-> SQL", s, "| pandas", p)
print("NULL rows (ids 12-14) with no IS NOT NULL filter, N=3:", col(con, SQL_ISLAND_NO_FILTER, 3))

# gaps in ids: id 3 was deleted, so 7,7,7 sits at ids 1,2,4
con.executescript("""
CREATE TABLE logs_gap(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs_gap VALUES (5,8),(1,7),(4,7),(2,7),(6,8);
""")
def on_gap(sql):
    return sql.replace("FROM logs", "FROM logs_gap")
print("\nids 1,2,4 hold 7,7,7 (id 3 missing):")
print("  self join (id arithmetic):", col(con, on_gap(SQL_JOIN)))
print("  LEAD (positional):", col(con, on_gap(SQL_LEAD)))
print("  id - ROW_NUMBER per num (id arithmetic):", col(con, on_gap(SQL_ISLAND_IDS), 3))
print("  ROW_NUMBER difference (positional):", col(con, on_gap(SQL_ISLAND), 3))
lg = pd.read_sql_query("SELECT * FROM logs_gap", con)
print("  pandas positional:", pd_consec(lg, 3), "| pandas respecting ids:", pd_consec(lg, 3, respect_ids=True))
assert pd_consec(lg, 3) == col(con, on_gap(SQL_ISLAND), 3)
assert pd_consec(lg, 3, respect_ids=True) == col(con, on_gap(SQL_ISLAND_IDS), 3) == col(con, on_gap(SQL_JOIN))
print("  asserts: positional == positional, id-aware == id-aware")

# single row and empty table
con.execute("DELETE FROM logs_gap")
print("\nempty table:", col(con, on_gap(SQL_ISLAND), 3), "| pandas:", pd_consec(pd.read_sql_query("SELECT * FROM logs_gap", con), 3))
con.execute("INSERT INTO logs_gap VALUES (1, 9)")
print("single row, N=1:", col(con, on_gap(SQL_ISLAND), 1), "| N=3:", col(con, on_gap(SQL_ISLAND), 3))
print("asserts passed")
```

**Output (my run):**
```text
self join: [1, 2]
self join without DISTINCT: [1, 2, 2] (num 2 has a run of 4, so two start rows)
LEAD + DISTINCT: [1, 2]
ROW_NUMBER difference, N=3: [1, 2]
pandas, N=3: [1, 2]
N = 2 -> SQL [1, 2, 3] | pandas [1, 2, 3]
N = 3 -> SQL [1, 2] | pandas [1, 2]
N = 4 -> SQL [2] | pandas [2]
N = 5 -> SQL [] | pandas []
NULL rows (ids 12-14) with no IS NOT NULL filter, N=3: [None, 1, 2]

ids 1,2,4 hold 7,7,7 (id 3 missing):
  self join (id arithmetic): []
  LEAD (positional): [7]
  id - ROW_NUMBER per num (id arithmetic): []
  ROW_NUMBER difference (positional): [7]
  pandas positional: [7] | pandas respecting ids: []
  asserts: positional == positional, id-aware == id-aware

empty table: [] | pandas: []
single row, N=1: [9] | N=3: []
asserts passed
```

**Edge cases:**
- Run of four: the self join without `DISTINCT` returned `[1, 2, 2]` (num 2 starts a qualifying triple at two ids). `LEAD` has the same effect and needs `DISTINCT`. The ROW_NUMBER version groups by island so it returns one row per island, with `DISTINCT` guarding against two separate qualifying islands of the same value (value 1 could have two).
- NULL `num`: `NULL = NULL` is unknown, so the self join and the `LEAD` version never match NULLs. The ROW_NUMBER version is different: `PARTITION BY` treats NULLs as one group, so without `WHERE num IS NOT NULL` it returned NULL as an answer (the unfiltered run shows `[None, 1, 2]`). pandas gives each NaN its own run, because `NaN != NaN` is true, so only the explicit `notna()` filter matters there and results agree.
- "In a row" means what? Consecutive ids (as the problem says) versus consecutive rows in id order are the same only when ids have no gaps. With id 3 deleted and 7,7,7 at ids 1,2,4: the self join and `id - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id)` (`SQL_ISLAND_IDS`) returned nothing, the `LEAD` version and the two-row-number version returned 7. All four are right for a different reading; state yours. For auto-increment ids with deleted rows, positional (row order) is usually what people mean.
- pandas run key is positional by default; adding the `id.diff() != 1` break gives the id-aware answer, and I asserted both against the matching SQL.
- Unsorted input: the window and the sort in pandas fix the order; the self join does not depend on order at all.
- Single row and empty table: no output for N=3, and `[9]` for a single row with N=1.
- Generalising N: N=2 gave 1,2,3, N=4 gave only 2, N=5 gave none, same in SQL and pandas. The self join does not generalise, because it needs N-1 joins.

**Then explain:**
- Self join: simple, readable, but a join per extra row and it depends on `id + 1` arithmetic.
- `LEAD`: one pass, but it is hard-wired to 3 (two `LEAD` calls); N would need N-1 calls.
- Islands: one formula for any N, and the `HAVING COUNT(*) >= N` is the only thing that changes.
- As I remember the LeetCode statement (not opened here) it is written for MySQL; MySQL 5.7 has no window functions, so only the self join works there. MySQL 8, PostgreSQL, BigQuery and Snowflake support the window forms (not executed).

**Follow-ups:**
- *Return the start id of each run, or the run length?* Keep `MIN(id)` and `COUNT(*)` from the island group instead of `DISTINCT num`.
- *At least N where ids may have gaps?* Use the positional form, or add the id-gap break in pandas.
- *Same value in 3 consecutive days per user?* Partition by user and use the date key (Q6 and Q9).

**Common mistakes:**
- Forgetting `DISTINCT` and returning a value once per qualifying triple.
- Mixing up the two readings of "in a row" when ids have gaps, and not saying which one is used.
- Letting NULLs through the `PARTITION BY` version.
- Hard-coding three `LEAD` calls and then being asked for N.
- Grouping by `grp` alone instead of `num, grp`.

### Q5 ⭐⭐⭐ 🟢 pandas run grouping, the core idiom: a Series of statuses ordered by time, for example 'up','up','down','down','down','up'. Build the run key with (s != s.shift()).cumsum(), then groupby that key and agg first value, first and last position and size to get run-length encoding. Explain why groupby on the value itself merges separate runs, why shift() makes the first comparison True, and how to do the same per entity with groupby('entity')['status'].shift(). Assert the result equals the SQL LAG-flag version on the same six rows.
**Asked at:** pandas Series.shift reference (opened) and search snippets of Stack Overflow and Towards Data Science run-grouping answers ((s != s.shift()).cumsum(), diff().ne(0).cumsum(); not opened); documentation and guides, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `(s != s.shift()).cumsum()` gives every run its own number, because the comparison is True exactly where the value changes (and on the first row), and `cumsum()` counts those changes; then `groupby` that key and aggregate to get the run-length table.

**Schema and sample data:** the six statuses from the question, plus a two-entity table to show the per-entity version. Entity B starts with `'up'` on purpose, the same value entity A ends with.
```sql
CREATE TABLE seq(pos INTEGER, status TEXT);
INSERT INTO seq VALUES (1,'up'),(2,'up'),(3,'down'),(4,'down'),(5,'down'),(6,'up');
CREATE TABLE ev(entity TEXT, ts INTEGER, status TEXT);
INSERT INTO ev VALUES
 ('A',1,'up'),('A',2,'up'),('A',3,'down'),('A',4,'down'),('A',5,'down'),('A',6,'up'),
 ('B',1,'up'),('B',2,'up'),('B',3,'down');
```

**SQL answer:** the LAG-flag version, `SQL_MAIN` in the Code block. The flag is 1 on the first row and wherever the status differs from the previous row; the running `SUM` of flags is the run id. I used `IS NOT` so the first row (previous value NULL) flags itself and NULL statuses compare safely:
```sql
WITH x AS (
  SELECT pos, status,
         CASE WHEN status IS NOT LAG(status) OVER (ORDER BY pos) THEN 1 ELSE 0 END AS new_run
  FROM seq
),
y AS (
  SELECT pos, status, SUM(new_run) OVER (ORDER BY pos) AS run_id
  FROM x
)
SELECT run_id,
       MIN(status) AS status,
       MIN(pos)    AS first_pos,
       MAX(pos)    AS last_pos,
       COUNT(*)    AS run_len
FROM y
GROUP BY run_id
ORDER BY run_id
```
The per-entity version (`SQL_ENTITY`) only adds `PARTITION BY entity` to both windows and `entity` to the final `GROUP BY`.

**pandas answer:** shown once, identical to the Code block. `shift()` moves the values down one row, so row i is compared with row i-1:
```py
s = seq.sort_values("pos")
run = (s["status"] != s["status"].shift()).cumsum()
pd_df = (s.groupby(run)
          .agg(status=("status", "first"), first_pos=("pos", "min"), last_pos=("pos", "max"), run_len=("pos", "size"))
          .rename_axis("run_id").reset_index())
```
Per entity, the shift must happen inside each entity and the running count must restart per entity (these two lines are in the Code block):
```py
new_run = e["status"] != e.groupby("entity")["status"].shift()
e_run = new_run.groupby(e["entity"]).cumsum()
```

**Example (by hand):** statuses at positions 1 to 6 are up, up, down, down, down, up.
- `shift()` gives NaN, up, up, down, down, down.
- `!=` gives True (up vs NaN), False, True, False, False, True.
- `cumsum()` gives 1, 1, 2, 2, 2, 3. That is the run key.
- Group by it: run 1 = up, positions 1-2, length 2; run 2 = down, 3-5, length 3; run 3 = up, position 6, length 1.
- The SQL does the same: flags 1,0,1,0,0,1 and running sum 1,1,2,2,2,3.

**Code:** run with `python3 -I`. The assert compares SQL and pandas frames in `run_id` order (and, for entities, sorted by `entity, run_id`), all columns including `run_len`.
```python
# Q5: pandas run grouping, (s != s.shift()).cumsum(), vs the SQL LAG-flag version
import itertools
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE seq(pos INTEGER, status TEXT);
INSERT INTO seq VALUES (1,'up'),(2,'up'),(3,'down'),(4,'down'),(5,'down'),(6,'up');
CREATE TABLE ev(entity TEXT, ts INTEGER, status TEXT);
INSERT INTO ev VALUES
 ('A',1,'up'),('A',2,'up'),('A',3,'down'),('A',4,'down'),('A',5,'down'),('A',6,'up'),
 ('B',1,'up'),('B',2,'up'),('B',3,'down');
"""
SQL_MAIN = """
WITH x AS (
  SELECT pos, status,
         CASE WHEN status IS NOT LAG(status) OVER (ORDER BY pos) THEN 1 ELSE 0 END AS new_run
  FROM seq
),
y AS (
  SELECT pos, status, SUM(new_run) OVER (ORDER BY pos) AS run_id
  FROM x
)
SELECT run_id,
       MIN(status) AS status,
       MIN(pos)    AS first_pos,
       MAX(pos)    AS last_pos,
       COUNT(*)    AS run_len
FROM y
GROUP BY run_id
ORDER BY run_id
"""
SQL_ENTITY = """
WITH x AS (
  SELECT entity, ts, status,
         CASE WHEN status IS NOT LAG(status) OVER (PARTITION BY entity ORDER BY ts) THEN 1 ELSE 0 END AS new_run
  FROM ev
),
y AS (
  SELECT entity, ts, status,
         SUM(new_run) OVER (PARTITION BY entity ORDER BY ts) AS run_id
  FROM x
)
SELECT entity, run_id, MIN(status) AS status, MIN(ts) AS first_ts, MAX(ts) AS last_ts, COUNT(*) AS run_len
FROM y
GROUP BY entity, run_id
ORDER BY entity, run_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL LAG flag + running SUM:")
print(sql_df.to_string(index=False))

seq = pd.read_sql_query("SELECT * FROM seq", con)
# pd:main
s = seq.sort_values("pos")
run = (s["status"] != s["status"].shift()).cumsum()
pd_df = (s.groupby(run)
          .agg(status=("status", "first"), first_pos=("pos", "min"), last_pos=("pos", "max"), run_len=("pos", "size"))
          .rename_axis("run_id").reset_index())
# pd:end
print("\npandas run key:", run.tolist())
# compared in run_id order; run_id starts at 1 in pandas (cumsum of a True first flag) and at 1 in SQL
pd.testing.assert_frame_equal(pd_df, sql_df)
print("pandas equals SQL: True")
print("\ngroupby on the value itself:", seq.groupby("status").size().to_dict(), "(two separate up runs merged into one group of 3)")
print("itertools.groupby run lengths:", [(k, len(list(g))) for k, g in itertools.groupby(seq.sort_values("pos")["status"])])

# the first comparison is True because shift() puts NaN in front
print("first flag:", (s["status"] != s["status"].shift()).iloc[0], "| shift()[0]:", s["status"].shift().iloc[0])

# per entity
ev = pd.read_sql_query("SELECT * FROM ev", con)
sql_e = pd.read_sql_query(SQL_ENTITY, con)
e = ev.sort_values(["entity", "ts"])
wrong_run = (e["status"] != e["status"].shift()).cumsum()
print("\nwrong, global shift: runs by run key only ->", e.groupby(wrong_run).agg(n_rows=("ts", "size"), n_entities=("entity", "nunique")).to_dict("records"))
new_run = e["status"] != e.groupby("entity")["status"].shift()
e_run = new_run.groupby(e["entity"]).cumsum()
pd_e = (e.groupby(["entity", e_run])
         .agg(status=("status", "first"), first_ts=("ts", "min"), last_ts=("ts", "max"), run_len=("ts", "size"))
         .rename_axis(["entity", "run_id"]).reset_index())
pd.testing.assert_frame_equal(pd_e, sql_e)
print("per-entity pandas equals SQL (sorted by entity, run_id): True")
print(sql_e.to_string(index=False))

# NULL status: SQL IS NOT merges consecutive NULLs, pandas != does not
con.executescript("CREATE TABLE seqn(pos INTEGER, status TEXT); INSERT INTO seqn VALUES (1,'up'),(2,NULL),(3,NULL),(4,'up');")
sn = pd.read_sql_query("SELECT * FROM seqn", con)
sql_n = pd.read_sql_query(SQL_MAIN.replace("FROM seq", "FROM seqn"), con)
naive = (sn["status"] != sn["status"].shift()).cumsum()
both_na = sn["status"].isna() & sn["status"].shift().isna()
fixed = ((sn["status"] != sn["status"].shift()) & ~both_na).cumsum()
print("\nNULL,NULL in the middle: SQL run lengths", sql_n["run_len"].tolist(),
      "| pandas naive", sn.groupby(naive).size().tolist(),
      "| pandas fixed", sn.groupby(fixed).size().tolist())
assert sn.groupby(fixed).size().tolist() == sql_n["run_len"].tolist()
print("NaN != NaN:", bool(np.nan != np.nan), "| pandas Series:", (pd.Series([np.nan]) != pd.Series([np.nan])).tolist())

# integer states: shift upcasts to float64
st = pd.Series([1, 1, 0, 0, 1])
print("int Series shift dtype:", st.shift().dtype, "| shift(fill_value=-1) dtype:", st.shift(fill_value=-1).dtype,
      "| runs:", (st != st.shift()).cumsum().tolist())

# groupby drops NaN keys unless dropna=False
ev_nan = pd.concat([ev, pd.DataFrame({"entity": [None], "ts": [1], "status": ["up"]})], ignore_index=True)
print("groupby rows with a NULL entity: default", ev_nan.groupby("entity")["ts"].size().sum(),
      "| dropna=False", ev_nan.groupby("entity", dropna=False)["ts"].size().sum(), "| total rows", len(ev_nan))

# unsorted input, ties on the sort key, stability
rng = np.random.default_rng(0)
big = pd.DataFrame({"k": rng.integers(0, 5, 20000), "orig": np.arange(20000)})
default_order = big.sort_values("k")["orig"].to_numpy()
stable_order = big.sort_values("k", kind="stable")["orig"].to_numpy()
print("sort_values single column, default kind equals stable order on 20000 tied rows:", bool((default_order == stable_order).all()))
print("empty and single-row:", (pd.Series([], dtype=object) != pd.Series([], dtype=object).shift()).cumsum().tolist(),
      (pd.Series(["up"]) != pd.Series(["up"]).shift()).cumsum().tolist())
print("asserts passed")
```

**Output (my run):**
```text
SQL LAG flag + running SUM:
 run_id status  first_pos  last_pos  run_len
      1     up          1         2        2
      2   down          3         5        3
      3     up          6         6        1

pandas run key: [1, 1, 2, 2, 2, 3]
pandas equals SQL: True

groupby on the value itself: {'down': 3, 'up': 3} (two separate up runs merged into one group of 3)
itertools.groupby run lengths: [('up', 2), ('down', 3), ('up', 1)]
first flag: True | shift()[0]: nan

wrong, global shift: runs by run key only -> [{'n_rows': 2, 'n_entities': 1}, {'n_rows': 3, 'n_entities': 1}, {'n_rows': 3, 'n_entities': 2}, {'n_rows': 1, 'n_entities': 1}]
per-entity pandas equals SQL (sorted by entity, run_id): True
entity  run_id status  first_ts  last_ts  run_len
     A       1     up         1        2        2
     A       2   down         3        5        3
     A       3     up         6        6        1
     B       1     up         1        2        2
     B       2   down         3        3        1

NULL,NULL in the middle: SQL run lengths [1, 2, 1] | pandas naive [1, 1, 1, 1] | pandas fixed [1, 2, 1]
NaN != NaN: True | pandas Series: [True]
int Series shift dtype: float64 | shift(fill_value=-1) dtype: int64 | runs: [1, 1, 2, 2, 3]
groupby rows with a NULL entity: default 9 | dropna=False 10 | total rows 10
sort_values single column, default kind equals stable order on 20000 tied rows: False
empty and single-row: [] [1]
asserts passed
```

**Edge cases:**
- Why `groupby` on the value merges runs: `seq.groupby("status").size()` gave `up: 3, down: 3` (the two separate up runs became one group of 3). The run key, not the value, identifies a run; the same value in two places is two runs.
- Why the first comparison is True: `shift()` puts NaN in the first slot, and `'up' != NaN` is True, so the first row always starts run 1. Without that you would have to treat row 0 specially (printed in the output: the first flag was True and `shift()[0]` was `nan`).
- Per entity: with one global `shift()` the end of entity A and the start of entity B were compared. B's first `'up'` equals A's last `'up'`, so the flag was False and one run mixed both entities (the wrong run list in the output has a run of 3 rows spanning 2 entities). `groupby("entity")["status"].shift()` makes B's first row NaN, so it starts a run, and `.groupby(entity).cumsum()` restarts the numbering (like `PARTITION BY` in the SQL).
- NULL status, an honest difference: in SQL, `status IS NOT LAG(status)` treats two consecutive NULLs as equal, so they form one run (lengths 1, 2, 1). In pandas `NaN != NaN` is True (checked: `np.nan != np.nan` printed `True`, also in a Series), so the naive key made every missing row its own run (1, 1, 1, 1). I made the pandas side match by masking rows where both the value and the previous value are missing (printed "pandas fixed"). Decide whether consecutive unknowns are one run or separate, and write it down.
- Integer states: `shift()` upcasts an integer Series to `float64` (printed: `float64`), because the first element becomes NaN; `shift(fill_value=-1)` keeps `int64`. The comparison still works, but any later arithmetic or equality with the original ints needs a cast.
- `groupby` drops rows with a NaN key by default: ten rows with one NULL entity gave a total size of 9, and 10 with `dropna=False`. In a run-key `groupby` the key is the cumsum, so it is never NaN, but an entity column with NULLs would silently lose rows.
- Sorting: unsorted input needs `sort_values` first, and the sort must be deterministic. A single-column `sort_values("k")` with default settings did not keep input order for tied rows in my test (20,000 rows, 5 distinct values: default order did not equal `kind="stable"` order). So sort by `["entity", "ts"]` plus a unique id, or pass `kind="stable"`, whenever timestamps can tie.
- Empty and single-row input: the key is empty for an empty Series and `[1]` for one row.
- `itertools.groupby` gives the same run lengths in plain Python, `[('up', 2), ('down', 3), ('up', 1)]`, but only over sorted data and one Series at a time.

**Then explain:**
- The trick is "mark the change, then count the marks". The same idea is the SQL running `SUM` of a flag.
- Output of the aggregation is run-length encoding: value, first position, last position, length.
- `diff().ne(0).cumsum()` is the numeric version of the same key (a run changes when the difference is not 0). It is covered in Q2 with `ne(1)`.
- For data with real timestamps, the position columns would be times, and gaps in time can be added as another change condition (sessions, Q11 onward).
- SQL dialect note (not executed): `IS DISTINCT FROM` is the standard NULL-safe form in PostgreSQL; I ran `IS NOT` on SQLite only.

**Follow-ups:**
- *Longest run per entity?* `run_len` max after the aggregation (Q7 and Q13 style).
- *Only the up runs?* Filter the status after the aggregation, never before the run key (filtering first would glue separate runs together).
- *Runs of the same status across both statuses at once?* The run key already does this; every row belongs to exactly one run.

**Common mistakes:**
- Grouping by the value instead of the run key.
- A global `shift()` across entities.
- Forgetting to sort, or sorting with ties and no tie-breaker.
- Treating NaN like an ordinary value (`NaN != NaN` is True) and getting one run per missing row.
- Filtering to one status before building the run key.

### Q6 ⭐⭐⭐ 🟡 Consecutive-day login streaks per user: logins(user_id, login_date) with ISO dates, possibly unsorted and with several users. Return one row per streak: user_id, streak_start, streak_end, streak_days, using the date minus ROW_NUMBER key with julianday in SQLite. Include a user with a single login day (a streak of 1) and a user whose logins span a month and year boundary (2024-12-30 to 2025-01-02) to show that day arithmetic, not string arithmetic, is needed.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** Dedupe to one row per user per day, number each user's days with `ROW_NUMBER()`, subtract that from `julianday(login_date)`, and `GROUP BY user_id, key`; each group is one streak with `MIN` as start, `MAX` as end and `COUNT(*)` as days.

**Schema and sample data:** four users, inserted out of order. User 1: 03-01, 03-02 | 03-04 | 03-07 to 03-09 (three streaks, gaps of exactly 2 and 3 days). User 2: one login (streak of 1). User 3: 2024-12-30 to 2025-01-02 (month and year boundary). User 4: 2024-02-28, 2024-02-29, 2024-03-01 (leap day, to show the month-end arithmetic with 29 days).
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-07'),(1,'2024-03-02'),(1,'2024-03-01'),(1,'2024-03-09'),(1,'2024-03-08'),(1,'2024-03-04'),
 (2,'2024-03-15'),
 (3,'2025-01-02'),(3,'2024-12-30'),(3,'2025-01-01'),(3,'2024-12-31'),
 (4,'2024-03-01'),(4,'2024-02-28'),(4,'2024-02-29');
```
This is the same idea as Q1 (why it works) with more users and boundaries; here the focus is the streak table and what breaks it.

**SQL answer:** `SQL_MAIN` in the Code block. The `d` CTE removes duplicate days and NULL dates so the numbering is safe (Q8 shows what happens without it):
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start
```
Day arithmetic needs a number. SQLite has no integer date type, so `julianday()` supplies it. `SQL_INT_KEY` uses `CAST(julianday(login_date) AS INTEGER)` and gave identical streaks. `SQL_STRING_KEY` is the wrong version that uses a `yyyymmdd` integer.

**pandas answer:** shown once, identical to the Code block. Parse to real dates, drop duplicates and NULLs, sort, then key = date minus a timedelta of the per-user row number:
```py
l = (logins.dropna(subset=["login_date"]).drop_duplicates()
           .assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
           .sort_values(["user_id", "login_date"]))
l["key"] = l["login_date"] - pd.to_timedelta(l.groupby("user_id").cumcount() + 1, unit="D")
pd_df = (l.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start"]).reset_index(drop=True))
```
A second idiom is in the Code block: `diff()` per user, a new streak wherever the step is not exactly `pd.Timedelta(days=1)`, then a per-user `cumsum`. It matched SQL too.

**Example (by hand):** user 1 sorted: 03-01, 03-02, 03-04, 03-07, 03-08, 03-09 (six distinct days).
- Row numbers 1..6. Day number minus row number (last digits of julianday, 2460000 dropped): 369.5, 369.5, 370.5, 372.5, 372.5, 372.5. (03-01 is 370.5; 370.5 - 1 = 369.5 and so on.)
- Three keys: 369.5 (03-01, 03-02, 2 days), 370.5 (03-04, 1 day), 372.5 (03-07 to 03-09, 3 days).
- User 2: one row, one streak of 1.
- User 3: day numbers rise by exactly 1 across 12-31 to 01-01, so one streak of 4.
- User 4: 02-28, 02-29, 03-01 are consecutive days in a leap year, so one streak of 3. A `yyyymmdd` key jumps from 20240229 to 20240301 (a step of 72), so it cut this into 2 + 1 (output above); it cut user 3 into 2 + 2.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after sorting both by `user_id, streak_start` (dates formatted as `YYYY-MM-DD`).
```python
# Q6: consecutive-day login streaks per user (date minus ROW_NUMBER with julianday) + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-07'),(1,'2024-03-02'),(1,'2024-03-01'),(1,'2024-03-09'),(1,'2024-03-08'),(1,'2024-03-04'),
 (2,'2024-03-15'),
 (3,'2025-01-02'),(3,'2024-12-30'),(3,'2025-01-01'),(3,'2024-12-31'),
 (4,'2024-03-01'),(4,'2024-02-28'),(4,'2024-02-29');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start
"""
SQL_INT_KEY = SQL_MAIN.replace(
    "julianday(login_date)\n           - ROW_NUMBER()",
    "CAST(julianday(login_date) AS INTEGER)\n           - ROW_NUMBER()")
SQL_STRING_KEY = SQL_MAIN.replace(
    "julianday(login_date)\n           - ROW_NUMBER()",
    "CAST(strftime('%Y%m%d', login_date) AS INTEGER)\n           - ROW_NUMBER()")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
assert SQL_INT_KEY != SQL_MAIN and SQL_STRING_KEY != SQL_MAIN
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("streaks (SQL):")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(pd.read_sql_query(SQL_INT_KEY, con), sql_df)
print("integer day-number key gives the same streaks: True")
bad = pd.read_sql_query(SQL_STRING_KEY, con)
print("\nyyyymmdd-style key, wrong at month ends (users 3 and 4):")
print(bad.query("user_id in (3, 4)").to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
l = (logins.dropna(subset=["login_date"]).drop_duplicates()
           .assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
           .sort_values(["user_id", "login_date"]))
l["key"] = l["login_date"] - pd.to_timedelta(l.groupby("user_id").cumcount() + 1, unit="D")
pd_df = (l.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start"]).reset_index(drop=True))
# pd:end
for c in ("streak_start", "streak_end"):
    pd_df[c] = pd_df[c].dt.strftime("%Y-%m-%d")
# compared after sorting by user_id, streak_start
pd.testing.assert_frame_equal(pd_df, sql_df)
print("\npandas equals SQL: True")

# second pandas idiom: new streak when the day step is not exactly one day
step = l.groupby("user_id")["login_date"].diff()
new = step != pd.Timedelta(days=1)
sid = new.groupby(l["user_id"]).cumsum()
alt = l.groupby(["user_id", sid]).agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"),
        streak_days=("login_date", "size")).reset_index(level=0).reset_index(drop=True)
alt["streak_start"] = alt["streak_start"].dt.strftime("%Y-%m-%d")
alt["streak_end"] = alt["streak_end"].dt.strftime("%Y-%m-%d")
pd.testing.assert_frame_equal(alt, sql_df)
print("diff() != 1 day version equals SQL: True")

# exact-threshold gap and single login
print("user 1 steps in days:", [int(x.days) if pd.notna(x) else None for x in step[l["user_id"] == 1]])
print("single-login user 2:", sql_df[sql_df.user_id == 2].to_dict("records"))

# timestamps instead of dates: julianday is fractional, date() fixes it
con.executescript("""
CREATE TABLE lt(user_id INTEGER, login_date TEXT);
INSERT INTO lt VALUES (7,'2024-03-01 09:00:00'),(7,'2024-03-02 08:00:00'),(7,'2024-03-03 23:30:00');
""")
print("\ntimestamps, julianday key on raw text:", con.execute(SQL_MAIN.replace("FROM logins", "FROM lt")).fetchall())
fixed = SQL_MAIN.replace("SELECT DISTINCT user_id, login_date\n  FROM logins", "SELECT DISTINCT user_id, date(login_date) AS login_date\n  FROM lt")
print("timestamps, date() first:", con.execute(fixed).fetchall())
print("non-ISO text: julianday('2024-1-6') =", con.execute("SELECT julianday('2024-1-6')").fetchone()[0])

# duplicates and NULL and empty
con.executescript("INSERT INTO logins VALUES (1,'2024-03-02'),(2,NULL);")
pd.testing.assert_frame_equal(pd.read_sql_query(SQL_MAIN, con), sql_df)
print("duplicate day and NULL date added: SQL result unchanged (DISTINCT and IS NOT NULL in the CTE)")
con.execute("DELETE FROM logins")
print("empty table rows:", len(con.execute(SQL_MAIN).fetchall()))
print("asserts passed")
```

**Output (my run):**
```text
streaks (SQL):
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-02            2
       1   2024-03-04 2024-03-04            1
       1   2024-03-07 2024-03-09            3
       2   2024-03-15 2024-03-15            1
       3   2024-12-30 2025-01-02            4
       4   2024-02-28 2024-03-01            3
integer day-number key gives the same streaks: True

yyyymmdd-style key, wrong at month ends (users 3 and 4):
 user_id streak_start streak_end  streak_days
       3   2024-12-30 2024-12-31            2
       3   2025-01-01 2025-01-02            2
       4   2024-02-28 2024-02-29            2
       4   2024-03-01 2024-03-01            1

pandas equals SQL: True
diff() != 1 day version equals SQL: True
user 1 steps in days: [None, 1, 2, 3, 1, 1]
single-login user 2: [{'user_id': 2, 'streak_start': '2024-03-15', 'streak_end': '2024-03-15', 'streak_days': 1}]

timestamps, julianday key on raw text: [(7, '2024-03-01 09:00:00', '2024-03-01 09:00:00', 1), (7, '2024-03-02 08:00:00', '2024-03-02 08:00:00', 1), (7, '2024-03-03 23:30:00', '2024-03-03 23:30:00', 1)]
timestamps, date() first: [(7, '2024-03-01', '2024-03-03', 3)]
non-ISO text: julianday('2024-1-6') = None
duplicate day and NULL date added: SQL result unchanged (DISTINCT and IS NOT NULL in the CTE)
empty table rows: 0
asserts passed
```

**Edge cases:**
- Exact thresholds: a step of exactly 1 day continues the streak; a step of exactly 2 days (03-02 to 03-04 for user 1) ends it. The printed day steps for user 1 are 1, 2, 3, 1, 1 (first is None).
- Month, year and leap-year boundaries need real day numbers. The `yyyymmdd` key broke users 3 and 4 in my run; plain string subtraction (`login_date - rn`) coerces the text to 2024 or 2025 and was shown in Q1.
- Single-row user: streak of 1, start = end (user 2).
- Duplicates in the date column: after adding a second row for user 1 on 03-02 and a NULL date for user 2, the result was unchanged only because of `SELECT DISTINCT` and `IS NOT NULL` in the CTE. Without them the key splits (Q1 and Q8).
- Unsorted input: the window `ORDER BY` and the pandas `sort_values` define the order; the insertion order does not matter (the sample is deliberately unsorted).
- Timestamps instead of dates: with `'2024-03-01 09:00:00'` style text, `julianday` carries a fractional part that changes day to day, so the key was not constant and the three consecutive days came out as three streaks of 1. Taking `date(login_date)` first returned one streak of 3. Always reduce timestamps to dates before the key.
- Non-ISO text such as `'2024-1-6'`: `julianday` returns NULL (printed `None`) and the NULL key silently merges all such rows, so validate formats. pandas would parse some of these (Part 6 note).
- Empty table: zero rows.

**Then explain:**
- A streak is a maximal run of consecutive calendar days, so one row per user per day is the precondition; everything else (duplicates, timestamps, NULLs) is cleaned in a CTE first.
- `julianday` returns a float (midnight dates end in `.5`, exact in binary); the integer cast is a safe alternative for dates.
- Streak length is `COUNT(*)` of the distinct days, which equals `end - start + 1` in days; that identity is a good sanity check.
- Dialects (not executed here): PostgreSQL can do `login_date - (ROW_NUMBER() OVER (...))::int` on a `DATE`; MySQL 8 and BigQuery use `DATE_SUB(login_date, INTERVAL rn DAY)`. I did not run these.

**Follow-ups:**
- *Longest streak per user, with dates?* Rank the streaks (Q7).
- *Current streak as of a date?* Keep the island whose end is the as-of date or the day before (Q15).
- *Does a login at 23:59 and another at 00:01 count as two days?* By calendar date, yes; by 24-hour windows, no. State the rule.

**Common mistakes:**
- String or `yyyymmdd` arithmetic instead of day numbers.
- Not deduplicating days or removing NULLs.
- Using timestamps without truncating to dates.
- Grouping by the key without `user_id`.
- Not sorting in pandas before `cumcount`.

### Q7 ⭐⭐⭐ 🟡 Longest streak per user: logins(user_id, login_date). Return the longest consecutive-day streak per user with its start and end dates. Show the island CTE then a reduction, and handle ties between two equally long streaks (return both or the most recent, state the rule and enforce it with ROW_NUMBER ordered by days DESC, streak_end DESC). Compare MAX(days) grouped (loses the dates) with the ranking approach (keeps them).
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** Build the streak table first (one row per island), then rank each user's streaks with `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, streak_end DESC)` and keep rank 1, so ties go to the most recent streak and the dates survive, which a grouped `MAX(days)` cannot do.

**Schema and sample data:** four users with logins inserted out of order, plus a `users` table with a fifth user who never logged in. User 1 has two 3-day streaks (tie) and a 1-day streak; user 2 has a 5-day streak and a later 2-day one; user 3 has one login; user 4 has two 2-day streaks (tie).
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-11'),(1,'2024-03-01'),(1,'2024-03-10'),(1,'2024-03-02'),(1,'2024-03-12'),(1,'2024-03-03'),(1,'2024-03-06'),
 (2,'2024-04-05'),(2,'2024-04-01'),(2,'2024-04-02'),(2,'2024-04-03'),(2,'2024-04-04'),(2,'2024-04-20'),(2,'2024-04-21'),
 (3,'2024-05-09'),
 (4,'2024-06-01'),(4,'2024-06-02'),(4,'2024-06-05'),(4,'2024-06-06');
CREATE TABLE users(user_id INTEGER);
INSERT INTO users VALUES (1),(2),(3),(4),(5);
```

**SQL answer:** the island CTE (same as Q6: distinct days, `julianday - ROW_NUMBER`, group) followed by a ranking step. `SQL_MAIN` in the Code block is `ISLANDS` followed by `SQL_RANK_ONE` (concatenated). The island part:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
),
s AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
  FROM x
  GROUP BY user_id, grp
)
```
and the ranking part:
```sql
, r AS (
  SELECT user_id, streak_start, streak_end, days,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, streak_end DESC) AS rn
  FROM s
)
SELECT user_id, streak_start, streak_end, days
FROM r
WHERE rn = 1
ORDER BY user_id
```
Rule stated and enforced: if two streaks have equal length, the one with the later `streak_end` wins. Because `ROW_NUMBER` never ties, each user gets exactly one row. To return both tied streaks instead, replace the window with `RANK() OVER (PARTITION BY user_id ORDER BY days DESC)` and filter `rk = 1` (`SQL_RANK_TIES`, appended to `ISLANDS` as `SQL_BOTH`). Ranking function behaviour in general is Part 4; here only the tie rule matters.

**pandas answer:** the same streak table (as in Q6), then sort by `user_id`, `days` descending, `streak_end` descending and take the first row per user; the keep-ties version compares each streak with the user's maximum. Shown once, identical to the Code block:
```py
l = (logins.dropna(subset=["login_date"]).drop_duplicates()
           .assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
           .sort_values(["user_id", "login_date"]))
l["key"] = l["login_date"] - pd.to_timedelta(l.groupby("user_id").cumcount() + 1, unit="D")
st = (l.groupby(["user_id", "key"])
        .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), days=("login_date", "size"))
        .reset_index().drop(columns="key"))
best = (st.sort_values(["user_id", "days", "streak_end"], ascending=[True, False, False])
          .groupby("user_id").head(1).sort_values("user_id").reset_index(drop=True))
both = st[st["days"] == st.groupby("user_id")["days"].transform("max")].sort_values(["user_id", "streak_start"]).reset_index(drop=True)
```

**Example (by hand):**
- User 1 streaks: 03-01 to 03-03 (3 days), 03-06 (1 day), 03-10 to 03-12 (3 days). Longest is 3, tied; rule says latest end, so 03-10 to 03-12. `RANK` keeps both.
- User 2: 04-01 to 04-05 (5 days) beats 04-20 to 04-21 (2 days): one row, no tie.
- User 3: one login, one streak of 1.
- User 4: two streaks of 2 (06-01 to 06-02 and 06-05 to 06-06); tie, latest wins: 06-05 to 06-06.
- User 5 never logged in: no streak rows, so the ranking has no row for them; a `LEFT JOIN` from `users` with `COALESCE(days, 0)` returns 0.

**Code:** run with `python3 -I`. The asserts compare after sorting by `user_id` (most recent tie rule) and by `user_id, streak_start` (keep-ties version), dates as `YYYY-MM-DD` text.
```python
# Q7: longest streak per user with dates, tie rule most recent (days DESC, streak_end DESC)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-11'),(1,'2024-03-01'),(1,'2024-03-10'),(1,'2024-03-02'),(1,'2024-03-12'),(1,'2024-03-03'),(1,'2024-03-06'),
 (2,'2024-04-05'),(2,'2024-04-01'),(2,'2024-04-02'),(2,'2024-04-03'),(2,'2024-04-04'),(2,'2024-04-20'),(2,'2024-04-21'),
 (3,'2024-05-09'),
 (4,'2024-06-01'),(4,'2024-06-02'),(4,'2024-06-05'),(4,'2024-06-06');
CREATE TABLE users(user_id INTEGER);
INSERT INTO users VALUES (1),(2),(3),(4),(5);
"""
ISLANDS = """
WITH d AS (
  SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
),
s AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
  FROM x
  GROUP BY user_id, grp
)
"""
SQL_ALL = ISLANDS + "SELECT * FROM s ORDER BY user_id, streak_start"
SQL_RANK_ONE = """
, r AS (
  SELECT user_id, streak_start, streak_end, days,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, streak_end DESC) AS rn
  FROM s
)
SELECT user_id, streak_start, streak_end, days
FROM r
WHERE rn = 1
ORDER BY user_id
"""
SQL_MAIN = ISLANDS + SQL_RANK_ONE
SQL_RANK_TIES = """
, r AS (
  SELECT user_id, streak_start, streak_end, days,
         RANK() OVER (PARTITION BY user_id ORDER BY days DESC) AS rk
  FROM s
)
SELECT user_id, streak_start, streak_end, days
FROM r
WHERE rk = 1
ORDER BY user_id, streak_start
"""
SQL_BOTH = ISLANDS + SQL_RANK_TIES
SQL_MAX_ONLY = ISLANDS + "SELECT user_id, MAX(days) AS days FROM s GROUP BY user_id ORDER BY user_id"
SQL_ZERO = ISLANDS + """
, r AS (
  SELECT user_id, days,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, streak_end DESC) AS rn
  FROM s
)
SELECT u.user_id, COALESCE(r.days, 0) AS days
FROM users u LEFT JOIN r ON r.user_id = u.user_id AND r.rn = 1
ORDER BY u.user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
show = lambda sql: print(pd.read_sql_query(sql, con).to_string(index=False))
print("all streaks:"); show(SQL_ALL)
print("\nlongest per user, tie -> most recent (ROW_NUMBER):"); show(SQL_MAIN)
print("\nlongest per user, ties kept (RANK):"); show(SQL_BOTH)
print("\nMAX(days) grouped, dates lost:"); show(SQL_MAX_ONLY)
print("\nusers with no logins via LEFT JOIN + COALESCE:"); show(SQL_ZERO)
print("\nSQLite bare-column quirk (not standard, tie is arbitrary), MAX(days) with streak_start:")
show(ISLANDS + "SELECT user_id, MAX(days) AS days, streak_start FROM s GROUP BY user_id ORDER BY user_id")
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_both = pd.read_sql_query(SQL_BOTH, con)

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
l = (logins.dropna(subset=["login_date"]).drop_duplicates()
           .assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
           .sort_values(["user_id", "login_date"]))
l["key"] = l["login_date"] - pd.to_timedelta(l.groupby("user_id").cumcount() + 1, unit="D")
st = (l.groupby(["user_id", "key"])
        .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), days=("login_date", "size"))
        .reset_index().drop(columns="key"))
best = (st.sort_values(["user_id", "days", "streak_end"], ascending=[True, False, False])
          .groupby("user_id").head(1).sort_values("user_id").reset_index(drop=True))
both = st[st["days"] == st.groupby("user_id")["days"].transform("max")].sort_values(["user_id", "streak_start"]).reset_index(drop=True)
# pd:end
fmt = lambda f: f.assign(streak_start=f["streak_start"].dt.strftime("%Y-%m-%d"), streak_end=f["streak_end"].dt.strftime("%Y-%m-%d"))
# compared after sorting by user_id (and streak_start for the keep-ties version)
pd.testing.assert_frame_equal(fmt(best), sql_df)
pd.testing.assert_frame_equal(fmt(both), sql_both)
print("\npandas most-recent-tie and keep-ties versions equal SQL: True")
print("pandas groupby max only:", st.groupby("user_id")["days"].max().to_dict())
idx = st.groupby("user_id")["days"].idxmax()
print("idxmax picks the first row among ties (stable by position), user 1 ->", st.loc[idx[1], "streak_end"].strftime("%Y-%m-%d"), "(older streak, not the most recent)")

# edge: empty and single-row
con.execute("DELETE FROM logins")
print("empty table, rows:", len(con.execute(SQL_MAIN).fetchall()), "| users LEFT JOIN:", con.execute(SQL_ZERO).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
all streaks:
 user_id streak_start streak_end  days
       1   2024-03-01 2024-03-03     3
       1   2024-03-06 2024-03-06     1
       1   2024-03-10 2024-03-12     3
       2   2024-04-01 2024-04-05     5
       2   2024-04-20 2024-04-21     2
       3   2024-05-09 2024-05-09     1
       4   2024-06-01 2024-06-02     2
       4   2024-06-05 2024-06-06     2

longest per user, tie -> most recent (ROW_NUMBER):
 user_id streak_start streak_end  days
       1   2024-03-10 2024-03-12     3
       2   2024-04-01 2024-04-05     5
       3   2024-05-09 2024-05-09     1
       4   2024-06-05 2024-06-06     2

longest per user, ties kept (RANK):
 user_id streak_start streak_end  days
       1   2024-03-01 2024-03-03     3
       1   2024-03-10 2024-03-12     3
       2   2024-04-01 2024-04-05     5
       3   2024-05-09 2024-05-09     1
       4   2024-06-01 2024-06-02     2
       4   2024-06-05 2024-06-06     2

MAX(days) grouped, dates lost:
 user_id  days
       1     3
       2     5
       3     1
       4     2

users with no logins via LEFT JOIN + COALESCE:
 user_id  days
       1     3
       2     5
       3     1
       4     2
       5     0

SQLite bare-column quirk (not standard, tie is arbitrary), MAX(days) with streak_start:
 user_id  days streak_start
       1     3   2024-03-01
       2     5   2024-04-01
       3     1   2024-05-09
       4     2   2024-06-01

pandas most-recent-tie and keep-ties versions equal SQL: True
pandas groupby max only: {1: 3, 2: 5, 3: 1, 4: 2}
idxmax picks the first row among ties (stable by position), user 1 -> 2024-03-03 (older streak, not the most recent)
empty table, rows: 0 | users LEFT JOIN: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
asserts passed
```

**Edge cases:**
- Ties: shown for users 1 and 4. `ROW_NUMBER` with `streak_end DESC` is deterministic; `ROW_NUMBER ... ORDER BY days DESC` alone would pick an arbitrary tied row, which can change between runs or engines.
- `MAX(days)` grouped by user returned the right length (3, 5, 1, 2) but no dates. Joining it back to the streak table on `days` returns both tied rows (the keep-ties result), so it is not a shortcut for the one-row rule.
- SQLite quirk (not standard, so avoid): `SELECT user_id, MAX(days), streak_start ... GROUP BY user_id` returned a `streak_start` from the max row, and for the tied users it returned the older streak (03-01 and 06-01). SQLite documents that bare columns come from the row holding the max, but the tie is arbitrary, and PostgreSQL would reject the query (not executed here).
- pandas `idxmax` also picks the first of the tied rows (user 1 returned the older streak ending 03-03), so a plain `groupby().idxmax()` silently applies a "keep the oldest" rule. Sorting with the explicit tie column avoids that.
- User with no logins: no row from the ranking; use `users LEFT JOIN` if a zero is wanted (user 5 got 0 in my run, and with an empty `logins` table every user got 0).
- Single-row user: streak of 1 is the longest (user 3).
- Duplicate days and NULL dates are cleaned in the first CTE (`SELECT DISTINCT ... WHERE login_date IS NOT NULL`); without that the streak lengths are wrong (Q8).
- Unsorted input: handled by the window orders and by `sort_values` in pandas.
- Empty table: zero rows from the ranking.

**Then explain:**
- Two steps: islands (one row per streak), then reduction (one row per user). The reduction is just a top-1 per group (Part 4).
- The tie rule is a business decision; "most recent" is natural for a current-form view, "earliest" for a record that was set first. Either way it must be a total order, so the last sort key has to separate any two streaks of one user. Two streaks of the same user cannot share an end date, so `streak_end` is a safe tiebreaker.
- `RANK = 1` returns all ties; `ROW_NUMBER = 1` returns exactly one.
- Dialects (not executed here): PostgreSQL has `DISTINCT ON (user_id)` with `ORDER BY user_id, days DESC, streak_end DESC` as a shortcut, BigQuery and Snowflake have `QUALIFY ROW_NUMBER() OVER (...) = 1`. SQLite 3.45 has neither, so the extra CTE is needed.

**Follow-ups:**
- *Top 3 streaks per user?* `rn <= 3` (or `DENSE_RANK`).
- *Longest streak ever across all users?* Same ranking without the `PARTITION BY`.
- *Current streak versus longest?* Current is the island ending on the as-of date (Q15).

**Common mistakes:**
- `GROUP BY user_id` with `MAX(days)` and then trying to attach the dates.
- A tie rule left to chance (no second sort key).
- Using `RANK` when exactly one row is expected.
- Forgetting users with no logins in a "per user" report.
- Relying on SQLite's bare-column behaviour.

### Q8 ⭐⭐⭐ 🟡 Debugging: the streak counts are wrong when logins has duplicate dates. logins(user_id, login_date) contains the same user and day twice (several logins per day). Show that date minus ROW_NUMBER then breaks the island (a duplicate day gets a different row number, splitting a run into islands or shortening the run) and that counting rows overstates streak_days. Fix it two ways: SELECT DISTINCT user_id, login_date first, and DENSE_RANK in place of ROW_NUMBER with COUNT(DISTINCT login_date). Show the wrong and fixed output for one user.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** `ROW_NUMBER` gives a repeated day its own number, so the number advances while the date does not and the key moves; the run splits (or even bridges a real gap), and `COUNT(*)` counts duplicate rows as extra days; fix it by taking `DISTINCT` days first, or by `DENSE_RANK` with `COUNT(DISTINCT login_date)`.

**Schema and sample data:** four users with duplicate login rows, inserted out of order.
- User 1: 03-01, 03-02 (twice), 03-03, 03-04. The true streak is 4 days.
- User 2: 03-01 (twice), 03-02, 03-03. True streak 3 days (duplicate at the start).
- User 3: 03-10, 03-11, 03-13 (twice). True: a 2-day streak 03-10 to 03-11 and a 1-day streak on 03-13; the gap on 03-12 is exactly one missing day.
- User 4: 03-09 twice. True: one streak of 1 day.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-02'),(2,'2024-03-01'),(2,'2024-03-03'),(2,'2024-03-01'),
 (3,'2024-03-13'),(3,'2024-03-10'),(3,'2024-03-13'),(3,'2024-03-11'),
 (4,'2024-03-09'),(4,'2024-03-09');
```

**SQL answer:** the wrong query first (`SQL_WRONG`), the same query with the fixes (`SQL_DISTINCT`, `SQL_DENSE`), all in the Code block.
```sql
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
```
Fix 1, `DISTINCT` days first, then the usual key:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
```
Fix 2, `DENSE_RANK` (equal dates share one number, no gaps in the numbering) and a distinct count:
```sql
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - DENSE_RANK() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
  WHERE login_date IS NOT NULL
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end,
       COUNT(DISTINCT login_date) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
```
`SQL_DENSE_COUNT_STAR` in the Code block is Fix 2 with `COUNT(*)` left in, to show the overstated count.

**pandas answer:** shown once, identical to the Code block. `drop_duplicates()` is Fix 1; the Code block also runs `rank(method="dense")` as Fix 2 and asserts it against the same SQL.
```py
d = logins.dropna(subset=["login_date"]).drop_duplicates()
d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["user_id", "login_date"])
d["key"] = d["login_date"] - pd.to_timedelta(d.groupby("user_id").cumcount() + 1, unit="D")
pd_df = (d.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "nunique"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
```

**Example (by hand):** user 1 sorted: 03-01, 03-02, 03-02, 03-03, 03-04 (day numbers 370.5, 371.5, 371.5, 372.5, 373.5 with 2460000 dropped).
- `ROW_NUMBER` gives 1..5, so the keys are 369.5, 369.5, 368.5, 368.5, 368.5. The second 03-02 carries a number that is one too high for its date, so the key drops and the run splits: 03-01 to 03-02 (2 rows) and 03-02 to 03-04 (3 rows). The true answer is one streak of 4.
- `DENSE_RANK` gives 1, 2, 2, 3, 4, so keys are 369.5 for all five rows: one island, 03-01 to 03-04. But `COUNT(*)` counts 5 rows; `COUNT(DISTINCT login_date)` counts 4.
- `DISTINCT` first leaves four rows, numbers 1..4, one key, 4 days.
- User 3 is the nastier case: the duplicate 03-13 raises the row number by one, which exactly cancels the one-day gap on 03-12, so the wrong query reported a 03-10 to 03-13 streak of 3 across a real gap, plus a separate one-day streak.

**Code:** run with `python3 -I`. The asserts compare frames sorted by `user_id, streak_start, streak_end`: Fix 1 equals Fix 2 in SQL, both differ from the wrong versions, and pandas equals the fixed SQL.
```python
# Q8: duplicate dates break date minus ROW_NUMBER; fix with DISTINCT or DENSE_RANK + COUNT(DISTINCT)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-02'),(2,'2024-03-01'),(2,'2024-03-03'),(2,'2024-03-01'),
 (3,'2024-03-13'),(3,'2024-03-10'),(3,'2024-03-13'),(3,'2024-03-11'),
 (4,'2024-03-09'),(4,'2024-03-09');
"""
SQL_WRONG = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_DENSE_COUNT_STAR = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - DENSE_RANK() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_DISTINCT = """
WITH d AS (
  SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_DENSE = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - DENSE_RANK() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
  WHERE login_date IS NOT NULL
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end,
       COUNT(DISTINCT login_date) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda sql: pd.read_sql_query(sql, con)
wrong, dense_star, fix1, fix2 = q(SQL_WRONG), q(SQL_DENSE_COUNT_STAR), q(SQL_DISTINCT), q(SQL_DENSE)
for title, df in [("WRONG: ROW_NUMBER on duplicate rows", wrong),
                  ("WRONG: DENSE_RANK but COUNT(*)", dense_star),
                  ("FIX 1: DISTINCT first", fix1),
                  ("FIX 2: DENSE_RANK + COUNT(DISTINCT login_date)", fix2)]:
    print(title); print(df.to_string(index=False)); print()
pd.testing.assert_frame_equal(fix1, fix2)
assert not wrong.equals(fix1) and not dense_star.equals(fix1)
print("fix 1 equals fix 2: True; both wrong versions differ from the fixed result: True")
print("user 1, wrong vs fixed:", wrong[wrong.user_id == 1][["streak_start", "streak_end", "streak_days"]].values.tolist(),
      "vs", fix1[fix1.user_id == 1][["streak_start", "streak_end", "streak_days"]].values.tolist())

logins = pd.read_sql_query("SELECT * FROM logins", con)
def streaks(frame, mode):
    f = frame.dropna(subset=["login_date"]).assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
    f = f.sort_values(["user_id", "login_date"])
    if mode == "row_number":
        rn = f.groupby("user_id").cumcount() + 1
    else:
        rn = f.groupby("user_id")["login_date"].rank(method="dense").astype("int64")
    f["key"] = f["login_date"] - pd.to_timedelta(rn, unit="D")
    return f
# pd:main
d = logins.dropna(subset=["login_date"]).drop_duplicates()
d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["user_id", "login_date"])
d["key"] = d["login_date"] - pd.to_timedelta(d.groupby("user_id").cumcount() + 1, unit="D")
pd_df = (d.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "nunique"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
# pd:end
pd_df["streak_start"] = pd_df["streak_start"].dt.strftime("%Y-%m-%d")
pd_df["streak_end"] = pd_df["streak_end"].dt.strftime("%Y-%m-%d")
# compared after sorting by user_id, streak_start, streak_end
pd.testing.assert_frame_equal(pd_df, fix1)
print("pandas (drop_duplicates first) equals the fixed SQL: True")

# pandas without the fix reproduces the SQL bug; dense rank in pandas fixes it
f = streaks(logins, "row_number")
bug = f.groupby(["user_id", "key"]).agg(streak_days=("login_date", "size")).reset_index()
print("pandas without drop_duplicates, user 1 row counts per island:", bug[bug.user_id == 1]["streak_days"].tolist())
g = streaks(logins, "dense")
dd = (g.groupby(["user_id", "key"]).agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"),
      streak_days=("login_date", "nunique")).reset_index().drop(columns="key")
      .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
dd["streak_start"] = dd["streak_start"].dt.strftime("%Y-%m-%d")
dd["streak_end"] = dd["streak_end"].dt.strftime("%Y-%m-%d")
pd.testing.assert_frame_equal(dd, fix1)
print("pandas rank(method='dense') + nunique equals the fixed SQL: True")
print("rank returns dtype:", logins.assign(login_date=pd.to_datetime(logins["login_date"])).groupby("user_id")["login_date"].rank(method="dense").dtype)

# NULL date: DENSE_RANK variant without the filter, single-row and exact-threshold checks
con.execute("INSERT INTO logins VALUES (4, NULL)")
print("NULL date, DENSE version unfiltered:", con.execute(SQL_DENSE.replace("  WHERE login_date IS NOT NULL\n", "")).fetchall()[-2:])
pd.testing.assert_frame_equal(q(SQL_DENSE), fix1)
print("NULL date, filtered versions unchanged: True")
con.execute("DELETE FROM logins")
print("empty table:", len(con.execute(SQL_DISTINCT).fetchall()), "rows")
print("asserts passed")
```

**Output (my run):**
```text
WRONG: ROW_NUMBER on duplicate rows
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-02            2
       1   2024-03-02 2024-03-04            3
       2   2024-03-01 2024-03-01            1
       2   2024-03-01 2024-03-03            3
       3   2024-03-10 2024-03-13            3
       3   2024-03-13 2024-03-13            1
       4   2024-03-09 2024-03-09            1
       4   2024-03-09 2024-03-09            1

WRONG: DENSE_RANK but COUNT(*)
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-04            5
       2   2024-03-01 2024-03-03            4
       3   2024-03-10 2024-03-11            2
       3   2024-03-13 2024-03-13            2
       4   2024-03-09 2024-03-09            2

FIX 1: DISTINCT first
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-04            4
       2   2024-03-01 2024-03-03            3
       3   2024-03-10 2024-03-11            2
       3   2024-03-13 2024-03-13            1
       4   2024-03-09 2024-03-09            1

FIX 2: DENSE_RANK + COUNT(DISTINCT login_date)
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-04            4
       2   2024-03-01 2024-03-03            3
       3   2024-03-10 2024-03-11            2
       3   2024-03-13 2024-03-13            1
       4   2024-03-09 2024-03-09            1

fix 1 equals fix 2: True; both wrong versions differ from the fixed result: True
user 1, wrong vs fixed: [['2024-03-01', '2024-03-02', 2], ['2024-03-02', '2024-03-04', 3]] vs [['2024-03-01', '2024-03-04', 4]]
pandas (drop_duplicates first) equals the fixed SQL: True
pandas without drop_duplicates, user 1 row counts per island: [3, 2]
pandas rank(method='dense') + nunique equals the fixed SQL: True
rank returns dtype: float64
NULL date, DENSE version unfiltered: [(4, None, None, 0), (4, '2024-03-09', '2024-03-09', 1)]
NULL date, filtered versions unchanged: True
empty table: 0 rows
asserts passed
```

**Edge cases:**
- Duplicate at the start of a run (user 2): split into a 1-day island and a 3-row island whose `COUNT(*)` of 3 happens to match the true 3 days; the start date is repeated across two output rows. Correct-looking numbers are not proof.
- Duplicate in the middle (user 1): two islands of 2 and 3 rows instead of one of 4.
- Duplicate next to a real gap (user 3): the wrong query bridged the gap, a streak that never existed. This is the worst variant, because the total looks plausible.
- Single date, duplicated (user 4): the wrong query reported two streaks of 1 for one day.
- Count issue: `DENSE_RANK` with `COUNT(*)` found the right islands but reported 5, 4, 2, 2, 2 rows instead of 4, 3, 2, 1, 1 days. Every duplicate is an overstated day.
- NULL date: the `DENSE_RANK` version without `IS NOT NULL` gave an island with a NULL start and 0 days (`COUNT(DISTINCT NULL)` is 0), so filter first.
- Unsorted input is fine because the windows order the rows.
- Exact threshold: dates exactly 1 day apart stay together, exactly 2 apart split (user 3, 03-11 to 03-13, once duplicates are removed).
- Empty table: zero rows.
- pandas: without `drop_duplicates` the same split happens (user 1 row counts per island `[3, 2]`). `rank(method="dense")` returns `float64` (printed), so cast to integer before using it as a timedelta count. Which of two duplicate rows `drop_duplicates` keeps depends on the current row order and does not matter here (only user and date are kept), but it matters if you carry other columns; sort with `kind="stable"` or a tie column first.

**Then explain:**
- Day-minus-row-number needs the counter to rise exactly by one per distinct day. Any duplicate breaks that, either by shifting the key or by hiding a gap.
- `DISTINCT` first is simplest and also fixes the count. `DENSE_RANK` fixes the key but you must also count distinct days.
- Both are the same idea as Q1 and Q6; in a real warehouse the dedupe often belongs one layer upstream (a daily activity table).
- Duplicate timestamps (not just dates) show up the same way in sessionization; the sort needs a tie-breaker (Q11).
- Dialects (not executed here): `DENSE_RANK` and `COUNT(DISTINCT ...)` are standard; I expect them to behave the same in PostgreSQL, MySQL 8, BigQuery and Snowflake, but I did not run them.

**Follow-ups:**
- *How do you detect duplicates quickly?* `GROUP BY user_id, login_date HAVING COUNT(*) > 1`.
- *Which fix scales better?* Both sort once; `DISTINCT` adds a de-duplication step, `DENSE_RANK` needs the distinct count. Measure on your engine (not measured here).
- *What if the duplicate rows differ in other columns?* Decide which row to keep, or aggregate them, before the streak logic.

**Common mistakes:**
- Using `ROW_NUMBER` on data that is not unique per day.
- Fixing the key with `DENSE_RANK` but leaving `COUNT(*)`.
- Believing the output because the numbers look plausible.
- Deduplicating after the window instead of before.
- Forgetting NULL dates.
