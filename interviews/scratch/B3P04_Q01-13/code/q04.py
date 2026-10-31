# Q4: top 3 per department with ROW_NUMBER and a unique tie-breaker
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),(4,'Dev',10,70),
  (5,'Esha',10,70),(6,'Farid',20,90),(7,'Gita',20,80),(8,'Hari',20,NULL),
  (9,'Ila',30,55),(10,'Jay',30,55),(11,'Kiran',30,55),(12,'Lata',30,55);
"""
# tie-break stated: lower emp_id first among equal salaries
SQL_MAIN = """
WITH ranked AS (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT dept_id, emp_id, name, salary, rn
FROM ranked
WHERE rn <= 3
ORDER BY dept_id, rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:head
ordered = emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = ordered.groupby("dept_id").head(3)
# pd:end
# pd:cum
ordered = ordered.assign(rn=ordered.groupby("dept_id").cumcount() + 1)
pd_cum = ordered[ordered["rn"] <= 3][["dept_id", "emp_id", "name", "salary", "rn"]]
# pd:end
print("\ncumcount() starts at 0, so rn = cumcount()+1:",
      ordered.groupby("dept_id").cumcount().tolist())
# compared after sorting by dept_id, rn (head keeps the sorted order but has no rn column)
pd.testing.assert_frame_equal(sql_df, pd_cum.reset_index(drop=True), check_dtype=False)
assert pd_head["emp_id"].tolist() == sql_df["emp_id"].tolist()
print("rows per department:", sql_df.groupby("dept_id").size().to_dict())
print("asserts passed: SQL == head(3) emp_ids == cumcount version")
