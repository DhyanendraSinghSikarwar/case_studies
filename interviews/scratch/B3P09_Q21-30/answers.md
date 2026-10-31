### Q21 ⭐⭐ 🟡 Engine portability of hierarchical queries: take the employee subtree query and write it for MySQL 8 (WITH RECURSIVE, CAST in the anchor so the path column is wide enough, cte_max_recursion_depth), SQL Server (WITH without RECURSIVE, OPTION (MAXRECURSION 100 by default), + for concatenation), PostgreSQL 14+ (SEARCH DEPTH FIRST and CYCLE clauses) and Oracle (START WITH ... CONNECT BY PRIOR, LEVEL, SYS_CONNECT_BY_PATH, CONNECT_BY_ISLEAF, NOCYCLE). Run only the SQLite version and mark the others not executed. Include what SQLite 3.45.1 does not support (the CYCLE and SEARCH clauses fail with a syntax error and there is no generate_series without an extension), as checked by running them.
**Asked at:** Oracle hierarchical query documentation (search snippets only, not opened: START WITH, CONNECT BY PRIOR, LEVEL, SYS_CONNECT_BY_PATH, CONNECT_BY_ISLEAF, NOCYCLE, CONNECT_BY_ISCYCLE, ORA-01436 on a loop; Snowflake CONNECT BY docs supporting SYS_CONNECT_BY_PATH but not NOCYCLE, ISCYCLE or ISLEAF) plus the opened PostgreSQL, MySQL 8.4 and SQLite pages; documentation, not candidate reports; interviews on Oracle, SQL Server and PostgreSQL stacks
**Say this first (1 line):** The shape of a hierarchical query (anchor, recursive step, guard) is the same everywhere, but the spelling is not: SQLite, MySQL 8 and PostgreSQL write `WITH RECURSIVE`, SQL Server writes plain `WITH` and caps recursion with `OPTION (MAXRECURSION n)`, Oracle has its own `START WITH ... CONNECT BY PRIOR`, and PostgreSQL 14+ adds `SEARCH` and `CYCLE` clauses that SQLite 3.45.1 rejects; I ran only the SQLite version and the other dialects below are written from the docs and memory, not executed.

**Schema and sample data:** twelve employees, one tree (Tim is the CEO with a NULL manager), and the same data as the other hierarchy questions in this part; the subtree is Hari (emp 3).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
```

**SQL answer:** `SQL_MAIN` in the Code block, the SQLite version (it also runs unchanged on PostgreSQL and MySQL 8 apart from the string concatenation, see the table):
```sql
WITH RECURSIVE sub(emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, s.path || ' > ' || e.name
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT s.emp_id, s.name, s.level, s.path,
       CASE WHEN EXISTS (SELECT 1 FROM employees c WHERE c.manager_id = s.emp_id) THEN 0 ELSE 1 END AS is_leaf
FROM sub s
ORDER BY s.path
```
The `WHERE s.level < 20` line is a depth guard that I keep in every dialect: it is portable, it makes the intent visible, and it works even where the engine has its own cap.

The dialect versions below are **not executed here** (no PostgreSQL, MySQL, SQL Server, Oracle or Snowflake server in this environment). They follow the opened MySQL 8.4 and PostgreSQL pages and my memory of the others; check each against your engine's documentation before relying on it.

MySQL 8 (not executed): `WITH RECURSIVE` is required, `CONCAT` is the safe string join (`||` means OR unless the `PIPES_AS_CONCAT` mode is on), and the column types come from the anchor, so the path column is cast wide enough:
```sql
-- MySQL 8.x, NOT EXECUTED
WITH RECURSIVE sub (emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, CAST(name AS CHAR(200)) FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, CONCAT(s.path, ' > ', e.name)
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT s.emp_id, s.name, s.level, s.path FROM sub s ORDER BY s.path;
-- session cap on iterations (default 1000 per the MySQL 8.4 page): SET SESSION cte_max_recursion_depth = 5000;
```
SQL Server (not executed): no `RECURSIVE` keyword, `+` joins strings, the anchor and recursive column types must match exactly (hence both `CAST`s), and the default recursion cap is 100 levels (error 530, per search snippets; `OPTION (MAXRECURSION 0)` means no cap), written at the very end of the outer statement:
```sql
-- SQL Server, NOT EXECUTED
WITH sub (emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, CAST(name AS VARCHAR(400)) FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, CAST(s.path + ' > ' + e.name AS VARCHAR(400))
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT s.emp_id, s.name, s.level, s.path FROM sub s ORDER BY s.path
OPTION (MAXRECURSION 100);
```
PostgreSQL 14+ (not executed; the version number comes from a search snippet, the clause syntax from the opened PostgreSQL page): `SEARCH` orders the output depth-first or breadth-first, `CYCLE` marks and stops rows that revisit a node, so no hand-written path guard is needed:
```sql
-- PostgreSQL 14+, NOT EXECUTED
WITH RECURSIVE sub (emp_id, name, level) AS (
  SELECT emp_id, name, 0 FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
)
SEARCH DEPTH FIRST BY emp_id SET ordercol
CYCLE emp_id SET is_cycle USING cycle_path
SELECT * FROM sub ORDER BY ordercol;
```
Oracle (not executed; from documentation snippets, not opened): a separate hierarchical syntax. `LEVEL` starts at 1, `SYS_CONNECT_BY_PATH` starts with the separator (so the path is `' > Hari > Shyam'`), `NOCYCLE` suppresses the loop error (ORA-01436 without it, per snippets), `CONNECT_BY_ISLEAF` is the leaf flag:
```sql
-- Oracle, NOT EXECUTED
SELECT emp_id, name, LEVEL - 1 AS lvl, SYS_CONNECT_BY_PATH(name, ' > ') AS path, CONNECT_BY_ISLEAF AS is_leaf
FROM employees
START WITH emp_id = 3
CONNECT BY NOCYCLE PRIOR emp_id = manager_id
ORDER SIBLINGS BY name;
```
Snowflake (not executed): per a search snippet it supports both `WITH RECURSIVE` and `CONNECT BY` with `SYS_CONNECT_BY_PATH`, but not `NOCYCLE`, `CONNECT_BY_ISCYCLE` or `CONNECT_BY_ISLEAF`; I would write the `WITH RECURSIVE` form with a depth counter there.

| Item | SQLite 3.45.1 (run) | MySQL 8 | SQL Server | PostgreSQL | Oracle |
|---|---|---|---|---|---|
| Keyword | `WITH RECURSIVE` | `WITH RECURSIVE` | `WITH` | `WITH RECURSIVE` | `CONNECT BY` (or `WITH`) |
| String join | `\|\|` (`+` gives 0, see Output) | `CONCAT` | `+` or `CONCAT` | `\|\|` | `\|\|` |
| Iteration cap | none; stops by `LIMIT`, empty queue or your depth column | `cte_max_recursion_depth`, default 1000 | `MAXRECURSION`, default 100 | none by default; your depth column or `LIMIT` | no cap; a loop raises an error unless `NOCYCLE` |
| Cycle help | hand-written path or `UNION` | hand-written | hand-written | `CYCLE` clause (14+) | `NOCYCLE`, `CONNECT_BY_ISCYCLE` |
| Order help | `ORDER BY` in the recursive select sets queue order | none | none | `SEARCH` clause (14+) | `ORDER SIBLINGS BY` |
All non-SQLite cells are not executed here.

**pandas answer:** the portability question is about SQL; the pandas counterpart is dialect-free: a frontier merge that expands one level per iteration, with a visited set as the cycle guard. Shown once here and identical to the Code block:
```py
kids = employees[["emp_id", "manager_id", "name"]].rename(columns={"emp_id": "child_id", "name": "child_name"})
frontier = employees.loc[employees["emp_id"] == 3, ["emp_id", "name"]].assign(level=0)
frontier["path"] = frontier["name"]
parts, seen = [frontier], {3}
while len(frontier):
    nxt = frontier[["emp_id", "level", "path"]].merge(kids, left_on="emp_id", right_on="manager_id")
    nxt = nxt[~nxt["child_id"].isin(seen)]
    frontier = pd.DataFrame({"emp_id": nxt["child_id"], "name": nxt["child_name"],
                             "level": nxt["level"] + 1, "path": nxt["path"] + " > " + nxt["child_name"]})
    seen.update(frontier["emp_id"])
    parts.append(frontier)
pd_df = pd.concat(parts, ignore_index=True)
pd_df["is_leaf"] = (~pd_df["emp_id"].isin(employees["manager_id"].dropna())).astype(int)
pd_df = pd_df.sort_values("path").reset_index(drop=True)
```

**Example:** Hari (3) is the anchor, level 0, path `Hari`. Round 1 joins employees whose manager is 3: Shyam (4) and Asha (7), level 1, paths `Hari > Shyam` and `Hari > Asha`. Round 2: the reports of 4 are Ram (10) and Zoya (11), the report of 7 is Nina (12), level 2. Round 3: nobody reports to 10, 11 or 12, the working table is empty and the recursion stops. Six rows in total. `is_leaf` is 1 for Ram, Zoya and Nina (nobody has them as a manager) and 0 for Hari, Shyam and Asha. The pandas loop does the same: three merges (levels 1, 2, and a third that finds nothing), six rows, equal to the SQL after sorting both by `path`.

**Code:** run with `python3 -I`. It runs the SQLite query and the pandas loop, asserts they are equal after sorting both by `path`, then executes each SQLite-limitation probe and prints what happened (the failures are caught on purpose).
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
"""
SQL_MAIN = """
WITH RECURSIVE sub(emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, s.path || ' > ' || e.name
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT s.emp_id, s.name, s.level, s.path,
       CASE WHEN EXISTS (SELECT 1 FROM employees c WHERE c.manager_id = s.emp_id) THEN 0 ELSE 1 END AS is_leaf
FROM sub s
ORDER BY s.path
"""
PROBES = [
  ("CYCLE clause (PostgreSQL 14+ syntax)",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 3) "
   "CYCLE n SET is_cycle USING path SELECT * FROM t"),
  ("SEARCH DEPTH FIRST clause (PostgreSQL 14+ syntax)",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 3) "
   "SEARCH DEPTH FIRST BY n SET ordercol SELECT * FROM t ORDER BY ordercol"),
  ("generate_series", "SELECT value FROM generate_series(1, 3)"),
  ("CTE referenced twice in the recursive member",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t "
   "WHERE n < 3 AND n NOT IN (SELECT n FROM t)) SELECT * FROM t"),
  ("aggregate in the recursive member",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT MAX(n) + 1 FROM t WHERE n < 3) SELECT * FROM t"),
  ("'a' + 'b' (SQL Server style concatenation)", "SELECT 'a' + 'b'"),
  ("CAST in the anchor as MySQL needs it: length of the final path",
   "WITH RECURSIVE t(n, p) AS (SELECT 1, CAST('a' AS CHAR(1)) UNION ALL "
   "SELECT n + 1, p || 'bbbb' FROM t WHERE n < 5) SELECT length(p) FROM t WHERE n = 5"),
  ("no default recursion cap: count to 1,000,000",
   "WITH RECURSIVE c(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM c WHERE n < 1000000) "
   "SELECT COUNT(*), MAX(n) FROM c"),
]

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
employees["manager_id"] = employees["manager_id"].astype("Int64")

# pd:main
kids = employees[["emp_id", "manager_id", "name"]].rename(columns={"emp_id": "child_id", "name": "child_name"})
frontier = employees.loc[employees["emp_id"] == 3, ["emp_id", "name"]].assign(level=0)
frontier["path"] = frontier["name"]
parts, seen = [frontier], {3}
while len(frontier):
    nxt = frontier[["emp_id", "level", "path"]].merge(kids, left_on="emp_id", right_on="manager_id")
    nxt = nxt[~nxt["child_id"].isin(seen)]
    frontier = pd.DataFrame({"emp_id": nxt["child_id"], "name": nxt["child_name"],
                             "level": nxt["level"] + 1, "path": nxt["path"] + " > " + nxt["child_name"]})
    seen.update(frontier["emp_id"])
    parts.append(frontier)
pd_df = pd.concat(parts, ignore_index=True)
pd_df["is_leaf"] = (~pd_df["emp_id"].isin(employees["manager_id"].dropna())).astype(int)
pd_df = pd_df.sort_values("path").reset_index(drop=True)
# pd:end
# compare after ordering both by path (the SQL ORDER BY path)
pd.testing.assert_frame_equal(pd_df[list(sql_df.columns)].astype({"emp_id": "int64"}), sql_df, check_dtype=False)
print("pandas frontier loop equals the SQLite recursive CTE:", len(pd_df), "rows,", len(parts) - 1, "merges (the last one finds nothing)")

print("\nProbes on SQLite", sqlite3.sqlite_version, "(each statement was run):")
for label, sql in PROBES:
    try:
        print(f"  OK   {label}: {con.execute(sql).fetchall()}")
    except sqlite3.Error as ex:
        print(f"  FAIL {label}: {type(ex).__name__}: {ex}")
print("asserts passed")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5
 emp_id  name  level                path  is_leaf
      3  Hari      0                Hari        0
      7  Asha      1         Hari > Asha        0
     12  Nina      2  Hari > Asha > Nina        1
      4 Shyam      1        Hari > Shyam        0
     10   Ram      2  Hari > Shyam > Ram        1
     11  Zoya      2 Hari > Shyam > Zoya        1
pandas frontier loop equals the SQLite recursive CTE: 6 rows, 3 merges (the last one finds nothing)

Probes on SQLite 3.45.1 (each statement was run):
  FAIL CYCLE clause (PostgreSQL 14+ syntax): OperationalError: near "CYCLE": syntax error
  FAIL SEARCH DEPTH FIRST clause (PostgreSQL 14+ syntax): OperationalError: near "SEARCH": syntax error
  FAIL generate_series: OperationalError: no such table: generate_series
  FAIL CTE referenced twice in the recursive member: OperationalError: multiple recursive references: t
  FAIL aggregate in the recursive member: OperationalError: recursive aggregate queries not supported
  OK   'a' + 'b' (SQL Server style concatenation): [(0,)]
  OK   CAST in the anchor as MySQL needs it: length of the final path: [(17,)]
  OK   no default recursion cap: count to 1,000,000: [(1000000, 1000000)]
asserts passed
```

**Edge cases:**
- Things SQLite 3.45.1 refused or did differently in my run: the `CYCLE` and `SEARCH` clauses are syntax errors; `generate_series` is "no such table" (it exists in some builds as an extension, not in this one); the CTE name used twice in the recursive member (here inside `NOT IN (SELECT n FROM t)`) fails with `multiple recursive references`; an aggregate in the recursive member fails with `recursive aggregate queries not supported`. So "remember what I already visited" cannot be written as a subquery on the CTE itself; use a path string, or `UNION`.
- `'a' + 'b'` is `0` in SQLite (numeric addition of two non-numeric strings), so SQL Server style concatenation does not fail loudly, it silently returns a number. Use `||`.
- There is no built-in recursion cap in SQLite: a count to 1,000,000 ran in my run without any error. That is why a runaway query on SQLite keeps going until memory or a `LIMIT`, while SQL Server (100) and MySQL (1000) stop it with an error. The default caps are the reason a long chain can fail on SQL Server or MySQL with perfectly correct logic.
- `CAST(... AS CHAR(1))` does not truncate in SQLite (the final path was 17 characters long in my run); in MySQL the anchor's declared width matters, which is why the cast is there (hedged: MySQL behaviour from the opened docs, not executed).
- NULL manager (the CEO) is never joined from a child row, so in a subtree query it matters only for the anchor; ordering by `path` makes the output deterministic across engines (collation differences aside).
- Calendar spines: `generate_series` is the PostgreSQL way (not executed here) and the recursive CTE is the portable one; Part 6 Q31 (calendar table) shows both and `pd.date_range`.

**Then explain:**
- Common core: anchor member, `UNION ALL`, recursive member that joins the CTE to the table, a stop condition (empty result or a depth guard). That is portable; only the keyword, string join, type matching and caps change.
- SQL Server and MySQL want the recursive columns to have the anchor's type, which is the single most common portability failure with path strings (the anchor `name` is narrow, the path grows).
- Iteration caps are a safety net, not a design: a correct query on deep data needs the cap raised (`MAXRECURSION`, `cte_max_recursion_depth`), and a query with a cycle should be fixed with a guard rather than a larger cap.
- `CYCLE` and `SEARCH` in PostgreSQL 14+ replace the hand-written path-and-flag and the manual `ORDER BY path`; in SQLite and MySQL you write those by hand (Q8 shows the path guard).
- Oracle's `CONNECT BY` is a different model (a row source walked from `START WITH`, `PRIOR` marks the parent side), with built-in `LEVEL`, path and leaf functions; Oracle also supports a standard recursive `WITH` (stated from memory, not executed).
- pandas has no dialect problem, but it has its own guard: the visited set.

**Follow-ups:**
- Which engine would stop first on a 500-deep chain? SQL Server with its default 100 (hedged, not executed) and MySQL with 1000 would stop at their caps; SQLite would not stop.
- Can you do this in a view on SQL Server? The `MAXRECURSION` hint cannot be placed inside a view; it goes on the outer query (snippet, not executed).
- How do you make breadth-first output in SQLite? A recursive select with no `ORDER BY` is a FIFO queue (breadth-first); Q27 shows the queue order.

**Common mistakes:**
- Copying a PostgreSQL `CYCLE ...` query to SQLite and being surprised by a syntax error.
- Using `+` for strings in SQLite, or `||` in MySQL, and getting numbers or OR logic back.
- Forgetting the anchor `CAST` on MySQL or SQL Server, and getting truncation or a type-mismatch error when the path grows.
- Raising `MAXRECURSION 0` or the MySQL depth to hide a loop in the data.
- Claiming a dialect works because it looked right: only the SQLite lines in this answer were run.

### Q22 ⭐⭐ 🔴 Topological order and dependency resolution: tasks(task_id, depends_on) with one row per dependency and tasks with no dependency listed with depends_on NULL. Return a valid build order as 'stage' numbers (stage = longest chain of dependencies below the task, so independent tasks share a stage), and detect whether the graph has a cycle (some tasks never get a stage). Show the recursive CTE that propagates the stage as MAX(depth), why a DAG can have many paths to the same node, how the cycle check works (tasks missing from the result), and the Python graphlib.TopologicalSorter or networkx topological_generations equivalent with an assert.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Start the recursion from tasks that have no dependency (stage 0), let every dependent task inherit "depth + 1" from each of its prerequisites, take `MAX(depth)` per task because a DAG can reach the same task through several paths and the longest chain decides the stage, and flag a cycle by the tasks that never receive a stage; independent tasks then share a stage number.

**Schema and sample data:** one row per dependency, `depends_on` NULL for a task with no prerequisite. `tasks` is a DAG: A and F are free, B and C need A, D needs B and C (and the row `('D','B')` is loaded twice on purpose), E needs D and also A directly, G needs F. `tasks_cyc` has a pure loop (X and Y wait for each other, Z waits for Y). `tasks_mix` is the trap: X also depends on a normal task A, so the loop can be entered from a task that has a stage.
```sql
CREATE TABLE tasks(task_id TEXT, depends_on TEXT);
INSERT INTO tasks VALUES
 ('A',NULL),('F',NULL),('B','A'),('C','A'),('D','B'),('D','C'),('E','D'),('E','A'),('G','F'),('D','B');
-- X and Y wait for each other, Z waits for Y; none of them is reachable from a task without dependencies
CREATE TABLE tasks_cyc(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_cyc VALUES
 ('A',NULL),('B','A'),('X','Y'),('Y','X'),('Z','Y');
-- trap: X also depends on a normal task A, so the loop can be entered from a root
CREATE TABLE tasks_mix(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_mix VALUES
 ('A',NULL),('B','A'),('X','A'),('X','Y'),('Y','X'),('Z','Y');
```

**SQL answer:** `SQL_MAIN` in the Code block; run on the DAG, it is the stage per task:
```sql
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT task_id, MAX(depth) AS stage, COUNT(*) AS paths_seen
FROM stage
GROUP BY task_id
ORDER BY stage, task_id
```
Why `HAVING COUNT(depends_on) = 0` for the anchor: `COUNT(col)` skips NULLs, so a task whose only row has `depends_on` NULL has count 0 (no prerequisites); a task with at least one real dependency does not. The depth guard `s.depth < 50` is set above the number of tasks and exists only so a loop cannot run forever.

Which tasks never got a stage (`SQL_NOSTAGE` in the Code block, a plain anti-check on the result of the same CTE):
```sql
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT DISTINCT task_id FROM tasks
WHERE task_id NOT IN (SELECT task_id FROM stage)
ORDER BY task_id
```
A second, more reliable cycle check (`SQL_SELF_REACH`): walk "depends on" as a transitive closure with `UNION` (no depth column, so the set of `(start, cur)` pairs is finite and the query terminates by itself) and report the tasks that reach themselves:
```sql
WITH RECURSIVE w(start, cur) AS (
  SELECT task_id, depends_on FROM tasks WHERE depends_on IS NOT NULL
  UNION
  SELECT w.start, t.depends_on
  FROM w JOIN tasks t ON t.task_id = w.cur
  WHERE t.depends_on IS NOT NULL
)
SELECT DISTINCT start AS task_in_cycle FROM w WHERE cur = start ORDER BY 1
```

**pandas answer:** assign layers in a loop: a task is ready in round `r` when all its prerequisites already have a stage, and then its stage is `r`. That gives 1 + the largest prerequisite stage, which is the same longest-chain rule. Shown once here and identical to the Code block:
```py
def stages_pandas(tasks):
    edges = tasks.dropna(subset=["depends_on"]).drop_duplicates()
    nodes = set(tasks["task_id"])
    ndeps = edges.groupby("task_id").size()
    stage = {t: 0 for t in nodes - set(ndeps.index)}
    r = 0
    while True:
        r += 1
        e = edges[~edges["task_id"].isin(stage)]
        done = e["depends_on"].isin(stage).groupby(e["task_id"]).sum()
        ready = done[done == ndeps.reindex(done.index)].index
        if len(ready) == 0:
            break
        stage.update({t: r for t in ready})
    return pd.DataFrame({"task_id": list(stage), "stage": list(stage.values())})
```
Standard library and networkx versions (these are in the Code block and are asserted equal to the SQL stages): `graphlib.TopologicalSorter` with `prepare()`, then each `get_ready()` batch followed by `done(*batch)` gives one stage per batch; `networkx.topological_generations(G)` with edges prerequisite to task gives the same layers. Both were called as written at run time on Python 3.13 and networkx 3.6.1.

**Example:** DAG, stage by hand. A and F have no prerequisite: stage 0. B and C wait only for A, G waits only for F: stage 1. D waits for B and C (both stage 1): stage 2. E waits for D (stage 2) and for A (stage 0): the longest chain is A, B, D, E, so stage 3, not 1. The recursive CTE visits E four times (once through each dependency row: three rows reach D because `('D','B')` is duplicated, plus the direct `A` row), at depths 3, 3, 3 and 1, and `MAX(depth)` returns 3. The `paths_seen` column in the output is exactly that count: D has 3, E has 4. `MIN` or a plain `GROUP BY` without `MAX` would give a wrong build order.
Cycle: in `tasks_cyc`, X, Y and Z have no way in from stage 0, so they never appear in the CTE and `SQL_NOSTAGE` returns X, Y, Z; `SQL_SELF_REACH` returns only X and Y, because Z is stuck behind the loop but is not part of it.

**Code:** run with `python3 -I`. Compared after ordering by `stage, task_id`; the graphlib and networkx stage dictionaries are asserted equal to the SQL stages on the DAG; the cycle datasets are printed, not asserted equal, because that is the point.
```python
import sqlite3
from graphlib import TopologicalSorter, CycleError
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE tasks(task_id TEXT, depends_on TEXT);
INSERT INTO tasks VALUES
 ('A',NULL),('F',NULL),('B','A'),('C','A'),('D','B'),('D','C'),('E','D'),('E','A'),('G','F'),('D','B');
-- X and Y wait for each other, Z waits for Y; none of them is reachable from a task without dependencies
CREATE TABLE tasks_cyc(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_cyc VALUES
 ('A',NULL),('B','A'),('X','Y'),('Y','X'),('Z','Y');
-- trap: X also depends on a normal task A, so the loop can be entered from a root
CREATE TABLE tasks_mix(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_mix VALUES
 ('A',NULL),('B','A'),('X','A'),('X','Y'),('Y','X'),('Z','Y');
"""
SQL_MAIN = """
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT task_id, MAX(depth) AS stage, COUNT(*) AS paths_seen
FROM stage
GROUP BY task_id
ORDER BY stage, task_id
"""
SQL_NOSTAGE = """
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT DISTINCT task_id FROM tasks
WHERE task_id NOT IN (SELECT task_id FROM stage)
ORDER BY task_id
"""
SQL_SELF_REACH = """
WITH RECURSIVE w(start, cur) AS (
  SELECT task_id, depends_on FROM tasks WHERE depends_on IS NOT NULL
  UNION
  SELECT w.start, t.depends_on
  FROM w JOIN tasks t ON t.task_id = w.cur
  WHERE t.depends_on IS NOT NULL
)
SELECT DISTINCT start AS task_in_cycle FROM w WHERE cur = start ORDER BY 1
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

def swap(sql, table):
    return sql.replace("FROM tasks", f"FROM {table}").replace("JOIN tasks", f"JOIN {table}")

sql_dag = pd.read_sql_query(SQL_MAIN, con)
print("DAG: tasks with no stage:", [r[0] for r in con.execute(SQL_NOSTAGE)])
print("DAG, stage = longest chain below the task (paths_seen = rows the CTE produced for it):")
print(sql_dag.to_string(index=False))

# pd:main
def stages_pandas(tasks):
    edges = tasks.dropna(subset=["depends_on"]).drop_duplicates()
    nodes = set(tasks["task_id"])
    ndeps = edges.groupby("task_id").size()
    stage = {t: 0 for t in nodes - set(ndeps.index)}
    r = 0
    while True:
        r += 1
        e = edges[~edges["task_id"].isin(stage)]
        done = e["depends_on"].isin(stage).groupby(e["task_id"]).sum()
        ready = done[done == ndeps.reindex(done.index)].index
        if len(ready) == 0:
            break
        stage.update({t: r for t in ready})
    return pd.DataFrame({"task_id": list(stage), "stage": list(stage.values())})
# pd:end

tasks = pd.read_sql_query("SELECT * FROM tasks", con)
pd_dag = stages_pandas(tasks).sort_values(["stage", "task_id"]).reset_index(drop=True)
# compare after ordering by stage, task_id (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_dag, sql_dag[["task_id", "stage"]], check_dtype=False)
print("pandas layer loop equals SQL")

# graphlib: dependencies as {task: {what it waits for}}
deps = {}
for t, d in con.execute("SELECT task_id, depends_on FROM tasks").fetchall():
    deps.setdefault(t, set())
    if d is not None:
        deps[t].add(d)
ts = TopologicalSorter(deps)
ts.prepare()
gl, k = {}, 0
while ts.is_active():
    batch = ts.get_ready()
    for t in batch:
        gl[t] = k
    ts.done(*batch)
    k += 1
G = nx.DiGraph()
G.add_nodes_from(deps)
G.add_edges_from((d, t) for t, ds in deps.items() for d in ds)      # edge: prerequisite -> task
nxg = {t: i for i, gen in enumerate(nx.topological_generations(G)) for t in gen}
assert gl == nxg == dict(zip(sql_dag["task_id"], sql_dag["stage"]))
print("graphlib batches and networkx topological_generations equal the SQL stages")

for table in ("tasks_cyc", "tasks_mix"):
    q = swap(SQL_MAIN, table)
    got = pd.read_sql_query(q, con)
    print(f"\n{table}: stages from the recursive CTE (depth cap 50)")
    print(got.to_string(index=False))
    all_tasks = [r[0] for r in con.execute(f"SELECT DISTINCT task_id FROM {table} ORDER BY 1")]
    nostage = [r[0] for r in con.execute(swap(SQL_NOSTAGE, table))]
    assert nostage == sorted(set(all_tasks) - set(got["task_id"]))
    print("  tasks with no stage (SQL_NOSTAGE):", nostage)
    print("  tasks that reach themselves:", [r[0] for r in con.execute(swap(SQL_SELF_REACH, table))])
    t2 = pd.read_sql_query(f"SELECT * FROM {table}", con)
    s2 = stages_pandas(t2)
    print("  pandas layer loop stages:", dict(zip(s2["task_id"], s2["stage"])))
    d2 = {}
    for t, d in con.execute(f"SELECT task_id, depends_on FROM {table}").fetchall():
        d2.setdefault(t, set())
        if d is not None:
            d2[t].add(d)
    try:
        TopologicalSorter(d2).prepare()
    except CycleError as ex:
        print("  graphlib CycleError, cycle found:", ex.args[1])
    G2 = nx.DiGraph([(d, t) for t, ds in d2.items() for d in ds])
    try:
        list(nx.topological_generations(G2))
    except nx.NetworkXUnfeasible as ex:
        print("  networkx NetworkXUnfeasible:", ex)
    print("  networkx find_cycle:", nx.find_cycle(G2))
print("asserts passed")
```

**Output (my run):**
```text
DAG: tasks with no stage: []
DAG, stage = longest chain below the task (paths_seen = rows the CTE produced for it):
task_id  stage  paths_seen
      A      0           1
      F      0           1
      B      1           1
      C      1           1
      G      1           1
      D      2           3
      E      3           4
pandas layer loop equals SQL
graphlib batches and networkx topological_generations equal the SQL stages

tasks_cyc: stages from the recursive CTE (depth cap 50)
task_id  stage  paths_seen
      A      0           1
      B      1           1
  tasks with no stage (SQL_NOSTAGE): ['X', 'Y', 'Z']
  tasks that reach themselves: ['X', 'Y']
  pandas layer loop stages: {'A': 0, 'B': 1}
  graphlib CycleError, cycle found: ['X', 'Y', 'X']
  networkx NetworkXUnfeasible: Graph contains a cycle or graph changed during iteration
  networkx find_cycle: [('Y', 'X'), ('X', 'Y')]

tasks_mix: stages from the recursive CTE (depth cap 50)
task_id  stage  paths_seen
      A      0           1
      B      1           1
      X     49          25
      Z     49          24
      Y     50          25
  tasks with no stage (SQL_NOSTAGE): []
  tasks that reach themselves: ['X', 'Y']
  pandas layer loop stages: {'A': 0, 'B': 1}
  graphlib CycleError, cycle found: ['X', 'Y', 'X']
  networkx NetworkXUnfeasible: Graph contains a cycle or graph changed during iteration
  networkx find_cycle: [('X', 'Y'), ('Y', 'X')]
asserts passed
```

**Edge cases:**
- Loop reachable only from itself (`tasks_cyc`): the CTE returns stages for A and B only; X, Y and Z are missing. "Tasks missing from the result" is therefore the loop check, but it also lists tasks that are merely downstream of a loop (Z).
- The trap (`tasks_mix`): X depends on A and on Y. Starting from A, the CTE reaches X (A is a stage 0 task), then Y, then X again, and so on until my depth guard of 50 stops it. Result in my run: X 49, Z 49, Y 50, and no task is missing. So here the missing-task check says "no cycle" and gives stages that are nonsense (they are just the depth cap). The guard keeps the query finite but the answer wrong; the `SQL_SELF_REACH` closure finds X and Y in both datasets. The rule I state: stages from this CTE are only trustworthy after a cycle check that does not rely on the same CTE.
- The pandas layer loop is safer here: X and Y can never be ready (each waits for the other), so it returns only A and B on both cyclic datasets, and the missing tasks are the cycle and everything stuck behind it.
- Duplicate dependency rows: harmless for `MAX(depth)` (they inflate `paths_seen` only); the pandas loop uses `drop_duplicates` before counting prerequisites, otherwise `ready` would compare against an inflated count.
- Task with a prerequisite that has no row of its own as `task_id`: it would never get a stage in the CTE (nothing starts it). Normalise the input first so every prerequisite also appears as a task with a NULL-dependency row.
- Self dependency (`('W','W')`): a loop of length 1, found by `SQL_SELF_REACH` (start = cur) and never staged.
- graphlib raises `CycleError` (the cycle is in `args[1]`, printed above as `['X', 'Y', 'X']`) and networkx raises `NetworkXUnfeasible`; networkx `find_cycle` returns the loop edges. Those are the library versions of the cycle check.

**Then explain:**
- `stage` equals the length of the longest chain below the task; it is what a scheduler uses for "all tasks of one stage can run in parallel".
- A DAG can have many paths to the same node (E has four rows in the CTE). The recursive CTE enumerates paths, not nodes, so its cost grows with the number of paths: this is cheap on this toy graph and can explode on wide layered graphs (Q29 counts doubling paths).
- `MAX(depth)` over all paths is correct because every dependency must finish before the task: the slowest chain wins.
- The CTE propagates from stage 0 outward, so it never checks that a task's other prerequisites are done. In a DAG that does not matter (the longest chain covers them), in a graph with a loop it can give the wrong answer, as the mixed dataset shows.
- Recursion limits per engine, hedged and not executed: SQL Server `MAXRECURSION`, MySQL `cte_max_recursion_depth`; PostgreSQL 14+ has a `CYCLE` clause that marks loops for you (not executed).
- Window functions are not needed here (they belong to Parts 4-5).

**Follow-ups:**
- Return a full ordering and not stages? Order by `stage, task_id`; ties are free to run in parallel.
- What if a dependency points to a task that does not exist? Treat it as a data error and list it; with the CTE as written such a task is never staged, and `SQL_NOSTAGE` would show it.
- How would you stop a cycle inside the CTE? Add a path string and an `instr` guard, and keep `MAX(depth)`; the answer for tasks behind a loop is still undefined, so report them separately.

**Common mistakes:**
- Using `MIN(depth)` or taking the first row per task: stage ends up one too small for tasks with a long chain.
- Starting the anchor from every task (including ones with prerequisites): everything gets stage 0 rows and `MAX` is polluted.
- Counting a NULL `depends_on` as a dependency (use `COUNT(depends_on)`, not `COUNT(*)`).
- Trusting "no missing tasks" as proof of no cycle (the mixed dataset breaks it).
- Treating the depth guard value as a result (stage 49 or 50 above is a cap, not a stage).

### Q23 ⭐⭐ 🔴 Weighted shortest path with a cycle guard: roads(src, dst, km) on a small directed graph with a loop and two competing routes from 'A' to 'F'. Return the cheapest path with its path string and total km by enumerating all simple paths (path-string guard) and taking the minimum, then explain why this enumeration is exponential in the worst case, why a plain depth limit is not enough to be correct with cycles of negative or zero weight, and how Dijkstra differs (visited set with a priority queue, not expressible with plain recursion without extras). Check the answer with networkx shortest_path (installed here; scipy is not) and a hand-written heapq Dijkstra, asserting all agree.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Enumerate every simple path from A with a path-string guard (never step to a node already in the path), keep the ones that end at F, and take the smallest total; that is correct but exponential in the worst case, a plain depth limit is not a correct guard once a cycle has zero or negative weight, and the real shortest-path algorithm is Dijkstra (priority queue plus a visited set, no negative edges), which I cross-check with `heapq` and networkx.

**Schema and sample data:** nine directed roads between A and F. Two competing families of routes: through B (A to B costs 2) or straight to C (cost 5), a loop between B and C (`B>C` costs 1, `C>B` costs 1), then C or B to D, then D to F directly (6) or via E (1 + 2). `roads_neg` is the same graph with `C>B` set to -3, so the loop B, C, B costs -2 each time round.
```sql
CREATE TABLE roads(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads VALUES
 ('A','B',2),('A','C',5),('B','C',1),('C','B',1),('B','D',7),('C','D',2),
 ('D','E',1),('D','F',6),('E','F',2);
-- same graph but the road C to B has a negative weight (a refund or a downhill credit), so B-C-B costs -2 per loop
CREATE TABLE roads_neg(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads_neg SELECT src, dst, CASE WHEN src = 'C' AND dst = 'B' THEN -3 ELSE km END FROM roads;
```

**SQL answer:** `SQL_MAIN` in the Code block; it returns all simple routes ordered by cost, so the first row is the cheapest:
```sql
WITH RECURSIVE p(node, path, km, legs) AS (
  SELECT 'A', ',A,', 0, 0
  UNION ALL
  SELECT r.dst, p.path || r.dst || ',', p.km + r.km, p.legs + 1
  FROM p JOIN roads r ON r.src = p.node
  WHERE instr(p.path, ',' || r.dst || ',') = 0
)
SELECT trim(path, ',') AS route, km, legs
FROM p
WHERE node = 'F'
ORDER BY km, route
```
The path is stored as `,A,B,` with commas around each node so that `instr(path, ',B,')` cannot match inside a longer name (`AB` versus `B`). `ORDER BY km, route` makes ties deterministic.

**pandas answer:** a frontier of partial paths; each iteration merges the frontier with the edge list on `node = src`, drops the extensions whose `dst` is already in the route, and collects the rows that reached F. Shown once here and identical to the Code block:
```py
paths = pd.DataFrame({"node": ["A"], "route": ["A"], "km": [0], "legs": [0]})
found = []
while len(paths):
    nxt = paths.merge(roads, left_on="node", right_on="src")
    fresh = pd.Series([d not in r.split(">") for d, r in zip(nxt["dst"], nxt["route"])], index=nxt.index, dtype=bool)
    nxt = nxt[fresh]
    paths = pd.DataFrame({"node": nxt["dst"], "route": nxt["route"] + ">" + nxt["dst"],
                          "km": nxt["km"] + nxt["w"], "legs": nxt["legs"] + 1})
    found.append(paths[paths["node"] == "F"])
pd_df = (pd.concat(found)[["route", "km", "legs"]]
           .sort_values(["km", "route"]).reset_index(drop=True))
```
Dijkstra with `heapq` and `networkx.shortest_path`/`shortest_path_length` with `weight='km'` are in the Code block; the asserts compare route and distance across SQL, `heapq` and networkx.

**Example:** from A: routes reaching F by hand. A, B, C, D, E, F costs 2+1+2+1+2 = 8. A, C, D, E, F costs 5+2+1+2 = 10. A, B, C, D, F costs 2+1+2+6 = 11. A, B, D, E, F costs 2+7+1+2 = 12. A, C, D, F is 13, A, B, D, F is 15, and the two routes that use the `C>B` road (A, C, B, D, E, F and A, C, B, D, F) cost 16 and 19. That is 8 simple routes; the cheapest is A>B>C>D>E>F at 8 km over 5 legs, even though it has the most legs: fewest legs and cheapest are different questions. The loop B to C to B is never walked twice because the path guard blocks revisiting B (or C) inside one route.

**Code:** run with `python3 -I`. Compared after ordering by `km, route`; the cheapest route and km are asserted equal across SQL, the pandas frontier merge, a hand-written `heapq` Dijkstra and `networkx.shortest_path` / `shortest_path_length`.
```python
import heapq
import sqlite3
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE roads(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads VALUES
 ('A','B',2),('A','C',5),('B','C',1),('C','B',1),('B','D',7),('C','D',2),
 ('D','E',1),('D','F',6),('E','F',2);
-- same graph but the road C to B has a negative weight (a refund or a downhill credit), so B-C-B costs -2 per loop
CREATE TABLE roads_neg(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads_neg SELECT src, dst, CASE WHEN src = 'C' AND dst = 'B' THEN -3 ELSE km END FROM roads;
"""
SQL_MAIN = """
WITH RECURSIVE p(node, path, km, legs) AS (
  SELECT 'A', ',A,', 0, 0
  UNION ALL
  SELECT r.dst, p.path || r.dst || ',', p.km + r.km, p.legs + 1
  FROM p JOIN roads r ON r.src = p.node
  WHERE instr(p.path, ',' || r.dst || ',') = 0
)
SELECT trim(path, ',') AS route, km, legs
FROM p
WHERE node = 'F'
ORDER BY km, route
"""
SQL_NODEPTH = """
WITH RECURSIVE w(node, km, legs) AS (
  SELECT 'A', 0, 0
  UNION ALL
  SELECT r.dst, w.km + r.km, w.legs + 1
  FROM w JOIN roads_t r ON r.src = w.node
  WHERE w.legs < {cap}
)
SELECT COUNT(*) AS walks_to_F, MIN(km) AS cheapest_km FROM w WHERE node = 'F'
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_df["route"] = sql_df["route"].str.replace(",", ">")
print("All simple routes A to F, cheapest first (SQL path-string guard):")
print(sql_df.to_string(index=False))

roads = pd.read_sql_query("SELECT src, dst, km AS w FROM roads", con)

# pd:main
paths = pd.DataFrame({"node": ["A"], "route": ["A"], "km": [0], "legs": [0]})
found = []
while len(paths):
    nxt = paths.merge(roads, left_on="node", right_on="src")
    fresh = pd.Series([d not in r.split(">") for d, r in zip(nxt["dst"], nxt["route"])], index=nxt.index, dtype=bool)
    nxt = nxt[fresh]
    paths = pd.DataFrame({"node": nxt["dst"], "route": nxt["route"] + ">" + nxt["dst"],
                          "km": nxt["km"] + nxt["w"], "legs": nxt["legs"] + 1})
    found.append(paths[paths["node"] == "F"])
pd_df = (pd.concat(found)[["route", "km", "legs"]]
           .sort_values(["km", "route"]).reset_index(drop=True))
# pd:end
# compare after ordering by km, route (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas frontier merge equals SQL:", len(pd_df), "simple routes")

def dijkstra(edges, source, target):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    best, heap = {source: 0}, [(0, source, [source])]
    done = set()
    while heap:
        d, u, route = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        if u == target:
            return d, ">".join(route)
        for v, w in graph.get(u, []):
            if v not in done and d + w < best.get(v, float("inf")):
                best[v] = d + w
                heapq.heappush(heap, (d + w, v, route + [v]))
    return None

edges = con.execute("SELECT src, dst, km FROM roads").fetchall()
dj_km, dj_route = dijkstra(edges, "A", "F")
G = nx.DiGraph()
G.add_weighted_edges_from(edges, weight="km")
nx_route = ">".join(nx.shortest_path(G, "A", "F", weight="km"))
nx_km = nx.shortest_path_length(G, "A", "F", weight="km")
best = sql_df.iloc[0]
assert (best["route"], best["km"]) == (dj_route, dj_km) == (nx_route, nx_km)
print("cheapest: SQL", (best["route"], int(best["km"])), "| heapq Dijkstra", (dj_route, dj_km), "| networkx", (nx_route, nx_km))

print("\nDepth limit only (no path guard), cheapest walk from A to F and number of walks, by leg cap:")
for table in ("roads", "roads_neg"):
    rows = []
    for cap in (4, 6, 8, 10, 12):
        n, m = con.execute(SQL_NODEPTH.replace("roads_t", table).format(cap=cap)).fetchone()
        rows.append((cap, n, m))
    print(f"  {table}:", rows, "(cap, walks_to_F, cheapest_km)")

neg = nx.DiGraph()
neg.add_weighted_edges_from(con.execute("SELECT src, dst, km FROM roads_neg").fetchall(), weight="km")
print("networkx negative_edge_cycle on roads_neg:", nx.negative_edge_cycle(neg, weight="km"))
try:
    nx.bellman_ford_path(neg, "A", "F", weight="km")
except nx.NetworkXUnbounded as ex:
    print("networkx bellman_ford_path raises NetworkXUnbounded:", ex)
try:
    print("networkx dijkstra on the negative cycle returns:", nx.dijkstra_path(neg, "A", "F", weight="km"))
except Exception as ex:
    print("networkx dijkstra raises", type(ex).__name__, ex)

import time
print("\nSimple-path enumeration on a chain of k diamonds (2 routes per diamond), SQL path-string guard:")
for k in (6, 10, 14):
    d = []
    for i in range(k):
        d += [(f"s{i}", f"a{i}", 1), (f"s{i}", f"b{i}", 1), (f"a{i}", f"s{i+1}", 1), (f"b{i}", f"s{i+1}", 1)]
    con.execute("DROP TABLE IF EXISTS dia")
    con.execute("CREATE TABLE dia(src TEXT, dst TEXT, km INTEGER)")
    con.executemany("INSERT INTO dia VALUES (?, ?, ?)", d)
    q = SQL_MAIN.replace("'A'", "'s0'").replace("roads", "dia").replace("node = 'F'", f"node = 's{k}'")
    t0 = time.perf_counter()
    n = con.execute(f"SELECT COUNT(*) FROM ({q.replace(chr(10) + 'ORDER BY km, route', '')})").fetchone()[0]
    print(f"  k={k:2d}: {n} simple routes (2^k = {2**k}), {len(d)} edges, {time.perf_counter() - t0:.3f} s on this machine")
print("asserts passed")
```

**Output (my run):**
```text
All simple routes A to F, cheapest first (SQL path-string guard):
      route  km  legs
A>B>C>D>E>F   8     5
  A>C>D>E>F  10     4
  A>B>C>D>F  11     4
  A>B>D>E>F  12     4
    A>C>D>F  13     3
    A>B>D>F  15     3
A>C>B>D>E>F  16     5
  A>C>B>D>F  19     4
pandas frontier merge equals SQL: 8 simple routes
cheapest: SQL ('A>B>C>D>E>F', 8) | heapq Dijkstra ('A>B>C>D>E>F', 8) | networkx ('A>B>C>D>E>F', 8)

Depth limit only (no path guard), cheapest walk from A to F and number of walks, by leg cap:
  roads: [(4, 6, 10), (6, 14, 8), (8, 22, 8), (10, 30, 8), (12, 38, 8)] (cap, walks_to_F, cheapest_km)
  roads_neg: [(4, 6, 10), (6, 14, 8), (8, 22, 6), (10, 30, 4), (12, 38, 2)] (cap, walks_to_F, cheapest_km)
networkx negative_edge_cycle on roads_neg: True
networkx bellman_ford_path raises NetworkXUnbounded: Negative cycle detected.
networkx dijkstra raises ValueError ('Contradictory paths found:', 'negative weights?')

Simple-path enumeration on a chain of k diamonds (2 routes per diamond), SQL path-string guard:
  k= 6: 64 simple routes (2^k = 64), 24 edges, 0.000 s on this machine
  k=10: 1024 simple routes (2^k = 1024), 40 edges, 0.004 s on this machine
  k=14: 16384 simple routes (2^k = 16384), 56 edges, 0.071 s on this machine
asserts passed
```

**Edge cases:**
- Depth limit only, no path guard (the `Depth limit only` block in the output): on `roads` the number of walks keeps growing with the cap (6, 14, 22, 30, 38 walks for caps 4, 6, 8, 10, 12) while the cheapest cost stays 8 once the cap reaches 6. A depth limit therefore terminates, but it counts repeated-node walks and costs time; on positive weights the minimum is still right once the cap is big enough.
- With the negative loop (`roads_neg`) the minimum is not stable: cheapest walk cost 10, 8, 6, 4, 2 for caps 4, 6, 8, 10, 12. Every extra lap of B, C, B lowers the cost by 2, so no cap gives "the" answer. That is why a depth limit is not enough when a cycle has negative total weight, and a zero-weight cycle gives infinitely many walks of equal cost (the cost is fine, the row count is not). The path guard answers a different, well-defined question (cheapest simple path), but even that is hard in general with negative edges and is not what Dijkstra computes.
- networkx behaviour I ran: `negative_edge_cycle` returned `True` on `roads_neg`, `bellman_ford_path` raised `NetworkXUnbounded` ("Negative cycle detected."), and `dijkstra_path` raised `ValueError` ("Contradictory paths found: negative weights?"), meaning Dijkstra on negative edges can fail loudly or, on other graphs, return a wrong path without an error (I did not test a silent case here).
- Ties: two routes with the same cost both appear; `ORDER BY km, route` picks the alphabetically first. Dijkstra and networkx may return either of two tied routes; the assert is on this graph where the cheapest is unique.
- No route (target unreachable): the SQL returns no rows, `dijkstra` returns `None` in my function, networkx raises `NetworkXNoPath` (from memory of its documentation, not run here); handle the empty case explicitly.
- Edge direction: the data is directed; for two-way roads insert both directions or the search will miss routes.

**Then explain:**
- Why the enumeration is exponential: every branch point multiplies the number of simple paths. A chain of k diamonds (two routes per diamond) has 2^k simple paths: in my run 64, 1,024 and 16,384 routes for k = 6, 10 and 14 (SQL path guard, last block of the output; the elapsed times printed there are from this machine only). On a dense graph the count is worse than exponential in the number of nodes.
- Dijkstra: keep the best-known distance for each node, always settle the unsettled node with the smallest distance (priority queue), never revisit a settled node; with non-negative weights each node is settled once, so it is about O((V+E) log V). It stores one distance per node, not one row per path.
- Why plain recursion cannot do Dijkstra: the recursive member cannot reference the CTE twice (SQLite fails with `multiple recursive references`, checked in Q21), cannot use aggregates over the CTE, and cannot "settle" a node because the working table is a queue of all rows, not a priority queue with a visited set. You can approximate by keeping `MIN(km)` per node after a depth cap, which is a Bellman-Ford style relaxation, not Dijkstra; I did not run that here.
- A depth limit is a safety net; a path guard (or `UNION` on node) is correctness for cycles. Use both in practice: the guard for correctness, the cap for safety.
- Other engines: PostgreSQL 14+ `CYCLE` clause and SQL Server `MAXRECURSION` / MySQL `cte_max_recursion_depth` caps exist (hedged, not executed).

**Follow-ups:**
- Fewest legs instead of cheapest? Order by `legs` (BFS), then `km`.
- Shortest path for all pairs on a large graph? Not in SQL; use a graph library or a graph database (not covered here; scipy is not installed in this environment, networkx is).
- Why did you not use `UNION` to dedupe? `UNION` removes duplicate rows only; rows with different paths or costs are different rows, so it does not prevent walks around a loop.

**Common mistakes:**
- Substring matching without delimiters (`instr(path, 'B')` also matches `BLR`).
- Using only a depth cap and calling the minimum "the shortest path" when a cheaper loop exists.
- Forgetting the graph is directed, or adding reverse edges that were not roads.
- Ordering by `legs` and calling it cheapest.
- Presenting enumeration as scalable: it is exponential in the worst case.

### Q24 ⭐ 🟡 Hierarchy storage models at concept level: adjacency list (parent_id), materialized path ('/1/4/9/'), nested sets (lft, rgt) and closure table (ancestor, descendant, depth). For one 8-node category tree load all four models in SQLite and write the same query in each: all descendants of node 4, the ancestors of node 9, the depth of each node and the move of a subtree, stating the read and write cost, the integrity risk and the index needed for each. Say which you would pick for a read-heavy catalogue, a comment thread with frequent inserts and a deep, frequently changing org chart. The trade-offs are rules of thumb, not benchmarks.
**Asked at:** hierarchy storage-model guides (search snippets only, not opened: Medium 'From Trees to Tables', jopr, oneuptime MySQL hierarchical schema, dev.to PostgreSQL ltree versus adjacency versus closure table; adjacency is simplest but needs recursion, nested sets fast reads and costly writes, materialized path prefix queries, closure table all pairs with O(n squared) worst-case rows); blog posts, not candidate reports; data modelling and backend-adjacent analyst rounds
**Say this first (1 line):** I load the same tree four ways and run the same questions in each: adjacency list (simple writes, needs recursion to read), materialized path (prefix queries, a subtree move rewrites every path below it), nested sets (very fast subtree reads, an insert or move renumbers many rows) and closure table (every ancestor-descendant pair stored, fast reads both ways, more rows and more write work); the costs I give are rules of thumb from blogs, not benchmarks, and the only numbers here are row counts and query plans I ran.

**Schema and sample data:** premise check: the question says an 8-node tree and also asks for the ancestors of node 9, so the ids cannot be 1 to 8. I use eight nodes with ids 1, 2, 3, 4, 5, 6, 7 and 9 (id 8 was "deleted earlier"), a realistic id gap. Tree: Root(1) has Electronics(2) and Books(3); Electronics has Phones(4) and Laptops(5); Books has Fiction(6); Phones has iOS(7) and Android(9).
```sql
CREATE TABLE adj(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO adj VALUES
 (1,NULL,'Root'),(2,1,'Electronics'),(3,1,'Books'),(4,2,'Phones'),(5,2,'Laptops'),
 (6,3,'Fiction'),(7,4,'iOS'),(9,4,'Android');
```
The other three models are built from the adjacency table (`BUILD` in the Code block creates `mat` (path text) and `closure` (ancestor, descendant, depth, self rows included) with recursive CTEs; nested set numbers `lft`/`rgt` come from a small depth-first walk in Python, children in id order):
```sql
CREATE TABLE mat(id INTEGER PRIMARY KEY, path TEXT);
INSERT INTO mat
WITH RECURSIVE t(id, path) AS (
  SELECT id, '/' || id || '/' FROM adj WHERE parent_id IS NULL
  UNION ALL
  SELECT a.id, t.path || a.id || '/' FROM adj a JOIN t ON a.parent_id = t.id
)
SELECT id, path FROM t;
CREATE TABLE closure(ancestor INTEGER, descendant INTEGER, depth INTEGER, PRIMARY KEY (ancestor, descendant));
INSERT INTO closure
WITH RECURSIVE c(ancestor, descendant, depth) AS (
  SELECT id, id, 0 FROM adj
  UNION ALL
  SELECT c.ancestor, a.id, c.depth + 1 FROM c JOIN adj a ON a.parent_id = c.descendant
)
SELECT ancestor, descendant, depth FROM c;
CREATE INDEX closure_desc ON closure(descendant, ancestor);
```

**SQL answer:** the same three questions in four dialects of the schema (all in the dict `Q` in the Code block, asserted equal to each other; node 4 for descendants, node 9 for ancestors):
- Adjacency list: recursive CTE down for descendants (`SELECT id FROM adj WHERE parent_id = 4` then join on `parent_id = d.id`), recursive CTE up for ancestors (join `a.id = u.parent_id`), recursive CTE from the root for depth. Move: `UPDATE adj SET parent_id = 3 WHERE id = 4`, one row.
- Materialized path: descendants `n.path LIKE t.path || '%'` (plus `n.id <> 4`), ancestors `t.path LIKE a.path || '%'`, depth is the number of slashes minus 2. The trailing slash in the path matters: `/1/2/4/` cannot match `/1/2/40/`. Move:
```sql
UPDATE mat SET path = '/1/3/' || substr(path, length('/1/2/') + 1)
WHERE path LIKE '/1/2/4/%'
```
- Nested sets: descendants `n.lft > t.lft AND n.rgt < t.rgt`, ancestors `a.lft < t.lft AND a.rgt > t.rgt`, depth is a count of ancestors. Move: renumber; I rebuild the numbers in Python and count what changed, since the pure SQL shift is a multi-statement script (not shown, not executed).
- Closure table: descendants `ancestor = 4 AND depth > 0`, ancestors `descendant = 9 AND depth > 0`, depth is the `depth` column from the root's rows. Move is two statements:
```sql
DELETE FROM closure
WHERE descendant IN (SELECT descendant FROM closure WHERE ancestor = 4)
  AND ancestor IN (SELECT ancestor FROM closure WHERE descendant = 4 AND ancestor <> 4)
```
```sql
INSERT INTO closure
SELECT sup.ancestor, sub.descendant, sup.depth + sub.depth + 1
FROM closure sup, closure sub
WHERE sup.descendant = 3 AND sub.ancestor = 4
```
Statement 1 removes the links between the moved subtree and its old ancestors above it (not the links inside the subtree); statement 2 links the moved subtree to the new parent and all of the new parent's ancestors, with depth adding up.

**pandas answer:** the path model and the pair model, built in pandas from the adjacency frame and checked against the SQL results. Shown once here and identical to the Code block:
```py
parent = dict(zip(adj["id"], adj["parent_id"]))
def chain(i):
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out[::-1]
paths = pd.Series({i: "/" + "/".join(map(str, chain(i))) + "/" for i in adj["id"]}).rename_axis("id").rename("path").reset_index()
p4 = paths.loc[paths["id"] == 4, "path"].item()
p9 = paths.loc[paths["id"] == 9, "path"].item()
pd_desc = paths.loc[paths["path"].str.startswith(p4) & (paths["id"] != 4), "id"].sort_values().tolist()
pd_anc = sorted(int(x) for x in p9.strip("/").split("/") if int(x) != 9)
pd_depth = dict(zip(paths["id"], paths["path"].str.count("/") - 2))
pairs = pd.DataFrame([(a, i, k) for i in adj["id"] for k, a in enumerate(chain(i)[::-1])],
                     columns=["ancestor", "descendant", "depth"])
```

**Example:** the path column for node 9 is `/1/2/4/9/`, so its ancestors are the ids in the path before it (1, 2, 4), its depth is 4 slashes minus 2 = 3 (Root is depth 0), and the descendants of 4 are the rows whose path starts with `/1/2/4/` other than 4 itself (7 and 9). In nested sets the numbers from the walk are 1(1,16), 2(2,11), 4(3,8), 7(4,5), 9(6,7), 5(9,10), 3(12,15), 6(13,14); node 4 is (3,8), so descendants are nodes with `lft > 3 and rgt < 8`, which are 7 (4,5) and 9 (6,7), and the ancestors of 9 (6,7) are the nodes with `lft < 6 and rgt > 7`, which are 1, 2 and 4. In the closure table 22 rows exist: 8 self rows plus one per ancestor-descendant pair (depths 0, 1, 1, 2, 2, 2, 3, 3 sum to 14). Moving subtree 4 (nodes 4, 7, 9) under 3: adjacency changes 1 row; materialized path changes 3 paths; the closure table deletes 6 rows (3 nodes times 2 old ancestors, 1 and 2) and inserts 6 (3 nodes times 2 new ancestors, 3 and 1); nested sets changed 6 of 8 rows in my rebuild. After the move all four models agree again: ancestors of 9 are 1, 3 and 4 and its depth is still 3.

**Code:** run with `python3 -I`. It builds the four models, asserts that all three questions give identical results across them before and after the move, asserts the pandas path/prefix and pair frames equal the SQL results, prints the number of rows each move changed, and prints `EXPLAIN QUERY PLAN` for the path-prefix lookup.
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE adj(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO adj VALUES
 (1,NULL,'Root'),(2,1,'Electronics'),(3,1,'Books'),(4,2,'Phones'),(5,2,'Laptops'),
 (6,3,'Fiction'),(7,4,'iOS'),(9,4,'Android');
"""
BUILD = """
CREATE TABLE mat(id INTEGER PRIMARY KEY, path TEXT);
INSERT INTO mat
WITH RECURSIVE t(id, path) AS (
  SELECT id, '/' || id || '/' FROM adj WHERE parent_id IS NULL
  UNION ALL
  SELECT a.id, t.path || a.id || '/' FROM adj a JOIN t ON a.parent_id = t.id
)
SELECT id, path FROM t;
CREATE TABLE closure(ancestor INTEGER, descendant INTEGER, depth INTEGER, PRIMARY KEY (ancestor, descendant));
INSERT INTO closure
WITH RECURSIVE c(ancestor, descendant, depth) AS (
  SELECT id, id, 0 FROM adj
  UNION ALL
  SELECT c.ancestor, a.id, c.depth + 1 FROM c JOIN adj a ON a.parent_id = c.descendant
)
SELECT ancestor, descendant, depth FROM c;
CREATE INDEX closure_desc ON closure(descendant, ancestor);
"""
Q = {
 "adjacency": {
  "desc": """WITH RECURSIVE d(id) AS (SELECT id FROM adj WHERE parent_id = 4
             UNION ALL SELECT a.id FROM adj a JOIN d ON a.parent_id = d.id) SELECT id FROM d ORDER BY id""",
  "anc": """WITH RECURSIVE u(id, parent_id) AS (SELECT id, parent_id FROM adj WHERE id = 9
            UNION ALL SELECT a.id, a.parent_id FROM adj a JOIN u ON a.id = u.parent_id)
            SELECT id FROM u WHERE id <> 9 ORDER BY id""",
  "depth": """WITH RECURSIVE t(id, depth) AS (SELECT id, 0 FROM adj WHERE parent_id IS NULL
              UNION ALL SELECT a.id, t.depth + 1 FROM adj a JOIN t ON a.parent_id = t.id)
              SELECT id, depth FROM t ORDER BY id"""},
 "materialized path": {
  "desc": "SELECT n.id FROM mat n, mat t WHERE t.id = 4 AND n.path LIKE t.path || '%' AND n.id <> 4 ORDER BY n.id",
  "anc": "SELECT a.id FROM mat a, mat t WHERE t.id = 9 AND t.path LIKE a.path || '%' AND a.id <> 9 ORDER BY a.id",
  "depth": "SELECT id, length(path) - length(replace(path, '/', '')) - 2 AS depth FROM mat ORDER BY id"},
 "nested sets": {
  "desc": "SELECT n.id FROM ns n, ns t WHERE t.id = 4 AND n.lft > t.lft AND n.rgt < t.rgt ORDER BY n.id",
  "anc": "SELECT a.id FROM ns a, ns t WHERE t.id = 9 AND a.lft < t.lft AND a.rgt > t.rgt ORDER BY a.id",
  "depth": "SELECT n.id, (SELECT COUNT(*) FROM ns a WHERE a.lft < n.lft AND a.rgt > n.rgt) AS depth FROM ns n ORDER BY n.id"},
 "closure table": {
  "desc": "SELECT descendant FROM closure WHERE ancestor = 4 AND depth > 0 ORDER BY descendant",
  "anc": "SELECT ancestor FROM closure WHERE descendant = 9 AND depth > 0 ORDER BY ancestor",
  "depth": "SELECT descendant, depth FROM closure WHERE ancestor = 1 ORDER BY descendant"},
}
MOVE_MAT = """
UPDATE mat SET path = '/1/3/' || substr(path, length('/1/2/') + 1)
WHERE path LIKE '/1/2/4/%'
"""
MOVE_CLOSURE_DELETE = """
DELETE FROM closure
WHERE descendant IN (SELECT descendant FROM closure WHERE ancestor = 4)
  AND ancestor IN (SELECT ancestor FROM closure WHERE descendant = 4 AND ancestor <> 4)
"""
MOVE_CLOSURE_INSERT = """
INSERT INTO closure
SELECT sup.ancestor, sub.descendant, sup.depth + sub.depth + 1
FROM closure sup, closure sub
WHERE sup.descendant = 3 AND sub.ancestor = 4
"""

def build_nested_sets(con):
    kids = {}
    for i, p in con.execute("SELECT id, parent_id FROM adj ORDER BY id"):
        kids.setdefault(p, []).append(i)
    out, counter = [], [0]
    def visit(i):
        counter[0] += 1
        lft = counter[0]
        for c in kids.get(i, []):
            visit(c)
        counter[0] += 1
        out.append((i, lft, counter[0]))
    visit(kids[None][0])
    con.execute("DROP TABLE IF EXISTS ns")
    con.execute("CREATE TABLE ns(id INTEGER PRIMARY KEY, lft INTEGER, rgt INTEGER)")
    con.executemany("INSERT INTO ns VALUES (?, ?, ?)", out)

def run_all(con):
    return {m: {k: con.execute(q).fetchall() for k, q in qs.items()} for m, qs in Q.items()}

def agree(res):
    base = res["adjacency"]
    for m, r in res.items():
        assert r == base, (m, r, base)

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.executescript(BUILD)
build_nested_sets(con)
print("nested sets (id, lft, rgt):", con.execute("SELECT * FROM ns ORDER BY lft").fetchall())
print("materialized paths:", con.execute("SELECT id, path FROM mat ORDER BY id").fetchall())
print("closure rows:", con.execute("SELECT COUNT(*) FROM closure").fetchone()[0], "for 8 nodes (8 self rows + one per ancestor-descendant pair)")
before = run_all(con)
agree(before)
print("\nBefore the move, the four models agree. descendants of 4:", [r[0] for r in before["adjacency"]["desc"]],
      "| ancestors of 9:", [r[0] for r in before["adjacency"]["anc"]])
print("depth by id:", dict(before["adjacency"]["depth"]))

# pandas: adjacency walk for paths, then prefix tests on the path column and pair rows for the closure
adj = pd.read_sql_query("SELECT * FROM adj", con)
adj["parent_id"] = adj["parent_id"].astype("Int64")

# pd:main
parent = dict(zip(adj["id"], adj["parent_id"]))
def chain(i):
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out[::-1]
paths = pd.Series({i: "/" + "/".join(map(str, chain(i))) + "/" for i in adj["id"]}).rename_axis("id").rename("path").reset_index()
p4 = paths.loc[paths["id"] == 4, "path"].item()
p9 = paths.loc[paths["id"] == 9, "path"].item()
pd_desc = paths.loc[paths["path"].str.startswith(p4) & (paths["id"] != 4), "id"].sort_values().tolist()
pd_anc = sorted(int(x) for x in p9.strip("/").split("/") if int(x) != 9)
pd_depth = dict(zip(paths["id"], paths["path"].str.count("/") - 2))
pairs = pd.DataFrame([(a, i, k) for i in adj["id"] for k, a in enumerate(chain(i)[::-1])],
                     columns=["ancestor", "descendant", "depth"])
# pd:end
assert pd_desc == [r[0] for r in before["adjacency"]["desc"]]
assert pd_anc == [r[0] for r in before["adjacency"]["anc"]]
assert pd_depth == dict(before["adjacency"]["depth"])
sql_pairs = pd.read_sql_query("SELECT ancestor, descendant, depth FROM closure ORDER BY ancestor, descendant", con)
pd.testing.assert_frame_equal(pairs.sort_values(["ancestor", "descendant"]).reset_index(drop=True), sql_pairs, check_dtype=False)
print("pandas path, prefix and pair frames equal the SQL results (pairs compared after sorting by ancestor, descendant)")

# the move: subtree 4 goes under 3
changes = {}
con.execute("UPDATE adj SET parent_id = 3 WHERE id = 4")
changes["adjacency"] = con.execute("SELECT changes()").fetchone()[0]
con.execute(MOVE_MAT)
changes["materialized path"] = con.execute("SELECT changes()").fetchone()[0]
old_ns = dict((i, (l, r)) for i, l, r in con.execute("SELECT * FROM ns"))
build_nested_sets(con)
new_ns = dict((i, (l, r)) for i, l, r in con.execute("SELECT * FROM ns"))
changes["nested sets (rebuild)"] = sum(old_ns[i] != new_ns[i] for i in old_ns)
con.execute(MOVE_CLOSURE_DELETE)
deleted = con.execute("SELECT changes()").fetchone()[0]
con.execute(MOVE_CLOSURE_INSERT)
inserted = con.execute("SELECT changes()").fetchone()[0]
changes["closure table"] = f"{deleted} deleted + {inserted} inserted"
after = run_all(con)
agree(after)
print("\nAfter moving 4 under 3 the four models still agree. ancestors of 9 now:", [r[0] for r in after["adjacency"]["anc"]],
      "| depth of 9 now:", dict(after["adjacency"]["depth"])[9])
print("rows changed by the move:", changes)
print("nested sets after:", sorted(new_ns.items()))

print("\nEXPLAIN QUERY PLAN for the materialized-path prefix lookup:")
con.execute("CREATE INDEX mat_path ON mat(path)")
for label, q in [("LIKE on a default-collation index", "SELECT id FROM mat WHERE path LIKE '/1/3/4/%'"),
                 ("range on the same index", "SELECT id FROM mat WHERE path >= '/1/3/4/' AND path < '/1/3/40'")]:
    print(" ", label, "->", [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q)])
con.execute("DROP INDEX mat_path")
con.execute("CREATE INDEX mat_path ON mat(path COLLATE NOCASE)")
print("  LIKE on a NOCASE index ->", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT id FROM mat WHERE path LIKE '/1/3/4/%'")])
print("asserts passed")
```

**Output (my run):**
```text
nested sets (id, lft, rgt): [(1, 1, 16), (2, 2, 11), (4, 3, 8), (7, 4, 5), (9, 6, 7), (5, 9, 10), (3, 12, 15), (6, 13, 14)]
materialized paths: [(1, '/1/'), (2, '/1/2/'), (3, '/1/3/'), (4, '/1/2/4/'), (5, '/1/2/5/'), (6, '/1/3/6/'), (7, '/1/2/4/7/'), (9, '/1/2/4/9/')]
closure rows: 22 for 8 nodes (8 self rows + one per ancestor-descendant pair)

Before the move, the four models agree. descendants of 4: [7, 9] | ancestors of 9: [1, 2, 4]
depth by id: {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 9: 3}
pandas path, prefix and pair frames equal the SQL results (pairs compared after sorting by ancestor, descendant)

After moving 4 under 3 the four models still agree. ancestors of 9 now: [1, 3, 4] | depth of 9 now: 3
rows changed by the move: {'adjacency': 1, 'materialized path': 3, 'nested sets (rebuild)': 6, 'closure table': '6 deleted + 6 inserted'}
nested sets after: [(1, (1, 16)), (2, (2, 5)), (3, (6, 15)), (4, (7, 12)), (5, (3, 4)), (6, (13, 14)), (7, (8, 9)), (9, (10, 11))]

EXPLAIN QUERY PLAN for the materialized-path prefix lookup:
  LIKE on a default-collation index -> ['SCAN mat']
  range on the same index -> ['SEARCH mat USING COVERING INDEX mat_path (path>? AND path<?)']
  LIKE on a NOCASE index -> ['SEARCH mat USING COVERING INDEX mat_path (path>? AND path<?)']
asserts passed
```

**Edge cases:**
- Index surprise I ran: with a plain index on `mat(path)`, `path LIKE '/1/3/4/%'` was a full `SCAN mat` in SQLite 3.45.1; the same lookup written as a range (`path >= '/1/3/4/' AND path < '/1/3/40'`, where `0` is the character after `/`) used the index, and so did `LIKE` once the index was created `COLLATE NOCASE` (SQLite's default `LIKE` is case-insensitive). Other engines have their own rules for `LIKE` and indexes (not executed here).
- Path as text breaks on ids that contain the separator, and the path length limits the depth; the leading and trailing slash make prefix tests safe.
- Nested sets: insert or move renumbers many rows, and two concurrent writers can corrupt the numbering, so writes need locking or a rebuild. My rebuild changed 6 of 8 rows to move a 3-node subtree in an 8-node tree.
- Closure table grows with the number of ancestor-descendant pairs: 22 rows for 8 nodes here; a straight chain of n nodes has n(n+1)/2 rows (Q26 prints the numbers for a 2,000-node chain).
- Orphans, loops and a second root are not prevented by any of these models by themselves; adjacency needs a foreign key plus a cycle check on move (Q20), and the others can hold impossible states if written by hand.
- Moving a node under its own descendant must be rejected in every model; none of the SQL above checks it.

**Then explain:**
- Adjacency list: simplest, one row per node, trivial inserts and moves (one cell), every subtree read needs a recursive query and an index on `parent_id`; foreign keys keep integrity easily.
- Materialized path: one indexed string per row, descendants by prefix, ancestors by splitting; moving a subtree rewrites every path below it; the path must be kept consistent by the application, no foreign key helps. Index on `path` (with the right collation or a range predicate, see above).
- Nested sets: subtree and ancestor reads are range comparisons with no recursion, depth needs a count; every insert, delete or move touches many rows; integrity is easy to break. Index on `(lft, rgt)`.
- Closure table: ancestors, descendants and depth are one indexed lookup each; storage is O(n squared) in the worst case (a chain); inserting a leaf adds one row per ancestor, moving a subtree rewrites the pairs between the subtree and its old and new ancestors; integrity needs the application or triggers. Index on `(ancestor, descendant)` and `(descendant, ancestor)`.
- My picks (rules of thumb, not benchmarks): read-heavy catalogue with rare changes: closure table or materialized path (or nested sets if the tree almost never changes); comment thread with frequent inserts: adjacency list (plus a materialized path for sorting and fetching a thread); deep org chart that changes often: adjacency list with a recursive CTE, adding a closure table only if the recursive reads become the bottleneck.
- The O(n squared) closure-table and the nested-set write cost come from blog posts I only saw as search snippets; what I measured here is only row counts on one tiny tree.

**Follow-ups:**
- Which gives ordered sibling output for a UI? Nested sets (order by `lft`), or a materialized path padded to fixed width, or an adjacency list with a sort key.
- PostgreSQL has `ltree`; is it a fifth model? It is a typed materialized path with index support; hedged, not executed.
- How do you keep a closure table correct? Insert the node's rows in the same transaction as the node (all ancestors of the parent, plus the self row); on delete remove the rows where it is a descendant.

**Common mistakes:**
- Prefix tests without a trailing separator (`/1/2/4` also matches `/1/2/40`).
- Using `LIKE` on a path column and assuming the index is used.
- Leaving out the self row in the closure table and then missing the node itself in counts.
- Calling the model choice a benchmark result.
- Moving a subtree under its own descendant.

### Q25 ⭐ 🟡 pandas: all reports under a manager with iterative merges. employees DataFrame(emp_id, manager_id, name, salary) with a NaN manager_id for the CEO. Compute the subtree of manager 3 with a while loop that merges the current frontier to the edge frame until the frontier is empty, tracking level and visited ids so cycles terminate, and the equivalent for the whole company (pairs ancestor, descendant). Assert equality with the SQL recursive CTE, note that manager_id becomes float64 because of NaN (use the nullable Int64 dtype) and that merge matches NaN to NaN, and say why a pandas loop costs one merge per level, not per row.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** In pandas I expand the tree one level per iteration: merge the current frontier (ids and their level) to the edge frame on `emp_id = manager_id`, drop anything already seen, and stop when the frontier is empty; the cost is one merge per level of depth, not one per employee, and the two pandas traps are that a NaN manager turns `manager_id` into float64 (use `Int64`) and that `merge` matches NaN to NaN while SQL never does.

**Schema and sample data:** the twelve-employee tree used across this part (Tim is the CEO with a NULL manager; Hari is emp 3). `emp_cyc` is a tiny second table with a loop (6 and 7 manage each other, 8 reports to 7) to show the cycle guard.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
-- a loop: 6 and 7 manage each other, 8 reports to 7
CREATE TABLE emp_cyc(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO emp_cyc VALUES (1,NULL),(2,1),(6,7),(7,6),(8,7);
```

**SQL answer:** three queries in the Code block. The subtree of manager 3 with its level:
```sql
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = 3
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
```
All ancestor-descendant pairs for the whole company with the depth (anchor: every direct manager link; step: extend each pair one level down):
```sql
WITH RECURSIVE pairs(ancestor, descendant, depth) AS (
  SELECT manager_id, emp_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT p.ancestor, e.emp_id, p.depth + 1
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
  WHERE p.depth < 20
)
SELECT ancestor, descendant, depth FROM pairs ORDER BY ancestor, descendant
```
And the loop case with `UNION` (rows are bare ids, so a repeated id is dropped and the recursion ends):
```sql
WITH RECURSIVE sub(emp_id) AS (
  SELECT emp_id FROM emp_cyc WHERE manager_id = 6
  UNION
  SELECT e.emp_id FROM emp_cyc e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id FROM sub ORDER BY emp_id
```

**pandas answer:** two functions, shown once here and identical to the Code block. `subtree` is the frontier loop with a visited set; `all_pairs` is the same loop where the frontier is a pairs frame (ancestor, descendant, depth) and a pair is dropped when it was already seen. Both return the number of merges:
```py
def subtree(emp, boss):
    kids = emp[["emp_id", "manager_id"]]
    frontier = kids[kids["manager_id"] == boss][["emp_id"]].assign(level=1)
    seen, parts, merges = set(frontier["emp_id"]), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(kids, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
        merges += 1
        nxt = nxt[~nxt["emp_id"].isin(seen)]
        frontier = nxt[["emp_id"]].assign(level=nxt["level"] + 1)
        seen.update(frontier["emp_id"])
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges

def all_pairs(emp):
    edges = emp.dropna(subset=["manager_id"]).rename(columns={"manager_id": "ancestor", "emp_id": "descendant"})[["ancestor", "descendant"]]
    frontier = edges.assign(depth=1)
    seen, parts, merges = set(zip(edges["ancestor"], edges["descendant"])), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(edges.rename(columns={"ancestor": "descendant", "descendant": "child"}), on="descendant")
        merges += 1
        nxt = pd.DataFrame({"ancestor": nxt["ancestor"], "descendant": nxt["child"], "depth": nxt["depth"] + 1})
        fresh = [(a, d) not in seen for a, d in zip(nxt["ancestor"], nxt["descendant"])]
        frontier = nxt[pd.Series(fresh, index=nxt.index, dtype=bool)].drop_duplicates(["ancestor", "descendant"])
        seen.update(zip(frontier["ancestor"], frontier["descendant"]))
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges
```

**Example:** subtree of 3. Level 1 (the anchor, direct reports): Shyam (4) and Asha (7). Merge 1 joins these ids to the rows whose manager is 4 or 7: Ram (10), Zoya (11), Nina (12), level 2. Merge 2 finds nobody under 10, 11, 12, the frontier is empty, the loop stops. So 5 rows and 2 merges for a tree with 12 employees: the loop count follows the depth (2 levels below Hari), not the head count. For the whole company, the deepest chain is Tim, Radha, Hari, Shyam, Ram (depth 4), so there are 4 merges, and 29 pairs in total (the sum of depths over all employees).
Loop case: from emp 6 the visited-set loop returns 7 (a report of 6), then 6 and 8 (reports of 7) after merge 1, and merge 2 finds only already-seen ids; result 6, 7, 8 (6 appears as its own descendant because of the loop), same as `UNION` in SQL.

**Code:** run with `python3 -I`. Compared after ordering by `level, emp_id` (subtree) and `ancestor, descendant` (pairs); ids are cast to `int64` after the loop because the frames carry nullable integers.
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
-- a loop: 6 and 7 manage each other, 8 reports to 7
CREATE TABLE emp_cyc(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO emp_cyc VALUES (1,NULL),(2,1),(6,7),(7,6),(8,7);
"""
SQL_SUBTREE = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = 3
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
"""
SQL_PAIRS = """
WITH RECURSIVE pairs(ancestor, descendant, depth) AS (
  SELECT manager_id, emp_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT p.ancestor, e.emp_id, p.depth + 1
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
  WHERE p.depth < 20
)
SELECT ancestor, descendant, depth FROM pairs ORDER BY ancestor, descendant
"""
SQL_CYC = """
WITH RECURSIVE sub(emp_id) AS (
  SELECT emp_id FROM emp_cyc WHERE manager_id = 6
  UNION
  SELECT e.emp_id FROM emp_cyc e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id FROM sub ORDER BY emp_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_sub = pd.read_sql_query(SQL_SUBTREE, con)
sql_pairs = pd.read_sql_query(SQL_PAIRS, con)
sql_cyc = pd.read_sql_query(SQL_CYC, con)
print("SQL subtree of manager 3:\n" + sql_sub.to_string(index=False))
print("SQL ancestor-descendant pairs:", len(sql_pairs), "rows; max depth", sql_pairs["depth"].max())

employees = pd.read_sql_query("SELECT * FROM employees", con)
emp_cyc = pd.read_sql_query("SELECT * FROM emp_cyc", con)
print("\nread_sql dtype of manager_id:", employees["manager_id"].dtype, "| emp_id:", employees["emp_id"].dtype)
employees["manager_id"] = employees["manager_id"].astype("Int64")
emp_cyc["manager_id"] = emp_cyc["manager_id"].astype("Int64")
print("after astype('Int64'):", employees["manager_id"].dtype, "| root value:", employees.loc[0, "manager_id"])

# pd:main
def subtree(emp, boss):
    kids = emp[["emp_id", "manager_id"]]
    frontier = kids[kids["manager_id"] == boss][["emp_id"]].assign(level=1)
    seen, parts, merges = set(frontier["emp_id"]), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(kids, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
        merges += 1
        nxt = nxt[~nxt["emp_id"].isin(seen)]
        frontier = nxt[["emp_id"]].assign(level=nxt["level"] + 1)
        seen.update(frontier["emp_id"])
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges

def all_pairs(emp):
    edges = emp.dropna(subset=["manager_id"]).rename(columns={"manager_id": "ancestor", "emp_id": "descendant"})[["ancestor", "descendant"]]
    frontier = edges.assign(depth=1)
    seen, parts, merges = set(zip(edges["ancestor"], edges["descendant"])), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(edges.rename(columns={"ancestor": "descendant", "descendant": "child"}), on="descendant")
        merges += 1
        nxt = pd.DataFrame({"ancestor": nxt["ancestor"], "descendant": nxt["child"], "depth": nxt["depth"] + 1})
        fresh = [(a, d) not in seen for a, d in zip(nxt["ancestor"], nxt["descendant"])]
        frontier = nxt[pd.Series(fresh, index=nxt.index, dtype=bool)].drop_duplicates(["ancestor", "descendant"])
        seen.update(zip(frontier["ancestor"], frontier["descendant"]))
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges
# pd:end

pd_sub, m1 = subtree(employees, 3)
pd.testing.assert_frame_equal(pd_sub.sort_values(["level", "emp_id"]).reset_index(drop=True).astype("int64"), sql_sub, check_dtype=False)
print(f"\nsubtree of 3: equal to SQL after sorting by level, emp_id; {len(employees)} employees, {m1} merges (levels, not rows)")

pd_pairs, m2 = all_pairs(employees)
pd.testing.assert_frame_equal(pd_pairs.sort_values(["ancestor", "descendant"]).reset_index(drop=True).astype("int64"), sql_pairs, check_dtype=False)
print(f"all pairs: {len(pd_pairs)} rows equal to SQL after sorting by ancestor, descendant; {m2} merges")

# cycle: visited set terminates, SQL UNION (rows are bare ids) terminates
cyc_pd, m3 = subtree(emp_cyc, 6)
assert sorted(cyc_pd["emp_id"]) == sql_cyc["emp_id"].tolist()
print("cycle 6<->7 (8 under 7), subtree of 6, visited-set loop:", sorted(cyc_pd["emp_id"]), "after", m3, "merges; SQL UNION:", sql_cyc["emp_id"].tolist())

# the same loop WITHOUT the visited filter never ends: stop it after 8 merges and watch the frontier
kids = emp_cyc[["emp_id", "manager_id"]]
fr = kids[kids["manager_id"] == 6][["emp_id"]]
sizes = []
for _ in range(8):
    fr = fr.merge(kids, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))[["emp_id"]]
    sizes.append(len(fr))
print("no visited filter, frontier size after each of 8 merges:", sizes, "(never reaches 0)")

# NaN keys: SQL NULL never joins, pandas merge matches NaN to NaN
sql_same = con.execute("SELECT COUNT(*) FROM employees a JOIN employees b ON a.manager_id = b.manager_id").fetchone()[0]
pd_same = len(employees.merge(employees, on="manager_id"))
pd_same_fixed = len(employees.dropna(subset=["manager_id"]).merge(employees.dropna(subset=["manager_id"]), on="manager_id"))
print("same-manager pairs (a.manager_id = b.manager_id): SQL", sql_same, "| pandas merge", pd_same, "| pandas after dropna", pd_same_fixed)
assert pd_same == sql_same + 1 and pd_same_fixed == sql_same
leaf, mleaf = subtree(employees, 10)
assert len(leaf) == 0 and list(leaf.columns) == ["emp_id", "level"]
print("empty case: subtree of leaf 10 ->", len(leaf), "rows, columns", list(leaf.columns), ",", mleaf, "merges")
print("asserts passed")
```

**Output (my run):**
```text
SQL subtree of manager 3:
 emp_id  level
      4      1
      7      1
     10      2
     11      2
     12      2
SQL ancestor-descendant pairs: 29 rows; max depth 4

read_sql dtype of manager_id: float64 | emp_id: int64
after astype('Int64'): Int64 | root value: <NA>

subtree of 3: equal to SQL after sorting by level, emp_id; 12 employees, 2 merges (levels, not rows)
all pairs: 29 rows equal to SQL after sorting by ancestor, descendant; 4 merges
cycle 6<->7 (8 under 7), subtree of 6, visited-set loop: [6, 7, 8] after 2 merges; SQL UNION: [6, 7, 8]
no visited filter, frontier size after each of 8 merges: [2, 1, 2, 1, 2, 1, 2, 1] (never reaches 0)
same-manager pairs (a.manager_id = b.manager_id): SQL 19 | pandas merge 20 | pandas after dropna 19
empty case: subtree of leaf 10 -> 0 rows, columns ['emp_id', 'level'] , 0 merges
asserts passed
```

**Edge cases:**
- dtype: `pd.read_sql_query` gave `manager_id` as float64 in my run because of the NULL; `astype("Int64")` (nullable integer) keeps whole numbers and shows `<NA>` for the root. Joining float ids to int ids works but invites precision and display surprises; cast early.
- NaN matches NaN in `merge`: the same-manager self join (`a.manager_id = b.manager_id`) gave 19 rows in SQLite and 20 in pandas (the CEO row paired with itself). After `dropna(subset=["manager_id"])` pandas also gave 19. In a frontier loop this matters if the frontier can hold NaN keys: dropping NaN first is the safe habit. Also `employees["manager_id"] == np.nan` is never true; use `isna()`.
- Cycle: with the visited filter the loop ended after 2 merges; without it, the frontier sizes were 2, 1, 2, 1, 2, 1, 2, 1 over 8 merges and would never reach 0 (I stopped it myself).
- Duplicate edge rows: the visited filter drops repeats by id, the plain merge would carry duplicates forward (Q28).
- Empty case: a manager with no reports (leaf 10 in my run) gives an empty first frontier, the loop body never runs, and the result is an empty frame that still has the columns `emp_id` and `level` (0 rows, 0 merges).
- Orphans (manager id not in the table) are never reached from the root; they simply do not appear.

**Then explain:**
- One merge per level: each merge expands every frontier row at once (vectorised), so the number of Python-level iterations is the tree depth. A pure row-by-row loop would cost one step per employee.
- Cost of a merge is about frontier size plus edges, so the whole-company pair loop does roughly depth merges each as large as the current pair set; the result size is the number of ancestor-descendant pairs (29 here, but Q26 shows what it can reach on 50,000 or a long chain).
- Why the guard is two things: a visited set (so cycles end) and `drop_duplicates` on the frontier (so duplicate edges do not multiply rows); the SQL equivalents are `UNION` or a path string, and cleaning duplicates beforehand.
- The SQL and pandas results agree on the clean tree; they differ only where NULL key semantics or unguarded loops come in, which is exactly what the edge cases above show.
- Part 4-5 window functions are not needed here.

**Follow-ups:**
- Include the root of the subtree in the result? Add the anchor row with level 0 (the SQL anchor row `SELECT emp_id, 0` does that).
- Many roots at once? Start the frontier from all of them (as `reports` does in Q28).
- Can you avoid the loop? For a known small depth, repeated merges unrolled; for unknown depth use the loop; for very large frames use a graph library (networkx is installed; I did not use it here).

**Common mistakes:**
- Merging float ids against int ids and not noticing `NaN` in the frontier.
- No visited set: infinite loop on a cycle, duplicated rows on a repeated edge.
- Forgetting that `merge` matches NaN to NaN (SQL does not).
- Counting loop iterations as employees (cost is depth).
- Comparing the SQL and pandas results without sorting.

### Q26 ⭐ 🟡 pandas: roll-ups, depth and paths. From the employees DataFrame compute per-employee depth and path string by walking parents with a dict or repeated merge, then the subtree size and subtree salary with groupby, transform and the pairs frame, and use explode to turn the path list into one row per ancestor and the reverse (groupby then list). Assert equality with the SQL results of the roll-up question and show that groupby(manager_id) alone gives direct reports only. Mention the memory cost of the full ancestor-descendant pair frame and when it is acceptable.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Walk each employee's chain of managers once (a dict lookup) to get depth and path, `explode` the chain into one row per (descendant, ancestor) pair, and every roll-up becomes an ordinary `groupby` on the ancestor; `groupby("manager_id")` alone only counts direct reports, and the pair frame costs as many rows as there are ancestor-descendant pairs.

**Schema and sample data:** the twelve-employee tree (Tim is the CEO; salary is toy column data).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
```

**SQL answer:** three queries in the Code block. Depth and path from the root (path of names with `/`):
```sql
WITH RECURSIVE t(emp_id, name, depth, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.depth + 1, t.path || '/' || e.name
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.depth < 20
)
SELECT emp_id, depth, path FROM t ORDER BY emp_id
```
Subtree size and subtree salary per employee, including the employee himself, through a pairs CTE that starts with one self pair per employee (so there is no depth guard needed on a clean tree; Q15 and Q28 cover dirty data):
```sql
WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT emp_id, emp_id FROM employees
  UNION ALL
  SELECT p.ancestor, e.emp_id
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
)
SELECT p.ancestor AS emp_id,
       COUNT(*) AS subtree_size,
       SUM(e.salary) AS subtree_salary
FROM pairs p JOIN employees e ON e.emp_id = p.descendant
GROUP BY p.ancestor
ORDER BY p.ancestor
```
And direct reports only, for the contrast:
```sql
SELECT manager_id AS emp_id, COUNT(*) AS direct_reports FROM employees
WHERE manager_id IS NOT NULL GROUP BY manager_id ORDER BY manager_id
```

**pandas answer:** shown once here and identical to the Code block. `up` is the chain `[emp, manager, ..., CEO]` from a dict walk; `depth` is its length minus 1, `path` joins the names reversed; `explode` makes the pairs frame; the roll-up merges the salary on the descendant and groups by ancestor; `desc_lists` is the reverse (groupby then list); `direct` is the groupby on `manager_id` only:
```py
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
name = dict(zip(employees["emp_id"], employees["name"]))
def chain_up(i):                       # [i, manager, ..., CEO]
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out
emp = employees.assign(up=employees["emp_id"].map(chain_up))
emp["depth"] = emp["up"].str.len() - 1
emp["path"] = emp["up"].map(lambda u: "/".join(name[x] for x in u[::-1]))
# explode: one row per (descendant, ancestor), self included
pairs = emp[["emp_id", "up"]].explode("up").rename(columns={"emp_id": "descendant", "up": "ancestor"})
pairs["ancestor"] = pairs["ancestor"].astype("int64")
roll = (pairs.merge(employees[["emp_id", "salary"]], left_on="descendant", right_on="emp_id")
             .groupby("ancestor")
             .agg(subtree_size=("descendant", "size"), subtree_salary=("salary", "sum"))
             .rename_axis("emp_id").reset_index())
# the reverse: collect the descendants of each ancestor back into a list
desc_lists = pairs.groupby("ancestor")["descendant"].agg(lambda s: sorted(s)).rename("descendants")
# groupby on manager_id alone gives direct reports only
direct = (employees.dropna(subset=["manager_id"]).groupby("manager_id").size()
          .rename("direct_reports").rename_axis("emp_id").reset_index())
```

**Example:** Ram (10): the chain is `[10, 4, 3, 2, 1]`, so depth 4 and path `Tim/Radha/Hari/Shyam/Ram`. `explode` gives five pairs for Ram (ancestors 10, 4, 3, 2, 1, himself included at distance 0). Grouping all pairs by ancestor: Hari (3) has descendants 3, 4, 7, 10, 11, 12, so subtree size 6 and salary 60 + 50 + 45 + 25 + 28 + 27 = 235. Tim has 12 (everybody, salary 590) but `groupby("manager_id")` gives Tim only 2, his direct reports Radha and Meera. The two are different questions: direct reports versus everybody below.

**Code:** run with `python3 -I`. All three pandas results are compared with the SQL results after ordering by `emp_id` (every SQL query is ordered by `emp_id`).
```python
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
"""
SQL_PATHS = """
WITH RECURSIVE t(emp_id, name, depth, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.depth + 1, t.path || '/' || e.name
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.depth < 20
)
SELECT emp_id, depth, path FROM t ORDER BY emp_id
"""
SQL_ROLLUP = """
WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT emp_id, emp_id FROM employees
  UNION ALL
  SELECT p.ancestor, e.emp_id
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
)
SELECT p.ancestor AS emp_id,
       COUNT(*) AS subtree_size,
       SUM(e.salary) AS subtree_salary
FROM pairs p JOIN employees e ON e.emp_id = p.descendant
GROUP BY p.ancestor
ORDER BY p.ancestor
"""
SQL_DIRECT = """
SELECT manager_id AS emp_id, COUNT(*) AS direct_reports FROM employees
WHERE manager_id IS NOT NULL GROUP BY manager_id ORDER BY manager_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_paths = pd.read_sql_query(SQL_PATHS, con)
sql_roll = pd.read_sql_query(SQL_ROLLUP, con)
sql_direct = pd.read_sql_query(SQL_DIRECT, con)
employees = pd.read_sql_query("SELECT * FROM employees", con)
employees["manager_id"] = employees["manager_id"].astype("Int64")

# pd:main
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
name = dict(zip(employees["emp_id"], employees["name"]))
def chain_up(i):                       # [i, manager, ..., CEO]
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out
emp = employees.assign(up=employees["emp_id"].map(chain_up))
emp["depth"] = emp["up"].str.len() - 1
emp["path"] = emp["up"].map(lambda u: "/".join(name[x] for x in u[::-1]))
# explode: one row per (descendant, ancestor), self included
pairs = emp[["emp_id", "up"]].explode("up").rename(columns={"emp_id": "descendant", "up": "ancestor"})
pairs["ancestor"] = pairs["ancestor"].astype("int64")
roll = (pairs.merge(employees[["emp_id", "salary"]], left_on="descendant", right_on="emp_id")
             .groupby("ancestor")
             .agg(subtree_size=("descendant", "size"), subtree_salary=("salary", "sum"))
             .rename_axis("emp_id").reset_index())
# the reverse: collect the descendants of each ancestor back into a list
desc_lists = pairs.groupby("ancestor")["descendant"].agg(lambda s: sorted(s)).rename("descendants")
# groupby on manager_id alone gives direct reports only
direct = (employees.dropna(subset=["manager_id"]).groupby("manager_id").size()
          .rename("direct_reports").rename_axis("emp_id").reset_index())
# pd:end
direct["emp_id"] = direct["emp_id"].astype("int64")

# compare after ordering by emp_id (all SQL queries are ordered by emp_id)
pd.testing.assert_frame_equal(emp[["emp_id", "depth", "path"]].sort_values("emp_id").reset_index(drop=True), sql_paths, check_dtype=False)
pd.testing.assert_frame_equal(roll.sort_values("emp_id").reset_index(drop=True), sql_roll, check_dtype=False)
pd.testing.assert_frame_equal(direct.sort_values("emp_id").reset_index(drop=True), sql_direct, check_dtype=False)
print("depth/path, roll-up and direct-report counts equal the SQL results")
print(sql_paths.merge(sql_roll, on="emp_id").merge(sql_direct, on="emp_id", how="left").to_string(index=False))
print("\nexploded pairs for Ram (10):", pairs[pairs["descendant"] == 10]["ancestor"].tolist(), "| descendants list of Hari (3):", desc_lists[3])
print("Tim: direct reports =", int(direct.loc[direct["emp_id"] == 1, "direct_reports"].iloc[0]),
      "but subtree_size =", int(roll.loc[roll["emp_id"] == 1, "subtree_size"].iloc[0]), "(includes Tim himself)")

# memory of the pairs frame: toy tree, a balanced tree of 50,000 nodes (8 children per node) and a 2,000-node chain
def pair_stats(parent_arr):
    n = len(parent_arr)
    depth = np.zeros(n, dtype=np.int64)
    for i in range(1, n):
        depth[i] = depth[parent_arr[i]] + 1
    rows = int((depth + 1).sum())
    return n, rows, rows * 16 / 1e6
bal = np.array([-1] + [(i - 1) // 8 for i in range(1, 50000)])
chain = np.array([-1] + list(range(1999)))
print("\nrows in the pairs frame (self rows included); int64 payload computed as rows x 2 columns x 8 bytes, not allocated:")
print("  toy tree      : %d nodes -> %d rows, deep memory %d bytes" % (len(employees), len(pairs), pairs.memory_usage(deep=True).sum()))
for label, arr in [("balanced 8-ary ", bal), ("straight chain ", chain)]:
    n, rows, mb = pair_stats(arr)
    print(f"  {label}: {n} nodes -> {rows} rows, about {mb:.1f} MB")
print("asserts passed")
```

**Output (my run):**
```text
depth/path, roll-up and direct-report counts equal the SQL results
 emp_id  depth                      path  subtree_size  subtree_salary  direct_reports
      1      0                       Tim            12             590             2.0
      2      1                 Tim/Radha             7             315             1.0
      3      2            Tim/Radha/Hari             6             235             2.0
      4      3      Tim/Radha/Hari/Shyam             3             103             2.0
      5      1                 Tim/Meera             4             175             2.0
      6      2           Tim/Meera/Kiran             2              70             1.0
      7      3       Tim/Radha/Hari/Asha             2              72             1.0
      8      3       Tim/Meera/Kiran/Dev             1              30             NaN
      9      2            Tim/Meera/Isha             1              35             NaN
     10      4  Tim/Radha/Hari/Shyam/Ram             1              25             NaN
     11      4 Tim/Radha/Hari/Shyam/Zoya             1              28             NaN
     12      4  Tim/Radha/Hari/Asha/Nina             1              27             NaN

exploded pairs for Ram (10): [10, 4, 3, 2, 1] | descendants list of Hari (3): [3, 4, 7, 10, 11, 12]
Tim: direct reports = 2 but subtree_size = 12 (includes Tim himself)

rows in the pairs frame (self rows included); int64 payload computed as rows x 2 columns x 8 bytes, not allocated:
  toy tree      : 12 nodes -> 41 rows, deep memory 984 bytes
  balanced 8-ary : 50000 nodes -> 307202 rows, about 4.9 MB
  straight chain : 2000 nodes -> 2001000 rows, about 32.0 MB
asserts passed
```

**Edge cases:**
- The pairs frame includes the self pair, so subtree size counts the manager; "number of reports" is `subtree_size - 1` (Tim: 12 versus 11 reports at any depth).
- Leaves have no direct reports: they are absent from the `groupby(manager_id)` output; the merge in my comparison table shows `NaN` (float) for them, so fill with 0 and cast if you need an integer column.
- The CEO has `NaN` as manager: `groupby` and `dropna` drop it (the root is not a report of anybody); `explode` of the chain is fine because the walk stops at the root.
- `explode` returns object dtype; cast the ancestor to `int64` before merging.
- A cycle or orphan would break the dict walk (an infinite loop for a cycle; a `KeyError` for an unknown manager), so clean first (Q28).
- Order: `groupby` sorts by key by default; I still sort before comparing.

**Then explain:**
- Why `explode`: a list-valued column (the chain) becomes one row per element; it is the pandas version of the SQL pairs CTE (one row per ancestor-descendant pair). The reverse is `groupby("ancestor")["descendant"].agg(list)`.
- Memory and when it is acceptable: the pairs frame has one row per ancestor-descendant pair including self. For the toy tree that is 41 rows (984 bytes in `memory_usage(deep=True)` in my run). For a balanced tree of 50,000 nodes with 8 children per node I computed 307,202 rows, about 4.9 MB of int64 payload (rows times 16 bytes, computed, not allocated); for a straight chain of 2,000 nodes 2,001,000 rows, about 32 MB. It is fine for trees of ordinary depth (rows about nodes times depth) and a problem for very deep ones (rows about nodes squared over two).
- When not to build it: if you only need subtree size and salary and the depth is small, aggregate bottom-up (children before parents, one pass by level) instead of materialising every pair.
- Depth and path are per-row facts; subtree size and salary are per-ancestor facts: the first comes from walking up, the second from grouping the pairs.
- SQL parity: the CTE uses `UNION ALL` and a join back to `employees` for the salary; both versions equal after sorting.

**Follow-ups:**
- Average salary of a subtree? `subtree_salary / subtree_size` from the same frame.
- Roll up by level (a manager's reports at depth 2 only)? Keep the distance column in the pairs frame and filter it.
- Only managers with at least three reports at any depth? Filter `subtree_size - 1 >= 3` after the groupby (Q9).

**Common mistakes:**
- Using `groupby("manager_id").size()` as "team size" (direct reports only).
- Counting the manager in his own subtree without saying so.
- Joining salary onto the ancestor instead of the descendant in the pairs frame (summing the manager's salary many times).
- Building the full pairs frame on a very deep or huge hierarchy without estimating its size.
- Leaving NaN and float dtypes in the key columns.

### Q27 ⭐ 🔴 Plain Python BFS and DFS against SQL: friendships and flights as edge lists. Write BFS (collections.deque) for shortest distance and connected components and DFS (stack) for all simple paths, then check results against the SQL recursive CTE answers with asserts. Say in the answer that networkx 3.6.1 is installed in this environment and scipy is not, show the networkx call (shortest_path_length, connected_components) as the library check, and keep the plain-Python version as the interview answer. Explain the equivalence between a BFS queue and the SQLite recursive queue with ORDER BY level.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** In plain Python I keep an adjacency dict, use a `collections.deque` queue for BFS (shortest distance in an unweighted graph, connected components) and a stack for DFS (all simple paths), then check each result against the SQL recursive CTE and against networkx; a SQLite recursive CTE is itself a queue, and with no `ORDER BY` it is the BFS queue.

**Schema and sample data:** `friendships(user_a, user_b)` stores each undirected friendship once: 1-2, 1-3, 2-4, 3-4, 4-5, 5-6 (one cluster), 7-8, 8-9 (a second cluster), and user 10 has no friends and is only in `nodes`. `flights(src, dst, cost)` is directed: DEL to BOM and HYD, BOM and HYD connect to each other, both reach BLR, and BLR flies back to DEL (a loop).
```sql
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER);
INSERT INTO friendships VALUES (1,2),(1,3),(2,4),(3,4),(4,5),(5,6),(7,8),(8,9);
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BOM',100),('DEL','HYD',80),('BOM','HYD',20),('HYD','BOM',25),
 ('BOM','BLR',90),('HYD','BLR',70),('BLR','DEL',150);
```

**SQL answer:** `SQL_DIST`, `SQL_COMP`, `SQL_PATHS` and `SQL_QUEUE` in the Code block. The undirected edge list is symmetrised in a plain (non-recursive) CTE `e` and distances from user 1 are `MIN(dist)` per node, with a depth cap of 10 as the guard:
```sql
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
)
SELECT node, MIN(dist) AS dist FROM r GROUP BY node ORDER BY dist, node
```
Components as "smallest id reachable" (closure with `UNION`, so it ends by itself):
```sql
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), reach(src, dst) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT reach.src, e.b FROM reach JOIN e ON e.a = reach.dst
)
SELECT src AS node, MIN(dst) AS component FROM reach GROUP BY src ORDER BY src
```
All simple routes DEL to BLR with a path-string guard:
```sql
WITH RECURSIVE p(node, path, cost) AS (
  SELECT 'DEL', ',DEL,', 0
  UNION ALL
  SELECT f.dst, p.path || f.dst || ',', p.cost + f.cost
  FROM p JOIN flights f ON f.src = p.node
  WHERE instr(p.path, ',' || f.dst || ',') = 0
)
SELECT trim(path, ',') AS route, cost FROM p WHERE node = 'BLR' ORDER BY cost, route
```

**pandas answer:** this is a question about algorithms, so the interview answer is plain Python, not pandas; the DataFrames are only the carrier (`pd.DataFrame(...)` of the results compared with the SQL frames). Shown once here and identical to the Code block:
```py
def adjacency(pairs, directed):
    g = {}
    for a, b in pairs:
        g.setdefault(a, []).append(b)
        g.setdefault(b, [])
        if not directed:
            g[b].append(a)
    return {k: sorted(v) for k, v in g.items()}

def bfs_distance(g, start):
    dist, queue, order = {start: 0}, deque([start]), [start]
    while queue:
        u = queue.popleft()
        for v in g[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
                order.append(v)
    return dist, order

def components(g):
    comp = {}
    for s in sorted(g):
        if s in comp:
            continue
        label, queue = s, deque([s])         # s is the smallest unseen node, so it is the component's smallest id
        comp[s] = label
        while queue:
            u = queue.popleft()
            for v in g[u]:
                if v not in comp:
                    comp[v] = label
                    queue.append(v)
    return comp

def all_simple_paths(g, cost, start, goal):
    out, stack = [], [(start, [start], 0)]
    while stack:
        u, path, total = stack.pop()
        if u == goal:
            out.append((">".join(path), total))
            continue
        for v in g[u]:
            if v not in path:
                stack.append((v, path + [v], total + cost[(u, v)]))
    return sorted(out, key=lambda t: (t[1], t[0]))
```
The library check (also in the Code block): `nx.shortest_path_length(G, 1)`, `nx.connected_components(G)` and `nx.all_simple_paths(D, "DEL", "BLR")`, called as written at run time with networkx 3.6.1. scipy is not installed in this environment, so I did not use `scipy.sparse.csgraph`.

**Example:** BFS from user 1: queue `[1]`; pop 1, neighbours 2 and 3 get distance 1; pop 2, neighbour 4 gets distance 2; pop 3, its neighbour 4 is already seen; pop 4, neighbour 5 gets 3; pop 5, neighbour 6 gets 4; the queue empties. Distances 1:0, 2:1, 3:1, 4:2, 5:3, 6:4; users 7, 8, 9, 10 are never reached. Components: BFS from the smallest unseen node labels the whole cluster with that node: {1..6} gets 1, {7, 8, 9} gets 7, {10} gets 10, matching the SQL "smallest reachable id". DFS with a stack from DEL to BLR (never stepping to a node already on the path): DEL, HYD, BLR (150); DEL, BOM, BLR (190); DEL, BOM, HYD, BLR (190); DEL, HYD, BOM, BLR (195). The loop BLR to DEL is never used because DEL is already on every path.

**Code:** run with `python3 -I`. The SQL frames and the Python results are compared after ordering by `dist, node` (distances), `node` (components) and `cost, route` (flight routes); networkx results are asserted equal; the last block prints the SQLite queue order.
```python
import sqlite3
from collections import deque
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER);
INSERT INTO friendships VALUES (1,2),(1,3),(2,4),(3,4),(4,5),(5,6),(7,8),(8,9);
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BOM',100),('DEL','HYD',80),('BOM','HYD',20),('HYD','BOM',25),
 ('BOM','BLR',90),('HYD','BLR',70),('BLR','DEL',150);
"""
SQL_DIST = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
)
SELECT node, MIN(dist) AS dist FROM r GROUP BY node ORDER BY dist, node
"""
SQL_COMP = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), reach(src, dst) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT reach.src, e.b FROM reach JOIN e ON e.a = reach.dst
)
SELECT src AS node, MIN(dst) AS component FROM reach GROUP BY src ORDER BY src
"""
SQL_PATHS = """
WITH RECURSIVE p(node, path, cost) AS (
  SELECT 'DEL', ',DEL,', 0
  UNION ALL
  SELECT f.dst, p.path || f.dst || ',', p.cost + f.cost
  FROM p JOIN flights f ON f.src = p.node
  WHERE instr(p.path, ',' || f.dst || ',') = 0
)
SELECT trim(path, ',') AS route, cost FROM p WHERE node = 'BLR' ORDER BY cost, route
"""
SQL_QUEUE = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
  {order}
)
SELECT node, dist FROM r
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_dist = pd.read_sql_query(SQL_DIST, con)
sql_comp = pd.read_sql_query(SQL_COMP, con)
sql_paths = pd.read_sql_query(SQL_PATHS, con)
friends = pd.read_sql_query("SELECT * FROM friendships", con)
flights = pd.read_sql_query("SELECT * FROM flights", con)
all_nodes = [r[0] for r in con.execute("SELECT node_id FROM nodes ORDER BY 1")]

# pd:main
def adjacency(pairs, directed):
    g = {}
    for a, b in pairs:
        g.setdefault(a, []).append(b)
        g.setdefault(b, [])
        if not directed:
            g[b].append(a)
    return {k: sorted(v) for k, v in g.items()}

def bfs_distance(g, start):
    dist, queue, order = {start: 0}, deque([start]), [start]
    while queue:
        u = queue.popleft()
        for v in g[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
                order.append(v)
    return dist, order

def components(g):
    comp = {}
    for s in sorted(g):
        if s in comp:
            continue
        label, queue = s, deque([s])         # s is the smallest unseen node, so it is the component's smallest id
        comp[s] = label
        while queue:
            u = queue.popleft()
            for v in g[u]:
                if v not in comp:
                    comp[v] = label
                    queue.append(v)
    return comp

def all_simple_paths(g, cost, start, goal):
    out, stack = [], [(start, [start], 0)]
    while stack:
        u, path, total = stack.pop()
        if u == goal:
            out.append((">".join(path), total))
            continue
        for v in g[u]:
            if v not in path:
                stack.append((v, path + [v], total + cost[(u, v)]))
    return sorted(out, key=lambda t: (t[1], t[0]))
# pd:end

g = adjacency(zip(friends["user_a"], friends["user_b"]), directed=False)
for n in all_nodes:
    g.setdefault(n, [])
dist, bfs_order = bfs_distance(g, 1)
py_dist = pd.DataFrame(sorted(dist.items(), key=lambda t: (t[1], t[0])), columns=["node", "dist"])
# compare after ordering by dist, node (the SQL ORDER BY)
pd.testing.assert_frame_equal(py_dist, sql_dist, check_dtype=False)
comp = components(g)
py_comp = pd.DataFrame(sorted(comp.items()), columns=["node", "component"])
pd.testing.assert_frame_equal(py_comp, sql_comp, check_dtype=False)
fg = adjacency(zip(flights["src"], flights["dst"]), directed=True)
cost = {(s, d): c for s, d, c in zip(flights["src"], flights["dst"], flights["cost"])}
py_paths = pd.DataFrame(all_simple_paths(fg, cost, "DEL", "BLR"), columns=["route", "cost"])
sql_paths["route"] = sql_paths["route"].str.replace(",", ">")
pd.testing.assert_frame_equal(py_paths, sql_paths, check_dtype=False)
print("plain Python BFS distances, components and DFS simple paths equal the SQL results")
print("distances from user 1:", dict(zip(py_dist["node"], py_dist["dist"])))
print("components (node -> smallest id):", comp)
print(py_paths.to_string(index=False))

# networkx as the library check
G = nx.Graph(list(zip(friends["user_a"], friends["user_b"])))
G.add_nodes_from(all_nodes)
assert dict(nx.shortest_path_length(G, 1)) == dist
nx_comp = sorted(sorted(c) for c in nx.connected_components(G))
assert nx_comp == sorted(sorted(n for n, c in comp.items() if c == lab) for lab in set(comp.values()))
D = nx.DiGraph([(s, d) for s, d in zip(flights["src"], flights["dst"])])
nx_paths = sorted(">".join(p) for p in nx.all_simple_paths(D, "DEL", "BLR"))
assert nx_paths == sorted(py_paths["route"])
print("networkx", nx.__version__, "agrees: shortest_path_length, connected_components", nx_comp, "all_simple_paths", len(nx_paths))

# SQLite queue: default FIFO order is BFS; ORDER BY in the recursive select changes the queue to LIFO (DFS-like)
fifo = con.execute(SQL_QUEUE.format(order="")).fetchall()
lifo = con.execute(SQL_QUEUE.format(order="ORDER BY 2 DESC")).fetchall()
print("\nSQLite queue order, FIFO (no ORDER BY):", [f"{n}@{d}" for n, d in fifo])
print("SQLite queue order, ORDER BY dist DESC:", [f"{n}@{d}" for n, d in lifo])
print("Python BFS visit order                :", bfs_order)
assert [d for _, d in fifo] == sorted(d for _, d in fifo)
assert sorted(fifo) == sorted(lifo)
print("asserts passed")
```

**Output (my run):**
```text
plain Python BFS distances, components and DFS simple paths equal the SQL results
distances from user 1: {1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 6: 4}
components (node -> smallest id): {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 7, 8: 7, 9: 7, 10: 10}
          route  cost
    DEL>HYD>BLR   150
    DEL>BOM>BLR   190
DEL>BOM>HYD>BLR   190
DEL>HYD>BOM>BLR   195
networkx 3.6.1 agrees: shortest_path_length, connected_components [[1, 2, 3, 4, 5, 6], [7, 8, 9], [10]] all_simple_paths 4

SQLite queue order, FIFO (no ORDER BY): ['1@0', '2@1', '3@1', '1@2', '4@2', '2@3', '3@3', '5@3', '1@4', '4@4', '6@4', '2@5', '3@5', '5@5', '1@6', '4@6', '6@6', '2@7', '3@7', '5@7', '1@8', '4@8', '6@8', '2@9', '3@9', '5@9', '1@10', '4@10', '6@10']
SQLite queue order, ORDER BY dist DESC: ['1@0', '2@1', '1@2', '2@3', '1@4', '2@5', '1@6', '2@7', '1@8', '2@9', '1@10', '4@10', '3@9', '4@8', '5@9', '6@10', '3@7', '4@6', '5@7', '6@8', '3@5', '4@4', '5@5', '6@6', '3@3', '4@2', '5@3', '6@4', '3@1']
Python BFS visit order                : [1, 2, 3, 4, 5, 6]
asserts passed
```

**Edge cases:**
- Isolated node (10): BFS never reaches it from 1, and it needs its own component label; SQL only has it because it comes from the `nodes` table, not from the edge list. Components computed from edges alone would silently drop it.
- Undirected storage (each friendship once): the SQL needs the symmetric edge list; forgetting it makes distances direction-dependent. Python's `adjacency(..., directed=False)` adds both directions.
- Cycle (BLR back to DEL): BFS needs a visited/distance dict, DFS needs "not already on the path"; without them both loop forever.
- Two routes with the same cost (190): both are returned; the sort by `cost, route` makes the order deterministic.
- No route: BFS leaves the node out of `dist`, the SQL has no row, networkx raises `NetworkXNoPath` for `shortest_path` (from its documentation; not run here).
- The SQLite queue in my run (surprise): with `UNION` deduplicating whole rows `(node, dist)`, a node is revisited at each new distance (the FIFO output contains `1@2`, `1@4`, `1@6`, ... because friend 2 leads back to user 1) until the depth cap ends it, so the distance has to be taken with `MIN(dist)` per node, as `SQL_DIST` does. Dedup by node alone, as Python's `dist` dict does, would need the distance not to be a column, which is why SQL BFS needs the cap and the `MIN`.

**Then explain:**
- BFS equals the SQLite recursive queue: the engine takes the oldest row from the queue, runs the recursive select on it, appends the results, so rows come out in order of distance; in my run the distance column of the FIFO output is non-decreasing (asserted). With `ORDER BY dist DESC` in the recursive select the newest and deepest row is taken first (last-in-first-out), which is the depth-first style (SQLite documents `ORDER BY` as the queue order); the output above shows the deep rows first.
- Differences from Python: Python's BFS marks a node visited once and never expands it again; the SQL carries the distance as data, so it re-expands unless the depth cap, a path string or `UNION` on node-only rows stops it.
- Complexity: BFS and DFS visit each node and edge once, O(V + E). Enumerating all simple paths is exponential in the worst case (Q23, Q29).
- Components: repeated BFS from unseen nodes; labelling by the smallest id matches the SQL.
- networkx is the check, not the interview answer: `connected_components` yields sets, `shortest_path_length` returns a dict of distances, `all_simple_paths` yields node lists; I compared them with the plain Python results.

**Follow-ups:**
- Shortest path with weights? Dijkstra with `heapq` (Q23).
- Friends of friends (distance exactly 2, not already friends)? Filter `dist == 2` from the BFS (Q11 shows the SQL).
- BFS on a huge graph? Not in SQL; a graph library or an engine with graph support (not covered here).

**Common mistakes:**
- Marking visited when popping instead of when pushing (the same node gets queued many times).
- Using a list as a queue with `pop(0)` (O(n) per pop); use `deque`.
- Using the edge list for components and losing isolated nodes.
- Forgetting the symmetric edges for an undirected graph.
- Treating `UNION` in a recursive CTE as BFS dedup by node when the distance is a column (it dedups by `(node, dist)`).

### Q28 ⭐ 🔴 SQL versus pandas on cycles, NULL parents and duplicate edges: build one edge table with a duplicate edge row, a NULL parent that is a real root, an edge pointing to an unknown parent and a 2-cycle. Show for each of the recursive CTE (UNION ALL, UNION, with path guard) and the pandas merge loop what happens: duplicated output rows, double counted salaries in a roll-up, missed root when a NULL join key never matches in SQL but does match in pandas merge, infinite loop versus visited-set termination. Return a compact table of behaviours and the cleaning steps (drop_duplicates, flag orphans, break cycles) that make both engines agree.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** The same dirty edge table makes SQL and pandas disagree in four ways: a repeated edge row double counts in both (UNION ALL rows and an unguarded merge loop), a NULL parent never matches in a SQL join but matches in a pandas `merge`, an orphan is silently invisible from the root in both, and a loop runs forever in both unless you add a guard (path string, `UNION` on bare ids, depth cap, or a visited set); after cleaning (drop duplicates, set orphans aside, break loops) the two engines agree.

**Schema and sample data:** one table with no primary key so a loader can repeat a row: emp 1 is the real root (NULL manager), 2 and 3 report to 1, the row for 3 appears twice (duplicate edge), 4 reports to 2, emp 5 points to manager 99 who does not exist (orphan), and 6 and 7 manage each other (a 2-cycle that is not connected to the root). Salaries are toy column data.
```sql
CREATE TABLE employees(emp_id INTEGER, manager_id INTEGER, salary INTEGER);   -- no primary key: a loader may repeat a row
INSERT INTO employees VALUES
 (1,NULL,100),   -- real root: NULL manager
 (2,1,50),(3,1,40),(3,1,40),   -- the last two rows are the same edge twice
 (4,2,30),
 (5,99,35),      -- 99 does not exist: orphan
 (6,7,20),(7,6,25);   -- 2-cycle, unreachable from the root
```

**SQL answer:** `SQL_ROLLUP` in the Code block is the roll-up from the NULL root with `UNION ALL` and a depth cap. The other statements used for the table of behaviours are `SQL_NULL_ANCHOR` (the same text with `manager_id = NULL`), `SQL_CYCLE_ALL` (from the loop, with a guard that I swap), `SQL_UNION_BARE`, `SQL_UNION_LEVEL`, `SQL_PATH`, `SQL_PEERS`, `SQL_LOOPERS` and `SQL_CLEAN`.
```sql
WITH RECURSIVE t(emp_id, level, salary) AS (
  SELECT emp_id, 0, salary FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, t.level + 1, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 10
)
SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people, SUM(salary) AS total_salary FROM t
```
Starting from the loop (emp 6), with a path guard:
```sql
WITH RECURSIVE t(emp_id, path) AS (
  SELECT emp_id, ',' || emp_id || ',' FROM employees WHERE emp_id = 6
  UNION ALL
  SELECT e.emp_id, t.path || e.emp_id || ','
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE instr(t.path, ',' || e.emp_id || ',') = 0
)
SELECT COUNT(*) AS result_rows FROM t
```
Detecting loop members (transitive closure of the manager link with `UNION`, so it ends by itself):
```sql
WITH RECURSIVE w(start, cur) AS (
  SELECT emp_id, manager_id FROM employees WHERE manager_id IS NOT NULL
  UNION
  SELECT w.start, e.manager_id FROM w JOIN employees e ON e.emp_id = w.cur WHERE e.manager_id IS NOT NULL
)
SELECT DISTINCT start FROM w WHERE cur = start ORDER BY 1
```
Cleaning in SQL: `DISTINCT` removes the repeated row, the `WHERE` keeps real roots and rows whose manager exists (the orphan is set aside), and the loop is broken at its smallest id by nulling that manager:
```sql
CREATE TABLE emp_clean AS
SELECT DISTINCT emp_id,
       CASE WHEN emp_id IN (SELECT start FROM ({loopers})) AND emp_id = (SELECT MIN(start) FROM ({loopers}))
            THEN NULL ELSE manager_id END AS manager_id,
       salary
FROM employees e
WHERE manager_id IS NULL OR EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
```

**pandas answer:** `reports` is the frontier merge from given root ids with an optional guard (visited set plus `drop_duplicates`), `clean` is the same three cleaning steps as the SQL, and `loop_members` walks the manager chain. Shown once here and identical to the Code block:
```py
def reports(emp, roots, guard=True, cap=10):
    """Frontier merge from the given root ids; returns one row per output row (emp_id, level, salary)."""
    kids = emp.rename(columns={"emp_id": "child", "salary": "child_salary"})
    frontier = emp[emp["emp_id"].isin(roots)].rename(columns={"salary": "child_salary"}).assign(child=lambda d: d["emp_id"], level=0)
    frontier = frontier[["child", "child_salary", "level"]]
    parts, seen = [frontier], set(frontier["child"])
    for _ in range(cap):
        nxt = frontier.merge(kids, left_on="child", right_on="manager_id", suffixes=("_p", ""))
        if guard:
            nxt = nxt[~nxt["child"].isin(seen)].drop_duplicates("child")
        frontier = pd.DataFrame({"child": nxt["child"], "child_salary": nxt["child_salary"], "level": nxt["level"] + 1})
        if not len(frontier):
            break
        seen.update(frontier["child"])
        parts.append(frontier)
    out = pd.concat(parts, ignore_index=True)
    return out.rename(columns={"child": "emp_id", "child_salary": "salary"})

def clean(emp):
    emp = emp.drop_duplicates()                                                     # repeated edge rows
    orphan = emp["manager_id"].notna() & ~emp["manager_id"].isin(emp["emp_id"])     # unknown manager: set aside
    emp = emp[~orphan]
    loops = loop_members(emp)
    if loops:
        emp = emp.assign(manager_id=emp["manager_id"].where(emp["emp_id"] != min(loops)))   # break each loop at its smallest id
    return emp.reset_index(drop=True)

def loop_members(emp):
    par = dict(zip(emp["emp_id"], emp["manager_id"]))
    out = set()
    for s in par:
        cur, hops = par[s], 0
        while pd.notna(cur) and cur in par and hops <= len(par):
            if cur == s:
                out.add(s)
                break
            cur, hops = par[cur], hops + 1
    return out
```

**Example:** from the real root, by hand. Level 0: emp 1 (100). Level 1: rows whose manager is 1: emp 2 (50), emp 3 (40) and emp 3 again (40) because the edge is stored twice. Level 2: the reports of 2 (emp 4, 30) and the reports of 3 (nobody). That is 5 output rows, 4 distinct people, and salary 100 + 50 + 40 + 40 + 30 = 260, while the true total is 220: the duplicate edge double counted emp 3. Emp 5 (35) is never reached because its manager 99 is not in the table, so a roll-up from the root silently leaves 35 out. Emp 6 and 7 are not reachable from the root either; started from emp 6, a `UNION ALL` bounces 6, 7, 6, 7 forever (6 rows with a depth cap of 5, 8 rows when the outer query has `LIMIT 8`). After cleaning there are two roots (1 and the loop-breaker 6) and the roll-up is 6 rows and 265 (220 for the tree of 1 plus 20 + 25 for 6 and 7; orphan 35 left out on purpose).

**Behaviours (every number from the run below):**

| Situation | SQL (SQLite 3.45.1) | pandas merge loop |
|---|---|---|
| Duplicate edge row, `UNION ALL` / no guard | 5 rows, 4 people, salary 260 | same: 5 rows, 4 people, 260 |
| Duplicate edge row, visited set (pandas) / drop duplicates first | `UNION` on `(emp_id, salary)` hides it only if rows match exactly; the clean way is to dedupe the table | 4 rows, 4 people, 220 |
| Root found by a NULL test | `manager_id IS NULL` finds it; `manager_id = NULL` returns 0 rows and the recursion never starts | `isna()` finds it; `== np.nan` selects 0 rows |
| NULL key in a join (same-manager pairs) | 13 rows: the NULL root never matches | 14 rows: NaN matches NaN; 13 after `dropna` |
| Orphan (manager 99 does not exist) | not reached from the root, no error | same: not reached, no error |
| Loop from emp 6 | `UNION ALL` with depth cap 5: 6 rows; unguarded with outer `LIMIT 8`: 8 rows; path guard: 2 rows; `UNION` on bare ids: 2 rows; `UNION` with a level column and cap 10: 11 rows | no guard with cap 5: 6 rows (never ends without the cap); visited set: 2 rows |

**Code:** run with `python3 -I`. The SQL and pandas cleaned tables are compared after ordering by `emp_id`; the roll-ups after cleaning are compared as (rows, distinct people, salary total).
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER, manager_id INTEGER, salary INTEGER);   -- no primary key: a loader may repeat a row
INSERT INTO employees VALUES
 (1,NULL,100),   -- real root: NULL manager
 (2,1,50),(3,1,40),(3,1,40),   -- the last two rows are the same edge twice
 (4,2,30),
 (5,99,35),      -- 99 does not exist: orphan
 (6,7,20),(7,6,25);   -- 2-cycle, unreachable from the root
"""
SQL_ROLLUP = """
WITH RECURSIVE t(emp_id, level, salary) AS (
  SELECT emp_id, 0, salary FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, t.level + 1, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 10
)
SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people, SUM(salary) AS total_salary FROM t
"""
SQL_NULL_ANCHOR = SQL_ROLLUP.replace("manager_id IS NULL", "manager_id = NULL")
SQL_CYCLE_ALL = """
WITH RECURSIVE t(emp_id, level, salary) AS (
  SELECT emp_id, 0, salary FROM employees WHERE emp_id = 6
  UNION ALL
  SELECT e.emp_id, t.level + 1, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
  {guard}
)
SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people FROM t
"""
SQL_UNION_BARE = """
WITH RECURSIVE t(emp_id, salary) AS (
  SELECT emp_id, salary FROM employees WHERE emp_id = 6
  UNION
  SELECT e.emp_id, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
)
SELECT COUNT(*) AS result_rows FROM t
"""
SQL_UNION_LEVEL = """
WITH RECURSIVE t(emp_id, level) AS (
  SELECT emp_id, 0 FROM employees WHERE emp_id = 6
  UNION
  SELECT e.emp_id, t.level + 1 FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 10
)
SELECT COUNT(*) AS result_rows FROM t
"""
SQL_PATH = """
WITH RECURSIVE t(emp_id, path) AS (
  SELECT emp_id, ',' || emp_id || ',' FROM employees WHERE emp_id = 6
  UNION ALL
  SELECT e.emp_id, t.path || e.emp_id || ','
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE instr(t.path, ',' || e.emp_id || ',') = 0
)
SELECT COUNT(*) AS result_rows FROM t
"""
SQL_PEERS = "SELECT COUNT(*) FROM employees a JOIN employees b ON a.manager_id = b.manager_id"
SQL_LOOPERS = """
WITH RECURSIVE w(start, cur) AS (
  SELECT emp_id, manager_id FROM employees WHERE manager_id IS NOT NULL
  UNION
  SELECT w.start, e.manager_id FROM w JOIN employees e ON e.emp_id = w.cur WHERE e.manager_id IS NOT NULL
)
SELECT DISTINCT start FROM w WHERE cur = start ORDER BY 1
"""
SQL_CHECKS = {
  "duplicate emp_id rows": "SELECT emp_id FROM employees GROUP BY emp_id HAVING COUNT(*) > 1",
  "orphans": "SELECT emp_id FROM employees e WHERE manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)",
  "roots": "SELECT DISTINCT emp_id FROM employees WHERE manager_id IS NULL",
}
SQL_CLEAN = """
CREATE TABLE emp_clean AS
SELECT DISTINCT emp_id,
       CASE WHEN emp_id IN (SELECT start FROM ({loopers})) AND emp_id = (SELECT MIN(start) FROM ({loopers}))
            THEN NULL ELSE manager_id END AS manager_id,
       salary
FROM employees e
WHERE manager_id IS NULL OR EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda sql: con.execute(sql).fetchall()
print("raw table: duplicates", [r[0] for r in q(SQL_CHECKS["duplicate emp_id rows"])], "| orphans", [r[0] for r in q(SQL_CHECKS["orphans"])],
      "| roots", [r[0] for r in q(SQL_CHECKS["roots"])], "| members of a loop", [r[0] for r in q(SQL_LOOPERS)])
sql_raw = q(SQL_ROLLUP)[0]
print("SQL UNION ALL from the NULL root (rows, people, salary):", sql_raw, "| true salary of root 1's tree is 220")
print("SQL anchor written as manager_id = NULL:", q(SQL_NULL_ANCHOR)[0])
cycle_runs = {
    "UNION ALL, depth cap 5": q(SQL_CYCLE_ALL.format(guard="WHERE t.level < 5"))[0][0],
    "UNION ALL, no guard, outer LIMIT 8": len(q(SQL_CYCLE_ALL.format(guard="").replace(
        "SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people FROM t", "SELECT * FROM t LIMIT 8"))),
    "UNION ALL, path guard": q(SQL_PATH)[0][0],
    "UNION on (emp_id, salary), no level column": q(SQL_UNION_BARE)[0][0],
    "UNION with a level column, cap 10": q(SQL_UNION_LEVEL)[0][0],
}
print("SQL from the loop (anchor emp 6), result rows:", cycle_runs)
sql_peers = q(SQL_PEERS)[0][0]

employees = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
def reports(emp, roots, guard=True, cap=10):
    """Frontier merge from the given root ids; returns one row per output row (emp_id, level, salary)."""
    kids = emp.rename(columns={"emp_id": "child", "salary": "child_salary"})
    frontier = emp[emp["emp_id"].isin(roots)].rename(columns={"salary": "child_salary"}).assign(child=lambda d: d["emp_id"], level=0)
    frontier = frontier[["child", "child_salary", "level"]]
    parts, seen = [frontier], set(frontier["child"])
    for _ in range(cap):
        nxt = frontier.merge(kids, left_on="child", right_on="manager_id", suffixes=("_p", ""))
        if guard:
            nxt = nxt[~nxt["child"].isin(seen)].drop_duplicates("child")
        frontier = pd.DataFrame({"child": nxt["child"], "child_salary": nxt["child_salary"], "level": nxt["level"] + 1})
        if not len(frontier):
            break
        seen.update(frontier["child"])
        parts.append(frontier)
    out = pd.concat(parts, ignore_index=True)
    return out.rename(columns={"child": "emp_id", "child_salary": "salary"})

def clean(emp):
    emp = emp.drop_duplicates()                                                     # repeated edge rows
    orphan = emp["manager_id"].notna() & ~emp["manager_id"].isin(emp["emp_id"])     # unknown manager: set aside
    emp = emp[~orphan]
    loops = loop_members(emp)
    if loops:
        emp = emp.assign(manager_id=emp["manager_id"].where(emp["emp_id"] != min(loops)))   # break each loop at its smallest id
    return emp.reset_index(drop=True)

def loop_members(emp):
    par = dict(zip(emp["emp_id"], emp["manager_id"]))
    out = set()
    for s in par:
        cur, hops = par[s], 0
        while pd.notna(cur) and cur in par and hops <= len(par):
            if cur == s:
                out.add(s)
                break
            cur, hops = par[cur], hops + 1
    return out
# pd:end

root = employees[employees["manager_id"].isna()]["emp_id"].tolist()
raw = reports(employees, root, guard=False)
assert (len(raw), raw["emp_id"].nunique(), int(raw["salary"].sum())) == sql_raw
print("\npandas merge loop from the NaN root, no guard:", (len(raw), raw["emp_id"].nunique(), int(raw["salary"].sum())), "(same as SQL UNION ALL)")
guarded = reports(employees, root, guard=True)
print("pandas with visited set + drop_duplicates:", (len(guarded), guarded["emp_id"].nunique(), int(guarded["salary"].sum())))
print("pandas employees.manager_id == np.nan selects", int((employees["manager_id"] == float("nan")).sum()), "rows; isna() selects", len(root))
cyc_nog = reports(employees, [6], guard=False, cap=5)
cyc_g = reports(employees, [6], guard=True)
print("pandas from the loop: no guard, cap 5 ->", len(cyc_nog), "rows; visited set ->", len(cyc_g), "rows")
pd_peers = len(employees.merge(employees, on="manager_id"))
pd_peers_fixed = len(employees.dropna(subset=["manager_id"]).merge(employees.dropna(subset=["manager_id"]), on="manager_id"))
print("same-manager pairs: SQL", sql_peers, "| pandas merge", pd_peers, "| pandas after dropna", pd_peers_fixed)
assert pd_peers == sql_peers + 1 and pd_peers_fixed == sql_peers

# cleaning: dedupe, set aside orphans, break loops; then both engines must agree
con.execute(SQL_CLEAN.format(loopers=SQL_LOOPERS.strip().replace(chr(10), " ")))
clean_sql = pd.read_sql_query("SELECT * FROM emp_clean ORDER BY emp_id", con)
clean_pd = clean(employees).sort_values("emp_id").reset_index(drop=True)
clean_sql["manager_id"] = clean_sql["manager_id"].astype("Int64")
clean_pd["manager_id"] = clean_pd["manager_id"].astype("Int64")
pd.testing.assert_frame_equal(clean_pd, clean_sql, check_dtype=False)
print("\ncleaned table (SQL and pandas identical after sorting by emp_id):")
print(clean_sql.to_string(index=False))
sql_clean_roll = con.execute(SQL_ROLLUP.replace("FROM employees", "FROM emp_clean").replace("JOIN employees", "JOIN emp_clean")).fetchone()
roots_clean = clean_pd[clean_pd["manager_id"].isna()]["emp_id"].tolist()
pd_clean_roll = reports(clean_pd, roots_clean, guard=False)
assert sql_clean_roll == (len(pd_clean_roll), pd_clean_roll["emp_id"].nunique(), int(pd_clean_roll["salary"].sum()))
print("after cleaning, UNION ALL roll-up from all roots: SQL", sql_clean_roll, "| pandas", (len(pd_clean_roll), pd_clean_roll["emp_id"].nunique(), int(pd_clean_roll["salary"].sum())), "no guard needed")
print("asserts passed")
```

**Output (my run):**
```text
raw table: duplicates [3] | orphans [5] | roots [1] | members of a loop [6, 7]
SQL UNION ALL from the NULL root (rows, people, salary): (5, 4, 260) | true salary of root 1's tree is 220
SQL anchor written as manager_id = NULL: (0, 0, None)
SQL from the loop (anchor emp 6), result rows: {'UNION ALL, depth cap 5': 6, 'UNION ALL, no guard, outer LIMIT 8': 8, 'UNION ALL, path guard': 2, 'UNION on (emp_id, salary), no level column': 2, 'UNION with a level column, cap 10': 11}

pandas merge loop from the NaN root, no guard: (5, 4, 260) (same as SQL UNION ALL)
pandas with visited set + drop_duplicates: (4, 4, 220)
pandas employees.manager_id == np.nan selects 0 rows; isna() selects 1
pandas from the loop: no guard, cap 5 -> 6 rows; visited set -> 2 rows
same-manager pairs: SQL 13 | pandas merge 14 | pandas after dropna 13

cleaned table (SQL and pandas identical after sorting by emp_id):
 emp_id  manager_id  salary
      1        <NA>     100
      2           1      50
      3           1      40
      4           2      30
      6        <NA>      20
      7           6      25
after cleaning, UNION ALL roll-up from all roots: SQL (6, 6, 265) | pandas (6, 6, 265) no guard needed
asserts passed
```

**Edge cases:**
- Duplicate edges: the full-row duplicate (3, 1, 40) is removed by `DISTINCT` or `drop_duplicates()`. If the duplicates differ in salary (a data error, not run here), `DISTINCT` keeps both and the cleaning needs a rule for which to keep.
- NULL parent that is a real root: keep it as a root; do not drop it, and do not join on it. The pandas merge matching NaN to NaN is a bug source in sibling-style joins (14 versus 13 pairs in the table above; Q25 shows 20 versus 19 on its own tree) but it is also why a pandas anchor test with `==` fails silently.
- Orphan: decide a policy (treat as a root, quarantine, or fail the load). I set it aside, so its salary (35) is not in the 265 total; a policy of "treat as a root" would add it.
- 2-cycle that is not reachable from the root: a roll-up from the root never sees it, so it does not hang; it hangs only when you start from a member (or start from every row). `UNION` with a level column does not stop a loop (11 rows until the cap), `UNION` on bare ids does.
- Self-managed row (`emp_id = manager_id`): a loop of length 1; `SQL_LOOPERS` finds it (start = cur); not in the sample data and not run here.
- Empty table: the anchor returns nothing, SQL and pandas both return empty results; not run for this table.

**Then explain:**
- Why the engines differ: SQL three-valued logic makes `NULL = NULL` unknown, so it is not a match; pandas treats NaN keys as equal in `merge` by default.
- Why duplicates double count: a recursive CTE with `UNION ALL` and a merge loop both produce one output row per matching edge row; two identical edge rows give two rows per level.
- Guards compared: depth cap (finite, but wrong rows repeat), path string (exact for simple paths), `UNION` on columns that do not grow (cheap, hides duplicates), visited set in pandas (finite and exact).
- Cleaning order that makes both agree: dedupe, flag and set aside orphans, find loop members, break each loop at a deterministic member, then the data is a forest and `UNION ALL` is safe. I asserted the cleaned tables and roll-ups equal.
- Other engines: PostgreSQL 14+ `CYCLE`, SQL Server `MAXRECURSION`, MySQL `cte_max_recursion_depth` would stop or mark the loop differently (hedged, not executed).

**Follow-ups:**
- How do you stop this at load time? A primary key on `emp_id`, a foreign key on `manager_id`, and a check query for loops before publishing (a database cannot easily enforce acyclicity with a constraint).
- Which loop member do you break? Any deterministic rule (smallest id here); the business may have a better one, so report the loop rather than hide it.
- Is `UNION` always a safe guard? Only when the other columns cannot differ between visits; adding a depth or path column makes rows distinct again.

**Common mistakes:**
- Writing `manager_id = NULL` for the anchor (SQL) or `== np.nan` (pandas).
- Trusting a roll-up total without reconciling it to the table total (260 and 220 against 300 for the salaries of the seven distinct people in the table).
- Fixing a loop with a bigger depth cap.
- Dropping the NULL root to avoid the NaN merge problem.
- Comparing SQL and pandas outputs without cleaning and sorting first.

### Q29 ⭐ 🔴 Performance and safety of recursive queries: employees with 50,000 rows in a balanced tree (about 6 levels) and a chain table of 2,000 nodes in a straight line, plus a lattice DAG where the number of paths doubles per level. Time the subtree query with and without an index on manager_id, show EXPLAIN QUERY PLAN in SQLite (executed), show that UNION ALL path enumeration on the lattice explodes (count paths at 10, 15, 20 levels) while DISTINCT node reachability stays linear, and list the guards (depth counters, LIMIT in the recursive member, per-engine recursion limits, timeouts). Report the real timings honestly as machine specific.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** A recursive subtree query is fast when `manager_id` is indexed (each level is an index lookup per frontier row) and catastrophic when it is not, `UNION ALL` path enumeration on a DAG grows with the number of paths (doubling per level in my lattice) while `UNION` reachability stays linear in nodes, and the guards are a depth counter, `LIMIT`, `UNION` on non-growing columns and the engine's own recursion cap; every timing below is from one run on this machine and will differ on yours.

**Schema and sample data:** nothing small to check by hand here, so the data is generated in the Code block and the logic is checked on counts. `emp(emp_id INTEGER PRIMARY KEY, manager_id INTEGER)` has 50,000 rows in a balanced tree: emp 1 is the root and emp i (i >= 2) reports to `(i - 2) / 8 + 1`, so every manager has up to 8 reports and the deepest level is 6 (seven levels counting the root). `chain` has 2,000 nodes in a straight line (each reports to the previous). `lattice(src, dst)` has two nodes per level and every node links to both nodes of the next level, so the number of paths from the start doubles at each level.
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);          -- 50,000 rows, generated in Python
CREATE TABLE chain(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);        -- 2,000 rows, emp i reports to i - 1
CREATE TABLE lattice(src TEXT, dst TEXT);                                  -- (level l, a) to (level l+1, b) for a, b in {0, 1}
```

**SQL answer:** the subtree count (the template used for the tree and the chain; `{t}`, `{root}`, `{cap}` are filled in by the script) and the two lattice queries, all in the Code block:
```sql
WITH RECURSIVE s(emp_id, level) AS (
  SELECT emp_id, 0 FROM {t} WHERE emp_id = {root}
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM {t} e JOIN s ON e.manager_id = s.emp_id
  WHERE s.level < {cap}
)
SELECT COUNT(*) AS people, MAX(level) AS max_level FROM s
```
Path enumeration (one row per path) versus reachability (one row per node):
```sql
WITH RECURSIVE p(node, depth) AS (
  SELECT '0_0', 0
  UNION ALL
  SELECT l.dst, p.depth + 1 FROM p JOIN lattice l ON l.src = p.node
)
SELECT COUNT(*) AS rows_made, SUM(depth = {levels}) AS paths_to_last_level FROM p
```
```sql
WITH RECURSIVE r(node) AS (
  SELECT '0_0'
  UNION
  SELECT l.dst FROM r JOIN lattice l ON l.src = r.node
)
SELECT COUNT(*) AS nodes_reached FROM r
```

**pandas answer:** the frontier merge on the same 50,000-row frame (the count and the deepest level are asserted equal to the SQL result; the merge is on `Int64` ids). Shown once here and identical to the Code block:
```py
frontier = emp.loc[emp["emp_id"] == 2, ["emp_id"]].assign(level=0)
total, merges, deepest = 1, 0, 0
while len(frontier):
    nxt = frontier.merge(emp, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
    merges += 1
    frontier = pd.DataFrame({"emp_id": nxt["emp_id"], "level": nxt["level"] + 1})
    total += len(frontier)
    deepest = deepest + 1 if len(frontier) else deepest
```

**Example:** the subtree of manager 2 on the 50,000-row tree has 17,232 people and reaches level 5. The recursive step runs once per level but processes every frontier row: for each manager in the queue it needs "all employees with `manager_id` = this id". With an index on `manager_id` that is a lookup; without one, it is a scan of the table per frontier row. The plans I ran: default (SQLite built an automatic covering index and added a bloom filter: `SEARCH e USING AUTOMATIC COVERING INDEX (manager_id=?)`), automatic indexing switched off with no index (`SCAN e` inside the recursive step, a full table scan for each frontier row), and my own index (`SEARCH e USING COVERING INDEX emp_mgr (manager_id=?)`). Lattice by hand: level 1 has 2 paths, level 2 has 4, level l has 2^l; so 10 levels make 1,024 paths and 20 levels make 1,048,576, while the number of distinct nodes reached is 2 per level plus the start: 21, 31 and 41.

**Code:** run with `python3 -I`. It builds the data, prints `EXPLAIN QUERY PLAN`, times each variant (best of 3 runs, one run for the very slow no-index case), asserts the three subtree counts are identical and that the lattice counts equal 2^levels, and prints the pandas timing. The assertions cover correctness only; the printed seconds are machine specific.
```python
import sqlite3
import time
import pandas as pd

SQL_SUBTREE = """
WITH RECURSIVE s(emp_id, level) AS (
  SELECT emp_id, 0 FROM {t} WHERE emp_id = {root}
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM {t} e JOIN s ON e.manager_id = s.emp_id
  WHERE s.level < {cap}
)
SELECT COUNT(*) AS people, MAX(level) AS max_level FROM s
"""
SQL_PATHS = """
WITH RECURSIVE p(node, depth) AS (
  SELECT '0_0', 0
  UNION ALL
  SELECT l.dst, p.depth + 1 FROM p JOIN lattice l ON l.src = p.node
)
SELECT COUNT(*) AS rows_made, SUM(depth = {levels}) AS paths_to_last_level FROM p
"""
SQL_REACH = """
WITH RECURSIVE r(node) AS (
  SELECT '0_0'
  UNION
  SELECT l.dst FROM r JOIN lattice l ON l.src = r.node
)
SELECT COUNT(*) AS nodes_reached FROM r
"""

def timed(con, sql, repeat=3):
    best, res = None, None
    for _ in range(repeat):
        t0 = time.perf_counter()
        res = con.execute(sql).fetchone()
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    return res, best

def plan(con, sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

con = sqlite3.connect(":memory:")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__, "(all timings are from this machine and this run only)")
con.execute("CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, manager_id INTEGER)")
con.executemany("INSERT INTO emp VALUES (?, ?)", [(1, None)] + [(i, (i - 2) // 8 + 1) for i in range(2, 50001)])
con.execute("CREATE TABLE chain(emp_id INTEGER PRIMARY KEY, manager_id INTEGER)")
con.executemany("INSERT INTO chain VALUES (?, ?)", [(1, None)] + [(i, i - 1) for i in range(2, 2001)])
print("tree:", con.execute("SELECT COUNT(*), MAX(level) FROM (WITH RECURSIVE s(emp_id, level) AS (SELECT 1, 0 UNION ALL SELECT e.emp_id, s.level + 1 FROM emp e JOIN s ON e.manager_id = s.emp_id) SELECT * FROM s)").fetchone(),
      "(rows, deepest level); 8 children per node")

q2 = SQL_SUBTREE.format(t="emp", root=2, cap=100)
qroot = SQL_SUBTREE.format(t="emp", root=1, cap=100)
res = {}
print("\nSubtree of manager 2 on the 50,000-row table:")
con.execute("PRAGMA automatic_index = ON")
r, t = timed(con, q2)
res["default (automatic index allowed, no explicit index)"] = (r, t)
print("  plan:", plan(con, q2))
con.execute("PRAGMA automatic_index = OFF")
r, t = timed(con, q2, repeat=1)
res["automatic_index OFF, no index on manager_id"] = (r, t)
print("  plan:", plan(con, q2))
con.execute("CREATE INDEX emp_mgr ON emp(manager_id)")
r, t = timed(con, q2)
res["explicit index on manager_id"] = (r, t)
print("  plan:", plan(con, q2))
for k, (r, t) in res.items():
    print(f"  {k}: people={r[0]}, max_level={r[1]}, best time {t:.3f} s")
assert len({v[0] for v in res.values()}) == 1
r, t = timed(con, qroot)
print(f"Whole company (root 1) with the index: people={r[0]}, max_level={r[1]}, best time {t:.3f} s")

# pandas frontier merge on the same data
emp = pd.read_sql_query("SELECT * FROM emp", con)
emp["manager_id"] = emp["manager_id"].astype("Int64")
t0 = time.perf_counter()
# pd:main
frontier = emp.loc[emp["emp_id"] == 2, ["emp_id"]].assign(level=0)
total, merges, deepest = 1, 0, 0
while len(frontier):
    nxt = frontier.merge(emp, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
    merges += 1
    frontier = pd.DataFrame({"emp_id": nxt["emp_id"], "level": nxt["level"] + 1})
    total += len(frontier)
    deepest = deepest + 1 if len(frontier) else deepest
# pd:end
dt = time.perf_counter() - t0
assert (total, deepest) == res["explicit index on manager_id"][0]
print(f"pandas frontier merge, subtree of 2: people={total}, max_level={deepest}, {merges} merges, {dt:.3f} s")

print("\nChain of 2,000 nodes (depth 1999), with an index on manager_id:")
con.execute("CREATE INDEX chain_mgr ON chain(manager_id)")
r, t = timed(con, SQL_SUBTREE.format(t="chain", root=1, cap=5000))
print(f"  people={r[0]}, max_level={r[1]}, best time {t:.3f} s (no recursion limit in SQLite; a depth cap of 5000 was set by me)")
r2, _ = timed(con, SQL_SUBTREE.format(t="chain", root=1, cap=100), repeat=1)
print(f"  with the usual depth cap of 100 the answer is silently truncated: people={r2[0]}, max_level={r2[1]}")

print("\nLattice DAG: 2 nodes per level, every node links to both nodes of the next level; start at 0_0")
for levels in (10, 15, 20):
    con.execute("DROP TABLE IF EXISTS lattice")
    con.execute("CREATE TABLE lattice(src TEXT, dst TEXT)")
    con.executemany("INSERT INTO lattice VALUES (?, ?)",
                    [(f"{l}_{a}", f"{l + 1}_{b}") for l in range(levels) for a in (0, 1) for b in (0, 1)])
    con.execute("CREATE INDEX lattice_src ON lattice(src)")
    rp, tp = timed(con, SQL_PATHS.format(levels=levels), repeat=1)
    rr, tr = timed(con, SQL_REACH, repeat=1)
    assert rp[1] == 2 ** levels and rp[0] == 2 ** (levels + 1) - 1
    print(f"  {levels:2d} levels: UNION ALL made {rp[0]} rows, {rp[1]} paths to the last level (2^{levels}), {tp:.3f} s | "
          f"UNION reached {rr[0]} nodes, {tr:.4f} s")
print("asserts passed")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5 (all timings are from this machine and this run only)
tree: (50000, 6) (rows, deepest level); 8 children per node

Subtree of manager 2 on the 50,000-row table:
  plan: ['CO-ROUTINE s', 'SETUP', 'SEARCH emp USING INTEGER PRIMARY KEY (rowid=?)', 'RECURSIVE STEP', 'SCAN s', 'BLOOM FILTER ON e (manager_id=?)', 'SEARCH e USING AUTOMATIC COVERING INDEX (manager_id=?)', 'SCAN s']
  plan: ['CO-ROUTINE s', 'SETUP', 'SEARCH emp USING INTEGER PRIMARY KEY (rowid=?)', 'RECURSIVE STEP', 'SCAN s', 'SCAN e', 'SCAN s']
  plan: ['CO-ROUTINE s', 'SETUP', 'SEARCH emp USING INTEGER PRIMARY KEY (rowid=?)', 'RECURSIVE STEP', 'SCAN s', 'SEARCH e USING COVERING INDEX emp_mgr (manager_id=?)', 'SCAN s']
  default (automatic index allowed, no explicit index): people=17232, max_level=5, best time 0.012 s
  automatic_index OFF, no index on manager_id: people=17232, max_level=5, best time 19.968 s
  explicit index on manager_id: people=17232, max_level=5, best time 0.007 s
Whole company (root 1) with the index: people=50000, max_level=6, best time 0.020 s
pandas frontier merge, subtree of 2: people=17232, max_level=5, 6 merges, 0.015 s

Chain of 2,000 nodes (depth 1999), with an index on manager_id:
  people=2000, max_level=1999, best time 0.001 s (no recursion limit in SQLite; a depth cap of 5000 was set by me)
  with the usual depth cap of 100 the answer is silently truncated: people=101, max_level=100

Lattice DAG: 2 nodes per level, every node links to both nodes of the next level; start at 0_0
  10 levels: UNION ALL made 2047 rows, 1024 paths to the last level (2^10), 0.001 s | UNION reached 21 nodes, 0.0000 s
  15 levels: UNION ALL made 65535 rows, 32768 paths to the last level (2^15), 0.030 s | UNION reached 31 nodes, 0.0001 s
  20 levels: UNION ALL made 2097151 rows, 1048576 paths to the last level (2^20), 0.967 s | UNION reached 41 nodes, 0.0002 s
asserts passed
```

**Edge cases:**
- Timings in my run (SQLite 3.45.1, pandas 3.0.5, this machine only; yours will differ, so treat the ratios, not the seconds, as the finding): subtree of manager 2 (17,232 people) took 0.012 s with SQLite's automatic index, 0.007 s with an explicit index and 19.968 s with automatic indexing switched off and no index. The whole company (50,000 people) took 0.020 s with the index. The pandas frontier merge took 0.015 s for the same subtree with 6 merges. The answers were identical in all variants. So the missing index is not a small slowdown, it is the difference between milliseconds and tens of seconds, but SQLite hides it by default with an automatic index (not every engine does that, hedged).
- Chain of 2,000 nodes: with a depth cap of 5000 the full chain came back in about a millisecond (2,000 people, deepest level 1,999). With the usual-looking cap of 100 the answer was silently truncated to 101 people. In SQLite there is no built-in recursion limit (Q21 counted to 1,000,000 without error). Other engines, not executed here: SQL Server stops at 100 levels by default with an error and MySQL at 1000 (`cte_max_recursion_depth`), so a 2,000-deep chain would need the limit raised there.
- Lattice: `UNION ALL` produced 2,047 rows at 10 levels, 65,535 at 15 and 2,097,151 at 20 (1,048,576 paths to the last level); the reachability query returned 21, 31 and 41 nodes. Elapsed times in my run: 0.001 s, 0.030 s and 0.967 s for path enumeration versus under a millisecond for reachability. The explosion is in rows, which also means memory (the whole queue can grow), not only time.
- Cycles: a loop makes the path count infinite; the guards are in the next section.
- Skewed trees (one manager with thousands of reports) make one frontier huge; the cost is still about the number of rows touched.

**Then explain:**
- Where the time goes: each iteration takes the rows produced by the previous iteration, joins them to the table, and the cost is roughly (rows produced) times (cost of one lookup). Index on the join column makes a lookup cheap. An index on `emp_id` as the primary key serves the anchor.
- Output size is the lower bound: a subtree query cannot be cheaper than the number of people it returns; path enumeration returns paths, so on a DAG it can be much larger than the node count.
- Reachability (`UNION` on node ids) versus enumeration (`UNION ALL`): if you only need to know which nodes can be reached, deduplicate so each node is expanded once; if you need every path or a cost per path you pay for the paths.
- Guards: a depth counter column with `WHERE depth < N` (the portable one), an outer `LIMIT` (I used it in Q28 to stop a loop at 8 rows; SQLite stops producing when the limit is reached), a path string with `instr` for loops, `UNION` on columns that cannot grow, and engine-specific caps and timeouts. Engine caps, hedged and not executed: SQL Server `OPTION (MAXRECURSION n)` default 100, MySQL `cte_max_recursion_depth` default 1000 plus `max_execution_time`, PostgreSQL has no default iteration cap but has the `CYCLE` clause from 14 and `statement_timeout`.
- Recursion cannot use aggregates or reference the CTE twice in SQLite (checked in Q21), so "remember visited nodes" is a `UNION` or a path column, not a subquery.
- Window functions are not part of this question (Parts 4-5).

**Follow-ups:**
- How would you speed up very frequent subtree queries? Store a materialized path or a closure table (Q24) and index it, so a read becomes an index range or lookup.
- What if the table is 50 million rows? Index first, limit depth, filter in the anchor (a small subtree), and consider precomputing; I did not benchmark anything at that size.
- How do you see the plan? `EXPLAIN QUERY PLAN` in SQLite (run above); other engines use their own `EXPLAIN` forms (not executed; Part 11 covers plans).

**Common mistakes:**
- No index on the join column of the recursive step.
- Enumerating paths when only reachability is needed.
- A depth cap that is smaller than the real depth: the result is silently truncated (101 people instead of 2,000 above).
- Quoting a timing without saying machine and run; mine is one run on one machine.
- Raising the engine's recursion limit to hide a loop.

### Q30 ⭐ 🔴 Lowest common ancestor and path between two employees: employees(emp_id, manager_id, name). For employees 10 and 12 return their lowest common manager and the number of hops between them. Use the upward chain CTE for each employee (ancestor, distance), join the two on the ancestor, and take the minimum of the sum of distances (a tie-free tree gives one answer). Show what happens when the two are in different trees (no common ancestor, a forest with two roots) and when one is an ancestor of the other, and compare with a materialized-path longest common prefix solution.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Build the upward chain of ancestors with distances for each of the two employees (including the employee himself at distance 0), join the two chains on the ancestor, and take the row with the smallest sum of distances: that ancestor is the lowest common manager and the sum is the number of hops; if the chains share nothing the two are in different trees and there is no answer.

**Schema and sample data:** the twelve-employee company (Tim is the CEO), plus Tej (emp 30, a report of Radha) to test ids that share a prefix, plus a second company with its own root: Zed (20, NULL manager) and Uma (21, reports to Zed), so the data is a forest with two roots.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,2,'Hari'),(4,3,'Shyam'),(5,1,'Meera'),
 (6,5,'Kiran'),(7,3,'Asha'),(8,6,'Dev'),(9,5,'Isha'),(10,4,'Ram'),
 (11,4,'Zoya'),(12,7,'Nina'),
 (30,2,'Tej'),
 (20,NULL,'Zed'),(21,20,'Uma');     -- a second company: a forest with two roots
```

**SQL answer:** `SQL_MAIN` in the Code block (`{a}` and `{b}` are filled in by the script; the example is 10 and 12):
```sql
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees WHERE emp_id IN ({a}, {b})
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
)
SELECT x.ancestor AS lca, x.dist + y.dist AS hops
FROM up x JOIN up y ON y.ancestor = x.ancestor
WHERE x.start = {a} AND y.start = {b}
ORDER BY hops LIMIT 1
```
`LIMIT 1` after `ORDER BY hops` takes the smallest sum; in a tree the minimum is unique, so there is no tie to break. The `WHERE e.manager_id IS NOT NULL` stops the chain at the root.

Materialized-path version (`SQL_MATPATH`): build each employee's path (`/1/2/3/4/10/`), take the longest common character prefix of the two paths with a small recursive counter, cut it back to the last `/` with `rtrim(common, replace(common, '/', ''))` (which strips trailing digits), and look up the employee whose path is that prefix; hops come from the slash counts (depth of each minus twice the depth of the common ancestor):
```sql
WITH RECURSIVE mp(emp_id, path) AS (
  SELECT emp_id, '/' || emp_id || '/' FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, mp.path || e.emp_id || '/' FROM employees e JOIN mp ON e.manager_id = mp.emp_id
), pick AS (
  SELECT (SELECT path FROM mp WHERE emp_id = {a}) AS pa, (SELECT path FROM mp WHERE emp_id = {b}) AS pb
), lcp(n) AS (
  SELECT 0
  UNION ALL
  SELECT n + 1 FROM lcp, pick WHERE n < length(pa) AND n < length(pb) AND substr(pa, n + 1, 1) = substr(pb, n + 1, 1)
), cut AS (
  SELECT substr(pa, 1, MAX(n)) AS common, pa, pb FROM lcp, pick
)
SELECT m.emp_id AS lca,
       (length(pa) - length(replace(pa, '/', '')) - 1) + (length(pb) - length(replace(pb, '/', '')) - 1)
         - 2 * (length(rtrim(common, replace(common, '/', ''))) - length(replace(rtrim(common, replace(common, '/', '')), '/', '')) - 1) AS hops
FROM cut JOIN mp m ON m.path = rtrim(common, replace(common, '/', ''))
```
Also in the Code block is `SQL_ALL_PAIRS`, the chain join for every pair of employees at once; it picks the best candidate per pair with `ROW_NUMBER` (window functions are covered in Parts 4-5) so that the whole table can be compared with the Python answer.

**pandas answer:** the chain of each employee as a dict (ancestor to distance) from a walk up the manager column; the common ancestors are the intersection of the two key sets, and the answer is the one with the smallest sum of distances. Shown once here and identical to the Code block:
```py
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
def up_chain(i):
    out = {i: 0}
    while not pd.isna(parent[i]):
        i = int(parent[i])
        out[i] = len(out)
    return out

def lca_pandas(a, b):
    ca, cb = up_chain(a), up_chain(b)
    common = set(ca) & set(cb)
    if not common:
        return None
    best = min(common, key=lambda x: (ca[x] + cb[x], x))
    return best, ca[best] + cb[best]
```

**Example:** employee 10 (Ram) has the chain Ram 0, Shyam 1, Hari 2, Radha 3, Tim 4. Employee 12 (Nina) has Nina 0, Asha 1, Hari 2, Radha 3, Tim 4. The common ancestors are Hari, Radha and Tim with distance sums 2 + 2 = 4, 3 + 3 = 6 and 4 + 4 = 8; the minimum is 4, so the lowest common manager is Hari and the number of hops between them is 4 (Ram, Shyam, Hari, Asha, Nina). The other cases:
- One is the ancestor of the other (4 and 10): Shyam's own chain contains Shyam at distance 0, so the common ancestor is Shyam with 0 + 1 = 1 hop. This is why each chain must include the employee himself.
- Same employee (10 and 10): the LCA is Ram, 0 hops.
- Different trees (10 and 21): Ram's chain ends at Tim, Uma's at Zed; no common ancestor, no row (SQL returns nothing, my function returns `None`).
- Ids that share a prefix (10 and 30): the paths are `/1/2/3/4/10/` and `/1/2/30/`; the longest common character prefix is `/1/2/3`, which is not an ancestor (3 is not a prefix of 30); cutting back to the last slash gives `/1/2/`, so the answer is Radha (2) with 4 hops. A naive prefix check without the cut would return Hari (3), wrong.

**Code:** run with `python3 -I`. It checks six cases (SQL chain join equals the materialized-path SQL equals the pandas walk), then compares the all-pairs SQL result with the pandas answer for every pair of employees (rows ordered by `a, b`; pairs across the two companies have no row in either), then checks every connected pair against `networkx.lowest_common_ancestor`.
```python
import sqlite3
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,2,'Hari'),(4,3,'Shyam'),(5,1,'Meera'),
 (6,5,'Kiran'),(7,3,'Asha'),(8,6,'Dev'),(9,5,'Isha'),(10,4,'Ram'),
 (11,4,'Zoya'),(12,7,'Nina'),
 (30,2,'Tej'),
 (20,NULL,'Zed'),(21,20,'Uma');     -- a second company: a forest with two roots
"""
SQL_MAIN = """
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees WHERE emp_id IN ({a}, {b})
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
)
SELECT x.ancestor AS lca, x.dist + y.dist AS hops
FROM up x JOIN up y ON y.ancestor = x.ancestor
WHERE x.start = {a} AND y.start = {b}
ORDER BY hops LIMIT 1
"""
SQL_ALL_PAIRS = """
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
), cand AS (
  SELECT x.start AS a, y.start AS b, x.ancestor AS lca, x.dist + y.dist AS hops,
         ROW_NUMBER() OVER (PARTITION BY x.start, y.start ORDER BY x.dist + y.dist) AS rn
  FROM up x JOIN up y ON y.ancestor = x.ancestor
  WHERE x.start < y.start
)
SELECT a, b, lca, hops FROM cand WHERE rn = 1 ORDER BY a, b
"""
SQL_MATPATH = """
WITH RECURSIVE mp(emp_id, path) AS (
  SELECT emp_id, '/' || emp_id || '/' FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, mp.path || e.emp_id || '/' FROM employees e JOIN mp ON e.manager_id = mp.emp_id
), pick AS (
  SELECT (SELECT path FROM mp WHERE emp_id = {a}) AS pa, (SELECT path FROM mp WHERE emp_id = {b}) AS pb
), lcp(n) AS (
  SELECT 0
  UNION ALL
  SELECT n + 1 FROM lcp, pick WHERE n < length(pa) AND n < length(pb) AND substr(pa, n + 1, 1) = substr(pb, n + 1, 1)
), cut AS (
  SELECT substr(pa, 1, MAX(n)) AS common, pa, pb FROM lcp, pick
)
SELECT m.emp_id AS lca,
       (length(pa) - length(replace(pa, '/', '')) - 1) + (length(pb) - length(replace(pb, '/', '')) - 1)
         - 2 * (length(rtrim(common, replace(common, '/', ''))) - length(replace(rtrim(common, replace(common, '/', '')), '/', '')) - 1) AS hops
FROM cut JOIN mp m ON m.path = rtrim(common, replace(common, '/', ''))
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
names = dict(con.execute("SELECT emp_id, name FROM employees").fetchall())

def lca_sql(a, b):
    rows = con.execute(SQL_MAIN.format(a=a, b=b)).fetchall()
    return rows[0] if rows else None

def lca_matpath(a, b):
    rows = con.execute(SQL_MATPATH.format(a=a, b=b)).fetchall()
    return rows[0] if rows else None

cases = [("10 and 12 (the question)", 10, 12), ("4 and 10 (one is the ancestor of the other)", 4, 10),
         ("10 and 10 (same employee)", 10, 10), ("10 and 21 (different trees)", 10, 21),
         ("10 and 30 (ids '/1/2/3/4/10/' and '/1/2/30/')", 10, 30), ("8 and 11", 8, 11)]
print("case -> SQL chain join (lca, hops) | SQL materialized-path prefix (lca, hops)")
for label, a, b in cases:
    r1, r2 = lca_sql(a, b), lca_matpath(a, b)
    print(f"  {label}: {r1} ({names[r1[0]] if r1 else '-'}) | {r2}")
    assert r1 == r2

employees = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
def up_chain(i):
    out = {i: 0}
    while not pd.isna(parent[i]):
        i = int(parent[i])
        out[i] = len(out)
    return out

def lca_pandas(a, b):
    ca, cb = up_chain(a), up_chain(b)
    common = set(ca) & set(cb)
    if not common:
        return None
    best = min(common, key=lambda x: (ca[x] + cb[x], x))
    return best, ca[best] + cb[best]
# pd:end

for label, a, b in cases:
    assert lca_pandas(a, b) == lca_sql(a, b)
sql_all = pd.read_sql_query(SQL_ALL_PAIRS, con)
ids = sorted(employees["emp_id"])
rows = []
for i, a in enumerate(ids):
    for b in ids[i + 1:]:
        r = lca_pandas(a, b)
        if r is not None:
            rows.append((a, b, r[0], r[1]))
pd_all = pd.DataFrame(rows, columns=["a", "b", "lca", "hops"])
# compare after ordering by a, b (the SQL ORDER BY); pairs across the two companies have no row in either
pd.testing.assert_frame_equal(pd_all, sql_all, check_dtype=False)
print(f"\nall {len(sql_all)} connected pairs: SQL chain join == pandas dict walk; pairs across the two companies are absent in both")
print("number of employee pairs in total:", len(ids) * (len(ids) - 1) // 2, "| pairs with no common ancestor:", len(ids) * (len(ids) - 1) // 2 - len(sql_all))

# networkx check on the tree edges (manager -> report)
D = nx.DiGraph([(int(m), int(e)) for e, m in zip(employees["emp_id"], employees["manager_id"]) if pd.notna(m)])
D.add_nodes_from(ids)
for label, a, b in cases:
    got = None
    try:
        got = nx.lowest_common_ancestor(D, a, b)
    except Exception as ex:
        got = type(ex).__name__
    print(f"  networkx lowest_common_ancestor({a}, {b}) = {got}")
bad = 0
for a, b, lca, hops in sql_all.itertuples(index=False):
    got = nx.lowest_common_ancestor(D, a, b)
    bad += (got != lca)
print("networkx 3.6.1 lowest_common_ancestor disagrees with the SQL answer on", bad, "of", len(sql_all), "connected pairs")
print("asserts passed")
```

**Output (my run):**
```text
case -> SQL chain join (lca, hops) | SQL materialized-path prefix (lca, hops)
  10 and 12 (the question): (3, 4) (Hari) | (3, 4)
  4 and 10 (one is the ancestor of the other): (4, 1) (Shyam) | (4, 1)
  10 and 10 (same employee): (10, 0) (Ram) | (10, 0)
  10 and 21 (different trees): None (-) | None
  10 and 30 (ids '/1/2/3/4/10/' and '/1/2/30/'): (2, 4) (Radha) | (2, 4)
  8 and 11: (1, 7) (Tim) | (1, 7)

all 79 connected pairs: SQL chain join == pandas dict walk; pairs across the two companies are absent in both
number of employee pairs in total: 105 | pairs with no common ancestor: 26
  networkx lowest_common_ancestor(10, 12) = 3
  networkx lowest_common_ancestor(4, 10) = 4
  networkx lowest_common_ancestor(10, 10) = 10
  networkx lowest_common_ancestor(10, 21) = None
  networkx lowest_common_ancestor(10, 30) = 2
  networkx lowest_common_ancestor(8, 11) = 1
networkx 3.6.1 lowest_common_ancestor disagrees with the SQL answer on 0 of 79 connected pairs
asserts passed
```

**Edge cases:**
- Different trees: no common ancestor. In SQL the join returns zero rows (so a caller must handle the empty result); in pandas the intersection is empty; networkx returned `None` for 10 and 21 in my run. In my data 26 of the 105 employee pairs are across the two companies (no answer).
- One employee is an ancestor of the other: works because each chain includes distance 0 for the employee himself; without the distance-0 rows the common set would be Hari, Radha and Tim and the query would return Hari with 3 hops, which is wrong (the answer is Shyam with 1).
- Same employee: 0 hops, LCA is himself.
- NULL manager (the root): the upward recursion stops where `manager_id IS NULL` (that is what the guard is for); a NULL is never joined.
- Orphan (manager id missing from the table) would end the chain early, so two employees under such managers can look unrelated; not in this data and not run.
- A loop in the manager data would make the upward recursion run forever; add a depth cap or a path guard (Q8, Q15). Not run here for this query.
- Ties: in a tree the lowest common ancestor is unique. In a DAG (several parents) there can be several lowest common ancestors with the same sum, and `LIMIT 1` would pick one arbitrarily; not applicable here.
- All 105 pairs: 79 had a common manager and all 79 agree between SQL, the pandas walk and networkx; `networkx.lowest_common_ancestor` was called on a directed graph with edges manager to report, as at run time.

**Then explain:**
- Two upward chains are cheap: each is at most depth rows, so the cost is about the depth of the tree, not its size.
- The minimum of the distance sum picks the lowest (deepest) common ancestor: every ancestor above it is also common but strictly further from both.
- Hops equal `dist_a + dist_b` at the LCA because the path between two nodes in a tree goes up to the LCA and back down.
- Materialized path: the LCA is the longest common prefix cut at a separator; it needs no recursion at query time, at the price of storing and maintaining the path (Q24). The prefix must be cut at a separator, otherwise ids such as 3 and 30 fool it.
- Cross-engine: the recursive CTE form needs `WITH RECURSIVE` in SQLite, MySQL 8 and PostgreSQL and plain `WITH` in SQL Server (hedged, not executed); Oracle would use `CONNECT BY PRIOR` upwards (not executed).

**Follow-ups:**
- LCA of many employees at once? Intersect all the chains (the deepest common one), or take the longest common path prefix of all the paths.
- Distance between two employees without the LCA? Not possible in general for trees without it; for a materialized path it is `depth_a + depth_b - 2 * depth_lca`.
- Common manager but also the same department? Add the filter after finding the LCA, not in the chain, or you change the tree.

**Common mistakes:**
- Not including the employee himself in his own chain (breaks the "one is the ancestor of the other" case).
- Taking the first common ancestor found, or the minimum ancestor id, instead of the minimum sum of distances.
- Taking a character prefix of the paths without cutting at a separator (3 versus 30).
- Forgetting the empty result for different trees.
- Hops off by one (counting nodes instead of edges).
