# Q29: chained CTEs: first order date, first/repeat label, new vs repeat customers per month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',20),(2,1,'2024-01-20',30),(3,2,'2024-01-25',40),
 (4,1,'2024-02-03',10),(5,2,'2024-02-10',25),
 (6,3,'2024-02-15',60),(7,3,'2024-02-15',15),
 (8,4,'2024-03-01',35),(9,1,'2024-03-09',50);
"""
SQL_MAIN = """
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders
  GROUP BY customer_id
),
labelled AS (
  SELECT o.order_id, o.customer_id, strftime('%Y-%m', o.order_date) AS order_month,
         CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o
  JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT order_month,
       COUNT(DISTINCT CASE WHEN label = 'first'  THEN customer_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN label = 'repeat' THEN customer_id END) AS repeat_customers
FROM labelled
GROUP BY order_month
ORDER BY order_month
"""
SQL_GRAIN = """
WITH first_order AS (SELECT customer_id, MIN(order_date) AS first_date FROM orders GROUP BY customer_id),
labelled AS (
  SELECT o.order_id, o.customer_id, CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT 'first_order' AS cte, COUNT(*) AS n_rows, COUNT(DISTINCT customer_id) AS n_customers FROM first_order
UNION ALL SELECT 'labelled', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled
UNION ALL SELECT 'labelled first rows', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled WHERE label = 'first'
UNION ALL SELECT 'orders', COUNT(*), COUNT(DISTINCT customer_id) FROM orders
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
orders = pd.read_sql_query("SELECT * FROM orders", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("new vs repeat customers per month (SQL):")
print(sql_df.to_string(index=False))
print("\ngrain check (rows vs distinct customers):")
print(pd.read_sql_query(SQL_GRAIN, con).to_string(index=False))

# pd:main
o = orders.assign(first_date=orders.groupby("customer_id")["order_date"].transform("min"),
                  order_month=orders["order_date"].str[:7])
o["label"] = (o["order_date"] == o["first_date"]).map({True: "first", False: "repeat"})
new_c = o[o["label"] == "first"].groupby("order_month")["customer_id"].nunique()
rep_c = o[o["label"] == "repeat"].groupby("order_month")["customer_id"].nunique()
pd_df = (pd.DataFrame({"new_customers": new_c, "repeat_customers": rep_c})
         .fillna(0).astype("int64").rename_axis("order_month").reset_index())
# pd:end
print("\npandas version:")
print(pd_df.to_string(index=False))
print("\nlabelled orders per label:", o["label"].value_counts().to_dict())

# compared after ordering both by order_month
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert o["first_date"].notna().all() and len(o) == len(orders) == 9
assert o.loc[o["label"] == "first", "customer_id"].nunique() == 4 and (o["label"] == "first").sum() == 5
print("\nasserts passed: SQL == pandas (4 customers, 5 rows labelled 'first' because customer 3 has two orders on the first day)")
