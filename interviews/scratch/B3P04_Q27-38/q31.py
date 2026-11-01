# Q31: top-N per group in pandas with tie awareness: head, nlargest (keep first/all), rank dense
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO emp VALUES (1,10,100),(2,10,90),(3,10,90),(4,10,80),(5,10,70),
                       (6,20,60),(7,20,60),(8,20,60),(9,20,50);
"""
SQL_RN = """
SELECT emp_id, dept_id, salary FROM (
  SELECT emp_id, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS pos
  FROM emp) WHERE pos <= 2 ORDER BY dept_id, salary DESC, emp_id
"""
SQL_RANK = """
SELECT emp_id, dept_id, salary FROM (
  SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS pos
  FROM emp) WHERE pos <= 2 ORDER BY dept_id, salary DESC, emp_id
"""
SQL_DENSE = """
SELECT emp_id, dept_id, salary FROM (
  SELECT emp_id, dept_id, salary, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS pos
  FROM emp) WHERE pos <= 2 ORDER BY dept_id, salary DESC, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
sql_rn, sql_rank, sql_dense = q(SQL_RN), q(SQL_RANK), q(SQL_DENSE)
for name, d in [("ROW_NUMBER <= 2", sql_rn), ("RANK <= 2", sql_rank), ("DENSE_RANK <= 2", sql_dense)]:
    print("SQL", name, "-> emp_ids", d["emp_id"].tolist())

emp = pd.read_sql_query("SELECT * FROM emp ORDER BY emp_id", con)   # row order = emp_id order
# pd:main
n = 2
head_df = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
              .groupby("dept_id").head(n))
nl_first = emp.groupby("dept_id")["salary"].nlargest(n)                # keep='first' is the default
nl_all = emp.groupby("dept_id")["salary"].nlargest(n, keep="all")
dense_df = emp[emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False) <= n]
# pd:end
ids = lambda d: sorted(d["emp_id"].tolist())
nl_first_ids = sorted(emp.loc[nl_first.index.get_level_values(1), "emp_id"].tolist())
nl_all_ids = sorted(emp.loc[nl_all.index.get_level_values(1), "emp_id"].tolist())
print("\npandas head(2) after sort   :", ids(head_df), "| index type:", type(head_df.index).__name__)
print("pandas nlargest keep='first':", nl_first_ids, "| index levels:", list(nl_first.index.names))
print("pandas nlargest keep='all'  :", nl_all_ids, "| index levels:", list(nl_all.index.names))
print("pandas dense rank <= 2      :", ids(dense_df), "| index type:", type(dense_df.index).__name__)
print("\nnlargest keep='first' as a Series:"); print(nl_first.to_string())

assert ids(head_df) == sql_rn["emp_id"].tolist() == [1, 2, 6, 7]
assert nl_first_ids == sql_rn["emp_id"].tolist()          # only because emp is in emp_id order
assert nl_all_ids == sorted(sql_rank["emp_id"].tolist()) == [1, 2, 3, 6, 7, 8]
assert ids(dense_df) == sorted(sql_dense["emp_id"].tolist()) == [1, 2, 3, 6, 7, 8, 9]
# keep='first' follows the frame's row order: reverse the rows and it picks the other tied row
rev = emp.iloc[::-1]
rev_first = sorted(rev.loc[rev.groupby("dept_id")["salary"].nlargest(n).index.get_level_values(1), "emp_id"].tolist())
print("\nsame nlargest keep='first' on the frame in reverse row order picks emp_ids:", rev_first)
assert rev_first != sql_rn["emp_id"].tolist()
print("asserts passed (compared as sorted emp_id lists)")
