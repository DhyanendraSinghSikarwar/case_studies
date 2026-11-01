# Q2: what an index buys and costs: VM steps, page counts, dbstat sizes
import os, sqlite3, tempfile, time
import numpy as np
import pandas as pd

rng = np.random.default_rng(2)
N = 100_000
df = pd.DataFrame({
    "order_id": np.arange(1, N + 1),
    "customer_id": rng.integers(1, 20_001, N),
    "order_date": (pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 365, N), unit="D")).strftime("%Y-%m-%d").to_numpy(),
    "status": rng.choice(["placed", "shipped", "delivered", "cancelled"], N, p=[.2, .3, .4, .1]),
    "amount": rng.integers(100, 50_000, N) / 100,
})
rows = list(df.itertuples(index=False, name=None))
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL)"
INDEXES = ["CREATE INDEX ix_cust ON orders(customer_id)",
           "CREATE INDEX ix_date ON orders(order_date)",
           "CREATE INDEX ix_status ON orders(status)"]

def steps(con, sql, params=()):
    """Count SQLite VM opcodes: set_progress_handler(cb, 1) fires once per opcode."""
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    try:
        out = con.execute(sql, params).fetchall()
    finally:
        con.set_progress_handler(None, 1)
    return n[0], out

print("sqlite", sqlite3.sqlite_version)
d = tempfile.mkdtemp()
path = os.path.join(d, "q2.db")
con = sqlite3.connect(path)
con.execute(DDL)
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows); con.commit()
LOOK = "SELECT * FROM orders WHERE customer_id = 5"
s_scan, r_scan = steps(con, LOOK)
pages0 = con.execute("PRAGMA page_count").fetchone()[0]
con.execute(INDEXES[0]); con.commit()
con.close()
con = sqlite3.connect(path)           # fresh connection: no cached statements
s_idx, r_idx = steps(con, LOOK + " ")
assert sorted(r_scan) == sorted(r_idx)
pages1 = con.execute("PRAGMA page_count").fetchone()[0]
ps = con.execute("PRAGMA page_size").fetchone()[0]
db = dict(con.execute("SELECT name, SUM(pgsize) FROM dbstat GROUP BY name"))
print(f"lookup customer_id=5 -> {len(r_idx)} rows")
print(f"  VM steps as scan: {s_scan:,}   with ix_cust: {s_idx}")
print(f"  page_size {ps}; page_count before index {pages0}, after {pages1} (+{pages1 - pages0} pages)")
print(f"  dbstat bytes: table orders {db['orders']:,}  index ix_cust {db['ix_cust']:,}")
assert s_scan > 250_000 and s_idx < 500
con.close()

# pandas check of the lookup
pd_rows = df[df["customer_id"] == 5].sort_values("order_id")
assert [r[0] for r in sorted(r_idx)] == pd_rows["order_id"].tolist()

# insert cost with 0, 1, 2, 3 indexes (steps are deterministic; ms are machine-specific)
print("\ninserting 100,000 rows with k secondary indexes (executemany in one transaction)")
print("k  VM_steps    ms(machine-specific)")
res = []
for k in range(4):
    p = os.path.join(d, f"ins{k}.db")
    c = sqlite3.connect(p)
    c.execute(DDL)
    for stmt in INDEXES[:k]:
        c.execute(stmt)
    n = [0]
    def cb():
        n[0] += 1
        return 0
    c.set_progress_handler(cb, 1)
    t = time.perf_counter()
    c.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
    c.commit()
    ms = (time.perf_counter() - t) * 1000
    c.set_progress_handler(None, 1)
    cnt = c.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert cnt == N
    res.append(n[0])
    print(f"{k}  {n[0]:>9,}  {ms:7.0f}")
    c.close()
assert res == sorted(res) and len(set(res)) == 4
print("steps grow with every extra index:", [res[i + 1] - res[i] for i in range(3)])
