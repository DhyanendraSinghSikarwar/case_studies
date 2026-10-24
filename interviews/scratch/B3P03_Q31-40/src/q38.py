# Q38: orders above the customer's average of EARLIER orders: correlated subquery with date and tie-break
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-01',100),(2,1,'2024-01-10',200),(3,1,'2024-01-10',150),(4,1,'2024-02-01',90),
 (5,2,'2024-01-05',50),(6,2,'2024-01-06',70),
 (7,3,'2024-01-09',500);
"""
SQL_MAIN = """
SELECT o.order_id, o.customer_id, o.order_date, o.amount,
       (SELECT AVG(p.amount) FROM orders p
        WHERE p.customer_id = o.customer_id
          AND (p.order_date < o.order_date
               OR (p.order_date = o.order_date AND p.order_id < o.order_id))) AS earlier_avg
FROM orders o
WHERE o.amount > (SELECT AVG(p.amount) FROM orders p
                  WHERE p.customer_id = o.customer_id
                    AND (p.order_date < o.order_date
                         OR (p.order_date = o.order_date AND p.order_id < o.order_id)))
ORDER BY o.order_id
"""
# the same condition with a row-value comparison
SQL_ROW = """
SELECT o.order_id, o.customer_id, o.order_date, o.amount,
       (SELECT AVG(p.amount) FROM orders p
        WHERE p.customer_id = o.customer_id AND (p.order_date, p.order_id) < (o.order_date, o.order_id)) AS earlier_avg
FROM orders o
WHERE o.amount > (SELECT AVG(p.amount) FROM orders p
                  WHERE p.customer_id = o.customer_id AND (p.order_date, p.order_id) < (o.order_date, o.order_id))
ORDER BY o.order_id
"""
SQL_ALL = """
SELECT o.order_id, (SELECT AVG(p.amount) FROM orders p
        WHERE p.customer_id = o.customer_id
          AND (p.order_date < o.order_date OR (p.order_date = o.order_date AND p.order_id < o.order_id))) AS earlier_avg
FROM orders o ORDER BY o.order_id
"""
SQL_DATE_ONLY = SQL_MAIN.replace("OR (p.order_date = o.order_date AND p.order_id < o.order_id)", "")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
row_df = pd.read_sql_query(SQL_ROW, con)
print("earlier average for every order (NULL = no earlier order):")
print(pd.read_sql_query(SQL_ALL, con).to_string(index=False))
print("\nSQL result (amount > earlier average):")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, row_df)
print("\nassert: row-value comparison (a, b) < (c, d) gives the same rows as the OR form")
print("date-only version (no tie-break):", [r[0] for r in con.execute(SQL_DATE_ONLY)], "| with tie-break:", sql_df["order_id"].tolist())

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.sort_values(["customer_id", "order_date", "order_id"]).copy()
o["earlier_avg"] = o.groupby("customer_id")["amount"].transform(lambda s: s.expanding().mean().shift(1))
pd_df = (o[o["amount"] > o["earlier_avg"]]
         .sort_values("order_id").reset_index(drop=True))
# pd:end
print("\npandas expanding().mean().shift(1):")
print(pd_df.to_string(index=False))
# compared by order_id
pd.testing.assert_frame_equal(sql_df, pd_df[["order_id", "customer_id", "order_date", "amount", "earlier_avg"]], check_dtype=False)
print("\nassert: SQL == pandas")
