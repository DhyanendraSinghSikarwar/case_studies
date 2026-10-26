# Q2: campaign coverage: merged ranges and distinct live days per advertiser.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE flights(advertiser_id INTEGER, campaign_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO flights VALUES
 (1,11,'2025-03-01','2025-03-10'),
 (1,12,'2025-03-03','2025-03-05'),   -- nested inside 11
 (1,13,'2025-03-08','2025-03-15'),   -- overlaps 11, extends it
 (1,14,'2025-03-20','2025-03-22'),   -- separate island
 (2,21,'2025-03-01','2025-03-10'),
 (2,22,'2025-03-11','2025-03-15'),   -- touches 21 (end 03-10, start 03-11)
 (2,23,'2025-03-17','2025-03-18'),   -- one-day gap (03-16) so not merged
 (3,31,'2025-04-01','2025-04-07');
""")

merged_sql = """
WITH o AS (
  SELECT *, MAX(end_date) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max_end
  FROM flights
), f AS (
  SELECT *, CASE WHEN prev_max_end IS NULL OR start_date > date(prev_max_end, '+1 day')
                 THEN 1 ELSE 0 END AS new_island
  FROM o
), g AS (
  SELECT *, SUM(new_island) OVER (PARTITION BY advertiser_id ORDER BY start_date, campaign_id) AS grp
  FROM f
)
SELECT advertiser_id, MIN(start_date) AS range_start, MAX(end_date) AS range_end,
       CAST(julianday(MAX(end_date)) - julianday(MIN(start_date)) AS INTEGER) + 1 AS days
FROM g
GROUP BY advertiser_id, grp
ORDER BY advertiser_id, range_start
"""
days_sql = """
WITH m AS (%s)
SELECT advertiser_id, SUM(days) AS live_days, COUNT(*) AS ranges FROM m GROUP BY advertiser_id ORDER BY advertiser_id
""" % merged_sql
naive_sql = """
SELECT advertiser_id, SUM(CAST(julianday(end_date) - julianday(start_date) AS INTEGER) + 1) AS naive_days
FROM flights GROUP BY advertiser_id ORDER BY advertiser_id
"""
strict_sql = merged_sql.replace("date(prev_max_end, '+1 day')", "prev_max_end")   # touching NOT merged (overlap only)

s_m = pd.read_sql(merged_sql, con)
s_d = pd.read_sql(days_sql, con)
print("SQL merged ranges (touching merged):"); print(s_m.to_string(index=False)); print()
print("SQL live days per advertiser:"); print(s_d.to_string(index=False)); print()
print("naive sum of campaign lengths (double counts overlaps):"); print(pd.read_sql(naive_sql, con).to_string(index=False)); print()
print("overlap-only rule (touching NOT merged), advertiser 2:")
print(pd.read_sql(strict_sql, con).query("advertiser_id == 2").to_string(index=False)); print()

# pandas
fl = pd.read_sql("SELECT * FROM flights", con, parse_dates=["start_date", "end_date"])
fl = fl.sort_values(["advertiser_id", "start_date", "campaign_id"]).reset_index(drop=True)
fl["prev_max_end"] = fl.groupby("advertiser_id")["end_date"].transform(lambda s: s.cummax().shift())
fl["new_island"] = (fl["prev_max_end"].isna() | (fl["start_date"] > fl["prev_max_end"] + pd.Timedelta(days=1))).astype(int)
fl["grp"] = fl.groupby("advertiser_id")["new_island"].cumsum()
p_m = (fl.groupby(["advertiser_id", "grp"], as_index=False)
         .agg(range_start=("start_date", "min"), range_end=("end_date", "max")))
p_m["days"] = (p_m["range_end"] - p_m["range_start"]).dt.days + 1
p_m = p_m.drop(columns="grp")
p_m["range_start"] = p_m["range_start"].dt.strftime("%Y-%m-%d")
p_m["range_end"] = p_m["range_end"].dt.strftime("%Y-%m-%d")
p_d = p_m.groupby("advertiser_id", as_index=False).agg(live_days=("days", "sum"), ranges=("days", "size"))
print("pandas merged ranges:"); print(p_m.to_string(index=False)); print()
print("pandas live days:"); print(p_d.to_string(index=False)); print()

pd.testing.assert_frame_equal(s_m, p_m, check_dtype=False)
pd.testing.assert_frame_equal(s_d, p_d, check_dtype=False)
print("asserts passed (compared in order advertiser_id, range_start)")
