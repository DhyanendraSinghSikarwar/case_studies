# Q31: correlated scalar subqueries in the SELECT list vs one join to a derived table; pandas transform
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',100),(2,1,'2024-01-20',200),(3,1,'2024-02-02',300),
 (4,2,'2024-01-10',50),(5,2,'2024-03-01',150),
 (6,3,'2024-02-14',80),(7,3,'2024-02-20',NULL);
"""
SQL_MAIN = """
SELECT o.order_id, o.customer_id, o.amount,
       (SELECT COUNT(*) FROM orders i WHERE i.customer_id = o.customer_id) AS n_orders,
       (SELECT AVG(i.amount) FROM orders i WHERE i.customer_id = o.customer_id) AS avg_amount,
       o.amount - (SELECT AVG(i.amount) FROM orders i WHERE i.customer_id = o.customer_id) AS diff_from_avg
FROM orders o
ORDER BY o.order_id
"""
SQL_JOIN = """
SELECT o.order_id, o.customer_id, o.amount,
       s.n_orders, s.avg_amount, o.amount - s.avg_amount AS diff_from_avg
FROM orders o
JOIN (SELECT customer_id, COUNT(*) AS n_orders, AVG(amount) AS avg_amount
      FROM orders GROUP BY customer_id) s ON s.customer_id = o.customer_id
ORDER BY o.order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
join_df = pd.read_sql_query(SQL_JOIN, con)
print("SQL correlated scalar subqueries:")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, join_df)
print("\nassert: correlated version == derived-table join (same rows, ordered by order_id)")

print("\nEXPLAIN QUERY PLAN, correlated version:")
for r in con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN):
    print("  ", r[3])
print("EXPLAIN QUERY PLAN, join version:")
for r in con.execute("EXPLAIN QUERY PLAN " + SQL_JOIN):
    print("  ", r[3])

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
g = orders.groupby("customer_id")
pd_df = orders.assign(
    n_orders=g["order_id"].transform("count"),
    avg_amount=g["amount"].transform("mean"),
)
pd_df["diff_from_avg"] = pd_df["amount"] - pd_df["avg_amount"]
pd_df = pd_df[["order_id", "customer_id", "amount", "n_orders", "avg_amount", "diff_from_avg"]].sort_values("order_id").reset_index(drop=True)
# pd:end
print("\npandas transform:")
print(pd_df.to_string(index=False))
# compared after sorting by order_id; amount is float in pandas because of the NULL
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nassert: SQL == pandas")
print("transform('count') on amount instead of order_id, customer 3:",
      g["amount"].transform("count")[orders.customer_id == 3].tolist(), "(NULL amount not counted; COUNT(*) gives 2)")
print("SQL COUNT(amount) for customer 3:", con.execute("SELECT COUNT(amount) FROM orders WHERE customer_id=3").fetchone()[0])

# an order with a NULL customer_id: correlation '=' never matches it
con.execute("INSERT INTO orders VALUES (8, NULL, '2024-03-05', 40)")
c_df = pd.read_sql_query(SQL_MAIN, con)
j_df = pd.read_sql_query(SQL_JOIN, con)
print("\nafter adding order 8 with customer_id NULL:")
print("correlated row for order 8:", c_df[c_df.order_id == 8][["n_orders", "avg_amount"]].values.tolist(), "(COUNT(*) is 0, AVG is NULL)")
print("rows: correlated", len(c_df), "| INNER JOIN to derived table", len(j_df), "(order 8 is dropped)")
orders2 = pd.read_sql_query("SELECT * FROM orders", con)
tc = orders2.groupby("customer_id")["order_id"].transform("count")
print("pandas transform('count') for order 8:", tc[orders2.order_id == 8].tolist(), "(NaN key, so NaN; SQL gives 0)")
