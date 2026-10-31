# Q37: ORDER BY inside OVER versus the outer ORDER BY
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,90),(3,'Chitra',20,90),
                             (4,'Dev',20,50),(5,'Esha',10,70),(6,'Farid',20,60);
"""
SQL_NAIVE = """
SELECT emp_id, name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
FROM employees
"""
SQL_NAIVE_TWO = """
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
       ROW_NUMBER() OVER (ORDER BY name DESC)   AS rn_name
FROM employees
"""
SQL_MAIN = """
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn
FROM employees
ORDER BY rn
"""
SQL_FIXED_TWO = """
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn,
       ROW_NUMBER() OVER (ORDER BY name DESC)           AS rn_name
FROM employees
ORDER BY rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
naive, naive_two, sql_df, fixed_two = q(SQL_NAIVE), q(SQL_NAIVE_TWO), q(SQL_MAIN), q(SQL_FIXED_TWO)
print("NAIVE (no outer ORDER BY, no tie-break), rows in the order returned:"); print(naive.to_string(index=False))
print("\nNAIVE with a second window added (same table, same rn expression):"); print(naive_two.to_string(index=False))
tied = lambda d: dict(zip(d["name"], d["rn"]))
print("\nrn of the tied 90s: first query", {k: tied(naive)[k] for k in ("Ben", "Chitra")},
      "| second query", {k: tied(naive_two)[k] for k in ("Ben", "Chitra")},
      "| numbering identical across queries:", tied(naive) == tied(naive_two))
print("\nFIXED (tie-break in OVER, ORDER BY rn outside):"); print(sql_df.to_string(index=False))
print("\nFIXED with the second window added; rn unchanged:", dict(zip(fixed_two["name"], fixed_two["rn"])) == dict(zip(sql_df["name"], sql_df["rn"])))

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
ranked = emp.assign(rn=emp["salary"].rank(method="first", ascending=False).astype("int64"))
pd_df = ranked.sort_values("rn")
# pd:end
print("\npandas rank() keeps the row order (emp_id order):", ranked["emp_id"].tolist())
print("pandas sort_values('rn') returns the rows in ranked order:", pd_df["emp_id"].tolist())
assert ranked["emp_id"].tolist() == emp["emp_id"].tolist()
# compared in rn order (both sorted by rn)
cols = ["emp_id", "name", "salary", "rn"]
pd.testing.assert_frame_equal(sql_df[cols].reset_index(drop=True), pd_df[cols].reset_index(drop=True), check_dtype=False)
assert fixed_two["rn"].tolist() == sql_df["rn"].tolist()
print("asserts passed: SQL (tie-break + outer ORDER BY) == pandas rank(method='first') + sort_values")
