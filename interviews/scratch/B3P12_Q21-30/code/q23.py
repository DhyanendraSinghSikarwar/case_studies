# Q23: latest transaction per user with the balance after it; tie on timestamp broken by txn_id.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE bank_txns(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_ts TEXT, signed_amount INTEGER);
INSERT INTO bank_txns VALUES
 (1,1,'2025-06-01 09:00:00',1000),
 (2,1,'2025-06-02 10:00:00',-300),
 (3,1,'2025-06-02 10:00:00',-200),
 (4,2,'2025-06-01 12:00:00',500),
 (5,2,'2025-06-03 08:00:00',250),
 (6,3,'2025-06-05 15:30:00',-40);
"""
SQL = """
WITH t AS (
  SELECT txn_id, user_id, txn_ts,
         SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts, txn_id
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_after,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_ts DESC, txn_id DESC) AS rn
  FROM bank_txns
)
SELECT user_id, txn_id AS last_txn_id, txn_ts AS last_ts, balance_after
FROM t
WHERE rn = 1
ORDER BY user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

tx = pd.read_sql("SELECT * FROM bank_txns", con)
# PANDAS START
t = tx.sort_values(["user_id", "txn_ts", "txn_id"]).reset_index(drop=True)
t["balance_after"] = t.groupby("user_id")["signed_amount"].cumsum()
p = (t.groupby("user_id").tail(1)
     .rename(columns={"txn_id": "last_txn_id", "txn_ts": "last_ts"})
     [["user_id", "last_txn_id", "last_ts", "balance_after"]]
     .sort_values("user_id").reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (one row per user, ordered by user_id)")

# the tie trap: ORDER BY txn_ts DESC only picks either of txns 2 and 3 for user 1 (not defined)
# and a default-frame running sum gives both tied rows the SAME balance
r = con.execute("""SELECT txn_id, SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts) AS bal
                   FROM bank_txns WHERE user_id = 1 ORDER BY txn_id""").fetchall()
print("user 1, default frame, ORDER BY txn_ts only (txn_id, balance):", r)
