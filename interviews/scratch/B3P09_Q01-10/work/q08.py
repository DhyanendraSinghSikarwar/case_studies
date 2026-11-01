# Q8: debug a recursive query that never terminates: reproduce safely, find the bad rows, three fixes
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES
 (1, NULL), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3),
 (7, 9), (9, 7),            -- 7 and 9 report to each other
 (8, 7), (10, 8),           -- below the loop
 (15, 15), (16, 15);        -- 15 is his own manager, 16 reports to him
"""
SQL_HANG = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  LIMIT 25                                              -- safety net for the reproduction only
)
SELECT emp_id, level FROM sub
"""
SQL_DEPTH = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < :cap                                  -- fix 1: depth cap
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
"""
SQL_PATH = """
WITH RECURSIVE sub(emp_id, level, path) AS (
  SELECT emp_id, 1, ',' || :boss || ',' || emp_id || ',' FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1, s.path || e.emp_id || ','
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.path NOT LIKE '%,' || e.emp_id || ',%'        -- fix 2: visited-path check (boss seeded in the path)
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
"""
SQL_UNION = """
WITH RECURSIVE sub(emp_id) AS (
  SELECT emp_id FROM employees WHERE manager_id = :boss
  UNION                                                 -- fix 3: key-only row, repeats are dropped
  SELECT e.emp_id FROM employees e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id FROM sub ORDER BY emp_id
"""
SQL_BAD = """
WITH RECURSIVE up(start_id, cur_id, depth) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.start_id, e.manager_id, u.depth + 1
  FROM up u JOIN employees e ON e.emp_id = u.cur_id
  WHERE e.manager_id IS NOT NULL AND u.depth < 20      -- the finder needs its own guard
)
SELECT DISTINCT start_id AS emp_id,
       CASE WHEN start_id = (SELECT manager_id FROM employees WHERE emp_id = start_id) THEN 'self-managed' ELSE 'in a loop' END AS problem
FROM up WHERE cur_id = start_id ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

# Premise check: does the subtree of manager 1 hang? (an unguarded query, safety LIMIT only)
r1 = con.execute(SQL_HANG, {"boss": 1}).fetchall()
print("boss 1 unguarded, LIMIT 25:", len(r1), "rows (fewer than 25 means it ended by itself):", sorted(e for e, _ in r1))
r7 = con.execute(SQL_HANG, {"boss": 7}).fetchall()
print("boss 7 unguarded, LIMIT 25:", len(r7), "rows, first 10:", r7[:10])
r15 = con.execute(SQL_HANG, {"boss": 15}).fetchall()
print("boss 15 unguarded, LIMIT 25:", len(r15), "rows, first 6:", r15[:6])

print("bad rows:", con.execute(SQL_BAD).fetchall())

d = pd.read_sql_query(SQL_DEPTH, con, params={"boss": 7, "cap": 4})
p = pd.read_sql_query(SQL_PATH, con, params={"boss": 7})
u = pd.read_sql_query(SQL_UNION, con, params={"boss": 7})
print("fix 1 depth cap 4:", len(d), "rows, distinct people", d.emp_id.nunique(), "->", d.emp_id.tolist())
print("fix 2 path check:", p.values.tolist())
print("fix 3 UNION key-only:", u.emp_id.tolist(), "(7 is in his own subtree because he reports to 9)")

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
def subtree(boss, seed_boss=True):
    frontier = edges[edges["manager_id"] == boss][["emp_id"]].assign(level=1)
    seen = {boss} if seed_boss else set()
    out = []
    while not frontier.empty:
        frontier = frontier[~frontier["emp_id"].isin(seen)]          # visited set instead of a path string
        seen |= set(frontier["emp_id"])
        out.append(frontier)
        frontier = (frontier.rename(columns={"emp_id": "manager_id"})
                    .merge(edges, on="manager_id")[["emp_id", "level"]].assign(level=lambda x: x["level"] + 1))
    return pd.concat(out, ignore_index=True).sort_values(["level", "emp_id"]).reset_index(drop=True)
pd_path = subtree(7)                       # same as the path check: the boss is seeded as visited
pd_union = subtree(7, seed_boss=False)     # same as UNION on a key: the boss is not seeded
# pd:end
pd.testing.assert_frame_equal(pd_path, p, check_dtype=False)                 # both ordered by level, emp_id
assert sorted(pd_union["emp_id"]) == u["emp_id"].tolist()                    # UNION answer, as a sorted id list
print("pandas visited-set versions equal the SQL path check and the UNION answer")

# a loop that includes the CEO: the 'subtree of manager 1' really hangs
con.execute("UPDATE employees SET manager_id = 5 WHERE emp_id = 1")
rr = con.execute(SQL_HANG, {"boss": 1}).fetchall()
print("CEO reports to his own descendant 5; boss 1 unguarded, LIMIT 25:", len(rr), "rows (hit the limit)")
print("same data, path check:", con.execute(SQL_PATH, {"boss": 1}).fetchall())
print("asserts passed")
