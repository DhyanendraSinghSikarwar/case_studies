# Q5: velocity check: >= 3 APPROVED txns in any 10-minute window (inclusive), per card.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE card_txns(txn_id INTEGER PRIMARY KEY, card_id INTEGER, txn_ts TEXT, amount INTEGER, status TEXT);
INSERT INTO card_txns VALUES
 (1,1,'2025-05-01 10:00:00',100,'APPROVED'),
 (2,1,'2025-05-01 10:04:00',100,'APPROVED'),
 (3,1,'2025-05-01 10:10:00',100,'APPROVED'),   -- exactly 10:00 after the first: counts
 (4,1,'2025-05-01 10:10:30',100,'APPROVED'),
 (5,2,'2025-05-01 11:00:00',100,'APPROVED'),
 (6,2,'2025-05-01 11:05:00',100,'APPROVED'),
 (7,2,'2025-05-01 11:10:01',100,'APPROVED'),   -- 10 min 1 sec after the first: too late
 (8,3,'2025-05-01 12:00:00',100,'APPROVED'),
 (9,3,'2025-05-01 12:02:00',100,'DECLINED'),   -- would be the third, but declined
 (10,3,'2025-05-01 12:04:00',100,'APPROVED'),
 (11,4,'2025-05-01 13:00:00',100,'APPROVED'),
 (12,4,'2025-05-01 13:01:00',100,'APPROVED'),
 (13,4,'2025-05-01 13:02:00',100,'APPROVED');
""")

windows_sql = """
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
)
SELECT x.card_id, x.txn_ts AS window_start, COUNT(*) AS txns
FROM a x JOIN a y ON y.card_id = x.card_id AND y.s BETWEEN x.s AND x.s + 600
GROUP BY x.card_id, x.txn_ts
HAVING COUNT(*) >= 3
ORDER BY x.card_id, x.txn_ts
"""
lag_sql = """
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
), l AS (
  SELECT card_id, txn_ts, s, LAG(s, 2) OVER (PARTITION BY card_id ORDER BY s) AS s2,
         LAG(txn_ts, 2) OVER (PARTITION BY card_id ORDER BY s) AS ts2
  FROM a
)
SELECT card_id, MIN(ts2) AS first_window_start
FROM l WHERE s2 IS NOT NULL AND s - s2 <= 600
GROUP BY card_id ORDER BY card_id
"""
range_sql = """
WITH a AS (
  SELECT card_id, txn_ts, CAST(strftime('%s', txn_ts) AS INTEGER) AS s
  FROM card_txns WHERE status = 'APPROVED'
)
SELECT card_id, txn_ts AS window_start,
       COUNT(*) OVER (PARTITION BY card_id ORDER BY s RANGE BETWEEN CURRENT ROW AND 600 FOLLOWING) AS txns
FROM a ORDER BY card_id, txn_ts
"""
text_range = """
SELECT COUNT(*) OVER (PARTITION BY card_id ORDER BY txn_ts RANGE BETWEEN CURRENT ROW AND '10 minutes' FOLLOWING) FROM card_txns
"""
w = pd.read_sql(windows_sql, con)
print("SQL windows (self join on integer seconds):"); print(w.to_string(index=False)); print()
lg = pd.read_sql(lag_sql, con)
print("SQL LAG(...,2) cross-check, earliest window start per card:"); print(lg.to_string(index=False)); print()
rg = pd.read_sql(range_sql, con); rg = rg[rg.txns >= 3].reset_index(drop=True)
print("SQL RANGE frame over integer seconds (works):"); print(rg.to_string(index=False)); print()
try:
    con.execute(text_range).fetchall()
    print("RANGE with an interval string over text: no error")
except sqlite3.Error as e:
    print("RANGE with '10 minutes' over text timestamps ->", type(e).__name__, ":", e)
print()

# pandas: per card, sorted approved times; count txns in [t, t + 600s] with searchsorted
t = pd.read_sql("SELECT * FROM card_txns", con)
t = t[t["status"] == "APPROVED"].copy()
t["ts"] = pd.to_datetime(t["txn_ts"])
t = t.sort_values(["card_id", "ts"]).reset_index(drop=True)
def count_in_window(g):
    v = g["ts"].to_numpy()
    end = np.searchsorted(v, v + np.timedelta64(600, "s"), side="right")   # side=right keeps t+600s inclusive
    return pd.Series(end - np.arange(len(v)), index=g.index)
t["txns"] = t.groupby("card_id", group_keys=False).apply(count_in_window)
p = (t[t["txns"] >= 3][["card_id", "txn_ts", "txns"]]
     .rename(columns={"txn_ts": "window_start"}).reset_index(drop=True))
print("pandas windows:"); print(p.to_string(index=False)); print()
pd.testing.assert_frame_equal(w, p, check_dtype=False)
pd.testing.assert_frame_equal(w, rg, check_dtype=False)

# LAG(2) equivalent in pandas: shift(2), earliest start per card
t["ts2"] = t.groupby("card_id")["ts"].shift(2)
flag = t[(t["ts"] - t["ts2"]) <= pd.Timedelta(minutes=10)]
p_lag = flag.groupby("card_id", as_index=False)["ts2"].min()
p_lag["first_window_start"] = p_lag.pop("ts2").dt.strftime("%Y-%m-%d %H:%M:%S")
pd.testing.assert_frame_equal(lg, p_lag, check_dtype=False)
print("asserts passed (self join = RANGE-on-seconds = pandas searchsorted; LAG(2) = shift(2); order card_id, window_start)")
