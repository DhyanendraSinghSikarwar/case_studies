# Q36: payment success rate by merchant, NULL status counted two ways.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE payments(payment_id INTEGER, merchant_id TEXT, status TEXT);
INSERT INTO payments VALUES
 (1,'m1','SUCCESS'),(2,'m1','SUCCESS'),(3,'m1','FAILED'),(4,'m1',NULL),
 (5,'m2','SUCCESS'),(6,'m2','FAILED'),
 (7,'m3',NULL),(8,'m3',NULL);
""")

sql_answer = """
SELECT merchant_id,
       COUNT(*) AS attempts,
       SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successes,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS rate_all,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(status), 0), 4) AS rate_known
FROM payments
GROUP BY merchant_id
ORDER BY merchant_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\ntrap: WHERE status <> 'SUCCESS' returns", con.execute(
    "SELECT COUNT(*) FROM payments WHERE status <> 'SUCCESS'").fetchone()[0],
    "rows (FAILED only), the 3 NULL rows vanish")

# --- pandas
p = pd.read_sql("SELECT * FROM payments", con)
p["ok"] = (p.status == "SUCCESS").astype(int)
g = p.groupby("merchant_id").agg(attempts=("payment_id", "size"), successes=("ok", "sum"),
                                 known=("status", "count")).reset_index()
g["rate_all"] = (g.successes / g.attempts).round(4)
g["rate_known"] = (g.successes / g.known.replace(0, np.nan)).round(4)
want = g[["merchant_id", "attempts", "successes", "rate_all", "rate_known"]]
# --- end pandas
print("\npandas"); print(want.to_string(index=False, na_rep="NaN"))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: ordered by merchant_id; m3 has rate_all 0.0 and rate_known NULL/NaN")
