# Q25: DELETE duplicates with a subquery on the same table: NOT IN vs NOT EXISTS, NULL email, NULL id
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO employees VALUES
 (1,'Asha','a@x.com'),(2,'Asha R','a@x.com'),
 (3,'Ben','b@x.com'),(4,'Ben K','b@x.com'),(5,'Ben K2','b@x.com'),
 (6,'Chitra','c@x.com'),
 (7,'Dev',NULL),(8,'Eve',NULL);
CREATE TABLE emp_loose(emp_id INTEGER, email TEXT);
INSERT INTO emp_loose VALUES (1,'a@x.com'),(2,'a@x.com'),(NULL,'b@x.com'),(NULL,'b@x.com'),(5,'c@x.com');
"""
SQL_NOT_IN = """
DELETE FROM employees
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email)
"""
SQL_NOT_EXISTS = """
DELETE FROM employees
WHERE EXISTS (SELECT 1 FROM employees e2
              WHERE e2.email = employees.email
                AND e2.emp_id < employees.emp_id)
"""
SQL_WITH_DELETE = """
WITH keep AS (SELECT MIN(emp_id) AS id FROM employees GROUP BY email)
DELETE FROM employees WHERE emp_id NOT IN (SELECT id FROM keep)
"""
SQL_LOOSE_NOT_IN = """
DELETE FROM emp_loose
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM emp_loose GROUP BY email)
"""
SQL_LOOSE_NOT_EXISTS = """
DELETE FROM emp_loose
WHERE NOT EXISTS (SELECT 1 FROM (SELECT MIN(emp_id) AS m FROM emp_loose GROUP BY email) k
                  WHERE k.m = emp_loose.emp_id)
"""
def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c
BASE = fresh().total_changes          # rows inserted by the setup script
def run(sql, tbl="employees"):
    c = fresh()
    c.execute(sql)
    rows = c.execute(f"SELECT * FROM {tbl} ORDER BY emp_id").fetchall()
    return rows, c.total_changes - BASE

con = fresh()
emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
print("before:", len(emp), "rows")
rows_in, n_in = run(SQL_NOT_IN)
rows_ex, n_ex = run(SQL_NOT_EXISTS)
rows_with, n_with = run(SQL_WITH_DELETE)
print("\nNOT IN (MIN(emp_id) ... GROUP BY email):  deleted", n_in, "kept ids", [r[0] for r in rows_in])
print("NOT EXISTS (earlier row, same email):     deleted", n_ex, "kept ids", [r[0] for r in rows_ex])
print("WITH keep AS (...) DELETE ... NOT IN:      deleted", n_with, "kept ids", [r[0] for r in rows_with])

# pd:main
dedup_all = emp.sort_values("emp_id").drop_duplicates(subset="email", keep="first")        # NaN emails count as equal
dedup_sql_exists = emp[emp["email"].isna() | ~emp.duplicated(subset="email", keep="first")]  # NULL emails never match
# pd:end
print("\npandas drop_duplicates(subset='email', keep='first') ids:", dedup_all["emp_id"].tolist())
print("pandas NULL emails kept (like NOT EXISTS) ids:           ", dedup_sql_exists["emp_id"].tolist())

loose_in, _ = run(SQL_LOOSE_NOT_IN, "emp_loose")
loose_ex, _ = run(SQL_LOOSE_NOT_EXISTS, "emp_loose")
print("\nemp_loose has NULL emp_id rows (no primary key). Before: 5 rows")
print("  NOT IN with a NULL in the list, rows left:", len(loose_in), loose_in)
print("  NOT EXISTS form, rows left:               ", len(loose_ex), loose_ex)

assert [r[0] for r in rows_in] == [r[0] for r in rows_with] == dedup_all["emp_id"].tolist() == [1, 3, 6, 7]
assert [r[0] for r in rows_ex] == dedup_sql_exists["emp_id"].tolist() == [1, 3, 6, 7, 8]
assert len(loose_in) == 5
print("\nasserts passed: NOT IN == WITH variant == drop_duplicates (ids 1,3,6,7); NOT EXISTS == pandas with NULL emails kept (ids 1,3,6,7,8); compared as lists of emp_id sorted ascending")
