# Q9: joins that miss rows because of trailing spaces, case and NBSP; diagnose and fix; pandas merge.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_name TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha Rao');
INSERT INTO orders VALUES
 (101,'Asha Rao ',250),                         -- trailing space
 (102,'asha rao',120),                          -- lower case
 (103,'Asha' || char(160) || 'Rao',90),         -- NBSP between the words
 (104,'Asha Rao',400),                          -- exact
 (105,'Asha Rao' || char(160),30);              -- NBSP at the end
""")

def rows(sql):
    return [r for r in con.execute(sql)]

sql_exact = "SELECT o.order_id FROM orders o JOIN customers c ON o.customer_name = c.name ORDER BY o.order_id"
sql_trim_lower = ("SELECT o.order_id FROM orders o JOIN customers c "
                  "ON LOWER(TRIM(o.customer_name)) = LOWER(TRIM(c.name)) ORDER BY o.order_id")
sql_fixed = """
SELECT o.order_id FROM orders o JOIN customers c
  ON LOWER(TRIM(REPLACE(o.customer_name, char(160), ' '))) = LOWER(TRIM(REPLACE(c.name, char(160), ' ')))
ORDER BY o.order_id
"""
sql_diag = """
SELECT order_id, customer_name, LENGTH(customer_name) AS len, OCTET_LENGTH(customer_name) AS bytes,
       HEX(customer_name) AS hex, UNICODE(SUBSTR(customer_name, -1)) AS last_cp,
       UNICODE(SUBSTR(customer_name, 5, 1)) AS fifth_cp
FROM orders ORDER BY order_id
"""
print(pd.read_sql(sql_diag, con).assign(customer_name=lambda d: d.customer_name.map(repr)).to_string(index=False)); print()

print("exact equality join      :", [r[0] for r in rows(sql_exact)])
print("TRIM + LOWER on both     :", [r[0] for r in rows(sql_trim_lower)], "(103 and 105 still missing)")
print("TRIM('Asha Rao' || NBSP) length:", con.execute("SELECT LENGTH(TRIM('Asha Rao' || char(160)))").fetchone()[0], "(unchanged, 9)")
print("TRIM with NBSP listed    :", con.execute("SELECT LENGTH(TRIM('Asha Rao' || char(160), ' ' || char(160)))").fetchone()[0], "(8)")
print("+ REPLACE char(160) first:", [r[0] for r in rows(sql_fixed)])

sql_total = """
SELECT SUM(o.amount) FROM orders o JOIN customers c
ON LOWER(TRIM(REPLACE(o.customer_name, char(160), ' '))) = LOWER(TRIM(REPLACE(c.name, char(160), ' ')))"""
print("revenue for Asha: exact join", con.execute(sql_exact.replace("o.order_id", "SUM(o.amount)").replace(" ORDER BY o.order_id", "")).fetchone()[0],
      "| after cleaning", con.execute(sql_total).fetchone()[0], "| all orders", con.execute("SELECT SUM(amount) FROM orders").fetchone()[0])

# the index point (details of plans are Part 11)
con.execute("CREATE INDEX ix_cust_name ON orders(customer_name)")
for label, where in (("customer_name = 'Asha Rao'", "customer_name = 'Asha Rao'"),
                     ("LOWER(TRIM(customer_name)) = ...", "LOWER(TRIM(customer_name)) = 'asha rao'")):
    plan = [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE " + where)]
    print(f"plan for {label:34s}", plan)

# pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

def key(s):
    return s.str.replace(r"\s+", " ", regex=True).str.strip().str.casefold()

strip_only = orders.assign(k=orders.customer_name.str.strip().str.casefold())
print("\nstr.strip().str.casefold() only, keys:", strip_only.k.map(repr).tolist())
print("str.strip removes the trailing NBSP of 105 but not the NBSP inside 103")
orders["k"] = key(orders.customer_name)
customers["k"] = key(customers.name)
merged = orders.merge(customers[["customer_id", "k"]], on="k", how="inner")
p_ids = sorted(merged.order_id.tolist())
sql_ids = [r[0] for r in rows(sql_fixed)]
assert p_ids == sql_ids == [101, 102, 103, 104, 105]
assert [r[0] for r in rows(sql_exact)] == [104]
assert strip_only.merge(customers[["customer_id", "k"]], on="k").order_id.tolist() != p_ids
print("pandas matched order ids:", p_ids, "| revenue:", merged.amount.sum())
print("asserts passed (order ids compared sorted)")
