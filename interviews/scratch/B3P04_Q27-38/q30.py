# Q30: pandas rank and NaN handling versus SQL
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO emp VALUES (1,10,70),(2,10,50),(3,10,NULL),(4,10,70),(5,20,NULL),(6,20,40),(7,20,40),(8,20,60);
"""
SQL_MAIN = """
SELECT emp_id, salary,
  RANK()       OVER (ORDER BY salary DESC NULLS LAST)         AS rk,
  DENSE_RANK() OVER (ORDER BY salary DESC NULLS LAST)         AS dr,
  ROW_NUMBER() OVER (ORDER BY salary DESC NULLS LAST, emp_id) AS rn
FROM emp ORDER BY emp_id
"""
SQL_GROUP = """
SELECT emp_id, dept_id, salary,
  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk_in_dept
FROM emp WHERE salary IS NOT NULL
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_grp = pd.read_sql_query(SQL_GROUP, con)
print("SQL (NULLs ranked last):"); print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM emp ORDER BY emp_id", con)
# pd:main
s = emp["salary"]
methods = pd.DataFrame({m: s.rank(method=m, ascending=False)
                        for m in ["average", "min", "max", "first", "dense"]})
na = pd.DataFrame({o: s.rank(method="min", ascending=False, na_option=o)
                   for o in ["keep", "top", "bottom"]})
pct = pd.DataFrame({"pct_max": s.rank(method="max", ascending=False, pct=True),
                    "pct_min": s.rank(method="min", ascending=False, pct=True)})
pd_df = pd.DataFrame({"emp_id": emp["emp_id"], "salary": s,
                      "rk": s.rank(method="min", ascending=False, na_option="bottom"),
                      "dr": s.rank(method="dense", ascending=False, na_option="bottom"),
                      "rn": s.rank(method="first", ascending=False, na_option="bottom")})
in_dept = emp.dropna(subset=["salary"]).copy()
in_dept["rk_in_dept"] = in_dept.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("Int64")
# pd:end
print("\npandas methods (ascending=False, na_option='keep'):"); print(methods.assign(salary=s).to_string())
print("\nna_option (method='min'):"); print(na.assign(salary=s).to_string())
print("\npct=True (NaN not counted in n=6):"); print(pct.assign(salary=s).round(4).to_string())
print("dtype of rank:", s.rank().dtype, "| after cast to nullable Int64:", s.rank(method="min").astype("Int64").dtype)
print("\nper-department rank (NaN rows dropped first):"); print(in_dept.to_string(index=False))

pd_cmp = pd_df.astype({"rk": "int64", "dr": "int64", "rn": "int64"})
pd.testing.assert_frame_equal(sql_df, pd_cmp, check_dtype=False)   # both in emp_id order
pd.testing.assert_frame_equal(sql_grp.reset_index(drop=True),
                              in_dept.astype({"rk_in_dept": "int64"}).reset_index(drop=True), check_dtype=False)
# ranks without a tie-breaker: method='first' follows row order, so rn is deterministic only because emp is sorted by emp_id
print("asserts passed: SQL RANK/DENSE_RANK/ROW_NUMBER == pandas min/dense/first (compared in emp_id order); per-dept == groupby rank")
