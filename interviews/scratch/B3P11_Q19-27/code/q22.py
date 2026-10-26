# Q22: partial, expression and unique indexes
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
def plan(con, sql, params=()):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0], params)]

# tiny sample
t = sqlite3.connect(":memory:")
t.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT, email TEXT);
INSERT INTO orders VALUES (1,'placed','2024-06-01','Asha@Mail.com'),(2,'delivered','2024-06-02','ben@mail.com'),(3,'placed','2024-06-03',NULL),(4,'delivered','2024-06-04',NULL);
CREATE UNIQUE INDEX ux_email ON orders(email);
""")
print("tiny: two NULL emails coexist under UNIQUE:", t.execute("SELECT COUNT(*) FROM orders WHERE email IS NULL").fetchone()[0])
try:
    t.execute("INSERT INTO orders VALUES (5,'placed','2024-06-05','ben@mail.com')")
except sqlite3.IntegrityError as e:
    print("tiny: duplicate non-NULL email ->", type(e).__name__, e)
t.execute("INSERT INTO orders VALUES (6,'placed','2024-06-06','BEN@mail.com')")
print("tiny: 'BEN@mail.com' is accepted next to 'ben@mail.com' (UNIQUE is case-sensitive, BINARY)")

# scaled data: 200,000 rows
rnd = random.Random(22)
rows = []
for i in range(1, 200001):
    st = "placed" if rnd.random() < 0.03 else rnd.choice(["delivered", "delivered", "shipped", "cancelled"])
    local = "user%d" % i
    email = None if rnd.random() < 0.05 else (local.upper() if rnd.random() < 0.3 else local.capitalize()) + "@Example.COM"
    rows.append((i, rnd.randint(1, 20000), st, "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500), email))
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER, email TEXT)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", rows)
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
print("\nplaced rows: %d of %d (%.2f%%)" % ((df.status == "placed").sum(), len(df), 100 * (df.status == "placed").mean()))

con.execute("CREATE INDEX ix_placed ON orders(order_date) WHERE status = 'placed'")
con.execute("CREATE INDEX ix_lower_email ON orders(lower(email))")
con.execute("CREATE UNIQUE INDEX ux_email ON orders(email)")
con.commit()

Q = [
 ("status = 'placed' AND order_date > ...", "SELECT order_id FROM orders WHERE status = 'placed' AND order_date > '2024-11-01'", ()),
 ("status IN ('placed') AND ...", "SELECT order_id FROM orders WHERE status IN ('placed') AND order_date > '2024-11-01'", ()),
 ("status != 'delivered' AND ...", "SELECT order_id FROM orders WHERE status != 'delivered' AND order_date > '2024-11-01'", ()),
 ("status = ? (bound) AND ...", "SELECT order_id FROM orders WHERE status = ? AND order_date > '2024-11-01'", ("placed",)),
 ("order_date > ... only", "SELECT order_id FROM orders WHERE order_date > '2024-11-01'", ()),
]
print("\nPARTIAL INDEX ix_placed(order_date) WHERE status = 'placed'")
for nm, sql, p in Q:
    r, n = steps(con, sql, p)
    print(" %-40s rows %5d steps %8d  %s" % (nm, len(r), n, plan(con, sql, p)))
exp = df[(df.status == "placed") & (df.order_date > "2024-11-01")]
assert sorted(x[0] for x in steps(con, Q[0][1])[0]) == sorted(exp.order_id)
assert sorted(x[0] for x in steps(con, Q[3][1], ("placed",))[0]) == sorted(exp.order_id)

target = df.email.dropna().iloc[1234]
E = [
 ("lower(email) = ?", "SELECT order_id FROM orders WHERE lower(email) = ?", (target.lower(),)),
 ("lower(email) = lower(?)", "SELECT order_id FROM orders WHERE lower(email) = lower(?)", (target,)),
 ("upper(email) = ?", "SELECT order_id FROM orders WHERE upper(email) = ?", (target.upper(),)),
 ("lower(trim(email)) = ?", "SELECT order_id FROM orders WHERE lower(trim(email)) = ?", (target.lower(),)),
 ("email = ? (exact)", "SELECT order_id FROM orders WHERE email = ?", (target,)),
 ("email = ? COLLATE NOCASE", "SELECT order_id FROM orders WHERE email = ? COLLATE NOCASE", (target.lower(),)),
 ("email LIKE ? (case-insensitive)", "SELECT order_id FROM orders WHERE email LIKE ?", (target.lower(),)),
]
print("\nEXPRESSION AND UNIQUE INDEXES, target email", target)
for nm, sql, p in E:
    r, n = steps(con, sql, p)
    print(" %-32s rows %d steps %8d  %s" % (nm, len(r), n, plan(con, sql, p)))
want = df[df.email.str.lower() == target.lower()]["order_id"].tolist()
assert [x[0] for x in con.execute(E[0][1], E[0][2])] == want
print("lower(email) lookup rows match pandas str.lower() filter:", want)

nulls = int(df.email.isna().sum())
print("\nNULL emails in the UNIQUE-indexed column: %d (all allowed)" % nulls)
assert con.execute("SELECT COUNT(*) FROM orders WHERE email IS NULL").fetchone()[0] == nulls
try:
    con.execute("INSERT INTO orders(customer_id,status,order_date,amount,email) VALUES (1,'placed','2024-01-01',1,?)", (target,))
except sqlite3.IntegrityError as e:
    print("duplicate insert ->", e)

# sizes
con.execute("CREATE INDEX ix_full ON orders(order_date)")
con.commit()
print("\nINDEX SIZES (dbstat bytes and pages, page_size %d)" % con.execute("PRAGMA page_size").fetchone()[0])
for nm in ("ix_placed", "ix_full", "ix_lower_email", "ux_email"):
    b, p = con.execute("SELECT SUM(pgsize), COUNT(*) FROM dbstat WHERE name = ?", (nm,)).fetchone()
    print("  %-15s %9d bytes %5d pages" % (nm, b, p))
b, p = con.execute("SELECT SUM(pgsize), COUNT(*) FROM dbstat WHERE name = 'orders'").fetchone()
print("  %-15s %9d bytes %5d pages (the table itself)" % ("orders", b, p))

# write cost: insert 'delivered' rows with only the partial index vs only the full index
import time
def insert_cost(index_sql):
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT)")
    c.execute(index_sql)
    batch = [(i, "delivered", "2024-%02d-%02d" % (1 + i % 12, 1 + i % 28)) for i in range(1, 100001)]
    n = [0]
    def cb():
        n[0] += 1
        return 0
    t0 = time.perf_counter()
    c.set_progress_handler(cb, 1)
    c.executemany("INSERT INTO orders VALUES (?,?,?)", batch)
    c.set_progress_handler(None, 0)
    c.commit()
    ms = (time.perf_counter() - t0) * 1000
    pages = c.execute("SELECT COUNT(*) FROM dbstat WHERE name = 'i'").fetchone()[0]
    return n[0], ms, pages
for label, ddl in (("partial index", "CREATE INDEX i ON orders(order_date) WHERE status = 'placed'"),
                   ("full index", "CREATE INDEX i ON orders(order_date)"),
                   ("no index", "CREATE TABLE IF NOT EXISTS unused(x)")):
    n, ms, pages = insert_cost(ddl)
    print("insert 100,000 'delivered' rows, %-13s: progress callbacks %d, index pages %d, wall %.0f ms (machine-specific, single run)" % (label, n, pages, ms))
