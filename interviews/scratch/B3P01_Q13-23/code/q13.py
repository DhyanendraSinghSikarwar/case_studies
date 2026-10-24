# NOT IN with a NULL in the subquery: SQL result, the fixes, and what pandas isin does with NaN.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);  -- NULL = guest checkout
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,NULL);
""")

sql_not_in = "SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders) ORDER BY customer_id"
sql_not_in_filtered = ("SELECT name FROM customers WHERE customer_id NOT IN "
                       "(SELECT customer_id FROM orders WHERE customer_id IS NOT NULL) ORDER BY customer_id")
sql_not_exists = ("SELECT c.name FROM customers c WHERE NOT EXISTS "
                  "(SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id")

def run(q): return [r[0] for r in con.execute(q).fetchall()]
print("NOT IN (subquery has a NULL):", run(sql_not_in))
print("NOT IN with IS NOT NULL filter:", run(sql_not_in_filtered))
print("NOT EXISTS:", run(sql_not_exists))
print("3 NOT IN (1, 2, NULL) ->", con.execute("SELECT 3 NOT IN (1,2,NULL)").fetchone()[0])
print("1 NOT IN (1, 2, NULL) ->", con.execute("SELECT 1 NOT IN (1,2,NULL)").fetchone()[0])
print("3 NOT IN (1, 2)       ->", con.execute("SELECT 3 NOT IN (1,2)").fetchone()[0])

# pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
print("orders.customer_id dtype:", orders["customer_id"].dtype, "(NULL became NaN, ints became float)")
p_not_in = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
print("pandas ~isin:", p_not_in)

# isin and NaN: NaN matches NaN, so a NaN key on the left WOULD be treated as 'found'
left = pd.Series([1.0, 3.0, np.nan])
print("isin with NaN in values:", left.isin([1.0, np.nan]).tolist())

# the pandas result matches the NOT EXISTS result (compare as lists, ordered by customer_id)
assert p_not_in == run(sql_not_exists) == run(sql_not_in_filtered) == ["Chitra", "Dev"]
assert run(sql_not_in) == []

# NOT IN with NULL filtered out explicitly in pandas gives the same thing
ids = orders["customer_id"].dropna()
assert customers.loc[~customers["customer_id"].isin(ids), "name"].tolist() == p_not_in
print("asserts passed")
