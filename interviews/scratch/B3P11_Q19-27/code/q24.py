# Q24: the N+1 query pattern
import sqlite3, random, time
import pandas as pd

random.seed(24)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
""")
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, "cust%03d" % i) for i in range(1, 101)])
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, random.randint(1, 100), random.randint(10, 500)) for i in range(1, 1001)])
con.commit()

class Counter:
    def __init__(self, c):
        self.stmts = []
        c.set_trace_callback(self.stmts.append)
    def reset(self):
        self.stmts.clear()
ctr = Counter(con)

# 1. N+1: one query for the list, then one per customer
ctr.reset()
t0 = time.perf_counter()
customers = con.execute("SELECT customer_id, name FROM customers ORDER BY customer_id").fetchall()
n_plus_1 = []
for cid, name in customers:
    tot, cnt = con.execute("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?", (cid,)).fetchone()
    n_plus_1.append((cid, name, cnt, tot))
t1 = (time.perf_counter() - t0) * 1000
print("N+1 loop: %d statements; first three traced:" % len(ctr.stmts))
for s in ctr.stmts[:3]: print("   ", s)
assert len(ctr.stmts) == 101

# 2. one JOIN + GROUP BY
ctr.reset()
t0 = time.perf_counter()
joined = con.execute("""SELECT c.customer_id, c.name, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id""").fetchall()
t2 = (time.perf_counter() - t0) * 1000
print("JOIN + GROUP BY: %d statement" % len(ctr.stmts))
assert len(ctr.stmts) == 1

# 3. one batched IN (?, ?, ...) query, then group in Python
ctr.reset()
t0 = time.perf_counter()
ids = [c[0] for c in con.execute("SELECT customer_id FROM customers ORDER BY customer_id")]
ph = ",".join("?" * len(ids))
fetched = con.execute("SELECT customer_id, amount FROM orders WHERE customer_id IN (%s)" % ph, ids).fetchall()
agg = {}
for cid, amt in fetched:
    c, s = agg.get(cid, (0, 0)); agg[cid] = (c + 1, s + amt)
names = dict(customers)
batched = [(cid, names[cid], *agg.get(cid, (0, 0))) for cid in ids]
t3 = (time.perf_counter() - t0) * 1000
print("batched IN: %d statements (1 for ids + 1 for orders)" % len(ctr.stmts))
assert len(ctr.stmts) == 2
assert n_plus_1 == joined == batched
print("asserts passed: N+1, JOIN and batched IN give the same 100 rows (customer_id, name, order_count, total)")
print("in-process times (machine-specific, MISLEADING for a network database): N+1 %.2f ms, JOIN %.2f ms, IN %.2f ms" % (t1, t2, t3))
print("simulated latency of 0.5 ms per round trip (arithmetic, not a measurement): N+1 adds %.1f ms, JOIN adds %.1f ms, IN adds %.1f ms" % (101 * 0.5, 1 * 0.5, 2 * 0.5))

print("\nplan of the per-customer lookup, no index:", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM orders WHERE customer_id = ?", (5,))])
con.execute("CREATE INDEX ix_orders_cust ON orders(customer_id)")
print("plan with index on orders(customer_id):  ", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM orders WHERE customer_id = ? ", (5,))])

n = [0]
def cb():
    n[0] += 1
    return 0
def vm(sql, p=()):
    n[0] = 0; con.set_progress_handler(cb, 1); con.execute(sql, p).fetchall(); con.set_progress_handler(None, 0); return n[0]
loop_steps = sum(vm("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?", (cid,)) for cid in ids)
print("VM steps with the index: 100 lookups total %d; the single JOIN/GROUP BY query %d" % (loop_steps, vm("""SELECT c.customer_id, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id GROUP BY c.customer_id""")))

opts = [o[0] for o in con.execute("PRAGMA compile_options") if "MAX_VARIABLE" in o[0]]
print("\nbound-variable limit compile option:", opts)
big = list(range(1, 300001))
try:
    con.execute("SELECT COUNT(*) FROM orders WHERE customer_id IN (%s)" % ",".join("?" * len(big)), big)
except sqlite3.Error as ex:
    print("IN list with 300,000 placeholders ->", type(ex).__name__, ex)
chunks = [ids[i:i + 30] for i in range(0, len(ids), 30)]
tot = sum(con.execute("SELECT COUNT(*) FROM orders WHERE customer_id IN (%s)" % ",".join("?" * len(ch)), ch).fetchone()[0] for ch in chunks)
print("chunked IN (4 chunks of up to 30 ids): %d orders counted, table has %d" % (tot, con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]))

# pandas: read_sql per row versus one read_sql + merge
ctr.reset()
rows = []
cust_df = pd.read_sql("SELECT * FROM customers ORDER BY customer_id", con)
for cid in cust_df["customer_id"]:
    one = pd.read_sql("SELECT COALESCE(SUM(amount),0) AS total, COUNT(*) AS cnt FROM orders WHERE customer_id = ?", con, params=(int(cid),))
    rows.append((int(cid), int(one.at[0, "cnt"]), int(one.at[0, "total"])))
loop_df = pd.DataFrame(rows, columns=["customer_id", "cnt", "total"])
print("\npandas per-row read_sql loop: %d statements" % len(ctr.stmts))
ctr.reset()
ord_df = pd.read_sql("SELECT customer_id, amount FROM orders", con)
agg = ord_df.groupby("customer_id")["amount"].agg(cnt="size", total="sum").reset_index()
merged = cust_df.merge(agg, on="customer_id", how="left").fillna({"cnt": 0, "total": 0}).astype({"cnt": "int64", "total": "int64"})
print("pandas one read_sql + groupby + merge: %d statements" % len(ctr.stmts))
pd.testing.assert_frame_equal(loop_df, merged[["customer_id", "cnt", "total"]])
print("asserts passed: both pandas versions equal (sorted by customer_id)")
