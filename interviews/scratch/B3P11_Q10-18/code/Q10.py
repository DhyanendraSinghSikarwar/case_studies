# Q10
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

# ---------- data: 200,000 orders, status skewed (90% delivered) ----------
rng = random.Random(11)
statuses = ["delivered"] * 90 + ["placed"] * 6 + ["cancelled"] * 3 + ["returned"] * 1
rows = [(i, rng.randint(1, 20000), rng.choice(statuses),
         "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         round(rng.uniform(5, 500), 2), str(rng.randint(1, 5000))) for i in range(1, 200001)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL, code TEXT)"

def build(name, index_sql):
    path = WORK + "/" + name
    c = sqlite3.connect(path)
    c.execute(DDL)
    c.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)", rows)
    for s in index_sql:
        c.execute(s)
    c.commit(); c.close()
    return path

IDX = ["CREATE INDEX ix_cust ON orders(customer_id)",
       "CREATE INDEX ix_st_dt ON orders(status, order_date)",
       "CREATE INDEX ix_code ON orders(code)",
       "CREATE INDEX ix_part ON orders(customer_id) WHERE status = 'cancelled'"]
db = build("main.db", IDX)
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount", "code"])

def show(label, path, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"{label}\n   plan : {' | '.join(plan(path, sql, params))}\n   steps: {st:,}   rows: {len(res):,}")
    return sorted(r[0] for r in res)          # order_ids, compared after sorting

print("=== 1. function on the column ===")
a = show("bad : customer_id + 0 = 5", db, "SELECT * FROM orders WHERE customer_id + 0 = 5")
b = show("good: customer_id = 5", db, "SELECT * FROM orders WHERE customer_id = 5")
assert a == b == sorted(df.order_id[df.customer_id == 5])
a = show("bad : substr(code, 1, 2) = '12'", db, "SELECT * FROM orders WHERE substr(code, 1, 2) = '12'")
b = show("good: code >= '12' AND code < '13'", db, "SELECT * FROM orders WHERE code >= '12' AND code < '13'")
assert a == b == sorted(df.order_id[df.code.str.startswith("12")])

print("=== 2. leading wildcard ===")
a = show("bad : code LIKE '%7'", db, "SELECT * FROM orders WHERE code LIKE '%7'")
assert a == sorted(df.order_id[df.code.str.endswith("7")])
a = show("prefix LIKE '12%' on a BINARY index", db, "SELECT * FROM orders WHERE code LIKE '12%'")
c = sqlite3.connect(db); c.execute("CREATE INDEX ix_code_nc ON orders(code COLLATE NOCASE)"); c.commit(); c.close()
b = show("prefix LIKE '12%' after a NOCASE index", db, "SELECT * FROM orders WHERE code LIKE '12%'")
assert a == b
c = sqlite3.connect(db); c.execute("DROP INDEX ix_code_nc"); c.commit(); c.close()
c = sqlite3.connect(db); c.execute("PRAGMA case_sensitive_like = ON")
print("   with PRAGMA case_sensitive_like=ON, BINARY index only:",
      " | ".join(r[3] for r in c.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE '12%'")))
c.close()

print("=== 3. second column of the composite index only ===")
a = show("bad : order_date = '2024-03-05'  (before ANALYZE)", db, "SELECT * FROM orders WHERE order_date = '2024-03-05'")
c = sqlite3.connect(db); c.execute("ANALYZE"); c.commit(); c.close()
b = show("same query after ANALYZE (skip-scan possible)", db, "SELECT * FROM orders WHERE order_date = '2024-03-05'")
c = sqlite3.connect(db); c.execute("CREATE INDEX ix_dt ON orders(order_date)"); c.commit(); c.close()
e = show("good: index on order_date", db, "SELECT * FROM orders WHERE order_date = '2024-03-05'")
assert a == b == e == sorted(df.order_id[df.order_date == "2024-03-05"])

print("=== 4. OR across two columns ===")
a = show("bad : customer_id = 5 OR amount > 490 (amount unindexed)", db, "SELECT * FROM orders WHERE customer_id = 5 OR amount > 490")
c = sqlite3.connect(db); c.execute("CREATE INDEX ix_amt ON orders(amount)"); c.commit(); c.close()
b = show("good: index on amount too", db, "SELECT * FROM orders WHERE customer_id = 5 OR amount > 490")
u = show("UNION rewrite", db, "SELECT * FROM orders WHERE customer_id = 5 UNION SELECT * FROM orders WHERE amount > 490")
assert a == b == u == sorted(df.order_id[(df.customer_id == 5) | (df.amount > 490)])

print("=== 5. != on a column where 97% of rows match ===")
a = show("status != 'cancelled'", db, "SELECT * FROM orders WHERE status != 'cancelled'")
b = show("INDEXED BY ix_st_dt (forced)", db, "SELECT * FROM orders INDEXED BY ix_st_dt WHERE status != 'cancelled'")
assert a == b == sorted(df.order_id[df.status != "cancelled"])
a = show("status != 'delivered' (10% match, still a scan)", db, "SELECT * FROM orders WHERE status != 'delivered'")
b = show("status IN ('placed','cancelled','returned')", db, "SELECT * FROM orders WHERE status IN ('placed', 'cancelled', 'returned')")
assert a == b

print("=== 6. partial index, WHERE not repeated (only the partial index on customer_id exists) ===")
dbp = build("partial.db", ["CREATE INDEX ix_part ON orders(customer_id) WHERE status = 'cancelled'"])
a = show("customer_id = 5", dbp, "SELECT * FROM orders WHERE customer_id = 5")
b = show("customer_id = 5 AND status = 'cancelled'", dbp, "SELECT * FROM orders WHERE customer_id = 5 AND status = 'cancelled'")
c_ = show("customer_id = 5 AND status IN ('cancelled')", dbp, "SELECT * FROM orders WHERE customer_id = 5 AND status IN ('cancelled')")
assert b == sorted(df.order_id[(df.customer_id == 5) & (df.status == "cancelled")])

print("=== 7. stale statistics (small table analysed while b was constant, then grown) ===")
dbs = WORK + "/stale.db"
c = sqlite3.connect(dbs)
c.execute("CREATE TABLE w(id INTEGER PRIMARY KEY, a INT, b INT)")
c.execute("CREATE INDEX ix_a ON w(a)"); c.execute("CREATE INDEX ix_b ON w(b)")
c.executemany("INSERT INTO w(a, b) VALUES(?, ?)", [(i % 2, 7) for i in range(1000)])
c.execute("ANALYZE"); c.commit()
print("   stat1 when analysed:", c.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall())
r2 = random.Random(5)
w_rows = [(r2.randint(0, 1), r2.randint(1, 100000)) for _ in range(200000)]
c.executemany("INSERT INTO w(a, b) VALUES(?, ?)", w_rows); c.commit()
print("   stat1 after 200,000 more rows (not refreshed):", c.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall())
q = "SELECT * FROM w WHERE a = 1 AND b = 500"
q2 = "SELECT * FROM w WHERE b = 500"
sa = show("stale stats: a = 1 AND b = 500", dbs, q)
sb = show("stale stats: b = 500", dbs, q2)
c.execute("ANALYZE"); c.commit()
print("   stat1 after re-ANALYZE:", c.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall())
print("   same connection that ran ANALYZE, EXPLAIN b = 500:", " | ".join(r[3] for r in c.execute("EXPLAIN QUERY PLAN " + q2 + " ")))
c.close()
fa = show("fresh stats: a = 1 AND b = 500", dbs, q)
fb = show("fresh stats: b = 500", dbs, q2)
assert sa == fa and sb == fb

print("=== 8. a scan is the right choice (status = 'delivered', 90% of rows) ===")
dbm = db
a = show("planner choice", dbm, "SELECT * FROM orders WHERE status = 'delivered'")
b = show("NOT INDEXED (forced scan)", dbm, "SELECT * FROM orders NOT INDEXED WHERE status = 'delivered'")
d_ = show("INDEXED BY ix_st_dt (forced)", dbm, "SELECT * FROM orders INDEXED BY ix_st_dt WHERE status = 'delivered'")
assert a == b == d_ == sorted(df.order_id[df.status == "delivered"])
print("   pandas: a boolean mask is always a full scan; rows =", int((df.status == "delivered").sum()))
