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
