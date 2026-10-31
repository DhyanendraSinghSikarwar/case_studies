# Q4: NULL inside CASE, special bonus with a NULL name, COALESCE / IFNULL / NULLIF / IIF.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(employee_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, dept TEXT);
INSERT INTO employees VALUES
 (1,'Asha',60000,'Eng'),(2,'Meera',40000,'Ops'),(3,'Mohan',50000,'Eng'),(4,NULL,30000,'Ops'),
 (5,NULL,70000,'Eng'),(6,'Zoya',NULL,'Ops'),(7,'Ravi',50000,NULL),(8,'Hema',0,'Eng');
""")

def q(sql):
    return pd.read_sql(sql, con)

sql_band = """
SELECT employee_id, salary,
  CASE WHEN salary > 50000 THEN 'high' WHEN salary <= 50000 THEN 'low' END                  AS band_no_else,
  CASE WHEN salary > 50000 THEN 'high' ELSE 'not high' END                                  AS band_else,
  CASE salary WHEN NULL THEN 'is null' ELSE 'never matches' END                              AS simple_case_null,
  CASE WHEN salary IS NULL THEN 'unknown' WHEN salary > 50000 THEN 'high' ELSE 'low' END     AS band_safe,
  IIF(salary > 50000, 'high', 'low')                                                         AS iif_band
FROM employees ORDER BY employee_id
"""
print(q(sql_band).to_string(index=False)); print()

sql_bonus_naive = """
SELECT employee_id, name, salary,
  CASE WHEN employee_id % 2 = 1 AND name NOT LIKE 'M%' THEN salary ELSE 0 END AS bonus
FROM employees ORDER BY employee_id
"""
sql_bonus = """
SELECT employee_id, name, salary,
  CASE WHEN employee_id % 2 = 1 AND COALESCE(name, '') NOT LIKE 'M%' THEN salary ELSE 0 END AS bonus
FROM employees ORDER BY employee_id
"""
naive = q(sql_bonus_naive)
fixed = q(sql_bonus)
print(pd.DataFrame({"employee_id": naive.employee_id, "name": naive.name, "naive_bonus": naive.bonus,
                    "fixed_bonus": fixed.bonus}).to_string(index=False)); print()
print("NULL NOT LIKE 'M%' ->", con.execute("SELECT NULL NOT LIKE 'M%'").fetchone()[0], "(NULL, so the CASE takes ELSE 0)")

sql_funcs = """
SELECT employee_id,
       COALESCE(salary, 0)                  AS coalesce_,
       IFNULL(salary, -1)                   AS ifnull_,
       COALESCE(name, dept, 'n/a')          AS first_non_null,
       100.0 / NULLIF(salary, 0)            AS safe_div,
       salary / 1.0                         AS plain
FROM employees WHERE employee_id IN (1, 4, 6, 7, 8) ORDER BY employee_id
"""
print(q(sql_funcs).to_string(index=False)); print()
print("IFNULL with three arguments:", end=" ")
try:
    con.execute("SELECT IFNULL(NULL, NULL, 3)")
except sqlite3.Error as ex:
    print("error:", ex)
print("100.0 / 0 in SQLite (no NULLIF):", con.execute("SELECT 100.0 / 0").fetchone()[0], "(NULL, not an error)")

# pandas versions
emp = q("SELECT * FROM employees ORDER BY employee_id")
print("\npandas NaN comparisons: salary > 50000 for NaN ->", (emp.salary > 50000)[5])
band_trap = np.where(emp.salary > 50000, "high", "low")           # NaN silently becomes 'low'
band_safe = np.select([emp.salary.isna(), emp.salary > 50000], ["unknown", "high"], default="low")
print("np.where trap for Zoya:", band_trap[5], "| np.select with isna first:", band_safe[5])

odd = emp.employee_id % 2 == 1
starts_m = emp.name.str.startswith("M")
print("name.str.startswith('M') for the NULL name:", starts_m[3], "(pandas 3 str dtype gives False, not NaN)")
p_bonus = np.where(odd & ~starts_m, emp.salary, 0)               # NaN name counts as 'not M': same as the COALESCE fix
p_bonus = pd.Series(p_bonus).fillna(0)  # NaN salary would stay NaN in SQL; see the edge case
pd.testing.assert_series_equal(fixed.bonus.astype(float), p_bonus.astype(float), check_names=False)
assert naive.bonus.tolist() != fixed.bonus.tolist()
assert q(sql_band).band_safe.tolist() == list(band_safe)
print("asserts passed (employee_id order)")
