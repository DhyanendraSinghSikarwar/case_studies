# Q34: idxmax versus rank-based selection of the top row per group, with ties and NaN
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
  (4,'Dev',20,NULL),(5,'Esha',20,60),(6,'Farid',20,NULL),
  (7,'Gita',30,NULL),(8,'Hari',30,NULL),(9,'Ila',40,50);
"""
SQL_RN = """
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS pos
  FROM employees WHERE salary IS NOT NULL)
WHERE pos = 1 ORDER BY dept_id
"""
SQL_RANK = """
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS pos
  FROM employees WHERE salary IS NOT NULL)
WHERE pos = 1 ORDER BY dept_id, emp_id
"""
SQL_NO_FILTER = """
SELECT emp_id, name, dept_id, salary FROM (
  SELECT emp_id, name, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC NULLS LAST, emp_id) AS pos
  FROM employees)
WHERE pos = 1 ORDER BY dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
sql_rn, sql_rank, sql_nf = q(SQL_RN), q(SQL_RANK), q(SQL_NO_FILTER)
print("SQL ROW_NUMBER = 1 (NULL salaries filtered):"); print(sql_rn.to_string(index=False))
print("\nSQL RANK = 1 (ties kept):"); print(sql_rank.to_string(index=False))
print("\nSQL ROW_NUMBER = 1 WITHOUT the NULL filter (NULLS LAST):"); print(sql_nf.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
valid = emp.dropna(subset=["salary"])
idx_df = emp.loc[valid.groupby("dept_id")["salary"].idxmax()]                       # one row per group, first tied row
max_df = emp[emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")]    # all tied rows
rank_df = emp[emp.groupby("dept_id")["salary"].rank(method="min", ascending=False) == 1]
nofilter_df = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True], na_position="last")
                  .groupby("dept_id").head(1))
# pd:end
# the raw calls on the data that has NaN
for label, fn in [("idxmax on all groups (skipna=True)", lambda: emp.groupby("dept_id")["salary"].idxmax()),
                  ("idxmax(skipna=False) on dept 20", lambda: emp[emp.dept_id == 20].groupby("dept_id")["salary"].idxmax(skipna=False)),
                  ("idxmax on dept 20 only (NaN rows, one real value, skipna=True)", lambda: emp[emp.dept_id == 20].groupby("dept_id")["salary"].idxmax()),
                  ("idxmax on dept 30 only (all NaN)", lambda: emp[emp.dept_id == 30].groupby("dept_id")["salary"].idxmax()),
                  ("idxmax on dept 10 only", lambda: emp[emp.dept_id == 10].groupby("dept_id")["salary"].idxmax())]:
    try:
        print(f"\n{label}: ->", fn().to_dict())
    except ValueError as ex:
        print(f"\n{label}: raises ValueError: {ex}")
print("\nidxmax after dropna ->", idx_df["emp_id"].tolist(), "| transform('max') ->", max_df["emp_id"].tolist(),
      "| rank==1 ->", rank_df["emp_id"].tolist(), "| sort+head(1) no filter ->", nofilter_df.sort_values("dept_id")["emp_id"].tolist())
key = ["emp_id", "name", "dept_id"]
srt = lambda d: d[key].sort_values("emp_id").reset_index(drop=True)
# compared after sorting by emp_id
pd.testing.assert_frame_equal(srt(idx_df), srt(sql_rn), check_dtype=False)
pd.testing.assert_frame_equal(srt(max_df), srt(sql_rank), check_dtype=False)
pd.testing.assert_frame_equal(srt(rank_df), srt(sql_rank), check_dtype=False)
pd.testing.assert_frame_equal(srt(nofilter_df), srt(sql_nf), check_dtype=False)
assert sql_nf["emp_id"].tolist() == [1, 5, 7, 9]
print("asserts passed: idxmax(after dropna) == ROW_NUMBER; transform('max') == rank==1 == RANK")
