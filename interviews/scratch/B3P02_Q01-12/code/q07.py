# Q7: pandas merge arguments mapped to SQL, with differently named keys and a shared created_at column.
import sqlite3
import pandas as pd
from pandas.errors import MergeError

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, created_at TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, cust_id INTEGER, amount INTEGER, created_at TEXT);
INSERT INTO customers VALUES (1,'Asha','2024-01-01'),(2,'Ben','2024-02-01'),(3,'Chitra','2024-03-01');
INSERT INTO orders VALUES (101,1,50,'2024-05-01'),(102,1,20,'2024-05-02'),(103,2,30,'2024-05-03'),(104,9,10,'2024-05-04');
""")
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

# 1) default merge: how='inner', and a clash on created_at gives _x / _y
d = customers.merge(orders, left_on="customer_id", right_on="cust_id")
print("default how, auto suffixes:", list(d.columns), "| rows:", len(d))

# 2) the full version: how, left_on/right_on, suffixes, indicator, validate
p = customers.merge(orders, how="outer", left_on="customer_id", right_on="cust_id",
                    suffixes=("_cust", "_order"), indicator=True, validate="one_to_many")
print(p[["customer_id", "name", "order_id", "cust_id", "_merge"]].to_string(index=False))
print(p["_merge"].value_counts().to_dict())

sql = """SELECT c.customer_id, c.name, c.created_at AS created_at_cust, o.order_id, o.cust_id, o.amount,
       o.created_at AS created_at_order
FROM customers c FULL OUTER JOIN orders o ON c.customer_id = o.cust_id"""
s = con.execute(sql).fetchall()

cols = ["customer_id", "name", "created_at_cust", "order_id", "cust_id", "amount", "created_at_order"]
def rows(items):
    out = []
    for r in items:
        out.append(tuple(None if (x is None or (isinstance(x, float) and x != x))
                         else int(x) if isinstance(x, float) else x for x in r))
    return sorted(out, key=lambda t: tuple((v is None, str(v)) for v in t))
assert rows(p[cols].itertuples(index=False, name=None)) == rows(s)   # all rows sorted before comparing
print("SQL FULL OUTER JOIN == pandas outer merge (", len(s), "rows )")

# 3) what validate guards: a duplicated key on the 'one' side
dup = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)
try:
    dup.merge(orders, left_on="customer_id", right_on="cust_id", validate="one_to_many")
except MergeError as e:
    print("MergeError:", e)
print("without validate the duplicate silently gives", len(dup.merge(orders, left_on="customer_id", right_on="cust_id")), "rows (was", len(d), ")")
assert len(d) == 3
print("asserts passed")
