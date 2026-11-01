# Q29: NULLs inside window ORDER BY (SQLite 3.45) and pandas na_option
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,50),(3,'Chitra',10,NULL),
  (4,'Dev',10,70),(5,'Esha',10,NULL),(6,'Farid',10,40);
"""
SQL_MAIN = """
SELECT emp_id, name, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn_desc,
  RANK()       OVER (ORDER BY salary DESC)         AS rk_desc,
  ROW_NUMBER() OVER (ORDER BY salary ASC, emp_id)  AS rn_asc,
  RANK()       OVER (ORDER BY salary ASC)          AS rk_asc,
  RANK()       OVER (ORDER BY salary DESC NULLS FIRST) AS rk_desc_nf,
  RANK()       OVER (ORDER BY salary ASC  NULLS LAST)  AS rk_asc_nl
FROM employees
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (SQLite", sqlite3.sqlite_version + "):"); print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
s = emp["salary"]
pd_df = emp[["emp_id", "name", "salary"]].copy()
pd_df["rn_desc"] = s.rank(method="first", ascending=False, na_option="bottom")
pd_df["rk_desc"] = s.rank(method="min", ascending=False, na_option="bottom")
pd_df["rn_asc"] = s.rank(method="first", ascending=True, na_option="top")
pd_df["rk_asc"] = s.rank(method="min", ascending=True, na_option="top")
pd_df["rk_desc_nf"] = s.rank(method="min", ascending=False, na_option="top")
pd_df["rk_asc_nl"] = s.rank(method="min", ascending=True, na_option="bottom")
keep = s.rank(method="min", ascending=False, na_option="keep")
# pd:end
pd_df = pd_df.astype({c: "int64" for c in pd_df.columns if c.startswith(("rn_", "rk_"))})
print("\npandas (na_option 'bottom' for DESC default, 'top' for ASC default):"); print(pd_df.to_string(index=False))
print("\nna_option='keep' (no SQL equivalent):", keep.tolist())
# compared by emp_id (both already in emp_id order)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

# NULL keys are peers: same rank, and ROW_NUMBER only separates them via the tie-breaker
assert sql_df.loc[sql_df.salary.isna(), "rk_desc"].nunique() == 1
# without a tie-breaker, ROW_NUMBER on the NULL rows is allowed to vary; show it is only fixed by emp_id
print("\nNULL rows get rn_desc", sql_df.loc[sql_df.salary.isna(), "rn_desc"].tolist(),
      "because emp_id breaks the tie")
print("asserts passed: SQL == pandas for all six rank columns")
