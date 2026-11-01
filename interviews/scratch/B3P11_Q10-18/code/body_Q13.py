rng = random.Random(41)
words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet"]
def note():
    s = " ".join(rng.choice(words) for _ in range(50))
    return s[:300]
N = 100000
rows = [(i, rng.randint(1, 10000), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         rng.choice(["placed", "shipped", "delivered"]), round(rng.uniform(5, 500), 2), note()) for i in range(1, N + 1)]
path = WORK + "/o.db"
c = sqlite3.connect(path)
c.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL, notes TEXT)")
c.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)", rows)
c.execute("CREATE INDEX ix_cust ON orders(customer_id)")
c.commit(); c.close()
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "status", "amount", "notes"])
print("average notes length:", round(df.notes.str.len().mean(), 1))

def sizes(label):
    c = sqlite3.connect(path)
    pc = c.execute("PRAGMA page_count").fetchone()[0]
    ds = c.execute("SELECT name, COUNT(*) pages, SUM(pgsize) FROM dbstat GROUP BY name ORDER BY name").fetchall()
    c.close()
    print(f"{label}: page_count={pc} ->", ", ".join(f"{n}: {p} pages ({b:,} bytes)" for n, p, b in ds))

def run(label, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"{label}\n   plan : {' | '.join(plan(path, sql, params))}\n   steps: {st:,}   rows: {len(res):,}")
    return res

SEL_STAR = "SELECT * FROM orders WHERE customer_id BETWEEN 1 AND 500"
SEL_COLS = "SELECT customer_id, order_date, amount, order_id FROM orders WHERE customer_id BETWEEN 1 AND 500"
sizes("with ix_cust only")
a1 = run("SELECT * with ix_cust(customer_id)", SEL_STAR)
b1 = run("3 columns with ix_cust(customer_id): still needs the table row for order_date and amount", SEL_COLS)
c = sqlite3.connect(path); c.execute("CREATE INDEX ix_cov ON orders(customer_id, order_date, amount)"); c.commit(); c.close()
sizes("after ix_cov")
a2 = run("SELECT * with both indexes", SEL_STAR)
b2 = run("3 columns with ix_cov(customer_id, order_date, amount)", SEL_COLS)
sub = df[df.customer_id.between(1, 500)]
assert sorted(b1) == sorted(b2) == sorted(zip(sub.customer_id, sub.order_date, sub.amount, sub.order_id))
assert len(a1) == len(a2) == len(sub)
one = run("one customer, 3 columns, covering", "SELECT order_date, amount FROM orders WHERE customer_id = 7")
run("one customer, SELECT *", "SELECT * FROM orders WHERE customer_id = 7")
c = sqlite3.connect(path); c.execute("DROP INDEX ix_cov"); c.commit(); c.close()
run("one customer, 3 columns, no covering index", "SELECT order_date, amount FROM orders WHERE customer_id = 7")

print("--- SELECT * is not stable when the schema changes ---")
c = sqlite3.connect(path)
cols_before = [d[0] for d in c.execute("SELECT * FROM orders LIMIT 1").description]
c.execute("ALTER TABLE orders ADD COLUMN coupon TEXT"); c.commit()
cols_after = [d[0] for d in c.execute("SELECT * FROM orders LIMIT 1").description]
print("columns before:", cols_before); print("columns after :", cols_after)
c.close()

print("--- pandas: only read the columns you need ---")
csv = WORK + "/orders.csv"
df.to_csv(csv, index=False)
full = pd.read_csv(csv)
slim = pd.read_csv(csv, usecols=["customer_id", "order_date", "amount"])
print("memory_usage(deep=True) bytes: all columns", int(full.memory_usage(deep=True).sum()), "| usecols", int(slim.memory_usage(deep=True).sum()))
print("notes column alone:", int(full.notes.memory_usage(deep=True)))
assert slim.equals(full[["customer_id", "order_date", "amount"]])
