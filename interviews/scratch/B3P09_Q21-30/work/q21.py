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
