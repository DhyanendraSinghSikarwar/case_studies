# Q26: highest-paid employee per department, ties included: derived-table join vs correlated subquery
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
 (4,'Dev',20,80),
 (5,'Eve',30,60),(6,'Farid',30,50),
 (7,'Hari',40,NULL),
 (8,'Ivy',NULL,95);
"""
SQL_MAIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, MAX(salary) AS max_salary
      FROM employees
      GROUP BY dept_id) m
  ON m.dept_id = e.dept_id AND m.max_salary = e.salary
ORDER BY e.dept_id, e.emp_id
"""
SQL_CORRELATED = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary = (SELECT MAX(e2.salary)
                  FROM employees e2
                  WHERE e2.dept_id = e.dept_id)
ORDER BY e.dept_id, e.emp_id
"""
SQL_NOT_EXISTS = """
SELECT e.emp_id FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM employees e2
                  WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary)
ORDER BY e.emp_id
"""
SQL_LIMIT1 = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.emp_id = (SELECT e2.emp_id FROM employees e2
                  WHERE e2.dept_id = e.dept_id
                  ORDER BY e2.salary DESC LIMIT 1)
ORDER BY e.dept_id
"""
SQL_BARE = """
SELECT dept_id, name, MAX(salary) AS max_salary
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id
ORDER BY dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
corr_df = pd.read_sql_query(SQL_CORRELATED, con)
print("derived-table join (ties kept):")
print(sql_df.to_string(index=False))
print("correlated subquery ids:", corr_df["emp_id"].tolist())
print("NOT EXISTS (nobody earns more) ids:", [r[0] for r in con.execute(SQL_NOT_EXISTS)])
print("\nLIMIT 1 per group (no tie-break) -> one row per department:")
print(pd.read_sql_query(SQL_LIMIT1, con).to_string(index=False))
print("\nGROUP BY dept_id with bare column `name` next to MAX(salary) (SQLite only):")
print(pd.read_sql_query(SQL_BARE, con).to_string(index=False))

print("\nFROM-subquery without an alias:", con.execute(
    "SELECT MAX(m) FROM (SELECT MAX(salary) AS m FROM employees GROUP BY dept_id)").fetchall())
print("scalar subquery returning many rows (dept 10, ORDER BY salary ASC / DESC):",
      con.execute("SELECT (SELECT salary FROM employees WHERE dept_id = 10 ORDER BY salary), "
                  "(SELECT salary FROM employees WHERE dept_id = 10 ORDER BY salary DESC)").fetchone())

# pd:main
mask = emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[mask].sort_values(["dept_id", "emp_id"]).reset_index(drop=True)
idx_df = emp.dropna(subset=["salary", "dept_id"]).loc[lambda d: d.groupby("dept_id")["salary"].idxmax()]
# pd:end
print("\npandas transform('max') mask ids:", pd_df["emp_id"].tolist())
print("pandas idxmax ids (one per dept):", idx_df["emp_id"].tolist())
print("transform('max') on the NaN dept key:", emp.groupby("dept_id")["salary"].transform("max").tolist())

# compared after sorting by dept_id, emp_id; NaN dept/salary rows never match in either engine
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert corr_df["emp_id"].tolist() == sql_df["emp_id"].tolist() == [1, 2, 4, 5]
assert len(idx_df) == 3 and set(idx_df["dept_id"]) == {10, 20, 30}
print("\nasserts passed: join == correlated == pandas transform mask (ids 1,2,4,5); idxmax returns one row per department")
