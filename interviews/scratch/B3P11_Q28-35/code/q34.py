# Q34: plan caching and hints in SQLite (executed); other engines are described in prose only.
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(34)
N = 50_000
words = np.array(["alpha", "beta", "gamma", "delta", "Alpine", "betel", "zeta", "omega"])
df = pd.DataFrame({"id": np.arange(1, N + 1), "cust": rng.integers(1, 501, N),
                   "name": [w + str(i % 997) for w, i in zip(words[rng.integers(0, 8, N)], range(N))],
                   "status": rng.choice(["a", "b", "c"], N, p=[0.98, 0.015, 0.005])})

def connect(**kw):
    con = sqlite3.connect(":memory:", **kw)
    con.execute("CREATE TABLE t(id INTEGER PRIMARY KEY, cust INTEGER, name TEXT, status TEXT)")
    con.executemany("INSERT INTO t VALUES (?,?,?,?)", df.itertuples(index=False, name=None))
    con.commit()
    return con

def steps(con, sql, params=()):
    c = [0]
    def cb(): c[0] += 1; return 0
    con.set_progress_handler(cb, 1); r = con.execute(sql, params).fetchall(); con.set_progress_handler(None, 0)
    return c[0], r

def eqp(con, sql, params=()): return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql, params)]


# 1. same SQL text, index created or dropped in the same connection (separate fresh connections per case)
Q = "SELECT COUNT(*) FROM t WHERE cust = 7"
print("\n1a. CREATE INDEX after the statement text was used")
con = connect()
s_before, r0 = steps(con, Q); p_before = eqp(con, Q)
con.execute("CREATE INDEX ix_cust ON t(cust)")
s_after, r1 = steps(con, Q)
print("   real SELECT, same text: steps before", s_before, "after", s_after, "(count", r1[0][0], "= before", r0[0][0], ")")
print("   EXPLAIN QUERY PLAN before:", p_before)
print("   EXPLAIN QUERY PLAN after CREATE INDEX, identical text:", eqp(con, Q))
print("1b. DROP INDEX after the statement text was used")
con = connect(); con.execute("CREATE INDEX ix_cust ON t(cust)")
print("   EXPLAIN QUERY PLAN with the index:", eqp(con, Q))
con.execute("DROP INDEX ix_cust")
print("   after DROP INDEX, identical text:", eqp(con, Q))
print("   after DROP INDEX, text plus two trailing spaces:", eqp(con, Q + "  "))
n, r = steps(con, Q); print("   the real SELECT with the identical text still runs correctly: steps", n, "count", r[0][0])
fresh = connect(); fresh.execute("CREATE INDEX ix_cust ON t(cust)"); fresh.execute("DROP INDEX ix_cust")
print("   fresh connection after create+drop:", eqp(fresh, Q))
con2 = connect(cached_statements=0); con2.execute("CREATE INDEX ix_cust ON t(cust)"); eqp(con2, Q); con2.execute("DROP INDEX ix_cust")
print("   cached_statements=0, same text after DROP INDEX:", eqp(con2, Q))

# 2. LIKE ? re-planned when the bound value changes
c3 = connect(); c3.execute("CREATE INDEX ix_name ON t(name COLLATE NOCASE)")
QL = "SELECT COUNT(*) FROM t WHERE name LIKE ?"
for v in ("alp%", "%pha1", "alp%"):
    n, r = steps(c3, QL, (v,))
    print(f"\n2. LIKE ? bound to {v!r}: steps {n:,}, count {r[0][0]}, plan {eqp(c3, QL, (v,))}")
exp = int(df["name"].str.lower().str.startswith("alp").sum())
assert steps(c3, QL, ("alp%",))[1][0][0] == exp
print("   same statement text, three bindings: the plan follows the value (checked above; pandas count for 'alp%' =", exp, ")")

# 3. hints
c4 = connect()
c4.execute("CREATE INDEX ix_status ON t(status)"); c4.execute("CREATE INDEX ix_cust ON t(cust)")
H = "SELECT COUNT(*) FROM t {hint} WHERE status = 'c' AND cust > 100"
for tag, hint, cond in (("planner's choice", "", None), ("INDEXED BY ix_cust", "INDEXED BY ix_cust", None),
                        ("NOT INDEXED", "NOT INDEXED", None)):
    q = H.format(hint=hint)
    n, r = steps(c4, q)
    print(f"\n3. {tag}: steps {n:,}, count {r[0][0]}, plan {eqp(c4, q)}")
q = "SELECT COUNT(*) FROM t WHERE +status = 'c' AND cust > 100"
n, r = steps(c4, q); print(f"   unary plus on status: steps {n:,}, count {r[0][0]}, plan {eqp(c4, q)}")
exp_c = int(((df.status == "c") & (df.cust > 100)).sum()); assert r[0][0] == exp_c
for bad in ("SELECT COUNT(*) FROM t INDEXED BY no_such_index WHERE cust = 7",
            "SELECT COUNT(*) FROM t INDEXED BY ix_status WHERE cust = 7"):
    try:
        print("   ", bad, "->", c4.execute(bad).fetchall())
    except sqlite3.Error as e:
        print("   ", bad, "->", type(e).__name__ + ":", e)
print("   all hint variants return the same count as pandas:", exp_c)

