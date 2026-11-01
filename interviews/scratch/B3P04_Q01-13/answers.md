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
