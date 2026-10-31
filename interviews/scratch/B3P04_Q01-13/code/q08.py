# Q8: Department Top Three Salaries (LeetCode 185 style)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept_id INTEGER);
INSERT INTO departments VALUES (1,'IT'),(2,'Sales'),(3,'HR');
INSERT INTO employees VALUES (1,'Joe',85,1),(2,'Henry',80,2),(3,'Sam',60,2),(4,'Max',90,1),
  (5,'Janet',69,1),(6,'Randy',85,1),(7,'Will',85,1),(8,'Tia',NULL,2),(9,'Ravi',60,1);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT name, salary, dept_id,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT d.dept_name AS department, r.name AS employee, r.salary
FROM ranked r
JOIN departments d ON d.dept_id = r.dept_id
WHERE r.rnk <= 3
ORDER BY d.dept_name, r.salary DESC, r.name
"""
def variant(fn, where="", order="salary DESC"):
    return f"""
WITH ranked AS (SELECT name, salary, dept_id, {fn} OVER (PARTITION BY dept_id ORDER BY {order}) AS k
                FROM employees {where})
SELECT d.dept_name, r.name FROM ranked r JOIN departments d ON d.dept_id = r.dept_id WHERE r.k <= 3
ORDER BY d.dept_name, r.name"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("DENSE_RANK <= 3 (NULL salary filtered):"); print(sql_df.to_string(index=False))
for fn, order in [("RANK()", "salary DESC"), ("ROW_NUMBER()", "salary DESC, emp_id")]:
    r = con.execute(variant(fn, "WHERE salary IS NOT NULL", order)).fetchall()
    print("%-13s <= 3 returns %d rows; IT rows: %s" % (fn, len(r), [n for d, n in r if d == "IT"]))
nofilter = con.execute(variant("DENSE_RANK()")).fetchall()
print("DENSE_RANK without the IS NOT NULL filter, Sales rows:", [n for d, n in nofilter if d == "Sales"])

emp = pd.read_sql_query("SELECT * FROM employees", con)
dept = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
emp["rnk"] = emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
top = emp[emp["rnk"] <= 3]
pd_df = (top.merge(dept, on="dept_id")
            .rename(columns={"dept_name": "department", "name": "employee"})
            [["department", "employee", "salary"]])
# pd:end
# compared after sorting by department, salary desc, employee
pd.testing.assert_frame_equal(
    sql_df,
    pd_df.sort_values(["department", "salary", "employee"], ascending=[True, False, True]).reset_index(drop=True),
    check_dtype=False)
print("\nasserts passed: SQL DENSE_RANK <= 3 (non-NULL salaries) == pandas groupby rank(method='dense')")
