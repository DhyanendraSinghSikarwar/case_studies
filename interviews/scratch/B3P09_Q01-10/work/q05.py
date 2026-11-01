# Q5: chain of command upwards for one employee and the levels-to-top for everyone; guards for loops and orphans
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,  NULL, 'Tim'),
 (2,  1,    'Radha'),
 (3,  2,    'Hari'),
 (4,  3,    'Shyam'),
 (10, 4,    'Ram'),
 (11, 3,    'Sita'),
 (20, 99,   'Orphan'),   -- manager 99 is missing
 (30, 31,   'LoopA'),    -- 30 and 31 manage each other
 (31, 30,   'LoopB'),
 (40, 40,   'Self');     -- manages himself
"""
SQL_CHAIN = """
WITH RECURSIVE chain(emp_id, manager_id, name, level, path, ids) AS (
  SELECT emp_id, manager_id, name, 0, name, ',' || emp_id || ','
  FROM employees WHERE emp_id = :emp
  UNION ALL
  SELECT e.emp_id, e.manager_id, e.name, c.level + 1, c.path || ' > ' || e.name, c.ids || e.emp_id || ','
  FROM employees e JOIN chain c ON e.emp_id = c.manager_id
  WHERE instr(c.ids, ',' || e.emp_id || ',') = 0        -- cycle guard: never visit an employee twice
)
SELECT emp_id, name, level, path FROM chain ORDER BY level
"""
SQL_ALL = """
WITH RECURSIVE up(start_id, mgr_id, level, ids) AS (
  SELECT emp_id, manager_id, 0, ',' || emp_id || ',' FROM employees
  UNION ALL
  SELECT u.start_id, e.manager_id, u.level + 1, u.ids || e.emp_id || ','
  FROM up u JOIN employees e ON e.emp_id = u.mgr_id
  WHERE instr(u.ids, ',' || e.emp_id || ',') = 0
)
SELECT start_id AS emp_id,
       MAX(level) AS levels_to_top,
       MAX(CASE WHEN mgr_id IS NULL THEN 1 ELSE 0 END) AS reached_ceo
FROM up GROUP BY start_id ORDER BY start_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_chain = pd.read_sql_query(SQL_CHAIN, con, params={"emp": 10})
print(sql_chain.to_string(index=False))
print("chain string:", sql_chain["path"].iloc[-1])
sql_all = pd.read_sql_query(SQL_ALL, con)
print(sql_all.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
mgr = dict(zip(employees["emp_id"], employees["manager_id"]))      # NaN for the CEO
nm = dict(zip(employees["emp_id"], employees["name"]))
def walk(emp):
    rows, seen, cur = [], set(), emp
    while cur not in seen:
        seen.add(cur)
        rows.append((cur, nm[cur], len(rows)))
        nxt = mgr[cur]
        if pd.isna(nxt) or int(nxt) not in mgr:                     # CEO (NaN) or missing manager: stop
            break
        cur = int(nxt)
    path = []
    out = []
    for e, n_, lvl in rows:
        path.append(n_)
        out.append((e, n_, lvl, " > ".join(path)))
    last_mgr = mgr[rows[-1][0]]
    return pd.DataFrame(out, columns=["emp_id", "name", "level", "path"]), bool(pd.isna(last_mgr))
pd_chain, _ = walk(10)
pd_all = pd.DataFrame([(e, len(walk(e)[0]) - 1, int(walk(e)[1])) for e in employees["emp_id"]],
                      columns=["emp_id", "levels_to_top", "reached_ceo"])
# pd:end
pd.testing.assert_frame_equal(pd_chain, sql_chain, check_dtype=False)               # ordered by level
pd.testing.assert_frame_equal(pd_all.sort_values("emp_id").reset_index(drop=True), sql_all, check_dtype=False)
print("pandas equals SQL (chain by level, all by emp_id)")

# Edge cases
print("CEO himself:", con.execute(SQL_CHAIN, {"emp": 1}).fetchall())
print("orphan chain stops at the missing manager:", con.execute(SQL_CHAIN, {"emp": 20}).fetchall())
print("unknown employee:", con.execute(SQL_CHAIN, {"emp": 777}).fetchall())
unguarded = SQL_CHAIN.replace("  WHERE instr(c.ids, ',' || e.emp_id || ',') = 0        -- cycle guard: never visit an employee twice\n", "").replace("ORDER BY level", "LIMIT 7")
print("loop employee 30 without the guard, LIMIT 7:", [(r[1], r[2]) for r in con.execute(unguarded, {"emp": 30})])
print("loop employee 30 with the guard:", [(r[1], r[2]) for r in con.execute(SQL_CHAIN, {"emp": 30})])
print("asserts passed")
