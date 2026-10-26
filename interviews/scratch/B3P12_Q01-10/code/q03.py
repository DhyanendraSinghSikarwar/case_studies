# Q3: org size roll-up: direct and total reports per manager, orphan listed separately.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'CEO',NULL),
 (2,'VP-A',1),(3,'VP-B',1),
 (4,'Dir-A1',2),(5,'Dir-A2',2),(6,'Dir-B1',3),(12,'Dir-B2',3),
 (7,'Mgr-1',4),(8,'Mgr-2',4),(9,'Mgr-3',5),
 (10,'Mgr-4',6),(11,'Mgr-5',6),
 (13,'Orphan',99);            -- manager 99 does not exist
""")
# 12 employees in 4 levels (CEO, 2 VPs, 4 Directors, 5 Managers) plus 1 orphan row = 13 rows

sql = """
WITH RECURSIVE d(mgr, emp, depth) AS (
  SELECT e.manager_id, e.emp_id, 1                       -- direct edges, only when the manager exists
  FROM employees e JOIN employees m ON m.emp_id = e.manager_id
  UNION ALL
  SELECT d.mgr, e.emp_id, d.depth + 1                    -- walk one level further down
  FROM d JOIN employees e ON e.manager_id = d.emp
)
SELECT mgr AS emp_id,
       SUM(depth = 1) AS direct_reports,
       COUNT(*)       AS total_reports
FROM d
GROUP BY mgr
ORDER BY total_reports DESC, emp_id
"""
orphan_sql = """
SELECT emp_id, name, manager_id FROM employees e
WHERE manager_id IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
"""
s = pd.read_sql(sql, con)
so = pd.read_sql(orphan_sql, con)
print("SQL roll-up:"); print(s.to_string(index=False)); print()
print("SQL orphan rows:"); print(so.to_string(index=False)); print()

# pandas: iterative frame walk
emp = pd.read_sql("SELECT * FROM employees", con)
edges = (emp[emp["manager_id"].isin(emp["emp_id"])][["manager_id", "emp_id"]]
         .rename(columns={"manager_id": "mgr", "emp_id": "emp"}).assign(depth=1))
frames, cur, level = [edges], edges, 1
while True:
    nxt = cur.merge(edges[["mgr", "emp"]], left_on="emp", right_on="mgr", suffixes=("", "_child"))
    nxt = nxt[["mgr", "emp_child"]].rename(columns={"emp_child": "emp"}).assign(depth=level + 1)
    if nxt.empty:
        break
    frames.append(nxt)
    cur, level = nxt, level + 1
    assert level <= len(emp), "cycle in manager_id"       # guard: a cycle would loop forever
closure = pd.concat(frames, ignore_index=True)
print("levels walked:", level)
closure["mgr"] = closure["mgr"].astype("int64")
p = (closure.groupby("mgr").agg(direct_reports=("depth", lambda d: int((d == 1).sum())),
                                total_reports=("depth", "size"))
            .reset_index().rename(columns={"mgr": "emp_id"})
            .sort_values(["total_reports", "emp_id"], ascending=[False, True]).reset_index(drop=True))
po = emp[emp["manager_id"].notna() & ~emp["manager_id"].isin(emp["emp_id"])][["emp_id", "name", "manager_id"]].reset_index(drop=True)
print("pandas roll-up:"); print(p.to_string(index=False)); print()
pd.testing.assert_frame_equal(s, p, check_dtype=False)
pd.testing.assert_frame_equal(so, po.astype({"manager_id": "int64"}), check_dtype=False)
print("asserts passed (order: total_reports desc, emp_id)")
