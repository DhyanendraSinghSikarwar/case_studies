# Q39: orders and revenue by status with NULL amounts.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'DELIVERED',100),(2,2,'DELIVERED',200),(3,3,'DELIVERED',NULL),
 (4,4,'CANCELLED',NULL),(5,5,'CANCELLED',50),(6,6,'CANCELLED',NULL),
 (7,7,'RETURNED',80),
 (8,8,'SHIPPED',NULL);
""")

sql_answer = """
SELECT status,
       COUNT(*) AS orders,
       COUNT(amount) AS orders_with_amount,
       SUM(amount) AS revenue,
       AVG(amount) AS avg_amount
FROM orders
GROUP BY status
ORDER BY status
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\nwrong average, SUM / COUNT(*) for DELIVERED:",
      con.execute("SELECT SUM(amount) * 1.0 / COUNT(*) FROM orders WHERE status = 'DELIVERED'").fetchone()[0],
      "vs AVG:", con.execute("SELECT AVG(amount) FROM orders WHERE status = 'DELIVERED'").fetchone()[0])

# --- pandas
o = pd.read_sql("SELECT * FROM orders", con)
want = (o.groupby("status").agg(orders=("order_id", "size"), orders_with_amount=("amount", "count"),
                                revenue=("amount", lambda s: s.sum(min_count=1)),
                                avg_amount=("amount", "mean"))
        .reset_index())
# --- end pandas
print("\npandas (sum with min_count=1)"); print(want.to_string(index=False, na_rep="NaN"))
plain = o.groupby("status").amount.sum()
print("\npandas plain sum() for SHIPPED:", plain["SHIPPED"], "(SQL SUM gives NULL; pandas gives 0.0)")
print("amount.count() =", o.amount.count(), "| len(o) =", len(o), "| mean(skipna=False) =", o.amount.mean(skipna=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: ordered by status; SHIPPED revenue NULL equals NaN only with min_count=1")
