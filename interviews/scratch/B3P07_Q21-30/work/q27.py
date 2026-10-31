# Q27: state-change detection with NULL states: IS NOT / IS DISTINCT FROM versus != ; pandas NaN != NaN
import itertools
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE sensor_state(device_id INTEGER, ts TEXT, state TEXT);
INSERT INTO sensor_state VALUES
 (1,'2024-03-01 00:03:00','on'),
 (1,'2024-03-01 00:00:00','on'),
 (1,'2024-03-01 00:01:00','on'),
 (1,'2024-03-01 00:02:00','off'),
 (1,'2024-03-01 00:04:00','off'),
 (2,'2024-03-01 00:00:00',NULL),
 (2,'2024-03-01 00:01:00',NULL),
 (2,'2024-03-01 00:02:00','on'),
 (2,'2024-03-01 00:03:00',NULL),
 (2,'2024-03-01 00:04:00','on'),
 (3,'2024-03-01 00:00:00','off'),
 (4,'2024-03-01 00:00:00',NULL);
"""
SQL_MAIN = """
WITH x AS (
  SELECT device_id, ts, state,
         ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY ts) AS rn,
         LAG(state) OVER (PARTITION BY device_id ORDER BY ts) AS prev_state
  FROM sensor_state
)
SELECT device_id, ts, prev_state, state,
       CASE WHEN rn = 1 THEN 'first row' ELSE 'transition' END AS kind
FROM x
WHERE rn = 1 OR state IS NOT prev_state
ORDER BY device_id, ts
"""
SQL_NEQ = """
WITH x AS (
  SELECT device_id, ts, state, LAG(state) OVER (PARTITION BY device_id ORDER BY ts) AS prev_state
  FROM sensor_state
)
SELECT device_id, ts, prev_state, state FROM x WHERE state != prev_state ORDER BY device_id, ts
"""
SQL_DISTINCT_FROM = """
WITH x AS (
  SELECT device_id, ts, state,
         ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY ts) AS rn,
         LAG(state) OVER (PARTITION BY device_id ORDER BY ts) AS prev_state
  FROM sensor_state
)
SELECT device_id, ts, prev_state, state,
       CASE WHEN rn = 1 THEN 'first row' ELSE 'transition' END AS kind
FROM x
WHERE rn = 1 OR state IS DISTINCT FROM prev_state
ORDER BY device_id, ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer (IS NOT):")
print(sql_df.to_string(index=False))
dist = pd.read_sql_query(SQL_DISTINCT_FROM, con)
assert dist.equals(sql_df)
print("IS DISTINCT FROM on SQLite 3.45.1 gives the same rows:", dist.equals(sql_df))
print("probes NULL != NULL, NULL IS NOT NULL, NULL IS DISTINCT FROM NULL, 1 IS NOT NULL:",
      con.execute("SELECT NULL != NULL, NULL IS NOT NULL, NULL IS DISTINCT FROM NULL, 1 IS NOT NULL").fetchone())
print("wrong: != (first rows and everything touching a NULL vanish):")
print(pd.read_sql_query(SQL_NEQ, con).to_string(index=False))

sensor = pd.read_sql_query("SELECT * FROM sensor_state", con)
# pd:main
s = sensor.sort_values(["device_id", "ts"]).reset_index(drop=True)
prev = s.groupby("device_id")["state"].shift()
first_row = s.groupby("device_id").cumcount().eq(0)
differs = s["state"].ne(prev) & ~(s["state"].isna() & prev.isna())
out = s[first_row | differs].copy()
out["prev_state"] = prev[out.index]
out["kind"] = np.where(first_row[out.index], "first row", "transition")
pd_df = out[["device_id", "ts", "prev_state", "state", "kind"]].reset_index(drop=True)
# pd:end
print("pandas answer:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df, check_dtype=False)  # both ordered by device_id, ts

naive = s[first_row | s["state"].ne(prev)]
print("naive pandas ne(shift) rows per device:", naive.groupby("device_id").size().to_dict(), "vs correct", pd_df.groupby("device_id").size().to_dict())
print("NaN != NaN:", np.nan != np.nan, "; Series ne:", pd.Series([np.nan]).ne(pd.Series([np.nan])).tolist())
print("groupby drops NaN keys:", s.groupby("state")["device_id"].size().to_dict(), "; with dropna=False:", s.groupby("state", dropna=False)["device_id"].size().to_dict())
# itertools.groupby run lengths: identity shortcut for the same NaN object, distinct objects are not equal
same_obj = [len(list(g)) for _, g in itertools.groupby([np.nan, np.nan, np.nan])]
list_of_floats = [float("nan"), float("nan"), float("nan")]
diff_obj = [len(list(g)) for _, g in itertools.groupby(list_of_floats)]
from_series = [len(list(g)) for _, g in itertools.groupby(pd.Series([np.nan, np.nan, np.nan]).tolist())]
print("itertools.groupby NaN run lengths: same object", same_obj, "; separate float objects", diff_obj, "; from Series.tolist()", from_series)
print("asserts passed")
