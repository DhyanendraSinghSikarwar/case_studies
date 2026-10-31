# Q38: new vs returning active customers per month.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2025-01-05'),(1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-02'),
 (2,'2025-01-20'),(2,'2025-03-15'),
 (3,'2025-02-01'),(3,'2025-02-01'),(3,'2025-02-14'),
 (4,'2025-02-20'),(4,'2025-03-01'),
 (5,'2025-03-05'),(5,'2025-03-05'),
 (6,'2025-01-31'),(6,'2025-02-01'),
 (7,'2025-03-30');
""")

sql_answer = """
WITH m AS (
  SELECT DISTINCT customer_id, SUBSTR(activity_date, 1, 7) AS ym FROM wallet_activity
), f AS (
  SELECT customer_id, MIN(ym) AS first_ym FROM m GROUP BY customer_id
)
SELECT m.ym,
       SUM(CASE WHEN m.ym = f.first_ym THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN m.ym > f.first_ym THEN 1 ELSE 0 END) AS returning_customers
FROM m JOIN f ON f.customer_id = m.customer_id
GROUP BY m.ym
ORDER BY m.ym
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nsanity: raw rows", con.execute("SELECT COUNT(*) FROM wallet_activity").fetchone()[0],
      "| distinct customer-months", con.execute(
      "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, SUBSTR(activity_date,1,7) FROM wallet_activity)").fetchone()[0],
      "| sum of new + returning", int(got.new_customers.sum() + got.returning_customers.sum()))

# --- pandas
w = pd.read_sql("SELECT * FROM wallet_activity", con)
w["ym"] = w.activity_date.str[:7]
m = w[["customer_id", "ym"]].drop_duplicates()
m["first_ym"] = m.groupby("customer_id").ym.transform("min")
m["is_new"] = (m.ym == m.first_ym).astype(int)
m["is_ret"] = (m.ym > m.first_ym).astype(int)
want = (m.groupby("ym").agg(new_customers=("is_new", "sum"), returning_customers=("is_ret", "sum"))
        .reset_index())
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: 3 rows ordered by month")
