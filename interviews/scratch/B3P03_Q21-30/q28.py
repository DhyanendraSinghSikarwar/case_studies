# Q28: orders of the top 3 customers by total spend: LIMIT inside IN, derived-table join, tie at rank 3
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Eve'),(6,'Farid');
INSERT INTO orders VALUES
 (1,1,300),(2,1,200),(3,2,400),(4,3,300),(5,4,100),(6,4,200),(7,5,100);
"""
SQL_MAIN = """
SELECT order_id, customer_id, amount
FROM orders
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      ORDER BY SUM(amount) DESC, customer_id
                      LIMIT 3)
ORDER BY order_id
"""
SQL_DERIVED = """
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN (SELECT customer_id
      FROM orders
      GROUP BY customer_id
      ORDER BY SUM(amount) DESC, customer_id
      LIMIT 3) top3 ON top3.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_TIES = """
WITH spend AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN spend s ON s.customer_id = o.customer_id
WHERE s.total >= (SELECT total FROM spend ORDER BY total DESC LIMIT 1 OFFSET 2)
ORDER BY o.order_id
"""
SQL_NO_TIEBREAK = """
SELECT customer_id FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC LIMIT 3
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("totals per customer:", con.execute(
    "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC, customer_id").fetchall())

sql_df = pd.read_sql_query(SQL_MAIN, con)
der_df = pd.read_sql_query(SQL_DERIVED, con)
ties_df = pd.read_sql_query(SQL_TIES, con)
print("\nIN (... LIMIT 3), tie broken by customer_id:")
print(sql_df.to_string(index=False))
print("derived-table join gives the same rows:", sql_df.equals(der_df))
print("tie-inclusive (total >= third-highest total) customers:", sorted(ties_df["customer_id"].unique().tolist()))
print("without the customer_id tie-break the rank-3 pick is left to the engine; this run chose:",
      [r[0] for r in con.execute(SQL_NO_TIEBREAK)])

print("\nLIMIT / OFFSET forms on SQLite 3.45:")
print("  LIMIT 1+1 OFFSET 4/2        ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT 1+1 OFFSET 4/2")])
print("  LIMIT -1 OFFSET 5           ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT -1 OFFSET 5")])
print("  LIMIT (SELECT 2)            ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT (SELECT 2)")])
try:
    con.execute("SELECT order_id FROM orders ORDER BY order_id OFFSET 1").fetchall()
except sqlite3.Error as e:
    print("  OFFSET without LIMIT        -> error:", e)

# pd:main
totals = orders.groupby("customer_id")["amount"].sum().reset_index()
top3 = totals.sort_values(["amount", "customer_id"], ascending=[False, True]).head(3)     # tie-break by id
pd_df = orders[orders["customer_id"].isin(top3["customer_id"])].sort_values("order_id").reset_index(drop=True)
tie_ids = totals.set_index("customer_id")["amount"].nlargest(3, keep="all").index     # keep every tie at rank 3
pd_ties = orders[orders["customer_id"].isin(tie_ids)].sort_values("order_id").reset_index(drop=True)
# pd:end
print("\npandas nlargest(3, keep='all') customers:", sorted(tie_ids.tolist()))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(ties_df, pd_ties, check_dtype=False)
assert sorted(sql_df["customer_id"].unique()) == [1, 2, 3] and sorted(ties_df["customer_id"].unique()) == [1, 2, 3, 4]
print("\nasserts passed: SQL IN(LIMIT) == derived join == pandas (customers 1, 2, 3); tie-inclusive == nlargest(keep='all') (1, 2, 3, 4); compared by order_id")
