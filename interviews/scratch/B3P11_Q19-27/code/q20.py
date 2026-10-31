# Q20: correlated subquery vs derived table vs window (SQLite in-memory + pandas)
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

A = """SELECT e.emp_id FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.emp_id"""
B = """SELECT e.emp_id FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal ORDER BY e.emp_id"""
C = """SELECT emp_id FROM (SELECT emp_id, salary, AVG(salary) OVER (PARTITION BY dept_id) AS avg_sal FROM employees)
WHERE salary > avg_sal ORDER BY emp_id"""
FORMS = (("A correlated", A), ("B derived join", B), ("C window", C))

def build(n, n_dept, seed):
    rnd = random.Random(seed)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT)")
    con.executemany("INSERT INTO employees VALUES (?,?,?,?)",
        [(i, rnd.randint(1, n_dept), rnd.randint(20, 200) * 1000, "20%02d-%02d-01" % (rnd.randint(10, 24), rnd.randint(1, 12))) for i in range(1, n + 1)])
    con.commit()
    return con

def pandas_answer(df):
    m = df.groupby("dept_id")["salary"].transform("mean")
    return df.loc[df["salary"] > m, ["emp_id"]].sort_values("emp_id").reset_index(drop=True)

# tiny sample
con = sqlite3.connect(":memory:")
con.executescript("""CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT);
INSERT INTO employees VALUES (1,10,100,'2020-01-01'),(2,10,200,'2021-01-01'),(3,10,300,'2022-01-01'),(4,20,50,'2020-05-01'),(5,20,50,'2021-05-01'),(6,30,70,'2023-01-01');""")
for name, sql in FORMS:
    print("tiny", name, [r[0] for r in con.execute(sql)])
print("tiny dept avgs:", con.execute("SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id").fetchall())

# the unindexed correlated form is quadratic: measure it on small tables only
print("\nCorrelated form WITHOUT an index, VM steps by table size (200 departments):")
small = {}
for n in (500, 1000, 2000):
    c = build(n, 200, 20)
    rows, st = steps(c, A)
    small[n] = st
    print("  n=%5d  steps %10d  steps/n^2 = %.2f" % (n, st, st / n / n))
print("  plan:", plan(build(500, 200, 20), A))
est = small[2000] / 2000 / 2000 * 50000 * 50000
print("  extrapolated to 50,000 rows by steps/n^2 (an estimate, NOT run): about %.1e steps" % est)

con = build(50000, 200, 20)
df = pd.read_sql("SELECT * FROM employees", con)
exp = pandas_answer(df)
print("\n50,000 employees, 200 departments, pandas answer rows:", len(exp))
for idx in (False, True):
    if idx:
        con.execute("CREATE INDEX ix_dept_sal ON employees(dept_id, salary)"); con.commit()
    print("--- index on (dept_id, salary):", idx)
    for name, sql in FORMS:
        if name.startswith("A") and not idx:
            print("  %-15s not run at 50,000 rows without an index (quadratic, see above)" % name)
            continue
        rows, n = steps(con, sql)
        pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["emp_id"]), exp)
        print("  %-15s rows %5d  VM steps %10d" % (name, len(rows), n))
    for name, sql in FORMS:
        print("  PLAN", name)
        for l in plan(con, sql): print("     ", l)
print("asserts passed: every form run returned the pandas rows (compared sorted by emp_id)")
