# Q1: window function versus GROUP BY
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55),(7,'Gita',20,NULL);
"""
SQL_WINDOW = """
SELECT emp_id, name, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees
ORDER BY emp_id
"""
SQL_GROUP = """
SELECT dept_id, AVG(salary) AS dept_avg, COUNT(*) AS n_rows
FROM employees
GROUP BY dept_id
ORDER BY dept_id
"""
SQL_ORDERED = """
SELECT emp_id, dept_id, salary,
       AVG(salary) OVER ()                                 AS company_avg,
       AVG(salary) OVER (PARTITION BY dept_id ORDER BY emp_id) AS avg_so_far
FROM employees
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_win = pd.read_sql_query(SQL_WINDOW, con)
sql_grp = pd.read_sql_query(SQL_GROUP, con)
sql_ord = pd.read_sql_query(SQL_ORDERED, con)
print("window (every row kept):"); print(sql_win.to_string(index=False))
print("\nGROUP BY (one row per department):"); print(sql_grp.to_string(index=False))
print("\nOVER () and ORDER BY inside OVER:"); print(sql_ord.round(2).to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:window
pd_win = emp.assign(dept_avg=emp.groupby("dept_id")["salary"].transform("mean"))
# pd:end
# pd:group
pd_grp = (emp.groupby("dept_id")
             .agg(dept_avg=("salary", "mean"), n_rows=("emp_id", "size"))
             .reset_index())
# pd:end
# compared after sorting by emp_id (window) and dept_id (group)
pd.testing.assert_frame_equal(sql_win, pd_win.sort_values("emp_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_grp, pd_grp.sort_values("dept_id").reset_index(drop=True), check_dtype=False)
print("\nrows in: %d, window rows out: %d, group rows out: %d" % (len(emp), len(sql_win), len(sql_grp)))
print("asserts passed: window == transform('mean'), GROUP BY == groupby.agg")
