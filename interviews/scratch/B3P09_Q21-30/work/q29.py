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
