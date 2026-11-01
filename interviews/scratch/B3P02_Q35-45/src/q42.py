# Q42: JOIN vs EXISTS vs IN: duplicates, the NOT IN NULL trap, and a case where all forms agree
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);      -- several rows per customer, one NULL
CREATE TABLE orders_clean(order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL UNIQUE);  -- one row per customer, no NULL
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,1),(104,2),(105,NULL);
INSERT INTO orders_clean VALUES (201,1),(202,2);
"""
def queries(t):
    return {
        "JOIN":        f"SELECT c.name FROM customers c JOIN {t} o ON o.customer_id = c.customer_id ORDER BY c.customer_id",
        "EXISTS":      f"SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id",
        "IN":          f"SELECT c.name FROM customers c WHERE c.customer_id IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id",
        "NOT EXISTS":  f"SELECT c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id",
        "NOT IN":      f"SELECT c.name FROM customers c WHERE c.customer_id NOT IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id",
        "LEFT JOIN IS NULL": f"SELECT c.name FROM customers c LEFT JOIN {t} o ON o.customer_id = c.customer_id WHERE o.order_id IS NULL ORDER BY c.customer_id",
    }
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for t in ("orders", "orders_clean"):
    print(f"--- table {t}")
    res[t] = {k: [r[0] for r in con.execute(q).fetchall()] for k, q in queries(t).items()}
    for k, v in res[t].items():
        print(f"{k:>18}: {v}")

# the three existence forms agree on the clean table, JOIN differs on the duplicated table, NOT IN fails on NULLs
c = res["orders_clean"]
assert c["JOIN"] == c["EXISTS"] == c["IN"] == ["Asha", "Ben"]
assert c["NOT EXISTS"] == c["NOT IN"] == c["LEFT JOIN IS NULL"] == ["Chitra", "Dev"]
d = res["orders"]
assert d["JOIN"] == ["Asha", "Asha", "Asha", "Ben"] and d["EXISTS"] == d["IN"] == ["Asha", "Ben"]
assert d["NOT IN"] == [] and d["NOT EXISTS"] == d["LEFT JOIN IS NULL"] == ["Chitra", "Dev"]

# pandas idioms
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
p_join = customers.merge(orders, on="customer_id").sort_values(["customer_id", "order_id"])["name"].tolist()
p_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_semi = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id").sort_values("customer_id")["name"].tolist()
p_not = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
          .query("_merge == 'left_only'").sort_values("customer_id")["name"].tolist())
print("\npandas merge (like JOIN):", p_join)
print("pandas isin (like EXISTS/IN):", p_in)
print("pandas merge on dropped-duplicate keys (semi-join):", p_semi)
print("pandas ~isin (like NOT EXISTS, NOT like NOT IN):", p_not)
print("pandas anti-join via indicator:", p_anti)
assert p_join == d["JOIN"] and p_in == p_semi == d["EXISTS"] and p_not == p_anti == d["NOT EXISTS"]
print("asserts passed: pandas matches the SQL form named in each label (lists in customer_id order)")
con.close()
