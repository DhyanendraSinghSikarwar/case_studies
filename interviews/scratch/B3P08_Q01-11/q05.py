# Q5: LeetCode 1174 Immediate Food Delivery II: join-to-MIN and ROW_NUMBER, SQL and pandas
import sqlite3
import pandas as pd

BASE = """
 (1,1,'2024-03-01','2024-03-01'),(2,1,'2024-03-05','2024-03-05'),
 (3,2,'2024-03-02','2024-03-04'),(4,2,'2024-03-10','2024-03-10'),
 (5,3,'2024-03-03','2024-03-03'),
 (6,4,'2024-03-04','2024-03-09'),(7,4,'2024-03-06','2024-03-06'),
 (8,5,'2024-03-07','2024-03-07'),
 (9,6,'2024-03-08','2024-03-12')"""
DIRTY = ",\n (10,7,'2024-03-02','2024-03-04'),(11,7,'2024-03-09','2024-03-02')"      # a pref date before the order date
TIE = ",\n (12,8,'2024-03-11','2024-03-11'),(13,8,'2024-03-11','2024-03-15')"        # two orders on the earliest date
DDL = "CREATE TABLE delivery(delivery_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, customer_pref_delivery_date TEXT);\nINSERT INTO delivery VALUES"

SQL_JOIN = """
SELECT ROUND(100.0 * SUM(d.order_date = d.customer_pref_delivery_date) / COUNT(*), 2) AS immediate_pct
FROM delivery d
JOIN (SELECT customer_id, MIN(order_date) AS first_date
      FROM delivery GROUP BY customer_id) f
  ON f.customer_id = d.customer_id AND f.first_date = d.order_date
"""
SQL_RN = """
SELECT ROUND(100.0 * AVG(order_date = customer_pref_delivery_date), 2) AS immediate_pct
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, delivery_id) AS rn
      FROM delivery)
WHERE rn = 1
"""
SQL_MIN_MIN = """
SELECT ROUND(100.0 * SUM(min_order = min_pref) / COUNT(*), 2) AS immediate_pct
FROM (SELECT customer_id, MIN(order_date) AS min_order, MIN(customer_pref_delivery_date) AS min_pref
      FROM delivery GROUP BY customer_id)
"""
SQL_ALL_ORDERS = """
SELECT ROUND(100.0 * AVG(order_date = customer_pref_delivery_date), 2) FROM delivery
"""

def make(extra=""):
    con = sqlite3.connect(":memory:")
    con.executescript(DDL + BASE + extra + ";")
    return con

def pandas_versions(delivery):
    # pd:main
    d = delivery.sort_values(["customer_id", "order_date", "delivery_id"])
    first = d.groupby("customer_id").head(1)                       # ROW_NUMBER() = 1
    rn = round(100 * (first["order_date"] == first["customer_pref_delivery_date"]).mean(), 2)
    m = delivery.groupby("customer_id")["order_date"].transform("min")
    f = delivery[delivery["order_date"] == m]                      # join to MIN keeps ties
    jn = round(100 * (f["order_date"] == f["customer_pref_delivery_date"]).mean(), 2)
    # pd:end
    return jn, rn

for label, extra in [("clean data (guarantee holds)", ""), ("dirty: pref date before order date", DIRTY),
                     ("tie: two orders on the earliest date", TIE)]:
    con = make(extra)
    j = con.execute(SQL_JOIN).fetchone()[0]
    r = con.execute(SQL_RN).fetchone()[0]
    mm = con.execute(SQL_MIN_MIN).fetchone()[0]
    allo = con.execute(SQL_ALL_ORDERS).fetchone()[0]
    pj, pr = pandas_versions(pd.read_sql_query("SELECT * FROM delivery", con))
    assert (pj, pr) == (j, r)   # scalars, no row order
    print(f"{label}: join-to-MIN {j} | ROW_NUMBER {r} | MIN vs MIN {mm} | all orders {allo} | pandas {pj} / {pr}")
print("asserts passed")
