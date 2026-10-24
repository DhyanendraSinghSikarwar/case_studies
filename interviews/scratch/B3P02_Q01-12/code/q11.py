# Q11: predicting join row counts; 100 customers, 450 orders, 20 customers without orders.
import sqlite3
from collections import Counter
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE customers(customer_id INTEGER, name TEXT); CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);")
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, f"c{i}") for i in range(1, 101)])
# customers 81..100 (20 of them) never order; orders 1..450 are spread over customers 1..80
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i - 1) % 80 + 1, 10) for i in range(1, 451)])
n = lambda q: con.execute(q).fetchone()[0]
J = "customers c {} orders o ON o.customer_id = c.customer_id"
counts = {k: n(f"SELECT COUNT(*) FROM " + J.format(k)) for k in ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"]}
counts["CROSS"] = n("SELECT COUNT(*) FROM customers CROSS JOIN orders")
print("SQL counts:", counts)
assert counts == {"INNER JOIN": 450, "LEFT JOIN": 470, "RIGHT JOIN": 450, "FULL JOIN": 470, "CROSS": 45000}

print("grain customers: COUNT(*) =", n("SELECT COUNT(*) FROM customers"), " COUNT(DISTINCT customer_id) =", n("SELECT COUNT(DISTINCT customer_id) FROM customers"))
print("grain orders   : COUNT(*) =", n("SELECT COUNT(*) FROM orders"), " COUNT(DISTINCT order_id) =", n("SELECT COUNT(DISTINCT order_id) FROM orders"))

# duplicate customer_id: customers 1..5 (they have orders) and customer 90 (no orders) loaded twice
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, f"c{i}") for i in (1, 2, 3, 4, 5, 90)])
inner_dup = n("SELECT COUNT(*) FROM " + J.format("INNER JOIN"))
left_dup = n("SELECT COUNT(*) FROM " + J.format("LEFT JOIN"))
print("after duplicating customers 1-5 and 90: INNER", inner_dup, "| LEFT", left_dup)

# formula: sum over keys of (left rows with key) x (right rows with key); LEFT adds unmatched left rows
cl = Counter(r[0] for r in con.execute("SELECT customer_id FROM customers"))
cr = Counter(r[0] for r in con.execute("SELECT customer_id FROM orders"))
pred_inner = sum(cl[k] * cr[k] for k in cl)
pred_left = pred_inner + sum(cl[k] for k in cl if k not in cr)
print("formula predicts INNER", pred_inner, "LEFT", pred_left)
assert pred_inner == inner_dup and pred_left == left_dup

# pandas: the same counts and the checks
cust = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
print("pandas: customer_id.is_unique:", cust["customer_id"].is_unique, "| rows", len(cust), "nunique", cust["customer_id"].nunique())
assert len(cust.merge(orders, on="customer_id")) == inner_dup
assert len(cust.merge(orders, on="customer_id", how="left")) == left_dup
cust1 = cust.drop_duplicates("customer_id")
res = {h: len(cust1.merge(orders, on="customer_id", how=h)) for h in ["inner", "left", "right", "outer"]}
res["cross"] = len(cust1.merge(orders, how="cross"))
print("pandas on deduplicated customers:", res)
assert res == {"inner": 450, "left": 470, "right": 450, "outer": 470, "cross": 45000}
assert len(cust1.merge(orders, on="customer_id", validate="one_to_many")) == 450
print("asserts passed")
