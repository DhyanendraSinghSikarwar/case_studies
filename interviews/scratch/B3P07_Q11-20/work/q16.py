# Q16: merge overlapping inclusive date ranges: running MAX(end) over previous rows, flag, running SUM
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE bookings(room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-09','2024-03-10'),
 (1,'2024-03-05','2024-03-08'),
 (1,'2024-03-01','2024-03-05'),
 (1,'2024-03-02','2024-03-03'),
 (1,'2024-03-15','2024-03-16'),
 (2,'2024-03-01','2024-03-01'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-11',NULL),
 (3,'2024-03-20','2024-03-18'),
 (4,'2024-03-01','2024-03-03'),
 (4,'2024-03-01','2024-03-10');
"""
SQL_MAIN = """
WITH b AS (
  SELECT room_id, start_date, end_date
  FROM bookings
  WHERE start_date IS NOT NULL AND end_date IS NOT NULL AND end_date >= start_date
), m AS (
  SELECT room_id, start_date, end_date,
         MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM b
), f AS (
  SELECT *, CASE WHEN prev_max IS NULL OR start_date > prev_max THEN 1 ELSE 0 END AS new_block
  FROM m
), g AS (
  SELECT *, SUM(new_block) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block_id
  FROM f
)
SELECT room_id, MIN(start_date) AS block_start, MAX(end_date) AS block_end
FROM g
GROUP BY room_id, block_id
ORDER BY room_id, block_start
"""
# rule B: ranges one day apart (end 03-10, next start 03-11) also merge
SQL_ADJ = SQL_MAIN.replace("start_date > prev_max", "start_date > date(prev_max, '+1 day')")
assert SQL_ADJ != SQL_MAIN
# wrong: compare with the previous row's end (LAG) instead of the running max
SQL_LAG = SQL_MAIN.replace(
    """MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)""",
    "LAG(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date)")
assert SQL_LAG != SQL_MAIN
# NULL end_date read as open-ended instead of excluded
SQL_OPEN = SQL_MAIN.replace("end_date IS NOT NULL AND end_date >= start_date", "1 = 1") \
                   .replace("end_date\n  FROM bookings", "COALESCE(end_date, '9999-12-31') AS end_date\n  FROM bookings")
assert SQL_OPEN != SQL_MAIN
SQL_DETAIL = """
SELECT room_id, start_date, end_date,
       MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
FROM bookings WHERE room_id = 1 ORDER BY start_date, end_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("room 1 running max of the previous rows' end_date:"); print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
print("rule A, merge when start <= running max end (touching merges, one day apart does not):"); print(a.to_string(index=False))
b = pd.read_sql_query(SQL_ADJ, con)
print("rule B, also merge ranges one day apart:"); print(b.to_string(index=False))
print("wrong, LAG(end_date) instead of running max, room 1 and 4:")
print(pd.read_sql_query(SQL_LAG, con).query("room_id in (1, 4)").to_string(index=False))
print("NULL end_date treated as open-ended (room 3):")
print(pd.read_sql_query(SQL_OPEN, con).query("room_id == 3").to_string(index=False))

bookings = pd.read_sql_query("SELECT * FROM bookings", con)

def merge_ranges(bookings, adjacent=False):
    # pd:main
    d = bookings.dropna(subset=["start_date", "end_date"]).copy()
    d["start_date"] = pd.to_datetime(d["start_date"])
    d["end_date"] = pd.to_datetime(d["end_date"])
    d = d[d["end_date"] >= d["start_date"]].sort_values(["room_id", "start_date", "end_date"])
    prev_max = d.groupby("room_id")["end_date"].cummax().groupby(d["room_id"]).shift()
    slack = pd.Timedelta(days=1) if adjacent else pd.Timedelta(0)
    new_block = prev_max.isna() | (d["start_date"] > prev_max + slack)
    d["block_id"] = new_block.astype(int).groupby(d["room_id"]).cumsum()
    out = d.groupby(["room_id", "block_id"], as_index=False).agg(
        block_start=("start_date", "min"), block_end=("end_date", "max"))
    # pd:end
    out = out.drop(columns="block_id")
    for c in ("block_start", "block_end"):
        out[c] = out[c].dt.strftime("%Y-%m-%d")
    return out.sort_values(["room_id", "block_start"]).reset_index(drop=True)

pd.testing.assert_frame_equal(merge_ranges(bookings, False), a, check_dtype=False)   # ordered by room_id, block_start
pd.testing.assert_frame_equal(merge_ranges(bookings, True), b, check_dtype=False)
print("pandas equals SQL for both rules (ordered by room_id, block_start): True")
print("asserts passed")
