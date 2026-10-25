# Q4: all reports under a manager (recursive CTE), fixed-depth self-joins, pandas frontier loop, cycle demo
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,  NULL, 'Tim',   500),
 (2,  1,    'Radha', 300),
 (3,  1,    'Hari',  300),
 (4,  2,    'Asha',  100),
 (5,  3,    'Ben',   200),
 (6,  3,    'Chen',  200),
 (7,  5,    'Dev',   150),
 (8,  5,    'Esha',  150),
 (9,  6,    'Farid', 120),
 (10, 7,    'Gita',  100),
 (11, 7,    'Hugo',  100),
 (12, 10,   'Ivy',    90),
 (13, 99,   'Jay',    80);     -- orphan: manager 99 does not exist
"""
SQL_MAIN = """
WITH RECURSIVE sub(emp_id, name, level) AS (
  SELECT emp_id, name, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20                                   -- depth guard
)
SELECT emp_id, name, level FROM sub ORDER BY level, emp_id
"""
SQL_FIXED = """
SELECT e1.emp_id, e1.name, 1 AS level FROM employees e1 WHERE e1.manager_id = :boss
UNION ALL
SELECT e2.emp_id, e2.name, 2 FROM employees e1 JOIN employees e2 ON e2.manager_id = e1.emp_id
WHERE e1.manager_id = :boss
UNION ALL
SELECT e3.emp_id, e3.name, 3 FROM employees e1 JOIN employees e2 ON e2.manager_id = e1.emp_id
JOIN employees e3 ON e3.manager_id = e2.emp_id WHERE e1.manager_id = :boss
ORDER BY level, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"boss": 3})
print(sql_df.to_string(index=False))
fixed_df = pd.read_sql_query(SQL_FIXED, con, params={"boss": 3})
print("fixed 3-join version rows:", len(fixed_df), "| recursive rows:", len(sql_df),
      "| missed:", sorted(set(sql_df.emp_id) - set(fixed_df.emp_id)))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def reports_under(employees, boss, max_levels=20):
    edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
    frontier = edges[edges["manager_id"] == boss][["emp_id", "name"]].assign(level=1)
    seen = set(frontier["emp_id"])
    out = [frontier]
    while not frontier.empty and frontier["level"].iloc[0] < max_levels:
        nxt = (frontier[["emp_id", "level"]].rename(columns={"emp_id": "manager_id"})
               .merge(edges[["emp_id", "manager_id", "name"]], on="manager_id")
               .assign(level=lambda d: d["level"] + 1)[["emp_id", "name", "level"]])
        frontier = nxt[~nxt["emp_id"].isin(seen)]
        seen |= set(frontier["emp_id"])
        out.append(frontier)
    return pd.concat(out, ignore_index=True).sort_values(["level", "emp_id"]).reset_index(drop=True)
pd_df = reports_under(employees, 3)
# pd:end
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)     # both ordered by level, emp_id
print("pandas equals SQL")

# Edge cases
for boss in (7, 12, 42, 99, 1):
    r = pd.read_sql_query(SQL_MAIN, con, params={"boss": boss})
    p = reports_under(employees, boss)
    pd.testing.assert_frame_equal(p, r, check_dtype=False)
    print(f"boss {boss}: {len(r)} rows, levels {sorted(set(r['level']))}")
print("boss NULL (manager_id = NULL never matches):", con.execute(SQL_MAIN, {"boss": None}).fetchall())
# manager included? add him with level 0 via UNION ALL
print("with the manager as level 0:", con.execute("""
WITH RECURSIVE sub(emp_id, name, level) AS (
  SELECT emp_id, name, 0 FROM employees WHERE emp_id = :boss
  UNION ALL SELECT e.emp_id, e.name, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id WHERE s.level < 20)
SELECT count(*), min(level) FROM sub""", {"boss": 3}).fetchone())

# Cycle demo on a copy: Hari (3) now reports to Dev (7), who is below him
con.execute("CREATE TABLE emp_cyc AS SELECT * FROM employees")
con.execute("UPDATE emp_cyc SET manager_id = 7 WHERE emp_id = 3")
unguarded = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM emp_cyc WHERE manager_id = 3
  UNION ALL SELECT e.emp_id, s.level + 1 FROM emp_cyc e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id, level FROM sub LIMIT 14"""     # LIMIT is the only thing stopping this demo
rows = con.execute(unguarded).fetchall()
print("cycle, no guard, LIMIT 14 shows repeats:", rows)
guarded = pd.read_sql_query(SQL_MAIN.replace("employees", "emp_cyc"), con, params={"boss": 3})
print("cycle, depth cap 20: rows =", len(guarded), "| distinct emp_ids =", guarded.emp_id.nunique(), "| clean answer rows would be", len(sql_df))
print("asserts passed")
