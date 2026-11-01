# Q3: ON versus WHERE for a filter on the right table of a LEFT JOIN.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,'completed',100),(102,1,'completed',50),(103,1,'cancelled',40),
                          (104,2,'cancelled',75),(105,4,'completed',20);
""")

sql_on = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""
sql_where = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""
sql_inner_on = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""
sql_inner_where = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""

run = lambda q: con.execute(q).fetchall()
r_on, r_where = run(sql_on), run(sql_where)
print("LEFT, filter in ON   :", r_on)
print("LEFT, filter in WHERE:", r_where)
print("INNER, filter in ON   :", run(sql_inner_on))
print("INNER, filter in WHERE:", run(sql_inner_where))

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

# pandas: filter the RIGHT frame first, then merge (this is the ON version)
done = orders[orders["status"] == "completed"]
m = customers.merge(done, on="customer_id", how="left")
p_on = (m.groupby(["customer_id", "name"], as_index=False)["order_id"].count()
         .rename(columns={"order_id": "completed_orders"}).sort_values("customer_id"))
# the trap in pandas: merge first, filter after (this is the WHERE version)
m2 = customers.merge(orders, on="customer_id", how="left")
p_where = (m2[m2["status"] == "completed"].groupby(["customer_id", "name"], as_index=False)["order_id"].count()
           .rename(columns={"order_id": "completed_orders"}).sort_values("customer_id"))
print(p_on[["name", "completed_orders"]].to_string(index=False))
print("pandas filter-after-merge rows:", p_where["name"].tolist())

as_tuples = lambda df: list(df[["name", "completed_orders"]].itertuples(index=False, name=None))
assert as_tuples(p_on) == r_on == [("Asha", 2), ("Ben", 0), ("Chitra", 0), ("Dev", 1)]
assert as_tuples(p_where) == r_where == [("Asha", 2), ("Dev", 1)]
assert run(sql_inner_on) == run(sql_inner_where) == r_where
print("asserts passed (compared in customer_id order)")
