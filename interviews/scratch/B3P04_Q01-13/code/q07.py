# Q7: Department Highest Salary (LeetCode 184 style)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'Sales'),(3,'HR');
INSERT INTO employees VALUES (1,'Joe',70,1),(2,'Max',90,1),(3,'Randy',90,1),(4,'Henry',80,2),
  (5,'Sam',60,2),(6,'Tia',NULL,2),(7,'Zed',99,NULL);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT name, salary, dept_id,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r
JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rnk = 1
ORDER BY d.dept_name, r.name
"""
SQL_MAX = """
WITH m AS (
  SELECT name, salary, dept_id,
         MAX(salary) OVER (PARTITION BY dept_id) AS dept_max
  FROM employees
)
SELECT d.dept_name AS department, m.name AS employee, m.salary
FROM m
JOIN departments d ON d.dept_id = m.dept_id
WHERE m.salary = m.dept_max
ORDER BY d.dept_name, m.name
"""
SQL_ROWNUM = """
WITH ranked AS (
  SELECT name, salary, dept_id,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rn = 1
ORDER BY d.dept_name, r.name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
max_df = pd.read_sql_query(SQL_MAX, con)
rn_df = pd.read_sql_query(SQL_ROWNUM, con)
print("RANK() = 1:"); print(sql_df.to_string(index=False))
print("\nROW_NUMBER() = 1 (loses the tied employee):"); print(rn_df.to_string(index=False))
assert sql_df.equals(max_df)

emp = pd.read_sql_query("SELECT * FROM employees", con)
dept = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
top = emp[emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")]
pd_df = (top.merge(dept, on="dept_id")
            .rename(columns={"dept_name": "department", "name": "employee"})
            [["department", "employee", "salary"]])
# pd:end
# compared after sorting by department, employee
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values(["department", "employee"]).reset_index(drop=True), check_dtype=False)
assert len(rn_df) < len(sql_df)
print("\nasserts passed: RANK=1 == MAX() OVER == pandas transform('max') + merge; ROW_NUMBER=1 returns fewer rows")
