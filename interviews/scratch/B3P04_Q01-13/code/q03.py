# Q3: window function in WHERE
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),(4,'Dev',10,70),
  (5,'Esha',10,40),(6,'Farid',20,90),(7,'Gita',20,80),(8,'Hari',20,80),(9,'Ila',30,55);
"""
SQL_FAIL = """
SELECT emp_id, name FROM employees
WHERE RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) <= 3
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT dept_id, emp_id, name, salary, rnk
FROM ranked
WHERE rnk <= 3
ORDER BY dept_id, rnk, emp_id
"""
SQL_SUBQ = """
SELECT dept_id, emp_id, name, salary, rnk
FROM (SELECT emp_id, name, dept_id, salary,
             RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
      FROM employees)
WHERE rnk <= 3
ORDER BY dept_id, rnk, emp_id
"""
SQL_WHEREFIRST = """
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary < 70
)
SELECT dept_id, emp_id, name, salary, rnk FROM ranked ORDER BY dept_id, rnk, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
try:
    con.execute(SQL_FAIL).fetchall()
except sqlite3.OperationalError as e:
    print("window function in WHERE ->", type(e).__name__ + ":", e)

sql_df = pd.read_sql_query(SQL_MAIN, con)
sub_df = pd.read_sql_query(SQL_SUBQ, con)
print("\nCTE version:"); print(sql_df.to_string(index=False))
assert sql_df.equals(sub_df)

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
emp["rnk"] = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype(int)
pd_df = emp[emp["rnk"] <= 3][["dept_id", "emp_id", "name", "salary", "rnk"]]
# pd:end
# compared after sorting by dept_id, rnk, emp_id
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values(["dept_id", "rnk", "emp_id"]).reset_index(drop=True), check_dtype=False)

print("\nWHERE salary < 70 runs BEFORE the window, so ranks restart among the survivors:")
print(pd.read_sql_query(SQL_WHEREFIRST, con).to_string(index=False))
print("asserts passed: CTE == subquery == pandas rank(method='min') <= 3")
