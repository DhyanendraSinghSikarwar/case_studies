# Q36: second-highest distinct salary per department without window functions
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (1,'Eng'),(2,'Ops'),(3,'Sales'),(4,'Legal'),(5,'HR');
INSERT INTO employees VALUES
 (1,'Asha',1,100),(2,'Ben',1,100),(3,'Chitra',1,90),(4,'Dev',1,80),
 (5,'Esha',2,70),
 (6,'Farid',3,60),(7,'Gita',3,50),
 (8,'Hari',5,40),(9,'Isha',5,NULL),(10,'Jay',5,NULL);
"""
SQL_MAIN = """
SELECT d.dept_id, d.dept_name,
       (SELECT MAX(e.salary)
        FROM employees e
        WHERE e.dept_id = d.dept_id
          AND e.salary < (SELECT MAX(x.salary) FROM employees x WHERE x.dept_id = d.dept_id)
       ) AS second_highest
FROM departments d
ORDER BY d.dept_id
"""
# the Nth-highest version: count distinct higher salaries (generalises to N)
SQL_COUNT = """
SELECT d.dept_id, d.dept_name,
       (SELECT DISTINCT e.salary FROM employees e
        WHERE e.dept_id = d.dept_id
          AND (SELECT COUNT(DISTINCT x.salary) FROM employees x
               WHERE x.dept_id = e.dept_id AND x.salary > e.salary) = 1
       ) AS second_highest
FROM departments d
ORDER BY d.dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
cnt_df = pd.read_sql_query(SQL_COUNT, con)
print("SQL (MAX below the department MAX):")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, cnt_df)
print("\nassert: MAX-below-MAX == count-of-higher-distinct-salaries version")

departments = pd.read_sql_query("SELECT * FROM departments", con)
employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def second_distinct(s):
    vals = np.sort(s.dropna().unique())[::-1]
    return vals[1] if len(vals) > 1 else np.nan
second = employees.groupby("dept_id")["salary"].apply(second_distinct).rename("second_highest").reset_index()
pd_df = departments.merge(second, on="dept_id", how="left").sort_values("dept_id").reset_index(drop=True)
# pd:end
print("\npandas (unique, sort descending, take the second):")
print(pd_df.to_string(index=False))
# compared by dept_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nassert: SQL == pandas")

# the tempting nlargest version is wrong when the top salary is tied
nl = employees.groupby("dept_id")["salary"].apply(lambda s: s.nlargest(2).iloc[-1] if s.notna().sum() > 0 else np.nan)
print("\nnlargest(2) without drop_duplicates, last value per dept:", nl.to_dict(), "(dept 1 gives 100, not 90)")
nl2 = employees.groupby("dept_id")["salary"].apply(lambda s: s.drop_duplicates().nlargest(2).iloc[-1])
print("with drop_duplicates, last of nlargest(2):", nl2.to_dict(), "(dept 2 gives its only salary, 70, not NULL)")

# inner join to the employees only would lose Legal (dept 4, no employees)
lost = con.execute("""SELECT d.dept_id FROM departments d JOIN employees e ON e.dept_id = d.dept_id GROUP BY d.dept_id""").fetchall()
print("\ndepartments with at least one employee:", [r[0] for r in lost], "(Legal, dept 4, would vanish without driving from departments)")
