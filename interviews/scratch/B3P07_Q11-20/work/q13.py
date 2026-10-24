# Q13: consecutive same-status runs: LAG flag + running SUM, ROW_NUMBER difference, pandas, itertools.groupby
import sqlite3
import itertools
import pandas as pd

SCHEMA = """
CREATE TABLE status_log(entity_id INTEGER, ts TEXT, status TEXT);
INSERT INTO status_log VALUES
 (1,'2024-03-01 00:05:00','ok'),
 (1,'2024-03-01 00:00:00','ok'),
 (1,'2024-03-01 00:10:00','down'),
 (1,'2024-03-01 00:15:00','down'),
 (1,'2024-03-01 00:20:00','down'),
 (1,'2024-03-01 00:25:00','ok'),
 (2,'2024-03-01 00:00:00','down'),
 (3,'2024-03-01 00:00:00','ok'),
 (3,'2024-03-01 00:05:00',NULL),
 (3,'2024-03-01 00:10:00',NULL),
 (3,'2024-03-01 00:15:00','ok');
"""
SQL_MAIN = """
WITH f AS (
  SELECT entity_id, ts, status,
         CASE WHEN LAG(ts) OVER w IS NULL OR status IS NOT LAG(status) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM status_log
  WINDOW w AS (PARTITION BY entity_id ORDER BY ts)
), g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY entity_id ORDER BY ts) AS run_id
  FROM f
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM g
GROUP BY entity_id, run_id, status
ORDER BY entity_id, run_start
"""
SQL_RN = """
WITH r AS (
  SELECT entity_id, ts, status,
         ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
       - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
  FROM status_log
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM r
GROUP BY entity_id, status, grp
ORDER BY entity_id, run_start
"""
# wrong: <> instead of IS NOT (NULL comparison is NULL, so CASE falls to ELSE 0)
SQL_WRONG = SQL_MAIN.replace("status IS NOT LAG(status) OVER w", "status <> LAG(status) OVER w")
assert SQL_WRONG != SQL_MAIN
SQL_GRP = """
SELECT entity_id, ts, status,
       ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts) AS rn_all,
       ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS rn_status,
       ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
     - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
FROM status_log WHERE entity_id = 1 ORDER BY ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_RN, con)
w = pd.read_sql_query(SQL_WRONG, con)
print("LAG + running SUM:"); print(a.to_string(index=False))
print("ROW_NUMBER difference, entity 1 detail:"); print(pd.read_sql_query(SQL_GRP, con).to_string(index=False))
pd.testing.assert_frame_equal(a, b)
print("two SQL methods equal (ordered by entity_id, run_start): True")
print("wrong version with <> (NULL status rows vanish from the flag):"); print(w.to_string(index=False))

log = pd.read_sql_query("SELECT * FROM status_log", con)
# pd:main
d = log.sort_values(["entity_id", "ts"], kind="stable").copy()
prev = d.groupby("entity_id")["status"].shift()
first = d.groupby("entity_id").cumcount() == 0
same = (d["status"] == prev) | (d["status"].isna() & prev.isna())
d["run_id"] = (first | ~same).astype(int).groupby(d["entity_id"]).cumsum()
runs = (d.groupby(["entity_id", "run_id"], as_index=False, dropna=False)
          .agg(status=("status", "first"), run_start=("ts", "min"), run_end=("ts", "max"),
               n_rows=("ts", "size")))
runs = runs[["entity_id", "status", "run_start", "run_end", "n_rows"]]
# pd:end
pd.testing.assert_frame_equal(runs.reset_index(drop=True), a.assign(status=a["status"]), check_dtype=False)
print("pandas equals SQL (ordered by entity_id, run_start): True")
naive = (d["status"] != prev) | first
print("naive pandas (s != s.shift()) runs for entity 3:",
      int(naive[d.entity_id == 3].sum()), "(correct: 3 runs, NaN != NaN is True so each NULL row is its own run)")

# itertools.groupby run lengths for entity 1, as a cross-check
e1 = d[d.entity_id == 1]["status"].tolist()
ig = [(k, len(list(g))) for k, g in itertools.groupby(e1)]
print("itertools.groupby entity 1:", ig)
assert ig == list(zip(a[a.entity_id == 1].status, a[a.entity_id == 1].n_rows))
# duplicated ts in the same entity changes the answer unless a tie-breaker exists: show the guard
con.execute("INSERT INTO status_log VALUES (2,'2024-03-01 00:00:00','ok')")
dup = pd.read_sql_query("SELECT entity_id, ts, COUNT(*) c FROM status_log GROUP BY entity_id, ts HAVING c > 1", con)
print("duplicate (entity_id, ts) keys after inserting one extra row:"); print(dup.to_string(index=False))
d2 = pd.read_sql_query(SQL_MAIN, con)
r2 = pd.read_sql_query(SQL_RN, con)
print("entity 2 after the tied row, LAG method:"); print(d2[d2.entity_id == 2].to_string(index=False))
print("entity 2 after the tied row, ROW_NUMBER method:"); print(r2[r2.entity_id == 2].to_string(index=False))
print("asserts passed")
