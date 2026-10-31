rng = random.Random(51)
cities = ["Pune", "Delhi", "Mumbai", "Chennai", "Kolkata", "Jaipur", "Indore", "Surat", "Patna", "Noida"]
cust = [(i, "c%d" % i, rng.choice(cities)) for i in range(1, 20001)]
orders = [(i, rng.randint(1, 20000), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
           rng.choice(["placed", "shipped", "delivered"]), round(rng.uniform(5, 500), 2)) for i in range(1, 200001)]
items = [(i, rng.randint(1, 200000), rng.randint(1, 500), rng.randint(1, 5)) for i in range(1, 600001)]
path = WORK + "/j.db"
c = sqlite3.connect(path)
c.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INT, product_id INT, qty INT);""")
c.executemany("INSERT INTO customers VALUES(?,?,?)", cust)
c.executemany("INSERT INTO orders VALUES(?,?,?,?,?)", orders)
c.executemany("INSERT INTO order_items VALUES(?,?,?,?)", items)
c.commit(); c.close()
C = pd.DataFrame(cust, columns=["customer_id", "name", "city"])
O = pd.DataFrame(orders, columns=["order_id", "customer_id", "order_date", "status", "amount"])
I = pd.DataFrame(items, columns=["item_id", "order_id", "product_id", "qty"])

Q = """SELECT COUNT(*), SUM(i.qty) FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items i ON i.order_id = o.order_id
WHERE c.city = 'Pune'"""
QX = Q.replace("FROM customers c\nJOIN orders o", "FROM customers c CROSS JOIN orders o")
QX_BAD = """SELECT COUNT(*), SUM(i.qty) FROM order_items i CROSS JOIN orders o CROSS JOIN customers c
WHERE o.order_id = i.order_id AND c.customer_id = o.customer_id AND c.city = 'Pune'"""
m = C[C.city == "Pune"].merge(O, on="customer_id").merge(I, on="order_id")
expected = (len(m), int(m.qty.sum()))

def run(label, sql, auto=True):
    cc = sqlite3.connect(path)
    if not auto: cc.execute("PRAGMA automatic_index = OFF")
    pl = [r[3] for r in cc.execute("EXPLAIN QUERY PLAN " + sql)]
    n = [0]
    def tick():
        n[0] += 1; return 0
    cc.set_progress_handler(tick, 1); res = cc.execute(sql).fetchone(); cc.set_progress_handler(None, 0); cc.close()
    print(f"{label}\n   plan : {' | '.join(pl)}\n   steps: {n[0]:,}   result: {res}")
    assert tuple(res) == expected
print("pandas result (rows, sum qty):", expected)
run("1. primary keys only", Q)
run("2. same, PRAGMA automatic_index = OFF", Q, auto=False)
c = sqlite3.connect(path)
c.execute("CREATE INDEX ix_o_cust ON orders(customer_id)"); c.execute("CREATE INDEX ix_i_ord ON order_items(order_id)"); c.commit(); c.close()
run("3. indexes on orders(customer_id), order_items(order_id), NO statistics yet", Q)
run("3b. same indexes, CROSS JOIN customers -> orders pins customers as the outer loop", QX)
c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
run("4. after ANALYZE", Q)
run("5. after ANALYZE, CROSS JOIN customers -> orders (same plan as 4)", QX)
c = sqlite3.connect(path); c.execute("DROP INDEX ix_o_cust"); c.execute("DROP INDEX ix_i_ord"); c.execute("DELETE FROM sqlite_stat1"); c.commit(); c.close()
run("6. indexes dropped again, stats cleared", Q)
run("7. CROSS JOIN order forced to items -> orders -> customers, no FK indexes", QX_BAD)

print("--- automatic index and BLOOM FILTER: other orders of the same customer (self join, no index on customer_id) ---")
S = """SELECT COUNT(*) FROM orders a JOIN orders b ON b.customer_id = a.customer_id AND b.order_id <> a.order_id WHERE a.order_id <= 100"""
def runs(label, auto):
    cc = sqlite3.connect(path)
    if not auto: cc.execute("PRAGMA automatic_index = OFF")
    pl = [r[3] for r in cc.execute("EXPLAIN QUERY PLAN " + S)]
    n = [0]
    def tick():
        n[0] += 1; return 0
    cc.set_progress_handler(tick, 1); res = cc.execute(S).fetchone()[0]; cc.set_progress_handler(None, 0); cc.close()
    print(f"{label}\n   plan : {' | '.join(pl)}\n   steps: {n[0]:,}   result: {res}")
    return res
a = O[O.order_id <= 100][["order_id", "customer_id"]].merge(O[["order_id", "customer_id"]], on="customer_id", suffixes=("_a", "_b"))
want = int((a.order_id_a != a.order_id_b).sum())
r1 = runs("automatic_index ON", True)
r2 = runs("automatic_index OFF", False)
assert r1 == r2 == want
print("pandas self-merge count:", want)
