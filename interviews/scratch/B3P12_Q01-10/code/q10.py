# Q10: new / retained / resurrected / churned customers per month of 2025.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2024-12-20'),(1,'2025-01-05'),(1,'2025-01-20'),(1,'2025-02-03'),(1,'2025-03-03'),   -- Dec, Jan, Feb, Mar (two Jan rows)
 (2,'2025-01-10'),(2,'2025-04-02'),(2,'2025-05-01'),                                      -- Jan, gap Feb-Mar, back Apr: resurrected
 (3,'2025-02-14'),(3,'2025-03-14'),(3,'2025-03-15'),                                      -- new Feb, Mar, then churns
 (4,'2025-03-09'),(4,'2025-05-09'),                                                       -- new Mar, skips Apr, back May
 (5,'2025-01-30'),                                                                        -- Jan only: churned in Feb
 (6,'2024-10-11'),(6,'2025-03-21'),                                                       -- active in Oct 2024, back in Mar: resurrected
 (7,'2025-04-04'),(7,'2025-05-05'),(7,'2025-06-06'),                                      -- new Apr, retained
 (8,'2025-06-01');                                                                        -- new Jun
""")

sql = """
WITH spine(m) AS (VALUES ('2025-01'),('2025-02'),('2025-03'),('2025-04'),('2025-05'),('2025-06')),
am AS (SELECT DISTINCT customer_id, substr(activity_date, 1, 7) AS m FROM wallet_activity),
fst AS (SELECT customer_id, MIN(m) AS fm FROM am GROUP BY customer_id),
s AS (SELECT m, strftime('%Y-%m', m || '-01', '-1 month') AS prev FROM spine)
SELECT s.m AS month,
  (SELECT COUNT(*) FROM am WHERE am.m = s.m) AS active,
  (SELECT COUNT(*) FROM fst WHERE fst.fm = s.m) AS new_customers,
  (SELECT COUNT(*) FROM am a WHERE a.m = s.m
     AND EXISTS (SELECT 1 FROM am p WHERE p.customer_id = a.customer_id AND p.m = s.prev)) AS retained,
  (SELECT COUNT(*) FROM am a WHERE a.m = s.m
     AND NOT EXISTS (SELECT 1 FROM am p WHERE p.customer_id = a.customer_id AND p.m = s.prev)
     AND EXISTS (SELECT 1 FROM am e WHERE e.customer_id = a.customer_id AND e.m < s.prev)) AS resurrected,
  (SELECT COUNT(*) FROM am p WHERE p.m = s.prev
     AND NOT EXISTS (SELECT 1 FROM am a WHERE a.customer_id = p.customer_id AND a.m = s.m)) AS churned
FROM s ORDER BY s.m
"""
s = pd.read_sql(sql, con)
print("SQL:"); print(s.to_string(index=False)); print()
assert (s["active"] == s["new_customers"] + s["retained"] + s["resurrected"]).all()
print("identity holds in SQL: active = new + retained + resurrected")

# pandas: monthly sets
wa = pd.read_sql("SELECT * FROM wallet_activity", con)
wa["m"] = pd.to_datetime(wa["activity_date"]).dt.to_period("M")
sets = wa.groupby("m")["customer_id"].agg(set)
first = wa.groupby("customer_id")["m"].min()
rows = []
for m in pd.period_range("2025-01", "2025-06", freq="M"):
    cur = sets.get(m, set()); prev = sets.get(m - 1, set())
    earlier = set().union(*[v for k, v in sets.items() if k < m - 1])
    rows.append({"month": str(m), "active": len(cur),
                 "new_customers": int((first == m).sum()),
                 "retained": len(cur & prev),
                 "resurrected": len((cur - prev) & earlier),
                 "churned": len(prev - cur)})
p = pd.DataFrame(rows)
print(); print("pandas:"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("asserts passed (order: month)")
