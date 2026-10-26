# Q25: CTE materialisation and subquery flattening
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

# tiny sample
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'2024-01-01',10),(2,5,'2024-01-02',30),(3,6,'2024-01-03',5),(4,7,'2024-01-04',100);""")
TWICE = "WITH t AS %s (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE s > (SELECT AVG(s) FROM t) ORDER BY customer_id"
print("tiny: per-customer totals", t.execute("SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id").fetchall(),
      "average of totals", t.execute("SELECT AVG(s) FROM (SELECT SUM(amount) s FROM orders GROUP BY customer_id)").fetchone()[0])
print("tiny: customers above the average total:", t.execute(TWICE % "").fetchall())

rnd = random.Random(25)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?)",
    [(i, rnd.randint(1, 20000), "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500)) for i in range(1, 200001)])
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
tot = df.groupby("customer_id")["amount"].sum()
exp_twice = tot[tot > tot.mean()].reset_index().rename(columns={"amount": "s"}).sort_values("customer_id").reset_index(drop=True)
exp5 = int(df.loc[df.customer_id == 5, "amount"].sum())

print("\n== CTE referenced twice (customers whose total exceeds the average total)")
for nm, hint in (("default", ""), ("AS MATERIALIZED", "MATERIALIZED"), ("AS NOT MATERIALIZED", "NOT MATERIALIZED")):
    sql = TWICE % hint
    rows, n = steps(con, sql)
    pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["customer_id", "s"]), exp_twice)
    print("%-20s rows %5d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)

print("\n== filter applied OUTSIDE a GROUP BY subquery versus the inlined query (customer_id = 5)")
OUT = "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE customer_id = 5"
INL = "SELECT customer_id, SUM(amount) AS s FROM orders WHERE customer_id = 5 GROUP BY customer_id"
CTE1 = "WITH t AS (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE customer_id = 5"
CTE1M = CTE1.replace("AS (SELECT", "AS MATERIALIZED (SELECT")
NOFILT = "SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id"
for nm, sql in (("subquery, filter outside", OUT), ("inlined filter", INL), ("CTE used once, filter outside", CTE1),
                ("CTE used once, AS MATERIALIZED", CTE1M), ("whole aggregate, no filter (for scale)", NOFILT)):
    rows, n = steps(con, sql)
    if "no filter" not in nm:
        assert rows == [(5, exp5)], (nm, rows)
    print("%-38s rows %5d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)

print("\n== what blocks push-down (outer filter customer_id = 5)")
BLOCK = [
 ("LIMIT inside", "SELECT customer_id, amount FROM (SELECT customer_id, amount FROM orders LIMIT 1000000) WHERE customer_id = 5"),
 ("no LIMIT (flattened)", "SELECT customer_id, amount FROM (SELECT customer_id, amount FROM orders) WHERE customer_id = 5"),
 ("DISTINCT inside, filter on a distinct column", "SELECT customer_id, amount FROM (SELECT DISTINCT customer_id, amount FROM orders) WHERE customer_id = 5"),
 ("window inside, filter on PARTITION BY column", "SELECT customer_id, rn FROM (SELECT customer_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id) rn FROM orders) WHERE customer_id = 5"),
 ("window inside, filter on the rank", "SELECT customer_id, rn FROM (SELECT customer_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id) rn FROM orders) WHERE rn = 1 AND customer_id = 5"),
 ("aggregate inside, filter on the aggregate", "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) s FROM orders GROUP BY customer_id) WHERE s > 2000"),
]
for nm, sql in BLOCK:
    rows, n = steps(con, sql)
    want = int((tot > 2000).sum()) if "s > 2000" in sql else (1 if "rn = 1" in sql else int((df.customer_id == 5).sum()))
    assert len(rows) == want, (nm, len(rows), want)
    print("%-46s rows %6d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)
print("asserts passed: every CTE or subquery form matched the pandas result (compared sorted by customer_id)")
