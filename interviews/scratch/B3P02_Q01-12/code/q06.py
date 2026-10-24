# Q6: NULL join keys in SQL versus NaN join keys in pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
CREATE TABLE departments(dept_id INTEGER, dept_name TEXT);          -- dept_id nullable, no PK
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',NULL),(4,'Dev',NULL),(5,'Esha',30);
INSERT INTO departments VALUES (10,'Sales'),(20,'Eng'),(NULL,'Unassigned');
""")
print("NULL = NULL ->", con.execute("SELECT NULL = NULL").fetchone()[0],
      "| NULL IS NULL ->", con.execute("SELECT NULL IS NULL").fetchone()[0])

q = lambda on, how="LEFT": f"""SELECT e.name, d.dept_name FROM employees e {how} JOIN departments d ON {on}
ORDER BY e.emp_id"""
sql_inner = q("e.dept_id = d.dept_id", "INNER")
sql_left = q("e.dept_id = d.dept_id")
sql_is = q("e.dept_id IS d.dept_id")
sql_isndf = q("e.dept_id IS NOT DISTINCT FROM d.dept_id")
run = lambda s: con.execute(s).fetchall()
print("INNER  =        :", run(sql_inner))
print("LEFT   =        :", run(sql_left))
print("LEFT   IS       :", run(sql_is))
print("LEFT   IS NOT DISTINCT FROM (runs on SQLite 3.45):", run(sql_isndf))
assert run(sql_is) == run(sql_isndf)

emp = pd.read_sql("SELECT * FROM employees", con)
dep = pd.read_sql("SELECT * FROM departments", con)
print("dept_id dtypes:", emp["dept_id"].dtype, dep["dept_id"].dtype)

key = lambda df: list(df[["name", "dept_name"]].itertuples(index=False, name=None))
fix = lambda t: [(a, None if b != b else b) for a, b in t]     # NaN -> None for comparison
p_inner = emp.merge(dep, on="dept_id", how="inner").sort_values("emp_id")
p_left = emp.merge(dep, on="dept_id", how="left").sort_values("emp_id")
print("pandas inner merge (NaN keys match NaN):", key(p_inner))
print("pandas left  merge                     :", key(p_left))

# pandas default equals the SQLite IS version, not the = version
assert fix(key(p_left)) == run(sql_is)
# to get SQL = behaviour in pandas, drop NaN keys on both sides first
emp_k = emp.dropna(subset=["dept_id"]); dep_k = dep.dropna(subset=["dept_id"])
p_sql_like_inner = emp_k.merge(dep_k, on="dept_id", how="inner").sort_values("emp_id")
p_sql_like_left = emp.merge(dep_k, on="dept_id", how="left").sort_values("emp_id")
assert key(p_sql_like_inner) == run(sql_inner)
assert fix(key(p_sql_like_left)) == run(sql_left)
print("pandas with NaN keys dropped from the right side matches SQL =:", fix(key(p_sql_like_left)))
many = pd.DataFrame({"dept_id": [None, None], "who": ["x", "y"]}).merge(pd.DataFrame({"dept_id": [None, None, None], "d": [1, 2, 3]}), on="dept_id")
print("2 NaN keys x 3 NaN keys in pandas ->", len(many), "rows")
assert len(many) == 6
print("asserts passed (compared in emp_id order)")
