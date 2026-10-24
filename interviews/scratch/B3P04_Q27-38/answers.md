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
- **pandas:** `emp[mask]` then `groupby().rank()` is the first version; `groupby().rank()` on the full frame and then `[mask]` is the second. Assigning the rank to a filtered slice needs `.copy()` to avoid a chained-assignment warning.
- **Other engines:** the same evaluation order holds in PostgreSQL, MySQL 8 and the others (not executed here); `QUALIFY` filters after the window, so a `WHERE` next to it is still before.

**Follow-ups:**
- *How do you get both ranks in one result?* Rank all rows in a CTE with a `CASE WHEN status = 'active'` partition trick, or run the window twice (one over everyone, one over `PARTITION BY dept_id, status`); in pandas, group by `["dept_id", "status"]`.
- *What if you want the top active earner per department, ties included?* `RANK() = 1` after `WHERE status = 'active'`.
- *Why not put the status test in `PARTITION BY`?* Then active and left are ranked as separate groups and you still have to filter; it is the same as filtering first for the active group.

**Common mistakes:**
- Writing the filter in the outer query when the question says "among active": ranks include departed staff.
- Believing `WHERE` runs after `RANK()`; it does not.
- In pandas, ranking the full frame and then forgetting to filter, or filtering and ranking into a view and getting a `SettingWithCopyWarning`.
- Reading `rank` as an int: pandas returns floats unless you cast.
