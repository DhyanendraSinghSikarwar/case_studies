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
print("asserts passed")
