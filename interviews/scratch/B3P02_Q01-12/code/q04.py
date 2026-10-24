# Q4: self join, employees earning more than their managers.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, manager_id INTEGER);
INSERT INTO employees VALUES (1,'Ann',90,NULL),(2,'Bob',60,1),(3,'Cy',100,1),(4,'Di',70,2),(5,'Eli',55,2);
""")

sql = """SELECT e.name AS employee, e.salary AS emp_salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary
ORDER BY e.emp_id"""
sql_all = """SELECT e.name, m.name FROM employees e JOIN employees m ON e.manager_id = m.emp_id ORDER BY e.emp_id"""

s = con.execute(sql).fetchall()
print("SQL:", s)
print("all employee-manager pairs (Ann has no row):", con.execute(sql_all).fetchall())

emp = pd.read_sql("SELECT * FROM employees", con)
print("manager_id dtype:", emp["manager_id"].dtype)   # float64 because of the NULL
p = emp.merge(emp, left_on="manager_id", right_on="emp_id", suffixes=("_emp", "_mgr"))
p = p[p["salary_emp"] > p["salary_mgr"]].sort_values("emp_id_emp")
p = p[["name_emp", "salary_emp", "name_mgr", "salary_mgr"]]
print(p.to_string(index=False))

assert list(p.itertuples(index=False, name=None)) == s == [("Cy", 100, "Ann", 90), ("Di", 70, "Bob", 60)]
print("asserts passed (compared in emp_id order)")
