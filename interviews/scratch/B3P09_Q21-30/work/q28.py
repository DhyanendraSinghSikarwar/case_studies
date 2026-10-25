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
