# Q35: delete duplicates keeping the latest row per (user_id, message)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logs(log_id INTEGER PRIMARY KEY, user_id INTEGER, message TEXT, created_at TEXT);
INSERT INTO logs VALUES
 (1,1,'login','2026-01-01 10:00'),(2,1,'login','2026-01-02 09:00'),(3,1,'login','2026-01-02 09:00'),
 (4,1,'logout','2026-01-01 11:00'),(5,2,'login','2026-01-03 08:00'),(6,2,'login','2026-01-01 08:00'),
 (7,3,'view','2026-01-01 12:00'),(8,4,NULL,'2026-01-01 13:00'),(9,4,NULL,'2026-01-02 13:00');
"""
SQL_PREVIEW = """
SELECT log_id, user_id, message, created_at, rn FROM (
  SELECT log_id, user_id, message, created_at,
         ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn
  FROM logs)
WHERE rn > 1 ORDER BY log_id
"""
SQL_MAIN = """
DELETE FROM logs WHERE log_id IN (
  SELECT log_id FROM (
    SELECT log_id,
           ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn
    FROM logs)
  WHERE rn > 1)
"""
SQL_CTE = """
WITH ranked AS (
  SELECT log_id,
         ROW_NUMBER() OVER (PARTITION BY user_id, message ORDER BY created_at DESC, log_id DESC) AS rn
  FROM logs)
DELETE FROM logs WHERE log_id IN (SELECT log_id FROM ranked WHERE rn > 1)
"""
def fresh():
    c = sqlite3.connect(":memory:"); c.executescript(SCHEMA); return c
con = fresh()
before = pd.read_sql_query("SELECT * FROM logs ORDER BY log_id", con)
print("BEFORE:"); print(before.to_string(index=False))
print("\nPreview (rows with rn > 1, to be deleted):"); print(pd.read_sql_query(SQL_PREVIEW, con).to_string(index=False))
t0 = con.total_changes
con.execute(SQL_MAIN)
print("\nrows deleted by subquery form:", con.total_changes - t0)
after = pd.read_sql_query("SELECT * FROM logs ORDER BY log_id", con)
print("AFTER:"); print(after.to_string(index=False))
con2 = fresh(); t0 = con2.total_changes
con2.execute(SQL_CTE)
after_cte = pd.read_sql_query("SELECT * FROM logs ORDER BY log_id", con2)
print("rows deleted by WITH ... DELETE form:", con2.total_changes - t0, "| same table:", after.equals(after_cte))

logs = before.copy()
# pd:main
pd_df = (logs.sort_values(["created_at", "log_id"])
             .drop_duplicates(subset=["user_id", "message"], keep="last")
             .sort_values("log_id"))
# pd:end
print("\npandas drop_duplicates(keep='last') after sorting by created_at, log_id:"); print(pd_df.to_string(index=False))
# compared after sorting by log_id
pd.testing.assert_frame_equal(after.reset_index(drop=True), pd_df.reset_index(drop=True), check_dtype=False)
assert after.equals(after_cte)
assert after["log_id"].tolist() == [3, 4, 5, 7, 9]
# the NULL message pair is treated as one group by PARTITION BY and by drop_duplicates
assert 8 not in after["log_id"].tolist()
# without the log_id tie-break the choice between rows 2 and 3 (identical timestamps) is not defined
print("asserts passed: SQL delete (subquery) == SQL delete (CTE) == pandas drop_duplicates; kept log_ids", after["log_id"].tolist())
