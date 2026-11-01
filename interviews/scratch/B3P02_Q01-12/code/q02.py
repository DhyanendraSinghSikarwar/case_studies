# Q2: anti-join three ways in SQL, plus pandas indicator and ~isin.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
-- 104 is a guest order (NULL customer); 105 belongs to Esha but its amount is NULL
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,5,NULL);
""")

sql_left = """SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL ORDER BY c.customer_id"""
sql_not_exists = """SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id"""
sql_not_in = """SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY customer_id"""
sql_not_in_safe = """SELECT name FROM customers WHERE customer_id NOT IN
(SELECT customer_id FROM orders WHERE customer_id IS NOT NULL) ORDER BY customer_id"""
sql_wrong_col = """SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount IS NULL ORDER BY c.customer_id"""   # tests a nullable data column: wrong

run = lambda q: [r[0] for r in con.execute(q).fetchall()]
print("LEFT JOIN ... o.order_id IS NULL:", run(sql_left))
print("NOT EXISTS                      :", run(sql_not_exists))
print("NOT IN (subquery has a NULL)    :", run(sql_not_in))
print("NOT IN with IS NOT NULL filter  :", run(sql_not_in_safe))
print("LEFT JOIN ... o.amount IS NULL  :", run(sql_wrong_col), "<- Esha is wrongly listed")

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

m = customers.merge(orders, on="customer_id", how="left", indicator=True)
p_ind = m.loc[m["_merge"] == "left_only", "name"].tolist()
p_isin = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
print("pandas merge indicator:", p_ind, "| pandas ~isin:", p_isin)
print(m[["name", "order_id", "_merge"]].to_string(index=False))

# all agree with the order-by-customer_id SQL results
assert run(sql_left) == run(sql_not_exists) == run(sql_not_in_safe) == p_ind == p_isin == ["Chitra", "Dev"]
assert run(sql_not_in) == []
assert run(sql_wrong_col) == ["Chitra", "Dev", "Esha"]
print("asserts passed")
