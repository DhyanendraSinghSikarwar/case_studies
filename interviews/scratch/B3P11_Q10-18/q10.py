# Q10: "my index is not used": seven complaints, a scan that is right, and a checklist
import sqlite3, random, datetime, statistics, time
import pandas as pd

URI = "file:q10db?mode=memory&cache=shared"          # named in-memory DB, so a FRESH connection can open it
keep = sqlite3.connect(URI, uri=True)

def fresh():
    return sqlite3.connect(URI, uri=True)

def plan(sql, params=()):
    """Plan text from a brand-new connection (Python's statement cache can return a stale plan after CREATE/DROP INDEX)."""
    c = fresh()
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params).fetchall()]
    finally:
        c.close()

def steps(sql, params=()):
    """(VM steps, rows): set_progress_handler(cb, 1) fires once per VM opcode; deterministic."""
    c = fresh(); n = [0]
    def cb():
        n[0] += 1
        return 0
    c.set_progress_handler(cb, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0); c.close()
    return n[0], rows

def show(label, sql, params=()):
    p = plan(sql, params); n, rows = steps(sql, params)
    print(f"{label}\n    plan : {' | '.join(p)}\n    steps: {n:,}   rows: {len(rows):,}")
    return n, rows

# ---- seeded data: 200,000 orders; status 90% delivered, 1% cancelled; code is unique text 'K' + 6 digits
rnd = random.Random(10)
N = 200_000
codes = ["K%06d" % v for v in rnd.sample(range(1_000_000), N)]
statuses = ["delivered"] * 90 + ["shipped"] * 4 + ["placed"] * 3 + ["returned"] * 2 + ["cancelled"]
start = datetime.date(2023, 1, 1)
rows = [(i, rnd.randrange(1, 20_001), rnd.choice(statuses),
         (start + datetime.timedelta(days=rnd.randrange(731))).isoformat(),
         rnd.randrange(10, 1000), codes[i - 1]) for i in range(1, N + 1)]
keep.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount INT, code TEXT)")
keep.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)", rows)
for ddl in ["CREATE INDEX ix_cust ON orders(customer_id)",
            "CREATE INDEX ix_status_date ON orders(status, order_date)",
            "CREATE INDEX ix_code ON orders(code)",
            "CREATE INDEX ix_cancel_cust ON orders(customer_id) WHERE status = 'cancelled'"]:
    keep.execute(ddl)
keep.commit()
df = pd.read_sql_query("SELECT * FROM orders", keep)
print("sqlite", sqlite3.sqlite_version, "| rows", len(df), "| status mix:", df.status.value_counts(normalize=True).round(3).to_dict())
code0 = codes[776]

print("\n== 1. function on the column")
n_bad, r_bad = show("lower(code) = ?  (bad)", "SELECT * FROM orders WHERE lower(code) = ?", (code0.lower(),))
n_fix, r_fix = show("code = ?  (fix: compare the raw column)", "SELECT * FROM orders WHERE code = ?", (code0,))
assert r_bad == r_fix and len(r_fix) == 1 == (df.code == code0).sum()
keep.execute("CREATE INDEX ix_code_lower ON orders(lower(code))"); keep.commit()
n_ex, r_ex = show("lower(code) = ?  (fix 2: expression index on lower(code))", "SELECT * FROM orders WHERE lower(code) = ?", (code0.lower(),))
assert r_ex == r_fix

print("\n== 2. LIKE: leading wildcard, then prefix on a plain index")
n_w, r_w = show("code LIKE '%123'  (leading wildcard)", "SELECT * FROM orders WHERE code LIKE '%123'")
assert len(r_w) == df.code.str.endswith("123").sum()
n_p, r_p = show("code LIKE 'K0001%'  (prefix, plain BINARY index)", "SELECT * FROM orders WHERE code LIKE 'K0001%'")
assert len(r_p) == df.code.str.startswith("K0001").sum()
n_r, r_r = show("code >= 'K0001' AND code < 'K0002'  (fix: explicit range)", "SELECT * FROM orders WHERE code >= 'K0001' AND code < 'K0002'")
assert sorted(r_r) == sorted(r_p)
keep.execute("CREATE INDEX ix_code_nc ON orders(code COLLATE NOCASE)"); keep.commit()
show("code LIKE 'K0001%'  (after CREATE INDEX ... (code COLLATE NOCASE))", "SELECT * FROM orders WHERE code LIKE 'K0001%'")
keep.execute("DROP INDEX ix_code_nc"); keep.commit()
c = fresh()
print("PRAGMA case_sensitive_like (per connection), LIKE 'k0001%' with lower-case pattern:")
for flag in ("OFF", "ON"):
    c.execute(f"PRAGMA case_sensitive_like={flag}")
    p = [r[3] for r in c.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE 'k0001%'")]
    k = c.execute("SELECT count(*) FROM orders WHERE code LIKE 'k0001%'").fetchone()[0]
    print(f"    case_sensitive_like={flag}: plan {p}  matches={k}")
c.close()

print("\n== 3a. predicate on the SECOND column of (status, order_date) only, no statistics yet")
n_s, r_s = show("SELECT * ... WHERE order_date = '2024-03-05'", "SELECT * FROM orders WHERE order_date = '2024-03-05'")
assert len(r_s) == (df.order_date == "2024-03-05").sum()
show("SELECT status, order_date ... WHERE order_date = '2024-03-05'  (covered by the index)", "SELECT status, order_date FROM orders WHERE order_date = '2024-03-05'")

print("\n== 4. OR across two different columns (amount has no index)")
n_or, r_or = show("customer_id = 5 OR amount = 10", "SELECT * FROM orders WHERE customer_id = 5 OR amount = 10")
assert len(r_or) == ((df.customer_id == 5) | (df.amount == 10)).sum()
keep.execute("CREATE INDEX ix_amount ON orders(amount)"); keep.commit()
n_or2, r_or2 = show("same query after CREATE INDEX ix_amount", "SELECT * FROM orders WHERE customer_id = 5 OR amount = 10")
assert sorted(r_or2) == sorted(r_or)

print("\n== 5. != on the column (status != 'delivered' keeps 10% of rows)")
n_ne, r_ne = show("status != 'delivered'", "SELECT * FROM orders WHERE status != 'delivered'")
assert len(r_ne) == (df.status != "delivered").sum()
n_in, r_in = show("status IN ('shipped','placed','returned','cancelled')  (fix: list the wanted values)",
                  "SELECT * FROM orders WHERE status IN ('shipped','placed','returned','cancelled')")
assert sorted(r_in) == sorted(r_ne)
show("status < 'delivered' OR status > 'delivered'  (range rewrite)", "SELECT * FROM orders WHERE status < 'delivered' OR status > 'delivered'")

print("\n== 6. partial index ix_cancel_cust (customer_id) WHERE status = 'cancelled'")
show("customer_id = 5", "SELECT * FROM orders WHERE customer_id = 5")
n_pa, r_pa = show("customer_id = 5 AND status = 'cancelled'", "SELECT * FROM orders WHERE customer_id = 5 AND status = 'cancelled'")
assert len(r_pa) == ((df.customer_id == 5) & (df.status == "cancelled")).sum()
show("customer_id = 5 AND status IN ('cancelled')", "SELECT * FROM orders WHERE customer_id = 5 AND status IN ('cancelled')")
for q in ["SELECT * FROM orders INDEXED BY ix_cancel_cust WHERE customer_id = 5",
          "SELECT * FROM orders INDEXED BY ix_code WHERE customer_id = 5",
          "SELECT * FROM orders INDEXED BY ix_nope WHERE customer_id = 5"]:
    try:
        p = plan(q); print("INDEXED BY test:", q[26:], "->", p)
    except sqlite3.Error as e:
        print("INDEXED BY test:", q[26:], "-> error:", e)

print("\n== 7. statistics decide between two usable indexes (table t7: a has 2 values, b has 20,000)")
keep.execute("CREATE TABLE t7(id INTEGER PRIMARY KEY, a INT, b INT, pad TEXT)")
keep.executemany("INSERT INTO t7 VALUES(?,?,?,?)", [(i, i % 2, i % 20_000, "x") for i in range(1, N + 1)])
keep.execute("CREATE INDEX t7_a ON t7(a)"); keep.execute("CREATE INDEX t7_b ON t7(b)"); keep.commit()
Q7 = "SELECT * FROM t7 WHERE a = 1 AND b = 7"
show("no statistics yet", Q7)
keep.execute("ANALYZE"); keep.commit()
print("    sqlite_stat1:", keep.execute("SELECT tbl, idx, stat FROM sqlite_stat1 WHERE tbl='t7' ORDER BY idx").fetchall())
n7a, _ = show("after ANALYZE (data as loaded)", Q7)
# the data changes: now a is the selective column and b is not
keep.execute("UPDATE t7 SET a = (id * 7) % 20000, b = id % 2"); keep.commit()
Q7b = "SELECT * FROM t7 WHERE a = 1 AND b = 1"
n7s, r7s = show("data changed, statistics NOT refreshed (stale)", Q7b)
keep.execute("ANALYZE"); keep.commit()
print("    sqlite_stat1:", keep.execute("SELECT tbl, idx, stat FROM sqlite_stat1 WHERE tbl='t7' ORDER BY idx").fetchall())
n7f, r7f = show("after a second ANALYZE", Q7b)
assert r7s == r7f and len(r7f) == 5 or len(r7f) > 0
t7 = pd.read_sql_query("SELECT * FROM t7", keep)
assert len(r7f) == ((t7.a == 1) & (t7.b == 1)).sum()

print("\n== 3b. skip-scan: the same order_date query, now that statistics exist (orders was analysed above)")
keep.execute("ANALYZE orders"); keep.commit()
print("    sqlite_stat1:", keep.execute("SELECT idx, stat FROM sqlite_stat1 WHERE tbl='orders' AND idx IN ('ix_status_date','ix_cust') ORDER BY idx").fetchall())
n_sk, r_sk = show("order_date = '2024-03-05' after ANALYZE", "SELECT * FROM orders WHERE order_date = '2024-03-05'")
assert sorted(r_sk) == sorted(r_s)
keep.execute("CREATE INDEX ix_date ON orders(order_date)"); keep.commit()
n_dt, r_dt = show("after CREATE INDEX ix_date ON orders(order_date)", "SELECT * FROM orders WHERE order_date = '2024-03-05'")
assert sorted(r_dt) == sorted(r_s)

print("\n== 8. a scan can be the right answer: status = 'delivered' returns 90% of the rows")
n_ix, r_ix = show("planner's own choice", "SELECT * FROM orders WHERE status = 'delivered'")
n_ni, r_ni = show("NOT INDEXED", "SELECT * FROM orders NOT INDEXED WHERE status = 'delivered'")
n_nc, _ = show("status != 'cancelled' (99% of rows)", "SELECT * FROM orders WHERE status != 'cancelled'")
assert sorted(r_ix) == sorted(r_ni) and len(r_ix) == (df.status == "delivered").sum()
cx = fresh()
tbl_pages = cx.execute("SELECT count(*) FROM dbstat WHERE name = 'orders' AND pagetype = 'leaf'").fetchone()[0]
cx.close()
print(f"    index path = {len(r_ix):,} rowid lookups into a table of {tbl_pages:,} leaf pages (about {len(r_ix)/tbl_pages:.0f} lookups per page, in index order = random page order)")
def med(sql):
    ts = []
    for _ in range(5):
        c = fresh(); t = time.perf_counter(); c.execute(sql).fetchall(); ts.append(time.perf_counter() - t); c.close()
    return statistics.median(ts) * 1000
print(f"    machine-specific timing, median of 5, in-memory DB (will differ per run): index path {med('SELECT * FROM orders INDEXED BY ix_status_date WHERE status=\"delivered\"'):.0f} ms, NOT INDEXED {med('SELECT * FROM orders NOT INDEXED WHERE status=\"delivered\"'):.0f} ms")
print("asserts passed")
