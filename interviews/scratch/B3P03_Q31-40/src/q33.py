# Q33: NaN / NULL pitfalls: pandas vs SQL for the same subquery-style logic
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER);
INSERT INTO emp VALUES
 (1,'A',100),(2,'A',200),(3,'B',NULL),(4,'B',NULL),
 (5,NULL,300),(6,NULL,50),(7,'C',150);
"""
# NULL-safe correlation with IS (SQLite); standard SQL spells it IS NOT DISTINCT FROM (not executed here)
SQL_MAIN = """
SELECT o.emp_id, o.dept, o.salary,
       (SELECT AVG(i.salary) FROM emp i WHERE i.dept IS o.dept) AS dept_avg
FROM emp o
ORDER BY o.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
emp = pd.read_sql_query("SELECT * FROM emp", con)
print("emp (NULL shows as NaN / None in pandas):")
print(emp.to_string(index=False))
print("\nSQL: department average with a NULL-safe correlation (IS):")
print(sql_df.to_string(index=False))

# pd:main
pd_df = emp.assign(dept_avg=emp.groupby("dept", dropna=False)["salary"].transform("mean"))
# pd:end
print("\npandas transform('mean') with dropna=False:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("assert: SQL (IS correlation) == pandas (dropna=False); compared by emp_id")

print("\n--- the plain '=' correlation and the default groupby ---")
eq = pd.read_sql_query("SELECT o.emp_id, (SELECT AVG(i.salary) FROM emp i WHERE i.dept = o.dept) AS dept_avg FROM emp o ORDER BY o.emp_id", con)
dflt = emp.groupby("dept")["salary"].transform("mean")
print("SQL with '=':           ", eq["dept_avg"].tolist())
print("pandas default dropna: ", dflt.tolist())
print("NaN-key rows are NaN in both (emp 5, 6):", bool(np.isnan(eq["dept_avg"][[4, 5]]).all()), bool(dflt[[4, 5]].isna().all()))

print("\n--- salary > average ---")
n_sql = con.execute("SELECT COUNT(*) FROM emp WHERE salary > (SELECT AVG(salary) FROM emp)").fetchone()[0]
mean = emp.salary.mean()
print("mean skips NaN:", mean, "| SQL AVG:", con.execute("SELECT AVG(salary) FROM emp").fetchone()[0])
print("rows with salary > mean: pandas", int((emp.salary > mean).sum()), "| SQL", n_sql, "| NaN-salary rows among them:", int((emp.salary.isna() & (emp.salary > mean)).sum()), "of", int(emp.salary.isna().sum()), "NaN rows (all dropped)")
assert int((emp.salary > mean).sum()) == n_sql

print("\n--- equality with NaN / NULL ---")
print("pandas (salary == np.nan).sum():", int((emp.salary == np.nan).sum()))
print("SQL salary = NULL rows:", con.execute("SELECT COUNT(*) FROM emp WHERE salary = NULL").fetchone()[0],
      "| salary IS NULL rows:", con.execute("SELECT COUNT(*) FROM emp WHERE salary IS NULL").fetchone()[0],
      "| pandas isna:", int(emp.salary.isna().sum()))

print("\n--- IN / isin with NaN ---")
print("pandas salary.isin([np.nan]).sum():", int(emp.salary.isin([np.nan]).sum()), "(NaN matches NaN)")
print("pandas salary.isin([100, np.nan]).sum():", int(emp.salary.isin([100, np.nan]).sum()))
print("SQL salary IN (100, NULL):", con.execute("SELECT COUNT(*) FROM emp WHERE salary IN (100, NULL)").fetchone()[0], "(NULL never matches)")
print("SQL salary IN (NULL):", con.execute("SELECT COUNT(*) FROM emp WHERE salary IN (NULL)").fetchone()[0])
print("SQL NOT IN with a NULL in the list:", con.execute("SELECT COUNT(*) FROM emp WHERE emp_id NOT IN (SELECT salary FROM emp WHERE dept='B')").fetchone()[0],
      "(subquery returns NULLs)")
print("pandas ~isin of the same values:", int((~emp.emp_id.isin(emp.loc[emp.dept == "B", "salary"])).sum()), "(all 7 rows)")

print("\n--- GROUP BY and NaN group keys ---")
print("SQL GROUP BY dept:", con.execute("SELECT dept, COUNT(*), AVG(salary) FROM emp GROUP BY dept ORDER BY dept").fetchall())
print("pandas groupby default groups:", emp.groupby("dept")["salary"].size().to_dict())
print("pandas groupby dropna=False groups:", emp.groupby("dept", dropna=False)["salary"].size().to_dict())

print("\n--- sum of an all-NaN group ---")
print("SQL SUM per dept:", con.execute("SELECT dept, SUM(salary), TOTAL(salary) FROM emp WHERE dept IS NOT NULL GROUP BY dept ORDER BY dept").fetchall())
print("pandas sum:          ", emp.groupby("dept")["salary"].sum().to_dict())
print("pandas sum min_count=1:", emp.groupby("dept")["salary"].sum(min_count=1).to_dict())
print("pandas Series([nan]).sum():", pd.Series([np.nan]).sum(), "| min_count=1:", pd.Series([np.nan]).sum(min_count=1))
sql_sum = pd.read_sql_query("SELECT dept, SUM(salary) AS s FROM emp WHERE dept IS NOT NULL GROUP BY dept ORDER BY dept", con).set_index("dept")["s"]
pd.testing.assert_series_equal(sql_sum, emp.groupby("dept")["salary"].sum(min_count=1).rename("s"), check_dtype=False)
print("assert: SQL SUM == pandas sum(min_count=1)")
