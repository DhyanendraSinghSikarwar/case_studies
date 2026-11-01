# Q40: cart abandonment rate and purchase-before-add anomaly.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(session_id TEXT, event_name TEXT, event_ts TEXT);
INSERT INTO events VALUES
 ('s1','add_to_cart','2025-05-01 10:00:00'),('s1','purchase','2025-05-01 10:05:00'),
 ('s2','add_to_cart','2025-05-01 11:00:00'),
 ('s3','add_to_cart','2025-05-01 12:00:00'),('s3','add_to_cart','2025-05-01 12:02:00'),
 ('s4','purchase','2025-05-01 09:00:00'),('s4','add_to_cart','2025-05-01 09:30:00'),
 ('s5','add_to_cart','2025-05-01 10:00:00'),('s5','purchase','2025-05-01 10:30:00'),('s5','add_to_cart','2025-05-01 10:40:00'),
 ('s6','page_view','2025-05-01 13:00:00'),
 ('s7','purchase','2025-05-01 14:00:00'),
 ('s8','add_to_cart','2025-05-01 15:00:00'),('s8','purchase','2025-05-01 15:00:00');
""")

sql_answer = """
WITH s AS (
  SELECT session_id,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_add,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY session_id
)
SELECT COUNT(*) AS carts,
       SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) AS abandoned,
       ROUND(SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS abandonment_rate,
       SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) AS purchase_before_add,
       ROUND(SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS anomaly_rate
FROM s
WHERE first_add IS NOT NULL
"""
# second formulation with EXISTS, same two counts
sql_exists = """
SELECT COUNT(*) AS carts,
       SUM(NOT EXISTS (SELECT 1 FROM events p WHERE p.session_id = a.session_id AND p.event_name = 'purchase')) AS abandoned,
       SUM(EXISTS (SELECT 1 FROM events p WHERE p.session_id = a.session_id AND p.event_name = 'purchase'
                   AND p.event_ts < a.first_add)) AS purchase_before_add
FROM (SELECT session_id, MIN(event_ts) AS first_add FROM events WHERE event_name = 'add_to_cart' GROUP BY session_id) a
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
ex = pd.read_sql(sql_exists, con)
print("\nEXISTS version"); print(ex.to_string(index=False))

# --- pandas
e = pd.read_sql("SELECT * FROM events", con)
s = (e.assign(add=e.event_ts.where(e.event_name == "add_to_cart"),
              buy=e.event_ts.where(e.event_name == "purchase"))
     .groupby("session_id").agg(first_add=("add", "min"), first_purchase=("buy", "min")))
carts = s[s.first_add.notna()]
abandoned = int(carts.first_purchase.isna().sum())
anomaly = int((carts.first_purchase < carts.first_add).sum())
want = pd.DataFrame({"carts": [len(carts)], "abandoned": [abandoned],
                     "abandonment_rate": [round(abandoned / len(carts), 4)],
                     "purchase_before_add": [anomaly], "anomaly_rate": [round(anomaly / len(carts), 4)]})
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
assert (ex.iloc[0].tolist() == got[["carts", "abandoned", "purchase_before_add"]].iloc[0].tolist())
print("assert passed: one-row result equal in SQL (CASE and EXISTS) and pandas; 8 sessions, 6 with an add_to_cart")
