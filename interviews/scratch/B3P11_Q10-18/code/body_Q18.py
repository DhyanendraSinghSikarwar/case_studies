rng = random.Random(81)
N = 200000
pool = ["delivered"] * 980 + ["cancelled"] * 5 + ["placed"] * 10 + ["returned"] * 5
cities = ["Pune", "Delhi", "Mumbai", "Chennai", "Kolkata", "Jaipur", "Indore", "Surat", "Patna", "Noida"]
cust = [(i, "c%d" % i, rng.choice(cities)) for i in range(1, 20001)]
rows = [(i, rng.randint(1, 20000), rng.choice(pool), round(rng.uniform(5, 500), 2)) for i in range(1, N + 1)]
path = WORK + "/s.db"
c = sqlite3.connect(path)
c.executescript("""CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, amount REAL);""")
c.executemany("INSERT INTO customers VALUES(?,?,?)", cust); c.executemany("INSERT INTO orders VALUES(?,?,?,?)", rows)
c.execute("CREATE INDEX ix_status ON orders(status)"); c.execute("CREATE INDEX ix_cust ON orders(customer_id)")
c.execute("CREATE INDEX ix_city ON customers(city)")
c.commit(); c.close()
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "amount"])
CU = pd.DataFrame(cust, columns=["customer_id", "name", "city"])
true = df.status.value_counts()
print("true counts:", true.to_dict(), "| shares %:", (true / N * 100).round(2).to_dict())

def stat():
    cc = sqlite3.connect(path)
    r = dict(cc.execute("SELECT idx, stat FROM sqlite_stat1").fetchall()) if cc.execute("SELECT 1 FROM sqlite_master WHERE name='sqlite_stat1'").fetchone() else None
    cc.close(); return r
def line(label, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"  {label:<44} steps {st:>9,} rows {len(res):>8,} | {' | '.join(plan(path, sql, params))}")
    return res

c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
print("sqlite_stat1 (status):", stat()["ix_status"], "-> 'rows, average rows per distinct status', not per value")
print("--- one estimate for every value; real counts differ ---")
for v in ("cancelled", "delivered"):
    a = line(f"status = '{v}' (planner)", "SELECT * FROM orders WHERE status = ?", (v,))
    b = line(f"status = '{v}' NOT INDEXED", "SELECT * FROM orders NOT INDEXED WHERE status = ?", (v,))
    d = line(f"status = '{v}' unary +", "SELECT * FROM orders WHERE +status = ?", (v,))
    assert sorted(a) == sorted(b) == sorted(d) and len(a) == true[v]

print("--- INDEXED BY and NOT INDEXED as hints; when INDEXED BY errors ---")
for lab, sql in (("INDEXED BY ix_nosuch", "SELECT * FROM orders INDEXED BY ix_nosuch WHERE status = 'x'"),
                 ("INDEXED BY ix_cust, filter on status", "SELECT * FROM orders INDEXED BY ix_cust WHERE status = 'cancelled'"),
                 ("INDEXED BY ix_status, filter on customer", "SELECT * FROM orders INDEXED BY ix_status WHERE customer_id = 5")):
    cc = sqlite3.connect(path)
    try:
        n = len(cc.execute(sql).fetchall()); print(f"  {lab}: ok, {n} rows | plan {' | '.join(r[3] for r in cc.execute('EXPLAIN QUERY PLAN ' + sql))}")
    except sqlite3.Error as e:
        print(f"  {lab}: error: {e}")
    cc.close()
cc = sqlite3.connect(path); cc.execute("CREATE INDEX ix_part ON orders(amount) WHERE status = 'cancelled'"); cc.commit()
try:
    cc.execute("SELECT * FROM orders INDEXED BY ix_part WHERE amount > 100").fetchall()
except sqlite3.Error as e:
    print("  INDEXED BY a partial index the WHERE does not imply: error:", e)
cc.execute("DROP INDEX ix_part"); cc.commit(); cc.close()

print("--- a cardinality error shows up as a join order ---")
QJ = "SELECT COUNT(*) FROM orders o %s customers c ON c.customer_id = o.customer_id WHERE o.status = 'cancelled' AND c.city = 'Pune'"
QJ2 = "SELECT COUNT(*) FROM customers c CROSS JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'cancelled' AND c.city = 'Pune'"
want = len(df[df.status == "cancelled"].merge(CU[CU.city == "Pune"], on="customer_id"))
for lab, sql in (("planner's order", QJ % "JOIN"), ("forced: orders first", QJ % "CROSS JOIN"), ("forced: customers first", QJ2)):
    r = line(lab, sql); assert r[0][0] == want
print("pandas merge count:", want)

print("--- a bulk update changes the distribution; statistics are not refreshed ---")
c = sqlite3.connect(path)
c.execute("UPDATE orders SET status = 'cancelled' WHERE order_id % 2 = 0 AND status = 'delivered'"); c.commit(); c.close()
df.loc[(df.order_id % 2 == 0) & (df.status == "delivered"), "status"] = "cancelled"
true2 = df.status.value_counts()
print("true counts now:", true2.to_dict(), "| stat still:", stat()["ix_status"])
a = line("status = 'cancelled' (stale stats)", "SELECT * FROM orders WHERE status = 'cancelled'")
b = line("status = 'cancelled' NOT INDEXED", "SELECT * FROM orders NOT INDEXED WHERE status = 'cancelled'")
assert len(a) == len(b) == true2["cancelled"]
c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
print("after ANALYZE (still 4 distinct values, so the average is unchanged):", stat()["ix_status"])
c = sqlite3.connect(path)
c.execute("UPDATE orders SET status = 'S' || (order_id % 40) WHERE status = 'delivered'"); c.commit()
print("after splitting 'delivered' into 40 labels, stat1 not refreshed:", stat()["ix_status"])
c.execute("ANALYZE"); c.commit(); c.close()
print("after ANALYZE:", stat()["ix_status"], "| distinct statuses:", sqlite3.connect(path).execute("SELECT COUNT(DISTINCT status) FROM orders").fetchone()[0])

