# Q24: duplicate payment detector (same user, merchant, amount, within 5 minutes of the previous such payment).
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, merchant TEXT, amount INTEGER, paid_at TEXT);
INSERT INTO payments VALUES
 (1,1,'m1',500,'2025-06-01 10:00:00'),
 (2,1,'m1',500,'2025-06-01 10:02:00'),
 (3,1,'m1',500,'2025-06-01 10:04:30'),
 (4,1,'m1',500,'2025-06-01 10:10:30'),
 (5,2,'m1',500,'2025-06-01 10:01:00'),
 (6,1,'m2',500,'2025-06-01 10:03:00'),
 (7,1,'m1',450,'2025-06-01 10:03:00');
"""
SQL = """
WITH x AS (
  SELECT payment_id, paid_at,
         LAG(payment_id) OVER w AS earlier_id,
         LAG(paid_at)    OVER w AS earlier_at
  FROM payments
  WINDOW w AS (PARTITION BY user_id, merchant, amount ORDER BY paid_at, payment_id)
)
SELECT payment_id AS later_id, earlier_id,
       CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) AS gap_seconds
FROM x
WHERE earlier_id IS NOT NULL
  AND CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) <= 300
ORDER BY later_id
"""
SQL_ALL_PAIRS = """
SELECT b.payment_id AS later_id, a.payment_id AS earlier_id
FROM payments a
JOIN payments b
  ON b.user_id = a.user_id AND b.merchant = a.merchant AND b.amount = a.amount
 AND (b.paid_at > a.paid_at OR (b.paid_at = a.paid_at AND b.payment_id > a.payment_id))
 AND CAST(strftime('%s', b.paid_at) AS INTEGER) - CAST(strftime('%s', a.paid_at) AS INTEGER) <= 300
ORDER BY later_id, earlier_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

pay = pd.read_sql("SELECT * FROM payments", con)
# PANDAS START
d = pay.assign(ts=pd.to_datetime(pay["paid_at"])).sort_values(["user_id", "merchant", "amount", "ts", "payment_id"])
g = d.groupby(["user_id", "merchant", "amount"])
d["earlier_id"] = g["payment_id"].shift(1)
d["gap_seconds"] = (d["ts"] - g["ts"].shift(1)).dt.total_seconds()
hit = d[d["earlier_id"].notna() & (d["gap_seconds"] <= 300)]
p = (hit.rename(columns={"payment_id": "later_id"})[["later_id", "earlier_id", "gap_seconds"]]
     .astype({"earlier_id": "int64", "gap_seconds": "int64"})
     .sort_values("later_id").reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (compared after sorting by later_id)")

allp = pd.read_sql(SQL_ALL_PAIRS, con)
print("\nself join on every earlier match returns", len(allp), "pairs:", [(int(a), int(b)) for a, b in allp.values])
print("payment 4 is 6:00 after payment 3, so it is not flagged; gap in seconds:",
      con.execute("SELECT CAST(strftime('%s','2025-06-01 10:10:30') AS INTEGER) - CAST(strftime('%s','2025-06-01 10:04:30') AS INTEGER)").fetchone()[0])
