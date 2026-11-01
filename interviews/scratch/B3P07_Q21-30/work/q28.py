# Q28: merge overlapping intervals per room: SQL running MAX vs pandas groupby cummax shifted; contained and touching cases
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE bookings(room_id INTEGER, start_ts TEXT, end_ts TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-01 13:00','2024-03-01 14:00'),
 (1,'2024-03-01 09:00','2024-03-01 12:00'),
 (1,'2024-03-01 10:00','2024-03-01 11:00'),
 (1,'2024-03-01 11:30','2024-03-01 12:30'),
 (1,'2024-03-01 12:30','2024-03-01 12:45'),
 (1,'2024-03-01 16:00','2024-03-01 17:00'),
 (1,'2024-03-01 16:00','2024-03-01 17:00'),
 (2,'2024-03-01 09:00','2024-03-01 10:00'),
 (2,'2024-03-01 10:00','2024-03-01 11:00'),
 (2,'2024-03-01 11:01','2024-03-01 12:00'),
 (3,'2024-03-01 08:00','2024-03-01 08:30'),
 (4,'2024-03-01 09:00',NULL),
 (4,'2024-03-01 10:00','2024-03-01 11:00');
"""
SQL_MAIN = """
WITH o AS (
  SELECT room_id, start_ts, end_ts,
         MAX(end_ts) OVER (
           PARTITION BY room_id ORDER BY start_ts, end_ts
           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max_end
  FROM bookings
  WHERE end_ts IS NOT NULL
), f AS (
  SELECT *, CASE WHEN prev_max_end IS NULL OR start_ts > prev_max_end THEN 1 ELSE 0 END AS new_block
  FROM o
), g AS (
  SELECT *, SUM(new_block) OVER (
           PARTITION BY room_id ORDER BY start_ts, end_ts
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block
  FROM f
)
SELECT room_id, MIN(start_ts) AS start_ts, MAX(end_ts) AS end_ts, COUNT(*) AS n_merged
FROM g
GROUP BY room_id, block
ORDER BY room_id, start_ts
"""
SQL_TOUCH_SEPARATE = SQL_MAIN.replace("start_ts > prev_max_end", "start_ts >= prev_max_end")
SQL_NAIVE_PREV = """
WITH o AS (
  SELECT room_id, start_ts, end_ts,
         LAG(end_ts) OVER (PARTITION BY room_id ORDER BY start_ts, end_ts) AS prev_end
  FROM bookings WHERE end_ts IS NOT NULL
), f AS (SELECT *, CASE WHEN prev_end IS NULL OR start_ts > prev_end THEN 1 ELSE 0 END AS new_block FROM o),
g AS (SELECT *, SUM(new_block) OVER (PARTITION BY room_id ORDER BY start_ts, end_ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block FROM f)
SELECT room_id, MIN(start_ts) AS start_ts, MAX(end_ts) AS end_ts, COUNT(*) AS n_merged
FROM g GROUP BY room_id, block ORDER BY room_id, start_ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL merged (touching merges, strict >):")
print(sql_df.to_string(index=False))
print("SQL with >= (touching stays separate), room 2 only:")
print(pd.read_sql_query(SQL_TOUCH_SEPARATE, con).query("room_id == 2").to_string(index=False))
print("wrong: LAG(end_ts) instead of the running MAX, room 1 (contained booking shrinks the end):")
print(pd.read_sql_query(SQL_NAIVE_PREV, con).query("room_id == 1").to_string(index=False))

bookings = pd.read_sql_query("SELECT * FROM bookings", con)
def merge_pandas(bookings, touching_merges=True):
    # pd:main
    b = bookings.dropna(subset=["end_ts"]).copy()
    b["start_ts"] = pd.to_datetime(b["start_ts"])
    b["end_ts"] = pd.to_datetime(b["end_ts"])
    b = b.sort_values(["room_id", "start_ts", "end_ts"]).reset_index(drop=True)
    prev_max_end = b.groupby("room_id")["end_ts"].cummax().groupby(b["room_id"]).shift()
    new_block = prev_max_end.isna() | (b["start_ts"] > prev_max_end)
    b["block"] = new_block.astype(int).groupby(b["room_id"]).cumsum()
    merged = (b.groupby(["room_id", "block"])
                .agg(start_ts=("start_ts", "min"), end_ts=("end_ts", "max"), n_merged=("start_ts", "size"))
                .reset_index().drop(columns="block"))
    # pd:end
    return merged
pd_df = merge_pandas(bookings)
shown = pd_df.assign(start_ts=pd_df["start_ts"].dt.strftime("%Y-%m-%d %H:%M"), end_ts=pd_df["end_ts"].dt.strftime("%Y-%m-%d %H:%M"))
print("pandas merged:")
print(shown.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), shown.reset_index(drop=True), check_dtype=False)  # both ordered by room_id, start_ts

# checks for the unverified list
print("cummax in groupby on datetimes dtype:", bookings.assign(e=pd.to_datetime(bookings["end_ts"])).groupby("room_id")["e"].cummax().dtype)
print("first row of each group after shift is NaT:", int(pd.Series(pd.to_datetime(["2024-01-01","2024-01-02"])).shift().isna().sum()))
# sort_values stability: default kind on a single key with ties versus kind='stable'
rng = np.random.default_rng(0)
df = pd.DataFrame({"k": rng.integers(0, 5, 2000), "i": np.arange(2000)})
default_order = df.sort_values("k")["i"].tolist()
stable_order = df.sort_values("k", kind="stable")["i"].tolist()
two_key_order = df.sort_values(["k", "i"])["i"].tolist()
print("single-key default sort equals stable sort on 2000 rows with ties:", default_order == stable_order)
print("two-key sort equals stable sort:", two_key_order == stable_order)
print("asserts passed")
