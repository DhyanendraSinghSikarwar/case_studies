# Q16
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

import time
rng = random.Random(61)
N = 300000
stat = ["delivered"] * 80 + ["shipped"] * 15 + ["placed"] * 3 + ["cancelled"] * 2
rows = [(i, rng.randint(1, 30000), rng.choice(stat), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         round(rng.uniform(5, 500), 2)) for i in range(1, N + 1)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL)"
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount"])
print("share of 'placed':", round((df.status == "placed").mean() * 100, 2), "%")

def build(name, idx=()):
    path = WORK + "/" + name
    c = sqlite3.connect(path); c.execute(DDL)
    c.executemany("INSERT INTO orders VALUES(?,?,?,?,?)", rows)
    for s in idx: c.execute(s)
    c.commit(); c.close(); return path

QA = ("SELECT order_id, order_date FROM orders WHERE customer_id = ? ORDER BY order_date DESC, order_id DESC LIMIT 20", (77,))
QB = ("SELECT order_id FROM orders WHERE status = 'placed' AND order_date < ?", ("2024-02-01",))
QC = ("SELECT status, COUNT(*), ROUND(SUM(amount), 2) FROM orders WHERE order_date >= ? AND order_date < ? GROUP BY status ORDER BY status", ("2024-03-05", "2024-03-06"))
def report(label, path):
    out = {}
    for nm, (sql, p) in (("Qa", QA), ("Qb", QB), ("Qc", QC)):
        st, res = steps(path, sql, p)
        out[nm] = res
        print(f"  {nm}: steps {st:>9,} rows {len(res):>5} | {' | '.join(plan(path, sql, p))}")
    return out

print("--- 0. no secondary indexes ---")
r0 = report("none", build("none.db"))
IA = "CREATE INDEX ix_a ON orders(customer_id, order_date)"
IB = "CREATE INDEX ix_b ON orders(status, order_date)"
IC = "CREATE INDEX ix_c ON orders(order_date, status, amount)"
IP = "CREATE INDEX ix_p ON orders(order_date) WHERE status = 'placed'"
IA0 = "CREATE INDEX ix_cust ON orders(customer_id)"
print("--- 1. proposed set: ix_a(customer_id, order_date), ix_b(status, order_date), ix_c(order_date, status, amount) ---")
p3 = build("three.db", [IA, IB, IC])
r3 = report("three", p3)
print("--- 2. drop ix_b, keep ix_a and ix_c: how bad is Qb? ---")
p2 = build("ac.db", [IA, IC]); r2 = report("ac", p2)
print("--- 3. replace ix_b by the partial index ix_p(order_date) WHERE status = 'placed' ---")
pp = build("apc.db", [IA, IC, IP]); r3p = report("apc", pp)
print("--- 4. a redundant prefix: ix_cust(customer_id) next to ix_a ---")
pr = build("red.db", [IA0, IA])
print("  Qa with both:", " | ".join(plan(pr, *QA)))

# oracle: pandas answers
a = df[df.customer_id == 77].sort_values(["order_date", "order_id"], ascending=False).head(20)
b = df[(df.status == "placed") & (df.order_date < "2024-02-01")]
c = df[(df.order_date >= "2024-03-05") & (df.order_date < "2024-03-06")].groupby("status").agg(n=("amount", "size"), s=("amount", "sum")).reset_index().sort_values("status")
for r in (r0, r3, r2, r3p):
    assert r["Qa"] == list(zip(a.order_id, a.order_date))
    assert sorted(x[0] for x in r["Qb"]) == sorted(b.order_id)
    assert [(s, n) for s, n, _ in r["Qc"]] == list(zip(c.status, c.n))
    assert all(abs(t - round(s, 2)) < 0.011 for (_, _, t), s in zip(r["Qc"], c.s))

print("--- index sizes (dbstat) ---")
for nm, path in (("three.db", p3), ("apc.db", pp)):
    cc = sqlite3.connect(path)
    print(nm, [(n, pg) for n, pg in cc.execute("SELECT name, COUNT(*) FROM dbstat WHERE name LIKE 'ix_%' GROUP BY name ORDER BY name")])
    cc.close()

print("--- write cost: insert 100,000 more rows with k secondary indexes ---")
extra = [(N + i, rng.randint(1, 30000), rng.choice(stat), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
          round(rng.uniform(5, 500), 2)) for i in range(1, 100001)]
for label, idx in (("0 indexes", []), ("ix_a", [IA]), ("ix_a, ix_b", [IA, IB]), ("ix_a, ix_b, ix_c", [IA, IB, IC]), ("ix_a, ix_c, partial ix_p", [IA, IC, IP])):
    path = WORK + "/w_%d.db" % len(label)
    cc = sqlite3.connect(path); cc.execute(DDL)
    for s in idx: cc.execute(s)
    cc.commit()
    n = [0]
    def tick():
        n[0] += 1; return 0
    cc.set_progress_handler(tick, 1)
    t0 = time.perf_counter()
    cc.executemany("INSERT INTO orders VALUES(?,?,?,?,?)", extra)
    cc.commit()
    ms = (time.perf_counter() - t0) * 1000
    cc.set_progress_handler(None, 0); cc.close()
    print(f"  {label:<26} VM steps {n[0]:>10,}   time {ms:7.0f} ms (machine-specific)")
