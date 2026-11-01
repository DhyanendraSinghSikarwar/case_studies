# Q38: median per group with ROW_NUMBER and COUNT (no PERCENTILE_CONT in SQLite)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,50),(2,'Ben',10,60),(3,'Chitra',10,70),(4,'Dev',10,80),(5,'Esha',10,NULL),
 (6,'Farid',20,40),(7,'Gita',20,40),(8,'Hari',20,100),
 (9,'Ila',30,55),
 (10,'Jay',40,NULL),(11,'Kiran',40,NULL),
 (12,'Lata',50,10),(13,'Manu',50,20),(14,'Nina',50,20),(15,'Om',50,30);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id)                         AS cnt
  FROM employees
  WHERE salary IS NOT NULL)
SELECT dept_id, AVG(salary) AS median_salary
FROM ranked
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
GROUP BY dept_id
ORDER BY dept_id
"""
SQL_WRONG = SQL_MAIN.replace("  WHERE salary IS NOT NULL)", "  )")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL median per department (NULL salaries filtered first):"); print(sql_df.to_string(index=False))
wrong = pd.read_sql_query(SQL_WRONG, con)
print("\nWRONG (NULL filter removed; NULLs sort first and count in cnt):"); print(wrong.to_string(index=False))
assert wrong["median_salary"].tolist()[0] == 60.0 and wrong["median_salary"].isna().any()
print("\nmiddle positions used, for each count:", {c: sorted({(c + 1) // 2, (c + 2) // 2}) for c in (1, 2, 3, 4)})

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
med = emp.groupby("dept_id")["salary"].median()
pd_df = med.dropna().rename("median_salary").reset_index()
# pd:end
print("\npandas groupby median (all-NaN dept 40 shows NaN):", med.to_dict())
print("pandas quantile(0.5) default interpolation:", emp.groupby("dept_id")["salary"].quantile(0.5).to_dict())
print("quantile lower :", emp.groupby("dept_id")["salary"].quantile(0.5, interpolation="lower").dropna().to_dict())
print("quantile higher:", emp.groupby("dept_id")["salary"].quantile(0.5, interpolation="higher").dropna().to_dict())
# compared after sorting by dept_id; dept 40 (all NULL) has no SQL row, so NaN rows are dropped from pandas
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("dept_id").reset_index(drop=True), check_dtype=False)
assert med.isna().tolist() == [False, False, False, True, False]
assert sql_df["median_salary"].tolist() == [65.0, 40.0, 55.0, 20.0]
print("asserts passed: SQL ROW_NUMBER/COUNT median == pandas groupby median (dept 40 absent in SQL, NaN in pandas)")
