# Q2: what an index buys (lookup VM steps) and costs (insert VM steps, time, pages).
import random
import sqlite3
import time
import statistics
import pandas as pd

random.seed(2)
statuses = ["placed", "shipped", "delivered", "cancelled"]
rows = [(i, random.randint(1, 20000),
         f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
         random.choice(statuses), round(random.uniform(10, 500), 2))
        for i in range(1, 100001)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL)"
INDEXES = ["CREATE INDEX i1 ON orders(customer_id)",
           "CREATE INDEX i2 ON orders(order_date)",
           "CREATE INDEX i3 ON orders(status, amount)"]

def count_steps(con, sql, args=()):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql, args).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

# 1. lookup: scan versus index
con = sqlite3.connect(":memory:")
con.execute(DDL)
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
q = "SELECT * FROM orders WHERE customer_id = 5"
s_scan, r_scan = count_steps(con, q)
con.execute(INDEXES[0])
s_idx, r_idx = count_steps(con, q)
s_cov, _ = count_steps(con, "SELECT customer_id, order_id FROM orders WHERE customer_id = 5")
print("rows matched:", len(r_scan), "| VM steps scan:", s_scan, "index:", s_idx, "covering:", s_cov)
assert sorted(r_scan) == sorted(r_idx)

# 2. write cost with 0..3 indexes
res = []
for k in range(4):
    c = sqlite3.connect(":memory:")
    c.execute(DDL)
    for ddl in INDEXES[:k]:
        c.execute(ddl)
    cnt = [0]
    def cb():
        cnt[0] += 1
        return 0
    times = []
    c.set_progress_handler(cb, 1)
    t = time.perf_counter()
    c.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
    c.commit()
    times.append(time.perf_counter() - t)
    c.set_progress_handler(None, 0)
    pages = c.execute("PRAGMA page_count").fetchone()[0]
    res.append((k, cnt[0], round(times[0] * 1000), pages))
out = pd.DataFrame(res, columns=["indexes", "vm_steps", "insert_ms_machine_specific", "page_count"])
print(out.to_string(index=False))

# 3. size of the table and each index (dbstat), page size 4096
con.execute("CREATE INDEX i2 ON orders(order_date)")
con.execute("CREATE INDEX i3 ON orders(status, amount)")
for name, nbytes, npages in con.execute(
        "SELECT name, SUM(pgsize), COUNT(*) FROM dbstat WHERE name IN ('orders','i1','i2','i3') GROUP BY name ORDER BY name"):
    print(f"{name:7s} {npages:5d} pages {nbytes:9d} bytes")
print("page_size", con.execute("PRAGMA page_size").fetchone()[0])

# pandas analogue: a boolean mask scans every row; a sorted index finds them by binary search
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "status", "amount"])
m = df[df.customer_id == 5].sort_values("order_id").reset_index(drop=True)
s = df.sort_values("customer_id", kind="stable")
lo, hi = s.customer_id.searchsorted(5, "left"), s.customer_id.searchsorted(5, "right")
via_sorted = s.iloc[lo:hi].sort_values("order_id").reset_index(drop=True)
pd.testing.assert_frame_equal(m, via_sorted)
pd.testing.assert_frame_equal(m, pd.DataFrame(sorted(r_idx), columns=m.columns), check_dtype=False)
print("asserts passed: SQL scan, SQL index, pandas mask and sorted searchsorted give the same rows (sorted by order_id)")
