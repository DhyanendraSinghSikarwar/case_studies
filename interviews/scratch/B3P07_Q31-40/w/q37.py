# Q37: coverage and uncovered gaps in a 09:00-18:00 window, SQL + pandas
import sqlite3
import pandas as pd

WSTART, WEND = "2024-03-04 09:00", "2024-03-04 18:00"
SCHEMA = """
CREATE TABLE shifts(guard_id TEXT, start_ts TEXT, end_ts TEXT);
INSERT INTO shifts VALUES
 ('g2','2024-03-04 10:00','2024-03-04 12:00'),
 ('g1','2024-03-04 08:00','2024-03-04 11:00'),
 ('g4','2024-03-04 12:00','2024-03-04 13:00'),
 ('g3','2024-03-04 11:30','2024-03-04 11:45'),
 ('g5','2024-03-04 14:00','2024-03-04 15:00'),
 ('g5','2024-03-04 14:00','2024-03-04 15:00'),
 ('g6','2024-03-04 16:00','2024-03-04 19:00'),
 ('g7','2024-03-04 06:00','2024-03-04 08:30'),
 ('g8','2024-03-04 17:00',NULL);
"""
SQL_MAIN = """
WITH w AS (SELECT :ws AS ws, :we AS we),
clipped AS (
  SELECT MAX(s.start_ts, w.ws) AS st, MIN(s.end_ts, w.we) AS en
  FROM shifts s, w
  WHERE s.start_ts IS NOT NULL AND s.end_ts IS NOT NULL
),
pieces AS (
  SELECT st, en FROM clipped WHERE st < en
  UNION ALL SELECT ws, ws FROM w
  UNION ALL SELECT we, we FROM w
),
ordered AS (
  SELECT st, en,
         MAX(en) OVER (ORDER BY st, en ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM pieces
),
flagged AS (
  SELECT st, en,
         SUM(CASE WHEN prev_max IS NULL OR st > prev_max THEN 1 ELSE 0 END)
             OVER (ORDER BY st, en) AS blk
  FROM ordered
),
merged AS (
  SELECT MIN(st) AS b_start, MAX(en) AS b_end FROM flagged GROUP BY blk
),
nxt AS (
  SELECT b_end AS gap_start, LEAD(b_start) OVER (ORDER BY b_start) AS gap_end FROM merged
)
SELECT gap_start, gap_end,
       CAST((unixepoch(gap_end) - unixepoch(gap_start)) / 60 AS INTEGER) AS minutes
FROM nxt
WHERE gap_end > gap_start
ORDER BY gap_start
"""
SQL_SUMMARY = """
WITH g AS (""" + SQL_MAIN.replace("ORDER BY gap_start\n", "\n") + """)
SELECT CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) AS window_minutes,
       COALESCE(SUM(minutes), 0) AS uncovered_minutes,
       CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) - COALESCE(SUM(minutes), 0) AS covered_minutes,
       ROUND(100.0 * (CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER) - COALESCE(SUM(minutes), 0))
             / (CAST((unixepoch(:we) - unixepoch(:ws)) / 60 AS INTEGER)), 1) AS coverage_pct
FROM g
"""
params = {"ws": WSTART, "we": WEND}
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_gaps = pd.read_sql_query(SQL_MAIN, con, params=params)
sql_sum = pd.read_sql_query(SQL_SUMMARY, con, params=params)
print("SQL gaps:"); print(sql_gaps.to_string(index=False))
print("SQL summary:"); print(sql_sum.to_string(index=False))

shifts = pd.read_sql_query("SELECT * FROM shifts", con)
# pd:main
def coverage(shifts, ws, we):
    ws, we = pd.Timestamp(ws), pd.Timestamp(we)
    x = shifts.dropna().copy()
    x["st"] = pd.to_datetime(x["start_ts"]).clip(lower=ws)
    x["en"] = pd.to_datetime(x["end_ts"]).clip(upper=we)
    x = x[x["st"] < x["en"]][["st", "en"]]
    x = pd.concat([x, pd.DataFrame({"st": [ws, we], "en": [ws, we]})]).sort_values(["st", "en"]).reset_index(drop=True)
    prev_max = x["en"].cummax().shift()
    x["blk"] = ((prev_max.isna()) | (x["st"] > prev_max)).cumsum()
    m = x.groupby("blk").agg(b_start=("st", "min"), b_end=("en", "max"))
    gaps = pd.DataFrame({"gap_start": m["b_end"], "gap_end": m["b_start"].shift(-1)}).dropna()
    gaps = gaps[gaps["gap_end"] > gaps["gap_start"]].reset_index(drop=True)
    gaps["minutes"] = ((gaps["gap_end"] - gaps["gap_start"]).dt.total_seconds() / 60).astype(int)
    total = int((we - ws).total_seconds() / 60)
    unc = int(gaps["minutes"].sum())
    return gaps, (total, unc, total - unc, round(100.0 * (total - unc) / total, 1))
# pd:end
pd_gaps, pd_sum = coverage(shifts, WSTART, WEND)
out = pd_gaps.assign(gap_start=pd_gaps["gap_start"].dt.strftime("%Y-%m-%d %H:%M"),
                     gap_end=pd_gaps["gap_end"].dt.strftime("%Y-%m-%d %H:%M"))
print("pandas gaps:"); print(out.to_string(index=False))
print("pandas summary:", pd_sum)
# compare after sorting by gap_start
assert out.astype({"minutes": "int64"}).equals(sql_gaps.astype({"minutes": "int64"}))
assert pd_sum == tuple(sql_sum.iloc[0].tolist())

print("--- edge cases ---")
con.execute("DELETE FROM shifts")
print("no shifts, SQL:", pd.read_sql_query(SQL_MAIN, con, params=params).values.tolist(),
      pd.read_sql_query(SQL_SUMMARY, con, params=params).values.tolist())
print("no shifts, pandas:", coverage(shifts.iloc[0:0], WSTART, WEND)[1])
con.execute("INSERT INTO shifts VALUES ('x','2024-03-04 06:00','2024-03-04 08:30'),('y','2024-03-04 18:00','2024-03-04 20:00')")
print("only shifts outside the window, SQL:", pd.read_sql_query(SQL_MAIN, con, params=params).values.tolist())
con.execute("DELETE FROM shifts")
con.execute("INSERT INTO shifts VALUES ('z','2024-03-04 08:00','2024-03-04 19:00')")
print("one shift covering everything, SQL gaps:", pd.read_sql_query(SQL_MAIN, con, params=params).values.tolist(),
      pd.read_sql_query(SQL_SUMMARY, con, params=params).values.tolist())
print("asserts passed")
