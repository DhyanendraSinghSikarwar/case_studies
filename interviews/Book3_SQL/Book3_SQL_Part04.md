# Book 3 — Part 4: Window functions: ranking and top-N per group, with pandas equivalents

**Topic:** window function concepts (OVER, PARTITION BY, ORDER BY inside OVER, window versus GROUP BY, order of evaluation and why windows cannot be used in WHERE, CTE or subquery workaround, QUALIFY as dialect text), ROW_NUMBER versus RANK versus DENSE_RANK and ties, tie-breakers and deterministic ranking, top-N per group (with and without ties, WITH TIES hedge), nth highest salary and the LeetCode 176, 177, 184 and 185 classics, deduplication keeping the latest or first row, finding and deleting duplicates, first and last row per group, FIRST_VALUE, LAST_VALUE (default-frame trap) and NTH_VALUE, NTILE and quartiles or deciles, PERCENT_RANK and CUME_DIST, median and percentiles via windows (PERCENTILE_CONT hedged), percent of group total and difference from group average, ranking by multiple columns, ranking within a filtered subset, NULLs in window ORDER BY, ranking an aggregate (GROUP BY then RANK), named windows, windows versus join fan-out, window performance concept, and the pandas side (rank methods and na_option, groupby rank, cumcount, head, nlargest, transform, sort_values with drop_duplicates, idxmax, qcut versus NTILE, pct=True versus PERCENT_RANK)
**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 19, ⭐⭐ 19, ⭐ 12)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers ranking, top-N, deduplication, first/last-value and percentile-style window functions. Running totals, LAG and LEAD, moving averages (Part 5), date/cohort logic (Part 6), gaps and islands and sessionization (Part 7) are deliberately out; frames appear only to explain the default RANGE frame and the LAST_VALUE trap. Every query question states its tables and columns so Wave B can build small sample data; answers must run on SQLite 3.45 (window functions since 3.25) and compare with pandas 3.0.x; anything engine-specific (QUALIFY, DISTINCT ON, WITH TIES, PERCENTILE_CONT) is shown as hedged text labelled 'not executed' unless run.

Verification notes for Wave B (from pages opened in Wave A, as summarised by the fetch tool): the SQLite windowfunctions page says window functions may appear only in the result set and ORDER BY of a SELECT, lists 11 built-ins (row_number, rank, dense_rank, percent_rank, cume_dist, ntile, lag, lead, first_value, last_value, nth_value), says ntile gives larger groups first, percent_rank is (rank-1)/(partition-rows-1) and 0.0 for a one-row partition, cume_dist is row-number of the last peer over partition rows, nth_value gives NULL when the frame has no Nth row, the default frame is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE NO OTHERS, peers share ORDER BY values, the WINDOW clause sits after HAVING and before ORDER BY, and window functions arrived in 3.25.0 (2018-09-15) with GROUPS frames and EXCLUDE in 3.28.0; first_value, last_value and nth_value are the built-ins that use the frame. The PostgreSQL tutorial says windows run after WHERE, GROUP BY and HAVING, are allowed only in SELECT and ORDER BY, ties in row_number are numbered in unspecified order, and gives the subquery pattern for top-N. The pandas rank reference says methods are average, min, max, first and dense, na_option is keep, top or bottom, pct gives percentile form (docs example: pct 0.625 for a tied pair at ranks 2 and 3 of 4 non-NaN values), and the qcut reference says equal-frequency bins, duplicates='raise' by default and 'drop' removes non-unique edges. Items NOT verified from pages (run or hedge): how SQLite orders NULLs in a window ORDER BY (the page does not say; run it), NULLS FIRST / LAST in SQLite 3.30+ (version from general knowledge), PostgreSQL and MySQL NULL ordering defaults, QUALIFY support list, DISTINCT ON, FETCH FIRST WITH TIES (PostgreSQL 13), MySQL 8.0 window support, PERCENTILE_CONT availability, IGNORE NULLS, whether SQLite allows a named window to be extended in OVER, pandas cumcount, groupby head and nlargest keep='all' behaviour, groupby idxmax with NaN, pandas quantile default interpolation, and any LeetCode problem statement wording.

Evidence limits: no candidate-reported SQL questions were found; the search returned prep guides, practice-site pages, third-party LeetCode list snippets and documentation. The 'Asked at' tags are source types, and 'expert gap-check' marks questions chosen from practice. Star ratings blend how often a topic appears across guides with judgement. See research_notes/Book3_Part04_sources.md for which pages were opened.

---

### Q1 ⭐⭐⭐ 🟢 What is a window function, and how does it differ from GROUP BY? employees(emp_id, name, dept_id, salary). Show each employee's row with the average salary of their department using AVG(salary) OVER (PARTITION BY dept_id), and the same average with GROUP BY (one row per department). Explain OVER, PARTITION BY (no PARTITION BY means one partition) and ORDER BY inside OVER, that window functions keep every input row, and give the pandas equivalents (groupby transform('mean') versus groupby agg).
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** A window function computes a value over a set of related rows but keeps every input row; `GROUP BY` collapses each group to one row, so `AVG(salary) OVER (PARTITION BY dept_id)` gives each employee the department average next to their own salary, while `GROUP BY dept_id` gives one row per department.

**Schema and sample data:** seven employees, one NULL salary (Gita), and a department (30) with one person.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55),(7,'Gita',20,NULL);
```

**SQL answer:** `SQL_WINDOW` keeps all rows, `SQL_GROUP` collapses, `SQL_ORDERED` shows `OVER ()` and an `ORDER BY` inside `OVER` (all in the Code block).
```sql
SELECT emp_id, name, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees
ORDER BY emp_id
```
```sql
SELECT dept_id, AVG(salary) AS dept_avg, COUNT(*) AS n_rows
FROM employees
GROUP BY dept_id
ORDER BY dept_id
```
```sql
SELECT emp_id, dept_id, salary,
       AVG(salary) OVER ()                                 AS company_avg,
       AVG(salary) OVER (PARTITION BY dept_id ORDER BY emp_id) AS avg_so_far
FROM employees
ORDER BY emp_id
```

**pandas answer:** `transform("mean")` is the window version (one value per original row); `groupby().agg()` is the GROUP BY version.
```py
pd_win = emp.assign(dept_avg=emp.groupby("dept_id")["salary"].transform("mean"))
```
```py
pd_grp = (emp.groupby("dept_id")
             .agg(dept_avg=("salary", "mean"), n_rows=("emp_id", "size"))
             .reset_index())
```

**Example:** averages ignore NULL.
- Dept 10: (50 + 70 + 60) / 3 = 60, so Asha, Ben and Chitra all show 60.
- Dept 20: Dev 90, Esha 40, Gita NULL, so (90 + 40) / 2 = 65 (NULL is skipped); all three rows show 65.
- Dept 30: Farid alone, 55.
- `OVER ()` has no PARTITION BY, so the whole table is one partition: (50+70+60+90+40+55) / 6 = 60.83 on every row.
- With `ORDER BY emp_id` inside `OVER`, the average becomes "so far": dept 10 shows 50, then (50+70)/2 = 60, then 60; dept 20 shows 90, then 65, then 65 (Gita's NULL adds nothing). That is a running value, which is Part 5 territory; here it only shows that ORDER BY inside OVER changes what the function sees.
- GROUP BY returns 3 rows for 7 input rows; the window query returns 7.

**Code:** run with `python3 -I`.
```python
# Q1: window function versus GROUP BY
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55),(7,'Gita',20,NULL);
"""
SQL_WINDOW = """
SELECT emp_id, name, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees
ORDER BY emp_id
"""
SQL_GROUP = """
SELECT dept_id, AVG(salary) AS dept_avg, COUNT(*) AS n_rows
FROM employees
GROUP BY dept_id
ORDER BY dept_id
"""
SQL_ORDERED = """
SELECT emp_id, dept_id, salary,
       AVG(salary) OVER ()                                 AS company_avg,
       AVG(salary) OVER (PARTITION BY dept_id ORDER BY emp_id) AS avg_so_far
FROM employees
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_win = pd.read_sql_query(SQL_WINDOW, con)
sql_grp = pd.read_sql_query(SQL_GROUP, con)
sql_ord = pd.read_sql_query(SQL_ORDERED, con)
print("window (every row kept):"); print(sql_win.to_string(index=False))
print("\nGROUP BY (one row per department):"); print(sql_grp.to_string(index=False))
print("\nOVER () and ORDER BY inside OVER:"); print(sql_ord.round(2).to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:window
pd_win = emp.assign(dept_avg=emp.groupby("dept_id")["salary"].transform("mean"))
# pd:end
# pd:group
pd_grp = (emp.groupby("dept_id")
             .agg(dept_avg=("salary", "mean"), n_rows=("emp_id", "size"))
             .reset_index())
# pd:end
# compared after sorting by emp_id (window) and dept_id (group)
pd.testing.assert_frame_equal(sql_win, pd_win.sort_values("emp_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_grp, pd_grp.sort_values("dept_id").reset_index(drop=True), check_dtype=False)
print("\nrows in: %d, window rows out: %d, group rows out: %d" % (len(emp), len(sql_win), len(sql_grp)))
print("asserts passed: window == transform('mean'), GROUP BY == groupby.agg")
```

**Output (my run):**
```text
window (every row kept):
 emp_id   name  dept_id  salary  dept_avg
      1   Asha       10    50.0      60.0
      2    Ben       10    70.0      60.0
      3 Chitra       10    60.0      60.0
      4    Dev       20    90.0      65.0
      5   Esha       20    40.0      65.0
      6  Farid       30    55.0      55.0
      7   Gita       20     NaN      65.0

GROUP BY (one row per department):
 dept_id  dept_avg  n_rows
      10      60.0       3
      20      65.0       3
      30      55.0       1

OVER () and ORDER BY inside OVER:
 emp_id  dept_id  salary  company_avg  avg_so_far
      1       10    50.0        60.83        50.0
      2       10    70.0        60.83        60.0
      3       10    60.0        60.83        60.0
      4       20    90.0        60.83        90.0
      5       20    40.0        60.83        65.0
      6       30    55.0        60.83        55.0
      7       20     NaN        60.83        65.0

rows in: 7, window rows out: 7, group rows out: 3
asserts passed: window == transform('mean'), GROUP BY == groupby.agg
```

**Edge cases:**
- NULL salary: skipped by `AVG` in both forms (Gita still gets a department average of 65, her own salary stays NULL / NaN).
- NULL `dept_id` (none in this data): `PARTITION BY` and `GROUP BY` both put all NULLs in one group. In pandas, `groupby` drops NaN keys by default, so `transform` would give NaN for those rows (the Part 3 Q5 answer shows this); pass `dropna=False` to keep them.
- A one-row partition: the average is the row itself (Farid, 55).
- Empty table: the window query returns no rows, and so does GROUP BY (no groups).

**Then explain:**
- `OVER (...)` is what turns an aggregate into a window function. `PARTITION BY` splits rows into groups for the calculation only; no PARTITION BY means one partition holding every row.
- `ORDER BY` inside `OVER` orders rows within the partition, and for aggregates it also shrinks the frame (default frame: start of partition up to the current row and its ties). I only show the idea; running totals are Part 5.
- Use a window when you need row detail next to a group number (above-average earners, share of total). Use GROUP BY when you want the summary only.
- Window functions run after `WHERE`, `GROUP BY` and `HAVING`, so they see the rows that survived those steps.
- pandas mapping: window = `groupby(...).transform(...)` (same length as the frame, same index); GROUP BY = `groupby(...).agg(...)` (one row per group).

**Follow-ups:**
- *Can I get both in one query?* Yes: `GROUP BY` first, then a window over the grouped rows (Q13 does this).
- *Can I filter on the window value?* Not in `WHERE`; wrap it in a CTE or subquery (Q3).
- *Is the window slower?* It needs the rows grouped and, if ordered, sorted; I did not time it (Q40 looks at the plan).

**Common mistakes:**
- Expecting `OVER` to reduce rows.
- Forgetting `PARTITION BY` and getting the company-wide average on every row.
- Adding `ORDER BY` inside `OVER` for an average and getting a running average by accident.
- In pandas, using `groupby().mean()` where `transform("mean")` is needed, which gives a different length.

### Q2 ⭐⭐⭐ 🟢 ROW_NUMBER versus RANK versus DENSE_RANK on ties: scores(player_id, score) with scores 100, 100, 90, 80. Show the three columns side by side (1,2,3,4 / 1,1,3,4 / 1,1,2,3), explain the gap after a tie in RANK, which function is arbitrary on ties (ROW_NUMBER) and why, and give the pandas rank(method='first' / 'min' / 'dense') equivalents with ascending=False.
**Asked at:** GeeksforGeeks SQL interview questions (RANK vs DENSE_RANK vs ROW_NUMBER, window functions, duplicates entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** On scores 100, 100, 90, 80, `ROW_NUMBER` gives 1,2,3,4 (always unique), `RANK` gives 1,1,3,4 (ties share a number and the next number skips), and `DENSE_RANK` gives 1,1,2,3 (ties share a number and nothing is skipped).

**Schema and sample data:**
```sql
CREATE TABLE scores(player_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,100),(2,100),(3,90),(4,80);
```

**SQL answer:** `SQL_MAIN` shows the three side by side. For `ROW_NUMBER` I add `player_id` as a stated tie-breaker (lower player_id first) so the result is deterministic. `SQL_NOTIE` is the same function with `ORDER BY score DESC` only.
```sql
SELECT player_id, score,
       ROW_NUMBER() OVER (ORDER BY score DESC, player_id) AS row_num,
       RANK()       OVER (ORDER BY score DESC)            AS rnk,
       DENSE_RANK() OVER (ORDER BY score DESC)            AS dense_rnk
FROM scores
ORDER BY score DESC, player_id
```
```sql
SELECT player_id, score, ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
FROM scores
ORDER BY score DESC, player_id
```

**pandas answer:** `rank(method=..., ascending=False)` with `first`, `min` and `dense`; rank returns floats, so I cast to int (there are no NaN here).
```py
pd_df = scores.assign(
    row_num=scores["score"].rank(method="first", ascending=False).astype(int),
    rnk=scores["score"].rank(method="min", ascending=False).astype(int),
    dense_rnk=scores["score"].rank(method="dense", ascending=False).astype(int),
)
```

**Example:**

| player | score | ROW_NUMBER | RANK | DENSE_RANK |
|---|---|---|---|---|
| 1 | 100 | 1 | 1 | 1 |
| 2 | 100 | 2 | 1 | 1 |
| 3 | 90 | 3 | 3 | 2 |
| 4 | 80 | 4 | 4 | 3 |

- Players 1 and 2 are tied on score, so `RANK` and `DENSE_RANK` give both 1.
- `RANK` then skips to 3 because two rows already sit above player 3 (rank = 1 + number of rows strictly ahead). `DENSE_RANK` gives 2 (it counts distinct score levels).
- `ROW_NUMBER` just numbers the sorted rows; with the `player_id` tie-break player 1 gets 1 and player 2 gets 2.

**Code:** run with `python3 -I`.
```python
# Q2: ROW_NUMBER vs RANK vs DENSE_RANK on ties
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE scores(player_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,100),(2,100),(3,90),(4,80);
"""
# tie-break for ROW_NUMBER stated: player_id ascending
SQL_MAIN = """
SELECT player_id, score,
       ROW_NUMBER() OVER (ORDER BY score DESC, player_id) AS row_num,
       RANK()       OVER (ORDER BY score DESC)            AS rnk,
       DENSE_RANK() OVER (ORDER BY score DESC)            AS dense_rnk
FROM scores
ORDER BY score DESC, player_id
"""
SQL_NOTIE = """
SELECT player_id, score, ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
FROM scores
ORDER BY score DESC, player_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

scores = pd.read_sql_query("SELECT * FROM scores ORDER BY player_id", con)
# pd:main
pd_df = scores.assign(
    row_num=scores["score"].rank(method="first", ascending=False).astype(int),
    rnk=scores["score"].rank(method="min", ascending=False).astype(int),
    dense_rnk=scores["score"].rank(method="dense", ascending=False).astype(int),
)
# pd:end
# compared after sorting by score desc, player_id
pd_sorted = pd_df.sort_values(["score", "player_id"], ascending=[False, True]).reset_index(drop=True)
pd.testing.assert_frame_equal(sql_df, pd_sorted, check_dtype=False)

# without a tie-breaker: only the SET of numbers given to the tied pair is guaranteed
nt = pd.read_sql_query(SQL_NOTIE, con)
print("\nROW_NUMBER with ORDER BY score DESC only (which tied player gets 1 is not guaranteed):")
print(nt.to_string(index=False))
assert sorted(nt.loc[nt["score"] == 100, "row_num"]) == [1, 2]

# pandas 'first' follows row order, so it is deterministic only because the frame is in player_id order
rev = scores.iloc[::-1]
print("\npandas method='first' on the reversed frame gives the tied pair:",
      dict(zip(rev["player_id"], rev["score"].rank(method="first", ascending=False).astype(int))))
print("asserts passed: SQL row_num/rnk/dense_rnk == pandas first/min/dense")
```

**Output (my run):**
```text
 player_id  score  row_num  rnk  dense_rnk
         1    100        1    1          1
         2    100        2    1          1
         3     90        3    3          2
         4     80        4    4          3

ROW_NUMBER with ORDER BY score DESC only (which tied player gets 1 is not guaranteed):
 player_id  score  row_num
         1    100        1
         2    100        2
         3     90        3
         4     80        4

pandas method='first' on the reversed frame gives the tied pair: {4: 4, 3: 3, 2: 1, 1: 2}
asserts passed: SQL row_num/rnk/dense_rnk == pandas first/min/dense
```

**Edge cases:**
- Ties: the only function that must break them is `ROW_NUMBER`. Without a tie-breaker the standard promises only that the tied rows get 1 and 2 in some order. In my SQLite 3.45 run the unbroken query gave player 1 the 1 (the same as the stated tie-break), but that is the engine's scan order showing through, not a guarantee; other engines were not executed.
- pandas `method="first"` breaks ties by row order in the frame, not by any column. On the same data reversed, player 2 got 1 and player 1 got 2 (see output). So sort first if you need a rule.
- NULL scores: SQL ranks them (NULL is smallest in SQLite, so last in DESC); pandas `rank` leaves NaN as NaN by default (`na_option="keep"`). No NULLs in this data; Q29 and Q30 cover it.
- A table with one row: all three give 1.

**Then explain:**
- `RANK` has gaps after ties; `DENSE_RANK` never has gaps; `ROW_NUMBER` never has ties.
- Use `ROW_NUMBER` when you need exactly one row per rank (dedup, pagination), `RANK` for competition-style positions, `DENSE_RANK` for "top N levels".
- pandas map: `first` = ROW_NUMBER (on a pre-sorted frame), `min` = RANK, `dense` = DENSE_RANK. `method="min"` gives the lowest position of the tied group, which is what RANK does.
- `ascending=False` is needed because SQL used `ORDER BY score DESC`; pandas ranks smallest first by default.

**Follow-ups:**
- *Which one is arbitrary on ties and why?* `ROW_NUMBER`: it must give distinct numbers to rows that compare equal, so the engine picks an order unless you supply more `ORDER BY` columns.
- *What do the numbers look like for 100, 100, 100?* 1,2,3 / 1,1,1 / 1,1,1.
- *What is `method="max"`?* The highest position of the tie; it has no direct built-in SQL twin (Q42 relates it to `CUME_DIST`).

**Common mistakes:**
- Believing `ROW_NUMBER` is "the same as RANK but without ties" and trusting which tied row got 1.
- Forgetting `ascending=False` in pandas and ranking the lowest score first.
- Reading `RANK = 2` as "second place" when two rows tie for first (no row has rank 2).

### Q3 ⭐⭐⭐ 🟢 Why can't you use a window function in WHERE, and what is the workaround? employees(emp_id, name, dept_id, salary). Show the failing query WHERE RANK() OVER (...) <= 3 and explain the order of evaluation (FROM, WHERE, GROUP BY, HAVING, window functions, SELECT, ORDER BY, LIMIT). Give the CTE or subquery fix, and show QUALIFY as dialect text (BigQuery, Snowflake, DuckDB; not in SQLite, PostgreSQL or MySQL; not executed).
**Asked at:** techinterview.org window-function gotchas article (ties, RANK = 2 returning nothing, window in WHERE, default frame), a guide and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** A window function cannot be in `WHERE` because `WHERE` runs before windows are computed; compute the rank in a CTE or subquery, then filter on it in the outer query.

**Schema and sample data:** nine employees; department 10 has a tie at the top (Ben and Dev both 70) and five people; department 20 has a tie at 80.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),(4,'Dev',10,70),
  (5,'Esha',10,40),(6,'Farid',20,90),(7,'Gita',20,80),(8,'Hari',20,80),(9,'Ila',30,55);
```

**SQL answer:** `SQL_FAIL` is the broken query. `SQL_MAIN` is the CTE fix, `SQL_SUBQ` is the derived-table fix (same rows).
```sql
SELECT emp_id, name FROM employees
WHERE RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 3
```
```sql
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT dept_id, emp_id, name, salary, rnk
FROM ranked
WHERE rnk <= 3
ORDER BY dept_id, rnk, emp_id
```
```sql
SELECT dept_id, emp_id, name, salary, rnk
FROM (SELECT emp_id, name, dept_id, salary,
             RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
      FROM employees)
WHERE rnk <= 3
ORDER BY dept_id, rnk, emp_id
```

Dialect text, not executed here: BigQuery, Snowflake and DuckDB accept `QUALIFY`, which filters on a window result without the wrapper. SQLite, PostgreSQL and MySQL do not have it.
```sql
SELECT dept_id, emp_id, name, salary
FROM employees
QUALIFY RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 3;
```

**pandas answer:** compute the rank as a column, then filter on it; `method="min"` matches `RANK`.
```py
emp["rnk"] = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype(int)
pd_df = emp[emp["rnk"] <= 3][["dept_id", "emp_id", "name", "salary", "rnk"]]
```

**Example:**
- Department 10 salaries: 70, 70, 60, 50, 40. `RANK` gives 1, 1, 3, 4, 5, so `rnk <= 3` keeps Ben, Dev (rank 1) and Chitra (rank 3).
- Department 20: 90, 80, 80 gives ranks 1, 2, 2: all three rows stay.
- Department 30: Ila alone, rank 1.
- 7 rows come back; Asha (rank 4) and Esha (rank 5) are filtered out.

**Code:** run with `python3 -I`.
```python
# Q3: window function in WHERE
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),(4,'Dev',10,70),
  (5,'Esha',10,40),(6,'Farid',20,90),(7,'Gita',20,80),(8,'Hari',20,80),(9,'Ila',30,55);
"""
SQL_FAIL = """
SELECT emp_id, name FROM employees
WHERE RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 3
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT dept_id, emp_id, name, salary, rnk
FROM ranked
WHERE rnk <= 3
ORDER BY dept_id, rnk, emp_id
"""
SQL_SUBQ = """
SELECT dept_id, emp_id, name, salary, rnk
FROM (SELECT emp_id, name, dept_id, salary,
             RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
      FROM employees)
WHERE rnk <= 3
ORDER BY dept_id, rnk, emp_id
"""
SQL_WHEREFIRST = """
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary < 70
)
SELECT dept_id, emp_id, name, salary, rnk FROM ranked ORDER BY dept_id, rnk, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
try:
    con.execute(SQL_FAIL).fetchall()
except sqlite3.OperationalError as e:
    print("window function in WHERE ->", type(e).__name__ + ":", e)

sql_df = pd.read_sql_query(SQL_MAIN, con)
sub_df = pd.read_sql_query(SQL_SUBQ, con)
print("\nCTE version:"); print(sql_df.to_string(index=False))
assert sql_df.equals(sub_df)

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
emp["rnk"] = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype(int)
pd_df = emp[emp["rnk"] <= 3][["dept_id", "emp_id", "name", "salary", "rnk"]]
# pd:end
# compared after sorting by dept_id, rnk, emp_id
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values(["dept_id", "rnk", "emp_id"]).reset_index(drop=True), check_dtype=False)

print("\nWHERE salary < 70 runs BEFORE the window, so ranks restart among the survivors:")
print(pd.read_sql_query(SQL_WHEREFIRST, con).to_string(index=False))
print("asserts passed: CTE == subquery == pandas rank(method='min') <= 3")
```

**Output (my run):**
```text
window function in WHERE -> OperationalError: misuse of window function RANK()

CTE version:
 dept_id  emp_id   name  salary  rnk
      10       2    Ben      70    1
      10       4    Dev      70    1
      10       3 Chitra      60    3
      20       6  Farid      90    1
      20       7   Gita      80    2
      20       8   Hari      80    2
      30       9    Ila      55    1

WHERE salary < 70 runs BEFORE the window, so ranks restart among the survivors:
 dept_id  emp_id   name  salary  rnk
      10       3 Chitra      60    1
      10       1   Asha      50    2
      10       5   Esha      40    3
      30       9    Ila      55    1
asserts passed: CTE == subquery == pandas rank(method='min') <= 3
```

**Edge cases:**
- The error: SQLite 3.45 says `misuse of window function RANK()` (see output). Message text differs by engine (not executed elsewhere).
- Order of evaluation matters for results, not just syntax. Putting a `WHERE` inside the CTE changes the ranks: with `WHERE salary < 70` first, Chitra becomes rank 1 in department 10 because the 70s were removed before ranking (last query in the output). If you want "top 3 overall, then something else", filter after.
- Ties at the cutoff: `RANK <= 3` can return more than three rows per department (Q11).
- Department with fewer than three people returns them all.

**Then explain:**
- Logical order: `FROM`, `WHERE`, `GROUP BY`, `HAVING`, window functions, `SELECT` list, `DISTINCT`, `ORDER BY`, `LIMIT`. The window value does not exist yet when `WHERE` runs.
- Window functions are allowed only in the `SELECT` list and `ORDER BY` (SQLite docs, and the PostgreSQL tutorial says the same for PostgreSQL).
- The CTE and the subquery give the same result here; pick the readable one. Whether an engine rewrites them identically is not something I measured.
- `QUALIFY` is just sugar for that wrapper, so the CTE form is the portable answer.

**Follow-ups:**
- *Can I put the rank in `HAVING`?* No, `HAVING` runs before windows too.
- *Can I use the alias `rnk` in the same SELECT's `WHERE`?* No, for the same reason (aliases come after windows).
- *What if I only want the top row per group?* Use `ROW_NUMBER() = 1` or `RANK() = 1` in the same wrapper (Q4, Q7).

**Common mistakes:**
- Writing `WHERE rnk <= 3` against an alias in the same query.
- Filtering with `WHERE` before ranking and not realising ranks are computed on the survivors.
- Saying `QUALIFY` works "in SQL"; it is not in SQLite, PostgreSQL or MySQL.

### Q4 ⭐⭐⭐ 🟢 Top 3 salaries per department as rows: employees(emp_id, name, dept_id, salary). Return the three highest-paid employees in each department using ROW_NUMBER with a unique tie-breaker (emp_id) inside a CTE, ordered by department then rank. Explain why ROW_NUMBER always gives exactly 3 rows per department (when available) and why the tie-breaker makes it deterministic, and give the pandas sort_values plus groupby().head(3) and the groupby().cumcount() versions.
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Number each department's rows with `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id)` in a CTE and keep `rn <= 3`; because `ROW_NUMBER` never repeats a number, you get exactly three rows per department when that many exist, and the `emp_id` tie-breaker makes the choice among equal salaries repeatable.

**Schema and sample data:** twelve employees. Department 10 has three people tied at 70 plus two lower salaries; department 20 has only two salaries and a NULL; department 30 has four people all at 55.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),(4,'Dev',10,70),
  (5,'Esha',10,70),(6,'Farid',20,90),(7,'Gita',20,80),(8,'Hari',20,NULL),
  (9,'Ila',30,55),(10,'Jay',30,55),(11,'Kiran',30,55),(12,'Lata',30,55);
```

**SQL answer:** tie-break rule I state: among equal salaries, the lower `emp_id` comes first.
```sql
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT dept_id, emp_id, name, salary, rn
FROM ranked
WHERE rn <= 3
ORDER BY dept_id, rn
```

**pandas answer:** sort by department, salary descending, emp_id ascending, then either `groupby().head(3)` or `groupby().cumcount()`; `cumcount` starts at 0, so add 1 to match `ROW_NUMBER`.
```py
ordered = emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = ordered.groupby("dept_id").head(3)
```
```py
ordered = ordered.assign(rn=ordered.groupby("dept_id").cumcount() + 1)
pd_cum = ordered[ordered["rn"] <= 3][["dept_id", "emp_id", "name", "salary", "rn"]]
```

**Example:**
- Dept 10: sorted by salary DESC then emp_id: Ben (70, id 2), Dev (70, id 4), Esha (70, id 5), Chitra (60), Asha (50). Top three: Ben, Dev, Esha. Chitra at 60 is out even though she is the next-best, because three people tie at 70 and `ROW_NUMBER` hands out 1, 2, 3 to them.
- Dept 20: Farid 90, Gita 80, Hari NULL. Only three rows exist and NULL sorts last in descending order in both SQLite and pandas, so Hari is returned as number 3 with a NULL salary.
- Dept 30: four people at 55 (Ila 9, Jay 10, Kiran 11, Lata 12). The tie-breaker keeps Ila, Jay, Kiran and drops Lata.
- Nine rows total, three per department.

**Code:** run with `python3 -I`.
```python
# Q4: top 3 per department with ROW_NUMBER and a unique tie-breaker
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),(4,'Dev',10,70),
  (5,'Esha',10,70),(6,'Farid',20,90),(7,'Gita',20,80),(8,'Hari',20,NULL),
  (9,'Ila',30,55),(10,'Jay',30,55),(11,'Kiran',30,55),(12,'Lata',30,55);
"""
# tie-break stated: lower emp_id first among equal salaries
SQL_MAIN = """
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT dept_id, emp_id, name, salary, rn
FROM ranked
WHERE rn <= 3
ORDER BY dept_id, rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:head
ordered = emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = ordered.groupby("dept_id").head(3)
# pd:end
# pd:cum
ordered = ordered.assign(rn=ordered.groupby("dept_id").cumcount() + 1)
pd_cum = ordered[ordered["rn"] <= 3][["dept_id", "emp_id", "name", "salary", "rn"]]
# pd:end
print("\ncumcount() starts at 0, so rn = cumcount()+1:",
      ordered.groupby("dept_id").cumcount().tolist())
# compared after sorting by dept_id, rn (head keeps the sorted order but has no rn column)
pd.testing.assert_frame_equal(sql_df, pd_cum.reset_index(drop=True), check_dtype=False)
assert pd_head["emp_id"].tolist() == sql_df["emp_id"].tolist()
print("rows per department:", sql_df.groupby("dept_id").size().to_dict())
print("asserts passed: SQL == head(3) emp_ids == cumcount version")
```

**Output (my run):**
```text
 dept_id  emp_id  name  salary  rn
      10       2   Ben    70.0   1
      10       4   Dev    70.0   2
      10       5  Esha    70.0   3
      20       6 Farid    90.0   1
      20       7  Gita    80.0   2
      20       8  Hari     NaN   3
      30       9   Ila    55.0   1
      30      10   Jay    55.0   2
      30      11 Kiran    55.0   3

cumcount() starts at 0, so rn = cumcount()+1: [0, 1, 2, 3, 4, 0, 1, 2, 0, 1, 2, 3]
rows per department: {10: 3, 20: 3, 30: 3}
asserts passed: SQL == head(3) emp_ids == cumcount version
```

**Edge cases:**
- Fewer than three rows in a department: you get what exists. With the NULL salary here, department 20 filled its third slot with a NULL-salary employee; add `WHERE salary IS NOT NULL` inside the CTE (and `dropna` in pandas) if that is unwanted.
- Ties at the cutoff are cut arbitrarily by `ROW_NUMBER`; the `emp_id` rule makes it a rule instead of luck. If the business wants every tied person, use `RANK` (Q11).
- The `cumcount` list in the output starts at 0 in every group (dept 10 has 0 to 4); that is why it needs `+ 1`.
- `groupby().head(3)` keeps the original index labels and has no rank column; the cumcount version gives you `rn`.

**Then explain:**
- `ROW_NUMBER` assigns a distinct integer to each row of the partition in `ORDER BY` order, so `rn <= 3` returns at most three rows per partition.
- Without `emp_id`, rows tied on salary can be numbered in any order, so which three come back can change between runs or engines (the standard leaves it open; PostgreSQL's tutorial says tied rows are numbered in unspecified order).
- The window cannot be in `WHERE`, so the CTE wrapper is needed (Q3).
- pandas: sort once with all the keys, then `head(3)` per group is the shortest form; `cumcount()` is the version that also gives you the number.

**Follow-ups:**
- *Top 3 including ties?* `RANK() <= 3` (Q11).
- *Top 3 salary levels?* `DENSE_RANK() <= 3` (Q8).
- *Need the output ordered?* Add the outer `ORDER BY` as I did; the order inside `OVER` does not order the result.

**Common mistakes:**
- Leaving out the unique tie-breaker and calling the result deterministic.
- Forgetting that `cumcount` starts at 0.
- Calling `groupby().head(3)` on an unsorted frame (it takes the first three rows as they come).

### Q5 ⭐⭐⭐ 🟢 Second highest salary (LeetCode 176 style): employees(emp_id, name, salary) with duplicate salaries, and the case where there is only one distinct salary. Return the second highest distinct salary, NULL when it does not exist, using DENSE_RANK in a CTE and wrapped so an empty result becomes NULL. Explain why ROW_NUMBER or RANK = 2 gives the wrong answer when the top salary is tied, and give the pandas unique/nlargest version returning NaN or None when absent.
**Asked at:** public LeetCode-style problem bank (176 Second Highest Salary, 177 Nth Highest Salary, 184 Department Highest Salary, 185 Department Top Three Salaries; known only from third-party list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Rank the distinct salaries with `DENSE_RANK() OVER (ORDER BY salary DESC)` in a CTE and take `MAX(salary)` where the rank is 2; the `MAX` wrapper returns NULL when no rank-2 row exists, and `ROW_NUMBER` or `RANK = 2` fail when the top salary is tied.

**Schema and sample data:** the same table shape, four different contents (each run in its own in-memory database).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
-- A tied top:      100, 100, 90, 80
-- B one distinct:  50, 50
-- C empty table
-- D with a NULL:   NULL, 70, 70, 40
```
The exact rows are in the Code block.

**SQL answer:** `SQL_MAIN` is the answer; `SQL_RANK2` and `SQL_ROWNUM2` are the wrong versions for comparison.
```sql
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS second_highest FROM ranked WHERE rnk = 2
```
```sql
WITH ranked AS (SELECT salary, RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees WHERE salary IS NOT NULL)
SELECT MAX(salary) FROM ranked WHERE rnk = 2
```
```sql
WITH ranked AS (SELECT salary, ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn FROM employees WHERE salary IS NOT NULL)
SELECT MAX(salary) FROM ranked WHERE rn = 2
```

**pandas answer:** drop NaN, drop duplicates, take the two largest, return the second or `None`.
```py
def second_highest(s):
    top2 = s.dropna().drop_duplicates().nlargest(2)
    return int(top2.iloc[1]) if len(top2) == 2 else None
```

**Example:**
- A (100, 100, 90, 80): distinct levels are 100, 90, 80, so DENSE_RANK gives 1, 1, 2, 3 and the second highest is 90. `RANK` gives 1, 1, 3, 4: no row has rank 2, so it returns NULL, which is wrong. `ROW_NUMBER` gives 1, 2, 3, 4: the second row is the other 100, wrong.
- B (50, 50): only one distinct salary, so there is no second highest. DENSE_RANK has no rank 2, so `MAX` of nothing is NULL. `ROW_NUMBER = 2` returns 50, wrong.
- C: empty table, NULL.
- D: the NULL is filtered out, salaries 70, 70, 40 give levels 70 and 40, so the answer is 40.

**Code:** run with `python3 -I`.
```python
# Q5: second highest distinct salary (LeetCode 176 style)
import sqlite3
import pandas as pd

DATASETS = {
    "A tied top":      [(1, "Asha", 100), (2, "Ben", 100), (3, "Chitra", 90), (4, "Dev", 80)],
    "B one distinct":  [(1, "Asha", 50), (2, "Ben", 50)],
    "C empty":         [],
    "D NULLs":         [(1, "Asha", None), (2, "Ben", 70), (3, "Chitra", 70), (4, "Dev", 40)],
}
SQL_MAIN = """
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS second_highest FROM ranked WHERE rnk = 2
"""
SQL_RANK2 = """
WITH ranked AS (SELECT salary, RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees WHERE salary IS NOT NULL)
SELECT MAX(salary) FROM ranked WHERE rnk = 2
"""
SQL_ROWNUM2 = """
WITH ranked AS (SELECT salary, ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn FROM employees WHERE salary IS NOT NULL)
SELECT MAX(salary) FROM ranked WHERE rn = 2
"""

# pd:main
def second_highest(s):
    top2 = s.dropna().drop_duplicates().nlargest(2)
    return int(top2.iloc[1]) if len(top2) == 2 else None
# pd:end

print("dataset          | DENSE_RANK | RANK=2 | ROW_NUMBER=2 | pandas")
for name, rows in DATASETS.items():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)")
    con.executemany("INSERT INTO employees VALUES (?,?,?)", rows)
    a = con.execute(SQL_MAIN).fetchone()[0]
    b = con.execute(SQL_RANK2).fetchone()[0]
    c = con.execute(SQL_ROWNUM2).fetchone()[0]
    emp = pd.DataFrame(rows, columns=["emp_id", "name", "salary"]).astype({"salary": "float"})
    p = second_highest(emp["salary"])
    print("%-16s | %-10s | %-6s | %-12s | %s" % (name, a, b, c, p))
    assert a == p, (name, a, p)
print("asserts passed: DENSE_RANK wrapper == pandas on all four datasets (None means NULL)")
```

**Output (my run):**
```text
dataset          | DENSE_RANK | RANK=2 | ROW_NUMBER=2 | pandas
A tied top       | 90         | None   | 100          | 90
B one distinct   | None       | None   | 50           | None
C empty          | None       | None   | None         | None
D NULLs          | 40         | None   | 70           | 40
asserts passed: DENSE_RANK wrapper == pandas on all four datasets (None means NULL)
```

**Edge cases:**
- Fewer than two distinct values: NULL in SQL, `None` in pandas (the assert compares them).
- NULL salaries: filtered with `WHERE salary IS NOT NULL`, otherwise NULL would take a rank of its own (NULL sorts as smallest in SQLite).
- Why `MAX`: an aggregate over zero rows returns one row containing NULL, so the caller always gets exactly one row. A bare `SELECT salary ... WHERE rnk = 2` would return zero rows, or two identical rows when the second level is tied.
- A pandas surprise I hit: on the empty dataset the salary column had dtype object, and `nlargest` raised `TypeError: Cannot use method 'nlargest' with dtype object`. I cast the column to float in the script; real data from `read_sql_query` with no rows can do the same.
- `nlargest(2)` alone would return duplicates (100, 100), so `drop_duplicates()` first.

**Then explain:**
- You want the second highest value, not the second row, so rank values: `DENSE_RANK`.
- `RANK` skips numbers after a tie, so rank 2 can be missing. `ROW_NUMBER` counts rows, so it counts duplicates as separate positions.
- The `LIMIT 1 OFFSET 1` plus `DISTINCT` version works too (Part 3 Q15); the window version generalises to Nth and to per-group (Q6, Q46).
- I only know LeetCode 176's wording from third-party snippets; the behaviour above is what I ran.

**Follow-ups:**
- *Generalise to Nth?* Parameterise the rank (Q6).
- *Second highest per department?* Add `PARTITION BY dept_id` and group the result (Q46).
- *Without window functions?* `MAX(salary) WHERE salary < (SELECT MAX(salary) ...)`; it returns NULL naturally when absent.

**Common mistakes:**
- `RANK = 2` or `ROW_NUMBER = 2`.
- Returning no row instead of NULL.
- Forgetting `drop_duplicates` before `nlargest`.

### Q6 ⭐⭐⭐ 🟡 Nth highest salary (LeetCode 177 style): employees(emp_id, name, salary) with ties and fewer than N distinct values for large N. Return the Nth highest distinct salary using DENSE_RANK with N passed as a parameter (Python sqlite3 parameter, since SQLite has no stored functions), NULL when absent. Explain the DISTINCT-ranking logic (rank values, not rows), why DENSE_RANK matches 'Nth highest', how the OFFSET version in Part 3 compares, and give the pandas version.
**Asked at:** public LeetCode-style problem bank (176 Second Highest Salary, 177 Nth Highest Salary, 184 Department Highest Salary, 185 Department Top Three Salaries; known only from third-party list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Rank the distinct non-NULL salaries with `DENSE_RANK() OVER (ORDER BY salary DESC)`, bind N as a `?` parameter, and return `MAX(salary)` where `rnk = ?`; when N is bigger than the number of distinct values the `MAX` gives NULL.

**Schema and sample data:** seven employees, four distinct salaries (100, 90, 80, 70) and one NULL.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',100),(2,'Ben',100),(3,'Chitra',90),(4,'Dev',80),
  (5,'Esha',80),(6,'Farid',70),(7,'Gita',NULL);
```

**SQL answer:** SQLite has no stored functions, so N goes in as a parameter from Python (`con.execute(SQL, (n,))`). `SQL_OFFSET` is the Part 3 style comparison.
```sql
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS nth_salary FROM ranked WHERE rnk = ?
```
```sql
SELECT (SELECT DISTINCT salary FROM employees WHERE salary IS NOT NULL
        ORDER BY salary DESC LIMIT 1 OFFSET ? - 1) AS nth_salary
```

**pandas answer:** unique descending values, with an explicit range guard.
```py
def nth_highest(s, n):
    u = s.dropna().drop_duplicates().sort_values(ascending=False)
    return int(u.iloc[n - 1]) if 1 <= n <= len(u) else None
```

**Example:** distinct values descending: 100, 90, 80, 70.
- N = 1 gives 100, N = 2 gives 90 (the duplicate 100 does not take a place), N = 3 gives 80, N = 4 gives 70.
- N = 5 and N = 10: there are only four levels, so no rank-5 row exists, so NULL.
- N = 0: no row has rank 0, so NULL from the window version.

**Code:** run with `python3 -I`.
```python
# Q6: Nth highest distinct salary with N as a parameter
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',100),(2,'Ben',100),(3,'Chitra',90),(4,'Dev',80),
  (5,'Esha',80),(6,'Farid',70),(7,'Gita',NULL);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS nth_salary FROM ranked WHERE rnk = ?
"""
SQL_OFFSET = """
SELECT (SELECT DISTINCT salary FROM employees WHERE salary IS NOT NULL
        ORDER BY salary DESC LIMIT 1 OFFSET ? - 1) AS nth_salary
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
def nth_highest(s, n):
    u = s.dropna().drop_duplicates().sort_values(ascending=False)
    return int(u.iloc[n - 1]) if 1 <= n <= len(u) else None
# pd:end

print("N | DENSE_RANK | LIMIT/OFFSET | pandas")
for n in [0, 1, 2, 3, 4, 5, 10]:
    a = con.execute(SQL_MAIN, (n,)).fetchone()[0]
    b = con.execute(SQL_OFFSET, (n,)).fetchone()[0]
    p = nth_highest(emp["salary"], n)
    print("%d | %-10s | %-12s | %s" % (n, a, b, p))
    assert a == p
    if n >= 1:
        assert b == p
print("distinct values:", sorted(emp["salary"].dropna().unique().tolist(), reverse=True))
print("without the 1 <= n guard pandas iloc[-1] would return:", int(emp["salary"].dropna().drop_duplicates().sort_values(ascending=False).iloc[0 - 1]))
print("asserts passed: DENSE_RANK == pandas for N = 0..10; OFFSET version == for N >= 1")
```

**Output (my run):**
```text
N | DENSE_RANK | LIMIT/OFFSET | pandas
0 | None       | 100          | None
1 | 100        | 100          | 100
2 | 90         | 90           | 90
3 | 80         | 80           | 80
4 | 70         | 70           | 70
5 | None       | None         | None
10 | None       | None         | None
distinct values: [100.0, 90.0, 80.0, 70.0]
without the 1 <= n guard pandas iloc[-1] would return: 70
asserts passed: DENSE_RANK == pandas for N = 0..10; OFFSET version == for N >= 1
```

**Edge cases:**
- N = 0: the window version returns NULL, but the `OFFSET ? - 1` version computes `OFFSET -1`, which SQLite treats as 0, so it returned 100 (the highest) silently (output, N = 0 row). Same trap as in Part 3 Q15. Other engines reportedly reject a negative OFFSET (not executed here). Validate N >= 1 in the caller.
- pandas: `u.iloc[n - 1]` with `n = 0` is `iloc[-1]`, the smallest value (70 here, printed below the table). Hence the `1 <= n <= len(u)` guard.
- Ties: rows with equal salary share one level; `DISTINCT`/`DENSE_RANK` both count levels.
- NULL salaries: excluded by the filter.
- Duplicates and fewer-than-N values behave as above.

**Then explain:**
- "Nth highest" means the Nth distinct value, so I rank values, not rows. `DENSE_RANK` numbers distinct levels 1, 2, 3 without gaps, so `rnk = N` is exactly that level.
- `RANK` has gaps after ties and `ROW_NUMBER` counts duplicates, so both can miss or misplace the Nth level (Q5).
- Compare the OFFSET version in Part 3: `SELECT DISTINCT salary ... LIMIT 1 OFFSET N-1` gives the same answers for N >= 1 here, but it has the N = 0 trap and is not per-group. The window form extends to `PARTITION BY`.
- Both versions sort the salaries; I did not time them on large data.

**Follow-ups:**
- *Nth highest per department?* Partition and group (Q46).
- *Without a parameter?* A view or CTE with a literal; in engines with functions (PostgreSQL, MySQL) the LeetCode answer is often a function (not executed here).
- *Why return NULL?* The caller can tell "no such level" from an error.

**Common mistakes:**
- Using `ROW_NUMBER` or `RANK` and getting wrong values with ties.
- Not guarding N <= 0.
- Using OFFSET N instead of N-1.

### Q7 ⭐⭐⭐ 🟡 Department Highest Salary (LeetCode 184 style): employees(emp_id, name, salary, dept_id) and departments(dept_id, dept_name), with ties for the top salary in some departments. Return department name, employee name and salary for every employee earning the department's maximum. Solve with RANK() = 1 (or MAX(salary) OVER (PARTITION BY dept_id)), join to departments, explain why a tie returns all tied employees, why ROW_NUMBER = 1 would lose people, and give the pandas transform('max') mask plus merge.
**Asked at:** public LeetCode-style problem bank (176 Second Highest Salary, 177 Nth Highest Salary, 184 Department Highest Salary, 185 Department Top Three Salaries; known only from third-party list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Use `RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) = 1` in a CTE (or `salary = MAX(salary) OVER (PARTITION BY dept_id)`), join to `departments`, and every employee tied at the department maximum comes back; `ROW_NUMBER() = 1` returns only one of them.

**Schema and sample data:** IT has a tie at 90 (Max and Randy); Sales has Henry 80, Sam 60 and Tia with a NULL salary; HR has no employees; Zed has a NULL department.
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'Sales'),(3,'HR');
INSERT INTO employees VALUES (1,'Joe',70,1),(2,'Max',90,1),(3,'Randy',90,1),(4,'Henry',80,2),
  (5,'Sam',60,2),(6,'Tia',NULL,2),(7,'Zed',99,NULL);
```

**SQL answer:**
```sql
WITH ranked AS (
  SELECT name, salary, dept_id,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r
JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rnk = 1
ORDER BY d.dept_name, r.name
```
Alternative with `MAX() OVER`:
```sql
WITH m AS (
  SELECT name, salary, dept_id,
         MAX(salary) OVER (PARTITION BY dept_id) AS dept_max
  FROM employees
)
SELECT d.dept_name AS department, m.name AS employee, m.salary
FROM m
JOIN departments d ON d.dept_id = m.dept_id
WHERE m.salary = m.dept_max
ORDER BY d.dept_name, m.name
```
The `ROW_NUMBER` version, to show what goes wrong (tie rule: lower emp_id):
```sql
WITH ranked AS (
  SELECT name, salary, dept_id,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rn = 1
ORDER BY d.dept_name, r.name
```

**pandas answer:** compare each salary to its group's `transform("max")`, then merge to the department names.
```py
top = emp[emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")]
pd_df = (top.merge(dept, on="dept_id")
            .rename(columns={"dept_name": "department", "name": "employee"})
            [["department", "employee", "salary"]])
```

**Example:**
- IT: max is 90, held by Max and Randy. Both are returned (Joe at 70 is not).
- Sales: Henry 80 is the max. Sam is lower; Tia's NULL salary is never equal to 80.
- HR: no employees, so with an inner join it does not appear.
- Zed (99, NULL department): his partition is the NULL group, ranks first inside it, but the join to `departments` finds no match (`NULL = dept_id` is not true), so he is dropped.
- `ROW_NUMBER() = 1` returns Max for IT only, losing Randy: it hands out 1 to exactly one row per department.

**Code:** run with `python3 -I`.
```python
# Q7: Department Highest Salary (LeetCode 184 style)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'Sales'),(3,'HR');
INSERT INTO employees VALUES (1,'Joe',70,1),(2,'Max',90,1),(3,'Randy',90,1),(4,'Henry',80,2),
  (5,'Sam',60,2),(6,'Tia',NULL,2),(7,'Zed',99,NULL);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT name, salary, dept_id,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r
JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rnk = 1
ORDER BY d.dept_name, r.name
"""
SQL_MAX = """
WITH m AS (
  SELECT name, salary, dept_id,
         MAX(salary) OVER (PARTITION BY dept_id) AS dept_max
  FROM employees
)
SELECT d.dept_name AS department, m.name AS employee, m.salary
FROM m
JOIN departments d ON d.dept_id = m.dept_id
WHERE m.salary = m.dept_max
ORDER BY d.dept_name, m.name
"""
SQL_ROWNUM = """
WITH ranked AS (
  SELECT name, salary, dept_id,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rn = 1
ORDER BY d.dept_name, r.name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
max_df = pd.read_sql_query(SQL_MAX, con)
rn_df = pd.read_sql_query(SQL_ROWNUM, con)
print("RANK() = 1:"); print(sql_df.to_string(index=False))
print("\nROW_NUMBER() = 1 (loses the tied employee):"); print(rn_df.to_string(index=False))
assert sql_df.equals(max_df)

emp = pd.read_sql_query("SELECT * FROM employees", con)
dept = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
top = emp[emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")]
pd_df = (top.merge(dept, on="dept_id")
            .rename(columns={"dept_name": "department", "name": "employee"})
            [["department", "employee", "salary"]])
# pd:end
# compared after sorting by department, employee
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values(["department", "employee"]).reset_index(drop=True), check_dtype=False)
assert len(rn_df) < len(sql_df)
print("\nasserts passed: RANK=1 == MAX() OVER == pandas transform('max') + merge; ROW_NUMBER=1 returns fewer rows")
```

**Output (my run):**
```text
RANK() = 1:
department employee  salary
        IT      Max      90
        IT    Randy      90
     Sales    Henry      80

ROW_NUMBER() = 1 (loses the tied employee):
department employee  salary
        IT      Max      90
     Sales    Henry      80

asserts passed: RANK=1 == MAX() OVER == pandas transform('max') + merge; ROW_NUMBER=1 returns fewer rows
```

**Edge cases:**
- Ties: all tied rows are returned (that is the point).
- All-NULL department: `MAX(salary) OVER` is NULL and `salary = NULL` is never true, so nobody is returned; by the NULL-peers rule `RANK` should rank the NULLs together as 1 and return them with NULL salary, so the two forms would differ on that edge (reasoned, not run: this data has no all-NULL department). Filter `salary IS NOT NULL` if it matters.
- Department with no employees: absent from an inner join; a `LEFT JOIN` from `departments` would show it with NULLs.
- NULL department: dropped by the join; pandas `groupby` drops the NaN key too, so `transform` gives NaN and the mask is False.

**Then explain:**
- `RANK` gives equal salaries the same rank, so rank 1 can be several rows. That is the correct answer to "everyone earning the max".
- `ROW_NUMBER = 1` is right only when you want exactly one row per department, with a stated tie rule (Q4, Q45).
- `MAX() OVER` reads more directly ("salary equals the department max") and has no rank to think about.
- I know the LeetCode 184 statement only from list snippets; the behaviour above is from my run.

**Follow-ups:**
- *One row per department even with ties?* `ROW_NUMBER` with a tie-breaker.
- *Top two salaries per department?* `DENSE_RANK <= 2` or `RANK <= 2` (Q8, Q11).
- *Without window functions?* A join to `SELECT dept_id, MAX(salary) ... GROUP BY dept_id` on dept and salary.

**Common mistakes:**
- `ROW_NUMBER() = 1` when ties must be kept.
- Using an inner join and not noticing the NULL-department or empty departments dropped.
- In pandas, `idxmax` per group, which returns only the first tied row (Q17, Q34).

### Q8 ⭐⭐⭐ 🟡 Department Top Three Salaries (LeetCode 185 style): employees(emp_id, name, salary, dept_id) and departments(dept_id, dept_name). A high earner is one whose salary is among the top three distinct salaries in their department. Return department, employee and salary using DENSE_RANK() <= 3 in a CTE, with ties included (so more than three employees can appear). Explain why DENSE_RANK and not RANK or ROW_NUMBER, how departments with fewer than three salaries behave, and give the pandas groupby rank(method='dense', ascending=False) version.
**Asked at:** public LeetCode-style problem bank (176 Second Highest Salary, 177 Nth Highest Salary, 184 Department Highest Salary, 185 Department Top Three Salaries; known only from third-party list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Filter out NULL salaries, compute `DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)` in a CTE, keep `rnk <= 3`, and join to `departments`; `DENSE_RANK` counts distinct salary levels, so ties are all included and a department can return more than three people.

**Schema and sample data:** IT has levels 90, 85 (three people tied), 69 and 60; Sales has two salaries plus a NULL; HR has no employees.
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'Sales'),(3,'HR');
INSERT INTO employees VALUES (1,'Joe',85,1),(2,'Henry',80,2),(3,'Sam',60,2),(4,'Max',90,1),
  (5,'Janet',69,1),(6,'Randy',85,1),(7,'Will',85,1),(8,'Tia',NULL,2),(9,'Ravi',60,1);
```

**SQL answer:**
```sql
WITH ranked AS (
  SELECT name, salary, dept_id,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r
JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rnk <= 3
ORDER BY d.dept_name, r.salary DESC, r.name
```
The Code block also builds `RANK` and `ROW_NUMBER` variants of the same filter by string substitution, to compare counts.

**pandas answer:** dense rank within each department, descending, then filter and merge.
```py
emp["rnk"] = emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
top = emp[emp["rnk"] <= 3]
pd_df = (top.merge(dept, on="dept_id")
            .rename(columns={"dept_name": "department", "name": "employee"})
            [["department", "employee", "salary"]])
```

**Example:**
- IT salary levels descending: 90 (Max), 85 (Joe, Randy, Will), 69 (Janet), 60 (Ravi). Top three levels are 90, 85, 69, so five people: Max, Joe, Randy, Will, Janet. Ravi (level 4) is out.
- Sales: levels 80 and 60 only, so both Henry and Sam are returned (fewer than three levels means everyone is included).
- HR: no employees, no rows.
- Compare: `RANK <= 3` gives IT ranks 1, 2, 2, 2, 5: Max, Joe, Randy, Will and not Janet (6 rows overall). `ROW_NUMBER <= 3` gives only three IT people (5 rows overall). Only `DENSE_RANK` returns the five who hold one of the top three salary levels.

**Code:** run with `python3 -I`.
```python
# Q8: Department Top Three Salaries (LeetCode 185 style)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'Sales'),(3,'HR');
INSERT INTO employees VALUES (1,'Joe',85,1),(2,'Henry',80,2),(3,'Sam',60,2),(4,'Max',90,1),
  (5,'Janet',69,1),(6,'Randy',85,1),(7,'Will',85,1),(8,'Tia',NULL,2),(9,'Ravi',60,1);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT name, salary, dept_id,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r
JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rnk <= 3
ORDER BY d.dept_name, r.salary DESC, r.name
"""
def variant(fn, where="", order="salary DESC"):
    return f"""
WITH ranked AS (SELECT name, salary, dept_id, {fn} OVER (PARTITION BY dept_id ORDER BY {order}) AS k
                FROM employees {where})
SELECT d.dept_name, r.name FROM ranked r JOIN departments d ON d.dept_id = r.dept_id WHERE r.k <= 3
ORDER BY d.dept_name, r.name"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("DENSE_RANK <= 3 (NULL salary filtered):"); print(sql_df.to_string(index=False))
for fn, order in [("RANK()", "salary DESC"), ("ROW_NUMBER()", "salary DESC, emp_id")]:
    r = con.execute(variant(fn, "WHERE salary IS NOT NULL", order)).fetchall()
    print("%-13s <= 3 returns %d rows; IT rows: %s" % (fn, len(r), [n for d, n in r if d == "IT"]))
nofilter = con.execute(variant("DENSE_RANK()")).fetchall()
print("DENSE_RANK without the IS NOT NULL filter, Sales rows:", [n for d, n in nofilter if d == "Sales"])

emp = pd.read_sql_query("SELECT * FROM employees", con)
dept = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
emp["rnk"] = emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
top = emp[emp["rnk"] <= 3]
pd_df = (top.merge(dept, on="dept_id")
            .rename(columns={"dept_name": "department", "name": "employee"})
            [["department", "employee", "salary"]])
# pd:end
# compared after sorting by department, salary desc, employee
pd.testing.assert_frame_equal(
    sql_df,
    pd_df.sort_values(["department", "salary", "employee"], ascending=[True, False, True]).reset_index(drop=True),
    check_dtype=False)
print("\nasserts passed: SQL DENSE_RANK <= 3 (non-NULL salaries) == pandas groupby rank(method='dense')")
```

**Output (my run):**
```text
DENSE_RANK <= 3 (NULL salary filtered):
department employee  salary
        IT      Max      90
        IT      Joe      85
        IT    Randy      85
        IT     Will      85
        IT    Janet      69
     Sales    Henry      80
     Sales      Sam      60
RANK()        <= 3 returns 6 rows; IT rows: ['Joe', 'Max', 'Randy', 'Will']
ROW_NUMBER()  <= 3 returns 5 rows; IT rows: ['Joe', 'Max', 'Randy']
DENSE_RANK without the IS NOT NULL filter, Sales rows: ['Henry', 'Sam', 'Tia']

asserts passed: SQL DENSE_RANK <= 3 (non-NULL salaries) == pandas groupby rank(method='dense')
```

**Edge cases:**
- NULL salary (Tia in Sales): without `WHERE salary IS NOT NULL` SQLite ranks NULL as the smallest value, so in a department with fewer than three levels it gets a rank and is returned with a NULL salary (output line "without the IS NOT NULL filter" shows Tia). pandas `rank` gives NaN and `NaN <= 3` is False, so pandas would drop her. A real SQL/pandas difference; the filter makes them agree.
- Department with fewer than three salary levels: all employees returned.
- Department with no employees: not in the output (inner join).
- Ties: all tied employees stay, so more than three rows per department is correct here.

**Then explain:**
- "Top three salaries" here means top three distinct amounts, so rank levels: `DENSE_RANK`. `RANK` skips (1, 2, 2, 2, 5) and would cut Janet; `ROW_NUMBER` would pick arbitrary people among the 85 tie.
- The window cannot sit in `WHERE`, hence the CTE (Q3).
- pandas `rank(method="dense", ascending=False)` does the same inside `groupby`; it returns floats.
- I know the LeetCode 185 wording only from snippets; the definition I used is the one stated in the question.

**Follow-ups:**
- *Exactly three people per department?* `ROW_NUMBER` with a tie-breaker (Q4).
- *Include departments with no employees?* `LEFT JOIN` from `departments`; the NULL employee row would need a decision.
- *Why not `LIMIT`?* `LIMIT` applies to the whole result, not per group.

**Common mistakes:**
- Using `RANK` or `ROW_NUMBER` for "top three salaries".
- Forgetting to filter NULL salaries and returning a NULL earner.
- Joining the departments table first and ranking after (fine for results, but a join fan-out can change ranks, Q48).

### Q9 ⭐⭐⭐ 🟡 Deduplicate keeping the latest row per key: customer_updates(update_id, customer_id, email, updated_at) holds several versions per customer, and two rows for one customer may share the same updated_at. Return one row per customer, the latest by updated_at, with update_id DESC as the tie-breaker, using ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC, update_id DESC) = 1. Explain why the tie-breaker is needed for repeatable results, how to keep the first row instead, and give the pandas sort_values plus drop_duplicates(subset=..., keep='first') version.
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Number each customer's rows with `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC, update_id DESC)` and keep `rn = 1`; the `update_id` tie-breaker makes the winner among rows sharing `updated_at` a fixed rule, and flipping the order direction (ASC) keeps the first row instead.

**Schema and sample data:** nine update rows for five customers. Customer 1 has two rows on the same date (update 2 and 3); customer 4 has a NULL date row and a dated row; customer 5 has only a NULL date.
```sql
CREATE TABLE customer_updates(update_id INTEGER PRIMARY KEY, customer_id INTEGER, email TEXT, updated_at TEXT);
INSERT INTO customer_updates VALUES
 (1,1,'a@x.com','2026-01-01'),(2,1,'a2@x.com','2026-02-01'),(3,1,'a3@x.com','2026-02-01'),
 (4,2,'b@x.com','2026-01-15'),(5,3,'c@x.com','2026-03-05'),(6,3,'c0@x.com','2026-01-01'),
 (7,4,'d@x.com',NULL),(8,4,'d2@x.com','2026-01-10'),(9,5,'e@x.com',NULL);
```

**SQL answer:** tie rule: later `update_id` wins. `SQL_FIRST` flips both keys to ASC for "keep the first row". `SQL_NOTIE` drops the tie-breaker.
```sql
WITH ranked AS (
  SELECT update_id, customer_id, email, updated_at,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY updated_at DESC, update_id DESC) AS rn
  FROM customer_updates
)
SELECT update_id, customer_id, email, updated_at
FROM ranked
WHERE rn = 1
ORDER BY customer_id
```
```sql
WITH ranked AS (
  SELECT update_id, customer_id, email, updated_at,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY updated_at ASC, update_id ASC) AS rn
  FROM customer_updates
)
SELECT update_id, customer_id, email, updated_at FROM ranked WHERE rn = 1 ORDER BY customer_id
```
```sql
WITH ranked AS (
  SELECT update_id, customer_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM customer_updates)
SELECT update_id FROM ranked WHERE rn = 1 AND customer_id = 1
```

**pandas answer:** sort by the same keys, then keep the first row per customer.
```py
pd_df = (cu.sort_values(["updated_at", "update_id"], ascending=[False, False])
           .drop_duplicates(subset="customer_id", keep="first"))
```
```py
pd_first = (cu.sort_values(["updated_at", "update_id"], ascending=[True, True])
              .drop_duplicates(subset="customer_id", keep="first"))
```

**Example:**
- Customer 1: updates 2 and 3 share 2026-02-01, the latest date. `update_id DESC` puts 3 first, so update 3 (a3@x.com) wins. Update 1 is older.
- Customer 2 has one row, kept. Customer 3: 2026-03-05 beats 2026-01-01, so update 5.
- Customer 4: NULL date sorts last in a DESC order (in SQLite and in pandas), so the dated update 8 wins.
- Customer 5 only has a NULL-date row, so that row is still returned (update 9).
- Keep-first (ASC): customer 1 gives update 1, customer 3 gives update 6.

**Code:** run with `python3 -I`.
```python
# Q9: keep the latest row per key, with a tie-breaker
import sqlite3
import pandas as pd

ROWS = [(1,1,'a@x.com','2026-01-01'),(2,1,'a2@x.com','2026-02-01'),(3,1,'a3@x.com','2026-02-01'),
        (4,2,'b@x.com','2026-01-15'),(5,3,'c@x.com','2026-03-05'),(6,3,'c0@x.com','2026-01-01'),
        (7,4,'d@x.com',None),(8,4,'d2@x.com','2026-01-10'),(9,5,'e@x.com',None)]
SCHEMA = "CREATE TABLE customer_updates(update_id INTEGER PRIMARY KEY, customer_id INTEGER, email TEXT, updated_at TEXT);"
# latest updated_at wins; update_id DESC breaks ties
SQL_MAIN = """
WITH ranked AS (
  SELECT update_id, customer_id, email, updated_at,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY updated_at DESC, update_id DESC) AS rn
  FROM customer_updates
)
SELECT update_id, customer_id, email, updated_at
FROM ranked
WHERE rn = 1
ORDER BY customer_id
"""
SQL_FIRST = """
WITH ranked AS (
  SELECT update_id, customer_id, email, updated_at,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY updated_at ASC, update_id ASC) AS rn
  FROM customer_updates
)
SELECT update_id, customer_id, email, updated_at FROM ranked WHERE rn = 1 ORDER BY customer_id
"""
SQL_NOTIE = """
WITH ranked AS (
  SELECT update_id, customer_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) AS rn
  FROM customer_updates)
SELECT update_id FROM ranked WHERE rn = 1 AND customer_id = 1
"""
def load(rows):
    con = sqlite3.connect(":memory:")
    con.execute(SCHEMA)
    con.executemany("INSERT INTO customer_updates VALUES (?,?,?,?)", rows)
    return con
con = load(ROWS)
sql_df = pd.read_sql_query(SQL_MAIN, con)
first_df = pd.read_sql_query(SQL_FIRST, con)
print("latest per customer:"); print(sql_df.to_string(index=False))
print("\nfirst per customer:"); print(first_df.to_string(index=False))

cu = pd.read_sql_query("SELECT * FROM customer_updates", con)
# pd:main
pd_df = (cu.sort_values(["updated_at", "update_id"], ascending=[False, False])
           .drop_duplicates(subset="customer_id", keep="first"))
# pd:end
# pd:first
pd_first = (cu.sort_values(["updated_at", "update_id"], ascending=[True, True])
              .drop_duplicates(subset="customer_id", keep="first"))
# pd:end
# compared after sorting by customer_id
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
pf = pd_first.sort_values("customer_id").reset_index(drop=True)
diff = first_df.loc[first_df["update_id"] != pf["update_id"], "customer_id"].tolist()
print("\ncustomers where SQL keep-first (ASC) and pandas keep-first (ASC) pick different rows:", diff)
assert diff == [4]   # NULL date sorts FIRST in SQLite ASC, but pandas sort_values puts NaN LAST

print("\nno tie-breaker, customer 1 pick on SQLite 3.45 (repeatable here, not guaranteed):",
      load(ROWS).execute(SQL_NOTIE).fetchall(), load(ROWS[::-1]).execute(SQL_NOTIE).fetchall())
print("asserts passed: SQL latest == pandas sort_values + drop_duplicates")
```

**Output (my run):**
```text
latest per customer:
 update_id  customer_id    email updated_at
         3            1 a3@x.com 2026-02-01
         4            2  b@x.com 2026-01-15
         5            3  c@x.com 2026-03-05
         8            4 d2@x.com 2026-01-10
         9            5  e@x.com        NaN

first per customer:
 update_id  customer_id    email updated_at
         1            1  a@x.com 2026-01-01
         4            2  b@x.com 2026-01-15
         6            3 c0@x.com 2026-01-01
         7            4  d@x.com        NaN
         9            5  e@x.com        NaN

customers where SQL keep-first (ASC) and pandas keep-first (ASC) pick different rows: [4]

no tie-breaker, customer 1 pick on SQLite 3.45 (repeatable here, not guaranteed): [(2,)] [(2,)]
asserts passed: SQL latest == pandas sort_values + drop_duplicates
```

**Edge cases:**
- Ties without the tie-breaker: customer 1's pick is left to the engine. On SQLite 3.45 it returned update 2 in both runs (even with the input rows inserted in reverse, because `update_id` is the rowid and the scan follows it), so it looks repeatable here, but that is an implementation side effect, not a promise. Other engines were not executed.
- NULL dates: keep-latest agrees between SQL and pandas (NULL/NaN last). Keep-first does not: SQLite sorts NULL smallest, so ASC puts NULL first and picks update 7 for customer 4, while `sort_values` defaults to `na_position="last"` and picks update 8. The output shows customer 4 as the one disagreement; fix with `na_position="first"` or by filtering NULL dates. NULL ordering defaults in PostgreSQL and MySQL differ from SQLite (not executed here).
- Dates must sort correctly as text: ISO `YYYY-MM-DD` does.
- Customer with a single row: kept.

**Then explain:**
- `ROW_NUMBER` is the right tool because it gives exactly one winner per customer. `RANK` would keep both tied rows.
- Repeatable results need a total order inside the window: `updated_at DESC, update_id DESC`. Rows that differ in no ordering column get an arbitrary order.
- Keep first: reverse the directions (or use ASC on both keys).
- pandas: `drop_duplicates(subset=..., keep="first")` keeps the first row it sees, so sort first. Sorting both columns descending reproduces the SQL rule.
- Deleting the losers instead of selecting the winner is Q35.

**Follow-ups:**
- *Is `GROUP BY customer_id, MAX(updated_at)` enough?* It loses the other columns and returns both tied rows when joined back; the window version returns one.
- *Several columns define "latest"?* Add keys to the ORDER BY (Q44).
- *Performance?* An index on `(customer_id, updated_at)` can help; deeper tuning is Q40 and Part 11.

**Common mistakes:**
- Omitting the tie-breaker and trusting the result.
- Sorting ascending in pandas and keeping `first`.
- Assuming NULLs sort the same way in every tool (see the keep-first difference).

### Q10 ⭐⭐⭐ 🟡 Finding duplicates: users(user_id, name, email), where the same email may appear several times and some emails are NULL. List every row whose email appears more than once, using COUNT(*) OVER (PARTITION BY email) > 1 in a CTE, and a GROUP BY email HAVING COUNT(*) > 1 version, plus the ROW_NUMBER = 1 flag for 'first copy' versus 'extra copies'. Explain how NULL emails are grouped by PARTITION BY and GROUP BY (all NULLs together), and give the pandas duplicated(subset='email', keep=False) and keep='first' versions.
**Asked at:** GeeksforGeeks SQL interview questions (RANK vs DENSE_RANK vs ROW_NUMBER, window functions, duplicates entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** `COUNT(*) OVER (PARTITION BY email)` gives every row the size of its email group, so `> 1` lists all copies; the `GROUP BY email HAVING COUNT(*) > 1` version needs a join back to the rows, and `ROW_NUMBER() = 1` marks the first copy, so `rn > 1` marks the extra ones; NULL emails form one group in both.

**Schema and sample data:** eight users. a@x.com appears three times, two users have a NULL email, and 'A@x.com' differs only by case.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO users VALUES (1,'Asha','a@x.com'),(2,'Ben','b@x.com'),(3,'Chitra','a@x.com'),
  (4,'Dev',NULL),(5,'Esha',NULL),(6,'Farid','c@x.com'),(7,'Gita','a@x.com'),(8,'Hari','A@x.com');
```

**SQL answer:** first copy = lowest `user_id`.
```sql
WITH w AS (
  SELECT user_id, name, email,
         COUNT(*) OVER (PARTITION BY email) AS copies,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY user_id) AS rn
  FROM users
)
SELECT user_id, name, email, copies, rn,
       CASE WHEN rn = 1 THEN 'first copy' ELSE 'extra copy' END AS flag
FROM w
WHERE copies > 1
ORDER BY user_id
```
```sql
SELECT u.user_id, u.name, u.email
FROM users u
JOIN (SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1) d
  ON u.email IS d.email
ORDER BY u.user_id
```

**pandas answer:**
```py
all_copies = users[users.duplicated(subset="email", keep=False)]
extra = users.duplicated(subset="email", keep="first")
```

**Example:**
- a@x.com: users 1, 3, 7 give copies = 3 and rn = 1, 2, 3, so user 1 is the first copy and users 3 and 7 are extras.
- NULL: users 4 and 5 are one partition (PARTITION BY puts NULLs together), copies = 2, so user 4 is first and 5 is an extra.
- b@x.com, c@x.com: one row each, not listed. 'A@x.com' (user 8) is a different string in SQLite (default binary comparison) and in pandas, so not a duplicate.
- Result: users 1, 3, 4, 5, 7.

**Code:** run with `python3 -I`.
```python
# Q10: finding duplicates with windows and GROUP BY
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO users VALUES (1,'Asha','a@x.com'),(2,'Ben','b@x.com'),(3,'Chitra','a@x.com'),
  (4,'Dev',NULL),(5,'Esha',NULL),(6,'Farid','c@x.com'),(7,'Gita','a@x.com'),(8,'Hari','A@x.com');
"""
# first copy = lowest user_id
SQL_MAIN = """
WITH w AS (
  SELECT user_id, name, email,
         COUNT(*) OVER (PARTITION BY email) AS copies,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY user_id) AS rn
  FROM users
)
SELECT user_id, name, email, copies, rn,
       CASE WHEN rn = 1 THEN 'first copy' ELSE 'extra copy' END AS flag
FROM w
WHERE copies > 1
ORDER BY user_id
"""
SQL_GROUP = """
SELECT u.user_id, u.name, u.email
FROM users u
JOIN (SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1) d
  ON u.email IS d.email
ORDER BY u.user_id
"""
SQL_GROUP_EQ = SQL_GROUP.replace("u.email IS d.email", "u.email = d.email")
SQL_COUNTCOL = """
SELECT user_id FROM (SELECT user_id, COUNT(email) OVER (PARTITION BY email) AS c FROM users)
WHERE c > 1 ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
grp_df = pd.read_sql_query(SQL_GROUP, con)
print(sql_df.to_string(index=False))
print("\nGROUP BY version with ON u.email IS d.email:", grp_df["user_id"].tolist())
print("same with ON u.email = d.email (NULL rows drop):", [r[0] for r in con.execute(SQL_GROUP_EQ)])
print("COUNT(email) OVER instead of COUNT(*):", [r[0] for r in con.execute(SQL_COUNTCOL)])
assert grp_df["user_id"].tolist() == sql_df["user_id"].tolist()

users = pd.read_sql_query("SELECT * FROM users ORDER BY user_id", con)
# pd:main
all_copies = users[users.duplicated(subset="email", keep=False)]
extra = users.duplicated(subset="email", keep="first")
# pd:end
pd_df = all_copies.assign(flag=extra[all_copies.index].map({True: "extra copy", False: "first copy"}))
# compared after sorting by user_id
pd.testing.assert_frame_equal(sql_df[["user_id", "name", "email", "flag"]],
                              pd_df[["user_id", "name", "email", "flag"]].sort_values("user_id").reset_index(drop=True),
                              check_dtype=False)
print("\npandas duplicated(keep=False) user_ids:", all_copies["user_id"].tolist())
print("pandas keep='first' marks as extra:", users.loc[extra, "user_id"].tolist())
print("asserts passed: window == GROUP BY join == pandas duplicated")
```

**Output (my run):**
```text
 user_id   name   email  copies  rn       flag
       1   Asha a@x.com       3   1 first copy
       3 Chitra a@x.com       3   2 extra copy
       4    Dev     NaN       2   1 first copy
       5   Esha     NaN       2   2 extra copy
       7   Gita a@x.com       3   3 extra copy

GROUP BY version with ON u.email IS d.email: [1, 3, 4, 5, 7]
same with ON u.email = d.email (NULL rows drop): [1, 3, 7]
COUNT(email) OVER instead of COUNT(*): [1, 3, 7]

pandas duplicated(keep=False) user_ids: [1, 3, 4, 5, 7]
pandas keep='first' marks as extra: [3, 5, 7]
asserts passed: window == GROUP BY join == pandas duplicated
```

**Edge cases:**
- NULL emails are grouped together by `PARTITION BY`, `GROUP BY` and by pandas `duplicated` (NaN/None counted equal). Whether two NULL emails are "the same person" is a business decision; exclude them with `WHERE email IS NOT NULL` if not.
- The GROUP BY version joined with `=` loses the NULL group (`NULL = NULL` is not true; output shows [1, 3, 7]); I joined with `IS`, which is NULL-safe in SQLite (PostgreSQL uses `IS NOT DISTINCT FROM`, MySQL `<=>`; not executed).
- `COUNT(email)` instead of `COUNT(*)` counts non-NULL values, so the NULL group counts 0 and drops out ([1, 3, 7]): a quiet difference.
- Case and whitespace: 'A@x.com' is not matched here; a case-insensitive rule needs `LOWER(email)` (and in pandas `str.lower()`). Some engines compare text case-insensitively by default (MySQL collations, from memory, not executed).

**Then explain:**
- Window version: one pass, keeps the row detail, gives you the count and the first-copy flag together. GROUP BY version: shows only the duplicated values unless you join back.
- `ROW_NUMBER = 1` marks the keeper; `rn > 1` marks what you would delete (Q35). The order inside OVER decides which copy is "first", so give it a unique key (`user_id`).
- pandas: `duplicated(subset="email", keep=False)` marks all copies; `keep="first"` marks only the later ones, which is the `rn > 1` set.

**Follow-ups:**
- *Count the duplicate groups?* `COUNT(DISTINCT email)` over the filtered rows, or `GROUP BY ... HAVING` then count.
- *Remove the duplicates?* Keep `rn = 1` or delete `rn > 1` (Q35).
- *Duplicates across several columns?* Partition by all of them.

**Common mistakes:**
- Using `=` to join back and silently losing NULL groups.
- Using `COUNT(email)` and not flagging NULL duplicates.
- Not saying which copy is kept.

### Q11 ⭐⭐⭐ 🟡 Debug: 'my top-N per group returns more than N rows' (and, in another report, fewer than expected). employees(emp_id, name, dept_id, salary) with ties at the cutoff. A query uses RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 3 and returns four rows for one department; another uses ROW_NUMBER and drops a tied employee. Reproduce both, explain exactly why, decide which behaviour the business wants (all ties versus exactly N), and show the fix for each. Give the pandas reproduction with rank(method='min') versus head(3).
**Asked at:** techinterview.org window-function gotchas article (ties, RANK = 2 returning nothing, window in WHERE, default frame), a guide and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** `RANK() <= 3` returns four rows when several employees tie for the last qualifying place, because tied rows share a rank; `ROW_NUMBER() <= 3` returns exactly three but drops one of the tied employees arbitrarily; pick the behaviour the business wants, and fix the first with `ROW_NUMBER` plus a stated tie rule, the second with `RANK` (or `DENSE_RANK`).

**Schema and sample data:** department 10 has Ben at 90 and three people tied at 70; department 20 has four distinct salaries.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,70),
  (5,'Esha',20,90),(6,'Farid',20,80),(7,'Gita',20,70),(8,'Hari',20,60);
```

**SQL answer:** tie rule for the exactly-N version: lower `emp_id` first.
```sql
WITH r AS (SELECT emp_id, name, dept_id, salary,
                  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS k FROM employees)
SELECT dept_id, emp_id, name, salary, k FROM r WHERE k <= 3 ORDER BY dept_id, k, emp_id
```
```sql
WITH r AS (SELECT emp_id, name, dept_id, salary,
                  ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS k FROM employees)
SELECT dept_id, emp_id, name, salary, k FROM r WHERE k <= 3 ORDER BY dept_id, k
```

**pandas answer:** `rank(method="min")` reproduces RANK; sort plus `head(3)` reproduces ROW_NUMBER.
```py
pd_rank = emp[emp.groupby("dept_id")["salary"].rank(method="min", ascending=False) <= 3]
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
              .groupby("dept_id").head(3))
```

**Example:**
- Department 10: salaries 90, 70, 70, 70. `RANK` gives 1, 2, 2, 2, so all four are `<= 3`: four rows. That is the report "more than N".
- `ROW_NUMBER` with `emp_id` as tie-break gives Ben 1, Asha 2, Chitra 3, Dev 4: Dev is dropped although he earns the same as Asha and Chitra. That is the report "someone is missing".
- Department 20: 90, 80, 70, 60 are all distinct, so both give three rows (Hari at 60 is out).

**Code:** run with `python3 -I`.
```python
# Q11: debug, top-N per group returns more (or fewer) rows than expected
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,70),
  (5,'Esha',20,90),(6,'Farid',20,80),(7,'Gita',20,70),(8,'Hari',20,60);
"""
SQL_RANK = """
WITH r AS (SELECT emp_id, name, dept_id, salary,
                  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS k FROM employees)
SELECT dept_id, emp_id, name, salary, k FROM r WHERE k <= 3 ORDER BY dept_id, k, emp_id
"""
# exactly N: tie rule stated = lower emp_id first
SQL_ROWNUM = """
WITH r AS (SELECT emp_id, name, dept_id, salary,
                  ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS k FROM employees)
SELECT dept_id, emp_id, name, salary, k FROM r WHERE k <= 3 ORDER BY dept_id, k
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
rank_df = pd.read_sql_query(SQL_RANK, con)
rn_df = pd.read_sql_query(SQL_ROWNUM, con)
print("RANK <= 3:"); print(rank_df.to_string(index=False))
print("\nROW_NUMBER <= 3 (tie-break emp_id):"); print(rn_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
pd_rank = emp[emp.groupby("dept_id")["salary"].rank(method="min", ascending=False) <= 3]
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
              .groupby("dept_id").head(3))
# pd:end
# compared after sorting by dept_id, salary desc, emp_id
key = lambda d: d.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])["emp_id"].tolist()
assert key(pd_rank) == key(rank_df) and key(pd_head) == key(rn_df)
print("\nrows per dept  RANK:", rank_df.groupby("dept_id").size().to_dict(),
      " ROW_NUMBER:", rn_df.groupby("dept_id").size().to_dict())
print("tied at the cutoff but dropped by ROW_NUMBER:", sorted(set(rank_df["name"]) - set(rn_df["name"])))
print("asserts passed: RANK<=3 == pandas rank(method='min')<=3; ROW_NUMBER<=3 == sort_values + head(3)")
```

**Output (my run):**
```text
RANK <= 3:
 dept_id  emp_id   name  salary  k
      10       2    Ben      90  1
      10       1   Asha      70  2
      10       3 Chitra      70  2
      10       4    Dev      70  2
      20       5   Esha      90  1
      20       6  Farid      80  2
      20       7   Gita      70  3

ROW_NUMBER <= 3 (tie-break emp_id):
 dept_id  emp_id   name  salary  k
      10       2    Ben      90  1
      10       1   Asha      70  2
      10       3 Chitra      70  3
      20       5   Esha      90  1
      20       6  Farid      80  2
      20       7   Gita      70  3

rows per dept  RANK: {10: 4, 20: 3}  ROW_NUMBER: {10: 3, 20: 3}
tied at the cutoff but dropped by ROW_NUMBER: ['Dev']
asserts passed: RANK<=3 == pandas rank(method='min')<=3; ROW_NUMBER<=3 == sort_values + head(3)
```

**Edge cases:**
- If the tie-break were missing, which tied employee `ROW_NUMBER` drops would be engine-dependent; I did not rely on that, and the query above has `emp_id` in the ORDER BY.
- The number of rows per department with RANK is 3 or more; it is never fewer than N when N rows exist.
- A department with fewer than N people returns them all in both.
- NULL salaries rank last in DESC in SQLite; filter them if they should not appear (Q4 shows a NULL taking a slot).

**Then explain:**
- Both behaviours are "correct" for their function: `RANK` treats equal salaries as equal, so it cannot cut between them; `ROW_NUMBER` forces distinct numbers, so it must cut.
- Decide with the business: "everyone who is in the top 3 by salary" (ties included, use `RANK`) versus "exactly three people" (use `ROW_NUMBER` and agree the tie rule, such as earlier hire date or lower id).
- If they want three salary levels, use `DENSE_RANK` (Q8).
- pandas: `rank(method="min") <= 3` matches the RANK rows; `head(3)` after sorting matches ROW_NUMBER.

**Follow-ups:**
- *How do I stop the extra rows without losing fairness?* Say so out loud and add the agreed tie-break columns.
- *How do I check the count?* count rows per department in the result, as the "rows per dept" line does.
- *What does the interviewer want?* I would ask which rule applies before coding.

**Common mistakes:**
- Using `RANK` when exactly N is required, or `ROW_NUMBER` when ties should be kept.
- Adding a tie-breaker to `RANK` (it turns it into ROW_NUMBER, since ties disappear).
- Not telling the stakeholder that the cutoff rule exists.

### Q12 ⭐⭐⭐ 🟡 Ranking with ties and tie-breakers, deterministic results: players(player_id, name, score, last_updated). Build a leaderboard that ranks by score descending, then by earlier last_updated, then by player_id, and show how ROW_NUMBER differs with and without the full tie-breaker. Explain why ROW_NUMBER over a tied ORDER BY is not guaranteed to be repeatable across runs or engines, and give the pandas sort_values with a list of columns and rank(method='first') version.
**Asked at:** techinterview.org window-function gotchas article (ties, RANK = 2 returning nothing, window in WHERE, default frame), a guide and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Rank with `ROW_NUMBER() OVER (ORDER BY score DESC, last_updated, player_id)` so no two rows tie in the ORDER BY; with only `score DESC` the order of tied rows is left to the engine, so positions can change between runs or engines.

**Schema and sample data:** six players; three tie at 90 (Ben and Chitra even share the same date) and two tie at 80.
```sql
CREATE TABLE players(player_id INTEGER PRIMARY KEY, name TEXT, score INTEGER, last_updated TEXT);
INSERT INTO players VALUES (1,'Asha',90,'2026-03-01'),(2,'Ben',90,'2026-02-01'),(3,'Chitra',90,'2026-02-01'),
 (4,'Dev',80,'2026-01-20'),(5,'Esha',80,'2026-01-05'),(6,'Farid',100,'2026-04-01');
```

**SQL answer:** rule: higher score first, then earlier `last_updated`, then lower `player_id`.
```sql
SELECT player_id, name, score, last_updated,
       ROW_NUMBER() OVER (ORDER BY score DESC, last_updated, player_id) AS position
FROM players
ORDER BY position
```
```sql
SELECT player_id, ROW_NUMBER() OVER (ORDER BY score DESC) AS position
FROM players ORDER BY player_id
```
```sql
SELECT player_id, RANK() OVER (ORDER BY score DESC) AS shared_pos
FROM players ORDER BY player_id
```

**pandas answer:** sort with a list of columns and number the rows, or pre-sort by the tie-breakers and use `rank(method="first")`.
```py
board = players.sort_values(["score", "last_updated", "player_id"], ascending=[False, True, True])
board = board.assign(position=range(1, len(board) + 1))
```
```py
alt = players.sort_values(["last_updated", "player_id"]).copy()
alt["position"] = alt["score"].rank(method="first", ascending=False).astype(int)
```

**Example:**
- Farid 100 is first.
- Three players at 90: Ben and Chitra (2026-02-01) come before Asha (2026-03-01) because earlier date wins; Ben and Chitra tie on date, so `player_id` puts Ben (2) before Chitra (3). Positions: Farid 1, Ben 2, Chitra 3, Asha 4.
- Two at 80: Esha (2026-01-05) before Dev (2026-01-20), positions 5 and 6.
- Score only: SQLite numbered the tied rows in row order: by player id the positions were [2, 3, 4, 5, 6, 1], so Asha got 2 (full rule: 4) and Dev got 5 (full rule: 6). It looks stable, but it just reflects scan order.

**Code:** run with `python3 -I`.
```python
# Q12: leaderboard with a full tie-breaker
import sqlite3
import pandas as pd

ROWS = [(1,'Asha',90,'2026-03-01'),(2,'Ben',90,'2026-02-01'),(3,'Chitra',90,'2026-02-01'),
        (4,'Dev',80,'2026-01-20'),(5,'Esha',80,'2026-01-05'),(6,'Farid',100,'2026-04-01')]
SCHEMA = "CREATE TABLE players(player_id INTEGER PRIMARY KEY, name TEXT, score INTEGER, last_updated TEXT);"
# score DESC, earlier last_updated first, then lower player_id
SQL_MAIN = """
SELECT player_id, name, score, last_updated,
       ROW_NUMBER() OVER (ORDER BY score DESC, last_updated, player_id) AS position
FROM players
ORDER BY position
"""
SQL_PARTIAL = """
SELECT player_id, ROW_NUMBER() OVER (ORDER BY score DESC) AS position
FROM players ORDER BY player_id
"""
SQL_RANK = """
SELECT player_id, RANK() OVER (ORDER BY score DESC) AS shared_pos
FROM players ORDER BY player_id
"""
def load(rows):
    con = sqlite3.connect(":memory:")
    con.execute(SCHEMA)
    con.executemany("INSERT INTO players VALUES (?,?,?,?)", rows)
    return con
con = load(ROWS)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nscore-only ORDER BY, positions by player_id:", [r[1] for r in con.execute(SQL_PARTIAL)])
print("same query, rows inserted in reverse order:   ", [r[1] for r in load(ROWS[::-1]).execute(SQL_PARTIAL)])
print("RANK on score only, shared positions:         ", [r[1] for r in con.execute(SQL_RANK)])

players = pd.read_sql_query("SELECT * FROM players", con)
# pd:main
board = players.sort_values(["score", "last_updated", "player_id"], ascending=[False, True, True])
board = board.assign(position=range(1, len(board) + 1))
# pd:end
# pd:rank
alt = players.sort_values(["last_updated", "player_id"]).copy()
alt["position"] = alt["score"].rank(method="first", ascending=False).astype(int)
# pd:end
# compared in leaderboard order (position)
pd.testing.assert_frame_equal(sql_df, board.sort_values("position").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_df, alt.sort_values("position").reset_index(drop=True)[sql_df.columns], check_dtype=False)
print("\nasserts passed: SQL ROW_NUMBER == pandas sort_values + position == rank(method='first') after pre-sorting by the tie-breakers")
```

**Output (my run):**
```text
 player_id   name  score last_updated  position
         6  Farid    100   2026-04-01         1
         2    Ben     90   2026-02-01         2
         3 Chitra     90   2026-02-01         3
         1   Asha     90   2026-03-01         4
         5   Esha     80   2026-01-05         5
         4    Dev     80   2026-01-20         6

score-only ORDER BY, positions by player_id: [2, 3, 4, 5, 6, 1]
same query, rows inserted in reverse order:    [2, 3, 4, 5, 6, 1]
RANK on score only, shared positions:          [2, 2, 2, 5, 5, 1]

asserts passed: SQL ROW_NUMBER == pandas sort_values + position == rank(method='first') after pre-sorting by the tie-breakers
```

**Edge cases:**
- Honest result: on SQLite 3.45 the score-only query gave the same positions when I inserted the rows in reverse, so I could not make it flip. The standard does not promise that, and an index, a parallel plan or another engine can change it; other engines were not executed.
- If the product requirement is shared positions for equal scores, use `RANK` on score only: output `[2, 2, 2, 5, 5, 1]`.
- NULL scores: they rank last in DESC in SQLite; pandas `sort_values` puts NaN last too (not in this data).
- Ties in all three columns are impossible here because `player_id` is unique; that is what makes the order total.

**Then explain:**
- An ORDER BY is deterministic only if it is a total order. Add a unique column last (`player_id`).
- `ROW_NUMBER` over a tied order must still give different numbers, so the engine picks; a different plan or data layout can pick differently.
- Choose tie-breakers that mean something to users (earlier achievement wins), then the unique id as the last resort.
- pandas: `sort_values(["score","last_updated","player_id"], ascending=[False, True, True])` gives the order; `rank(method="first")` follows row order among ties, so pre-sort by the tie-breakers.

**Follow-ups:**
- *Shared positions with a gap?* `RANK` on score only.
- *Is the outer `ORDER BY position` needed?* Yes; ordering inside `OVER` does not order the result (Q37).
- *Do I need an index?* Not for correctness.

**Common mistakes:**
- Calling a leaderboard deterministic because it gave the same output twice.
- Using `RANK` and expecting no ties.
- Using `rank(method="first")` in pandas on an unsorted frame.

### Q13 ⭐⭐⭐ 🟡 Rank an aggregate in the same query (aggregate then rank): sales(sale_id, region, product, amount). Rank products by total revenue within each region using SUM(amount) with GROUP BY and RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) in one SELECT. Explain the order of evaluation (GROUP BY first, then the window sees the grouped rows), why a window function cannot be inside an aggregate, the CTE alternative, and give pandas groupby sum then groupby rank.
**Asked at:** techinterview.org window-function gotchas article (ties, RANK = 2 returning nothing, window in WHERE, default frame), a guide and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** In SQL you can write `GROUP BY region, product` and `RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC)` in the same SELECT, because the grouping happens first and the window then runs over the grouped rows; a window function cannot go inside an aggregate, and a CTE that aggregates first is the clearer alternative.

**Schema and sample data:** nine sales rows. North has a tie (B and C at 120); East has a product whose only sale has a NULL amount.
```sql
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'North','A',100),(2,'North','A',50),(3,'North','B',120),(4,'North','C',120),
  (5,'North','D',30),(6,'South','A',200),(7,'South','B',80),(8,'East','C',40),(9,'East','X',NULL);
```

**SQL answer:**
```sql
SELECT region, product, SUM(amount) AS total,
       RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) AS rnk
FROM sales
GROUP BY region, product
ORDER BY region, rnk, product
```
The CTE alternative (same rows):
```sql
WITH t AS (SELECT region, product, SUM(amount) AS total FROM sales GROUP BY region, product)
SELECT region, product, total,
       RANK() OVER (PARTITION BY region ORDER BY total DESC) AS rnk
FROM t
ORDER BY region, rnk, product
```

**pandas answer:** `groupby` sum, then `groupby("region")` rank. `min_count=1` makes an all-NaN sum NaN, as in SQL.
```py
tot = sales.groupby(["region", "product"], as_index=False).agg(total=("amount", lambda s: s.sum(min_count=1)))
tot["rnk"] = (tot.groupby("region")["total"]
                 .rank(method="min", ascending=False, na_option="bottom").astype(int))
```

**Example:**
- North: A = 100 + 50 = 150, B = 120, C = 120, D = 30. `RANK` gives A 1, B 2, C 2, D 4 (tie shares 2, the next is 4).
- South: A 200 rank 1, B 80 rank 2.
- East: C 40 rank 1; X's only amount is NULL, so `SUM` is NULL, which sorts last in DESC and gets rank 2.
- Output is ordered by region, rank, product so the tie between B and C is shown in a fixed order.

**Code:** run with `python3 -I`.
```python
# Q13: rank an aggregate in the same query
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'North','A',100),(2,'North','A',50),(3,'North','B',120),(4,'North','C',120),
  (5,'North','D',30),(6,'South','A',200),(7,'South','B',80),(8,'East','C',40),(9,'East','X',NULL);
"""
SQL_MAIN = """
SELECT region, product, SUM(amount) AS total,
       RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) AS rnk
FROM sales
GROUP BY region, product
ORDER BY region, rnk, product
"""
SQL_CTE = """
WITH t AS (SELECT region, product, SUM(amount) AS total FROM sales GROUP BY region, product)
SELECT region, product, total,
       RANK() OVER (PARTITION BY region ORDER BY total DESC) AS rnk
FROM t
ORDER BY region, rnk, product
"""
SQL_BAD = """
SELECT region, SUM(RANK() OVER (ORDER BY amount)) FROM sales GROUP BY region
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
cte_df = pd.read_sql_query(SQL_CTE, con)
print(sql_df.to_string(index=False))
assert sql_df.equals(cte_df)
try:
    con.execute(SQL_BAD).fetchall()
except sqlite3.OperationalError as e:
    print("\nwindow function inside an aggregate ->", type(e).__name__ + ":", e)

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
tot = sales.groupby(["region", "product"], as_index=False).agg(total=("amount", lambda s: s.sum(min_count=1)))
tot["rnk"] = (tot.groupby("region")["total"]
                 .rank(method="min", ascending=False, na_option="bottom").astype(int))
# pd:end
# compared after sorting by region, rnk, product
pd.testing.assert_frame_equal(sql_df, tot.sort_values(["region", "rnk", "product"]).reset_index(drop=True), check_dtype=False)
plain = sales.groupby(["region", "product"])["amount"].sum()
print("\nplain pandas .sum() for East/X (all NaN):", plain[("East", "X")], "  SQL SUM gives NULL")
print("asserts passed: aggregate+window == CTE == pandas groupby sum then rank")
```

**Output (my run):**
```text
region product  total  rnk
  East       C   40.0    1
  East       X    NaN    2
 North       A  150.0    1
 North       B  120.0    2
 North       C  120.0    2
 North       D   30.0    4
 South       A  200.0    1
 South       B   80.0    2

window function inside an aggregate -> OperationalError: misuse of window function RANK()

plain pandas .sum() for East/X (all NaN): 0.0   SQL SUM gives NULL
asserts passed: aggregate+window == CTE == pandas groupby sum then rank
```

**Edge cases:**
- NULL total: SQL `SUM` of only NULLs is NULL (and still gets a rank, last). pandas `.sum()` returns 0.0 for an all-NaN group (output line), which gives X a 0.0 total instead of NULL (same rank 2 here, wrong number); I used `min_count=1` plus `na_option="bottom"` to match.
- Ties: shared rank with `RANK`; use `ROW_NUMBER` with a tie-breaker for unique positions.
- A region with one product: rank 1.
- Nesting error: `SUM(RANK() OVER (...))` fails with `misuse of window function RANK()` in SQLite 3.45 (output). Message wording on other engines was not executed.

**Then explain:**
- Order of evaluation: `FROM`, `WHERE`, `GROUP BY`, `HAVING`, then window functions (which see one row per group), then `SELECT` list, `ORDER BY`. That is why `SUM(amount)` is allowed inside the window's ORDER BY: it is already computed.
- A window function can use aggregate results, but an aggregate cannot contain a window function, since windows run after aggregates.
- CTE form: aggregate in the CTE, rank in the next step; clearer, and the only way to filter on the rank (`WHERE rnk <= 2`), because windows are not allowed in `WHERE` (Q3).
- pandas: two steps, `groupby([...]).sum()` then `groupby("region").rank(...)`.

**Follow-ups:**
- *Top product per region?* Filter `rnk = 1` in an outer query (ties kept) or `ROW_NUMBER` for one.
- *Rank across all regions instead?* Drop `PARTITION BY`.
- *Why not rank before grouping?* You would rank individual sales, not product totals (Q48 shows how the wrong grain misleads).

**Common mistakes:**
- Putting the window function inside `SUM` or trying to filter on the alias in the same SELECT.
- Forgetting that the window sees grouped rows, not the original sales rows.
- Using `.sum()` in pandas and ranking an all-NaN group as 0.

### Q14 ⭐⭐⭐ 🟡 Percent of group total and difference from group average: orders(order_id, region, amount). For each order show its share of the region's total (amount / SUM(amount) OVER (PARTITION BY region)) as a percentage with one decimal, and its difference from the region's average amount. Explain the integer-division trap (multiply by 100.0), what happens when the group total is zero or NULL (NULLIF), why no ORDER BY is used in OVER here, and give the pandas transform('sum') and transform('mean') version.
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `amount / SUM(amount) OVER (PARTITION BY region)` gives each row's share of its region, but it must be written `100.0 * amount / ...` or integer division returns 0, and the denominator needs `NULLIF(..., 0)` so a zero total gives NULL instead of a divide-by-zero.

**Schema and sample data:** nine orders. Region N is clean (total 1000), S has a NULL amount, Z totals zero, E has only a NULL amount.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'N',100),(2,'N',300),(3,'N',600),
  (4,'S',50),(5,'S',150),(6,'S',NULL),
  (7,'Z',0),(8,'Z',0),(9,'E',NULL);
```

**SQL answer:** `SQL_MAIN` (Code block). The other two queries (`SQL_INT`, `SQL_ORDERED`) are the traps, run next to it.
```sql
SELECT order_id, region, amount,
       ROUND(100.0 * amount / NULLIF(SUM(amount) OVER (PARTITION BY region), 0), 1) AS pct_of_region,
       ROUND(amount - AVG(amount) OVER (PARTITION BY region), 2) AS diff_from_avg
FROM orders
ORDER BY order_id
```

**pandas answer:** `transform` returns one value per original row, so the share is a plain column expression.
```python
total = orders.groupby("region")["amount"].transform("sum")
avg = orders.groupby("region")["amount"].transform("mean")
pd_df = orders.assign(
    pct_of_region=(100.0 * orders["amount"] / total.replace(0, np.nan)).round(1),
    diff_from_avg=(orders["amount"] - avg).round(2),
)
```

**Example:**
- Region N: total 100 + 300 + 600 = 1000, average 333.33. Order 1: 100 / 1000 = 10.0 percent, difference 100 - 333.33 = -233.33. Order 2: 30.0 percent, -33.33. Order 3: 60.0 percent, +266.67.
- Region S: `SUM` and `AVG` skip the NULL, so total 200 and average 100. Order 4: 25.0 percent and -50; order 5: 75.0 percent and +50. Order 6 has a NULL amount, so both its numbers are NULL.
- Region Z: total 0, so `NULLIF(0, 0)` is NULL and the share is NULL. The average is 0, so the difference is 0.
- Region E: only a NULL amount, so the total is NULL and everything is NULL.
- No `ORDER BY` inside `OVER`, so the window is the whole region for every row. This is what makes the total a total.

**Code:** run with `python3 -I`.
```python
# Q14: percent of group total and difference from group average
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'N',100),(2,'N',300),(3,'N',600),
  (4,'S',50),(5,'S',150),(6,'S',NULL),
  (7,'Z',0),(8,'Z',0),(9,'E',NULL);
"""
SQL_MAIN = """
SELECT order_id, region, amount,
       ROUND(100.0 * amount / NULLIF(SUM(amount) OVER (PARTITION BY region), 0), 1) AS pct_of_region,
       ROUND(amount - AVG(amount) OVER (PARTITION BY region), 2) AS diff_from_avg
FROM orders
ORDER BY order_id
"""
SQL_INT = """
SELECT order_id, amount / SUM(amount) OVER (PARTITION BY region) * 100 AS int_pct,
       100.0 * amount / SUM(amount) OVER (PARTITION BY region) AS float_pct
FROM orders WHERE region IN ('N', 'Z')
ORDER BY order_id
"""
SQL_ORDERED = """
SELECT order_id, amount, SUM(amount) OVER (PARTITION BY region ORDER BY order_id) AS sum_with_order_by
FROM orders WHERE region = 'N'
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main:"); print(sql_df.to_string(index=False))
print("\nInteger-division trap and zero total (regions N and Z):")
print(pd.read_sql_query(SQL_INT, con).to_string(index=False))
print("\nOrdered window by mistake (region N):")
print(pd.read_sql_query(SQL_ORDERED, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
total = orders.groupby("region")["amount"].transform("sum")
avg = orders.groupby("region")["amount"].transform("mean")
pd_df = orders.assign(
    pct_of_region=(100.0 * orders["amount"] / total.replace(0, np.nan)).round(1),
    diff_from_avg=(orders["amount"] - avg).round(2),
)
# pd:end
print("\npandas transform('sum') per row:", total.tolist())
print(pd_df.to_string(index=False))
# compared after sorting both by order_id
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("order_id").reset_index(drop=True), check_dtype=False)

# surprise: pandas sum of an all-NaN group is 0.0 (SQL SUM is NULL); region E amount is NULL either way
print("\nall-NULL region E: pandas sum =", total[orders["region"] == "E"].tolist(),
      "| SQL SUM =", con.execute("SELECT SUM(amount) FROM orders WHERE region='E'").fetchone())
# division by zero in SQLite is NULL, not an error
print("SQLite 1/0 =", con.execute("SELECT 1.0/0").fetchone())
print("asserts passed: SQL == pandas")
```

**Output (my run):**
```text
SQL main:
 order_id region  amount  pct_of_region  diff_from_avg
        1      N   100.0           10.0        -233.33
        2      N   300.0           30.0         -33.33
        3      N   600.0           60.0         266.67
        4      S    50.0           25.0         -50.00
        5      S   150.0           75.0          50.00
        6      S     NaN            NaN            NaN
        7      Z     0.0            NaN           0.00
        8      Z     0.0            NaN           0.00
        9      E     NaN            NaN            NaN

Integer-division trap and zero total (regions N and Z):
 order_id  int_pct  float_pct
        1      0.0       10.0
        2      0.0       30.0
        3      0.0       60.0
        7      NaN        NaN
        8      NaN        NaN

Ordered window by mistake (region N):
 order_id  amount  sum_with_order_by
        1     100                100
        2     300                400
        3     600               1000

pandas transform('sum') per row: [1000.0, 1000.0, 1000.0, 200.0, 200.0, 200.0, 0.0, 0.0, 0.0]
 order_id region  amount  pct_of_region  diff_from_avg
        1      N   100.0           10.0        -233.33
        2      N   300.0           30.0         -33.33
        3      N   600.0           60.0         266.67
        4      S    50.0           25.0         -50.00
        5      S   150.0           75.0          50.00
        6      S     NaN            NaN            NaN
        7      Z     0.0            NaN           0.00
        8      Z     0.0            NaN           0.00
        9      E     NaN            NaN            NaN

all-NULL region E: pandas sum = [0.0] | SQL SUM = (None,)
SQLite 1/0 = (None,)
asserts passed: SQL == pandas
```

**Edge cases:**
- Zero total: SQLite returns NULL for a divide by zero (the run shows `1.0/0` is NULL), so without `NULLIF` it would also come out NULL here. PostgreSQL raises a division-by-zero error (from memory, not executed here), so `NULLIF` is the portable habit.
- NULL amount: skipped by `SUM` and `AVG`, and the row's own share is NULL. NULL is not 0: decide whether the business wants NULLs treated as zero (`COALESCE(amount, 0)`) before ranking or averaging, because that changes the average.
- All-NULL region: SQL `SUM` is NULL, but pandas `sum` of an all-NaN group is 0.0 (surprise in the run: the pandas total for region E is 0.0). My `replace(0, np.nan)` turns it into NaN, so the result still matches, but only because of that line.
- Percentages of a region should add to 100 only if no rounding and no NULLs; rounded shares can add to 99.9 or 100.1.

**Then explain:**
- **Integer division:** `amount / total` with two integers is integer division in SQLite (and in PostgreSQL, from memory), so 100 / 1000 is 0. Multiplying by `100.0` first makes it a float. The run shows `int_pct` all zero and `float_pct` correct.
- **No ORDER BY in OVER:** with `PARTITION BY` only, the frame is the whole partition. Adding `ORDER BY` changes the default frame to "start to current row (with peers)", so `SUM` becomes a running sum. The run shows region N becoming 100, 400, 1000. That is the classic wrong-total bug.
- **Window versus GROUP BY plus join:** the window keeps every row and attaches the group statistic, with no self-join.
- **pandas:** `groupby().transform("sum")` is the same idea; plain `groupby().sum()` has one row per group and would not line up.

**Follow-ups:**
- *Show the share of the grand total instead?* `SUM(amount) OVER ()`, an empty window, and in pandas `amount / amount.sum()`.
- *Why round in the query?* Presentation only; keep the raw ratio if more arithmetic follows.
- *Where does the window run?* After `WHERE` and `GROUP BY`, so filtered-out rows are not in the total.

**Common mistakes:**
- `amount / SUM(...) * 100` with integers.
- Adding `ORDER BY` inside `OVER` out of habit.
- Forgetting `NULLIF`, then being surprised by a crash on another engine.
- In pandas, using `groupby().sum()` and assigning it to a column (index mismatch) instead of `transform`.

### Q15 ⭐⭐⭐ 🟡 Top product per category per month: sales(sale_id, product_id, category, sale_date, amount) with ISO dates. Return the best-selling product (by total amount) in each category and month using a CTE that aggregates by category, month (strftime('%Y-%m')) and product, then ROW_NUMBER or RANK partitioned by category and month. Explain aggregate-before-rank, the tie rule you choose (product_id as tie-break), the month-must-keep-the-year trap, and give the pandas groupby sum then sort_values and drop_duplicates or idxmax version.
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Aggregate first (one row per category, month, product), then rank those totals inside each (category, month) and keep rank 1; the month must be `'%Y-%m'` so January 2024 and January 2025 stay apart, and the tie rule is "higher total, then lower product_id".

**Schema and sample data:** twelve sales over Books and Toys, in January and February 2024 and January 2025. Books January 2024 is a tie on purpose.
```sql
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, category TEXT, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,1,'Books','2024-01-05',30),(2,1,'Books','2024-01-20',20),(3,2,'Books','2024-01-11',50),
 (4,3,'Books','2024-02-02',10),(5,2,'Books','2024-02-15',15),
 (6,2,'Books','2025-01-09',40),(7,1,'Books','2025-01-10',25),
 (8,4,'Toys','2024-01-03',90),(9,5,'Toys','2024-01-04',60),(10,5,'Toys','2024-01-25',40),
 (11,4,'Toys','2025-01-02',10),(12,6,'Toys','2025-01-30',70);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_RANK` (keeps ties) and `SQL_WRONG` (month without year) are run next to it.
```sql
WITH monthly AS (
  SELECT category, strftime('%Y-%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%Y-%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         ROW_NUMBER() OVER (PARTITION BY category, month ORDER BY total DESC, product_id) AS rn
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rn = 1
ORDER BY category, month
```

**pandas answer:** group and sum, sort so the winner of each group comes first (total descending, product_id ascending), then keep the first row per group.
```python
monthly = (sales.assign(month=pd.to_datetime(sales["sale_date"]).dt.strftime("%Y-%m"))
           .groupby(["category", "month", "product_id"], as_index=False)
           .agg(total=("amount", "sum")))
pd_df = (monthly.sort_values(["category", "month", "total", "product_id"],
                             ascending=[True, True, False, True])
         .drop_duplicates(["category", "month"])
         .reset_index(drop=True))
```

**Example:**
- Books, 2024-01: product 1 has 30 + 20 = 50, product 2 has 50. A tie. `ORDER BY total DESC, product_id` puts product 1 first, so product 1 wins. `RANK` would return both.
- Books, 2024-02: product 3 has 10, product 2 has 15, so product 2 wins.
- Books, 2025-01: product 2 has 40, product 1 has 25, so product 2 wins.
- Toys, 2024-01: product 4 has 90, product 5 has 60 + 40 = 100, so product 5 wins. Note a single sale of 90 would have looked best if I ranked rows instead of totals.
- Toys, 2025-01: product 6 has 70, product 4 has 10, so product 6 wins.
- Result: five rows, one per (category, month).

**Code:** run with `python3 -I`.
```python
# Q15: top product per category per month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, category TEXT, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,1,'Books','2024-01-05',30),(2,1,'Books','2024-01-20',20),(3,2,'Books','2024-01-11',50),
 (4,3,'Books','2024-02-02',10),(5,2,'Books','2024-02-15',15),
 (6,2,'Books','2025-01-09',40),(7,1,'Books','2025-01-10',25),
 (8,4,'Toys','2024-01-03',90),(9,5,'Toys','2024-01-04',60),(10,5,'Toys','2024-01-25',40),
 (11,4,'Toys','2025-01-02',10),(12,6,'Toys','2025-01-30',70);
"""
SQL_MAIN = """
WITH monthly AS (
  SELECT category, strftime('%Y-%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%Y-%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         ROW_NUMBER() OVER (PARTITION BY category, month ORDER BY total DESC, product_id) AS rn
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rn = 1
ORDER BY category, month
"""
SQL_RANK = """
WITH monthly AS (
  SELECT category, strftime('%Y-%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%Y-%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         RANK() OVER (PARTITION BY category, month ORDER BY total DESC) AS rk
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rk = 1
ORDER BY category, month, product_id
"""
SQL_WRONG = """
WITH monthly AS (
  SELECT category, strftime('%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         ROW_NUMBER() OVER (PARTITION BY category, month ORDER BY total DESC, product_id) AS rn
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rn = 1
ORDER BY category, month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL ROW_NUMBER (tie-break product_id):"); print(sql_df.to_string(index=False))
print("\nSQL RANK (keeps ties):"); print(pd.read_sql_query(SQL_RANK, con).to_string(index=False))
print("\nSQL wrong: month without the year:"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
monthly = (sales.assign(month=pd.to_datetime(sales["sale_date"]).dt.strftime("%Y-%m"))
           .groupby(["category", "month", "product_id"], as_index=False)
           .agg(total=("amount", "sum")))
pd_df = (monthly.sort_values(["category", "month", "total", "product_id"],
                             ascending=[True, True, False, True])
         .drop_duplicates(["category", "month"])
         .reset_index(drop=True))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in order category, month (both already sorted that way)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

# idxmax variant: first row with the max in frame order, so sort first to make it deterministic
im = monthly.sort_values(["category", "month", "product_id"]).reset_index(drop=True)
im = im.loc[im.groupby(["category", "month"])["total"].idxmax()].reset_index(drop=True)
pd.testing.assert_frame_equal(sql_df, im, check_dtype=False)
print("\nidxmax after sorting by product_id gives the same rows (first max wins)")
print("asserts passed: SQL == pandas (drop_duplicates) == pandas (idxmax)")
```

**Output (my run):**
```text
SQL ROW_NUMBER (tie-break product_id):
category   month  product_id  total
   Books 2024-01           1     50
   Books 2024-02           2     15
   Books 2025-01           2     40
    Toys 2024-01           5    100
    Toys 2025-01           6     70

SQL RANK (keeps ties):
category   month  product_id  total
   Books 2024-01           1     50
   Books 2024-01           2     50
   Books 2024-02           2     15
   Books 2025-01           2     40
    Toys 2024-01           5    100
    Toys 2025-01           6     70

SQL wrong: month without the year:
category month  product_id  total
   Books    01           2     90
   Books    02           2     15
    Toys    01           4    100

pandas:
category   month  product_id  total
   Books 2024-01           1     50
   Books 2024-02           2     15
   Books 2025-01           2     40
    Toys 2024-01           5    100
    Toys 2025-01           6     70

idxmax after sorting by product_id gives the same rows (first max wins)
asserts passed: SQL == pandas (drop_duplicates) == pandas (idxmax)
```

**Edge cases:**
- Ties: with `ROW_NUMBER` exactly one winner per group, chosen by `product_id`. With `RANK`, both tied products come back (the run shows two rows for Books 2024-01).
- The month trap: with `strftime('%m')` the January rows of 2024 and 2025 merge. In the run Books January becomes one group (product 2: 50 + 40 = 90 against product 1: 75) and the two real Januaries disappear, as do Toys' two Januaries.
- Category-months with no sales produce no row (they are not in the data to group).
- NULL amounts are skipped by `SUM`; a product with only NULL amounts gets a NULL total, and in `ORDER BY total DESC` SQLite sorts NULL last (so it only wins if it is the only product).

**Then explain:**
- **Aggregate before rank:** the question is "best-selling product", which is about product totals, not single sales rows. Ranking rows first would rank individual sales.
- **Tie rule I choose:** total descending, then product_id ascending; I say it out loud so the answer is reproducible.
- **ROW_NUMBER versus RANK here:** `ROW_NUMBER` for "exactly one product per month"; `RANK` if the business wants all tied winners.
- **pandas:** `sort_values` then `drop_duplicates(subset=[...])` keeps the first row per group, so the sort decides the winner. The `idxmax` version works too, but it returns the first row with the maximum in the frame's current order, so I sort by product_id first to make it deterministic (the run asserts it matches).
- **ISO dates** sort and `strftime` correctly as text in SQLite; in pandas I convert with `to_datetime` before formatting.

**Follow-ups:**
- *Top 3 products per month?* Change `rn = 1` to `rn <= 3` (Q26 covers the tie variants).
- *Why not `GROUP BY` with `MAX(total)`?* It gives the maximum but not which product earned it; joining back would return ties.
- *Share of the month's category sales won by the top product?* Add `SUM(total) OVER (PARTITION BY category, month)` in the ranked CTE.

**Common mistakes:**
- Month name or number without the year.
- Ranking raw sales instead of per-product totals.
- No tie-break, so the winner can change between runs or engines.
- Using `idxmax` on an unsorted frame and assuming it is deterministic.

### Q16 ⭐⭐⭐ 🟡 The Nth transaction per user: transactions(txn_id, user_id, txn_time, amount). Return each user's second transaction (and say how to get the first and the last). Use ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) = 2, and the reversed ORDER BY for the last. Explain users with fewer than two transactions (no row), why the tie-breaker matters when two transactions share a timestamp, and give the pandas groupby().cumcount() + 1 version (cumcount starts at 0).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Number each user's transactions with `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id)` in a subquery and keep `rn = 2`; the first is `rn = 1`, the last is the same numbering with the order reversed, and `txn_id` in the order makes ties on the timestamp deterministic.

**Schema and sample data:** seven transactions. User 2's first two share a timestamp; user 3 has one transaction.
```sql
CREATE TABLE transactions(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_time TEXT, amount INTEGER);
INSERT INTO transactions VALUES
 (1,1,'2024-01-01 09:00',10),(2,1,'2024-01-02 10:00',20),(3,1,'2024-01-03 11:00',30),
 (4,2,'2024-02-01 08:00',5),(5,2,'2024-02-01 08:00',7),(6,2,'2024-02-05 09:00',9),
 (7,3,'2024-03-01 12:00',40);
```

**SQL answer:** `SQL_MAIN` for the second transaction, `SQL_FIRST_LAST` for first and last (Code block).
```sql
SELECT txn_id, user_id, txn_time, amount
FROM (SELECT t.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn
      FROM transactions t)
WHERE rn = 2
ORDER BY user_id
```
```sql
SELECT user_id,
       MAX(CASE WHEN rn_first = 1 THEN txn_id END) AS first_txn,
       MAX(CASE WHEN rn_last = 1 THEN txn_id END) AS last_txn
FROM (SELECT user_id, txn_id,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn_first,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time DESC, txn_id DESC) AS rn_last
      FROM transactions)
GROUP BY user_id
ORDER BY user_id
```

**pandas answer:** sort by user, time and id, number with `cumcount` (starts at 0, so add 1), filter.
```python
s = txn.sort_values(["user_id", "txn_time", "txn_id"]).reset_index(drop=True)
s["n"] = s.groupby("user_id").cumcount() + 1
pd_df = s[s["n"] == 2].drop(columns="n").reset_index(drop=True)
```

**Example:**
- User 1: 09:00, 10:00, 11:00 are numbered 1, 2, 3. Second is txn 2.
- User 2: txn 4 and txn 5 have the same time. `ORDER BY txn_time, txn_id` puts 4 first and 5 second, so the second transaction is txn 5. Txn 6 is third.
- User 3: only rn = 1 exists, so no row comes back.
- First: txns 1, 4, 7. Last (reversed order): txns 3, 6, 7. User 3's first and last are the same row.

**Code:** run with `python3 -I`.
```python
# Q16: Nth transaction per user
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE transactions(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_time TEXT, amount INTEGER);
INSERT INTO transactions VALUES
 (1,1,'2024-01-01 09:00',10),(2,1,'2024-01-02 10:00',20),(3,1,'2024-01-03 11:00',30),
 (4,2,'2024-02-01 08:00',5),(5,2,'2024-02-01 08:00',7),(6,2,'2024-02-05 09:00',9),
 (7,3,'2024-03-01 12:00',40);
"""
SQL_MAIN = """
SELECT txn_id, user_id, txn_time, amount
FROM (SELECT t.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn
      FROM transactions t)
WHERE rn = 2
ORDER BY user_id
"""
SQL_FIRST_LAST = """
SELECT user_id,
       MAX(CASE WHEN rn_first = 1 THEN txn_id END) AS first_txn,
       MAX(CASE WHEN rn_last = 1 THEN txn_id END) AS last_txn
FROM (SELECT user_id, txn_id,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn_first,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time DESC, txn_id DESC) AS rn_last
      FROM transactions)
GROUP BY user_id
ORDER BY user_id
"""
SQL_NO_TIEBREAK = """
SELECT txn_id, user_id
FROM (SELECT t.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time) AS rn
      FROM transactions t)
WHERE rn = 2 AND user_id = 2
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL second transaction per user:"); print(sql_df.to_string(index=False))
sql_fl = pd.read_sql_query(SQL_FIRST_LAST, con)
print("\nSQL first and last txn_id per user:"); print(sql_fl.to_string(index=False))
print("\nWithout txn_id tie-break, user 2 second txn_id (unspecified order, only this run):",
      con.execute(SQL_NO_TIEBREAK).fetchall())

txn = pd.read_sql_query("SELECT * FROM transactions", con)
# pd:main
s = txn.sort_values(["user_id", "txn_time", "txn_id"]).reset_index(drop=True)
s["n"] = s.groupby("user_id").cumcount() + 1
pd_df = s[s["n"] == 2].drop(columns="n").reset_index(drop=True)
# pd:end
print("\ncumcount before +1 (starts at 0):", txn.sort_values(["user_id", "txn_time", "txn_id"]).groupby("user_id").cumcount().tolist())
print("pandas second transaction per user:"); print(pd_df.to_string(index=False))
# compared in user_id order
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("user_id").reset_index(drop=True), check_dtype=False)

first = s.groupby("user_id").head(1)["txn_id"].tolist()
last = s.groupby("user_id").tail(1)["txn_id"].tolist()
last2 = s[s.groupby("user_id").cumcount(ascending=False) == 0]["txn_id"].tolist()
assert first == sql_fl["first_txn"].tolist() and last == sql_fl["last_txn"].tolist() == last2
print("first:", first, "last:", last, "(same as SQL)")
assert sql_df["user_id"].tolist() == [1, 2] and 3 not in sql_df["user_id"].tolist()
print("asserts passed: SQL == pandas; user 3 (one transaction) has no second row")
```

**Output (my run):**
```text
SQL second transaction per user:
 txn_id  user_id         txn_time  amount
      2        1 2024-01-02 10:00      20
      5        2 2024-02-01 08:00       7

SQL first and last txn_id per user:
 user_id  first_txn  last_txn
       1          1         3
       2          4         6
       3          7         7

Without txn_id tie-break, user 2 second txn_id (unspecified order, only this run): [(5, 2)]

cumcount before +1 (starts at 0): [0, 1, 2, 0, 1, 2, 0]
pandas second transaction per user:
 txn_id  user_id         txn_time  amount
      2        1 2024-01-02 10:00      20
      5        2 2024-02-01 08:00       7
first: [1, 4, 7] last: [3, 6, 7] (same as SQL)
asserts passed: SQL == pandas; user 3 (one transaction) has no second row
```

**Edge cases:**
- Fewer than two transactions: no row (user 3). To list the user anyway with NULL, join the users table with `LEFT JOIN` to the filtered result.
- Timestamp ties: without `txn_id` the second transaction of user 2 is whichever tied row the engine happens to put second. The run shows what SQLite did here, but that is not a guarantee, and it can change with an index or another engine.
- Duplicates: if two rows are identical in every column including `txn_id` (no primary key), `ROW_NUMBER` still numbers them, so one of them is called "second". Dedupe first if that is not wanted.
- NULL `txn_time`: SQLite sorts NULL first in ascending order, so a NULL-time row would count as the user's first. Other engines default differently (not executed here); filter or use an explicit `NULLS LAST` (works on SQLite 3.45) when it matters.

**Then explain:**
- **Why a subquery:** window functions cannot appear in `WHERE`, so number in an inner query and filter outside.
- **Last transaction:** either reverse both sort keys (`txn_time DESC, txn_id DESC`) and take `rn = 1`, or compute `COUNT(*) OVER (PARTITION BY user_id)` and compare. Reversing is simpler.
- **Why `ROW_NUMBER`, not `RANK`:** `RANK` can give two rows rank 2 on ties, and "the second transaction" must be exactly one row.
- **pandas:** `cumcount()` is zero-based (the run prints 0, 1, 2 for user 1), so `+ 1` matches `ROW_NUMBER`. `head(1)`/`tail(1)` give first and last; `cumcount(ascending=False) == 0` also gives last, and the run asserts they agree.

**Follow-ups:**
- *Second transaction's gap from the first?* That needs `LAG` or `LEAD` (Part 5).
- *Nth for a parameter N?* Pass N as a Python sqlite3 parameter in `rn = ?`.
- *Why not `LIMIT 1 OFFSET 1`?* It works on the whole table, not per user.

**Common mistakes:**
- No tie-breaker on `txn_time`.
- Off-by-one with `cumcount` (zero-based).
- Using `RANK`, which can return two "second" rows.
- Expecting a row for users with one transaction.

### Q17 ⭐⭐⭐ 🟡 Employees whose salary is their department's top: employees(emp_id, name, dept_id, salary). Return them with MAX(salary) OVER (PARTITION BY dept_id) compared in an outer query, and again with RANK() = 1, and show the two give the same rows including ties. Explain which one reads better, what happens when salary is NULL (a NULL max if all NULL, NULL rows never equal the max), and give the pandas transform('max') mask and the idxmax contrast (idxmax returns only the first tied row).
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Both `salary = MAX(salary) OVER (PARTITION BY dept_id)` and `RANK() = 1` return every employee tied for the top, but they only agree if NULL salaries are filtered for the RANK version; I find the `MAX` comparison clearer, and in pandas it is a `transform("max")` mask, not `idxmax`.

**Schema and sample data:** eight employees. Department 10 has a tie at 70, department 20 has a NULL salary, department 30 has only a NULL salary, department 40 has one employee.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Gita',20,NULL),
  (7,'Farid',30,NULL),(8,'Hari',40,55);
```

**SQL answer:** `SQL_MAIN` (MAX version), `SQL_RANK` (RANK version) and `SQL_RANK_SAFE` (RANK with NULLs filtered) in the Code block.
```sql
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, MAX(salary) OVER (PARTITION BY dept_id) AS dept_max FROM employees e)
WHERE salary = dept_max
ORDER BY emp_id
```
```sql
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk FROM employees e)
WHERE rk = 1
ORDER BY emp_id
```
```sql
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
      FROM employees e WHERE salary IS NOT NULL)
WHERE rk = 1
ORDER BY emp_id
```

**pandas answer:** one value per row (the department maximum), then compare.
```python
dept_max = emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[emp["salary"] == dept_max]
```

**Example:**
- Dept 10: max is 70; Asha and Ben both equal it, so both are returned (tie kept). Chitra (60) is not.
- Dept 20: `MAX` skips the NULL, giving 90; Dev is returned. Esha (40) no. Gita's NULL is not equal to 90.
- Dept 30: Farid's salary is NULL, so the max is NULL, and `NULL = NULL` is unknown, so `MAX` returns no one.
- Dept 40: Hari is alone, so he is the max and is returned.
- `MAX` result: Asha, Ben, Dev, Hari.
- Plain `RANK() ... ORDER BY salary DESC` in SQLite puts NULL last, so dept 20 is fine, but in dept 30 the only row (the NULL) gets rank 1, and Farid also appears. That is the one place the two differ; adding `WHERE salary IS NOT NULL` removes him.

**Code:** run with `python3 -I`.
```python
# Q17: employees whose salary is the department's top (MAX OVER vs RANK = 1)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Gita',20,NULL),
  (7,'Farid',30,NULL),(8,'Hari',40,55);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, MAX(salary) OVER (PARTITION BY dept_id) AS dept_max FROM employees e)
WHERE salary = dept_max
ORDER BY emp_id
"""
SQL_RANK = """
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk FROM employees e)
WHERE rk = 1
ORDER BY emp_id
"""
SQL_RANK_SAFE = """
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
      FROM employees e WHERE salary IS NOT NULL)
WHERE rk = 1
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_rank = pd.read_sql_query(SQL_RANK, con)
sql_safe = pd.read_sql_query(SQL_RANK_SAFE, con)
print("MAX() OVER:"); print(sql_main.to_string(index=False))
print("\nRANK() = 1 (no NULL filter):"); print(sql_rank.to_string(index=False))
print("\nRANK() = 1 with salary IS NOT NULL:"); print(sql_safe.to_string(index=False))
print("\nMAX == safe RANK:", sql_main.equals(sql_safe), "| MAX == plain RANK:", sql_main.equals(sql_rank))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
dept_max = emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[emp["salary"] == dept_max]
# pd:end
print("\npandas transform('max') mask:"); print(pd_df.to_string(index=False))
# compared after sorting by emp_id
pd.testing.assert_frame_equal(sql_main, pd_df.sort_values("emp_id").reset_index(drop=True), check_dtype=False)
assert sql_main.equals(sql_safe)

rk = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False)
print("\npandas rank(method='min', ascending=False) == 1:", emp.loc[rk == 1, "name"].tolist(), "(NaN rank is NaN, so Farid is out)")
try:
    emp.groupby("dept_id")["salary"].idxmax()
except ValueError as e:
    print("idxmax with an all-NaN group raises ValueError:", e)
ok = emp.dropna(subset=["salary"])
print("idxmax on non-null rows returns only first tied row:", emp.loc[ok.groupby("dept_id")["salary"].idxmax(), "name"].tolist())
print("asserts passed: MAX OVER == RANK (NULLs filtered) == pandas mask")
```

**Output (my run):**
```text
MAX() OVER:
 emp_id name  dept_id  salary
      1 Asha       10      70
      2  Ben       10      70
      4  Dev       20      90
      8 Hari       40      55

RANK() = 1 (no NULL filter):
 emp_id  name  dept_id  salary
      1  Asha       10    70.0
      2   Ben       10    70.0
      4   Dev       20    90.0
      7 Farid       30     NaN
      8  Hari       40    55.0

RANK() = 1 with salary IS NOT NULL:
 emp_id name  dept_id  salary
      1 Asha       10      70
      2  Ben       10      70
      4  Dev       20      90
      8 Hari       40      55

MAX == safe RANK: True | MAX == plain RANK: False

pandas transform('max') mask:
 emp_id name  dept_id  salary
      1 Asha       10    70.0
      2  Ben       10    70.0
      4  Dev       20    90.0
      8 Hari       40    55.0

pandas rank(method='min', ascending=False) == 1: ['Asha', 'Ben', 'Dev', 'Hari'] (NaN rank is NaN, so Farid is out)
idxmax with an all-NaN group raises ValueError: idxmax with skipna=True encountered all NA values in a group.
idxmax on non-null rows returns only first tied row: ['Asha', 'Dev', 'Hari']
asserts passed: MAX OVER == RANK (NULLs filtered) == pandas mask
```

**Edge cases:**
- All-NULL department: `MAX` version returns nobody; plain `RANK` returns the NULL row. So the premise "they give the same rows" holds for ties but not for an all-NULL group unless you filter.
- NULL among real values: `MAX` ignores it. For `RANK`, where NULL sorts depends on the engine: SQLite treats NULL as smallest, so it is last under `DESC`. PostgreSQL treats NULL as largest by default, so a NULL could rank first under `DESC` (from memory, not executed here); `ORDER BY salary DESC NULLS LAST` makes it explicit and ran on SQLite 3.45 in my probe.
- Ties: both keep every tied row.
- One-employee department: returned by both.

**Then explain:**
- **Which reads better:** `MAX` says exactly what is meant ("equals the department maximum") and has no ranking concept to explain. `RANK` generalises to "top 3" (Q26). I choose by whether the question might become top N.
- **Cost:** both compute one window pass per partition; I did not time them.
- **pandas:** `transform("max")` gives the department maximum per row, so `==` keeps ties. NaN never equals NaN in pandas either, so the all-NaN department is excluded, matching the `MAX` version.
- **idxmax contrast:** `idxmax` returns one row label per group, the first row holding the maximum, so a tie loses a row (the run returns Asha but not Ben). On pandas 3.0.5 it also raises a `ValueError` when a group is all NaN (shown in the run), so drop the NaN rows first.

**Follow-ups:**
- *Show the employee next to the max?* Keep `dept_max` in the select list.
- *Exactly one per department?* `ROW_NUMBER` with a tie-break (Q4, Q20).
- *`QUALIFY`?* Some engines let you filter on a window directly (Snowflake, BigQuery, Teradata, from memory, not executed here); SQLite does not.

**Common mistakes:**
- Using `idxmax` and silently losing tied employees.
- Not filtering NULL salaries in the `RANK` version.
- Writing `WHERE salary = MAX(salary) OVER (...)` in the same query (windows are not allowed in `WHERE`).
- Using `groupby().max()` and merging back without thinking about NULL keys.

### Q18 ⭐⭐⭐ 🟡 Rank users by activity: events(event_id, user_id, event_time). Rank users by number of events (most active first), show ties sharing a rank with RANK and consecutive ranks with DENSE_RANK, and return the top 5 including ties. Explain count-then-rank structure, adding a tie-breaker when you need exactly five, and give the pandas value_counts or groupby size then rank(method='min', ascending=False) version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Count events per user in a CTE, then rank the counts: `RANK()` gives tied users the same number and skips (1, 2, 2, 4), `DENSE_RANK()` does not skip (1, 2, 2, 3), and "top 5 including ties" is `RANK() <= 5` in an outer query; for exactly five rows add a unique tie-breaker and use `ROW_NUMBER`.

**Schema and sample data:** 21 events for seven users, with counts 5, 4, 4, 3, 2, 2, 1.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
INSERT INTO events VALUES
 (1,1,'2024-01-01'),(2,1,'2024-01-02'),(3,1,'2024-01-03'),(4,1,'2024-01-04'),(5,1,'2024-01-05'),
 (6,2,'2024-01-01'),(7,2,'2024-01-02'),(8,2,'2024-01-03'),(9,2,'2024-01-04'),
 (10,3,'2024-01-01'),(11,3,'2024-01-02'),(12,3,'2024-01-03'),(13,3,'2024-01-04'),
 (14,4,'2024-01-01'),(15,4,'2024-01-02'),(16,4,'2024-01-03'),
 (17,5,'2024-01-01'),(18,5,'2024-01-02'),
 (19,6,'2024-01-01'),(20,6,'2024-01-02'),
 (21,7,'2024-01-01');
```

**SQL answer:** `SQL_MAIN` shows all three rankings; `SQL_TOP5` and `SQL_EXACT5` are the two answers (Code block).
```sql
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events,
         RANK() OVER (ORDER BY n_events DESC) AS rnk,
         DENSE_RANK() OVER (ORDER BY n_events DESC) AS dense_rnk,
         ROW_NUMBER() OVER (ORDER BY n_events DESC, user_id) AS rn
  FROM counts
)
SELECT user_id, n_events, rnk, dense_rnk, rn
FROM ranked
ORDER BY rn
```
```sql
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events, RANK() OVER (ORDER BY n_events DESC) AS rnk
  FROM counts
)
SELECT user_id, n_events, rnk FROM ranked WHERE rnk <= 5 ORDER BY rnk, user_id
```

**pandas answer:** count with `groupby().size()`, rank the counts with `method="min"` (same as `RANK`) and `"dense"` (same as `DENSE_RANK`), filter.
```python
counts = ev.groupby("user_id").size().rename("n_events").reset_index()
counts["rnk"] = counts["n_events"].rank(method="min", ascending=False).astype(int)
counts["dense_rnk"] = counts["n_events"].rank(method="dense", ascending=False).astype(int)
pd_all = counts.sort_values(["n_events", "user_id"], ascending=[False, True]).reset_index(drop=True)
pd_all["rn"] = pd_all.index + 1
pd_top5 = pd_all.loc[pd_all["rnk"] <= 5, ["user_id", "n_events", "rnk"]].reset_index(drop=True)
pd_exact = pd_all.head(5)[["user_id", "n_events", "rn"]]
```

**Example:**
- Counts: user 1 has 5, users 2 and 3 have 4, user 4 has 3, users 5 and 6 have 2, user 7 has 1.
- `RANK`: 1, 2, 2, 4, 5, 5, 7. Users 2 and 3 share 2, the next is 4 (gap). Users 5 and 6 share 5.
- `DENSE_RANK`: 1, 2, 2, 3, 4, 4, 5. No gaps.
- Top 5 with `RANK <= 5`: users 1 to 6 (six rows), because users 5 and 6 are both rank 5. User 7 has rank 7 and is out.
- Exactly five with `ROW_NUMBER` and tie-break `user_id`: users 1, 2, 3, 4, 5. User 6 is dropped only because its id is larger than 5's.

**Code:** run with `python3 -I`.
```python
# Q18: rank users by number of events
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
INSERT INTO events VALUES
 (1,1,'2024-01-01'),(2,1,'2024-01-02'),(3,1,'2024-01-03'),(4,1,'2024-01-04'),(5,1,'2024-01-05'),
 (6,2,'2024-01-01'),(7,2,'2024-01-02'),(8,2,'2024-01-03'),(9,2,'2024-01-04'),
 (10,3,'2024-01-01'),(11,3,'2024-01-02'),(12,3,'2024-01-03'),(13,3,'2024-01-04'),
 (14,4,'2024-01-01'),(15,4,'2024-01-02'),(16,4,'2024-01-03'),
 (17,5,'2024-01-01'),(18,5,'2024-01-02'),
 (19,6,'2024-01-01'),(20,6,'2024-01-02'),
 (21,7,'2024-01-01');
"""
SQL_MAIN = """
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events,
         RANK() OVER (ORDER BY n_events DESC) AS rnk,
         DENSE_RANK() OVER (ORDER BY n_events DESC) AS dense_rnk,
         ROW_NUMBER() OVER (ORDER BY n_events DESC, user_id) AS rn
  FROM counts
)
SELECT user_id, n_events, rnk, dense_rnk, rn
FROM ranked
ORDER BY rn
"""
SQL_TOP5 = """
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events, RANK() OVER (ORDER BY n_events DESC) AS rnk
  FROM counts
)
SELECT user_id, n_events, rnk FROM ranked WHERE rnk <= 5 ORDER BY rnk, user_id
"""
SQL_EXACT5 = """
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events, ROW_NUMBER() OVER (ORDER BY n_events DESC, user_id) AS rn
  FROM counts
)
SELECT user_id, n_events, rn FROM ranked WHERE rn <= 5 ORDER BY rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_all = pd.read_sql_query(SQL_MAIN, con)
sql_top5 = pd.read_sql_query(SQL_TOP5, con)
sql_exact = pd.read_sql_query(SQL_EXACT5, con)
print("All users ranked:"); print(sql_all.to_string(index=False))
print("\nTop 5 including ties (RANK <= 5):"); print(sql_top5.to_string(index=False))
print("\nExactly five (ROW_NUMBER, tie-break user_id):"); print(sql_exact.to_string(index=False))
print("\nDENSE_RANK <= 5 would return", int((sql_all["dense_rnk"] <= 5).sum()), "users")

ev = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
counts = ev.groupby("user_id").size().rename("n_events").reset_index()
counts["rnk"] = counts["n_events"].rank(method="min", ascending=False).astype(int)
counts["dense_rnk"] = counts["n_events"].rank(method="dense", ascending=False).astype(int)
pd_all = counts.sort_values(["n_events", "user_id"], ascending=[False, True]).reset_index(drop=True)
pd_all["rn"] = pd_all.index + 1
pd_top5 = pd_all.loc[pd_all["rnk"] <= 5, ["user_id", "n_events", "rnk"]].reset_index(drop=True)
pd_exact = pd_all.head(5)[["user_id", "n_events", "rn"]]
# pd:end
print("\npandas value_counts:", ev["user_id"].value_counts().sort_index().tolist())
# compared in rn order (most events first, then user_id)
pd.testing.assert_frame_equal(sql_all, pd_all[["user_id", "n_events", "rnk", "dense_rnk", "rn"]], check_dtype=False)
pd.testing.assert_frame_equal(sql_top5, pd_top5, check_dtype=False)
pd.testing.assert_frame_equal(sql_exact, pd_exact.reset_index(drop=True), check_dtype=False)
print("asserts passed: SQL == pandas for ranks, top 5 with ties and exactly five")
```

**Output (my run):**
```text
All users ranked:
 user_id  n_events  rnk  dense_rnk  rn
       1         5    1          1   1
       2         4    2          2   2
       3         4    2          2   3
       4         3    4          3   4
       5         2    5          4   5
       6         2    5          4   6
       7         1    7          5   7

Top 5 including ties (RANK <= 5):
 user_id  n_events  rnk
       1         5    1
       2         4    2
       3         4    2
       4         3    4
       5         2    5
       6         2    5

Exactly five (ROW_NUMBER, tie-break user_id):
 user_id  n_events  rn
       1         5   1
       2         4   2
       3         4   3
       4         3   4
       5         2   5

DENSE_RANK <= 5 would return 7 users

pandas value_counts: [5, 4, 4, 3, 2, 2, 1]
asserts passed: SQL == pandas for ranks, top 5 with ties and exactly five
```

**Edge cases:**
- Ties at the cutoff: the tied users 5 and 6 are both returned with `RANK <= 5`; "top 5" then returns six rows. If a downstream step needs exactly five, say so and pick a tie-break.
- `DENSE_RANK <= 5` would return all seven users here (the run prints 7) because there are only five distinct counts.
- Users with zero events do not appear: they have no rows to count. Join to a users table with `LEFT JOIN` and `COUNT(e.event_id)` if they should be ranked at 0.
- Empty events table: the CTE is empty, so the query returns no rows.

**Then explain:**
- **Count then rank:** `RANK() OVER (ORDER BY COUNT(*) DESC)` in the same `GROUP BY` query also works in SQLite because windows are evaluated after grouping, but the CTE form is easier to read and to extend.
- **Tie-breaker for exactly five:** the choice (lowest user_id, earliest first event, and so on) is a business rule, and I state it.
- **pandas:** `rank(method="min", ascending=False)` returns floats, so I cast to int. `value_counts()` sorts by count but its order among equal counts is not something I rely on; I sort by `n_events` and `user_id` explicitly.

**Follow-ups:**
- *Top 5 per country?* Add `PARTITION BY country` to the window and join the user's country (Q4 pattern).
- *Rank by distinct days active?* `COUNT(DISTINCT date(event_time))`.
- *Use `LIMIT 5`?* That gives exactly five with an arbitrary tie rule unless `ORDER BY` includes a tie-break.

**Common mistakes:**
- Ranking raw events instead of counts.
- `LIMIT 5` without a tie-break, then claiming "top 5 including ties".
- Using `ROW_NUMBER` and silently dropping tied users.
- Forgetting `ascending=False` in pandas `rank` (rank 1 would be the least active).

### Q19 ⭐⭐⭐ 🔴 FIRST_VALUE, LAST_VALUE and the default-frame trap: products(product_id, category, name, price). For each product show the cheapest and the most expensive product name in its category using FIRST_VALUE and LAST_VALUE over (PARTITION BY category ORDER BY price). Show that LAST_VALUE returns the current row's own value (or its ties) under the default frame, explain that the default frame with ORDER BY is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, and fix it with ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING or by reversing the ORDER BY. Give the pandas groupby transform('first') / transform('last') after sorting.
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** With `ORDER BY` in the window, the default frame ends at the current row (and its peers), so `LAST_VALUE` just returns the current row's own value; fix it with `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, or get the same answer from `FIRST_VALUE` over the reversed order.

**Schema and sample data:** six products, Fruit has two items at price 20 (Banana, Cherry) to show peers.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Veg','Okra',25);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_PEERS` shows the peer behaviour.
```sql
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS priciest_default,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS priciest_fixed,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price DESC, product_id DESC) AS priciest_rev
FROM products
ORDER BY product_id
```

**pandas answer:** sort, then take the first and last name of each group with `transform`.
```python
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
g = s.groupby("category")["name"]
pd_df = s.assign(cheapest=g.transform("first"), priciest_fixed=g.transform("last"))
```

**Example:**
- Fruit sorted by price, product_id: Banana (20), Cherry (20), Apple (30), Date (50). Veg: Leek (10), Okra (25).
- `FIRST_VALUE(name)`: Banana for every Fruit row, Leek for every Veg row. Correct.
- `LAST_VALUE(name)` with the default frame: the frame for Banana is just Banana (start to current row), so it returns Banana; Cherry returns Cherry; Apple returns Apple; Date returns Date. Each row sees itself, never the group's last row. Same for Veg.
- With `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, the frame is the whole category, so every Fruit row gets Date and every Veg row gets Okra.
- Reversed order: `FIRST_VALUE(name)` over `ORDER BY price DESC, product_id DESC` gives the same Date and Okra, with no frame clause needed.
- Peers: if the window orders by `price` only, Banana and Cherry are peers (same price). The default frame is a RANGE frame, so a row's frame includes all its peers: `COUNT(*)` over that frame is 2 for both Banana and Cherry (the run shows it), not 1 and 2. So a peer can see a later tied row. I printed a count rather than a name because which tied name comes last is unspecified.

**Code:** run with `python3 -I`.
```python
# Q19: FIRST_VALUE, LAST_VALUE and the default-frame trap
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Veg','Okra',25);
"""
SQL_MAIN = """
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS priciest_default,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS priciest_fixed,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price DESC, product_id DESC) AS priciest_rev
FROM products
ORDER BY product_id
"""
SQL_PEERS = """
SELECT product_id, name, price,
       COUNT(*) OVER (PARTITION BY category ORDER BY price) AS rows_in_frame
FROM products WHERE category = 'Fruit'
ORDER BY product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))
print("\nPeers under the default frame (price only in ORDER BY):")
print(pd.read_sql_query(SQL_PEERS, con).to_string(index=False))

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
g = s.groupby("category")["name"]
pd_df = s.assign(cheapest=g.transform("first"), priciest_fixed=g.transform("last"))
# pd:end
print("\npandas:"); print(pd_df.sort_values("product_id").to_string(index=False))
cols = ["product_id", "category", "name", "price", "cheapest"]
# compared after sorting by product_id
pd.testing.assert_frame_equal(sql_df[cols], pd_df.sort_values("product_id").reset_index(drop=True)[cols], check_dtype=False)
assert sql_df["priciest_fixed"].tolist() == pd_df.sort_values("product_id")["priciest_fixed"].tolist()
assert sql_df["priciest_rev"].tolist() == sql_df["priciest_fixed"].tolist()
assert sql_df["priciest_default"].tolist() == sql_df["name"].tolist()   # default frame: last_value is the row itself here
print("\nasserts passed: fixed frame == reversed order == pandas 'last'; default LAST_VALUE equals the row's own name")
```

**Output (my run):**
```text
SQL:
 product_id category   name  price cheapest priciest_default priciest_fixed priciest_rev
          1    Fruit  Apple     30   Banana            Apple           Date         Date
          2    Fruit Banana     20   Banana           Banana           Date         Date
          3    Fruit Cherry     20   Banana           Cherry           Date         Date
          4    Fruit   Date     50   Banana             Date           Date         Date
          5      Veg   Leek     10     Leek             Leek           Okra         Okra
          6      Veg   Okra     25     Leek             Okra           Okra         Okra

Peers under the default frame (price only in ORDER BY):
 product_id   name  price  rows_in_frame
          1  Apple     30              3
          2 Banana     20              2
          3 Cherry     20              2
          4   Date     50              4

pandas:
 product_id category   name  price cheapest priciest_fixed
          1    Fruit  Apple     30   Banana           Date
          2    Fruit Banana     20   Banana           Date
          3    Fruit Cherry     20   Banana           Date
          4    Fruit   Date     50   Banana           Date
          5      Veg   Leek     10     Leek           Okra
          6      Veg   Okra     25     Leek           Okra

asserts passed: fixed frame == reversed order == pandas 'last'; default LAST_VALUE equals the row's own name
```

**Edge cases:**
- Ties on price: the cheapest name depends on the tie-break; I added `product_id` so the answer is fixed. Without it, which tied product is "first" is unspecified.
- NULL price: SQLite sorts NULL first in ascending order, so a NULL-priced product would be "cheapest". Filter NULL prices first or use `ORDER BY price NULLS LAST` (ran on SQLite 3.45). Other engines default differently (not executed here).
- One product in a category: first and last are that product.
- `FIRST_VALUE` is not affected by the trap because the default frame always starts at the partition start.

**Then explain:**
- **Default frame:** when the window has `ORDER BY` and no frame clause, it is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`; without `ORDER BY` it is the whole partition. SQLite documents this default.
- **Two fixes:** an explicit full frame, or reverse the order and use `FIRST_VALUE`. I prefer the explicit frame because it states intent.
- **ROWS versus RANGE:** `ROWS` counts physical rows, `RANGE` includes all peers (rows tied on the `ORDER BY` key).
- **pandas:** there is no frame, just sort, then `transform("first")` and `transform("last")`. The sort is the whole definition of "first".

**Follow-ups:**
- *Price difference from the cheapest?* `price - FIRST_VALUE(price) OVER (...)`.
- *Why not `MIN`/`MAX`?* They give the price but not the name; for names you need the value functions or a join.
- *Does the same trap hit `NTH_VALUE`?* Yes, it is also frame-sensitive (Q23).

**Common mistakes:**
- Using `LAST_VALUE` with the default frame and getting "the current row" back.
- Reversing the order but forgetting the tie-break.
- Forgetting to sort in pandas before `first`/`last`.

### Q20 ⭐⭐ 🟢 Choosing the ranking function from the requirement: for each requirement below state ROW_NUMBER, RANK or DENSE_RANK and show it on employees(emp_id, name, dept_id, salary) with ties: 'exactly one row per department', 'everyone tied for the top', 'top three salary levels', 'second highest salary', 'number every row for pagination', 'leaderboard with shared positions and gaps'. Explain the reasoning in one line each and give the pandas rank(method=...) mapping.
**Asked at:** GeeksforGeeks SQL interview questions (RANK vs DENSE_RANK vs ROW_NUMBER, window functions, duplicates entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** `ROW_NUMBER` when you need exactly N rows or a unique number, `RANK` when tied rows should share a place and the next place is skipped, `DENSE_RANK` when you count distinct values (salary levels) with no gaps.

**Schema and sample data:** eight employees; Asha and Ben tie at 90, Dev and Esha tie at 70 in dept 10; Gita and Hari tie at 50 in dept 20.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',10,70),(6,'Farid',20,60),(7,'Gita',20,50),(8,'Hari',20,50);
```

**SQL answer:** `SQL_MAIN` computes all three functions (Code block). The requirements below filter it.
```sql
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dr
FROM employees
ORDER BY dept_id, rn
```

**pandas answer:** `rank` with `method="first"` / `"min"` / `"dense"` maps to `ROW_NUMBER` / `RANK` / `DENSE_RANK`. I get `ROW_NUMBER` with `cumcount` after an explicit sort so ties are deterministic.
```python
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int))
```

**Example:** dept 10, salary descending: Asha 90, Ben 90, Chitra 80, Dev 70, Esha 70. `ROW_NUMBER` with tie-break `emp_id`: 1, 2, 3, 4, 5. `RANK`: 1, 1, 3, 4, 4. `DENSE_RANK`: 1, 1, 2, 3, 3. Dept 20: Farid 60, Gita 50, Hari 50: `RANK` 1, 2, 2; `DENSE_RANK` 1, 2, 2.

| Requirement | Function and filter | Reason, one line | pandas |
|---|---|---|---|
| Exactly one row per department | `ROW_NUMBER`, `rn = 1` | Always one row per partition; the tie-break decides who. | `rank(method="first")` after sorting, or `head(1)` |
| Everyone tied for the top | `RANK`, `rk = 1` | Tied rows share rank 1. | `rank(method="min") == 1` |
| Top three salary levels | `DENSE_RANK`, `dr <= 3` | Counts distinct salaries, so ties do not use up places. | `rank(method="dense") <= 3` |
| Second highest salary | `DENSE_RANK`, `dr = 2` | `RANK = 2` returns nothing when two people tie for first. | `rank(method="dense") == 2` |
| Number every row for pagination | `ROW_NUMBER` over a total order | Unique and gapless, so pages never repeat or skip a row. | `reset_index` after sort, then slice |
| Leaderboard with shared positions and gaps | `RANK` | Competition style: 1, 1, 3. | `rank(method="min")` |

**Code:** run with `python3 -I`.
```python
# Q20: choosing the ranking function from the requirement
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',10,70),(6,'Farid',20,60),(7,'Gita',20,50),(8,'Hari',20,50);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dr
FROM employees
ORDER BY dept_id, rn
"""
SQL_PAGE = """
SELECT name, salary FROM (
  SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn FROM employees)
WHERE rn BETWEEN 4 AND 6
ORDER BY rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in dept_id, rn order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

pick = {
    "exactly one row per department (rn = 1)": sql_df[sql_df.rn == 1]["name"].tolist(),
    "everyone tied for the top (rk = 1)": sql_df[sql_df.rk == 1]["name"].tolist(),
    "top three salary levels (dr <= 3)": sql_df[sql_df.dr <= 3]["name"].tolist(),
    "second highest salary (dr = 2)": sql_df[sql_df.dr == 2]["name"].tolist(),
    "leaderboard with gaps (rk)": list(zip(sql_df["name"], sql_df["rk"])),
}
print()
for k, v in pick.items():
    print(k, "->", v)
print("pagination, page 2 of size 3 over the whole table (global ROW_NUMBER, rn 4..6):")
print(pd.read_sql_query(SQL_PAGE, con).to_string(index=False))
# the pandas 'first' method numbers ties in order of appearance, which is only deterministic after sorting
first = s.groupby("dept_id")["salary"].rank(method="first", ascending=False).astype(int)
assert first.tolist() == pd_df["rn"].tolist()
print("\nasserts passed: SQL == pandas; rank(method='first') on sorted data == ROW_NUMBER")
```

**Output (my run):**
```text
SQL:
 emp_id   name  dept_id  salary  rn  rk  dr
      1   Asha       10      90   1   1   1
      2    Ben       10      90   2   1   1
      3 Chitra       10      80   3   3   2
      4    Dev       10      70   4   4   3
      5   Esha       10      70   5   4   3
      6  Farid       20      60   1   1   1
      7   Gita       20      50   2   2   2
      8   Hari       20      50   3   2   2

pandas:
 emp_id   name  dept_id  salary  rn  rk  dr
      1   Asha       10      90   1   1   1
      2    Ben       10      90   2   1   1
      3 Chitra       10      80   3   3   2
      4    Dev       10      70   4   4   3
      5   Esha       10      70   5   4   3
      6  Farid       20      60   1   1   1
      7   Gita       20      50   2   2   2
      8   Hari       20      50   3   2   2

exactly one row per department (rn = 1) -> ['Asha', 'Farid']
everyone tied for the top (rk = 1) -> ['Asha', 'Ben', 'Farid']
top three salary levels (dr <= 3) -> ['Asha', 'Ben', 'Chitra', 'Dev', 'Esha', 'Farid', 'Gita', 'Hari']
second highest salary (dr = 2) -> ['Chitra', 'Gita', 'Hari']
leaderboard with gaps (rk) -> [('Asha', 1), ('Ben', 1), ('Chitra', 3), ('Dev', 4), ('Esha', 4), ('Farid', 1), ('Gita', 2), ('Hari', 2)]
pagination, page 2 of size 3 over the whole table (global ROW_NUMBER, rn 4..6):
 name  salary
  Dev      70
 Esha      70
Farid      60

asserts passed: SQL == pandas; rank(method='first') on sorted data == ROW_NUMBER
```

**Edge cases:**
- Without a tie-break, `ROW_NUMBER` still assigns 1..n but the order among tied rows is unspecified, so I always add `emp_id` (shown here).
- Second highest salary with `RANK = 2`: dept 10 has two people at 90, so `RANK` goes 1, 1, 3 and `rk = 2` returns no one; `dr = 2` correctly returns Chitra.
- NULL salary: SQLite sorts NULL last under `DESC` (smallest), so NULL rows rank last; other engines can differ (not executed here), and pandas `rank` leaves NaN unranked by default (`na_option="keep"`).
- Pagination over the whole table needs a total order; the page query in the run uses `salary DESC, emp_id`.

**Then explain:**
- Three questions pick the function: do ties need separate numbers (`ROW_NUMBER`), do I need the gap after a tie (`RANK`), do I count distinct values (`DENSE_RANK`).
- **pandas methods:** `rank` returns floats, so I cast to int. `method="first"` numbers ties in the order rows appear, which is why I sort first.
- For huge offsets, keyset pagination (`WHERE (salary, emp_id) < (?, ?)`) is better than numbering every row; not executed here.

**Follow-ups:**
- *Which one for "top 3 earners" if the business says "3 people"?* Ask; `ROW_NUMBER` gives exactly three, `RANK` may give more (Q26).
- *Percent rank?* `PERCENT_RANK`, Q22.
- *Do the functions ignore `PARTITION BY` by default?* Without it, the whole result is one partition.

**Common mistakes:**
- `RANK = 2` for the second highest salary.
- `ROW_NUMBER` without a tie-break and treating the order as stable.
- Forgetting `ascending=False` in pandas.
- Using `RANK` for pagination: gaps and repeats make page boundaries wrong.

### Q21 ⭐⭐ 🟢 NTILE: bucket customers into quartiles by total spend. customers(customer_id, name) and orders(order_id, customer_id, amount). Compute each customer's total, then NTILE(4) OVER (ORDER BY total DESC) so bucket 1 is the top spenders. Show what happens when the row count does not divide evenly (SQLite: larger groups come first) and say what ordering direction does to bucket meaning. Give the pandas version (rank then qcut or a computed bucket) and note NTILE is positional.
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Total spend per customer in a CTE, then `NTILE(4) OVER (ORDER BY total DESC)`; bucket 1 is the top quarter, ten customers split 3, 3, 2, 2 (larger groups first), and NTILE is purely positional, so customers with equal totals can land in different buckets.

**Schema and sample data:** ten customers; Jai has no orders. Ben and Chitra tie at 400, and Hari and Ila tie at 100.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),
  (6,'Farid'),(7,'Gita'),(8,'Hari'),(9,'Ila'),(10,'Jai');
INSERT INTO orders VALUES (1,1,300),(2,1,200),(3,2,400),(4,3,250),(5,3,150),(6,4,300),
  (7,5,250),(8,6,100),(9,6,100),(10,7,150),(11,8,100),(12,9,60),(13,9,40);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_ASC` is the ascending variant.
```sql
WITH totals AS (
  SELECT c.customer_id, c.name, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, total,
       NTILE(4) OVER (ORDER BY total DESC, customer_id) AS quartile
FROM totals
ORDER BY total DESC, customer_id
```

**pandas answer:** sort by total (with a tie-break), then compute the bucket from the 0-based position with the same rule SQLite uses: with n rows and k buckets, the first `n % k` buckets get one extra row. `pd.qcut` is shown in the run as a contrast, not as the equivalent.
```python
def ntile(pos0, n, k):
    # pos0 = 0-based position; the first n % k buckets get one extra row (SQLite and most engines)
    q, r = divmod(n, k)
    cut = r * (q + 1)
    return pos0 // (q + 1) + 1 if pos0 < cut else r + (pos0 - cut) // q + 1

tot = (customers.merge(orders.groupby("customer_id", as_index=False).agg(total=("amount", "sum")),
                       on="customer_id", how="left")
       .fillna({"total": 0}).astype({"total": "int64"}))
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
tot["quartile"] = [ntile(i, len(tot), 4) for i in range(len(tot))]
pd_df = tot
```

**Example:**
- Totals: Asha 500, Ben 400, Chitra 400, Dev 300, Esha 250, Farid 200, Gita 150, Hari 100, Ila 100, Jai 0 (no orders, so `COALESCE` gives 0).
- 10 rows into 4 buckets is 2 each plus 2 left over, and the first two buckets get the extra row: sizes 3, 3, 2, 2.
- Sorted by total descending, then customer_id: positions 1 to 3 (Asha, Ben, Chitra) are bucket 1; 4 to 6 (Dev, Esha, Farid) bucket 2; 7 and 8 (Gita, Hari) bucket 3; 9 and 10 (Ila, Jai) bucket 4.
- Hari and Ila both spent 100, yet Hari is in bucket 3 and Ila in bucket 4. That is the positional nature of NTILE: the tie-break (customer_id) decides.
- With ascending order bucket 1 would mean the lowest spenders, and the extra rows would go to the low buckets (the run shows Ben and Chitra, tied at 400, landing in buckets 3 and 4).

**Code:** run with `python3 -I`.
```python
# Q21: NTILE quartiles by total spend
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),
  (6,'Farid'),(7,'Gita'),(8,'Hari'),(9,'Ila'),(10,'Jai');
INSERT INTO orders VALUES (1,1,300),(2,1,200),(3,2,400),(4,3,250),(5,3,150),(6,4,300),
  (7,5,250),(8,6,100),(9,6,100),(10,7,150),(11,8,100),(12,9,60),(13,9,40);
"""
SQL_MAIN = """
WITH totals AS (
  SELECT c.customer_id, c.name, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, total,
       NTILE(4) OVER (ORDER BY total DESC, customer_id) AS quartile
FROM totals
ORDER BY total DESC, customer_id
"""
SQL_ASC = """
WITH totals AS (
  SELECT c.customer_id, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id
)
SELECT customer_id, total, NTILE(4) OVER (ORDER BY total, customer_id) AS quartile_asc
FROM totals
ORDER BY total DESC, customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL NTILE(4), bucket 1 = top spenders:"); print(sql_df.to_string(index=False))
print("\nbucket sizes:", sql_df["quartile"].value_counts().sort_index().tolist())
asc = pd.read_sql_query(SQL_ASC, con)
print("\nSame with ascending order (bucket 1 = lowest spenders):", asc["quartile_asc"].tolist())

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
def ntile(pos0, n, k):
    # pos0 = 0-based position; the first n % k buckets get one extra row (SQLite and most engines)
    q, r = divmod(n, k)
    cut = r * (q + 1)
    return pos0 // (q + 1) + 1 if pos0 < cut else r + (pos0 - cut) // q + 1

tot = (customers.merge(orders.groupby("customer_id", as_index=False).agg(total=("amount", "sum")),
                       on="customer_id", how="left")
       .fillna({"total": 0}).astype({"total": "int64"}))
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
tot["quartile"] = [ntile(i, len(tot), 4) for i in range(len(tot))]
pd_df = tot
# pd:end
print("\npandas positional NTILE:"); print(pd_df.to_string(index=False))
# compared in total DESC, customer_id order
pd.testing.assert_frame_equal(sql_df, pd_df[["customer_id", "name", "total", "quartile"]], check_dtype=False)

# contrast: qcut cuts by VALUE quantiles, so equal values stay together and sizes are not forced
qc = 4 - pd.qcut(pd_df["total"], 4, labels=False)
pd_df = pd_df.assign(qcut_bucket=qc)
print("\nqcut (relabelled so 1 = top):"); print(pd_df[["name", "total", "quartile", "qcut_bucket"]].to_string(index=False))
print("qcut bucket sizes:", pd_df["qcut_bucket"].value_counts().sort_index().tolist())
diff = pd_df[pd_df["quartile"] != pd_df["qcut_bucket"]]["name"].tolist()
print("customers where NTILE and qcut disagree:", diff)
print("asserts passed: SQL NTILE == pandas positional version")
```

**Output (my run):**
```text
SQL NTILE(4), bucket 1 = top spenders:
 customer_id   name  total  quartile
           1   Asha    500         1
           2    Ben    400         1
           3 Chitra    400         1
           4    Dev    300         2
           5   Esha    250         2
           6  Farid    200         2
           7   Gita    150         3
           8   Hari    100         3
           9    Ila    100         4
          10    Jai      0         4

bucket sizes: [3, 3, 2, 2]

Same with ascending order (bucket 1 = lowest spenders): [4, 3, 4, 3, 2, 2, 2, 1, 1, 1]

pandas positional NTILE:
 customer_id   name  total  quartile
           1   Asha    500         1
           2    Ben    400         1
           3 Chitra    400         1
           4    Dev    300         2
           5   Esha    250         2
           6  Farid    200         2
           7   Gita    150         3
           8   Hari    100         3
           9    Ila    100         4
          10    Jai      0         4

qcut (relabelled so 1 = top):
  name  total  quartile  qcut_bucket
  Asha    500         1            1
   Ben    400         1            1
Chitra    400         1            1
   Dev    300         2            2
  Esha    250         2            2
 Farid    200         2            3
  Gita    150         3            3
  Hari    100         3            4
   Ila    100         4            4
   Jai      0         4            4
qcut bucket sizes: [3, 2, 2, 3]
customers where NTILE and qcut disagree: ['Farid', 'Hari']
asserts passed: SQL NTILE == pandas positional version
```

**Edge cases:**
- Customers with no orders: the `LEFT JOIN` plus `COALESCE` keeps them as 0 spend (Jai). An inner join would drop them and change the bucket sizes. Whether non-buyers belong in the quartiles is a business decision; say it.
- Ties: NTILE can split equal totals across buckets; if equal totals must share a bucket, use `qcut`-style value thresholds or `PERCENT_RANK`/`CUME_DIST` (Q22) and bucket on those.
- Fewer rows than buckets (for example 3 customers, `NTILE(4)`): the first three buckets get one row each and bucket 4 is empty, from SQLite's documented behaviour; I did not run it here.
- NULL total: not possible after `COALESCE`; with a NULL, SQLite would sort it last under `DESC`.

**Then explain:**
- **Uneven split:** SQLite puts the larger groups first, as documented and shown in the run (3, 3, 2, 2). I believe other engines do the same, but that is not executed here.
- **Direction:** `ORDER BY total DESC` makes bucket 1 the best; `ASC` flips the meaning. I name the column (`top_quartile`) so nobody misreads it.
- **qcut versus NTILE:** the run shows `qcut` sizes 3, 2, 2, 3 against NTILE's 3, 3, 2, 2, and they disagree for Farid and Hari. `qcut` computes quantile edges from the values and puts each value into a bin, so Hari and Ila (both 100) share a bin; NTILE counts positions and splits them.
- **pandas:** there is no built-in NTILE. A positional formula (above) reproduces it exactly, which the run asserts; `rank(method="first")` then integer arithmetic is the other common route.

**Follow-ups:**
- *Average spend per quartile?* Group the result by `quartile`.
- *Deciles?* `NTILE(10)`.
- *Quartile within each region?* Add `PARTITION BY region`.

**Common mistakes:**
- Forgetting the tie-break, so bucket membership of tied customers is arbitrary.
- Reading NTILE as "value thresholds" instead of "equal counts".
- Inner join dropping customers with no orders.
- Using `pd.qcut` and expecting it to match NTILE exactly.

### Q22 ⭐⭐ 🟢 PERCENT_RANK and CUME_DIST: scores(student_id, score) with ties. Show RANK, PERCENT_RANK (rank-1)/(n-1) and CUME_DIST (rows up to and including the last peer / n) side by side, explain the one-row partition (PERCENT_RANK is 0.0) and what each one means in words ('percentage of rows below you' versus 'at or below you'), and give the pandas rank(pct=True) comparison.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `PERCENT_RANK` is (rank - 1) / (n - 1), the share of rows strictly below you (0 for the lowest, 1 for the highest); `CUME_DIST` is (rows up to and including your last tie) / n, the share at or below you, and pandas `rank(pct=True, method="max")` equals `CUME_DIST`.

**Schema and sample data:** five scores with a tie at 60, plus a one-row table.
```sql
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,50),(2,60),(3,60),(4,70),(5,90);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
```

**SQL answer:** `SQL_MAIN` uses one named window for all three (Code block); `SQL_SOLO` tests the one-row case.
```sql
SELECT student_id, score,
       RANK() OVER w AS rnk,
       PERCENT_RANK() OVER w AS pct_rank,
       CUME_DIST() OVER w AS cume_dist
FROM scores
WINDOW w AS (ORDER BY score)
ORDER BY score, student_id
```

**pandas answer:** `PERCENT_RANK` from a `method="min"` rank; `CUME_DIST` from `rank(method="max", pct=True)`.
```python
n = len(scores)
rk = scores["score"].rank(method="min")
pd_df = scores.assign(
    rnk=rk.astype(int),
    pct_rank=(rk - 1) / (n - 1),
    cume_dist=scores["score"].rank(method="max", pct=True),
).sort_values(["score", "student_id"]).reset_index(drop=True)
```

**Example:** n = 5; scores 50, 60, 60, 70, 90.
- `RANK`: 1, 2, 2, 4, 5.
- `PERCENT_RANK` = (rank - 1) / 4: 0.0, 0.25, 0.25, 0.75, 1.0.
- `CUME_DIST` = rows at or below / 5: 50 has 1 row so 0.2; both 60s have 3 rows up to the last tie so 0.6; 70 has 4 so 0.8; 90 has 5 so 1.0.
- In words: the score of 70 is above 75 percent of the rows (percent rank) and at or above 80 percent of the rows (cumulative distribution). The two 60s both get 0.6 for `CUME_DIST` because it counts through the last peer.
- One row: `PERCENT_RANK` is 0.0 (SQLite does not divide by zero here), `CUME_DIST` is 1.0.

**Code:** run with `python3 -I`.
```python
# Q22: PERCENT_RANK and CUME_DIST
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,50),(2,60),(3,60),(4,70),(5,90);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
"""
SQL_MAIN = """
SELECT student_id, score,
       RANK() OVER w AS rnk,
       PERCENT_RANK() OVER w AS pct_rank,
       CUME_DIST() OVER w AS cume_dist
FROM scores
WINDOW w AS (ORDER BY score)
ORDER BY score, student_id
"""
SQL_SOLO = """
SELECT student_id, score, PERCENT_RANK() OVER (ORDER BY score) AS pct_rank,
       CUME_DIST() OVER (ORDER BY score) AS cume_dist
FROM solo
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))
print("\nOne-row table:"); print(pd.read_sql_query(SQL_SOLO, con).to_string(index=False))

scores = pd.read_sql_query("SELECT * FROM scores", con)
# pd:main
n = len(scores)
rk = scores["score"].rank(method="min")
pd_df = scores.assign(
    rnk=rk.astype(int),
    pct_rank=(rk - 1) / (n - 1),
    cume_dist=scores["score"].rank(method="max", pct=True),
).sort_values(["score", "student_id"]).reset_index(drop=True)
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in score, student_id order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

print("\nrank(pct=True) default method (average):", scores["score"].rank(pct=True).tolist())
print("rank(pct=True, method='max'):            ", scores["score"].rank(pct=True, method="max").tolist())
one = pd.Series([75])
with np.errstate(all="ignore"):
    print("one row: my pct_rank formula =", ((one.rank(method="min") - 1) / (len(one) - 1)).tolist(),
          "| rank(pct=True) =", one.rank(pct=True).tolist())
manual = [(scores['score'] <= v).sum() / n for v in sql_df['score']]
assert sql_df['cume_dist'].tolist() == manual
print("asserts passed: SQL == pandas; cume_dist == rank(method='max', pct=True)")
```

**Output (my run):**
```text
SQL:
 student_id  score  rnk  pct_rank  cume_dist
          1     50    1      0.00        0.2
          2     60    2      0.25        0.6
          3     60    2      0.25        0.6
          4     70    4      0.75        0.8
          5     90    5      1.00        1.0

One-row table:
 student_id  score  pct_rank  cume_dist
          1     75       0.0        1.0

pandas:
 student_id  score  rnk  pct_rank  cume_dist
          1     50    1      0.00        0.2
          2     60    2      0.25        0.6
          3     60    2      0.25        0.6
          4     70    4      0.75        0.8
          5     90    5      1.00        1.0

rank(pct=True) default method (average): [0.2, 0.5, 0.5, 0.8, 1.0]
rank(pct=True, method='max'):             [0.2, 0.6, 0.6, 0.8, 1.0]
one row: my pct_rank formula = [nan] | rank(pct=True) = [1.0]
asserts passed: SQL == pandas; cume_dist == rank(method='max', pct=True)
```

**Edge cases:**
- One-row partition: SQLite returns 0.0 for `PERCENT_RANK` (the run). My pandas formula gives NaN there because (1-1)/(1-1) is 0/0, so guard it if single-row groups can occur; `rank(pct=True)` on one value is 1.0, which matches `CUME_DIST`, not `PERCENT_RANK`.
- Ties: `PERCENT_RANK` uses the first row of the tie (rank), `CUME_DIST` the last. Surprise from the run: pandas default `rank(pct=True)` uses the average method and gives 0.5 for the tied 60s, which equals neither SQL function. Only `method="max"` matches `CUME_DIST`.
- NULL scores: SQLite orders them first and counts them in n. pandas `rank` leaves NaN unranked and `pct=True` divides by the non-NaN count, so results can differ (I did not run a NULL case here).
- `CUME_DIST` is never 0; `PERCENT_RANK` is always 0 for the first rank.

**Then explain:**
- **Which to use:** "what percent of students scored below me" is `PERCENT_RANK`; "what percentile am I at or below" is `CUME_DIST`. Say which one you mean.
- **Formulas:** both are documented in the SQLite window-function page; the run confirms them on this data.
- **Top 10 percent:** `CUME_DIST() > 0.9` on a descending order, or `PERCENT_RANK`, are the usual filters.

**Follow-ups:**
- *Do they depend on ties?* Yes, as above.
- *Percentile value (median)?* That is `PERCENTILE_CONT`, which is not in SQLite; pandas `quantile` does it.
- *Same as `NTILE`?* No: NTILE equalises counts, these report position.

**Common mistakes:**
- Using pandas `rank(pct=True)` with the default method and expecting `CUME_DIST`.
- Reading `PERCENT_RANK = 1.0` as "100 percent of rows are below you"; it is the top rank.
- Not guarding the single-row group in pandas.

### Q23 ⭐⭐ 🟢 FIRST_VALUE and NTH_VALUE: products(product_id, category, name, price). For each product show the cheapest product's name in its category and the second cheapest, using FIRST_VALUE and NTH_VALUE(name, 2) over (PARTITION BY category ORDER BY price, product_id). Explain that NTH_VALUE returns NULL when the frame has fewer than N rows (and is frame-sensitive, so rows early in the default frame may see NULL), and give the pandas groupby nth or sort and cumcount version.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `FIRST_VALUE(name)` gives the cheapest name for every row, and `NTH_VALUE(name, 2)` gives the second cheapest only for rows whose frame already contains two rows, so with the default frame early rows see NULL; add `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` so every row sees it.

**Schema and sample data:** seven products. Fruit has four (Banana and Cherry tie at 20), Dairy has two, Veg has one.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Dairy','Milk',12),(7,'Dairy','Curd',18);
```

**SQL answer:** `SQL_MAIN` shows `FIRST_VALUE`, the default-frame `NTH_VALUE`, and the full-frame `NTH_VALUE` (Code block).
```sql
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id) AS second_default,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_cheapest
FROM products
ORDER BY product_id
```

**pandas answer:** sort, number with `cumcount`, take the position-2 row per category and map it back.
```python
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
s["pos"] = s.groupby("category").cumcount() + 1
second = s[s["pos"] == 2].set_index("category")["name"]
pd_df = s.assign(cheapest=s.groupby("category")["name"].transform("first"),
                 second_cheapest=s["category"].map(second)).drop(columns="pos")
```

**Example:** ordering inside each category is `price, product_id`.
- Fruit: Banana (20, id 2), Cherry (20, id 3), Apple (30), Date (50). Cheapest is Banana for every row.
- Second cheapest is Cherry (the tie on price is settled by `product_id`).
- Default frame: Banana's frame is just Banana (one row), so `NTH_VALUE(name, 2)` is NULL; Cherry's frame has two rows, so it is Cherry; Apple and Date also see Cherry. That is why the `second_default` column starts with a NULL in each category.
- Full frame: all four Fruit rows show Cherry.
- Dairy: Milk (12), Curd (18): second is Curd. With the default frame, Milk gets NULL, Curd gets Curd.
- Veg: one product, so `NTH_VALUE(name, 2)` is NULL in every case. The run shows NULL there even with the full frame.

**Code:** run with `python3 -I`.
```python
# Q23: FIRST_VALUE and NTH_VALUE
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Dairy','Milk',12),(7,'Dairy','Curd',18);
"""
SQL_MAIN = """
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id) AS second_default,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_cheapest
FROM products
ORDER BY product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))
try:
    con.execute("SELECT NTH_VALUE(name, 2) FROM LAST OVER (ORDER BY price) FROM products").fetchall()
    print("\nFROM LAST accepted")
except sqlite3.Error as e:
    print("\nNTH_VALUE ... FROM LAST on SQLite 3.45:", e)

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
s["pos"] = s.groupby("category").cumcount() + 1
second = s[s["pos"] == 2].set_index("category")["name"]
pd_df = s.assign(cheapest=s.groupby("category")["name"].transform("first"),
                 second_cheapest=s["category"].map(second)).drop(columns="pos")
# pd:end
print("\npandas:"); print(pd_df.sort_values("product_id").to_string(index=False))
cols = ["product_id", "category", "name", "price", "cheapest", "second_cheapest"]
# compared after sorting by product_id
pd.testing.assert_frame_equal(sql_df[cols], pd_df.sort_values("product_id").reset_index(drop=True)[cols], check_dtype=False)
nth = s.groupby("category")["name"].nth(1)
print("\ngroupby().nth(1) returns:", nth.tolist(), "(rows, one per category with at least 2 items)")
assert sorted(nth.tolist()) == sorted(second.tolist())
print("asserts passed: SQL (full frame) == pandas; nth(1) agrees")
```

**Output (my run):**
```text
SQL:
 product_id category   name  price cheapest second_default second_cheapest
          1    Fruit  Apple     30   Banana         Cherry          Cherry
          2    Fruit Banana     20   Banana            NaN          Cherry
          3    Fruit Cherry     20   Banana         Cherry          Cherry
          4    Fruit   Date     50   Banana         Cherry          Cherry
          5      Veg   Leek     10     Leek            NaN             NaN
          6    Dairy   Milk     12     Milk            NaN            Curd
          7    Dairy   Curd     18     Milk           Curd            Curd

NTH_VALUE ... FROM LAST on SQLite 3.45: near "(": syntax error

pandas:
 product_id category   name  price cheapest second_cheapest
          1    Fruit  Apple     30   Banana          Cherry
          2    Fruit Banana     20   Banana          Cherry
          3    Fruit Cherry     20   Banana          Cherry
          4    Fruit   Date     50   Banana          Cherry
          5      Veg   Leek     10     Leek             NaN
          6    Dairy   Milk     12     Milk            Curd
          7    Dairy   Curd     18     Milk            Curd

groupby().nth(1) returns: ['Curd', 'Cherry'] (rows, one per category with at least 2 items)
asserts passed: SQL (full frame) == pandas; nth(1) agrees
```

**Edge cases:**
- Fewer than N rows in the frame: NULL (Veg; also the first row of every category under the default frame).
- Ties in price: without `product_id` the "second" could be either tied product, so I include it.
- NULL price: SQLite orders NULL first, so a NULL-priced product would be "cheapest". Filter or order explicitly.
- pandas: a category with one product has no position-2 row, so `map` gives NaN; SQL gives NULL. They compare equal in the assertion.

**Then explain:**
- **Frame-sensitive:** `FIRST_VALUE`, `LAST_VALUE` and `NTH_VALUE` look inside the frame, not the partition. Default frame with `ORDER BY` ends at the current row (and peers), so "second" is not visible yet for the first row (Q19 covers `LAST_VALUE`).
- **Counting direction:** SQLite does not support `FROM LAST` on `NTH_VALUE`; the run prints SQLite 3.45's syntax error for it. Reverse the order instead. Other engines may support it (not executed here).
- **pandas:** `cumcount() + 1 == 2` is explicit and keeps the row; `groupby().nth(1)` returns the same rows, as the run asserts. `nth` is zero-based.

**Follow-ups:**
- *Third cheapest?* `NTH_VALUE(name, 3)`.
- *Second cheapest price gap from the cheapest?* `NTH_VALUE(price, 2) - FIRST_VALUE(price)` over the full frame.
- *Why not `LIMIT 1 OFFSET 1`?* It is not per category.

**Common mistakes:**
- Using `NTH_VALUE` with the default frame and wondering about NULLs.
- Off-by-one between SQL (1-based) and pandas `nth`/`cumcount` (0-based).
- Not breaking price ties.

### Q24 ⭐⭐ 🟢 Named windows and reuse: employees(emp_id, name, dept_id, salary). Write one query that uses ROW_NUMBER, RANK, DENSE_RANK and AVG over the same (PARTITION BY dept_id ORDER BY salary DESC) via a WINDOW clause (WINDOW w AS (...)) and OVER w. Explain where the WINDOW clause sits (after HAVING, before ORDER BY), the benefit (one definition, no drift), that a named window can be extended in OVER (w ORDER BY ...) in some cases (hedge), and that PostgreSQL, MySQL 8 and SQLite support it (hedged beyond SQLite).
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Define the window once with `WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC)` after `HAVING` and before `ORDER BY`, then write `OVER w` on each function; a named window can be extended with `OVER (w ORDER BY ...)` only when `w` does not already have that clause, and `AVG` over an ordered window is a running average, not the department average.

**Schema and sample data:** five employees; Asha and Ben tie at 90 in dept 10.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
  (4,'Dev',20,80),(5,'Esha',20,60);
```

**SQL answer:** `SQL_MAIN` (Code block). It defines three windows: `dept` (partition only), `w` (extends `dept` with the salary order) and `ws` (adds `emp_id` so `ROW_NUMBER` is deterministic).
```sql
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER ws AS rn,
       RANK() OVER w AS rk,
       DENSE_RANK() OVER w AS dr,
       AVG(salary) OVER w AS avg_same_window,
       AVG(salary) OVER dept AS dept_avg
FROM employees
WINDOW dept AS (PARTITION BY dept_id),
       w AS (dept ORDER BY salary DESC),
       ws AS (dept ORDER BY salary DESC, emp_id)
ORDER BY dept_id, rn
```

**pandas answer:** there is no named-window object; the equivalent reuse is one sorted frame and one `groupby`.
```python
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int),
                 dept_avg=g.transform("mean"))
```

**Example:**
- Dept 10 by salary descending: Asha 90, Ben 90, Chitra 70. Dept 20: Dev 80, Esha 60.
- `RANK` over `w`: 1, 1, 3 and 1, 2. `DENSE_RANK`: 1, 1, 2 and 1, 2. `ROW_NUMBER` over `ws` (tie-break `emp_id`): 1, 2, 3 and 1, 2.
- `AVG(salary) OVER dept` (no ORDER BY): the whole department, (90 + 90 + 70) / 3 = 83.33 for all three dept 10 rows; 70 for dept 20.
- `AVG(salary) OVER w` (the same ordered window): this is a cumulative average through the current row and its peers. Asha and Ben are peers, so both get (90 + 90) / 2 = 90; Chitra gets 83.33. In dept 20: Dev 80, then (80 + 60) / 2 = 70. So it equals the department average only on the last row. If someone asks for "the same window including AVG", I point this out and use the unordered window for the department average.

**Code:** run with `python3 -I`.
```python
# Q24: named windows and reuse
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
  (4,'Dev',20,80),(5,'Esha',20,60);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER ws AS rn,
       RANK() OVER w AS rk,
       DENSE_RANK() OVER w AS dr,
       AVG(salary) OVER w AS avg_same_window,
       AVG(salary) OVER dept AS dept_avg
FROM employees
WINDOW dept AS (PARTITION BY dept_id),
       w AS (dept ORDER BY salary DESC),
       ws AS (dept ORDER BY salary DESC, emp_id)
ORDER BY dept_id, rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

def attempt(label, sql):
    try:
        con.execute(sql).fetchall()
        print(label, "-> OK")
    except sqlite3.Error as e:
        print(label, "-> ERROR:", e)
attempt("extend a window with no ORDER BY: OVER (dept ORDER BY salary)",
        "SELECT RANK() OVER (d ORDER BY salary) FROM employees WINDOW d AS (PARTITION BY dept_id)")
attempt("override an existing ORDER BY: OVER (w ORDER BY emp_id)",
        "SELECT RANK() OVER (w ORDER BY emp_id) FROM employees WINDOW w AS (PARTITION BY dept_id ORDER BY salary)")
attempt("add PARTITION BY to a named window: OVER (w PARTITION BY dept_id)",
        "SELECT RANK() OVER (w PARTITION BY dept_id) FROM employees WINDOW w AS (ORDER BY salary)")
attempt("WINDOW clause after ORDER BY",
        "SELECT RANK() OVER w FROM employees ORDER BY emp_id WINDOW w AS (ORDER BY salary)")
attempt("WINDOW clause after GROUP BY/HAVING, before ORDER BY",
        "SELECT dept_id, RANK() OVER w FROM employees GROUP BY dept_id HAVING COUNT(*) > 0 WINDOW w AS (ORDER BY dept_id) ORDER BY dept_id")

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int),
                 dept_avg=g.transform("mean"))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
cols = ["emp_id", "name", "dept_id", "salary", "rn", "rk", "dr", "dept_avg"]
# compared in dept_id, rn order
pd.testing.assert_frame_equal(sql_df.drop(columns="avg_same_window"), pd_df[cols], check_dtype=False)
print("\nasserts passed: SQL == pandas on rn, rk, dr, dept_avg (avg_same_window is a cumulative average, not compared)")
```

**Output (my run):**
```text
SQL:
 emp_id   name  dept_id  salary  rn  rk  dr  avg_same_window  dept_avg
      1   Asha       10      90   1   1   1        90.000000 83.333333
      2    Ben       10      90   2   1   1        90.000000 83.333333
      3 Chitra       10      70   3   3   2        83.333333 83.333333
      4    Dev       20      80   1   1   1        80.000000 70.000000
      5   Esha       20      60   2   2   2        70.000000 70.000000
extend a window with no ORDER BY: OVER (dept ORDER BY salary) -> OK
override an existing ORDER BY: OVER (w ORDER BY emp_id) -> ERROR: cannot override ORDER BY clause of window: w
add PARTITION BY to a named window: OVER (w PARTITION BY dept_id) -> ERROR: cannot override PARTITION clause of window: w
WINDOW clause after ORDER BY -> ERROR: near "WINDOW": syntax error
WINDOW clause after GROUP BY/HAVING, before ORDER BY -> OK

pandas:
 emp_id   name  dept_id  salary  rn  rk  dr  dept_avg
      1   Asha       10      90   1   1   1 83.333333
      2    Ben       10      90   2   1   1 83.333333
      3 Chitra       10      70   3   3   2 83.333333
      4    Dev       20      80   1   1   1 70.000000
      5   Esha       20      60   2   2   2 70.000000

asserts passed: SQL == pandas on rn, rk, dr, dept_avg (avg_same_window is a cumulative average, not compared)
```

**Edge cases:**
- Extending: `OVER (dept ORDER BY salary)` works because `dept` has no `ORDER BY`. `OVER (w ORDER BY emp_id)` fails because `w` already has one, and `OVER (w PARTITION BY ...)` fails because partitions cannot be added (error texts above, SQLite 3.45). So the rule in my run is: you may add `ORDER BY` (and a frame) to a base that lacks them; you cannot override.
- Clause position: after `HAVING`, before `ORDER BY` works; after `ORDER BY` is a syntax error (both tried in the run).
- Ties: `RANK` and `DENSE_RANK` treat tied rows as peers; `ROW_NUMBER` needs the extra `emp_id` key.
- PostgreSQL and MySQL 8 also have the `WINDOW` clause (from memory, not executed here); the extension rules are stated in the SQL standard and I believe they are similar, but I did not test them.

**Then explain:**
- **Benefit:** one definition, so changing the partition or order in one place cannot leave a column on a different window ("no drift"), and the select list is shorter.
- **Where it sits:** `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... WINDOW ... ORDER BY ... LIMIT`.
- **pandas:** sort once, `groupby` once, then `rank(method=...)` and `transform("mean")`; the mean is the department mean (the unordered window), which the run asserts. The cumulative average has no direct single call and belongs to Part 5.

**Follow-ups:**
- *Can the same name be used in two different clauses?* Yes, any number of `OVER w`.
- *Does naming a window change performance?* Not by itself as far as I know; I did not time it.
- *Why not just repeat the clause?* It works, but it invites drift.

**Common mistakes:**
- Putting `WINDOW` after `ORDER BY`.
- Trying to override an `ORDER BY` of a named window.
- Treating `AVG(...) OVER (... ORDER BY ...)` as the group average.
- `ROW_NUMBER` with ties and no tie-break key.

### Q25 ⭐⭐ 🟡 PARTITION BY versus ORDER BY inside OVER, and the default frame basics: employees(emp_id, name, dept_id, salary). Compare SUM(salary) OVER (PARTITION BY dept_id) with SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary) and explain why the second one changes row by row (default frame RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, peers share a value) while the first is the whole partition. Show ROWS versus RANGE with two equal salaries. Keep it to the idea of a frame; running totals are Part 5. Give the pandas transform('sum') contrast.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `PARTITION BY` splits rows into groups and `SUM(...) OVER (PARTITION BY dept_id)` is the whole group's total on every row; adding `ORDER BY` inside `OVER` also sets a default frame that ends at the current row (and its peers), so the same `SUM` changes row by row, and equal salaries share one value under `RANGE` but not under `ROWS`.

**Schema and sample data:** six employees; Ben and Chitra both earn 60 in dept 10.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,60),(3,'Chitra',10,60),(4,'Dev',10,80),
  (5,'Esha',20,40),(6,'Farid',20,70);
```

**SQL answer:** `SQL_MAIN` (Code block).
```sql
SELECT emp_id, name, dept_id, salary,
       SUM(salary) OVER (PARTITION BY dept_id) AS dept_total,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary) AS sum_range,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary, emp_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sum_rows
FROM employees
ORDER BY dept_id, salary, emp_id
```

**pandas answer:** `transform("sum")` is the unordered window; `cumsum` after a sort behaves like a `ROWS` frame; taking the maximum of that within tied rows gives the `RANGE` value.
```python
s = employees.sort_values(["dept_id", "salary", "emp_id"]).reset_index(drop=True)
s["dept_total"] = s.groupby("dept_id")["salary"].transform("sum")
s["sum_rows"] = s.groupby("dept_id")["salary"].cumsum()
s["sum_range"] = s.groupby(["dept_id", "salary"])["sum_rows"].transform("max")
pd_df = s[["emp_id", "name", "dept_id", "salary", "dept_total", "sum_range", "sum_rows"]]
```

**Example:** dept 10, ordered by salary: Asha 50, Ben 60, Chitra 60, Dev 80. Dept total 250.
- `SUM OVER (PARTITION BY dept_id)`: 250 on all four rows (whole partition, no ordering involved).
- `SUM OVER (PARTITION BY dept_id ORDER BY salary)` with the default `RANGE` frame: Asha 50; Ben and Chitra are peers (same salary), so both see everything up to the last peer: 50 + 60 + 60 = 170 for both; Dev 250.
- Same with `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (ordering by `salary, emp_id` so the row order is fixed): Asha 50, Ben 110, Chitra 170, Dev 250. Only the tied pair differs from `RANGE` (110 versus 170).
- Dept 20: Esha 40 then Farid 70: total 110 on both, and 40 then 110 under both frames (no ties).

**Code:** run with `python3 -I`.
```python
# Q25: PARTITION BY versus ORDER BY inside OVER; default frame basics
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,60),(3,'Chitra',10,60),(4,'Dev',10,80),
  (5,'Esha',20,40),(6,'Farid',20,70);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       SUM(salary) OVER (PARTITION BY dept_id) AS dept_total,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary) AS sum_range,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary, emp_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sum_rows
FROM employees
ORDER BY dept_id, salary, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
s = employees.sort_values(["dept_id", "salary", "emp_id"]).reset_index(drop=True)
s["dept_total"] = s.groupby("dept_id")["salary"].transform("sum")
s["sum_rows"] = s.groupby("dept_id")["salary"].cumsum()
s["sum_range"] = s.groupby(["dept_id", "salary"])["sum_rows"].transform("max")
pd_df = s[["emp_id", "name", "dept_id", "salary", "dept_total", "sum_range", "sum_rows"]]
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in dept_id, salary, emp_id order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nasserts passed: SQL == pandas (cumsum is ROWS-like; max over peers gives the RANGE value)")
```

**Output (my run):**
```text
SQL:
 emp_id   name  dept_id  salary  dept_total  sum_range  sum_rows
      1   Asha       10      50         250         50        50
      2    Ben       10      60         250        170       110
      3 Chitra       10      60         250        170       170
      4    Dev       10      80         250        250       250
      5   Esha       20      40         110         40        40
      6  Farid       20      70         110        110       110

pandas:
 emp_id   name  dept_id  salary  dept_total  sum_range  sum_rows
      1   Asha       10      50         250         50        50
      2    Ben       10      60         250        170       110
      3 Chitra       10      60         250        170       170
      4    Dev       10      80         250        250       250
      5   Esha       20      40         110         40        40
      6  Farid       20      70         110        110       110

asserts passed: SQL == pandas (cumsum is ROWS-like; max over peers gives the RANGE value)
```

**Edge cases:**
- Ties: peers share a `RANGE` value; `ROWS` depends on physical row order, so add a tie-break (`emp_id`) to make it deterministic. Without one, which of Ben and Chitra shows 110 is unspecified.
- NULL salary: `SUM` skips it, and in the ordered window SQLite sorts NULL first, so the NULL row would come first with a NULL-only partial sum if it is first. I did not run a NULL case here.
- One-row partition: the sum is just that row, under any frame.
- Without `ORDER BY`, the default frame is the whole partition, which is why the first column is a total.

**Then explain:**
- **Two jobs inside `OVER`:** `PARTITION BY` chooses which rows are in the group; `ORDER BY` chooses their order and, as a side effect, shrinks the default frame to "start through current row and peers".
- **ROWS versus RANGE:** `ROWS` counts rows; `RANGE` includes all rows whose `ORDER BY` value equals the current row's.
- **Scope:** I am only using this to explain frames. Running totals as a technique, moving averages and `LAG`/`LEAD` are Part 5.
- **pandas:** `transform("sum")` repeats the group total; `cumsum` is ROWS-like, so I take the maximum per tied salary to emulate RANGE.

**Follow-ups:**
- *Why did my share-of-total break?* An `ORDER BY` slipped into the window (Q14).
- *Can I change the frame?* Yes, with `ROWS`/`RANGE`/`GROUPS` clauses; SQLite supports all three (documented; I only ran ROWS and the default RANGE here).
- *Default frame without ORDER BY?* Whole partition.

**Common mistakes:**
- Adding `ORDER BY` to a total and getting a running sum.
- Assuming `ROWS` and `RANGE` are the same when there are ties.
- No tie-break with `ROWS`, so the output order of ties changes.

### Q26 ⭐⭐ 🟡 Top-N with ties rules: products(product_id, category, name, sales). Return the top 3 products by sales per category in three variants: exactly 3 (ROW_NUMBER with a tie-breaker), 3 including ties at the cutoff (RANK <= 3), and top 3 distinct sales values (DENSE_RANK <= 3). Show the standard FETCH FIRST n ROWS WITH TIES / WITH TIES syntax as dialect text (PostgreSQL 13+, hedged, not executed; SQLite has no WITH TIES; per-group still needs a window). Explain how to ask the interviewer which variant they want.
**Asked at:** techinterview.org window-function gotchas article (ties, RANK = 2 returning nothing, window in WHERE, default frame), a guide and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** "Top 3" is ambiguous when sales tie, so I pick by the requirement: `ROW_NUMBER <= 3` with a tie-breaker for exactly 3 rows, `RANK <= 3` for 3 places plus everyone tied at the cutoff, and `DENSE_RANK <= 3` for the top 3 distinct sales values; I ask the interviewer which one they mean before writing it.

**Schema and sample data:** category A has a three-way tie at 90 right below the leader; category B has a tie for first and only four products.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, sales INTEGER);
INSERT INTO products VALUES (1,'A','P1',100),(2,'A','P2',90),(3,'A','P3',90),(4,'A','P4',90),
  (5,'A','P5',80),(6,'A','P6',70),(7,'B','P7',50),(8,'B','P8',50),(9,'B','P9',40),(10,'B','P10',30);
```

**SQL answer:** `SQL_MAIN` shows all three numberings; `SQL_EXACT`, `SQL_TIES` and `SQL_DISTINCT` are the three answers (Code block).
```sql
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC, product_id) AS rn
  FROM products)
WHERE rn <= 3
ORDER BY category, product_id
```
```sql
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rk
  FROM products)
WHERE rk <= 3
ORDER BY category, product_id
```
```sql
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dr
  FROM products)
WHERE dr <= 3
ORDER BY category, product_id
```

**pandas answer:** sort with the tie-break, then `head(3)` per group for exactly 3, and `rank` with `method="min"` / `"dense"` for the other two.
```python
s = products.sort_values(["category", "sales", "product_id"], ascending=[True, False, True])
g = s.groupby("category")["sales"]
cols = ["category", "product_id", "sales"]
pd_exact = s.groupby("category").head(3)[cols]
pd_ties = s[g.rank(method="min", ascending=False) <= 3][cols]
pd_dist = s[g.rank(method="dense", ascending=False) <= 3][cols]
```

**Example:**
- Category A sales: P1 100, P2 90, P3 90, P4 90, P5 80, P6 70. `ROW_NUMBER` (tie-break product_id): 1 to 6, so exactly 3 gives P1, P2, P3. `RANK`: 1, 2, 2, 2, 5, 6, so `rk <= 3` gives P1 to P4 (four rows). `DENSE_RANK`: 1, 2, 2, 2, 3, 4, so `dr <= 3` gives P1 to P5 (five rows).
- Category B: P7 50, P8 50, P9 40, P10 30. `ROW_NUMBER`: P7, P8, P9. `RANK`: 1, 1, 3, 4, so P7, P8, P9. `DENSE_RANK`: 1, 1, 2, 3, so all four products.
- Totals: 6, 7 and 9 rows for the three variants.

**Code:** run with `python3 -I`.
```python
# Q26: top-N with ties rules
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, sales INTEGER);
INSERT INTO products VALUES (1,'A','P1',100),(2,'A','P2',90),(3,'A','P3',90),(4,'A','P4',90),
  (5,'A','P5',80),(6,'A','P6',70),(7,'B','P7',50),(8,'B','P8',50),(9,'B','P9',40),(10,'B','P10',30);
"""
SQL_MAIN = """
SELECT category, product_id, sales, rn, rk, dr
FROM (SELECT category, product_id, sales,
             ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC, product_id) AS rn,
             RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rk,
             DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dr
      FROM products)
ORDER BY category, rn
"""
SQL_EXACT = """
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC, product_id) AS rn
  FROM products)
WHERE rn <= 3
ORDER BY category, product_id
"""
SQL_TIES = """
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rk
  FROM products)
WHERE rk <= 3
ORDER BY category, product_id
"""
SQL_DISTINCT = """
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dr
  FROM products)
WHERE dr <= 3
ORDER BY category, product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("All ranks:"); print(pd.read_sql_query(SQL_MAIN, con).to_string(index=False))
exact = pd.read_sql_query(SQL_EXACT, con)
ties = pd.read_sql_query(SQL_TIES, con)
dist = pd.read_sql_query(SQL_DISTINCT, con)
for label, d in (("exactly 3 (ROW_NUMBER)", exact), ("3 including ties (RANK <= 3)", ties), ("top 3 distinct values (DENSE_RANK <= 3)", dist)):
    print("\n" + label + ":", len(d), "rows"); print(d.to_string(index=False))
try:
    con.execute("SELECT product_id FROM products ORDER BY sales DESC FETCH FIRST 3 ROWS WITH TIES").fetchall()
except sqlite3.Error as e:
    print("\nFETCH FIRST ... WITH TIES on SQLite 3.45:", e)

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
s = products.sort_values(["category", "sales", "product_id"], ascending=[True, False, True])
g = s.groupby("category")["sales"]
cols = ["category", "product_id", "sales"]
pd_exact = s.groupby("category").head(3)[cols]
pd_ties = s[g.rank(method="min", ascending=False) <= 3][cols]
pd_dist = s[g.rank(method="dense", ascending=False) <= 3][cols]
# pd:end
# compared in category, product_id order
for a, b in ((exact, pd_exact), (ties, pd_ties), (dist, pd_dist)):
    pd.testing.assert_frame_equal(a, b.sort_values(["category", "product_id"]).reset_index(drop=True), check_dtype=False)
print("\nrow counts:", len(pd_exact), len(pd_ties), len(pd_dist))
print("asserts passed: all three SQL variants == pandas")
```

**Output (my run):**
```text
All ranks:
category  product_id  sales  rn  rk  dr
       A           1    100   1   1   1
       A           2     90   2   2   2
       A           3     90   3   2   2
       A           4     90   4   2   2
       A           5     80   5   5   3
       A           6     70   6   6   4
       B           7     50   1   1   1
       B           8     50   2   1   1
       B           9     40   3   3   2
       B          10     30   4   4   3

exactly 3 (ROW_NUMBER): 6 rows
category  product_id  sales
       A           1    100
       A           2     90
       A           3     90
       B           7     50
       B           8     50
       B           9     40

3 including ties (RANK <= 3): 7 rows
category  product_id  sales
       A           1    100
       A           2     90
       A           3     90
       A           4     90
       B           7     50
       B           8     50
       B           9     40

top 3 distinct values (DENSE_RANK <= 3): 9 rows
category  product_id  sales
       A           1    100
       A           2     90
       A           3     90
       A           4     90
       A           5     80
       B           7     50
       B           8     50
       B           9     40
       B          10     30

FETCH FIRST ... WITH TIES on SQLite 3.45: near "FETCH": syntax error

row counts: 6 7 9
asserts passed: all three SQL variants == pandas
```

**Edge cases:**
- Fewer than 3 products in a category: all of them are returned in every variant.
- Ties at the cutoff: only `ROW_NUMBER` cuts through a tie, and it does so by the tie-breaker I choose (lowest product_id), which drops P4 from A even though it sold as much as P2 and P3.
- NULL sales: SQLite sorts NULL last under `DESC`, so NULL rows rank last but can still enter the top 3 in a small category; filter `sales IS NOT NULL` if they should not.
- Dialect text, not executed here: PostgreSQL 13+ supports `FETCH FIRST 3 ROWS WITH TIES` (the `ORDER BY` must precede it), and MySQL has no `WITH TIES`. SQLite 3.45 rejects it (the run prints the syntax error). Even where it exists it limits the whole result, not each group, so per-category top 3 with ties still needs a window or a lateral join.

**Then explain:**
- **Which variant, in interview terms:** I ask "if two products tie for third, do you want both, or exactly three?" and "is it the top three products or the top three sales values?" Then I state my tie-break aloud for the exactly-3 case.
- **Why filter outside:** windows cannot appear in `WHERE`, so the number is computed in a subquery and filtered outside (Q3).
- **pandas:** `groupby().head(3)` is the `ROW_NUMBER` answer only after sorting with a tie-break; `rank` with `min` and `dense` give the others. All three match SQL in the run.
- **Ordering of output:** I order by category and product_id before comparing, since the variants return different row counts.

**Follow-ups:**
- *`QUALIFY`?* Snowflake, BigQuery and Teradata let you filter window results directly (from memory, not executed here); SQLite does not.
- *Top 3 overall, not per group?* Drop `PARTITION BY` (or `LIMIT 3` with a tie-break).
- *Performance?* The window sorts each partition; an index on (category, sales) may help, but I did not test it here.

**Common mistakes:**
- Using `ROW_NUMBER` with no tie-break and calling the result "the top 3".
- Using `RANK <= 3` and being surprised by four or more rows.
- Using `DENSE_RANK` when the business means "3 products".
- Assuming `WITH TIES` is per group.

### Q27 ⭐⭐ 🟡 Ranking by multiple columns and mixed directions: candidates(candidate_id, name, score, attempts, submitted_at). Rank by score descending, then attempts ascending (fewer attempts is better), then submitted_at ascending, using DENSE_RANK and ROW_NUMBER. Explain how each ORDER BY key sets its own direction, that RANK treats rows as tied only when all ORDER BY keys are equal, and give the pandas sort_values(by=[...], ascending=[False, True, True]) with rank(method='first') and a tuple-based dense rank (groupby ngroup).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Each key in `ORDER BY` carries its own `ASC`/`DESC`; `RANK` and `DENSE_RANK` call two rows tied only when every key is equal, and `ROW_NUMBER` needs a unique last key (here `candidate_id`) or ties are numbered arbitrarily; in pandas it is `sort_values(by=[...], ascending=[False, True, True, True])` plus `groupby(keys, sort=False).ngroup()` for the dense rank.

**Schema and sample data:** six candidates. Chitra and Ben tie on score and attempts but differ on time; Dev and Esha tie on all three keys.
```sql
CREATE TABLE candidates(candidate_id INTEGER PRIMARY KEY, name TEXT, score INTEGER,
                        attempts INTEGER, submitted_at TEXT);
INSERT INTO candidates VALUES
 (1,'Asha',90,2,'2026-01-05'),(2,'Ben',90,1,'2026-01-06'),(3,'Chitra',90,1,'2026-01-04'),
 (4,'Dev',85,3,'2026-01-02'),(5,'Esha',85,3,'2026-01-02'),(6,'Farid',70,1,'2026-01-01');
```
`submitted_at` is ISO text, so text order equals date order.

**SQL answer:** `SQL_MAIN` in the Code block. Tie-breaking rule: `ROW_NUMBER` adds `candidate_id` as a final key so the numbering is the same on every run; `RANK` and `DENSE_RANK` do not need it because ties are meant to share a number.
```sql
SELECT candidate_id, name, score, attempts, submitted_at,
       DENSE_RANK() OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC)               AS dense_pos,
       RANK()       OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC)               AS rank_pos,
       ROW_NUMBER() OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC, candidate_id) AS row_pos
FROM candidates
ORDER BY row_pos
```

**pandas answer:** inside `# pd:main` in the Code block. `sort_values` takes one direction per key; `ngroup()` with `sort=False` numbers each distinct key tuple in order of first appearance, which in a sorted frame is the dense rank; the minimum row position inside each tuple is the `RANK`.
```python
keys = ["score", "attempts", "submitted_at"]
ordered = cand.sort_values(by=keys + ["candidate_id"], ascending=[False, True, True, True]).reset_index(drop=True)
ordered["row_pos"] = ordered.index + 1
ordered["dense_pos"] = ordered.groupby(keys, sort=False).ngroup() + 1
ordered["rank_pos"] = ordered.groupby(keys, sort=False)["row_pos"].transform("min")
```

**Example:** order by score high first, then fewer attempts, then earlier time.
- 90s: Chitra (1 attempt, 01-04) beats Ben (1 attempt, 01-06) on time; Asha has 2 attempts so she is third. Positions 1, 2, 3.
- 85s: Dev and Esha are equal on all three keys, so they are tied. Dense rank 4 and 4, rank 4 and 4. `ROW_NUMBER` must split them, and `candidate_id` does: Dev 4, Esha 5.
- Farid (70) is next: dense rank 5 (no gap), rank 6 (the tie used up positions 4 and 5), row number 6.
- Contrast: ranking on score alone puts Asha, Ben and Chitra all at 1 and Dev and Esha at 4, which ignores the other two keys.

**Code:** run with `python3 -I`.
```python
# Q27: multi-column ranking with mixed directions (score DESC, attempts ASC, submitted_at ASC)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE candidates(candidate_id INTEGER PRIMARY KEY, name TEXT, score INTEGER,
                        attempts INTEGER, submitted_at TEXT);
INSERT INTO candidates VALUES
 (1,'Asha',90,2,'2026-01-05'),(2,'Ben',90,1,'2026-01-06'),(3,'Chitra',90,1,'2026-01-04'),
 (4,'Dev',85,3,'2026-01-02'),(5,'Esha',85,3,'2026-01-02'),(6,'Farid',70,1,'2026-01-01');
"""
SQL_MAIN = """
SELECT candidate_id, name, score, attempts, submitted_at,
       DENSE_RANK() OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC)               AS dense_pos,
       RANK()       OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC)               AS rank_pos,
       ROW_NUMBER() OVER (ORDER BY score DESC, attempts ASC, submitted_at ASC, candidate_id) AS row_pos
FROM candidates
ORDER BY row_pos
"""
SQL_SCORE_ONLY = """
SELECT candidate_id, RANK() OVER (ORDER BY score DESC) AS rank_score_only
FROM candidates ORDER BY candidate_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (ties broken for ROW_NUMBER by candidate_id):")
print(sql_df.to_string(index=False))
print("\nRANK on score only, for contrast:")
print(pd.read_sql_query(SQL_SCORE_ONLY, con).to_string(index=False))

# named window: a window that already has ORDER BY cannot be given another one
for label, q in [
    ("OVER (w ORDER BY candidate_id) where w has ORDER BY",
     "SELECT RANK() OVER (w ORDER BY candidate_id) FROM candidates WINDOW w AS (ORDER BY score DESC)"),
    ("OVER (w ORDER BY ...) where w has only PARTITION BY",
     "SELECT candidate_id, RANK() OVER (w ORDER BY score DESC) FROM candidates WINDOW w AS (PARTITION BY attempts)"),
]:
    try:
        n = len(con.execute(q).fetchall())
        print("named window OK  :", label, "->", n, "rows")
    except sqlite3.Error as ex:
        print("named window FAIL:", label, "->", ex)

cand = pd.read_sql_query("SELECT * FROM candidates", con)
# pd:main
keys = ["score", "attempts", "submitted_at"]
ordered = cand.sort_values(by=keys + ["candidate_id"], ascending=[False, True, True, True]).reset_index(drop=True)
ordered["row_pos"] = ordered.index + 1
ordered["dense_pos"] = ordered.groupby(keys, sort=False).ngroup() + 1
ordered["rank_pos"] = ordered.groupby(keys, sort=False)["row_pos"].transform("min")
# pd:end
# rank(method='first') on score alone is right only if the frame is first sorted by the other keys
by_rest = cand.sort_values(["attempts", "submitted_at", "candidate_id"])
first_pos = by_rest["score"].rank(method="first", ascending=False).astype(int)
print("\npandas:")
print(ordered.to_string(index=False))
# compared after sorting both by candidate_id
cols = ["candidate_id", "dense_pos", "rank_pos", "row_pos"]
a = sql_df[cols].sort_values("candidate_id").reset_index(drop=True)
b = ordered[cols].sort_values("candidate_id").reset_index(drop=True).astype("int64")
pd.testing.assert_frame_equal(a, b, check_dtype=False)
# the 'first' route: its ranks are by score only, so it differs where score ties exist
by_rest_df = pd.DataFrame({"candidate_id": by_rest["candidate_id"], "first_on_score_only": first_pos}).sort_values("candidate_id")
print("\nrank(method='first') on score alone after sorting by the other keys ascending:")
print(by_rest_df.to_string(index=False))
assert by_rest_df["first_on_score_only"].tolist() == a["row_pos"].tolist()
print("asserts passed: SQL == pandas for dense_pos, rank_pos, row_pos; 'first' route == row_pos")
```

**Output (my run):**
```text
SQL (ties broken for ROW_NUMBER by candidate_id):
 candidate_id   name  score  attempts submitted_at  dense_pos  rank_pos  row_pos
            3 Chitra     90         1   2026-01-04          1         1        1
            2    Ben     90         1   2026-01-06          2         2        2
            1   Asha     90         2   2026-01-05          3         3        3
            4    Dev     85         3   2026-01-02          4         4        4
            5   Esha     85         3   2026-01-02          4         4        5
            6  Farid     70         1   2026-01-01          5         6        6

RANK on score only, for contrast:
 candidate_id  rank_score_only
            1                1
            2                1
            3                1
            4                4
            5                4
            6                6
named window FAIL: OVER (w ORDER BY candidate_id) where w has ORDER BY -> cannot override ORDER BY clause of window: w
named window OK  : OVER (w ORDER BY ...) where w has only PARTITION BY -> 6 rows

pandas:
 candidate_id   name  score  attempts submitted_at  row_pos  dense_pos  rank_pos
            3 Chitra     90         1   2026-01-04        1          1         1
            2    Ben     90         1   2026-01-06        2          2         2
            1   Asha     90         2   2026-01-05        3          3         3
            4    Dev     85         3   2026-01-02        4          4         4
            5   Esha     85         3   2026-01-02        5          4         4
            6  Farid     70         1   2026-01-01        6          5         6

rank(method='first') on score alone after sorting by the other keys ascending:
 candidate_id  first_on_score_only
            1                    3
            2                    2
            3                    1
            4                    4
            5                    5
            6                    6
asserts passed: SQL == pandas for dense_pos, rank_pos, row_pos; 'first' route == row_pos
```

**Edge cases:**
- Full ties (Dev, Esha): `RANK` and `DENSE_RANK` give them the same number by design; only `ROW_NUMBER` needs the extra key.
- NULL in a key: it sorts as the smallest value in SQLite, so with `ASC` it comes first (see Q29); I did not put a NULL in this table.
- Mixed types in the sort key: text dates sort correctly only in ISO form; `'5/1/2026'` would not. Store real dates or ISO strings.
- Named windows: `WINDOW w AS (ORDER BY score DESC)` then `OVER (w ORDER BY candidate_id)` fails on SQLite 3.45 with "cannot override ORDER BY clause of window: w" (run above); a window that has only `PARTITION BY` can be extended with an `ORDER BY` (ran fine). So I wrote the full `ORDER BY` three times; a named window works for the two functions with identical keys.

**Then explain:**
- **Per-key direction:** `ORDER BY score DESC, attempts ASC, submitted_at ASC` puts a direction on each key; a `DESC` written once does not carry over to the following keys.
- **When rows are tied:** `RANK` and `DENSE_RANK` compare the whole `ORDER BY` tuple (peers). One different key and the rows are not peers.
- **Which function:** `ROW_NUMBER` for "one winner per position", `DENSE_RANK` for "how many distinct levels above me", `RANK` for competition-style positions with gaps.
- **pandas route 1:** `sort_values` with `ascending=[False, True, True, True]`, then positions `index + 1`, `ngroup()` for dense, group-minimum for rank.
- **pandas route 2:** `Series.rank(method="first")` ranks one column only. It reproduces `ROW_NUMBER` if you first sort by the other keys in their own order (ran above and asserted), because "first" breaks ties by row order in the frame.
- Dialect: all of this is standard SQL; named windows exist in PostgreSQL and MySQL 8 (not executed here), their rules about extending a named window may differ.

**Follow-ups:**
- *How do you rank with `ORDER BY` on an expression, e.g. highest score per attempt?* Put the expression inside `OVER (ORDER BY score * 1.0 / attempts DESC)`; in pandas compute it as a column first.
- *What if the direction depends on a column?* Use `CASE` inside the ORDER BY; in pandas sort on a derived key.
- *Which tie-breaker do you pick?* A unique, meaningful key (id or timestamp plus id), stated out loud.

**Common mistakes:**
- Using `ORDER BY score, attempts DESC`: score ascending and attempts descending, the opposite of both intents.
- Forgetting the unique key for `ROW_NUMBER` and then saying the result is deterministic.
- In pandas, `sort_values(by=keys, ascending=False)` applies descending to every key.
- Calling `groupby(...).ngroup()` without `sort=False`; it then numbers groups in sorted key order, which for descending-by-score keys is the wrong direction.

### Q28 ⭐⭐ 🟡 Rank within a filtered subset: employees(emp_id, name, dept_id, salary, status) with status 'active' or 'left'. Rank only active employees by salary within each department, and explain the difference between filtering in WHERE before the window (rank among active only) and filtering after in an outer query (rank among everyone, then hide). Show both give different ranks, say which is wanted, and give the pandas filter-then-rank versus rank-then-filter versions.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** A `WHERE` filter runs before the window function, so the window only sees the surviving rows and ranks among them; filtering in an outer query runs after, so the ranks were computed among everyone and the hidden rows still occupy positions; for "rank among active staff" you want `WHERE status = 'active'` in the same query as the window, and in pandas the same split is filter-then-rank versus rank-then-filter.

**Schema and sample data:** eight employees; each department's top earner is somebody who has left, except department 30 where everyone has left.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER, status TEXT);
INSERT INTO employees VALUES
 (1,'Asha',10,90,'active'),(2,'Ben',10,100,'left'),(3,'Chitra',10,80,'active'),(4,'Dev',10,80,'active'),
 (5,'Esha',20,70,'left'),(6,'Farid',20,60,'active'),(7,'Gita',20,50,'active'),
 (8,'Hari',30,40,'left');
```

**SQL answer:** `SQL_MAIN` (filter before) and `SQL_AFTER` (filter after) in the Code block. Tie-breaking: both use `RANK`, so Chitra and Dev (80 each) legitimately share a rank; the final `ORDER BY` has `emp_id` so the printed order is fixed.
```sql
SELECT emp_id, name, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk_active
FROM employees
WHERE status = 'active'
ORDER BY dept_id, rnk_active, emp_id
```
```sql
SELECT emp_id, name, dept_id, salary, rnk_all
FROM (SELECT emp_id, name, dept_id, salary, status,
             RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk_all
      FROM employees)
WHERE status = 'active'
ORDER BY dept_id, rnk_all, emp_id
```

**pandas answer:** inside `# pd:main` in the Code block. `rank(method="min", ascending=False)` is `RANK()`; `groupby("dept_id")` is `PARTITION BY`.
```python
active = emp[emp["status"] == "active"].copy()
active["rnk_active"] = active.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("int64")
everyone = emp.copy()
everyone["rnk_all"] = everyone.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("int64")
after_pd = everyone[everyone["status"] == "active"]
```

**Example:**
- Filter first: department 10 keeps Asha 90, Chitra 80, Dev 80. Ranks 1, 2, 2. Department 20 keeps Farid 60 and Gita 50: ranks 1, 2. Department 30 has no active employee, so it disappears.
- Filter after: department 10 ranks Ben 100 as 1, Asha 2, Chitra and Dev 3. Hiding Ben leaves Asha at 2 and Chitra, Dev at 3. Department 20: Esha 70 is 1, so Farid is 2 and Gita 3.
- All 5 active employees get a different rank under the two orders (the Code block prints the comparison).
- Top-1 per department: "filter first" returns Asha and Farid; "filter after" returns nobody, because the rank-1 person in each department has left.

**Code:** run with `python3 -I`.
```python
# Q28: rank within a filtered subset: filter before the window (WHERE) vs after (outer query)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER, status TEXT);
INSERT INTO employees VALUES
 (1,'Asha',10,90,'active'),(2,'Ben',10,100,'left'),(3,'Chitra',10,80,'active'),(4,'Dev',10,80,'active'),
 (5,'Esha',20,70,'left'),(6,'Farid',20,60,'active'),(7,'Gita',20,50,'active'),
 (8,'Hari',30,40,'left');
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk_active
FROM employees
WHERE status = 'active'
ORDER BY dept_id, rnk_active, emp_id
"""
SQL_AFTER = """
SELECT emp_id, name, dept_id, salary, rnk_all
FROM (SELECT emp_id, name, dept_id, salary, status,
             RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk_all
      FROM employees)
WHERE status = 'active'
ORDER BY dept_id, rnk_all, emp_id
"""
SQL_TOP1 = """
SELECT 'filter first' AS how, emp_id, name, dept_id FROM (
  SELECT emp_id, name, dept_id, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
  FROM employees WHERE status = 'active') WHERE r = 1
UNION ALL
SELECT 'filter after', emp_id, name, dept_id FROM (
  SELECT emp_id, name, dept_id, status, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
  FROM employees) WHERE r = 1 AND status = 'active'
ORDER BY 1, dept_id, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
before = pd.read_sql_query(SQL_MAIN, con)
after = pd.read_sql_query(SQL_AFTER, con)
top1 = pd.read_sql_query(SQL_TOP1, con)
print("SQL filter BEFORE the window (rank among active only):"); print(before.to_string(index=False))
print("\nSQL filter AFTER the window (rank among everyone, then hide 'left'):"); print(after.to_string(index=False))
print("\nTop-1 per department, both ways:"); print(top1.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
active = emp[emp["status"] == "active"].copy()
active["rnk_active"] = active.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("int64")
everyone = emp.copy()
everyone["rnk_all"] = everyone.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("int64")
after_pd = everyone[everyone["status"] == "active"]
# pd:end
# compared after sorting by emp_id
pd.testing.assert_frame_equal(
    before.sort_values("emp_id").reset_index(drop=True),
    active.drop(columns="status").sort_values("emp_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(
    after.sort_values("emp_id").reset_index(drop=True),
    after_pd.drop(columns="status").sort_values("emp_id").reset_index(drop=True), check_dtype=False)
diff = before.merge(after, on=["emp_id", "name", "dept_id", "salary"])
diff["same"] = diff["rnk_active"] == diff["rnk_all"]
print("\nSide by side (ranks differ for", int((~diff["same"]).sum()), "of", len(diff), "active employees):")
print(diff.sort_values("emp_id").to_string(index=False))
assert top1[top1["how"] == "filter first"]["emp_id"].tolist() == [1, 6]
assert top1[top1["how"] == "filter after"].empty
print("asserts passed: SQL == pandas for both orders; top-1 after the filter is empty")
```

**Output (my run):**
```text
SQL filter BEFORE the window (rank among active only):
 emp_id   name  dept_id  salary  rnk_active
      1   Asha       10      90           1
      3 Chitra       10      80           2
      4    Dev       10      80           2
      6  Farid       20      60           1
      7   Gita       20      50           2

SQL filter AFTER the window (rank among everyone, then hide 'left'):
 emp_id   name  dept_id  salary  rnk_all
      1   Asha       10      90        2
      3 Chitra       10      80        3
      4    Dev       10      80        3
      6  Farid       20      60        2
      7   Gita       20      50        3

Top-1 per department, both ways:
         how  emp_id  name  dept_id
filter first       1  Asha       10
filter first       6 Farid       20

Side by side (ranks differ for 5 of 5 active employees):
 emp_id   name  dept_id  salary  rnk_active  rnk_all  same
      1   Asha       10      90           1        2 False
      3 Chitra       10      80           2        3 False
      4    Dev       10      80           2        3 False
      6  Farid       20      60           1        2 False
      7   Gita       20      50           2        3 False
asserts passed: SQL == pandas for both orders; top-1 after the filter is empty
```

**Edge cases:**
- A department with only inactive employees (30) disappears from the filter-first result; it does not show a row with NULL.
- Ties (Chitra and Dev) keep the same rank in both versions; only the starting number moves.
- If "left" rows are wanted for context (for example a gap analysis), filter after is the right tool; if the question says "among active", filter first.
- `status` with NULL: `WHERE status = 'active'` drops NULL-status rows from the ranking (unknown is not true); decide whether NULL means active.

**Then explain:**
- **Order of evaluation:** FROM, WHERE, GROUP BY, HAVING, window functions, SELECT, ORDER BY. A `WHERE` condition on a plain column removes rows before the window sees them.
- **Subquery needed only for the window's own result:** you cannot filter on `rnk` in the same level; but you can filter on `status` in the same level and it still applies first.
- **Which is wanted:** read the wording. "Rank of the active employees" is filter first. "Where does this person stand overall" (and just show active people) is filter after.
- **pandas:** `emp[mask]` then `groupby().rank()` is the first version; `groupby().rank()` on the full frame and then `[mask]` is the second. On pandas 3.0 a filtered frame is its own copy (copy-on-write), so adding a column to it does not touch `emp` and raised no warning when I tried it; I still write `.copy()` to make that intent visible.
- **Other engines:** the same evaluation order holds in PostgreSQL, MySQL 8 and the others (not executed here); `QUALIFY` filters after the window, so a `WHERE` next to it is still before.

**Follow-ups:**
- *How do you get both ranks in one result?* Rank all rows in a CTE with a `CASE WHEN status = 'active'` partition trick, or run the window twice (one over everyone, one over `PARTITION BY dept_id, status`); in pandas, group by `["dept_id", "status"]`.
- *What if you want the top active earner per department, ties included?* `RANK() = 1` after `WHERE status = 'active'`.
- *Why not put the status test in `PARTITION BY`?* Then active and left are ranked as separate groups and you still have to filter; it is the same as filtering first for the active group.

**Common mistakes:**
- Writing the filter in the outer query when the question says "among active": ranks include departed staff.
- Believing `WHERE` runs after `RANK()`; it does not.
- In pandas, ranking the full frame and then forgetting to filter, or expecting the new rank column to appear in the original `emp` after ranking a filtered slice (it does not on pandas 3.0).
- Reading `rank` as an int: pandas returns floats unless you cast.

### Q29 ⭐⭐ 🟡 NULLs inside window ORDER BY: employees(emp_id, name, dept_id, salary) with some NULL salaries. Show ROW_NUMBER and RANK over ORDER BY salary DESC and over ORDER BY salary ASC, where the NULLs land in SQLite (NULLs are treated as smaller than any value) and how NULLS FIRST / NULLS LAST changes it (SQLite 3.30+; run it). State PostgreSQL treats NULLs as larger by default and MySQL as smaller (hedged, not executed), that NULLs are peers of each other, and give the pandas rank(na_option='keep'/'top'/'bottom') comparison.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** In SQLite a NULL sorts as smaller than every value, so inside a window `ORDER BY` NULLs come last under `DESC` and first under `ASC`, they are peers of each other (same `RANK`), and `NULLS FIRST` / `NULLS LAST` overrides the default (ran it on 3.45); pandas `rank` never gives NaN a rank by default (`na_option="keep"`), and `"top"` / `"bottom"` are the options that match SQL.

**Schema and sample data:** six employees, two with NULL salary and a tie at 70.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,50),(3,'Chitra',10,NULL),
  (4,'Dev',10,70),(5,'Esha',10,NULL),(6,'Farid',10,40);
```

**SQL answer:** `SQL_MAIN` in the Code block. Tie-breaking: the two `ROW_NUMBER` columns end with `emp_id`, so they are deterministic; the `RANK` columns have no tie-breaker because tied rows should share a rank.
```sql
SELECT emp_id, name, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn_desc,
  RANK()       OVER (ORDER BY salary DESC)         AS rk_desc,
  ROW_NUMBER() OVER (ORDER BY salary ASC, emp_id)  AS rn_asc,
  RANK()       OVER (ORDER BY salary ASC)          AS rk_asc,
  RANK()       OVER (ORDER BY salary DESC NULLS FIRST) AS rk_desc_nf,
  RANK()       OVER (ORDER BY salary ASC  NULLS LAST)  AS rk_asc_nl
FROM employees
ORDER BY emp_id
```

**pandas answer:** inside `# pd:main` in the Code block. `na_option="bottom"` with `ascending=False` reproduces SQLite's default for `DESC`; `na_option="top"` with `ascending=True` reproduces its default for `ASC`; the other two columns flip the option to match `NULLS FIRST` / `NULLS LAST`.
```python
s = emp["salary"]
pd_df = emp[["emp_id", "name", "salary"]].copy()
pd_df["rn_desc"] = s.rank(method="first", ascending=False, na_option="bottom")
pd_df["rk_desc"] = s.rank(method="min", ascending=False, na_option="bottom")
pd_df["rn_asc"] = s.rank(method="first", ascending=True, na_option="top")
pd_df["rk_asc"] = s.rank(method="min", ascending=True, na_option="top")
pd_df["rk_desc_nf"] = s.rank(method="min", ascending=False, na_option="top")
pd_df["rk_asc_nl"] = s.rank(method="min", ascending=True, na_option="bottom")
keep = s.rank(method="min", ascending=False, na_option="keep")
```

**Example:** salaries 70, 50, NULL, 70, NULL, 40.
- `ORDER BY salary DESC`: Asha and Dev (70) are peers, rank 1; Ben (50) is 3; Farid (40) is 4; the two NULLs are peers at rank 5. `ROW_NUMBER` with `emp_id` gives Asha 1, Dev 2, Ben 3, Farid 4, Chitra 5, Esha 6.
- `ORDER BY salary ASC`: the NULLs come first and tie at rank 1; Farid 3, Ben 4, Asha and Dev tie at 5. `ROW_NUMBER`: Chitra 1, Esha 2, Farid 3, Ben 4, Asha 5, Dev 6.
- `DESC NULLS FIRST`: NULLs rank 1 (tied), then Asha and Dev rank 3, Ben 5, Farid 6.
- `ASC NULLS LAST`: Farid 1, Ben 2, Asha and Dev 3, NULLs 5.

**Code:** run with `python3 -I`.
```python
# Q29: NULLs inside window ORDER BY (SQLite 3.45) and pandas na_option
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,50),(3,'Chitra',10,NULL),
  (4,'Dev',10,70),(5,'Esha',10,NULL),(6,'Farid',10,40);
"""
SQL_MAIN = """
SELECT emp_id, name, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn_desc,
  RANK()       OVER (ORDER BY salary DESC)         AS rk_desc,
  ROW_NUMBER() OVER (ORDER BY salary ASC, emp_id)  AS rn_asc,
  RANK()       OVER (ORDER BY salary ASC)          AS rk_asc,
  RANK()       OVER (ORDER BY salary DESC NULLS FIRST) AS rk_desc_nf,
  RANK()       OVER (ORDER BY salary ASC  NULLS LAST)  AS rk_asc_nl
FROM employees
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (SQLite", sqlite3.sqlite_version + "):"); print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
s = emp["salary"]
pd_df = emp[["emp_id", "name", "salary"]].copy()
pd_df["rn_desc"] = s.rank(method="first", ascending=False, na_option="bottom")
pd_df["rk_desc"] = s.rank(method="min", ascending=False, na_option="bottom")
pd_df["rn_asc"] = s.rank(method="first", ascending=True, na_option="top")
pd_df["rk_asc"] = s.rank(method="min", ascending=True, na_option="top")
pd_df["rk_desc_nf"] = s.rank(method="min", ascending=False, na_option="top")
pd_df["rk_asc_nl"] = s.rank(method="min", ascending=True, na_option="bottom")
keep = s.rank(method="min", ascending=False, na_option="keep")
# pd:end
pd_df = pd_df.astype({c: "int64" for c in pd_df.columns if c.startswith(("rn_", "rk_"))})
print("\npandas (na_option 'bottom' for DESC default, 'top' for ASC default):"); print(pd_df.to_string(index=False))
print("\nna_option='keep' (no SQL equivalent):", keep.tolist())
# compared by emp_id (both already in emp_id order)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

# NULL keys are peers: same rank, and ROW_NUMBER only separates them via the tie-breaker
assert sql_df.loc[sql_df.salary.isna(), "rk_desc"].nunique() == 1
# without a tie-breaker, ROW_NUMBER on the NULL rows is allowed to vary; show it is only fixed by emp_id
print("\nNULL rows get rn_desc", sql_df.loc[sql_df.salary.isna(), "rn_desc"].tolist(),
      "because emp_id breaks the tie")
print("asserts passed: SQL == pandas for all six rank columns")
```

**Output (my run):**
```text
SQL (SQLite 3.45.1):
 emp_id   name  salary  rn_desc  rk_desc  rn_asc  rk_asc  rk_desc_nf  rk_asc_nl
      1   Asha    70.0        1        1       5       5           3          3
      2    Ben    50.0        3        3       4       4           5          2
      3 Chitra     NaN        5        5       1       1           1          5
      4    Dev    70.0        2        1       6       5           3          3
      5   Esha     NaN        6        5       2       1           1          5
      6  Farid    40.0        4        4       3       3           6          1

pandas (na_option 'bottom' for DESC default, 'top' for ASC default):
 emp_id   name  salary  rn_desc  rk_desc  rn_asc  rk_asc  rk_desc_nf  rk_asc_nl
      1   Asha    70.0        1        1       5       5           3          3
      2    Ben    50.0        3        3       4       4           5          2
      3 Chitra     NaN        5        5       1       1           1          5
      4    Dev    70.0        2        1       6       5           3          3
      5   Esha     NaN        6        5       2       1           1          5
      6  Farid    40.0        4        4       3       3           6          1

na_option='keep' (no SQL equivalent): [1.0, 3.0, nan, 1.0, nan, 4.0]

NULL rows get rn_desc [5, 6] because emp_id breaks the tie
asserts passed: SQL == pandas for all six rank columns
```

**Edge cases:**
- NULLs are peers: both NULL rows get the same `RANK` (5 under `DESC`, 1 under `ASC`) and the next non-NULL rank skips accordingly. Only `ROW_NUMBER` separates them, and only via the tie-breaker.
- `NULLS FIRST` / `NULLS LAST` ran without error on SQLite 3.45.1. The SQLite documentation page I opened does not say how NULLs sort in a window `ORDER BY`; I measured it, and from general knowledge the syntax arrived in SQLite 3.30.
- An all-NULL partition: every row is a peer, so `RANK` is 1 for all, and `ROW_NUMBER` depends entirely on the tie-breaker.
- pandas `na_option="keep"` returns NaN for those rows (printed as `[1.0, 3.0, nan, 1.0, nan, 4.0]`), and the result is a float column.

**Then explain:**
- **Default placement:** SQLite treats NULL as smaller than any value (measured). PostgreSQL treats NULL as larger than any value by default, so `DESC` puts NULLs first there; MySQL treats them as smaller like SQLite (both from memory, not executed). Do not rely on a default across engines: write `NULLS FIRST` / `NULLS LAST` where the engine supports it (PostgreSQL does; MySQL does not have the syntax as far as I know, not executed) or add `CASE WHEN salary IS NULL THEN 1 ELSE 0 END` as the first sort key.
- **Why it matters:** a top-N by salary `DESC` is fine in SQLite because NULLs sink, but in PostgreSQL the NULLs would be rank 1.
- **Peers:** "peer" means equal on all `ORDER BY` keys; NULL equals NULL for this purpose even though `NULL = NULL` is unknown in `WHERE`.
- **pandas:** `keep` leaves NaN unranked, which is usually what you want for analysis; `top` / `bottom` are the SQL-like choices. The two direction and `na_option` settings are independent, which is why `DESC NULLS FIRST` needs `ascending=False, na_option="top"`.

**Follow-ups:**
- *How do you push NULLs to the end in an engine without `NULLS LAST`?* A leading `CASE WHEN col IS NULL THEN 1 ELSE 0 END` key.
- *Should NULL salaries get a rank at all?* Often not: filter them first (`WHERE salary IS NOT NULL`) or in pandas keep NaN.
- *Does `ORDER BY` in the window decide the output order?* No, see Q37.

**Common mistakes:**
- Assuming NULLs sort the same way in every engine.
- Forgetting that NULLs can take rank 1 in a `DESC` ranking on engines that treat them as largest.
- Using pandas `rank()` and expecting NaN rows to be ranked.
- Comparing the pandas float ranks to integer SQL ranks without casting.

### Q30 ⭐⭐ 🟡 pandas rank and NaN handling versus SQL: a Series of salaries with NaN and ties. Show rank() with na_option 'keep' (NaN stays NaN, result is float), 'top' and 'bottom', method 'average' versus 'min', 'max', 'first' and 'dense', ascending=False, and pct=True. Contrast with SQL (NULLs always get a rank; NULL ordering depends on the engine). Explain how to cast the result to a nullable integer after dropping NaN, and what rank returns with groupby (ranks restart per group).
**Asked at:** pandas reference and user guide (DataFrame.rank, qcut; groupby, Comparison with SQL), not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** pandas `rank()` leaves NaN unranked (`na_option="keep"`) and returns floats, `method` picks the tie rule (`min` is SQL `RANK`, `dense` is `DENSE_RANK`, `first` is `ROW_NUMBER` in row order, `average` and `max` have no direct SQL function), and with `groupby` the ranks restart per group; SQL always gives NULLs a rank, placed by the engine's NULL ordering.

**Schema and sample data:** eight employees in two departments, NULL salaries in both, a tie at 70 and a tie at 40.
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO emp VALUES (1,10,70),(2,10,50),(3,10,NULL),(4,10,70),(5,20,NULL),(6,20,40),(7,20,40),(8,20,60);
```

**SQL answer:** `SQL_MAIN` (company-wide, NULLs last) and `SQL_GROUP` (per department, NULL rows removed first) in the Code block. Tie-breaking: `ROW_NUMBER` ends with `emp_id`; `RANK` and `DENSE_RANK` share ranks on ties by design.
```sql
SELECT emp_id, salary,
  RANK()       OVER (ORDER BY salary DESC NULLS LAST)         AS rk,
  DENSE_RANK() OVER (ORDER BY salary DESC NULLS LAST)         AS dr,
  ROW_NUMBER() OVER (ORDER BY salary DESC NULLS LAST, emp_id) AS rn
FROM emp ORDER BY emp_id
```
```sql
SELECT emp_id, dept_id, salary,
  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk_in_dept
FROM emp WHERE salary IS NOT NULL
ORDER BY emp_id
```

**pandas answer:** inside `# pd:main` in the Code block: all five methods side by side, the three `na_option` values, `pct=True`, and the grouped rank.
```python
s = emp["salary"]
methods = pd.DataFrame({m: s.rank(method=m, ascending=False)
                        for m in ["average", "min", "max", "first", "dense"]})
na = pd.DataFrame({o: s.rank(method="min", ascending=False, na_option=o)
                   for o in ["keep", "top", "bottom"]})
pct = pd.DataFrame({"pct_max": s.rank(method="max", ascending=False, pct=True),
                    "pct_min": s.rank(method="min", ascending=False, pct=True)})
pd_df = pd.DataFrame({"emp_id": emp["emp_id"], "salary": s,
                      "rk": s.rank(method="min", ascending=False, na_option="bottom"),
                      "dr": s.rank(method="dense", ascending=False, na_option="bottom"),
                      "rn": s.rank(method="first", ascending=False, na_option="bottom")})
in_dept = emp.dropna(subset=["salary"]).copy()
in_dept["rk_in_dept"] = in_dept.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("Int64")
```

**Example:** salaries sorted high to low are 70, 70, 60, 50, 40, 40 and two NaN.
- Tied 70s: `average` 1.5, `min` 1, `max` 2, `first` 1 and 2 (row order), `dense` 1. SQL `RANK` gives 1 and 1, `ROW_NUMBER` 1 and 2.
- Tied 40s: `min` 5, `max` 6, `average` 5.5, `dense` 4.
- `na_option="keep"`: the NaN rows stay NaN. `"bottom"`: they take rank 7 (tied, with `min`). `"top"`: they take rank 1 and everyone else shifts down by two. SQL with `NULLS LAST` matches `"bottom"`: rank 7, dense rank 5.
- `pct=True`: `method="max"` gives 70 as 2/6 = 0.3333 and the bottom 40s as 6/6 = 1.0; the default `method="average"` would use the average rank instead. The NaN rows are not counted in `n`.
- Per department (NaN dropped): dept 10 has 70, 70, 50 so ranks 1, 1, 3; dept 20 has 60, 40, 40 so ranks 1, 2, 2 (restart at 1 for each group).

**Code:** run with `python3 -I`.
```python
# Q30: pandas rank and NaN handling versus SQL
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO emp VALUES (1,10,70),(2,10,50),(3,10,NULL),(4,10,70),(5,20,NULL),(6,20,40),(7,20,40),(8,20,60);
"""
SQL_MAIN = """
SELECT emp_id, salary,
  RANK()       OVER (ORDER BY salary DESC NULLS LAST)         AS rk,
  DENSE_RANK() OVER (ORDER BY salary DESC NULLS LAST)         AS dr,
  ROW_NUMBER() OVER (ORDER BY salary DESC NULLS LAST, emp_id) AS rn
FROM emp ORDER BY emp_id
"""
SQL_GROUP = """
SELECT emp_id, dept_id, salary,
  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk_in_dept
FROM emp WHERE salary IS NOT NULL
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_grp = pd.read_sql_query(SQL_GROUP, con)
print("SQL (NULLs ranked last):"); print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM emp ORDER BY emp_id", con)
# pd:main
s = emp["salary"]
methods = pd.DataFrame({m: s.rank(method=m, ascending=False)
                        for m in ["average", "min", "max", "first", "dense"]})
na = pd.DataFrame({o: s.rank(method="min", ascending=False, na_option=o)
                   for o in ["keep", "top", "bottom"]})
pct = pd.DataFrame({"pct_max": s.rank(method="max", ascending=False, pct=True),
                    "pct_min": s.rank(method="min", ascending=False, pct=True)})
pd_df = pd.DataFrame({"emp_id": emp["emp_id"], "salary": s,
                      "rk": s.rank(method="min", ascending=False, na_option="bottom"),
                      "dr": s.rank(method="dense", ascending=False, na_option="bottom"),
                      "rn": s.rank(method="first", ascending=False, na_option="bottom")})
in_dept = emp.dropna(subset=["salary"]).copy()
in_dept["rk_in_dept"] = in_dept.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("Int64")
# pd:end
print("\npandas methods (ascending=False, na_option='keep'):"); print(methods.assign(salary=s).to_string())
print("\nna_option (method='min'):"); print(na.assign(salary=s).to_string())
print("\npct=True (NaN not counted in n=6):"); print(pct.assign(salary=s).round(4).to_string())
print("dtype of rank:", s.rank().dtype, "| after cast to nullable Int64:", s.rank(method="min").astype("Int64").dtype)
print("\nper-department rank (NaN rows dropped first):"); print(in_dept.to_string(index=False))

pd_cmp = pd_df.astype({"rk": "int64", "dr": "int64", "rn": "int64"})
pd.testing.assert_frame_equal(sql_df, pd_cmp, check_dtype=False)   # both in emp_id order
pd.testing.assert_frame_equal(sql_grp.reset_index(drop=True),
                              in_dept.astype({"rk_in_dept": "int64"}).reset_index(drop=True), check_dtype=False)
# ranks without a tie-breaker: method='first' follows row order, so rn is deterministic only because emp is sorted by emp_id
print("asserts passed: SQL RANK/DENSE_RANK/ROW_NUMBER == pandas min/dense/first (compared in emp_id order); per-dept == groupby rank")
```

**Output (my run):**
```text
SQL (NULLs ranked last):
 emp_id  salary  rk  dr  rn
      1    70.0   1   1   1
      2    50.0   4   3   4
      3     NaN   7   5   7
      4    70.0   1   1   2
      5     NaN   7   5   8
      6    40.0   5   4   5
      7    40.0   5   4   6
      8    60.0   3   2   3

pandas methods (ascending=False, na_option='keep'):
   average  min  max  first  dense  salary
0      1.5  1.0  2.0    1.0    1.0    70.0
1      4.0  4.0  4.0    4.0    3.0    50.0
2      NaN  NaN  NaN    NaN    NaN     NaN
3      1.5  1.0  2.0    2.0    1.0    70.0
4      NaN  NaN  NaN    NaN    NaN     NaN
5      5.5  5.0  6.0    5.0    4.0    40.0
6      5.5  5.0  6.0    6.0    4.0    40.0
7      3.0  3.0  3.0    3.0    2.0    60.0

na_option (method='min'):
   keep  top  bottom  salary
0   1.0  3.0     1.0    70.0
1   4.0  6.0     4.0    50.0
2   NaN  1.0     7.0     NaN
3   1.0  3.0     1.0    70.0
4   NaN  1.0     7.0     NaN
5   5.0  7.0     5.0    40.0
6   5.0  7.0     5.0    40.0
7   3.0  5.0     3.0    60.0

pct=True (NaN not counted in n=6):
   pct_max  pct_min  salary
0   0.3333   0.1667    70.0
1   0.6667   0.6667    50.0
2      NaN      NaN     NaN
3   0.3333   0.1667    70.0
4      NaN      NaN     NaN
5   1.0000   0.8333    40.0
6   1.0000   0.8333    40.0
7   0.5000   0.5000    60.0
dtype of rank: float64 | after cast to nullable Int64: Int64

per-department rank (NaN rows dropped first):
 emp_id  dept_id  salary  rk_in_dept
      1       10    70.0           1
      2       10    50.0           3
      4       10    70.0           1
      6       20    40.0           2
      7       20    40.0           2
      8       20    60.0           1
asserts passed: SQL RANK/DENSE_RANK/ROW_NUMBER == pandas min/dense/first (compared in emp_id order); per-dept == groupby rank
```

**Edge cases:**
- Ranks are `float64`. Because NaN cannot live in an int64 column, casting needs either dropping NaN first and `astype("int64")`, or the nullable type: `s.rank(method="min").astype("Int64")` worked on the NaN-containing result in my run and gives `<NA>` for the NaN rows.
- `method="first"` depends on row order in the frame, so sort (or include an id sort) before ranking if you need it reproducible. I compared in `emp_id` order, where it matches `ROW_NUMBER ... emp_id`.
- SQL gives NULLs a rank; pandas by default does not. If you want SQL's behaviour you must choose `top` or `bottom` (see Q29).
- An all-NaN group returns all NaN under `keep`.
- `pct=True` with `method="max"` is rank divided by the number of non-NaN values; that is the SQL `CUME_DIST` idea (Q36 checks it).

**Then explain:**
- **Method mapping:** `min` is `RANK`, `dense` is `DENSE_RANK`, `first` is `ROW_NUMBER` with ties in row order, `max` is the last position among tied rows, `average` is the mean of the tied positions.
- **No SQL function for `average`/`max`:** you can derive them, for example `rank + count_of_peers - 1` for `max`.
- **`ascending=False`:** pandas ranks smallest as 1 by default. For "highest salary is rank 1" always pass `ascending=False`.
- **With `groupby`:** `df.groupby("dept_id")["salary"].rank(...)` is `PARTITION BY dept_id`; the result keeps the original index, one value per row.
- **NULL ordering across engines:** SQL engines disagree on where NULLs sort (see Q29); pandas avoids the question by leaving them out.

**Follow-ups:**
- *How do you rank on two columns in pandas?* `rank` ranks one column; sort by both and use `ngroup` or positions (Q27).
- *How do you get "top 3 per group" from rank?* `groupby().rank(method="dense", ascending=False) <= 3` (Q31).
- *Why does rank return floats even with no NaN?* The `average` default can produce halves; the other methods still return floats.

**Common mistakes:**
- Using the default ascending order and calling the lowest value "top".
- Expecting `method="first"` to be reproducible on an unsorted frame.
- Forgetting that NaN rows come back as NaN and then filtering `rank <= 3`, which silently drops them (a good thing, but know it).
- Casting a rank column containing NaN to `int64`: it raises. Use `Int64` or drop NaN first.

### Q31 ⭐⭐ 🟡 Top-N per group in pandas, with tie awareness: a DataFrame emp(emp_id, dept_id, salary) with ties. Show sort_values + groupby().head(n), groupby()['salary'].nlargest(n) (keep='first' default versus keep='all'), and groupby().rank(method='dense', ascending=False) <= n, and say which SQL window pattern each matches (ROW_NUMBER, ROW_NUMBER with arbitrary ties, DENSE_RANK). Give the equivalent SQL for one of them, confirm the rows match on small data, and explain the index shape returned by each.
**Asked at:** pandas reference and user guide (DataFrame.rank, qcut; groupby, Comparison with SQL), not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** In pandas, sort then `groupby().head(n)` is `ROW_NUMBER() <= n` (exactly n rows per group), `groupby()["salary"].nlargest(n)` is also exactly n rows but breaks ties by row order (arbitrary unless the frame order is meaningful), `nlargest(n, keep="all")` keeps every row tied at the cut-off and so matches `RANK() <= n`, and `groupby().rank(method="dense", ascending=False) <= n` matches `DENSE_RANK() <= n` (the n highest distinct values).

**Schema and sample data:** two departments with ties around the cut-off at n = 2. Department 10 has 100, 90, 90, 80, 70; department 20 has 60, 60, 60, 50.
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO emp VALUES (1,10,100),(2,10,90),(3,10,90),(4,10,80),(5,10,70),
                       (6,20,60),(7,20,60),(8,20,60),(9,20,50);
```

**SQL answer:** three queries in the Code block, `SQL_RN`, `SQL_RANK` and `SQL_DENSE`. Tie-breaking: `ROW_NUMBER` ends with `emp_id`, so it is deterministic (lowest `emp_id` wins a tie); `RANK` and `DENSE_RANK` keep all tied rows. `SQL_RN` is the one I use for "exactly 2 per department":
```sql
SELECT emp_id, dept_id, salary FROM (
  SELECT emp_id, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS pos
  FROM emp) WHERE pos <= 2 ORDER BY dept_id, salary DESC, emp_id
```

**pandas answer:** four forms inside `# pd:main` in the Code block.
```python
n = 2
head_df = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
              .groupby("dept_id").head(n))
nl_first = emp.groupby("dept_id")["salary"].nlargest(n)                # keep='first' is the default
nl_all = emp.groupby("dept_id")["salary"].nlargest(n, keep="all")
dense_df = emp[emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False) <= n]
```

**Example:** n = 2.
- `ROW_NUMBER`: department 10 gives emp 1 (100) and emp 2 (90; emp 3 is the other 90 and loses the tie-break). Department 20 gives emp 6 and 7 (the three 60s are split by `emp_id`). Result 1, 2, 6, 7.
- `RANK <= 2`: department 10: 100 is rank 1, both 90s are rank 2, so emp 1, 2, 3; department 20: all three 60s are rank 1 and 50 is rank 4, so 6, 7, 8. Result 1, 2, 3, 6, 7, 8. This equals `nlargest(2, keep="all")`.
- `DENSE_RANK <= 2`: department 20 has only two distinct values in the top 2 (60 and 50), so emp 9 is included: 1, 2, 3, 6, 7, 8, 9.
- `nlargest(2)` default keeps the first tied row in frame order: 1, 2, 6, 7. With the frame reversed it picked 1, 3, 7, 8 (the Code block prints this), so it is arbitrary unless you control the row order.

**Code:** run with `python3 -I`.
```python
# Q31: top-N per group in pandas with tie awareness: head, nlargest (keep first/all), rank dense
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO emp VALUES (1,10,100),(2,10,90),(3,10,90),(4,10,80),(5,10,70),
                       (6,20,60),(7,20,60),(8,20,60),(9,20,50);
"""
SQL_RN = """
SELECT emp_id, dept_id, salary FROM (
  SELECT emp_id, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS pos
  FROM emp) WHERE pos <= 2 ORDER BY dept_id, salary DESC, emp_id
"""
SQL_RANK = """
SELECT emp_id, dept_id, salary FROM (
  SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS pos
  FROM emp) WHERE pos <= 2 ORDER BY dept_id, salary DESC, emp_id
"""
SQL_DENSE = """
SELECT emp_id, dept_id, salary FROM (
  SELECT emp_id, dept_id, salary, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS pos
  FROM emp) WHERE pos <= 2 ORDER BY dept_id, salary DESC, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
sql_rn, sql_rank, sql_dense = q(SQL_RN), q(SQL_RANK), q(SQL_DENSE)
for name, d in [("ROW_NUMBER <= 2", sql_rn), ("RANK <= 2", sql_rank), ("DENSE_RANK <= 2", sql_dense)]:
    print("SQL", name, "-> emp_ids", d["emp_id"].tolist())

emp = pd.read_sql_query("SELECT * FROM emp ORDER BY emp_id", con)   # row order = emp_id order
# pd:main
n = 2
head_df = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
              .groupby("dept_id").head(n))
nl_first = emp.groupby("dept_id")["salary"].nlargest(n)                # keep='first' is the default
nl_all = emp.groupby("dept_id")["salary"].nlargest(n, keep="all")
dense_df = emp[emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False) <= n]
# pd:end
ids = lambda d: sorted(d["emp_id"].tolist())
nl_first_ids = sorted(emp.loc[nl_first.index.get_level_values(1), "emp_id"].tolist())
nl_all_ids = sorted(emp.loc[nl_all.index.get_level_values(1), "emp_id"].tolist())
print("\npandas head(2) after sort   :", ids(head_df), "| index type:", type(head_df.index).__name__)
print("pandas nlargest keep='first':", nl_first_ids, "| index levels:", list(nl_first.index.names))
print("pandas nlargest keep='all'  :", nl_all_ids, "| index levels:", list(nl_all.index.names))
print("pandas dense rank <= 2      :", ids(dense_df), "| index type:", type(dense_df.index).__name__)
print("\nnlargest keep='first' as a Series:"); print(nl_first.to_string())

assert ids(head_df) == sql_rn["emp_id"].tolist() == [1, 2, 6, 7]
assert nl_first_ids == sql_rn["emp_id"].tolist()          # only because emp is in emp_id order
assert nl_all_ids == sorted(sql_rank["emp_id"].tolist()) == [1, 2, 3, 6, 7, 8]
assert ids(dense_df) == sorted(sql_dense["emp_id"].tolist()) == [1, 2, 3, 6, 7, 8, 9]
# keep='first' follows the frame's row order: reverse the rows and it picks the other tied row
rev = emp.iloc[::-1]
rev_first = sorted(rev.loc[rev.groupby("dept_id")["salary"].nlargest(n).index.get_level_values(1), "emp_id"].tolist())
print("\nsame nlargest keep='first' on the frame in reverse row order picks emp_ids:", rev_first)
assert rev_first != sql_rn["emp_id"].tolist()
print("asserts passed (compared as sorted emp_id lists)")
```

**Output (my run):**
```text
SQL ROW_NUMBER <= 2 -> emp_ids [1, 2, 6, 7]
SQL RANK <= 2 -> emp_ids [1, 2, 3, 6, 7, 8]
SQL DENSE_RANK <= 2 -> emp_ids [1, 2, 3, 6, 7, 8, 9]

pandas head(2) after sort   : [1, 2, 6, 7] | index type: Index
pandas nlargest keep='first': [1, 2, 6, 7] | index levels: ['dept_id', None]
pandas nlargest keep='all'  : [1, 2, 3, 6, 7, 8] | index levels: ['dept_id', None]
pandas dense rank <= 2      : [1, 2, 3, 6, 7, 8, 9] | index type: Index

nlargest keep='first' as a Series:
dept_id   
10       0    100
         1     90
20       5     60
         6     60

same nlargest keep='first' on the frame in reverse row order picks emp_ids: [1, 3, 7, 8]
asserts passed (compared as sorted emp_id lists)
```

**Edge cases:**
- Index shapes: `head` returns the original rows with their original index labels (a flat index); `nlargest` on a `SeriesGroupBy` returns a Series with a two-level index (`dept_id` and the original row label), values only (no `emp_id` column); the dense-rank mask returns a filtered frame with the original index. To get rows from the `nlargest` result I looked the labels up with `emp.loc[...index.get_level_values(1)]`.
- Group smaller than n: `head`, `nlargest` and the rank forms simply return fewer rows; SQL does the same.
- NaN salaries: `nlargest` skips them; `rank` leaves them NaN, so `<= n` is False for them; in SQL put `WHERE salary IS NOT NULL` or know where NULLs sort (Q29). I did not put NaN in this table.
- `keep="all"` can return more than n rows per group, so the output size is not capped.

**Then explain:**
- **Match table:** `head(n)` after a full sort is `ROW_NUMBER`; `nlargest(n)` is `ROW_NUMBER` with tie order left to chance; `nlargest(n, keep="all")` is `RANK`; `rank(method="dense")` is `DENSE_RANK`.
- **Why sort first for `head`:** `head` takes the first rows in current order, so without the sort it returns arbitrary rows. Include the tie-break key in the sort.
- **Cost:** `nlargest` per group avoids a full sort and is simple; the sort-based forms are clearer with several tie keys.
- **Confirming equality:** I compared the sorted `emp_id` lists from each pandas form with the matching SQL query, and all four asserts pass.

**Follow-ups:**
- *Which do you use for "top 2 salaries per department, ties included"?* `DENSE_RANK` or `RANK` depending on whether "2 salaries" means 2 distinct values (dense) or the cut-off position (rank); I say which one.
- *How do you flatten the `nlargest` result?* `.reset_index(level=0)` or look up rows by label as above.
- *Can `groupby().apply(lambda g: g.nlargest(n, "salary"))` do this?* Yes, it returns whole rows, but it is slower on many groups (I did not time it).

**Common mistakes:**
- Calling `head(n)` without sorting.
- Assuming `nlargest(n)` returns all ties; it needs `keep="all"`.
- Saying `keep="all"` matches `DENSE_RANK`; it matches `RANK` (the tied 60s here, and no 50).
- Forgetting the two-level index of the grouped `nlargest` and then joining on the wrong labels.

### Q32 ⭐⭐ 🟡 groupby().cumcount() and transform('size'/'max') as window functions: orders(order_id, customer_id, amount, order_date). Reproduce ROW_NUMBER() (cumcount()+1 after sort), COUNT(*) OVER (PARTITION BY customer_id) (transform('size')), MAX(amount) OVER (PARTITION BY customer_id) (transform('max')) and 'is last order of customer' flag. Explain that cumcount follows current row order (so sort first), that it starts at 0, why transform keeps the original index, and show the SQL version running on SQLite and asserting equal results.
**Asked at:** pandas reference and user guide (DataFrame.rank, qcut; groupby, Comparison with SQL), not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `ROW_NUMBER() OVER (PARTITION BY c ORDER BY ...)` is `groupby("c").cumcount() + 1` on a frame you sorted by those keys (cumcount counts in current row order and starts at 0), `COUNT(*) OVER (PARTITION BY c)` is `transform("size")`, `MAX(x) OVER (PARTITION BY c)` is `transform("max")`, and "is the last order" is `ROW_NUMBER() ... DESC = 1` or `cumcount(ascending=False) == 0`.

**Schema and sample data:** six orders, inserted out of date order; customer 1 has two orders on the same date.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, order_date TEXT);
INSERT INTO orders VALUES (1,1,50,'2026-01-03'),(2,2,70,'2026-01-01'),(3,1,80,'2026-01-01'),
                          (4,1,50,'2026-01-03'),(5,3,30,'2026-01-02'),(6,2,20,'2026-01-05');
```

**SQL answer:** `SQL_MAIN` in the Code block. Tie-breaking: customer 1's orders 1 and 4 share a date, so both the ascending and the descending `ROW_NUMBER` end with `order_id` (ascending and descending respectively), which makes "the last order" mean the highest `order_id` on that date. `COUNT(*)` and `MAX` have no `ORDER BY`, so each covers the whole partition (no frame question arises).
```sql
SELECT order_id, customer_id, amount, order_date,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn,
       COUNT(*)     OVER (PARTITION BY customer_id)                               AS n_orders,
       MAX(amount)  OVER (PARTITION BY customer_id)                               AS max_amount,
       CASE WHEN ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) = 1
            THEN 1 ELSE 0 END                                                     AS is_last
FROM orders
ORDER BY order_id
```

**pandas answer:** inside `# pd:main` in the Code block. The grouped object is built from the sorted frame, so `cumcount` follows date order; results are assigned back by index label, so the original row order of `orders` is kept.
```python
ordered = orders.sort_values(["order_date", "order_id"])
g = ordered.groupby("customer_id")
pd_df = orders.copy()
pd_df["rn"] = (g.cumcount() + 1)                      # index-aligned: assigned back by label
pd_df["n_orders"] = orders.groupby("customer_id")["order_id"].transform("size")
pd_df["max_amount"] = orders.groupby("customer_id")["amount"].transform("max")
pd_df["is_last"] = (g.cumcount(ascending=False) == 0).astype("int64")
```

**Example:**
- Customer 1 has orders 3 (01-01, amount 80), 1 (01-03, 50) and 4 (01-03, 50). In date order with the id tie-break the positions are 1, 2, 3, so order 3 is `rn` 1, order 1 is 2, order 4 is 3. `n_orders` = 3, `max_amount` = 80, and only order 4 has `is_last` = 1.
- Customer 2: order 2 (01-01) is `rn` 1, order 6 (01-05) is `rn` 2 and last; count 2; max 70.
- Customer 3: one order, `rn` 1, count 1, max 30, and it is also the last order.
- The same orders in file order give a different numbering: `cumcount` on the unsorted frame gives 1, 1, 2, 3, 1, 2 for order_ids 1 to 6, which is wrong for "by date" (order 1 would be customer 1's first order).

**Code:** run with `python3 -I`.
```python
# Q32: groupby().cumcount() and transform('size'/'max') as window functions
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, order_date TEXT);
INSERT INTO orders VALUES (1,1,50,'2026-01-03'),(2,2,70,'2026-01-01'),(3,1,80,'2026-01-01'),
                          (4,1,50,'2026-01-03'),(5,3,30,'2026-01-02'),(6,2,20,'2026-01-05');
"""
SQL_MAIN = """
SELECT order_id, customer_id, amount, order_date,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn,
       COUNT(*)     OVER (PARTITION BY customer_id)                               AS n_orders,
       MAX(amount)  OVER (PARTITION BY customer_id)                               AS max_amount,
       CASE WHEN ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) = 1
            THEN 1 ELSE 0 END                                                     AS is_last
FROM orders
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)   # frame is in order_id order, not date order
# pd:main
ordered = orders.sort_values(["order_date", "order_id"])
g = ordered.groupby("customer_id")
pd_df = orders.copy()
pd_df["rn"] = (g.cumcount() + 1)                      # index-aligned: assigned back by label
pd_df["n_orders"] = orders.groupby("customer_id")["order_id"].transform("size")
pd_df["max_amount"] = orders.groupby("customer_id")["amount"].transform("max")
pd_df["is_last"] = (g.cumcount(ascending=False) == 0).astype("int64")
# pd:end
print("\npandas (original row order kept):"); print(pd_df.to_string())
unsorted_cc = orders.groupby("customer_id").cumcount() + 1
print("\ncumcount WITHOUT sorting by date (follows current row order):", unsorted_cc.tolist())
print("cumcount first value is", orders.groupby("customer_id").cumcount().min(), "(starts at 0, so +1)")
print("index preserved by transform:", pd_df["n_orders"].index.equals(orders.index))
# compared after sorting by order_id
a = sql_df.sort_values("order_id").reset_index(drop=True)
b = pd_df.sort_values("order_id").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)
assert unsorted_cc.tolist() != pd_df["rn"].tolist()
print("asserts passed: SQL window columns == pandas cumcount/transform columns")
```

**Output (my run):**
```text
SQL:
 order_id  customer_id  amount order_date  rn  n_orders  max_amount  is_last
        1            1      50 2026-01-03   2         3          80        0
        2            2      70 2026-01-01   1         2          70        0
        3            1      80 2026-01-01   1         3          80        0
        4            1      50 2026-01-03   3         3          80        1
        5            3      30 2026-01-02   1         1          30        1
        6            2      20 2026-01-05   2         2          70        1

pandas (original row order kept):
   order_id  customer_id  amount  order_date  rn  n_orders  max_amount  is_last
0         1            1      50  2026-01-03   2         3          80        0
1         2            2      70  2026-01-01   1         2          70        0
2         3            1      80  2026-01-01   1         3          80        0
3         4            1      50  2026-01-03   3         3          80        1
4         5            3      30  2026-01-02   1         1          30        1
5         6            2      20  2026-01-05   2         2          70        1

cumcount WITHOUT sorting by date (follows current row order): [1, 1, 2, 3, 1, 2]
cumcount first value is 0 (starts at 0, so +1)
index preserved by transform: True
asserts passed: SQL window columns == pandas cumcount/transform columns
```

**Edge cases:**
- `cumcount` starts at 0 (confirmed: the minimum printed is 0); add 1 for `ROW_NUMBER`.
- Ties in the sort keys: include a unique key (`order_id`) in `sort_values`, or the numbering within the tie depends on the sort algorithm.
- `transform("size")` counts rows including NaN; `transform("count")` counts non-NaN, which matches `COUNT(col)` rather than `COUNT(*)`.
- Groups with NaN keys: `groupby` drops them by default, so `transform` returns NaN for those rows; SQL `PARTITION BY` groups NULLs into one partition. Not in this data, but a known difference.
- `transform` keeps the original index (confirmed `True`), so the result aligns with the frame without a merge; `agg` would return one row per group.

**Then explain:**
- **Window function as `transform`:** both attach a per-group value to every row without collapsing rows, unlike `GROUP BY` / `agg`.
- **Why sort first:** `cumcount` does not look at any column; it numbers rows as they currently sit within each group. SQL puts the ordering in the `OVER` clause; pandas needs an explicit `sort_values`.
- **Last-row flag:** SQL can compare `rn` to `n_orders` or use a descending `ROW_NUMBER`; pandas has `cumcount(ascending=False)` (0 for the last row), or `groupby().tail(1)` when you want the row itself.
- **Equal results:** I compared all four added columns after sorting both frames by `order_id`.

**Follow-ups:**
- *How would you keep only each customer's last order?* `groupby().tail(1)` on the sorted frame, or the SQL `ROW_NUMBER ... DESC = 1` in a subquery (Q35).
- *What if two orders tie on date and id is not meaningful?* Say so and pick a deterministic rule; there is no honest "latest".
- *Is `COUNT(*) OVER (PARTITION BY ...)` the same as a join to a `GROUP BY`?* Same numbers, but the window keeps one pass and no join key to get wrong.

**Common mistakes:**
- Using `cumcount()` without sorting, then treating it as chronological.
- Forgetting the +1.
- Using `groupby(...).agg("size")` and trying to assign it to the frame (length mismatch); use `transform`.
- Describing `MAX(x) OVER (PARTITION BY c ORDER BY d)` as the whole-group maximum: with an `ORDER BY` it becomes a running maximum (Part 5).

### Q33 ⭐⭐ 🟡 qcut versus NTILE: a column of 10 spend values with ties. Bucket into quartiles with SQL NTILE(4) and with pandas pd.qcut(x, 4, labels=False) and show they can differ (NTILE is positional and splits ties across buckets; qcut cuts on quantile values so ties stay together and bucket sizes can differ or duplicates='drop' is needed). Show how to reproduce NTILE in pandas (rank(method='first') then qcut or floor arithmetic), and how pd.cut differs (equal-width bins).
**Asked at:** pandas reference and user guide (DataFrame.rank, qcut; groupby, Comparison with SQL), not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `NTILE(4)` is positional (sort the rows, deal them into 4 buckets of near-equal size, bigger buckets first, and it will split tied values across buckets), `pd.qcut(x, 4)` cuts on quantile values (equal-ish counts, but tied values land in the same bin so sizes can differ, and it raises on duplicate edges unless `duplicates="drop"`), and `pd.cut` makes equal-width bins; to reproduce `NTILE` in pandas, rank with `method="first"` and use the bucket-size arithmetic.

**Schema and sample data:** ten customers' spend with ties at 20 (three rows) and 40 (two rows).
```sql
CREATE TABLE spend(cust_id INTEGER PRIMARY KEY, amount INTEGER);
INSERT INTO spend VALUES (1,10),(2,20),(3,20),(4,20),(5,30),(6,40),(7,40),(8,50),(9,60),(10,100);
```

**SQL answer:** `SQL_MAIN` in the Code block. Tie-breaking: `ORDER BY amount, cust_id` makes the split of the tied 20s and 40s reproducible (lowest `cust_id` goes to the lower bucket); without `cust_id`, which tied row lands in which bucket is not defined.
```sql
SELECT cust_id, amount,
       NTILE(4) OVER (ORDER BY amount, cust_id) AS ntile4
FROM spend
ORDER BY cust_id
```

**pandas answer:** inside `# pd:main` in the Code block: the NTILE reproduction (`ntile_pd`), `qcut` on values, `qcut` on the rank positions, and `cut`. The arithmetic: with n rows and k buckets, `q, r = divmod(n, k)`; the first r buckets hold q+1 rows, the rest hold q.
```python
x = spend["amount"]
k = 4
pos = x.rank(method="first")                                  # 1..n, ties broken by row order (cust_id order)
n = len(x)
q, r = divmod(n, k)                                           # NTILE: first r buckets get q+1 rows
big = r * (q + 1)
ntile_pd = np.where(pos <= big, np.ceil(pos / (q + 1)), r + np.ceil((pos - big) / q)).astype("int64")
qcut_vals = pd.qcut(x, k, labels=False) + 1                   # cuts on quantile VALUES
qcut_rank = pd.qcut(pos, k, labels=False) + 1                 # qcut on positions
cut_vals = pd.cut(x, k, labels=False) + 1                     # equal-WIDTH bins
```

**Example:** n = 10, k = 4, so q = 2, r = 2: buckets of 3, 3, 2, 2.
- `NTILE(4)`: rows 1-3 (10, 20, 20) are bucket 1, rows 4-6 (20, 30, 40) bucket 2, rows 7-8 (40, 50) bucket 3, rows 9-10 (60, 100) bucket 4. The three 20s are split across buckets 1 and 2, and the two 40s across 2 and 3.
- `qcut(amount, 4)`: edges 10, 20, 35, 47.5, 100. All 20s are in bin 1, both 40s in bin 3, so sizes are 4, 1, 2, 3 (not equal).
- `qcut` on the `rank(method="first")` positions: sizes 3, 2, 2, 3. Even with no ties it differs from `NTILE` (3, 3, 2, 2) because `qcut` places the cut points by linear interpolation of positions, while `NTILE` gives the extra rows to the first buckets.
- `cut(amount, 4)`: equal-width bins on the value range (about 9.91 to 100, width 22.5 each), so sizes 5, 3, 1, 1: one outlier (100) drags the bins.
- Other sizes in the Code block: n = 7 gives NTILE sizes 2, 2, 2, 1 and qcut sizes 2, 2, 1, 2; n = 9 gives the same 3, 2, 2, 2 for both.

**Code:** run with `python3 -I`.
```python
# Q33: qcut versus NTILE (and cut)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE spend(cust_id INTEGER PRIMARY KEY, amount INTEGER);
INSERT INTO spend VALUES (1,10),(2,20),(3,20),(4,20),(5,30),(6,40),(7,40),(8,50),(9,60),(10,100);
"""
SQL_MAIN = """
SELECT cust_id, amount,
       NTILE(4) OVER (ORDER BY amount, cust_id) AS ntile4
FROM spend
ORDER BY cust_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
spend = pd.read_sql_query("SELECT * FROM spend ORDER BY cust_id", con)
# pd:main
x = spend["amount"]
k = 4
pos = x.rank(method="first")                                  # 1..n, ties broken by row order (cust_id order)
n = len(x)
q, r = divmod(n, k)                                           # NTILE: first r buckets get q+1 rows
big = r * (q + 1)
ntile_pd = np.where(pos <= big, np.ceil(pos / (q + 1)), r + np.ceil((pos - big) / q)).astype("int64")
qcut_vals = pd.qcut(x, k, labels=False) + 1                   # cuts on quantile VALUES
qcut_rank = pd.qcut(pos, k, labels=False) + 1                 # qcut on positions
cut_vals = pd.cut(x, k, labels=False) + 1                     # equal-WIDTH bins
# pd:end
res = spend.assign(ntile4_sql=sql_df["ntile4"], ntile_pd=ntile_pd, qcut=qcut_vals, qcut_on_rank=qcut_rank, cut=cut_vals)
print(res.to_string(index=False))
for c in ["ntile4_sql", "qcut", "qcut_on_rank", "cut"]:
    print(f"bucket sizes {c:13s}:", res[c].value_counts().sort_index().tolist())
print("qcut bin edges:", pd.qcut(x, k, retbins=True)[1].tolist())
print("cut  bin edges:", [round(float(v), 2) for v in pd.cut(x, k, retbins=True)[1]])
# compared in cust_id order (SQL ORDER BY cust_id, frame in cust_id order)
assert sql_df["ntile4"].tolist() == ntile_pd.tolist()
assert qcut_vals.tolist() != ntile_pd.tolist()
assert qcut_rank.tolist() != ntile_pd.tolist()

# other sizes: NTILE puts the extra rows first, qcut-on-position does not
for m in (7, 9, 10):
    c2 = sqlite3.connect(":memory:")
    c2.execute("CREATE TABLE t(v INTEGER)")
    c2.executemany("INSERT INTO t VALUES (?)", [(i,) for i in range(m)])
    nt = [r_[0] for r_ in c2.execute("SELECT NTILE(4) OVER (ORDER BY v) FROM t")]
    qc = (pd.qcut(pd.Series(range(m)), 4, labels=False) + 1).tolist()
    print(f"n={m}: NTILE sizes {np.bincount(nt)[1:].tolist()} | qcut sizes {np.bincount(qc)[1:].tolist()}")

# heavy ties: qcut raises unless duplicates='drop' (then fewer bins)
heavy = pd.Series([5, 5, 5, 5, 5, 1, 2, 9, 9, 10])
try:
    pd.qcut(heavy, 4, labels=False)
except ValueError as ex:
    print("\nqcut on heavy ties raises:", str(ex).splitlines()[0])
print("duplicates='drop' labels:", pd.qcut(heavy, 4, labels=False, duplicates="drop").tolist())
print("asserts passed: NTILE == pandas formula; qcut differs from NTILE on this data")
```

**Output (my run):**
```text
 cust_id  amount  ntile4_sql  ntile_pd  qcut  qcut_on_rank  cut
       1      10           1         1     1             1    1
       2      20           1         1     1             1    1
       3      20           1         1     1             1    1
       4      20           2         2     1             2    1
       5      30           2         2     2             2    1
       6      40           2         2     3             3    2
       7      40           3         3     3             3    2
       8      50           3         3     4             4    2
       9      60           4         4     4             4    3
      10     100           4         4     4             4    4
bucket sizes ntile4_sql   : [3, 3, 2, 2]
bucket sizes qcut         : [4, 1, 2, 3]
bucket sizes qcut_on_rank : [3, 2, 2, 3]
bucket sizes cut          : [5, 3, 1, 1]
qcut bin edges: [10.0, 20.0, 35.0, 47.5, 100.0]
cut  bin edges: [9.91, 32.5, 55.0, 77.5, 100.0]
n=7: NTILE sizes [2, 2, 2, 1] | qcut sizes [2, 2, 1, 2]
n=9: NTILE sizes [3, 2, 2, 2] | qcut sizes [3, 2, 2, 2]
n=10: NTILE sizes [3, 3, 2, 2] | qcut sizes [3, 2, 2, 3]

qcut on heavy ties raises: Bin edges must be unique: Index([1.0, 5.0, 5.0, 8.0, 10.0], dtype='float64').
duplicates='drop' labels: [0, 0, 0, 0, 0, 0, 0, 2, 2, 2]
asserts passed: NTILE == pandas formula; qcut differs from NTILE on this data
```

**Edge cases:**
- Heavy ties: `pd.qcut` on `[5,5,5,5,5,1,2,9,9,10]` raised "Bin edges must be unique" in my run. With `duplicates="drop"` it works but gives fewer bins (three bins here, and the middle label 1 is empty, labels run 0 and 2).
- `labels=False` returns integer bin numbers from 0; add 1 to compare to `NTILE`.
- `NTILE` with fewer rows than buckets: a table of 3 rows with `NTILE(4)` gives buckets 1, 2, 3 (from a separate probe run, not in the Code block; bucket 4 is empty).
- If the amounts have NaN: `qcut` leaves NaN bins as NaN; `NTILE` would put NULLs first in `ASC` order in SQLite (Q29), so filter them.
- The `rank(method="first")` step makes the pandas reproduction deterministic only if the frame's row order is fixed (it is `cust_id` order here).

**Then explain:**
- **Which one to use:** `NTILE` when each bucket must hold the same number of customers (even if equal spenders are split); `qcut` when equal values must share a bucket.
- **Ties:** `NTILE` is unfair to equal values (two customers spending 20 can land in different quartiles); `qcut` is fair but unbalanced.
- **cut versus qcut:** `cut` bins by value range (equal width), `qcut` by quantile (equal frequency, roughly).
- **Dialects:** `NTILE` exists in PostgreSQL, MySQL 8, BigQuery and Snowflake (not executed here); the extra-rows-first rule is documented for SQLite and I measured it; I have not confirmed it for other engines.

**Follow-ups:**
- *How do you do deciles?* `NTILE(10)` / `qcut(x, 10)`; the same points apply.
- *How do you label the buckets?* `labels=["Q1","Q2","Q3","Q4"]` in `qcut`; a `CASE` on the `NTILE` value in SQL.
- *How would you break ties for spend quartiles in a report?* Say that equal spend should share a bucket, then use `qcut`-like logic (or `PERCENT_RANK` thresholds, Q36).

**Common mistakes:**
- Assuming `NTILE(4)` and `qcut(x, 4)` agree.
- Using `NTILE` without a unique tie-breaker and getting a different split on each run.
- Using `cut` when equal counts were wanted.
- Forgetting that `qcut` can raise on duplicate edges.

### Q34 ⭐⭐ 🟡 idxmax versus rank-based selection: employees(emp_id, name, dept_id, salary) with ties and NaN salaries. Pick the highest-paid employee per department in pandas with groupby()['salary'].idxmax() and with transform('max') / rank(method='min') == 1, and compare with the SQL ROW_NUMBER = 1 and RANK = 1 results. Explain that idxmax returns only the first tied label, how NaN salaries and all-NaN groups behave (hedge by running), and when one row per group is wanted.
**Asked at:** pandas reference and user guide (DataFrame.rank, qcut; groupby, Comparison with SQL), not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `groupby()["salary"].idxmax()` returns one row label per group, the first tied row in frame order, so it matches `ROW_NUMBER() = 1` (with row order as the tie-break); `transform("max")` equality or `rank(method="min") == 1` returns every tied row, so it matches `RANK() = 1`; on pandas 3.0.5 `idxmax` raises a ValueError for a group that is entirely NaN, so drop NaN first.

**Schema and sample data:** four departments: 10 has a tie at 90 (Asha, Ben); 20 has two NaN and one real value; 30 is all NULL; 40 has a single employee.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
  (4,'Dev',20,NULL),(5,'Esha',20,60),(6,'Farid',20,NULL),
  (7,'Gita',30,NULL),(8,'Hari',30,NULL),(9,'Ila',40,50);
```

**SQL answer:** `SQL_RN` (one row per department) and `SQL_RANK` (all tied rows) in the Code block, both with `WHERE salary IS NOT NULL` inside, plus `SQL_NO_FILTER` to show what happens without the filter. Tie-breaking: `SQL_RN` orders by `salary DESC, emp_id`, so Asha beats Ben (lowest `emp_id`).
```sql
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS pos
  FROM employees WHERE salary IS NOT NULL)
WHERE pos = 1 ORDER BY dept_id
```
```sql
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS pos
  FROM employees WHERE salary IS NOT NULL)
WHERE pos = 1 ORDER BY dept_id, emp_id
```

**pandas answer:** inside `# pd:main` in the Code block. The frame is read in `emp_id` order, so "first tied row" means lowest `emp_id`, the same rule as the SQL.
```python
valid = emp.dropna(subset=["salary"])
idx_df = emp.loc[valid.groupby("dept_id")["salary"].idxmax()]                       # one row per group, first tied row
max_df = emp[emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")]    # all tied rows
rank_df = emp[emp.groupby("dept_id")["salary"].rank(method="min", ascending=False) == 1]
nofilter_df = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True], na_position="last")
                  .groupby("dept_id").head(1))
```

**Example:**
- Department 10: 90, 90, 70. `ROW_NUMBER = 1` is Asha only (Ben loses the id tie-break), `idxmax` also gives Asha (first in frame order), `RANK = 1` and `transform("max")` give both Asha and Ben.
- Department 20: two NaN and Esha 60. Esha is the max in every method.
- Department 30: all NaN. With the NULL filter there is no row for it. Without the filter (`SQL_NO_FILTER`, `NULLS LAST`) `ROW_NUMBER = 1` returns Gita with a NULL salary, because someone has to be row 1; the pandas `sort_values(..., na_position="last")` plus `head(1)` does the same.
- Department 40: Ila alone, in every method.
- Results: `idxmax` (after dropna) gives emp 1, 5, 9; `RANK = 1` and `transform("max")` give 1, 2, 5, 9; no-filter row number gives 1, 5, 7, 9.

**Code:** run with `python3 -I`.
```python
# Q34: idxmax versus rank-based selection of the top row per group, with ties and NaN
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
  (4,'Dev',20,NULL),(5,'Esha',20,60),(6,'Farid',20,NULL),
  (7,'Gita',30,NULL),(8,'Hari',30,NULL),(9,'Ila',40,50);
"""
SQL_RN = """
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS pos
  FROM employees WHERE salary IS NOT NULL)
WHERE pos = 1 ORDER BY dept_id
"""
SQL_RANK = """
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS pos
  FROM employees WHERE salary IS NOT NULL)
WHERE pos = 1 ORDER BY dept_id, emp_id
"""
SQL_NO_FILTER = """
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC NULLS LAST, emp_id) AS pos
  FROM employees)
WHERE pos = 1 ORDER BY dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
sql_rn, sql_rank, sql_nf = q(SQL_RN), q(SQL_RANK), q(SQL_NO_FILTER)
print("SQL ROW_NUMBER = 1 (NULL salaries filtered):"); print(sql_rn.to_string(index=False))
print("\nSQL RANK = 1 (ties kept):"); print(sql_rank.to_string(index=False))
print("\nSQL ROW_NUMBER = 1 WITHOUT the NULL filter (NULLS LAST):"); print(sql_nf.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
valid = emp.dropna(subset=["salary"])
idx_df = emp.loc[valid.groupby("dept_id")["salary"].idxmax()]                       # one row per group, first tied row
max_df = emp[emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")]    # all tied rows
rank_df = emp[emp.groupby("dept_id")["salary"].rank(method="min", ascending=False) == 1]
nofilter_df = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True], na_position="last")
                  .groupby("dept_id").head(1))
# pd:end
# the raw calls on the data that has NaN
for label, fn in [("idxmax on all groups (skipna=True)", lambda: emp.groupby("dept_id")["salary"].idxmax()),
                  ("idxmax(skipna=False) on dept 20", lambda: emp[emp.dept_id == 20].groupby("dept_id")["salary"].idxmax(skipna=False)),
                  ("idxmax on dept 20 only (NaN rows, one real value, skipna=True)", lambda: emp[emp.dept_id == 20].groupby("dept_id")["salary"].idxmax()),
                  ("idxmax on dept 30 only (all NaN)", lambda: emp[emp.dept_id == 30].groupby("dept_id")["salary"].idxmax()),
                  ("idxmax on dept 10 only", lambda: emp[emp.dept_id == 10].groupby("dept_id")["salary"].idxmax())]:
    try:
        print(f"\n{label}: ->", fn().to_dict())
    except ValueError as ex:
        print(f"\n{label}: raises ValueError: {ex}")
print("\nidxmax after dropna ->", idx_df["emp_id"].tolist(), "| transform('max') ->", max_df["emp_id"].tolist(),
      "| rank==1 ->", rank_df["emp_id"].tolist(), "| sort+head(1) no filter ->", nofilter_df.sort_values("dept_id")["emp_id"].tolist())
key = ["emp_id", "name", "dept_id"]
srt = lambda d: d[key].sort_values("emp_id").reset_index(drop=True)
# compared after sorting by emp_id
pd.testing.assert_frame_equal(srt(idx_df), srt(sql_rn), check_dtype=False)
pd.testing.assert_frame_equal(srt(max_df), srt(sql_rank), check_dtype=False)
pd.testing.assert_frame_equal(srt(rank_df), srt(sql_rank), check_dtype=False)
pd.testing.assert_frame_equal(srt(nofilter_df), srt(sql_nf), check_dtype=False)
assert sql_nf["emp_id"].tolist() == [1, 5, 7, 9]
print("asserts passed: idxmax(after dropna) == ROW_NUMBER; transform('max') == rank==1 == RANK")
```

**Output (my run):**
```text
SQL ROW_NUMBER = 1 (NULL salaries filtered):
 emp_id name  dept_id  salary
      1 Asha       10      90
      5 Esha       20      60
      9  Ila       40      50

SQL RANK = 1 (ties kept):
 emp_id name  dept_id  salary
      1 Asha       10      90
      2  Ben       10      90
      5 Esha       20      60
      9  Ila       40      50

SQL ROW_NUMBER = 1 WITHOUT the NULL filter (NULLS LAST):
 emp_id name  dept_id  salary
      1 Asha       10    90.0
      5 Esha       20    60.0
      7 Gita       30     NaN
      9  Ila       40    50.0

idxmax on all groups (skipna=True): raises ValueError: idxmax with skipna=True encountered all NA values in a group.

idxmax(skipna=False) on dept 20: raises ValueError: idxmax with skipna=False encountered an NA value.

idxmax on dept 20 only (NaN rows, one real value, skipna=True): -> {20: 4}

idxmax on dept 30 only (all NaN): raises ValueError: idxmax with skipna=True encountered all NA values in a group.

idxmax on dept 10 only: -> {10: 0}

idxmax after dropna -> [1, 5, 9] | transform('max') -> [1, 2, 5, 9] | rank==1 -> [1, 2, 5, 9] | sort+head(1) no filter -> [1, 5, 7, 9]
asserts passed: idxmax(after dropna) == ROW_NUMBER; transform('max') == rank==1 == RANK
```

**Edge cases:**
- All-NaN group: on pandas 3.0.5, `idxmax` raised `ValueError: idxmax with skipna=True encountered all NA values in a group` (the Code block runs it on department 30). Older pandas versions behaved differently (from memory, not executed); do not rely on a quiet NaN.
- NaN in a group that also has real values (department 20): `idxmax` with the default `skipna=True` worked and returned label 4 (Esha's row); `skipna=False` raised "encountered an NA value".
- Ties: `idxmax` silently hides them; Ben never appears. If a tie must be reported, use the `transform("max")` form.
- `transform("max") == salary` is never true for NaN, so NaN rows and all-NaN groups drop out; the same for `rank(...) == 1` (rank is NaN for NaN).
- `idxmax` returns index labels, so use `.loc` (not `.iloc`) on a frame whose index is not 0..n-1.

**Then explain:**
- **Which to use:** one row per group wanted (a single "top earner" or "latest row") means `idxmax` or `sort_values + head(1)` with an explicit tie-break; "everyone at the top" means `transform("max")` or `rank == 1`.
- **Mapping to SQL:** `ROW_NUMBER = 1` is exactly one row per partition; `RANK = 1` returns all ties (and `DENSE_RANK = 1` returns the same rows as `RANK = 1`).
- **NULLs:** a SQL `ROW_NUMBER = 1` without a `WHERE salary IS NOT NULL` can return a NULL-salary row in a department with only NULLs. Decide whether such a department should appear.
- **I compared** each pandas form with its SQL twin after sorting by `emp_id`; all four asserts pass.

**Follow-ups:**
- *How do you do the same for the lowest salary?* `idxmin`, `ASC` in the window.
- *Is `sort_values().drop_duplicates("dept_id")` an alternative?* Yes, it is `ROW_NUMBER = 1` again; Q35 uses `drop_duplicates`.
- *What if you also need the second highest?* Switch to `groupby().rank` or `nth`.

**Common mistakes:**
- Using `idxmax` and not noticing tied top earners vanish.
- Calling `idxmax` on data with an all-NaN group and getting an exception (pandas 3.0.5 here).
- Calling `df.loc[idx]` with labels and `df.iloc[idx]` with positions interchangeably after a filter or sort.
- Writing `ROW_NUMBER` with no tie-break and calling the result deterministic.

### Q35 ⭐⭐ 🟡 Delete duplicates keeping the latest row using a window function: logs(log_id, user_id, message, created_at) with duplicate (user_id, message) pairs. Delete all but the latest row of each pair with DELETE FROM logs WHERE log_id IN (SELECT log_id FROM (SELECT log_id, ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn FROM logs) WHERE rn > 1). Show before and after, explain why you SELECT the rows first, mention the CTE-before-DELETE alternative, a PostgreSQL ctid or MySQL derived-table variant (hedged, not executed), and give the pandas drop_duplicates version.
**Asked at:** GeeksforGeeks SQL interview questions (RANK vs DENSE_RANK vs ROW_NUMBER, window functions, duplicates entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** Number the rows inside each `(user_id, message)` group newest first with `ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC)`, then delete every row with `rn > 1`; preview with a `SELECT` before the `DELETE`, and in pandas it is `sort_values(["created_at", "log_id"]).drop_duplicates(subset=[...], keep="last")`.

**Schema and sample data:** nine log rows. User 1's "login" has three rows, two of them at exactly the same timestamp (log 2 and 3); user 2's "login" has two; user 4 has two rows with a NULL message.
```sql
CREATE TABLE logs(log_id INTEGER PRIMARY KEY, user_id INTEGER, message TEXT, created_at TEXT);
INSERT INTO logs VALUES
 (1,1,'login','2026-01-01 10:00'),(2,1,'login','2026-01-02 09:00'),(3,1,'login','2026-01-02 09:00'),
 (4,1,'logout','2026-01-01 11:00'),(5,2,'login','2026-01-03 08:00'),(6,2,'login','2026-01-01 08:00'),
 (7,3,'view','2026-01-01 12:00'),(8,4,NULL,'2026-01-01 13:00'),(9,4,NULL,'2026-01-02 13:00');
```

**SQL answer:** `SQL_PREVIEW` (the SELECT you run first), `SQL_MAIN` (the DELETE) and `SQL_CTE` (the same delete with a CTE in front) in the Code block. Tie-breaking: `log_id DESC` is the last key, so when two rows have the same `created_at` the higher `log_id` is kept. Without it, which of rows 2 and 3 survives is not defined.
```sql
DELETE FROM logs WHERE log_id IN (
  SELECT log_id FROM (
    SELECT log_id,
           ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn
    FROM logs)
  WHERE rn > 1)
```

**pandas answer:** inside `# pd:main` in the Code block. Sorting ascending by time and id and then `keep="last"` keeps the latest row of each group, with the same tie rule (higher `log_id`).
```python
pd_df = (logs.sort_values(["created_at", "log_id"])
             .drop_duplicates(subset=["user_id", "message"], keep="last")
             .sort_values("log_id"))
```

**Example:**
- Group (1, login): rows 1 (01-01 10:00), 2 and 3 (both 01-02 09:00). Newest first with `log_id DESC`: row 3 is `rn` 1, row 2 is `rn` 2, row 1 is `rn` 3. Rows 1 and 2 go.
- Group (2, login): row 5 (01-03) is newest, row 6 (01-01) goes.
- Group (4, NULL): rows 8 and 9; `PARTITION BY` puts both NULLs in one group, so row 9 stays and row 8 goes.
- Groups (1, logout) and (3, view) have one row each and are untouched.
- Preview shows rows 1, 2, 6, 8 (4 rows); after the delete the table holds log_ids 3, 4, 5, 7, 9.

**Code:** run with `python3 -I`.
```python
# Q35: delete duplicates keeping the latest row per (user_id, message)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logs(log_id INTEGER PRIMARY KEY, user_id INTEGER, message TEXT, created_at TEXT);
INSERT INTO logs VALUES
 (1,1,'login','2026-01-01 10:00'),(2,1,'login','2026-01-02 09:00'),(3,1,'login','2026-01-02 09:00'),
 (4,1,'logout','2026-01-01 11:00'),(5,2,'login','2026-01-03 08:00'),(6,2,'login','2026-01-01 08:00'),
 (7,3,'view','2026-01-01 12:00'),(8,4,NULL,'2026-01-01 13:00'),(9,4,NULL,'2026-01-02 13:00');
"""
SQL_PREVIEW = """
SELECT log_id, user_id, message, created_at, rn FROM (
  SELECT log_id, user_id, message, created_at,
         ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn
  FROM logs)
WHERE rn > 1 ORDER BY log_id
"""
SQL_MAIN = """
DELETE FROM logs WHERE log_id IN (
  SELECT log_id FROM (
    SELECT log_id,
           ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn
    FROM logs)
  WHERE rn > 1)
"""
SQL_CTE = """
WITH ranked AS (
  SELECT log_id,
         ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn
  FROM logs)
DELETE FROM logs WHERE log_id IN (SELECT log_id FROM ranked WHERE rn > 1)
"""
def fresh():
    c = sqlite3.connect(":memory:"); c.executescript(SCHEMA); return c
con = fresh()
before = pd.read_sql_query("SELECT * FROM logs ORDER BY log_id", con)
print("BEFORE:"); print(before.to_string(index=False))
print("\nPreview (rows with rn > 1, to be deleted):"); print(pd.read_sql_query(SQL_PREVIEW, con).to_string(index=False))
t0 = con.total_changes
con.execute(SQL_MAIN)
print("\nrows deleted by subquery form:", con.total_changes - t0)
after = pd.read_sql_query("SELECT * FROM logs ORDER BY log_id", con)
print("AFTER:"); print(after.to_string(index=False))
con2 = fresh(); t0 = con2.total_changes
con2.execute(SQL_CTE)
after_cte = pd.read_sql_query("SELECT * FROM logs ORDER BY log_id", con2)
print("rows deleted by WITH ... DELETE form:", con2.total_changes - t0, "| same table:", after.equals(after_cte))

logs = before.copy()
# pd:main
pd_df = (logs.sort_values(["created_at", "log_id"])
             .drop_duplicates(subset=["user_id", "message"], keep="last")
             .sort_values("log_id"))
# pd:end
print("\npandas drop_duplicates(keep='last') after sorting by created_at, log_id:"); print(pd_df.to_string(index=False))
# compared after sorting by log_id
pd.testing.assert_frame_equal(after.reset_index(drop=True), pd_df.reset_index(drop=True), check_dtype=False)
assert after.equals(after_cte)
assert after["log_id"].tolist() == [3, 4, 5, 7, 9]
# the NULL message pair is treated as one group by PARTITION BY and by drop_duplicates
assert 8 not in after["log_id"].tolist()
# without the log_id tie-break the choice between rows 2 and 3 (identical timestamps) is not defined
print("asserts passed: SQL delete (subquery) == SQL delete (CTE) == pandas drop_duplicates; kept log_ids", after["log_id"].tolist())
```

**Output (my run):**
```text
BEFORE:
 log_id  user_id message       created_at
      1        1   login 2026-01-01 10:00
      2        1   login 2026-01-02 09:00
      3        1   login 2026-01-02 09:00
      4        1  logout 2026-01-01 11:00
      5        2   login 2026-01-03 08:00
      6        2   login 2026-01-01 08:00
      7        3    view 2026-01-01 12:00
      8        4     NaN 2026-01-01 13:00
      9        4     NaN 2026-01-02 13:00

Preview (rows with rn > 1, to be deleted):
 log_id  user_id message       created_at  rn
      1        1   login 2026-01-01 10:00   3
      2        1   login 2026-01-02 09:00   2
      6        2   login 2026-01-01 08:00   2
      8        4     NaN 2026-01-01 13:00   2

rows deleted by subquery form: 4
AFTER:
 log_id  user_id message       created_at
      3        1   login 2026-01-02 09:00
      4        1  logout 2026-01-01 11:00
      5        2   login 2026-01-03 08:00
      7        3    view 2026-01-01 12:00
      9        4     NaN 2026-01-02 13:00
rows deleted by WITH ... DELETE form: 4 | same table: True

pandas drop_duplicates(keep='last') after sorting by created_at, log_id:
 log_id  user_id message       created_at
      3        1   login 2026-01-02 09:00
      4        1  logout 2026-01-01 11:00
      5        2   login 2026-01-03 08:00
      7        3    view 2026-01-01 12:00
      9        4     NaN 2026-01-02 13:00
asserts passed: SQL delete (subquery) == SQL delete (CTE) == pandas drop_duplicates; kept log_ids [3, 4, 5, 7, 9]
```

**Edge cases:**
- Same timestamp: handled only by the extra `log_id DESC` key. State it.
- NULL `message`: `PARTITION BY`, `GROUP BY` and `DISTINCT` treat NULLs as one group; `message = message` would not match them. pandas `drop_duplicates` also treated the two NaN rows as duplicates here (row 8 removed).
- Idempotent: running the delete again deletes 0 rows, since every group is then one row (I did not run a second delete).
- The subquery form and the `WITH ... DELETE` form deleted 4 rows each and left the same table (compared in the Code block); I used `total_changes` to count, since `rowcount` can be unreliable after `WITH` in Python's sqlite3.

**Then explain:**
- **Why SELECT first:** the preview shows exactly which rows will go and how many. A wrong `PARTITION BY` or sort direction deletes real data; run the `SELECT` (or wrap the `DELETE` in a transaction and check the count) before committing.
- **Why a subquery or CTE:** a window function cannot appear in the `WHERE` of the `DELETE` itself, so rank in a subquery or CTE and delete by id. Deleting by `log_id` needs a unique key; if the table has none, use the engine's physical row id.
- **CTE form:** `WITH ranked AS (...) DELETE FROM logs WHERE log_id IN (SELECT ...)` ran on SQLite 3.45. Support elsewhere varies (PostgreSQL allows a CTE before `DELETE`; MySQL 8 supports CTEs before `DELETE` as I remember; not executed here).
- **Other engines (not executed):** PostgreSQL can delete by `ctid` when there is no key, and it requires an alias on a derived table (my SQL has none, which SQLite accepts). MySQL refuses to select from the table being deleted from in a plain subquery (error 1093 as I remember), the usual workaround being the extra derived-table layer, which the query above already has, but I have not run it there.
- **pandas:** `drop_duplicates` returns a new frame; it does not delete in place unless you assign it back.

**Follow-ups:**
- *Keep the earliest instead?* `created_at ASC, log_id ASC` in the window, or `keep="first"` in pandas.
- *What if the table is huge?* Delete in batches, or build a new de-duplicated table and swap it (not executed here; a general practice).
- *Alternatives to `ROW_NUMBER`?* `DELETE ... WHERE log_id NOT IN (SELECT MAX(log_id) ... GROUP BY ...)`, which keeps the highest id rather than the latest timestamp, so it is only equal if ids increase with time.

**Common mistakes:**
- Using `RANK` instead of `ROW_NUMBER`: tied rows both get rank 1 and both survive.
- Ordering by `created_at ASC` and deleting `rn > 1`: that keeps the oldest.
- Running the `DELETE` without a preview.
- In pandas, `drop_duplicates(keep="last")` without sorting first, which keeps the last row by position, not by time.

### Q36 ⭐⭐ 🟡 Top 10 percent of customers by spend using CUME_DIST, PERCENT_RANK or NTILE(10): customers(customer_id, name) and orders(order_id, customer_id, amount). Show the three ways of selecting the top decile on 25 customers, why they return different counts (ties, small n, NTILE rounding), and which one you would choose to say 'at least top 10 percent'. Give the pandas rank(pct=True) >= 0.9 and qcut versions and note pandas pct is rank/n, not (rank-1)/(n-1).
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** On 25 customers the four rules give different answers (`CUME_DIST <= 0.10` returns 2, `NTILE(10) = 1` returns 3, `PERCENT_RANK <= 0.10` returns 4, and `RANK <= ceil(n/10)` returns 4), because CUME_DIST counts the tied peers, NTILE splits ties by position, and PERCENT_RANK uses (rank - 1) / (n - 1); for "at least the top 10 percent, ties included" I use `RANK() <= ceil(n / 10)`; in pandas `rank(pct=True, method="max")` is `CUME_DIST` (rank over n), not `PERCENT_RANK`.

**Schema and sample data:** 25 customers; customer 1 has two orders (3000 + 2000 = 5000), customers 2 to 24 have one order each, customer 25 has none (total 0 through the `LEFT JOIN`). Totals in descending order: 5000, 4800, 4400, 4400, 4000, 3500, 3000, 2800, 2600, 2500, 2400, 2200, 2000, 1800, 1600, 1500, 1400, 1200, 1000, 900, 800, 600, 500, 400, 0. The tie at 4400 (customers 3 and 4) sits right at the cut-off. ```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES
 (1,'C01'),(2,'C02'),(3,'C03'),(4,'C04'),(5,'C05'),(6,'C06'),(7,'C07'),(8,'C08'),(9,'C09'),(10,'C10'),(11,'C11'),(12,'C12'),(13,'C13'),(14,'C14'),(15,'C15'),(16,'C16'),(17,'C17'),(18,'C18'),(19,'C19'),(20,'C20'),(21,'C21'),(22,'C22'),(23,'C23'),(24,'C24'),(25,'C25');
INSERT INTO orders VALUES
 (1,1,3000),(2,1,2000),(3,2,4800),(4,3,4400),(5,4,4400),(6,5,4000),(7,6,3500),(8,7,3000),(9,8,2800),(10,9,2600),(11,10,2500),(12,11,2400),(13,12,2200),(14,13,2000),(15,14,1800),(16,15,1600),(17,16,1500),(18,17,1400),(19,18,1200),(20,19,1000),(21,20,900),(22,21,800),(23,22,600),(24,23,500),(25,24,400);
```

**SQL answer:** `SQL_MAIN` in the Code block aggregates each customer's total (so the ranking is over customers, not order rows), then computes all four measures and the four selection flags. Tie-breaking: `NTILE` orders by `total DESC, customer_id` so the split of the tied customers is reproducible (lower id goes to the better bucket); `CUME_DIST`, `PERCENT_RANK` and `RANK` need no tie-breaker.
```sql
WITH spend AS (
  SELECT c.customer_id, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id),
scored AS (
  SELECT customer_id, total,
         CUME_DIST()    OVER (ORDER BY total DESC)                  AS cd,
         PERCENT_RANK() OVER (ORDER BY total DESC)                  AS pr,
         NTILE(10)      OVER (ORDER BY total DESC, customer_id)     AS nt,
         RANK()         OVER (ORDER BY total DESC)                  AS rk,
         COUNT(*)       OVER ()                                     AS n
  FROM spend)
SELECT customer_id, total, cd, pr, nt, rk,
       cd <= 0.10                 AS in_cume,
       pr <= 0.10                 AS in_prank,
       nt = 1                     AS in_ntile,
       rk <= (n + 9) / 10         AS in_rank
FROM scored
ORDER BY total DESC, customer_id
```

**pandas answer:** inside `# pd:main` in the Code block. Rows are sorted by `total` descending then `customer_id`, which is the same order as the `NTILE` window.
```python
tot = (cust.merge(ords.groupby("customer_id", as_index=False)["amount"].sum(), on="customer_id", how="left")
           .fillna({"amount": 0}).rename(columns={"amount": "total"}))
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
n = len(tot)
tot["cd"] = tot["total"].rank(method="max", ascending=False, pct=True)           # = CUME_DIST
rmin = tot["total"].rank(method="min", ascending=False)
tot["pr"] = (rmin - 1) / (n - 1)                                                  # = PERCENT_RANK
q, r = divmod(n, 10)
pos = np.arange(1, n + 1)                                                         # rows are already in NTILE order
big = r * (q + 1)
tot["nt"] = np.where(pos <= big, np.ceil(pos / (q + 1)), r + np.ceil((pos - big) / q)).astype("int64")
tot["rk"] = rmin.astype("int64")
tot["in_cume"] = tot["cd"] <= 0.10
tot["in_prank"] = tot["pr"] <= 0.10
tot["in_ntile"] = tot["nt"] == 1
tot["in_rank"] = tot["rk"] <= (n + 9) // 10
```

**Example:** n = 25, so 10 percent is 2.5 customers.
- `CUME_DIST` (share of customers with total at or above mine): customer 1 is 1/25 = 0.04, customer 2 is 2/25 = 0.08, customers 3 and 4 are both 4/25 = 0.16 (the tied peers are counted together). `<= 0.10` selects customers 1 and 2: 2 rows, 8 percent, which is less than 10.
- `PERCENT_RANK` = (rank - 1) / 24: customer 1 is 0, customer 2 is 1/24 = 0.0417, customers 3 and 4 have rank 3 so 2/24 = 0.0833, customer 5 has rank 5 so 4/24 = 0.1667. `<= 0.10` selects customers 1 to 4: 4 rows, 16 percent.
- `NTILE(10)`: 25 = 10 x 2 + 5, so the first five buckets hold 3 rows. Bucket 1 is customers 1, 2, 3; customer 4 (same total as 3) is in bucket 2. 3 rows, and the tie is split.
- `RANK <= (25 + 9) / 10 = 3` (integer division, which is ceil(25/10)): customers 1, 2 and the two tied at rank 3: 4 rows (16 percent), ties kept together.
- `qcut(total, 10)` top bin: 2 rows in my run (it cuts on the 90th percentile value, so it is a different rule again).

**Code:** run with `python3 -I`.
```python
# Q36: top 10 percent of customers by spend: CUME_DIST vs PERCENT_RANK vs NTILE(10) vs RANK <= ceil(n/10)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES
 (1,'C01'),(2,'C02'),(3,'C03'),(4,'C04'),(5,'C05'),(6,'C06'),(7,'C07'),(8,'C08'),(9,'C09'),(10,'C10'),(11,'C11'),(12,'C12'),(13,'C13'),(14,'C14'),(15,'C15'),(16,'C16'),(17,'C17'),(18,'C18'),(19,'C19'),(20,'C20'),(21,'C21'),(22,'C22'),(23,'C23'),(24,'C24'),(25,'C25');
INSERT INTO orders VALUES
 (1,1,3000),(2,1,2000),(3,2,4800),(4,3,4400),(5,4,4400),(6,5,4000),(7,6,3500),(8,7,3000),(9,8,2800),(10,9,2600),(11,10,2500),(12,11,2400),(13,12,2200),(14,13,2000),(15,14,1800),(16,15,1600),(17,16,1500),(18,17,1400),(19,18,1200),(20,19,1000),(21,20,900),(22,21,800),(23,22,600),(24,23,500),(25,24,400);
"""
SQL_MAIN = """
WITH spend AS (
  SELECT c.customer_id, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id),
scored AS (
  SELECT customer_id, total,
         CUME_DIST()    OVER (ORDER BY total DESC)                  AS cd,
         PERCENT_RANK() OVER (ORDER BY total DESC)                  AS pr,
         NTILE(10)      OVER (ORDER BY total DESC, customer_id)     AS nt,
         RANK()         OVER (ORDER BY total DESC)                  AS rk,
         COUNT(*)       OVER ()                                     AS n
  FROM spend)
SELECT customer_id, total, cd, pr, nt, rk,
       cd <= 0.10                 AS in_cume,
       pr <= 0.10                 AS in_prank,
       nt = 1                     AS in_ntile,
       rk <= (n + 9) / 10         AS in_rank
FROM scored
ORDER BY total DESC, customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL, top 7 rows:"); print(sql_df.head(7).round(4).to_string(index=False))
flags = ["in_cume", "in_prank", "in_ntile", "in_rank"]
print("\nSQL rows selected per rule (n = %d):" % len(sql_df), {f: int(sql_df[f].sum()) for f in flags})
for f in flags:
    print(f"  {f:9s}", sql_df.loc[sql_df[f] == 1, "customer_id"].tolist())

cust = pd.read_sql_query("SELECT customer_id FROM customers", con)
ords = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
tot = (cust.merge(ords.groupby("customer_id", as_index=False)["amount"].sum(), on="customer_id", how="left")
           .fillna({"amount": 0}).rename(columns={"amount": "total"}))
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
n = len(tot)
tot["cd"] = tot["total"].rank(method="max", ascending=False, pct=True)           # = CUME_DIST
rmin = tot["total"].rank(method="min", ascending=False)
tot["pr"] = (rmin - 1) / (n - 1)                                                  # = PERCENT_RANK
q, r = divmod(n, 10)
pos = np.arange(1, n + 1)                                                         # rows are already in NTILE order
big = r * (q + 1)
tot["nt"] = np.where(pos <= big, np.ceil(pos / (q + 1)), r + np.ceil((pos - big) / q)).astype("int64")
tot["rk"] = rmin.astype("int64")
tot["in_cume"] = tot["cd"] <= 0.10
tot["in_prank"] = tot["pr"] <= 0.10
tot["in_ntile"] = tot["nt"] == 1
tot["in_rank"] = tot["rk"] <= (n + 9) // 10
# pd:end
pct_default = tot["total"].rank(ascending=False, pct=True)                        # default method='average'
qc = pd.qcut(tot["total"], 10, labels=False)
print("\npandas selected per rule:", {f: int(tot[f].sum()) for f in flags},
      "| qcut(total, 10) top bin (label 9):", int((qc == 9).sum()))
print("pandas pct=True default method='average' for ids 3,4 (tied 4400):",
      pct_default[tot.customer_id.isin([3, 4])].round(4).tolist(), "vs method='max':",
      tot.loc[tot.customer_id.isin([3, 4]), "cd"].round(4).tolist())
# compared after sorting both by customer_id
a = sql_df.sort_values("customer_id").reset_index(drop=True)
b = tot.rename(columns={}).sort_values("customer_id").reset_index(drop=True)
for col in ["total", "cd", "pr", "nt", "rk"]:
    pd.testing.assert_series_equal(a[col].astype(float), b[col].astype(float), check_names=False, check_dtype=False)
for col in flags:
    assert a[col].astype(bool).tolist() == b[col].tolist(), col
print("asserts passed: SQL CUME_DIST/PERCENT_RANK/NTILE/RANK columns and flags == pandas versions")
```

**Output (my run):**
```text
SQL, top 7 rows:
 customer_id  total   cd     pr  nt  rk  in_cume  in_prank  in_ntile  in_rank
           1   5000 0.04 0.0000   1   1        1         1         1        1
           2   4800 0.08 0.0417   1   2        1         1         1        1
           3   4400 0.16 0.0833   1   3        0         1         1        1
           4   4400 0.16 0.0833   2   3        0         1         0        1
           5   4000 0.20 0.1667   2   5        0         0         0        0
           6   3500 0.24 0.2083   2   6        0         0         0        0
           7   3000 0.28 0.2500   3   7        0         0         0        0

SQL rows selected per rule (n = 25): {'in_cume': 2, 'in_prank': 4, 'in_ntile': 3, 'in_rank': 4}
  in_cume   [1, 2]
  in_prank  [1, 2, 3, 4]
  in_ntile  [1, 2, 3]
  in_rank   [1, 2, 3, 4]

pandas selected per rule: {'in_cume': 2, 'in_prank': 4, 'in_ntile': 3, 'in_rank': 4} | qcut(total, 10) top bin (label 9): 2
pandas pct=True default method='average' for ids 3,4 (tied 4400): [0.14, 0.14] vs method='max': [0.16, 0.16]
asserts passed: SQL CUME_DIST/PERCENT_RANK/NTILE/RANK columns and flags == pandas versions
```

**Edge cases:**
- Ties at the boundary decide everything: here the tie sits exactly at rank 3 and 4, so `NTILE` returns an unfair 3 rows while `RANK` returns both.
- Small n: with 25 customers a decile is 2.5 customers; `NTILE` rounds by giving the extra rows to early buckets (3), `CUME_DIST <= 0.10` rounds down to 2, and the ceiling rule rounds up to 3 positions (plus ties).
- `CUME_DIST` can never be 0 (the smallest value is 1/n) and `PERCENT_RANK` always starts at 0 and ends at 1.
- Customers with no orders: the `LEFT JOIN` + `COALESCE` keeps them as total 0 and they count in n. Drop them in a `WHERE` first if "customers" means buyers only; every percentage changes.
- `pct=True` default `method="average"` gives the tied pair 0.14, not 0.16 (printed above), so it matches neither `CUME_DIST` nor `PERCENT_RANK`.

**Then explain:**
- **Definitions:** `CUME_DIST` = rows with value at or before this one in the window order / n. `PERCENT_RANK` = (rank - 1) / (n - 1). `NTILE(k)` = positional bucket.
- **pandas:** `rank(method="max", ascending=False, pct=True)` is `CUME_DIST` (asserted equal); `(rank(method="min") - 1) / (n - 1)` is `PERCENT_RANK` (asserted); `pct=True` alone is rank over n, never (rank - 1) / (n - 1).
- **Which to choose:** "at least top 10 percent" means do not under-cover and do not split equals: `RANK() <= ceil(n * 0.10)`. "At most 10 percent" is `CUME_DIST <= 0.10`.
- **Aggregate first:** compute one total per customer before ranking; ranking order rows would rank orders, not customers.
- **Dialects:** `CUME_DIST`, `PERCENT_RANK` and `NTILE` exist in PostgreSQL, MySQL 8, BigQuery and Snowflake as I remember (not executed here).

**Follow-ups:**
- *How do you get "top 5 percent per region"?* Add `PARTITION BY region` to each window and use the same logic per partition.
- *Do you need a minimum bucket size?* With tiny groups (n = 5) a decile is half a customer; say what you do (return at least one).
- *Is `NTILE(10) = 1` the same as the 90th-percentile cut?* No; it is positional, and it splits ties.

**Common mistakes:**
- Ranking order lines instead of customer totals.
- Using `PERCENT_RANK <= 0.1` and calling it "10 percent of rows".
- Using `NTILE` for a cut-off when ties matter.
- In pandas, using `rank(pct=True)` and assuming it is `PERCENT_RANK`.

### Q37 ⭐⭐ 🟡 Outer ORDER BY versus ORDER BY inside OVER: employees(emp_id, name, dept_id, salary). Explain that ORDER BY in OVER controls the numbering and does not order the output rows, so a query with ROW_NUMBER() OVER (ORDER BY salary DESC) and no outer ORDER BY may print rows in any order, and that a tied ORDER BY inside OVER can number tied rows differently between runs. Show a corrected query with both, and the pandas parallel (rank does not reorder rows; sort_values does).
**Asked at:** techinterview.org window-function gotchas article (ties, RANK = 2 returning nothing, window in WHERE, default frame), a guide and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** The `ORDER BY` inside `OVER (...)` only decides how the window numbers or ranks rows; it does not promise any order of the output rows, and if it has ties the numbering of tied rows is not defined either, so write a unique tie-break inside `OVER` and a separate outer `ORDER BY`; in pandas `rank` leaves the row order alone and `sort_values` is what reorders.

**Schema and sample data:** six employees; Ben and Chitra tie at 90, Asha and Esha tie at 70.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,90),(3,'Chitra',20,90),
                             (4,'Dev',20,50),(5,'Esha',10,70),(6,'Farid',20,60);
```

**SQL answer:** the corrected query is `SQL_MAIN` in the Code block: the unique key `emp_id` ends the window `ORDER BY` (so the two 90s always number the same way: lowest `emp_id` first), and the outer `ORDER BY rn` fixes the output order. The naive forms `SQL_NAIVE` and `SQL_NAIVE_TWO` are run next to it.
```sql
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn
FROM employees
ORDER BY rn
```

**pandas answer:** inside `# pd:main` in the Code block. `rank(method="first")` assigns positions by salary with ties in row order and does not move any row; `sort_values("rn")` is the step that reorders.
```python
ranked = emp.assign(rn=emp["salary"].rank(method="first", ascending=False).astype("int64"))
pd_df = ranked.sort_values("rn")
```

**Example:**
- Naive query `ROW_NUMBER() OVER (ORDER BY salary DESC)` with no outer `ORDER BY`: on SQLite 3.45.1 the rows happened to come back in window order (Ben 1, Chitra 2, Asha 3, Esha 4, Farid 5, Dev 6). That is what the implementation did, not a promise.
- Same table, same `rn` expression, plus a second window `ROW_NUMBER() OVER (ORDER BY name DESC)` in the select list: the rows came back in a different tie order and the tied employees swapped numbers (Chitra 1, Ben 2; Esha 3, Asha 4). The numbering of tied rows changed because an unrelated expression was added.
- Fixed query: `ORDER BY salary DESC, emp_id` inside the window and `ORDER BY rn` outside gives Ben 1, Chitra 2, Asha 3, Esha 4, Farid 5, Dev 6, and it stayed identical when I added the second window.
- pandas: `rank` on the frame in `emp_id` order returns the same six rows in `emp_id` order (1 to 6); `sort_values("rn")` returns them as 2, 3, 1, 5, 6, 4.

**Code:** run with `python3 -I`.
```python
# Q37: ORDER BY inside OVER versus the outer ORDER BY
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,90),(3,'Chitra',20,90),
                             (4,'Dev',20,50),(5,'Esha',10,70),(6,'Farid',20,60);
"""
SQL_NAIVE = """
SELECT emp_id, name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
FROM employees
"""
SQL_NAIVE_TWO = """
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
       ROW_NUMBER() OVER (ORDER BY name DESC)   AS rn_name
FROM employees
"""
SQL_MAIN = """
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn
FROM employees
ORDER BY rn
"""
SQL_FIXED_TWO = """
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn,
       ROW_NUMBER() OVER (ORDER BY name DESC)           AS rn_name
FROM employees
ORDER BY rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
naive, naive_two, sql_df, fixed_two = q(SQL_NAIVE), q(SQL_NAIVE_TWO), q(SQL_MAIN), q(SQL_FIXED_TWO)
print("NAIVE (no outer ORDER BY, no tie-break), rows in the order returned:"); print(naive.to_string(index=False))
print("\nNAIVE with a second window added (same table, same rn expression):"); print(naive_two.to_string(index=False))
tied = lambda d: dict(zip(d["name"], d["rn"]))
print("\nrn of the tied 90s: first query", {k: tied(naive)[k] for k in ("Ben", "Chitra")},
      "| second query", {k: tied(naive_two)[k] for k in ("Ben", "Chitra")},
      "| numbering identical across queries:", tied(naive) == tied(naive_two))
print("\nFIXED (tie-break in OVER, ORDER BY rn outside):"); print(sql_df.to_string(index=False))
print("\nFIXED with the second window added; rn unchanged:", dict(zip(fixed_two["name"], fixed_two["rn"])) == dict(zip(sql_df["name"], sql_df["rn"])))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
ranked = emp.assign(rn=emp["salary"].rank(method="first", ascending=False).astype("int64"))
pd_df = ranked.sort_values("rn")
# pd:end
print("\npandas rank() keeps the row order (emp_id order):", ranked["emp_id"].tolist())
print("pandas sort_values('rn') returns the rows in ranked order:", pd_df["emp_id"].tolist())
assert ranked["emp_id"].tolist() == emp["emp_id"].tolist()
# compared in rn order (both sorted by rn)
cols = ["emp_id", "name", "salary", "rn"]
pd.testing.assert_frame_equal(sql_df[cols].reset_index(drop=True), pd_df[cols].reset_index(drop=True), check_dtype=False)
assert fixed_two["rn"].tolist() == sql_df["rn"].tolist()
print("asserts passed: SQL (tie-break + outer ORDER BY) == pandas rank(method='first') + sort_values")
```

**Output (my run):**
```text
NAIVE (no outer ORDER BY, no tie-break), rows in the order returned:
 emp_id   name  salary  rn
      2    Ben      90   1
      3 Chitra      90   2
      1   Asha      70   3
      5   Esha      70   4
      6  Farid      60   5
      4    Dev      50   6

NAIVE with a second window added (same table, same rn expression):
 emp_id   name  salary  rn  rn_name
      3 Chitra      90   1        4
      2    Ben      90   2        5
      5   Esha      70   3        2
      1   Asha      70   4        6
      6  Farid      60   5        1
      4    Dev      50   6        3

rn of the tied 90s: first query {'Ben': 1, 'Chitra': 2} | second query {'Ben': 2, 'Chitra': 1} | numbering identical across queries: False

FIXED (tie-break in OVER, ORDER BY rn outside):
 emp_id   name  salary  rn
      2    Ben      90   1
      3 Chitra      90   2
      1   Asha      70   3
      5   Esha      70   4
      6  Farid      60   5
      4    Dev      50   6

FIXED with the second window added; rn unchanged: True

pandas rank() keeps the row order (emp_id order): [1, 2, 3, 4, 5, 6]
pandas sort_values('rn') returns the rows in ranked order: [2, 3, 1, 5, 6, 4]
asserts passed: SQL (tie-break + outer ORDER BY) == pandas rank(method='first') + sort_values
```

**Edge cases:**
- Ties inside `OVER`: both tied rows satisfy the order, so either can be number 1. In my run the engine's choice changed between two queries on the same data and the same table; I did not test repeated runs of one query on an unchanged database, so I do not claim it changes "each run" on SQLite. Other engines, parallel plans and changed indexes can reorder (not executed).
- Output order without an outer `ORDER BY`: SQL does not define it. The `ORDER BY` inside `OVER` can influence it in practice, as the first query shows, but that is an implementation side effect.
- Several windows with different `ORDER BY` keys in one query: the output can follow only one of them (in my second query it followed the salary window, not the name window).
- Keep the outer `ORDER BY rn` even if the output looked sorted without it; I did not time its cost.

**Then explain:**
- **Two jobs, two clauses:** the window `ORDER BY` defines position within a partition; the outer `ORDER BY` defines presentation.
- **Determinism rule:** every ranking used for a decision (top 1, dedup, pagination) needs a unique last key.
- **In pandas:** `rank()` returns a Series aligned to the original index, so row order is unchanged; `sort_values` is the explicit reorder. `rank(method="first")` breaks ties by current row order, which equals `emp_id` order here only because the frame was read `ORDER BY emp_id`.
- **Other engines:** PostgreSQL's tutorial says tied rows are numbered in an unspecified order (as read from the page I opened); I have not run PostgreSQL or MySQL here.

**Follow-ups:**
- *How do you order the output by the rank and then by name?* `ORDER BY rn, name` outside.
- *Does `ORDER BY` inside a subquery or view guarantee the outer order?* No; only the outermost `ORDER BY` does (general SQL rule).
- *What about `LIMIT` with a window function?* Add the outer `ORDER BY` first; `LIMIT` without it returns arbitrary rows.

**Common mistakes:**
- Assuming the output is sorted because the window had an `ORDER BY`.
- A window `ORDER BY` without a unique tie-break key in a decision query.
- In pandas, calling `rank()` and expecting the frame to be sorted.
- Treating the one run that looked sorted as proof.

### Q38 ⭐⭐ 🔴 Median per group using ROW_NUMBER and COUNT (PERCENTILE_CONT is not in SQLite): employees(emp_id, name, dept_id, salary) with even and odd group sizes. Compute the median salary per department with ROW_NUMBER() and COUNT(*) OVER (PARTITION BY dept_id), keeping the middle one or two rows and averaging them. State NULL salaries are filtered first, show PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as PostgreSQL/Snowflake dialect text (hedged, not executed), and confirm against pandas groupby median.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Drop NULL salaries first, number each department's salaries in order with `ROW_NUMBER()`, count them with `COUNT(*) OVER (PARTITION BY dept_id)`, keep the rows at positions `(cnt + 1) / 2` and `(cnt + 2) / 2` (one middle row for an odd count, two for an even count) and average them; pandas does it with `groupby("salary").median()`.

**Schema and sample data:** five departments: 10 has four real salaries and one NULL (even count), 20 has three (odd, with a tie), 30 has one, 40 is all NULL, 50 has four with a tie in the middle.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,50),(2,'Ben',10,60),(3,'Chitra',10,70),(4,'Dev',10,80),(5,'Esha',10,NULL),
 (6,'Farid',20,40),(7,'Gita',20,40),(8,'Hari',20,100),
 (9,'Ila',30,55),
 (10,'Jay',40,NULL),(11,'Kiran',40,NULL),
 (12,'Lata',50,10),(13,'Manu',50,20),(14,'Nina',50,20),(15,'Om',50,30);
```

**SQL answer:** `SQL_MAIN` in the Code block (`SQL_WRONG` is the same query without the NULL filter, run for contrast). Tie-breaking: the window orders by `salary, emp_id`; the median value does not depend on which tied row is numbered first, because tied rows have equal salaries, but the `emp_id` key keeps the numbering reproducible.
```sql
WITH ranked AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id)                         AS cnt
  FROM employees
  WHERE salary IS NOT NULL)
SELECT dept_id, AVG(salary) AS median_salary
FROM ranked
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
GROUP BY dept_id
ORDER BY dept_id
```

**pandas answer:** inside `# pd:main` in the Code block. `median` skips NaN; a group with no values gives NaN, so I drop those rows to match SQL, which has no row for department 40.
```python
med = emp.groupby("dept_id")["salary"].median()
pd_df = med.dropna().rename("median_salary").reset_index()
```

**Example:**
- Department 10, salaries 50, 60, 70, 80 (Esha's NULL removed): cnt = 4, positions (4 + 1) / 2 = 2 and (4 + 2) / 2 = 3 (integer division), the values 60 and 70, average 65.0.
- Department 20, salaries 40, 40, 100: cnt = 3, positions 2 and 2, so the one row at position 2 (a 40); `AVG` of one value is 40.0.
- Department 30: cnt = 1, positions 1 and 1, median 55.0.
- Department 50, salaries 10, 20, 20, 30: positions 2 and 3, both 20, median 20.0.
- Department 40: all NULL, filtered out, so there is no row (pandas shows NaN).
- Without the NULL filter (`SQL_WRONG`): department 10 has five rows with the NULL sorted first, so the middle row is position 3, the value 60 instead of 65; department 40 now returns a row with a NULL median.

**Code:** run with `python3 -I`.
```python
# Q38: median per group with ROW_NUMBER and COUNT (no PERCENTILE_CONT in SQLite)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,50),(2,'Ben',10,60),(3,'Chitra',10,70),(4,'Dev',10,80),(5,'Esha',10,NULL),
 (6,'Farid',20,40),(7,'Gita',20,40),(8,'Hari',20,100),
 (9,'Ila',30,55),
 (10,'Jay',40,NULL),(11,'Kiran',40,NULL),
 (12,'Lata',50,10),(13,'Manu',50,20),(14,'Nina',50,20),(15,'Om',50,30);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id)                         AS cnt
  FROM employees
  WHERE salary IS NOT NULL)
SELECT dept_id, AVG(salary) AS median_salary
FROM ranked
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
GROUP BY dept_id
ORDER BY dept_id
"""
SQL_WRONG = SQL_MAIN.replace("  WHERE salary IS NOT NULL)", "  )")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL median per department (NULL salaries filtered first):"); print(sql_df.to_string(index=False))
wrong = pd.read_sql_query(SQL_WRONG, con)
print("\nWRONG (NULL filter removed; NULLs sort first and count in cnt):"); print(wrong.to_string(index=False))
assert wrong["median_salary"].tolist()[0] == 60.0 and wrong["median_salary"].isna().any()
print("\nmiddle positions used, for each count:", {c: sorted({(c + 1) // 2, (c + 2) // 2}) for c in (1, 2, 3, 4)})

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
med = emp.groupby("dept_id")["salary"].median()
pd_df = med.dropna().rename("median_salary").reset_index()
# pd:end
print("\npandas groupby median (all-NaN dept 40 shows NaN):", med.to_dict())
print("pandas quantile(0.5) default interpolation:", emp.groupby("dept_id")["salary"].quantile(0.5).to_dict())
print("quantile lower :", emp.groupby("dept_id")["salary"].quantile(0.5, interpolation="lower").dropna().to_dict())
print("quantile higher:", emp.groupby("dept_id")["salary"].quantile(0.5, interpolation="higher").dropna().to_dict())
# compared after sorting by dept_id; dept 40 (all NULL) has no SQL row, so NaN rows are dropped from pandas
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("dept_id").reset_index(drop=True), check_dtype=False)
assert med.isna().tolist() == [False, False, False, True, False]
assert sql_df["median_salary"].tolist() == [65.0, 40.0, 55.0, 20.0]
print("asserts passed: SQL ROW_NUMBER/COUNT median == pandas groupby median (dept 40 absent in SQL, NaN in pandas)")
```

**Output (my run):**
```text
SQL median per department (NULL salaries filtered first):
 dept_id  median_salary
      10           65.0
      20           40.0
      30           55.0
      50           20.0

WRONG (NULL filter removed; NULLs sort first and count in cnt):
 dept_id  median_salary
      10           60.0
      20           40.0
      30           55.0
      40            NaN
      50           20.0

middle positions used, for each count: {1: [1], 2: [1, 2], 3: [2], 4: [2, 3]}

pandas groupby median (all-NaN dept 40 shows NaN): {10: 65.0, 20: 40.0, 30: 55.0, 40: nan, 50: 20.0}
pandas quantile(0.5) default interpolation: {10: 65.0, 20: 40.0, 30: 55.0, 40: nan, 50: 20.0}
quantile lower : {10: 60.0, 20: 40.0, 30: 55.0, 50: 20.0}
quantile higher: {10: 70.0, 20: 40.0, 30: 55.0, 50: 20.0}
asserts passed: SQL ROW_NUMBER/COUNT median == pandas groupby median (dept 40 absent in SQL, NaN in pandas)
```

**Edge cases:**
- NULL salaries: filter first, as the question states; counting them shifts the middle position and the NULLs sort first in SQLite (Q29), as `SQL_WRONG` shows.
- All-NULL group: SQL returns no row, pandas `median` returns NaN. Decide which you want and say so.
- Even count with a tie in the middle (department 50): the two middle rows are equal, so the median equals that value.
- Integer arithmetic: `(cnt + 1) / 2` is integer division in SQLite because both operands are integers. In MySQL `/` returns a decimal and would need `DIV` (from memory, not executed); PostgreSQL integer division also truncates (not executed).
- `AVG` of integers gives a float in SQLite (65.0); the median of an even count can be a half value.

**Then explain:**
- **Why two positions:** an odd count has one middle, an even count has two; `(cnt + 1) / 2` and `(cnt + 2) / 2` are the same number when `cnt` is odd and consecutive numbers when it is even, so `rn IN (...)` and `AVG` handle both.
- **PERCENTILE_CONT (not executed here):** PostgreSQL and Snowflake offer `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)` as an ordered-set aggregate (written from memory; SQLite has no such function and I did not run it). Availability and syntax differ across other engines (not executed here), so check your engine's documentation; MySQL has no such function as far as I remember.
- **Interpolation in pandas:** `quantile(0.5)` with the default linear interpolation equals the median (matched here); `interpolation="lower"` gave 60 and `"higher"` gave 70 for department 10, so they are not a median for an even count.
- **Confirmation:** the SQL median equals pandas `groupby().median()` for all four departments that have values.

**Follow-ups:**
- *Other percentiles?* Position `ceil(p * cnt)` for a discrete percentile (`PERCENTILE_DISC` idea); a continuous one needs interpolation between two ranked rows.
- *Is there a version without `COUNT`?* Yes: compare ascending and descending `ROW_NUMBER` and keep rows where they differ by at most 1; same result, two sorts.
- *Median of a whole table?* Remove the `PARTITION BY`.

**Common mistakes:**
- Not filtering NULLs before numbering and counting.
- Using `AVG` of the middle positions with `cnt / 2` and `cnt / 2 + 1`, which is wrong for odd counts.
- Calling the average of the group the median.
- Assuming `PERCENTILE_CONT` exists in every engine.

### Q39 ⭐ 🟡 Top N overall versus top N per group, and pagination with ROW_NUMBER: products(product_id, category, name, price). Show ORDER BY price DESC LIMIT 5 (overall), the per-group top 5 with ROW_NUMBER, and page 2 of a list (rows 11 to 20) with ROW_NUMBER BETWEEN versus LIMIT 10 OFFSET 10. Explain why OFFSET pagination gets slower on deep pages and is unstable if ties or inserts exist (a unique tie-breaker is needed), and give the pandas nlargest, head and iloc versions.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `ORDER BY price DESC LIMIT 5` gives the top 5 rows overall, `ROW_NUMBER() OVER (PARTITION BY category ...)` gives the top N inside each group, and a page is just a slice of a fully ordered list, so the order needs a unique tie-breaker or pages can overlap or skip rows.

**Schema and sample data:** 14 products in three categories. Two Books at price 40 (ids 1 and 3), two Toys at 30 (5 and 7), two Tech at 20 (9 and 12), two at 90 (6 and 11), so ties are on purpose. The question says top 5 per group and pages of 10; the table is tiny, so I use top 2 per category and pages of 5 (page 2 is rows 6 to 10). The logic is identical.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Books','Atlas',40),(2,'Books','Brief',25),(3,'Books','Cipher',40),(4,'Books','Digest',10),
 (5,'Toys','Kite',30),(6,'Toys','Lego',90),(7,'Toys','Mask',30),(8,'Toys','Net',15),
 (9,'Tech','Cable',20),(10,'Tech','Dock',60),(11,'Tech','Earbuds',90),(12,'Tech','Fan',20),
 (13,'Tech','Gimbal',150),(14,'Books','Epic',55);
```

**SQL answer:** all five queries are in the Code block. Overall top 5 (`SQL_TOP`), per-category top 2 (`SQL_PER_GROUP`), page 2 by row number (`SQL_PAGE_RN`), page 2 by offset (`SQL_PAGE_OFFSET`) and a keyset version (`SQL_KEYSET`).
```sql
SELECT product_id, category, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5
```
```sql
WITH r AS (
  SELECT product_id, category, name, price,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT category, rn, product_id, name, price
FROM r
WHERE rn <= 2
ORDER BY category, rn
```
```sql
WITH r AS (
  SELECT product_id, name, price,
         ROW_NUMBER() OVER (ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT rn, product_id, name, price
FROM r
WHERE rn BETWEEN 6 AND 10
ORDER BY rn
```
```sql
SELECT product_id, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5 OFFSET 5
```
```sql
SELECT product_id, name, price
FROM products
WHERE price < ? OR (price = ? AND product_id > ?)
ORDER BY price DESC, product_id
LIMIT 5
```

**pandas answer:** sort once by price descending then product_id, then `head`, `groupby().head` and `iloc` are all slices of the same ordered frame. `nlargest` is the one-liner for the overall case.
```python
ordered = prod.sort_values(["price", "product_id"], ascending=[False, True])
pd_top = ordered.head(5)
pd_nlargest = prod.nlargest(5, "price")          # keep='first': ties resolved by row order
pd_group = ordered.groupby("category").head(2)
pd_page2 = ordered.iloc[5:10]
```

**Example:** sorted by price DESC, product_id ASC the whole list is: 13 (150), 6 (90), 11 (90), 10 (60), 14 (55), 1 (40), 3 (40), 5 (30), 7 (30), 2 (25), then 9 (20), 12 (20), 8 (15), 4 (10).
- Overall top 5 is the first five: 13, 6, 11, 10, 14 (6 beats 11 at the 90 tie because its id is lower).
- Per category top 2: Books 14 (55) and 1 (40, because id 1 beats id 3 on the 40 tie); Tech 13 and 11; Toys 6 and 5 (30 tie broken by id).
- Page 2 (rows 6 to 10): 1, 3, 5, 7, 2. `ROW_NUMBER BETWEEN 6 AND 10` and `LIMIT 5 OFFSET 5` return the same rows.

**Code:** run with `python3 -I`.
```python
# Q39: top N overall, top N per group, pagination
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Books','Atlas',40),(2,'Books','Brief',25),(3,'Books','Cipher',40),(4,'Books','Digest',10),
 (5,'Toys','Kite',30),(6,'Toys','Lego',90),(7,'Toys','Mask',30),(8,'Toys','Net',15),
 (9,'Tech','Cable',20),(10,'Tech','Dock',60),(11,'Tech','Earbuds',90),(12,'Tech','Fan',20),
 (13,'Tech','Gimbal',150),(14,'Books','Epic',55);
"""
SQL_TOP = """
SELECT product_id, category, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5
"""
SQL_PER_GROUP = """
WITH r AS (
  SELECT product_id, category, name, price,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT category, rn, product_id, name, price
FROM r
WHERE rn <= 2
ORDER BY category, rn
"""
SQL_PAGE_RN = """
WITH r AS (
  SELECT product_id, name, price,
         ROW_NUMBER() OVER (ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT rn, product_id, name, price
FROM r
WHERE rn BETWEEN 6 AND 10
ORDER BY rn
"""
SQL_PAGE_OFFSET = """
SELECT product_id, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5 OFFSET 5
"""
SQL_KEYSET = """
SELECT product_id, name, price
FROM products
WHERE price < ? OR (price = ? AND product_id > ?)
ORDER BY price DESC, product_id
LIMIT 5
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s, p=(): pd.read_sql_query(s, con, params=p)

top = q(SQL_TOP)
per_group = q(SQL_PER_GROUP)
page_rn = q(SQL_PAGE_RN)
page_off = q(SQL_PAGE_OFFSET)
print("overall top 5:"); print(top.to_string(index=False))
print("\nper-category top 2:"); print(per_group.to_string(index=False))
print("\npage 2 via ROW_NUMBER BETWEEN 6 AND 10:"); print(page_rn.to_string(index=False))
assert page_rn[["product_id", "name", "price"]].equals(page_off)
print("page 2 via LIMIT 5 OFFSET 5 is identical: True")

# pandas
prod = q("SELECT * FROM products")
# pd:main
ordered = prod.sort_values(["price", "product_id"], ascending=[False, True])
pd_top = ordered.head(5)
pd_nlargest = prod.nlargest(5, "price")          # keep='first': ties resolved by row order
pd_group = ordered.groupby("category").head(2)
pd_page2 = ordered.iloc[5:10]
# pd:end
pd.testing.assert_frame_equal(top, pd_top.reset_index(drop=True))
assert pd_nlargest["product_id"].tolist() == top["product_id"].tolist()   # equal here only because rows are stored in product_id order
g = pd_group.sort_values(["category", "price", "product_id"], ascending=[True, False, True]).reset_index(drop=True)
assert per_group[["category", "product_id", "price"]].equals(g[["category", "product_id", "price"]])
pd.testing.assert_frame_equal(page_off, pd_page2[["product_id", "name", "price"]].reset_index(drop=True))
print("\npandas: head(5), nlargest(5), groupby.head(2), iloc[5:10] all match the SQL rows")

# instability: ties and inserts. Unstable page = ORDER BY price DESC only, no tie-breaker.
print("\nrows 6 and 7 tie at price 40 (products 1 and 3). With page size 6 the page boundary splits them.")
print("ORDER BY price DESC only, rows 6-7:", con.execute("SELECT product_id, price FROM products ORDER BY price DESC LIMIT 2 OFFSET 5").fetchall(),
      "<- product 1 first on this run; without a tie-breaker nothing guarantees it stays that way")
print("ORDER BY price DESC, product_id, rows 6-7:", con.execute("SELECT product_id, price FROM products ORDER BY price DESC, product_id LIMIT 2 OFFSET 5").fetchall())

# insert between page fetches: OFFSET repeats a row, keyset does not
page1 = q(SQL_TOP)
con.execute("INSERT INTO products VALUES (15,'Tech','Hub',200)")        # a new top-priced row arrives after page 1 was shown
page2_offset = q(SQL_PAGE_OFFSET)
last = page1.iloc[-1]
# keyset on the same order (price DESC, product_id ASC): next rows are price < last.price OR (price = last.price AND product_id > last.product_id)
page2_keyset = q(SQL_KEYSET, (int(last["price"]), int(last["price"]), int(last["product_id"])))
print("\nafter inserting Hub (200) once page 1 was shown:")
print("page 1 shown earlier :", page1["product_id"].tolist())
print("page 2 by OFFSET     :", page2_offset["product_id"].tolist(), "<- repeats product", sorted(set(page1["product_id"]) & set(page2_offset["product_id"])))
print("page 2 by keyset     :", page2_keyset["product_id"].tolist())
assert set(page1["product_id"]) & set(page2_offset["product_id"])
assert not (set(page1["product_id"]) & set(page2_keyset["product_id"]))
print("asserts passed")
```

**Output (my run):**
```text
overall top 5:
 product_id category    name  price
         13     Tech  Gimbal    150
          6     Toys    Lego     90
         11     Tech Earbuds     90
         10     Tech    Dock     60
         14    Books    Epic     55

per-category top 2:
category  rn  product_id    name  price
   Books   1          14    Epic     55
   Books   2           1   Atlas     40
    Tech   1          13  Gimbal    150
    Tech   2          11 Earbuds     90
    Toys   1           6    Lego     90
    Toys   2           5    Kite     30

page 2 via ROW_NUMBER BETWEEN 6 AND 10:
 rn  product_id   name  price
  6           1  Atlas     40
  7           3 Cipher     40
  8           5   Kite     30
  9           7   Mask     30
 10           2  Brief     25
page 2 via LIMIT 5 OFFSET 5 is identical: True

pandas: head(5), nlargest(5), groupby.head(2), iloc[5:10] all match the SQL rows

rows 6 and 7 tie at price 40 (products 1 and 3). With page size 6 the page boundary splits them.
ORDER BY price DESC only, rows 6-7: [(1, 40), (3, 40)] <- product 1 first on this run; without a tie-breaker nothing guarantees it stays that way
ORDER BY price DESC, product_id, rows 6-7: [(1, 40), (3, 40)]

after inserting Hub (200) once page 1 was shown:
page 1 shown earlier : [13, 6, 11, 10, 14]
page 2 by OFFSET     : [14, 1, 3, 5, 7] <- repeats product [14]
page 2 by keyset     : [1, 3, 5, 7, 2]
asserts passed
```

**Edge cases:**
- Ties: Atlas and Cipher both cost 40. Without `product_id` in the ORDER BY the engine may put either first, so which one is on which page can change. I printed rows 6 and 7 without the tie-breaker; they came out in id order on this tiny table, but nothing guarantees that.
- A category with fewer than N products simply returns fewer rows (ROW_NUMBER never invents rows).
- Insert between pages: after page 1 was shown I inserted a new top-priced product (id 15). `OFFSET 5` then returned product 14 again, which was already on page 1 (see output). The keyset query did not repeat it.
- `nlargest(5, 'price')` resolves ties by row order (keep='first'). It matched here only because the frame is stored in product_id order, so I assert against the explicit sort.
- Deleting a row between pages has the opposite effect: a row is skipped.

**Then explain:**
- **Overall versus per group:** `LIMIT` cuts the whole result once; per-group needs a window with `PARTITION BY category` and a filter on the row number, in a CTE because a window cannot sit in WHERE.
- **ROW_NUMBER BETWEEN versus LIMIT/OFFSET:** same rows. LIMIT/OFFSET is shorter; the row-number form is useful when the page filter must live inside a bigger query or when you also want the number printed.
- **Why deep pages are slow:** to return rows 1,000,001 to 1,000,010 the engine still has to produce and throw away the first million in order. I did not time this on SQLite here; it is the standard explanation (an index on the sort key helps the sort, but the skip is still a walk). Not executed on other engines.
- **Why unstable:** OFFSET counts positions, not rows. Inserts or deletes shift positions between requests, and tied rows can move.
- **Keyset (seek) pagination:** remember the last (price, product_id) you showed and ask for rows after it. The cost does not grow with the page number and inserted rows do not shift pages. Trade-off: you cannot jump to page 40 directly. Row-value comparisons such as `(price, product_id) < (?, ?)` exist in some engines (not run here); I wrote the expanded `OR` form, which runs on SQLite and handles the mixed directions (price DESC, product_id ASC).

**Follow-ups:**
- *How would you do this for a million-row table in a web app?* Keyset pagination on an indexed unique sort key.
- *Why include product_id in ORDER BY if price is almost unique?* Almost is not unique; one tie is enough to cause duplicates or gaps between pages.
- *`LIMIT 5` per group in one statement?* Not in standard SQL without a window (or LATERAL in engines that have it; not executed here).

**Common mistakes:**
- `LIMIT 2` on a grouped query and expecting two per group.
- OFFSET pagination on a non-unique ORDER BY.
- Putting `ROW_NUMBER() BETWEEN ...` in WHERE instead of using a CTE.
- Off-by-one: page p of size s is rows `(p-1)*s + 1` to `p*s`, and `OFFSET (p-1)*s`.

### Q40 ⭐ 🟡 Window function performance concept: employees(emp_id, name, dept_id, salary) with a million rows in a real system. Explain that a ranking window needs the rows sorted by partition and order keys, so the cost is a sort (or an index scan that delivers that order), that several windows with the same PARTITION BY/ORDER BY can share one sort, that different windows force different sorts (use a named window to see the reuse), and how an index on (dept_id, salary) may help. Run EXPLAIN QUERY PLAN on a SQLite example and hedge other engines; deeper tuning is Part 11.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** A ranking window has to see each partition's rows in the ORDER BY order, so its cost is a sort (or an index scan that already delivers that order); windows with the same PARTITION BY/ORDER BY can share one sort, different windows each pay for their own, and an index on (dept_id, salary) can remove the sort.

**Schema and sample data:** the question says a million rows; I cannot run that sensibly here, so the Code block builds 3000 employees in 30 departments with many salary ties and looks at the query plan text, which does not depend on the row count. No timings are printed, because they would vary by machine and say little at this size.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
-- 3000 rows: dept_id = i % 30, salary = 3000 + (i * 37) % 500 (loop in the Code block)
```

**SQL answer:** three queries, run through `EXPLAIN QUERY PLAN` before and after an index. `SQL_ONE` is one window, `SQL_SAME` uses a named window for ROW_NUMBER and RANK plus a SUM with only PARTITION BY, `SQL_DIFF` has two different windows.
```sql
SELECT emp_id, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
FROM employees
```
```sql
SELECT emp_id,
       ROW_NUMBER() OVER w AS rn,
       RANK()       OVER w AS rk,
       SUM(salary)  OVER (PARTITION BY dept_id) AS dept_total
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC, emp_id)
```
```sql
SELECT emp_id,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       ROW_NUMBER() OVER (ORDER BY salary, emp_id) AS overall_rn
FROM employees
```

**pandas answer:** pandas has no planner; the same work is an explicit sort plus `cumcount`. It is here to check the ranking, not to compare cost.
```python
ordered = emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
ordered["rn"] = ordered.groupby("dept_id").cumcount() + 1
pd_res = ordered.sort_values("emp_id").reset_index(drop=True)[["emp_id", "dept_id", "salary", "rn"]]
```

**Example:** how to read the plan lines in the output below (SQLite 3.45.1 wording).
- Query 1, no index: `SCAN employees`, then `USE TEMP B-TREE FOR ORDER BY`. The temp b-tree is the sort by (dept_id, salary DESC, emp_id). One window, one sort.
- Query 2: ROW_NUMBER and RANK share the named window, and SUM uses `PARTITION BY dept_id` only. The plan has two temp b-trees, so SQLite did not reuse the first sort for the SUM window even though its partitioning is a prefix of the other. I would not assume other engines behave the same (not executed).
- Query 3: two different windows, two temp b-trees.
- Query 4: after `CREATE INDEX ix_dept_salary ON employees(dept_id, salary DESC, emp_id)` the plan is `SCAN employees USING COVERING INDEX ix_dept_salary` and the temp b-tree disappears: the index delivers rows already in window order.
- Query 5 (two different windows with the index): still two temp b-trees. The index matches one window's order at best, and the plan text does not say which window each sort belongs to, so I do not claim more than "the index did not remove both sorts".

**Code:** run with `python3 -I`.
```python
# Q40: window function cost = a sort; EXPLAIN QUERY PLAN on SQLite 3.45
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);")
# deterministic toy data: 3000 employees, 30 departments, salaries with many ties
rows = [(i, f"e{i}", i % 30, 3000 + (i * 37) % 500) for i in range(1, 3001)]
con.executemany("INSERT INTO employees VALUES (?,?,?,?)", rows)
print("sqlite", sqlite3.sqlite_version, "| rows:", con.execute("SELECT COUNT(*) FROM employees").fetchone()[0])

SQL_ONE = """
SELECT emp_id, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
FROM employees
"""
SQL_SAME = """
SELECT emp_id,
       ROW_NUMBER() OVER w AS rn,
       RANK()       OVER w AS rk,
       SUM(salary)  OVER (PARTITION BY dept_id) AS dept_total
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC, emp_id)
"""
SQL_DIFF = """
SELECT emp_id,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       ROW_NUMBER() OVER (ORDER BY salary, emp_id) AS overall_rn
FROM employees
"""

def plan(sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

def show(title, sql):
    p = plan(sql)
    print(f"\n{title}")
    for line in p:
        print("   ", line)
    n = sum("TEMP B-TREE" in line for line in p)
    print("    -> temp b-tree lines:", n)
    return n

n1 = show("1) one window, no index", SQL_ONE)
n2 = show("2) ROW_NUMBER and RANK share one named window; SUM uses PARTITION BY only", SQL_SAME)
n3 = show("3) two windows with different ORDER BY / PARTITION BY", SQL_DIFF)
con.execute("CREATE INDEX ix_dept_salary ON employees(dept_id, salary DESC, emp_id)")
n4 = show("4) one window again, after CREATE INDEX (dept_id, salary DESC, emp_id)", SQL_ONE)
n5 = show("5) different windows, with the index", SQL_DIFF)

# correctness: SQL ranking equals pandas
sql_res = pd.read_sql_query(SQL_ONE + " ORDER BY emp_id", con)
emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
ordered = emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
ordered["rn"] = ordered.groupby("dept_id").cumcount() + 1
pd_res = ordered.sort_values("emp_id").reset_index(drop=True)[["emp_id", "dept_id", "salary", "rn"]]
# pd:end
pd.testing.assert_frame_equal(sql_res, pd_res, check_dtype=False)
print("\nSQL ROW_NUMBER equals pandas sort + cumcount + 1 on all", len(sql_res), "rows (compared after sorting by emp_id)")
print("note: result rows come back in index/partition order, not emp_id order, unless you add ORDER BY")
print("first 3 rows of SQL_ONE, index in place, no outer ORDER BY:", con.execute(SQL_ONE + " LIMIT 3").fetchall())
```

**Output (my run):**
```text
sqlite 3.45.1 | rows: 3000

1) one window, no index
    CO-ROUTINE (subquery-2)
    SCAN employees
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-2)
    -> temp b-tree lines: 1

2) ROW_NUMBER and RANK share one named window; SUM uses PARTITION BY only
    CO-ROUTINE (subquery-2)
    CO-ROUTINE (subquery-3)
    CO-ROUTINE (subquery-4)
    SCAN employees
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-4)
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-3)
    SCAN (subquery-2)
    -> temp b-tree lines: 2

3) two windows with different ORDER BY / PARTITION BY
    CO-ROUTINE (subquery-2)
    CO-ROUTINE (subquery-3)
    SCAN employees
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-3)
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-2)
    -> temp b-tree lines: 2

4) one window again, after CREATE INDEX (dept_id, salary DESC, emp_id)
    CO-ROUTINE (subquery-2)
    SCAN employees USING COVERING INDEX ix_dept_salary
    SCAN (subquery-2)
    -> temp b-tree lines: 0

5) different windows, with the index
    CO-ROUTINE (subquery-2)
    CO-ROUTINE (subquery-3)
    SCAN employees USING COVERING INDEX ix_dept_salary
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-3)
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-2)
    -> temp b-tree lines: 2

SQL ROW_NUMBER equals pandas sort + cumcount + 1 on all 3000 rows (compared after sorting by emp_id)
note: result rows come back in index/partition order, not emp_id order, unless you add ORDER BY
first 3 rows of SQL_ONE, index in place, no outer ORDER BY: [(270, 0, 3490, 1), (1770, 0, 3490, 2), (540, 0, 3480, 3)]
```

**Edge cases:**
- Without an outer `ORDER BY`, the output order is whatever the window evaluation leaves (in the last line, rows come back by department and salary, not by `emp_id`). Never rely on it.
- An index only helps if its column order and directions match the window: `(dept_id, salary)` helps `PARTITION BY dept_id ORDER BY salary`, not `ORDER BY salary` alone. I only tested one index (salary DESC); I did not test whether an ASC index would also avoid the sort.
- Plan wording differs between SQLite versions and engines. These lines are from 3.45.1 only.
- A window with no PARTITION BY puts the whole table in one partition, so one big sort of everything.

**Then explain:**
- **Why a sort:** RANK needs to know who comes before whom within the partition; the cheapest way is to sort by partition key then order key and walk the rows once.
- **Several windows:** identical window definitions (a named window makes this visible and removes drift) can be computed in one pass over one sorted stream. Different definitions need different orderings, hence another sort. In my run SQLite gave two sorts when the second window had the same partition but no ORDER BY.
- **Index:** a covering index on (dept_id, salary) lets the engine skip the sort. It costs write time and space; that trade-off and reading plans on other engines are Part 11.
- **Other engines:** PostgreSQL and MySQL also sort or use an index for window ordering and show it in `EXPLAIN`, with different wording; I am stating this from general knowledge, not executed here.
- **Cheaper still:** filter rows before the window (`WHERE` runs first), and rank only the columns you need.

**Follow-ups:**
- *Does top-N per group need to sort everything?* A full sort of each partition is the simple plan; some engines have top-N optimisations (not executed here).
- *Is a window faster than a self-join?* Often, because it makes one pass instead of re-reading, but measure on your engine; I did not benchmark.
- *What would you check first on a slow window query?* The plan for a sort that spills to disk, then whether an index matching PARTITION BY + ORDER BY exists.

**Common mistakes:**
- Saying "window functions are slow" without naming the sort.
- Adding an index with the columns in the wrong order and expecting the sort to vanish.
- Declaring several slightly different windows and paying for several sorts.
- Quoting plan text from one engine as if it were universal.

### Q41 ⭐ 🟡 PERCENTILE_CONT and percentiles via windows, hedged: salaries per department. Compute the 90th percentile salary per department in SQLite using the nearest-rank method with ROW_NUMBER / COUNT / CEIL-style arithmetic (or CUME_DIST >= 0.9 and MIN), show PERCENTILE_CONT and PERCENTILE_DISC as PostgreSQL, Snowflake and Oracle dialect text (hedged, not executed), and explain the difference between nearest-rank, interpolated, and pandas quantile(0.9) (linear interpolation by default). Run pandas and compare numbers, saying exactly where they differ.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** SQLite has no PERCENTILE_CONT, so the 90th percentile is built from ROW_NUMBER and COUNT (nearest-rank: the value at rank ceil(0.9 n)), or CUME_DIST >= 0.9 with MIN, or an interpolation between two neighbouring ranks; pandas `quantile(0.9)` is the interpolated one, so it gives different numbers from nearest-rank except when the position lands exactly on a row.

**Schema and sample data:** five departments chosen to expose the differences: dept 10 has ten salaries 10..100, dept 20 has four (100..400), dept 30 has one, dept 40 has seven with ties (10, 20 x5, 90), and dept 50 has one real salary (70) and two NULLs, which are filtered first.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,10,10),(2,10,20),(3,10,30),(4,10,40),(5,10,50),(6,10,60),(7,10,70),(8,10,80),(9,10,90),(10,10,100),
 (11,20,100),(12,20,200),(13,20,300),(14,20,400),
 (15,30,500),
 (16,40,10),(17,40,20),(18,40,20),(19,40,20),(20,40,20),(21,40,20),(22,40,90),
 (23,50,NULL),(24,50,70),(25,50,NULL);
```

**SQL answer:** nearest-rank with ROW_NUMBER (`SQL_NEAREST`; `ceil(9n/10)` written as `(9n + 9) / 10` in integer arithmetic so no CEIL function or float rounding is needed), the CUME_DIST form (`SQL_CUME`) and the interpolated form (`SQL_INTERP`).
```sql
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, salary AS p90_nearest
FROM r
WHERE rn = (9 * n + 9) / 10
ORDER BY dept_id
```
```sql
WITH c AS (
  SELECT dept_id, salary,
         CUME_DIST() OVER (PARTITION BY dept_id ORDER BY salary) AS cd
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, MIN(salary) AS p90_nearest
FROM c
WHERE cd >= 0.9
GROUP BY dept_id
ORDER BY dept_id
```
```sql
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
), p AS (
  SELECT dept_id, n,
         1 + (9 * (n - 1)) / 10          AS lo,
         (9 * (n - 1)) % 10 / 10.0       AS frac
  FROM r GROUP BY dept_id
)
SELECT p.dept_id,
       MAX(CASE WHEN r.rn = p.lo     THEN r.salary END) +
       p.frac * (COALESCE(MAX(CASE WHEN r.rn = p.lo + 1 THEN r.salary END),
                          MAX(CASE WHEN r.rn = p.lo     THEN r.salary END))
                 - MAX(CASE WHEN r.rn = p.lo THEN r.salary END)) AS p90_interp
FROM p JOIN r ON r.dept_id = p.dept_id
GROUP BY p.dept_id
ORDER BY p.dept_id
```
Dialect text, not executed here: PostgreSQL, Snowflake and Oracle have `PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY salary)` (interpolated) and `PERCENTILE_DISC(0.9) WITHIN GROUP (ORDER BY salary)` (the nearest-rank style value that actually exists in the data). Used per department with `GROUP BY dept_id`. SQL Server and BigQuery have analytic-function forms of PERCENTILE_CONT with an OVER clause; MySQL has no built-in. I am stating this from memory.

**pandas answer:** default `quantile` is linear interpolation. For nearest-rank I use numpy's `inverted_cdf` method (pandas `Series.quantile` does not take that method).
```python
clean = emp.dropna(subset=["salary"])
pd_linear = clean.groupby("dept_id")["salary"].quantile(0.9)                # default interpolation='linear'
pd_nearest = clean.groupby("dept_id")["salary"].apply(
    lambda s: np.quantile(s, 0.9, method="inverted_cdf"))                   # nearest-rank (numpy method name)
pd_higher = clean.groupby("dept_id")["salary"].quantile(0.9, interpolation="higher")
```

**Example:** dept 10 (n = 10, values 10..100).
- Nearest rank: ceil(0.9 x 10) = 9, the 9th smallest is 90. Check with CUME_DIST: the value 90 has 9 of 10 rows at or below it, 0.9, the first value reaching 0.9.
- Interpolated: position 1 + 0.9 x 9 = 9.1, so 90 + 0.1 x (100 - 90) = 91. pandas gives 91.0 too.
- Dept 20 (n = 4): nearest rank ceil(3.6) = 4, value 400; interpolated position 1 + 0.9 x 3 = 3.7, so 300 + 0.7 x 100 = 370.
- Dept 40 (n = 7, ties): nearest rank ceil(6.3) = 7, value 90; interpolated position 6.4, so 20 + 0.4 x 70 = 48 (a value that is not in the data).
- Dept 30 and 50 have one usable value, so every method returns it.

**Code:** run with `python3 -I`.
```python
# Q41: 90th percentile per department: nearest-rank, interpolated (PERCENTILE_CONT style), pandas
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,10,10),(2,10,20),(3,10,30),(4,10,40),(5,10,50),(6,10,60),(7,10,70),(8,10,80),(9,10,90),(10,10,100),
 (11,20,100),(12,20,200),(13,20,300),(14,20,400),
 (15,30,500),
 (16,40,10),(17,40,20),(18,40,20),(19,40,20),(20,40,20),(21,40,20),(22,40,90),
 (23,50,NULL),(24,50,70),(25,50,NULL);
"""
# nearest rank: value at rank k = ceil(0.9 * n) in ascending order; ceil(9n/10) = (9n + 9) / 10 in integer arithmetic
SQL_NEAREST = """
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, salary AS p90_nearest
FROM r
WHERE rn = (9 * n + 9) / 10
ORDER BY dept_id
"""
SQL_CUME = """
WITH c AS (
  SELECT dept_id, salary,
         CUME_DIST() OVER (PARTITION BY dept_id ORDER BY salary) AS cd
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, MIN(salary) AS p90_nearest
FROM c
WHERE cd >= 0.9
GROUP BY dept_id
ORDER BY dept_id
"""
# interpolated (what PERCENTILE_CONT(0.9) does): position 1 + 0.9 * (n - 1), blend the two neighbours
SQL_INTERP = """
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
), p AS (
  SELECT dept_id, n,
         1 + (9 * (n - 1)) / 10          AS lo,
         (9 * (n - 1)) % 10 / 10.0       AS frac
  FROM r GROUP BY dept_id
)
SELECT p.dept_id,
       MAX(CASE WHEN r.rn = p.lo     THEN r.salary END) +
       p.frac * (COALESCE(MAX(CASE WHEN r.rn = p.lo + 1 THEN r.salary END),
                          MAX(CASE WHEN r.rn = p.lo     THEN r.salary END))
                 - MAX(CASE WHEN r.rn = p.lo THEN r.salary END)) AS p90_interp
FROM p JOIN r ON r.dept_id = p.dept_id
GROUP BY p.dept_id
ORDER BY p.dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
nearest = pd.read_sql_query(SQL_NEAREST, con)
cume = pd.read_sql_query(SQL_CUME, con)
interp = pd.read_sql_query(SQL_INTERP, con)
assert nearest.equals(cume), "ROW_NUMBER nearest-rank and CUME_DIST >= 0.9 should agree"

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
clean = emp.dropna(subset=["salary"])
pd_linear = clean.groupby("dept_id")["salary"].quantile(0.9)                # default interpolation='linear'
pd_nearest = clean.groupby("dept_id")["salary"].apply(
    lambda s: np.quantile(s, 0.9, method="inverted_cdf"))                   # nearest-rank (numpy method name)
pd_higher = clean.groupby("dept_id")["salary"].quantile(0.9, interpolation="higher")
# pd:end
cmp = pd.DataFrame({"n": clean.groupby("dept_id").size(),
                    "sql_nearest": nearest.set_index("dept_id")["p90_nearest"],
                    "np_inverted_cdf": pd_nearest,
                    "pandas_higher": pd_higher,
                    "sql_interp": interp.set_index("dept_id")["p90_interp"],
                    "pandas_quantile": pd_linear})
print(cmp.to_string())
assert np.allclose(cmp["sql_nearest"], cmp["np_inverted_cdf"])
assert np.allclose(cmp["sql_interp"], cmp["pandas_quantile"])
diff = cmp.index[cmp["sql_nearest"] != cmp["pandas_quantile"]].tolist()
print("\ndepartments where nearest-rank != pandas default quantile:", diff)
print("departments where pandas 'higher' != nearest-rank:", cmp.index[cmp["sql_nearest"] != cmp["pandas_higher"]].tolist())
print("dept 50 has", int(emp[emp.dept_id == 50]["salary"].isna().sum()), "NULL salaries filtered first; n counts only the non-NULL one")
print("asserts passed: ROW_NUMBER == CUME_DIST (nearest-rank); SQL interpolation == pandas quantile; numpy inverted_cdf == nearest-rank")
```

**Output (my run):**
```text
          n  sql_nearest  np_inverted_cdf  pandas_higher  sql_interp  pandas_quantile
dept_id                                                                              
10       10           90             90.0          100.0        91.0             91.0
20        4          400            400.0          400.0       370.0            370.0
30        1          500            500.0          500.0       500.0            500.0
40        7           90             90.0           90.0        48.0             48.0
50        1           70             70.0           70.0        70.0             70.0

departments where nearest-rank != pandas default quantile: [10, 20, 40]
departments where pandas 'higher' != nearest-rank: [10]
dept 50 has 2 NULL salaries filtered first; n counts only the non-NULL one
asserts passed: ROW_NUMBER == CUME_DIST (nearest-rank); SQL interpolation == pandas quantile; numpy inverted_cdf == nearest-rank
```

**Edge cases:**
- Where they differ: nearest-rank and pandas default quantile differ in departments 10, 20 and 40 and agree in 30 and 50 (see output). They agree only when the interpolation position is a whole number or n = 1.
- pandas `interpolation='higher'` is not nearest-rank either: it differs in dept 10 (100.0 versus 90) because it rounds the interpolation position up, not the rank 0.9 n.
- NULLs: filtered first with `WHERE salary IS NOT NULL`, otherwise they would count in `n` and take ranks. Dept 50's n is 1.
- Ties: nearest-rank is well defined with ties (the value at that rank); the row chosen does not matter because the values are equal. I added emp_id to the ROW_NUMBER order only so the numbering is repeatable.
- Floating point: the nearest-rank row uses integers; `CUME_DIST >= 0.9` compares floats, which matched here (9/10 equals the literal 0.9), but I would prefer the integer form in production.

**Then explain:**
- **Nearest-rank:** sort, take the value at rank ceil(p n). Always returns a value that exists in the data. It is what PERCENTILE_DISC is meant to do (from documentation memory, not executed).
- **Interpolated (continuous):** treat the sorted values as points on a line and read the p position, which can fall between two values. SQL PERCENTILE_CONT and pandas default `quantile` agree on this definition; my SQL emulation matched pandas exactly in the assert.
- **Small groups:** the two definitions disagree most when n is small, which is exactly the per-group case.
- **Say which one you used.** A "p90" without a definition is ambiguous.

**Follow-ups:**
- *Median this way?* p = 0.5; see Q38.
- *Which should a dashboard use?* Whichever matches the other tools it is compared against; for small groups document it.
- *Can CUME_DIST replace the ROW_NUMBER form?* Yes for nearest-rank, as asserted, with the float caveat.

**Common mistakes:**
- Taking the top 10 percent of the whole table with one LIMIT instead of computing the percentile per department.
- Not filtering NULLs before computing `n`.
- Comparing SQL nearest-rank with pandas default quantile and calling the difference a bug.
- Using `ntile(10) = 10` as the 90th percentile (bucket sizes are positional).

### Q42 ⭐ 🟡 PERCENT_RANK, CUME_DIST and pandas rank(pct=True) are not the same thing: scores with ties on a small table. Compute SQL RANK, PERCENT_RANK ((rank-1)/(n-1)), CUME_DIST (rank of last peer / n) and pandas rank(pct=True) with method='average', 'min' and 'max', then show which pandas call equals CUME_DIST (method='max', pct=True) and how to get PERCENT_RANK ((rank(method='min') - 1) / (n - 1)). Run all in one script and assert the matches.
**Asked at:** pandas reference and user guide (DataFrame.rank, qcut; groupby, Comparison with SQL), not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** They are three different definitions: PERCENT_RANK is (rank - 1) / (n - 1) and starts at 0, CUME_DIST is (rows up to the last tied row) / n and ends at 1, and pandas `rank(pct=True)` is rank / n, which equals CUME_DIST only with `method='max'` and is not PERCENT_RANK at all.

**Schema and sample data:** seven scores with a tie of two (85) and a tie of three (70), plus a one-row table for the edge case.
```sql
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,90),(2,85),(3,85),(4,70),(5,70),(6,70),(7,60);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
```

**SQL answer:** `SQL_MAIN` shows RANK, PERCENT_RANK and CUME_DIST with scores descending; `SQL_SOLO` is the one-row case.
```sql
SELECT student_id, score,
       RANK()         OVER (ORDER BY score DESC) AS rnk,
       PERCENT_RANK() OVER (ORDER BY score DESC) AS pct_rank,
       CUME_DIST()    OVER (ORDER BY score DESC) AS cume_dist
FROM scores
ORDER BY student_id
```
```sql
SELECT student_id, PERCENT_RANK() OVER (ORDER BY score) AS pr, CUME_DIST() OVER (ORDER BY score) AS cd FROM solo
```

**pandas answer:** pct with the three tie methods, and the PERCENT_RANK formula built from `method='min'`.
```python
r_avg = sc["score"].rank(pct=True, ascending=False)                    # method='average' (default)
r_min = sc["score"].rank(pct=True, ascending=False, method="min")
r_max = sc["score"].rank(pct=True, ascending=False, method="max")
rank_min = sc["score"].rank(ascending=False, method="min")
pd_percent_rank = (rank_min - 1) / (n - 1)
```

**Example:** n = 7, scores descending.
- 90: RANK 1; PERCENT_RANK (1 - 1) / 6 = 0; CUME_DIST 1 / 7 = 0.1429.
- Two 85s: RANK 2 for both; PERCENT_RANK (2 - 1) / 6 = 0.1667; CUME_DIST uses the last tied row, row 3, so 3 / 7 = 0.4286.
- Three 70s: RANK 4; PERCENT_RANK 3 / 6 = 0.5; CUME_DIST 6 / 7 = 0.8571.
- 60: RANK 7; PERCENT_RANK 6 / 6 = 1; CUME_DIST 7 / 7 = 1.
- pandas pct for the two 85s: `method='min'` gives 2 / 7 = 0.2857, `'max'` gives 3 / 7 = 0.4286 (equal to CUME_DIST), and the default `'average'` gives rank 2.5 / 7 = 0.3571, which matches neither SQL function.

**Code:** run with `python3 -I`.
```python
# Q42: RANK, PERCENT_RANK, CUME_DIST versus pandas rank(pct=True)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,90),(2,85),(3,85),(4,70),(5,70),(6,70),(7,60);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
"""
SQL_MAIN = """
SELECT student_id, score,
       RANK()         OVER (ORDER BY score DESC) AS rnk,
       PERCENT_RANK() OVER (ORDER BY score DESC) AS pct_rank,
       CUME_DIST()    OVER (ORDER BY score DESC) AS cume_dist
FROM scores
ORDER BY student_id
"""
SQL_SOLO = """
SELECT student_id, PERCENT_RANK() OVER (ORDER BY score) AS pr, CUME_DIST() OVER (ORDER BY score) AS cd FROM solo
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql = pd.read_sql_query(SQL_MAIN, con)
solo = pd.read_sql_query(SQL_SOLO, con)

sc = pd.read_sql_query("SELECT * FROM scores ORDER BY student_id", con)
n = len(sc)
# pd:main
r_avg = sc["score"].rank(pct=True, ascending=False)                    # method='average' (default)
r_min = sc["score"].rank(pct=True, ascending=False, method="min")
r_max = sc["score"].rank(pct=True, ascending=False, method="max")
rank_min = sc["score"].rank(ascending=False, method="min")
pd_percent_rank = (rank_min - 1) / (n - 1)
# pd:end
out = sql.copy()
out["pd_avg"], out["pd_min"], out["pd_max"], out["pd_pr"] = r_avg.round(4), r_min.round(4), r_max.round(4), pd_percent_rank.round(4)
out["pct_rank"], out["cume_dist"] = out["pct_rank"].round(4), out["cume_dist"].round(4)
print(out.to_string(index=False))
assert np.allclose(sql["cume_dist"], r_max)
assert np.allclose(sql["pct_rank"], pd_percent_rank)
assert np.allclose(sql["rnk"] / n, r_min)           # pandas pct with method='min' is rank / n
assert not np.allclose(sql["cume_dist"], r_avg)
print("\nmatches: CUME_DIST == rank(pct=True, method='max'); PERCENT_RANK == (rank(method='min') - 1) / (n - 1); rank(pct=True, method='min') == RANK / n")
print("rank(pct=True) with the default 'average' matches neither:", r_avg.round(4).tolist())

print("\none-row table, SQL:", solo.to_dict("records"))
one = pd.Series([75])
with np.errstate(all="ignore"):
    print("one-row pandas (rank-1)/(n-1):", ((one.rank(method='min') - 1) / (len(one) - 1)).tolist(), "<- 0/0 is NaN; SQLite returns 0.0")
print("asserts passed")
```

**Output (my run):**
```text
 student_id  score  rnk  pct_rank  cume_dist  pd_avg  pd_min  pd_max  pd_pr
          1     90    1    0.0000     0.1429  0.1429  0.1429  0.1429 0.0000
          2     85    2    0.1667     0.4286  0.3571  0.2857  0.4286 0.1667
          3     85    2    0.1667     0.4286  0.3571  0.2857  0.4286 0.1667
          4     70    4    0.5000     0.8571  0.7143  0.5714  0.8571 0.5000
          5     70    4    0.5000     0.8571  0.7143  0.5714  0.8571 0.5000
          6     70    4    0.5000     0.8571  0.7143  0.5714  0.8571 0.5000
          7     60    7    1.0000     1.0000  1.0000  1.0000  1.0000 1.0000

matches: CUME_DIST == rank(pct=True, method='max'); PERCENT_RANK == (rank(method='min') - 1) / (n - 1); rank(pct=True, method='min') == RANK / n
rank(pct=True) with the default 'average' matches neither: [0.1429, 0.3571, 0.3571, 0.7143, 0.7143, 0.7143, 1.0]

one-row table, SQL: [{'student_id': 1, 'pr': 0.0, 'cd': 1.0}]
one-row pandas (rank-1)/(n-1): [nan] <- 0/0 is NaN; SQLite returns 0.0
asserts passed
```

**Edge cases:**
- One-row partition: PERCENT_RANK is 0.0 and CUME_DIST is 1.0 in SQLite (output). The pandas formula (rank - 1) / (n - 1) is 0 / 0 = NaN, so you must handle it (for example `fillna(0)`) to match SQL.
- Ties: PERCENT_RANK ties share one value (all based on the min rank), CUME_DIST ties share one value (based on the max position).
- Direction: I ranked with `ascending=False` in pandas and `ORDER BY score DESC` in SQL, so rank 1 is the top score. Flip both together; the formulas then describe the share of rows below or above you in the other direction.
- NULL scores: not in this table; they would take a rank in SQL (see Q29) and stay NaN in pandas by default.

**Then explain:**
- **Words:** PERCENT_RANK is "the fraction of the other rows that come strictly before this row's tie group". CUME_DIST is "the fraction of all rows at or before this row's tie group".
- **Why CUME_DIST >= 0.9 selects at least 10 percent:** a row's value includes its ties and itself.
- **pandas:** `rank(pct=True, method='max')` is CUME_DIST; `rank(method='min')` minus 1 over n minus 1 is PERCENT_RANK. Asserted in the Code block.
- **Default average:** the default `method='average'` is neither; it is often what people use by accident.

**Follow-ups:**
- *Which gives 0 for the lowest row?* PERCENT_RANK; CUME_DIST's lowest row is 1/n at least.
- *Which one for "top 10 percent"?* CUME_DIST on the descending order or >= 0.9 on ascending, see Q36 and Q47.
- *Do they ever agree?* On the last row both are 1.0 in the output; elsewhere they differ on this data.

**Common mistakes:**
- Assuming `rank(pct=True)` is PERCENT_RANK.
- Forgetting the one-row division by zero in pandas.
- Mixing `method='average'` pct with a SQL threshold and getting a different set of rows.
- Dividing RANK by COUNT yourself and calling it CUME_DIST (it is the min-method pct, not the max).

### Q43 ⭐ 🟡 Windows, DISTINCT and ORDER BY interplay: employees(emp_id, name, dept_id, salary). Show that SELECT DISTINCT dept_id, ROW_NUMBER() OVER (...) does not deduplicate as expected because the window runs before DISTINCT, that window functions may appear only in the SELECT list and ORDER BY, and how to rank departments by average salary in one query (ORDER BY RANK() OVER (...) in the outer query or via a CTE). Run it on SQLite and explain the evaluation order again in one line.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Window functions are computed after FROM, WHERE, GROUP BY and HAVING and before DISTINCT, ORDER BY and LIMIT, so `SELECT DISTINCT dept_id, ROW_NUMBER() OVER (...)` numbers every row first and DISTINCT then finds nothing to remove; windows are allowed only in the SELECT list and ORDER BY.

**Schema and sample data:** six employees in three departments (10: Asha 50, Ben 70, Chitra 60; 20: Dev 90, Esha 40; 30: Farid 55).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55);
```

**SQL answer:** the DISTINCT trap (`SQL_DISTINCT_BAD`), the case where DISTINCT does work because the window value repeats (`SQL_DISTINCT_OK`), and three ways to rank departments by average salary: window over an aggregate (`SQL_ONE_QUERY`), window in ORDER BY (`SQL_ORDER_BY_WINDOW`), and a CTE (`SQL_CTE`).
```sql
SELECT DISTINCT dept_id, ROW_NUMBER() OVER (ORDER BY dept_id) AS rn
FROM employees
ORDER BY rn
```
```sql
SELECT DISTINCT dept_id, DENSE_RANK() OVER (ORDER BY dept_id) AS drk
FROM employees
ORDER BY dept_id
```
```sql
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary,
       RANK() OVER (ORDER BY AVG(salary) DESC) AS rnk
FROM employees
GROUP BY dept_id
ORDER BY rnk, dept_id
```
```sql
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id
ORDER BY RANK() OVER (ORDER BY AVG(salary) DESC), dept_id
```
```sql
WITH d AS (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id)
SELECT dept_id, ROUND(avg_salary, 2) AS avg_salary, RANK() OVER (ORDER BY avg_salary DESC) AS rnk
FROM d
ORDER BY rnk, dept_id
```

**pandas answer:** `groupby().mean()` then `rank`, with no ordering of evaluation to worry about because each step is a separate statement.
```python
g = emp.groupby("dept_id", as_index=False)["salary"].mean().rename(columns={"salary": "avg_salary"})
g["rnk"] = g["avg_salary"].rank(method="min", ascending=False).astype(int)
pd_df = g.sort_values(["rnk", "dept_id"]).reset_index(drop=True)
pd_df["avg_salary"] = pd_df["avg_salary"].round(2)
```

**Example:**
- `ROW_NUMBER() OVER (ORDER BY dept_id)` gives 1 to 6 on the six employee rows. Each (dept_id, rn) pair is unique, so DISTINCT removes nothing and returns six rows, not three.
- `DENSE_RANK() OVER (ORDER BY dept_id)` gives 1, 1, 1, 2, 2, 3. Within a department the pair is identical, so DISTINCT collapses to three rows. DISTINCT is not broken; it ran after the window.
- Department averages: 10 is 60, 20 is 65, 30 is 55. Ranked by average descending: 20, 10, 30.

**Code:** run with `python3 -I`.
```python
# Q43: windows, DISTINCT and ORDER BY interplay
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55);
"""
SQL_DISTINCT_BAD = """
SELECT DISTINCT dept_id, ROW_NUMBER() OVER (ORDER BY dept_id) AS rn
FROM employees
ORDER BY rn
"""
SQL_DISTINCT_OK = """
SELECT DISTINCT dept_id, DENSE_RANK() OVER (ORDER BY dept_id) AS drk
FROM employees
ORDER BY dept_id
"""
SQL_ONE_QUERY = """
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary,
       RANK() OVER (ORDER BY AVG(salary) DESC) AS rnk
FROM employees
GROUP BY dept_id
ORDER BY rnk, dept_id
"""
SQL_ORDER_BY_WINDOW = """
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id
ORDER BY RANK() OVER (ORDER BY AVG(salary) DESC), dept_id
"""
SQL_CTE = """
WITH d AS (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id)
SELECT dept_id, ROUND(avg_salary, 2) AS avg_salary, RANK() OVER (ORDER BY avg_salary DESC) AS rnk
FROM d
ORDER BY rnk, dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)

bad = q(SQL_DISTINCT_BAD)
print("SELECT DISTINCT dept_id, ROW_NUMBER() ... returns", len(bad), "rows (6 employees, 3 departments):")
print(bad.to_string(index=False))
assert len(bad) == 6
ok = q(SQL_DISTINCT_OK)
print("\nwith DENSE_RANK over dept_id the window value is the same inside a department, so DISTINCT collapses:")
print(ok.to_string(index=False))
assert len(ok) == 3

for label, sql in [("window in WHERE", "SELECT * FROM employees WHERE ROW_NUMBER() OVER (ORDER BY salary) = 1"),
                   ("window in GROUP BY", "SELECT 1 FROM employees GROUP BY ROW_NUMBER() OVER (ORDER BY salary)"),
                   ("window inside an aggregate", "SELECT SUM(ROW_NUMBER() OVER (ORDER BY salary)) FROM employees")]:
    try:
        con.execute(sql).fetchall(); print(label, "-> ran")
    except sqlite3.Error as e:
        print(f"\n{label} -> {type(e).__name__}: {e}")

one = q(SQL_ONE_QUERY); ob = q(SQL_ORDER_BY_WINDOW); cte = q(SQL_CTE)
print("\ndepartments ranked by average salary, one query:"); print(one.to_string(index=False))
assert one[["dept_id", "avg_salary"]].equals(ob) and one.equals(cte)

emp = q("SELECT * FROM employees")
# pd:main
g = emp.groupby("dept_id", as_index=False)["salary"].mean().rename(columns={"salary": "avg_salary"})
g["rnk"] = g["avg_salary"].rank(method="min", ascending=False).astype(int)
pd_df = g.sort_values(["rnk", "dept_id"]).reset_index(drop=True)
pd_df["avg_salary"] = pd_df["avg_salary"].round(2)
# pd:end
pd.testing.assert_frame_equal(one, pd_df, check_dtype=False)
print("\nasserts passed: three SQL forms equal each other and pandas groupby mean + rank(method='min')")
```

**Output (my run):**
```text
SELECT DISTINCT dept_id, ROW_NUMBER() ... returns 6 rows (6 employees, 3 departments):
 dept_id  rn
      10   1
      10   2
      10   3
      20   4
      20   5
      30   6

with DENSE_RANK over dept_id the window value is the same inside a department, so DISTINCT collapses:
 dept_id  drk
      10    1
      20    2
      30    3

window in WHERE -> OperationalError: misuse of window function ROW_NUMBER()

window in GROUP BY -> OperationalError: misuse of window function ROW_NUMBER()

window inside an aggregate -> OperationalError: misuse of window function ROW_NUMBER()

departments ranked by average salary, one query:
 dept_id  avg_salary  rnk
      20        65.0    1
      10        60.0    2
      30        55.0    3

asserts passed: three SQL forms equal each other and pandas groupby mean + rank(method='min')
```

**Edge cases:**
- SQLite rejected a window function in WHERE, in GROUP BY and inside an aggregate with the same message (`misuse of window function ROW_NUMBER()`); see the output. The wording is SQLite's, other engines word it differently (not executed).
- `RANK() OVER (ORDER BY AVG(salary) DESC)` works because the window runs after GROUP BY and sees one row per department with the aggregate already computed. The window cannot be placed inside an aggregate, but an aggregate can be inside a window's ORDER BY.
- Ties in the average would share a rank (RANK), and I added `dept_id` to the outer ORDER BY so the printed order is repeatable.
- Departments with all-NULL salaries have a NULL average; they would sort as NULL (smallest in SQLite).

**Then explain:**
- **Order of evaluation in one line:** FROM, WHERE, GROUP BY, HAVING, window functions, SELECT list, DISTINCT, ORDER BY, LIMIT.
- **Where windows may appear:** SELECT list and ORDER BY only (the SQLite documentation page and the PostgreSQL tutorial both say this).
- **To deduplicate on a window result:** put the window in a CTE or subquery and filter or DISTINCT outside.
- **Ranking departments by average:** all three forms gave the same rows in my run; the CTE reads best.
- **pandas parallel:** `drop_duplicates` after adding a row number would also keep every row, for the same reason.

**Follow-ups:**
- *Can I `ORDER BY` a window function?* Yes, as in `SQL_ORDER_BY_WINDOW`; the window is computed, then the result is sorted by it.
- *Why not `WHERE rn = 1` directly?* The window does not exist yet at WHERE time; use a CTE (Q3).
- *What is the cleanest way to get one row per department?* GROUP BY if you only need aggregates, ROW_NUMBER = 1 in a CTE if you need a whole row.

**Common mistakes:**
- Using DISTINCT to remove duplicates created by a row number.
- Writing `AVG(RANK() OVER ...)` and expecting it to work.
- Trusting the display order after a window query with no outer ORDER BY.
- Assuming DISTINCT runs before the window.

### Q44 ⭐ 🔴 Dedup with several tie-break criteria: product_prices(row_id, product_id, price, source, updated_at) where several rows per product share the latest updated_at, and a source priority applies ('manual' beats 'feed' beats 'scrape'). Keep one row per product: latest updated_at, then highest source priority (CASE expression in ORDER BY), then highest row_id. Show ROW_NUMBER with a CASE in the ORDER BY, and the pandas version using a priority map and sort_values with keep='first'. Explain how to prove the result is unique per product.
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Keep one row per product with `ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY updated_at DESC, <CASE priority> DESC, row_id DESC) = 1`; the CASE turns the text source into a rank (manual 3, feed 2, scrape 1, anything else 0) and the unique `row_id` last makes the choice repeatable, and in pandas the same keys go into `sort_values` before `drop_duplicates(keep='first')`.

**Schema and sample data:** nine price rows for four products. Product 100 has three rows on the latest date with different sources (scrape, manual, feed); product 200 has two 'feed' rows on the same date (only `row_id` separates them); product 300 has 'import' (an unknown source) and 'scrape' on the same date; product 400 has a NULL source.
```sql
CREATE TABLE product_prices(row_id INTEGER PRIMARY KEY, product_id INTEGER, price INTEGER, source TEXT, updated_at TEXT);
INSERT INTO product_prices VALUES
 (1,100,50,'feed',  '2026-03-01'),
 (2,100,52,'scrape','2026-03-02'),
 (3,100,51,'manual','2026-03-02'),
 (4,100,53,'feed',  '2026-03-02'),
 (5,200,70,'feed',  '2026-03-05'),
 (6,200,71,'feed',  '2026-03-05'),
 (7,300,10,'import','2026-03-01'),
 (8,300,11,'scrape','2026-03-01'),
 (9,400,99,NULL,    '2026-03-04');
```

**SQL answer:** `SQL_MAIN` is the answer; `SQL_WRONG_ALPHA` shows the mistake of sorting the source text itself.
```sql
WITH r AS (
  SELECT row_id, product_id, price, source, updated_at,
         ROW_NUMBER() OVER (
           PARTITION BY product_id
           ORDER BY updated_at DESC,
                    CASE source WHEN 'manual' THEN 3 WHEN 'feed' THEN 2 WHEN 'scrape' THEN 1 ELSE 0 END DESC,
                    row_id DESC
         ) AS rn
  FROM product_prices
)
SELECT row_id, product_id, price, source, updated_at
FROM r
WHERE rn = 1
ORDER BY product_id
```
```sql
WITH r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY updated_at DESC, source DESC, row_id DESC) AS rn
  FROM product_prices
)
SELECT row_id, product_id, source FROM r WHERE rn = 1 ORDER BY product_id
```

**pandas answer:** map the source to a number (unknown or NULL gets 0), sort so the best row is first within each product, keep the first row.
```python
prio = {"manual": 3, "feed": 2, "scrape": 1}
pp["prio"] = pp["source"].map(prio).fillna(0)          # unknown or NULL source ranks lowest
pd_df = (pp.sort_values(["product_id", "updated_at", "prio", "row_id"], ascending=[True, False, False, False])
           .drop_duplicates("product_id", keep="first")
           .drop(columns="prio")
           .reset_index(drop=True))
```

**Example:**
- Product 100: latest date is 2026-03-02 (rows 2, 3, 4). Priorities: scrape 1, manual 3, feed 2, so row 3 (manual, price 51) wins.
- Product 200: both rows share date and priority; the highest `row_id` wins, row 6 (price 71).
- Product 300: same date; 'scrape' has priority 1 and 'import' is unknown (0), so row 8 wins.
- Product 400: one row, kept even though its source is NULL.
- Wrong alphabetical sort: `source DESC` puts 'scrape' above 'manual' and 'feed', so product 100 would keep row 2 (scrape). Alphabet is not the business priority.

**Code:** run with `python3 -I`.
```python
# Q44: dedup with several tie-break criteria (CASE priority)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE product_prices(row_id INTEGER PRIMARY KEY, product_id INTEGER, price INTEGER, source TEXT, updated_at TEXT);
INSERT INTO product_prices VALUES
 (1,100,50,'feed',  '2026-03-01'),
 (2,100,52,'scrape','2026-03-02'),
 (3,100,51,'manual','2026-03-02'),
 (4,100,53,'feed',  '2026-03-02'),
 (5,200,70,'feed',  '2026-03-05'),
 (6,200,71,'feed',  '2026-03-05'),
 (7,300,10,'import','2026-03-01'),
 (8,300,11,'scrape','2026-03-01'),
 (9,400,99,NULL,    '2026-03-04');
"""
SQL_MAIN = """
WITH r AS (
  SELECT row_id, product_id, price, source, updated_at,
         ROW_NUMBER() OVER (
           PARTITION BY product_id
           ORDER BY updated_at DESC,
                    CASE source WHEN 'manual' THEN 3 WHEN 'feed' THEN 2 WHEN 'scrape' THEN 1 ELSE 0 END DESC,
                    row_id DESC
         ) AS rn
  FROM product_prices
)
SELECT row_id, product_id, price, source, updated_at
FROM r
WHERE rn = 1
ORDER BY product_id
"""
SQL_WRONG_ALPHA = """
WITH r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY updated_at DESC, source DESC, row_id DESC) AS rn
  FROM product_prices
)
SELECT row_id, product_id, source FROM r WHERE rn = 1 ORDER BY product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql = pd.read_sql_query(SQL_MAIN, con)
print("kept rows:"); print(sql.to_string(index=False, na_rep="NULL"))

# proof of uniqueness: one row per product, and the sort key (product, updated_at, priority, row_id) has no duplicates
assert sql["product_id"].is_unique
dups = con.execute("""
SELECT COUNT(*) FROM (
  SELECT product_id, updated_at,
         CASE source WHEN 'manual' THEN 3 WHEN 'feed' THEN 2 WHEN 'scrape' THEN 1 ELSE 0 END AS prio, row_id
  FROM product_prices GROUP BY 1, 2, 3, 4 HAVING COUNT(*) > 1)""").fetchone()[0]
print("\nduplicate full sort keys (must be 0 for a repeatable pick):", dups)
assert dups == 0
print("rows kept vs distinct products:", len(sql), "vs", con.execute("SELECT COUNT(DISTINCT product_id) FROM product_prices").fetchone()[0])
print("\nalphabetical source DESC instead of the CASE (wrong):")
print(pd.read_sql_query(SQL_WRONG_ALPHA, con).to_string(index=False, na_rep="NULL"))

pp = pd.read_sql_query("SELECT * FROM product_prices", con)
# pd:main
prio = {"manual": 3, "feed": 2, "scrape": 1}
pp["prio"] = pp["source"].map(prio).fillna(0)          # unknown or NULL source ranks lowest
pd_df = (pp.sort_values(["product_id", "updated_at", "prio", "row_id"], ascending=[True, False, False, False])
           .drop_duplicates("product_id", keep="first")
           .drop(columns="prio")
           .reset_index(drop=True))
# pd:end
pd.testing.assert_frame_equal(sql, pd_df, check_dtype=False)
assert not pp.duplicated(["product_id", "updated_at", "prio", "row_id"]).any()
print("\nasserts passed: SQL ROW_NUMBER with CASE == pandas map + sort_values + drop_duplicates (rows compared in product_id order)")
```

**Output (my run):**
```text
kept rows:
 row_id  product_id  price source updated_at
      3         100     51 manual 2026-03-02
      6         200     71   feed 2026-03-05
      8         300     11 scrape 2026-03-01
      9         400     99   NULL 2026-03-04

duplicate full sort keys (must be 0 for a repeatable pick): 0
rows kept vs distinct products: 4 vs 4

alphabetical source DESC instead of the CASE (wrong):
 row_id  product_id source
      2         100 scrape
      6         200   feed
      8         300 scrape
      9         400   NULL

asserts passed: SQL ROW_NUMBER with CASE == pandas map + sort_values + drop_duplicates (rows compared in product_id order)
```

**Edge cases:**
- Unknown or NULL source: the CASE `ELSE 0` handles both (NULL matches no WHEN). Without an ELSE the CASE returns NULL, and with DESC order NULL sorts last in SQLite anyway, but write the ELSE so the rule is explicit.
- A source spelled differently ('Manual', ' manual') hits the ELSE and loses silently; normalise first if the data is messy.
- Same `updated_at` as text: ISO dates sort correctly as text; other formats do not.
- How to prove uniqueness: (1) the result has exactly as many rows as distinct products (checked in the Code block, 4 and 4); (2) the full sort key (product_id, updated_at, priority, row_id) has no duplicates, which is guaranteed because `row_id` is a primary key and checked by a GROUP BY ... HAVING COUNT(*) > 1 query returning 0.

**Then explain:**
- **Order of keys is the business rule:** newest first, then source trust, then newest row id. A tie-break column that is not unique is not a tie-break.
- **Why a CASE:** the ORDER BY needs a sortable rank; the alphabet is wrong here, as the run shows.
- **pandas:** a dictionary plus `map` is the CASE; `fillna(0)` is the ELSE. With one `ascending` list the directions can differ per key.
- **Stability:** I do not rely on the sort being stable, because every key combination is unique.

**Follow-ups:**
- *Priority stored in a lookup table?* Join to it (LEFT JOIN with COALESCE to 0) and order by that column.
- *Should the priority beat the date?* Then swap the order of the first two keys. State the rule to the stakeholder.
- *What if `row_id` is not available?* Then there is no repeatable answer for full ties; add a column or accept an arbitrary pick and say so.

**Common mistakes:**
- Sorting the text of `source`.
- Forgetting ELSE, so unknown sources get NULL and sort unpredictably across engines (NULL ordering differs by engine, see Q29).
- Putting the priority before the date when the rule says the date comes first.
- Relying on `drop_duplicates` after an unsorted frame.

### Q45 ⭐ 🔴 Top-N per group with explicit tie rules: employees(emp_id, name, dept_id, salary, hire_date). Return the top 2 per department by salary, with ties on salary broken by earlier hire_date, then lower emp_id, and also the variant 'top 2 salary levels with all tied employees' (DENSE_RANK). Show both, state what happens in a department with only one employee, and give the pandas versions. Discuss how you would explain the rule you chose to a stakeholder.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** "Top 2 per department" has two defensible meanings: exactly two people (ROW_NUMBER with a full tie-break: salary DESC, hire_date, emp_id) or the top two salary levels with everyone tied (DENSE_RANK <= 2); a department with one employee returns one row in both.

**Schema and sample data:** nine employees. Dept 10: Asha 90, then Ben, Chitra and Dev all at 80 (Ben hired 2019-05-01, Chitra and Dev both 2018-02-01), Esha 70. Dept 20: Farid and Gita both 60 hired on the same day, Hari 50. Dept 30: Ila alone. `salary` is declared NOT NULL here; the NULL case is a side check in the Code block.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER NOT NULL, hire_date TEXT);
INSERT INTO employees VALUES
 (1,'Asha',10,90,'2020-01-10'),(2,'Ben',10,80,'2019-05-01'),(3,'Chitra',10,80,'2018-02-01'),
 (4,'Dev',10,80,'2018-02-01'),(5,'Esha',10,70,'2021-07-01'),
 (6,'Farid',20,60,'2022-01-01'),(7,'Gita',20,60,'2022-01-01'),(8,'Hari',20,50,'2017-03-03'),
 (9,'Ila',30,75,'2023-04-04');
```

**SQL answer:** exactly two (`SQL_ROWNUM`) and the DENSE_RANK variant (`SQL_DENSE`).
```sql
WITH r AS (
  SELECT emp_id, name, dept_id, salary, hire_date,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, hire_date, emp_id) AS rn
  FROM employees
)
SELECT dept_id, rn, emp_id, name, salary, hire_date
FROM r
WHERE rn <= 2
ORDER BY dept_id, rn
```
```sql
WITH r AS (
  SELECT emp_id, name, dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS drk
  FROM employees
)
SELECT dept_id, drk, emp_id, name, salary
FROM r
WHERE drk <= 2
ORDER BY dept_id, drk, emp_id
```

**pandas answer:** sort by the same keys and take `groupby().head(2)`; the dense variant is a groupby rank with `method='dense'`.
```python
ordered = emp.sort_values(["dept_id", "salary", "hire_date", "emp_id"], ascending=[True, False, True, True])
pd_a = ordered.groupby("dept_id").head(2)
dense = emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
pd_b = emp[dense <= 2].assign(drk=dense)
```

**Example:**
- Dept 10, exactly two: Asha (90) is first. Among the three at 80 the earliest hire date wins, and Chitra and Dev tie on 2018-02-01, so emp_id decides: Chitra (3). Result Asha, Chitra. Ben (hired later) and Dev (higher id) are cut.
- Dept 10, DENSE_RANK <= 2: levels 90 and 80, so Asha plus all three at 80: four rows.
- Dept 20: Farid and Gita tie fully on salary and hire date, so emp_id puts Farid first and both are the top two, with Hari (50) cut. DENSE_RANK keeps Farid, Gita (level 1) and Hari (level 2): three rows.
- Dept 30: one employee, one row in both variants (no padding to two).

**Code:** run with `python3 -I`.
```python
# Q45: top 2 per department with explicit tie rules, and the DENSE_RANK variant
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER NOT NULL, hire_date TEXT);
INSERT INTO employees VALUES
 (1,'Asha',10,90,'2020-01-10'),(2,'Ben',10,80,'2019-05-01'),(3,'Chitra',10,80,'2018-02-01'),
 (4,'Dev',10,80,'2018-02-01'),(5,'Esha',10,70,'2021-07-01'),
 (6,'Farid',20,60,'2022-01-01'),(7,'Gita',20,60,'2022-01-01'),(8,'Hari',20,50,'2017-03-03'),
 (9,'Ila',30,75,'2023-04-04');
"""
SQL_ROWNUM = """
WITH r AS (
  SELECT emp_id, name, dept_id, salary, hire_date,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, hire_date, emp_id) AS rn
  FROM employees
)
SELECT dept_id, rn, emp_id, name, salary, hire_date
FROM r
WHERE rn <= 2
ORDER BY dept_id, rn
"""
SQL_DENSE = """
WITH r AS (
  SELECT emp_id, name, dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS drk
  FROM employees
)
SELECT dept_id, drk, emp_id, name, salary
FROM r
WHERE drk <= 2
ORDER BY dept_id, drk, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_ROWNUM, con)
b = pd.read_sql_query(SQL_DENSE, con)
print("exactly 2 per department (salary DESC, hire_date, emp_id):"); print(a.to_string(index=False))
print("\ntop 2 salary levels, all tied employees (DENSE_RANK <= 2):"); print(b.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
ordered = emp.sort_values(["dept_id", "salary", "hire_date", "emp_id"], ascending=[True, False, True, True])
pd_a = ordered.groupby("dept_id").head(2)
dense = emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
pd_b = emp[dense <= 2].assign(drk=dense)
# pd:end
pd_a = pd_a.assign(rn=pd_a.groupby("dept_id").cumcount() + 1)
pd.testing.assert_frame_equal(a[["dept_id", "rn", "emp_id"]],
    pd_a[["dept_id", "rn", "emp_id"]].reset_index(drop=True), check_dtype=False)
pd_b = pd_b.sort_values(["dept_id", "drk", "emp_id"]).reset_index(drop=True)
assert b["emp_id"].tolist() == pd_b["emp_id"].tolist() and b["drk"].tolist() == pd_b["drk"].astype(int).tolist()
print("\nrows per department, ROW_NUMBER variant:", a.groupby("dept_id").size().to_dict())
print("rows per department, DENSE_RANK variant:", b.groupby("dept_id").size().to_dict())

# side check: a NULL salary (the table above forbids it; a nullable column behaves differently)
con.executescript("CREATE TABLE emp2(emp_id INTEGER, dept_id INTEGER, salary INTEGER); INSERT INTO emp2 VALUES (1,10,80),(2,10,NULL),(3,10,NULL);")
n_rows = con.execute("""SELECT COUNT(*) FROM (SELECT ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) rn FROM emp2) WHERE rn <= 2""").fetchone()[0]
n_dense = con.execute("""SELECT COUNT(*) FROM (SELECT DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) r FROM emp2) WHERE r <= 2""").fetchone()[0]
e2 = pd.read_sql_query("SELECT * FROM emp2", con)
p_dense = int((e2.groupby("dept_id")["salary"].rank(method="dense", ascending=False) <= 2).sum())
print("\nNULL salary side check (one real salary, two NULLs): SQL ROW_NUMBER <= 2 keeps", n_rows,
      "| SQL DENSE_RANK <= 2 keeps", n_dense, "| pandas dense rank <= 2 keeps", p_dense)
print("asserts passed")
```

**Output (my run):**
```text
exactly 2 per department (salary DESC, hire_date, emp_id):
 dept_id  rn  emp_id   name  salary  hire_date
      10   1       1   Asha      90 2020-01-10
      10   2       3 Chitra      80 2018-02-01
      20   1       6  Farid      60 2022-01-01
      20   2       7   Gita      60 2022-01-01
      30   1       9    Ila      75 2023-04-04

top 2 salary levels, all tied employees (DENSE_RANK <= 2):
 dept_id  drk  emp_id   name  salary
      10    1       1   Asha      90
      10    2       2    Ben      80
      10    2       3 Chitra      80
      10    2       4    Dev      80
      20    1       6  Farid      60
      20    1       7   Gita      60
      20    2       8   Hari      50
      30    1       9    Ila      75

rows per department, ROW_NUMBER variant: {10: 2, 20: 2, 30: 1}
rows per department, DENSE_RANK variant: {10: 4, 20: 3, 30: 1}

NULL salary side check (one real salary, two NULLs): SQL ROW_NUMBER <= 2 keeps 2 | SQL DENSE_RANK <= 2 keeps 3 | pandas dense rank <= 2 keeps 1
asserts passed
```

**Edge cases:**
- Single-employee department: one row; ROW_NUMBER never invents rows.
- Row counts differ: 2 / 2 / 1 for the ROW_NUMBER variant versus 4 / 3 / 1 for DENSE_RANK in my run, so the DENSE_RANK result is not "top 2 people".
- NULL salary (not in the table above because of NOT NULL): in my side check (one real salary, two NULLs in one department) SQLite ROW_NUMBER <= 2 kept 2 rows (the NULL rows rank after the real one in DESC order), DENSE_RANK <= 2 kept 3, and pandas dense rank <= 2 kept 1, because pandas leaves NaN unranked. If the column is nullable, decide whether NULL salaries should be excluded and filter them out in both versions.
- Hire date as ISO text sorts correctly; a different text format would not.

**Then explain:**
- **ROW_NUMBER variant:** a precise, repeatable rule; the cost is that two people with the same salary can be treated differently because of hire date. That is only fair if the business agrees the hire date matters.
- **DENSE_RANK variant:** treats equal salary as equal, but the number of people returned varies.
- **Stakeholder wording:** "Two people per department; if salaries are equal, the earlier hire wins, then the lower employee id. If you would rather include everyone who ties, I can return the top two salary levels, which may give more than two people." Show the Dept 10 example, where it is 2 versus 4 rows.
- **pandas:** `head(2)` after a full sort is the ROW_NUMBER variant; `rank(method='dense')` is DENSE_RANK; both asserted equal to SQL.

**Follow-ups:**
- *Why not RANK <= 2?* It includes ties at the cutoff like DENSE_RANK but also leaves gaps after ties; worked by hand, not run: for dept 10 it returns Asha plus the three at 80 (ranks 1 and 2), the same four rows, but for dept 20 Farid and Gita are both rank 1 and Hari is rank 3, so RANK <= 2 drops Hari while DENSE_RANK keeps him.
- *Different tie rule?* Change the ORDER BY list; keep a unique column last.
- *How do I show the rank?* Select `rn` or `drk` as in the output.

**Common mistakes:**
- Not including a unique last tie-break column.
- Assuming "top 2" means two rows when the requirement was "top 2 salaries".
- Forgetting `ascending=[...]` with mixed directions in pandas.
- Leaving NULL salaries unhandled when the column allows them.

### Q46 ⭐ 🔴 Second highest salary per department including departments with a single distinct salary (returned as NULL), with windows: employees(emp_id, name, dept_id, salary) and departments(dept_id, dept_name). Use DENSE_RANK in a CTE, a LEFT JOIN from departments so a department with one distinct salary or no employees still appears with NULL, and aggregate with MAX(CASE WHEN rnk = 2 THEN salary END). Run it, compare with the Part 3 correlated-subquery version, and give the pandas groupby with unique and nlargest approach.
**Asked at:** public LeetCode-style problem bank (176 Second Highest Salary, 177 Nth Highest Salary, 184 Department Highest Salary, 185 Department Top Three Salaries; known only from third-party list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Rank distinct salaries with DENSE_RANK per department in a CTE, LEFT JOIN from `departments` so every department stays, and take `MAX(CASE WHEN rnk = 2 THEN salary END)`, which is NULL when there is no second distinct salary or no employee at all.

**Schema and sample data:** four departments. Eng (10) has salaries 100, 100, 80, 60 (top tied, so the second distinct is 80). Ops (20) has 70, 70 (one distinct salary). Legal (30) has no employees. Sales (40) has 90, 50 and one NULL salary.
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (10,'Eng'),(20,'Ops'),(30,'Legal'),(40,'Sales');
INSERT INTO employees VALUES
 (1,'Asha',10,100),(2,'Ben',10,100),(3,'Chitra',10,80),(4,'Dev',10,60),
 (5,'Esha',20,70),(6,'Farid',20,70),
 (7,'Gita',40,90),(8,'Hari',40,50),(9,'Ila',40,NULL);
```

**SQL answer:** window version `SQL_MAIN`, correlated-subquery version `SQL_CORRELATED`. A note on the premise: Part 3 does not contain a per-department version; its Q15 is the whole-company Nth highest and the answer there says the per-department form needs `AND e2.dept_id = e1.dept_id`. The version below is my own per-department correlated form (second highest = the maximum below the maximum).
```sql
WITH r AS (
  SELECT dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT d.dept_id, d.dept_name,
       MAX(CASE WHEN r.rnk = 2 THEN r.salary END) AS second_highest
FROM departments d
LEFT JOIN r ON r.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_id
```
```sql
SELECT d.dept_id, d.dept_name,
       (SELECT MAX(e.salary) FROM employees e
         WHERE e.dept_id = d.dept_id
           AND e.salary < (SELECT MAX(x.salary) FROM employees x WHERE x.dept_id = d.dept_id)) AS second_highest
FROM departments d
ORDER BY d.dept_id
```

**pandas answer:** per group, take the distinct non-NaN values sorted descending and pick the second if it exists; then map onto the departments table so empty departments appear as NaN.
```python
def second(s):
    u = np.sort(s.dropna().unique())[::-1]
    return u[1] if len(u) > 1 else np.nan
sec = emp.groupby("dept_id")["salary"].agg(second)
pd_df = dep.assign(second_highest=dep["dept_id"].map(sec)).sort_values("dept_id").reset_index(drop=True)
```

**Example:**
- Eng: distinct salaries 100, 80, 60, ranks 1, 2, 3, so the second is 80 (the tied 100s are one level).
- Ops: one distinct salary (70), no rank 2, so the CASE finds nothing and MAX of nothing is NULL.
- Legal: the LEFT JOIN keeps the department with no matching rows; MAX over a NULL-only group is NULL.
- Sales: the NULL salary is filtered in the CTE; distinct salaries 90 and 50, so the second is 50.

**Code:** run with `python3 -I`.
```python
# Q46: second highest distinct salary per department, NULL when it does not exist
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (10,'Eng'),(20,'Ops'),(30,'Legal'),(40,'Sales');
INSERT INTO employees VALUES
 (1,'Asha',10,100),(2,'Ben',10,100),(3,'Chitra',10,80),(4,'Dev',10,60),
 (5,'Esha',20,70),(6,'Farid',20,70),
 (7,'Gita',40,90),(8,'Hari',40,50),(9,'Ila',40,NULL);
"""
SQL_MAIN = """
WITH r AS (
  SELECT dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT d.dept_id, d.dept_name,
       MAX(CASE WHEN r.rnk = 2 THEN r.salary END) AS second_highest
FROM departments d
LEFT JOIN r ON r.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_id
"""
SQL_CORRELATED = """
SELECT d.dept_id, d.dept_name,
       (SELECT MAX(e.salary) FROM employees e
         WHERE e.dept_id = d.dept_id
           AND e.salary < (SELECT MAX(x.salary) FROM employees x WHERE x.dept_id = d.dept_id)) AS second_highest
FROM departments d
ORDER BY d.dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_CORRELATED, con)
print("window version:"); print(a.to_string(index=False, na_rep="NULL"))
pd.testing.assert_frame_equal(a, b)
print("\ncorrelated-subquery version is identical: True")

dep = pd.read_sql_query("SELECT * FROM departments", con)
emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def second(s):
    u = np.sort(s.dropna().unique())[::-1]
    return u[1] if len(u) > 1 else np.nan
sec = emp.groupby("dept_id")["salary"].agg(second)
pd_df = dep.assign(second_highest=dep["dept_id"].map(sec)).sort_values("dept_id").reset_index(drop=True)
# pd:end
pd.testing.assert_frame_equal(a, pd_df, check_dtype=False)
# the nlargest route: top 2 per group, then the smaller one only if two distinct values
nl = emp.dropna(subset=["salary"]).drop_duplicates(["dept_id", "salary"]).groupby("dept_id")["salary"].nlargest(2)
nl2 = nl.groupby(level=0).apply(lambda s: s.iloc[1] if len(s) == 2 else np.nan)
print("\nnlargest after drop_duplicates, second per dept:", nl2.to_dict())
print("without drop_duplicates, nlargest(2) would give dept 20 the value 70 (the top value twice):",
      emp.groupby("dept_id")["salary"].nlargest(2).loc[20].tolist())
print("asserts passed: window == correlated == pandas (dept 30 has no employees, dept 20 one distinct value: NaN/NULL)")
```

**Output (my run):**
```text
window version:
 dept_id dept_name  second_highest
      10       Eng            80.0
      20       Ops            NULL
      30     Legal            NULL
      40     Sales            50.0

correlated-subquery version is identical: True

nlargest after drop_duplicates, second per dept: {10: 80.0, 20: nan, 40: 50.0}
without drop_duplicates, nlargest(2) would give dept 20 the value 70 (the top value twice): [70.0, 70.0]
asserts passed: window == correlated == pandas (dept 30 has no employees, dept 20 one distinct value: NaN/NULL)
```

**Edge cases:**
- Why the filter `salary IS NOT NULL` in the CTE: in SQLite NULL sorts last in DESC order and would take a rank of its own; for a department with one real salary the NULL would become rank 2, and `MAX(CASE ... salary END)` would still return NULL, but for clarity and for other engines I remove NULL salaries first.
- `GROUP BY` after the LEFT JOIN with MAX is what turns "no rank 2" into a single NULL row instead of no row.
- Ties at the top (Eng) do not push the second level away, because DENSE_RANK counts values, not rows. RANK = 2 would find nothing for Eng.
- The two SQL versions and the pandas version agree on all four departments in the assert.
- pandas gives NaN (float) where SQL gives NULL.

**Then explain:**
- **DENSE_RANK:** ranks values, so rank 2 is the second distinct salary.
- **LEFT JOIN from departments:** an inner join, or aggregating only from `employees`, would silently drop Legal. Starting from the dimension table is how you keep empty groups.
- **Correlated version:** simpler to read for "second" only (max below the max), clumsy for third, fourth; it re-evaluates per department. I did not time it; on SQLite it matched the window result.
- **pandas:** `drop_duplicates(['dept_id','salary'])` before `nlargest(2)` is needed, otherwise the tied top value appears twice (run output: dept 20 gives 70 and 70).

**Follow-ups:**
- *Nth instead of second?* Replace 2 with N (in Python a parameter, as in Q6).
- *Return the employees who earn the second highest salary?* Filter `rnk = 2` in the CTE and join back, instead of aggregating.
- *What if a department should show 0 instead of NULL?* Wrap in COALESCE, but state that it changes the meaning.

**Common mistakes:**
- Using ROW_NUMBER or RANK and getting the tied top salary as "second".
- Starting from `employees` and losing departments with no (or one distinct) salary.
- Forgetting that `MAX` over zero matching CASE branches gives NULL, not 0.
- In pandas, `nlargest(2)` without removing duplicates.

### Q47 ⭐ 🔴 Users in the top 10 percent of activity within each country: events(event_id, user_id, event_time) and users(user_id, country). Count events per user, then within each country find users whose activity percentile is at or above the 90th using PERCENT_RANK or CUME_DIST over (PARTITION BY country ORDER BY n_events). Explain why NTILE(10) is a poor selector for small countries (one-user country is always bucket 1), how ties behave, and give the pandas groupby rank(pct=True) version, noting pandas pct differs from SQL PERCENT_RANK.
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Count events per user (LEFT JOIN so inactive users count as 0), then compute `CUME_DIST() OVER (PARTITION BY country ORDER BY n_events)` and keep rows with value >= 0.9 for "at or above the 90th percentile of the country"; PERCENT_RANK >= 0.9 is stricter and NTILE(10) is positional, so both behave badly on small or tied groups.

**Schema and sample data:** 16 users in three countries. Event counts per user (a loop in the Code block writes that many `events` rows): India (IN) users 1..10 have 50, 40, 40, 30, 20, 20, 10, 5, 3, 0 events (user 10 has none); US users 11..15 have 9, 4, 4, 1, 1; Singapore (SG) has one user (16) with 2.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
-- users 1..16 as above; events: one row per event (loop in the Code block)
```

**SQL answer:** one query shows PERCENT_RANK, CUME_DIST and NTILE(10) side by side with a 0/1 flag for each selection rule. The NTILE order has `user_id` as a tie-breaker so its output is repeatable.
```sql
WITH per_user AS (
  SELECT u.user_id, u.country, COUNT(e.event_id) AS n_events
  FROM users u
  LEFT JOIN events e ON e.user_id = u.user_id
  GROUP BY u.user_id, u.country
), scored AS (
  SELECT user_id, country, n_events,
         PERCENT_RANK() OVER (PARTITION BY country ORDER BY n_events) AS pr,
         CUME_DIST()    OVER (PARTITION BY country ORDER BY n_events) AS cd,
         NTILE(10)      OVER (PARTITION BY country ORDER BY n_events DESC, user_id) AS decile
  FROM per_user
)
SELECT country, user_id, n_events, ROUND(pr, 3) AS pr, ROUND(cd, 3) AS cd, decile,
       CASE WHEN pr >= 0.9 THEN 1 ELSE 0 END AS top_by_pr,
       CASE WHEN cd >= 0.9 THEN 1 ELSE 0 END AS top_by_cd
FROM scored
ORDER BY country, n_events DESC, user_id
```

**pandas answer:** merge, count, then rank within country. `method='max'` pct equals CUME_DIST; PERCENT_RANK is built from `method='min'`.
```python
n = (users.merge(events, on="user_id", how="left")
          .groupby(["user_id", "country"])["event_id"].count().rename("n_events").reset_index())
n["pct_max"] = n.groupby("country")["n_events"].rank(pct=True, method="max")      # equals CUME_DIST
n["pct_avg"] = n.groupby("country")["n_events"].rank(pct=True)                    # default 'average'
size = n.groupby("country")["n_events"].transform("size")
r_min = n.groupby("country")["n_events"].rank(method="min")
n["pr"] = ((r_min - 1) / (size - 1)).fillna(0.0)                                  # PERCENT_RANK; one-row group gives 0/0
top = n[n["pct_max"] >= 0.9]
```

**Example:**
- IN has 10 users. Ascending by events, user 1 (50) is last: CUME_DIST 10/10 = 1.0, PERCENT_RANK 9/9 = 1.0. Users 2 and 3 tie at 40 and occupy ranks 8 to 9: PERCENT_RANK (8 - 1) / 9 = 0.778 and CUME_DIST 9/10 = 0.9.
- So `CUME_DIST >= 0.9` selects users 1, 2, 3 (three users, 30 percent of a 10-user country) because the tie at 40 sits exactly on the cutoff. `PERCENT_RANK >= 0.9` selects only user 1.
- US has 5 users: user 11 (9 events) is 1.0 on both and is the only one selected. The two users with 4 events have CUME_DIST 0.8, not enough.
- SG has one user: CUME_DIST 1.0, PERCENT_RANK 0.0 (one-row partition), NTILE bucket 1. CUME_DIST and NTILE select that user; PERCENT_RANK does not.

**Code:** run with `python3 -I`.
```python
# Q47: users in the top 10 percent of activity within each country
import sqlite3
import numpy as np
import pandas as pd

# event counts per user are listed here so the data can be checked by hand; the loop writes one events row per event
COUNTS = {  # user_id: (country, events)
    1: ("IN", 50), 2: ("IN", 40), 3: ("IN", 40), 4: ("IN", 30), 5: ("IN", 20),
    6: ("IN", 20), 7: ("IN", 10), 8: ("IN", 5), 9: ("IN", 3), 10: ("IN", 0),
    11: ("US", 9), 12: ("US", 4), 13: ("US", 4), 14: ("US", 1), 15: ("US", 1),
    16: ("SG", 2),
}
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
""")
con.executemany("INSERT INTO users VALUES (?,?)", [(u, c) for u, (c, _) in COUNTS.items()])
ev, eid = [], 1
for u, (_, n) in COUNTS.items():
    for k in range(n):
        ev.append((eid, u, f"2026-01-{1 + k % 28:02d}")); eid += 1
con.executemany("INSERT INTO events VALUES (?,?,?)", ev)

SQL_MAIN = """
WITH per_user AS (
  SELECT u.user_id, u.country, COUNT(e.event_id) AS n_events
  FROM users u
  LEFT JOIN events e ON e.user_id = u.user_id
  GROUP BY u.user_id, u.country
), scored AS (
  SELECT user_id, country, n_events,
         PERCENT_RANK() OVER (PARTITION BY country ORDER BY n_events) AS pr,
         CUME_DIST()    OVER (PARTITION BY country ORDER BY n_events) AS cd,
         NTILE(10)      OVER (PARTITION BY country ORDER BY n_events DESC, user_id) AS decile
  FROM per_user
)
SELECT country, user_id, n_events, ROUND(pr, 3) AS pr, ROUND(cd, 3) AS cd, decile,
       CASE WHEN pr >= 0.9 THEN 1 ELSE 0 END AS top_by_pr,
       CASE WHEN cd >= 0.9 THEN 1 ELSE 0 END AS top_by_cd
FROM scored
ORDER BY country, n_events DESC, user_id
"""
sql = pd.read_sql_query(SQL_MAIN, con)
print(sql.to_string(index=False))
print("\nselected by PERCENT_RANK >= 0.9:", sql.loc[sql.top_by_pr == 1, "user_id"].tolist())
print("selected by CUME_DIST    >= 0.9:", sql.loc[sql.top_by_cd == 1, "user_id"].tolist())
print("NTILE(10) bucket 1         :", sql.loc[sql.decile == 1, "user_id"].tolist())

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
n = (users.merge(events, on="user_id", how="left")
          .groupby(["user_id", "country"])["event_id"].count().rename("n_events").reset_index())
n["pct_max"] = n.groupby("country")["n_events"].rank(pct=True, method="max")      # equals CUME_DIST
n["pct_avg"] = n.groupby("country")["n_events"].rank(pct=True)                    # default 'average'
size = n.groupby("country")["n_events"].transform("size")
r_min = n.groupby("country")["n_events"].rank(method="min")
n["pr"] = ((r_min - 1) / (size - 1)).fillna(0.0)                                  # PERCENT_RANK; one-row group gives 0/0
top = n[n["pct_max"] >= 0.9]
# pd:end
m = sql.merge(n, on=["user_id", "country"])
assert np.allclose(m["cd"], m["pct_max"].round(3))
assert np.allclose(m["pr_x"], m["pr_y"].round(3))
assert sorted(top["user_id"]) == sorted(sql.loc[sql.top_by_cd == 1, "user_id"])
print("\npandas rank(pct=True, method='max') >= 0.9 selects:", sorted(top["user_id"]), "(same as CUME_DIST)")
print("pandas default 'average' pct for the tied users 2,3 in IN:", n.loc[n.user_id.isin([2, 3]), "pct_avg"].round(3).tolist(),
      "vs method='max':", n.loc[n.user_id.isin([2, 3]), "pct_max"].round(3).tolist())
print("asserts passed")
```

**Output (my run):**
```text
country  user_id  n_events    pr  cd  decile  top_by_pr  top_by_cd
     IN        1        50 1.000 1.0       1          1          1
     IN        2        40 0.778 0.9       2          0          1
     IN        3        40 0.778 0.9       3          0          1
     IN        4        30 0.667 0.7       4          0          0
     IN        5        20 0.444 0.6       5          0          0
     IN        6        20 0.444 0.6       6          0          0
     IN        7        10 0.333 0.4       7          0          0
     IN        8         5 0.222 0.3       8          0          0
     IN        9         3 0.111 0.2       9          0          0
     IN       10         0 0.000 0.1      10          0          0
     SG       16         2 0.000 1.0       1          0          1
     US       11         9 1.000 1.0       1          1          1
     US       12         4 0.500 0.8       2          0          0
     US       13         4 0.500 0.8       3          0          0
     US       14         1 0.000 0.4       4          0          0
     US       15         1 0.000 0.4       5          0          0

selected by PERCENT_RANK >= 0.9: [1, 11]
selected by CUME_DIST    >= 0.9: [1, 2, 3, 16, 11]
NTILE(10) bucket 1         : [1, 16, 11]

pandas rank(pct=True, method='max') >= 0.9 selects: [1, 2, 3, 11, 16] (same as CUME_DIST)
pandas default 'average' pct for the tied users 2,3 in IN: [0.85, 0.85] vs method='max': [0.9, 0.9]
asserts passed
```

**Edge cases:**
- Small groups: NTILE(10) over a one-user country always gives bucket 1, so "bucket 1" means "everyone" there. With 5 users, NTILE(10) also makes five buckets of one, and user 11 alone is bucket 1 (output).
- Ties on the cutoff: CUME_DIST includes both tied users (2 and 3); NTILE(10) put users 2 and 3 in different buckets (2 and 3) even though both have 40 events, because it is positional.
- A single-user group: PERCENT_RANK is 0.0, so a PERCENT_RANK threshold excludes the only user; CUME_DIST includes them. Decide which you want.
- Zero-event users: included via LEFT JOIN with `COUNT(e.event_id)`; user 10 has 0. With an inner join they would vanish and change every percentile.
- pandas `rank(pct=True)` with default `average` ranks gives the tied pair 0.85 instead of 0.9 (output), so the threshold would drop them; with `method='max'` it matches CUME_DIST.

**Then explain:**
- **Which one to use:** CUME_DIST >= 0.9 reads as "at least as active as 90 percent of the country (including ties and yourself)". PERCENT_RANK >= 0.9 reads as "at least 90 percent of the others are strictly below you".
- **Why not NTILE(10):** it forces equal-sized buckets by position, ignores ties and cannot say "top 10 percent" when a group has fewer than ten users.
- **Whether a user is "top 10 percent" with n small:** no method can pick exactly 10 percent of 5 users; say so.
- **pandas:** `groupby('country')['n_events'].rank(pct=True, method='max') >= 0.9`; the code asserts the same users as CUME_DIST.

**Follow-ups:**
- *What if you need at most 10 percent?* Use PERCENT_RANK or a ROW_NUMBER cutoff, and say ties are cut arbitrarily or by a stated rule.
- *Minimum group size?* Exclude countries with fewer than, say, 10 users, and state the threshold.
- *Activity window?* Filter the events by date inside the first CTE.

**Common mistakes:**
- Using `NTILE(10) = 1` for small groups.
- Forgetting the LEFT JOIN so inactive users disappear.
- Mixing up pandas pct with SQL PERCENT_RANK.
- Not saying how ties at the cutoff are treated.

### Q48 ⭐ 🔴 Ranking after a join: a join fan-out silently changes ranks. orders(order_id, customer_id, amount) and order_items(item_id, order_id, product_id). A report ranks customers by SUM(amount) after joining orders to order_items, which repeats each order amount per item and inflates totals (and can change the rank order). Reproduce it, diagnose with COUNT(*) versus COUNT(DISTINCT order_id), and fix by aggregating to the right grain before ranking. Explain that RANK is computed on the wrong inputs, not wrongly, and give the pandas bug and fix.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Joining `orders` to `order_items` repeats each order's amount once per item, so `SUM(amount)` is inflated for customers whose orders have many items and the RANK computed on those totals is correct for the wrong numbers; diagnose with `COUNT(*)` versus `COUNT(DISTINCT order_id)` and rank after aggregating at the right grain.

**Schema and sample data:** five orders for four customers. Order 1 (customer 1, 100) has four items. Orders 2 and 3 (customer 2, 150 and 120) have one item each. Order 4 (customer 3, 200) has one item. Order 5 (customer 4, 50) has no items.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,2,150),(3,2,120),(4,3,200),(5,4,50);
INSERT INTO order_items VALUES
 (1,1,7),(2,1,8),(3,1,9),(4,1,10),
 (5,2,7),(6,3,8),(7,4,9);
```

**SQL answer:** the buggy ranking (`SQL_BUG`), the diagnostic (`SQL_DIAG`) and the fix (`SQL_FIX`), which does not need the items table at all because the question asks about order amounts.
```sql
SELECT o.customer_id, SUM(o.amount) AS total,
       RANK() OVER (ORDER BY SUM(o.amount) DESC) AS rnk
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY rnk, o.customer_id
```
```sql
SELECT o.customer_id, COUNT(*) AS joined_rows, COUNT(DISTINCT o.order_id) AS real_orders
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id
```
```sql
SELECT customer_id, SUM(amount) AS total,
       RANK() OVER (ORDER BY SUM(amount) DESC) AS rnk
FROM orders
GROUP BY customer_id
ORDER BY rnk, customer_id
```

**pandas answer:** the merge reproduces the fan-out; the fix aggregates the orders frame on its own (or collapses items to one row per order before merging if item columns are needed).
```python
joined = orders.merge(items, on="order_id")                                   # one row per item: the fan-out
bug_pd = joined.groupby("customer_id")["amount"].sum().rename("total").reset_index()
bug_pd["rnk"] = bug_pd["total"].rank(method="min", ascending=False).astype(int)
fix_pd = orders.groupby("customer_id")["amount"].sum().rename("total").reset_index()
fix_pd["rnk"] = fix_pd["total"].rank(method="min", ascending=False).astype(int)
```

**Example:**
- True totals from `orders` alone: customer 2 is 150 + 120 = 270, customer 3 is 200, customer 1 is 100, customer 4 is 50. True order: 2, 3, 1, 4.
- After the join, order 1 appears four times (once per item), so customer 1's total becomes 4 x 100 = 400 and jumps from last-but-one to first. Customer 2 stays 270 (one item per order).
- The buggy ranks: 1 (400), 2 (270), 3 (200). Customer 4 has no items, so the inner join removes it completely.
- Diagnostic: customer 1 shows 4 joined rows but 1 real order; that mismatch is the signature of the fan-out.

**Code:** run with `python3 -I`.
```python
# Q48: ranking after a join fan-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,2,150),(3,2,120),(4,3,200),(5,4,50);
INSERT INTO order_items VALUES
 (1,1,7),(2,1,8),(3,1,9),(4,1,10),      -- order 1 has 4 items
 (5,2,7),(6,3,8),(7,4,9);               -- orders 2, 3, 4 have 1 item; order 5 has none
"""
SQL_BUG = """
SELECT o.customer_id, SUM(o.amount) AS total,
       RANK() OVER (ORDER BY SUM(o.amount) DESC) AS rnk
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY rnk, o.customer_id
"""
SQL_DIAG = """
SELECT o.customer_id, COUNT(*) AS joined_rows, COUNT(DISTINCT o.order_id) AS real_orders
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id
"""
SQL_FIX = """
SELECT customer_id, SUM(amount) AS total,
       RANK() OVER (ORDER BY SUM(amount) DESC) AS rnk
FROM orders
GROUP BY customer_id
ORDER BY rnk, customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
bug, diag, fix = q(SQL_BUG), q(SQL_DIAG), q(SQL_FIX)
print("buggy (join first, then rank):"); print(bug.to_string(index=False))
print("\ndiagnosis, COUNT(*) vs COUNT(DISTINCT order_id):"); print(diag.to_string(index=False))
print("\nfixed (aggregate at order grain, then rank):"); print(fix.to_string(index=False))
assert bug["customer_id"].tolist() != fix["customer_id"].tolist()

orders = q("SELECT * FROM orders"); items = q("SELECT * FROM order_items")
# pd:main
joined = orders.merge(items, on="order_id")                                   # one row per item: the fan-out
bug_pd = joined.groupby("customer_id")["amount"].sum().rename("total").reset_index()
bug_pd["rnk"] = bug_pd["total"].rank(method="min", ascending=False).astype(int)
fix_pd = orders.groupby("customer_id")["amount"].sum().rename("total").reset_index()
fix_pd["rnk"] = fix_pd["total"].rank(method="min", ascending=False).astype(int)
# pd:end
pd.testing.assert_frame_equal(bug, bug_pd.sort_values(["rnk", "customer_id"]).reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(fix, fix_pd.sort_values(["rnk", "customer_id"]).reset_index(drop=True), check_dtype=False)
print("\ncustomer 4 (order 5 has no items) is missing from the buggy result:", 4 not in bug["customer_id"].tolist())
print("pandas: merged rows", len(joined), "vs orders", len(orders), "| order_id duplicated after merge:", int(joined["order_id"].duplicated().sum()))
# a second safe fix: collapse items to one row per order first
items_per_order = items.groupby("order_id").size().rename("n_items").reset_index()
safe = orders.merge(items_per_order, on="order_id", how="left")
assert len(safe) == len(orders)
assert safe.groupby("customer_id")["amount"].sum().equals(fix_pd.set_index("customer_id")["total"])
print("asserts passed: SQL bug == pandas bug; SQL fix == pandas fix; the two rankings differ")
```

**Output (my run):**
```text
buggy (join first, then rank):
 customer_id  total  rnk
           1    400    1
           2    270    2
           3    200    3

diagnosis, COUNT(*) vs COUNT(DISTINCT order_id):
 customer_id  joined_rows  real_orders
           1            4            1
           2            2            2
           3            1            1

fixed (aggregate at order grain, then rank):
 customer_id  total  rnk
           2    270    1
           3    200    2
           1    100    3
           4     50    4

customer 4 (order 5 has no items) is missing from the buggy result: True
pandas: merged rows 7 vs orders 5 | order_id duplicated after merge: 3
asserts passed: SQL bug == pandas bug; SQL fix == pandas fix; the two rankings differ
```

**Edge cases:**
- Rank order changed, not only the totals: customer 1 went from third to first in my run.
- Inner join also drops customers whose orders have no items (customer 4 disappears from the buggy result). A LEFT JOIN would keep the row but would not cure the inflation.
- `COUNT(DISTINCT order_id)` fixes a count of orders but not a SUM, because the repeated amount is still added several times.
- If you need item-level information as well, aggregate items to one row per order first (a CTE with `GROUP BY order_id`), then join; the Code block checks that this keeps one row per order.

**Then explain:**
- **RANK is not wrong:** it ranks whatever rows it is given. The bug is the grain of the inputs, which is why checking `COUNT(*)` against `COUNT(DISTINCT key)` right after a join is a good habit.
- **Fix:** choose the grain first (one row per order), aggregate to the grain you rank on (one row per customer), then rank. The window sits last.
- **Same bug in pandas:** `merge` also multiplies rows (7 merged rows from 5 orders, 3 duplicated order ids in the output); `groupby.sum` then adds them.
- **Sanity check to propose:** compare the report total with the plain `SUM(amount)` on `orders`; they should match.

**Follow-ups:**
- *Related trap?* Joining two child tables to one parent (see Part 2 on the chasm trap).
- *How do I test a CTE in isolation?* Select from it and compare row count and distinct keys.
- *Why not `SUM(DISTINCT amount)`?* It would collapse two different orders with the same amount.

**Common mistakes:**
- Using `SUM(DISTINCT amount)` as the fix.
- Adding more joins to a report without re-checking the grain.
- Believing a plausible-looking ranking proves the totals are right.
- Joining `order_items` just to filter and forgetting it multiplies rows (use EXISTS for filtering).

### Q49 ⭐ 🔴 Revenue by decile (Pareto-style) with NTILE: orders(order_id, customer_id, amount). Compute customer totals, bucket customers into deciles with NTILE(10) over total descending, and report per decile the number of customers, total revenue, and share of overall revenue, showing that the top decile holds a large share on skewed data. Explain NTILE unevenness with few customers, ties across a bucket boundary, and give the pandas qcut or rank-based version, stating where it differs from NTILE.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Total spend per customer, `NTILE(10) OVER (ORDER BY total DESC, customer_id)` to cut the customers into ten positional buckets, then per bucket count customers, sum revenue and divide by the grand total; on skewed data decile 1 holds a large share (about half in my sample).

**Schema and sample data:** 23 customers with totals 1000, 700, 500, 400, 300, 250, 200, 150, 120, 120, 100, 90, 80, 70, 60, 55, 50, 45, 40, 35, 30, 25, 20 (customer ids 1 to 23 in that order). Each customer has two orders that add up to the total (a loop in the Code block writes them). Customers 9 and 10 tie at 120 and sit across a bucket boundary.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
-- two orders per customer, amounts t // 2 and t - t // 2 for each total t (loop in the Code block)
```

**SQL answer:** the decile table (`SQL_MAIN`) and the per-customer assignment (`SQL_ASSIGN`), used to check the pandas version.
```sql
WITH t AS (
  SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
), b AS (
  SELECT customer_id, total,
         NTILE(10) OVER (ORDER BY total DESC, customer_id) AS decile
  FROM t
)
SELECT decile, COUNT(*) AS customers, SUM(total) AS revenue,
       ROUND(100.0 * SUM(total) / (SELECT SUM(total) FROM t), 1) AS share_pct
FROM b
GROUP BY decile
ORDER BY decile
```
```sql
SELECT customer_id, SUM(amount) AS total,
       NTILE(10) OVER (ORDER BY SUM(amount) DESC, customer_id) AS decile
FROM orders GROUP BY customer_id ORDER BY customer_id
```

**pandas answer:** reproduce NTILE exactly with arithmetic on the sorted position (first `n mod 10` buckets get one extra row), then group. `pd.qcut` is shown in the Code block and compared.
```python
tot = orders.groupby("customer_id", as_index=False)["amount"].sum().rename(columns={"amount": "total"})
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
n, k = len(tot), 10
q, r = divmod(n, k)                                   # first r buckets get q + 1 rows (NTILE rule)
pos = pd.Series(range(n))
tot["ntile"] = (pos // (q + 1) + 1).where(pos < r * (q + 1), r + (pos - r * (q + 1)) // q + 1).astype(int)
by = tot.groupby("ntile")["total"].agg(customers="size", revenue="sum").reset_index()
by["share_pct"] = (100.0 * by["revenue"] / tot["total"].sum()).round(1)
```

**Example:**
- 23 customers into 10 buckets: 23 = 10 x 2 + 3, so the first three buckets get 3 customers and the rest 2. Sizes: 3, 3, 3, 2, 2, 2, 2, 2, 2, 2.
- Decile 1 is customers 1 to 3: 1000 + 700 + 500 = 2200 of 4440 total, 49.5 percent.
- Decile 2 is customers 4 to 6: 400 + 300 + 250 = 950, 21.4 percent. Decile 10 holds 20 + 25 = 45, 1.0 percent.
- Customers 9 and 10 both have 120. Customer 9 is the last row of bucket 3 and customer 10 the first row of bucket 4: NTILE separated two equal customers, and only the `customer_id` tie-break decided which one landed in the higher bucket.

**Code:** run with `python3 -I`.
```python
# Q49: revenue by decile with NTILE(10)
import sqlite3
import pandas as pd

# 23 customers (ids 1..23); each has two orders that add up to the total listed
TOTALS = [1000, 700, 500, 400, 300, 250, 200, 150, 120, 120, 100, 90, 80, 70, 60, 55, 50, 45, 40, 35, 30, 25, 20]
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
""")
rows, oid = [], 1
for cid, t in enumerate(TOTALS, start=1):
    a = t // 2
    rows += [(oid, cid, a), (oid + 1, cid, t - a)]; oid += 2
con.executemany("INSERT INTO orders VALUES (?,?,?)", rows)

SQL_MAIN = """
WITH t AS (
  SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
), b AS (
  SELECT customer_id, total,
         NTILE(10) OVER (ORDER BY total DESC, customer_id) AS decile
  FROM t
)
SELECT decile, COUNT(*) AS customers, SUM(total) AS revenue,
       ROUND(100.0 * SUM(total) / (SELECT SUM(total) FROM t), 1) AS share_pct
FROM b
GROUP BY decile
ORDER BY decile
"""
SQL_ASSIGN = """
SELECT customer_id, SUM(amount) AS total,
       NTILE(10) OVER (ORDER BY SUM(amount) DESC, customer_id) AS decile
FROM orders GROUP BY customer_id ORDER BY customer_id
"""
sql = pd.read_sql_query(SQL_MAIN, con)
assign = pd.read_sql_query(SQL_ASSIGN, con)
print(sql.to_string(index=False))
print("customers per decile:", sql["customers"].tolist(), "| total revenue:", int(sql["revenue"].sum()))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
tot = orders.groupby("customer_id", as_index=False)["amount"].sum().rename(columns={"amount": "total"})
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
n, k = len(tot), 10
q, r = divmod(n, k)                                   # first r buckets get q + 1 rows (NTILE rule)
pos = pd.Series(range(n))
tot["ntile"] = (pos // (q + 1) + 1).where(pos < r * (q + 1), r + (pos - r * (q + 1)) // q + 1).astype(int)
by = tot.groupby("ntile")["total"].agg(customers="size", revenue="sum").reset_index()
by["share_pct"] = (100.0 * by["revenue"] / tot["total"].sum()).round(1)
# pd:end
tot_sorted = tot.sort_values("customer_id").reset_index(drop=True)
assert assign["decile"].tolist() == tot_sorted["ntile"].tolist()
assert sql["customers"].tolist() == by["customers"].tolist() and sql["share_pct"].tolist() == by["share_pct"].tolist()
print("\npandas floor arithmetic reproduces NTILE exactly (same decile for all", n, "customers)")

# qcut comparisons
by_value = pd.qcut(tot["total"], 10, labels=False, duplicates="drop")        # 0 = lowest total
by_rank = pd.qcut(tot["total"].rank(method="first", ascending=False), 10, labels=False)  # 0 = top rank
tot["qcut_value"] = 10 - by_value
tot["qcut_rank"] = by_rank + 1
print("\nqcut on total (ties stay together):    sizes", tot["qcut_value"].value_counts().sort_index().tolist())
print("qcut on rank(method='first'):           sizes", tot["qcut_rank"].value_counts().sort_index().tolist())
print("NTILE sizes                           :", sql["customers"].tolist())
print("customers whose qcut-on-rank decile differs from NTILE:", int((tot["qcut_rank"] != tot["ntile"]).sum()))
print("customers whose qcut-on-total decile differs from NTILE:", int((tot["qcut_value"] != tot["ntile"]).sum()))
split = tot[tot["total"] == 120][["customer_id", "total", "ntile", "qcut_value"]]
print("\nthe tied pair (total 120):"); print(split.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
 decile  customers  revenue  share_pct
      1          3     2200       49.5
      2          3      950       21.4
      3          3      470       10.6
      4          2      220        5.0
      5          2      170        3.8
      6          2      130        2.9
      7          2      105        2.4
      8          2       85        1.9
      9          2       65        1.5
     10          2       45        1.0
customers per decile: [3, 3, 3, 2, 2, 2, 2, 2, 2, 2] | total revenue: 4440

pandas floor arithmetic reproduces NTILE exactly (same decile for all 23 customers)

qcut on total (ties stay together):    sizes [3, 2, 2, 1, 3, 3, 2, 2, 2, 3]
qcut on rank(method='first'):           sizes [3, 2, 2, 2, 3, 2, 2, 2, 2, 3]
NTILE sizes                           : [3, 3, 3, 2, 2, 2, 2, 2, 2, 2]
customers whose qcut-on-rank decile differs from NTILE: 10
customers whose qcut-on-total decile differs from NTILE: 11

the tied pair (total 120):
 customer_id  total  ntile  qcut_value
           9    120      3           5
          10    120      4           5
asserts passed
```

**Edge cases:**
- Uneven sizes: with 23 customers the buckets are 3,3,3,2,... NTILE gives the larger buckets to the first (highest-spending) deciles, so the top deciles have slightly more customers and revenue shares are not strictly comparable across deciles.
- Few customers: with fewer than 10 customers I expect NTILE(10) to give each customer a bucket of their own, numbered 1 to n, leaving the higher deciles empty. I did not run that case.
- Ties across a boundary: customers 9 and 10 are in deciles 3 and 4 in SQL and in the same decile under `qcut` on the totals (output: `qcut_value` 5 for both).
- `qcut` versus NTILE: in my run, `qcut` on the totals produced bucket sizes 3, 2, 2, 1, 3, 3, 2, 2, 2, 3 and `qcut` on `rank(method='first')` produced 3, 2, 2, 2, 3, 2, 2, 2, 2, 3. Neither matches NTILE's 3, 3, 3, 2, ..., and 11 of the 23 customers (qcut on totals) or 10 of 23 (qcut on rank) land in a different decile than under NTILE. `qcut` cuts at interpolated quantile values; NTILE counts positions.
- `duplicates='drop'` can reduce the number of buckets when many totals are equal; I used it on the totals as a guard, and no bin was dropped here.

**Then explain:**
- **Pareto reading:** the top decile (3 customers) holds 49.5 percent of revenue and the top three deciles about 81.5 percent (2200 + 950 + 470 = 3620 of 4440), a skewed distribution. This is made-up data; real data would tell its own story.
- **NTILE:** positional, equal-count (to within one) buckets; it ignores ties, so equal customers can land in different deciles. Add a tie-breaker so the split is repeatable.
- **Direction:** NTILE over `total DESC` makes decile 1 the top spenders; over ASC it is the bottom.
- **pandas:** the floor arithmetic reproduces NTILE exactly (asserted); `qcut` is the idiomatic route but gives a different split.

**Follow-ups:**
- *What if customers with no orders should count?* Start from `customers` with a LEFT JOIN and `COALESCE(total, 0)`; they land in the bottom deciles.
- *Cumulative share by decile?* That is a running total, Part 5.
- *Why not 10 equal revenue buckets?* That is a different question (cut by cumulative revenue, not by customer count).

**Common mistakes:**
- Reporting decile shares without saying the buckets are equal in customers, not revenue.
- Forgetting the tie-breaker and getting different bucket members on each run.
- Using `qcut` and assuming it matches NTILE.
- Computing the overall share with a different base (for example orders instead of customers).

### Q50 ⭐ 🔴 Dialect map for ranking and top-N (hedge everything not run on SQLite 3.45): QUALIFY (BigQuery, Snowflake, DuckDB), PostgreSQL DISTINCT ON for one row per group, FETCH FIRST ... WITH TIES, PERCENTILE_CONT / PERCENTILE_DISC, NULLS FIRST / NULLS LAST support, window function support in MySQL 8.0 versus 5.7 (none), IGNORE NULLS on FIRST_VALUE / LAST_VALUE, and the ROW_NUMBER emulation in older engines. Present a table with a 'verified by running on SQLite' column and a 'hedged, not executed' column, and show the CTE emulation of QUALIFY that does run.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** On SQLite 3.45 I ran what exists (windows, CTE emulations of QUALIFY and DISTINCT ON, NULLS FIRST, a window-free rank) and ran the unsupported syntaxes to capture the errors; everything about PostgreSQL, MySQL, BigQuery, Snowflake, Oracle, DuckDB and SQL Server below is from memory and is labelled "not executed".

**Schema and sample data:** nine employees in three departments. Dept 10: Asha 90, Ben 80, Chitra 80, Dev 70. Dept 20: Esha 60, Farid NULL, Gita 50. Dept 30: Hari NULL, Ila NULL (only NULLs).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,80),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',20,60),(6,'Farid',20,NULL),(7,'Gita',20,50),(8,'Hari',30,NULL),(9,'Ila',30,NULL);
```

**SQL answer:** the CTE emulation of QUALIFY (`SQL_QUALIFY_EMU`), DISTINCT ON emulation (`SQL_DISTINCT_ON_EMU`), a rank with no window function (`SQL_NO_WINDOW_RANK`) compared with `SQL_WINDOW_RANK`, and NULLS FIRST with its portable emulation (`SQL_NULLS`, `SQL_NULLS_PORTABLE`).
```sql
WITH r AS (
  SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary, rk FROM r WHERE rk <= 2 ORDER BY dept_id, rk, emp_id
```
```sql
WITH r AS (
  SELECT emp_id, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary FROM r WHERE rn = 1 ORDER BY dept_id
```
```sql
SELECT e.emp_id, e.dept_id, e.salary,
       1 + (SELECT COUNT(*) FROM employees x WHERE x.dept_id = e.dept_id AND x.salary > e.salary) AS rk
FROM employees e
WHERE e.salary IS NOT NULL
ORDER BY e.dept_id, rk, e.emp_id
```
```sql
SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
FROM employees WHERE salary IS NOT NULL ORDER BY dept_id, rk, emp_id
```
```sql
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY salary DESC NULLS FIRST, emp_id
```
```sql
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY (salary IS NULL) DESC, salary DESC, emp_id
```

The dialect map. "Ran on SQLite 3.45.1" means I executed it here (or the error text in the output is from this run). Everything in the right column is from memory and not executed; check the vendor documentation for your version.

| Feature | Ran on SQLite 3.45.1 | Hedged, not executed |
|---|---|---|
| QUALIFY | Syntax error in the run (`near "ROW_NUMBER"`). The CTE emulation ran: `SQL_QUALIFY_EMU` | Exists in BigQuery, Snowflake, DuckDB (and Teradata, Databricks as far as I remember); not in PostgreSQL or MySQL |
| DISTINCT ON | Syntax error in the run (`near "ON"`). ROW_NUMBER = 1 emulation ran: `SQL_DISTINCT_ON_EMU` | PostgreSQL has `SELECT DISTINCT ON (dept_id) ... ORDER BY dept_id, salary DESC`; DuckDB I believe too |
| FETCH FIRST n ROWS WITH TIES | Syntax error in the run (`near "FETCH"`). Emulation: `RANK() <= n` over the whole set (same idea as Q26) | PostgreSQL 13+ and Oracle 12c+ support it; SQL Server has `TOP n WITH TIES`; MySQL has no equivalent |
| PERCENTILE_CONT / PERCENTILE_DISC | Syntax error in the run (`near "("`). Built from ROW_NUMBER/CUME_DIST in Q41 | PostgreSQL, Snowflake, Oracle use `... WITHIN GROUP (ORDER BY x)`; SQL Server and BigQuery have window-style forms; MySQL has none |
| NULLS FIRST / NULLS LAST | Ran: `SQL_NULLS` returned the NULL row first on 3.45.1. The portable `ORDER BY (col IS NULL) DESC, col` form gave the same rows | PostgreSQL and Oracle support the syntax; PostgreSQL treats NULL as larger than any value by default, MySQL as smaller and has no NULLS FIRST/LAST syntax; I did not run them |
| NULL order default in SQLite | Ran: NULLs come first in ASC, last in DESC (NULL acts as the smallest value) | See the row above |
| Window functions in MySQL | Not applicable | MySQL 8.0 added them; 5.7 and earlier have none (hence the user-variable or correlated-count tricks) |
| IGNORE NULLS on FIRST_VALUE / LAST_VALUE | Syntax error in the run (`near "NULLS"`). Emulation: filter NULLs in a CTE then take the first row | Oracle, BigQuery, Snowflake support `IGNORE NULLS`; PostgreSQL did not as far as I know; SQL Server added it in a recent version (I am unsure which) |
| ROW_NUMBER emulation with no windows | Ran: `SQL_NO_WINDOW_RANK` (1 + count of higher values in the group) equals RANK() | MySQL 5.7 era code often used session variables; not recommended, not executed |
| Named windows (`WINDOW w AS`) | Ran in this Code block; extending a named window in OVER (`OVER (w ORDER BY ...)`) works when `w` has no ORDER BY of its own, and fails with `cannot override ORDER BY clause of window: w` when it does | PostgreSQL and MySQL 8 support WINDOW clauses; the extension rules I did not execute |

**pandas answer:** the pandas side of the same features: QUALIFY is a mask on a groupby rank, DISTINCT ON is sort plus `drop_duplicates`, NULLS FIRST is `na_position`, and `groupby().first()` skips NaN, which is `FIRST_VALUE ... IGNORE NULLS`.
```python
clean = emp.dropna(subset=["salary"])
pd_qualify = clean.assign(rk=clean.groupby("dept_id")["salary"].rank(method="min", ascending=False))
pd_qualify = pd_qualify[pd_qualify["rk"] <= 2]                                      # QUALIFY
pd_distinct_on = (clean.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
                       .drop_duplicates("dept_id"))                                 # DISTINCT ON
pd_nulls_first = emp[emp["dept_id"] == 20].sort_values(["salary", "emp_id"], ascending=[False, True], na_position="first")
first_nonnull = emp.groupby("dept_id")["salary"].first()                            # FIRST_VALUE ... IGNORE NULLS
```

**Example:** dept 10: RANK by salary DESC gives Asha 1, Ben 2, Chitra 2, Dev 4, so `rk <= 2` keeps three rows (the tie at 2). Dept 20: after dropping the NULL, Esha 1 and Gita 2. Dept 30: only NULL salaries, filtered out, so the department disappears from the result. DISTINCT ON emulation: Asha for 10 (ROW_NUMBER with emp_id tie-break) and Esha for 20.
- The NULLS FIRST query on dept 20 returns emp 6 (Farid, NULL) first, then Esha 60 and Gita 50.
- First non-NULL salary per department by emp_id: 90 for dept 10, 60 for dept 20 (Farid's NULL skipped), and nothing for dept 30.

**Code:** run with `python3 -I`.
```python
# Q50: dialect map for ranking and top-N: what runs on SQLite 3.45, what is hedged
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,80),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',20,60),(6,'Farid',20,NULL),(7,'Gita',20,50),(8,'Hari',30,NULL),(9,'Ila',30,NULL);
"""
# the QUALIFY emulation that runs: CTE (or subquery) + WHERE on the window column
SQL_QUALIFY_EMU = """
WITH r AS (
  SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary, rk FROM r WHERE rk <= 2 ORDER BY dept_id, rk, emp_id
"""
# DISTINCT ON (dept_id) emulation: ROW_NUMBER = 1 with a tie-breaker
SQL_DISTINCT_ON_EMU = """
WITH r AS (
  SELECT emp_id, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary FROM r WHERE rn = 1 ORDER BY dept_id
"""
# no windows at all (MySQL 5.7 era): rank = 1 + number of rows in the same group with a higher value
SQL_NO_WINDOW_RANK = """
SELECT e.emp_id, e.dept_id, e.salary,
       1 + (SELECT COUNT(*) FROM employees x WHERE x.dept_id = e.dept_id AND x.salary > e.salary) AS rk
FROM employees e
WHERE e.salary IS NOT NULL
ORDER BY e.dept_id, rk, e.emp_id
"""
SQL_WINDOW_RANK = """
SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
FROM employees WHERE salary IS NOT NULL ORDER BY dept_id, rk, emp_id
"""
SQL_NULLS = """
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY salary DESC NULLS FIRST, emp_id
"""
SQL_NULLS_PORTABLE = """
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY (salary IS NULL) DESC, salary DESC, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
print("SQLite", sqlite3.sqlite_version)

qe, de, nw, wr = q(SQL_QUALIFY_EMU), q(SQL_DISTINCT_ON_EMU), q(SQL_NO_WINDOW_RANK), q(SQL_WINDOW_RANK)
print("\nQUALIFY emulation (RANK <= 2 per department, NULL salaries removed):"); print(qe.to_string(index=False))
print("\nDISTINCT ON emulation (one row per department):"); print(de.to_string(index=False))
assert nw.equals(wr)
print("\nrank without any window function (correlated COUNT) equals RANK(): True")
nf = q(SQL_NULLS); npt = q(SQL_NULLS_PORTABLE)
print("\nNULLS FIRST on SQLite 3.45 (dept 20):", nf["emp_id"].tolist(), "| portable IS NULL emulation gives the same:", nf.equals(npt))
assert nf.equals(npt)
print("default SQLite order, ASC puts NULLs first:",
      [r[0] for r in con.execute("SELECT salary FROM employees WHERE dept_id=20 ORDER BY salary")])

print("\nsyntax tried on SQLite 3.45 that is NOT supported (error text from the run):")
tries = {
 "QUALIFY": "SELECT emp_id FROM employees QUALIFY ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary) = 1",
 "DISTINCT ON": "SELECT DISTINCT ON (dept_id) emp_id FROM employees ORDER BY dept_id, salary DESC",
 "FETCH FIRST WITH TIES": "SELECT emp_id FROM employees ORDER BY salary DESC FETCH FIRST 2 ROWS WITH TIES",
 "PERCENTILE_CONT": "SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) FROM employees",
 "IGNORE NULLS": "SELECT FIRST_VALUE(salary) IGNORE NULLS OVER (PARTITION BY dept_id ORDER BY emp_id) FROM employees",
}
for name, sql in tries.items():
    try:
        con.execute(sql).fetchall(); print(f"  {name}: RAN (unexpected)")
    except sqlite3.Error as e:
        print(f"  {name}: {type(e).__name__}: {e}")

print("\nnamed window extension on SQLite 3.45.1:")
ok = con.execute("SELECT emp_id, ROW_NUMBER() OVER (w ORDER BY emp_id) FROM employees WINDOW w AS (PARTITION BY dept_id) ORDER BY emp_id").fetchall()
print("  OVER (w ORDER BY ...) where w has only PARTITION BY: ran, first rows", ok[:4])
try:
    con.execute("SELECT ROW_NUMBER() OVER (w ORDER BY emp_id) FROM employees WINDOW w AS (PARTITION BY dept_id ORDER BY salary)").fetchall()
except sqlite3.Error as e:
    print("  OVER (w ORDER BY ...) where w already has ORDER BY:", type(e).__name__ + ":", e)

emp = q("SELECT * FROM employees")
# pd:main
clean = emp.dropna(subset=["salary"])
pd_qualify = clean.assign(rk=clean.groupby("dept_id")["salary"].rank(method="min", ascending=False))
pd_qualify = pd_qualify[pd_qualify["rk"] <= 2]                                      # QUALIFY
pd_distinct_on = (clean.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
                       .drop_duplicates("dept_id"))                                 # DISTINCT ON
pd_nulls_first = emp[emp["dept_id"] == 20].sort_values(["salary", "emp_id"], ascending=[False, True], na_position="first")
first_nonnull = emp.groupby("dept_id")["salary"].first()                            # FIRST_VALUE ... IGNORE NULLS
# pd:end
pd.testing.assert_frame_equal(qe[["emp_id", "rk"]], pd_qualify.sort_values(["dept_id", "rk", "emp_id"])[["emp_id", "rk"]].astype(int).reset_index(drop=True), check_dtype=False)
assert de["emp_id"].tolist() == pd_distinct_on["emp_id"].tolist()
assert nf["emp_id"].tolist() == pd_nulls_first["emp_id"].tolist()
ign = con.execute("""SELECT dept_id, salary FROM (SELECT dept_id, salary, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY emp_id) rn
        FROM employees WHERE salary IS NOT NULL) WHERE rn = 1 ORDER BY dept_id""").fetchall()
print("\nFIRST_VALUE IGNORE NULLS emulated by filtering NULLs first (first non-NULL per dept by emp_id):", ign)
print("pandas groupby first() skips NaN by default:", first_nonnull.to_dict(), "(dept 30 has only NULLs -> NaN)")
assert [r[1] for r in ign] == [first_nonnull[10], first_nonnull[20]]
print("asserts passed")
```

**Output (my run):**
```text
SQLite 3.45.1

QUALIFY emulation (RANK <= 2 per department, NULL salaries removed):
 emp_id  dept_id  salary  rk
      1       10      90   1
      2       10      80   2
      3       10      80   2
      5       20      60   1
      7       20      50   2

DISTINCT ON emulation (one row per department):
 emp_id  dept_id  salary
      1       10      90
      5       20      60

rank without any window function (correlated COUNT) equals RANK(): True

NULLS FIRST on SQLite 3.45 (dept 20): [6, 5, 7] | portable IS NULL emulation gives the same: True
default SQLite order, ASC puts NULLs first: [None, 50, 60]

syntax tried on SQLite 3.45 that is NOT supported (error text from the run):
  QUALIFY: OperationalError: near "ROW_NUMBER": syntax error
  DISTINCT ON: OperationalError: near "ON": syntax error
  FETCH FIRST WITH TIES: OperationalError: near "FETCH": syntax error
  PERCENTILE_CONT: OperationalError: near "(": syntax error
  IGNORE NULLS: OperationalError: near "NULLS": syntax error

named window extension on SQLite 3.45.1:
  OVER (w ORDER BY ...) where w has only PARTITION BY: ran, first rows [(1, 1), (2, 2), (3, 3), (4, 4)]
  OVER (w ORDER BY ...) where w already has ORDER BY: OperationalError: cannot override ORDER BY clause of window: w

FIRST_VALUE IGNORE NULLS emulated by filtering NULLs first (first non-NULL per dept by emp_id): [(10, 90), (20, 60)]
pandas groupby first() skips NaN by default: {10: 90.0, 20: 60.0, 30: nan} (dept 30 has only NULLs -> NaN)
asserts passed
```

**Edge cases:**
- Unsupported syntax gave only a generic syntax error in SQLite (it points at the first unknown word). The error text is not a statement about other engines.
- An all-NULL department vanishes after `WHERE salary IS NOT NULL`; keep it with a LEFT JOIN from a departments table if needed (Q46).
- The portable NULLS emulation sorts by `(col IS NULL)` first. Be careful with the direction (`DESC` on the boolean puts NULLs first).
- `groupby().first()` returns NaN for the all-NaN department, like a NULL.

**Then explain:**
- **Main message:** the CTE (or subquery) plus WHERE on the window column replaces QUALIFY in every engine that has windows; QUALIFY is just shorthand.
- **Per-group top-1:** ROW_NUMBER = 1 with a tie-breaker replaces DISTINCT ON.
- **Ties with a limit:** RANK <= n replaces WITH TIES.
- **Percentiles:** emulate with ROW_NUMBER and COUNT or CUME_DIST (Q41).
- **Always add the caveat:** the right column of the table is memory, not a run.

**Follow-ups:**
- *Which engines can't do windows at all?* MySQL 5.7 and earlier (hedged); use a correlated count as run above.
- *Is the emulation slower than QUALIFY?* On engines that have QUALIFY it is the same plan idea; I did not measure.
- *How do you check your engine's support?* Run a tiny query for each syntax, as the Code block does on SQLite.

**Common mistakes:**
- Writing QUALIFY and being surprised by a syntax error on PostgreSQL, MySQL or SQLite.
- Assuming NULL ordering is the same everywhere.
- Using DISTINCT ON without ORDER BY and expecting a repeatable row.
- Stating dialect facts as verified when they are remembered.

