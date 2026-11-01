# Q24: UPDATE with a correlated scalar subquery (COALESCE), UPDATE ... FROM, WITH before UPDATE, pandas map
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, total_spent INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha',999),(2,'Ben',NULL),(3,'Chitra',NULL),(4,'Dev',77),(5,'Esha',NULL);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,200),(4,5,NULL);
"""
SQL_MAIN = """
UPDATE customers
SET total_spent = COALESCE((SELECT SUM(o.amount)
                            FROM orders o
                            WHERE o.customer_id = customers.customer_id), 0)
"""
SQL_NO_COALESCE = """
UPDATE customers
SET total_spent = (SELECT SUM(o.amount)
                   FROM orders o
                   WHERE o.customer_id = customers.customer_id)
"""
SQL_UPDATE_FROM = """
UPDATE customers
SET total_spent = t.s
FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) AS t
WHERE customers.customer_id = t.customer_id
"""
SQL_WITH_UPDATE = """
WITH t AS (SELECT customer_id, COALESCE(SUM(amount), 0) AS s FROM orders GROUP BY customer_id)
UPDATE customers
SET total_spent = COALESCE((SELECT s FROM t WHERE t.customer_id = customers.customer_id), 0)
"""
CHECK = "SELECT customer_id, name, total_spent FROM customers ORDER BY customer_id"

def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c
BASE = fresh().total_changes                   # rows inserted by the setup script
def run(sql):
    c = fresh()
    c.execute(sql)
    return c, c.total_changes - BASE     # rowcount is -1 for a statement that starts with WITH
def table(c):
    return pd.read_sql_query(CHECK, c)

con = fresh()
before = table(con)
print("BEFORE (stale values 999 and 77, NULLs elsewhere):")
print(before.to_string(index=False))
print("check query, orders per customer:", con.execute(
    "SELECT customer_id, SUM(amount), COUNT(*) FROM orders GROUP BY customer_id").fetchall())

c_main, n_main = run(SQL_MAIN)
c_nc, n_nc = run(SQL_NO_COALESCE)
c_from, n_from = run(SQL_UPDATE_FROM)
c_with, n_with = run(SQL_WITH_UPDATE)
sql_df = table(c_main)
print(f"\nAFTER SQL_MAIN (correlated subquery + COALESCE), rows updated: {n_main}")
print(sql_df.to_string(index=False))
print(f"\nAFTER SQL_NO_COALESCE, rows updated: {n_nc}")
print(table(c_nc).to_string(index=False))
print(f"\nAFTER SQL_UPDATE_FROM (SQLite 3.45), rows updated: {n_from}")
print(table(c_from).to_string(index=False))
print(f"\nAFTER SQL_WITH_UPDATE, rows updated: {n_with}")
print(table(c_with).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
cust = before.copy()
# pd:main
totals = orders.groupby("customer_id")["amount"].sum()                 # all-NaN group sums to 0.0 by default
pd_df = cust.assign(total_spent=cust["customer_id"].map(totals).fillna(0).astype("int64"))
# pd:end
print("\npandas map + fillna(0):")
print(pd_df.to_string(index=False))
strict = orders.groupby("customer_id")["amount"].sum(min_count=1)
print("pandas sum() of Esha's only (NaN) order:", totals.loc[5], "| with min_count=1:", strict.loc[5])

# compared by customer_id, same order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(sql_df, table(c_with), check_dtype=False)
assert table(c_nc)["total_spent"].isna().tolist() == [False, False, True, True, True]
assert table(c_from)["total_spent"].fillna(-1).tolist() == [150, 200, -1, 77, -1]
assert orders["amount"].sum() == sql_df["total_spent"].sum() == 350
print("\nasserts passed: SQL == pandas == WITH variant; UPDATE ... FROM leaves unmatched customers untouched; totals tie to orders (350)")
