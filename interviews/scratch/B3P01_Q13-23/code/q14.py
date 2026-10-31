# ORDER BY with NULLs and ties: SQLite behaviour, portable NULLS LAST, multi-column, ordinal, ties, pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha','Eng',90),(2,'Ben','Eng',NULL),(3,'Chitra','Ops',70),
 (4,'Dev','Ops',90),(5,'Esha','Eng',70),(6,'Farid','Ops',NULL),(7,'Gita','Eng',90);
""")

def ids(q): return [r[0] for r in con.execute(q).fetchall()]

asc = ids("SELECT emp_id FROM employees ORDER BY salary, emp_id")
desc = ids("SELECT emp_id FROM employees ORDER BY salary DESC, emp_id")
print("SQLite ASC  (salary, emp_id):", asc)
print("SQLite DESC (salary DESC, emp_id):", desc)

nl_asc = ids("SELECT emp_id FROM employees ORDER BY salary NULLS LAST, emp_id")
nl_desc = ids("SELECT emp_id FROM employees ORDER BY salary DESC NULLS FIRST, emp_id")
print("NULLS LAST asc:", nl_asc, "| DESC NULLS FIRST:", nl_desc)

# Portable NULLS LAST: a CASE sort key (works where NULLS LAST is not supported)
sql_portable = """SELECT emp_id FROM employees
ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC, emp_id"""
portable = ids(sql_portable)
print("portable, salary DESC NULLS LAST, tie-break emp_id:", portable)

# multi-column + expression + ordinal
sql_multi = "SELECT emp_id, dept, salary FROM employees ORDER BY dept ASC, salary DESC, emp_id ASC"
print("dept ASC, salary DESC, emp_id ASC (NULL salary is last within each dept):")
print(con.execute(sql_multi).fetchall())
print("ordinal ORDER BY 2, 1:", con.execute("SELECT emp_id, dept FROM employees ORDER BY 2, 1").fetchall())
print("expression ORDER BY -salary (NULL stays NULL):", ids("SELECT emp_id FROM employees ORDER BY -salary, emp_id"))

# ties without tie-breaker: only salary key. Order among equals is up to the engine
print("ties, no tie-breaker (engine's choice, not a guarantee):", ids("SELECT emp_id FROM employees ORDER BY salary DESC"))

# pandas
df = pd.read_sql("SELECT * FROM employees", con)
p_asc = df.sort_values(["salary", "emp_id"])["emp_id"].tolist()                      # na_position='last' is the default
p_asc_first = df.sort_values(["salary", "emp_id"], na_position="first")["emp_id"].tolist()
p_desc = df.sort_values(["salary", "emp_id"], ascending=[False, True])["emp_id"].tolist()
p_desc_first = df.sort_values(["salary", "emp_id"], ascending=[False, True], na_position="first")["emp_id"].tolist()
print("pandas default asc (NaN last):", p_asc)
print("pandas asc na_position='first' (matches SQLite ASC):", p_asc_first)
print("pandas desc default (NaN last, matches SQLite DESC):", p_desc)
print("pandas desc na_position='first':", p_desc_first)

# stable sort: sort by salary only with kind='stable' keeps original row order among ties
st = df.sort_values("salary", ascending=False, kind="stable")["emp_id"].tolist()
print("pandas stable desc, salary only:", st)
st2 = df.sort_values("salary", kind="stable").sort_values("dept", kind="stable")["emp_id"].tolist()
print("two stable passes (salary then dept):", st2)

assert asc == p_asc_first                    # SQLite puts NULL first in ASC
assert desc == p_desc                        # SQLite puts NULL last in DESC
assert nl_asc == p_asc and nl_desc == p_desc_first
assert portable == df.sort_values(["salary", "emp_id"], ascending=[False, True])["emp_id"].tolist()
p_multi = df.sort_values(["dept", "salary", "emp_id"], ascending=[True, False, True])[["emp_id", "dept", "salary"]]
sql_multi_rows = con.execute(sql_multi).fetchall()
assert [(a, b, None if pd.isna(c) else int(c)) for a, b, c in p_multi.itertuples(index=False)] == sql_multi_rows
print("asserts passed")
