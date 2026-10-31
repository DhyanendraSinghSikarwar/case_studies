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
