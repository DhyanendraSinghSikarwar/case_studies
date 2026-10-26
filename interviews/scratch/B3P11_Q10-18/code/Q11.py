# Q11
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(21)
rows = [(i, rng.randint(1, 20000), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         round(rng.uniform(5, 500), 2)) for i in range(1, 200001)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, amount REAL)"
def build(name, idx):
    path = WORK + "/" + name
    c = sqlite3.connect(path); c.execute(DDL)
    c.executemany("INSERT INTO orders VALUES(?,?,?,?)", rows)
    for s in idx: c.execute(s)
    c.commit(); c.close(); return path
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "amount"])

def run(label, path, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"{label}\n   plan : {' | '.join(plan(path, sql, params))}\n   steps: {st:,}   rows: {len(res)}")
    return res

def add(path, sql):
    c = sqlite3.connect(path); c.execute(sql); c.commit(); c.close()

db = build("o.db", [])
print("--- A. ORDER BY amount LIMIT 10 ---")
q = "SELECT order_id, amount FROM orders ORDER BY amount, order_id LIMIT 10"
a = run("no index", db, q)
add(db, "CREATE INDEX ix_amt ON orders(amount)")
b = run("index on amount (rowid is the hidden last column, so the order_id tie-break is free)", db, q)
run("no LIMIT, index on amount", db, "SELECT order_id, amount FROM orders ORDER BY amount, order_id")
run("LIMIT 10 but ORDER BY amount DESC, order_id", db, "SELECT order_id, amount FROM orders ORDER BY amount DESC, order_id LIMIT 10")
p = df.sort_values(["amount", "order_id"]).head(10)
assert a == b == list(zip(p.order_id, p.amount))
nl = df.nsmallest(10, "amount")           # keep='first' on ties: ties are broken by row position (= order_id here)
assert list(nl.order_id) == list(p.order_id)

print("--- B. ORDER BY order_date DESC LIMIT 10 (index read backwards) ---")
q = "SELECT order_id, order_date FROM orders ORDER BY order_date DESC, order_id DESC LIMIT 10"
a = run("no index on order_date", db, q)
add(db, "CREATE INDEX ix_dt ON orders(order_date)")
b = run("index on order_date", db, q)
p = df.sort_values(["order_date", "order_id"], ascending=False).head(10)
assert a == b == list(zip(p.order_id, p.order_date))
run("ORDER BY order_date DESC, order_id ASC (mixed direction)", db, "SELECT order_id, order_date FROM orders ORDER BY order_date DESC, order_id ASC LIMIT 10")

print("--- C. WHERE customer_id = ? ORDER BY order_date ---")
q = "SELECT order_id, order_date FROM orders WHERE customer_id = 5 ORDER BY order_date, order_id"
add(db, "CREATE INDEX ix_cust ON orders(customer_id)")
a = run("index on customer_id only", db, q)
add(db, "CREATE INDEX ix_cust_dt ON orders(customer_id, order_date)")
b = run("plus index on (customer_id, order_date)", db, q)
p = df[df.customer_id == 5].sort_values(["order_date", "order_id"])
assert a == b == list(zip(p.order_id, p.order_date))

print("--- D. LIMIT without ORDER BY is arbitrary ---")
q = "SELECT order_id, amount FROM orders WHERE amount > 495 LIMIT 3"
db2 = build("o2.db", [])
x = run("no index on amount", db2, q)
add(db2, "CREATE INDEX ix_amt ON orders(amount)")
y = run("after CREATE INDEX on amount (same SQL text)", db2, q)
print("   first run :", x); print("   second run:", y)
assert x != y
