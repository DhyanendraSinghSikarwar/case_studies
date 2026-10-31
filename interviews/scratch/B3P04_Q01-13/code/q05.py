# Q5: second highest distinct salary (LeetCode 176 style)
import sqlite3
import pandas as pd

DATASETS = {
    "A tied top":      [(1, "Asha", 100), (2, "Ben", 100), (3, "Chitra", 90), (4, "Dev", 80)],
    "B one distinct":  [(1, "Asha", 50), (2, "Ben", 50)],
    "C empty":         [],
    "D NULLs":         [(1, "Asha", None), (2, "Ben", 70), (3, "Chitra", 70), (4, "Dev", 40)],
}
SQL_MAIN = """
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT MAX(salary) AS second_highest FROM ranked WHERE rnk = 2
"""
SQL_RANK2 = """
WITH ranked AS (SELECT salary, RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees WHERE salary IS NOT NULL)
SELECT MAX(salary) FROM ranked WHERE rnk = 2
"""
SQL_ROWNUM2 = """
WITH ranked AS (SELECT salary, ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn FROM employees WHERE salary IS NOT NULL)
SELECT MAX(salary) FROM ranked WHERE rn = 2
"""

# pd:main
def second_highest(s):
    top2 = s.dropna().drop_duplicates().nlargest(2)
    return int(top2.iloc[1]) if len(top2) == 2 else None
# pd:end

print("dataset          | DENSE_RANK | RANK=2 | ROW_NUMBER=2 | pandas")
for name, rows in DATASETS.items():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)")
    con.executemany("INSERT INTO employees VALUES (?,?,?)", rows)
    a = con.execute(SQL_MAIN).fetchone()[0]
    b = con.execute(SQL_RANK2).fetchone()[0]
    c = con.execute(SQL_ROWNUM2).fetchone()[0]
    emp = pd.DataFrame(rows, columns=["emp_id", "name", "salary"]).astype({"salary": "float"})
    p = second_highest(emp["salary"])
    print("%-16s | %-10s | %-6s | %-12s | %s" % (name, a, b, c, p))
    assert a == p, (name, a, p)
print("asserts passed: DENSE_RANK wrapper == pandas on all four datasets (None means NULL)")
