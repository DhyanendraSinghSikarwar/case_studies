# Q37: median without window functions: LIMIT 2 - (n % 2) OFFSET (n - 1) / 2 wrapped in AVG
import sqlite3
import numpy as np
import pandas as pd

SQL_MAIN = """
SELECT AVG(salary) AS median_salary
FROM (SELECT salary FROM employees
      WHERE salary IS NOT NULL
      ORDER BY salary
      LIMIT 2 - (SELECT COUNT(salary) FROM employees) % 2
      OFFSET ((SELECT COUNT(salary) FROM employees) - 1) / 2)
"""
SQL_NO_NULL_FILTER = """
SELECT AVG(salary) FROM (SELECT salary FROM employees ORDER BY salary
      LIMIT 2 - (SELECT COUNT(salary) FROM employees) % 2
      OFFSET ((SELECT COUNT(salary) FROM employees) - 1) / 2)
"""
SQL_COUNT_STAR = """
SELECT AVG(salary) FROM (SELECT salary FROM employees WHERE salary IS NOT NULL ORDER BY salary
      LIMIT 2 - (SELECT COUNT(*) FROM employees) % 2
      OFFSET ((SELECT COUNT(*) FROM employees) - 1) / 2)
"""
SCENARIOS = {
    "odd (5 rows)":            [10, 20, 30, 40, 50],
    "even (6 rows)":           [10, 20, 30, 40, 50, 60],
    "ties (4 rows)":           [5, 5, 5, 9],
    "NULLs + 5 real (8 rows)": [10, None, 20, None, 30, 40, 50, None],
    "NULLs + 4 real (7 rows)": [10, None, 20, None, 30, 40, None],
    "one value":               [42],
    "all NULL":                [None, None],
    "empty table":             [],
}
print("%-26s %8s %8s %12s %12s" % ("scenario", "SQL", "pandas", "no NULL flt", "COUNT(*)"))
for name, vals in SCENARIOS.items():
    con = sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);")
    con.executemany("INSERT INTO employees(name, salary) VALUES (?, ?)", [("e%d" % i, v) for i, v in enumerate(vals)])
    sql_val = con.execute(SQL_MAIN).fetchone()[0]
    emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
    pd_val = emp["salary"].median()
# pd:end
    bad1 = con.execute(SQL_NO_NULL_FILTER).fetchone()[0]
    bad2 = con.execute(SQL_COUNT_STAR).fetchone()[0]
    same = (sql_val is None and np.isnan(pd_val)) or sql_val == pd_val
    assert same, (name, sql_val, pd_val)
    print("%-26s %8s %8s %12s %12s" % (name, sql_val, pd_val, bad1, bad2))
print("\nassert: SQL median == pandas median for every scenario (NaN/NULL where there is nothing to take the median of)")

con = sqlite3.connect(":memory:")
print("\nLIMIT / OFFSET with expressions on SQLite 3.45:")
print("  LIMIT 1 + 1       ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT 1 + 1").fetchall())
print("  OFFSET (3 - 1) / 2 ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT 5 OFFSET (3 - 1) / 2").fetchall())
print("  LIMIT (scalar subquery) ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT (SELECT 2)").fetchall())
print("  LIMIT -1 OFFSET 1 ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT -1 OFFSET 1").fetchall())
print("  OFFSET -1          ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT 2 OFFSET -1").fetchall())
print("  (0 - 1) / 2 in SQLite (integer division truncates toward zero) =", con.execute("SELECT (0 - 1) / 2").fetchone()[0])
print("  OFFSET without LIMIT ->", end=" ")
try:
    print(con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2) OFFSET 1").fetchall())
except sqlite3.Error as e:
    print("error:", e)
