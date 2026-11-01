# Q12: fan-out inflates SUM(order_total); the fixes in SQL and pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,2,80),(5,3,40);
INSERT INTO order_items VALUES (1,1,7,1),(2,1,8,2),(3,2,7,1),(4,3,7,1),(5,3,8,1),(6,3,9,3),(7,4,7,1);
-- order 1 has 2 items, 2 has 1, 3 has 3, 4 has 1, 5 has none
""")
one = lambda q: con.execute(q).fetchone()[0]
sql_bug = "SELECT SUM(o.order_total) FROM orders o JOIN order_items i ON i.order_id = o.order_id"
sql_orders_only = "SELECT SUM(order_total) FROM orders"
sql_distinct = "SELECT SUM(DISTINCT o.order_total) FROM orders o JOIN order_items i ON i.order_id = o.order_id"
sql_fix = """SELECT SUM(o.order_total) FROM orders o
LEFT JOIN (SELECT order_id, SUM(qty) AS units FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id"""
sql_fix_units = """SELECT SUM(o.order_total) AS revenue, SUM(COALESCE(i.units, 0)) AS units FROM orders o
LEFT JOIN (SELECT order_id, SUM(qty) AS units FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id"""
print("true (orders only):", one(sql_orders_only))
print("buggy join SUM    :", one(sql_bug))
print("SUM(DISTINCT)     :", one(sql_distinct), "<- also wrong")
print("pre-aggregated    :", one(sql_fix), "| with units:", con.execute(sql_fix_units).fetchone())
print("rows after join   :", one("SELECT COUNT(*) FROM orders o JOIN order_items i ON i.order_id = o.order_id"), "from", one("SELECT COUNT(*) FROM orders"), "orders")
assert (one(sql_orders_only), one(sql_bug), one(sql_distinct), one(sql_fix)) == (350, 570, 230, 350)

orders = pd.read_sql("SELECT * FROM orders", con)
items = pd.read_sql("SELECT * FROM order_items", con)
bug = orders.merge(items, on="order_id")["order_total"].sum()
dist = orders.merge(items, on="order_id")["order_total"].drop_duplicates().sum()
per_order = items.groupby("order_id", as_index=False).agg(units=("qty", "sum"))
fixed = orders.merge(per_order, on="order_id", how="left", validate="one_to_one")
print("pandas bug:", bug, "| drop_duplicates on the VALUE:", dist, "| orders alone:", orders["order_total"].sum(),
      "| pre-aggregated:", fixed["order_total"].sum(), "| units:", int(fixed["units"].fillna(0).sum()))
assert (bug, dist) == (570, 230) and fixed["order_total"].sum() == orders["order_total"].sum() == 350
assert int(fixed["units"].fillna(0).sum()) == con.execute(sql_fix_units).fetchone()[1]
# the merge is legitimately one-to-many, so validate= does NOT flag this bug
orders.merge(items, on="order_id", validate="one_to_many")
print("validate='one_to_many' passes on the buggy merge: the bug is the aggregation, not the join")
print("asserts passed")
