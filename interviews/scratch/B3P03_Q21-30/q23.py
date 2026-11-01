# Q23: subquery vs JOIN: IN vs JOIN (duplicates) and NOT IN vs LEFT JOIN ... IS NULL (the NULL trap)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,1,30),(4,2,40),(5,NULL,50);
"""
SQL_IN = """
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders)
ORDER BY name
"""
SQL_JOIN = """
SELECT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
"""
SQL_JOIN_DISTINCT = """
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
"""
SQL_NOT_IN = """
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY name
"""
SQL_NOT_IN_FIXED = """
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)
ORDER BY name
"""
SQL_ANTI_JOIN = """
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.name
"""
SQL_NOT_EXISTS = """
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def names(sql):
    return [r[0] for r in con.execute(sql)]
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)

r = {k: names(v) for k, v in [("IN", SQL_IN), ("JOIN", SQL_JOIN), ("JOIN DISTINCT", SQL_JOIN_DISTINCT),
                              ("NOT IN", SQL_NOT_IN), ("NOT IN (NULLs filtered)", SQL_NOT_IN_FIXED),
                              ("LEFT JOIN IS NULL", SQL_ANTI_JOIN), ("NOT EXISTS", SQL_NOT_EXISTS)]}
for k, v in r.items():
    print(f"{k:24s} {len(v)} rows  {v}")

# pd:main
pd_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
pd_join = customers.merge(orders, on="customer_id")["name"].sort_values().tolist()
pd_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
           .query("_merge == 'left_only'")["name"].sort_values().tolist())
pd_not_isin = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
# pd:end
print("\npandas isin          ", pd_in)
print("pandas merge (join)  ", pd_join)
print("pandas anti-join     ", pd_anti)
print("pandas ~isin         ", pd_not_isin)

assert r["IN"] == pd_in == ["Asha", "Ben"]
assert r["JOIN"] == pd_join == ["Asha", "Asha", "Asha", "Ben"]
assert r["JOIN DISTINCT"] == ["Asha", "Ben"]
assert r["NOT IN"] == []
assert r["NOT IN (NULLs filtered)"] == r["LEFT JOIN IS NULL"] == r["NOT EXISTS"] == pd_anti == pd_not_isin == ["Chitra", "Dev"]
print("\nasserts passed: IN == isin (2 rows), JOIN == merge (4 rows with duplicates), NOT IN returns 0 rows, anti-joins return Chitra and Dev")
