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
