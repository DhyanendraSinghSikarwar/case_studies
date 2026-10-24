# Book 3 — Part 7: Gaps and islands, streaks, sessionization, with pandas equivalents

**Topic:** islands of consecutive integers and dates (id or date minus ROW_NUMBER, julianday day numbers), login streaks per user (longest, current as of a fixed date, at least N days, number of streaks), gaps between consecutive values and dates (LAG/LEAD, missing ids, date spines), run-length encoding of status runs (LAG change flags, running SUM, ROW_NUMBER difference), consecutive-event counting (LeetCode 180, 601, 603, 1454, 1285, 2173), sessionization with a 30 minute timeout, overlapping and merging intervals, concurrency sweeps, booking conflicts, coverage gaps, state-change detection, slowly changing dimension range collapse, resets by condition, up-streaks and hot streaks, and the pandas counterparts ((s != s.shift()).cumsum(), diff().ne(1).cumsum(), cumcount, cummax interval merge, +1/-1 cumsum, rolling checks).
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 17, ⭐⭐ 14, ⭐ 9)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers gaps, islands, streaks, sessionization and interval problems. Basic ranking (Part 4), running-total mechanics and plain LAG/LEAD (Part 5), retention and cohorts (Part 6), funnels and DAU/MAU design (Part 8) and recursive CTEs in depth (Part 9) are out; where a question needs a date spine or a reset-by-condition it uses a short recursive CTE or points to Part 9. Every question states its tables so Wave B can build the sample data; dates are ISO text and 'as of' dates are fixed, never now.

Evidence limits: no candidate-reported SQL questions were found. Sources are practice-site and vendor pages (techinterview.org, DataVidhya, Dataiku, oneuptime, DataDriven; opened), the pandas shift reference (opened), and search snippets of LeetCode mirrors and Itzik Ben-Gan articles; leetcode.com returned HTTP 403 and the SQLite window functions page returned HTTP 503 again. 'Asked at' tags are source types, not company reports. Engine notes for Wave B (SQLite 3.45.1): date subtraction needs julianday or unixepoch; SQLite 3.45.1 supports both IS NOT and IS DISTINCT FROM for NULL-safe comparison (checked); other engines are hedged as not executed.

---

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

### Q9 ⭐⭐⭐ 🟡 Users with a streak of at least N days (LeetCode 1454 Active Users): logins(id, login_date) and accounts(id, name), where logins can contain duplicate rows. Return id and name of users who logged in on 5 or more consecutive days, ordered by id; then generalise to N as a parameter. Include a user with exactly 4 days and one with 5 days split by a gap, and explain why DISTINCT is applied before ranking.
**Asked at:** public LeetCode-style problem bank (statements known from search snippets and mirrors such as doocs, walkccc and talentd; the leetcode.com pages returned HTTP 403 and were not opened), not candidate reports; analyst, data scientist and data engineer screens at product companies and GCCs
**Say this first (1 line):** Dedupe to distinct (user, date) first, compute the island key `julianday(login_date) - ROW_NUMBER()` per user, keep users who have any island with `COUNT(*) >= N`, and look up their names in `accounts`; N is just the number in the `HAVING`.

**Schema and sample data:** five accounts and a `logins` table with duplicates, unsorted. Alice has 5 consecutive days (03-01 to 03-05) with 03-03 logged twice. Bob has exactly 4 distinct days (03-01 to 03-04) with 03-04 logged twice, so 5 rows. Carol has 5 days split by a gap (03-01 to 03-03, then 03-05 and 03-06). Dan has two long streaks (6 days, then 5 days). Eve has no logins. Id 6 has a 5-day streak but no row in `accounts`.
```sql
CREATE TABLE accounts(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO accounts VALUES (1,'Alice'),(2,'Bob'),(3,'Carol'),(4,'Dan'),(5,'Eve');
CREATE TABLE logins(id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-05'),(1,'2024-03-01'),(1,'2024-03-03'),(1,'2024-03-03'),(1,'2024-03-02'),(1,'2024-03-04'),
 (2,'2024-03-04'),(2,'2024-03-01'),(2,'2024-03-02'),(2,'2024-03-03'),(2,'2024-03-04'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-05'),(3,'2024-03-06'),
 (4,'2024-03-01'),(4,'2024-03-02'),(4,'2024-03-03'),(4,'2024-03-04'),(4,'2024-03-05'),(4,'2024-03-06'),
 (4,'2024-03-10'),(4,'2024-03-11'),(4,'2024-03-12'),(4,'2024-03-13'),(4,'2024-03-14'),
 (6,'2024-03-01'),(6,'2024-03-02'),(6,'2024-03-03'),(6,'2024-03-04'),(6,'2024-03-05');
```

**SQL answer:** `SQL_MAIN` in the Code block; the `?` is N (bound as 5 for the question, then 1 to 7 for the generalisation):
```sql
WITH d AS (
  SELECT DISTINCT id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
),
x AS (
  SELECT id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM d
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
ORDER BY a.id
```
It uses `IN` rather than a join so that a user with two qualifying streaks (Dan) appears once. `SQL_LAG` in the Code block is a second way that avoids islands: after distinct days, a user has N consecutive days if some row's date is exactly N-1 days after the date N-1 rows earlier, `LAG(login_date, N - 1)`. It also takes N as a bound parameter (SQLite accepted it as the `LAG` offset in my run) and matched the island version for every N from 1 to 7.

**pandas answer:** shown once, identical to the Code block (wrapped in a function of `n`):
```py
    d = logins.dropna(subset=["login_date"]).drop_duplicates()
    d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["id", "login_date"])
    d["key"] = d["login_date"] - pd.to_timedelta(d.groupby("id").cumcount() + 1, unit="D")
    sizes = d.groupby(["id", "key"]).size()
    ids = sizes[sizes >= n].index.get_level_values("id").unique()
    out = accounts[accounts["id"].isin(ids)].sort_values("id").reset_index(drop=True)
    
```

**Example (by hand):** N = 5.
- Alice: distinct days 03-01 to 03-05, five in a row: qualifies. The duplicate 03-03 row must not count as a sixth day.
- Bob: 03-01 to 03-04, four distinct days, one island of 4: does not qualify (a `COUNT(*)` over the five rows would say 5 and wrongly include him).
- Carol: islands of 3 and 2: no island reaches 5. Five distinct days in total is not five in a row.
- Dan: islands of 6 and 5: qualifies (once).
- Eve: no logins, no island. Id 6: 5-day island, but no account, so the join to `accounts` drops it.
- Result: Alice (1) and Dan (4), ordered by id.

**Code:** run with `python3 -I`. The assert compares SQL and pandas results as lists of `(id, name)` after sorting by `id`, for N from 1 to 7 (SQL `ORDER BY a.id`; pandas `sort_values("id")`).
```python
# Q9: users with a streak of at least N days (LeetCode 1454 pattern), duplicates in logins
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE accounts(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO accounts VALUES (1,'Alice'),(2,'Bob'),(3,'Carol'),(4,'Dan'),(5,'Eve');
CREATE TABLE logins(id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-05'),(1,'2024-03-01'),(1,'2024-03-03'),(1,'2024-03-03'),(1,'2024-03-02'),(1,'2024-03-04'),
 (2,'2024-03-04'),(2,'2024-03-01'),(2,'2024-03-02'),(2,'2024-03-03'),(2,'2024-03-04'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-05'),(3,'2024-03-06'),
 (4,'2024-03-01'),(4,'2024-03-02'),(4,'2024-03-03'),(4,'2024-03-04'),(4,'2024-03-05'),(4,'2024-03-06'),
 (4,'2024-03-10'),(4,'2024-03-11'),(4,'2024-03-12'),(4,'2024-03-13'),(4,'2024-03-14'),
 (6,'2024-03-01'),(6,'2024-03-02'),(6,'2024-03-03'),(6,'2024-03-04'),(6,'2024-03-05');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
),
x AS (
  SELECT id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM d
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
ORDER BY a.id
"""
SQL_JOIN_DUPES = """
WITH d AS (
  SELECT DISTINCT id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM d
),
s AS (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
SELECT a.id, a.name FROM accounts a JOIN s ON s.id = a.id ORDER BY a.id
"""
SQL_NO_DISTINCT = """
WITH x AS (
  SELECT id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM logins
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
ORDER BY a.id
"""
SQL_DENSE_COUNT_STAR = """
WITH x AS (
  SELECT id, login_date,
         julianday(login_date) - DENSE_RANK() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM logins
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
ORDER BY a.id
"""
SQL_LAG = """
WITH d AS (
  SELECT DISTINCT id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT id, login_date,
         LAG(login_date, ? - 1) OVER (PARTITION BY id ORDER BY login_date) AS back
  FROM d
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x WHERE julianday(login_date) - julianday(back) = ? - 1)
ORDER BY a.id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def pairs(df):
    return [(int(i), n) for i, n in zip(df["id"], df["name"])]

def rows(sql, *p):
    return pd.read_sql_query(sql, con, params=p)

sql_df = rows(SQL_MAIN, 5)
print("accounts with a streak of 5+ days:")
print(sql_df.to_string(index=False))
print("\nroster of streak lengths (distinct days) per user:")
print(pd.read_sql_query("""
WITH d AS (SELECT DISTINCT id, login_date FROM logins),
x AS (SELECT id, login_date, julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp FROM d)
SELECT id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days FROM x GROUP BY id, grp ORDER BY id, streak_start""", con).to_string(index=False))
print("\nwrong 1, ROW_NUMBER without DISTINCT:", rows(SQL_NO_DISTINCT, 5)["id"].tolist())
print("wrong 2, DENSE_RANK but COUNT(*):", rows(SQL_DENSE_COUNT_STAR, 5)["id"].tolist())
print("join instead of IN, Dan has two qualifying streaks:", rows(SQL_JOIN_DUPES, 5)["id"].tolist())

logins = pd.read_sql_query("SELECT * FROM logins", con)
accounts = pd.read_sql_query("SELECT * FROM accounts", con)
def pd_active(logins, accounts, n):
    # pd:main
    d = logins.dropna(subset=["login_date"]).drop_duplicates()
    d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["id", "login_date"])
    d["key"] = d["login_date"] - pd.to_timedelta(d.groupby("id").cumcount() + 1, unit="D")
    sizes = d.groupby(["id", "key"]).size()
    ids = sizes[sizes >= n].index.get_level_values("id").unique()
    out = accounts[accounts["id"].isin(ids)].sort_values("id").reset_index(drop=True)
    # pd:end
    return out
# compared after sorting by id
pd.testing.assert_frame_equal(pd_active(logins, accounts, 5), sql_df)
print("\npandas equals SQL for N=5: True")
for n in range(1, 8):
    a = rows(SQL_MAIN, n)
    b = pd_active(logins, accounts, n)
    c = rows(SQL_LAG, n, n)
    assert pairs(b) == pairs(a) == pairs(c)  # lists of (id, name); empty frames differ in dtype, so compare values
    print("N =", n, "-> ids", a["id"].tolist(), "(ROW_NUMBER, pandas and LAG(N-1) agree)")

# edge cases
con.execute("INSERT INTO logins VALUES (5, NULL)")
print("account with only a NULL date, N=1:", rows(SQL_MAIN, 1)["id"].tolist())
con.execute("DELETE FROM logins")
print("empty logins, N=5:", rows(SQL_MAIN, 5)["id"].tolist(), "| pandas rows:", len(pd_active(logins.iloc[0:0], accounts, 5)))
print("asserts passed")
```

**Output (my run):**
```text
accounts with a streak of 5+ days:
 id  name
  1 Alice
  4   Dan

roster of streak lengths (distinct days) per user:
 id streak_start streak_end  days
  1   2024-03-01 2024-03-05     5
  2   2024-03-01 2024-03-04     4
  3   2024-03-01 2024-03-03     3
  3   2024-03-05 2024-03-06     2
  4   2024-03-01 2024-03-06     6
  4   2024-03-10 2024-03-14     5
  6   2024-03-01 2024-03-05     5

wrong 1, ROW_NUMBER without DISTINCT: [4]
wrong 2, DENSE_RANK but COUNT(*): [1, 2, 4]
join instead of IN, Dan has two qualifying streaks: [1, 4, 4]

pandas equals SQL for N=5: True
N = 1 -> ids [1, 2, 3, 4] (ROW_NUMBER, pandas and LAG(N-1) agree)
N = 2 -> ids [1, 2, 3, 4] (ROW_NUMBER, pandas and LAG(N-1) agree)
N = 3 -> ids [1, 2, 3, 4] (ROW_NUMBER, pandas and LAG(N-1) agree)
N = 4 -> ids [1, 2, 4] (ROW_NUMBER, pandas and LAG(N-1) agree)
N = 5 -> ids [1, 4] (ROW_NUMBER, pandas and LAG(N-1) agree)
N = 6 -> ids [4] (ROW_NUMBER, pandas and LAG(N-1) agree)
N = 7 -> ids [] (ROW_NUMBER, pandas and LAG(N-1) agree)
account with only a NULL date, N=1: [1, 2, 3, 4]
empty logins, N=5: [] | pandas rows: 0
asserts passed
```

**Edge cases:**
- Exactly 4 days (Bob) is excluded and exactly 5 (Alice, and Dan's second streak) is included, so the threshold is `>= N`, not `> N`. N = 4 added Bob, N = 6 left only Dan, N = 7 returned nothing (all in the output).
- 5 days split by a gap (Carol): excluded, because the key changes at the gap (a step of exactly 2 days).
- Why `DISTINCT` before ranking: `ROW_NUMBER` on the duplicated rows split Alice's run at the second 03-03 and dropped her (the wrong list printed `[4]`, only Dan). `DENSE_RANK` with `COUNT(*)` fixed the split but counted Bob's duplicate row as a fifth day and wrongly included him (`[1, 2, 4]`). Dedupe first, then count distinct days (see Q8).
- Join instead of `IN`: Dan appeared twice (`[1, 4, 4]`) because he has two qualifying islands. Use `IN`/`EXISTS` or `DISTINCT`.
- Users with no account row: id 6 is dropped by the lookup in `accounts`. Whether that is correct depends on the product; the LeetCode problem returns names, so it needs the join.
- NULL date: an account with only a NULL date had no islands (the output shows N=1 unchanged), because the NULL is filtered.
- Single-row groups: Eve and a one-day user only appear for N = 1.
- Unsorted input: handled by the window order and the pandas sort.
- Empty `logins`: zero rows in SQL, zero in pandas.

**Then explain:**
- Generalising: only the number in `HAVING COUNT(*) >= ?` changes; the islands are the same for any N. That is the advantage over N-1 self joins.
- The `LAG(login_date, N - 1)` form answers "does a window of N days exist", which is faster to write but cannot report the streak itself.
- As I remember LeetCode 1454 (the page is premium and was not opened), the output is id and name ordered by id, and logins can have duplicates, which is why the dedupe step matters.
- Dialects (not executed here): the bound `?` placeholder style differs by driver (`%s`, `$1`, `@n`); a `LAG` offset that is a parameter may not be allowed in every engine, so use a literal there.

**Follow-ups:**
- *Active for N consecutive days ending today?* That is the current-streak question (Q15).
- *How many distinct streaks of at least N?* `COUNT(*)` of the qualifying islands per user.
- *Activity within a rolling window instead of strict consecutive days?* A different metric (Part 8).

**Common mistakes:**
- Not removing duplicate rows before numbering, or counting rows instead of distinct days.
- A join that duplicates users with several qualifying streaks.
- Treating "5 days in total" as "5 days in a row".
- Using `> N` instead of `>= N`.
- Forgetting that a user can have logins but no account row (or the reverse).

### Q10 ⭐⭐⭐ 🟡 Human Traffic of Stadium (LeetCode 601): stadium(id, visit_date, people) with id increasing with visit_date. Return all rows that belong to three or more consecutive ids each with people >= 100, ordered by visit_date. Solve with the id minus ROW_NUMBER over the filtered rows (islands among the qualifying rows), with a three-way self join, and with LAG/LEAD windows; explain why the island method needs the filter before ROW_NUMBER and why the join method must not double count a run of four rows.
**Asked at:** public LeetCode-style problem bank (statements known from search snippets and mirrors such as doocs, walkccc and talentd; the leetcode.com pages returned HTTP 403 and were not opened), not candidate reports; analyst, data scientist and data engineer screens at product companies and GCCs
**Say this first (1 line):** Filter to the rows with `people >= 100` first, then compute `id - ROW_NUMBER() OVER (ORDER BY id)` on those rows only, so every run of consecutive ids shares one key; keep the rows whose run has at least three members.

**Schema and sample data:** thirteen days, inserted out of order, with `id` increasing with `visit_date` and one date skipped (no 2017-01-08). Rows with 100 or more people: ids 2-3 (a run of 2), ids 5-8 (a run of four), ids 10-12 (exactly 100 each, a run of exactly 3, at the threshold). Ids 1, 4, 9, 13 are below 100.
```sql
CREATE TABLE stadium(id INTEGER PRIMARY KEY, visit_date TEXT, people INTEGER);
INSERT INTO stadium VALUES
 (5,'2017-01-05',145),(1,'2017-01-01',10),(2,'2017-01-02',109),(3,'2017-01-03',150),(4,'2017-01-04',99),
 (6,'2017-01-06',1455),(7,'2017-01-07',199),(8,'2017-01-09',188),(9,'2017-01-10',99),
 (10,'2017-01-11',100),(11,'2017-01-12',100),(12,'2017-01-13',100),(13,'2017-01-14',99);
```

**SQL answer:** island method, `SQL_ISLAND` in the Code block. A window `COUNT(*) OVER (PARTITION BY grp)` gives each row its run length, so no join back is needed:
```sql
WITH q AS (
  SELECT id, visit_date, people,
         id - ROW_NUMBER() OVER (ORDER BY id) AS grp
  FROM stadium
  WHERE people >= 100
),
r AS (
  SELECT id, visit_date, people,
         COUNT(*) OVER (PARTITION BY grp) AS run_len
  FROM q
)
SELECT id, visit_date, people
FROM r
WHERE run_len >= 3
ORDER BY visit_date, id
```
Three-way self join (`SQL_JOIN`): find every triple of ids `a, a+1, a+2` that all qualify, then return the rows that belong to any triple. `DISTINCT` is needed:
```sql
SELECT DISTINCT t.id, t.visit_date, t.people
FROM stadium a
JOIN stadium b ON b.id = a.id + 1
JOIN stadium c ON c.id = a.id + 2
JOIN stadium t ON t.id IN (a.id, b.id, c.id)
WHERE a.people >= 100 AND b.people >= 100 AND c.people >= 100
ORDER BY t.visit_date, t.id
```
LAG/LEAD windows (`SQL_WINDOW`): a qualifying row is in a run of 3 if it is the last, middle or first of three qualifying neighbours:
```sql
WITH x AS (
  SELECT id, visit_date, people,
         LAG(people, 2)  OVER (ORDER BY id) AS b2,
         LAG(people, 1)  OVER (ORDER BY id) AS b1,
         LEAD(people, 1) OVER (ORDER BY id) AS f1,
         LEAD(people, 2) OVER (ORDER BY id) AS f2
  FROM stadium
)
SELECT id, visit_date, people
FROM x
WHERE people >= 100
  AND ( (b1 >= 100 AND b2 >= 100)
     OR (b1 >= 100 AND f1 >= 100)
     OR (f1 >= 100 AND f2 >= 100) )
ORDER BY visit_date, id
```
All three returned the same seven rows. `SQL_FILTER_AFTER` in the Code block is the wrong island order (filter after numbering).

**pandas answer:** shown once, identical to the Code block (wrapped in a function). The `respect_ids` branch breaks a run where the id step is not 1; `people` NaN compares as False:
```py
    s = stadium.sort_values("id")
    ok = s["people"] >= 100
    key = (ok != ok.shift()).cumsum()
    if respect_ids:
        key = key + (s["id"].diff() != 1).cumsum()
    run_len = ok.groupby(key).transform("size")
    out = s[ok & (run_len >= 3)].sort_values(["visit_date", "id"]).reset_index(drop=True)
    
```

**Example (by hand):** sorted by id, qualifying (people >= 100): ids 2, 3, 5, 6, 7, 8, 10, 11, 12 (ids 1, 4, 9, 13 fail).
- Row numbers among the qualifying rows: 1..9.
- `id - row number`: 1, 1, 2, 2, 2, 2, 4, 4, 4.
- Groups: key 1 = ids 2-3 (size 2, dropped), key 2 = ids 5-8 (size 4, kept), key 4 = ids 10-12 (size 3, kept).
- Result: ids 5, 6, 7, 8, 10, 11, 12, ordered by visit_date (2017-01-05 to 01-07, 01-09, 01-11 to 01-13). The skipped date 01-08 does not matter, because the runs are by id; id 8 follows id 7 although the date skips a day.

**Code:** run with `python3 -I`. The asserts compare SQL and pandas frames sorted by `visit_date, id` (the SQL has `ORDER BY visit_date, id`).
```python
# Q10: Human Traffic of Stadium (LeetCode 601 pattern): island, three-way self join, LAG/LEAD
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE stadium(id INTEGER PRIMARY KEY, visit_date TEXT, people INTEGER);
INSERT INTO stadium VALUES
 (5,'2017-01-05',145),(1,'2017-01-01',10),(2,'2017-01-02',109),(3,'2017-01-03',150),(4,'2017-01-04',99),
 (6,'2017-01-06',1455),(7,'2017-01-07',199),(8,'2017-01-09',188),(9,'2017-01-10',99),
 (10,'2017-01-11',100),(11,'2017-01-12',100),(12,'2017-01-13',100),(13,'2017-01-14',99);
"""
SQL_ISLAND = """
WITH q AS (
  SELECT id, visit_date, people,
         id - ROW_NUMBER() OVER (ORDER BY id) AS grp
  FROM stadium
  WHERE people >= 100
),
r AS (
  SELECT id, visit_date, people,
         COUNT(*) OVER (PARTITION BY grp) AS run_len
  FROM q
)
SELECT id, visit_date, people
FROM r
WHERE run_len >= 3
ORDER BY visit_date, id
"""
SQL_FILTER_AFTER = """
WITH q AS (
  SELECT id, visit_date, people,
         id - ROW_NUMBER() OVER (ORDER BY id) AS grp
  FROM stadium
),
r AS (
  SELECT id, visit_date, people,
         COUNT(*) OVER (PARTITION BY grp) AS run_len
  FROM q
  WHERE people >= 100
)
SELECT id, visit_date, people
FROM r
WHERE run_len >= 3
ORDER BY visit_date, id
"""
SQL_JOIN = """
SELECT DISTINCT t.id, t.visit_date, t.people
FROM stadium a
JOIN stadium b ON b.id = a.id + 1
JOIN stadium c ON c.id = a.id + 2
JOIN stadium t ON t.id IN (a.id, b.id, c.id)
WHERE a.people >= 100 AND b.people >= 100 AND c.people >= 100
ORDER BY t.visit_date, t.id
"""
SQL_JOIN_NO_DISTINCT = SQL_JOIN.replace("SELECT DISTINCT", "SELECT")
SQL_WINDOW = """
WITH x AS (
  SELECT id, visit_date, people,
         LAG(people, 2)  OVER (ORDER BY id) AS b2,
         LAG(people, 1)  OVER (ORDER BY id) AS b1,
         LEAD(people, 1) OVER (ORDER BY id) AS f1,
         LEAD(people, 2) OVER (ORDER BY id) AS f2
  FROM stadium
)
SELECT id, visit_date, people
FROM x
WHERE people >= 100
  AND ( (b1 >= 100 AND b2 >= 100)
     OR (b1 >= 100 AND f1 >= 100)
     OR (f1 >= 100 AND f2 >= 100) )
ORDER BY visit_date, id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda sql: pd.read_sql_query(sql, con)
isl = q(SQL_ISLAND)
print("island method:"); print(isl.to_string(index=False))
jn, win = q(SQL_JOIN), q(SQL_WINDOW)
pd.testing.assert_frame_equal(jn, isl)
pd.testing.assert_frame_equal(win, isl)
print("\nself join and LAG/LEAD equal the island result: True")
print("join rows with DISTINCT:", len(jn), "| without DISTINCT:", len(q(SQL_JOIN_NO_DISTINCT)),
      "(ids 5-8 are a run of four: two triples share rows)")
print("island with the filter AFTER ROW_NUMBER (wrong):", q(SQL_FILTER_AFTER)["id"].tolist())

stadium = pd.read_sql_query("SELECT * FROM stadium", con)
def pd_traffic(stadium, respect_ids=False):
    # pd:main
    s = stadium.sort_values("id")
    ok = s["people"] >= 100
    key = (ok != ok.shift()).cumsum()
    if respect_ids:
        key = key + (s["id"].diff() != 1).cumsum()
    run_len = ok.groupby(key).transform("size")
    out = s[ok & (run_len >= 3)].sort_values(["visit_date", "id"]).reset_index(drop=True)
    # pd:end
    return out
# compared after sorting by visit_date, id
pd.testing.assert_frame_equal(pd_traffic(stadium), isl)
print("pandas equals SQL: True | ids:", pd_traffic(stadium)["id"].tolist())

# NULL people inside a run: unknown is not >= 100, so the run breaks
con.execute("CREATE TABLE s2 AS SELECT * FROM stadium")
con.execute("UPDATE s2 SET people = NULL WHERE id = 6")
sub = lambda sql: sql.replace("FROM stadium", "FROM s2").replace("JOIN stadium", "JOIN s2")
nul = q(sub(SQL_ISLAND))
print("\nNULL people at id 6, island:", nul["id"].tolist())
pd.testing.assert_frame_equal(q(sub(SQL_JOIN)), nul)
pd.testing.assert_frame_equal(q(sub(SQL_WINDOW)), nul)
s2 = pd.read_sql_query("SELECT * FROM s2", con)
print("pandas people dtype with a NULL:", s2["people"].dtype)
pd.testing.assert_frame_equal(pd_traffic(s2).astype({"people": "int64"}), nul)
print("NULL case: join, window and pandas agree with island: True (ids 5,7,8 do not form a run of 3)")

# gap in ids: delete id 6, so 5,7,8 are positionally adjacent but ids 5,7,8 are not consecutive
con.execute("CREATE TABLE s3 AS SELECT * FROM stadium WHERE id <> 6")
sub3 = lambda sql: sql.replace("FROM stadium", "FROM s3").replace("JOIN stadium", "JOIN s3")
s3 = pd.read_sql_query("SELECT * FROM s3", con)
print("\nid 6 deleted:")
print("  island (id arithmetic):", q(sub3(SQL_ISLAND))["id"].tolist(), "| self join:", q(sub3(SQL_JOIN))["id"].tolist())
print("  LAG/LEAD (positional):", q(sub3(SQL_WINDOW))["id"].tolist(), "| pandas positional:", pd_traffic(s3)["id"].tolist(),
      "| pandas respecting ids:", pd_traffic(s3, respect_ids=True)["id"].tolist())
assert q(sub3(SQL_ISLAND))["id"].tolist() == q(sub3(SQL_JOIN))["id"].tolist() == pd_traffic(s3, respect_ids=True)["id"].tolist()
assert q(sub3(SQL_WINDOW))["id"].tolist() == pd_traffic(s3)["id"].tolist()

# duplicate visit_date: ordering by visit_date alone would tie, so id is the tie-breaker
con.execute("CREATE TABLE s4 AS SELECT * FROM stadium")
con.execute("UPDATE s4 SET visit_date = '2017-01-06' WHERE id IN (5, 6, 7)")
sub4 = lambda sql: sql.replace("FROM stadium", "FROM s4").replace("JOIN stadium", "JOIN s4")
print("\nsame date 2017-01-06 on ids 5, 6, 7, ordered by visit_date, id:", q(sub4(SQL_ISLAND))["id"].tolist())

# single row and empty
con.execute("DELETE FROM s3")
con.execute("INSERT INTO s3 VALUES (1, '2017-01-01', 500)")
print("single qualifying row:", q(sub3(SQL_ISLAND))["id"].tolist())
con.execute("DELETE FROM s3")
print("empty table:", q(sub3(SQL_ISLAND))["id"].tolist())
print("asserts passed")
```

**Output (my run):**
```text
island method:
 id visit_date  people
  5 2017-01-05     145
  6 2017-01-06    1455
  7 2017-01-07     199
  8 2017-01-09     188
 10 2017-01-11     100
 11 2017-01-12     100
 12 2017-01-13     100

self join and LAG/LEAD equal the island result: True
join rows with DISTINCT: 7 | without DISTINCT: 9 (ids 5-8 are a run of four: two triples share rows)
island with the filter AFTER ROW_NUMBER (wrong): [2, 3, 5, 6, 7, 8, 10, 11, 12]
pandas equals SQL: True | ids: [5, 6, 7, 8, 10, 11, 12]

NULL people at id 6, island: [10, 11, 12]
pandas people dtype with a NULL: float64
NULL case: join, window and pandas agree with island: True (ids 5,7,8 do not form a run of 3)

id 6 deleted:
  island (id arithmetic): [10, 11, 12] | self join: [10, 11, 12]
  LAG/LEAD (positional): [5, 7, 8, 10, 11, 12] | pandas positional: [5, 7, 8, 10, 11, 12] | pandas respecting ids: [10, 11, 12]

same date 2017-01-06 on ids 5, 6, 7, ordered by visit_date, id: [5, 6, 7, 8, 10, 11, 12]
single qualifying row: []
empty table: []
asserts passed
```

**Edge cases:**
- Why the filter must come before `ROW_NUMBER`: ids are consecutive, so `id - ROW_NUMBER() OVER (ORDER BY id)` over all rows is the same for every row (a constant), so every row is "one run". Filtering afterwards then keeps any row with `people >= 100` whose "run" (the whole table) is long, which returned ids 2, 3, 5, 6, 7, 8, 10, 11, 12, including the two-row run 2-3 (printed in the output). Filtering first removes the failing rows, which makes the key jump at each break.
- Why the join must not double count: a run of four rows (ids 5-8) contains two triples (5,6,7) and (6,7,8) that share rows 6 and 7. Without `DISTINCT` the join returned 9 rows instead of 7. Same for any run longer than 3.
- Exactly at the threshold: 100 counts (`>=`), so ids 10-12 with exactly 100 qualify; 99 breaks the run (ids 9 and 13).
- NULL people: `NULL >= 100` is unknown, so the row does not qualify and it breaks the run. With id 6 set to NULL, only ids 10-12 remained, in all three SQL versions and pandas. In pandas the NULL turned `people` into `float64` (printed), so the comparison with SQL needed an integer cast (the NaN rows are filtered out, so the cast is safe).
- Gaps in ids: the question says `id` increases with date; if an id is missing, id-based methods and positional methods disagree. With id 6 deleted, the island and self-join versions returned only 10-12 (ids 5, 7, 8 are not consecutive ids), while LAG/LEAD and pandas positional returned 5, 7, 8, 10, 11, 12. pandas with the id-step break matched the id-based SQL. State which you mean; LeetCode's statement assumes consecutive ids, as I remember it (not opened).
- Duplicate dates: `ORDER BY visit_date` alone has ties when several rows share a date; add `id` as a tie-breaker (ids 5-7 sharing a date still returned in id order).
- Unsorted input: handled by the window orders and the pandas `sort_values("id")`.
- Single qualifying row and empty table: no output.

**Then explain:**
- A run of at least three among qualifying rows is a "gaps and islands" problem; the filter turns "not qualifying" rows into gaps.
- The island method gives the run size directly, so `>= N` is one number to change; the join needs N joins and the LAG/LEAD form needs (2N-1) shifted columns.
- The `COUNT(*) OVER (PARTITION BY grp)` window avoids a second join back to the table; the other common form is `GROUP BY grp HAVING COUNT(*) >= 3` and a join or `IN`.
- Dialects (not executed here): as I remember the problem it is written for MySQL; MySQL 5.7 has no window functions, so only the self join works there. MySQL 8, PostgreSQL, BigQuery and Snowflake support the window forms; PostgreSQL could also use `FILTER` or boolean casts, which I did not run.

**Follow-ups:**
- *Runs of at least N?* Change 3 to N in the island method.
- *Return one row per run (start date, end date, total people)?* `GROUP BY grp HAVING COUNT(*) >= 3` with `MIN`, `MAX`, `SUM`.
- *What if dates, not ids, must be consecutive?* Use `julianday(visit_date) - ROW_NUMBER()` as in Q6.

**Common mistakes:**
- Numbering all rows before filtering.
- A self join without `DISTINCT` (duplicates for runs longer than three), or only checking one position of the triple so the first or last rows of a run are lost.
- Using `>` instead of `>=` at the threshold.
- Ordering by `visit_date` without a tie-breaker.
- Assuming ids have no gaps without saying so.

### Q11 ⭐⭐⭐ 🟡 Sessionization with a 30 minute timeout: events(user_id, event_ts, event_name) with ISO timestamps. Assign a session id per user with LAG(event_ts) to get the previous event time, a CASE flag for a new session (first event, or gap of more than 30 minutes) and a running SUM of the flag over (PARTITION BY user_id ORDER BY event_ts). Return session_id, session_start, session_end, event count and duration in minutes per session. Use julianday differences times 1440 in SQLite and explain why unixepoch differences are safer.
**Asked at:** Dataiku sessionization tutorial (opened; vendor tutorial, uses a 30 minute timeout with >= and no tie handling) plus search snippets of Cube, DevGenius and LinkedIn sessionization posts (not opened); guides and not candidate reports; product analytics and data scientist rounds
**Say this first (1 line):** Order each user's events by time, use `LAG` to get the previous event time, flag a row as a new session when it is the user's first event or the gap is over 30 minutes, then a running `SUM` of the flag per user is the session number; I assume "more than 30 minutes" starts a new session (exactly 30 stays in), and I measure gaps with `unixepoch`, not `julianday * 1440`.

**Schema and sample data:** twelve event rows, three users, loaded out of time order on purpose (event 12 is 09:05 for user 1 but has the highest id). User 1 has a gap of exactly 30 minutes (09:10 to 09:40). User 2 has a single event. User 3 crosses midnight and has a gap of 31 minutes (00:10 to 00:41). Event 11 has a NULL timestamp. Timestamps are ISO text `YYYY-MM-DD HH:MM:SS`, no time zone.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 1,'2024-03-01 09:00:00','open'),
 (2, 1,'2024-03-01 09:10:00','search'),
 (3, 1,'2024-03-01 09:40:00','click'),
 (4, 1,'2024-03-01 09:41:00','click'),
 (5, 1,'2024-03-01 11:00:00','open'),
 (6, 1,'2024-03-01 11:05:00','buy'),
 (7, 2,'2024-03-01 10:00:00','open'),
 (8, 3,'2024-03-01 23:50:00','open'),
 (9, 3,'2024-03-02 00:10:00','click'),
 (10,3,'2024-03-02 00:41:00','click'),
 (11,3,NULL,'ghost'),
 (12,1,'2024-03-01 09:05:00','click');
```

**SQL answer:** `SQL_MAIN` in the Code block, the `>` convention (a gap of exactly 30 minutes stays in the same session):
```sql
WITH e AS (
  SELECT user_id, event_id, event_ts,
         LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_ts
  FROM events
  WHERE event_ts IS NOT NULL
), f AS (
  SELECT user_id, event_id, event_ts,
         CASE WHEN prev_ts IS NULL
                OR (unixepoch(event_ts) - unixepoch(prev_ts)) / 60.0 > 30
              THEN 1 ELSE 0 END AS new_session
  FROM e
), s AS (
  SELECT user_id, event_id, event_ts,
         SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS session_id
  FROM f
)
SELECT user_id, session_id,
       MIN(event_ts) AS session_start,
       MAX(event_ts) AS session_end,
       COUNT(*) AS events,
       (unixepoch(MAX(event_ts)) - unixepoch(MIN(event_ts))) / 60.0 AS duration_min
FROM s
GROUP BY user_id, session_id
ORDER BY user_id, session_id
```
The `>=` convention is the same query with `>= 30` (`SQL_GE` in the Code block). Both are printed. Assumption I state out loud: gap more than 30 minutes starts a new session, so exactly 30 minutes is still the same session. The Dataiku tutorial (opened) uses `>=`; sources differ, so in an interview I ask which one the product uses.

**pandas answer:** the same logic as a function, shown once here and identical to the Code block (`strict=True` is the `>` convention, `strict=False` is `>=`):
```py
    e = events.dropna(subset=["event_ts"]).copy()
    e["event_ts"] = pd.to_datetime(e["event_ts"])
    e = e.sort_values(["user_id", "event_ts", "event_id"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    new = gap.isna() | ((gap > limit) if strict else (gap >= limit))
    e["session_id"] = new.astype(int).groupby(e["user_id"]).cumsum()
    out = (e.groupby(["user_id", "session_id"], as_index=False)
             .agg(session_start=("event_ts", "min"), session_end=("event_ts", "max"),
                  events=("event_id", "size")))
    out["duration_min"] = (out["session_end"] - out["session_start"]).dt.total_seconds() / 60.0
    
```

**Example:** user 1 sorted by time: 09:00, 09:05, 09:10, 09:40, 09:41, 11:00, 11:05.
- Gaps to the previous event: first row (no previous), 5, 5, 30, 1, 79, 5 minutes.
- Under `>`: flags 1,0,0,0,0,1,0 so running sums 1,1,1,1,1,2,2. Session 1 is 09:00 to 09:41 (5 events, 41 minutes), session 2 is 11:00 to 11:05 (2 events, 5 minutes).
- Under `>=`: the 30 minute gap also flags, so flags 1,0,0,1,0,1,0. Session 1 is 09:00 to 09:10 (3 events), session 2 is 09:40 to 09:41 (2 events), session 3 is 11:00 to 11:05. One boundary decides whether user 1 has 2 or 3 sessions.
- User 2: one event, flag 1, one session of 0 minutes. User 3: 23:50 to 00:10 is 20 minutes across midnight, still one session (a date-based session would split it); 00:41 is 31 minutes later, a new session under both conventions.
- Totals: 5 sessions under `>`, 6 under `>=`. The NULL event is dropped by `WHERE event_ts IS NOT NULL`.

**Code:** run with `python3 -I`. The asserts compare SQL and pandas for both conventions after ordering by `user_id, session_id`; durations are floats so the comparison is on values, not dtypes.
```python
# Q11: sessionization with a 30 minute timeout: LAG + CASE flag + running SUM, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 1,'2024-03-01 09:00:00','open'),
 (2, 1,'2024-03-01 09:10:00','search'),
 (3, 1,'2024-03-01 09:40:00','click'),
 (4, 1,'2024-03-01 09:41:00','click'),
 (5, 1,'2024-03-01 11:00:00','open'),
 (6, 1,'2024-03-01 11:05:00','buy'),
 (7, 2,'2024-03-01 10:00:00','open'),
 (8, 3,'2024-03-01 23:50:00','open'),
 (9, 3,'2024-03-02 00:10:00','click'),
 (10,3,'2024-03-02 00:41:00','click'),
 (11,3,NULL,'ghost'),
 (12,1,'2024-03-01 09:05:00','click');
"""
SQL_MAIN = """
WITH e AS (
  SELECT user_id, event_id, event_ts,
         LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_ts
  FROM events
  WHERE event_ts IS NOT NULL
), f AS (
  SELECT user_id, event_id, event_ts,
         CASE WHEN prev_ts IS NULL
                OR (unixepoch(event_ts) - unixepoch(prev_ts)) / 60.0 > 30
              THEN 1 ELSE 0 END AS new_session
  FROM e
), s AS (
  SELECT user_id, event_id, event_ts,
         SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS session_id
  FROM f
)
SELECT user_id, session_id,
       MIN(event_ts) AS session_start,
       MAX(event_ts) AS session_end,
       COUNT(*) AS events,
       (unixepoch(MAX(event_ts)) - unixepoch(MIN(event_ts))) / 60.0 AS duration_min
FROM s
GROUP BY user_id, session_id
ORDER BY user_id, session_id
"""
SQL_GE = SQL_MAIN.replace("/ 60.0 > 30", "/ 60.0 >= 30")
assert SQL_GE != SQL_MAIN
SQL_JULIAN = SQL_MAIN.replace("(unixepoch(event_ts) - unixepoch(prev_ts)) / 60.0", "(julianday(event_ts) - julianday(prev_ts)) * 1440")
assert SQL_JULIAN != SQL_MAIN

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_gt = pd.read_sql_query(SQL_MAIN, con)
sql_ge = pd.read_sql_query(SQL_GE, con)
print("SQL, new session when gap > 30 minutes (assumed):")
print(sql_gt.to_string(index=False))
print("SQL, new session when gap >= 30 minutes:")
print(sql_ge.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)

def sessionize(events, strict=True, limit=pd.Timedelta(minutes=30)):
    # pd:main
    e = events.dropna(subset=["event_ts"]).copy()
    e["event_ts"] = pd.to_datetime(e["event_ts"])
    e = e.sort_values(["user_id", "event_ts", "event_id"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    new = gap.isna() | ((gap > limit) if strict else (gap >= limit))
    e["session_id"] = new.astype(int).groupby(e["user_id"]).cumsum()
    out = (e.groupby(["user_id", "session_id"], as_index=False)
             .agg(session_start=("event_ts", "min"), session_end=("event_ts", "max"),
                  events=("event_id", "size")))
    out["duration_min"] = (out["session_end"] - out["session_start"]).dt.total_seconds() / 60.0
    # pd:end
    for c in ("session_start", "session_end"):
        out[c] = out[c].dt.strftime("%Y-%m-%d %H:%M:%S")
    return out

pd_gt = sessionize(events, strict=True)
pd_ge = sessionize(events, strict=False)
cols = ["user_id", "session_id", "session_start", "session_end", "events", "duration_min"]
# compare after sorting by user_id, session_id (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_gt[cols].reset_index(drop=True), sql_gt[cols], check_dtype=False)
pd.testing.assert_frame_equal(pd_ge[cols].reset_index(drop=True), sql_ge[cols], check_dtype=False)
print("sessions: gap > 30 ->", len(sql_gt), "; gap >= 30 ->", len(sql_ge))

# julianday vs unixepoch on exactly 30 minute gaps
con.executescript("CREATE TABLE pairs(a TEXT, b TEXT);"
                  "INSERT INTO pairs VALUES ('2024-03-01 09:10:00','2024-03-01 09:40:00'),"
                  "('2024-03-01 23:50:00','2024-03-02 00:20:00'),('2024-03-01 09:00:00','2024-03-01 09:30:00');")
print(pd.read_sql_query(
    "SELECT a, b, printf('%.9f', (julianday(b) - julianday(a)) * 1440) AS julian_min, "
    "(julianday(b) - julianday(a)) * 1440 > 30 AS julian_gt_30, "
    "(unixepoch(b) - unixepoch(a)) / 60.0 AS unix_min, "
    "(unixepoch(b) - unixepoch(a)) / 60.0 > 30 AS unix_gt_30 FROM pairs", con).to_string(index=False))
julian = pd.read_sql_query(SQL_JULIAN, con)
print("julianday version, gap > 30: sessions =", len(julian), "(unixepoch version:", len(sql_gt), ")")
print(julian[["user_id", "session_id", "events", "duration_min"]].to_string(index=False))

# scale check: 20000 pairs that are exactly 30 minutes apart
import datetime as dt
base = dt.datetime(2024, 1, 1)
rows = []
for i in range(20000):
    a = base + dt.timedelta(minutes=7 * i + 3, seconds=i % 60)
    rows.append((a.strftime("%Y-%m-%d %H:%M:%S"), (a + dt.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")))
con.execute("CREATE TABLE big(a TEXT, b TEXT)")
con.executemany("INSERT INTO big VALUES (?, ?)", rows)
print(con.execute("SELECT COUNT(*), SUM((julianday(b)-julianday(a))*1440 > 30), "
                  "SUM((julianday(b)-julianday(a))*1440 = 30), "
                  "SUM(unixepoch(b)-unixepoch(a) = 1800) FROM big").fetchone(),
      "<- rows, julianday > 30, julianday = 30, unixepoch = 1800")
print("asserts passed")
```

**Output (my run):**
```text
SQL, new session when gap > 30 minutes (assumed):
 user_id  session_id       session_start         session_end  events  duration_min
       1           1 2024-03-01 09:00:00 2024-03-01 09:41:00       5          41.0
       1           2 2024-03-01 11:00:00 2024-03-01 11:05:00       2           5.0
       2           1 2024-03-01 10:00:00 2024-03-01 10:00:00       1           0.0
       3           1 2024-03-01 23:50:00 2024-03-02 00:10:00       2          20.0
       3           2 2024-03-02 00:41:00 2024-03-02 00:41:00       1           0.0
SQL, new session when gap >= 30 minutes:
 user_id  session_id       session_start         session_end  events  duration_min
       1           1 2024-03-01 09:00:00 2024-03-01 09:10:00       3          10.0
       1           2 2024-03-01 09:40:00 2024-03-01 09:41:00       2           1.0
       1           3 2024-03-01 11:00:00 2024-03-01 11:05:00       2           5.0
       2           1 2024-03-01 10:00:00 2024-03-01 10:00:00       1           0.0
       3           1 2024-03-01 23:50:00 2024-03-02 00:10:00       2          20.0
       3           2 2024-03-02 00:41:00 2024-03-02 00:41:00       1           0.0
sessions: gap > 30 -> 5 ; gap >= 30 -> 6
                  a                   b   julian_min  julian_gt_30  unix_min  unix_gt_30
2024-03-01 09:10:00 2024-03-01 09:40:00 30.000000224             1      30.0           0
2024-03-01 23:50:00 2024-03-02 00:20:00 30.000000224             1      30.0           0
2024-03-01 09:00:00 2024-03-01 09:30:00 30.000000224             1      30.0           0
julianday version, gap > 30: sessions = 6 (unixepoch version: 5 )
 user_id  session_id  events  duration_min
       1           1       3          10.0
       1           2       2           1.0
       1           3       2           5.0
       2           1       1           0.0
       3           1       2          20.0
       3           2       1           0.0
(20000, 13333, 0, 20000) <- rows, julianday > 30, julianday = 30, unixepoch = 1800
asserts passed
```

**Edge cases:**
- Exactly 30 minutes: 5 sessions under `>` and 6 under `>=` in my run. This is the one thing to confirm with the interviewer.
- `julianday` precision, run on this machine (SQLite 3.45.1): for the pair 09:10:00 and 09:40:00, `(julianday(b) - julianday(a)) * 1440` is `30.000000224`, so `> 30` is true and the julianday version wrongly started a new session (6 sessions instead of 5 under the `>` rule). Over 20000 pairs that were exactly 30 minutes apart, none came out as exactly 30 and 13333 were above 30. `unixepoch` differences were exactly 1800 seconds in all 20000. The cause is that `julianday` is a floating-point number of days with only about millisecond resolution at today's day numbers; this is why I use `unixepoch` (integer seconds) for thresholds, and why a julianday comparison needs `ROUND(..., 3)` at least.
- Unsorted input: the window `ORDER BY` fixes it; no pre-sort is needed. In pandas the sort is explicit.
- Single-event user: `prev_ts` is NULL, flag 1, one session with duration 0.
- NULL timestamp: filtered out first. Without the filter, `ORDER BY event_ts` puts NULLs first in SQLite and the NULL row would open a fake session; in pandas, `NaT` sorts last and `diff` gives `NaT`, which also reads as a new session.
- Midnight crossing is fine because the gap uses full timestamps, not dates.
- Duplicate timestamps: the `event_id` tie-breaker in both window clauses is explained in Q12.
- Duration here is last event minus first event, so a one-event session has duration 0; products that add a timeout tail or a minimum duration say so explicitly.

**Then explain:**
- Three steps: `LAG` to see the previous event (partitioned by user so the first event of a user has NULL), `CASE` to flag session starts, running `SUM` of the flag to number the sessions per user. Then group by user and session number for start, end, count and duration.
- `session_id` is only unique within a user; group by `(user_id, session_id)`, or build a global key such as `user_id || '-' || session_id`.
- The `OVER (PARTITION BY user_id ORDER BY ...)` running sum uses the default frame (`RANGE ... CURRENT ROW`); with the tie-breaker in the `ORDER BY` there are no peers, so it behaves like a row-by-row running total (running-total mechanics are Part 5).
- Why `unixepoch` is safer: it gives integer seconds, so a threshold of 1800 seconds is exact; `julianday` is a float and an exact 30 minute gap lands slightly above 30. `unixepoch()` is available from SQLite 3.38, and the sample runs on 3.45.1.
- pandas mapping: `groupby("user_id")["event_ts"].diff()` is `LAG`, `gap.isna() | (gap > limit)` is the flag (`isna` is the first-row case), `groupby().cumsum()` is the running `SUM`.
- Dialects, not executed here: PostgreSQL would use `event_ts - prev_ts > INTERVAL '30 minutes'` (or `EXTRACT(EPOCH FROM ...)`), MySQL `TIMESTAMPDIFF(MINUTE, prev_ts, event_ts) > 30` (note it counts whole minutes, so 30 min 59 s is 30), BigQuery `TIMESTAMP_DIFF(event_ts, prev_ts, SECOND)`. I did not run any of these.

**Follow-ups:**
- Which user-visible number changes with `>` versus `>=`? Session count and every duration near the boundary (here 5 versus 6 sessions).
- How do you also attach the session number to each event row? Keep the `s` CTE output and join or select from it; the grouped query is a summary of it.
- Sessions longer than a day or a hard cap (for example "also split after 4 hours")? That needs a second condition on the session start, which a plain running `SUM` cannot do; it needs a recursive CTE (pointer to Part 9).

**Common mistakes:**
- Flagging with `julianday(...) * 1440 > 30` and getting a spurious session at exactly 30 minutes (shown above).
- Forgetting `PARTITION BY user_id` in `LAG` or in the running `SUM`, so one user's last event is another user's previous event.
- Not flagging the first event (NULL gap compares as NULL, so the flag falls to ELSE 0 and the first session gets number 0 or merges with the wrong group).
- Grouping by `session_id` alone and merging different users' sessions.
- Using the date instead of a timestamp, which splits a session at midnight.
- Not saying which of `>` and `>=` was assumed.

### Q12 ⭐⭐⭐ 🟡 Session boundary and ties: with a 30 minute timeout, a gap of exactly 30 minutes (14:00:00 then 14:30:00) is a new session under >= and the same session under >. Show both on one table and state the rule you would confirm with the interviewer. Then show that two events with an identical event_ts for the same user make LAG order undefined, so the session flag and event order can differ between runs, and fix it with a tie-breaker (ORDER BY event_ts, event_id) in both the LAG and the running SUM.
**Asked at:** Dataiku sessionization tutorial (opened; vendor tutorial, uses a 30 minute timeout with >= and no tie handling) plus search snippets of Cube, DevGenius and LinkedIn sessionization posts (not opened); guides and not candidate reports; product analytics and data scientist rounds
**Say this first (1 line):** A gap of exactly 30 minutes is a new session under `>= 30` and the same session under `> 30`, so I state my rule up front (I assume `>`, "more than 30 minutes of inactivity", and would confirm it), and for identical timestamps I add a unique `event_id` to the `ORDER BY` of both the `LAG` and the running `SUM` so the order never depends on how the engine happened to read the rows.

**Schema and sample data:** seven rows. User 1: 14:00:00, then exactly 14:30:00, then 14:30:01 (the exact-threshold case, plus one second after it). User 2: 10:00, then two events with the identical timestamp 10:45:00 (`click`, event 5, and `buy`, event 6), then 10:50. `event_id` is a plain integer column (not the primary key) so the physical row order in the table is the insert order and I can load the same rows in two different physical orders (`SCHEMA` and `SCHEMA_REV`, the second is the reverse). The 45 minute gap before 10:45 starts a new session in both conventions, so the tie sits right at a session start.
```sql
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,1,'2024-03-01 14:00:00','a'),
 (2,1,'2024-03-01 14:30:00','b'),
 (3,1,'2024-03-01 14:30:01','c'),
 (4,2,'2024-03-01 10:00:00','open'),
 (5,2,'2024-03-01 10:45:00','click'),
 (6,2,'2024-03-01 10:45:00','buy'),
 (7,2,'2024-03-01 10:50:00','exit');
```

**SQL answer:** `SQL_MAIN` in the Code block, `>` convention with the tie-breaker in both window clauses (the `WINDOW w` clause is the same ordering the running `SUM` repeats):
```sql
WITH e AS (
  SELECT user_id, event_id, event_ts, event_name,
         LAG(event_ts) OVER w AS prev_ts,
         LAG(event_name) OVER w AS prev_name
  FROM events
  WINDOW w AS (PARTITION BY user_id ORDER BY event_ts, event_id)
), f AS (
  SELECT *, CASE WHEN prev_ts IS NULL
                   OR (unixepoch(event_ts) - unixepoch(prev_ts)) > 1800
                 THEN 1 ELSE 0 END AS new_session
  FROM e
)
SELECT user_id, event_id, event_name, prev_name, new_session,
       SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_ts, event_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_id
FROM f
ORDER BY user_id, event_ts, event_id
```
`SQL_GE` is the same text with `>= 1800` in place of `> 1800` (seconds; I use `unixepoch` for the reason given in Q11). `SQL_NOTIE` is the same text with the `event_id` removed from every `ORDER BY` of the windows, to show the failure.

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
    e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
    e = e.sort_values(["user_id", "event_ts", "event_id"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    limit = pd.Timedelta(minutes=30)
    new = gap.isna() | ((gap > limit) if strict else (gap >= limit))
    e["session_id"] = new.astype(int).groupby(e["user_id"]).cumsum()
    
```

**Example:** user 1.
- 14:00:00 is the first event: flag 1, session 1.
- 14:30:00 is 1800 seconds after 14:00:00. Under `>` (1800 > 1800 is false): flag 0, session 1. Under `>=`: flag 1, session 2.
- 14:30:01 is one second later: flag 0 in both, so it joins whichever session the 14:30:00 event is in. Result: events 1,2,3 are sessions 1,1,1 under `>` and 1,2,2 under `>=`.
- User 2: 10:00 is session 1. The two 10:45:00 events are 45 minutes after it, so the first of the two in the order gets flag 1 and the second has a gap of 0, flag 0. With the tie-breaker the order is event 5 (`click`) then event 6 (`buy`); the sessions are 1, 2, 2, 2.

**Code:** run with `python3 -I`. SQL and pandas are compared for both conventions on the rows ordered by `user_id, event_ts, event_id`; the tie runs compare the same query on the two physical insert orders.
```python
# Q12: session boundary (> vs >=) and ties in event_ts (tie-breaker event_id)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,1,'2024-03-01 14:00:00','a'),
 (2,1,'2024-03-01 14:30:00','b'),
 (3,1,'2024-03-01 14:30:01','c'),
 (4,2,'2024-03-01 10:00:00','open'),
 (5,2,'2024-03-01 10:45:00','click'),
 (6,2,'2024-03-01 10:45:00','buy'),
 (7,2,'2024-03-01 10:50:00','exit');
"""
# the same rows inserted in the opposite physical order (event_id values unchanged)
SCHEMA_REV = """
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (7,2,'2024-03-01 10:50:00','exit'),
 (6,2,'2024-03-01 10:45:00','buy'),
 (5,2,'2024-03-01 10:45:00','click'),
 (4,2,'2024-03-01 10:00:00','open'),
 (3,1,'2024-03-01 14:30:01','c'),
 (2,1,'2024-03-01 14:30:00','b'),
 (1,1,'2024-03-01 14:00:00','a');
"""
SQL_MAIN = """
WITH e AS (
  SELECT user_id, event_id, event_ts, event_name,
         LAG(event_ts) OVER w AS prev_ts,
         LAG(event_name) OVER w AS prev_name
  FROM events
  WINDOW w AS (PARTITION BY user_id ORDER BY event_ts, event_id)
), f AS (
  SELECT *, CASE WHEN prev_ts IS NULL
                   OR (unixepoch(event_ts) - unixepoch(prev_ts)) > 1800
                 THEN 1 ELSE 0 END AS new_session
  FROM e
)
SELECT user_id, event_id, event_name, prev_name, new_session,
       SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_ts, event_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_id
FROM f
ORDER BY user_id, event_ts, event_id
"""
SQL_GE = SQL_MAIN.replace("> 1800", ">= 1800")
assert SQL_GE != SQL_MAIN
# no tie-breaker: ORDER BY event_ts only (in the LAG window and in the running SUM)
SQL_NOTIE = SQL_MAIN.replace("ORDER BY event_ts, event_id", "ORDER BY event_ts")
assert "ORDER BY event_ts, event_id" not in SQL_NOTIE
# the final ORDER BY must not hide the problem: order the printout by the window result itself
SQL_NOTIE = SQL_NOTIE.replace("ORDER BY user_id, event_ts, event_id", "ORDER BY user_id, event_ts")

def run(schema, sql):
    c = sqlite3.connect(":memory:")
    c.executescript(schema)
    return pd.read_sql_query(sql, c)

print("== boundary: user 1 has a gap of exactly 30:00 (14:00 -> 14:30)")
gt = run(SCHEMA, SQL_MAIN)
ge = run(SCHEMA, SQL_GE)
u1 = pd.DataFrame({"event_id": gt[gt.user_id == 1].event_id.values,
                   "session_gt": gt[gt.user_id == 1].session_id.values,
                   "session_ge": ge[ge.user_id == 1].session_id.values})
print(u1.to_string(index=False))

print("== ties, with the tie-breaker (physical insert order A and B)")
a = run(SCHEMA, SQL_MAIN)
b = run(SCHEMA_REV, SQL_MAIN)
print(a[a.user_id == 2].to_string(index=False))
assert a.equals(b)
print("same result for both insert orders: True")

print("== ties, ORDER BY event_ts only (insert order A, then B)")
na = run(SCHEMA, SQL_NOTIE)
nb = run(SCHEMA_REV, SQL_NOTIE)
print(na[na.user_id == 2].to_string(index=False))
print(nb[nb.user_id == 2].to_string(index=False))
print("same result for both insert orders:", na.equals(nb))
print("session ids per row identical in both?", (na.session_id.values == nb.session_id.values).all())

# pandas: sort with the tie-breaker, then diff / cumsum
events = run(SCHEMA, "SELECT * FROM events")
def sessions(events, strict):
    # pd:main
    e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
    e = e.sort_values(["user_id", "event_ts", "event_id"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    limit = pd.Timedelta(minutes=30)
    new = gap.isna() | ((gap > limit) if strict else (gap >= limit))
    e["session_id"] = new.astype(int).groupby(e["user_id"]).cumsum()
    # pd:end
    return e[["user_id", "event_id", "session_id"]].reset_index(drop=True)

for strict, sql_df in ((True, gt), (False, ge)):
    p = sessions(events, strict)
    s = sql_df[["user_id", "event_id", "session_id"]]
    pd.testing.assert_frame_equal(p, s, check_dtype=False)  # both ordered by user_id, event_ts, event_id
print("pandas matches SQL for > and >=")

# pandas without the tie-breaker: sort_values(['user_id','event_ts']) on the reversed physical order
rev = run(SCHEMA_REV, "SELECT * FROM events").assign(event_ts=lambda d: pd.to_datetime(d["event_ts"]))
fwd = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
o1 = fwd.sort_values(["user_id", "event_ts"])["event_id"].tolist()
o2 = rev.sort_values(["user_id", "event_ts"])["event_id"].tolist()
print("pandas order of event_ids, no tie-breaker, insert order A:", o1)
print("pandas order of event_ids, no tie-breaker, insert order B:", o2)
print("asserts passed")
```

**Output (my run):**
```text
== boundary: user 1 has a gap of exactly 30:00 (14:00 -> 14:30)
 event_id  session_gt  session_ge
        1           1           1
        2           1           2
        3           1           2
== ties, with the tie-breaker (physical insert order A and B)
 user_id  event_id event_name prev_name  new_session  session_id
       2         4       open       NaN            1           1
       2         5      click      open            1           2
       2         6        buy     click            0           2
       2         7       exit       buy            0           2
same result for both insert orders: True
== ties, ORDER BY event_ts only (insert order A, then B)
 user_id  event_id event_name prev_name  new_session  session_id
       2         4       open       NaN            1           1
       2         5      click      open            1           2
       2         6        buy     click            0           2
       2         7       exit       buy            0           2
 user_id  event_id event_name prev_name  new_session  session_id
       2         4       open       NaN            1           1
       2         6        buy      open            1           2
       2         5      click       buy            0           2
       2         7       exit     click            0           2
same result for both insert orders: False
session ids per row identical in both? True
pandas matches SQL for > and >=
pandas order of event_ids, no tie-breaker, insert order A: [1, 2, 3, 4, 5, 6, 7]
pandas order of event_ids, no tie-breaker, insert order B: [1, 2, 3, 4, 6, 5, 7]
asserts passed
```

**Edge cases:**
- Exact threshold: event 2 is session 1 under `>` and session 2 under `>=` in my run, and event 3 (one second later) follows event 2 in both. Rule to confirm with the interviewer: is the timeout "inactive for more than 30 minutes" (`>`) or "30 minutes or more" (`>=`)? The Dataiku tutorial uses `>=`; other write-ups use `>`. I assume `>` and say so.
- Ties, honest result from my run: with `ORDER BY event_ts` only, the two physical insert orders gave different row orders for the tied events. In order A the sequence was click (5) then buy (6); in order B it was buy (6) then click (5), and `prev_name`, the row that carries `new_session = 1`, and any "first event of the session" or "event number" column changed with it. The session ids per row were identical in both runs, because the tied rows have the same timestamp and therefore the same gap from the earlier event; only which row of the pair carries the flag moves. So the claim "session numbers change" was not what I observed; what changed is every per-event output. With the tie-breaker the result was equal in both insert orders (`True`).
- The default frame of a running `SUM ... ORDER BY event_ts` is `RANGE`, which treats tied rows as peers and adds them together. That hides the difference in session ids above, but `ROW_NUMBER`, `LAG`, `FIRST_VALUE` and `ROWS` frames do not hide it. I wrote `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` in `SQL_MAIN` so the frame is explicit.
- Order of the tied events is arbitrary only in the sense of "not defined by the SQL"; in this SQLite run it followed the physical row order, other engines or plans may differ (I did not run them).
- pandas: `sort_values(["user_id", "event_ts"])` also left the tied events in their input order (order A gave 5 then 6, order B gave 6 then 5). Add `event_id` to the sort keys. I also pass `kind="stable"`; for a single sort key the default kind is quicksort, which in my probe on 2000 rows with many ties was not stable, while a multi-key sort was stable in my probe.
- Tie-breaker must be unique. If `event_id` is itself duplicated, the ties return.
- Single-event users and NULL timestamps behave as in Q11.

**Then explain:**
- Rule first, code second: write the boundary operator as a constant (here 1800 seconds) and say which side the equal case falls on.
- For `LAG` to be deterministic the window `ORDER BY` must give a total order. Timestamps are not unique, so append a unique column. The same total order must be used by every window in the query, otherwise the `LAG` row and the running `SUM` row sequences disagree.
- The tie-breaker does not decide whether `click` really came before `buy`; it only makes the result repeatable. If the true order matters, you need a sequence number from the source system.
- `WINDOW w AS (...)` names a window so the `LAG` calls share one definition (SQLite 3.28 and later). The final `SUM` repeats the ordering because it also needs the frame.
- Dialects, not executed here: PostgreSQL and MySQL 8 accept the same window syntax; MySQL 5.7 has no window functions at all.

**Follow-ups:**
- Which convention would you choose for a 30 minute product session? Whatever the product's analytics tool uses; many tools say "30 minutes of inactivity", which reads like `>`, but I would confirm.
- What if two tied events belong to different users? No effect, the windows are partitioned by user.
- What if the tie-breaker is missing and the data has no id? Use all columns that make the row unique, or accept that per-event outputs are not repeatable and only report session-level aggregates (counts and first/last timestamps, which were stable here).

**Common mistakes:**
- Using `>=` or `>` without saying so.
- A tie-breaker in only one of the windows.
- Relying on the default frame to make ties safe, then adding `ROW_NUMBER` or `FIRST_VALUE` later and getting unrepeatable output.
- Claiming the order of ties is random: in this run it followed the physical order, which is stable only by accident.
- Sorting a pandas frame by timestamp only and trusting the order of tied rows.

### Q13 ⭐⭐⭐ 🟡 Consecutive same-status runs (run-length encoding in SQL): status_log(entity_id, ts, status) with statuses such as 'ok' and 'down' that repeat. Return each run as entity_id, status, run_start, run_end, rows using LAG to flag a change (status <> prev_status, with the first row as a change) and a running SUM of the flag. Then show the partitioned ROW_NUMBER difference method (ROW_NUMBER over entity ordered by ts minus ROW_NUMBER over entity and status ordered by ts) and explain why the two methods agree.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** A run is a maximal stretch of consecutive rows with the same status; flag every row whose status differs from the previous row of the same entity (the first row always counts as a change), take a running `SUM` of the flag as the run number, then group to get start, end and row count; the alternative is two `ROW_NUMBER`s whose difference is constant inside a run.

**Schema and sample data:** eleven rows, inserted out of time order for entity 1 (00:05 before 00:00). Entity 1: ok, ok, down, down, down, ok. Entity 2: a single row. Entity 3: ok, NULL, NULL, ok (NULL status is a real case in logs). Timestamps are ISO text.
```sql
CREATE TABLE status_log(entity_id INTEGER, ts TEXT, status TEXT);
INSERT INTO status_log VALUES
 (1,'2024-03-01 00:05:00','ok'),
 (1,'2024-03-01 00:00:00','ok'),
 (1,'2024-03-01 00:10:00','down'),
 (1,'2024-03-01 00:15:00','down'),
 (1,'2024-03-01 00:20:00','down'),
 (1,'2024-03-01 00:25:00','ok'),
 (2,'2024-03-01 00:00:00','down'),
 (3,'2024-03-01 00:00:00','ok'),
 (3,'2024-03-01 00:05:00',NULL),
 (3,'2024-03-01 00:10:00',NULL),
 (3,'2024-03-01 00:15:00','ok');
```

**SQL answer:** `SQL_MAIN` in the Code block (LAG flag plus running SUM). `IS NOT` is the NULL-safe "different from" in SQLite:
```sql
WITH f AS (
  SELECT entity_id, ts, status,
         CASE WHEN LAG(ts) OVER w IS NULL OR status IS NOT LAG(status) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM status_log
  WINDOW w AS (PARTITION BY entity_id ORDER BY ts)
), g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY entity_id ORDER BY ts) AS run_id
  FROM f
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM g
GROUP BY entity_id, run_id, status
ORDER BY entity_id, run_start
```
The row-number difference method, `SQL_RN` in the Code block:
```sql
WITH r AS (
  SELECT entity_id, ts, status,
         ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
       - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
  FROM status_log
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM r
GROUP BY entity_id, status, grp
ORDER BY entity_id, run_start
```
`SQL_WRONG` is `SQL_MAIN` with `<>` instead of `IS NOT`, to show the NULL trap.

**pandas answer:** the same flag-and-cumsum logic, shown once here and identical to the Code block. The first-row flag and the NULL-safe comparison are explicit because `NaN != NaN` is `True` in pandas:
```py
d = log.sort_values(["entity_id", "ts"], kind="stable").copy()
prev = d.groupby("entity_id")["status"].shift()
first = d.groupby("entity_id").cumcount() == 0
same = (d["status"] == prev) | (d["status"].isna() & prev.isna())
d["run_id"] = (first | ~same).astype(int).groupby(d["entity_id"]).cumsum()
runs = (d.groupby(["entity_id", "run_id"], as_index=False, dropna=False)
          .agg(status=("status", "first"), run_start=("ts", "min"), run_end=("ts", "max"),
               n_rows=("ts", "size")))
runs = runs[["entity_id", "status", "run_start", "run_end", "n_rows"]]
```

**Example:** entity 1 sorted: ok 00:00, ok 00:05, down 00:10, down 00:15, down 00:20, ok 00:25.
- Flags: 1 (first), 0 (same), 1 (ok to down), 0, 0, 1 (down to ok). Running sum: 1,1,2,2,2,3. Runs: ok 00:00 to 00:05 (2 rows), down 00:10 to 00:20 (3 rows), ok 00:25 (1 row).
- Row-number method: `rn_all` is 1..6; `rn_status` counts inside each status: ok gets 1,2 then 3 for the last row, down gets 1,2,3. The difference `rn_all - rn_status` is 0,0,2,2,2,3. Inside a run both counters go up by one per row, so the difference cannot change; when a different status interrupts, `rn_all` jumps ahead while this status's own counter does not, so the difference becomes a new number.
- Why the final ok (difference 3) is not merged with the first ok (difference 0): the two oks have different differences because three rows of other status sit between them.
- Entity 3: ok, NULL x2, ok gives three runs: ok, NULL (2 rows), ok.

**Code:** run with `python3 -I`. The asserts compare the two SQL methods with each other, pandas with SQL (rows ordered by `entity_id, run_start`), and an `itertools.groupby` run-length cross-check for entity 1.
```python
# Q13: consecutive same-status runs: LAG flag + running SUM, ROW_NUMBER difference, pandas, itertools.groupby
import sqlite3
import itertools
import pandas as pd

SCHEMA = """
CREATE TABLE status_log(entity_id INTEGER, ts TEXT, status TEXT);
INSERT INTO status_log VALUES
 (1,'2024-03-01 00:05:00','ok'),
 (1,'2024-03-01 00:00:00','ok'),
 (1,'2024-03-01 00:10:00','down'),
 (1,'2024-03-01 00:15:00','down'),
 (1,'2024-03-01 00:20:00','down'),
 (1,'2024-03-01 00:25:00','ok'),
 (2,'2024-03-01 00:00:00','down'),
 (3,'2024-03-01 00:00:00','ok'),
 (3,'2024-03-01 00:05:00',NULL),
 (3,'2024-03-01 00:10:00',NULL),
 (3,'2024-03-01 00:15:00','ok');
"""
SQL_MAIN = """
WITH f AS (
  SELECT entity_id, ts, status,
         CASE WHEN LAG(ts) OVER w IS NULL OR status IS NOT LAG(status) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM status_log
  WINDOW w AS (PARTITION BY entity_id ORDER BY ts)
), g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY entity_id ORDER BY ts) AS run_id
  FROM f
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM g
GROUP BY entity_id, run_id, status
ORDER BY entity_id, run_start
"""
SQL_RN = """
WITH r AS (
  SELECT entity_id, ts, status,
         ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
       - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
  FROM status_log
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM r
GROUP BY entity_id, status, grp
ORDER BY entity_id, run_start
"""
# wrong: <> instead of IS NOT (NULL comparison is NULL, so CASE falls to ELSE 0)
SQL_WRONG = SQL_MAIN.replace("status IS NOT LAG(status) OVER w", "status <> LAG(status) OVER w")
assert SQL_WRONG != SQL_MAIN
SQL_GRP = """
SELECT entity_id, ts, status,
       ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts) AS rn_all,
       ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS rn_status,
       ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
     - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
FROM status_log WHERE entity_id = 1 ORDER BY ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_RN, con)
w = pd.read_sql_query(SQL_WRONG, con)
print("LAG + running SUM:"); print(a.to_string(index=False))
print("ROW_NUMBER difference, entity 1 detail:"); print(pd.read_sql_query(SQL_GRP, con).to_string(index=False))
pd.testing.assert_frame_equal(a, b)
print("two SQL methods equal (ordered by entity_id, run_start): True")
print("wrong version with <> (NULL status rows vanish from the flag):"); print(w.to_string(index=False))

log = pd.read_sql_query("SELECT * FROM status_log", con)
# pd:main
d = log.sort_values(["entity_id", "ts"], kind="stable").copy()
prev = d.groupby("entity_id")["status"].shift()
first = d.groupby("entity_id").cumcount() == 0
same = (d["status"] == prev) | (d["status"].isna() & prev.isna())
d["run_id"] = (first | ~same).astype(int).groupby(d["entity_id"]).cumsum()
runs = (d.groupby(["entity_id", "run_id"], as_index=False, dropna=False)
          .agg(status=("status", "first"), run_start=("ts", "min"), run_end=("ts", "max"),
               n_rows=("ts", "size")))
runs = runs[["entity_id", "status", "run_start", "run_end", "n_rows"]]
# pd:end
pd.testing.assert_frame_equal(runs.reset_index(drop=True), a.assign(status=a["status"]), check_dtype=False)
print("pandas equals SQL (ordered by entity_id, run_start): True")
naive = (d["status"] != prev) | first
print("naive pandas (s != s.shift()) runs for entity 3:",
      int(naive[d.entity_id == 3].sum()), "(correct: 3 runs, NaN != NaN is True so each NULL row is its own run)")

# itertools.groupby run lengths for entity 1, as a cross-check
e1 = d[d.entity_id == 1]["status"].tolist()
ig = [(k, len(list(g))) for k, g in itertools.groupby(e1)]
print("itertools.groupby entity 1:", ig)
assert ig == list(zip(a[a.entity_id == 1].status, a[a.entity_id == 1].n_rows))
# duplicated ts in the same entity changes the answer unless a tie-breaker exists: show the guard
con.execute("INSERT INTO status_log VALUES (2,'2024-03-01 00:00:00','ok')")
dup = pd.read_sql_query("SELECT entity_id, ts, COUNT(*) c FROM status_log GROUP BY entity_id, ts HAVING c > 1", con)
print("duplicate (entity_id, ts) keys after inserting one extra row:"); print(dup.to_string(index=False))
d2 = pd.read_sql_query(SQL_MAIN, con)
r2 = pd.read_sql_query(SQL_RN, con)
print("entity 2 after the tied row, LAG method:"); print(d2[d2.entity_id == 2].to_string(index=False))
print("entity 2 after the tied row, ROW_NUMBER method:"); print(r2[r2.entity_id == 2].to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
LAG + running SUM:
 entity_id status           run_start             run_end  n_rows
         1     ok 2024-03-01 00:00:00 2024-03-01 00:05:00       2
         1   down 2024-03-01 00:10:00 2024-03-01 00:20:00       3
         1     ok 2024-03-01 00:25:00 2024-03-01 00:25:00       1
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         3     ok 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         3    NaN 2024-03-01 00:05:00 2024-03-01 00:10:00       2
         3     ok 2024-03-01 00:15:00 2024-03-01 00:15:00       1
ROW_NUMBER difference, entity 1 detail:
 entity_id                  ts status  rn_all  rn_status  grp
         1 2024-03-01 00:00:00     ok       1          1    0
         1 2024-03-01 00:05:00     ok       2          2    0
         1 2024-03-01 00:10:00   down       3          1    2
         1 2024-03-01 00:15:00   down       4          2    2
         1 2024-03-01 00:20:00   down       5          3    2
         1 2024-03-01 00:25:00     ok       6          3    3
two SQL methods equal (ordered by entity_id, run_start): True
wrong version with <> (NULL status rows vanish from the flag):
 entity_id status           run_start             run_end  n_rows
         1     ok 2024-03-01 00:00:00 2024-03-01 00:05:00       2
         1   down 2024-03-01 00:10:00 2024-03-01 00:20:00       3
         1     ok 2024-03-01 00:25:00 2024-03-01 00:25:00       1
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         3     ok 2024-03-01 00:00:00 2024-03-01 00:15:00       2
         3    NaN 2024-03-01 00:05:00 2024-03-01 00:10:00       2
pandas equals SQL (ordered by entity_id, run_start): True
naive pandas (s != s.shift()) runs for entity 3: 4 (correct: 3 runs, NaN != NaN is True so each NULL row is its own run)
itertools.groupby entity 1: [('ok', 2), ('down', 3), ('ok', 1)]
duplicate (entity_id, ts) keys after inserting one extra row:
 entity_id                  ts  c
         2 2024-03-01 00:00:00  2
entity 2 after the tied row, LAG method:
 entity_id status           run_start             run_end  n_rows
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         2     ok 2024-03-01 00:00:00 2024-03-01 00:00:00       1
entity 2 after the tied row, ROW_NUMBER method:
 entity_id status           run_start             run_end  n_rows
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         2     ok 2024-03-01 00:00:00 2024-03-01 00:00:00       1
asserts passed
```

**Edge cases:**
- NULL status: with `status <> LAG(status)` the comparison is NULL when either side is NULL, so the `CASE` falls to `ELSE 0`. In my run entity 3 then collapsed to the wrong result (ok with 2 rows from 00:00 to 00:15, plus the NULL run), because the NULL rows never started a run and the later ok never started one either. With `IS NOT` the result is three runs.
- pandas: `s != s.shift()` treats every NaN as different from every other NaN (`NaN != NaN` is `True`), so the naive version made entity 3 four runs (each NULL row on its own) instead of three; and `groupby` drops NaN keys by default, so I pass `dropna=False`. My code builds the "same" test with `isna()` on both sides.
- First row of each entity: `LAG` gives NULL; I flag with `LAG(ts) IS NULL`, which is true only for the first row (a NULL `status` on the first row would otherwise be ambiguous). In pandas the first row is `cumcount() == 0`, because `shift()` also gives NaN on the first row.
- Single-row entity (entity 2): one run, start equals end, one row.
- Unsorted input: handled by the window `ORDER BY` and the pandas `sort_values`.
- Duplicate timestamps for the same entity: after inserting `(2, 00:00:00, 'ok')` next to the existing `down` at the same timestamp, both SQL methods returned two one-row runs for entity 2 in this run, but which of the two comes first is not defined by the SQL; add a unique tie-breaker column to every `ORDER BY` (Q12).
- Big gaps in time do not matter here; a run is about consecutive rows, not consecutive time. If a gap in time must also break a run, add that condition to the flag.
- The row-number difference works only because the ordering is a total order; both methods break with ties for the same reason.

**Then explain:**
- Method 1, flag and running sum: easiest to extend (add "or gap over N minutes" to the flag). Needs `LAG`, a `CASE`, a running `SUM` and a `GROUP BY`.
- Method 2, row-number difference: no `LAG`, no `CASE`, and NULL status works without a special case because `PARTITION BY` puts NULLs in one partition. The difference number itself has no meaning and is only unique inside an `(entity, status)` pair, so group by `(entity_id, status, grp)`; in `SQL_RN` grouping by `grp` alone would merge an ok run and a down run that happen to share the same difference.
- Why they agree: both are constants that change exactly when a run changes. Method 1 counts the number of starts so far; method 2 is `rn_all - rn_status`, and inside one run both advance together.
- Run length in pandas is `groupby(run_id).size()`, in plain Python `itertools.groupby` (shown for entity 1 and equal to the SQL).
- Dialects, not executed here: `IS DISTINCT FROM` is the standard spelling (it also ran on SQLite 3.45.1 in the Wave A probe, though this answer uses `IS NOT`; PostgreSQL support is from memory, not executed); MySQL uses `<=>` for NULL-safe equality; the row-number method needs window functions, so MySQL 5.7 cannot run either method.

**Follow-ups:**
- Only the longest `down` run per entity? Take `MAX(n_rows)` from the grouped result where `status = 'down'`, or rank with `ROW_NUMBER` (ranking itself is Part 4).
- Remove the repeated statuses and keep only the changes? Keep rows where the flag is 1 (state-change detection).
- Time spent in each run? `run_end` minus `run_start` gives the span between first and last row; adding the next run's start gives the full duration.

**Common mistakes:**
- `<>` with NULLs (shown above).
- Forgetting to partition by entity, so a run leaks across entities.
- Grouping only by `grp` in the row-number method, or only by `run_id` and forgetting that `status` has to be selected or grouped.
- Using `s != s.shift()` in pandas on data with NaN.
- Assuming the data is already sorted.

### Q14 ⭐⭐⭐ 🟡 pandas streaks per user: translate the date-minus-ROW_NUMBER streak query to pandas. logins(user_id, login_date) as a DataFrame with duplicates and unsorted rows. Show drop_duplicates and sort_values, then two keys: (date.diff().dt.days != 1).cumsum() per user via groupby, and day number minus cumcount as the island key. Return user_id, streak_start, streak_end, streak_days and assert the frame equals the SQL result (same rows, order stated). Explain why a global diff() without the groupby leaks a streak across users.
**Asked at:** pandas Series.shift reference (opened) and search snippets of Stack Overflow and Towards Data Science run-grouping answers ((s != s.shift()).cumsum(), diff().ne(0).cumsum(); not opened); documentation and guides, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Deduplicate and sort the logins, then give every row a streak key that is constant inside a streak and different between streaks, and group by `(user_id, key)`; the two keys are "cumulative sum of (gap to the previous login of the same user is not 1 day)" and "day number minus the row's position within the user".

**Schema and sample data:** twelve rows, four users, deliberately messy: user 1 is unsorted and has a duplicate login on 03-02 (distinct days 1, 2, 3 and 5 March), user 2 has a NULL date and last logs in on 03-10 after 03-06 and 03-07, user 3 has a single login, user 4 has two consecutive days. User 1's last login (03-05) is one day before user 2's first login (03-06), on purpose, for the leak demonstration. Dates are ISO text.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-05'),
 (2,'2024-03-07'),(2,'2024-03-06'),(2,'2024-03-10'),(2,NULL),
 (3,'2024-03-09'),
 (4,'2024-03-04'),(4,'2024-03-05');
```

**SQL answer:** `SQL_MAIN` in the Code block, the date-minus-`ROW_NUMBER` reference (dedupe with `DISTINCT` first, then subtract the position in days). Position within a user's sorted distinct dates is constant against the date on a streak, so `date - rn` is the same for the whole streak:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r
GROUP BY user_id, grp
ORDER BY user_id, streak_start
```
Streak length is `COUNT(*)` of distinct days; counting rows without the `DISTINCT` would inflate user 1's first streak to 4.

**pandas answer:** shown once here and identical to the Code block. `key1` is the diff approach, `key2` the island (day number minus `cumcount`) approach:
```py
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
# key 1: a new streak starts when the gap to the previous login of the SAME user is not 1 day
gap_days = d.groupby("user_id")["login_date"].diff().dt.days
d["key1"] = (gap_days != 1).groupby(d["user_id"]).cumsum()
# key 2: day number minus position inside the user's list is constant on a streak
daynum = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days
d["key2"] = daynum - d.groupby("user_id").cumcount()
res1 = d.groupby(["user_id", "key1"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
res2 = d.groupby(["user_id", "key2"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
```

**Example:** user 1 after dedupe and sort: 03-01, 03-02, 03-03, 03-05.
- Key 1: gaps to the previous login are NaT (first row), 1, 1, 2 days; `gap != 1` is True, False, False, True; the per-user cumulative sum is 1,1,1,2. Streaks: 03-01 to 03-03 (3 days) and 03-05 (1 day).
- Key 2: day numbers are `d, d+1, d+2, d+4`; `cumcount` is 0,1,2,3; the difference is `d, d, d, d+1`: the first three are equal, the fourth differs. Same two streaks.
- User 2: 03-06, 03-07, 03-10 gives 2 days and 1 day (the NULL row is dropped first). User 3: one streak of 1 day. User 4: one streak of 2 days (03-04, 03-05).
- Total: 6 streaks.

**Code:** run with `python3 -I`. Both pandas keys are asserted equal to the SQL result after ordering by `user_id, streak_start`; dates are compared as ISO text.
```python
# Q14: pandas streaks per user: translate date-minus-ROW_NUMBER to pandas, two keys, global diff leak
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-05'),
 (2,'2024-03-07'),(2,'2024-03-06'),(2,'2024-03-10'),(2,NULL),
 (3,'2024-03-09'),
 (4,'2024-03-04'),(4,'2024-03-05');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r
GROUP BY user_id, grp
ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_MAIN, con)
print("SQL streaks:"); print(sql_res.to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)

# pd:main
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
# key 1: a new streak starts when the gap to the previous login of the SAME user is not 1 day
gap_days = d.groupby("user_id")["login_date"].diff().dt.days
d["key1"] = (gap_days != 1).groupby(d["user_id"]).cumsum()
# key 2: day number minus position inside the user's list is constant on a streak
daynum = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days
d["key2"] = daynum - d.groupby("user_id").cumcount()
res1 = d.groupby(["user_id", "key1"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
res2 = d.groupby(["user_id", "key2"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
# pd:end
def fmt(r):
    r = r[["user_id", "streak_start", "streak_end", "streak_days"]].copy()
    for c in ("streak_start", "streak_end"):
        r[c] = r[c].dt.strftime("%Y-%m-%d")
    return r.sort_values(["user_id", "streak_start"]).reset_index(drop=True)
p1, p2 = fmt(res1), fmt(res2)
print("pandas key1 (groupby diff):"); print(p1.to_string(index=False))
pd.testing.assert_frame_equal(p1, sql_res, check_dtype=False)
pd.testing.assert_frame_equal(p2, sql_res, check_dtype=False)  # rows ordered by user_id, streak_start
print("both pandas keys equal the SQL result (ordered by user_id, streak_start): True")
print("gap_days dtype:", gap_days.dtype, "| first values:", gap_days.head(4).tolist())
print("NaN != 1 ->", float("nan") != 1)

# wrong: global diff (no groupby) and grouping on the key alone
gd = d["login_date"].diff().dt.days
d["wrong_key"] = (gd != 1).cumsum()
leak_alone = d.groupby("wrong_key", as_index=False).agg(
    user_id=("user_id", "first"), streak_start=("login_date", "min"),
    streak_end=("login_date", "max"), streak_days=("login_date", "size"), users=("user_id", "nunique"))
print("global diff, grouped by the key only (users column = distinct users inside the group):")
print(leak_alone.assign(streak_start=leak_alone.streak_start.dt.strftime("%Y-%m-%d"),
                        streak_end=leak_alone.streak_end.dt.strftime("%Y-%m-%d"))
      .drop(columns="wrong_key").to_string(index=False))
same_by_luck = d.groupby(["user_id", "wrong_key"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
print("global diff but grouped by (user_id, key) equals the right answer:",
      fmt(same_by_luck).equals(sql_res))

print("asserts passed")
```

**Output (my run):**
```text
SQL streaks:
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-03            3
       1   2024-03-05 2024-03-05            1
       2   2024-03-06 2024-03-07            2
       2   2024-03-10 2024-03-10            1
       3   2024-03-09 2024-03-09            1
       4   2024-03-04 2024-03-05            2
pandas key1 (groupby diff):
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-03            3
       1   2024-03-05 2024-03-05            1
       2   2024-03-06 2024-03-07            2
       2   2024-03-10 2024-03-10            1
       3   2024-03-09 2024-03-09            1
       4   2024-03-04 2024-03-05            2
both pandas keys equal the SQL result (ordered by user_id, streak_start): True
gap_days dtype: float64 | first values: [nan, 1.0, 1.0, 2.0]
NaN != 1 -> True
global diff, grouped by the key only (users column = distinct users inside the group):
 user_id streak_start streak_end  streak_days  users
       1   2024-03-01 2024-03-03            3      1
       1   2024-03-05 2024-03-07            3      2
       2   2024-03-10 2024-03-10            1      1
       3   2024-03-09 2024-03-09            1      1
       4   2024-03-04 2024-03-05            2      1
global diff but grouped by (user_id, key) equals the right answer: True
asserts passed
```

**Edge cases:**
- Duplicates: `drop_duplicates()` before the key, otherwise `cumcount` counts the repeated row and breaks the day-number-minus-position key, and the diff approach sees a gap of 0 days which is not 1, so a duplicate would also start a new streak.
- Unsorted input: sort before `diff` and `cumcount`; neither knows the order unless you sort. `groupby(...).diff()` works on the existing row order.
- Single-row user (user 3): `diff` is NaT for the first row, so `.dt.days` is NaN, and `NaN != 1` is `True` in my run, which correctly starts a streak of length 1.
- Dtype note from my run: `.dt.days` on a diff column with NaT is `float64` (NaN is a float), not integer; comparing it with 1 is fine. The shift/diff family upcasts integer data to float for the same reason (a `shift` of an integer column gave `float64` in my probe, and `fill_value=0` kept it integer).
- NULL date: `to_datetime` would give `NaT`, which sorts last and creates a bogus row; I drop the NULL rows before everything else, as the SQL does.
- Empty input: not run through this pipeline here; check it before relying on it.
- Timestamps instead of dates: normalize first (`dt.normalize()` in pandas, `date()` in SQL), otherwise two logins on the same day with different times are two rows.
- Time zones and daylight saving: a date column has none; timestamps in different zones need converting to the user's local date first (SQLite has no zones, so this is a note, not something I ran).

**Then explain:**
- Why the diff key needs `groupby`: without it, `login_date.diff()` also compares the first row of user 2 with the last row of user 1. In my data user 1's last login is 03-05 and user 2's first is 03-06, a gap of 1 day, so the first row of user 2 is not flagged as a streak start. If you then group by the key alone, user 2's first streak (03-06 and 03-07) glues onto user 1's streak 03-05: one bogus group of 3 days attributed to user 1 with 2 users inside (see the `users` column). That is the leak.
- Honest nuance, run: if you group by `(user_id, key)` the leak is hidden, because the user column separates the groups again; the global-diff frame still matched the correct answer in my run (`True`). So the global diff is a bug that is silent when you group by user and wrong when the key stands alone (a window or `transform` on the key, a `nunique` of the key, a merge on the key).
- The diff approach needs the per-user first row flagged (NaN gap is not equal to 1); the island approach has no such special case but needs unique days per user (hence the dedupe).
- Mapping to SQL: `groupby("user_id")["login_date"].diff()` is `LAG` over the partition, `groupby().cumsum()` is the running `SUM` over the partition, `cumcount()` is `ROW_NUMBER() - 1`.

**Follow-ups:**
- Longest streak per user? Add `groupby("user_id")["streak_days"].max()` on the result; Q21 does the full set of statistics.
- A calendar with weekends excluded? A calendar table of working days and ranking on that, not day numbers.
- Why two keys? The diff key is easier to read and to extend with extra reset conditions; the island key needs no first-row case.

**Common mistakes:**
- Global `diff()` or `shift()` without `groupby` (shown above).
- Not dropping duplicates (the island key is off and streak lengths inflate).
- Comparing `.dt.days` to 1 without handling the NaN first row, or using `== 1` and negating wrongly.
- Grouping by the key only; keys repeat across users (the same `date - rn` number can appear for two users).
- Sorting by date only and not by user and date.

### Q15 ⭐⭐⭐ 🔴 Current streak as of a fixed date: logins(user_id, login_date) and an as-of date of 2024-03-20 (not now). Return each user's current streak length, defined as the island whose end is the as-of date or the day before (state the rule and show the other rule), and 0 or no row for users whose last login is older. Include a user who logged in on the as-of date only, one who last logged in two days before, and one with an earlier longer streak that must not be reported.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** Cut the logins off at the as-of date (2024-03-20, a fixed value, never today), build the date-streak islands, keep the one island whose end is the as-of date or the day before, and report its length; users without such an island get 0.

**Rule I assume, and the other one:** rule A, "the streak is current if its last login is on the as-of date or the day before", because a user who has not yet logged in today has not broken the streak. Rule B, "the last login must be on the as-of date itself" is stricter. Both are in the Code block (`SQL_MAIN` is rule A, `SQL_STRICT` is rule B) and in the output. Say the rule before writing code.

**Schema and sample data:** twenty-one rows, six users, as-of date 2024-03-20. User 1 logged in on the as-of date only. User 2 last logged in two days before (03-17, 03-18). User 3 has an earlier longer streak (03-01 to 03-07, 7 days, unsorted rows) and a current streak of 03-19 and 03-20, with a duplicate row on 03-20. User 4 has 03-17, 03-18, 03-19 (last login the day before). User 5 has 03-19, 03-20 and two rows after the as-of date (03-21, 03-22, as if loaded later). User 6 has only a NULL date.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-20'),
 (2,'2024-03-17'),(2,'2024-03-18'),
 (3,'2024-03-20'),(3,'2024-03-02'),(3,'2024-03-01'),(3,'2024-03-03'),(3,'2024-03-04'),
 (3,'2024-03-05'),(3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-19'),(3,'2024-03-20'),
 (4,'2024-03-19'),(4,'2024-03-17'),(4,'2024-03-18'),
 (5,'2024-03-22'),(5,'2024-03-19'),(5,'2024-03-20'),(5,'2024-03-21'),
 (6,NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block (rule A). The island part is the date-minus-`ROW_NUMBER` pattern; the as-of cut-off is in the first CTE; the user list comes from the table itself and is `LEFT JOIN`ed to the islands so a user without a current streak shows 0:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
), isl AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
  FROM r
  GROUP BY user_id, grp
)
SELECT u.user_id, COALESCE(i.streak_days, 0) AS current_streak
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN isl i
  ON i.user_id = u.user_id
 AND i.streak_end >= date('2024-03-20', '-1 day')
ORDER BY u.user_id
```
Rule B is the same text with `i.streak_end = '2024-03-20'` in place of the `>=` condition.

**pandas answer:** shown once here and identical to the Code block (`rule_a=True` is rule A):
```py
    users = logins["user_id"].drop_duplicates()
    d = logins.dropna(subset=["login_date"]).copy()
    d["login_date"] = pd.to_datetime(d["login_date"])
    d = d[d["login_date"] <= as_of].drop_duplicates().sort_values(["user_id", "login_date"])
    d["key"] = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days - d.groupby("user_id").cumcount()
    isl = d.groupby(["user_id", "key"], as_index=False).agg(
        streak_end=("login_date", "max"), streak_days=("login_date", "size"))
    cutoff = as_of - pd.Timedelta(days=1) if rule_a else as_of
    cur = isl[isl["streak_end"] >= cutoff].set_index("user_id")["streak_days"]
    out = cur.reindex(users).fillna(0).astype(int).rename("current_streak").reset_index()
    
```

**Example:** islands after the cut-off: U1 03-20 (1 day); U2 03-17 to 03-18 (2); U3 03-01 to 03-07 (7) and 03-19 to 03-20 (2); U4 03-17 to 03-19 (3); U5 03-19 to 03-20 (2).
- Rule A needs `streak_end >= 03-19`. U1 1; U2 ends 03-18, 0; U3 the island ending 03-20, so 2 (the 7-day island ended on 03-07 and is not reported); U4 ends 03-19, so 3; U5 2; U6 has no valid date, 0.
- Rule B needs `streak_end = 03-20`: same except U4 is 0, because its last login was the day before.
- U5 shows why the cut-off matters: without `login_date <= as_of` the future rows 03-21 and 03-22 join the island and U5 becomes 4.

**Code:** run with `python3 -I`. The asserts compare pandas with SQL for both rules, ordered by `user_id`.
```python
# Q15: current streak as of a fixed date (2024-03-20), two rules, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-20'),
 (2,'2024-03-17'),(2,'2024-03-18'),
 (3,'2024-03-20'),(3,'2024-03-02'),(3,'2024-03-01'),(3,'2024-03-03'),(3,'2024-03-04'),
 (3,'2024-03-05'),(3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-19'),(3,'2024-03-20'),
 (4,'2024-03-19'),(4,'2024-03-17'),(4,'2024-03-18'),
 (5,'2024-03-22'),(5,'2024-03-19'),(5,'2024-03-20'),(5,'2024-03-21'),
 (6,NULL);
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
), isl AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
  FROM r
  GROUP BY user_id, grp
)
SELECT u.user_id, COALESCE(i.streak_days, 0) AS current_streak
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN isl i
  ON i.user_id = u.user_id
 AND i.streak_end >= date('2024-03-20', '-1 day')
ORDER BY u.user_id
"""
# other rule: the streak must end ON the as-of date
SQL_STRICT = SQL_MAIN.replace("i.streak_end >= date('2024-03-20', '-1 day')", "i.streak_end = '2024-03-20'")
assert SQL_STRICT != SQL_MAIN
# wrong 1: no cut-off on the as-of date (future rows counted)
SQL_NOCUT = SQL_MAIN.replace(" AND login_date <= '2024-03-20'", "")
assert SQL_NOCUT != SQL_MAIN
# wrong 2: report the longest island instead of the current one
SQL_LONGEST = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'),
r AS (SELECT user_id, login_date,
      date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp FROM d)
SELECT user_id, MAX(n) AS longest_streak FROM (SELECT user_id, grp, COUNT(*) AS n FROM r GROUP BY user_id, grp)
GROUP BY user_id ORDER BY user_id
"""
SQL_ISLANDS = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'),
r AS (SELECT user_id, login_date,
      date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp FROM d)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r GROUP BY user_id, grp ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("islands up to the as-of date:"); print(pd.read_sql_query(SQL_ISLANDS, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_STRICT, con)
c = pd.read_sql_query(SQL_NOCUT, con)
l = pd.read_sql_query(SQL_LONGEST, con)
cmp_ = a.rename(columns={"current_streak": "end_asof_or_day_before"}).assign(
    end_on_asof_only=b["current_streak"], wrong_no_cutoff=c["current_streak"],
    wrong_longest=l.set_index("user_id")["longest_streak"].reindex(a["user_id"]).fillna(0).astype(int).values)
print("current streak as of 2024-03-20:"); print(cmp_.to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
AS_OF = pd.Timestamp("2024-03-20")

def current_streak(logins, as_of, rule_a=True):
    # pd:main
    users = logins["user_id"].drop_duplicates()
    d = logins.dropna(subset=["login_date"]).copy()
    d["login_date"] = pd.to_datetime(d["login_date"])
    d = d[d["login_date"] <= as_of].drop_duplicates().sort_values(["user_id", "login_date"])
    d["key"] = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days - d.groupby("user_id").cumcount()
    isl = d.groupby(["user_id", "key"], as_index=False).agg(
        streak_end=("login_date", "max"), streak_days=("login_date", "size"))
    cutoff = as_of - pd.Timedelta(days=1) if rule_a else as_of
    cur = isl[isl["streak_end"] >= cutoff].set_index("user_id")["streak_days"]
    out = cur.reindex(users).fillna(0).astype(int).rename("current_streak").reset_index()
    # pd:end
    return out.sort_values("user_id").reset_index(drop=True)

pa = current_streak(logins, AS_OF, True)
pb = current_streak(logins, AS_OF, False)
pd.testing.assert_frame_equal(pa, a, check_dtype=False)   # ordered by user_id
pd.testing.assert_frame_equal(pb, b, check_dtype=False)
print("pandas equals SQL for both rules (ordered by user_id): True")

# different as-of date, same data: 2024-03-08 (user 3's long streak just ended on 03-07)
print("rule A as of 2024-03-08:", dict(zip(*[current_streak(logins, pd.Timestamp('2024-03-08'), True)[k] for k in ('user_id','current_streak')])))
print("asserts passed")
```

**Output (my run):**
```text
islands up to the as-of date:
 user_id streak_start streak_end  streak_days
       1   2024-03-20 2024-03-20            1
       2   2024-03-17 2024-03-18            2
       3   2024-03-01 2024-03-07            7
       3   2024-03-19 2024-03-20            2
       4   2024-03-17 2024-03-19            3
       5   2024-03-19 2024-03-20            2
current streak as of 2024-03-20:
 user_id  end_asof_or_day_before  end_on_asof_only  wrong_no_cutoff  wrong_longest
       1                       1                 1                1              1
       2                       0                 0                0              2
       3                       2                 2                2              7
       4                       3                 0                3              3
       5                       2                 2                4              2
       6                       0                 0                0              0
pandas equals SQL for both rules (ordered by user_id): True
rule A as of 2024-03-08: {1: 0, 2: 0, 3: 7, 4: 0, 5: 0, 6: 0}
asserts passed
```

**Edge cases:**
- As-of-date-only user (U1): one island of length 1, reported as 1 under both rules.
- Last login two days before (U2): 0 under both rules, because 03-18 is neither the as-of date nor the day before it.
- Earlier longer streak (U3): the 7-day island is ignored; the `wrong_longest` column shows what you get if you take the maximum island instead (7 for U3, and even 2 for U2).
- Last login the day before (U4): 3 under rule A, 0 under rule B. That one user is the entire difference between the rules.
- Rows after the as-of date (U5): without the cut-off the answer is 4 instead of 2. A fixed as-of date always needs the `<=` filter, or reruns on a growing table change the answer.
- Duplicate row on 03-20 (U3): the `DISTINCT` removes it; without it the day count and the row-number key are both wrong.
- NULL-only user (U6): the user list comes from all rows including the NULL, so U6 is reported with 0; if you want only users with at least one valid login, build the user list from the filtered CTE (then U6 has no row).
- Single-row user: handled (U1).
- Unsorted input: handled by the window `ORDER BY` and the pandas sort.
- At most one island can satisfy "end is the as-of date or the day before", because islands are separated by at least a 1 day gap of missing days, so the join does not duplicate users.
- I also ran rule A with the as-of date moved to 2024-03-08 on the same data: U3 reported 7 (its first streak ended 03-07, the day before). The as-of date is a parameter, not `date('now')`.

**Then explain:**
- Current streak is "the island that is still alive at the as-of date". The one condition `end >= as_of - 1` (or `= as_of`) selects it from the islands.
- Users with no current streak: either leave them out (inner join) or report 0 (left join from the user list). I show 0 and say that the other is also acceptable.
- A common shortcut, `COUNT(*)` of logins after the last gap, is the same idea; the island version is easier to explain and reuse for longest streak (Q21).
- Dialects, not executed here: PostgreSQL would use `login_date - ROW_NUMBER() OVER (...)::int` on a `DATE` column; MySQL `DATE_SUB(login_date, INTERVAL rn DAY)`; BigQuery `DATE_SUB(login_date, INTERVAL rn DAY)`. I did not run these.

**Follow-ups:**
- What about time zones? The streak is in the user's local calendar date; convert before taking the date.
- Current streak for every day of a month, not just one as-of date? Run the same logic per as-of date from a date spine (Q19), or compute islands once and join to the spine.
- Longest streak ever versus current? Longest is the `MAX` over islands (Q21); current is the island at the as-of date.

**Common mistakes:**
- Using `date('now')` as the as-of date, so the answer changes every day and cannot be tested.
- Forgetting the `<= as_of` filter.
- Reporting the longest island instead of the current one.
- Not saying whether yesterday counts (rule A) or only today (rule B).
- Inner join, then claiming users with 0 streak do not exist.

### Q16 ⭐⭐⭐ 🔴 Merge overlapping date ranges: bookings(room_id, start_date, end_date) with inclusive ISO dates. Return the merged continuous blocks per room (room_id, block_start, block_end). Use the sort by start, running MAX(end_date) over the previous rows (ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), a new-block flag when start is greater than that running max, and a running SUM of the flag. Cover a fully contained range (it must not shrink the end), ranges that touch (end = next start, merge) and ranges one day apart (adjacent but not overlapping; state your rule).
**Asked at:** oneuptime interval-merge write-up (opened; running max of end, strict > so touching intervals merge) and the DataDriven 'The Overlap' interval-merge problem (opened; a Python problem, labelled hard and L5, no company named); practice-site material and not candidate reports; data scientist and data engineer rounds
**Say this first (1 line):** Sort each room's ranges by start, compute the running maximum end date over the previous rows only, start a new block when a range starts after that maximum (strict `>`, so touching ranges merge), number the blocks with a running `SUM` of the flag, and take `MIN(start)` and `MAX(end)` per block.

**Rule I assume:** dates are inclusive. Overlapping ranges and ranges that touch (end 03-05, next start 03-05) merge. Ranges one day apart (end 03-08, next start 03-09) are adjacent but not overlapping, so I keep them separate (rule A); rule B, which merges adjacent days as well (useful for "continuous occupancy"), is `start > date(prev_max, '+1 day')`. Both are run below; I would ask which one the business wants.

**Schema and sample data:** twelve rows, four rooms, loaded unsorted. Room 1 has a contained range (03-02 to 03-03 inside 03-01 to 03-05), a touching range (03-05 to 03-08 starts on the end day of 03-01 to 03-05), a range one day apart (03-09 to 03-10 right after 03-08) and a separate far range (03-15 to 03-16). Room 2 has one single-day booking. Room 3 has an exact duplicate row, a row with a NULL end date and an inverted row (end before start). Room 4 has two ranges with the same start (03-01 to 03-03 and 03-01 to 03-10). Dates are ISO text, so string comparison orders them correctly.
```sql
CREATE TABLE bookings(room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-09','2024-03-10'),
 (1,'2024-03-05','2024-03-08'),
 (1,'2024-03-01','2024-03-05'),
 (1,'2024-03-02','2024-03-03'),
 (1,'2024-03-15','2024-03-16'),
 (2,'2024-03-01','2024-03-01'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-11',NULL),
 (3,'2024-03-20','2024-03-18'),
 (4,'2024-03-01','2024-03-03'),
 (4,'2024-03-01','2024-03-10');
```

**SQL answer:** `SQL_MAIN` in the Code block (rule A). Bad rows (NULL start or end, end before start) are excluded in the first CTE and I say so; the running `MAX` frame is `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`, which runs on SQLite 3.45.1 and gives NULL on the first row of each room:
```sql
WITH b AS (
  SELECT room_id, start_date, end_date
  FROM bookings
  WHERE start_date IS NOT NULL AND end_date IS NOT NULL AND end_date >= start_date
), m AS (
  SELECT room_id, start_date, end_date,
         MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM b
), f AS (
  SELECT *, CASE WHEN prev_max IS NULL OR start_date > prev_max THEN 1 ELSE 0 END AS new_block
  FROM m
), g AS (
  SELECT *, SUM(new_block) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block_id
  FROM f
)
SELECT room_id, MIN(start_date) AS block_start, MAX(end_date) AS block_end
FROM g
GROUP BY room_id, block_id
ORDER BY room_id, block_start
```
Rule B is the same text with `start_date > date(prev_max, '+1 day')` (`SQL_ADJ` in the Code block). `SQL_LAG` replaces the running max by `LAG(end_date)` to show the bug.

**pandas answer:** shown once here and identical to the Code block. `cummax()` inside `groupby` is the running maximum, and the second `groupby(...).shift()` makes it "previous rows only":
```py
    d = bookings.dropna(subset=["start_date", "end_date"]).copy()
    d["start_date"] = pd.to_datetime(d["start_date"])
    d["end_date"] = pd.to_datetime(d["end_date"])
    d = d[d["end_date"] >= d["start_date"]].sort_values(["room_id", "start_date", "end_date"])
    prev_max = d.groupby("room_id")["end_date"].cummax().groupby(d["room_id"]).shift()
    slack = pd.Timedelta(days=1) if adjacent else pd.Timedelta(0)
    new_block = prev_max.isna() | (d["start_date"] > prev_max + slack)
    d["block_id"] = new_block.astype(int).groupby(d["room_id"]).cumsum()
    out = d.groupby(["room_id", "block_id"], as_index=False).agg(
        block_start=("start_date", "min"), block_end=("end_date", "max"))
    
```

**Example:** room 1 sorted by start: A 03-01 to 03-05, B 03-02 to 03-03, C 03-05 to 03-08, D 03-09 to 03-10, E 03-15 to 03-16.
- Previous running max end: A none, B 03-05, C 03-05 (B did not shrink it), D 03-08, E 03-10.
- Flag (start > previous max): A 1 (first), B 0 (03-02 is not after 03-05), C 0 (03-05 is not after 03-05: touching merges), D 1 under rule A (03-09 is after 03-08), E 1 (03-15 is after 03-10).
- Blocks: A, B and C together are 03-01 to 03-08; D alone is 03-09 to 03-10; E alone is 03-15 to 03-16.
- Rule B: D's start is not after 03-08 plus one day (03-09), flag 0, so room 1 becomes 03-01 to 03-10 and 03-15 to 03-16.
- Room 4: sorted by start then end: 03-01 to 03-03, then 03-01 to 03-10, one block 03-01 to 03-10. Room 3: the duplicate merges into one block 03-10 to 03-12; the NULL-end and inverted rows are excluded.

**Code:** run with `python3 -I`. The asserts compare pandas with SQL for both rules after ordering by `room_id, block_start`.
```python
# Q16: merge overlapping inclusive date ranges: running MAX(end) over previous rows, flag, running SUM
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE bookings(room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-09','2024-03-10'),
 (1,'2024-03-05','2024-03-08'),
 (1,'2024-03-01','2024-03-05'),
 (1,'2024-03-02','2024-03-03'),
 (1,'2024-03-15','2024-03-16'),
 (2,'2024-03-01','2024-03-01'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-11',NULL),
 (3,'2024-03-20','2024-03-18'),
 (4,'2024-03-01','2024-03-03'),
 (4,'2024-03-01','2024-03-10');
"""
SQL_MAIN = """
WITH b AS (
  SELECT room_id, start_date, end_date
  FROM bookings
  WHERE start_date IS NOT NULL AND end_date IS NOT NULL AND end_date >= start_date
), m AS (
  SELECT room_id, start_date, end_date,
         MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM b
), f AS (
  SELECT *, CASE WHEN prev_max IS NULL OR start_date > prev_max THEN 1 ELSE 0 END AS new_block
  FROM m
), g AS (
  SELECT *, SUM(new_block) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block_id
  FROM f
)
SELECT room_id, MIN(start_date) AS block_start, MAX(end_date) AS block_end
FROM g
GROUP BY room_id, block_id
ORDER BY room_id, block_start
"""
# rule B: ranges one day apart (end 03-10, next start 03-11) also merge
SQL_ADJ = SQL_MAIN.replace("start_date > prev_max", "start_date > date(prev_max, '+1 day')")
assert SQL_ADJ != SQL_MAIN
# wrong: compare with the previous row's end (LAG) instead of the running max
SQL_LAG = SQL_MAIN.replace(
    """MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)""",
    "LAG(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date)")
assert SQL_LAG != SQL_MAIN
# NULL end_date read as open-ended instead of excluded
SQL_OPEN = SQL_MAIN.replace("end_date IS NOT NULL AND end_date >= start_date", "1 = 1") \
                   .replace("end_date\n  FROM bookings", "COALESCE(end_date, '9999-12-31') AS end_date\n  FROM bookings")
assert SQL_OPEN != SQL_MAIN
SQL_DETAIL = """
SELECT room_id, start_date, end_date,
       MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
FROM bookings WHERE room_id = 1 ORDER BY start_date, end_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("room 1 running max of the previous rows' end_date:"); print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
print("rule A, merge when start <= running max end (touching merges, one day apart does not):"); print(a.to_string(index=False))
b = pd.read_sql_query(SQL_ADJ, con)
print("rule B, also merge ranges one day apart:"); print(b.to_string(index=False))
print("wrong, LAG(end_date) instead of running max, room 1 and 4:")
print(pd.read_sql_query(SQL_LAG, con).query("room_id in (1, 4)").to_string(index=False))
print("NULL end_date treated as open-ended (room 3):")
print(pd.read_sql_query(SQL_OPEN, con).query("room_id == 3").to_string(index=False))

bookings = pd.read_sql_query("SELECT * FROM bookings", con)

def merge_ranges(bookings, adjacent=False):
    # pd:main
    d = bookings.dropna(subset=["start_date", "end_date"]).copy()
    d["start_date"] = pd.to_datetime(d["start_date"])
    d["end_date"] = pd.to_datetime(d["end_date"])
    d = d[d["end_date"] >= d["start_date"]].sort_values(["room_id", "start_date", "end_date"])
    prev_max = d.groupby("room_id")["end_date"].cummax().groupby(d["room_id"]).shift()
    slack = pd.Timedelta(days=1) if adjacent else pd.Timedelta(0)
    new_block = prev_max.isna() | (d["start_date"] > prev_max + slack)
    d["block_id"] = new_block.astype(int).groupby(d["room_id"]).cumsum()
    out = d.groupby(["room_id", "block_id"], as_index=False).agg(
        block_start=("start_date", "min"), block_end=("end_date", "max"))
    # pd:end
    out = out.drop(columns="block_id")
    for c in ("block_start", "block_end"):
        out[c] = out[c].dt.strftime("%Y-%m-%d")
    return out.sort_values(["room_id", "block_start"]).reset_index(drop=True)

pd.testing.assert_frame_equal(merge_ranges(bookings, False), a, check_dtype=False)   # ordered by room_id, block_start
pd.testing.assert_frame_equal(merge_ranges(bookings, True), b, check_dtype=False)
print("pandas equals SQL for both rules (ordered by room_id, block_start): True")
print("asserts passed")
```

**Output (my run):**
```text
room 1 running max of the previous rows' end_date:
 room_id start_date   end_date   prev_max
       1 2024-03-01 2024-03-05        NaN
       1 2024-03-02 2024-03-03 2024-03-05
       1 2024-03-05 2024-03-08 2024-03-05
       1 2024-03-09 2024-03-10 2024-03-08
       1 2024-03-15 2024-03-16 2024-03-10
rule A, merge when start <= running max end (touching merges, one day apart does not):
 room_id block_start  block_end
       1  2024-03-01 2024-03-08
       1  2024-03-09 2024-03-10
       1  2024-03-15 2024-03-16
       2  2024-03-01 2024-03-01
       3  2024-03-10 2024-03-12
       4  2024-03-01 2024-03-10
rule B, also merge ranges one day apart:
 room_id block_start  block_end
       1  2024-03-01 2024-03-10
       1  2024-03-15 2024-03-16
       2  2024-03-01 2024-03-01
       3  2024-03-10 2024-03-12
       4  2024-03-01 2024-03-10
wrong, LAG(end_date) instead of running max, room 1 and 4:
 room_id block_start  block_end
       1  2024-03-01 2024-03-05
       1  2024-03-05 2024-03-08
       1  2024-03-09 2024-03-10
       1  2024-03-15 2024-03-16
       4  2024-03-01 2024-03-10
NULL end_date treated as open-ended (room 3):
 room_id block_start  block_end
       3  2024-03-10 9999-12-31
pandas equals SQL for both rules (ordered by room_id, block_start): True
asserts passed
```

**Edge cases:**
- Contained range (B): the running max stayed 03-05 after B, shown in the detail table (`prev_max` for C is 03-05, not 03-03). Using `LAG(end_date)` instead (the wrong version in the output) compares C with B's end 03-03, so C looks like a new block and room 1 comes out as `03-01 to 03-05` and `03-05 to 03-08`, two blocks that touch and should be one.
- Touching (C starts on A's end day): merged under strict `>`. With `>=` they would split, the opposite of what inclusive dates mean.
- One day apart (D): separate under rule A, merged under rule B, and the two outputs differ for room 1 (three blocks versus two).
- Same start (room 4): ordering by `start_date, end_date` makes the shorter range first; the long one then has start equal to the previous max start, so it merges either way. The result does not depend on the tie order, but the frame must still list all previous rows.
- Exact duplicate rows (room 3): merge into one block, no special handling.
- NULL end: `MAX` ignores NULLs and `NULL >= start` is not true, so I exclude NULL rows explicitly. If NULL means "still open", treat it as a far-future date: in my run that turned room 3 into the single block `03-10 to 9999-12-31` (and that variant also stopped excluding the inverted row). Say which meaning you take.
- Single-range room (room 2): `prev_max` NULL, one block.
- Unsorted input: handled by the window `ORDER BY`.
- Inverted rows (end before start) are data errors; I filter them, you might instead report them.

**Then explain:**
- Why a running max and not the previous end: a long range can swallow several short ones, so the end to compare against is the largest end seen so far, not the last one.
- Why the frame stops one row before the current one: the test is "does this range start after everything that came before it?". The first row of each room then has an empty frame, `prev_max` is NULL, and that NULL is the "new block" signal.
- The running `SUM` of the flag numbers the blocks (running-total mechanics are Part 5); `MIN` and `MAX` per block give the merged range.
- Dialects, not executed here: PostgreSQL and MySQL 8 accept the same frame text, and PostgreSQL's date arithmetic would be `prev_max + 1`; MySQL 5.7 has no window functions; BigQuery would use `DATE_ADD(prev_max, INTERVAL 1 DAY)`. An engine without window frames needs a self-join or a recursive CTE (pointer to Part 9). None of this was executed.

**Follow-ups:**
- Total booked days per room after merging? `SUM(julianday(block_end) - julianday(block_start) + 1)` over the blocks (inclusive end adds one).
- Find double-bookings instead of merging them? A self-join where `a.start <= b.end AND b.start <= a.end AND a.rowid < b.rowid`.
- Why not just group by room and take min/max? That would join separate blocks into one range.

**Common mistakes:**
- `LAG(end_date)` instead of a running max (a contained range then shrinks the block).
- `>=` in the flag, which splits ranges that touch.
- Not stating whether one-day-apart ranges merge.
- Forgetting the first row's NULL, so the first range of each room never starts a block.
- Not sorting by start inside each room, or sorting by end.
- Comparing the new range's start with the maximum of start dates (or with its own end) instead of the maximum end of earlier rows.

### Q17 ⭐⭐⭐ 🔴 Maximum concurrent users: sessions(user_id, login_ts, logout_ts). Return the peak number of simultaneous sessions and the time it first occurs, using a +1/-1 event sweep: UNION ALL of (login_ts, +1) and (logout_ts, -1), a running SUM over time ordered so that at identical timestamps the -1 comes before the +1 (state why, and what the other order does to back-to-back sessions), then MAX. Show the answer on a small table with a session ending exactly when another starts.
**Asked at:** Itzik Ben-Gan interval packing and gaps-and-islands articles (search snippets only, not opened) and the Oracle SQL blog on longest and current streaks (snippet only); guides and not candidate reports; senior analyst and data engineer rounds
**Say this first (1 line):** Turn every session into two events, +1 at login and -1 at logout, sort all events by time with the -1 before the +1 at the same timestamp, take a running `SUM`, and the maximum of that running sum is the peak; the earliest time it reaches the peak is when it first occurs.

**Rule I assume:** a session is open from its login up to, but not including, its logout (half-open). A session that ends at 10:00:00 and another that starts at 10:00:00 do not overlap, so they must not count as 2 at that instant; that is why the -1 sorts first.

**Schema and sample data:** seven rows. User 1 is 09:00 to 10:00, user 2 is 09:30 to 10:30, user 3 is 10:00 to 11:00 (starts exactly when user 1 ends, the back-to-back case), user 4 is 10:40 to 10:50, user 5 logged in at 12:00 and has not logged out (NULL logout, still open), user 6 logs in and out at 13:00:00 (zero length), user 7 has a NULL login (bad row). Rows are not in time order. Timestamps are ISO text.
```sql
CREATE TABLE sessions(user_id INTEGER, login_ts TEXT, logout_ts TEXT);
INSERT INTO sessions VALUES
 (3,'2024-03-01 10:00:00','2024-03-01 11:00:00'),
 (1,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (2,'2024-03-01 09:30:00','2024-03-01 10:30:00'),
 (4,'2024-03-01 10:40:00','2024-03-01 10:50:00'),
 (5,'2024-03-01 12:00:00',NULL),
 (6,'2024-03-01 13:00:00','2024-03-01 13:00:00'),
 (7,NULL,'2024-03-01 14:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block. `ORDER BY ts, delta` puts -1 (smaller number) before +1 at the same timestamp; the frame is written out as `ROWS`:
```sql
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions WHERE login_ts IS NOT NULL
  UNION ALL
  SELECT logout_ts, -1 FROM sessions WHERE login_ts IS NOT NULL AND logout_ts IS NOT NULL
), run AS (
  SELECT ts, delta,
         SUM(delta) OVER (ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
  FROM ev
)
SELECT concurrent AS peak, MIN(ts) AS first_time
FROM run
WHERE concurrent = (SELECT MAX(concurrent) FROM run)
```
`SQL_PLUS_FIRST` is the same text with `delta DESC` (+1 first), `SQL_TS_ONLY` orders by `ts` only with a `ROWS` frame, and `SQL_RANGE` orders by `ts` only with the default frame.

**pandas answer:** shown once here and identical to the Code block. Both sort keys are given, so the order of the two concatenated halves does not matter:
```py
s = sessions.dropna(subset=["login_ts"])
ev = pd.concat([
    pd.DataFrame({"ts": s["login_ts"], "delta": 1}),
    pd.DataFrame({"ts": s["logout_ts"], "delta": -1}).dropna(subset=["ts"]),
])
ev["ts"] = pd.to_datetime(ev["ts"])
ev = ev.sort_values(["ts", "delta"], kind="stable").reset_index(drop=True)
ev["concurrent"] = ev["delta"].cumsum()
peak = ev["concurrent"].max()
first_time = ev.loc[ev["concurrent"] == peak, "ts"].min().strftime("%Y-%m-%d %H:%M:%S")
```

**Example:** the sorted events and running count are in the first block of the output.
- 09:00 +1 gives 1; 09:30 +1 gives 2.
- 10:00 has two events: -1 (user 1 leaves) then +1 (user 3 joins): 2 to 1 to 2. At no instant are three people in.
- 10:30 -1 gives 1; 10:40 +1 gives 2 (user 3 and user 4); 10:50 -1 gives 1; 11:00 -1 gives 0; 12:00 +1 gives 1 (user 5, never closed).
- Peak is 2, first reached at 09:30:00. An independent check that counts, for each login time, the sessions with `login <= t < logout` also gave 2.
- With +1 first at 10:00 the running count goes 2, 3, 2: it reports a peak of 3 at 10:00:00 that never happened.

**Code:** run with `python3 -I`. The assert compares the single result row (peak and first time) of pandas with SQL, so no row order is involved.
```python
# Q17: maximum concurrent sessions with a +1/-1 event sweep; -1 before +1 at identical timestamps
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sessions(user_id INTEGER, login_ts TEXT, logout_ts TEXT);
INSERT INTO sessions VALUES
 (3,'2024-03-01 10:00:00','2024-03-01 11:00:00'),
 (1,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (2,'2024-03-01 09:30:00','2024-03-01 10:30:00'),
 (4,'2024-03-01 10:40:00','2024-03-01 10:50:00'),
 (5,'2024-03-01 12:00:00',NULL),
 (6,'2024-03-01 13:00:00','2024-03-01 13:00:00'),
 (7,NULL,'2024-03-01 14:00:00');
"""
SQL_MAIN = """
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions WHERE login_ts IS NOT NULL
  UNION ALL
  SELECT logout_ts, -1 FROM sessions WHERE login_ts IS NOT NULL AND logout_ts IS NOT NULL
), run AS (
  SELECT ts, delta,
         SUM(delta) OVER (ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
  FROM ev
)
SELECT concurrent AS peak, MIN(ts) AS first_time
FROM run
WHERE concurrent = (SELECT MAX(concurrent) FROM run)
"""
# wrong order at identical timestamps: +1 before -1
SQL_PLUS_FIRST = SQL_MAIN.replace("ORDER BY ts, delta ROWS", "ORDER BY ts, delta DESC ROWS")
assert SQL_PLUS_FIRST != SQL_MAIN
# ties left to the engine: ORDER BY ts only with a ROWS frame
SQL_TS_ONLY = SQL_MAIN.replace("ORDER BY ts, delta ROWS", "ORDER BY ts ROWS")
assert SQL_TS_ONLY != SQL_MAIN
# ORDER BY ts only with the default RANGE frame: tied rows are peers and are added together
SQL_RANGE = SQL_MAIN.replace("ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW", "ORDER BY ts")
assert SQL_RANGE != SQL_MAIN
SQL_TRACE = """
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions WHERE login_ts IS NOT NULL
  UNION ALL
  SELECT logout_ts, -1 FROM sessions WHERE login_ts IS NOT NULL AND logout_ts IS NOT NULL
)
SELECT ts, delta,
       SUM(delta) OVER (ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
FROM ev ORDER BY ts, delta
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("event sweep, -1 before +1 at the same timestamp:"); print(pd.read_sql_query(SQL_TRACE, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
print("SQL_MAIN:", a.values.tolist())
print("wrong, +1 before -1 at ties:", pd.read_sql_query(SQL_PLUS_FIRST, con).values.tolist())
print("ORDER BY ts only, ROWS frame (ties left to the engine):", pd.read_sql_query(SQL_TS_ONLY, con).values.tolist())
print("ORDER BY ts only, default RANGE frame:", pd.read_sql_query(SQL_RANGE, con).values.tolist())
print("independent check, sessions open at each login time (login <= t < logout): peak sessions =",
      con.execute("SELECT MAX(c) FROM (SELECT (SELECT COUNT(*) FROM sessions o WHERE o.login_ts <= s.login_ts "
                  "AND (o.logout_ts IS NULL OR o.logout_ts > s.login_ts)) AS c FROM sessions s WHERE s.login_ts IS NOT NULL)").fetchone()[0])

sessions = pd.read_sql_query("SELECT * FROM sessions", con)
# pd:main
s = sessions.dropna(subset=["login_ts"])
ev = pd.concat([
    pd.DataFrame({"ts": s["login_ts"], "delta": 1}),
    pd.DataFrame({"ts": s["logout_ts"], "delta": -1}).dropna(subset=["ts"]),
])
ev["ts"] = pd.to_datetime(ev["ts"])
ev = ev.sort_values(["ts", "delta"], kind="stable").reset_index(drop=True)
ev["concurrent"] = ev["delta"].cumsum()
peak = ev["concurrent"].max()
first_time = ev.loc[ev["concurrent"] == peak, "ts"].min().strftime("%Y-%m-%d %H:%M:%S")
# pd:end
print("pandas:", [int(peak), first_time])
assert [int(peak), first_time] == a.values.tolist()[0]   # one row, no ordering needed
print("running value right after the zero-length session's -1 at 13:00:", int(ev.loc[(ev.ts == "2024-03-01 13:00:00") & (ev.delta == -1), "concurrent"].iloc[0]))

# empty table
con.execute("DELETE FROM sessions")
print("empty table, SQL rows returned:", con.execute(SQL_MAIN).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
event sweep, -1 before +1 at the same timestamp:
                 ts  delta  concurrent
2024-03-01 09:00:00      1           1
2024-03-01 09:30:00      1           2
2024-03-01 10:00:00     -1           1
2024-03-01 10:00:00      1           2
2024-03-01 10:30:00     -1           1
2024-03-01 10:40:00      1           2
2024-03-01 10:50:00     -1           1
2024-03-01 11:00:00     -1           0
2024-03-01 12:00:00      1           1
2024-03-01 13:00:00     -1           0
2024-03-01 13:00:00      1           1
SQL_MAIN: [[2, '2024-03-01 09:30:00']]
wrong, +1 before -1 at ties: [[3, '2024-03-01 10:00:00']]
ORDER BY ts only, ROWS frame (ties left to the engine): [[3, '2024-03-01 10:00:00']]
ORDER BY ts only, default RANGE frame: [[2, '2024-03-01 09:30:00']]
independent check, sessions open at each login time (login <= t < logout): peak sessions = 2
pandas: [2, '2024-03-01 09:30:00']
running value right after the zero-length session's -1 at 13:00: 0
empty table, SQL rows returned: [(None, None)]
asserts passed
```

**Edge cases:**
- Back-to-back sessions: correct order gives peak 2 at 09:30; the wrong order gives peak 3 at 10:00:00, both in my run.
- `ORDER BY ts` only with a `ROWS` frame leaves the order of the tied events to the engine; in this run it also gave the wrong 3 at 10:00:00 (the `+1` rows come from the first branch of the `UNION ALL`, so they came first here). Not guaranteed either way, so name the tie-break.
- `ORDER BY ts` only with the default `RANGE` frame treats tied rows as peers and adds them together, so the +1 and -1 at 10:00 net out; it gave the right answer (2 at 09:30). It works, but it relies on the default frame and hides the rule; I prefer the explicit `ts, delta` with `ROWS`.
- Still-open session (NULL logout): only a +1 event, no -1, so it stays open forever; user 5 is counted from 12:00 on. If instead open sessions should be cut at an as-of time, `COALESCE(logout_ts, as_of)` with a fixed as-of value (never now).
- Zero-length session (user 6): its -1 sorts before its own +1, so the running count dips by one at 13:00 (0 in my run, while user 5 is still open) and returns to 1. Under the half-open rule a zero-length session is open for no time, so ignoring it is consistent; the peak is unaffected unless a peak coincides with such a session. If you count it, sort by session instead.
- NULL login (user 7): excluded; its logout alone would produce a -1 with no +1 and a negative count.
- Same user with overlapping sessions (two tabs) counts twice; if the question is "distinct users online", a plain sweep is not enough (dedupe the user's overlapping sessions first, for example with the interval merge in Q16).
- Several moments with the same peak: the query returns the earliest. Empty table: SQL returned one row with NULL peak and NULL time in my run (the aggregate without `GROUP BY` always returns a row).
- Time zones: the events must all be in the same zone (UTC); SQLite stores text, no conversion here.

**Then explain:**
- The sweep is a running total over +1 and -1; the running sum after an event is the number of open sessions right after that event.
- Order at ties: ends first when the interval is half-open. If sessions were closed intervals (logout inclusive), the right order would be +1 first, so "state your convention" is the real answer.
- Peak versus when: `MAX(concurrent)` is the peak; the time is the minimum `ts` among events whose running count equals the peak. Because within a tie the -1 comes first, the running count at an intermediate row is never inflated.
- Compare with the self-join check: for each login time, count sessions with `login <= t AND logout > t`; same answer, O(n squared), fine for a check, slower on big data.
- Dialects, not executed here: the same query runs on PostgreSQL and MySQL 8 as written; BigQuery would need `ROWS` in the same form; on MySQL 5.7 there are no window functions, and a correlated count is the fallback.

**Follow-ups:**
- Peak per day or per hour? Partition the sweep (and cut sessions that cross midnight into two pieces).
- How long was the system at the peak level? Use `LEAD(ts)` over the events and sum the time where the count equals the peak.
- Count per minute for a chart? Join a date spine (Q19) to the sessions with `login <= minute AND logout > minute`.

**Common mistakes:**
- Putting +1 before -1 at the same timestamp (shown above: peak 3 at 10:00:00 instead of 2).
- Leaving the tie order to the engine.
- Excluding NULL-logout rows, which silently drops people still online.
- Counting a session twice because of `UNION` instead of `UNION ALL` (identical rows would collapse).
- Reporting the peak without saying whether the interval is half-open.

### Q18 ⭐⭐ 🟢 Consecutive Available Seats (LeetCode 603): cinema(seat_id, free) with free as 0 or 1, seat ids ordered. Return the seat ids of free seats that have an adjacent free seat, ordered by seat_id. Show the self join, a LAG/LEAD version, and the island version that finds runs of at least 2 free seats; say what each does with ids that have gaps and with a free seat at the first or last position.
**Asked at:** public LeetCode-style problem bank (statements known from search snippets and mirrors such as doocs, walkccc and talentd; the leetcode.com pages returned HTTP 403 and were not opened), not candidate reports; analyst, data scientist and data engineer screens at product companies and GCCs
**Say this first (1 line):** A free seat qualifies if the seat with id minus 1 or id plus 1 is also free; the self join says that directly with `ABS(a.seat_id - b.seat_id) = 1`, the `LAG`/`LEAD` version must also check that the neighbouring row's id really is id plus or minus 1, and the island version keeps free seats whose `seat_id - ROW_NUMBER()` group has at least 2 members.

**Schema and sample data:** thirteen rows loaded unsorted (seat 14 first). Free runs: seats 1 and 2 (the first position), seat 4 alone, seats 6, 7, 8 (a run of three), seat 10 has a NULL `free` (unknown), seat 11 is free but its neighbours are seat 10 (NULL) and a missing seat 12, seats 13 and 14 (the last position). Seat 12 does not exist in the table, so ids have a gap between 11 and 13. The statement of LeetCode 603 (premium; I did not open the page) is, as I remember it, `cinema(seat_id, free)` with seat ids in order and free 0 or 1; I do not rely on there being no gaps, and the data above has one.
```sql
CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER);
INSERT INTO cinema VALUES
 (14,1),(1,1),(2,1),(3,0),(4,1),(5,0),(6,1),(7,1),(8,1),(9,0),(10,NULL),(11,1),(13,1);
```
Expected by hand: 1, 2, 6, 7, 8, 13, 14.

**SQL answer:** three versions in the Code block. Self join (`SQL_JOIN`):
```sql
SELECT DISTINCT a.seat_id
FROM cinema a
JOIN cinema b ON ABS(a.seat_id - b.seat_id) = 1
WHERE a.free = 1 AND b.free = 1
ORDER BY a.seat_id
```
`LAG`/`LEAD` with the id check (`SQL_LAGLEAD`):
```sql
WITH x AS (
  SELECT seat_id, free,
         LAG(seat_id)  OVER (ORDER BY seat_id) AS prev_id,
         LAG(free)     OVER (ORDER BY seat_id) AS prev_free,
         LEAD(seat_id) OVER (ORDER BY seat_id) AS next_id,
         LEAD(free)    OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id
FROM x
WHERE free = 1
  AND ((prev_free = 1 AND prev_id = seat_id - 1) OR (next_free = 1 AND next_id = seat_id + 1))
ORDER BY seat_id
```
Island version (`SQL_ISLAND`), filtering to free seats first so the row numbers count only free seats:
```sql
WITH f AS (
  SELECT seat_id, seat_id - ROW_NUMBER() OVER (ORDER BY seat_id) AS grp
  FROM cinema
  WHERE free = 1
)
SELECT seat_id
FROM f
WHERE grp IN (SELECT grp FROM f GROUP BY grp HAVING COUNT(*) >= 2)
ORDER BY seat_id
```
`SQL_NAIVE` in the Code block is the `LAG`/`LEAD` version without the id check, to show the bug.

**pandas answer:** neighbour version and island version, shown once here and identical to the Code block:
```py
c = cinema.sort_values("seat_id").reset_index(drop=True)
is_free = c["free"].eq(1)                      # NULL counts as not free
prev_adj = is_free.shift(fill_value=False) & (c["seat_id"].diff() == 1)
next_adj = is_free.shift(-1, fill_value=False) & (c["seat_id"].diff(-1) == -1)
pd_neighbor = c.loc[is_free & (prev_adj | next_adj), "seat_id"].tolist()
f = c[is_free]
key = f["seat_id"] - range(len(f))
pd_island = f.loc[key.groupby(key).transform("size") >= 2, "seat_id"].tolist()
```

**Example:** free seats are 1, 2, 4, 6, 7, 8, 11, 13, 14.
- Self join: pairs of free seats whose ids differ by 1 are (1,2), (6,7), (7,8), (13,14), each in both directions; the distinct seat ids are 1, 2, 6, 7, 8, 13, 14. Seat 4 has no free neighbour (3 and 5 are taken) and seat 11 has none (10 is NULL, 12 does not exist).
- Island: `seat_id - ROW_NUMBER()` over free seats only: seats 1, 2, 4, 6, 7, 8, 11, 13, 14 get row numbers 1 to 9, so the groups are 0, 0, 1, 2, 2, 2, 4, 5, 5. Group sizes are 2, 1, 3, 1, 2. Keep sizes of 2 or more: 1, 2, 6, 7, 8, 13, 14.
- Naive `LAG`/`LEAD` on rows: seat 11's next row is seat 13, which is free, so it wrongly qualifies.

**Code:** run with `python3 -I`. The asserts compare the three SQL versions, both pandas versions and the hand-written expected list, all ordered by `seat_id`; the naive version is asserted to differ.
```python
# Q18: Consecutive Available Seats (LeetCode 603 style): self join, LAG/LEAD, island version
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER);
INSERT INTO cinema VALUES
 (14,1),(1,1),(2,1),(3,0),(4,1),(5,0),(6,1),(7,1),(8,1),(9,0),(10,NULL),(11,1),(13,1);
"""
SQL_JOIN = """
SELECT DISTINCT a.seat_id
FROM cinema a
JOIN cinema b ON ABS(a.seat_id - b.seat_id) = 1
WHERE a.free = 1 AND b.free = 1
ORDER BY a.seat_id
"""
SQL_LAGLEAD = """
WITH x AS (
  SELECT seat_id, free,
         LAG(seat_id)  OVER (ORDER BY seat_id) AS prev_id,
         LAG(free)     OVER (ORDER BY seat_id) AS prev_free,
         LEAD(seat_id) OVER (ORDER BY seat_id) AS next_id,
         LEAD(free)    OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id
FROM x
WHERE free = 1
  AND ((prev_free = 1 AND prev_id = seat_id - 1) OR (next_free = 1 AND next_id = seat_id + 1))
ORDER BY seat_id
"""
SQL_ISLAND = """
WITH f AS (
  SELECT seat_id, seat_id - ROW_NUMBER() OVER (ORDER BY seat_id) AS grp
  FROM cinema
  WHERE free = 1
)
SELECT seat_id
FROM f
WHERE grp IN (SELECT grp FROM f GROUP BY grp HAVING COUNT(*) >= 2)
ORDER BY seat_id
"""
# wrong: LAG/LEAD on rows without checking that the ids are consecutive
SQL_NAIVE = """
WITH x AS (
  SELECT seat_id, free,
         LAG(free)  OVER (ORDER BY seat_id) AS prev_free,
         LEAD(free) OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id FROM x WHERE free = 1 AND (prev_free = 1 OR next_free = 1) ORDER BY seat_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for name, sql in (("self join", SQL_JOIN), ("LAG/LEAD with id check", SQL_LAGLEAD),
                  ("island (ids minus ROW_NUMBER)", SQL_ISLAND), ("naive LAG/LEAD, no id check", SQL_NAIVE)):
    res[name] = [r[0] for r in con.execute(sql)]
    print(f"{name}: {res[name]}")

cinema = pd.read_sql_query("SELECT * FROM cinema", con)
# pd:main
c = cinema.sort_values("seat_id").reset_index(drop=True)
is_free = c["free"].eq(1)                      # NULL counts as not free
prev_adj = is_free.shift(fill_value=False) & (c["seat_id"].diff() == 1)
next_adj = is_free.shift(-1, fill_value=False) & (c["seat_id"].diff(-1) == -1)
pd_neighbor = c.loc[is_free & (prev_adj | next_adj), "seat_id"].tolist()
f = c[is_free]
key = f["seat_id"] - range(len(f))
pd_island = f.loc[key.groupby(key).transform("size") >= 2, "seat_id"].tolist()
# pd:end
print("pandas neighbour version:", pd_neighbor)
print("pandas island version:", pd_island)
expected = [1, 2, 6, 7, 8, 13, 14]
assert res["self join"] == res["LAG/LEAD with id check"] == res["island (ids minus ROW_NUMBER)"] == expected
assert pd_neighbor == pd_island == expected   # all lists are ordered by seat_id
assert res["naive LAG/LEAD, no id check"] != expected
print("the naive version adds:", sorted(set(res["naive LAG/LEAD, no id check"]) - set(expected)))

# tiny cases: one seat, empty table, all free
for label, rows in (("single free seat", [(1, 1)]), ("empty table", []), ("all free, ids 5..7", [(5, 1), (6, 1), (7, 1)])):
    c2 = sqlite3.connect(":memory:")
    c2.execute("CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER)")
    c2.executemany("INSERT INTO cinema VALUES (?, ?)", rows)
    out = [[r[0] for r in c2.execute(s)] for s in (SQL_JOIN, SQL_LAGLEAD, SQL_ISLAND)]
    assert out[0] == out[1] == out[2]
    print(f"{label}: all three SQL versions return {out[0]}")
print("asserts passed")
```

**Output (my run):**
```text
self join: [1, 2, 6, 7, 8, 13, 14]
LAG/LEAD with id check: [1, 2, 6, 7, 8, 13, 14]
island (ids minus ROW_NUMBER): [1, 2, 6, 7, 8, 13, 14]
naive LAG/LEAD, no id check: [1, 2, 6, 7, 8, 11, 13, 14]
pandas neighbour version: [1, 2, 6, 7, 8, 13, 14]
pandas island version: [1, 2, 6, 7, 8, 13, 14]
the naive version adds: [11]
single free seat: all three SQL versions return []
empty table: all three SQL versions return []
all free, ids 5..7: all three SQL versions return [5, 6, 7]
asserts passed
```

**Edge cases:**
- Gaps in ids: the self join and the island version handle them for free (a missing id never matches `ABS(...) = 1`, and a missing id breaks the `seat_id - ROW_NUMBER()` group). `LAG`/`LEAD` compare the neighbouring row, not the neighbouring id, so they need the extra `prev_id = seat_id - 1` check; without it seat 11 was returned in my run.
- First and last positions: seat 1 has no `LAG` row (NULL), so `prev_free = 1` is not true, but `next_free = 1` can still make it qualify; seat 14 has no `LEAD` row. The `OR` handles both ends. The self join has no special case at the ends either.
- NULL `free` (seat 10): `free = 1` is not true for NULL, so it is treated as not free everywhere; seat 11 does not qualify through it. In pandas, `.eq(1)` returns False for NaN.
- Single free seat, empty table, all free (ids 5 to 7): all three SQL versions agreed (`[]`, `[]`, `[5, 6, 7]`).
- Unsorted input: window `ORDER BY` handles it; pandas sorts first.
- Duplicate seat ids cannot occur with the primary key; if the real table has them, dedupe first (not tested here).
- A `free` column stored as text `'1'` does not equal integer 1 in the join; keep the type clean.
- In pandas, `shift(-1, fill_value=False)` keeps the boolean dtype; a plain `shift()` on an integer column would give float with NaN.

**Then explain:**
- Self join: simple, quadratic in the worst case (it is an index lookup on `seat_id`, in practice fast); needs `DISTINCT` because a seat in the middle of a run matches twice.
- `LAG`/`LEAD`: one pass; remember it is row-based, so it is only correct if ids are consecutive or you check them.
- Islands: the one that generalises to "at least N consecutive free seats" (change `>= 2` to `>= N`), which is what LeetCode 601 style questions ask.
- The three agree on this data. Which to show first? The self join, because it reads like the statement; then say why `LAG`/`LEAD` needs the id check.
- Dialects, not executed here: the `ABS` self join runs on MySQL and PostgreSQL unchanged; the other two need window functions (MySQL 8 and later). I did not execute them.

**Follow-ups:**
- At least three consecutive free seats? Island version with `HAVING COUNT(*) >= 3`, or `LAG`/`LEAD` twice.
- Return the runs (start seat, end seat, length) instead of seat ids? `GROUP BY grp` with `MIN`, `MAX`, `COUNT`.
- What if seats are in rows and columns? Partition by row.

**Common mistakes:**
- `LAG`/`LEAD` without checking the id gap (shown above: seat 11 appears).
- Forgetting `DISTINCT` in the self join.
- Using the island trick without filtering to free seats first, so taken seats get row numbers and the group sizes change.
- Treating NULL as free, or comparing `free` as text.
- Ordering by anything other than `seat_id`.

### Q19 ⭐⭐ 🟢 Missing dates against a date spine: logins(user_id, login_date) over 2024-03-01 to 2024-03-10. Return for each user the days in the range with no login, building the spine with a recursive CTE (a pointer to Part 9) and a CROSS JOIN of users with the spine LEFT JOINed to logins, plus the compact form as missing ranges. Explain why the NOT EXISTS version and the LEFT JOIN with IS NULL version give the same rows, and the effect of a user with no logins at all.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Build a date spine for the range, `CROSS JOIN` it with the users to get every (user, day) pair that should exist, `LEFT JOIN` the logins and keep the rows where nothing matched; the compact form numbers the missing days per user and groups them with the same date-minus-`ROW_NUMBER` island trick.

**Schema and sample data:** a `users` table (4 users) and a `logins` table, range 2024-03-01 to 2024-03-10 (10 days). User 1 logged in on 01, 02 (twice), 03, 06, 07, 10 (inserted unsorted), so missing are 04, 05, 08, 09. User 2 has no logins at all. User 3 logged in all ten days. User 4 has one in-range login (03-05), two out-of-range logins (02-28 and 03-11) and a NULL date.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1),(2),(3),(4);
INSERT INTO logins VALUES
 (1,'2024-03-06'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-03'),(1,'2024-03-07'),(1,'2024-03-10'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-04'),(3,'2024-03-05'),
 (3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-08'),(3,'2024-03-09'),(3,'2024-03-10'),
 (4,'2024-03-05'),(4,'2024-02-28'),(4,'2024-03-11'),(4,NULL);
```

**SQL answer:** `SQL_LEFT` in the Code block, the date spine as a recursive CTE (it runs on SQLite 3.45.1; recursive CTEs in depth are Part 9) and the anti-join:
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
WHERE l.user_id IS NULL
ORDER BY u.user_id, s.d
```
`SQL_NOTEXISTS` in the Code block is the same with a `NOT EXISTS` subquery:
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
WHERE NOT EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.user_id AND l.login_date = s.d)
ORDER BY u.user_id, s.d
```
The compact form, `SQL_RANGES` in the Code block (the missing days become the "rows" for the island trick):
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
), m AS (
  SELECT u.user_id, s.d AS missing_date
  FROM users u
  CROSS JOIN spine s
  LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
  WHERE l.user_id IS NULL
), g AS (
  SELECT user_id, missing_date,
         date(missing_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY missing_date) || ' days') AS grp
  FROM m
)
SELECT user_id, MIN(missing_date) AS range_start, MAX(missing_date) AS range_end, COUNT(*) AS days_missing
FROM g
GROUP BY user_id, grp
ORDER BY user_id, range_start
```

**pandas answer:** shown once here and identical to the Code block (`date_range` is the spine, `from_product` the cross join, `merge(..., indicator=True)` plus `left_only` the anti-join):
```py
spine = pd.date_range("2024-03-01", "2024-03-10", freq="D")
grid = pd.MultiIndex.from_product([users["user_id"], spine], names=["user_id", "d"]).to_frame(index=False)
seen = logins.dropna(subset=["login_date"]).assign(d=lambda x: pd.to_datetime(x["login_date"]))[["user_id", "d"]].drop_duplicates()
m = grid.merge(seen, on=["user_id", "d"], how="left", indicator=True)
miss = m[m["_merge"] == "left_only"][["user_id", "d"]].sort_values(["user_id", "d"]).reset_index(drop=True)
miss["grp"] = (miss["d"] - pd.Timestamp("1970-01-01")).dt.days - miss.groupby("user_id").cumcount()
ranges = (miss.groupby(["user_id", "grp"], as_index=False)
              .agg(range_start=("d", "min"), range_end=("d", "max"), days_missing=("d", "size"))
              .drop(columns="grp"))
```

**Example:** user 1 in the spine of 10 days has logins on 01, 02, 03, 06, 07, 10, so the unmatched days are 04, 05, 08, 09. Numbering them 1, 2, 3, 4 and subtracting from the day: 04-1, 05-2 are the same group (consecutive), 08-3, 09-4 are the same group, different from the first. Ranges: 04 to 05 (2 days) and 08 to 09 (2 days). User 2: all 10 days missing, one range 03-01 to 03-10. User 3: none. User 4: only 03-05 matched, so ranges 03-01 to 03-04 (4 days) and 03-06 to 03-10 (5 days). The out-of-range dates and the NULL never match a spine day.

**Code:** run with `python3 -I`. The asserts compare the `LEFT JOIN` and `NOT EXISTS` results (equal frames), then pandas with SQL, ordered by `user_id, missing_date` (and `user_id, range_start` for ranges).
```python
# Q19: missing dates against a date spine (2024-03-01 to 2024-03-10), anti-join forms, compact ranges
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1),(2),(3),(4);
INSERT INTO logins VALUES
 (1,'2024-03-06'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-03'),(1,'2024-03-07'),(1,'2024-03-10'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-04'),(3,'2024-03-05'),
 (3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-08'),(3,'2024-03-09'),(3,'2024-03-10'),
 (4,'2024-03-05'),(4,'2024-02-28'),(4,'2024-03-11'),(4,NULL);
"""
SQL_LEFT = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
WHERE l.user_id IS NULL
ORDER BY u.user_id, s.d
"""
SQL_NOTEXISTS = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
WHERE NOT EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.user_id AND l.login_date = s.d)
ORDER BY u.user_id, s.d
"""
SQL_RANGES = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
), m AS (
  SELECT u.user_id, s.d AS missing_date
  FROM users u
  CROSS JOIN spine s
  LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
  WHERE l.user_id IS NULL
), g AS (
  SELECT user_id, missing_date,
         date(missing_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY missing_date) || ' days') AS grp
  FROM m
)
SELECT user_id, MIN(missing_date) AS range_start, MAX(missing_date) AS range_end, COUNT(*) AS days_missing
FROM g
GROUP BY user_id, grp
ORDER BY user_id, range_start
"""
# traps
SQL_NOTIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u CROSS JOIN spine s
WHERE s.d NOT IN (SELECT l.login_date FROM logins l WHERE l.user_id = u.user_id)
ORDER BY u.user_id, s.d
"""
SQL_USERS_FROM_LOGINS = SQL_LEFT.replace("FROM users u", "FROM (SELECT DISTINCT user_id FROM logins) u")
assert SQL_USERS_FROM_LOGINS != SQL_LEFT

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_LEFT, con)
b = pd.read_sql_query(SQL_NOTEXISTS, con)
pd.testing.assert_frame_equal(a, b)
print("missing days per user (LEFT JOIN ... IS NULL), counts:", a.groupby("user_id").size().to_dict())
print(a.groupby("user_id")["missing_date"].apply(lambda s: ",".join(x[8:] for x in s)).to_string())
print("NOT EXISTS gives the same rows: True")
r = pd.read_sql_query(SQL_RANGES, con)
print("compact missing ranges:"); print(r.to_string(index=False))
n = pd.read_sql_query(SQL_NOTIN, con)
print("NOT IN with a NULL login_date: user_ids returned =", sorted(n.user_id.unique().tolist()),
      "(user 4 has a NULL date and vanishes)")
w = pd.read_sql_query(SQL_USERS_FROM_LOGINS, con)
print("user list taken from logins: user_ids returned =", sorted(w.user_id.unique().tolist()), "(user 2 vanishes)")

logins = pd.read_sql_query("SELECT * FROM logins", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
spine = pd.date_range("2024-03-01", "2024-03-10", freq="D")
grid = pd.MultiIndex.from_product([users["user_id"], spine], names=["user_id", "d"]).to_frame(index=False)
seen = logins.dropna(subset=["login_date"]).assign(d=lambda x: pd.to_datetime(x["login_date"]))[["user_id", "d"]].drop_duplicates()
m = grid.merge(seen, on=["user_id", "d"], how="left", indicator=True)
miss = m[m["_merge"] == "left_only"][["user_id", "d"]].sort_values(["user_id", "d"]).reset_index(drop=True)
miss["grp"] = (miss["d"] - pd.Timestamp("1970-01-01")).dt.days - miss.groupby("user_id").cumcount()
ranges = (miss.groupby(["user_id", "grp"], as_index=False)
              .agg(range_start=("d", "min"), range_end=("d", "max"), days_missing=("d", "size"))
              .drop(columns="grp"))
# pd:end
p_miss = miss.assign(missing_date=miss["d"].dt.strftime("%Y-%m-%d"))[["user_id", "missing_date"]]
pd.testing.assert_frame_equal(p_miss, a, check_dtype=False)   # ordered by user_id, missing_date
for c in ("range_start", "range_end"):
    ranges[c] = ranges[c].dt.strftime("%Y-%m-%d")
pd.testing.assert_frame_equal(ranges.sort_values(["user_id", "range_start"]).reset_index(drop=True), r, check_dtype=False)
print("pandas equals SQL (missing days ordered by user_id, missing_date; ranges by user_id, range_start): True")
print("asserts passed")
```

**Output (my run):**
```text
missing days per user (LEFT JOIN ... IS NULL), counts: {1: 4, 2: 10, 4: 9}
user_id
1                      04,05,08,09
2    01,02,03,04,05,06,07,08,09,10
4       01,02,03,04,06,07,08,09,10
NOT EXISTS gives the same rows: True
compact missing ranges:
 user_id range_start  range_end  days_missing
       1  2024-03-04 2024-03-05             2
       1  2024-03-08 2024-03-09             2
       2  2024-03-01 2024-03-10            10
       4  2024-03-01 2024-03-04             4
       4  2024-03-06 2024-03-10             5
NOT IN with a NULL login_date: user_ids returned = [1, 2] (user 4 has a NULL date and vanishes)
user list taken from logins: user_ids returned = [1, 4] (user 2 vanishes)
pandas equals SQL (missing days ordered by user_id, missing_date; ranges by user_id, range_start): True
asserts passed
```

**Edge cases:**
- Duplicate logins (user 1, 03-02 twice): in the anti-join they only make matched pairs appear twice, and matched pairs are thrown away, so the missing rows are unaffected. They would matter for a count of logins per day, not here.
- A user with no logins at all (user 2): comes out with all 10 days, but only because the user list comes from the `users` table. In my run, taking the user list from `SELECT DISTINCT user_id FROM logins` made user 2 vanish (only users 1 and 4 returned). If there is no users table, the "who should be here" question has to be answered from somewhere else.
- A user with all days (user 3): no rows, which is correct and easy to miss when you look for the user in the output.
- Out-of-range dates (02-28, 03-11) are ignored because they match no spine day; the spine limits the range.
- NULL `login_date` (user 4): matches no spine day, so it does no harm in `LEFT JOIN ... IS NULL` or `NOT EXISTS`. With `NOT IN (subquery)` it is poison: `d NOT IN (..., NULL)` is never true, so user 4's rows disappeared in my run (only users 1 and 2 returned).
- Anti-join test column: check a column that is never NULL when matched (`l.user_id`), not a nullable one; testing a nullable column would drop true matches whose value is NULL.
- Unsorted input: irrelevant for the anti-join; the island step sorts.
- Spine boundaries: the recursive condition `d < '2024-03-10'` stops after generating 03-10, so the end date is included; checking that the spine has 10 rows is cheap insurance.
- Time zones and timestamps: if `login_date` came from a timestamp it must be converted to the user's local date first; not covered here.

**Then explain:**
- Why `NOT EXISTS` and `LEFT JOIN ... IS NULL` give the same rows: both keep exactly the (user, day) pairs for which no login row has that user and that day. The join form creates a NULL-padded row when there is no match; the other form asks directly if one exists. A duplicate matched row cannot add a missing row, and the unmatched side is padded exactly once.
- Where they can differ in general: a join that multiplies rows (duplicate matches) changes counts after the join, but not the set of unmatched rows; `NOT IN` is different because of NULL (shown above).
- Spine versus window: `LAG` finds gaps only between existing logins (Q20); the spine finds all missing days including before the first and after the last login, and users with no logins at all.
- Pointer: the recursive CTE spine is explained in depth in Part 9; the alternative is a calendar table. Engine-specific spine generators (`generate_series` in PostgreSQL, `GENERATE_DATE_ARRAY` in BigQuery) are from memory and not executed here.

**Follow-ups:**
- Only users who missed at least one day, or the day count per user? Group the result by user.
- Range crossing the user's signup date (days before signup are not missing)? If `users` had a `signup_date` column (this one does not), add `s.d >= u.signup_date` to the cross join.
- A longer range, such as a year? I only ran the 10 day spine; for a long range a stored calendar table is the usual alternative (not benchmarked here).

**Common mistakes:**
- `NOT IN` with a nullable subquery.
- Building the user list from the logins table and losing users with no activity.
- Putting the date filter in the `WHERE` instead of the `ON` clause of the `LEFT JOIN`, which turns it into an inner join.
- Off-by-one on the spine end date.
- Testing a nullable column for `IS NULL` after the join.

### Q20 ⭐⭐ 🟡 Gaps between consecutive dates larger than one day: logins(user_id, login_date). For each user list every gap as gap_start (the first missing day), gap_end (the last missing day) and days_missing using LEAD or LAG with julianday difference > 1, and also the longest break between two logins per user. Explain the NULL on the last row of each partition, the threshold meaning of exactly 1 day apart (no gap) versus exactly 2 (one missing day), and a user with a single login.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Deduplicate the login days, use `LEAD` to get each user's next login date, and call it a gap when the next date is more than 1 day later; the first missing day is the login date plus 1, the last missing day is the next date minus 1, and the number of missing days is the difference minus 1.

**Definitions I use:** a gap is a stretch of calendar days with no login between two logins of the same user; `days_missing` counts the missing days (so logins on 03-02 and 03-04 leave 1 missing day). "Longest break" is the largest `days_missing` for a user; the days between the two logins is that number plus 1. Say which one you mean; I report the missing-days form and 0 for a user with no gap.

**Schema and sample data:** twelve rows, four users, unsorted. User 1: 03-01, 03-02, 03-04 (twice), 03-10. User 2: a single login (03-05). User 3: three consecutive days, no gap. User 4: 03-01, a NULL date, 03-03. Dates are ISO text.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-10'),(1,'2024-03-04'),(1,'2024-03-01'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-05'),
 (3,'2024-03-03'),(3,'2024-03-01'),(3,'2024-03-02'),
 (4,'2024-03-01'),(4,NULL),(4,'2024-03-03');
```

**SQL answer:** `SQL_GAPS` in the Code block:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
)
SELECT user_id,
       date(login_date, '+1 day') AS gap_start,
       date(next_date, '-1 day') AS gap_end,
       CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
FROM x
WHERE julianday(next_date) - julianday(login_date) > 1
ORDER BY user_id, gap_start
```
Longest break per user, `SQL_LONGEST` in the Code block, with a `LEFT JOIN` from all users so users without a gap show 0:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
), gaps AS (
  SELECT user_id, CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
  FROM x
  WHERE julianday(next_date) - julianday(login_date) > 1
)
SELECT u.user_id, COALESCE(MAX(g.days_missing), 0) AS longest_break_days
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN gaps g ON g.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
```

**pandas answer:** shown once here and identical to the Code block (`shift(-1)` is `LEAD`):
```py
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
d["next_date"] = d.groupby("user_id")["login_date"].shift(-1)
d["diff_days"] = (d["next_date"] - d["login_date"]).dt.days
g = d[d["diff_days"] > 1]
gaps = pd.DataFrame({
    "user_id": g["user_id"],
    "gap_start": (g["login_date"] + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "gap_end": (g["next_date"] - pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "days_missing": (g["diff_days"] - 1).astype(int),
}).reset_index(drop=True)
longest = (gaps.groupby("user_id")["days_missing"].max()
               .reindex(logins["user_id"].drop_duplicates().sort_values()).fillna(0).astype(int)
               .rename("longest_break_days").reset_index())
```

**Example:** user 1 distinct sorted days: 03-01, 03-02, 03-04, 03-10; next dates: 03-02, 03-04, 03-10, none; differences: 1, 2, 6, NULL.
- 1 day apart (03-01 to 03-02): consecutive days, no gap, filtered out.
- 2 days apart (03-02 to 03-04): one missing day, so `gap_start = 03-03`, `gap_end = 03-03`, `days_missing = 1`.
- 6 days apart (03-04 to 03-10): 03-05 to 03-09, `days_missing = 5`.
- The last row has no next date, so its difference is NULL and it is not a gap.
- Longest break for user 1 is 5. User 4: 03-01 and 03-03 give one gap, 03-02, so longest 1. Users 2 and 3: no gap, longest 0.

**Code:** run with `python3 -I`. The asserts compare pandas with SQL for the gap list (ordered by `user_id, gap_start`) and the longest break (ordered by `user_id`). The printed `NaN` in the detail table is pandas showing SQL NULL.
```python
# Q20: gaps larger than one day between consecutive logins, and the longest break per user
import sqlite3
import datetime as dt
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-10'),(1,'2024-03-04'),(1,'2024-03-01'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-05'),
 (3,'2024-03-03'),(3,'2024-03-01'),(3,'2024-03-02'),
 (4,'2024-03-01'),(4,NULL),(4,'2024-03-03');
"""
SQL_GAPS = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
)
SELECT user_id,
       date(login_date, '+1 day') AS gap_start,
       date(next_date, '-1 day') AS gap_end,
       CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
FROM x
WHERE julianday(next_date) - julianday(login_date) > 1
ORDER BY user_id, gap_start
"""
SQL_LONGEST = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
), gaps AS (
  SELECT user_id, CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
  FROM x
  WHERE julianday(next_date) - julianday(login_date) > 1
)
SELECT u.user_id, COALESCE(MAX(g.days_missing), 0) AS longest_break_days
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN gaps g ON g.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
"""
SQL_DETAIL = """
SELECT user_id, login_date,
       LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date,
       julianday(LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date)) - julianday(login_date) AS diff_days
FROM (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL)
ORDER BY user_id, login_date
"""
# no dedupe, to see what duplicates do
SQL_NODEDUP = SQL_GAPS.replace("SELECT DISTINCT user_id, login_date", "SELECT user_id, login_date")
assert SQL_NODEDUP != SQL_GAPS

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("LEAD detail (diff_days is NULL on each user's last row):"); print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
a = pd.read_sql_query(SQL_GAPS, con)
print("gaps:"); print(a.to_string(index=False))
l = pd.read_sql_query(SQL_LONGEST, con)
print("longest break (most missing days in a row between two logins; 0 if none):"); print(l.to_string(index=False))
nd = pd.read_sql_query(SQL_NODEDUP, con)
print("without DISTINCT the gap rows are the same as with it:", nd.equals(a))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
d["next_date"] = d.groupby("user_id")["login_date"].shift(-1)
d["diff_days"] = (d["next_date"] - d["login_date"]).dt.days
g = d[d["diff_days"] > 1]
gaps = pd.DataFrame({
    "user_id": g["user_id"],
    "gap_start": (g["login_date"] + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "gap_end": (g["next_date"] - pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "days_missing": (g["diff_days"] - 1).astype(int),
}).reset_index(drop=True)
longest = (gaps.groupby("user_id")["days_missing"].max()
               .reindex(logins["user_id"].drop_duplicates().sort_values()).fillna(0).astype(int)
               .rename("longest_break_days").reset_index())
# pd:end
pd.testing.assert_frame_equal(gaps, a, check_dtype=False)        # ordered by user_id, gap_start
pd.testing.assert_frame_equal(longest, l, check_dtype=False)     # ordered by user_id
print("pandas equals SQL for gaps and longest break: True")

# julianday on whole dates: exact? compare with unixepoch over 20000 date pairs
rows, base = [], dt.date(2000, 1, 1)
for i in range(20000):
    x = base + dt.timedelta(days=i * 3)
    y = x + dt.timedelta(days=1 + i % 400)
    rows.append((x.isoformat(), y.isoformat()))
con.execute("CREATE TABLE pairs(a TEXT, b TEXT)")
con.executemany("INSERT INTO pairs VALUES (?, ?)", rows)
print(con.execute("SELECT COUNT(*), SUM(julianday(b) - julianday(a) = CAST(julianday(b) - julianday(a) AS INTEGER)), "
                  "SUM((unixepoch(b) - unixepoch(a)) % 86400 = 0), "
                  "SUM(julianday(b) - julianday(a) = (unixepoch(b) - unixepoch(a)) / 86400) FROM pairs").fetchone(),
      "<- pairs, julianday diff is a whole number, unixepoch diff is whole days, the two agree")
print("asserts passed")
```

**Output (my run):**
```text
LEAD detail (diff_days is NULL on each user's last row):
 user_id login_date  next_date  diff_days
       1 2024-03-01 2024-03-02        1.0
       1 2024-03-02 2024-03-04        2.0
       1 2024-03-04 2024-03-10        6.0
       1 2024-03-10        NaN        NaN
       2 2024-03-05        NaN        NaN
       3 2024-03-01 2024-03-02        1.0
       3 2024-03-02 2024-03-03        1.0
       3 2024-03-03        NaN        NaN
       4 2024-03-01 2024-03-03        2.0
       4 2024-03-03        NaN        NaN
gaps:
 user_id  gap_start    gap_end  days_missing
       1 2024-03-03 2024-03-03             1
       1 2024-03-05 2024-03-09             5
       4 2024-03-02 2024-03-02             1
longest break (most missing days in a row between two logins; 0 if none):
 user_id  longest_break_days
       1                   5
       2                   0
       3                   0
       4                   1
without DISTINCT the gap rows are the same as with it: True
pandas equals SQL for gaps and longest break: True
(20000, 20000, 20000, 20000) <- pairs, julianday diff is a whole number, unixepoch diff is whole days, the two agree
asserts passed
```

**Edge cases:**
- NULL on the last row of each partition: `LEAD` has no next row, so `next_date` is NULL, the difference is NULL, and `NULL > 1` is NULL, which `WHERE` treats as not true, so the last row drops out. That is the wanted behaviour, but it is the NULL logic doing it, not a deliberate filter; in pandas, `NaT` gives a NaN `diff_days` and `NaN > 1` is `False` for the same effect.
- Exactly 1 day apart means consecutive days, no day missing, so the filter is `> 1`, not `>= 1`. Exactly 2 days apart means one missing day, which is why `days_missing` is the difference minus 1; mixing these up is the classic off-by-one.
- Single login (user 2): one row, `LEAD` is NULL, no gap; in the longest-break result it shows 0 because of the `LEFT JOIN` and `COALESCE`, it is not missing.
- Duplicate dates: I dedupe first. In my run, removing the `DISTINCT` gave the same gap rows (the tied rows have a difference of 0, and the second copy still carries the real next date), so it did not create false gaps here; it would matter for any count of days or logins, and for `LAG`/`LEAD` pairs where you test equality, so I still dedupe.
- NULL date (user 4): removed in the first CTE; without it, the NULL row sorts first in SQLite (it is smaller than any text) and distorts the LEAD pairs.
- Unsorted input: handled by the window `ORDER BY`.
- `julianday` on whole dates is fine: in my run over 20000 date pairs the difference was always an exact whole number and equal to the `unixepoch` difference divided by 86400 (unlike timestamps with times in Q11, where `julianday * 1440` came out slightly off). I still wrap it in `ROUND` before the `CAST` because the cast truncates.
- Only users with 2 or more logins can have a gap; the user with one login contributes no row to the gap list.
- The break before the first login and after the last (relative to a period) is not a gap between two logins; use a date spine (Q19) for those.

**Then explain:**
- `LEAD` looks at the next row, `LAG` at the previous one; the gap logic is the same, just anchored on the other row (with `LAG`, `gap_start` is `date(prev_date, '+1 day')` and `gap_end` is `date(login_date, '-1 day')`). Both need the days deduped and sorted.
- Why `julianday` here: a date has no time part, so day differences are exact; for timestamps use `unixepoch` (Q11).
- The threshold: difference of 1 is "yesterday to today" and has nothing in between; every difference above 1 has `difference - 1` missing days.
- Dialects, not executed here: PostgreSQL date subtraction `next_date - login_date` returns an integer number of days; MySQL `DATEDIFF(next_date, login_date)`; BigQuery `DATE_DIFF(next_date, login_date, DAY)`. I did not run these.

**Follow-ups:**
- Gaps larger than 7 days (churn-style)? Change the threshold to `> 7` in the same query.
- The first and last gaps in a fixed period, not just between logins? Use the date spine and the missing ranges from Q19.
- Average time between logins? `AVG(julianday(next_date) - julianday(login_date))` over the same rows including the 1 day differences, not only the gaps.

**Common mistakes:**
- `>= 1` instead of `> 1`, or forgetting the minus 1 in `days_missing`.
- Not deduplicating or not filtering NULL dates.
- Using `LAG`/`LEAD` without `PARTITION BY user_id`, so the first login of a user looks like it follows another user's last login.
- Treating the NULL on the last row as an error and filling it with today's date.
- Reporting 0 for a one-login user as if it were missing data, or leaving it out without saying so.

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

### Q31 ⭐⭐ 🔴 Attendance streaks over working days: attendance(emp_id, work_date) where employees do not attend on weekends or holidays, and holidays(holiday_date) is given. A streak should continue across a weekend (Friday then Monday is consecutive). Number the working days in a calendar table, join attendance to it, and use working_day_number minus ROW_NUMBER as the island key. Show the calendar-day version splitting at the weekend, and explain how a holiday in the middle is treated.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Build a calendar of working days only (weekdays minus holidays), number it 1, 2, 3, ..., join attendance to it, and use `working_day_number - ROW_NUMBER()` as the island key, so Friday to Monday is consecutive and a holiday is simply a day that has no number.

**Schema and sample data:** one month of calendar (a recursive CTE builds it inside the query), one holiday (Thursday 2024-03-14), six employees. Rows are inserted unsorted, E1 has a duplicate day, and the last two rows are a NULL employee and a NULL date.
```sql
CREATE TABLE attendance(emp_id TEXT, work_date TEXT);
CREATE TABLE holidays(holiday_date TEXT);
INSERT INTO holidays VALUES ('2024-03-14');
INSERT INTO attendance VALUES
 ('E1','2024-03-11'),('E1','2024-03-08'),('E1','2024-03-07'),('E1','2024-03-08'),
 ('E1','2024-03-12'),('E1','2024-03-13'),('E1','2024-03-15'),
 ('E2','2024-03-04'),('E2','2024-03-05'),('E2','2024-03-07'),('E2','2024-03-08'),
 ('E3','2024-03-18'),
 ('E4','2024-03-08'),('E4','2024-03-12'),
 ('E5','2024-03-13'),('E5','2024-03-14'),('E5','2024-03-15'),('E5','2024-03-16'),
 ('E6','2024-03-19'),(NULL,'2024-03-19'),('E6',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block. The calendar is a date spine (a recursive CTE, pointer to Part 9 for the mechanics) filtered to weekdays with `strftime('%w', d) NOT IN ('0','6')` (0 is Sunday, 6 is Saturday) and `NOT EXISTS` against `holidays`; `ROW_NUMBER()` over what is left gives `wd_no`.
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
),
cal AS (
  SELECT d AS cal_date, ROW_NUMBER() OVER (ORDER BY d) AS wd_no
  FROM spine s
  WHERE strftime('%w', d) NOT IN ('0', '6')
    AND NOT EXISTS (SELECT 1 FROM holidays h WHERE h.holiday_date = s.d)
),
a AS (
  SELECT DISTINCT emp_id, work_date FROM attendance
  WHERE emp_id IS NOT NULL AND work_date IS NOT NULL
),
j AS (
  SELECT a.emp_id, c.cal_date, c.wd_no,
         ROW_NUMBER() OVER (PARTITION BY a.emp_id ORDER BY c.cal_date) AS rn
  FROM a JOIN cal c ON c.cal_date = a.work_date
)

SELECT emp_id, MIN(cal_date) AS streak_start, MAX(cal_date) AS streak_end, COUNT(*) AS days
FROM j
GROUP BY emp_id, wd_no - rn
ORDER BY emp_id, streak_start
```
`CAL_CTE` is the `WITH RECURSIVE ...` prefix shown in the Code block (spine, `cal`, deduplicated `a`, and `j`, which joins attendance to the calendar and numbers each employee's attended working days). The calendar-day contrast is `SQL_CALDAY`: the same island query on raw dates with `julianday(work_date) - rn`.

**pandas answer:** same logic, identical to the Code block:
```py
days = pd.date_range("2024-03-01", "2024-03-31")
cal = pd.DataFrame({"cal_date": days})
cal = cal[(cal["cal_date"].dt.dayofweek < 5)
          & ~cal["cal_date"].isin(pd.to_datetime(holidays["holiday_date"]))].copy()
cal["wd_no"] = range(1, len(cal) + 1)
a = attendance.dropna().drop_duplicates()
a = a.assign(cal_date=pd.to_datetime(a["work_date"])).merge(cal, on="cal_date")
a = a.sort_values(["emp_id", "cal_date"])
a["key"] = a["wd_no"] - (a.groupby("emp_id").cumcount() + 1)
pd_df = (a.groupby(["emp_id", "key"])
          .agg(streak_start=("cal_date", "min"), streak_end=("cal_date", "max"), days=("cal_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["emp_id", "streak_start"]).reset_index(drop=True))
pd_df["streak_start"] = pd_df["streak_start"].dt.strftime("%Y-%m-%d")
pd_df["streak_end"] = pd_df["streak_end"].dt.strftime("%Y-%m-%d")
```

**Example:** working-day numbers around the holiday (from the printed calendar): Wed 6 Mar = 4, Thu 7 = 5, Fri 8 = 6, Mon 11 = 7, Tue 12 = 8, Wed 13 = 9, Fri 15 = 10 (Thu 14 is a holiday, so it has no number), Mon 18 = 11.
- E1 attended 7, 8, 11, 12, 13, 15 March (plus a duplicate 8 March that `DISTINCT` removes). Their numbers are 5, 6, 7, 8, 9, 10 and the row numbers are 1 to 6, so `wd_no - rn` is 4 for all six: one streak of 6 working days from 7 to 15 March. The weekend and the holiday did not break it.
- On raw calendar days the same employee splits into 7-8 (2 days), 11-13 (3 days) and 15 (1 day), because the weekend and the holiday are gaps in the date line.
- E2 attended 4, 5, 7, 8 March: numbers 2, 3, 5, 6 (Wed 6 March, number 4, is a working day E2 did not attend), so the key `wd_no - rn` goes from 1 to 2 at the missing Wednesday: two streaks of 2.
- E4 attended Fri 8 and Tue 12: numbers 6 and 8 (Monday 11 is number 7 and was skipped), so two streaks of 1. Friday then Tuesday is not consecutive.
- E5 attended Wed 13, Thu 14 (holiday), Fri 15 and Sat 16. The holiday and the Saturday rows find no calendar row and drop out in the inner join, leaving 13 and 15 (numbers 9 and 10): one streak of 2. The calendar-day version reports 4 days.

**Code:** run with `python3 -I`. The assert compares the pandas frame with the SQL frame after both are sorted by `emp_id, streak_start`.
```python
# Q31: attendance streaks over working days (weekend and holiday skipping), SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE attendance(emp_id TEXT, work_date TEXT);
CREATE TABLE holidays(holiday_date TEXT);
INSERT INTO holidays VALUES ('2024-03-14');
INSERT INTO attendance VALUES
 ('E1','2024-03-11'),('E1','2024-03-08'),('E1','2024-03-07'),('E1','2024-03-08'),
 ('E1','2024-03-12'),('E1','2024-03-13'),('E1','2024-03-15'),
 ('E2','2024-03-04'),('E2','2024-03-05'),('E2','2024-03-07'),('E2','2024-03-08'),
 ('E3','2024-03-18'),
 ('E4','2024-03-08'),('E4','2024-03-12'),
 ('E5','2024-03-13'),('E5','2024-03-14'),('E5','2024-03-15'),('E5','2024-03-16'),
 ('E6','2024-03-19'),(NULL,'2024-03-19'),('E6',NULL);
"""
CAL_CTE = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
),
cal AS (
  SELECT d AS cal_date, ROW_NUMBER() OVER (ORDER BY d) AS wd_no
  FROM spine s
  WHERE strftime('%w', d) NOT IN ('0', '6')
    AND NOT EXISTS (SELECT 1 FROM holidays h WHERE h.holiday_date = s.d)
),
a AS (
  SELECT DISTINCT emp_id, work_date FROM attendance
  WHERE emp_id IS NOT NULL AND work_date IS NOT NULL
),
j AS (
  SELECT a.emp_id, c.cal_date, c.wd_no,
         ROW_NUMBER() OVER (PARTITION BY a.emp_id ORDER BY c.cal_date) AS rn
  FROM a JOIN cal c ON c.cal_date = a.work_date
)
"""
SQL_MAIN = CAL_CTE + """
SELECT emp_id, MIN(cal_date) AS streak_start, MAX(cal_date) AS streak_end, COUNT(*) AS days
FROM j
GROUP BY emp_id, wd_no - rn
ORDER BY emp_id, streak_start
"""
SQL_CALDAY = """
WITH a AS (
  SELECT DISTINCT emp_id, work_date FROM attendance
  WHERE emp_id IS NOT NULL AND work_date IS NOT NULL
),
r AS (
  SELECT emp_id, work_date,
         ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY work_date) AS rn
  FROM a
)
SELECT emp_id, MIN(work_date) AS streak_start, MAX(work_date) AS streak_end, COUNT(*) AS days
FROM r
GROUP BY emp_id, julianday(work_date) - rn
ORDER BY emp_id, streak_start
"""
SQL_CAL = CAL_CTE + "SELECT cal_date, wd_no, strftime('%w', cal_date) AS dow FROM cal WHERE cal_date BETWEEN '2024-03-06' AND '2024-03-18'"

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL, working-day streaks:")
print(sql_df.to_string(index=False))
print("SQL, calendar-day streaks (splits at weekends):")
print(pd.read_sql_query(SQL_CALDAY, con).to_string(index=False))
print("working-day calendar, 6 to 18 March:")
print(pd.read_sql_query(SQL_CAL, con).to_string(index=False))

attendance = pd.read_sql_query("SELECT * FROM attendance", con)
holidays = pd.read_sql_query("SELECT * FROM holidays", con)
# pd:main
days = pd.date_range("2024-03-01", "2024-03-31")
cal = pd.DataFrame({"cal_date": days})
cal = cal[(cal["cal_date"].dt.dayofweek < 5)
          & ~cal["cal_date"].isin(pd.to_datetime(holidays["holiday_date"]))].copy()
cal["wd_no"] = range(1, len(cal) + 1)
a = attendance.dropna().drop_duplicates()
a = a.assign(cal_date=pd.to_datetime(a["work_date"])).merge(cal, on="cal_date")
a = a.sort_values(["emp_id", "cal_date"])
a["key"] = a["wd_no"] - (a.groupby("emp_id").cumcount() + 1)
pd_df = (a.groupby(["emp_id", "key"])
          .agg(streak_start=("cal_date", "min"), streak_end=("cal_date", "max"), days=("cal_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["emp_id", "streak_start"]).reset_index(drop=True))
pd_df["streak_start"] = pd_df["streak_start"].dt.strftime("%Y-%m-%d")
pd_df["streak_end"] = pd_df["streak_end"].dt.strftime("%Y-%m-%d")
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
# compare after sorting both by emp_id, streak_start
assert pd_df.astype({"days": "int64"}).equals(sql_df.astype({"days": "int64"}))

# edge: E5 attended on the holiday and on a Saturday; both rows are dropped by the inner join
print("E5 rows kept:", int((a["emp_id"] == "E5").sum()), "of", int((attendance["emp_id"] == "E5").sum()))
# edge: a NULL holiday_date would break NOT IN but not NOT EXISTS
con.execute("INSERT INTO holidays VALUES (NULL)")
print("rows with NULL holiday present:", len(pd.read_sql_query(SQL_MAIN, con)))
print("asserts passed")
```

**Output (my run):**
```text
SQL, working-day streaks:
emp_id streak_start streak_end  days
    E1   2024-03-07 2024-03-15     6
    E2   2024-03-04 2024-03-05     2
    E2   2024-03-07 2024-03-08     2
    E3   2024-03-18 2024-03-18     1
    E4   2024-03-08 2024-03-08     1
    E4   2024-03-12 2024-03-12     1
    E5   2024-03-13 2024-03-15     2
    E6   2024-03-19 2024-03-19     1
SQL, calendar-day streaks (splits at weekends):
emp_id streak_start streak_end  days
    E1   2024-03-07 2024-03-08     2
    E1   2024-03-11 2024-03-13     3
    E1   2024-03-15 2024-03-15     1
    E2   2024-03-04 2024-03-05     2
    E2   2024-03-07 2024-03-08     2
    E3   2024-03-18 2024-03-18     1
    E4   2024-03-08 2024-03-08     1
    E4   2024-03-12 2024-03-12     1
    E5   2024-03-13 2024-03-16     4
    E6   2024-03-19 2024-03-19     1
working-day calendar, 6 to 18 March:
  cal_date  wd_no dow
2024-03-06      4   3
2024-03-07      5   4
2024-03-08      6   5
2024-03-11      7   1
2024-03-12      8   2
2024-03-13      9   3
2024-03-15     10   5
2024-03-18     11   1
pandas:
emp_id streak_start streak_end  days
    E1   2024-03-07 2024-03-15     6
    E2   2024-03-04 2024-03-05     2
    E2   2024-03-07 2024-03-08     2
    E3   2024-03-18 2024-03-18     1
    E4   2024-03-08 2024-03-08     1
    E4   2024-03-12 2024-03-12     1
    E5   2024-03-13 2024-03-15     2
    E6   2024-03-19 2024-03-19     1
E5 rows kept: 2 of 4
rows with NULL holiday present: 8
asserts passed
```

**Edge cases:**
- Duplicates: E1's repeated 8 March row would give two row numbers to one day and split the run, so the attendance is `SELECT DISTINCT` first.
- NULLs: a NULL `emp_id` or `work_date` is dropped in the `WHERE`. A NULL date would otherwise never match the calendar anyway (the inner join drops it), but a NULL employee would form its own group. A NULL in `holidays` breaks `NOT IN` (every comparison becomes NULL, so no day passes and the calendar goes empty; a probe of `'2024-03-04' NOT IN (SELECT '2024-03-14' UNION ALL SELECT NULL)` returned NULL); `NOT EXISTS` is immune, and the run with a NULL holiday inserted returned the same 8 rows.
- Single-row groups: E3 and E6 each get a streak of 1.
- Attendance on a non-working day (E5's holiday and Saturday rows): this answer drops them. If those days should count (someone really worked), add them to the calendar as working days or build the calendar from "weekday or attended", and say so.
- Exact threshold: Friday to Monday differs by one working-day number, so it continues; Friday to Tuesday differs by two, so it breaks (E4).
- Unsorted input is harmless because every window orders explicitly.
- The calendar must cover the attendance range (here March 2024); dates outside it silently disappear. Generate the spine from `MIN` and `MAX` of the data in production.

**Then explain:**
- The island trick needs a gap-free number line. Calendar days are that line only for a seven-day business. For a five-day business with holidays the line is the working-day calendar, so you number the working days yourself instead of using `julianday`.
- A holiday in the middle is treated as if it did not exist: it has no number, so the days on either side are neighbours. This is a policy choice (nobody can be absent on a holiday). If the business wants a holiday to break a streak, give it a number (do not exclude it from the calendar) and then an employee who skipped it has a gap.
- Holidays that fall on a weekend are removed twice, which is harmless.
- Dialects (not executed here): PostgreSQL would use `generate_series` for the spine and `EXTRACT(ISODOW FROM d) < 6`; MySQL 8 uses a recursive CTE and `WEEKDAY(d) < 5`. In `strftime('%w')` Sunday is 0 in SQLite.
- Per-employee or per-country holiday calendars are the same query with the calendar keyed by region.

**Follow-ups:**
- Longest working-day streak per employee? Reduce the islands as in Q7.
- Current streak as of a date? Q15 logic on the working-day numbers: the island whose end is the last working day on or before the as-of date.
- Half-days or shift workers? Then the calendar is per employee (a roster table) and the same numbering applies to that roster.

**Common mistakes:**
- Using `julianday(work_date) - ROW_NUMBER()` and reporting a Friday-Monday run as two streaks (shown: E1 splits into three).
- Keeping holidays in the calendar and then expecting them to be skipped.
- Joining attendance with a LEFT JOIN, which creates NULL day numbers for attendance on non-working days and a NULL group.
- Forgetting `DISTINCT`, or numbering the calendar before filtering out weekends.
- Using `NOT IN` against a holiday table that can contain NULL.

### Q32 ⭐ 🟡 Slowly changing dimension range collapse: plan_snapshot(customer_id, snapshot_date, plan) has one row per customer per day. Collapse consecutive identical plans into validity ranges (customer_id, plan, valid_from, valid_to) where valid_to is the last day with that plan, using LAG change flags and a running SUM, and produce an open-ended valid_to (NULL) for the current plan. Show a customer who goes basic, premium, basic (the second basic is a new range) and a missing snapshot day (decide whether it breaks the range).
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Flag every row whose plan differs from the previous row of the same customer (first row counts as a change), take a running SUM of the flag as the range id, then `GROUP BY customer_id, range_id` with `MIN(date)` as `valid_from` and `MAX(date)` as `valid_to`, turning the last range into NULL when it is still current.

**Schema and sample data:** daily snapshots up to a fixed as-of date of 2024-03-10 (the latest snapshot date in the table, never today). C1 goes basic, premium, basic and has an exact duplicate row; C2 has no snapshot on 3 March; C3 has a single snapshot; C4 stops on 3 March (churned, not current); C5 has NULL plans. Rows are inserted unsorted.
```sql
CREATE TABLE plan_snapshot(customer_id TEXT, snapshot_date TEXT, plan TEXT);
INSERT INTO plan_snapshot VALUES
 ('C1','2024-03-04','premium'),('C1','2024-03-01','basic'),('C1','2024-03-02','basic'),('C1','2024-03-02','basic'),
 ('C1','2024-03-03','basic'),('C1','2024-03-05','premium'),('C1','2024-03-06','premium'),
 ('C1','2024-03-07','basic'),('C1','2024-03-08','basic'),('C1','2024-03-09','basic'),('C1','2024-03-10','basic'),
 ('C2','2024-03-01','premium'),('C2','2024-03-02','premium'),
 ('C2','2024-03-04','premium'),('C2','2024-03-05','premium'),
 ('C3','2024-03-10','basic'),
 ('C4','2024-03-01','basic'),('C4','2024-03-02','basic'),('C4','2024-03-03','basic'),
 ('C5','2024-03-01','basic'),('C5','2024-03-02',NULL),('C5','2024-03-03',NULL),('C5','2024-03-04','basic');
```

**SQL answer:** `SQL_MAIN` in the Code block. `LAG(snapshot_date) IS NULL` marks the customer's first row, and `plan IS NOT LAG(plan)` is the NULL-safe "changed" test (plain `<>` would drop the NULL rows). The current range gets `valid_to = NULL` only when its last snapshot is the as-of date; a customer whose last snapshot is older keeps a real end date.
```sql
WITH s AS (
  SELECT DISTINCT customer_id, snapshot_date, plan FROM plan_snapshot
),
f AS (
  SELECT *,
         CASE WHEN LAG(snapshot_date) OVER w IS NULL OR plan IS NOT LAG(plan) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM s
  WINDOW w AS (PARTITION BY customer_id ORDER BY snapshot_date)
),
g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY customer_id ORDER BY snapshot_date) AS grp
  FROM f
)
SELECT customer_id, plan,
       MIN(snapshot_date) AS valid_from,
       CASE WHEN MAX(snapshot_date) = '2024-03-10' THEN NULL ELSE MAX(snapshot_date) END AS valid_to
FROM g
GROUP BY customer_id, grp
ORDER BY customer_id, valid_from
```
The strict variant `SQL_STRICT` adds `OR julianday(snapshot_date) - julianday(LAG(snapshot_date) OVER w) > 1` to the flag, so a missing snapshot day starts a new range. `SQL_WRONG` is the tempting `GROUP BY customer_id, plan`.

**pandas answer:** same logic, identical to the Code block:
```py
s = snap.drop_duplicates().sort_values(["customer_id", "snapshot_date"]).reset_index(drop=True)
prev = s.groupby("customer_id")["plan"].shift()
first = s.groupby("customer_id").cumcount() == 0
same = (s["plan"] == prev) | (s["plan"].isna() & prev.isna())
s["grp"] = (first | ~same).groupby(s["customer_id"]).cumsum()
pd_df = (s.groupby(["customer_id", "grp"], as_index=False)
          .agg(plan=("plan", "first"), valid_from=("snapshot_date", "min"), valid_to=("snapshot_date", "max")))
pd_df["valid_to"] = pd_df["valid_to"].where(pd_df["valid_to"] != AS_OF, None)
pd_df = pd_df.drop(columns="grp").sort_values(["customer_id", "valid_from"]).reset_index(drop=True)
```

**Example:** C1 after `DISTINCT` has basic 1-3 March, premium 4-6 March, basic 7-10 March.
- Change flags by day: 1 (first), 0, 0, 1 (premium), 0, 0, 1 (basic again), 0, 0, 0. Running sum: 1, 1, 1, 2, 2, 2, 3, 3, 3, 3.
- Group 1 is basic 03-01 to 03-03, group 2 premium 03-04 to 03-06, group 3 basic from 03-07; its last snapshot is 03-10, the as-of date, so `valid_to` is NULL.
- `GROUP BY customer_id, plan` instead gives basic 03-01 to 03-10 and premium 03-04 to 03-06: the premium period is nested inside the basic one, which is wrong.
- C2 (1, 2, 4, 5 March, same plan): the main query gives one range 03-01 to 03-05 (the missing 3 March does not change the plan); the strict query gives 03-01 to 03-02 and 03-04 to 03-05.
- C4 ends on 03-03, which is before the as-of date, so `valid_to` is `2024-03-03`, not NULL.

**Code:** run with `python3 -I`. The assert compares after sorting by `customer_id, valid_from`, with NULL and None mapped to the same text.
```python
# Q32: SCD range collapse from daily plan snapshots, SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE plan_snapshot(customer_id TEXT, snapshot_date TEXT, plan TEXT);
INSERT INTO plan_snapshot VALUES
 ('C1','2024-03-04','premium'),('C1','2024-03-01','basic'),('C1','2024-03-02','basic'),('C1','2024-03-02','basic'),
 ('C1','2024-03-03','basic'),('C1','2024-03-05','premium'),('C1','2024-03-06','premium'),
 ('C1','2024-03-07','basic'),('C1','2024-03-08','basic'),('C1','2024-03-09','basic'),('C1','2024-03-10','basic'),
 ('C2','2024-03-01','premium'),('C2','2024-03-02','premium'),
 ('C2','2024-03-04','premium'),('C2','2024-03-05','premium'),
 ('C3','2024-03-10','basic'),
 ('C4','2024-03-01','basic'),('C4','2024-03-02','basic'),('C4','2024-03-03','basic'),
 ('C5','2024-03-01','basic'),('C5','2024-03-02',NULL),('C5','2024-03-03',NULL),('C5','2024-03-04','basic');
"""
SQL_MAIN = """
WITH s AS (
  SELECT DISTINCT customer_id, snapshot_date, plan FROM plan_snapshot
),
f AS (
  SELECT *,
         CASE WHEN LAG(snapshot_date) OVER w IS NULL OR plan IS NOT LAG(plan) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM s
  WINDOW w AS (PARTITION BY customer_id ORDER BY snapshot_date)
),
g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY customer_id ORDER BY snapshot_date) AS grp
  FROM f
)
SELECT customer_id, plan,
       MIN(snapshot_date) AS valid_from,
       CASE WHEN MAX(snapshot_date) = '2024-03-10' THEN NULL ELSE MAX(snapshot_date) END AS valid_to
FROM g
GROUP BY customer_id, grp
ORDER BY customer_id, valid_from
"""
SQL_STRICT = """
WITH s AS (
  SELECT DISTINCT customer_id, snapshot_date, plan FROM plan_snapshot
),
f AS (
  SELECT *,
         CASE WHEN LAG(snapshot_date) OVER w IS NULL
                OR plan IS NOT LAG(plan) OVER w
                OR julianday(snapshot_date) - julianday(LAG(snapshot_date) OVER w) > 1
              THEN 1 ELSE 0 END AS chg
  FROM s
  WINDOW w AS (PARTITION BY customer_id ORDER BY snapshot_date)
),
g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY customer_id ORDER BY snapshot_date) AS grp
  FROM f
)
SELECT customer_id, plan,
       MIN(snapshot_date) AS valid_from,
       CASE WHEN MAX(snapshot_date) = '2024-03-10' THEN NULL ELSE MAX(snapshot_date) END AS valid_to
FROM g
GROUP BY customer_id, grp
ORDER BY customer_id, valid_from
"""
SQL_WRONG = """
SELECT customer_id, plan, MIN(snapshot_date) AS valid_from, MAX(snapshot_date) AS valid_to
FROM (SELECT DISTINCT customer_id, snapshot_date, plan FROM plan_snapshot)
GROUP BY customer_id, plan
ORDER BY customer_id, valid_from
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main (missing day does not break the range):")
print(sql_df.to_string(index=False))
print("SQL strict (a missing snapshot day breaks the range):")
print(pd.read_sql_query(SQL_STRICT, con).to_string(index=False))
print("wrong: GROUP BY customer_id, plan merges basic, premium, basic:")
print(pd.read_sql_query(SQL_WRONG, con).query("customer_id == 'C1'").to_string(index=False))

snap = pd.read_sql_query("SELECT * FROM plan_snapshot", con)
AS_OF = "2024-03-10"
# pd:main
s = snap.drop_duplicates().sort_values(["customer_id", "snapshot_date"]).reset_index(drop=True)
prev = s.groupby("customer_id")["plan"].shift()
first = s.groupby("customer_id").cumcount() == 0
same = (s["plan"] == prev) | (s["plan"].isna() & prev.isna())
s["grp"] = (first | ~same).groupby(s["customer_id"]).cumsum()
pd_df = (s.groupby(["customer_id", "grp"], as_index=False)
          .agg(plan=("plan", "first"), valid_from=("snapshot_date", "min"), valid_to=("snapshot_date", "max")))
pd_df["valid_to"] = pd_df["valid_to"].where(pd_df["valid_to"] != AS_OF, None)
pd_df = pd_df.drop(columns="grp").sort_values(["customer_id", "valid_from"]).reset_index(drop=True)
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
# compare after sorting by customer_id, valid_from; NULL and None both mapped to the text OPEN
norm = lambda d: d.fillna({"valid_to": "OPEN", "plan": "NULLPLAN"}).astype(str).reset_index(drop=True)
assert norm(pd_df).equals(norm(sql_df))
print("asserts passed")
```

**Output (my run):** pandas prints a NULL as `NaN`.
```text
SQL main (missing day does not break the range):
customer_id    plan valid_from   valid_to
         C1   basic 2024-03-01 2024-03-03
         C1 premium 2024-03-04 2024-03-06
         C1   basic 2024-03-07        NaN
         C2 premium 2024-03-01 2024-03-05
         C3   basic 2024-03-10        NaN
         C4   basic 2024-03-01 2024-03-03
         C5   basic 2024-03-01 2024-03-01
         C5     NaN 2024-03-02 2024-03-03
         C5   basic 2024-03-04 2024-03-04
SQL strict (a missing snapshot day breaks the range):
customer_id    plan valid_from   valid_to
         C1   basic 2024-03-01 2024-03-03
         C1 premium 2024-03-04 2024-03-06
         C1   basic 2024-03-07        NaN
         C2 premium 2024-03-01 2024-03-02
         C2 premium 2024-03-04 2024-03-05
         C3   basic 2024-03-10        NaN
         C4   basic 2024-03-01 2024-03-03
         C5   basic 2024-03-01 2024-03-01
         C5     NaN 2024-03-02 2024-03-03
         C5   basic 2024-03-04 2024-03-04
wrong: GROUP BY customer_id, plan merges basic, premium, basic:
customer_id    plan valid_from   valid_to
         C1   basic 2024-03-01 2024-03-10
         C1 premium 2024-03-04 2024-03-06
pandas:
customer_id    plan valid_from   valid_to
         C1   basic 2024-03-01 2024-03-03
         C1 premium 2024-03-04 2024-03-06
         C1   basic 2024-03-07        NaN
         C2 premium 2024-03-01 2024-03-05
         C3   basic 2024-03-10        NaN
         C4   basic 2024-03-01 2024-03-03
         C5   basic 2024-03-01 2024-03-01
         C5     NaN 2024-03-02 2024-03-03
         C5   basic 2024-03-04 2024-03-04
asserts passed
```

**Edge cases:**
- Missing snapshot day, the decision: I assume the snapshot table is a sampling of a state, so the same plan on both sides of a missing day is the same range (main query). If a missing day means "no data, unknown state" (an outage in the pipeline) use the strict variant. Say which one you assume, because the two give different row counts for C2.
- Plan changes across a missing day: both variants start a new range at the first snapshot with the new plan, so `valid_to` of the earlier range is its last observed day, not the day before the new one. If ranges must tile with no holes, set `valid_to = LEAD(valid_from) - 1 day` instead (a follow-up, not shown).
- Duplicates: an exact duplicate row is removed by `DISTINCT`. Two rows for one day with different plans cannot be resolved by SQL; agree a rule (latest loaded wins) and apply it first.
- NULL plan: C5's NULL plan forms its own range of two days because `IS NOT` treats NULL as a value that equals NULL. With `<>` the transition into and out of NULL would be missed.
- Single row (C3): one range with `valid_from = 2024-03-10`, `valid_to` NULL.
- Unsorted input is handled by the explicit window `ORDER BY`.
- pandas: the `==` comparison gives False for NaN against NaN, so the NaN-safe test is written explicitly as `(plan == prev) | (plan.isna() & prev.isna())`.

**Then explain:**
- Collapsing equal consecutive rows is run-length encoding by a state, the same machinery as Q13; the only SCD-specific parts are the end-date convention and the open-ended current row.
- `valid_to = last day with that plan` is inclusive. Many warehouses prefer a half-open `[valid_from, valid_to)` with `valid_to = next valid_from`; the same grouping works, only the end expression changes.
- NULL for the current row follows the usual "open-ended" convention; some teams use `9999-12-31`, which is easier for range joins (`BETWEEN`) but a magic value.
- The as-of date must be a parameter or the table maximum, never `date('now')`, or the result changes every day.
- Dialects (not executed here): PostgreSQL and others support `IS DISTINCT FROM` as the NULL-safe test (SQLite 3.45.1 also does, probed in Q38 of this part), and `DATEDIFF` or date subtraction replaces `julianday`.

**Follow-ups:**
- Join facts to the dimension? `fact.date BETWEEN valid_from AND COALESCE(valid_to, '9999-12-31')`.
- Count plan switches per customer? Sum of the flag minus 1.
- Why not `GROUP BY customer_id, plan`? Shown above: a plan that returns later is merged into the earlier range.

**Common mistakes:**
- `GROUP BY customer_id, plan` (collapses the second basic into the first).
- Using `<>` and silently losing transitions involving NULL.
- Forgetting `SELECT DISTINCT`, so a duplicate row is carried into the range counts.
- Marking every customer's last range as open even when the customer stopped appearing.
- Hard-coding today's date for the open end.

### Q33 ⭐ 🟡 Subscription active periods from daily snapshots: sub_snapshot(user_id, snap_date, is_active). Return each user's active periods (active_from, active_to, days) as islands of consecutive snapshot days where is_active = 1, count how many times a user resubscribed (periods minus 1), and say what happens to a missing snapshot day and to an inactive day between two active days. Filter before ROW_NUMBER versus ROW_NUMBER over all rows then filter, and when each is right.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Keep only `is_active = 1` rows (deduplicated), number them per user, and group by `julianday(snap_date) - ROW_NUMBER()` to get each active period; filter before numbering, because numbering all rows and filtering afterwards merges periods across inactive days.

**Schema and sample data:** one row per user per snapshot day, 1 to 6 March 2024, no as-of date is needed, so nothing depends on today. U1 has an inactive day (4 March) between active days and a duplicate row; U2 has a missing snapshot (3 March); U3 is never active; U4 has one active day; U5 has a NULL `is_active`. Rows are inserted unsorted.
```sql
CREATE TABLE sub_snapshot(user_id TEXT, snap_date TEXT, is_active INTEGER);
INSERT INTO sub_snapshot VALUES
 ('U1','2024-03-05',1),('U1','2024-03-01',1),('U1','2024-03-02',1),('U1','2024-03-02',1),('U1','2024-03-03',1),
 ('U1','2024-03-04',0),('U1','2024-03-06',1),
 ('U2','2024-03-01',1),('U2','2024-03-02',1),('U2','2024-03-04',1),
 ('U3','2024-03-01',0),('U3','2024-03-02',0),
 ('U4','2024-03-03',1),
 ('U5','2024-03-01',1),('U5','2024-03-02',NULL),('U5','2024-03-03',1),('U5','2024-03-04',1);
```

**SQL answer:** `SQL_MAIN` in the Code block (filter, `DISTINCT`, then the date-minus-row-number key):
```sql
WITH d AS (
  SELECT DISTINCT user_id, snap_date FROM sub_snapshot WHERE is_active = 1
),
r AS (
  SELECT user_id, snap_date,
         julianday(snap_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS k
  FROM d
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM r
GROUP BY user_id, k
ORDER BY user_id, active_from
```
The resubscription count is `SQL_RESUB` in the Code block: the same query wrapped as `p`, `LEFT JOIN`ed from all users so that U3 (no periods) appears with 0, and `MAX(COUNT(p.user_id) - 1, 0)` (SQLite scalar `MAX` with two arguments) so that nobody gets -1.
```sql
WITH p AS (
WITH d AS (
  SELECT DISTINCT user_id, snap_date FROM sub_snapshot WHERE is_active = 1
),
r AS (
  SELECT user_id, snap_date,
         julianday(snap_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS k
  FROM d
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM r
GROUP BY user_id, k

)
SELECT u.user_id, COUNT(p.user_id) AS periods,
       MAX(COUNT(p.user_id) - 1, 0) AS resubscribed
FROM (SELECT DISTINCT user_id FROM sub_snapshot) u
LEFT JOIN p ON p.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
```
The two alternatives are `SQL_ROWBASED` (row numbers over all rows minus row numbers over the active rows, so missing snapshot rows do not break a period) and `SQL_WRONG` (all-rows row number, then filter).

**pandas answer:** same logic, identical to the Code block:
```py
a = snap[snap["is_active"] == 1][["user_id", "snap_date"]].drop_duplicates()
a = a.assign(d=pd.to_datetime(a["snap_date"])).sort_values(["user_id", "d"])
a["k"] = (a["d"] - pd.Timestamp("1970-01-01")).dt.days - a.groupby("user_id").cumcount()
pd_df = (a.groupby(["user_id", "k"])
          .agg(active_from=("snap_date", "min"), active_to=("snap_date", "max"), days=("snap_date", "size"))
          .reset_index().drop(columns="k").sort_values(["user_id", "active_from"]).reset_index(drop=True))
users = pd.DataFrame({"user_id": sorted(snap["user_id"].unique())})
cnt = pd_df.groupby("user_id").size().rename("periods")
pd_res = users.merge(cnt, on="user_id", how="left").fillna({"periods": 0}).astype({"periods": "int64"})
pd_res["resubscribed"] = (pd_res["periods"] - 1).clip(lower=0)
```

**Example:** active days after filtering and `DISTINCT`:
- U1: 1, 2, 3, 5, 6 March (the 0 on 4 March is gone). Day numbers minus row numbers: the first three share one key, the key increases by one at 5 March (a day is missing from the filtered list), so periods 1-3 March (3 days) and 5-6 March (2 days). Periods 2, resubscribed 1.
- U2: 1, 2, 4 March: 3 March has no row, so two periods (2 days and 1 day). Periods 2, resubscribed 1.
- U3: nothing survives the filter, so no period rows; the `LEFT JOIN` still gives periods 0 and resubscribed 0.
- U4: one period of 1 day, resubscribed 0.
- U5: 1 March active, 2 March NULL (not `= 1`, so dropped), 3 and 4 March active: periods 1 March and 3-4 March, resubscribed 1.
- Row-numbering all rows and filtering after (`SQL_WRONG`): day-number minus all-rows row number is constant for U1 across the whole table, so the inactive day does not split it and U1 becomes one 5-day period 1-6 March, and U5 becomes one 3-day period; both are wrong.

**Code:** run with `python3 -I`. The asserts compare the pandas frames with the SQL frames after sorting by `user_id, active_from` (periods) and by `user_id` (summary).
```python
# Q33: subscription active periods from daily snapshots, SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sub_snapshot(user_id TEXT, snap_date TEXT, is_active INTEGER);
INSERT INTO sub_snapshot VALUES
 ('U1','2024-03-05',1),('U1','2024-03-01',1),('U1','2024-03-02',1),('U1','2024-03-02',1),('U1','2024-03-03',1),
 ('U1','2024-03-04',0),('U1','2024-03-06',1),
 ('U2','2024-03-01',1),('U2','2024-03-02',1),('U2','2024-03-04',1),
 ('U3','2024-03-01',0),('U3','2024-03-02',0),
 ('U4','2024-03-03',1),
 ('U5','2024-03-01',1),('U5','2024-03-02',NULL),('U5','2024-03-03',1),('U5','2024-03-04',1);
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, snap_date FROM sub_snapshot WHERE is_active = 1
),
r AS (
  SELECT user_id, snap_date,
         julianday(snap_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS k
  FROM d
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM r
GROUP BY user_id, k
ORDER BY user_id, active_from
"""
SQL_ROWBASED = """
WITH t AS (
  SELECT user_id, snap_date, is_active,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS rn_all
  FROM (SELECT DISTINCT user_id, snap_date, is_active FROM sub_snapshot)
),
f AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS rn_act
  FROM t WHERE is_active = 1
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM f
GROUP BY user_id, rn_all - rn_act
ORDER BY user_id, active_from
"""
SQL_WRONG = """
WITH t AS (
  SELECT user_id, snap_date, is_active,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS rn_all
  FROM (SELECT DISTINCT user_id, snap_date, is_active FROM sub_snapshot)
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM t WHERE is_active = 1
GROUP BY user_id, julianday(snap_date) - rn_all
ORDER BY user_id, active_from
"""
SQL_RESUB = """
WITH p AS (""" + SQL_MAIN.replace("ORDER BY user_id, active_from", "") + """)
SELECT u.user_id, COUNT(p.user_id) AS periods,
       MAX(COUNT(p.user_id) - 1, 0) AS resubscribed
FROM (SELECT DISTINCT user_id FROM sub_snapshot) u
LEFT JOIN p ON p.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main (filter first, date-based key):")
print(sql_df.to_string(index=False))
print("SQL row-based (ROW_NUMBER over all rows minus over active rows):")
print(pd.read_sql_query(SQL_ROWBASED, con).to_string(index=False))
print("wrong: date minus ROW_NUMBER over all rows, then filter:")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))
sql_res = pd.read_sql_query(SQL_RESUB, con)
print("periods and resubscriptions per user:")
print(sql_res.to_string(index=False))

snap = pd.read_sql_query("SELECT * FROM sub_snapshot", con)
# pd:main
a = snap[snap["is_active"] == 1][["user_id", "snap_date"]].drop_duplicates()
a = a.assign(d=pd.to_datetime(a["snap_date"])).sort_values(["user_id", "d"])
a["k"] = (a["d"] - pd.Timestamp("1970-01-01")).dt.days - a.groupby("user_id").cumcount()
pd_df = (a.groupby(["user_id", "k"])
          .agg(active_from=("snap_date", "min"), active_to=("snap_date", "max"), days=("snap_date", "size"))
          .reset_index().drop(columns="k").sort_values(["user_id", "active_from"]).reset_index(drop=True))
users = pd.DataFrame({"user_id": sorted(snap["user_id"].unique())})
cnt = pd_df.groupby("user_id").size().rename("periods")
pd_res = users.merge(cnt, on="user_id", how="left").fillna({"periods": 0}).astype({"periods": "int64"})
pd_res["resubscribed"] = (pd_res["periods"] - 1).clip(lower=0)
# pd:end
print("pandas periods:")
print(pd_df.to_string(index=False))
# compare after sorting by user_id, active_from (and user_id for the summary)
assert pd_df.equals(sql_df)
assert pd_res.equals(sql_res.astype({"periods": "int64", "resubscribed": "int64"}))
print("asserts passed")
```

**Output (my run):**
```text
SQL main (filter first, date-based key):
user_id active_from  active_to  days
     U1  2024-03-01 2024-03-03     3
     U1  2024-03-05 2024-03-06     2
     U2  2024-03-01 2024-03-02     2
     U2  2024-03-04 2024-03-04     1
     U4  2024-03-03 2024-03-03     1
     U5  2024-03-01 2024-03-01     1
     U5  2024-03-03 2024-03-04     2
SQL row-based (ROW_NUMBER over all rows minus over active rows):
user_id active_from  active_to  days
     U1  2024-03-01 2024-03-03     3
     U1  2024-03-05 2024-03-06     2
     U2  2024-03-01 2024-03-04     3
     U4  2024-03-03 2024-03-03     1
     U5  2024-03-01 2024-03-01     1
     U5  2024-03-03 2024-03-04     2
wrong: date minus ROW_NUMBER over all rows, then filter:
user_id active_from  active_to  days
     U1  2024-03-01 2024-03-06     5
     U2  2024-03-01 2024-03-02     2
     U2  2024-03-04 2024-03-04     1
     U4  2024-03-03 2024-03-03     1
     U5  2024-03-01 2024-03-04     3
periods and resubscriptions per user:
user_id  periods  resubscribed
     U1        2             1
     U2        2             1
     U3        0             0
     U4        1             0
     U5        2             1
pandas periods:
user_id active_from  active_to  days
     U1  2024-03-01 2024-03-03     3
     U1  2024-03-05 2024-03-06     2
     U2  2024-03-01 2024-03-02     2
     U2  2024-03-04 2024-03-04     1
     U4  2024-03-03 2024-03-03     1
     U5  2024-03-01 2024-03-01     1
     U5  2024-03-03 2024-03-04     2
asserts passed
```

**Edge cases:**
- Missing snapshot day (U2): the main query ends the period, because the filtered list has no 3 March and the day number jumps. The row-based variant (`SQL_ROWBASED`) merges U2 into one 3-row period (1 to 4 March, 3 days) because it only looks at row order. Choose by what a missing row means: if it means "no information, treat the state as unknown", the date-based key is right; if the table is sparse because unchanged days are omitted, the row-based variant (or a state-change table) is right. I assume daily snapshots with no omission, so the main query.
- Inactive day between two active days (U1): always splits, in both variants, because the inactive row is not active.
- NULL `is_active` (U5): `= 1` drops it, so it behaves as inactive. Decide whether NULL means "unknown, keep the period open"; that would need a different rule.
- Duplicates (U1 on 2 March): without `DISTINCT` the duplicate gets its own row number and splits the period; here it is removed first.
- Users with no active days (U3) vanish from the island output, so anything that must list all users needs a `LEFT JOIN` from a users source.
- Single row (U4) and unsorted input are handled.

**Then explain:**
- Filter before numbering when the numbering is meant to run along the filtered rows (the key is `date - rn` with both measured on the same rows). Number all rows first only when you then compare row positions, as in `SQL_ROWBASED`, where the difference of two row numbers is the key. The wrong combination is a row number over all rows used with a date key after filtering.
- The date-based key makes the day line the truth and tolerates nothing missing; the row-number-difference key makes the row order the truth and tolerates missing rows.
- Resubscribed = periods - 1, floored at 0 for users who never subscribed.
- Dialects (not executed here): the two-argument scalar `MAX(a, 0)` is SQLite; PostgreSQL and MySQL write `GREATEST(a, 0)` and Postgres can subtract dates directly.

**Follow-ups:**
- Time to resubscribe? Gap days between consecutive periods with `LAG(active_to)`.
- Churn events? The day after each `active_to` that is not the last snapshot date.
- Only the current period? Q15 logic.

**Common mistakes:**
- `ROW_NUMBER()` over all rows, then `WHERE is_active = 1` (merges across inactive days; shown for U1 and U5).
- Missing `DISTINCT` on repeated snapshots.
- Treating NULL as active.
- Counting resubscriptions as the number of periods (a first subscription is not a resubscription).
- Using `julianday` differences with an assumed integer type; the key is a float here and equal values compare exactly because all values are whole day numbers.

### Q34 ⭐ 🟡 Longest run of zeros or increases: readings(ts, value) with integer values and possible NULLs. Return the longest run of consecutive zero readings and the longest run of strictly increasing readings (each value greater than the previous) with their start and end timestamps. Show the flag-and-group method for both, the ROW_NUMBER difference for zeros, and what NULL, equal readings and a single-row table do to each.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Both are runs: for zeros, flag `value = 0` and group by the running count of non-zero rows (or subtract two ROW_NUMBERs); for increases, flag `value > LAG(value)` and group by the running count of non-increase rows, so each group is a starting reading followed by its rises; and NULL breaks both because every comparison with NULL is not true.

**Schema and sample data:** sixteen hourly readings on 2024-03-01 (hour 0 to 15). The Code block inserts these rows in reverse order (built from a Python list), so the input is unsorted.
```sql
CREATE TABLE readings(ts TEXT, value INTEGER);
INSERT INTO readings VALUES
 ('2024-03-01 00:00',0),('2024-03-01 01:00',0),('2024-03-01 02:00',3),('2024-03-01 03:00',0),
 ('2024-03-01 04:00',0),('2024-03-01 05:00',0),('2024-03-01 06:00',NULL),('2024-03-01 07:00',0),
 ('2024-03-01 08:00',0),('2024-03-01 09:00',1),('2024-03-01 10:00',2),('2024-03-01 11:00',2),
 ('2024-03-01 12:00',5),('2024-03-01 13:00',6),('2024-03-01 14:00',7),('2024-03-01 15:00',3);
```

**SQL answer:** the three queries are `SQL_ZEROS`, `SQL_ZEROS_FLAG` and `SQL_UP` in the Code block. Zeros by ROW_NUMBER difference (the partition is the 0/1 flag, with `COALESCE` turning a NULL comparison into 0):
```sql
WITH r AS (
  SELECT ts,
         ROW_NUMBER() OVER (ORDER BY ts) AS rn_all,
         ROW_NUMBER() OVER (PARTITION BY COALESCE(value = 0, 0) ORDER BY ts) AS rn_part,
         COALESCE(value = 0, 0) AS is_zero
  FROM readings
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM r
WHERE is_zero = 1
GROUP BY rn_all - rn_part
ORDER BY readings DESC, run_start
LIMIT 1
```
Zeros by flag and group:
```sql
WITH f AS (
  SELECT ts, COALESCE(value = 0, 0) AS is_zero FROM readings
),
g AS (
  SELECT ts, is_zero, SUM(1 - is_zero) OVER (ORDER BY ts) AS grp FROM f
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM g
WHERE is_zero = 1
GROUP BY grp
ORDER BY readings DESC, run_start
LIMIT 1
```
Increasing runs by flag and group. A group starts at every row that is not a rise and holds the following rises, so `COUNT(*)` counts readings (a run of k rises has k + 1 readings), and `HAVING COUNT(*) >= 2` removes groups with no rise at all:
```sql
WITH f AS (
  SELECT ts, COALESCE(value > LAG(value) OVER (ORDER BY ts), 0) AS up FROM readings
),
g AS (
  SELECT ts, up, SUM(1 - up) OVER (ORDER BY ts) AS grp FROM f
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM g
GROUP BY grp
HAVING COUNT(*) >= 2
ORDER BY readings DESC, run_start
LIMIT 1
```

**pandas answer:** same logic, identical to the Code block (`eq(0)` and `gt(shift())` give False for NaN, as the COALESCE does in SQL):
```py
def longest_runs(df):
    r = df.sort_values("ts").reset_index(drop=True)
    r["value"] = r["value"].astype("float64")     # an all-NULL column arrives as object dtype
    zero = r["value"].eq(0)                      # NaN == 0 is False
    zg = (~zero).cumsum()
    up = r["value"].gt(r["value"].shift())       # NaN comparisons are False
    ug = (~up).cumsum()
    def best(mask, grp, min_len):
        x = r[mask].groupby(grp[mask]).agg(run_start=("ts", "min"), run_end=("ts", "max"), readings=("ts", "size"))
        x = x[x["readings"] >= min_len].sort_values(["readings", "run_start"], ascending=[False, True])
        return None if x.empty else (x.iloc[0]["run_start"], x.iloc[0]["run_end"], int(x.iloc[0]["readings"]))
    all_rows = pd.Series(True, index=r.index)
    return best(zero, zg, 1), best(all_rows, ug, 2)
```

**Example:** zeros are at hours 0-1, 3-5, 7-8, with a NULL at hour 6.
- Flag-and-group for zeros: the running count of non-zero rows goes up at hour 2 (value 3) and at hour 6 (the NULL counts as non-zero), so hours 0-1 are one group, hours 3-5 another and hours 7-8 a third (each group also holds the non-zero row that opened it, which the `WHERE is_zero = 1` filter removes). The largest group has 3 zero rows, hours 3 to 5. Because the NULL row splits 3-5 from 7-8, the answer is 3; if NULL were ignored they would join into a run of 5.
- Increases: the values 0 (hour 8), 1, 2 rise twice (a run of 3 readings, hours 8-10); hour 11 repeats the value 2, which is not a rise, so a new group starts at hour 11; 2, 5, 6, 7 rise three times, a run of 4 readings from hour 11 to hour 14; hour 15 (value 3) falls. The longest is 4 readings, 11:00 to 14:00. The earlier pair at hours 1-2 (0 then 3) is a run of 2.
- Answer: zeros `03:00` to `05:00` (3 readings); increasing `11:00` to `14:00` (4 readings).

**Code:** run with `python3 -I`. The asserts compare the two SQL zero methods, the pandas results with SQL (tuples of start, end, readings), and nine edge-case tables in SQL and pandas. Ties are broken by the earliest start.
```python
# Q34: longest run of zeros and of strictly increasing readings, SQL + pandas
import sqlite3
import pandas as pd

VALUES = [0, 0, 3, 0, 0, 0, None, 0, 0, 1, 2, 2, 5, 6, 7, 3]
def load(con, vals):
    con.execute("DROP TABLE IF EXISTS readings")
    con.execute("CREATE TABLE readings(ts TEXT, value INTEGER)")
    rows = [("2024-03-01 %02d:00" % h, v) for h, v in enumerate(vals)]
    rows = rows[::-1]  # insert in reverse order: input is unsorted
    con.executemany("INSERT INTO readings VALUES (?, ?)", rows)

SQL_ZEROS = """
WITH r AS (
  SELECT ts,
         ROW_NUMBER() OVER (ORDER BY ts) AS rn_all,
         ROW_NUMBER() OVER (PARTITION BY COALESCE(value = 0, 0) ORDER BY ts) AS rn_part,
         COALESCE(value = 0, 0) AS is_zero
  FROM readings
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM r
WHERE is_zero = 1
GROUP BY rn_all - rn_part
ORDER BY readings DESC, run_start
LIMIT 1
"""
SQL_ZEROS_FLAG = """
WITH f AS (
  SELECT ts, COALESCE(value = 0, 0) AS is_zero FROM readings
),
g AS (
  SELECT ts, is_zero, SUM(1 - is_zero) OVER (ORDER BY ts) AS grp FROM f
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM g
WHERE is_zero = 1
GROUP BY grp
ORDER BY readings DESC, run_start
LIMIT 1
"""
SQL_UP = """
WITH f AS (
  SELECT ts, COALESCE(value > LAG(value) OVER (ORDER BY ts), 0) AS up FROM readings
),
g AS (
  SELECT ts, up, SUM(1 - up) OVER (ORDER BY ts) AS grp FROM f
)
SELECT MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS readings
FROM g
GROUP BY grp
HAVING COUNT(*) >= 2
ORDER BY readings DESC, run_start
LIMIT 1
"""
def run(con, sql):
    r = con.execute(sql).fetchall()
    return r[0] if r else None

con = sqlite3.connect(":memory:")
load(con, VALUES)
z = run(con, SQL_ZEROS); zf = run(con, SQL_ZEROS_FLAG); up = run(con, SQL_UP)
print("zeros, ROW_NUMBER difference:", z)
print("zeros, flag and group:       ", zf)
print("increasing run:              ", up)
assert z == zf

readings = pd.read_sql_query("SELECT * FROM readings", con)
# pd:main
def longest_runs(df):
    r = df.sort_values("ts").reset_index(drop=True)
    r["value"] = r["value"].astype("float64")     # an all-NULL column arrives as object dtype
    zero = r["value"].eq(0)                      # NaN == 0 is False
    zg = (~zero).cumsum()
    up = r["value"].gt(r["value"].shift())       # NaN comparisons are False
    ug = (~up).cumsum()
    def best(mask, grp, min_len):
        x = r[mask].groupby(grp[mask]).agg(run_start=("ts", "min"), run_end=("ts", "max"), readings=("ts", "size"))
        x = x[x["readings"] >= min_len].sort_values(["readings", "run_start"], ascending=[False, True])
        return None if x.empty else (x.iloc[0]["run_start"], x.iloc[0]["run_end"], int(x.iloc[0]["readings"]))
    all_rows = pd.Series(True, index=r.index)
    return best(zero, zg, 1), best(all_rows, ug, 2)
# pd:end
pz, pu = longest_runs(readings)
print("pandas zeros:", pz, " pandas increasing:", pu)
assert pz == z and pu == up   # tuples (run_start, run_end, readings)

print("--- edge cases (zeros, increasing) ---")
for name, vals in [("empty", []), ("one zero", [0]), ("one non-zero", [5]), ("one NULL", [None]),
                   ("all NULL", [None, None]), ("flat 4,4,4", [4, 4, 4]),
                   ("0,NULL,0 (NULL splits)", [0, None, 0]),
                   ("1,2,NULL,3,4 (NULL splits)", [1, 2, None, 3, 4]),
                   ("tie 1,2,3 then 0,5,6", [1, 2, 3, 0, 5, 6])]:
    load(con, vals)
    df = pd.read_sql_query("SELECT * FROM readings", con)
    s = (run(con, SQL_ZEROS), run(con, SQL_UP))
    p = longest_runs(df) if len(df) else (None, None)
    assert s == p, (name, s, p)
    print(name, "->", s)
print("asserts passed")
```

**Output (my run):**
```text
zeros, ROW_NUMBER difference: ('2024-03-01 03:00', '2024-03-01 05:00', 3)
zeros, flag and group:        ('2024-03-01 03:00', '2024-03-01 05:00', 3)
increasing run:               ('2024-03-01 11:00', '2024-03-01 14:00', 4)
pandas zeros: ('2024-03-01 03:00', '2024-03-01 05:00', 3)  pandas increasing: ('2024-03-01 11:00', '2024-03-01 14:00', 4)
--- edge cases (zeros, increasing) ---
empty -> (None, None)
one zero -> (('2024-03-01 00:00', '2024-03-01 00:00', 1), None)
one non-zero -> (None, None)
one NULL -> (None, None)
all NULL -> (None, None)
flat 4,4,4 -> (None, None)
0,NULL,0 (NULL splits) -> (('2024-03-01 00:00', '2024-03-01 00:00', 1), None)
1,2,NULL,3,4 (NULL splits) -> (None, ('2024-03-01 00:00', '2024-03-01 01:00', 2))
tie 1,2,3 then 0,5,6 -> (('2024-03-01 03:00', '2024-03-01 03:00', 1), ('2024-03-01 00:00', '2024-03-01 02:00', 3))
asserts passed
```

**Edge cases:**
- NULL: breaks a zero run (`0, NULL, 0` gives runs of 1, not 2) and breaks an increasing run (`1, 2, NULL, 3, 4` gives a run of 2, not 4), because `NULL > x`, `x > NULL` and `NULL = 0` are not true. If NULLs are sensor dropouts that should be skipped, filter them out first, but then the run no longer means consecutive readings.
- Equal readings (`4, 4, 4`) are not increases: no increasing run is returned. A repeated value ends a run and starts the next one.
- Single-row table: a lone `0` is a zero run of 1; a lone non-zero or a lone NULL returns no zero run; no table of one reading has an increasing run (I require at least two readings, so it returns nothing).
- Empty table: both queries return no row (checked in SQL and pandas); do not expect a row of zeros.
- Ties between equally long runs (`1, 2, 3` then `0, 5, 6`): `ORDER BY readings DESC, run_start` picks the earliest; say the rule or return all tied runs.
- All-NULL column: pandas receives an object column of `None` from `read_sql_query` and `gt` raised `TypeError` in my first run, so the code casts the column with `astype("float64")` before comparing.
- Timestamps are assumed to be one per time step; a missing hour is not detected. If a missing reading should break a run, add the day-number check from Q40.

**Then explain:**
- Flag-and-group turns "consecutive rows with a property" into a running count of the rows without it; the same pattern covers Q13 (status runs) and Q23 (stock up-streaks).
- The ROW_NUMBER difference needs the two numberings to advance together inside a run: all-rows numbering minus numbering within the partition `value = 0`. It is shorter for equality-based runs but cannot express "greater than the previous row", which depends on a neighbour, so increases use LAG.
- A run of k rises has k + 1 readings; decide whether "length" is rises or readings and state it (I report readings).
- Dialects (not executed here): window functions as written are standard; `COALESCE(value = 0, 0)` relies on SQLite treating a comparison as an integer, while PostgreSQL, as I remember it, wants `CASE WHEN value = 0 THEN 1 ELSE 0 END` because its comparison returns a boolean, not an integer.

**Follow-ups:**
- Longest non-decreasing run? Use `>=` in the flag; equal readings then continue the run.
- All runs of zeros of at least 3 readings? Drop `LIMIT 1` and add `HAVING COUNT(*) >= 3`.
- Per sensor? Add `PARTITION BY sensor_id` to every window and the sensor to the group key.

**Common mistakes:**
- Ignoring NULL and gluing runs across a dropout.
- Counting rises instead of readings (off by one) or the other way round without saying so.
- Using `GROUP BY value` and merging separate zero runs.
- Forgetting the first row has no previous value (`NULL > x` is not a rise, which is right, but write it explicitly).
- Assuming `value > LAG(value)` is a valid integer in every dialect.

### Q35 ⭐ 🟡 Hot streak per player: games(player_id, game_no, points). A hot streak is three or more consecutive games with at least 30 points. Return each hot streak per player (start game, end game, length, average points), and the player with the longest hot streak. Explain why a game with exactly 30 points is inside (>=) and a missing game_no (a gap in the numbering) ends the streak only if game_no, not row order, is used for the island key.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Keep games with `points >= 30`, deduplicate, and group by `game_no - ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no)`; keep groups with at least 3 games; the key uses `game_no`, not row position, so a missing game number ends the streak.

**Schema and sample data:** eight players, 33 rows, inserted unsorted. P1 has two streaks (one of 3 and one of 4 games, split by a 10-point game). P2 has no game 4. P3 has one game. P4 has 29, 30, 31. P5 scores exactly 30 three times. P6 has a NULL in game 2. P7 has game 2 twice. P8 has a 4-game streak tying P1's longest.
```sql
CREATE TABLE games(player_id TEXT, game_no INTEGER, points INTEGER);
INSERT INTO games VALUES
 ('P1',8,36),('P1',1,35),('P1',2,30),('P1',3,41),('P1',4,10),('P1',5,32),('P1',6,33),('P1',7,34),
 ('P2',1,40),('P2',2,40),('P2',3,40),('P2',5,40),('P2',6,40),
 ('P3',1,40),
 ('P4',1,29),('P4',2,30),('P4',3,31),
 ('P5',1,30),('P5',2,30),('P5',3,30),
 ('P6',1,31),('P6',2,NULL),('P6',3,32),('P6',4,33),('P6',5,34),
 ('P7',1,35),('P7',2,35),('P7',2,35),('P7',3,35),
 ('P8',1,31),('P8',2,32),('P8',3,33),('P8',4,34);
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
WITH hot AS (
  SELECT DISTINCT player_id, game_no, points FROM games WHERE points >= 30
),
r AS (
  SELECT *, game_no - ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS k FROM hot
)
SELECT player_id, MIN(game_no) AS start_game, MAX(game_no) AS end_game,
       COUNT(*) AS length, ROUND(AVG(points), 2) AS avg_points
FROM r
GROUP BY player_id, k
HAVING COUNT(*) >= 3
ORDER BY player_id, start_game
```
The longest-streak player is `SQL_LONGEST`, which wraps `SQL_MAIN` as `s` and keeps rows where `length = (SELECT MAX(length) FROM s)`, so ties are all returned:
```sql
WITH s AS (
WITH hot AS (
  SELECT DISTINCT player_id, game_no, points FROM games WHERE points >= 30
),
r AS (
  SELECT *, game_no - ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS k FROM hot
)
SELECT player_id, MIN(game_no) AS start_game, MAX(game_no) AS end_game,
       COUNT(*) AS length, ROUND(AVG(points), 2) AS avg_points
FROM r
GROUP BY player_id, k
HAVING COUNT(*) >= 3

)
SELECT player_id, start_game, end_game, length FROM s
WHERE length = (SELECT MAX(length) FROM s)
ORDER BY player_id
```
The comparison queries in the Code block are `SQL_ROWORDER` (row order instead of `game_no`), `SQL_NODEDUP` (no `DISTINCT`) and `SQL_GT30` (`> 30`).

**pandas answer:** same logic, identical to the Code block:
```py
h = games[games["points"] >= 30].drop_duplicates()       # NaN >= 30 is False, so NULL points drop out
h = h.sort_values(["player_id", "game_no"])
h["k"] = h["game_no"] - (h.groupby("player_id").cumcount() + 1)
pd_df = (h.groupby(["player_id", "k"])
          .agg(start_game=("game_no", "min"), end_game=("game_no", "max"),
               length=("game_no", "size"), avg_points=("points", "mean")).reset_index())
pd_df = pd_df[pd_df["length"] >= 3].drop(columns="k")
pd_df["avg_points"] = pd_df["avg_points"].round(2)
pd_df = pd_df.sort_values(["player_id", "start_game"]).reset_index(drop=True)
pd_longest = pd_df[pd_df["length"] == pd_df["length"].max()][["player_id", "start_game", "end_game", "length"]]
```

**Example:**
- P1 games 1-8 have points 35, 30, 41, 10, 32, 33, 34, 36. Game 4 (10 points) is filtered out. Hot games are 1, 2, 3, 5, 6, 7, 8 with row numbers 1 to 7, so `game_no - rn` is 0 for games 1-3 and 1 for games 5-8: streak 1-3 (3 games, average (35 + 30 + 41) / 3 = 35.33) and streak 5-8 (4 games, average (32 + 33 + 34 + 36) / 4 = 33.75).
- P2 has games 1, 2, 3, 5, 6, all 40 points. Keys: 1 - 1 = 0, 0, 0, then 5 - 4 = 1, 1. Streak 1-3 (3 games) and 5-6 (2 games, below 3, discarded). Using row position instead (`SQL_ROWORDER`) merges them into one 5-game streak 1-6, which is wrong because game 4 is missing.
- P5 has exactly 30 points three times, so with `>= 30` it is a 3-game streak; with `> 30` it vanishes.
- P6: game 2 has NULL points, `NULL >= 30` is not true, so it is dropped and games 3-5 form a streak of 3 (game 1 is alone).
- P7 has game 2 twice. After `DISTINCT` it is one streak 1-3. Without `DISTINCT` the key sequence is 0, 0, -1, -1 and the run splits into two pairs, so P7 disappears.
- P1 (last streak 4) and P8 (1-4, 4 games) tie for the longest: both are returned.

**Code:** run with `python3 -I`. The asserts compare the pandas streak table and the longest-streak table with SQL after sorting by `player_id, start_game`.
```python
# Q35: hot streaks (>= 3 consecutive games with >= 30 points) per player, SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE games(player_id TEXT, game_no INTEGER, points INTEGER);
INSERT INTO games VALUES
 ('P1',8,36),('P1',1,35),('P1',2,30),('P1',3,41),('P1',4,10),('P1',5,32),('P1',6,33),('P1',7,34),
 ('P2',1,40),('P2',2,40),('P2',3,40),('P2',5,40),('P2',6,40),
 ('P3',1,40),
 ('P4',1,29),('P4',2,30),('P4',3,31),
 ('P5',1,30),('P5',2,30),('P5',3,30),
 ('P6',1,31),('P6',2,NULL),('P6',3,32),('P6',4,33),('P6',5,34),
 ('P7',1,35),('P7',2,35),('P7',2,35),('P7',3,35),
 ('P8',1,31),('P8',2,32),('P8',3,33),('P8',4,34);
"""
SQL_MAIN = """
WITH hot AS (
  SELECT DISTINCT player_id, game_no, points FROM games WHERE points >= 30
),
r AS (
  SELECT *, game_no - ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS k FROM hot
)
SELECT player_id, MIN(game_no) AS start_game, MAX(game_no) AS end_game,
       COUNT(*) AS length, ROUND(AVG(points), 2) AS avg_points
FROM r
GROUP BY player_id, k
HAVING COUNT(*) >= 3
ORDER BY player_id, start_game
"""
SQL_LONGEST = """
WITH s AS (""" + SQL_MAIN.replace("ORDER BY player_id, start_game", "") + """)
SELECT player_id, start_game, end_game, length FROM s
WHERE length = (SELECT MAX(length) FROM s)
ORDER BY player_id
"""
SQL_ROWORDER = """
WITH t AS (
  SELECT DISTINCT player_id, game_no, points FROM games
),
n AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS rn_all FROM t
),
h AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no) AS rn_hot
  FROM n WHERE points >= 30
)
SELECT player_id, MIN(game_no) AS start_game, MAX(game_no) AS end_game, COUNT(*) AS length
FROM h
GROUP BY player_id, rn_all - rn_hot
HAVING COUNT(*) >= 3
ORDER BY player_id, start_game
"""
SQL_NODEDUP = SQL_MAIN.replace("SELECT DISTINCT player_id, game_no, points FROM games", "SELECT player_id, game_no, points FROM games")
SQL_GT30 = SQL_MAIN.replace("points >= 30", "points > 30")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL hot streaks:"); print(sql_df.to_string(index=False))
longest = pd.read_sql_query(SQL_LONGEST, con)
print("longest hot streak (ties kept):"); print(longest.to_string(index=False))
print("wrong, row order instead of game_no (P2 merges across missing game 4):")
print(pd.read_sql_query(SQL_ROWORDER, con).to_string(index=False))
print("wrong, no DISTINCT (P7 duplicate game 2 splits the run):")
print(pd.read_sql_query(SQL_NODEDUP, con).to_string(index=False))
print("wrong, points > 30 (P5 with exactly 30 disappears):")
print(pd.read_sql_query(SQL_GT30, con)["player_id"].tolist())

games = pd.read_sql_query("SELECT * FROM games", con)
# pd:main
h = games[games["points"] >= 30].drop_duplicates()       # NaN >= 30 is False, so NULL points drop out
h = h.sort_values(["player_id", "game_no"])
h["k"] = h["game_no"] - (h.groupby("player_id").cumcount() + 1)
pd_df = (h.groupby(["player_id", "k"])
          .agg(start_game=("game_no", "min"), end_game=("game_no", "max"),
               length=("game_no", "size"), avg_points=("points", "mean")).reset_index())
pd_df = pd_df[pd_df["length"] >= 3].drop(columns="k")
pd_df["avg_points"] = pd_df["avg_points"].round(2)
pd_df = pd_df.sort_values(["player_id", "start_game"]).reset_index(drop=True)
pd_longest = pd_df[pd_df["length"] == pd_df["length"].max()][["player_id", "start_game", "end_game", "length"]]
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
# compare after sorting by player_id, start_game
assert pd_df.astype(sql_df.dtypes.to_dict()).equals(sql_df)
assert pd_longest.reset_index(drop=True).astype(longest.dtypes.to_dict()).equals(longest)
print("asserts passed")
```

**Output (my run):**
```text
SQL hot streaks:
player_id  start_game  end_game  length  avg_points
       P1           1         3       3       35.33
       P1           5         8       4       33.75
       P2           1         3       3       40.00
       P5           1         3       3       30.00
       P6           3         5       3       33.00
       P7           1         3       3       35.00
       P8           1         4       4       32.50
longest hot streak (ties kept):
player_id  start_game  end_game  length
       P1           5         8       4
       P8           1         4       4
wrong, row order instead of game_no (P2 merges across missing game 4):
player_id  start_game  end_game  length
       P1           1         3       3
       P1           5         8       4
       P2           1         6       5
       P5           1         3       3
       P6           3         5       3
       P7           1         3       3
       P8           1         4       4
wrong, no DISTINCT (P7 duplicate game 2 splits the run):
player_id  start_game  end_game  length  avg_points
       P1           1         3       3       35.33
       P1           5         8       4       33.75
       P2           1         3       3       40.00
       P5           1         3       3       30.00
       P6           3         5       3       33.00
       P8           1         4       4       32.50
wrong, points > 30 (P5 with exactly 30 disappears):
['P1', 'P2', 'P6', 'P7', 'P8']
pandas:
player_id  start_game  end_game  length  avg_points
       P1           1         3       3       35.33
       P1           5         8       4       33.75
       P2           1         3       3       40.00
       P5           1         3       3       30.00
       P6           3         5       3       33.00
       P7           1         3       3       35.00
       P8           1         4       4       32.50
asserts passed
```

**Edge cases:**
- Exactly 30: included by `>=`; the question says "at least 30", so the boundary belongs inside (P5, and game 2 of P1). Using `>` dropped P5 from the result in my run (the players left were P1, P2, P6, P7, P8); P1 also loses its 1-3 streak by the same logic, but keeps its 5-8 streak.
- Missing `game_no` (P2): only the `game_no`-based key splits there. A row-order key (`rn_all - rn_hot`, which is what you get when you number rows and then compare with a second ROW_NUMBER) merges across the hole. If the numbering can have gaps for a reason that should not break a streak (a game with no data), say so and use row order deliberately.
- Duplicate `game_no` (P7): dedupe first. Two rows for one game with different points would need a rule (take the max, or reject), which SQL cannot guess.
- NULL points (P6): not hot; this ends the streak, which is the safe reading ("unknown" is not 30 or more).
- Single-row player (P3) and a player whose longest streak is 2 (P4, 30 and 31): no output row.
- Ties for longest: `SQL_LONGEST` returns every tied player. `LIMIT 1` would pick one arbitrarily unless you add a tie-break.
- Players with no hot streak do not appear at all; if the output must list all players, `LEFT JOIN` from a players table.
- Unsorted input is fine because the window orders by `game_no`.

**Then explain:**
- A streak is a property of consecutive game numbers, so the key must be built from the numbers: the difference `game_no - rn` is constant exactly when `game_no` grows by one with each hot row.
- Filter first (`WHERE points >= 30`), then number: the numbering must run along the hot rows only.
- `HAVING COUNT(*) >= 3` turns islands into streaks; the length threshold is a parameter.
- Dialects (not executed here): the same SQL runs on PostgreSQL and MySQL 8; MySQL 5.7 has no window functions.

**Follow-ups:**
- Longest streak per player only? Rank streaks per player (Part 4 style) and keep rank 1.
- Different threshold (at least 4 games)? Change the `HAVING`.
- Current hot streak? Q15 logic on game numbers.

**Common mistakes:**
- `points > 30`.
- `ROW_NUMBER() OVER (ORDER BY game_no)` without `PARTITION BY player_id`, so keys leak across players.
- Using row position instead of `game_no` (shown: P2 becomes a 5-game streak).
- Not deduplicating (shown: P7 vanishes).
- Taking `MAX(length)` in a plain `GROUP BY`, which loses the start and end.

### Q36 ⭐ 🟡 rolling-based consecutive checks in pandas: for a boolean or 0/1 Series, find positions inside three or more in a row with rolling(3).min() == 1 and how to mark all rows of the run (not only the last one) by combining forward and backward windows. Contrast with groupby on the shift key, np.diff on the flag array and itertools.groupby for a longest run, and cover NaN in the first rows (min_periods), dtype of the result and speed on a large series (hedge anything not measured).
**Asked at:** pandas Series.shift reference (opened) and search snippets of Stack Overflow and Towards Data Science run-grouping answers ((s != s.shift()).cumsum(), diff().ne(0).cumsum(); not opened); documentation and guides, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `rolling(3).min() == 1` is True only on the last row of each three-in-a-row window; to mark every row of the run, spread it back over the previous two rows with a reversed window (or a forward window), or skip rolling and group by the run key and test the run size.

**Schema and sample data:** a 0/1 Series of 13 positions, `[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]`: runs of ones of length 2 (positions 0-1), 3 (positions 3-5), 4 (positions 7-10) and 1 (position 12). The same data is loaded into SQLite as `f(pos, flag)` so the rolling check can be compared with a window-frame query.
```sql
CREATE TABLE f(pos INTEGER, flag INTEGER);
INSERT INTO f VALUES (0,1),(1,1),(2,0),(3,1),(4,1),(5,1),(6,0),(7,1),(8,1),(9,1),(10,1),(11,0),(12,1);
```

**SQL answer:** `SQL_MAIN` in the Code block, the same rolling check as a window frame. `COUNT(flag) OVER w3 = 3` makes the first two rows (frames with fewer than three rows) fail, and the outer `MAX(end3) OVER (... ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)` spreads each qualifying window end back over the two rows before it:
```sql
WITH e AS (
  SELECT pos, flag,
         CASE WHEN COUNT(flag) OVER w3 = 3 AND MIN(flag) OVER w3 = 1 THEN 1 ELSE 0 END AS end3
  FROM f
  WINDOW w3 AS (ORDER BY pos ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
)
SELECT pos, MAX(end3) OVER (ORDER BY pos ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) AS in_run
FROM e
ORDER BY pos
```

**pandas answer:** same logic, identical to the Code block:
```py
end3 = s.rolling(3).min().eq(1)                                   # True only on the LAST row of each 3-window
in_run = end3[::-1].rolling(3, min_periods=1).max().astype(bool)[::-1]   # spread back over the next 2 rows
key = (s != s.shift()).cumsum()                                   # run key
size = s.groupby(key).transform("size")
in_run_key = s.eq(1) & size.ge(3)
```
The Code block also runs the other three methods (`np.diff` on the zero-padded array, `itertools.groupby`, and `FixedForwardWindowIndexer`) and asserts they agree.

**Example:** positions 0 to 12 with values 1 1 0 1 1 1 0 1 1 1 1 0 1.
- `rolling(3).min()` is 1 where the window of three ending at that row is all ones: position 5 (positions 3-5), position 9 (7-9) and position 10 (8-10). So `end3` has True at 5, 9 and 10 only, which marks one row of the first run and two of the second.
- Spreading back: a row is inside a run if a qualifying window ends at that row or at one of the next two rows. Position 3 sees the window ending at 5; positions 7 and 8 see the windows ending at 9 and 10; and so on. Result: True at 3, 4, 5 and 7, 8, 9, 10.
- Run key `(s != s.shift()).cumsum()` gives run sizes 2, 1, 3, 1, 4, 1, 1; `s.eq(1) & size >= 3` is True on exactly the same seven positions.
- `np.diff` of `[0] + flags + [0]` has `+1` at run starts and `-1` after run ends: runs (start, length) = (0,2), (3,3), (7,4), (12,1). `itertools.groupby` gives the same runs as (value, length) pairs, with 4 the longest.

**Code:** run with `python3 -I`. All methods are asserted equal on the mask (compared position by position) and on the longest run; the timing line is measured on this machine on 1,000,000 random flags and will differ on yours.
```python
# Q36: three-or-more-in-a-row checks in pandas: rolling, run keys, np.diff, itertools.groupby (+ SQL window frame)
import itertools
import sqlite3
import time
import numpy as np
import pandas as pd

flags = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]
s = pd.Series(flags, name="flag")

# pd:main
end3 = s.rolling(3).min().eq(1)                                   # True only on the LAST row of each 3-window
in_run = end3[::-1].rolling(3, min_periods=1).max().astype(bool)[::-1]   # spread back over the next 2 rows
key = (s != s.shift()).cumsum()                                   # run key
size = s.groupby(key).transform("size")
in_run_key = s.eq(1) & size.ge(3)
# pd:end
print("flag      :", flags)
print("end3      :", end3.astype(int).tolist())
print("in_run    :", in_run.astype(int).tolist())
print("in_run key:", in_run_key.astype(int).tolist())
assert in_run.equals(in_run_key)

# forward-looking window object gives the same mask
fwd = pd.api.indexers.FixedForwardWindowIndexer(window_size=3)
start3 = s.rolling(fwd).min().eq(1)                               # True on the FIRST row of each 3-window
in_run_fwd = (end3.astype(int) | start3.astype(int)).astype(bool)
mid = s.rolling(3, center=True).min().eq(1)
in_run_all = (end3 | start3 | mid)
assert in_run_all.equals(in_run_key)
print("end|start|centre windows equal the run-size mask:", True)

# np.diff on the padded flag array: starts and ends of every run of ones
a = np.asarray(flags)
d = np.diff(np.concatenate(([0], a, [0])))
starts = np.flatnonzero(d == 1); ends = np.flatnonzero(d == -1)    # end index is exclusive
lengths = ends - starts
print("np.diff runs (start, length):", list(zip(starts.tolist(), lengths.tolist())))
mask_np = np.zeros(len(a), dtype=bool)
for st, ln in zip(starts, lengths):
    if ln >= 3:
        mask_np[st:st + ln] = True
assert (mask_np == in_run_key.to_numpy()).all()

# itertools.groupby for the longest run of ones
runs = [(k, len(list(g))) for k, g in itertools.groupby(flags)]
longest_it = max(n for k, n in runs if k == 1)
print("itertools runs:", runs, "longest run of ones:", longest_it)
assert longest_it == int(lengths.max()) == int(size[s.eq(1)].max())

# SQL: the same rolling check as a window frame
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE f(pos INTEGER, flag INTEGER)")
con.executemany("INSERT INTO f VALUES (?, ?)", list(enumerate(flags)))
SQL_MAIN = """
WITH e AS (
  SELECT pos, flag,
         CASE WHEN COUNT(flag) OVER w3 = 3 AND MIN(flag) OVER w3 = 1 THEN 1 ELSE 0 END AS end3
  FROM f
  WINDOW w3 AS (ORDER BY pos ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
)
SELECT pos, MAX(end3) OVER (ORDER BY pos ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) AS in_run
FROM e
ORDER BY pos
"""
sql_mask = [r[1] for r in con.execute(SQL_MAIN)]
print("SQL in_run:", sql_mask)
assert sql_mask == in_run_key.astype(int).tolist()

# NaN in the first rows and min_periods
sn = pd.Series([np.nan, 1, 1, 1, 1, 0, 1, 1, np.nan, 1, 1, 1], dtype="float64")
print("with NaN, default min_periods :", sn.rolling(3).min().eq(1).astype(int).tolist())
print("with NaN, min_periods=1 (wrong):", sn.rolling(3, min_periods=1).min().eq(1).astype(int).tolist())
print("rolling(3).min() raw:", sn.rolling(3).min().tolist())
# dtype of results
print("dtypes: rolling min", s.rolling(3).min().dtype, "| eq(1)", end3.dtype, "| bool input ->",
      s.astype(bool).rolling(3).min().dtype)

# speed on a large series (best of 3; this machine only, not a benchmark claim)
rng = np.random.default_rng(0)
big = pd.Series((rng.random(1_000_000) < 0.7).astype(int))
def t(fn):
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter(); fn(); best = min(best, time.perf_counter() - t0)
    return round(best * 1000, 1)
def m_roll():
    e = big.rolling(3).min().eq(1)
    return e[::-1].rolling(3, min_periods=1).max().astype(bool)[::-1]
def m_key():
    k = (big != big.shift()).cumsum()
    return big.eq(1) & big.groupby(k).transform("size").ge(3)
def m_np():
    x = big.to_numpy(); dd = np.diff(np.concatenate(([0], x, [0])))
    return np.flatnonzero(dd == 1), np.flatnonzero(dd == -1)
def m_it():
    return max((len(list(g)) for k, g in itertools.groupby(big.tolist()) if k == 1), default=0)
r1, r2 = m_roll(), m_key()
assert r1.equals(r2)
print("1,000,000 rows, ms (best of 3): rolling", t(m_roll), "| shift-key groupby", t(m_key),
      "| np.diff", t(m_np), "| itertools.groupby (longest only)", t(m_it))
print("asserts passed")
```

**Output (my run):**
```text
flag      : [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]
end3      : [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
in_run    : [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0]
in_run key: [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0]
end|start|centre windows equal the run-size mask: True
np.diff runs (start, length): [(0, 2), (3, 3), (7, 4), (12, 1)]
itertools runs: [(1, 2), (0, 1), (1, 3), (0, 1), (1, 4), (0, 1), (1, 1)] longest run of ones: 4
SQL in_run: [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0]
with NaN, default min_periods : [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
with NaN, min_periods=1 (wrong): [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]
rolling(3).min() raw: [nan, nan, nan, 1.0, 1.0, 0.0, 0.0, 0.0, nan, nan, nan, 1.0]
dtypes: rolling min float64 | eq(1) bool | bool input -> float64
1,000,000 rows, ms (best of 3): rolling 37.3 | shift-key groupby 48.7 | np.diff 3.5 | itertools.groupby (longest only) 42.7
asserts passed
```

**Edge cases:**
- NaN and `min_periods`: with the default (`min_periods` equal to the window size), any window containing a NaN gives NaN, so the first two rows and any window touching a NaN are never True: the mask is conservative. With `min_periods=1`, `rolling(3, min_periods=1).min()` is computed over the non-NaN values that are present, so a single 1 in position 1 (after a NaN) gives 1 and the check says "three in a row" at row 1: wrong, as my run shows (`[0, 1, 1, 1, 1, ...]`). Use `min_periods=1` only on the spreading step (`.max()`), never on the qualifying `.min()`.
- NaN in a flag Series forces float64; a boolean Series also comes back as float64 from `rolling(3).min()` in my run, so compare with `== 1` or `.astype(bool)`.
- The mask of "inside a run" differs from "end of a run": the first form needs the spreading step.
- Single run shorter than 3 (position 12) and runs of exactly 3 (positions 3-5, the boundary): included correctly.
- Ties for the longest run: `np.diff` and `itertools.groupby` return every run; pick the first or last explicitly.
- Empty Series: `rolling(3).min()` returns an empty Series; `itertools.groupby` yields nothing, so `max` needs `default=0` (not tested beyond that note).

**Then explain:**
- Rolling asks "is this window all ones", which is local; the run-key approach asks "how long is the run that contains me", which is global. Rolling is neat for a fixed N and awkward for "longest run" or for arbitrary N.
- To mark all rows of a run, combine the window ending at the row, the window starting at the row and the centred window, or spread the ends with a reversed `rolling(3, min_periods=1).max()`. I verified the three-window OR equals the run-size mask.
- Speed, measured here only: the last printed line of the Output block is the best of three runs on one million random 0/1 flags (about 70% ones), in milliseconds, for the rolling approach, the shift-key groupby, `np.diff` and `itertools.groupby` (longest run only, after `tolist()`). In the run pasted below `np.diff` was clearly the fastest and the other three were within a small factor of each other, but the numbers move between runs and machines, and depend on the pandas and NumPy build and the data density, so treat the ranking as indicative and re-measure before relying on it. I did not measure memory or any size other than one million.
- The SQL window frame above is the same idea: a three-row frame plus a forward frame.
- Dialects (not executed here): `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` and `CURRENT ROW AND 2 FOLLOWING` are standard window syntax in PostgreSQL, MySQL 8 and others.

**Follow-ups:**
- At least N in a row, N a variable? `rolling(N)` with `min_periods=N`, or the run-size test, which is independent of N.
- Run lengths per group? Add `groupby('entity')` to both the shift and the key, as in Q5.
- Longest run of zeros? Invert the flag first.

**Common mistakes:**
- Setting `min_periods=1` on the qualifying `min()` (marks a false run at the start).
- Reading `rolling(3).min() == 1` as "this row is in a run" when it only marks the window end.
- Using `groupby(s)` directly instead of the run key (merges separate runs).
- Forgetting that float NaN turns a 0/1 column into float64.
- Measuring speed on a tiny Series and generalising.

### Q37 ⭐ 🔴 Coverage and uncovered gaps of a range: shifts(guard_id, start_ts, end_ts) on one day, required coverage 09:00 to 18:00. Return the uncovered gaps in the window, handling overlapping shifts (merge first with the running MAX of end), shifts that start before 09:00 or end after 18:00 (clip), and a day with no shifts at all (one gap equal to the whole window). Also return the covered minutes and the coverage percentage.
**Asked at:** oneuptime interval-merge write-up (opened; running max of end, strict > so touching intervals merge) and the DataDriven 'The Overlap' interval-merge problem (opened; a Python problem, labelled hard and L5, no company named); practice-site material and not candidate reports; data scientist and data engineer rounds
**Say this first (1 line):** Clip every shift to the 09:00-18:00 window, drop shifts that become empty, add two zero-length sentinel intervals at 09:00 and 18:00, merge overlaps with a running MAX of the end (new block when the start is strictly greater), and the gaps are the spaces between consecutive merged blocks; covered minutes are the window minus the gap minutes.

**Schema and sample data:** one day, 2024-03-04, window `09:00` to `18:00` (540 minutes). Nine shift rows: g1 starts before the window, g2 overlaps g1, g3 is contained in g2, g4 starts exactly when g2 ends (touching), g5 appears twice (exact duplicate), g6 ends after the window, g7 is entirely before the window, g8 has a NULL end (still on shift, unknown).
```sql
CREATE TABLE shifts(guard_id TEXT, start_ts TEXT, end_ts TEXT);
INSERT INTO shifts VALUES
 ('g2','2024-03-04 10:00','2024-03-04 12:00'),
 ('g1','2024-03-04 08:00','2024-03-04 11:00'),
 ('g4','2024-03-04 12:00','2024-03-04 13:00'),
 ('g3','2024-03-04 11:30','2024-03-04 11:45'),
 ('g5','2024-03-04 14:00','2024-03-04 15:00'),
 ('g5','2024-03-04 14:00','2024-03-04 15:00'),
 ('g6','2024-03-04 16:00','2024-03-04 19:00'),
 ('g7','2024-03-04 06:00','2024-03-04 08:30'),
 ('g8','2024-03-04 17:00',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block, with the window passed as named parameters `:ws` and `:we`. `clipped` uses SQLite's two-argument scalar `MAX` and `MIN` (a NULL argument would make the result NULL, so rows with NULLs are filtered first); `pieces` adds the sentinels; `ordered` computes the running MAX of the earlier rows' ends with `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`, which is NULL for the first row; `merged` groups by the running block id; `nxt` takes `LEAD` of the next block's start:
```sql
WITH w AS (SELECT :ws AS ws, :we AS we),
clipped AS (
  SELECT MAX(s.start_ts, w.ws) AS st, MIN(s.end_ts, w.we) AS en
  FROM shifts s, w
  WHERE s.start_ts IS NOT NULL AND s.end_ts IS NOT NULL
),
pieces AS (
  SELECT st, en FROM clipped WHERE st < en
  UNION ALL SELECT ws, ws FROM w
  UNION ALL SELECT we, we FROM w
),
ordered AS (
  SELECT st, en,
         MAX(en) OVER (ORDER BY st, en ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM pieces
),
flagged AS (
  SELECT st, en,
         SUM(CASE WHEN prev_max IS NULL OR st > prev_max THEN 1 ELSE 0 END)
             OVER (ORDER BY st, en) AS blk
  FROM ordered
),
merged AS (
  SELECT MIN(st) AS b_start, MAX(en) AS b_end FROM flagged GROUP BY blk
),
nxt AS (
  SELECT b_end AS gap_start, LEAD(b_start) OVER (ORDER BY b_start) AS gap_end FROM merged
)
SELECT gap_start, gap_end,
       CAST((unixepoch(gap_end) - unixepoch(gap_start)) / 60 AS INTEGER) AS minutes
FROM nxt
WHERE gap_end > gap_start
ORDER BY gap_start
```
The coverage figures are `SQL_SUMMARY` in the Code block, which wraps `SQL_MAIN` as `g` and subtracts the sum of gap minutes from the window length (with `COALESCE(SUM(minutes), 0)` for the no-gap case):
```sql
WITH g AS (
WITH w AS (SELECT :ws AS ws, :we AS we),
clipped AS (
  SELECT MAX(s.start_ts, w.ws) AS st, MIN(s.end_ts, w.we) AS en
  FROM shifts s, w
  WHERE s.start_ts IS NOT NULL AND s.end_ts IS NOT NULL
),
pieces AS (
  SELECT st, en FROM clipped WHERE st < en
  UNION ALL SELECT ws, ws FROM w
  UNION ALL SELECT we, we FROM w
),
ordered AS (
  SELECT st, en,
         MAX(en) OVER (ORDER BY st, en ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM pieces
),
flagged AS (
  SELECT st, en,
         SUM(CASE WHEN prev_max IS NULL OR st > prev_max THEN 1 ELSE 0 END)
             OVER (ORDER BY st, en) AS blk
  FROM ordered
),
merged AS (
  SELECT MIN(st) AS b_start, MAX(en) AS b_end FROM flagged GROUP BY blk
),
nxt AS (
  SELECT b_end AS gap_start, LEAD(b_start) OVER (ORDER BY b_start) AS gap_end FROM merged
)
SELECT gap_start, gap_end,
       CAST((unixepoch(gap_end) - unixepoch(gap_start)) / 60 AS INTEGER) AS minutes
FROM nxt
WHERE gap_end > gap_start

)
SELECT CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) AS window_minutes,
       COALESCE(SUM(minutes), 0) AS uncovered_minutes,
       CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) - COALESCE(SUM(minutes), 0) AS covered_minutes,
       ROUND(100.0 * (CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) - COALESCE(SUM(minutes), 0))
             / (CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER)), 1) AS coverage_pct
FROM g
```

**pandas answer:** same logic, identical to the Code block:
```py
def coverage(shifts, ws, we):
    ws, we = pd.Timestamp(ws), pd.Timestamp(we)
    x = shifts.dropna().copy()
    x["st"] = pd.to_datetime(x["start_ts"]).clip(lower=ws)
    x["en"] = pd.to_datetime(x["end_ts"]).clip(upper=we)
    x = x[x["st"] < x["en"]][["st", "en"]]
    x = pd.concat([x, pd.DataFrame({"st": [ws, we], "en": [ws, we]})]).sort_values(["st", "en"]).reset_index(drop=True)
    prev_max = x["en"].cummax().shift()
    x["blk"] = ((prev_max.isna()) | (x["st"] > prev_max)).cumsum()
    m = x.groupby("blk").agg(b_start=("st", "min"), b_end=("en", "max"))
    gaps = pd.DataFrame({"gap_start": m["b_end"], "gap_end": m["b_start"].shift(-1)}).dropna()
    gaps = gaps[gaps["gap_end"] > gaps["gap_start"]].reset_index(drop=True)
    gaps["minutes"] = ((gaps["gap_end"] - gaps["gap_start"]).dt.total_seconds() / 60).astype(int)
    total = int((we - ws).total_seconds() / 60)
    unc = int(gaps["minutes"].sum())
    return gaps, (total, unc, total - unc, round(100.0 * (total - unc) / total, 1))
```

**Example:** after clipping (g7 vanishes, g8 is dropped for the NULL end) the intervals are g1 09:00-11:00, g2 10:00-12:00, g3 11:30-11:45, g4 12:00-13:00, g5 14:00-15:00 (twice), g6 16:00-18:00, plus the sentinels 09:00-09:00 and 18:00-18:00.
- Sorted by start, end: sentinel 09:00, g1 09:00-11:00, g2 10:00-12:00, g3 11:30-11:45, g4 12:00-13:00, g5 14:00, g5 14:00, g6 16:00-18:00, sentinel 18:00.
- Running max of the ends of all earlier rows, row by row: NULL (sentinel), 09:00 (for g1), 11:00 (g2), 12:00 (g3), 12:00 (g4; g3 ended at 11:45, so the contained interval did not lower or raise it), 13:00 (first g5), 15:00 (duplicate g5), 15:00 (g6), 18:00 (closing sentinel).
- New block where start > running max (or NULL): sentinel (first), g1 no (09:00 > 09:00 false), g2 no, g3 no, g4 no (12:00 > 12:00 false, touching merges), g5 yes (14:00 > 13:00), duplicate g5 no, g6 yes (16:00 > 15:00), final sentinel no (18:00 > 18:00 false).
- Merged blocks: 09:00-13:00, 14:00-15:00, 16:00-18:00. Gaps: 13:00-14:00 and 15:00-16:00, 60 minutes each. Uncovered 120, covered 420 of 540 = 77.8 per cent.

**Code:** run with `python3 -I`. The asserts compare the gaps frame (after sorting by `gap_start`) and the summary tuple with SQL; the edge cases run in SQL only except the no-shift case, which also runs in pandas.
```python
# Q37: coverage and uncovered gaps in a 09:00-18:00 window, SQL + pandas
import sqlite3
import pandas as pd

WSTART, WEND = "2024-03-04 09:00", "2024-03-04 18:00"
SCHEMA = """
CREATE TABLE shifts(guard_id TEXT, start_ts TEXT, end_ts TEXT);
INSERT INTO shifts VALUES
 ('g2','2024-03-04 10:00','2024-03-04 12:00'),
 ('g1','2024-03-04 08:00','2024-03-04 11:00'),
 ('g4','2024-03-04 12:00','2024-03-04 13:00'),
 ('g3','2024-03-04 11:30','2024-03-04 11:45'),
 ('g5','2024-03-04 14:00','2024-03-04 15:00'),
 ('g5','2024-03-04 14:00','2024-03-04 15:00'),
 ('g6','2024-03-04 16:00','2024-03-04 19:00'),
 ('g7','2024-03-04 06:00','2024-03-04 08:30'),
 ('g8','2024-03-04 17:00',NULL);
"""
SQL_MAIN = """
WITH w AS (SELECT :ws AS ws, :we AS we),
clipped AS (
  SELECT MAX(s.start_ts, w.ws) AS st, MIN(s.end_ts, w.we) AS en
  FROM shifts s, w
  WHERE s.start_ts IS NOT NULL AND s.end_ts IS NOT NULL
),
pieces AS (
  SELECT st, en FROM clipped WHERE st < en
  UNION ALL SELECT ws, ws FROM w
  UNION ALL SELECT we, we FROM w
),
ordered AS (
  SELECT st, en,
         MAX(en) OVER (ORDER BY st, en ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM pieces
),
flagged AS (
  SELECT st, en,
         SUM(CASE WHEN prev_max IS NULL OR st > prev_max THEN 1 ELSE 0 END)
             OVER (ORDER BY st, en) AS blk
  FROM ordered
),
merged AS (
  SELECT MIN(st) AS b_start, MAX(en) AS b_end FROM flagged GROUP BY blk
),
nxt AS (
  SELECT b_end AS gap_start, LEAD(b_start) OVER (ORDER BY b_start) AS gap_end FROM merged
)
SELECT gap_start, gap_end,
       CAST((unixepoch(gap_end) - unixepoch(gap_start)) / 60 AS INTEGER) AS minutes
FROM nxt
WHERE gap_end > gap_start
ORDER BY gap_start
"""
SQL_SUMMARY = """
WITH g AS (""" + SQL_MAIN.replace("ORDER BY gap_start\n", "\n") + """)
SELECT CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) AS window_minutes,
       COALESCE(SUM(minutes), 0) AS uncovered_minutes,
       CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) - COALESCE(SUM(minutes), 0) AS covered_minutes,
       ROUND(100.0 * (CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) - COALESCE(SUM(minutes), 0))
             / (CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER)), 1) AS coverage_pct
FROM g
"""
params = {"ws": WSTART, "we": WEND}
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_gaps = pd.read_sql_query(SQL_MAIN, con, params=params)
sql_sum = pd.read_sql_query(SQL_SUMMARY, con, params=params)
print("SQL gaps:"); print(sql_gaps.to_string(index=False))
print("SQL summary:"); print(sql_sum.to_string(index=False))

shifts = pd.read_sql_query("SELECT * FROM shifts", con)
# pd:main
def coverage(shifts, ws, we):
    ws, we = pd.Timestamp(ws), pd.Timestamp(we)
    x = shifts.dropna().copy()
    x["st"] = pd.to_datetime(x["start_ts"]).clip(lower=ws)
    x["en"] = pd.to_datetime(x["end_ts"]).clip(upper=we)
    x = x[x["st"] < x["en"]][["st", "en"]]
    x = pd.concat([x, pd.DataFrame({"st": [ws, we], "en": [ws, we]})]).sort_values(["st", "en"]).reset_index(drop=True)
    prev_max = x["en"].cummax().shift()
    x["blk"] = ((prev_max.isna()) | (x["st"] > prev_max)).cumsum()
    m = x.groupby("blk").agg(b_start=("st", "min"), b_end=("en", "max"))
    gaps = pd.DataFrame({"gap_start": m["b_end"], "gap_end": m["b_start"].shift(-1)}).dropna()
    gaps = gaps[gaps["gap_end"] > gaps["gap_start"]].reset_index(drop=True)
    gaps["minutes"] = ((gaps["gap_end"] - gaps["gap_start"]).dt.total_seconds() / 60).astype(int)
    total = int((we - ws).total_seconds() / 60)
    unc = int(gaps["minutes"].sum())
    return gaps, (total, unc, total - unc, round(100.0 * (total - unc) / total, 1))
# pd:end
pd_gaps, pd_sum = coverage(shifts, WSTART, WEND)
out = pd_gaps.assign(gap_start=pd_gaps["gap_start"].dt.strftime("%Y-%m-%d %H:%M"),
                     gap_end=pd_gaps["gap_end"].dt.strftime("%Y-%m-%d %H:%M"))
print("pandas gaps:"); print(out.to_string(index=False))
print("pandas summary:", pd_sum)
# compare after sorting by gap_start
assert out.astype({"minutes": "int64"}).equals(sql_gaps.astype({"minutes": "int64"}))
assert pd_sum == tuple(sql_sum.iloc[0].tolist())

print("--- edge cases ---")
con.execute("DELETE FROM shifts")
print("no shifts, SQL:", pd.read_sql_query(SQL_MAIN, con, params=params).values.tolist(),
      pd.read_sql_query(SQL_SUMMARY, con, params=params).values.tolist())
print("no shifts, pandas:", coverage(shifts.iloc[0:0], WSTART, WEND)[1])
con.execute("INSERT INTO shifts VALUES ('x','2024-03-04 06:00','2024-03-04 08:30'),('y','2024-03-04 18:00','2024-03-04 20:00')")
print("only shifts outside the window, SQL:", pd.read_sql_query(SQL_MAIN, con, params=params).values.tolist())
con.execute("DELETE FROM shifts")
con.execute("INSERT INTO shifts VALUES ('z','2024-03-04 08:00','2024-03-04 19:00')")
print("one shift covering everything, SQL gaps:", pd.read_sql_query(SQL_MAIN, con, params=params).values.tolist(),
      pd.read_sql_query(SQL_SUMMARY, con, params=params).values.tolist())
print("asserts passed")
```

**Output (my run):**
```text
SQL gaps:
       gap_start          gap_end  minutes
2024-03-04 13:00 2024-03-04 14:00       60
2024-03-04 15:00 2024-03-04 16:00       60
SQL summary:
 window_minutes  uncovered_minutes  covered_minutes  coverage_pct
            540                120              420          77.8
pandas gaps:
       gap_start          gap_end  minutes
2024-03-04 13:00 2024-03-04 14:00       60
2024-03-04 15:00 2024-03-04 16:00       60
pandas summary: (540, 120, 420, 77.8)
--- edge cases ---
no shifts, SQL: [['2024-03-04 09:00', '2024-03-04 18:00', 540]] [[540.0, 540.0, 0.0, 0.0]]
no shifts, pandas: (540, 540, 0, 0.0)
only shifts outside the window, SQL: [['2024-03-04 09:00', '2024-03-04 18:00', 540]]
one shift covering everything, SQL gaps: [] [[540.0, 0.0, 540.0, 100.0]]
asserts passed
```

**Edge cases:**
- No shifts at all: the sentinels alone form two blocks 09:00-09:00 and 18:00-18:00, so one gap equal to the whole window, 540 minutes, 0 per cent covered (SQL and pandas both returned it). Without the sentinels the query would return nothing for an empty day, which is wrong for a coverage report.
- Shifts only outside the window (06:00-08:30 and 18:00-20:00): after clipping the start is not before the end, so they are dropped and the whole window is one gap.
- One shift covering everything: no gaps, 100 per cent.
- Touching shifts (g2 ends 12:00, g4 starts 12:00): merged because the test is strict `>`. If a hand-over takes a minute of cover you can lose, use `>=` and the touching pair stays two blocks with a zero-minute gap; zero-length gaps are filtered by `gap_end > gap_start` anyway.
- Contained shift (g3): does not shrink the block because the running max keeps 12:00.
- Duplicates (g5 twice): harmless for merging (the duplicate's start is not greater than the max); they do not double the covered minutes because coverage is computed from gaps, not from summing shift lengths.
- NULL end (g8) or NULL start: excluded and stated; if NULL means "still on shift", substitute the window end (`COALESCE(end_ts, :we)`) instead of dropping it, which changes the answer for g8 (17:00 to 18:00 would count as covered).
- The first row's running max is NULL (empty frame), which is why the flag tests `prev_max IS NULL OR st > prev_max`; the frame `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING` with `MAX` ran on SQLite 3.45.1 here.
- Timestamps are ISO text in one day so string comparison orders correctly; multi-day windows need the day in the window parameters (they have it here) and a partition per day.

**Then explain:**
- Gaps are the complement of the merged union, so the work is: clip, merge, then look between neighbours. The sentinels turn the two open ends of the window into ordinary neighbours so no special case is needed.
- Minutes come from `unixepoch` integer seconds divided by 60: exact for whole minutes, and no floating-point rounding (see the julianday test in Q40).
- Coverage percentage is covered over window length; state the denominator (the window, not the shifts).
- Dialects (not executed here): PostgreSQL would compute minutes with `EXTRACT(EPOCH FROM (b - a)) / 60` and could use range types (`tsrange`) with a union aggregate; MySQL uses `TIMESTAMPDIFF(MINUTE, a, b)`; the clipping uses `GREATEST` and `LEAST` there.

**Follow-ups:**
- Gaps per guard-location or per day? Add the partition key to every window and the day to the join.
- Minimum number of guards at any time (not just one)? That is the +1/-1 sweep of Q17 with a threshold.
- Pages of data too large for a self-contained sort? The same logic scales with an index on `start_ts`.

**Common mistakes:**
- Summing the shift lengths for coverage (double counts overlaps and out-of-window time).
- Merging by comparing with the previous row's end instead of the running max (a contained shift shrinks the block and creates a false gap).
- Forgetting to clip, so a gap before 09:00 appears or the coverage exceeds 100 per cent.
- No sentinels, so the empty day returns no rows.
- Using scalar `MIN`/`MAX` on a NULL end (the result is NULL).

### Q38 ⭐ 🔴 SQL versus pandas differences on islands, a translation table with each row demonstrated: duplicates breaking the ROW_NUMBER trick unless deduplicated, NULL != comparisons returning NULL versus NaN != NaN returning True, NaT and NaN produced by shift (integer columns turned into float unless fill_value is set), tie-breaking when timestamps are identical and sort_values stability (use kind='stable' or sort on two keys), and groupby dropping NaN keys. Give a tiny reproduction for each and say which were run.
**Asked at:** pandas Series.shift reference (opened) and search snippets of Stack Overflow and Towards Data Science run-grouping answers ((s != s.shift()).cumsum(), diff().ne(0).cumsum(); not opened); documentation and guides, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** The same island logic behaves differently in SQL and pandas in five places, and I ran a tiny reproduction of each: duplicates break the row-number key in both, NULL comparisons are NULL in SQL but `NaN != NaN` is True in pandas, `shift` turns integers into floats, tied sort keys have no guaranteed order unless you add a second key or `kind='stable'`, and `groupby` drops NaN keys where `GROUP BY` keeps NULL.

**Schema and sample data:** five small tables created inside the Code block, one per row of the table below (a `logins` table with a duplicate day, a four-row `st` state table with NULLs, a `tie` table, a `g` table with NULL keys, and in-memory pandas Series for the rest). The data is shown with each demonstration.
```sql
CREATE TABLE logins(user_id TEXT, login_date TEXT);
INSERT INTO logins VALUES ('u','2024-03-01'),('u','2024-03-02'),('u','2024-03-02'),('u','2024-03-03');
CREATE TABLE st(ts INTEGER, state TEXT);
INSERT INTO st VALUES (1,'up'),(2,NULL),(3,NULL),(4,'up');
CREATE TABLE tie(ts INTEGER, ev INTEGER);
INSERT INTO tie VALUES (1,2),(1,1),(1,3);
CREATE TABLE g(k TEXT, v INTEGER);
INSERT INTO g VALUES ('a',1),(NULL,2),('a',3),(NULL,4);
```

**SQL answer:** the SQL for each row is in the Code block; the island query used in row 1 is `SQL_ISLANDS` (with `{src}` replaced by `logins` or by `(SELECT DISTINCT login_date FROM logins)`):
```sql
WITH r AS (
  SELECT login_date, julianday(login_date) - ROW_NUMBER() OVER (ORDER BY login_date) AS k FROM {src}
)
SELECT MIN(login_date) AS s, MAX(login_date) AS e, COUNT(*) AS n FROM r GROUP BY k ORDER BY s
```
The translation table (every row was run; the output is below):

| Topic | SQL (SQLite 3.45.1) | pandas 3.0.5 | What I saw |
|---|---|---|---|
| Duplicate dates | `date - ROW_NUMBER()` splits the run (two islands of 2 days instead of one of 3); `DISTINCT` first | same with `cumcount` as the row number; `drop_duplicates()` first | both split into two islands raw, one island of 3 days after dedup |
| NULL / NaN in a `!=` run flag | `NULL != 1` and `NULL != NULL` are NULL; `IS NOT` is NULL-safe (`NULL IS NOT NULL` is 0); `IS DISTINCT FROM` also works on 3.45.1 | `np.nan != np.nan` is True; `x != x.shift()` is True on every NaN row; nullable `Int64` with `pd.NA` gives `<NA>` | with `<>` the transition into NULL was lost and a spurious start appeared; `IS NOT` gave 1, 2, 4 |
| Shift / LAG | `LAG` gives NULL for the first row; SQLite does not change column types | `shift()` makes integers float64 (NaN), datetimes get `NaT`; `fill_value=0` keeps int64; `diff().dt.days` gives floats | float64 versus int64 shown |
| Ties in the ordering column | `ORDER BY ts` with ties has no specified order; add `, ev` | `sort_values` default kind is `quicksort`, not stable; `kind='stable'` or a second key makes the order deterministic | on 2,000 rows with 5 distinct keys the default order differed from the stable order; a second key matched |
| NULL / NaN group keys | `GROUP BY k` keeps one NULL group (sum 6) | `groupby('k')` drops NaN keys (only `a` remains); `dropna=False` keeps them | shown |

**pandas answer:** the pandas side of each row is in the Code block; there is no single pandas query. The reusable pieces are the island key `day_number - cumcount()`, the NaN-safe run flag `(x != x.shift())` replaced by `(x != x.shift()) & ~(x.isna() & x.shift().isna())` when NaN should equal NaN, `shift(fill_value=...)`, `sort_values(..., kind="stable")` or a second key, and `groupby(..., dropna=False)`.

**Example:** walk the five rows with the tiny data.
- Duplicates: `u` has 1, 2, 2, 3 March. Row numbers 1, 2, 3, 4, day numbers D, D+1, D+1, D+2, so the keys are D-1, D-1, D-2, D-2: two islands of 2 rows (1-2 March and 2-3 March). After `DISTINCT` the rows are 1, 2, 3 March with keys D-1 for all: one island of 3 days.
- NULL: `st` has up, NULL, NULL, up. With `LAG(state)`: previous values are NULL, up, NULL, NULL. Test "first row or `state <> previous`": ts 1 (previous NULL, first) yes; ts 2 (`NULL <> 'up'` is NULL) no; ts 3 (previous NULL) yes (it is accepted as a first row by mistake); ts 4 (previous NULL) yes. Result 1, 3, 4. The NULL-safe `state IS NOT previous`: ts 1 (`'up' IS NOT NULL` true), ts 2 (`NULL IS NOT 'up'` true), ts 3 (`NULL IS NOT NULL` false), ts 4 (`'up' IS NOT NULL` true). Result 1, 2, 4, which are the true run starts.
- Shift: `[1, 2, 3].shift()` is `[NaN, 1.0, 2.0]` (float64); with `fill_value=0` it is `[0, 1, 2]` (int64).
- Ties: three rows with the same ts have no promised order in SQL, so add `ev` to the `ORDER BY`; in pandas a small input came back in original order (`a, b, c`) (I did not investigate why; short inputs may take a different code path inside NumPy), but 2,000 rows with five distinct keys did not match the stable order. The default `kind` in the signature is `quicksort`.
- Groups: `g` has keys a, NULL, a, NULL. SQL gives groups NULL (6) and a (4); pandas default gives only a (4).

**Code:** run with `python3 -I`. Most claims in the table are asserted; the 2,000-row sort-order result (which depends on the NumPy build), the nullable-`Int64` output and the `.dt.days` values are only printed.
```python
# Q38: SQL versus pandas differences on islands: five tiny reproductions, all run
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")

# ---- Row 1: duplicates break the ROW_NUMBER trick (SQL and pandas), fixed by dedup ----
con.executescript("""
CREATE TABLE logins(user_id TEXT, login_date TEXT);
INSERT INTO logins VALUES ('u','2024-03-01'),('u','2024-03-02'),('u','2024-03-02'),('u','2024-03-03');
""")
SQL_ISLANDS = """
WITH r AS (
  SELECT login_date, julianday(login_date) - ROW_NUMBER() OVER (ORDER BY login_date) AS k FROM {src}
)
SELECT MIN(login_date) AS s, MAX(login_date) AS e, COUNT(*) AS n FROM r GROUP BY k ORDER BY s
"""
raw = con.execute(SQL_ISLANDS.format(src="logins")).fetchall()
fixed = con.execute(SQL_ISLANDS.format(src="(SELECT DISTINCT login_date FROM logins)")).fetchall()
print("1 SQL raw  :", raw)
print("1 SQL dedup:", fixed)
lg = pd.read_sql_query("SELECT * FROM logins", con)
def pd_islands(df):
    d = pd.to_datetime(df["login_date"]).sort_values()
    k = (d - pd.Timestamp("1970-01-01")).dt.days - np.arange(len(d))
    return d.groupby(k.to_numpy()).agg(["min", "max", "size"]).sort_values("min").astype(str).values.tolist()
p_raw = pd_islands(lg); p_fix = pd_islands(lg.drop_duplicates())
print("1 pandas raw  :", p_raw)
print("1 pandas dedup:", p_fix)
assert len(raw) == 2 and len(fixed) == 1 and len(p_raw) == 2 and len(p_fix) == 1

# ---- Row 2: NULL != 1 is NULL in SQL; NaN != 1 and NaN != NaN are True in pandas ----
sql_row = con.execute("SELECT NULL != 1, NULL != NULL, NULL IS NOT 1, NULL IS NOT NULL, NULL IS DISTINCT FROM 1").fetchone()
print("2 SQL (NULL != 1, NULL != NULL, NULL IS NOT 1, NULL IS NOT NULL, IS DISTINCT FROM):", sql_row)
x = pd.Series([1.0, np.nan, np.nan, 2.0])
print("2 pandas x != x.shift():", (x != x.shift()).tolist())
print("2 pandas NaN != NaN:", np.nan != np.nan, "| nullable Int64 with <NA>:", (pd.Series([1, pd.NA], dtype="Int64") != 1).tolist())
assert sql_row == (None, None, 1, 0, 1)
assert (x != x.shift()).tolist() == [True, True, True, True]
# the SQL LAG flag with a plain <> drops the row after a NULL; IS NOT keeps it
con.executescript("""
CREATE TABLE st(ts INTEGER, state TEXT);
INSERT INTO st VALUES (1,'up'),(2,NULL),(3,NULL),(4,'up');
""")
q_ne = con.execute("SELECT ts FROM (SELECT ts, state, LAG(state) OVER (ORDER BY ts) AS p FROM st) WHERE p IS NULL OR state <> p").fetchall()
q_isnot = con.execute("SELECT ts FROM (SELECT ts, state, LAG(state) OVER (ORDER BY ts) AS p FROM st) WHERE state IS NOT p").fetchall()
print("2 SQL run starts, first-row test plus <> (loses ts 2, wrongly keeps ts 3):", q_ne, "| with IS NOT:", q_isnot)
assert q_ne == [(1,), (3,), (4,)] and q_isnot == [(1,), (2,), (4,)]

# ---- Row 3: shift upcasts int to float; NaT for datetimes; fill_value keeps int ----
i = pd.Series([1, 2, 3])
print("3 int shift dtype:", i.shift().dtype, "| fill_value=0:", i.shift(fill_value=0).dtype)
dts = pd.Series(pd.to_datetime(["2024-03-01", "2024-03-02"]))
print("3 datetime shift:", dts.shift().tolist())
print("3 diff on dates, dtype:", dts.diff().dtype, "| .dt.days:", dts.diff().dt.days.tolist())
print("3 SQL LAG on integers (SQLite types are dynamic, no upcast):",
      con.execute("SELECT LAG(v) OVER (ORDER BY v) FROM (SELECT 1 AS v UNION ALL SELECT 2)").fetchall())
assert i.shift().dtype == "float64" and i.shift(fill_value=0).dtype == "int64"
assert str(dts.shift().iloc[0]) == "NaT"

# ---- Row 4: ties in the ordering column ----
rng = np.random.default_rng(1)
n = 2000
t = pd.DataFrame({"ts": rng.integers(0, 5, n), "ev": np.arange(n)})        # ev records original position
default = t.sort_values("ts")
stable = t.sort_values("ts", kind="stable")
two_key = t.sort_values(["ts", "ev"])
print("4 sort_values default kind equals stable order:", default["ev"].tolist() == stable["ev"].tolist())
print("4 sort on two keys equals stable order:", two_key["ev"].tolist() == stable["ev"].tolist())
assert default["ts"].is_monotonic_increasing   # sorted by ts either way; only the tie order differs
small = pd.DataFrame({"ts": [1, 1, 1], "ev": ["a", "b", "c"]})
print("4 three tied rows, default kind:", small.sort_values("ts")["ev"].tolist())
# the pandas default kind, read from the signature
import inspect
print("4 default kind in signature:", inspect.signature(pd.DataFrame.sort_values).parameters["kind"].default)
con.executescript("CREATE TABLE tie(ts INTEGER, ev INTEGER); INSERT INTO tie VALUES (1,2),(1,1),(1,3);")
print("4 SQL ORDER BY ts only (tie order is not specified):", con.execute("SELECT ev FROM tie ORDER BY ts").fetchall(),
      "| ORDER BY ts, ev:", con.execute("SELECT ev FROM tie ORDER BY ts, ev").fetchall())

# ---- Row 5: groupby drops NaN keys; GROUP BY keeps NULL ----
g = pd.DataFrame({"k": ["a", None, "a", None], "v": [1, 2, 3, 4]})
print("5 pandas groupby default:", g.groupby("k")["v"].sum().to_dict())
print("5 pandas dropna=False   :", g.groupby("k", dropna=False)["v"].sum().to_dict())
con.executescript("CREATE TABLE g(k TEXT, v INTEGER); INSERT INTO g VALUES ('a',1),(NULL,2),('a',3),(NULL,4);")
print("5 SQL GROUP BY k:", con.execute("SELECT k, SUM(v) FROM g GROUP BY k ORDER BY k").fetchall())
assert g.groupby("k")["v"].sum().to_dict() == {"a": 4}
assert con.execute("SELECT COUNT(*) FROM (SELECT k FROM g GROUP BY k)").fetchone()[0] == 2
print("asserts passed")
```

**Output (my run):**
```text
1 SQL raw  : [('2024-03-01', '2024-03-02', 2), ('2024-03-02', '2024-03-03', 2)]
1 SQL dedup: [('2024-03-01', '2024-03-03', 3)]
1 pandas raw  : [['2024-03-01', '2024-03-02', '2'], ['2024-03-02', '2024-03-03', '2']]
1 pandas dedup: [['2024-03-01', '2024-03-03', '3']]
2 SQL (NULL != 1, NULL != NULL, NULL IS NOT 1, NULL IS NOT NULL, IS DISTINCT FROM): (None, None, 1, 0, 1)
2 pandas x != x.shift(): [True, True, True, True]
2 pandas NaN != NaN: True | nullable Int64 with <NA>: [False, <NA>]
2 SQL run starts, first-row test plus <> (loses ts 2, wrongly keeps ts 3): [(1,), (3,), (4,)] | with IS NOT: [(1,), (2,), (4,)]
3 int shift dtype: float64 | fill_value=0: int64
3 datetime shift: [NaT, Timestamp('2024-03-01 00:00:00')]
3 diff on dates, dtype: timedelta64[us] | .dt.days: [nan, 1.0]
3 SQL LAG on integers (SQLite types are dynamic, no upcast): [(None,), (1,)]
4 sort_values default kind equals stable order: False
4 sort on two keys equals stable order: True
4 three tied rows, default kind: ['a', 'b', 'c']
4 default kind in signature: quicksort
4 SQL ORDER BY ts only (tie order is not specified): [(2,), (1,), (3,)] | ORDER BY ts, ev: [(1,), (2,), (3,)]
5 pandas groupby default: {'a': 4}
5 pandas dropna=False   : {'a': 4, nan: 6}
5 SQL GROUP BY k: [(None, 6), ('a', 4)]
asserts passed
```

**Edge cases:**
- Tie order: the unstable default is observed behaviour on this machine's pandas 3.0.5 and NumPy build for 2,000 rows; it is not a documented promise either way for other sizes or builds, so the safe habit is an explicit stable sort or a unique second key.
- `diff()` on datetimes gives a `Timedelta` with NaT on the first row; `.dt.days` of NaT is NaN, so a comparison `== 1` is False for the first row, which is the desired "first row starts a streak".
- A nullable `Int64` column avoids the float upcast but then `pd.NA` makes comparisons `<NA>`, and I printed that `<NA>` result only; I did not test it as a boolean mask.
- Group order: SQL `ORDER BY k` put the NULL group first in SQLite in my run; with `dropna=False` the NaN key sits in its own group in the dictionary printed above.
- Not executed here, from memory: PostgreSQL puts NULLs last in an ascending `ORDER BY` where SQLite puts them first; `IS DISTINCT FROM` is the SQL-standard NULL-safe test, while `IS NOT` between two values is SQLite syntax and MySQL spells it `<=>`.

**Then explain:**
- SQL is three-valued: NULL comparisons give NULL and a `WHERE` or `CASE WHEN` treats NULL as false. pandas follows IEEE floating point: NaN compared with anything, including itself, is unequal, so `!=` is True. The same flag expression therefore gives different run starts on the same data.
- Neither engine promises an order for ties unless told; pandas happens to be stable on tiny inputs, which hides the bug in tests.
- The type upcast is the quiet one: integer IDs or days that go through `shift` become floats, so a join or an equality against an integer column can fail later; use `fill_value`, `Int64` or cast back.
- The fix list: dedupe before the key, NULL-safe comparisons (`IS NOT` or explicit `isna` tests), `fill_value`, a tie-breaker column, `dropna=False`.

**Follow-ups:**
- Which row is most dangerous in production? Duplicates and ties, because the code runs without errors and the numbers are just wrong.
- Other differences worth checking? How each engine treats NULL or NaN inside aggregates; test it with a fixture rather than assume.
- How would you test it? Put a duplicate, a NULL, a tie and a single-row group into the fixture, as this answer does.

**Common mistakes:**
- Assuming `NaN != NaN` is False, or `NULL != NULL` is true.
- Trusting the order of tied rows because it looked right in a small test.
- Letting `shift` change a column to float and then merging on it.
- Forgetting `dropna=False` and silently losing rows with missing keys.
- Skipping `DISTINCT` and checking only one clean user.

### Q39 ⭐ 🔴 Time zone and midnight boundaries in streaks: logins(user_id, login_ts_utc) stored as UTC ISO text. Compute daily-login streaks per user by the IST calendar day (UTC+5:30, applied with datetime(login_ts_utc, '+330 minutes')) versus the UTC day, and show a login at 20:00 UTC on 5 March that becomes 6 March in IST and merges or splits a streak. Explain the daylight saving problem for zones with DST (hedge as not executed in SQLite), and the 'one day' definition to agree with the product team.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** A streak needs a definition of "day", so first convert each UTC timestamp to the calendar day you agreed on (IST is UTC plus 330 minutes, applied with `date(login_ts_utc, '+330 minutes')`), deduplicate to one row per user per day, and only then use the day-number minus ROW_NUMBER key; the same data can merge or split streaks depending on that choice.

**Schema and sample data:** timestamps are UTC ISO text (`YYYY-MM-DD HH:MM:SS`). U1 has a login at 20:00 UTC on 5 March, which is 01:30 on 6 March in IST. U2 straddles the IST midnight exactly (18:29:59 and 18:30:00 UTC). U3 has two logins on one UTC day that fall on different IST days. U4 has a single login. U5 has a NULL and a malformed timestamp. Rows are unsorted.
```sql
CREATE TABLE logins(user_id TEXT, login_ts_utc TEXT);
INSERT INTO logins VALUES
 ('U1','2024-03-07 10:00:00'),('U1','2024-03-03 10:00:00'),('U1','2024-03-05 20:00:00'),('U1','2024-03-04 10:00:00'),
 ('U2','2024-03-04 18:29:59'),('U2','2024-03-05 18:30:00'),
 ('U3','2024-03-04 10:00:00'),('U3','2024-03-04 19:00:00'),('U3','2024-03-06 10:00:00'),('U3','2024-03-06 10:00:00'),
 ('U4','2024-03-09 12:00:00'),
 ('U5','2024-03-04 10:00:00'),('U5',NULL),('U5','not a timestamp');
```

**SQL answer:** one query, `SQL_MAIN` in the Code block, run twice with a bound parameter `:shift` of `'+330 minutes'` (IST) and `'+0 minutes'` (UTC). It converts, drops rows where `date()` returns NULL (a NULL or unparseable timestamp), deduplicates days, and uses `unixepoch(day) / 86400` (an integer day number) minus `ROW_NUMBER()` as the key:
```sql
WITH d AS (
  SELECT DISTINCT user_id, date(login_ts_utc, :shift) AS day
  FROM logins
  WHERE date(login_ts_utc, :shift) IS NOT NULL
),
r AS (
  SELECT user_id, day,
         unixepoch(day) / 86400 - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS k
  FROM d
)
SELECT user_id, MIN(day) AS streak_start, MAX(day) AS streak_end, COUNT(*) AS days
FROM r
GROUP BY user_id, k
ORDER BY user_id, streak_start
```

**pandas answer:** same logic, identical to the Code block (`errors="coerce"` turns a bad timestamp into NaT, which `dropna` removes, matching the SQL `IS NOT NULL` filter):
```py
def streaks(df, shift_minutes):
    t = pd.to_datetime(df["login_ts_utc"], errors="coerce", format="%Y-%m-%d %H:%M:%S")
    x = pd.DataFrame({"user_id": df["user_id"], "day": (t + pd.Timedelta(minutes=shift_minutes)).dt.normalize()})
    x = x.dropna().drop_duplicates().sort_values(["user_id", "day"])
    x["k"] = (x["day"] - pd.Timestamp("1970-01-01")).dt.days - x.groupby("user_id").cumcount()
    out = (x.groupby(["user_id", "k"])
            .agg(streak_start=("day", "min"), streak_end=("day", "max"), days=("day", "size"))
            .reset_index().drop(columns="k").sort_values(["user_id", "streak_start"]).reset_index(drop=True))
    out["streak_start"] = out["streak_start"].dt.strftime("%Y-%m-%d")
    out["streak_end"] = out["streak_end"].dt.strftime("%Y-%m-%d")
    return out
```

**Example:**
- U1: UTC logins on 3, 4, 5 and 7 March (the 5 March one at 20:00). UTC days 3, 4, 5, 7 give streaks 3-5 (3 days) and 7 (1 day). In IST the 20:00 UTC login is 01:30 on 6 March, so the IST days are 3, 4, 6, 7: streaks 3-4 and 6-7 (2 days each). Same four logins, one 3-day streak became two 2-day streaks: the 5 March login moved to 6 March, leaving 5 March empty and gluing it to 7 March instead.
- U2: 18:29:59 UTC on 4 March is 23:59:59 IST on 4 March; 18:30:00 UTC on 5 March is 00:00:00 IST on 6 March. UTC days 4 and 5: one 2-day streak. IST days 4 and 6: two streaks of 1 day. One second of difference at the boundary decides it.
- U3: logins 10:00 and 19:00 UTC on 4 March and 10:00 on 6 March (twice). UTC days 4 and 6: two streaks. 19:00 UTC is 00:30 IST on 5 March, so IST days are 4, 5, 6: one 3-day streak. Here IST merges what UTC splits.
- U5: the NULL and the malformed text give `date()` NULL and are dropped; one valid login remains.

**Code:** run with `python3 -I`. The asserts compare the pandas frames with the SQL frames for both IST and UTC after sorting by `user_id, streak_start`. The DST part is pandas only.
```python
# Q39: daily-login streaks by IST day versus UTC day, SQL + pandas (+ a pandas-only DST demo)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id TEXT, login_ts_utc TEXT);
INSERT INTO logins VALUES
 ('U1','2024-03-07 10:00:00'),('U1','2024-03-03 10:00:00'),('U1','2024-03-05 20:00:00'),('U1','2024-03-04 10:00:00'),
 ('U2','2024-03-04 18:29:59'),('U2','2024-03-05 18:30:00'),
 ('U3','2024-03-04 10:00:00'),('U3','2024-03-04 19:00:00'),('U3','2024-03-06 10:00:00'),('U3','2024-03-06 10:00:00'),
 ('U4','2024-03-09 12:00:00'),
 ('U5','2024-03-04 10:00:00'),('U5',NULL),('U5','not a timestamp');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, date(login_ts_utc, :shift) AS day
  FROM logins
  WHERE date(login_ts_utc, :shift) IS NOT NULL
),
r AS (
  SELECT user_id, day,
         unixepoch(day) / 86400 - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS k
  FROM d
)
SELECT user_id, MIN(day) AS streak_start, MAX(day) AS streak_end, COUNT(*) AS days
FROM r
GROUP BY user_id, k
ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ist = pd.read_sql_query(SQL_MAIN, con, params={"shift": "+330 minutes"})
utc = pd.read_sql_query(SQL_MAIN, con, params={"shift": "+0 minutes"})
print("SQL, IST day:"); print(ist.to_string(index=False))
print("SQL, UTC day:"); print(utc.to_string(index=False))
print("check 20:00 UTC on 5 March:", con.execute("SELECT datetime('2024-03-05 20:00:00', '+330 minutes'), date('2024-03-05 20:00:00', '+330 minutes')").fetchone())
print("T and Z form accepted:", con.execute("SELECT datetime('2024-03-05T20:00:00Z', '+330 minutes')").fetchone())

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
def streaks(df, shift_minutes):
    t = pd.to_datetime(df["login_ts_utc"], errors="coerce", format="%Y-%m-%d %H:%M:%S")
    x = pd.DataFrame({"user_id": df["user_id"], "day": (t + pd.Timedelta(minutes=shift_minutes)).dt.normalize()})
    x = x.dropna().drop_duplicates().sort_values(["user_id", "day"])
    x["k"] = (x["day"] - pd.Timestamp("1970-01-01")).dt.days - x.groupby("user_id").cumcount()
    out = (x.groupby(["user_id", "k"])
            .agg(streak_start=("day", "min"), streak_end=("day", "max"), days=("day", "size"))
            .reset_index().drop(columns="k").sort_values(["user_id", "streak_start"]).reset_index(drop=True))
    out["streak_start"] = out["streak_start"].dt.strftime("%Y-%m-%d")
    out["streak_end"] = out["streak_end"].dt.strftime("%Y-%m-%d")
    return out
# pd:end
p_ist, p_utc = streaks(logins, 330), streaks(logins, 0)
print("pandas IST:"); print(p_ist.to_string(index=False))
# compare after sorting by user_id, streak_start
assert p_ist.astype({"days": "int64"}).equals(ist.astype({"days": "int64"}))
assert p_utc.astype({"days": "int64"}).equals(utc.astype({"days": "int64"}))

# DST: pandas only (SQLite has no zones; not executed in SQLite). A fixed UTC-5 offset versus America/New_York.
try:
    t = pd.Timestamp("2024-03-11 04:30:00", tz="UTC")
    real = t.tz_convert("America/New_York")
    fixed = t - pd.Timedelta(hours=5)
    print("DST demo, real New York:", real.strftime("%Y-%m-%d %H:%M %Z"), "| fixed UTC-5:", fixed.strftime("%Y-%m-%d %H:%M"))
    day_start = pd.Timestamp("2024-03-10", tz="America/New_York")
    print("length of New York local day 2024-03-10:", (day_start + pd.offsets.Day(1) - day_start))
except Exception as e:
    print("DST demo skipped:", type(e).__name__, e)
print("asserts passed")
```

**Output (my run):**
```text
SQL, IST day:
user_id streak_start streak_end  days
     U1   2024-03-03 2024-03-04     2
     U1   2024-03-06 2024-03-07     2
     U2   2024-03-04 2024-03-04     1
     U2   2024-03-06 2024-03-06     1
     U3   2024-03-04 2024-03-06     3
     U4   2024-03-09 2024-03-09     1
     U5   2024-03-04 2024-03-04     1
SQL, UTC day:
user_id streak_start streak_end  days
     U1   2024-03-03 2024-03-05     3
     U1   2024-03-07 2024-03-07     1
     U2   2024-03-04 2024-03-05     2
     U3   2024-03-04 2024-03-04     1
     U3   2024-03-06 2024-03-06     1
     U4   2024-03-09 2024-03-09     1
     U5   2024-03-04 2024-03-04     1
check 20:00 UTC on 5 March: ('2024-03-06 01:30:00', '2024-03-06')
T and Z form accepted: ('2024-03-06 01:30:00',)
pandas IST:
user_id streak_start streak_end  days
     U1   2024-03-03 2024-03-04     2
     U1   2024-03-06 2024-03-07     2
     U2   2024-03-04 2024-03-04     1
     U2   2024-03-06 2024-03-06     1
     U3   2024-03-04 2024-03-06     3
     U4   2024-03-09 2024-03-09     1
     U5   2024-03-04 2024-03-04     1
DST demo, real New York: 2024-03-11 00:30 EDT | fixed UTC-5: 2024-03-10 23:30
length of New York local day 2024-03-10: 0 days 23:00:00
asserts passed
```

**Edge cases:**
- Boundary second: 18:30:00 UTC is the first instant of the next IST day (U2); an `end < 18:30:00` style filter on UTC is the same boundary.
- Duplicate days: two logins on one IST day (U3's 6 March) are collapsed by `DISTINCT` on the converted day; the duplicate would otherwise split the streak.
- NULL and malformed timestamps: `date(NULL, ...)` and `date('not a timestamp', ...)` both return NULL in SQLite, so the filter on `IS NOT NULL` is what keeps them out; a NULL group would otherwise appear. Strings like `2024-03-05T20:00:00Z` are also accepted by `datetime()` in this version (my check returned `2024-03-06 01:30:00`).
- Single-row user (U4) and unsorted insertion are handled.
- The day number uses `unixepoch(day) / 86400` (integer seconds, whole days) instead of `julianday`, so there are no floating-point day numbers.

**Then explain:**
- India has no daylight saving, so a fixed offset of +5:30 is exact all year. A zone with DST (New York, London, Berlin) is not a fixed offset: the same UTC instant maps to different local days depending on the date. SQLite has no time zone database, so the fixed-modifier approach is wrong there; do not run it on a DST zone. In pandas I did run a demonstration (above): 04:30 UTC on 11 March 2024 is 00:30 EDT on 11 March in `America/New_York`, whereas a fixed UTC-5 offset gives 23:30 on 10 March, a different day; and the local day of 10 March 2024 is 23 hours long. In SQL engines with zone support, convert with `AT TIME ZONE` in PostgreSQL or `CONVERT_TZ` in MySQL (not executed here, from memory) and store the zone, not the offset.
- Which day is it? Agree with the product team: the user's local day, the company's reporting day (often IST or UTC), or a rolling 24 hours. A user who travels changes local day; a fixed reporting zone is simplest and reproducible. Whatever the choice, compute it once in a conformed `login_day` column.
- Streak length differs between definitions, so any dashboard comparing streaks across time zones must use the same definition.
- Storing UTC and converting at query time keeps the raw data unambiguous; storing local time loses the instant at the DST hour that happens twice.

**Follow-ups:**
- Streak by each user's own zone? Join to a users table with a stored `tz_offset_minutes`, valid only for fixed-offset zones; for DST zones convert in the warehouse with real zone rules.
- Month or year boundaries? Day arithmetic through `unixepoch` handles them; string arithmetic does not (Q6).
- How do you test the boundary? Keep fixture rows at 18:29:59 and 18:30:00 UTC, as U2 does.

**Common mistakes:**
- Using `date(login_ts_utc)` for an Indian audience and calling it daily activity.
- Applying a fixed offset to a DST zone.
- Forgetting to deduplicate after the conversion (two UTC days can collapse onto one local day, or one UTC day can fall on two).
- Converting inside the key but grouping on the raw UTC day.
- Not agreeing the definition of a day before comparing numbers.

### Q40 ⭐ 🔴 Room availability islands: slots(room_id, slot_start, is_free) with one row per room per hour. Return for each room the ranges of at least 3 consecutive free hours as free_from, free_to and hours (the room-booking version of seat availability), using the filtered ROW_NUMBER difference on an hour number derived from julianday, and the LAG-flag alternative on all rows. Show a missing slot row (a gap in the data, not a busy hour) and why it must break a run.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Collapse to one row per room per hour, turn each slot into an integer hour number, keep only the free rows, and group by `hour_number - ROW_NUMBER()` per room; a missing slot row makes the hour number jump, so it breaks the run, and `HAVING COUNT(*) >= 3` keeps ranges of at least three hours.

**Schema and sample data:** hourly slots on 2024-03-04 (R2 runs across midnight), inserted unsorted. R1 has a duplicate row at 11:00, a busy hour at 12:00 and no row at all for 15:00. R2 is free from 22:00 to 01:00. R3 has one free slot. R4 has exactly three free hours then a busy hour and two free hours. R5 has a NULL `is_free`. R6 has a conflicting duplicate at 10:00 (free and busy).
```sql
CREATE TABLE slots(room_id TEXT, slot_start TEXT, is_free INTEGER);
INSERT INTO slots VALUES
 ('R1','2024-03-04 09:00',1),('R1','2024-03-04 10:00',1),('R1','2024-03-04 11:00',1),('R1','2024-03-04 11:00',1),
 ('R1','2024-03-04 12:00',0),
 ('R1','2024-03-04 13:00',1),('R1','2024-03-04 14:00',1),
 ('R1','2024-03-04 16:00',1),('R1','2024-03-04 17:00',1),('R1','2024-03-04 18:00',1),
 ('R2','2024-03-04 23:00',1),('R2','2024-03-05 00:00',1),('R2','2024-03-05 01:00',1),('R2','2024-03-04 22:00',1),
 ('R3','2024-03-04 09:00',1),
 ('R4','2024-03-04 09:00',1),('R4','2024-03-04 10:00',1),('R4','2024-03-04 11:00',1),('R4','2024-03-04 12:00',0),
 ('R4','2024-03-04 13:00',1),('R4','2024-03-04 14:00',1),
 ('R5','2024-03-04 09:00',1),('R5','2024-03-04 10:00',NULL),('R5','2024-03-04 11:00',1),('R5','2024-03-04 12:00',1),
 ('R6','2024-03-04 09:00',1),('R6','2024-03-04 10:00',1),('R6','2024-03-04 10:00',0),('R6','2024-03-04 11:00',1),('R6','2024-03-04 12:00',1);
```

**SQL answer:** `SQL_MAIN` in the Code block. `BASE` (two CTEs, `s` and `h`) collapses duplicates with `MIN(is_free)`, so a slot that is both free and busy counts as busy, and computes the hour number `CAST(ROUND(julianday(slot_start) * 24) AS INTEGER)`. `free_to` is the end of the last free hour (`datetime(MAX(slot_start), '+1 hour')`), so `hours` equals the length of the range:
```sql
WITH s AS (
  SELECT room_id, slot_start, MIN(is_free) AS is_free
  FROM slots GROUP BY room_id, slot_start
),
h AS (
  SELECT room_id, slot_start, is_free,
         CAST(ROUND(julianday(slot_start) * 24) AS INTEGER) AS hr
  FROM s
)
,
f AS (
  SELECT room_id, slot_start, hr,
         hr - ROW_NUMBER() OVER (PARTITION BY room_id ORDER BY hr) AS k
  FROM h WHERE is_free = 1
)
SELECT room_id, MIN(slot_start) AS free_from,
       datetime(MAX(slot_start), '+1 hour') AS free_to, COUNT(*) AS hours
FROM f
GROUP BY room_id, k
HAVING COUNT(*) >= 3
ORDER BY room_id, free_from
```
The LAG-flag alternative on all rows, `SQL_LAG` (also `BASE`, then `l` and `g`): a row continues a run only when it is free, the previous row is free, and the hour number is exactly one more; otherwise the flag is 1 and a new group starts. Group, filter to free rows, and apply the same `HAVING`:
```sql
WITH s AS (
  SELECT room_id, slot_start, MIN(is_free) AS is_free
  FROM slots GROUP BY room_id, slot_start
),
h AS (
  SELECT room_id, slot_start, is_free,
         CAST(ROUND(julianday(slot_start) * 24) AS INTEGER) AS hr
  FROM s
)
,
l AS (
  SELECT room_id, slot_start, is_free, hr,
         LAG(is_free) OVER w AS pf, LAG(hr) OVER w AS ph
  FROM h WINDOW w AS (PARTITION BY room_id ORDER BY hr)
),
g AS (
  SELECT *, SUM(CASE WHEN is_free = 1 AND pf = 1 AND hr - ph = 1 THEN 0 ELSE 1 END)
            OVER (PARTITION BY room_id ORDER BY hr) AS grp
  FROM l
)
SELECT room_id, MIN(slot_start) AS free_from,
       datetime(MAX(slot_start), '+1 hour') AS free_to, COUNT(*) AS hours
FROM g
WHERE is_free = 1
GROUP BY room_id, grp
HAVING COUNT(*) >= 3
ORDER BY room_id, free_from
```
`SQL_ROWORDER` in the Code block is the wrong version that numbers rows instead of using the hour number.

**pandas answer:** same logic, identical to the Code block:
```py
s = slots.groupby(["room_id", "slot_start"], as_index=False)["is_free"].min()   # MIN skips NaN like SQL
t = pd.to_datetime(s["slot_start"])
s["hr"] = (t - pd.Timestamp("1970-01-01")) // pd.Timedelta(hours=1)
f = s[s["is_free"] == 1].sort_values(["room_id", "hr"]).copy()
f["k"] = f["hr"] - f.groupby("room_id").cumcount()
pd_df = (f.groupby(["room_id", "k"])
          .agg(free_from=("slot_start", "min"), last=("slot_start", "max"), hours=("hr", "size"))
          .reset_index())
pd_df = pd_df[pd_df["hours"] >= 3].copy()
pd_df["free_to"] = (pd.to_datetime(pd_df["last"]) + pd.Timedelta(hours=1)).dt.strftime("%Y-%m-%d %H:%M:%S")
pd_df = pd_df[["room_id", "free_from", "free_to", "hours"]].sort_values(["room_id", "free_from"]).reset_index(drop=True)
```

**Example:**
- R1: after dedup, 09:00, 10:00, 11:00 are free (hour numbers h, h+1, h+2), 12:00 is busy, 13:00 and 14:00 are free, 15:00 has no row, 16:00, 17:00, 18:00 are free. Free rows in order get row numbers 1 to 8. Keys `hr - rn`: the first three share one key; 13:00 and 14:00 are the next two rows but their hour numbers jumped by 2 (past the busy 12:00), so the key is larger and shared by those two; 16:00 jumped again (the missing 15:00 row), so the key rises again and is shared by 16, 17, 18. Groups of 3, 2 and 3: ranges 09:00-12:00 (3 hours) and 16:00-19:00 (3 hours); the 2-hour group is dropped.
- With row order instead of hour numbers (`SQL_ROWORDER`) the missing 15:00 row is invisible, 13:00, 14:00, 16:00, 17:00, 18:00 look consecutive and the output shows a bogus 5-hour range starting 13:00.
- R2: 22:00, 23:00, 00:00, 01:00 have consecutive hour numbers across midnight: one range of 4 hours, 22:00 to 02:00 the next day.
- R3 (one slot) and R6 (the 10:00 duplicate resolves to busy, leaving 09:00 alone and 11:00-12:00, a 2-hour group) return nothing.
- R4: exactly 3 free hours, 09:00-12:00: returned, so the threshold is inclusive. The later 2-hour group is dropped.
- R5: the NULL slot is neither free nor busy; `is_free = 1` drops it and the hour numbers jump, so 09:00 alone and 11:00-12:00 (2 hours) both fall short.

**Code:** run with `python3 -I`. The asserts check that the two SQL methods return identical frames and that pandas equals SQL after sorting by `room_id, free_from`. The block also tests how `julianday * 24` behaves, and a few small tables.
```python
# Q40: room availability islands (>= 3 consecutive free hours), SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE slots(room_id TEXT, slot_start TEXT, is_free INTEGER);
INSERT INTO slots VALUES
 ('R1','2024-03-04 09:00',1),('R1','2024-03-04 10:00',1),('R1','2024-03-04 11:00',1),('R1','2024-03-04 11:00',1),
 ('R1','2024-03-04 12:00',0),
 ('R1','2024-03-04 13:00',1),('R1','2024-03-04 14:00',1),
 ('R1','2024-03-04 16:00',1),('R1','2024-03-04 17:00',1),('R1','2024-03-04 18:00',1),
 ('R2','2024-03-04 23:00',1),('R2','2024-03-05 00:00',1),('R2','2024-03-05 01:00',1),('R2','2024-03-04 22:00',1),
 ('R3','2024-03-04 09:00',1),
 ('R4','2024-03-04 09:00',1),('R4','2024-03-04 10:00',1),('R4','2024-03-04 11:00',1),('R4','2024-03-04 12:00',0),
 ('R4','2024-03-04 13:00',1),('R4','2024-03-04 14:00',1),
 ('R5','2024-03-04 09:00',1),('R5','2024-03-04 10:00',NULL),('R5','2024-03-04 11:00',1),('R5','2024-03-04 12:00',1),
 ('R6','2024-03-04 09:00',1),('R6','2024-03-04 10:00',1),('R6','2024-03-04 10:00',0),('R6','2024-03-04 11:00',1),('R6','2024-03-04 12:00',1);
"""
BASE = """
WITH s AS (
  SELECT room_id, slot_start, MIN(is_free) AS is_free
  FROM slots GROUP BY room_id, slot_start
),
h AS (
  SELECT room_id, slot_start, is_free,
         CAST(ROUND(julianday(slot_start) * 24) AS INTEGER) AS hr
  FROM s
)
"""
SQL_MAIN = BASE + """,
f AS (
  SELECT room_id, slot_start, hr,
         hr - ROW_NUMBER() OVER (PARTITION BY room_id ORDER BY hr) AS k
  FROM h WHERE is_free = 1
)
SELECT room_id, MIN(slot_start) AS free_from,
       datetime(MAX(slot_start), '+1 hour') AS free_to, COUNT(*) AS hours
FROM f
GROUP BY room_id, k
HAVING COUNT(*) >= 3
ORDER BY room_id, free_from
"""
SQL_LAG = BASE + """,
l AS (
  SELECT room_id, slot_start, is_free, hr,
         LAG(is_free) OVER w AS pf, LAG(hr) OVER w AS ph
  FROM h WINDOW w AS (PARTITION BY room_id ORDER BY hr)
),
g AS (
  SELECT *, SUM(CASE WHEN is_free = 1 AND pf = 1 AND hr - ph = 1 THEN 0 ELSE 1 END)
            OVER (PARTITION BY room_id ORDER BY hr) AS grp
  FROM l
)
SELECT room_id, MIN(slot_start) AS free_from,
       datetime(MAX(slot_start), '+1 hour') AS free_to, COUNT(*) AS hours
FROM g
WHERE is_free = 1
GROUP BY room_id, grp
HAVING COUNT(*) >= 3
ORDER BY room_id, free_from
"""
SQL_ROWORDER = """
WITH s AS (SELECT room_id, slot_start, MIN(is_free) AS is_free FROM slots GROUP BY room_id, slot_start),
f AS (
  SELECT room_id, slot_start,
         ROW_NUMBER() OVER (PARTITION BY room_id ORDER BY slot_start) AS rn_all
  FROM s
),
t AS (
  SELECT s.room_id, s.slot_start, f.rn_all,
         ROW_NUMBER() OVER (PARTITION BY s.room_id ORDER BY s.slot_start) AS rn_free
  FROM s JOIN f USING (room_id, slot_start) WHERE s.is_free = 1
)
SELECT room_id, MIN(slot_start) AS free_from, COUNT(*) AS hours
FROM t GROUP BY room_id, rn_all - rn_free HAVING COUNT(*) >= 3 ORDER BY room_id, free_from
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
lag_df = pd.read_sql_query(SQL_LAG, con)
print("SQL filtered ROW_NUMBER difference:"); print(sql_df.to_string(index=False))
assert sql_df.equals(lag_df)
print("SQL LAG-flag on all rows gives the same rows: True")
print("wrong, row order instead of hour number (R1 merges across the missing 15:00 row):")
print(pd.read_sql_query(SQL_ROWORDER, con).to_string(index=False))

slots = pd.read_sql_query("SELECT * FROM slots", con)
# pd:main
s = slots.groupby(["room_id", "slot_start"], as_index=False)["is_free"].min()   # MIN skips NaN like SQL
t = pd.to_datetime(s["slot_start"])
s["hr"] = (t - pd.Timestamp("1970-01-01")) // pd.Timedelta(hours=1)
f = s[s["is_free"] == 1].sort_values(["room_id", "hr"]).copy()
f["k"] = f["hr"] - f.groupby("room_id").cumcount()
pd_df = (f.groupby(["room_id", "k"])
          .agg(free_from=("slot_start", "min"), last=("slot_start", "max"), hours=("hr", "size"))
          .reset_index())
pd_df = pd_df[pd_df["hours"] >= 3].copy()
pd_df["free_to"] = (pd.to_datetime(pd_df["last"]) + pd.Timedelta(hours=1)).dt.strftime("%Y-%m-%d %H:%M:%S")
pd_df = pd_df[["room_id", "free_from", "free_to", "hours"]].sort_values(["room_id", "free_from"]).reset_index(drop=True)
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
# compare after sorting by room_id, free_from
assert pd_df.astype({"hours": "int64"}).equals(sql_df.astype({"hours": "int64"}))

# julianday precision test: does CAST(julianday * 24 AS INTEGER) truncate wrongly where ROUND does not?
con.execute("""
CREATE TABLE hrs AS
WITH RECURSIVE x(ts) AS (
  SELECT '2020-01-01 00:00' UNION ALL SELECT strftime('%Y-%m-%d %H:%M', ts, '+1 hour') FROM x WHERE ts < '2030-12-31 23:00'
) SELECT ts FROM x
""")
row = con.execute("""
SELECT COUNT(*), SUM(CAST(julianday(ts) * 24 AS INTEGER) <> CAST(ROUND(julianday(ts) * 24) AS INTEGER)) FROM hrs
""").fetchone()
# offset between the two day-number systems is constant: julianday(1970-01-01) * 24
off = con.execute("SELECT CAST(ROUND(julianday('1970-01-01') * 24) AS INTEGER)").fetchone()[0]
mism = con.execute("SELECT COUNT(*) FROM hrs WHERE CAST(ROUND(julianday(ts) * 24) AS INTEGER) - unixepoch(ts) / 3600 <> ?", (off,)).fetchone()[0]
print("hourly stamps 2020-2030:", row[0], "| CAST truncation differs from ROUND:", row[1],
      "| ROUND(julianday*24) minus unixepoch/3600 not constant:", mism)

# the same test one level finer: minute stamps in 2024, julianday * 1440 truncated versus rounded
con.execute("""
CREATE TABLE mins AS
WITH RECURSIVE x(ts) AS (
  SELECT '2024-01-01 00:00' UNION ALL SELECT strftime('%Y-%m-%d %H:%M', ts, '+1 minute') FROM x WHERE ts < '2024-12-31 23:59'
) SELECT ts FROM x
""")
m = con.execute("""
SELECT COUNT(*), SUM(CAST(julianday(ts) * 1440 AS INTEGER) <> CAST(ROUND(julianday(ts) * 1440) AS INTEGER)),
       SUM(ABS(julianday(ts) * 1440 - ROUND(julianday(ts) * 1440)) > 0.001)
FROM mins
""").fetchone()
print("minute stamps in 2024:", m[0], "| truncation differs from ROUND:", m[1], "| off by more than 0.001 minute:", m[2])

print("--- edge cases ---")
for name, ins in [("empty table", ""), ("one free slot", "('Z','2024-03-04 09:00',1)"),
                  ("exactly 2 free", "('Z','2024-03-04 09:00',1),('Z','2024-03-04 10:00',1)"),
                  ("exactly 3 free", "('Z','2024-03-04 09:00',1),('Z','2024-03-04 10:00',1),('Z','2024-03-04 11:00',1)")]:
    con.execute("DELETE FROM slots")
    if ins:
        con.execute("INSERT INTO slots VALUES " + ins)
    print(name, "->", con.execute(SQL_MAIN).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
SQL filtered ROW_NUMBER difference:
room_id        free_from             free_to  hours
     R1 2024-03-04 09:00 2024-03-04 12:00:00      3
     R1 2024-03-04 16:00 2024-03-04 19:00:00      3
     R2 2024-03-04 22:00 2024-03-05 02:00:00      4
     R4 2024-03-04 09:00 2024-03-04 12:00:00      3
SQL LAG-flag on all rows gives the same rows: True
wrong, row order instead of hour number (R1 merges across the missing 15:00 row):
room_id        free_from  hours
     R1 2024-03-04 09:00      3
     R1 2024-03-04 13:00      5
     R2 2024-03-04 22:00      4
     R4 2024-03-04 09:00      3
pandas:
room_id        free_from             free_to  hours
     R1 2024-03-04 09:00 2024-03-04 12:00:00      3
     R1 2024-03-04 16:00 2024-03-04 19:00:00      3
     R2 2024-03-04 22:00 2024-03-05 02:00:00      4
     R4 2024-03-04 09:00 2024-03-04 12:00:00      3
hourly stamps 2020-2030: 96432 | CAST truncation differs from ROUND: 0 | ROUND(julianday*24) minus unixepoch/3600 not constant: 0
minute stamps in 2024: 527040 | truncation differs from ROUND: 70272 | off by more than 0.001 minute: 0
--- edge cases ---
empty table -> []
one free slot -> []
exactly 2 free -> []
exactly 3 free -> [('Z', '2024-03-04 09:00', '2024-03-04 12:00:00', 3)]
asserts passed
```

**Edge cases:**
- Missing slot row (R1 15:00): it is absent data, not a busy hour; the hour-number key breaks the run, which is the safe choice (an unknown hour must not be reported as free). Row-order keys miss it, as the wrong version shows.
- Busy hour (R1 12:00) also breaks the run because it is filtered out and the hour number jumps. In the LAG version it breaks because `is_free = 1` fails.
- Duplicates: exact duplicates collapse; conflicting duplicates take `MIN(is_free)`, so any busy row wins. If you prefer "any free wins" use `MAX`. SQL `MIN` skips NULLs, so a free row plus a NULL row resolves to free; state that rule.
- NULL `is_free` (R5): not free (it does not equal 1). Decide whether unknown should be treated as busy; this answer does.
- Single-row room, and a room with exactly 2 or 3 free hours: the code ran an empty table, one slot, two slots and exactly three slots; only three returned a row.
- Midnight (R2): the hour number is continuous across the date change; a key built from the date or the hour of day would break.
- Precision: hour number from `julianday` needs `ROUND` before `CAST`. Over 96,432 hourly stamps (2020 to 2030) `CAST(julianday * 24 AS INTEGER)` happened to equal the rounded value every time, and `ROUND(julianday * 24)` minus `unixepoch / 3600` was the same constant for every row. At minute granularity in 2024 (527,040 stamps) truncating `julianday * 1440` differed from the rounded value for 70,272 stamps (the printed counts), although the value itself was never off by more than 0.001 minute. So always `ROUND`, or use integer `unixepoch(slot_start) / 3600`, which is exact.
- Time zones and DST: slot times are assumed to be in one fixed zone; across a DST change a local day has 23 or 25 hours and the hour numbers of local timestamps would repeat or skip (not executed in SQLite; see Q39).

**Then explain:**
- This is the seat-availability problem (Q18) with time instead of seat ids: the number line is the hour number, and a missing or busy hour is a gap in it.
- Filtering before `ROW_NUMBER` is what lets the hour number and the row number advance together; any row that is not free must leave the numbered set.
- The LAG version keeps all rows and flags run boundaries explicitly. It is longer but makes the missing-row check visible (`hr - ph = 1`) and does not depend on filter-then-number ordering; both gave identical rows here.
- `free_to` is exclusive (the end of the last hour), so a range 16:00 to 19:00 means the room is free from 16:00 until 19:00.
- Dialects (not executed here): PostgreSQL would compute the hour number with `EXTRACT(EPOCH FROM slot_start) / 3600` and could use `generate_series` to complete the grid; MySQL uses `UNIX_TIMESTAMP(slot_start) DIV 3600`.

**Follow-ups:**
- Rooms free for at least 3 hours that start on the hour, between 09:00 and 18:00? Add a filter on the hour of day before numbering.
- Find a slot common to two rooms? Intersect the free hour numbers per room first.
- Thirty-minute slots? Use `unixepoch / 1800` as the number.

**Common mistakes:**
- `ROW_NUMBER()` difference on row position, so a missing slot row looks consecutive.
- `CAST(julianday(...) * 24 AS INTEGER)` without `ROUND`.
- Treating NULL as free.
- Using `>= 3` hours but counting rows that include duplicates.
- Forgetting `PARTITION BY room_id`, so runs leak across rooms.

