# Q30: booking conflicts via self join; half-open overlap test; touching vs inclusive end dates; containment
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE bookings(booking_id INTEGER, room_id INTEGER, start_ts TEXT, end_ts TEXT);
INSERT INTO bookings VALUES
 (5,1,'2024-03-01 12:00','2024-03-01 13:00'),
 (1,1,'2024-03-01 09:00','2024-03-01 11:00'),
 (2,1,'2024-03-01 11:00','2024-03-01 12:00'),
 (3,1,'2024-03-01 09:30','2024-03-01 10:00'),
 (4,1,'2024-03-01 10:30','2024-03-01 11:30'),
 (6,2,'2024-03-01 09:00','2024-03-01 10:00'),
 (7,2,'2024-03-01 09:00','2024-03-01 10:00'),
 (8,3,'2024-03-01 09:00','2024-03-01 10:00'),
 (9,1,'2024-03-01 14:00',NULL);
CREATE TABLE stays(booking_id INTEGER, room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO stays VALUES (1,1,'2024-03-01','2024-03-03'),(2,1,'2024-03-03','2024-03-05'),(3,1,'2024-03-06','2024-03-07');
"""
SQL_MAIN = """
SELECT a.booking_id AS booking_a, b.booking_id AS booking_b, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_ts < b.end_ts
 AND b.start_ts < a.end_ts
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
SQL_NO_ORDER = """
SELECT a.booking_id AS booking_a, b.booking_id AS booking_b
FROM bookings a JOIN bookings b
  ON a.room_id = b.room_id AND a.start_ts < b.end_ts AND b.start_ts < a.end_ts
ORDER BY a.booking_id, b.booking_id
"""
SQL_INCLUSIVE_TS = """
SELECT a.booking_id AS booking_a, b.booking_id AS booking_b
FROM bookings a JOIN bookings b
  ON a.room_id = b.room_id AND a.start_ts <= b.end_ts AND b.start_ts <= a.end_ts AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
# stays use an inclusive end date: both the first and the last night are occupied
SQL_STAYS_INCLUSIVE = """
SELECT a.booking_id AS stay_a, b.booking_id AS stay_b
FROM stays a JOIN stays b
  ON a.room_id = b.room_id AND a.start_date <= b.end_date AND b.start_date <= a.end_date AND a.booking_id < b.booking_id
ORDER BY 1, 2
"""
SQL_STAYS_HALFOPEN_WRONG = """
SELECT a.booking_id AS stay_a, b.booking_id AS stay_b
FROM stays a JOIN stays b
  ON a.room_id = b.room_id AND a.start_date < b.end_date AND b.start_date < a.end_date AND a.booking_id < b.booking_id
ORDER BY 1, 2
"""
SQL_STAYS_NORMALISED = """
SELECT a.booking_id AS stay_a, b.booking_id AS stay_b
FROM stays a JOIN stays b
  ON a.room_id = b.room_id
 AND a.start_date < date(b.end_date, '+1 day')
 AND b.start_date < date(a.end_date, '+1 day')
 AND a.booking_id < b.booking_id
ORDER BY 1, 2
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL conflicts (half-open [start, end)):")
print(sql_df.to_string(index=False))
nb = pd.read_sql_query(SQL_NO_ORDER, con)
print("without a.booking_id < b.booking_id:", len(nb), "rows instead of", len(sql_df), "(self pairs and mirrored pairs)")
print(nb.head(8).to_string(index=False))
print("wrong: inclusive timestamp test <=, bookings 1 and 2 now collide:")
print(pd.read_sql_query(SQL_INCLUSIVE_TS, con).to_string(index=False))
print("stays with INCLUSIVE end dates, inclusive test (correct for that convention):")
print(pd.read_sql_query(SQL_STAYS_INCLUSIVE, con).to_string(index=False))
print("same stays with the half-open test (misses the shared 2024-03-03):")
print(pd.read_sql_query(SQL_STAYS_HALFOPEN_WRONG, con).to_string(index=False))
print("same stays normalised to half-open with date(end, '+1 day'):")
print(pd.read_sql_query(SQL_STAYS_NORMALISED, con).to_string(index=False))

bookings = pd.read_sql_query("SELECT * FROM bookings", con)
# pd:main
b = bookings.copy()
b["start_ts"] = pd.to_datetime(b["start_ts"])
b["end_ts"] = pd.to_datetime(b["end_ts"])
m = b.merge(b, on="room_id", suffixes=("_a", "_b"))
hit = m[(m["start_ts_a"] < m["end_ts_b"]) & (m["start_ts_b"] < m["end_ts_a"]) & (m["booking_id_a"] < m["booking_id_b"])]
pd_df = (hit[["booking_id_a", "booking_id_b", "room_id"]]
         .rename(columns={"booking_id_a": "booking_a", "booking_id_b": "booking_b"})
         .sort_values(["booking_a", "booking_b"]).reset_index(drop=True))
# pd:end
print("pandas conflicts:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df, check_dtype=False)  # both ordered by booking_a, booking_b
print("NaT comparisons are False, so booking 9 (NULL end) never conflicts:", 9 not in set(pd_df["booking_a"]) | set(pd_df["booking_b"]))
print("asserts passed")
