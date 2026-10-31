# Q41: join performance at concept level: plans before/after an index, function on a join column, missing ON, filter-first
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, email TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE leads(lead_id INTEGER PRIMARY KEY, email TEXT);
""")
cities = ["Pune", "Delhi", "Chennai", "Kolkata"]
con.executemany("INSERT INTO customers VALUES (?,?,?)",
                [(i, f"User{i}@Example.com", cities[i % 4]) for i in range(1, 201)])
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i * 7) % 200 + 1, i % 50) for i in range(1, 2001)])
con.executemany("INSERT INTO leads VALUES (?,?)", [(i, f"user{i}@example.com") for i in range(1, 101)])

def plan(q):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q).fetchall()]

Q_FK = "SELECT COUNT(*) FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'"
print("1. join on the foreign key, no index on orders.customer_id:"); [print("   ", p) for p in plan(Q_FK)]
con.execute("CREATE INDEX ix_orders_customer ON orders(customer_id)")
print("   after CREATE INDEX ix_orders_customer:"); [print("   ", p) for p in plan(Q_FK)]

Q_FUNC = "SELECT COUNT(*) FROM leads l JOIN customers c ON LOWER(c.email) = LOWER(l.email)"
Q_PLAIN = "SELECT COUNT(*) FROM leads l JOIN customers c ON c.email = l.email"
print("\n2. LOWER() on both join columns (no index on email yet):"); [print("   ", p) for p in plan(Q_FUNC)]
con.execute("CREATE INDEX ix_cust_email_lower ON customers(LOWER(email))")
print("   after an index on the expression LOWER(email):"); [print("   ", p) for p in plan(Q_FUNC)]
print("   matches:", con.execute(Q_FUNC).fetchone()[0], "| plain equality matches (case differs):", con.execute(Q_PLAIN).fetchone()[0])

n_c, n_o = 200, 2000
print("\n3. missing ON (comma join without a condition):",
      con.execute("SELECT COUNT(*) FROM customers c, orders o").fetchone()[0], "rows =", n_c, "x", n_o)

# 4. filter before join gives the same answer as filter after
Q_AFTER = """SELECT c.city, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount >= 25 GROUP BY c.city ORDER BY c.city"""
Q_BEFORE = """SELECT c.city, SUM(o.amount) AS total FROM customers c
JOIN (SELECT customer_id, amount FROM orders WHERE amount >= 25) o ON o.customer_id = c.customer_id
GROUP BY c.city ORDER BY c.city"""
s_after = pd.read_sql_query(Q_AFTER, con)
s_before = pd.read_sql_query(Q_BEFORE, con)
pd.testing.assert_frame_equal(s_after, s_before)
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
p = (customers.merge(orders[orders["amount"] >= 25][["customer_id", "amount"]], on="customer_id")
     .groupby("city", as_index=False).agg(total=("amount", "sum")).sort_values("city").reset_index(drop=True))
pd.testing.assert_frame_equal(s_before, p, check_dtype=False)
print("\n4. filter-first SQL == filter-after SQL == pandas filter-then-merge (sorted by city):")
print(p.to_string(index=False))
big = customers.merge(orders, how="cross")
print("pandas cross merge rows:", len(big))
con.close()
