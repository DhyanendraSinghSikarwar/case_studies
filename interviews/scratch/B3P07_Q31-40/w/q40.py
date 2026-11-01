# Q40: room availability islands (>= 3 consecutive free hours), SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE slots(room_id TEXT, slot_start TEXT, is_free INTEGER);
INSERT INTO slots VALUES
 ('R1','2024-03-04 09:00',1),('R1','2024-03-04 10:00',1),('R1','2024-03-04 11:00',1),('R1','2024-03-04 11:00',1),
 ('R1','2024-03-04 12:00',0),
 ('R1','2024-03-04 13:00',1),('R1','2024-03-04 14:00',1),
 ('R1','2024-03-04 16:00',1),('R1','2024-03-04 17:00',1),('R1','2024-03-04 18:00',1),
 ('R2','2024-03-04 23:00',1),('R2','2024-03-05 00:00',1),('R2','2024-03-05 01:00',1),('R2','2024-03-04 22:00',1),
 ('R3','2024-03-04 09:00',1),
 ('R4','2024-03-04 09:00',1),('R4','2024-03-04 10:00',1),('R4','2024-03-04 11:00',1),('R4','2024-03-04 12:00',0),
 ('R4','2024-03-04 13:00',1),('R4','2024-03-04 14:00',1),
 ('R5','2024-03-04 09:00',1),('R5','2024-03-04 10:00',NULL),('R5','2024-03-04 11:00',1),('R5','2024-03-04 12:00',1),
 ('R6','2024-03-04 09:00',1),('R6','2024-03-04 10:00',1),('R6','2024-03-04 10:00',0),('R6','2024-03-04 11:00',1),('R6','2024-03-04 12:00',1);
"""
BASE = """
WITH s AS (
  SELECT room_id, slot_start, MIN(is_free) AS is_free
  FROM slots GROUP BY room_id, slot_start
),
h AS (
  SELECT room_id, slot_start, is_free,
         CAST(ROUND(julianday(slot_start) * 24) AS INTEGER) AS hr
  FROM s
)
"""
SQL_MAIN = BASE + """,
f AS (
  SELECT room_id, slot_start, hr,
         hr - ROW_NUMBER() OVER (PARTITION BY room_id ORDER BY hr) AS k
  FROM h WHERE is_free = 1
)
SELECT room_id, MIN(slot_start) AS free_from,
       datetime(MAX(slot_start), '+1 hour') AS free_to, COUNT(*) AS hours
FROM f
GROUP BY room_id, k
HAVING COUNT(*) >= 3
ORDER BY room_id, free_from
"""
SQL_LAG = BASE + """,
l AS (
  SELECT room_id, slot_start, is_free, hr,
         LAG(is_free) OVER w AS pf, LAG(hr) OVER w AS ph
  FROM h WINDOW w AS (PARTITION BY room_id ORDER BY hr)
),
g AS (
  SELECT *, SUM(CASE WHEN is_free = 1 AND pf = 1 AND hr - ph = 1 THEN 0 ELSE 1 END)
            OVER (PARTITION BY room_id ORDER BY hr) AS grp
  FROM l
)
SELECT room_id, MIN(slot_start) AS free_from,
       datetime(MAX(slot_start), '+1 hour') AS free_to, COUNT(*) AS hours
FROM g
WHERE is_free = 1
GROUP BY room_id, grp
HAVING COUNT(*) >= 3
ORDER BY room_id, free_from
"""
SQL_ROWORDER = """
WITH s AS (SELECT room_id, slot_start, MIN(is_free) AS is_free FROM slots GROUP BY room_id, slot_start),
f AS (
  SELECT room_id, slot_start,
         ROW_NUMBER() OVER (PARTITION BY room_id ORDER BY slot_start) AS rn_all
  FROM s
),
t AS (
  SELECT s.room_id, s.slot_start, f.rn_all,
         ROW_NUMBER() OVER (PARTITION BY s.room_id ORDER BY s.slot_start) AS rn_free
  FROM s JOIN f USING (room_id, slot_start) WHERE s.is_free = 1
)
SELECT room_id, MIN(slot_start) AS free_from, COUNT(*) AS hours
FROM t GROUP BY room_id, rn_all - rn_free HAVING COUNT(*) >= 3 ORDER BY room_id, free_from
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
lag_df = pd.read_sql_query(SQL_LAG, con)
print("SQL filtered ROW_NUMBER difference:"); print(sql_df.to_string(index=False))
assert sql_df.equals(lag_df)
print("SQL LAG-flag on all rows gives the same rows: True")
print("wrong, row order instead of hour number (R1 merges across the missing 15:00 row):")
print(pd.read_sql_query(SQL_ROWORDER, con).to_string(index=False))

slots = pd.read_sql_query("SELECT * FROM slots", con)
# pd:main
s = slots.groupby(["room_id", "slot_start"], as_index=False)["is_free"].min()   # MIN skips NaN like SQL
t = pd.to_datetime(s["slot_start"])
s["hr"] = (t - pd.Timestamp("1970-01-01")) // pd.Timedelta(hours=1)
f = s[s["is_free"] == 1].sort_values(["room_id", "hr"]).copy()
f["k"] = f["hr"] - f.groupby("room_id").cumcount()
pd_df = (f.groupby(["room_id", "k"])
          .agg(free_from=("slot_start", "min"), last=("slot_start", "max"), hours=("hr", "size"))
          .reset_index())
pd_df = pd_df[pd_df["hours"] >= 3].copy()
pd_df["free_to"] = (pd.to_datetime(pd_df["last"]) + pd.Timedelta(hours=1)).dt.strftime("%Y-%m-%d %H:%M:%S")
pd_df = pd_df[["room_id", "free_from", "free_to", "hours"]].sort_values(["room_id", "free_from"]).reset_index(drop=True)
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
# compare after sorting by room_id, free_from
assert pd_df.astype({"hours": "int64"}).equals(sql_df.astype({"hours": "int64"}))

# julianday precision test: does CAST(julianday * 24 AS INTEGER) truncate wrongly where ROUND does not?
con.execute("""
CREATE TABLE hrs AS
WITH RECURSIVE x(ts) AS (
  SELECT '2020-01-01 00:00' UNION ALL SELECT strftime('%Y-%m-%d %H:%M', ts, '+1 hour') FROM x WHERE ts < '2030-12-31 23:00'
) SELECT ts FROM x
""")
row = con.execute("""
SELECT COUNT(*), SUM(CAST(julianday(ts) * 24 AS INTEGER) <> CAST(ROUND(julianday(ts) * 24) AS INTEGER)) FROM hrs
""").fetchone()
# offset between the two day-number systems is constant: julianday(1970-01-01) * 24
off = con.execute("SELECT CAST(ROUND(julianday('1970-01-01') * 24) AS INTEGER)").fetchone()[0]
mism = con.execute("SELECT COUNT(*) FROM hrs WHERE CAST(ROUND(julianday(ts) * 24) AS INTEGER) - unixepoch(ts) / 3600 <> ?", (off,)).fetchone()[0]
print("hourly stamps 2020-2030:", row[0], "| CAST truncation differs from ROUND:", row[1],
      "| ROUND(julianday*24) minus unixepoch/3600 not constant:", mism)

# the same test one level finer: minute stamps in 2024, julianday * 1440 truncated versus rounded
con.execute("""
CREATE TABLE mins AS
WITH RECURSIVE x(ts) AS (
  SELECT '2024-01-01 00:00' UNION ALL SELECT strftime('%Y-%m-%d %H:%M', ts, '+1 minute') FROM x WHERE ts < '2024-12-31 23:59'
) SELECT ts FROM x
""")
m = con.execute("""
SELECT COUNT(*), SUM(CAST(julianday(ts) * 1440 AS INTEGER) <> CAST(ROUND(julianday(ts) * 1440) AS INTEGER)),
       SUM(ABS(julianday(ts) * 1440 - ROUND(julianday(ts) * 1440)) > 0.001)
FROM mins
""").fetchone()
print("minute stamps in 2024:", m[0], "| truncation differs from ROUND:", m[1], "| off by more than 0.001 minute:", m[2])

print("--- edge cases ---")
for name, ins in [("empty table", ""), ("one free slot", "('Z','2024-03-04 09:00',1)"),
                  ("exactly 2 free", "('Z','2024-03-04 09:00',1),('Z','2024-03-04 10:00',1)"),
                  ("exactly 3 free", "('Z','2024-03-04 09:00',1),('Z','2024-03-04 10:00',1),('Z','2024-03-04 11:00',1)")]:
    con.execute("DELETE FROM slots")
    if ins:
        con.execute("INSERT INTO slots VALUES " + ins)
    print(name, "->", con.execute(SQL_MAIN).fetchall())
print("asserts passed")
