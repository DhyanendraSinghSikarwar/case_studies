# Q29: repeat purchase share and days from first to second order, cancelled orders excluded.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2025-01-01','DELIVERED'),(2,1,'2025-01-31','DELIVERED'),
 (3,2,'2025-01-05','DELIVERED'),(4,2,'2025-01-05','DELIVERED'),
 (5,3,'2025-01-01','CANCELLED'),(6,3,'2025-01-10','DELIVERED'),(7,3,'2025-01-20','DELIVERED'),
 (8,4,'2025-02-01','DELIVERED'),
 (9,5,'2025-02-10','DELIVERED'),
 (10,6,'2025-03-01','DELIVERED'),(11,6,'2025-03-05','CANCELLED'),
 (12,7,'2025-01-15','DELIVERED'),(13,7,'2025-02-14','DELIVERED'),(14,7,'2025-03-16','DELIVERED'),
 (15,8,'2025-02-20','CANCELLED');
"""
SQL = """
WITH ok AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
  WHERE status <> 'CANCELLED'
),
per AS (
  SELECT customer_id,
         MAX(CASE WHEN rn = 1 THEN order_date END) AS first_date,
         MAX(CASE WHEN rn = 2 THEN order_date END) AS second_date
  FROM ok
  GROUP BY customer_id
)
SELECT COUNT(*) AS customers,
       COUNT(second_date) AS repeaters,
       ROUND(1.0 * COUNT(second_date) / COUNT(*), 4) AS repeat_share,
       AVG(julianday(second_date) - julianday(first_date)) AS avg_days_to_second
FROM per
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

o = pd.read_sql("SELECT * FROM orders", con)
# PANDAS START
ok = o[o["status"] != "CANCELLED"].copy()
ok["order_date"] = pd.to_datetime(ok["order_date"])
ok = ok.sort_values(["customer_id", "order_date", "order_id"])
ok["rn"] = ok.groupby("customer_id").cumcount() + 1
first = ok[ok["rn"] == 1].set_index("customer_id")["order_date"]
second = ok[ok["rn"] == 2].set_index("customer_id")["order_date"]
days = (second - first.reindex(second.index)).dt.days
p = pd.DataFrame({"customers": [len(first)], "repeaters": [len(second)],
                  "repeat_share": [round(len(second) / len(first), 4)],
                  "avg_days_to_second": [days.mean()]})
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (single row)")
print("per-customer days to second order:", days.sort_index().to_dict())
print("customers with any order (incl. cancelled-only):", o["customer_id"].nunique(),
      "-> share on that denominator:", round(len(second) / o["customer_id"].nunique(), 4))
