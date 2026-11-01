# Q8: semi-join: customers with at least one order.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30);   -- 104 = guest, NULL customer
""")
sql_exists = """SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id"""
sql_in = """SELECT customer_id, name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders) ORDER BY customer_id"""
sql_join_distinct = """SELECT DISTINCT c.customer_id, c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id ORDER BY c.customer_id"""
sql_plain_join = """SELECT c.customer_id, c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id ORDER BY c.customer_id"""
run = lambda q: con.execute(q).fetchall()
print("EXISTS           :", run(sql_exists))
print("IN (NULL present):", run(sql_in))
print("JOIN + DISTINCT  :", run(sql_join_distinct))
print("plain JOIN       :", run(sql_plain_join), "<- Asha twice")

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
p_isin = customers[customers["customer_id"].isin(orders["customer_id"])]
keys = orders[["customer_id"]].drop_duplicates()
p_merge = customers.merge(keys, on="customer_id", how="inner")
print("pandas isin:", p_isin["name"].tolist(), "| merge on dedup keys:", p_merge["name"].tolist())
p_plain = customers.merge(orders, on="customer_id")
print("pandas merge on raw orders rows:", len(p_plain), "(one per order, like the plain JOIN)")

as_t = lambda df: list(df[["customer_id", "name"]].itertuples(index=False, name=None))
assert as_t(p_isin) == as_t(p_merge.sort_values("customer_id")) == run(sql_exists) == run(sql_in) == run(sql_join_distinct)
assert len(run(sql_plain_join)) == 3 == len(p_plain)
print("asserts passed (compared in customer_id order)")
