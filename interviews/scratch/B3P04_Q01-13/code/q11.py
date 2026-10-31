# Q11: debug, top-N per group returns more (or fewer) rows than expected
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,70),
  (5,'Esha',20,90),(6,'Farid',20,80),(7,'Gita',20,70),(8,'Hari',20,60);
"""
SQL_RANK = """
WITH r AS (SELECT emp_id, name, dept_id, salary,
                  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS k FROM employees)
SELECT dept_id, emp_id, name, salary, k FROM r WHERE k <= 3 ORDER BY dept_id, k, emp_id
"""
# exactly N: tie rule stated = lower emp_id first
SQL_ROWNUM = """
WITH r AS (SELECT emp_id, name, dept_id, salary,
                  ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS k FROM employees)
SELECT dept_id, emp_id, name, salary, k FROM r WHERE k <= 3 ORDER BY dept_id, k
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
rank_df = pd.read_sql_query(SQL_RANK, con)
rn_df = pd.read_sql_query(SQL_ROWNUM, con)
print("RANK <= 3:"); print(rank_df.to_string(index=False))
print("\nROW_NUMBER <= 3 (tie-break emp_id):"); print(rn_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
pd_rank = emp[emp.groupby("dept_id")["salary"].rank(method="min", ascending=False) <= 3]
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
              .groupby("dept_id").head(3))
# pd:end
# compared after sorting by dept_id, salary desc, emp_id
key = lambda d: d.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])["emp_id"].tolist()
assert key(pd_rank) == key(rank_df) and key(pd_head) == key(rn_df)
print("\nrows per dept  RANK:", rank_df.groupby("dept_id").size().to_dict(),
      " ROW_NUMBER:", rn_df.groupby("dept_id").size().to_dict())
print("tied at the cutoff but dropped by ROW_NUMBER:", sorted(set(rank_df["name"]) - set(rn_df["name"])))
print("asserts passed: RANK<=3 == pandas rank(method='min')<=3; ROW_NUMBER<=3 == sort_values + head(3)")
