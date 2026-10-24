# Q6: Nth highest distinct salary with N as a parameter
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',100),(2,'Ben',100),(3,'Chitra',90),(4,'Dev',80),
  (5,'Esha',80),(6,'Farid',70),(7,'Gita',NULL);
"""
SQL_MAIN = """
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS nth_salary FROM ranked WHERE rnk = ?
"""
SQL_OFFSET = """
SELECT (SELECT DISTINCT salary FROM employees WHERE salary IS NOT NULL
        ORDER BY salary DESC LIMIT 1 OFFSET ? - 1) AS nth_salary
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
def nth_highest(s, n):
    u = s.dropna().drop_duplicates().sort_values(ascending=False)
    return int(u.iloc[n - 1]) if 1 <= n <= len(u) else None
# pd:end

print("N | DENSE_RANK | LIMIT/OFFSET | pandas")
for n in [0, 1, 2, 3, 4, 5, 10]:
    a = con.execute(SQL_MAIN, (n,)).fetchone()[0]
    b = con.execute(SQL_OFFSET, (n,)).fetchone()[0]
    p = nth_highest(emp["salary"], n)
    print("%d | %-10s | %-12s | %s" % (n, a, b, p))
    assert a == p
    if n >= 1:
        assert b == p
print("distinct values:", sorted(emp["salary"].dropna().unique().tolist(), reverse=True))
print("without the 1 <= n guard pandas iloc[-1] would return:", int(emp["salary"].dropna().drop_duplicates().sort_values(ascending=False).iloc[0 - 1]))
print("asserts passed: DENSE_RANK == pandas for N = 0..10; OFFSET version == for N >= 1")
